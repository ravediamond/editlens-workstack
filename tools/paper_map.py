#!/usr/bin/env python3
"""WS-162: paper AI map. Scores the sections of the owner's research papers with Pangram's open EditLens 3B detector
(pangram/editlens_Llama-3.2-3B on meta-llama/Llama-3.2-3B, CC BY-NC-SA 4.0, non-commercial) so the OWNER can rewrite the
sections that read as AI by hand.

    python tools/paper_map.py <paper-repo-dir | file.md | file.md.in | file.pdf> [--pdf FILE] [--refs DIR] [--out DIR]

Needs results/WS-162.md for the facts behind the model use (score decoding, preprocessing, thresholds)."""
import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import prose_check as P  # noqa: E402  (the same prose extractor as the gate; no second one)

ALLOWED = [ROOT / "papers", ROOT / "editlens-paper", ROOT / "results", Path(os.environ.get("EDITLENS_REFS") or ROOT / "refs")]  # the owner's own papers, their results, and the human reference PDFs (EDITLENS_REFS)
REFUSAL = "paper_map is for research papers only (CC BY-NC-SA, non-commercial)"
BASE, ADAPTER = "meta-llama/Llama-3.2-3B", "pangram/editlens_Llama-3.2-3B"
MAX_TOKENS, MIN_WORDS, MAX_LENGTH = 900, 40, 1024  # chunk cap under the model's 1024; shorter chunks merge into a neighbour
CAPTION = re.compile(r"^(Table|Fig\.?|Figure)\s+\d+\s*[:.—–-]")


def fence(path, explicit_pdf=False):
    p = Path(path).resolve()
    if p.suffix == ".pdf" and explicit_pdf:
        return p
    if not any(p == a or a in p.parents for a in ALLOWED):
        raise SystemExit(REFUSAL)
    return p


# ------------------------------------------------------------------------------------------------ text as the model sees it
def clean_text(text):
    """pangramlabs/EditLens scripts/preprocess.py clean_text: demojize, drop a </think> prefix, drop a first paragraph that
    starts like an assistant preface (Sure, Here, Abstract, Title, ...), lower-case, collapse whitespace."""
    try:
        import emoji
        text = emoji.demojize(text)
    except ImportError:
        pass
    if "</think>" in text:
        text = text.split("</think>")[1].strip()
    paras = [p for p in text.split("\n") if p.strip()]
    if paras:
        first = re.sub(r"^[^a-zA-Z0-9]*", "", paras[0])
        if any(first.startswith(s) for s in ("Sure", "Here", "Abstract", "Title", "I'm happy to help", "Certainly")) and len(paras) > 1:
            text = "\n".join(paras[1:])
    return re.sub(r"\s+", " ", text.lower()).strip()


def strip_cites(t):
    t = re.sub(r"\[@[^\]]+\]", "", t)
    t = re.sub(r"\\cite[a-z]*\{[^}]*\}", "", t)
    return re.sub(r"[ \t]+", " ", re.sub(r"\s+([,.;:])", r"\1", t)).strip()


def words(t):
    return len(re.findall(r"\b\w+\b", t))


# ------------------------------------------------------------------------------------------------ sections
def md_sections(src, kind="md"):
    """-> [{"title", "paras": [{"text", "l0", "l1"}]}] from markdown source, with the source line of every paragraph.
    References are dropped; figure and table captions are kept in their own section."""
    raw = src.split("\n")
    heads = {n + 1: re.sub(r"^#+\s+", "", l).strip() for n, l in enumerate(raw) if re.match(r"#{1,6}\s+\S", l)}
    h1 = {n + 1 for n, l in enumerate(raw) if re.match(r"#\s+\S", l)}  # the paper title: its byline is not prose to score
    caps = {n + 1: m.group(1) for n, l in enumerate(raw) if (m := re.match(r"!\[([^\]]+)\]\(", l.strip()))}
    secs, cur, buf = [{"title": "(front matter)", "paras": []}], None, []

    def flush():
        nonlocal buf
        if buf:
            secs[-1]["paras"].append({"text": strip_cites(" ".join(t for _, t in buf)), "l0": buf[0][0], "l1": buf[-1][0]})
        buf = []

    caption_paras = []
    for n, t in P.extract(src, kind):
        if n in caps:
            flush(); caption_paras.append({"text": strip_cites(caps[n]), "l0": n, "l1": n}); continue
        if n in heads:
            flush(); secs.append({"title": "(title block)" if n in h1 else heads[n], "paras": []}); continue
        if not t.strip():
            flush(); continue
        if CAPTION.match(t.strip()):
            flush(); caption_paras.append({"text": strip_cites(t), "l0": n, "l1": n}); continue
        buf.append((n, t))
    flush()
    out = []
    for s in secs:
        if re.match(r"(References|Bibliography)\b", s["title"]) or s["title"] == "(title block)":
            continue
        if s["paras"] and not (len(out) == 0 and s["title"] == "(front matter)" and False):
            out.append(s)
    if caption_paras:
        out.append({"title": "(figure and table captions)", "paras": caption_paras})
    return [s for s in out if any(p["text"] for p in s["paras"])]


