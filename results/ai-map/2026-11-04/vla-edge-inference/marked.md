# paper-vla-edge-inference: chunks in paper order

## rendered source (numbers filled)

### Abstract (mean 0.310)

<!-- editlens chunk 0.310 lines 9-17 -->
<!-- editlens paragraph 0.310 lines 9-17 -->
Training-free tricks promise faster or smoother execution of flow-matching vision-language-action policies. They are measured on desktop GPUs. We re-measure seven of them where a low-cost robot actually runs: a 450M SmolVLA on a Jetson Orin NX, one checkpoint, the same 20 recorded episodes, a bar committed before each run. On this board the chunk is dominated by a cost most tricks never touch — the vision encoder alone takes 151.0 of 219.0 ms of server time per action chunk (25 W). What survives acts on the chunk seam. A gradient-free prefix overwrite cuts the boundary jump by 72–74 % (25 W), and movement-primitive seam conditioning removes 83–87 % of the seam jerk. Sampling does not transfer: every N-sample method pays N chunks in series on a sequential edge engine. The recipe is short. Overwrite the prefix, smooth the seam, leave the sampler alone.

### 1 Introduction (mean 0.278)

<!-- editlens chunk 0.278 lines 21-28 -->
<!-- editlens paragraph 0.278 lines 21-28 -->
Robot-learning papers that speed up or smooth action chunking report their latencies on desktop and data-centre GPUs (RTX 4090, A100, H100, RTX 5090), where a chunk costs tens of milliseconds and spare compute can hide an extra pass. The robots people can buy run their policies on edge GPUs. Our setup is one of those: an SO-101 arm [arXiv:2606.08881], a Jetson Orin NX 16 GB, and SmolVLA [arXiv:2506.01844] served through a C++ engine (vla.cpp) on episodes recorded with LeRobot. For each of seven published tricks we ask the question its paper does not. How much of the benefit survives where the chunk is dominated by a cost the trick never touches? Each answer is a gate with a bar committed before the number, an episode bootstrap for offline effects, and medians of ≥ 50 calls for latency; the appendix maps every number to its result file and protocol commit.

### 2 Where the time goes (mean 0.298)

<!-- editlens chunk 0.298 lines 32-37 -->
<!-- editlens paragraph 0.298 lines 32-37 -->
A chunk at ten Euler steps costs 237.5 ms end to end on the Orin at full power (MAXN_SUPER): 150.7 ms of vision, 14.9 ms of prefill and 5.3 ms per denoise step (Fig. 1). At 25 W the server-side split is 151.0 ms of vision in 219.0 ms. Two power modes appear in this paper because each gate's protocol froze the mode it ran in: the serving split and the boundary experiments at 25 W, the latency experiments at full power. Every number carries its mode. Any trick that only touches the denoising loop works on at most a quarter of the chunk.

### 3 Seven tricks, one checkpoint (mean 0.407)

<!-- editlens chunk 0.407 lines 43-65 -->
<!-- editlens paragraph 0.436 lines 46-49 -->
**Prefix overwrite vs exact real-time chunking** [arXiv:2506.07339]. Overwriting the new chunk's executed prefix with the committed actions passes the 50 % jump-cut bar at every delay, in PyTorch and in vla.cpp for 0.4 ms per chunk, while the exact guided inpainting of real-time chunking cuts less than the bar and costs 1.9× a naive chunk (Fig. 2).

<!-- editlens paragraph 0.400 lines 51-53 -->
**Movement-primitive projection and seam conditioning** [arXiv:2610.39451]. Both pass their bars: projecting each chunk onto ten Gaussian bases stays within the error bar while removing within-chunk jerk, and conditioning on the last action sent removes most of the seam jerk at +0.19° of error.

<!-- editlens paragraph 0.445 lines 58-61 -->
**Speculative chunk selection** [arXiv:2610.28019]. Choosing among four candidates with the pre-commit frame picks chunks closer to the recorded teleop continuation (one recorded continuation per frame, training-set episodes, open loop), but vla.cpp samples sequentially: a cycle costs 1,200 ms and 37 control ticks against 8, so the paper's "no added control-step delay" fails (Fig. 3).

<!-- editlens paragraph 0.420 lines 63-65 -->
**Entropy-adaptive chunk length** [arXiv:2604.04161]. The chosen length sits at its floor in both task phases, the boundary jump does not improve over fixed chunks with overwrite, and one 20-sample decision costs 4,751 ms against a 298 ms bar (Fig. 3).

### 4 The recipe, and what does not transfer (mean 0.420)

<!-- editlens chunk 0.420 lines 85-91 -->
<!-- editlens paragraph 0.420 lines 85-91 -->
Turn on the prefix overwrite and the primitive projection with seam conditioning: both act on the seam, which the vision cost does not hide, and both cost under a millisecond. Keep ten Euler steps, by the protocol's rule (the two-step contraction is not proven) rather than because the saving is unreal: it is real but small because vision dominates. Do not sample several chunks per decision on a sequential edge engine: every N-sample method (exact guidance, speculative selection, adaptive length) pays N chunks in series. This version is offline and latency only; the closed-loop arm columns (seam smoothing and the overwrite in the robot client) are the planned addition of the longer version.

