# paper-reward-models-stopping-rule: chunks in paper order

## rendered source (numbers filled)

### Abstract (mean 0.175)

<!-- editlens chunk 0.175 lines 9-16 -->
<!-- editlens paragraph 0.175 lines 9-16 -->
Reward models that score robot rollouts are also used as failure detectors. We compared two zero-shot reward models with plain episode length. On ArmnetBench, a public SO-101 benchmark where runs end at a time limit, length separates failure from success at AUROC 0.942 within policy. Failed runs are slow rather than cut off. Length observed only up to half of the longest episode still gives 0.851. Both reward models score below length, the better one at 0.821. On our own rollouts an operator stopped each run by judgment. There length falls to 0.56, and neither reward model beats the identity of the policy. A judge that sees the finished episode passes its threshold, at an operating point chosen in-sample. No mid-episode monitor reaches its bar. The baseline a detector has to beat depends on the dataset's stopping rule.

### 1 Introduction (mean 0.176)

<!-- editlens chunk 0.176 lines 20-33 -->
<!-- editlens paragraph 0.299 lines 20-25 -->
Papers that evaluate a reward model as a failure detector normally compare it with other learned detectors. When a benchmark stops failed runs at a time limit, the length of an episode also encodes its outcome. The identity of the policy that ran can carry it too, and we call this the policy-identity null (mainly with models that give out-of-distribution results). When the operator stops each run by his judgment, both signals are weaker. We call the way a dataset ends its episodes its stopping rule. None of the reward-model papers in our library reports the stopping rule or a length baseline.

<!-- editlens paragraph 0.271 lines 27-29 -->
We started with a narrower claim, that elapsed time is the reward model to beat. Our own rollouts did not support it. On them length is near chance, and a robot-trained judge passed its pre-registered threshold. The stopping rule separates the two results, so it became the subject of the paper.

<!-- editlens paragraph 0.093 lines 31-33 -->
We measured length on ArmnetBench and on our own rollouts. The length analyses were frozen before any number existed. We compared length with two zero-shot reward models, Robometer and TOPReward. On our 88 operator-stopped rollouts we also compared it with every judge and monitor we had run.

### 2 Data and labels (mean 0.211)

<!-- editlens chunk 0.211 lines 37-42 -->
<!-- editlens paragraph 0.211 lines 37-42 -->
ArmnetBench v0.1 has 8 tasks and 7 policies on the SO-101. We use its 2,047 policy rollouts with a success or failure class (515 successes, 1,532 failures). We leave out the teleoperated episodes. One task, pushing a Displayport cable (270 rollouts), has rollouts of a single class and so no per-task AUROC. Our own data are 88 labelled bowls-task episodes on one SO-101 arm with a Jetson Orin NX. Every monitor gate used the same 50-episode subset (42 successes, 8 failures). The author was the operator. He stopped each run and labelled it at rest, not blind to the policy.

### 3 The length baseline (mean 0.125)

<!-- editlens chunk 0.125 lines 46-56 -->
<!-- editlens paragraph 0.176 lines 46-48 -->
On ArmnetBench, episode length is a strong failure detector within each policy (Table 1, Fig. 1). Pooled over policies it reaches 0.938. Within each policy it ranges from 0.91 to 0.96. Pair-weighted, the within-policy value is 0.942, with a CI of 0.927–0.956.

<!-- editlens paragraph 0.147 lines 50-56 -->
We ran Robometer-4B zero-shot, as its authors ship it. It scores 0.818 pooled and 0.821 within policy. The within-policy value is pair-weighted over its per-policy scores, and their range stands in for a CI (§7). We ran TOPReward with Qwen3-VL-8B and no training. It scores 0.661 within policy. Its paired difference to length has a 95 % CI of -0.31 to -0.25. The protocols fixed each model's primary score before any score existed. For Robometer it is the success probability, and for TOPReward the success score of its paper. Two other scores from the same runs are in Table 1 as descriptive rows. They are higher, and still below length.