HEAD_PDF = re.compile(r"^(Abstract|References|Appendix\b.*|\d+(\.\d+)*\.?\s+[A-Z][A-Za-z ,:'/&-]{2,70})$")


def pdf_sections(pdf, drop_refs=True):
    """pdftotext in reading order (two columns: no -layout, which interleaves them), sections by heading lines."""
    txt = subprocess.run(["pdftotext", "-nopgbrk", str(pdf), "-"], capture_output=True, text=True).stdout
    txt = re.sub(r"-\n(?=[a-z])", "", txt).replace("\ufb01", "fi").replace("\ufb02", "fl")
    secs, cur, buf, skip = [{"title": "(front matter)", "paras": []}], None, [], False

    def prose_like(lines):
        toks = " ".join(lines).split()
        alpha = sum(bool(re.fullmatch(r"[A-Za-z][A-Za-z'-]*[.,;:]?", t)) for t in toks)
        return len(toks) >= 12 and alpha / len(toks) >= 0.6 and sum(len(l.split()) for l in lines) / len(lines) >= 5

    def flush(n):
        nonlocal buf
        if buf and not skip and prose_like(buf):
            secs[-1]["paras"].append({"text": strip_cites(" ".join(buf)), "l0": n - len(buf), "l1": n})
        buf = []

    for n, l in enumerate(txt.split("\n"), 1):
        s = l.strip()
        if HEAD_PDF.match(s) and len(s.split()) <= 12:
            flush(n)
            skip = bool(re.match(r"(References|Bibliography)", s)) and drop_refs
            if not skip:
                secs.append({"title": s, "paras": []})
        elif not s:
            flush(n)
        else:
            buf.append(s)
    flush(n)
    return [s for s in secs if any(words(p["text"]) >= 12 for p in s["paras"])]


# ------------------------------------------------------------------------------------------------ chunks
def split_sentences(t):
    return [s for s in re.split(r"(?<=[.!?])\s+", t) if s]


def chunk_section(paras, tok_len):
    """Pack paragraphs into chunks of at most MAX_TOKENS (cleaned text); an over-long paragraph is cut at sentences; chunks
    under MIN_WORDS merge into a neighbour of the same section. No chunk crosses a section."""
    units = []
    for p in paras:
        if tok_len(clean_text(p["text"])) <= MAX_TOKENS:
            units.append(p)
        else:
            cur = ""
            for s in split_sentences(p["text"]):
                if cur and tok_len(clean_text(cur + " " + s)) > MAX_TOKENS:
                    units.append({"text": cur, "l0": p["l0"], "l1": p["l1"]}); cur = s
                else:
                    cur = (cur + " " + s).strip()
            if cur:
                units.append({"text": cur, "l0": p["l0"], "l1": p["l1"]})
    chunks = []
    for u in units:
        if chunks and tok_len(clean_text(chunks[-1]["text"] + "\n" + u["text"])) <= MAX_TOKENS:
            c = chunks[-1]; c["text"] += "\n" + u["text"]; c["l1"] = max(c["l1"], u["l1"])
        else:
            chunks.append(dict(u))
    i = 0
    while i < len(chunks):
        if words(chunks[i]["text"]) < MIN_WORDS and len(chunks) > 1:
            j = i - 1 if i > 0 else i + 1
            a, b = (chunks[j], chunks[i]) if j < i else (chunks[i], chunks[j])
            if tok_len(clean_text(a["text"] + "\n" + b["text"])) <= MAX_TOKENS:
                a["text"] += "\n" + b["text"]; a["l0"] = min(a["l0"], b["l0"]); a["l1"] = max(a["l1"], b["l1"])
                chunks.pop(i if j < i else j); i = max(i - 1, 0); continue
        i += 1
    for c in chunks:
        c["words"], c["tokens"] = words(c["text"]), tok_len(clean_text(c["text"]))
    return chunks


