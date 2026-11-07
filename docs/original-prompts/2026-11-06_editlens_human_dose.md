# Claude Code prompt — WS-166: human-edit dose–response of the open EditLens score (paper-editlens-sensitivity)

Owner (chat 2026-11-06): the EditLens paper is reframed. Not "how do our papers pass the detector" but: *same edit magnitude,
opposite direction — does the open EditLens 3B score fall when a human edits an AI-drafted paragraph as much as it rises
when an AI edits a human paragraph, or does it track the last editor?* Data for the human direction = the owner's own
hand rewrites of the four papers, one commit per editing session, over the coming weeks. Only the local 3B model until the
curve is readable; the production Pangram API once, at the end, under the gate in the protocol.

Everything is in `~/scratch/paper-repos/paper-editlens-sensitivity/repro/human-dose/` (committed 2026-11-06, `main`):
`PROTOCOL.md` (question, data, metric, nulls, bars B1–B4, the production-run gate, checks before numbers), `REPRODUCE.md`
(the command list), `scripts/` (snapshot, align, magnitude, score_versions, ai_curve, analyze), `l0_check.py`.

Standing rules: no `rm`/`sudo`/interactive (rm only in `~/scratch/WS-166/`); no vast, no arm; nothing posted outside the
owner's repos; never call the Pangram paid API in this item (that is a later item, after the gate); the HF token is never
printed or committed; commits as Ravindu Somawansa, one line, no AI mention, no session links; `git pull --rebase` before
every push. **Do not edit any paper text**: the versions must be the owner's hand edits only; `[polish]` commits and
commits by any other author are excluded by `snapshot.py`.

## Step 0 — bars (stop here first)

The bars in `PROTOCOL.md` §5 are *proposed* (source: chat 2026-11-06, Claude draft). Frozen-protocol step 3: a bar not
given by the owner is not a bar. Set `status=waiting-owner`, `needs-from-owner: confirm or change PROTOCOL.md §5 (B1–B4,
the production gate) and the bin edges of §3; then say 'WS-166 go'`. Add the HUMAN.md line. Do nothing else until the go.

## Step 1 — freeze (on 'go')

1. Run the `protocol-readback` subagent on `PROTOCOL.md`; fix wording ambiguities only (never a threshold); open items in
   the item log.
2. `cd ~/scratch/paper-repos/paper-editlens-sensitivity && git pull --rebase`; commit `WS-166: protocol frozen (before any number)`;
   push; record the hash in the item log and in `journal/workstack/notes/WS-166.md`.
3. `ws paper-polish serve` (the 3B model; wait for free memory ≥ 9 GB as in WS-162, never kill another process).
4. In the `editlens` venv (`~/venvs/editlens/bin/python`), install `sentence-transformers` if missing (pin it in
   `requirements-editlens.txt` of road-to-robotics; nothing else changes in that venv). First run of `magnitude.py`
   downloads `Qwen/Qwen3-Embedding-0.6B` (~1.2 GB) and `all-MiniLM-L6-v2`.
5. `snapshot.py --freeze` — prints the four baseline commits and paragraph counts (about 50 in total). These must be the
   repos' HEAD *before* any hand edit: if any paper repo already has a commit by the owner touching `paper/DRAFT_4p.md`
   after 2026-11-06 09:00 Paris, stop and ask which commit is the baseline (`needs-from-owner`).
6. `magnitude.py --selftest` (want SELFTEST PASS), `ai_curve.py --columns` (writes `expected/ai_route.json`; paste the
   columns into the notes). Commit `expected/baseline.json` and `ai_route.json`: `WS-166: baselines frozen, AI route chosen`.
7. `ai_curve.py` (600 rows, ~20–40 min at 25 W with the magnitude models; detach with nohup, pid in `runs/WS-166/`).
   Commit `expected/ai_rows.json`. If the route is `fallback`, stop: `needs-from-owner: go for the fallback (Anthropic key,
   ~$3, 300 paragraphs)`.
8. `score_versions.py` once on the baselines alone (identity null); report the mean |diff| in the log. If it is ≥ 0.01 the
   production gate cannot open: say so.
9. `ws human add --type do --ask "Hand-rewrite paragraphs of the four papers, commit per session (optional [reword]/[content] in
   the subject), no scorer open while editing; say 'WS-166 batch' after each batch"` blocked by nothing; status `waiting-owner`.

## Step 2 — each batch (on 'WS-166 batch')

`git pull` the four paper repos; `snapshot.py`, `align.py --check` (paste merges/new into the log), `align.py`, `magnitude.py`,
`score_versions.py`, `analyze.py --progress`. Commit `expected/*.json` as `WS-166: batch <date>, <n> covered paragraphs`.
Report in the log: covered paragraphs (of ~50; need 40), rows per bin, which bins are evaluable. No interpretation yet.
Back to `waiting-owner`.

## Step 3 — the curve (when `analyze.py --progress` shows ≥ 40 covered and ≥ 3 evaluable bins)

`analyze.py`; `make l0`; commit `expected/summary.json`: `WS-166: curve, <k> bins evaluable`. Result line, with every number
citing `expected/summary.json`: per-bin R with CI, verdicts B1–B4, the first bin where half of the versions fall below the
human p90, the production gate value. Then `status=done` with `needs-from-owner: production run is a new item (WS-167:
same ids through the Pangram API, cap $25) — say go`. Do not write paper prose in this item; the paper is rewritten by
the owner.

## Stop points

Memory < 9 GB for 10 min → log and stop. Any model download refused (gated) → `waiting-owner` with the URL to accept.
`snapshot.py` finding fewer than 35 baseline paragraphs → stop and ask (the 40-word cut may need a look, a threshold change
is a numbered deviation signed by the owner).
