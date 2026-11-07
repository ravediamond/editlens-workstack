#!/usr/bin/env python3
"""Freeze the baselines and collect every later version of every paragraph of the four papers.

    snapshot.py --freeze        record the baseline commit (the commit a24994eabd72a41969506f37d69cea008ac869e1 of this repository: the four papers exactly as
                                they were before the first hand edit) in expected/baseline.json; refuses to overwrite
    snapshot.py                 walk this repository's history since the baseline for each papers/<name>/paper/DRAFT_4p.md; write expected/versions.json

versions.json: {paper: {"baseline": [{"id", "text", "words"}], "versions": [{"commit", "date", "subject", "override", "text", "words"}]}}
A version is a distinct paragraph text (sha) not present in the baseline; identical texts across commits count once (first commit kept).
Commits with `[polish]` in the subject, or whose author is not the owner, are skipped (PROTOCOL §2)."""
import json, sys
from common import *  # noqa: F401,F403

OWNER = "Ravindu Somawansa"


def freeze():
    if (EXP / "baseline.json").exists():
        sys.exit("baseline.json exists; the baseline is frozen (delete it by hand only before the first number)")
    base = {}
    head = git(ROOT, "rev-parse", "a24994eabd72a41969506f37d69cea008ac869e1^{commit}").strip()
    origin = json.loads((ROOT / "papers/SYNC.json").read_text())  # the heads of the original paper repositories at import
    changed = git(ROOT, "diff", "--name-only", head, "HEAD", "--", *[draft_path(p) for p in PAPERS]).split()
    if changed:
        print("note: these drafts already differ from the import baseline (hand edits since the import):", *changed)
    for p in PAPERS:
        paras = paragraphs(show(head, p))
        base[p] = {"commit": head, "origin_commit": origin[p]["synced_head"], "date": git(ROOT, "log", "-1", "--format=%cI", head).strip(), "paragraphs": len(paras)}
        print(f"{p}: {head[:10]} {base[p]['date'][:10]} {len(paras)} paragraphs >= {MIN_WORDS} words")
    dump("baseline.json", base)
    print("total", sum(v["paragraphs"] for v in base.values()))


def collect():
    base = load("baseline.json") or sys.exit("run --freeze first")
    out = {}
    for p in PAPERS:
        b = base[p]["commit"]
        bparas = paragraphs(show(b, p))
        seen = {sha(t) for t in bparas}
        entry = {"baseline": [{"id": sha(t), "text": t, "words": nwords(t)} for t in bparas], "versions": []}
        log = git(ROOT, "log", "--reverse", "--format=%H%x1f%cI%x1f%an%x1f%s", f"{b}..HEAD", "--", draft_path(p)).strip()
        for line in filter(None, log.split("\n")):
            commit, date, author, subject = line.split("\x1f")
            if "[polish]" in subject or author != OWNER:
                continue
            override = "reword" if "[reword]" in subject else "content" if "[content]" in subject else None
            for t in paragraphs(show(commit, p)):
                h = sha(t)
                if h in seen:
                    continue
                seen.add(h)
                entry["versions"].append({"id": h, "commit": commit[:10], "date": date, "subject": subject, "override": override, "text": t, "words": nwords(t)})
        out[p] = entry
        print(f"{p}: {len(entry['baseline'])} baseline, {len(entry['versions'])} new paragraph texts")
    dump("versions.json", out)


if __name__ == "__main__":
    freeze() if "--freeze" in sys.argv else collect()
