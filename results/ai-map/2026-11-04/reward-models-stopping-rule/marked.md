# paper-reward-models-stopping-rule: chunks in paper order

## rendered source (numbers filled)

### Abstract (mean 0.329)

<!-- editlens chunk 0.329 lines 9-17 -->
<!-- editlens paragraph 0.329 lines 9-17 -->
Reward models that score robot rollouts are also used as failure detectors, and the baseline they must beat depends on who stopped the episode. On 2,047 public SO-101 rollouts from 7 policies, where runs end at a time limit, plain episode length separates failure from success at AUROC 0.942 within policy. Half the run is enough: observed only up to half of the longest episode, length still gives 0.851. Failed runs are slow, not timed out. Both zero-shot reward models we test score below that baseline (the best reaches 0.821 within policy). On our own operator-stopped rollouts the regime flips. Length falls to 0.56, neither reward model beats the policy-identity null, and what works is a judge at rest: a robot-trained 27B judge passes its pre-registered bar, though its operating threshold is in-sample, and every mid-episode monitor we tested misses the bar. We recommend reporting a length baseline, within policy, and naming the dataset's stopping rule.

### 1 Introduction (mean 0.390)

<!-- editlens chunk 0.390 lines 21-31 -->
<!-- editlens paragraph 0.390 lines 21-31 -->
A reward model that scores robot rollouts is also a failure detector, and papers evaluate it as one. Any such evaluation has a hidden variable: the dataset's *stopping rule* — who decides that an episode is over. When a benchmark stops failed runs at a time limit, how long an episode ran encodes its outcome. A detector should then be read against the baselines the stopping rule hands out for free: elapsed length, and the identity of the policy that ran. When an operator stops each run by judgment, those baselines collapse, and the task changes. None of the reward-model papers in our library reports how far plain episode length gets on the same data. We measure it on a public SO-101 benchmark and on our own rollouts, with the length analyses frozen before the numbers, and set every learned judge and monitor we ran against it. Three things follow. First, a pre-registered length analysis of 2,047 public rollouts: pooled, within policy, and truncated in time. Second, the same analysis for two zero-shot reward models, with the stopping-rule baselines beside them. Third, judge and monitor gates on 88 operator-stopped rollouts of our own, every in-sample threshold disclosed.

### 2 Data and labels (mean 0.189)

<!-- editlens chunk 0.189 lines 35-39 -->
<!-- editlens paragraph 0.189 lines 35-39 -->
ArmnetBench v0.1 (SO-101, 8 tasks, 7 policies): 2,047 policy rollouts with a success or failure class (515 successes, 1,532 failures); teleoperated episodes excluded. One task (pushing a Displayport cable, 270 rollouts) has rollouts of a single class and so no per-task AUROC. Our rollouts: 88 labelled bowls-task episodes on one SO-101 arm and a Jetson Orin NX, and the 50-episode subset (42 successes, 8 failures) every monitor gate used. Labels are the operator's, not blind to policy.

### 3 The length baseline (mean 0.144)

<!-- editlens chunk 0.144 lines 43-53 -->
<!-- editlens paragraph 0.144 lines 43-53 -->
Table 1 carries the numbers. Pooled over policies, length gives 0.938 (CI 0.925–0.951); within each policy it ranges 0.91–0.96, pair-weighted 0.942 (CI 0.927–0.956): the baseline is not the policy identity (Fig. 1). Robometer-4B, run zero-shot as its authors ship it, gives 0.818 pooled (CI 0.790–0.843) and 0.821 within policy (pair-weighted over the per-policy scores, which span 0.79–0.87; its per-episode scores were not stored, so these carry no episode-bootstrap CI). The protocol fixed Robometer's primary score as its success probability; read descriptively from the same run, its last-progress head does better, 0.838 pooled, but stays below length. TOPReward (Qwen3-VL-8B, no training; the primary score, fixed before any score, is the paper's success score) gives 0.653 pooled (CI 0.623–0.684) and 0.661 within policy (CI 0.631–0.692), below length by -0.31 to -0.25 (paired 95 % CI); its full-video Yes/No component alone reaches 0.678 within policy, descriptively.

