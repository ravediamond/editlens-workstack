# paper-vla-edge-inference: chunks in paper order

## rendered source (numbers filled)

### Abstract (mean 0.267)

<!-- editlens chunk 0.267 lines 9-16 -->
<!-- editlens paragraph 0.267 lines 9-16 -->
We re-measured seven training-free methods for action chunking in flow-matching VLAs, whose papers report numbers from desktop GPUs, on the hardware a low-cost robot runs: SmolVLA on a Jetson Orin NX. All tests share one checkpoint and the same recorded episodes, each had its threshold committed before the run, and every number traces to a result file and a protocol commit. On this board the vision encoder takes 151.0 of 219.0 ms of server time per chunk (25 W). The two methods that act on the seam between chunks pass. A gradient-free prefix overwrite cuts the boundary jump by 72 % or more, and movement-primitive seam conditioning removes most of the seam jerk. The sampling methods do not transfer, because vla.cpp samples in sequence and every N-sample method pays for N chunks one after another.

### 1 Introduction (mean 0.218)

<!-- editlens chunk 0.218 lines 20-30 -->
<!-- editlens paragraph 0.292 lines 20-23 -->
Several training-free chunking tricks for flow-matching VLAs were published this year, with numbers from desktop and data-centre GPUs (RTX 4090, A100, H100, RTX 5090). There a chunk costs tens of milliseconds, and spare compute can hide an extra pass. A robot people can buy runs its policy on an edge GPU, where most of the chunk goes to the vision encoder, which these tricks do not touch. We measured how much of each trick is left on such a board.

<!-- editlens paragraph 0.236 lines 25-30 -->
Our robot is an SO-101 arm [arXiv:2606.08881] with a Jetson Orin NX 16 GB. It runs SmolVLA [arXiv:2506.01844] through vla.cpp, a C++ inference engine, on episodes recorded with LeRobot. This paper started once SmolVLA ran on the arm through vla.cpp, when we looked at where the rest of a chunk's time went and at which published tricks could still help. We took seven of them, each as a gate with a bar committed before the number. Offline effects get an episode bootstrap, and latencies are medians of at least 50 calls. The appendix maps every number to its result file and protocol commit.

### 2 Where the time goes (mean 0.326)

<!-- editlens chunk 0.326 lines 34-40 -->
<!-- editlens paragraph 0.292 lines 34-37 -->
We follow one chunk of ten Euler steps at full power (MAXN_SUPER), which costs 237.5 ms end to end (Fig. 1). Vision takes 150.7 ms, prefill 14.9 ms, and each denoise step 5.3 ms. At 25 W the server-side split is 151.0 ms of vision in 219.0 ms. A trick that only touches the denoising loop works on at most a quarter of the chunk.

<!-- editlens paragraph 0.301 lines 39-40 -->
Two power modes appear in this paper because each gate's protocol froze the mode it ran in: the serving split and the boundary experiments ran at 25 W, and the latency experiments at full power. Every number below carries its mode.

### 3 Seven tricks, one checkpoint (mean 0.196)

<!-- editlens chunk 0.196 lines 46-73 -->
<!-- editlens paragraph 0.306 lines 49-54 -->
Two tricks act on the seam between chunks, and both pass. The first overwrites the new chunk's executed prefix with the actions already committed, and it passes the 50 % jump-cut bar at every delay, in PyTorch and in vla.cpp, where it adds 0.4 ms per chunk. The second is movement-primitive chunking [arXiv:2610.39451]. Projecting each chunk onto ten Gaussian bases keeps the error within its bar and removes within-chunk jerk. Conditioning on the last action sent removes 83–87 % of the seam jerk at +0.19° of error, against 73–84 % in its paper (we measured on the commanded stream only).

<!-- editlens paragraph 0.286 lines 59-64 -->
Cutting the Euler steps from ten to two [arXiv:2610.32102] saves 41 ms per chunk at full power, which is small next to the vision cost. The paper claims that the action cloud contracts around an unchanged centroid, with a cloud ratio of 0.51 on π0. Our ratio is 0.78, between the bar of 0.70 and the fail line of 0.85, so the claim is not proven here. The paper also expects fewer steps to remove edge-GPU thermal throttling, and our Orin did not throttle at ten steps in either power mode. We keep ten steps, as the protocol says while the contraction is unproven.

