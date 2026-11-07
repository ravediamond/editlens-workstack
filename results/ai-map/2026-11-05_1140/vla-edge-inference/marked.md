# paper-vla-edge-inference: chunks in paper order

## rendered source (numbers filled)

### Abstract (mean 0.339)

<!-- editlens chunk 0.339 lines 9-17 -->
<!-- editlens paragraph 0.339 lines 9-17 -->
On an edge GPU, most of a VLA's action chunk goes to vision, so a method that speeds up or smooths chunking keeps only the part of its benefit that touches the seam between chunks. We re-measured seven training-free methods, published with desktop-GPU numbers, where a low-cost robot runs its policy: SmolVLA on a Jetson Orin NX. Every gate had its threshold committed before the run, and all of them share one checkpoint and the same recorded episodes, so every number traces to a result file and a protocol commit. The vision encoder alone takes 151.0 of 219.0 ms of server time per chunk (25 W). The two seam methods pass: a gradient-free prefix overwrite cuts the boundary jump by 72 % or more, and movement-primitive seam conditioning removes most of the seam jerk. Sampling does not transfer, because on a sequential edge engine every N-sample method pays for N chunks in series. So on this board, smooth the seam and leave the sampler alone.

### 1 Introduction (mean 0.256)

<!-- editlens chunk 0.256 lines 21-32 -->
<!-- editlens paragraph 0.404 lines 21-25 -->
With several training-free chunking tricks published this year for flow-matching VLAs, it is tempting to think they make a policy faster or smoother on any robot. Their numbers come from desktop and data-centre GPUs (RTX 4090, A100, H100, RTX 5090). There a chunk costs tens of milliseconds, and spare compute can hide an extra pass. A robot people can buy runs its policy on an edge GPU instead, where most of the chunk goes to a part the tricks never touch (the vision encoder). So the useful question is how much of each trick is left on that board.

<!-- editlens paragraph 0.209 lines 27-32 -->
Ours is an SO-101 arm [arXiv:2606.08881] with a Jetson Orin NX 16 GB, running SmolVLA [arXiv:2506.01844] through vla.cpp, a C++ inference engine, on episodes recorded with LeRobot. This paper started once SmolVLA ran on the arm through vla.cpp: the next question was where the remaining time of a chunk went, and which published tricks could still buy something. We took seven of them. Each answer is a gate with a bar committed before the number; offline effects get an episode bootstrap, and latencies are medians of at least 50 calls. The appendix maps every number to its result file and protocol commit.

### 2 Where the time goes (mean 0.219)

<!-- editlens chunk 0.219 lines 36-42 -->
<!-- editlens paragraph 0.168 lines 36-39 -->
Follow one chunk. At ten Euler steps and full power (MAXN_SUPER) it costs 237.5 ms end to end: 150.7 ms of vision, 14.9 ms of prefill and 5.3 ms per denoise step (Fig. 1). At 25 W the server-side split is 151.0 ms of vision in 219.0 ms. A trick that only touches the denoising loop therefore works on at most a quarter of that chunk.

### 3 Seven tricks, one checkpoint (mean 0.222)

<!-- editlens chunk 0.222 lines 48-76 -->
<!-- editlens paragraph 0.300 lines 51-56 -->
The two tricks that pass both act where our chunk meets the next one. Overwriting the new chunk's executed prefix with the actions already committed passes the 50 % jump-cut bar at every delay, in PyTorch and in vla.cpp, where it adds 0.4 ms per chunk. Movement-primitive chunking [arXiv:2610.39451] passes as well. Projecting each chunk onto ten Gaussian bases keeps the error within its bar while removing within-chunk jerk, and conditioning on the last action sent removes 83–87 % of the seam jerk at +0.19° of error (its paper reports 73–84 %; ours is measured on the commanded stream only).

<!-- editlens paragraph 0.252 lines 58-60 -->
Exact real-time chunking [arXiv:2506.07339], which inpaints the prefix with guidance instead of overwriting it, cuts the jump by less than the 50 % pass mark at every delay (Fig. 2). It also costs 1.9× a naive chunk in PyTorch.

<!-- editlens paragraph 0.349 lines 62-67 -->
Cutting the Euler steps from ten to two [arXiv:2610.32102] saves 41 ms per chunk at full power (real, but small next to the vision cost). The paper's central claim, that the action cloud contracts around an unchanged centroid, is not proven here: our cloud ratio of 0.78 falls between the bar of 0.70 and the fail line of 0.85, where the paper reports 0.51 on π0. The paper also expects fewer steps to remove edge-GPU thermal throttling, but our Orin did not throttle at ten steps in either power mode. We keep ten steps, as the protocol's rule says while the contraction is unproven.

