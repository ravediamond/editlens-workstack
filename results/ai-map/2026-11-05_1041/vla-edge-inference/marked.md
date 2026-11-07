# paper-vla-edge-inference: chunks in paper order

## rendered source (numbers filled)

### Abstract (mean 0.281)

<!-- editlens chunk 0.281 lines 9-16 -->
<!-- editlens paragraph 0.281 lines 9-16 -->
On an edge GPU, most of a VLA's action chunk goes to vision, so a trick that speeds up or smooths chunking keeps only the part of its benefit that touches the seam between chunks. We re-measured seven training-free tricks, published and measured on desktop GPUs, where a low-cost robot runs its policy: SmolVLA on a Jetson Orin NX, with one checkpoint, the same recorded episodes and a bar committed before each run. The vision encoder alone takes 151.0 of 219.0 ms of server time per chunk (25 W). The two tricks that act on the seam pass: a gradient-free prefix overwrite cuts the boundary jump by 72 % or more, and movement-primitive seam conditioning removes most of the seam jerk. Sampling does not transfer, because on a sequential edge engine every N-sample method pays for N chunks in series. So on this board, smooth the seam and leave the sampler alone.

### 1 Introduction (mean 0.265)

<!-- editlens chunk 0.265 lines 20-31 -->
<!-- editlens paragraph 0.481 lines 20-24 -->
With several training-free chunking tricks published this year for flow-matching VLAs, it is tempting to think they make a policy faster or smoother on any robot. They are measured on desktop and data-centre GPUs (RTX 4090, A100, H100, RTX 5090), where a chunk costs tens of milliseconds and spare compute can hide an extra pass. A robot people can buy runs its policy on an edge GPU, where most of the chunk goes to a part the tricks never touch (the vision encoder). So the useful question is not whether a trick works, but how much of it is left on that board.

<!-- editlens paragraph 0.209 lines 26-31 -->
Ours is an SO-101 arm [arXiv:2606.08881] with a Jetson Orin NX 16 GB, running SmolVLA [arXiv:2506.01844] through vla.cpp, a C++ inference engine, on episodes recorded with LeRobot. This paper started once SmolVLA ran on the arm through vla.cpp: the next question was where the remaining time of a chunk went, and which published tricks could still buy something. We took seven of them. Each answer is a gate with a bar committed before the number; offline effects get an episode bootstrap, and latencies are medians of at least 50 calls. The appendix maps every number to its result file and protocol commit.

### 2 Where the time goes (mean 0.219)

<!-- editlens chunk 0.219 lines 35-41 -->
<!-- editlens paragraph 0.168 lines 35-38 -->
Follow one chunk. At ten Euler steps and full power (MAXN_SUPER) it costs 237.5 ms end to end: 150.7 ms of vision, 14.9 ms of prefill and 5.3 ms per denoise step (Fig. 1). At 25 W the server-side split is 151.0 ms of vision in 219.0 ms. A trick that only touches the denoising loop therefore works on at most a quarter of that chunk.

### 3 Seven tricks, one checkpoint (mean 0.234)

<!-- editlens chunk 0.234 lines 47-74 -->
<!-- editlens paragraph 0.300 lines 50-55 -->
The two tricks that pass both act where our chunk meets the next one. Overwriting the new chunk's executed prefix with the actions already committed passes the 50 % jump-cut bar at every delay, in PyTorch and in vla.cpp, where it adds 0.4 ms per chunk. Movement-primitive chunking [arXiv:2610.39451] passes as well. Projecting each chunk onto ten Gaussian bases keeps the error within its bar while removing within-chunk jerk, and conditioning on the last action sent removes 83–87 % of the seam jerk at +0.19° of error (its paper reports 73–84 %; ours is measured on the commanded stream only).

<!-- editlens paragraph 0.338 lines 57-58 -->
Exact real-time chunking [arXiv:2506.07339], which inpaints the prefix with guidance instead of overwriting it, cuts the jump by less than the bar at every delay (Fig. 2). It also costs 1.9× a naive chunk in PyTorch.

<!-- editlens paragraph 0.349 lines 60-65 -->
Cutting the Euler steps from ten to two [arXiv:2610.32102] saves 41 ms per chunk at full power (real, but small next to the vision cost). The paper's central claim, that the action cloud contracts around an unchanged centroid, is not proven here: our cloud ratio of 0.78 falls between the bar of 0.70 and the fail line of 0.85, where the paper reports 0.51 on π0. The paper also expects fewer steps to remove edge-GPU thermal throttling, but our Orin did not throttle at ten steps in either power mode. We keep ten steps, as the protocol's rule says while the contraction is unproven.

