# Claude Code prompt — Paper B (failure monitors / length null): make it endorsable

Repo: `/home/jetson/scratch/paper-repos/paper-reward-models-stopping-rule` (`ravediamond/paper-reward-models-stopping-rule`).
Journal side: `journal/papers/failure-monitors/` (memo, `REVIEW_2026-11-01.md`, `LENGTH_RESULTS.md`). Read first: the
repo's `README.md`, `BUILD.md`, `paper/DRAFT_4p.src.md`, `paper/numbers.json`, `paper/make_paper.py`, `paper/md2tex.py`,
`repro/robometer-judge/expected/g9a_ab_complete.json`, `repro/robometer-judge/PROTOCOL.md`.

Review of 2026-11-02 (chat, owner accepted). Every number in the built paper traces to its anchor; the problems are
structural. The paper is the strongest of the four and the first one to send to an endorser, so it goes first.

Standing rules: no `rm` outside `~/scratch/WS-NNN/`, no `sudo`; commits as Ravindu Somawansa, one line, no AI mention,
no session links; nothing posted outside the owner's repos; no verdict changed by hand — every number in the text comes
from `numbers.json`, which comes from `repro/*/expected/` through `make check`. The pipeline is
`DRAFT_4p.src.md → md2tex.py → main.src.tex → make_paper.py → main.tex → tectonic`; edit the sources, never `main.tex`.
Commit at every milestone (K3).

## Part 1 — offline, $0 (do all of it before any gated step)

1. **Robometer within policy is not pending.** `repro/robometer-judge/expected/g9a_ab_complete.json` → `complete` holds
   `within_policy_mean` 0.8187 and a `within_policy` block with one AUROC + CI per policy. Add the pair-weighted
   within-policy AUROC (same weighting as the length number, `len_within` in numbers.json; compute it in
   `l0_check.py` from the per-policy block and the per-policy success/failure counts) to `numbers.json` as `rbm_within`
   with its CI, and delete every "pending" in the abstract, §3, §6. If per-episode Robometer scores exist on the Orin
   (`~/robot-data/robometer/`), store them as rows under `repro/robometer-judge/expected/` and recompute pooled, within
   and the truncation column for Robometer from them; otherwise say in Limitations that Robometer's truncation
   column is not available (per-episode scores not stored), not "pending".