### 4 Length is more than the timeout (mean 0.189)

<!-- editlens chunk 0.189 lines 73-85 -->
<!-- editlens paragraph 0.285 lines 73-76 -->
We take each task's longest episode as its timeout. Only 8.7 % of failures run that long. At half that length, 88 % of failures are still running. Only 19 % of successes are. Length observed up to that cut gives 0.851 within policy (CI 0.829–0.873; Fig. 2). TOPReward on frames up to the same cut reaches 0.667. Failed rollouts are slow, not timed out. Both readings fixed in the protocol hold.

<!-- editlens paragraph 0.100 lines 80-85 -->
On our own operator-stopped rollouts, length is at chance. It gives 0.56 on the 69 rollouts TOPReward scored and 0.52 on all 88. Here the policy-identity null is the baseline to beat. 17 of the 25 failures in the 69 come from one policy, TurboVLA. Neither reward model beats policy identity. TOPReward scores 0.82 (CI 0.70–0.93), and policy identity alone 0.87. On the 50 episodes without TurboVLA, TOPReward scores 0.78. Robometer scores 0.577 on all 88, and policy identity 0.878.

### 5 Judges and monitors on our rollouts (mean 0.173)

<!-- editlens chunk 0.173 lines 89-108 -->
<!-- editlens paragraph 0.224 lines 92-100 -->
We first ran a deterministic top-camera check (colour masks and geometry, no learning). It is right on 94.3 % of judged episodes. It has 0 false positives (Wilson 0–13 %) and 5 false negatives. We then gave Flora-Rewarder-27B a 64-frame two-view clip and NVIDIA's prompt. It reaches a threshold-free AUROC of 1.00 (bootstrap CI 1.00–1.00). At its in-sample operating point it flags 8 of 8 failures at 2 of 42 successes (Wilson on the false alarms 1–16 %). The pre-registered bar was at least 6 of 8 failures at no more than 2 of 42 successes, so it passes. Its base model, Qwen3.5-27B, has no robot fine-tune. On the same input it also passes, with AUROC 0.91 (0.78–1.00) and 7 of 8 at 2 of 42. The input format mattered more than the fine-tune. Qwen3.5-9B flags 16 successes and fails. Gemini 3.8 Flash fails by one false alarm.

<!-- editlens paragraph 0.269 lines 102-108 -->
The bar for mid-episode monitors is at least 5 of 8 failures at no more than 1 of 20 false interventions. No monitor reaches it on these 50 rollouts (Fig. 3). The surprise of a separate world model, trained in the LeWorldModel recipe, catches 2 of 8 at 2 of 42 (AUROC 0.86). A Gemini sliding-window judge catches 0. We also built an action-conditioned risk head on the world model's latent. Its first version reached AUROC 0.93. It read elapsed time, so we withdrew that result. We pre-registered a second version without time or length. It catches 3 of 8 at 5 of 42. Its AUROC is 0.79, and 0.71 with shuffled actions. The MLP variant catches 6 of 8 and flags 13 of 42.

### 6 Related work (mean 0.301)

<!-- editlens chunk 0.301 lines 129-137 -->
<!-- editlens paragraph 0.301 lines 129-137 -->
Robometer scales a general-purpose reward model through trajectory comparisons. TOPReward reads the token probabilities of a video-language model as hidden rewards. A survey of verifiers for robot policies covers the wider family. FAIL-Detect and SAFE learn uncertainty- and feature-based failure scores for imitation and VLA policies. FARM reads failure signals from the internal states of a frozen world model, like our world-model monitors. ReAP predicts action-conditioned risk, and our risk head follows it. VLA-Corrector verifies stages, Spotter adds a reflecting VLM, and REMORA tracks progress through errors and recovery. ArmnetBench and a standardized SO-101 VLA benchmark evaluate policies on the same arm. None of these works reports the elapsed-length baseline under the dataset's stopping rule.

### 7 Limitations (mean 0.121)