<!-- editlens paragraph 0.274 lines 66-73 -->
Two tricks sample several chunks per decision. Speculative chunk selection [arXiv:2610.28019] samples four candidates and uses the pre-commit frame to pick the one closest to the recorded teleoperation continuation. Offline it beats a random pick (one continuation per frame, training-set episodes, open loop). Its paper promises no added control-step delay, but on the Orin vla.cpp samples the candidates in sequence, and a cycle costs 1,200 ms and 37 control ticks against 8 for a naive chunk (Fig. 3). Entropy-adaptive chunk length [arXiv:2604.04161] samples 20 chunks per decision, and one decision takes 4,751 ms on the Orin against a threshold of 298 ms. Its chosen length also sits at the floor in both task phases, and the jump is no better than with fixed chunks and the overwrite.

### 4 What transfers to the board (mean 0.346)

<!-- editlens chunk 0.346 lines 93-98 -->
<!-- editlens paragraph 0.346 lines 93-98 -->
The prefix overwrite and the primitive projection with seam conditioning act on the seam, and each costs under a millisecond on this board. We keep ten Euler steps until the contraction passes its threshold, since the two-step saving is small next to vision. Exact guidance, speculative selection and adaptive length all pay for N chunks in series on a sequential engine. If you run one of them on an edge board, check first whether your engine samples in a batch, because ours does not. This version is offline and latency only, and the closed-loop columns on the arm, for seam smoothing and for the overwrite in the robot client, belong to a longer version.

### 5 Related work (mean 0.135)

<!-- editlens chunk 0.135 lines 102-108 -->
<!-- editlens paragraph 0.135 lines 102-108 -->
Other chunking tricks are also reported on desktop-class GPUs, and we did not re-measure them here: extending the executing chunk instead of resampling [arXiv:2610.05719], driving reactive chunking with a latent world model [arXiv:2606.18589], and fine-tuning the policy for latency with reinforcement learning [arXiv:2608.23831]. On the engine side, TurboVLA [arXiv:2607.27205] pushes VLA throughput on a desktop GPU. vla.cpp, the engine we measure, runs VLAs on edge boards. Two works use the same arm to evaluate policies, a standardized benchmark that reports failures and recoveries of VLA policies [arXiv:2606.08881] and a fleet of SO-101 cells that evaluates policies at scale [arXiv:2607.24481]. We re-measure the execution tricks around one policy, under bars fixed before the run.

### 6 Limitations (mean 0.174)

<!-- editlens chunk 0.174 lines 112-119 -->
<!-- editlens paragraph 0.174 lines 112-119 -->
The sampling result depends on the engine. vla.cpp samples sequentially, and we contribute to it (the overwrite runs on our fork, X). Parity and determinism checks against PyTorch on the same board are in the gate logs, and a batched sampler would test the sampling result, but we have not run one. Effects other than latency are offline and come from 20 recorded demonstrations of one task family (bowls), which the policy was trained on. The arm gates for seam smoothing and for the overwrite in the robot client have not run. We left out the adaptive-length arm gate because SmolVLA is at ceiling on this task, so a gain could not show. Latency rows run at MAXN_SUPER and the serving and boundary rows at 25 W, which makes power mode a confound wherever the two are compared. The study covers one policy, SmolVLA at 450M, since π0-class models do not fit on the Orin.

### Appendix: from plain name to gate (mean 0.172)

<!-- editlens chunk 0.172 lines 123-123 -->
Every number in this paper is recomputable from the repository; this table maps each experiment to its files.

### (figure and table captions) (mean 0.300)

<!-- editlens chunk 0.300 lines 42-89 -->
Fig. 1 — where one SmolVLA chunk's time goes on the Orin NX (vla.cpp, ten Euler steps, MAXN_SUPER): vision is most of it
Table 1: Seven tricks on one checkpoint: what each acts on, its offline effect, the pre-registered bar, the verdict and its cost on the Orin NX.
Fig. 2 — median boundary-jump cut against naive asynchronous execution (254 boundaries per delay, 25 W): the overwrite clears the 50 % bar at every delay, exact RTC guidance does not.
Fig. 3 — cost per decision on the Orin NX (log scale, MAXN_SUPER): both sampling methods miss their bar (dashed: AAC's 298 ms; PACT's bar is one chunk, 237.5 ms).

## built PDF

### Abstract (mean 0.159)

<!-- editlens chunk 0.159 lines 12-65 -->
<!-- editlens paragraph 0.267 lines 12-26 -->
We re-measured seven training-free methods for action chunking in flow-matching VLAs, whose papers report numbers from desktop GPUs, on the hardware a low-cost robot runs: SmolVLA on a Jetson Orin NX. All tests share one checkpoint and the same recorded episodes, each had its threshold committed before the run, and every number traces to a result file and a protocol commit. On this board the vision encoder takes 151.0 of 219.0 ms of server time per chunk (25 W). The two methods that act on the seam between chunks pass. A gradient-free prefix overwrite cuts the boundary jump by 72 % or more, and movement-primitive seam conditioning removes most of the seam jerk. The sampling methods do not transfer, because vla.cpp samples in sequence and every N-sample method pays for N chunks one after another.

