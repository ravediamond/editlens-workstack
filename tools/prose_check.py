#!/usr/bin/env python3
"""WS-158: deterministic prose check for texts that people will read (zero model tokens, stdlib only here).

    python3 tools/prose_check.py <file|-> [--kind md|tex|txt] [--json] [--review OUT.md]

Extracts the prose (no code, tables, math, URLs, BibTeX), keeps a map back to source lines, and runs two scanners in
the current Python through tools/prose_engine.py: slopscore-lint (hard gate: any finding of severity >= medium fails; a
text under ~100 words gates on high only) and lmscan (advisory: sentences with AI probability >= 0.80). The source file
is never modified. Exit: 0 pass, 1 fail, 2 usage, 3 tool missing. Non-English text is skipped (exit 0)."""
import argparse
import bisect
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(os.environ.get("PROSE_ROOT") or HERE.parent)  # the repo whose texts are checked (tests point it at a fixture)
RUNS_PROSE = Path(os.environ.get("PROSE_RUNS") or ROOT / "runs" / "prose")
PROSE_PY = os.environ.get("PROSE_PY", sys.executable)
ENGINE = HERE / "prose_engine.py"
PIP = "pip install -r tools/requirements-prose.txt"
SEV = {"low": 1, "medium": 2, "high": 3}
MAX_LINES, ADVISORY_P, SHORT_WORDS = 30, 0.80, 100


# --------------------------------------------------------------------------------------------- extraction
def _inline_md(s):
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", s)
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"`[^`\n]+`", "X", s)
    s = re.sub(r"\{\{[^}]*\}\}", "N", s)
    s = re.sub(r"\$\$[^$]*\$\$|\$[^$\n]+\$", "X", s)
    s = re.sub(r"<!--.*?-->", "", s)
    s = re.sub(r"</?[A-Za-z][^>]*>", "", s)
    s = re.sub(r"https?://\S+", "", s)
    s = re.sub(r"\[\^[^\]]+\]", "", s)
    return re.sub(r"^#{1,6}\s+", "", s)


def extract_md(src):
    out, fence, comment, math, prev_code, in_list, prev_blank = [], False, False, False, False, False, True
    lines = src.split("\n")
    i0 = 0
    if lines and lines[0].strip() == "---":
        for j in range(1, len(lines)):
            if lines[j].strip() == "---":
                i0 = j + 1
                break
    for n in range(i0, len(lines)):
        raw, st = lines[n], lines[n].strip()
        if fence:
            fence = not re.match(r"(```|~~~)", st)
            out.append((n + 1, "")); continue
        if re.match(r"(```|~~~)", st):
            fence = True; out.append((n + 1, "")); continue
        if comment:
            comment = "-->" not in raw; out.append((n + 1, "")); continue
        if st.startswith("<!--") and "-->" not in st:
            comment = True; out.append((n + 1, "")); continue
        if math:
            math = "$$" not in st; out.append((n + 1, "")); continue
        if st.startswith("$$") and st.count("$$") == 1:
            math = True; out.append((n + 1, "")); continue
        if st.startswith("|") or re.match(r"!\[", st):
            out.append((n + 1, "")); continue
        if st and re.match(r"(\s{4,}|\t)", raw) and not in_list and (prev_blank or prev_code):
            prev_code = True; out.append((n + 1, "")); continue
        prev_code = False
        if st:
            in_list = bool(re.match(r"([-*+]|\d+[.)])\s", st)) or (in_list and raw.startswith((" ", "\t")))
        else:
            in_list = False
        prev_blank = not st
        out.append((n + 1, _inline_md(raw).rstrip()))
    return out


def _unwrap_tex(s):
    s = re.sub(r"\\(?:cite[a-z]*|ref|eqref|label|url|footnotemark|includegraphics)\*?(?:\[[^\]]*\])*\{[^}]*\}", "", s)
    s = re.sub(r"\\(?:begin|end)\{[^}]*\}", "", s)
    s = re.sub(r"\{\{[^}]*\}\}", "N", s)
    s = re.sub(r"\$[^$]*\$", "X", s)
    for _ in range(6):
        t = re.sub(r"\\[A-Za-z]+\*?(?:\[[^\]]*\])?\{([^{}]*)\}", r"\1", s)
        if t == s:
            break
        s = t
    s = re.sub(r"\\[A-Za-z]+\*?", "", s).replace("\\\\", " ").replace("~", " ")
    return re.sub(r"[{}]", "", s).replace("\\%", "%").replace("\\&", "&").replace("\\_", "_")