<!-- editlens chunk 0.121 lines 141-150 -->
<!-- editlens paragraph 0.121 lines 141-150 -->
The judge pass on our own rollouts rests on 8 failures. Its operating thresholds were chosen on the same 50 episodes. A single operator, the author, labelled them and was not blind to the policy. The threshold-free AUROCs do not depend on the threshold. Fresh rollouts scored at the frozen thresholds would confirm the operating points. 17 of the 25 failures in our 69 rollouts are TurboVLA's. Any score that reads the policy therefore gets the policy-identity null for free. The risk head is trained and tested on the same 50 episodes. Five folds by episode keep episodes from leaking, but tasks and policies leak. Robometer's per-episode scores stayed on an older machine. Its within-policy number therefore has no episode-bootstrap CI, and it is missing from the truncation analysis. A copy from that machine or a re-score of about $6 would restore both. TOPReward's paper does not give its prefix count, frames per query or Yes/No wording, so those are our choices. The ArmnetBench result covers eight tasks. The timeout is approximated by each task's longest episode.

### 8 Conclusion (mean 0.193)

<!-- editlens chunk 0.193 lines 154-157 -->
<!-- editlens paragraph 0.193 lines 154-157 -->
On ArmnetBench, where runs end at a time limit, episode length beat both reward models. On our operator-stopped rollouts length was at chance, and a judge that saw the whole finished episode caught the failures. When you evaluate a reward model as a failure detector, report episode length within policy on the same rows and say how the episodes ended.

### Appendix: from plain name to analysis (mean 0.240)

<!-- editlens chunk 0.240 lines 161-161 -->
Every number is recomputable from the repository; this table maps each analysis to its files.

### (figure and table captions) (mean 0.084)

<!-- editlens chunk 0.084 lines 58-125 -->
Table 1: ArmnetBench, failure AUROC with 95 % episode-bootstrap CIs. Read down the within-policy column: no reward-model score reaches length.
Failure AUROC on ArmnetBench: episode length against two zero-shot reward models. Length leads both, pooled and within policy (95 % CIs where available).
Length observed up to a fraction of the task's longest episode, AUROC within policy: most of the signal is there by half the episode (band: 95 % CI).
Table 2: Judges and monitors on the 50 operator-stopped rollouts (42 successes, 8 failures). Judges see the finished episode; monitors are held to ≥ 5/8 caught at ≤ 1/20 false interventions.
Failures caught against successes flagged on the 50 rollouts. No monitor (circles) reaches its shaded bar; the judges at rest (squares) sit at their in-sample operating point, where the monitor bar does not apply.

## built PDF

### (front matter) (mean 0.060)

<!-- editlens chunk 0.046 lines 3-46 -->
<!-- editlens paragraph 0.045 lines 3-27 -->
What a reward model can show depends on who stopped the episode: failure judges and monitors on a low-cost arm Ravindu Somawansa Shisso Robotics, Paris ravindu.somawansa@shissorobotics.com∗ We measured length on ArmnetBench [12] and on our own rollouts. The length analyses were frozen before any number existed. We compared length with two zeroAbstract shot reward models, Robometer [5] and TOPReward [1]. Reward models that score robot rollouts are also used On our 88 operator-stopped rollouts we also compared it as failure detectors. We compared two zero-shot reward with every judge and monitor we had run. models with plain episode length. On ArmnetBench, a public SO-101 benchmark where runs end at a time limit, length separates failure from success at AUROC 0.942 2 Data and labels within policy. Failed runs are slow rather than cut off. Length observed only up to half of the longest episode ArmnetBench v0.1 [12] has 8 tasks and 7 policies on the still gives 0.851. Both reward models score below length, SO-101. We use its 2,047 policy rollouts with a success the better one at 0.821. On our own rollouts an opera- or failure class (515 successes, 1,532 failures). We leave tor stopped each run by judgment. There length falls to out the teleoperated episodes. One task, pushing a Dis0.56, and neither reward model beats the identity of the playport cable (270 rollouts), has rollouts of a single class policy. A judge that sees the finished episode passes its and so no per-task AUROC. Our own data are 88 labelled threshold, at an operating point chosen in-sample. No bowls-task episodes on one SO-101 arm with a Jetson mid-episode monitor reaches its bar. The baseline a de- Orin NX. Every monitor gate used the same 50-episode tector has to beat depends on the dataset’s stopping rule. subset (42 successes, 8 failures). The author was the operator. He stopped each run and labelled it at rest, not blind to the policy.