<!-- editlens paragraph 0.213 lines 60-65 -->
We follow one chunk of ten Euler steps at full power (MAXN_SUPER), which costs 237.5 ms end to end (Fig. 1). Vision takes 150.7 ms, prefill 14.9 ms, and each denoise step 5.3 ms. At 25 W the server-side split is 151.0 ms of vision in 219.0 ms. A trick that only touches the

### 1 Introduction (mean 0.032)

<!-- editlens chunk 0.032 lines 66-94 -->
<!-- editlens paragraph 0.032 lines 66-94 -->
denoising loop works on at most a quarter of the chunk. Two power modes appear in this paper because each Several training-free chunking tricks for flow-matching gate’s protocol froze the mode it ran in: the serving split VLAs were published this year, with numbers from deskand the boundary experiments ran at 25 W, and the latop and data-centre GPUs (RTX 4090, A100, H100, RTX tency experiments at full power. Every number below 5090). There a chunk costs tens of milliseconds, and carries its mode. spare compute can hide an extra pass. A robot people can buy runs its policy on an edge GPU, where most of the chunk goes to the vision encoder, which these tricks 3 Seven tricks, one checkpoint do not touch. We measured how much of each trick is left on such a board. All offline effects use the same SmolVLA checkpoint and Our robot is an SO-101 arm [3, 5] with a Jetson Orin the same 20 recorded episodes, with 254 chunk boundNX 16 GB [2]. It runs SmolVLA [14] through vla.cpp aries per delay. Table 1 gives every effect, bar and ver[4], a C++ inference engine, on episodes recorded with dict. LeRobot [1]. This paper started once SmolVLA ran on Two tricks act on the seam between chunks, and both the arm through vla.cpp, when we looked at where the pass. The first overwrites the new chunk’s executed prerest of a chunk’s time went and at which published tricks fix with the actions already committed, and it passes the could still help. We took seven of them, each as a gate 50 % jump-cut bar at every delay, in PyTorch and in with a bar committed before the number. Offline effects vla.cpp, where it adds 0.4 ms per chunk. The second get an episode bootstrap, and latencies are medians of at is movement-primitive chunking [13]. Projecting each least 50 calls. The appendix maps every number to its chunk onto ten Gaussian bases keeps the error within result file and protocol commit. its bar and removes within-chunk jerk. Conditioning on ∗ Every number with its source file and protocol commit: the last action sent removes 83–87 % of the seam jerk at github.com/ravediamond/paper-vla-edge-inference. +0.19◦ of error, against 73–84 % in its paper (we meagithub.com/ravediamond/paper-vla-edge-inference · 3e85729

### 2 Euler steps (mean 0.170)

<!-- editlens chunk 0.170 lines 147-212 -->
<!-- editlens paragraph 0.180 lines 147-174 -->
Figure 2: Median boundary-jump cut against naive asynchronous execution (254 boundaries per delay, 25 W): the overwrite clears the 50 % bar at every delay, exact RTC guidance does not. sured on the commanded stream only). Exact real-time chunking [11] inpaints the prefix with guidance instead of overwriting it. It cuts the jump by less than 50 % at every delay (Fig. 2), and in PyTorch it costs 1.9× a naive chunk. Cutting the Euler steps from ten to two [15] saves 41 ms per chunk at full power, which is small next to the vision cost. The paper claims that the action cloud contracts around an unchanged centroid, with a cloud ratio of 0.51 on π0. Our ratio is 0.78, between the bar of 0.70 and the fail line of 0.85, so the claim is not proven here. The paper also expects fewer steps to remove edge-GPU thermal throttling, and our Orin did not throttle at ten steps in either power mode. We keep ten steps, as the protocol says while the contraction is unproven. Two tricks sample several chunks per decision. Speculative chunk selection [16] samples four candidates and uses the pre-commit frame to pick the one closest to the recorded teleoperation continuation. Offline it beats a random pick (one continuation per frame, trainingset episodes, open loop). Its paper promises no added control-step delay, but on the Orin vla.cpp samples the candidates in sequence, and a cycle costs 1,200 ms and 37 control ticks against 8 for a naive chunk (Fig. 3). Entropyadaptive chunk length [12] samples 20 chunks per decision, and one decision takes 4,751 ms on the Orin against a threshold of 298 ms. Its chosen length also sits at the floor in both task phases, and the jump is no better than with fixed chunks and the overwrite.