def extract_tex(src):
    m = re.search(r"\\begin\{document\}", src)
    pre = src[: m.end()].count("\n") if m else 0
    body = src[m.end():] if m else src
    body = re.sub(r"\\end\{document\}.*", "", body, flags=re.S)
    env = r"(figure|table|equation|align|algorithm|lstlisting|tabular|thebibliography|verbatim)\*?"
    body = re.sub(r"\\begin\{" + env + r"\}.*?\\end\{\1\*?\}", lambda mm: "\n" * mm.group(0).count("\n"), body, flags=re.S)
    out = []
    for k, raw in enumerate(body.split("\n")):
        raw = re.sub(r"(?<!\\)%.*", "", raw)
        out.append((pre + k + 1, _unwrap_tex(raw).strip()))
    return out


def extract(src, kind):
    if kind == "tex":
        return extract_tex(src)
    if kind == "txt":
        return [(i + 1, l.rstrip()) for i, l in enumerate(src.split("\n"))]
    return extract_md(src)


def paragraphs(lines):
    paras, cur = [], []
    for n, t in lines:
        if t.strip():
            cur.append((n, t))
        elif cur:
            paras.append(cur); cur = []
    if cur:
        paras.append(cur)
    text, offs, off = [], [], 0
    for p in paras:
        body = "\n".join(t for _, t in p)
        offs.append((off, p, body)); text.append(body); off += len(body) + 2
    return "\n\n".join(text), offs


def line_of(text, offs, span, hint=0):
    """Source line for a span: find it in the extracted text (the scanners' offsets are into their normalised copy)."""
    key = span.strip()[:80]
    i = text.find(key, max(0, hint - 80)) if key else -1
    if i < 0 and key:
        i = text.find(key)
    if i < 0:
        return offs[0][1][0][0] if offs else 1
    starts = [o[0] for o in offs]
    k = max(bisect.bisect_right(starts, i) - 1, 0)
    off, p, body = offs[k]
    rel = i - off
    line = p[0][0]
    pos = 0
    for n, t in p:
        if rel >= pos:
            line = n
        pos += len(t) + 1
    return line


# --------------------------------------------------------------------------------------------- scope and rounds
def _rx(g):
    out, i = "", 0
    while i < len(g):
        if g.startswith("**/", i):
            out += "(?:.*/)?"; i += 3
        elif g.startswith("**", i):
            out += ".*"; i += 2
        elif g[i] == "*":
            out += "[^/]*"; i += 1
        elif g[i] == "?":
            out += "[^/]"; i += 1
        else:
            out += re.escape(g[i]); i += 1
    return re.compile("^" + out + "$")


def load_allow():
    """tools/prose_allow.txt (owner-edited): {rule id: {allowed span, lowercase}}."""
    allow, f = {}, HERE / "prose_allow.txt"
    for l in (f.read_text().splitlines() if f.exists() else []):
        l = l.strip()
        if l and not l.startswith("#") and ":" in l:
            r, w = l.split(":", 1)
            allow.setdefault(r.strip(), set()).add(w.strip().lower())
    return allow


def load_scope():
    inc, exc = [], []
    for l in (HERE / "prose_scope.txt").read_text().splitlines():
        l = l.split("  #")[0].strip()
        if not l or l.startswith("#"):
            continue
        (exc if l.startswith("!") else inc).append(l.lstrip("!"))
    return inc, exc


def _key(path, pat):
    path = Path(path).resolve()
    if pat.startswith(("~", "/")):
        return str(path), os.path.expanduser(pat)
    try:
        return str(path.relative_to(ROOT)), pat
    except ValueError:
        return None, pat


def in_scope(path):
    inc, exc = load_scope()
    hit = lambda pats: any((k := _key(path, g))[0] is not None and _rx(k[1]).match(k[0]) for g in pats)  # noqa: E731
    return hit(inc) and not hit(exc) and Path(path).suffix in (".md", ".tex", ".in", ".txt")


def scope_files():
    """Every in-scope file that exists today, with the glob that matched it first."""
    inc, exc = load_scope(); seen, per = {}, {}
    roots = [ROOT]
    for r in roots:
        for dp, dn, fn in os.walk(r):
            dn[:] = [d for d in dn if d not in (".git", "node_modules", "runs", "outputs", "archive", ".venv")]
            for f in fn:
                fp = Path(dp) / f
                if fp.suffix in (".md", ".tex", ".in", ".txt") and str(fp) not in seen and in_scope(fp):
                    g = next(g for g in inc if (k := _key(fp, g))[0] is not None and _rx(k[1]).match(k[0]))
                    seen[str(fp)] = g; per[g] = per.get(g, 0) + 1
    return seen, per