<!-- editlens paragraph 0.275 lines 67-74 -->
Both sampling tricks pay for their samples one after another. Speculative chunk selection [arXiv:2610.28019] uses the pre-commit frame to pick, among four candidates, the chunk closest to the recorded teleoperation continuation, and offline it does beat a random pick (one continuation per frame, training-set episodes, open loop). Its paper promises no added control-step delay. On the Orin, vla.cpp samples the candidates in sequence, so a cycle costs 1,200 ms and 37 control ticks against 8 for a naive chunk (Fig. 3). Entropy-adaptive chunk length [arXiv:2604.04161] fails on every count. The chosen length sits at its floor in both task phases, the boundary jump does not improve on fixed chunks with the overwrite, and one 20-sample decision takes 4,751 ms against a bar of 298 ms.

### 4 What transfers to the board (mean 0.198)

<!-- editlens chunk 0.198 lines 94-100 -->
<!-- editlens paragraph 0.198 lines 94-100 -->
On this board, the prefix overwrite and the primitive projection with seam conditioning are worth turning on. Both act on the seam, which the vision cost does not hide, and both cost under a millisecond. Ten Euler steps stay until the contraction passes its bar; the two-step saving is real but small because vision dominates. Sampling several chunks per decision does not pay on a sequential edge engine, since exact guidance, speculative selection and adaptive length all pay for N chunks in series. Before turning one of them on, check whether your engine samples in a batch (ours does not). This version is offline and latency only. The closed-loop columns on the arm, seam smoothing and the overwrite in the robot client, belong to a longer version.

### 5 Related work (mean 0.182)

<!-- editlens chunk 0.182 lines 104-110 -->
<!-- editlens paragraph 0.182 lines 104-110 -->
Other chunking tricks are also reported on desktop-class GPUs, and we did not re-measure them here: extending the executing chunk instead of resampling [arXiv:2610.05719], reactive chunking driven by a latent world model [arXiv:2606.18589], and fine-tuning the policy for latency with reinforcement learning [arXiv:2608.23831]. On the engine side, TurboVLA [arXiv:2607.27205] pushes VLA throughput on a desktop GPU, while vla.cpp, the engine we measure, runs VLAs on edge boards. Two works use the same arm. A standardized benchmark reports failures and recoveries of VLA policies [arXiv:2606.08881], and a fleet of SO-101 cells evaluates policies at scale [arXiv:2607.24481]. Both evaluate policies, while we re-measure the execution tricks around one policy under bars fixed before the run.

### 6 Limitations (mean 0.309)

<!-- editlens chunk 0.309 lines 114-123 -->
<!-- editlens paragraph 0.309 lines 114-123 -->
The finding most likely to move is that sampling does not transfer, because it depends on the engine. vla.cpp samples sequentially, and it is not independent of us: we contribute to it, and the overwrite runs on our fork (X). A batched sampler could cut the N-sample cost, and that control has not been run. The engine is checked against PyTorch on the same board, with parity and determinism checks in the gate logs. The next gap is the arm: there is no success column on it yet. Every effect except latency comes from offline episodes of one task family (bowls), and the 20 episodes are demonstrations the policy was trained on. The seam-smoothing arm gate and the overwrite in the robot client have not run, and the adaptive-length arm gate was left out because SmolVLA is at ceiling on this task, so a gain could not show. Power mode is a confound (latency rows at MAXN_SUPER, the serving and boundary rows at 25 W). Everything runs one policy, SmolVLA at 450M; π0-class models do not fit on the Orin, which is part of the condition we study.

### Appendix: from plain name to gate (mean 0.172)

<!-- editlens chunk 0.172 lines 127-127 -->
Every number in this paper is recomputable from the repository; this table maps each experiment to its files.

### (figure and table captions) (mean 0.293)

<!-- editlens chunk 0.293 lines 43-90 -->
Fig. 1 — where one SmolVLA chunk's time goes on the Orin NX (vla.cpp, ten Euler steps, MAXN_SUPER): vision is most of it
Table 1: Seven tricks on one checkpoint. Read the acts-on column against the verdict: the seam tricks pass, the sampling tricks fail.
Fig. 2 — median boundary-jump cut against naive asynchronous execution (254 boundaries per delay, 25 W): the overwrite clears the 50 % bar at every delay, exact RTC guidance does not.
Fig. 3 — cost per decision on the Orin NX (log scale, MAXN_SUPER): both sampling methods miss their bar (dashed: AAC's 298 ms; PACT's bar is one chunk, 237.5 ms).

## built PDF

### Abstract (mean 0.099)

