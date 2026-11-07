#!/usr/bin/env python3
"""Paragraph-level EditLens scorer for the owner's own research papers. DIAGNOSTIC AND EXPERIMENT TOOL: it scores, ranks and logs; it never writes paper text (the `apply` step of the original harness was left out on purpose, see AGENTS.md) (WS-162 follow-up, 2026-11-05; lessons in
journal/papers/ai-map/WRITING_RULES.md group L and EDITLENS_LEXICON.md).

    python tools/paper_polish.py serve | stop | status          keep the open EditLens 3B model loaded (~7 GB, ~0.5 s per paragraph at 25 W)
    python tools/paper_polish.py list REPO [--top N]            paragraphs of the paper source with their score (baseline kept in REPO/polish/)
    python tools/paper_polish.py loo REPO N [N ...]             what the paragraph loses without each sentence: fix the top one or two first
    python tools/paper_polish.py try REPO N cands.json [--round R]   score candidate rewrites of paragraph N (a JSON list of source texts)
    python tools/paper_polish.py report REPO                    word-weighted mean before / after, worst paragraph, paragraphs changed

A paragraph is a blank-line-separated block of the paper source (DRAFT_4p.src.md or DRAFT_4p.md.in; code, tables, headings and
image lines skipped) of at least 40 words, rendered with paper/numbers.json before it is scored, so the text the model sees is the
text of the paper. Every
scored candidate goes to REPO/polish/iterlog.jsonl, the provenance of the rewrite. The score is a pointer to paragraphs to reread
(rule 40), not a measure of authorship; the model is CC BY-NC-SA 4.0 and runs on the owner's own research papers only
(paper_map.fence)."""
import json
import os
import re
import subprocess
import sys
import time
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import paper_map as M  # noqa: E402  (scorer, text cleaning, the research-papers-only fence)
import prose_check as P  # noqa: E402

SRV = Path(os.environ.get("EDITLENS_SERVER") or HERE.parent / ".cache/paper-polish-server")
SOURCES = ["paper/DRAFT_4p.src.md", "paper/DRAFT_4p.md.in", "paper/DRAFT_4p.md"]
MIN_WORDS = 40


# ------------------------------------------------------------------------------------------------ the model server (files in, files out)
def serve():
    (SRV / "req").mkdir(parents=True, exist_ok=True); (SRV / "resp").mkdir(parents=True, exist_ok=True)
    scorer = M.EditLensScorer()
    (SRV / "ready").write_text(str(os.getpid()))
    while True:
        for f in sorted((SRV / "req").glob("*.json")):
            try:
                texts = json.loads(f.read_text())
            except Exception:
                continue
            (SRV / "resp" / f.name).write_text(json.dumps([round(scorer.score(M.clean_text(t))[0], 4) for t in texts]))
            f.rename(f.with_suffix(".done"))
        time.sleep(0.3)


def alive():
    try:
        pid = int((SRV / "ready").read_text()); os.kill(pid, 0); return pid
    except Exception:
        return None


def score(texts, wait=300):
    if not alive():
        sys.exit("the model is not loaded: run `python tools/paper_polish.py serve` first (about a minute)")
    rid = uuid.uuid4().hex[:10] + ".json"
    (SRV / "req" / (rid + ".tmp")).write_text(json.dumps(texts)); (SRV / "req" / (rid + ".tmp")).rename(SRV / "req" / rid)
    t0 = time.time()
    while not (SRV / "resp" / rid).exists():
        if time.time() - t0 > wait:
            sys.exit("the scorer did not answer")
        time.sleep(0.3)
    time.sleep(0.1)
    return json.loads((SRV / "resp" / rid).read_text())