def changed_files(repo):
    """Working-tree changes plus commits not yet pushed in the git repo at `repo`, as absolute paths that exist."""
    def git(*a):
        r = subprocess.run(["git", "-C", str(repo), *a], capture_output=True, text=True)
        return r.stdout.splitlines() if r.returncode == 0 else []
    top = (git("rev-parse", "--show-toplevel") or [str(repo)])[0]
    names = [l[3:].split(" -> ")[-1].strip('"') for l in git("status", "--porcelain", "-uall")]
    names += git("diff", "--name-only", "@{upstream}..HEAD")
    return sorted({str(Path(top) / n) for n in names if (Path(top) / n).is_file()})


ROUNDS = RUNS_PROSE / "rounds.json"
MAX_ROUNDS = 3


def bump_round(path, session):
    """Failed-check counter per file and session (the stop gate and ws verify share it); returns the new count."""
    ROUNDS.parent.mkdir(parents=True, exist_ok=True)
    d = json.loads(ROUNDS.read_text()) if ROUNDS.exists() else {}
    k = f"{path}|{session}"; d[k] = d.get(k, 0) + 1
    ROUNDS.write_text(json.dumps(d)); return d[k]


def slug_of(path):
    """Report name: the path under the repo root, else under the home folder (so two README.md files do not share a report)."""
    p = Path(path).resolve()
    for base in (ROOT, Path.home()):
        try:
            return re.sub(r"[^A-Za-z0-9_.-]+", "_", str(p.relative_to(base)))
        except ValueError:
            continue
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", p.name)


def check_path(path):
    p = Path(path); kind = {".tex": "tex", ".txt": "txt"}.get(p.suffix, "md")
    slug = slug_of(p)
    src = p.read_text(errors="replace"); rep = check(src, kind, slug)
    out = RUNS_PROSE; out.mkdir(parents=True, exist_ok=True)
    (out / f"{slug}.json").write_text(json.dumps(rep, indent=1))
    if rep["status"] == "fail":
        (out / f"{slug}.review.md").write_text(review_copy(src, rep))
    return rep


# --------------------------------------------------------------------------------------------- run
def run_engine(text):
    if not Path(PROSE_PY).exists():
        print(f"prose: tool missing ({PROSE_PY}); install with: {PIP}", file=sys.stderr)
        sys.exit(3)
    r = subprocess.run([PROSE_PY, str(ENGINE)], input=json.dumps({"text": text}), capture_output=True, text=True, timeout=180)
    if r.returncode:
        print("prose: engine failed: " + r.stderr[-300:], file=sys.stderr)
        sys.exit(3)
    return json.loads(r.stdout)


def _rel(p):
    try:
        return str(Path(p).relative_to(ROOT))
    except ValueError:
        return str(p)


def short(s, n=60):
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= n else s[: n - 1] + "…"


def check(src, kind, slug):
    t0 = time.time()
    text, offs = paragraphs(extract(src, kind))
    words = len(text.split())
    res = run_engine(text) if words else {"lang": "en", "slop": {"score": {"slop_score": 0, "label": "empty"}, "evidence": []}, "lm": []}
    rep = {"slug": slug, "kind": kind, "words": words, "lang": res["lang"], "seconds": 0}
    if res["lang"] != "en":
        rep.update(status="skipped", must=[], consider=[], seconds=round(time.time() - t0, 2))
        return rep
    score = res["slop"]["score"]
    gate = SEV["high"] if words < SHORT_WORDS else SEV["medium"]
    must, allow = [], load_allow()
    for e in res["slop"]["evidence"]:
        if e.get("kind") != "finding" or SEV.get(e["severity"], 0) < gate:
            continue
        if e["span"].strip().lower() in allow.get(e["rule_id"], ()):
            continue  # the owner allowed this word for this rule
        must.append({"line": line_of(text, offs, e["span"], e.get("start_char", 0)), "rule": e["rule_id"], "severity": e["severity"],
                     "span": e["span"], "explanation": e["explanation"]})
    must.sort(key=lambda m: m["line"])
    consider = sorted(({"line": line_of(text, offs, s["text"]), "p": s["p"], "text": s["text"]} for s in res["lm"] if s["p"] >= ADVISORY_P),
                      key=lambda c: c["line"])
    rep.update(status="fail" if must else "pass", slop=score.get("slop_score"), label=score.get("label"), must=must, consider=consider,
               lm_doc_p=res.get("lm_doc_p"), warnings=res["slop"].get("warnings", []), seconds=round(time.time() - t0, 2))
    return rep


