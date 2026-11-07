# paper-vla-edge-inference: chunks in paper order

## rendered source (numbers filled)

### Abstract (mean 0.267)

<!-- editlens chunk 0.267 lines 9-16 -->
<!-- editlens paragraph 0.267 lines 9-16 -->
Training-free tricks that make flow-matching vision-language-action policies faster or smoother are measured on desktop GPUs. We re-measured seven of them where a low-cost robot actually runs its policy: a 450M SmolVLA on a Jetson Orin NX, with one checkpoint, the same 20 recorded episodes and a bar committed before each run. On this board the vision encoder alone takes 151.0 of 219.0 ms of server time per action chunk (25 W), a cost most of the tricks never touch. The tricks that survive act on the seam between chunks. A gradient-free prefix overwrite cuts the boundary jump by 72–74 % (25 W), and movement-primitive seam conditioning removes 83–87 % of the seam jerk. Sampling does not transfer, because on a sequential edge engine every N-sample method pays for N chunks in series.

### 1 Introduction (mean 0.303)

<!-- editlens chunk 0.303 lines 20-28 -->
<!-- editlens paragraph 0.338 lines 20-22 -->
Papers that speed up or smooth action chunking report their latencies on desktop and data-centre GPUs (RTX 4090, A100, H100, RTX 5090). There a chunk costs tens of milliseconds, and spare compute can hide an extra pass. The robots people can buy run their policies on edge GPUs.

<!-- editlens paragraph 0.297 lines 24-28 -->
Ours is an SO-101 arm [arXiv:2606.08881] with a Jetson Orin NX 16 GB, running SmolVLA [arXiv:2506.01844] through vla.cpp, a C++ inference engine, on episodes recorded with LeRobot. We took seven published tricks and asked each the question its paper does not: how much of the benefit survives when most of the chunk's time goes to a cost the trick never touches? Each answer is a gate with a bar committed before the number. Offline effects get an episode bootstrap, and latencies are medians of at least 50 calls. The appendix maps every number to its result file and protocol commit.

### 2 Where the time goes (mean 0.232)

<!-- editlens chunk 0.232 lines 32-38 -->
<!-- editlens paragraph 0.147 lines 32-35 -->
Vision dominates the chunk. At ten Euler steps and full power (MAXN_SUPER), a chunk costs 237.5 ms end to end: 150.7 ms of vision, 14.9 ms of prefill and 5.3 ms per denoise step (Fig. 1). At 25 W the server-side split is 151.0 ms of vision in 219.0 ms. A trick that only touches the denoising loop therefore works on at most a quarter of the chunk.

### 3 Seven tricks, one checkpoint (mean 0.220)

<!-- editlens chunk 0.220 lines 44-70 -->
<!-- editlens paragraph 0.294 lines 47-52 -->
The two tricks that work both act on the seam. Overwriting the new chunk's executed prefix with the actions already committed passes the 50 % jump-cut bar at every delay, in PyTorch and in vla.cpp, where it adds 0.4 ms per chunk. Movement-primitive chunking [arXiv:2610.39451] passes as well. Projecting each chunk onto ten Gaussian bases keeps the error within its bar while removing within-chunk jerk, and conditioning on the last action sent removes most of the seam jerk at +0.19° of error. Its paper reports 73–84 % of boundary jerk removed. We measured 83–87 %, though on the commanded stream only.

<!-- editlens paragraph 0.338 lines 54-55 -->
Exact real-time chunking [arXiv:2506.07339], which inpaints the prefix with guidance instead of overwriting it, cuts the jump by less than the bar at every delay (Fig. 2). It also costs 1.9× a naive chunk in PyTorch.

<!-- editlens paragraph 0.356 lines 57-61 -->
Cutting the Euler steps from ten to two [arXiv:2610.32102] saves 41 ms per chunk at full power, real but small next to the vision cost. The paper's central claim, that the action cloud contracts around an unchanged centroid, is not proven here. Our cloud ratio of 0.78 falls between the bar of 0.70 and the fail line of 0.85, where the paper reports 0.51 on π0. The paper also expects fewer steps to remove edge-GPU thermal throttling, but our Orin did not throttle at ten steps in either power mode.

<!-- editlens paragraph 0.275 lines 63-70 -->
Both sampling tricks pay for their samples one after another. Speculative chunk selection [arXiv:2610.28019] uses the pre-commit frame to pick, among four candidates, the chunk closest to the recorded teleoperation continuation, and offline it does beat a random pick (one continuation per frame, training-set episodes, open loop). Its paper promises no added control-step delay. On the Orin, vla.cpp samples the candidates in sequence, so a cycle costs 1,200 ms and 37 control ticks against 8 for a naive chunk (Fig. 3). Entropy-adaptive chunk length [arXiv:2604.04161] fails on every count. The chosen length sits at its floor in both task phases, the boundary jump does not improve on fixed chunks with the overwrite, and one 20-sample decision takes 4,751 ms against a bar of 298 ms.

