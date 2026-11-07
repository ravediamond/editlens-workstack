# Claude Code prompt — Paper C (VLA edge inference): make it endorsable

Repo: `/home/jetson/scratch/paper-repos/paper-vla-edge-inference` (`ravediamond/paper-vla-edge-inference`). Journal side:
`journal/papers/edge-inference/` (`FEASIBILITY.md`, `REVIEW_2026-11-01.md`). Read first: the repo's `README.md`,
`BUILD.md`, `paper/DRAFT_4p.src.md`, `paper/numbers.json`, `paper/refs.bib`, `paper/make_paper.py`, each
`repro/*/PROTOCOL.md`, and `ws show WS-064` (gate A/B of smooth chunking), `ws show WS-089`.

Review of 2026-11-02 (chat, owner accepted). All 52 numbers match their anchors; what blocks endorsement is in the
text and in two missing controls.

Standing rules: no `rm` outside `~/scratch/WS-NNN/`, no `sudo`; commits as Ravindu Somawansa, one line, no AI mention,
no session links; nothing posted outside the owner's repos; every number in the text comes from `numbers.json` through
`make check`; edit `DRAFT_4p.src.md` / `main.src.tex`, never `main.tex`. Commit at every milestone (K3).

## Part 1 — offline, $0

1. **No placeholders.** §4 contains `[to run]` for the three arm columns. Remove the sentence; state in Limitations and
   in the conclusion what is offline and what is not, with the arm results named as the longer version's addition.
   A paper with a placeholder is not sent to anyone.
2. **Citations inline.** `\nocite{*}` → real `\cite` at each trick the first time it is named (RTC 2506.07339,
   smooth chunking 2610.39451, horizon × depth 2610.32102, PACT-VLA 2610.28019, AAC 2604.04161, SmolVLA 2506.01844,
   TurboVLA 2607.27205, When-to-Switch 2610.05719, DREAM-Chunk 2606.18589, Act-while-waiting 2608.23831), plus
   vla.cpp (repo URL + commit), the Jetson Orin NX, the SO-101, LeRobot. Add the missing entries to `refs.bib` with
   authors (from the PDFs in `~/workspace/papers/`); drop `\nocite{*}` and any bib entry no sentence uses.
3. **Codenames out of the prose.** G13b, G-lat-2, A2, gate B, bar commits in the body → plain names in the text
   ("the chunk-boundary experiment", "the latency split") and an appendix table mapping plain name → repro folder →
   expected file → protocol commit → bar. The commit hashes move to that table only.
4. **Power mode once per number.** Every latency number carries "(25 W)" or "(MAXN)" the first time it appears in the
   abstract and in §2; one sentence in §2 says the two rows were measured in two modes and why. Fig. 1 and Fig. 3
   captions state the mode.
5. **Count and title.** "Seven tricks" everywhere (abstract says seven, §3 heading says seven, the introduction must
   not say six). The title promises "what transfers to the edge" while no closed-loop number exists: retitle to what
   is shown, e.g. "Vision is the bottleneck: measuring seven action-chunking tricks for a VLA on a Jetson Orin NX"
   (owner picks the final title; propose two in the log).
6. **Fig. 2 caption** must say that exact RTC guidance misses the 50 % bar; add the dashed bar line to the figure if
   it is not there. Fig. 3: say that AAC's and PACT's bars are "one chunk" and "298 ms" and that both miss.
7. **Tables.** One results table (trick · what it acts on · offline effect with CI · bar · verdict · cost per chunk on
   the Orin · mode) replaces the number-dense §3 paragraphs; the paragraphs keep one sentence each. Abstract ≤ 150
   words, ≤ 4 numbers (151/219 ms vision share, overwrite −72–74 %, seam jerk −83–87 %, N-sample methods pay N chunks).
8. **Prose and front matter** as in the Paper B item: full sentences, neutral voice, Related work paragraph (chunking
   tricks measured on desktop GPUs; edge inference engines; the SO-101 benchmarks), introduction a reader outside the
   project can follow, author block with affiliation + email + repo footnote, house style from WS-132.
9. `make check` green, CI green, CHANGELOG, `journal/papers/edge-inference/REVIEW_2026-11-02.md` with the commits.
   Push, log, then **stop, `waiting-owner`**: "Part 1 done; Part 2 needs `go rig` (MAXN, owner sudo) for the batched
   sampling control and `go arm` for the arm column; the repo is private — make it public before any endorsement
   request".

## Part 2 — gated

**2a. Batched sampling control (needs `go rig`; MAXN, $0).** The paper's "N-sample methods pay N chunks in series"
rests on vla.cpp sampling sequentially. The reviewer's question is whether that is the Orin or the engine. Frozen
protocol first (`frozen-protocol` skill, `repro/pact/PROTOCOL_BATCHED.md`): PyTorch SmolVLA on the Orin at MAXN,
one forward with a batch of 4 candidate chunks sharing the vision/prefill pass (the vision features computed once,
the denoising loop batched), median of ≥ 50 calls; bar = the batched cycle costs ≥ 2× one chunk (then the claim is
about the hardware); report also peak memory. Run (`gate-run`), rows to `expected/`, the number into §3 (PACT
paragraph) and the table whatever the result; if batching makes PACT cheaper than 2× a chunk, the recipe sentence
"do not sample several chunks per decision" is weakened to "on a sequential engine" and Limitations says so.

**2b. One arm column (needs `go arm`, after 2a).** The smooth-chunking gate B and the overwrite in the robot client
are already protocolled (`ws show WS-064`, `repro/smooth-chunking/PROTOCOL.md` gate B, `repro/chunk-boundary/`). Run
the smallest one that gives a closed-loop success column: 20 paired episodes, overwrite on/off, success + seam jerk,
bar as in the protocol. Then §4 gets one sentence with the arm result and the title can keep "transfers". Commit,
push, log, `waiting-owner`.