### 4 Is it the timeout? (mean 0.227)

<!-- editlens chunk 0.227 lines 70-80 -->
<!-- editlens paragraph 0.227 lines 70-80 -->
Only 8.7 % of failures run to the task's longest episode. Observing length only up to half of that, when 88 % of failures but 19 % of successes are still running, gives 0.851 within policy (CI 0.829–0.873; Fig. 2; TOPReward on frames up to the same cut: 0.667): failed rollouts are slow, not timed out. Both pre-registered readings hold: length is a within-policy null, and it is more than the timeout. On our own operator-stopped rollouts the same baseline is at chance (0.56 on the 69; 0.52 on all 88). Neither reward model beats the policy-identity null there: TOPReward 0.82 (CI 0.70–0.93) against 0.87 for policy identity alone, and 0.78 on the 50 episodes without TurboVLA (17 of the 25 failures in the 69 come from TurboVLA); Robometer 0.577 against 0.878 on 88. The baseline depends on how episodes end, which is why it must be reported per dataset; what works on operator-stopped runs is the judge at rest (§5).

### 5 Judges and monitors on our rollouts (mean 0.273)

<!-- editlens chunk 0.273 lines 86-107 -->
<!-- editlens paragraph 0.126 lines 86-88 -->
Table 2 carries every judge and monitor with the same triple: threshold-free AUROC where defined, failures caught and successes flagged at the operating point. Every operating threshold of the judges at rest is chosen in-sample on the same 50 episodes; the AUROCs are not.

<!-- editlens paragraph 0.340 lines 90-98 -->
**At rest.** A deterministic top-camera check (colour masks and geometry, no learning) is right on 94.3 % of judged episodes with 0 false positives (Wilson 0–13 %) and 5 false negatives. Given a 64-frame two-view clip and NVIDIA's prompt, Flora-Rewarder-27B reaches a threshold-free AUROC of 1.00 (bootstrap CI 1.00–1.00); at its in-sample operating point it flags 8 of 8 failures at 2 of 42 successes (Wilson on the false alarms 1–16 %) and passes its pre-registered bar. Its base model Qwen3.5-27B reaches 0.91 (0.78–1.00; 7/8 at 2/42) on the same input at its own in-sample threshold; Qwen3.5-9B reaches 0.75 (7/8 at 16/42) and Gemini 3.8 Flash 0.96 (8/8 at 3/42, one false alarm over the bar): neither passes. The input format, not the robot fine-tune, decided the result.

<!-- editlens paragraph 0.393 lines 100-107 -->
**Mid-episode.** A Gemini sliding-window judge catches 0 of 8 failures at 1 of 42; the surprise of a separate world model, trained in the LeWorldModel recipe, catches 2 of 8 at 2 of 42 (AUROC 0.86, Wilson 7–59 %); the same model's latent drift catches 0 at 2 of 42 (AUROC 0.30). An action-conditioned risk head on the world model's latent reached 0.93 in a first version that read elapsed time, and that result is withdrawn; the pre-registered second version, without time or length, catches 3 of 8 at 5 of 42 (AUROC 0.79 against 0.71 with shuffled actions; Wilson 14–69 %), and its MLP variant 6 of 8 at 13 of 42. No monitor meets the bar of at least 5 of 8 failures at no more than 1 of 20 false interventions (Fig. 3).

### 6 Related work (mean 0.357)