### 5 Related work (mean 0.189)

<!-- editlens chunk 0.189 lines 95-101 -->
<!-- editlens paragraph 0.189 lines 95-101 -->
Other chunking tricks are also reported on desktop-class GPUs: extending the executing chunk instead of resampling [arXiv:2610.05719], reactive chunking driven by a latent world model [arXiv:2606.18589], and fine-tuning the policy for latency with reinforcement learning rather than leaving it fixed [arXiv:2608.23831]. On the engine side, TurboVLA [arXiv:2607.27205] pushes VLA throughput on a desktop GPU, while vla.cpp runs them on edge boards. On the same arm, a standardized benchmark reports failure and recovery of VLA policies [arXiv:2606.08881] and a fleet of SO-101 cells evaluates policies at scale [arXiv:2607.24481]; they evaluate policies, we re-measure the execution tricks around them under bars fixed before the run.

### 6 Limitations (mean 0.267)

<!-- editlens chunk 0.267 lines 105-110 -->
<!-- editlens paragraph 0.267 lines 105-110 -->
One policy (SmolVLA, 450M); π0-class models do not fit the Orin, which is itself part of the condition. vla.cpp is the author's own port: it is measured against PyTorch on the same board (parity and determinism checks in the gate logs), but an independent engine might move the sequential-sampling costs — in particular, a batched sampler could cut the N-sample cost, and that control has not been run. Power mode is a confound: latency rows are at MAXN_SUPER, the serving and boundary rows at 25 W. One task family (bowls), offline episodes for every effect except latency; no arm success column yet (smooth-chunking gate B, the overwrite in the robot client).

### Appendix: from plain name to gate (mean 0.172)

<!-- editlens chunk 0.172 lines 114-114 -->
Every number in this paper is recomputable from the repository; this table maps each experiment to its files.

### (figure and table captions) (mean 0.284)

<!-- editlens chunk 0.284 lines 39-81 -->
Fig. 1 — where a SmolVLA chunk's time goes on the Orin NX (vla.cpp, ten Euler steps, MAXN_SUPER)
Table 1: Seven tricks on one checkpoint: what each acts on, the measured offline effect, the pre-registered bar, the verdict, and its cost on the Orin NX. Modes: serving and boundary rows 25 W, latency rows MAXN_SUPER.
Fig. 2 — median boundary-jump cut against naive asynchronous execution (254 boundaries per delay; PyTorch and vla.cpp, 25 W). Exact RTC guidance misses the 50 % bar at every delay.
Fig. 3 — cost per decision on the Orin NX (log scale, MAXN_SUPER). The dashed line is AAC's 298 ms bar; PACT's bar is one chunk (237.5 ms); both miss.

## built PDF

### Abstract (mean 0.244)

<!-- editlens chunk 0.244 lines 12-59 -->
<!-- editlens paragraph 0.263 lines 12-26 -->
Training-free tricks promise faster or smoother execution of flow-matching vision-language-action policies, and they are measured on desktop GPUs. On a Jetson Orin NX, a 450M SmolVLA spends 151.0 of 219.0 ms of server time per action chunk in its vision encoder (69 %, at 25 W). We measured seven of these tricks with one checkpoint, the same 20 recorded episodes and bars committed before each run. A gradient-free prefix overwrite cuts the boundary jump by 72–74 % for 0.4 ms per chunk; projecting each chunk onto ten movement primitives with a via-point at the seam removes 83–87 % of the seam jerk at +0.19◦ of error. Two Euler steps instead of ten save 41 ms (at MAXN) (17 %). Exact real-time chunking costs 1.9× a chunk; speculative selection (PACT) 1,200 ms per cycle, 37 control ticks instead of 8; entropy-adaptive chunking 4,751 ms per decision. On the edge, overwrite the prefix, smooth the seam, and leave the sampler alone.

<!-- editlens paragraph 0.259 lines 53-59 -->
Figure 1: Where a SmolVLA chunk’s time goes on the Orin NX (vla.cpp, ten Euler steps). × depth A2). At 25 W the server-side split is 151.0 ms of vision in 219.0 ms (G-lat-2, bar commit 82fdc15). Any trick that only touches the denoising loop works on at most a quarter of the chunk.

### 3 Seven tricks, one checkpoint (mean 0.201)