# ------------------------------------------------------------------------------------------------ scorers
class FakeScorer:
    """No GPU, no download: a deterministic stand-in (long words and short sentences push the score up)."""
    name = "fake"

    def tok_len(self, text):
        return len(text.split())

    def score(self, text):
        w = text.split()
        s = min(1.0, sum(len(x) > 7 for x in w) / max(len(w), 1) * 3)
        return s, [1 - s, 0.0, 0.0, s]


class EditLensScorer:
    name = "pangram/editlens_Llama-3.2-3B"

    def __init__(self):
        import torch
        from huggingface_hub import hf_hub_download
        from peft import PeftModel
        from safetensors import safe_open
        from transformers import AutoModelForSequenceClassification, AutoTokenizer
        self.torch = torch
        tok = os.environ.get("HF_TOKEN") or (Path.home() / ".cache/huggingface/token").read_text().strip()  # never printed, never committed
        self.avail_wait()
        self.tokenizer = AutoTokenizer.from_pretrained(BASE, token=tok)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token, self.tokenizer.padding_side = self.tokenizer.eos_token, "left"
        path = hf_hub_download(ADAPTER, "adapter_model.safetensors", token=tok)
        with safe_open(path, framework="pt") as f:
            keys = [k for k in f.keys() if "score" in k and "linear.weight" in k]
            self.n = f.get_tensor(keys[0]).shape[0]
        base = AutoModelForSequenceClassification.from_pretrained(BASE, num_labels=self.n, torch_dtype=torch.float16, token=tok)
        base.config.pad_token_id = self.tokenizer.pad_token_id

        class NormedLinear(torch.nn.Module):  # scripts/train.py of pangramlabs/EditLens, lines 111-120
            def __init__(s, hidden, n, dtype=None):
                super().__init__(); s.norm = torch.nn.LayerNorm(hidden, dtype=dtype); s.linear = torch.nn.Linear(hidden, n, bias=False, dtype=dtype)

            def forward(s, x):
                return s.linear(s.norm(x))

        base.score = NormedLinear(base.config.hidden_size, self.n, dtype=torch.float16)
        self.model = PeftModel.from_pretrained(base, ADAPTER, token=tok).to("cuda").eval()
        with safe_open(path, framework="pt") as f:  # the saved score head must be the one the model now uses (not the untouched original_module copy)
            for k in (k for k in f.keys() if "score" in k):
                live = dict(self.model.named_parameters())["base_model.model." + k[len("base_model.model."):].replace("score.", "score.modules_to_save.default.", 1)]
                assert torch.allclose(f.get_tensor(k).to(live.device, live.dtype), live, atol=1e-3), f"the adapter's {k} was not loaded"

    @staticmethod
    def avail_wait(need_gb=9.0, max_wait=600):
        t0 = time.time()
        while True:
            kb = int(re.search(r"MemAvailable:\s+(\d+)", Path("/proc/meminfo").read_text()).group(1))
            if kb / 1e6 >= need_gb:
                return
            if time.time() - t0 > max_wait:
                raise SystemExit(f"only {kb / 1e6:.1f} GB memory available (need {need_gb}); another job is running, stopped after 10 min")
            time.sleep(15)

    def tok_len(self, text):
        return len(self.tokenizer(text)["input_ids"])

    def score(self, text):
        t = self.torch
        x = self.tokenizer(text, truncation=True, max_length=MAX_LENGTH, return_tensors="pt").to("cuda")
        with t.no_grad():
            p = t.softmax(self.model(**x).logits.float(), dim=-1)[0].cpu().tolist()
        return sum(i * v for i, v in enumerate(p)) / (len(p) - 1), p  # inference.py: probs @ arange(n) / (n - 1)

    def peak_gb(self):
        return self.torch.cuda.max_memory_allocated() / 1e9


