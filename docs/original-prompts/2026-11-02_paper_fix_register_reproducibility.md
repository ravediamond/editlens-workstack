# Claude Code prompt — Paper A (reproducibility of the register): close the pre-registration audit, then draft

Repo: `/home/jetson/scratch/paper-repos/paper-register-reproducibility` (`ravediamond/paper-register-reproducibility`,
skeleton, no PDF). Journal side: `journal/papers/reproducibility-study/` (`FEASIBILITY.md`, `PREREG_CHECK.md`,
`prereg_check.json`, `prereg_check.py`, `prereg_table.py`, `RECOMPUTED.md`, `PAPER_WORDING.md`). Read first: all of
those, the repo's `README.md`, `ws show WS-067`, `WS-068`, `WS-078`, `WS-088`, `WS-105`, `WS-113`, `WS-121`.

Review of 2026-11-02 (chat, owner accepted). There is nothing to review yet; the blocker before a draft is the paper's
own pre-registration, which today reads "36 bar-first, 0 result-first, 31 same-commit, 19 no-bar of 89 gate rows". A
reproducibility paper whose own bars are one-third unprovable is the easiest paper to reject. The item does the
audit first and only then drafts.

Standing rules: no `rm` outside `~/scratch/WS-NNN/`, no `sudo`; commits as Ravindu Somawansa, one line, no AI mention,
no session links; nothing posted outside the owner's repos; no verdict changed by hand. Commit at every milestone (K3).

## Part 1 — the audit, $0, Orin CPU

1. **Bar-before-result per gate, resolved.** For each of the 31 same-commit and 19 no-bar rows in `prereg_check.json`:
   `git log -S` (road-to-robotics full history, and paper-vs-hardware) for the bar text and for the first result
   number; also the dated rows of the experiment log (`grep -n "<gate id>" journal/EXPERIMENTS.md`, the matching lines only; never read the whole file), the `PROTOCOL.md` files and the `shared/gate/data/*` folder
   timestamps. Classify each row into exactly one of: bar-first (commit of the bar strictly before the first commit of
   its result), same-commit (bar and result first appear together: not provable), result-first, no-bar. Write
   `journal/papers/reproducibility-study/PREREG_AUDIT.md`: the table (row · gate · bar commit · result commit · class ·
   evidence path) and the counts; regenerate `prereg_check.json` from it (`prereg_check.py` reads the audit). No row is
   upgraded on a note or a memory — only on a commit ordering.
2. **Recompute the early gates with the episode bootstrap** from the stored rows (`RECOMPUTED.md` says which rows
   exist): every early gate whose rows are stored gets a point estimate + 95 % CI with METHOD I.4 (2,000 resamples);
   gates without rows are listed as "point estimate only, rows not stored". Append to `RECOMPUTED.md`; no verdict
   changes — a verdict that would flip under the CI is flagged `flip-under-CI` and reported to the owner, not changed.
3. **Paper-side audit, closed.** The 12 content rows and the 20 citation fixes of WS-068 are either applied in the site
   register (`~/workspace/site/data/register.yaml`, one commit) or listed with the owner decision they need. The 10
   papers missing from the mirror: list them with arXiv ids for the owner to add to Drive; do not fetch PDFs here.
4. **Second-reader protocol** for the failure classes (edge latency / zero-shot judges / latent planners beaten by
   joints): write `repro/classes/PROTOCOL.md` — the three class definitions in one sentence each, the 20 claim rows a
   second reader would classify blind, the agreement statistic (Cohen's κ, bar ≥ 0.6), the form to send. The reading
   itself is the owner's (a human second reader).
5. Commit, push, log the counts, **stop, `waiting-owner`** with the new prereg counts and the flip-under-CI list.

## Part 2 — the draft (after the owner's go on Part 1's counts)

Draft `paper/DRAFT_4p.md.in` + `make_paper.py` + `numbers.json` on the same pipeline as the other three repos (copy
`paper-jepa-world-model/paper/make_paper.py` and adapt; every number anchored to a file under `repro/`): title
"What survives when a paper leaves the lab: a pre-registered re-test of N robot-learning papers on a €1,350 rig";
abstract ≤ 150 words, ≤ 4 numbers (papers / claim rows / reproduce fraction / cost); §1 what the register is and the
three conditions (accessible hardware, cheapest baseline first, bar before the run); §2 the rig and the method with
the **audited** prereg counts and the honest sentence from `PAPER_WORDING.md`; §3 the results as one table (paper ·
their rig class · claim · bar · result · verdict · class) generated from the register; §4 the three failure classes
with one example each; §5 Limitations (one rig, one owner's labels, same-commit rows, the second reader not yet done);
Related work with `\cite` (2606.08881, 2607.24481, 2603.13966, 2610.18869, RoboSeed 2610.40026 — read it first, it is
the closest statement of the thesis). House style from WS-132, bibliography with natbib, plain names, no codenames in
the prose, author block + repo footnote. `make check` green, CI, CHANGELOG, `REVIEW_2026-11-02.md` in the journal
folder. Push, log, `waiting-owner`: "draft built; repo private — make public before any endorsement request".