<!-- editlens chunk 0.357 lines 128-138 -->
<!-- editlens paragraph 0.357 lines 128-138 -->
Reward models are increasingly proposed as zero-shot failure detectors for manipulation: Robometer scales a general-purpose reward model by trajectory comparisons, and TOPReward reads token probabilities of a video-language model as hidden rewards; a recent survey of verifiers for robot policies maps the wider family. Mid-episode failure detection is its own line: FAIL-Detect and SAFE learn uncertainty- and feature-based failure scores for imitation and VLA policies, FARM reads failure signals from the internal states of a frozen world model, ReAP predicts action-conditioned risk, VLA-Corrector verifies stages to drive prompt-based recovery, Spotter pairs the embodied model with a reflecting VLM, and REMORA tracks task progress through errors and recovery with a recurrent distributional model. Benchmarks on the same low-cost arm — ArmnetBench and a standardized SO-101 VLA benchmark — evaluate policies; none of these works reports the elapsed-length baseline under the dataset's stopping rule, which is the comparison this paper adds.

### 7 Limitations (mean 0.180)

<!-- editlens chunk 0.180 lines 142-149 -->
<!-- editlens paragraph 0.180 lines 142-149 -->
Two task families (ArmnetBench's eight tasks, our bowls task); our labels are the operator's and not blind; the risk head is trained and tested on the same 50 episodes (5-fold by episode: episodes do not leak, tasks and policies do); Robometer's within-policy and truncation analyses carry no episode-bootstrap CI and no truncation column because its per-episode scores were not stored; TOPReward's prefix count, frames per query and Yes/No wording are not given in its paper and are ours; the operating points of Flora-Rewarder-27B, Qwen3.5-27B and Gemini 3.8 Flash are chosen in-sample on the 50 episodes they are scored on (their AUROCs are not); 17 of the 25 failures in our 69 rollouts are TurboVLA's, so on our set any score that reads the policy gets the identity null for free; the timeout is approximated by each task's longest episode.

### Appendix: from plain name to analysis (mean 0.240)

<!-- editlens chunk 0.240 lines 153-153 -->
Every number is recomputable from the repository; this table maps each analysis to its files.

### (figure and table captions) (mean 0.127)

<!-- editlens chunk 0.127 lines 55-124 -->
<!-- editlens paragraph 0.111 lines 55-55 -->
Table 1: ArmnetBench, failure AUROC with 95 % episode-bootstrap CIs. The Robometer within-policy entry is pair-weighted over its per-policy block and carries the per-policy range instead of a CI (per-episode scores not stored); the last-progress entry is descriptive (the protocol's primary score was the success probability).

<!-- editlens paragraph 0.092 lines 66-66 -->
Failure AUROC on ArmnetBench (95 % CIs where available): episode length against two zero-shot reward models (Robometer-4B, TOPReward with Qwen3-VL-8B). The last-progress bar is descriptive and carries no CI. The Displayport-cable task contributes rollouts of one class only and has no per-task AUROC.

<!-- editlens paragraph 0.361 lines 109-109 -->
Table 2: Judges and monitors on 50 own operator-stopped rollouts (42 successes, 8 failures). Judges score the finished episode; monitors score mid-episode windows against the monitor bar (≥ 5/8 caught at ≤ 1/20 false interventions). "In-sample" marks an operating threshold chosen on these same 50 episodes.

<!-- editlens paragraph 0.364 lines 124-124 -->
Fifty own rollouts: failures caught (of 8) against successes flagged (of 42). Circles: mid-episode monitors; shaded: their bar (≥ 5/8 at ≤ 1/20). Squares: judges at rest (one score per finished episode) at their in-sample operating point; the monitor bar does not apply to them.

## built PDF

### (front matter) (mean 0.092)

<!-- editlens chunk 0.092 lines 3-8 -->
What a reward model can show depends on who stopped the episode: failure judges and monitors on a low-cost arm Ravindu Somawansa Shisso Robotics, Paris ravindu.somawansa@gmail.com∗

### Abstract (mean 0.343)

<!-- editlens chunk 0.343 lines 10-23 -->
<!-- editlens paragraph 0.343 lines 10-23 -->
Reward models that score robot rollouts are also used as failure detectors, and the baseline they must beat depends on who stopped the episode. On 2,047 public SO101 rollouts from 7 policies, where runs end at a time limit, plain episode length separates failure from success at AUROC 0.942 within policy — and still 0.851 when only half of the longest run has been observed: failed runs are slow, not timed out. Both zero-shot reward models we test score below that baseline (the best reaches 0.821 within policy). On our own operator-stopped rollouts the regime flips: length falls to 0.56, neither reward model beats the policy-identity null, and what works is a judge at rest — a robot-trained 27B judge passes its pre-registered bar, though its operating threshold is insample, and every mid-episode monitor we tested misses the bar. We recommend reporting a length baseline, within policy, and the dataset’s stopping rule.

### 1 Introduction (mean 0.212)

<!-- editlens chunk 0.212 lines 25-50 -->
<!-- editlens paragraph 0.210 lines 25-42 -->
A reward model that scores robot rollouts is also a failure detector, and papers evaluate it as one. Any such evaluation has a hidden variable: the dataset’s stopping rule — who decides that an episode is over. When a benchmark stops failed runs at a time limit, how long an episode ran encodes its outcome, and a detector should be read against the baselines the stopping rule hands out for free: elapsed length, and the identity of the policy that ran. When an operator stops each run by judgment, those baselines collapse, and the task changes. None of the reward-model papers in our library reports how far plain episode length gets on the same data. We measure it on a public SO-101 benchmark [12] and on our own rollouts, with the length analyses frozen before the ∗ Code, result files and the checks that regenerate every number: github.com/ravediamond/paper-reward-models-stopping-rule. The frozen protocols are copied verbatim under repro/; the bar commits named in the paper belong to the authors’ research repository ravediamond/road-to-robotics.

<!-- editlens paragraph 0.242 lines 43-50 -->
numbers, and set every learned judge and monitor we ran against it. Contributions: (i) a pre-registered length analysis of 2,047 public rollouts, pooled, within policy and truncated in time; (ii) the same analysis for two zero-shot reward models [5, 1], with the stopping-rule baselines beside them; (iii) judge and monitor gates on 88 operator-stopped rollouts of our own, with every insample threshold disclosed.

### 2 Data and labels (mean 0.239)

<!-- editlens chunk 0.239 lines 52-58 -->
<!-- editlens paragraph 0.239 lines 52-58 -->
ArmnetBench v0.1 [12] (SO-101, 8 tasks, 7 policies): 2,047 policy rollouts with a success or failure class (515 successes, 1,532 failures); teleoperated episodes excluded. One task (pushing a Displayport cable, 270 rollouts) has rollouts of a single class and so no per-task AUROC. Our rollouts: 88 labelled bowls-task episodes on one SO-101 arm and a Jetson Orin NX, and the 50-episode subset (42 successes, 8 failures) every monitor gate used. Labels are the operator’s, not blind to policy.

### 3 The length baseline (mean 0.091)

<!-- editlens chunk 0.091 lines 60-152 -->
<!-- editlens paragraph 0.122 lines 60-73 -->
Table 1 carries the numbers. Pooled over policies, length gives 0.938 (CI 0.925–0.951); within each policy it ranges 0.91–0.96, pair-weighted 0.942 (CI 0.927–0.956): the baseline is not the policy identity (Fig. 1). Robometer4B [5], run zero-shot as its authors ship it, gives 0.818 pooled (CI 0.790–0.843) and 0.821 within policy (pairweighted over the per-policy scores, which span 0.79– 0.87; its per-episode scores were not stored, so these carry no episode-bootstrap CI). The protocol fixed Robometer’s primary score as its success probability; read descriptively from the same run, its last-progress head does better, 0.838 pooled, but stays below length. TOPReward [1] (Qwen3-VL-8B [11], no training; the primary score, fixed before any score, is the paper’s success score) gives 0.653 pooled (CI 0.623–0.684) and 0.661 within policy (CI 0.631–0.692), below length by -0.31 to -0.25 (paired 95 % CI); its full-video Yes/No component alone reaches 0.678 within policy, descriptively.

<!-- editlens paragraph 0.130 lines 113-118 -->
Table 1: ArmnetBench, failure AUROC with 95 % episode-bootstrap CIs. The Robometer within-policy entry is pair-weighted over its per-policy block and carries the per-policy range instead of a CI (per-episode scores not stored); the last-progress entry is descriptive (the protocol’s primary score was the success probability).

### 5 Judges and monitors on our rollouts (mean 0.051)

<!-- editlens chunk 0.042 lines 155-209 -->
Table 2 carries every judge and monitor with the same triple: threshold-free AUROC where defined, failures 0.938 episode length, pooled caught and successes flagged at the operating point. Ev0.942 episode length, within policy ery operating threshold of the judges at rest is chosen insample on the same 50 episodes; the AUROCs are not. 0.851 length seen up to 50 % of T, within policy At rest. A deterministic top-camera check (colour 0.818 Robometer-4B zero-shot, pooled masks and geometry, no learning) is right on 94.3 % 0.838 of judged episodes with 0 false positives (Wilson 0–13 Robometer-4B last progress, pooled (no CI) 64-frame two-view clip and NVIDIA’s prompt, Flora0.661 TOPReward (Qwen3-VL-8B), within policy Rewarder-27B [8] reaches a threshold-free AUROC of 1.00 (bootstrap CI 1.00–1.00); at its in-sample operating 0.6 0.8 1.0 point it flags 8 of 8 failures at 2 of 42 successes (Wilson failure AUROC, n = 2,047 on the false alarms 1–16 bar. Its base model Qwen3.527B [10] reaches 0.91 (0.78–1.00; 7/8 at 2/42) on the same Figure 1: Failure AUROC on ArmnetBench (95 % CIs input at its own in-sample threshold; Qwen3.5-9B [10] where available): episode length against two zero- reaches 0.75 (7/8 at 16/42) and Gemini 3.8 Flash [2] 0.96 shot reward models (Robometer-4B, TOPReward with (8/8 at 3/42, one false alarm over the bar): neither passes. Qwen3-VL-8B). The last-progress bar is descriptive and The input format, not the robot fine-tune, decided the recarries no CI. The Displayport-cable task contributes roll- sult. outs of one class only and has no per-task AUROC. Mid-episode. A Gemini sliding-window judge catches 0 of 8 failures at 1 of 42; the surprise of a separate world model, trained in the LeWorldModel recipe 4 Is it the timeout? [7], catches 2 of 8 at 2 of 42 (AUROC 0.86, Wilson 7– 59 (AUROC 0.30). An action-conditioned risk head on Only 8.7 % of failures run to the task’s longest episode. the world model’s latent reached 0.93 in a first version Observing length only up to half of that, when 88 % that read elapsed time, and that result is withdrawn; the of failures but 19 % of successes are still running, gives pre-registered second version, without time or length, 0.851 within policy (CI 0.829–0.873; Fig. 2; TOPReward catches 3 of 8 at 5 of 42 (AUROC 0.79 against 0.71 with on frames up to the same cut: 0.667): failed rollouts are shuffled actions; Wilson 14–69 bar of at least 5 of 8 failslow, not timed out. Both pre-registered readings hold: ures at no more than 1 of 20 false interventions (Fig. 3). length is a within-policy null, and it is more than the timeout. On our own operator-stopped rollouts the same baseline is at chance (0.56 on the 69; 0.52 on all 88).

<!-- editlens chunk 0.065 lines 155-350 -->
<!-- editlens paragraph 0.309 lines 297-298 -->
Table 2: Judges and monitors on 50 own operator-stopped rollouts (42 successes, 8 failures). Judges score the finished episode; monitors score mid-episode windows against the monitor bar (≥ 5/8 caught at ≤ 1/20 false interventions). ”In-sample” marks an operating threshold chosen on these same 50 episodes.

<!-- editlens paragraph 0.165 lines 341-350 -->
do); Robometer’s within-policy and truncation analyses carry no episode-bootstrap CI and no truncation column because its per-episode scores were not stored; TOPReward’s prefix count, frames per query and Yes/No wording are not given in its paper and are ours; the operating points of Flora-Rewarder-27B, Qwen3.5-27B and Gemini 3.8 Flash are chosen in-sample on the 50 episodes they are scored on (their AUROCs are not); 17 of the 25 failures in our 69 rollouts are TurboVLA’s, so on our set any score that reads the policy gets the identity null for free; the timeout is approximated by each task’s longest episode.

### 7 Limitations (mean 0.066)

<!-- editlens chunk 0.066 lines 372-528 -->
<!-- editlens paragraph 0.292 lines 372-375 -->
Two task families (ArmnetBench’s eight tasks, our bowls task); our labels are the operator’s and not blind; the risk head is trained and tested on the same 50 episodes (5fold by episode: episodes do not leak, tasks and policies

<!-- editlens paragraph 0.178 lines 378-398 -->
[1] Shirui Chen, Cole Harrison, Ying-Chun Lee, Angela Jin Yang, Zhongzheng Ren, Lillian J. Ratliff, et al. Topreward: Token probabilities as hidden zero-shot rewards for robotics. arXiv preprint arXiv:2602.19313, 2026. [2] Google DeepMind. Gemini 3.8 Flash. Google model page, 2026. URL https://aistudio.google.com/ docs/models. model id gemini-3.8-flash; the page gives no release date; accessed 2026-11-04. [3] Qiao Gu, Yuanliang Ju, Shengxiang Sun, Igor Gilitschenski, Haruki Nishimura, Masha Itkina, and Florian Shkurti. Safe: Multitask failure detection for vision-language-action models. arXiv preprint arXiv:2506.09937, 2025. [4] Long Li, Qichao Zhao, Yue Yang, et al. Spotter: Let the embodied model lead, and the vlm reflect for it. arXiv preprint arXiv:2609.36808, 2026. [5] Anthony Liang, Yigit Korkmaz, Jiahui Zhang, et al. Robometer: Scaling general-purpose robotic reward models via trajectory comparisons. arXiv preprint arXiv:2603.02115, 2026. [6] Jingyuan Liu, Yunpeng Qing, Changxu Wei, and Zhi Hou. Reap: From visual failure recognition to action-conditioned risk prediction for runtime

<!-- editlens paragraph 0.048 lines 524-528 -->
[18] Yi Yu and Xinchuan Qiu. Benchmarking visionlanguage-action models on so-101: Failure and recovery analysis. arXiv preprint arXiv:2606.08881, [12] Praveen Selvaraj, Lorenzo Uttini, and Ville Kuosma2026. nen. Armnetbench v0.1: Parallel real-world evaluation of manipulation policies on a low-cost arm farm. arXiv preprint arXiv:2607.24481, 2026.

### Appendix: from plain name to analysis (mean 0.099)

<!-- editlens chunk 0.099 lines 531-550 -->
<!-- editlens paragraph 0.099 lines 531-550 -->
[13] Chang Song, Bin Qian, Yan Feng, and Zhijie Song. Vla-corrector: Stage-aware observable state under- Every number is recomputable from the repository; this standing for prompt-based closed-loop recovery table maps each analysis to its files. of vision-language-action policies. arXiv preprint arXiv:2609.06508, 2026. [14] Yang Wan, Xihang Yue, Zhirui Liu, Ziyuan Chu, Shuxun Wang, Yuhan Chen, et al. No free checker: A survey of verifiers for robot policies. arXiv preprint arXiv:2609.09250, 2026. [15] Chen Wang, Xinze Niu, Zihao Zhu, Keru Zhou, Yicheng Xu, Shihao Jin, et al. Tracking task progress through errors and recovery: A benchmark and recurrent distributional model. arXiv preprint arXiv:2610.39125, 2026. [16] Hengyi Xie, Chenfei Yao, Xianjin Wu, Yingying Zhu, Dingkang Liang, Xiang Bai, et al. Turbovla: Real-time vision-language-action model at 32 hz on an rtx 4090 with <1 gb vram. arXiv preprint arXiv:2607.27205, 2026.