<!-- editlens paragraph 0.195 lines 32-46 -->
Papers that evaluate a reward model as a failure detector normally compare it with other learned detectors. When a benchmark stops failed runs at a time limit, the length of an episode also encodes its outcome. The identity of the policy that ran can carry it too, and we call this the policy-identity null (mainly with models that give outof-distribution results). When the operator stops each run by his judgment, both signals are weaker. We call the way a dataset ends its episodes its stopping rule. None of the reward-model papers in our library reports the stopping rule or a length baseline. We started with a narrower claim, that elapsed time is the reward model to beat. Our own rollouts did not support it. On them length is near chance, and a robottrained judge passed its pre-registered threshold. The stopping rule separates the two results, so it became the subject of the paper.

<!-- editlens chunk 0.078 lines 51-146 -->
<!-- editlens paragraph 0.093 lines 51-70 -->
On ArmnetBench, episode length is a strong failure detector within each policy (Table 1, Fig. 1). Pooled over policies it reaches 0.938. Within each policy it ranges from 0.91 to 0.96. Pair-weighted, the within-policy value is 0.942, with a CI of 0.927–0.956. We ran Robometer-4B [5] zero-shot, as its authors ship it. It scores 0.818 pooled and 0.821 within policy. The within-policy value is pair-weighted over its per-policy scores, and their range stands in for a CI (§7). We ran TOPReward [1] with Qwen3-VL-8B [11] and no training. It scores 0.661 within policy. Its paired difference to length has a 95 % CI of -0.31 to -0.25. The protocols fixed each model’s primary score before any score existed. For Robometer it is the success probability, and for TOPReward the success score of its paper. Two other ∗ Code, result files and the checks that regenerate every number: scores from the same runs are in Table 1 as descriptive github.com/ravediamond/paper-reward-models-stopping-rule. rows. They are higher, and still below length. The frozen protocols are copied verbatim under repro/; the bar commits named in the paper belong to the authors’ research repository ravediamond/road-to-robotics.