<!-- editlens paragraph 0.279 lines 69-76 -->
Both sampling tricks pay for their samples one after another. Speculative chunk selection [arXiv:2610.28019] uses the pre-commit frame to pick, among four candidates, the chunk closest to the recorded teleoperation continuation, and offline it does beat a random pick (one continuation per frame, training-set episodes, open loop). Its paper promises no added control-step delay. On the Orin, vla.cpp samples the candidates in sequence, so a cycle costs 1,200 ms and 37 control ticks against 8 for a naive chunk (Fig. 3). Entropy-adaptive chunk length [arXiv:2604.04161] is the clearest miss. One 20-sample decision takes 4,751 ms on the Orin against a threshold of 298 ms, because the samples run one after another. Its chosen length also sits at the floor in both task phases, and the jump is no better than with fixed chunks and the overwrite.

### 4 What transfers to the board (mean 0.207)

<!-- editlens chunk 0.207 lines 96-102 -->
<!-- editlens paragraph 0.207 lines 96-102 -->
Turn on the prefix overwrite and the primitive projection with seam conditioning. Both act on the seam, which the vision cost does not hide, and each costs under a millisecond on this board, so there is little reason to leave them off. Ten Euler steps stay until the contraction passes its threshold; the two-step saving is real but small because vision dominates. Sampling several chunks per decision does not pay on a sequential edge engine, since exact guidance, speculative selection and adaptive length all pay for N chunks in series. Before turning one of them on, check whether your engine samples in a batch (ours does not). This version is offline and latency only. The closed-loop columns on the arm, seam smoothing and the overwrite in the robot client, belong to a longer version.

### 5 Related work (mean 0.182)

<!-- editlens chunk 0.182 lines 106-112 -->
<!-- editlens paragraph 0.182 lines 106-112 -->
Other chunking tricks are also reported on desktop-class GPUs, and we did not re-measure them here: extending the executing chunk instead of resampling [arXiv:2610.05719], reactive chunking driven by a latent world model [arXiv:2606.18589], and fine-tuning the policy for latency with reinforcement learning [arXiv:2608.23831]. On the engine side, TurboVLA [arXiv:2607.27205] pushes VLA throughput on a desktop GPU, while vla.cpp, the engine we measure, runs VLAs on edge boards. Two works use the same arm. A standardized benchmark reports failures and recoveries of VLA policies [arXiv:2606.08881], and a fleet of SO-101 cells evaluates policies at scale [arXiv:2607.24481]. Both evaluate policies, while we re-measure the execution tricks around one policy under bars fixed before the run.

### 6 Limitations (mean 0.191)

<!-- editlens chunk 0.191 lines 116-123 -->
<!-- editlens paragraph 0.191 lines 116-123 -->
The sampling result is conditional on the engine. vla.cpp samples sequentially, and we contribute to it (the overwrite runs on our fork, X). Parity and determinism checks against PyTorch on the same board are in the gate logs. A batched sampler is the control that would test the conclusion, and it has not run. Effects other than latency are offline, measured on 20 recorded demonstrations of one task family (bowls) that the policy was trained on. The arm gates for seam smoothing and for the overwrite in the robot client are the next step; the adaptive-length arm gate was left out because SmolVLA is at ceiling on this task, so a gain could not show. Latency rows run at MAXN_SUPER and the serving and boundary rows at 25 W, which makes power mode a confound wherever the two are compared. The study covers one policy, SmolVLA at 450M, since π0-class models do not fit on the Orin.

### Appendix: from plain name to gate (mean 0.172)

<!-- editlens chunk 0.172 lines 127-127 -->
Every number in this paper is recomputable from the repository; this table maps each experiment to its files.

### (figure and table captions) (mean 0.293)

<!-- editlens chunk 0.293 lines 44-92 -->
Fig. 1 — where one SmolVLA chunk's time goes on the Orin NX (vla.cpp, ten Euler steps, MAXN_SUPER): vision is most of it
Table 1: Seven tricks on one checkpoint. Read the acts-on column against the verdict: the seam tricks pass, the sampling tricks fail.
Fig. 2 — median boundary-jump cut against naive asynchronous execution (254 boundaries per delay, 25 W): the overwrite clears the 50 % bar at every delay, exact RTC guidance does not.
Fig. 3 — cost per decision on the Orin NX (log scale, MAXN_SUPER): both sampling methods miss their bar (dashed: AAC's 298 ms; PACT's bar is one chunk, 237.5 ms).

## built PDF

### Abstract (mean 0.162)