<!-- editlens chunk 0.099 lines 12-79 -->
<!-- editlens paragraph 0.259 lines 12-26 -->
On an edge GPU, most of a VLA’s action chunk goes to vision, so a trick that speeds up or smooths chunking keeps only the part of its benefit that touches the seam between chunks. We re-measured seven trainingfree tricks, published and measured on desktop GPUs, where a low-cost robot runs its policy: SmolVLA on a Jetson Orin NX, with one checkpoint, the same recorded episodes and a bar committed before each run. The vision encoder alone takes 151.0 of 219.0 ms of server time per chunk (25 W). The two tricks that act on the seam pass: a gradient-free prefix overwrite cuts the boundary jump by 72 % or more, and movement-primitive seam conditioning removes most of the seam jerk. Sampling does not transfer, because on a sequential edge engine every N-sample method pays for N chunks in series. So on this board, smooth the seam and leave the sampler alone.

<!-- editlens paragraph 0.394 lines 55-61 -->
Figure 1: Where one SmolVLA chunk’s time goes on the Orin NX (vla.cpp, ten Euler steps, MAXN_SUPER): vision is most of it. tricks could still buy something. We took seven of them. Each answer is a gate with a bar committed before the number; offline effects get an episode bootstrap, and latencies are medians of at least 50 calls. The appendix maps every number to its result file and protocol commit.

<!-- editlens paragraph 0.080 lines 68-79 -->
Follow one chunk. At ten Euler steps and full power (MAXN_SUPER) it costs 237.5 ms end to end: 150.7 ms With several training-free chunking tricks published this of vision, 14.9 ms of prefill and 5.3 ms per denoise step year for flow-matching VLAs, it is tempting to think they (Fig. 1). At 25 W the server-side split is 151.0 ms of vision make a policy faster or smoother on any robot. They are in 219.0 ms. A trick that only touches the denoising loop measured on desktop and data-centre GPUs (RTX 4090, therefore works on at most a quarter of that chunk. A100, H100, RTX 5090), where a chunk costs tens of milTwo power modes appear because each gate’s protocol liseconds and spare compute can hide an extra pass. A froze the mode it ran in (the serving split and the boundrobot people can buy runs its policy on an edge GPU, ary experiments at 25 W, the latency experiments at full where most of the chunk goes to a part the tricks never power). Every number below carries its mode. touch (the vision encoder). So the useful question is not whether a trick works, but how much of it is left on that

### 3 Seven tricks, one checkpoint (mean 0.057)

<!-- editlens chunk 0.057 lines 80-94 -->
<!-- editlens paragraph 0.057 lines 80-94 -->
board. Ours is an SO-101 arm [3, 5] with a Jetson Orin NX All offline effects use the same SmolVLA checkpoint and 16 GB [2], running SmolVLA [14] through vla.cpp [4], a the same 20 recorded episodes, with 254 chunk boundC++ inference engine, on episodes recorded with LeRaries per delay. Table 1 carries every effect, bar and verobot [1]. This paper started once SmolVLA ran on the dict; the text covers what the table cannot show. arm through vla.cpp: the next question was where the The two tricks that pass both act where our chunk remaining time of a chunk went, and which published meets the next one. Overwriting the new chunk’s exe∗ Every number with its source file and protocol commit: cuted prefix with the actions already committed passes github.com/ravediamond/paper-vla-edge-inference. the 50 % jump-cut bar at every delay, in PyTorch and github.com/ravediamond/paper-vla-edge-inference · af9ddb4

### 2 Euler steps (mean 0.223)

<!-- editlens chunk 0.207 lines 147-216 -->
<!-- editlens paragraph 0.264 lines 151-178 -->
in vla.cpp, where it adds 0.4 ms per chunk. Movementprimitive chunking [13] passes as well. Projecting each chunk onto ten Gaussian bases keeps the error within its bar while removing within-chunk jerk, and conditioning on the last action sent removes 83–87 % of the seam jerk at +0.19◦ of error (its paper reports 73–84 %; ours is measured on the commanded stream only). Exact real-time chunking [11], which inpaints the prefix with guidance instead of overwriting it, cuts the jump by less than the bar at every delay (Fig. 2). It also costs 1.9× a naive chunk in PyTorch. Cutting the Euler steps from ten to two [15] saves 41 ms per chunk at full power (real, but small next to the vision cost). The paper’s central claim, that the action cloud contracts around an unchanged centroid, is not proven here: our cloud ratio of 0.78 falls between the bar of 0.70 and the fail line of 0.85, where the paper reports 0.51 on π0. The paper also expects fewer steps to remove edgeGPU thermal throttling, but our Orin did not throttle at ten steps in either power mode. We keep ten steps, as the protocol’s rule says while the contraction is unproven. Both sampling tricks pay for their samples one after another. Speculative chunk selection [16] uses the pre-commit frame to pick, among four candidates, the chunk closest to the recorded teleoperation continuation, and offline it does beat a random pick (one continuation per frame, training-set episodes, open loop). Its paper promises no added control-step delay. On the Orin, vla.cpp samples the candidates in sequence, so a cycle costs 1,200 ms and 37 control ticks against 8 for a naive chunk (Fig. 3). Entropy-adaptive chunk length [12] fails on every count. The chosen length sits at its floor in both task phases, the boundary jump does not improve on fixed chunks with the overwrite, and one 20-sample decision takes 4,751 ms against a bar of 298 ms.

