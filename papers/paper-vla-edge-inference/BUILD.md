# Build (WS-093, 2026-11-01)

Assembled by road-to-robotics `scripts/paper_repo_build.py` from road-to-robotics and paper-vs-hardware at the commits in PROVENANCE.md, by copying only (85 files). Experiments: aac chunk-boundary glat2 horizon-depth pact smooth-chunking .

- L0: every `repro/*/l0_check.py` passes from a fresh copy (`make l0`); nothing failed to reproduce.
- `make check` regenerates the paper from `repro/` and fails on any difference; two consecutive builds are byte-identical (`SOURCE_DATE_EPOCH` pinned).
- `paper/make_paper.py`: reads and anchors point into `repro/` (as for the other paper). Regenerated before any edit: all 52 values identical to road-to-robotics `journal/papers/edge-inference/numbers.json`; text unchanged.
- Review of 2026-11-01 applied in both `DRAFT_4p.src.md` and `main.src.tex`: PACT compared with the recorded teleop continuation (open loop, training-set episodes), the AAC jump given as a median ratio (lower is better), 25 W / MAXN inline in the abstract and §2, seven tricks, the ten-step rule attributed to the protocol, the `[to run]` arm columns named as the 8-page addition.
- `repro/glat2` and `repro/smooth-chunking` are new (no paper-vs-hardware folder existed); their L0s recompute the timing split and every gate-A median and ratio.
- Not copied: reviews, feasibility memos, strategy notes, keys, raw data.