<!-- editlens chunk 0.162 lines 12-79 -->
<!-- editlens paragraph 0.354 lines 12-29 -->
On an edge GPU, most of a VLA’s action chunk goes to vision, so a method that speeds up or smooths chunking keeps only the part of its benefit that touches the seam between chunks. We re-measured seven training-free methods, published with desktop-GPU numbers, where a low-cost robot runs its policy: SmolVLA on a Jetson Orin NX. Every gate had its threshold committed before the run, and all of them share one checkpoint and the same recorded episodes, so every number traces to a result file and a protocol commit. The vision encoder alone takes 151.0 of 219.0 ms of server time per chunk (25 W). The two seam methods pass: a gradient-free prefix overwrite cuts the boundary jump by 72 % or more, and movement-primitive seam conditioning removes most of the seam jerk. Sampling does not transfer, because on a sequential edge engine every N-sample method pays for N chunks in series. So on this board, smooth the seam and leave the sampler alone.

<!-- editlens paragraph 0.394 lines 56-62 -->
Figure 1: Where one SmolVLA chunk’s time goes on the Orin NX (vla.cpp, ten Euler steps, MAXN_SUPER): vision is most of it. tricks could still buy something. We took seven of them. Each answer is a gate with a bar committed before the number; offline effects get an episode bootstrap, and latencies are medians of at least 50 calls. The appendix maps every number to its result file and protocol commit.

<!-- editlens paragraph 0.119 lines 67-79 -->
Follow one chunk. At ten Euler steps and full power (MAXN_SUPER) it costs 237.5 ms end to end: 150.7 ms of vision, 14.9 ms of prefill and 5.3 ms per denoise step With several training-free chunking tricks published this (Fig. 1). At 25 W the server-side split is 151.0 ms of vision year for flow-matching VLAs, it is tempting to think they in 219.0 ms. A trick that only touches the denoising loop make a policy faster or smoother on any robot. Their therefore works on at most a quarter of that chunk. numbers come from desktop and data-centre GPUs (RTX Two power modes appear because each gate’s protocol 4090, A100, H100, RTX 5090). There a chunk costs tens of froze the mode it ran in (the serving split and the boundmilliseconds, and spare compute can hide an extra pass. ary experiments at 25 W, the latency experiments at full A robot people can buy runs its policy on an edge GPU power). Every number below carries its mode. instead, where most of the chunk goes to a part the tricks never touch (the vision encoder). So the useful question

### 3 Seven tricks, one checkpoint (mean 0.068)

<!-- editlens chunk 0.068 lines 80-93 -->
<!-- editlens paragraph 0.068 lines 80-93 -->
is how much of each trick is left on that board. Ours is an SO-101 arm [3, 5] with a Jetson Orin NX All offline effects use the same SmolVLA checkpoint and 16 GB [2], running SmolVLA [14] through vla.cpp [4], a the same 20 recorded episodes, with 254 chunk boundC++ inference engine, on episodes recorded with LeRaries per delay. Table 1 carries every effect, bar and verobot [1]. This paper started once SmolVLA ran on the dict; the text covers what the table cannot show. arm through vla.cpp: the next question was where the The two tricks that pass both act where our chunk remaining time of a chunk went, and which published meets the next one. Overwriting the new chunk’s exe∗ Every number with its source file and protocol commit: cuted prefix with the actions already committed passes github.com/ravediamond/paper-vla-edge-inference. the 50 % jump-cut bar at every delay, in PyTorch and

### 2 Euler steps (mean 0.076)

<!-- editlens chunk 0.076 lines 152-196 -->
<!-- editlens paragraph 0.099 lines 165-196 -->
Turn on the prefix overwrite and the primitive projection with seam conditioning. Both act on the seam, which the vision cost does not hide, and each costs under a millisecin vla.cpp, where it adds 0.4 ms per chunk. Movement- ond on this board, so there is little reason to leave them primitive chunking [13] passes as well. Projecting each off. Ten Euler steps stay until the contraction passes its chunk onto ten Gaussian bases keeps the error within its threshold; the two-step saving is real but small because bar while removing within-chunk jerk, and conditioning vision dominates. Sampling several chunks per decision on the last action sent removes 83–87 % of the seam jerk does not pay on a sequential edge engine, since exact at +0.19◦ of error (its paper reports 73–84 %; ours is mea- guidance, speculative selection and adaptive length all sured on the commanded stream only). pay for N chunks in series. Before turning one of them Exact real-time chunking [11], which inpaints the pre- on, check whether your engine samples in a batch (ours fix with guidance instead of overwriting it, cuts the jump does not). This version is offline and latency only. The by less than the 50 % pass mark at every delay (Fig. 2). It closed-loop columns on the arm, seam smoothing and also costs 1.9× a naive chunk in PyTorch. the overwrite in the robot client, belong to a longer verCutting the Euler steps from ten to two [15] saves 41 ms sion. per chunk at full power (real, but small next to the vision cost). The paper’s central claim, that the action cloud contracts around an unchanged centroid, is not proven 5 Related work here: our cloud ratio of 0.78 falls between the bar of 0.70 and the fail line of 0.85, where the paper reports 0.51 on Other chunking tricks are also reported on desktop-class π0. The paper also expects fewer steps to remove edge- GPUs, and we did not re-measure them here: extending GPU thermal throttling, but our Orin did not throttle at the executing chunk instead of resampling [10], reactive ten steps in either power mode. We keep ten steps, as the chunking driven by a latent world model [6], and finetuning the policy for latency with reinforcement learnprotocol’s rule says while the contraction is unproven. Both sampling tricks pay for their samples one af- ing [9]. On the engine side, TurboVLA [8] pushes VLA ter another. Speculative chunk selection [16] uses the throughput on a desktop GPU, while vla.cpp [4], the enpre-commit frame to pick, among four candidates, the gine we measure, runs VLAs on edge boards. Two works chunk closest to the recorded teleoperation continuation, use the same arm. A standardized benchmark reports and offline it does beat a random pick (one continua- failures and recoveries of VLA policies [5], and a fleet tion per frame, training-set episodes, open loop). Its pa- of SO-101 cells evaluates policies at scale [7]. Both evalper promises no added control-step delay. On the Orin, uate policies, while we re-measure the execution tricks vla.cpp samples the candidates in sequence, so a cycle around one policy under bars fixed before the run. costs 1,200 ms and 37 control ticks against 8 for a naive chunk (Fig. 3). Entropy-adaptive chunk length [12] is

