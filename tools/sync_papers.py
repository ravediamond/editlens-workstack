#!/usr/bin/env python3
"""Replay new commits of the original paper repositories into this repository (run by the owner, on a machine that can read them).

    python tools/sync_papers.py --from DIR [--dry-run]

DIR holds up-to-date clones named like the originals (DIR/paper-jepa-world-model, ..., DIR/paper-editlens-sensitivity), each with
its full history (`git pull` them first). For each entry of papers/SYNC.json the commits after `synced_head` (first-parent
order) are replayed one by one: the folder (papers/<name>/ or editlens-paper/) is replaced by that commit's tree, and one commit
is made here with the original author, author date and subject, plus the suffix `[<repo> <hash7>]`. `[polish]`, `[reword]` and
`[content]` in a subject therefore survive, and the human-dose experiment (editlens-paper/repro/human-dose) sees one version
per original commit. SYNC.json is advanced in the same commit. Nothing is pushed.

The agent working in this repository never runs this: it has no access to the private originals."""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
from io import BytesIO
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SYNC = ROOT / "papers/SYNC.json"


def git(repo, *args, env=None, check=True):
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, env=env)
    if check and r.returncode:
        sys.exit(f"git {' '.join(args)} failed in {repo}: {r.stderr.strip()}")
    return r.stdout


def target(key):
    return ROOT / ("editlens-paper" if key == "editlens-paper" else f"papers/{key}")


def replay(key, entry, src, dry):
    last = entry["synced_head"]
    if subprocess.run(["git", "-C", str(src), "merge-base", "--is-ancestor", last, "HEAD"], capture_output=True).returncode:
        sys.exit(f"{key}: synced_head {last[:10]} is not an ancestor of HEAD in {src} (history rewritten or wrong clone)")
    commits = git(src, "rev-list", "--reverse", "--first-parent", f"{last}..HEAD").split()
    print(f"{key}: {len(commits)} new commit(s) in {src.name}")
    for c in commits:
        name, mail, date, subject = git(src, "log", "-1", "--format=%an%x1f%ae%x1f%aI%x1f%s", c).strip().split("\x1f")
        print(f"  {c[:7]} {date[:16]} {name}: {subject[:80]}")
        if dry:
            continue
        data = subprocess.run(["git", "-C", str(src), "archive", c], capture_output=True, check=True).stdout
        with tempfile.TemporaryDirectory() as tmp:
            tarfile.open(fileobj=BytesIO(data)).extractall(tmp, filter="data")
            tgt = target(key)
            if tgt.exists():
                shutil.rmtree(tgt)
            shutil.copytree(tmp, tgt)
        entry["synced_head"] = c
        SYNC.write_text(json.dumps(json.load(open(SYNC)) | {key: entry}, indent=1) + "\n")
        git(ROOT, "add", "-A", str(target(key)), str(SYNC))
        if not git(ROOT, "diff", "--cached", "--name-only").strip():
            continue
        env = {**os.environ, "GIT_AUTHOR_NAME": name, "GIT_AUTHOR_EMAIL": mail, "GIT_AUTHOR_DATE": date,
               "GIT_COMMITTER_NAME": name, "GIT_COMMITTER_EMAIL": mail, "GIT_COMMITTER_DATE": date}
        git(ROOT, "commit", "-q", "-m", f"{subject} [{src.name} {c[:7]}]", env=env)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--from", dest="src", required=True, help="folder with the clones of the original repositories")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if git(ROOT, "status", "--porcelain").strip():
        sys.exit("the working tree is not clean: commit or stash first")
    sync = json.load(open(SYNC))
    for key, entry in sync.items():
        src = Path(a.src).expanduser() / entry["origin"].split("/")[1]
        if not (src / ".git").exists():
            sys.exit(f"{src} is not a clone")
        replay(key, entry, src, a.dry_run)
    print("done; push when you are happy with `git log`")


if __name__ == "__main__":
    main()