<!-- editlens paragraph 0.134 lines 175-185 -->
Figure 3: Cost per decision on the Orin NX (log scale, MAXN_SUPER): both sampling methods miss their bar (dashed: AAC’s 298 ms; PACT’s bar is one chunk, 237.5 ms). tive selection and adaptive length all pay for N chunks in series on a sequential engine. If you run one of them on an edge board, check first whether your engine samples in a batch, because ours does not. This version is offline and latency only, and the closed-loop columns on the arm, for seam smoothing and for the overwrite in the robot client, belong to a longer version.

<!-- editlens paragraph 0.132 lines 190-199 -->
Other chunking tricks are also reported on desktop-class GPUs, and we did not re-measure them here: extending the executing chunk instead of resampling [10], driving reactive chunking with a latent world model [6], and fine-tuning the policy for latency with reinforcement learning [9]. On the engine side, TurboVLA [8] pushes VLA throughput on a desktop GPU. vla.cpp [4], the engine we measure, runs VLAs on edge boards. Two works use the same arm to evaluate policies, a standardized benchmark that reports failures and recoveries of VLA policies [5] and a fleet of SO-101 cells that evaluates policies at scale [7]. We re-measure the execution tricks around one policy, under bars fixed before the run.

<!-- editlens paragraph 0.187 lines 204-212 -->
The sampling result depends on the engine. vla.cpp samples sequentially, and we contribute to it (the overwrite runs on our fork, ravediamond/vla.cpp). Parity and determinism checks against PyTorch on the same board are in the gate logs, and a batched sampler would test the sampling result, but we have not run one. Effects other than latency are offline and come from 20 recorded demonstrations of one task family (bowls), which the policy was trained on. The arm gates for seam smoothing

### 4 What transfers to the board (mean 0.113)

<!-- editlens chunk 0.113 lines 213-226 -->
<!-- editlens paragraph 0.097 lines 213-218 -->
and for the overwrite in the robot client have not run. We The prefix overwrite and the primitive projection with left out the adaptive-length arm gate because SmolVLA seam conditioning act on the seam, and each costs under is at ceiling on this task, so a gain could not show. Laa millisecond on this board. We keep ten Euler steps un- tency rows run at MAXN_SUPER and the serving and til the contraction passes its threshold, since the two-step boundary rows at 25 W, which makes power mode a consaving is small next to vision. Exact guidance, specula- found wherever the two are compared. The study covers github.com/ravediamond/paper-vla-edge-inference · 3e85729

### Appendix: from plain name to gate (mean 0.120)

<!-- editlens chunk 0.120 lines 247-449 -->
<!-- editlens paragraph 0.051 lines 250-283 -->
[4] vla.cpp. https://github.com/VinRobotics/vla. cpp. C++ inference engine for VLA policies; the engine commit of each measurement is in the gate logs. [5] Benchmarking Vision-Language-Action Models on SO-101: Failure and Recovery Analysis, 2026. arXiv:2606.08881. [6] DREAM-Chunk: Reactive Action Chunking with Latent World Model, 2026. arXiv:2606.18589. [7] ArmnetBench v0.1: Parallel Real-World Evaluation of Manipulation Policies on a Low-Cost Arm Farm, 2026. arXiv:2607.24481. [8] TurboVLA: Real-Time Vision-Language-Action Model at 32 Hz on an RTX 4090 with <1 GB VRAM, 2026. arXiv:2607.27205. [9] Learning to Act While Waiting: RL Finetuning of Generalist Robot Policies Under Inference Latency, 2026. arXiv:2608.23831. [10] When to Switch: Reliable Action-Chunk Extension for Vision-Language-Action Models, 2026. arXiv:2610.05719. [11] Kevin Black, Manuel Y. Galliker, and Sergey Levine. Real-Time Execution of Action Chunking Flow Policies, 2025. arXiv:2506.07339. [12] Liang et al. Adaptive Action Chunking at Inferencetime for Vision-Language-Action Models, 2026. arXiv:2604.04161; CVPR 2026. [13] Nomura, Osa, Kato, Ota, Shitanda, and Harada. Smooth Action Chunking Via Movement-Primitive Representations for Imitation Learning, 2026. arXiv:2610.39451. [14] Mustafa Shukor, Dana Aubakirova, Francesco Capuano, et al. SmolVLA: A Vision-Language-Action Model for Affordable and Eﬀicient Robotics, 2025. arXiv:2506.01844. github.com/ravediamond/paper-vla-edge-inference · 3e85729
