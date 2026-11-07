<!-- copied verbatim from road-to-robotics projects/pact-vla/PROTOCOL_BATCHED.md, first committed 1d7e6c4, deviations 9b5b8db and 24cf97b -->

# Batched sampling control for "N-sample methods pay N chunks" (WS-134 Part 2a): protocol, frozen 2026-11-05 before any number

Owner (chat, 2026-11-05): "do the engine work that does not need me yet tonight". Bar and design from the WS-134 prompt, part 2a (`journal/prompts/2026-11-02_paper_fix_edge_inference.md`).

## Question

The paper says that speculative selection (N = 4 candidates) and adaptive length (N = 20 samples) "pay for N chunks in series". That rests on vla.cpp, which samples one candidate at a time and has no batched path. Is the series cost a property of the Orin or of the engine? The control samples N candidate chunks for one observation in PyTorch on the Orin, sharing the vision and prefill pass and batching the denoising loop, and compares its cost with one chunk.

## Data and setting

- Policy `ravediamond/smolvla_2026-09-24_14-34-40` @ `c1d76f6`, PyTorch LeRobot in `lerobot-jetson:rc` (`LEROBOT_SRC=image`), as in `projects/pact-vla/PROTOCOL.md`. 10 Euler steps, chunk H = 50.
- Observations: five frames of `ravediamond/so101_bowls_all`, the first five episodes of the G13b list (seed 0), each at t = 50 (the frame the gate A ratio used for the first one). Each frame gives all three timings below.
- Orin NX 16 GB at MAXN_SUPER with `jetson_clocks`, inside the 01:00 to 08:00 Paris window (`ws power` says `window=open`, `nvpmodel -q` says MAXN_SUPER). The profile is recorded next to every number. Nothing else on the GPU: the EditLens scorer is stopped and `ws jobs` shows no running job. A run is aborted if the GPU temperature reaches 90 °C.

## Quantities (milliseconds, `torch.cuda.synchronize()` before and after, 5 warm-up calls then 50 timed calls per frame, median)

- **T1**, one chunk: prefix (vision encoder and prefill, KV cache) plus 10 denoising steps at batch 1.
- **T_prefix**: the prefix alone.
- **T_seq(N)**, N chunks in series as vla.cpp does: N × T1 measured as N separate calls of the T1 function.
- **T_shared(N)**: prefix once, then N denoising loops at batch 1 one after the other.
- **T_batch(N)**: prefix once, KV cache and padding mask expanded along the batch dimension to N (the expansion is inside the timed call), then one denoising loop at batch N. N = 4 (speculative selection) and N = 20 (adaptive length).
- Peak GPU memory (`torch.cuda.max_memory_allocated`) of the T_batch(N) calls, with the baseline model memory subtracted and reported separately.

## Checks before any timing

- **C1 parity.** With identical noise, row i of the batched result equals the batch-1 result for the same noise: mean absolute difference ≤ 1e-3 and maximum ≤ 2e-2 in the model's normalised action space, for N = 4, on two frames. If this fails the sampler is fixed (a deviation is written down) before any timing is taken.
- **C2 harness.** T1 reproduces the gate A step ratio setting: the batch-1 denoising step at the frame of `pact_latency.py ratio` is within 25 % of `projects/pact-vla/results/ver_ratio.json` `pytorch_step_ms` (same board, the numbers are not expected to be identical).
- **C3 shapes** printed once: prefix KV shape, expanded KV shape, output (N, 50, 32).

## Bars (from the prompt, part 2a)

- The cost of N samples on this hardware is **N chunks in series** (the paper's claim stands as a statement about the hardware) if the median over the five frames of T_batch(4) / T1 is **≥ 2.0**.
- If it is **< 2.0**, the claim is a property of a sequential engine, the recipe sentence "do not sample several chunks per decision" is weakened to "on a sequential engine", and Limitations says so.
- T_batch(20) / T1, T_shared(N) / T1 and the peak memory are descriptive. They are reported whatever they are.

## Reading and reporting

The result goes into §3 (the speculative-selection paragraph) and the results table whichever way it falls, as "PyTorch on the Orin, MAXN_SUPER". The vla.cpp numbers already in the paper stay as they are and are labelled with their engine. The batched number is not a vla.cpp number.

## Deviations

1. **2026-11-05, before any timing number.** The first run of the checks (quiet 25 W profile, `--checks`) gave C3 shapes as expected (prefix cache 139 tokens, 16 layers, expanded to batch 4 by `batch_repeat_interleave` on a copy) and C1 parity in the working precision of mean 1.04e-3 and max 5.9e-3 against a mean tolerance of 1e-3, a miss of 4 %. The same comparison with the whole policy cast to float32 (new check C1b) gives mean 1.6e-7 and max 1.2e-6, so the batched sampler is correct and the difference in the working precision is rounding of the lower-precision path. Change: C1 keeps its maximum tolerance (2e-2) and its mean tolerance becomes 3e-3; C1b is added with mean ≤ 1e-4 and max ≤ 1e-3 in float32 and must pass before any timing (`--run` refuses to time without a passing `batched_checks.json`). C2 at the quiet profile gave a batch-1 step of 123.6 ms against the gate A reference of 63.8 ms; C2 is judged at MAXN_SUPER in the window, where it must be within 25 % before any timing is kept. No timing of T1, T_seq, T_shared or T_batch exists at this point.

2. **2026-11-06 01:10, MAXN_SUPER in the window, before any timing is kept.** The first `--run` took the C2 step through `denoise_step` called directly and got 98.7 ms against the 63.8 ms reference, so the run refused to time (as the protocol says). A diagnostic at MAXN_SUPER (GPU at 1173 MHz, nothing else running) showed that the reference path, `m.velocity` as `pact_latency.py ratio` used, gives 64.7 ms now (1.4 % from the reference), that the direct call gives 98.7 ms as the first measurement after the model loads and 76 to 78 ms later, and that the cache does not grow (seq_len 139 throughout). So the harness is slow to warm up and drifts, not the board. Changes, none of them to a bar: (a) C2 is judged through `m.velocity`, the function the reference used, after 15 warm-up calls, and the direct step is reported as descriptive; (b) the timings are taken interleaved, every round timing each variant once in random order, so drift affects all variants alike, with 15 warm-up rounds and a 5 s burn-in first; (c) N = 4 variants and T1 use 50 rounds, the N = 20 variants (descriptive) use 20 rounds. No timing of T1, T_seq, T_shared or T_batch has been kept.

## Exploratory

The choice of five frames, the parity tolerances and the 90 °C abort are fixed here, before any number. Anything added after data is labelled exploratory.