2. **Report Robometer's progress head.** Same file, `complete.baselines.last_progress_auroc` (0.875) beats the
   p_succ-based pooled number (0.818). Add it to §3 and Fig. 1 as a second Robometer bar ("Robometer-4B, last
   progress"), with the sentence that the protocol's primary Robometer score was p_succ (cite the PROTOCOL.md line) and
   that its progress head does better but still sits below length (0.938). If the CI for `last_progress_auroc` is not in
   the file, compute it with the episode bootstrap from the rows if they exist, else report it without CI and say so.
3. **Displayport task.** `per_task` shows `auroc: null` for "Push the Displayport cable…" (one class only). Say so in
   §2 (Data) in one clause and in the Fig. 1 caption.
4. **Bibliography.** Replace the bare-ID "References" list with a `refs.bib` + natbib (`plainnat`, numbered), one entry
   per cited work with authors, title, year, arXiv id, and **inline `\cite` at the claim** — every model and dataset
   named in the text gets a citation the first time it appears: ArmnetBench, SO-101 benchmark, Robometer, TOPReward,
   SARM / SARM2 / VLLR / STDR only where a sentence actually uses them (drop the rest from the list), FAIL-Detect,
   SAFE, FARM, ReAP, VLA-Corrector, Spotter, REMORA, No Free Checker, Flora-Rewarder-27B (NVIDIA model card or
   paper), Qwen3-VL-8B, Qwen3.5-27B / 9B, Gemini 3.8 Flash (Google model page), LeWM (the world model behind the
   surprise and drift monitors), TurboVLA, SmolVLA. Titles and authors from `~/workspace/papers/INDEX.md` and the
   PDFs; for model cards use the Hub / vendor page and the access date. `md2tex.py` must pass `\cite{}` through
   unchanged (extend it if it escapes braces).
5. **Codenames out of the prose.** G9c-3, G9a, G-flora, W1-A, REAP v1/v2 and similar: replace in the text with
   plain names ("the colour judge", "the Robometer run", "the Flora gate", "the world-model surprise monitor", "the
   risk head"), and add one table in an appendix (page 4 is free: the paper is 2 pages) mapping plain name → repro
   folder → expected file → bar commit. Keep the codes only there.
6. **Abstract.** Cut to ≤ 150 words and ≤ 4 numbers: the 0.851 half-length result, length 0.942 within policy vs the
   best reward model, the own-rollout regime (length at chance, judge at rest works), and the recommendation. All the
   other numbers move to a new Table 1 (ArmnetBench: length / Robometer p_succ / Robometer progress / TOPReward s_succ /
   TOPReward Yes-No, pooled and within policy, CI each) and Table 2 (own rollouts: judges at rest and monitors, caught /
   flagged / AUROC / Wilson / bar / in-sample threshold yes-no). Fig. 3 keeps the two-glyph split. Drop "separates
   every failure from every success" — lead with the threshold-free AUROC and its CI, then the in-sample operating point.
7. **Units.** In §5 the 9B and Gemini numbers are AUROCs next to 8/8 counts; give each model the same triple (AUROC,
   caught/flagged at its in-sample point).
8. **Prose pass.** Full sentences, neutral voice, no imperative sentences ("Report a length baseline…" → "We recommend
   reporting…"), no sentence that starts with a number, every claim stated on the 69 / 50 own rollouts carries
   "exploratory" or the n in the same sentence. Add a short Related work (one paragraph: reward models used as failure
   detectors; mid-episode monitors; benchmarks on the SO-101) and expand the introduction to say what a stopping rule
   is and why it matters, in a paragraph a roboticist outside this project can follow. Target 4 pages two-column with
   the appendix table.
9. **Front matter.** `\author{Ravindu Somawansa \\ Shisso Robotics, Paris \\ ravindu.somawansa@gmail.com}` and a footnote
   with the repository URL (`https://github.com/ravediamond/paper-reward-models-stopping-rule`) and the sentence that
   every bar commit named in the paper is in that repository's history. Keep the title.
10. **House style.** Apply `shisso.sty` and the matplotlib style from `journal/papers/style/` (WS-132): class, accent
    colour, logo on page 1, repo footer, figure palette. Regenerate the figures with the style (`make_figs.py` /
    the fig scripts in repro). No other decoration.
11. `make check` green (L0, numbers.json regenerated, PDF rebuilt), CI green, `CHANGELOG.md` entry, `REVIEW_2026-11-02.md`
    in `journal/papers/failure-monitors/` listing each point above with its commit. Log on the item, push, then
    **stop and set `waiting-owner`** with one line: "Part 1 done; Part 2 needs `go vast`; the repo is private — make it
    public before any endorsement request".

## Part 2 — gated: the fine-tuned Robometer against the length null (needs `go vast`, cap $5)

A Robometer-4B fine-tuned on ArmnetBench is public: `jesbu1/robometer-4b-fft-armnet-tiled` (base Qwen3-VL-4B-Instruct,
trained on `jesbu1/armnetbench_v01_tiled_so101`, Apache-2.0; its card reports Pearson 0.92 on single-arm SO-101). The
paper tests the zero-shot claim only; the obvious rebuttal is "use the released fine-tune". Frozen protocol first
(`frozen-protocol` skill, `repro/robometer-judge/PROTOCOL_FT.md`, committed before any score): same 2,047 episodes,
same top view, same inference code path as the zero-shot run (`scripts/score_robometer.py`, tiled input as the card
describes), primary = pooled AUROC of p_succ with the episode bootstrap, secondary = pair-weighted within policy and
last-progress; the bar is the paper's own length numbers (0.938 pooled, 0.942 within). **Leakage check in the protocol:**
list which ArmnetBench episodes are in the fine-tune's training set (read the card and `jesbu1/armnetbench_v01_tiled_so101`
splits); if the evaluation episodes overlap the training set, the comparison is reported as in-sample for the
fine-tune and the paper says so — that is itself the result. Run on vast (`gate-run` skill, the WS-127 fetch path),
rows to `repro/robometer-judge/expected/ft_rows.jsonl`, numbers into `numbers.json`, one paragraph in §3 and a row in
Table 1 whatever the outcome, Limitations updated. Commit, push, log, `waiting-owner`.