<!-- editlens chunk 0.064 lines 151-202 -->
the judges at rest, that point is chosen in-sample. We first ran a deterministic top-camera check (colour length seen up to 50 % of T, within policy masks and geometry, no learning). It is right on 94.3 % 0.818 Robometer-4B zero-shot, pooled of judged episodes. It has 0 false positives (Wilson 0–13 then gave Flora-Rewarder-27B [8] a 64-frame two-view 0.838 Robometer-4B last progress, pooled (no CI) clip and NVIDIA’s prompt. It reaches a threshold-free 0.661 TOPReward (Qwen3-VL-8B), within policy AUROC of 1.00 (bootstrap CI 1.00–1.00). At its in-sample operating point it flags 8 of 8 failures at 2 of 42 successes 0.6 0.8 1.0 (Wilson on the false alarms 1–16 at least 6 of 8 failures failure AUROC, n = 2,047 at no more than 2 of 42 successes, so it passes. Its base model, Qwen3.5-27B [10], has no robot fine-tune. On the Figure 1: Failure AUROC on ArmnetBench: episode same input it also passes, with AUROC 0.91 (0.78–1.00) length against two zero-shot reward models. Length and 7 of 8 at 2 of 42. The input format mattered more leads both, pooled and within policy (95 % CIs where than the fine-tune. Qwen3.5-9B [10] flags 16 successes available). and fails. Gemini 3.8 Flash [2] fails by one false alarm. The bar for mid-episode monitors is at least 5 of 8 failures at no more than 1 of 20 false interventions. No mon4 Length is more than the timeout itor reaches it on these 50 rollouts (Fig. 3). The surprise of a separate world model, trained in the LeWorldModel We take each task’s longest episode as its timeout. Only recipe [7], catches 2 of 8 at 2 of 42 (AUROC 0.86). A 8.7 % of failures run that long. At half that length, 88 % Gemini sliding-window judge catches 0. We also built an of failures are still running. Only 19 % of successes are. action-conditioned risk head on the world model’s latent. Length observed up to that cut gives 0.851 within policy Its first version reached AUROC 0.93. It read elapsed (CI 0.829–0.873; Fig. 2). TOPReward on frames up to time, so we withdrew that result. We pre-registered a the same cut reaches 0.667. Failed rollouts are slow, not second version without time or length. It catches 3 of 8 timed out. Both readings fixed in the protocol hold. at 5 of 42. Its AUROC is 0.79, and 0.71 with shuffled acOn our own operator-stopped rollouts, length is at tions. The MLP variant catches 6 of 8 and flags 13 of 42. chance. It gives 0.56 on the 69 rollouts TOPReward scored and 0.52 on all 88. Here the policy-identity null is the baseline to beat. 17 of the 25 failures in the 69 come 6 Related work from one policy, TurboVLA [16]. Neither reward model beats policy identity. TOPReward scores 0.82 (CI 0.70– Robometer [5] scales a general-purpose reward model 0.93), and policy identity alone 0.87. On the 50 episodes through trajectory comparisons. TOPReward [1] reads without TurboVLA, TOPReward scores 0.78. Robometer the token probabilities of a video-language model as hidden rewards. A survey of verifiers for robot policies [14] scores 0.577 on all 88, and policy identity 0.878.

<!-- editlens chunk 0.060 lines 151-346 -->
<!-- editlens paragraph 0.123 lines 312-316 -->
about $6 would restore both. TOPReward’s paper does not give its prefix count, frames per query or Yes/No wording, so those are our choices. The ArmnetBench result covers eight tasks. The timeout is approximated by each task’s longest episode.

<!-- editlens paragraph 0.038 lines 329-346 -->
On ArmnetBench, where runs end at a time limit, episode length beat both reward models. On our 0 2 4 6 8 10 12 14 16 operator-stopped rollouts length was at chance, and a successes flagged (of 42) judge that saw the whole finished episode caught the failures. When you evaluate a reward model as a failure deFigure 3: Failures caught against successes flagged on the tector, report episode length within policy on the same 50 rollouts. No monitor (circles) reaches its shaded bar; rows and say how the episodes ended. the judges at rest (squares) sit at their in-sample operating point, where the monitor bar does not apply. 0

### Appendix: from plain name to analysis (mean 0.104)

<!-- editlens chunk 0.104 lines 511-530 -->
<!-- editlens paragraph 0.104 lines 511-530 -->
farm. arXiv preprint arXiv:2607.24481, 2026. [13] Chang Song, Bin Qian, Yan Feng, and Zhijie Song. Every number is recomputable from the repository; this Vla-corrector: Stage-aware observable state under- table maps each analysis to its files. standing for prompt-based closed-loop recovery of vision-language-action policies. arXiv preprint arXiv:2609.06508, 2026. [14] Yang Wan, Xihang Yue, Zhirui Liu, Ziyuan Chu, Shuxun Wang, Yuhan Chen, et al. No free checker: A survey of verifiers for robot policies. arXiv preprint arXiv:2609.09250, 2026. [15] Chen Wang, Xinze Niu, Zihao Zhu, Keru Zhou, Yicheng Xu, Shihao Jin, et al. Tracking task progress through errors and recovery: A benchmark and recurrent distributional model. arXiv preprint arXiv:2610.39125, 2026. [16] Hengyi Xie, Chenfei Yao, Xianjin Wu, Yingying Zhu, Dingkang Liang, Xiang Bai, et al. Turbovla: Real-time vision-language-action model at 32 hz github.com/ravediamond/paper-reward-models-stopping-rule · f995e0d