def report_lines(rep):
    if rep["status"] == "skipped":
        return [f"prose: skipped (lang={rep['lang']})"]
    lines = [f"L{m['line']} [MUST] {m['rule']} \"{short(m['span'])}\" — {m['explanation']}" for m in rep["must"]]
    adv = [f"L{c['line']} [consider] lmscan p={c['p']:.2f} \"{short(c['text'])}\"" for c in rep["consider"]]
    room = MAX_LINES - 1 - len(lines)
    if room < 0:
        lines = lines[: MAX_LINES - 2] + [f"… {len(rep['must']) - (MAX_LINES - 2)} more MUST lines in the full report"]; adv = []
    elif len(adv) > room:
        adv = adv[: max(room - 1, 0)] + ([f"… {len(rep['consider']) - max(room - 1, 0)} more advisory sentences"] if room else [])
    head = "PASS" if rep["status"] == "pass" else "FAIL"
    return lines + adv + [f"prose: {head} slop={rep['slop']} must={len(rep['must'])} consider={len(rep['consider'])} "
                          f"(full report: {_rel(RUNS_PROSE)}/{rep['slug']}.json)"]


def review_copy(src, rep):
    lines = src.split("\n")
    notes = []
    for n, m in enumerate(rep["must"], 1):
        ln = lines[m["line"] - 1] if 0 < m["line"] <= len(lines) else ""
        k = ln.find(m["span"].strip()[:80])
        mark = f"=={m['span'].strip()[:80]}==[^{n}]"
        if k >= 0:
            lines[m["line"] - 1] = ln[:k] + mark + ln[k + len(m["span"].strip()[:80]):]
        else:
            lines[m["line"] - 1] = ln + f" <!-- MUST [^{n}] \"{short(m['span'], 40)}\" -->"
        notes.append(f"[^{n}]: {m['rule']} — {m['explanation']}")
    for c in rep["consider"]:
        if 0 < c["line"] <= len(lines):
            lines[c["line"] - 1] += f" <!-- lmscan p={c['p']:.2f} -->"
    return "\n".join(lines).rstrip("\n") + "\n\n" + "\n".join(notes) + ("\n" if notes else "")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", nargs="?"); ap.add_argument("--kind", choices=["md", "tex", "txt"]); ap.add_argument("--json", action="store_true")
    ap.add_argument("--review", help="write the marked review copy here (default runs/prose/<slug>.review.md on a failure)")
    ap.add_argument("--changed", metavar="REPO", help="check the in-scope files changed in this git repo (working tree and unpushed commits)")
    ap.add_argument("--scope", action="store_true", help="list the in-scope files that exist today, per glob")
    a = ap.parse_args(argv)
    if a.scope:
        seen, per = scope_files()
        for g, n in per.items():
            print(f"{n:4d}  {g}")
        print(f"{len(seen)} in-scope files")
        return 0
    if a.changed:
        bad = 0
        for f in changed_files(a.changed):
            if in_scope(f):
                rep = check_path(f); bad += rep["status"] == "fail"
                print(f"{f}: {report_lines(rep)[-1]}", file=sys.stderr)
        return 1 if bad else 0
    if not a.file:
        ap.error("a file, -, --scope or --changed is required")
    if a.file == "-":
        src, slug, kind = sys.stdin.read(), "stdin", a.kind or "md"
    else:
        p = Path(a.file)
        if not p.is_file():
            print(f"prose: no such file {a.file}", file=sys.stderr); return 2
        src, kind = p.read_text(errors="replace"), a.kind or {".tex": "tex", ".txt": "txt"}.get(p.suffix, "md")
        slug = slug_of(p)
    rep = check(src, kind, slug)
    out = RUNS_PROSE; out.mkdir(parents=True, exist_ok=True)
    (out / f"{slug}.json").write_text(json.dumps(rep, indent=1))
    if rep["status"] == "fail":
        Path(a.review or out / f"{slug}.review.md").write_text(review_copy(src, rep))
    print("\n".join(report_lines(rep)), file=sys.stderr)
    if a.json:
        print(json.dumps(rep))
    return 1 if rep["status"] == "fail" else 0


if __name__ == "__main__":
    sys.exit(main())