# ------------------------------------------------------------------------------------------------ scoring and output
def score_sections(secs, scorer):
    out = []
    for s in secs:
        chunks = chunk_section(s["paras"], scorer.tok_len)
        for c in chunks:
            c["score"], c["bins"] = scorer.score(clean_text(c["text"]))
        w = sum(c["words"] for c in chunks) or 1
        pscored = []
        for p in s["paras"]:  # each paragraph on its own too (reliable from about 40 words), so the owner sees which paragraph, not only which section
            if words(p["text"]) >= MIN_WORDS and scorer.tok_len(clean_text(p["text"])) <= MAX_TOKENS:
                sc, _ = scorer.score(clean_text(p["text"]))
                pscored.append({"score": sc, "l0": p["l0"], "l1": p["l1"], "words": words(p["text"]), "text": p["text"]})
        out.append({"title": s["title"], "words": sum(c["words"] for c in chunks), "chunks": chunks, "paragraphs": pscored,
                    "mean": sum(c["score"] * c["words"] for c in chunks) / w, "max": max((c["score"] for c in chunks), default=0.0)})
    return out


def paper_mean(scored):
    w = sum(s["words"] for s in scored) or 1
    return sum(s["mean"] * s["words"] for s in scored) / w


def previous_run(repo_dir, this):
    runs = sorted(d for d in repo_dir.glob("*") if d.is_dir() and d != this)
    if not runs:
        return {}
    f = runs[-1] / "scores.json"
    return {(k["input"], s["title"]): s["mean"] for k in json.loads(f.read_text())["inputs"] for s in k["sections"]} if f.exists() else {}


def reference_block(refs):
    if not refs:
        return "Reference papers: none scored in this run."
    meds = sorted(r["mean"] for r in refs)
    allc = sorted(c["score"] for r in refs for s in r["sections"] for c in s["chunks"])
    return (f"Human reference ({len(refs)} papers from before 2022-11, same extraction): paper means {', '.join(f'{m:.3f}' for m in meds)}; "
            f"median {meds[len(meds) // 2]:.3f}; chunk scores {allc[0]:.3f} to {allc[-1]:.3f} (max {allc[-1]:.3f}). AI reference: n/a (see notes).")


def write_outputs(out, name, inputs, refs, meta, prev):
    out.mkdir(parents=True, exist_ok=True)
    ref_max = max((c["score"] for r in refs for s in r["sections"] for c in s["chunks"]), default=None)
    md = [f"# Paper AI map: {name}", "", f"EditLens `{meta['model']}`; raw score in [0, 1] (0 = human, 1 = AI). No threshold is published, so there are no labels; "
          "read the scores next to the reference below. A map for the owner to rewrite by hand.", "", reference_block(refs), ""]
    marked = [f"# {name}: chunks in paper order", ""]
    for k in inputs:
        top = sorted(k["sections"], key=lambda s: -s["mean"])[:3]
        md += [f"## {k['input']}", "", "| section | words | chunks | mean | max | delta | worst paragraph | source lines |", "|---|---|---|---|---|---|---|---|"]
        for s in k["sections"]:
            worst = max(s["paragraphs"] or s["chunks"], key=lambda c: c["score"])
            d = prev.get((k["input"], s["title"]))
            delta = "" if d is None else "%+.3f" % (s["mean"] - d)
            ttl = (f"**{s['title']}**" if s in top else s["title"]) + (" (short, noisy)" if s["words"] < MIN_WORDS else "")
            snippet = repr(worst["text"][:80].replace("|", "/"))
            md.append(f"| {ttl} | {s['words']} | {len(s['chunks'])} | {s['mean']:.3f} | {s['max']:.3f} | {delta} | {snippet} | {worst['l0']}-{worst['l1']} |")
        above = sum(c["words"] for s in k["sections"] for c in s["chunks"] if ref_max is not None and c["score"] > ref_max)
        tot = sum(s["words"] for s in k["sections"]) or 1
        md += ["", f"Paper mean {k['mean']:.3f}; " + (f"{100 * above / tot:.0f} % of words in chunks above the human-reference maximum ({ref_max:.3f})." if ref_max is not None else "no human reference scored."), ""]
        marked += [f"## {k['input']}", ""]
        for s in k["sections"]:
            marked += [f"### {s['title']} (mean {s['mean']:.3f})", ""]
            for c in s["chunks"]:
                marked += [f"<!-- editlens chunk {c['score']:.3f} lines {c['l0']}-{c['l1']} -->"]
                for p in s["paragraphs"]:
                    if c["l0"] <= p["l0"] and p["l1"] <= c["l1"]:
                        marked += [f"<!-- editlens paragraph {p['score']:.3f} lines {p['l0']}-{p['l1']} -->", p["text"], ""]
                if not any(c["l0"] <= p["l0"] and p["l1"] <= c["l1"] for p in s["paragraphs"]):
                    marked += [c["text"], ""]
    (out / "map.md").write_text("\n".join(md)); (out / "marked.md").write_text("\n".join(marked))
    (out / "scores.json").write_text(json.dumps({"paper": name, "meta": meta, "inputs": inputs, "references": [{k: v for k, v in r.items()} for r in refs]}, indent=1))