<!-- editlens paragraph 0.198 lines 190-202 -->
On this board, the prefix overwrite and the primitive projection with seam conditioning are worth turning on. Both act on the seam, which the vision cost does not hide, and both cost under a millisecond. Ten Euler steps stay until the contraction passes its bar; the two-step saving is real but small because vision dominates. Sampling several chunks per decision does not pay on a sequential edge engine, since exact guidance, speculative selection and adaptive length all pay for N chunks in series. Before turning one of them on, check whether your engine samples in a batch (ours does not). This version is offline and latency only. The closed-loop columns on the arm, seam smoothing and the overwrite in the robot client, belong to a longer version.

<!-- editlens paragraph 0.168 lines 207-216 -->
Other chunking tricks are also reported on desktop-class GPUs, and we did not re-measure them here: extending the executing chunk instead of resampling [10], reactive chunking driven by a latent world model [6], and finetuning the policy for latency with reinforcement learning [9]. On the engine side, TurboVLA [8] pushes VLA throughput on a desktop GPU, while vla.cpp [4], the engine we measure, runs VLAs on edge boards. Two works use the same arm. A standardized benchmark reports failures and recoveries of VLA policies [5], and a fleet of SO-101 cells evaluates policies at scale [7]. Both evaluate policies, while we re-measure the execution tricks around one policy under bars fixed before the run.

<!-- editlens chunk 0.276 lines 221-241 -->
<!-- editlens paragraph 0.135 lines 221-228 -->
The finding most likely to move is that sampling does not transfer, because it depends on the engine. vla.cpp samples sequentially, and it is not independent of us: we contribute to it, and the overwrite runs on our fork (ravediamond/vla.cpp). A batched sampler could cut the N-sample cost, and that control has not been run. The 2

<!-- editlens paragraph 0.127 lines 229-241 -->
engine is checked against PyTorch on the same board, with parity and determinism checks in the gate logs. The next gap is the arm: there is no success column on it yet. Every effect except latency comes from offline episodes of one task family (bowls), and the 20 episodes are demonstrations the policy was trained on. The seamsmoothing arm gate and the overwrite in the robot client have not run, and the adaptive-length arm gate was left out because SmolVLA is at ceiling on this task, so a gain could not show. Power mode is a confound (latency rows at MAXN_SUPER, the serving and boundary rows at 25 W). Everything runs one policy, SmolVLA at 450M; π0 class models do not fit on the Orin, which is part of the condition we study.

### Appendix: from plain name to gate (mean 0.115)

<!-- editlens chunk 0.115 lines 263-463 -->
<!-- editlens paragraph 0.040 lines 263-295 -->
[2] NVIDIA Jetson Orin NX 16 GB. https:// Every number in this paper is recomputable from the developer.nvidia.com/embedded/jetson-orin. repository; this table maps each experiment to its files. [3] SO-ARM100 (SO-101 low-cost robot arm). https: //github.com/TheRobotStudio/SO-ARM100. [4] vla.cpp. https://github.com/VinRobotics/vla. cpp. C++ inference engine for VLA policies; the engine commit of each measurement is in the gate logs. [5] Benchmarking Vision-Language-Action Models on SO-101: Failure and Recovery Analysis, 2026. arXiv:2606.08881. [6] DREAM-Chunk: Reactive Action Chunking with Latent World Model, 2026. arXiv:2606.18589. [7] ArmnetBench v0.1: Parallel Real-World Evaluation of Manipulation Policies on a Low-Cost Arm Farm, 2026. arXiv:2607.24481. [8] TurboVLA: Real-Time Vision-Language-Action Model at 32 Hz on an RTX 4090 with <1 GB VRAM, 2026. arXiv:2607.27205. [9] Learning to Act While Waiting: RL Finetuning of Generalist Robot Policies Under Inference Latency, 2026. arXiv:2608.23831. [10] When to Switch: Reliable Action-Chunk Extension for Vision-Language-Action Models, 2026. arXiv:2610.05719. [11] Kevin Black, Manuel Y. Galliker, and Sergey Levine. Real-Time Execution of Action Chunking Flow Policies, 2025. arXiv:2506.07339. [12] Liang et al. Adaptive Action Chunking at Inferencetime for Vision-Language-Action Models, 2026. arXiv:2604.04161; CVPR 2026. github.com/ravediamond/paper-vla-edge-inference · af9ddb4
