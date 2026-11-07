# Reproduce

## L0
```bash
python3 l0_check.py
```
Recomputes the per-stream medians over the 20 episodes and the A1 / A2 ratios and verdicts from `expected/a_rows.jsonl`; paired-difference CIs are read from `expected/a_summary.json`.

## L1 (Orin NX, PyTorch, ~1 h)
`scripts/smooth_chunking.py chunks|checks|score` with SmolVLA `ravediamond/smolvla_2026-09-24_14-34-40` @ `c1d76f6` on the 20 G13b episodes of `ravediamond/so101_bowls_all` (needs the research repo's G13b hook, `scripts/run_g13b_rtc_offline.py`; status: not re-verified from this folder).

## L2
Gate B (raw vs S3 on the arm) not run.