### 4 What transfers to the board (mean 0.202)

<!-- editlens chunk 0.202 lines 90-96 -->
<!-- editlens paragraph 0.202 lines 90-96 -->
On this board, the prefix overwrite and the primitive projection with seam conditioning are worth turning on. Both act on the seam, which the vision cost does not hide, and both cost under a millisecond. We keep ten Euler steps because the protocol's rule says so while the contraction is unproven, not because the saving is unreal; it is small because vision dominates. Sampling several chunks per decision does not pay on a sequential edge engine, since exact guidance, speculative selection and adaptive length all pay for N chunks in series. A batched sampler could change that, and we have not tested one. This version is offline and latency only. The closed-loop columns on the arm, seam smoothing and the overwrite in the robot client, belong to a longer version.

### 5 Related work (mean 0.183)

<!-- editlens chunk 0.183 lines 100-107 -->
<!-- editlens paragraph 0.183 lines 100-107 -->
Other chunking tricks are also reported on desktop-class GPUs, and we did not re-measure them here: extending the executing chunk instead of resampling [arXiv:2610.05719], reactive chunking driven by a latent world model [arXiv:2606.18589], and fine-tuning the policy for latency with reinforcement learning rather than leaving it fixed [arXiv:2608.23831]. On the engine side, TurboVLA [arXiv:2607.27205] pushes VLA throughput on a desktop GPU, while vla.cpp, the engine we measure, runs VLAs on edge boards. Two works use the same arm. A standardized benchmark reports failures and recoveries of VLA policies [arXiv:2606.08881], and a fleet of SO-101 cells evaluates policies at scale [arXiv:2607.24481]. Both evaluate policies, while we re-measure the execution tricks around one policy under bars fixed before the run.

### 6 Limitations (mean 0.263)

<!-- editlens chunk 0.263 lines 111-119 -->
<!-- editlens paragraph 0.263 lines 111-119 -->
Everything runs one policy, SmolVLA at 450M. π0-class models do not fit on the Orin, which is part of the condition we study. vla.cpp is not independent of us: we contribute to it, and the overwrite runs on our fork (X). It is checked against PyTorch on the same board, with parity and determinism checks in the gate logs, but another engine could move the sequential-sampling costs. In particular, a batched sampler could cut the N-sample cost, and that control has not been run. Power mode is a confound, with latency rows at MAXN_SUPER and the serving and boundary rows at 25 W. Every effect except latency comes from offline episodes of one task family (bowls), and the 20 episodes are demonstrations the policy was trained on. There is no success column on the arm yet. The seam-smoothing arm gate and the overwrite in the robot client have not run, and the adaptive-length arm gate was left out because SmolVLA is at ceiling on this task, so a gain could not show.

### Appendix: from plain name to gate (mean 0.172)

<!-- editlens chunk 0.172 lines 123-123 -->
Every number in this paper is recomputable from the repository; this table maps each experiment to its files.

### (figure and table captions) (mean 0.284)

<!-- editlens chunk 0.284 lines 40-86 -->
Fig. 1 — where a SmolVLA chunk's time goes on the Orin NX (vla.cpp, ten Euler steps, MAXN_SUPER)
Table 1: Seven tricks on one checkpoint: what each acts on, the measured offline effect, the pre-registered bar, the verdict, and its cost on the Orin NX. Modes: serving and boundary rows 25 W, latency rows MAXN_SUPER.
Fig. 2 — median boundary-jump cut against naive asynchronous execution (254 boundaries per delay; PyTorch and vla.cpp, 25 W). Exact RTC guidance misses the 50 % bar at every delay.
Fig. 3 — cost per decision on the Orin NX (log scale, MAXN_SUPER). The dashed line is AAC's 298 ms bar; PACT's bar is one chunk (237.5 ms); both miss.

## built PDF

### Abstract (mean 0.129)

<!-- editlens chunk 0.129 lines 12-64 -->
<!-- editlens paragraph 0.214 lines 12-23 -->
Training-free tricks that make flow-matching visionlanguage-action policies faster or smoother are measured on desktop GPUs. We re-measured seven of them where a low-cost robot actually runs its policy: a 450M SmolVLA on a Jetson Orin NX, with one checkpoint, the same 20 recorded episodes and a bar committed before each run. On this board the vision encoder alone takes 151.0 of 219.0 ms of server time per action chunk (25 W), a cost most of the tricks never touch. The tricks that survive act on the seam between chunks. A gradientfree prefix overwrite cuts the boundary jump by 72–74 % (25 W), and movement-primitive seam conditioning removes 83–87 % of the seam jerk. Sampling does not transfer, because on a sequential edge engine every Nsample method pays for N chunks in series.