# ------------------------------------------------------------------------------------------------ the paper
class Paper:
    def __init__(self, repo):
        self.root = M.fence(repo)
        self.src = next((self.root / s for s in SOURCES if (self.root / s).exists()), None)
        if not self.src:
            sys.exit(f"no paper source in {self.root} ({', '.join(SOURCES)})")
        nj = self.root / "paper/numbers.json"
        self.nums = {k: v["value"] for k, v in json.loads(nj.read_text()).items()} if nj.exists() else {}
        self.pol = self.root / "polish"

    def render(self, t):
        t = re.sub(r"\{\{(\w+)\}\}", lambda m: str(self.nums.get(m.group(1), "X")), t)
        if t.lstrip().startswith("!["):
            return M.strip_cites(re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", t))
        return M.strip_cites(" ".join(x for _, x in P.extract(t, "md") if x.strip()))

    def blocks(self):
        """[{"l0", "l1", "src", "sec"}] of every scoreable paragraph of the current source, in file order."""
        L = self.src.read_text().split("\n"); out, cur, code, sec = [], [], False, ""

        def flush():
            nonlocal cur
            if cur:
                first = cur[0][1]
                if not first.startswith(("|", "!", "<", "$$", "#", "```")) and sec != "(title block)" and not re.match(r"(References|Bibliography)\b", sec):
                    src = "\n".join(x[1] for x in cur)
                    if len(self.render(src).split()) >= MIN_WORDS:
                        out.append({"l0": cur[0][0], "l1": cur[-1][0], "src": src, "sec": sec})
            cur = []
        for n, l in enumerate(L, 1):
            if l.strip().startswith("```"):
                flush(); code = not code; continue
            if code:
                continue
            if l.startswith("#"):
                flush(); sec = "(title block)" if re.match(r"#\s", l) else l.lstrip("# ").strip(); continue
            if not l.strip():
                flush(); continue
            cur.append((n, l))
        flush()
        return out

    def inventory(self):
        f = self.pol / "inventory.json"
        return json.loads(f.read_text()) if f.exists() else None

    def start(self):
        """First call: freeze the baseline (the scores of the paragraphs as they are now)."""
        inv = self.inventory()
        if inv:
            return inv
        bl = self.blocks(); sc = score([self.render(b["src"]) for b in bl]); self.pol.mkdir(exist_ok=True)
        inv = [{"sec": b["sec"], "words": len(self.render(b["src"]).split()), "base": s, "text": self.render(b["src"])} for b, s in zip(bl, sc)]
        (self.pol / "inventory.json").write_text(json.dumps(inv, indent=1)); return inv

    def log(self, **kw):
        with open(self.pol / "iterlog.jsonl", "a") as f:
            f.write(json.dumps({**kw, "t": time.time()}) + "\n")


def phs(t):
    return sorted(re.findall(r"\{\{\w+\}\}", t))


def wmean(scores, words):
    return sum(s * w for s, w in zip(scores, words)) / (sum(words) or 1)


# ------------------------------------------------------------------------------------------------ commands
def cmd_list(p, a):
    top = int(a[a.index("--top") + 1]) if "--top" in a else 0
    inv = p.start(); bl = p.blocks(); cur = score([p.render(b["src"]) for b in bl])
    if len(bl) != len(inv):
        sys.exit(f"the source has {len(bl)} paragraphs, the baseline {len(inv)}: a paragraph was added or removed; move polish/inventory.json aside to start a new baseline")
    rows = sorted(range(len(bl)), key=lambda i: -cur[i]) if top else range(len(bl))
    for i in list(rows)[: top or None]:
        print(f"{i:3d} L{bl[i]['l0']}-{bl[i]['l1']} {cur[i]:.3f} (base {inv[i]['base']:.3f}) {inv[i]['words']:4d}w [{bl[i]['sec'][:26]}] {bl[i]['src'][:60]}")
    print(f"mean {wmean(cur, [inv[i]['words'] for i in range(len(bl))]):.3f}; 39 human papers (pre-2022): paper means 0.033 to 0.123, median 0.071; human results paragraphs median 0.045 (rule 88)")


def cmd_loo(p, a):
    sys.path.insert(0, str(HERE)); import paper_sentences as S
    bl = p.blocks()
    for i in map(int, a):
        t = p.render(bl[i]["src"]); ss = S.split_sentences(t)
        sc = score([t] + [" ".join(x for j, x in enumerate(ss) if j != k) for k in range(len(ss))])
        print(f"--- {i}: {sc[0]:.3f}  (positive = the sentence pushes the paragraph up; fix the top one or two, rules 80 to 87)")
        for k, s in enumerate(ss):
            print(f"  {sc[0] - sc[k + 1]:+.3f}  {s[:150]}")


def cmd_try(p, a):
    i = int(a[0]); cands = json.loads(Path(a[1]).read_text()); rnd = a[a.index("--round") + 1] if "--round" in a else "?"
    p.start(); bl = p.blocks(); cur = bl[i]["src"]
    sc = score([p.render(cur)] + [p.render(c) for c in cands]); (p.pol / f"last_try_{i}.json").write_text(json.dumps({"para": i, "cands": cands}))
    for k, (c, s) in enumerate(zip([cur] + cands, sc)):
        ok = phs(c) == phs(cur)
        print(f"{'cur' if k == 0 else 'c' + str(k)}  {s:.3f}  {'' if ok else 'PLACEHOLDERS CHANGED  '}{len(p.render(c).split())}w")
        p.log(para=i, round=rnd, cand=k, score=s, ph_ok=ok, text=c)


def cmd_report(p, a):
    inv = p.inventory() or sys.exit("no baseline yet: run `list` first")
    bl = p.blocks(); cur = score([p.render(b["src"]) for b in bl]); w = [x["words"] for x in inv]
    print(f"{p.root.name}: {wmean([x['base'] for x in inv], w):.3f} -> {wmean(cur, w):.3f}; worst {max(x['base'] for x in inv):.3f} -> {max(cur):.3f}; "
          f"{sum(abs(c - x['base']) > 0.02 for c, x in zip(cur, inv))} of {len(inv)} paragraphs moved by more than 0.02")


def main(argv=None):
    a = list(sys.argv[1:] if argv is None else argv)
    if not a or a[0] in ("-h", "--help"):
        print(__doc__); return 0
    cmd = a.pop(0)
    if cmd == "_serve":
        serve(); return 0
    if cmd == "serve":
        if alive():
            print(f"already running (pid {alive()})"); return 0
        SRV.mkdir(parents=True, exist_ok=True)
        try:
            (SRV / "ready").unlink()
        except FileNotFoundError:
            pass
        py = Path(os.environ.get("EDITLENS_PY") or sys.executable)
        subprocess.Popen([str(py), str(Path(__file__).resolve()), "_serve"], stdout=open(SRV / "server.log", "w"), stderr=subprocess.STDOUT, start_new_session=True)
        for _ in range(120):
            if alive():
                print("ready"); return 0
            time.sleep(2)
        sys.exit(f"not ready after 4 minutes: see {SRV / 'server.log'}")
    if cmd == "stop":
        pid = alive()
        if pid:
            os.kill(pid, 15); (SRV / "ready").write_text("0"); print("stopped")
        return 0
    if cmd == "status":
        print("running" if alive() else "not running"); return 0
    fn = {"list": cmd_list, "loo": cmd_loo, "try": cmd_try, "report": cmd_report}.get(cmd)
    if not fn or not a:
        print(__doc__); return 2
    fn(Paper(a[0]), a[1:])
    return 0


if __name__ == "__main__":
    sys.exit(main())
