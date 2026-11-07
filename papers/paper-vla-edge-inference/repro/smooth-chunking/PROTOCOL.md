<!-- copied verbatim from road-to-robotics projects/smooth-chunking/PROTOCOL.md, first committed 6f58d7b -->

# Smooth MP chunking (2610.39451) on SmolVLA + SO-101: protocol (frozen 2026-10-31, before any number)

Paper: Nomura, Osa, Kato, Ota, Shitanda, Harada, *Smooth Action Chunking via Movement-Primitive Representations for
Imitation Learning*, arXiv 2610.39451v1 (29 Oct 2026), U. Tokyo / RIKEN AIP. No code found at freeze time. Analysis:
`journal/queue/2026-10-31_two_papers.md` §1. Draft: `journal/drafts/2610.39451.md`.

## Question

On this rig (SmolVLA, H = 50 at 30 Hz, sync s = 50 on the arm, s = 25 offline), do (a) projecting the predicted chunk
onto n = 10 ProMP bases and (b) training-free via-point conditioning at the seam reduce commanded jerk without
raising the error against the recorded continuation, and on the arm reduce clamp events and executed vibration at
non-inferior success? The MP *retrain* is not tested: only the training-free parts of the paper.

## Decision rule

- A1 pass and A2 pass and B1 pass → projected + conditioned chunks become the sync default on the Orin (vla.cpp
  client-side post-processing and the PyTorch fallback), written into the deploy config and DECISIONS.md.
- A1 fail (projection costs accuracy) → nothing adopted; B is not run; published as "does not transfer".
- A1 pass, A2 fail (seam not removed) → projection may still be adopted for the interior if B1 passes with projection
  alone; the item then runs B with raw vs projected only.
- B1 fail → nothing adopted; published as "does not transfer".

## Fixed setup

- Policy `ravediamond/smolvla_2026-09-24_14-34-40` @ `c1d76f6` (H = 50), PyTorch via `scripts/run_g13b_rtc_offline.py`'s
  hook for gate A (chunks are the same ones G13b generated: seed per boundary as that script, 10 Euler steps).
- Episodes and boundaries: the 20 G13b episodes of `ravediamond/so101_bowls_all` (seed 0 list), s = 25 → 254
  boundaries; and s = 50 → the 50-step seams of the same episodes (≈ 127).
- Basis: n = 10 Gaussian bases over the chunk phase τ ∈ [0, 1], centres uniform, σ = half the centre spacing, rows
  normalised to sum to one (paper §V-A.1). Projection of a raw chunk A ∈ R^{50×6} by ridge regression, λ = 10⁻⁶:
  ŵ = (ΨᵀΨ + λI)⁻¹ΨᵀA, decoded as Ψŵ. Computed in the policy's normalised action space.
- Conditioning (paper Eq. 3–4): m = 1 via-point = the previous chunk's last commanded action (at the seam), Σ_w = I,
  Σ*_y = 10⁻¹ (normalised units), K precomputed. Applied per action dimension, gripper included then clamped to its
  command floor.
- Blending (+WS, s = 25 only): linear ramp from the previous to the new chunk over the 25-step overlap, on raw chunks
  (as the paper's raw+WS cell).
- Jerk: mean |third finite difference| of the commanded 5 arm joints at 30 Hz, normalised action units per s³, gripper
  excluded. Within-chunk = samples more than 2 steps from a seam; boundary = samples within ±2 steps of a seam.
- Clamp proxy: per joint, limit = 1.3 × the 99.9th-percentile speed of that joint in `so101_bowls_all` + 0.15 rad/s;
  an event = a commanded step whose displacement exceeds it. Computed once on the demos, committed before any
  stream is scored.
- Error vs the recorded continuation: the G13b metric (mean |commanded − recorded| in degrees over the executed
  window, 5 arm joints).
- Statistics: episode bootstrap, 2,000 resamples, seed 0, 95 % CIs on paired differences.

## Gate A — offline, $0 (Orin, PyTorch, nothing moved)

Streams at s = 25 (overlap): S0 raw naive stitch, S1 raw + WS, S2 projected, S3 projected + Cond.
Streams at s = 50 (sync, no overlap): S0 raw, S2 projected, S3 projected + Cond.

Per stream and geometry: within-chunk jerk, boundary jerk, clamp-proxy events per 100 steps, error vs recorded, and
the first-action change |a₀(stream) − a₀(raw)| in degrees (descriptive).

**Bar A1 (projection is free):** at both geometries, S2 error vs recorded − S0 error ≤ +0.30° (paired CI upper bound
≤ +0.50°) AND S2 within-chunk jerk ≤ 0.5 × S0. FAIL if the error rises > 0.50° (point estimate) at either geometry.

**Bar A2 (conditioning removes the seam without training):** S3 boundary jerk ≤ 0.40 × S2 boundary jerk at s = 25 and
at s = 50 (paper: 73–84 % removed), with S3 error vs recorded − S2 error ≤ +0.30°. FAIL if < 40 % removed at s = 50
(the geometry the arm uses).

**Descriptive, no bar:** S1 vs S3 at s = 25 (the paper's finding that blending wins on the seam); clamp proxy per
stream; the paper's Σ*_y grid {10⁻³, 10⁻², 10⁻¹, 1} as exploratory, the pre-registered value is 10⁻¹.

**Checks before any number is read:** (1) decoding the projection of a demonstrated chunk recovers it within 0.5°
mean (basis sanity); (2) with Σ*_y → 0 the conditioned chunk's first row equals the via-point to 10⁻⁶ (conditioning
sanity); (3) raw S0 at s = 25 reproduces G13b's naive error on 2 episodes to 0.01° (same chunks).

## Gate B — on the arm (`go arm WS-064`, only if A1 passes)

Sync s = 50, vla.cpp, raw (S0) vs the adopted stream (S3 if A2 passed, else S2), post-processing applied client-side
to the returned chunk before it is sent to the arm. 20 + 20 trials on the first 20 rows of the §29 sealed
`LAYOUTS.csv`, arm order alternating per layout, owner labels at rest blind to arm. Rig check first (motors off:
post-processing latency ≤ 2 ms per chunk, recorded).

Per trial: success, clamp-proxy events on the commanded stream, executed 1–5 Hz band jerk from the recorded
`observation.state` velocity (band-pass, mean |d/dt|), G14 oscillation flag on the executed trajectory.

**Bar B1 (non-inferior and quieter):** successes(S3) ≥ successes(S0) − 1 AND median clamp-proxy events per trial
(S3) ≤ 0.5 × S0 with paired CI upper bound < 1.0. "Not proven: ceiling" if S0 ≥ 18/20 and clamps already ≤ 1 per
trial. Executed band jerk and oscillation rate are reported with CIs, no bar.

## Notes

The paper's own stronger seam method, +WS, cannot run on the arm here (sync, no overlap); that is the register's
condition line. The MP retrain is a separate decision, taken only if gate A shows the interior error vs recorded is
where S0 loses against the demos — not expected. Anything decided after this commit is exploratory.

## Cost

$0. Gate A ≈ 1–2 h Orin (chunks regenerated once if G13b's per-boundary rows are not on disk; they are in
`outputs/g13b_offline/` on the Orin). Gate B: one robot session, 40 trials.

## Outputs

`projects/smooth-chunking/README.md`, `projects/smooth-chunking/results/` (`a_rows.jsonl` per boundary and stream,
`a_summary.json`, `clamp_limits.json`, `b_trials.csv`), EXPERIMENTS.md §2 rows, draft sections 5–8.