<!-- editlens paragraph 0.147 lines 57-64 -->
Vision dominates the chunk. At ten Euler steps and full power (MAXN_SUPER), a chunk costs 237.5 ms end to end: 150.7 ms of vision, 14.9 ms of prefill and 5.3 ms per denoise step (Fig. 1). At 25 W the server-side split is 151.0 ms of vision in 219.0 ms. A trick that only touches the denoising loop therefore works on at most a quarter of the chunk.

### 1 Introduction (mean 0.189)

<!-- editlens chunk 0.189 lines 65-96 -->
<!-- editlens paragraph 0.189 lines 65-96 -->
Two power modes appear because each gate’s protocol froze the mode it ran in. The serving split and the boundPapers that speed up or smooth action chunking report ary experiments ran at 25 W, the latency experiments at their latencies on desktop and data-centre GPUs (RTX full power, and every number below carries its mode. 4090, A100, H100, RTX 5090). There a chunk costs tens of milliseconds, and spare compute can hide an extra pass. The robots people can buy run their policies on 3 Seven tricks, one checkpoint edge GPUs. Ours is an SO-101 arm [3, 5] with a Jetson Orin NX All offline effects use the same SmolVLA checkpoint and 16 GB [2], running SmolVLA [14] through vla.cpp [4], a the same 20 recorded episodes, with 254 chunk boundC++ inference engine, on episodes recorded with LeR- aries per delay. Table 1 carries every effect, bar and verobot [1]. We took seven published tricks and asked each dict; the text covers what the table cannot show. the question its paper does not: how much of the benefit The two tricks that work both act on the seam. Oversurvives when most of the chunk’s time goes to a cost writing the new chunk’s executed prefix with the actions the trick never touches? Each answer is a gate with a already committed passes the 50 % jump-cut bar at every bar committed before the number. Offline effects get an delay, in PyTorch and in vla.cpp, where it adds 0.4 ms episode bootstrap, and latencies are medians of at least per chunk. Movement-primitive chunking [13] passes 50 calls. The appendix maps every number to its result as well. Projecting each chunk onto ten Gaussian bases file and protocol commit. keeps the error within its bar while removing withinchunk jerk, and conditioning on the last action sent removes most of the seam jerk at +0.19◦ of error. Its paper ∗ Every number with its source file and protocol commit: reports 73–84 % of boundary jerk removed. We measured github.com/ravediamond/paper-vla-edge-inference. 83–87 %, though on the commanded stream only. github.com/ravediamond/paper-vla-edge-inference · a899c5e

### 2 Euler steps (mean 0.164)

<!-- editlens chunk 0.164 lines 149-211 -->
<!-- editlens paragraph 0.249 lines 149-172 -->
Figure 2: Median boundary-jump cut against naive asynchronous execution (254 boundaries per delay; PyTorch and vla.cpp, 25 W). Exact RTC guidance misses the 50 % bar at every delay. Exact real-time chunking [11], which inpaints the prefix with guidance instead of overwriting it, cuts the jump by less than the bar at every delay (Fig. 2). It also costs 1.9× a naive chunk in PyTorch. Cutting the Euler steps from ten to two [15] saves 41 ms per chunk at full power, real but small next to the vision cost. The paper’s central claim, that the action cloud contracts around an unchanged centroid, is not proven here. Our cloud ratio of 0.78 falls between the bar of 0.70 and the fail line of 0.85, where the paper reports 0.51 on π0. The paper also expects fewer steps to remove edgeGPU thermal throttling, but our Orin did not throttle at ten steps in either power mode. Both sampling tricks pay for their samples one after another. Speculative chunk selection [16] uses the pre-commit frame to pick, among four candidates, the chunk closest to the recorded teleoperation continuation, and offline it does beat a random pick (one continuation per frame, training-set episodes, open loop). Its paper promises no added control-step delay. On the Orin, vla.cpp samples the candidates in sequence, so a cycle costs 1,200 ms and 37 control ticks against 8 for a naive chunk (Fig. 3). Entropy-adaptive chunk length [12] fails on every count. The chosen length sits at its floor in both task phases, the boundary jump does not improve on fixed chunks with the overwrite, and one 20-sample decision takes 4,751 ms against a bar of 298 ms.

<!-- editlens paragraph 0.119 lines 173-183 -->
Figure 3: Cost per decision on the Orin NX (log scale, MAXN_SUPER). The dashed line is AAC’s 298 ms bar; PACT’s bar is one chunk (237.5 ms); both miss. chunks per decision does not pay on a sequential edge engine, since exact guidance, speculative selection and adaptive length all pay for N chunks in series. A batched sampler could change that, and we have not tested one. This version is offline and latency only. The closed-loop columns on the arm, seam smoothing and the overwrite in the robot client, belong to a longer version.