def load_input(path, kind):
    if kind == "pdf":
        return pdf_sections(path)
    src = Path(path).read_text()
    return md_sections(src, "md")


def find_inputs(target, pdf=None):
    p = fence(target, explicit_pdf=bool(pdf) or str(target).endswith(".pdf"))
    ins = []
    if p.is_dir():
        # the rendered markdown has the numbers filled in; the source keeps {{placeholders}} that extraction turns into "N" (a text without
        # its numbers reads more machine-like), so the rendered file is scored when it exists (same line numbers as the source)
        for cand, label in (("paper/DRAFT_4p.md", "rendered source (numbers filled)"), ("paper/DRAFT_4p.src.md", "source"), ("paper/DRAFT_4p.md.in", "source")):
            if (p / cand).exists():
                ins.append((label, p / cand, "md")); break
        if (p / "paper/main.pdf").exists():
            ins.append(("built PDF", p / "paper/main.pdf", "pdf"))
    elif p.suffix == ".pdf":
        ins.append(("PDF", p, "pdf"))
    else:
        ins.append(("source", p, "md"))
    if pdf:
        ins.append(("PDF", fence(pdf, explicit_pdf=True), "pdf"))
    return ins


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target"); ap.add_argument("--pdf"); ap.add_argument("--refs", help="folder of reference PDFs (human text from before 2022-11)")
    ap.add_argument("--out"); ap.add_argument("--fake", action="store_true", help="no model: the deterministic stand-in (tests)")
    a = ap.parse_args(argv)
    inputs_spec = find_inputs(a.target, a.pdf)
    if not inputs_spec:
        raise SystemExit("no paper source or PDF found at that path")
    t0 = time.time()
    scorer = FakeScorer() if a.fake else EditLensScorer()
    name = Path(a.target).resolve().name if Path(a.target).is_dir() else Path(a.target).resolve().stem
    ins = []
    for label, path, kind in inputs_spec:
        scored = score_sections(load_input(path, kind), scorer)
        ins.append({"input": label, "file": str(path), "words": sum(s["words"] for s in scored), "mean": paper_mean(scored), "sections": scored})
    refs = []
    if a.refs:
        for pdf in sorted(Path(fence(a.refs, explicit_pdf=True)).glob("*.pdf")):
            secs = pdf_sections(pdf)
            body = [s for s in secs if re.search(r"Introduction|Method|Approach|Background|Related", s["title"], re.I)] or secs
            text, kept = [], 0
            for s in body:
                for p in s["paras"]:
                    if kept < 1500:
                        text.append(p); kept += words(p["text"])
            scored = score_sections([{"title": "reference body", "paras": text}], scorer)
            refs.append({"file": pdf.name, "words": kept, "mean": paper_mean(scored), "sections": scored})
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    repo_dir = (Path(a.out) if a.out else ROOT / "runs/paper_map" / name)
    out = repo_dir / stamp
    prev = previous_run(repo_dir, out) if repo_dir.exists() else {}
    meta = {"model": scorer.name, "base": BASE, "seconds": round(time.time() - t0, 1), "peak_gpu_gb": round(getattr(scorer, "peak_gb", lambda: 0)(), 2),
            "max_tokens_per_chunk": MAX_TOKENS, "versions": _versions()}
    write_outputs(out, name, ins, refs, meta, prev)
    print(f"{name}: " + "; ".join(f"{k['input']} mean {k['mean']:.3f} ({k['words']} words)" for k in ins) + f" -> {out}/map.md ({meta['seconds']} s, peak {meta['peak_gpu_gb']} GB)")
    return 0


def _versions():
    try:
        import peft, torch, transformers
        return {"torch": torch.__version__, "transformers": transformers.__version__, "peft": peft.__version__}
    except Exception:  # a failing import must not hide the scores
        return {}


if __name__ == "__main__":
    sys.exit(main())
