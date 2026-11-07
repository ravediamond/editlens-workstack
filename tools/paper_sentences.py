#!/usr/bin/env python3
"""WS-162: EditLens score of every sentence of the owner's papers (the rendered text, numbers filled in), as JSON.

    python tools/paper_sentences.py <paper-repo-dir> [<paper-repo-dir> ...] --out DIR [--combined FILE] [--fake]

Per sentence: `score_alone` (the sentence as a text of its own; a single sentence is far below the 75 words the model was trained on, so
it is noisy), and, for paragraphs of at least 40 words, `score_without_it` (the paragraph with that sentence removed) and
`contribution` = paragraph score - score_without_it (positive: the sentence pushes the paragraph toward AI). Raw EditLens scores in [0, 1],
no thresholds. Same research-papers-only fence as paper_map.py (CC BY-NC-SA, non-commercial)."""
import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import paper_map as M  # noqa: E402

ABBREV = ("Fig.", "Figs.", "Table", "Tab.", "e.g.", "i.e.", "vs.", "al.", "cf.", "approx.", "No.", "Eq.", "Sec.")


def split_sentences(text):
    """Sentences of a paragraph; a full stop after an abbreviation, a number or a single capital does not end one."""
    t = text
    for a in ABBREV:
        t = t.replace(a + " ", a.replace(".", "․") + " ")
    t = re.sub(r"(\b[A-Z])\. ", lambda m: m.group(1) + "․ ", t)
    t = re.sub(r"(\d)\. (?=\d)", lambda m: m.group(1) + "․ ", t)
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9*_\[(\"'])", t)
    return [p.replace("․", ".").replace(" ", " ").strip() for p in parts if p.strip()]


def score_paper(repo, scorer, refs):
    ins = M.find_inputs(str(repo))
    label, path, kind = next(i for i in ins if i[2] == "md")
    secs = M.md_sections(Path(path).read_text(), "md")
    out, n = [], 0
    for s in secs:
        for pi, p in enumerate(s["paras"]):
            sents = split_sentences(p["text"])
            pw = M.words(p["text"])
            para = None
            if pw >= M.MIN_WORDS and scorer.tok_len(M.clean_text(p["text"])) <= M.MAX_TOKENS:
                para, _ = scorer.score(M.clean_text(p["text"]))
            for k, sent in enumerate(sents):
                n += 1
                alone, _ = scorer.score(M.clean_text(sent)) if M.words(sent) >= 3 else (None, None)
                without = contrib = None
                if para is not None and len(sents) > 1:
                    rest = " ".join(x for j, x in enumerate(sents) if j != k)
                    without, _ = scorer.score(M.clean_text(rest))
                    contrib = para - without
                out.append({"id": n, "section": s["title"], "lines": [p["l0"], p["l1"]], "paragraph": pi + 1,
                            "paragraph_score": None if para is None else round(para, 4), "sentence_in_paragraph": k + 1,
                            "sentence": sent, "words": M.words(sent), "score_alone": None if alone is None else round(alone, 4),
                            "score_without_it": None if without is None else round(without, 4),
                            "contribution": None if contrib is None else round(contrib, 4)})
    return {"paper": Path(repo).resolve().name, "text": f"{label} ({path.name})", "file": str(path),
            "sentences": out, "n_sentences": len(out)}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("repos", nargs="+"); ap.add_argument("--out", required=True); ap.add_argument("--combined")
    ap.add_argument("--fake", action="store_true")
    a = ap.parse_args(argv)
    scorer = M.FakeScorer() if a.fake else M.EditLensScorer()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    meta = {"model": scorer.name, "base": M.BASE, "date": dt.datetime.now().isoformat(timespec="seconds"),
            "scale": "raw EditLens score in [0, 1], 0 = human, 1 = AI; no thresholds are published",
            "note": "score_alone is for one sentence as a text of its own (noisy: the model trained on 75+ words); contribution = paragraph score minus the score of the paragraph without that sentence (paragraphs of 40+ words only)"}
    allp = []
    for r in a.repos:
        M.fence(r)
        res = score_paper(r, scorer, None)
        (out / f"{res['paper']}.sentences.json").write_text(json.dumps({"meta": meta, **res}, indent=1, ensure_ascii=False))
        allp.append(res)
        sc = [s["score_alone"] for s in res["sentences"] if s["score_alone"] is not None]
        print(f"{res['paper']}: {res['n_sentences']} sentences, score_alone mean {sum(sc) / len(sc):.3f}, max {max(sc):.3f}")
    if a.combined:
        Path(a.combined).write_text(json.dumps({"meta": meta, "papers": allp}, indent=1, ensure_ascii=False))
        print("combined ->", a.combined)
    return 0


if __name__ == "__main__":
    sys.exit(main())