<!-- editlens paragraph 0.173 lines 188-199 -->
Other chunking tricks are also reported on desktop-class GPUs, and we did not re-measure them here: extending the executing chunk instead of resampling [10], reactive chunking driven by a latent world model [6], and finetuning the policy for latency with reinforcement learning rather than leaving it fixed [9]. On the engine side, TurboVLA [8] pushes VLA throughput on a desktop GPU, while vla.cpp [4], the engine we measure, runs VLAs on edge boards. Two works use the same arm. A standardized benchmark reports failures and recoveries of VLA policies [5], and a fleet of SO-101 cells evaluates policies at scale [7]. Both evaluate policies, while we re-measure the execution tricks around one policy under bars fixed before the run.

<!-- editlens paragraph 0.118 lines 204-211 -->
Everything runs one policy, SmolVLA at 450M. π0 -class models do not fit on the Orin, which is part of the condition we study. vla.cpp is not independent of us: we contribute to it, and the overwrite runs on our fork (ravediamond/vla.cpp). It is checked against PyTorch on the same board, with parity and determinism checks in the gate logs, but another engine could move the

### 4 What transfers to the board (mean 0.086)

<!-- editlens chunk 0.086 lines 212-229 -->
<!-- editlens paragraph 0.096 lines 212-220 -->
sequential-sampling costs. In particular, a batched samOn this board, the prefix overwrite and the primitive pler could cut the N-sample cost, and that control has not projection with seam conditioning are worth turning on. been run. Power mode is a confound, with latency rows Both act on the seam, which the vision cost does not hide, at MAXN_SUPER and the serving and boundary rows and both cost under a millisecond. We keep ten Euler at 25 W. Every effect except latency comes from offline steps because the protocol’s rule says so while the con- episodes of one task family (bowls), and the 20 episodes traction is unproven, not because the saving is unreal; are demonstrations the policy was trained on. There is it is small because vision dominates. Sampling several no success column on the arm yet. The seam-smoothing github.com/ravediamond/paper-vla-edge-inference · a899c5e

<!-- editlens paragraph 0.078 lines 223-229 -->
arm gate and the overwrite in the robot client have not [15] Yang et al. Coupling Execution Horizon and Samrun, and the adaptive-length arm gate was left out bepling Depth in Flow-Matching VLA Policies, 2026. cause SmolVLA is at ceiling on this task, so a gain could arXiv:2610.32102. not show. [16] Zhu et al. PACT-VLA: Speculative Action-Chunk Verification with Pre-Commit Observations, 2026.

### Appendix: from plain name to gate (mean 0.114)

<!-- editlens chunk 0.114 lines 238-446 -->
<!-- editlens paragraph 0.079 lines 238-278 -->
[2] NVIDIA Jetson Orin NX 16 GB. https:// Every number in this paper is recomputable from the developer.nvidia.com/embedded/jetson-orin. repository; this table maps each experiment to its files. [3] SO-ARM100 (SO-101 low-cost robot arm). https: //github.com/TheRobotStudio/SO-ARM100. [4] vla.cpp. https://github.com/VinRobotics/vla. cpp. C++ inference engine for VLA policies; the engine commit of each measurement is in the gate logs. [5] Benchmarking Vision-Language-Action Models on SO-101: Failure and Recovery Analysis, 2026. arXiv:2606.08881. [6] DREAM-Chunk: Reactive Action Chunking with Latent World Model, 2026. arXiv:2606.18589. [7] ArmnetBench v0.1: Parallel Real-World Evaluation of Manipulation Policies on a Low-Cost Arm Farm, 2026. arXiv:2607.24481. [8] TurboVLA: Real-Time Vision-Language-Action Model at 32 Hz on an RTX 4090 with <1 GB VRAM, 2026. arXiv:2607.27205. [9] Learning to Act While Waiting: RL Finetuning of Generalist Robot Policies Under Inference Latency, 2026. arXiv:2608.23831. [10] When to Switch: Reliable Action-Chunk Extension for Vision-Language-Action Models, 2026. arXiv:2610.05719. [11] Kevin Black, Manuel Y. Galliker, and Sergey Levine. Real-Time Execution of Action Chunking Flow Policies, 2025. arXiv:2506.07339. [12] Liang et al. Adaptive Action Chunking at Inferencetime for Vision-Language-Action Models, 2026. arXiv:2604.04161; CVPR 2026. [13] Nomura, Osa, Kato, Ota, Shitanda, and Harada. Smooth Action Chunking Via Movement-Primitive Representations for Imitation Learning, 2026. arXiv:2610.39451. [14] Mustafa Shukor, Dana Aubakirova, Francesco Capuano, et al. SmolVLA: A Vision-Language-Action Model for Affordable and Eﬀicient Robotics, 2025. arXiv:2506.01844. github.com/ravediamond/paper-vla-edge-inference · a899c5e