<!-- editlens chunk 0.201 lines 62-64 -->
All offline effects use the same SmolVLA checkpoint and the same 20 recorded episodes (254 chunk boundaries

### 1 Introduction (mean 0.267)

<!-- editlens chunk 0.267 lines 65-88 -->
<!-- editlens paragraph 0.267 lines 65-88 -->
per delay). Prefix overwrite vs exact real-time chunking (G13b). Robot-learning papers that speed up or smooth action Overwriting the new chunk’s executed prefix with the chunking report their latencies on desktop and datacommitted actions cuts the median boundary jump by centre GPUs (RTX 4090, A100, H100, RTX 5090), where a 73 / 74 / 72 % at delays of 8 / 12 / 20 steps (bar ≥ 50 %); chunk costs tens of milliseconds and spare compute can the exact guided inpainting of real-time chunking cuts it hide an extra pass. The robots people can buy run their by 29 / 31 / 21 % and costs 1962 ms per chunk in PyTorch policies on edge GPUs. We take one such setup — an against 1028 ms naive (1.9×). Ported to vla.cpp, the overSO-101 arm, a Jetson Orin NX 16 GB, SmolVLA through write cuts 71 / 73 / 72 % for 0.4 ms per chunk (Fig. 2). a C++ engine (vla.cpp) — and ask, for each trick, the Movement-primitive projection and seam conditionquestion its paper does not: how much of its benefit suring (smooth chunking, bar commit 6f58d7b). Projectvives where the chunk is dominated by a cost the trick ing each chunk onto ten Gaussian bases changes the erdoes not touch. Each answer is a pre-registered gate: a ror against the recorded continuation by -0.020◦ and rebar committed before the number, an episode bootstrap moves 94 % of the within-chunk jerk; conditioning on the for offline effects, medians of ≥ 50 calls for latency. last action sent removes 83 % (25-step overlap) and 87 % (sync) of the seam jerk at +0.19◦. Both pass their bars. Two Euler steps (horizon × depth, bar commit

### 2 Where the time goes (mean 0.188)

<!-- editlens chunk 0.188 lines 89-118 -->
<!-- editlens paragraph 0.178 lines 89-93 -->
0a79846). Two steps contract the action cloud to 0.78 of A chunk at ten Euler steps costs 237.5 ms end to end on its ten-step radius (CI 0.73–0.81; bar ≤ 0.70, paper 0.51): the Orin at full power (MAXN): 150.7 ms of vision, 14.9 not proven. They save 41 ms per chunk (196.1 vs 237.5 ms of prefill and 5.3 ms per denoise step (Fig. 1; horizon ms, ratio 0.83).

<!-- editlens paragraph 0.289 lines 112-118 -->
dominates. Do not sample several chunks per decision on a sequential edge engine: every N-sample method (exact guidance, PACT, AAC) pays N chunks in series. Arm results for the three transferring tricks are [to run] (smooth chunking gate B, horizon × depth gate B, the overwrite in the robot client); they are the whole addition of the 8-page version.

### 5 Limitations (mean 0.156)

<!-- editlens chunk 0.156 lines 131-132 -->
Figure 2: Median boundary-jump cut against naive asynchronous execution, 254 boundaries per delay.

### 2 Euler steps (mean 0.177)

<!-- editlens chunk 0.177 lines 145-184 -->
<!-- editlens paragraph 0.318 lines 145-155 -->
One policy (SmolVLA, 450M); π0 -class models do not fit the Orin, which is itself part of the condition. vla.cpp is the author’s own port: it is measured against PyTorch on the same board (parity and determinism checks in the gate logs), but an independent engine might move the sequential-sampling costs. Power mode is a confound: latency rows are at MAXN_SUPER unless stated, the G13b and G-lat-2 rows at 25 W. One task family (bowls), offline episodes for every effect except latency; no arm success column yet.

<!-- editlens paragraph 0.180 lines 167-184 -->
Figure 3: Cost per decision on the Orin NX; dashed: AAC’s pre-registered bar. Speculative chunk selection (PACT-VLA, bar commit 0a79846). Choosing among four candidates with the pre-commit frame picks chunks closer to the recorded teleop continuation (-0.27◦ against a random pick, CI -0.44 to -0.09; one recorded continuation per frame, training-set episodes, open loop), but vla.cpp samples sequentially: the cycle costs 1,200 ms against 237.5 ms, 37 control ticks against 8, so ”no added control-step delay” fails. Entropy-adaptive chunk length (AAC, bar commit 581a955). The chosen length sits at its floor in both phases (median 2 steps in transport and 2 at the grasp), the median boundary-jump ratio with overwrite (the step at the seam over the median step inside the chunk; lower is better) is 0.973 against 0.940 for fixed chunks, and one decision with 20 samples costs 4,751 ms against a 298 ms bar (Fig. 3).

### 4 The recipe, and what does not transfer (mean 0.228)

<!-- editlens chunk 0.228 lines 186-191 -->
<!-- editlens paragraph 0.228 lines 186-191 -->
Turn on the prefix overwrite and the primitive projection with seam conditioning: both act on the seam, which the vision cost does not hide, and both cost under a millisecond. Keep ten Euler steps, by the protocol’s rule (the two-step contraction is not proven) rather than because the saving is unreal: it is real but small because vision
