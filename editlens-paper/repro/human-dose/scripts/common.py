"""Shared pieces of the human-dose experiment: paths, paragraph extraction from a rendered DRAFT_4p.md, git helpers.

Runs from the repository root with the EditLens environment (tools/requirements-editlens.txt). The four papers are the folders
papers/<name>/ of this single repository; their history is this repository's history (hand-edited commits of the original
paper repositories are replayed by tools/sync_papers.py with the original author, date and subject)."""
import hashlib, json, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent / "expected"
ROOT = next(p for p in HERE.parents if (p / "AGENTS.md").exists())
sys.path.insert(0, str(ROOT / "tools"))
PAPERS = ["paper-register-reproducibility", "paper-jepa-world-model", "paper-reward-models-stopping-rule", "paper-vla-edge-inference"]
REPOS = ROOT  # git runs in the single repository; a paper is papers/<name>/
DRAFT = "paper/DRAFT_4p.md"  # inside papers/<name>/
MIN_WORDS = 40
BINS = [(0.00, 0.03), (0.03, 0.06), (0.06, 0.10), (0.10, 0.15), (0.15, 1.01)]


def strip_cites(t):
    try:
        import paper_map as M
        return M.strip_cites(t)
    except Exception:
        t = re.sub(r"\[@[^\]]+\]", "", t)
        t = re.sub(r"\[arXiv:[^\]]+\]", "", t)
        return re.sub(r"[ \t]+", " ", re.sub(r"\s+([,.;:])", r"\1", t)).strip()


def nwords(t):
    return len(re.findall(r"\b\w+\b", t))


def paragraphs(md):
    """Prose paragraphs of a rendered markdown draft: blank-line blocks that are not headings, tables, quotes, code,
    figures, list items or the author line; citations stripped; at least MIN_WORDS words."""
    out, fence = [], False
    for block in re.split(r"\n\s*\n", md):
        b = block.strip()
        if not b:
            continue
        if b.startswith("```"):
            fence = not fence if b.count("```") % 2 else fence
            continue
        if fence:
            continue
        first = b.lstrip()
        if first[0] in "#|>!-*" or first.startswith("Table ") or first.startswith("Figure ") or first.startswith("*") or re.match(r"^\d+\.\s", first):
            continue
        t = strip_cites(re.sub(r"\s+", " ", b))
        if nwords(t) >= MIN_WORDS:
            out.append(t)
    return out


def sha(t):
    return hashlib.sha1(t.encode()).hexdigest()[:12]


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, check=True).stdout


def draft_path(name):
    return f"papers/{name}/{DRAFT}"


def show(rev, name):
    return git(ROOT, "show", f"{rev}:{draft_path(name)}")


def load(name):
    p = EXP / name
    return json.loads(p.read_text()) if p.exists() else None


def dump(name, obj):
    EXP.mkdir(parents=True, exist_ok=True)
    (EXP / name).write_text(json.dumps(obj, indent=1, ensure_ascii=False) + "\n")


def bin_of(m):
    for i, (lo, hi) in enumerate(BINS):
        if lo <= m < hi:
            return i
    return len(BINS) - 1