### 6 Limitations (mean 0.067)

<!-- editlens chunk 0.067 lines 197-227 -->
<!-- editlens paragraph 0.091 lines 197-207 -->
the clearest miss. One 20-sample decision takes 4,751 ms on the Orin against a threshold of 298 ms, because the The sampling result is conditional on the engine. vla.cpp samples run one after another. Its chosen length also sits samples sequentially, and we contribute to it (the overat the floor in both task phases, and the jump is no better write runs on our fork, ravediamond/vla.cpp). Parity than with fixed chunks and the overwrite. and determinism checks against PyTorch on the same board are in the gate logs. A batched sampler is the github.com/ravediamond/paper-vla-edge-inference · 4cb31cd

<!-- editlens paragraph 0.080 lines 210-227 -->
control that would test the conclusion, and it has not [13] Nomura, Osa, Kato, Ota, Shitanda, and Harada. run. Effects other than latency are offline, measured on Smooth Action Chunking Via Movement-Primitive 20 recorded demonstrations of one task family (bowls) Representations for Imitation Learning, 2026. that the policy was trained on. The arm gates for seam arXiv:2610.39451. smoothing and for the overwrite in the robot client are the next step; the adaptive-length arm gate was left out [14] Mustafa Shukor, Dana Aubakirova, Francesco Capuano, et al. SmolVLA: A Vision-Language-Action because SmolVLA is at ceiling on this task, so a gain Model for Affordable and Eﬀicient Robotics, 2025. could not show. Latency rows run at MAXN_SUPER and arXiv:2506.01844. the serving and boundary rows at 25 W, which makes power mode a confound wherever the two are compared. [15] Yang et al. Coupling Execution Horizon and SamThe study covers one policy, SmolVLA at 450M, since π0 pling Depth in Flow-Matching VLA Policies, 2026. class models do not fit on the Orin. arXiv:2610.32102.

### Appendix: from plain name to gate (mean 0.131)

<!-- editlens chunk 0.131 lines 245-442 -->
<!-- editlens paragraph 0.109 lines 248-274 -->
[4] vla.cpp. https://github.com/VinRobotics/vla. cpp. C++ inference engine for VLA policies; the engine commit of each measurement is in the gate logs. [5] Benchmarking Vision-Language-Action Models on SO-101: Failure and Recovery Analysis, 2026. arXiv:2606.08881. [6] DREAM-Chunk: Reactive Action Chunking with Latent World Model, 2026. arXiv:2606.18589. [7] ArmnetBench v0.1: Parallel Real-World Evaluation of Manipulation Policies on a Low-Cost Arm Farm, 2026. arXiv:2607.24481. [8] TurboVLA: Real-Time Vision-Language-Action Model at 32 Hz on an RTX 4090 with <1 GB VRAM, 2026. arXiv:2607.27205. [9] Learning to Act While Waiting: RL Finetuning of Generalist Robot Policies Under Inference Latency, 2026. arXiv:2608.23831. [10] When to Switch: Reliable Action-Chunk Extension for Vision-Language-Action Models, 2026. arXiv:2610.05719. [11] Kevin Black, Manuel Y. Galliker, and Sergey Levine. Real-Time Execution of Action Chunking Flow Policies, 2025. arXiv:2506.07339. [12] Liang et al. Adaptive Action Chunking at Inferencetime for Vision-Language-Action Models, 2026. arXiv:2604.04161; CVPR 2026. github.com/ravediamond/paper-vla-edge-inference · 4cb31cd
