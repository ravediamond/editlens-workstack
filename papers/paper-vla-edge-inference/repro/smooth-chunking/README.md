# WS-064 · Smooth MP chunking (arXiv 2610.39451) on SmolVLA + SO-101, training-free parts — gate A (offline)

Protocol `PROTOCOL.md` (frozen 2026-10-31, before any number). Scripts `scripts/smooth_chunking.py` (`4c421a7`),
clamp limits `results/clamp_limits.json` (`cbba80a`, from the demos, before any stream was scored). Paper: Nomura,
Osa, Kato, Ota, Shitanda, Harada, *Smooth Action Chunking via Movement-Primitive Representations for Imitation
Learning* (U. Tokyo / RIKEN AIP; no code found at freeze time).

## Claim tested

Two training-free parts of the paper: (a) projecting a predicted chunk onto n = 10 Gaussian (ProMP) bases makes the
chunk interior smooth at no cost in accuracy; (b) a closed-form via-point conditioning of the projected weights on
the last commanded action removes the seam between chunks without training (paper: 73–84 % of boundary jerk
removed). The MP retrain is not tested.

## Setup

SmolVLA `ravediamond/smolvla_2026-09-24_14-34-40` @ `c1d76f6` (H = 50, 30 Hz), PyTorch on the Orin, 10 Euler steps,
chunks from G13b's hook with its seed rule on the 20 G13b episodes of `ravediamond/so101_bowls_all` (G13b's
per-boundary rows were no longer on disk; regenerated, and S0 reproduces G13b's naive error exactly on 2 episodes).
Two geometries: s = 25 (overlap) and s = 50 (sync, how the arm runs). Streams: S0 raw stitch, S1 raw + linear blend
(s = 25 only), S2 projected (ridge λ = 10⁻⁶), S3 projected + conditioned (Σ_w = I, Σ*_y = 10⁻¹, gripper clamped
to its command floor). All in the policy's normalised action space; jerk = mean |Δ³| of the 5 arm joints at 30 Hz
(normalised units / s³), boundary = within ±2 steps of a seam; error = mean |commanded − recorded| in degrees (5 arm
joints); clamp proxy = per-joint step speed over 1.3 × the demos' 99.9th percentile + 0.15 rad/s.

Checks (2 episodes, before the full run): decoding the projection of a demonstrated chunk recovers it within 0.14°
mean (bar 0.5°); with Σ*_y → 0 the conditioned first row equals the via-point to 2 × 10⁻¹² (bar 10⁻⁶); S0 at
s = 25 reproduces G13b's naive error to 0.00° (bar 0.01°).

## Results (20 episodes; medians over episodes, `results/a_summary.json`; rows `results/a_rows.jsonl`)

| s | stream | within-chunk jerk | boundary jerk | error vs recorded (°) | clamp proxy / 100 steps | first-action change (°) |
|---|---|---|---|---|---|---|
| 25 | S0 raw | 1,432 | 3,744 | 1.703 | 4.31 | 0 |
| 25 | S1 raw + blend | 1,176 | 1,400 | 2.257 | 0.60 | 2.81 |
| 25 | S2 projected | 81 | 2,930 | 1.690 | 2.55 | 0.32 |
| 25 | S3 projected + Cond | 86 | 510 | 1.867 | 1.12 | 2.37 |
| 50 | S0 raw | 1,490 | 5,117 | 2.292 | 3.44 | 0 |
| 50 | S2 projected | 87 | 4,287 | 2.275 | 2.17 | 0.30 |
| 50 | S3 projected + Cond | 91 | 538 | 2.408 | 0.76 | 3.23 |

| bar | s = 25 | s = 50 | verdict |
|---|---|---|---|
| **A1** S2 − S0 error ≤ +0.30° (CI upper ≤ +0.50°) and S2 within-jerk ≤ 0.5 × S0 | −0.025° (CI −0.028 to −0.021), jerk × 0.057 | −0.020° (CI −0.023 to −0.018), jerk × 0.058 | **pass** |
| **A2** S3 boundary jerk ≤ 0.40 × S2 and S3 − S2 error ≤ +0.30° | × 0.174 (83 % removed), +0.184° (CI 0.136–0.232) | × 0.125 (87 % removed), +0.191° (CI 0.123–0.264) | **pass** |

**Verdicts: A1 pass, A2 pass.** Projection costs nothing against the recorded continuation (it is slightly closer)
and removes ~94 % of the within-chunk jerk; conditioning removes 83–87 % of the seam jerk, inside the paper's
73–84 % to slightly above it, at +0.19° error. By the decision rule gate B runs raw (S0) vs S3 on the arm.

**Descriptive, no bar.** S1 vs S3 at s = 25: blending leaves 2.74 × S3's boundary jerk and is 0.30° further from the
recorded continuation (CI 0.16–0.45). This is the opposite of the paper's Table II (blending wins on the seam where
an overlap exists); here the linear ramp sits on unsmoothed raw chunks. The clamp proxy falls from 3.44 to 0.76 per
100 steps at s = 50 (S0 → S3), the quantity B1 measures on the arm. The first action moves by 3.2° under
conditioning at s = 50: that is the pull towards the last action sent, by design.

**Exploratory (the paper's Σ*_y grid; the pre-registered value is 10⁻¹), boundary jerk median:**

| Σ*_y | 10⁻³ | 10⁻² | 10⁻¹ | 1 |
|---|---|---|---|---|
| s = 25 | 498 | 481 | 510 | 1,649 |
| s = 50 | 409 | 390 | 538 | 2,397 |

Error moves by < 0.1° across the grid; 10⁻³–10⁻¹ are equivalent on the seam and Σ*_y = 1 loses most of it. Not used
for any decision.

## What is not proven

Commanded stream only (no executed trajectory: the servo's own filtering is not modelled); training-set episodes
(the 20 G13b episodes are demos the policy was trained on); no closed loop (the observation never responds to the
smoothed command); the MP retrain is not tested. Gate B answers the first and third on the arm.
