# paper-reward-models-stopping-rule: chunks in paper order

## rendered source (numbers filled)

### Abstract (mean 0.202)

<!-- editlens chunk 0.202 lines 9-16 -->
<!-- editlens paragraph 0.202 lines 9-16 -->
Reward models that score robot rollouts are also used as failure detectors, and we compared two zero-shot reward models with plain episode length. On ArmnetBench, a public SO-101 benchmark where runs end at a time limit, length separates failure from success at AUROC 0.942 within policy. Failed runs there are slow rather than cut off, and length observed only up to half of the longest episode still gives 0.851. Both reward models score below length, the better one at 0.821. On our own rollouts, which an operator stopped by judgment, length falls to 0.56 and neither reward model beats the identity of the policy. A judge that sees the finished episode passes its threshold there, at an operating point chosen in-sample, and no mid-episode monitor reaches its bar. The baseline a detector has to beat depends on the dataset's stopping rule.

### 1 Introduction (mean 0.229)

<!-- editlens chunk 0.229 lines 20-32 -->
<!-- editlens paragraph 0.287 lines 20-24 -->
Papers that evaluate a reward model as a failure detector usually compare it with other learned detectors. When a benchmark stops failed runs at a time limit, the length of an episode also encodes its outcome, and so can the identity of the policy that ran (we call this the policy-identity null). When an operator stops each run by judgment, both signals are weaker. We call the way a dataset ends its episodes its *stopping rule*. None of the reward-model papers in our library reports the stopping rule or a length baseline.

<!-- editlens paragraph 0.280 lines 26-28 -->
We started with a narrower claim, that elapsed time is the reward model to beat, and our own rollouts did not support it: on them length is near chance, and a robot-trained judge passed its pre-registered threshold. The stopping rule separates the two results, so it became the subject of the paper.

<!-- editlens paragraph 0.223 lines 30-32 -->
We measured length on ArmnetBench and on our own rollouts, with the length analyses frozen before any number existed. We compared it with two zero-shot reward models, Robometer and TOPReward, and on our 88 operator-stopped rollouts also with every judge and monitor we had run.

### 2 Data and labels (mean 0.216)

<!-- editlens chunk 0.216 lines 36-41 -->
<!-- editlens paragraph 0.216 lines 36-41 -->
ArmnetBench v0.1 has 8 tasks and 7 policies on the SO-101. We use its 2,047 policy rollouts with a success or failure class (515 successes, 1,532 failures) and leave out the teleoperated episodes. One task, pushing a Displayport cable (270 rollouts), has rollouts of a single class and so no per-task AUROC. Our own data are 88 labelled bowls-task episodes on one SO-101 arm with a Jetson Orin NX, and every monitor gate used the same 50-episode subset (42 successes, 8 failures). The author was the operator, who stopped each run and labelled it at rest, not blind to the policy.

### 3 The length baseline (mean 0.160)

<!-- editlens chunk 0.160 lines 45-55 -->
<!-- editlens paragraph 0.198 lines 45-47 -->
On ArmnetBench, episode length is a strong failure detector within each policy (Table 1, Fig. 1). Pooled over policies it reaches 0.938, and within each policy it ranges from 0.91 to 0.96. Pair-weighted, the within-policy value is 0.942, with a CI of 0.927–0.956.

<!-- editlens paragraph 0.193 lines 49-55 -->
We ran Robometer-4B zero-shot, as its authors ship it, and it scores 0.818 pooled and 0.821 within policy. The within-policy value is pair-weighted over its per-policy scores, whose range stands in for a CI (§7). TOPReward, run with Qwen3-VL-8B and no training, scores 0.661 within policy, and its paired difference to length has a 95 % CI of -0.31 to -0.25. The protocols fixed each model's primary score before any score existed: the success probability for Robometer and the success score of its paper for TOPReward. Two other scores from the same runs, listed in Table 1 as descriptive rows, are higher and still below length.

### 4 Length is more than the timeout (mean 0.170)

<!-- editlens chunk 0.170 lines 72-84 -->
<!-- editlens paragraph 0.303 lines 72-75 -->
We take each task's longest episode as its timeout, and only 8.7 % of failures run that long. At half that length 88 % of failures are still running, against 19 % of successes. Length observed up to that cut gives 0.851 within policy (CI 0.829–0.873; Fig. 2), and TOPReward on frames up to the same cut reaches 0.667. Failed rollouts are slow, not timed out, and both readings fixed in the protocol hold.

<!-- editlens paragraph 0.065 lines 79-84 -->
On our own operator-stopped rollouts length is at chance, with 0.56 on the 69 rollouts TOPReward scored and 0.52 on all 88. The baseline to beat here is the policy-identity null, because 17 of the 25 failures in the 69 come from one policy, TurboVLA. Neither reward model beats it. TOPReward scores 0.82 (CI 0.70–0.93) where policy identity alone gives 0.87, and 0.78 on the 50 episodes without TurboVLA. Robometer scores 0.577 on all 88, and policy identity 0.878.

### 5 Judges and monitors on our rollouts (mean 0.174)

<!-- editlens chunk 0.174 lines 88-107 -->
<!-- editlens paragraph 0.229 lines 91-99 -->
We first ran a deterministic top-camera check (colour masks and geometry, no learning). It is right on 94.3 % of judged episodes, with 0 false positives (Wilson 0–13 %) and 5 false negatives. We then gave Flora-Rewarder-27B a 64-frame two-view clip and NVIDIA's prompt, and it reaches a threshold-free AUROC of 1.00 (bootstrap CI 1.00–1.00). At its in-sample operating point it flags 8 of 8 failures at 2 of 42 successes (Wilson on the false alarms 1–16 %), which passes the pre-registered bar of at least 6 of 8 failures at no more than 2 of 42 successes. Its base model, Qwen3.5-27B, has no robot fine-tune and passes on the same input too, with AUROC 0.91 (0.78–1.00) and 7 of 8 at 2 of 42. The input format mattered more than the fine-tune. Qwen3.5-9B flags 16 successes and fails, and Gemini 3.8 Flash fails by one false alarm.

<!-- editlens paragraph 0.287 lines 101-107 -->
No mid-episode monitor reaches its bar of at least 5 of 8 failures at no more than 1 of 20 false interventions on these 50 rollouts (Fig. 3). The surprise of a separate world model, trained in the LeWorldModel recipe, catches 2 of 8 at 2 of 42 (AUROC 0.86), and a Gemini sliding-window judge catches 0. We also built an action-conditioned risk head on the world model's latent. Its first version reached AUROC 0.93, but it read elapsed time, so we withdrew that result and pre-registered a second version without time or length. That version catches 3 of 8 at 5 of 42, with AUROC 0.79 against 0.71 for shuffled actions. The MLP variant catches 6 of 8 and flags 13 of 42.

### 6 Related work (mean 0.246)

<!-- editlens chunk 0.246 lines 128-136 -->
<!-- editlens paragraph 0.246 lines 128-136 -->
Robometer scales a general-purpose reward model through trajectory comparisons, and TOPReward reads the token probabilities of a video-language model as hidden rewards. A survey of verifiers for robot policies covers the wider family. FAIL-Detect and SAFE learn uncertainty- and feature-based failure scores for imitation and VLA policies. FARM reads failure signals from the internal states of a frozen world model, as our world-model monitors do, and our risk head follows ReAP, which predicts action-conditioned risk. VLA-Corrector verifies stages, Spotter adds a reflecting VLM, and REMORA tracks progress through errors and recovery. ArmnetBench and a standardized SO-101 VLA benchmark evaluate policies on the same arm. None of these works reports the elapsed-length baseline under the dataset's stopping rule.

### 7 Limitations (mean 0.151)

<!-- editlens chunk 0.151 lines 140-149 -->
<!-- editlens paragraph 0.151 lines 140-149 -->
The judge pass on our own rollouts rests on 8 failures and on operating thresholds chosen on the same 50 episodes, which a single operator, the author, labelled without being blind to the policy. The threshold-free AUROCs do not depend on the threshold, and fresh rollouts scored at the frozen thresholds would confirm the operating points. 17 of the 25 failures in our 69 rollouts are TurboVLA's, so any score that reads the policy gets the policy-identity null for free. The risk head is trained and tested on the same 50 episodes, with five folds by episode that keep episodes from leaking (tasks and policies do leak). Robometer's per-episode scores stayed on an older machine. Its within-policy number therefore has no episode-bootstrap CI and it is missing from the truncation analysis, and a copy from that machine or a re-score of about $6 would restore both. TOPReward's paper does not give its prefix count, frames per query or Yes/No wording, so those are our choices. The ArmnetBench result covers eight tasks, and the timeout is approximated by each task's longest episode.

### 8 Conclusion (mean 0.193)

<!-- editlens chunk 0.193 lines 153-156 -->
<!-- editlens paragraph 0.193 lines 153-156 -->
On ArmnetBench, where runs end at a time limit, episode length beat both reward models. On our operator-stopped rollouts length was at chance, and a judge that saw the whole finished episode caught the failures. When you evaluate a reward model as a failure detector, report episode length within policy on the same rows and say how the episodes ended.

### Appendix: from plain name to analysis (mean 0.240)

<!-- editlens chunk 0.240 lines 160-160 -->
Every number is recomputable from the repository; this table maps each analysis to its files.

### (figure and table captions) (mean 0.084)

<!-- editlens chunk 0.084 lines 57-124 -->
Table 1: ArmnetBench, failure AUROC with 95 % episode-bootstrap CIs. Read down the within-policy column: no reward-model score reaches length.
Failure AUROC on ArmnetBench: episode length against two zero-shot reward models. Length leads both, pooled and within policy (95 % CIs where available).
Length observed up to a fraction of the task's longest episode, AUROC within policy: most of the signal is there by half the episode (band: 95 % CI).
Table 2: Judges and monitors on the 50 operator-stopped rollouts (42 successes, 8 failures). Judges see the finished episode; monitors are held to ≥ 5/8 caught at ≤ 1/20 false interventions.
Failures caught against successes flagged on the 50 rollouts. No monitor (circles) reaches its shaded bar; the judges at rest (squares) sit at their in-sample operating point, where the monitor bar does not apply.

## built PDF

### (front matter) (mean 0.055)

<!-- editlens chunk 0.055 lines 3-44 -->
<!-- editlens paragraph 0.041 lines 3-25 -->
What a reward model can show depends on who stopped the episode: failure judges and monitors on a low-cost arm Ravindu Somawansa Shisso Robotics, Paris ravindu.somawansa@shissorobotics.com∗ We measured length on ArmnetBench [12] and on our own rollouts, with the length analyses frozen before any number existed. We compared it with two zeroAbstract shot reward models, Robometer [5] and TOPReward [1], Reward models that score robot rollouts are also used as and on our 88 operator-stopped rollouts also with every failure detectors, and we compared two zero-shot reward judge and monitor we had run. models with plain episode length. On ArmnetBench, a public SO-101 benchmark where runs end at a time limit, length separates failure from success at AUROC 0.942 2 Data and labels within policy. Failed runs there are slow rather than cut off, and length observed only up to half of the longest ArmnetBench v0.1 [12] has 8 tasks and 7 policies on the episode still gives 0.851. Both reward models score be- SO-101. We use its 2,047 policy rollouts with a success low length, the better one at 0.821. On our own rollouts, or failure class (515 successes, 1,532 failures) and leave which an operator stopped by judgment, length falls to out the teleoperated episodes. One task, pushing a Dis0.56 and neither reward model beats the identity of the playport cable (270 rollouts), has rollouts of a single class policy. A judge that sees the finished episode passes its and so no per-task AUROC. Our own data are 88 lathreshold there, at an operating point chosen in-sample, belled bowls-task episodes on one SO-101 arm with a Jetand no mid-episode monitor reaches its bar. The baseline son Orin NX, and every monitor gate used the same 50a detector has to beat depends on the dataset’s stopping episode subset (42 successes, 8 failures). The author was the operator, who stopped each run and labelled it at rest, rule. not blind to the policy.

<!-- editlens paragraph 0.187 lines 30-44 -->
Papers that evaluate a reward model as a failure detector usually compare it with other learned detectors. When a benchmark stops failed runs at a time limit, the length of an episode also encodes its outcome, and so can the identity of the policy that ran (we call this the policy-identity null). When an operator stops each run by judgment, both signals are weaker. We call the way a dataset ends its episodes its stopping rule. None of the reward-model papers in our library reports the stopping rule or a length baseline. We started with a narrower claim, that elapsed time is the reward model to beat, and our own rollouts did not support it: on them length is near chance, and a robottrained judge passed its pre-registered threshold. The stopping rule separates the two results, so it became the subject of the paper.

<!-- editlens chunk 0.054 lines 49-176 -->
<!-- editlens paragraph 0.137 lines 49-67 -->
On ArmnetBench, episode length is a strong failure detector within each policy (Table 1, Fig. 1). Pooled over policies it reaches 0.938, and within each policy it ranges from 0.91 to 0.96. Pair-weighted, the within-policy value is 0.942, with a CI of 0.927–0.956. We ran Robometer-4B [5] zero-shot, as its authors ship it, and it scores 0.818 pooled and 0.821 within policy. The within-policy value is pair-weighted over its per-policy scores, whose range stands in for a CI (§7). TOPReward [1], run with Qwen3-VL-8B [11] and no training, scores 0.661 within policy, and its paired difference to length has a 95 % CI of -0.31 to -0.25. The protocols fixed each model’s primary score before any score existed: the success probability for Robometer and the success score of its paper for TOPReward. Two other scores ∗ Code, result files and the checks that regenerate every number: from the same runs, listed in Table 1 as descriptive rows, github.com/ravediamond/paper-reward-models-stopping-rule. are higher and still below length. The frozen protocols are copied verbatim under repro/; the bar commits named in the paper belong to the authors’ research repository ravediamond/road-to-robotics.

<!-- editlens paragraph 0.067 lines 148-176 -->
the judges at rest is chosen in-sample. We first ran a deterministic top-camera check (colour length seen up to 50 % of T, within policy masks and geometry, no learning). It is right on 94.3 % 0.818 Robometer-4B zero-shot, pooled of judged episodes, with 0 false positives (Wilson 0–13 gave Flora-Rewarder-27B [8] a 64-frame two-view clip 0.838 Robometer-4B last progress, pooled (no CI) and NVIDIA’s prompt, and it reaches a threshold-free 0.661 TOPReward (Qwen3-VL-8B), within policy AUROC of 1.00 (bootstrap CI 1.00–1.00). At its in-sample operating point it flags 8 of 8 failures at 2 of 42 successes 0.6 0.8 1.0 (Wilson on the false alarms 1–16 pre-registered bar of at failure AUROC, n = 2,047 least 6 of 8 failures at no more than 2 of 42 successes. Its base model, Qwen3.5-27B [10], has no robot fine-tune Figure 1: Failure AUROC on ArmnetBench: episode and passes on the same input too, with AUROC 0.91 length against two zero-shot reward models. Length (0.78–1.00) and 7 of 8 at 2 of 42. The input format matleads both, pooled and within policy (95 % CIs where tered more than the fine-tune. Qwen3.5-9B [10] flags 16 available). successes and fails, and Gemini 3.8 Flash [2] fails by one false alarm. No mid-episode monitor reaches its bar of at least 5

### 4 Length is more than the timeout (mean 0.107)

<!-- editlens chunk 0.107 lines 177-195 -->
<!-- editlens paragraph 0.107 lines 177-195 -->
of 8 failures at no more than 1 of 20 false interventions on these 50 rollouts (Fig. 3). The surprise of a sepaWe take each task’s longest episode as its timeout, and rate world model, trained in the LeWorldModel recipe only 8.7 % of failures run that long. At half that length 88 [7], catches 2 of 8 at 2 of 42 (AUROC 0.86), and a Gemini % of failures are still running, against 19 % of successes. sliding-window judge catches 0. We also built an actionLength observed up to that cut gives 0.851 within policy conditioned risk head on the world model’s latent. Its (CI 0.829–0.873; Fig. 2), and TOPReward on frames up to first version reached AUROC 0.93, but it read elapsed the same cut reaches 0.667. Failed rollouts are slow, not time, so we withdrew that result and pre-registered a sectimed out, and both readings fixed in the protocol hold. ond version without time or length. That version catches On our own operator-stopped rollouts length is at 3 of 8 at 5 of 42, with AUROC 0.79 against 0.71 for shufchance, with 0.56 on the 69 rollouts TOPReward scored fled actions. The MLP variant catches 6 of 8 and flags 13 and 0.52 on all 88. The baseline to beat here is the of 42. policy-identity null, because 17 of the 25 failures in the 69 come from one policy, TurboVLA [16]. Neither reward model beats it. TOPReward scores 0.82 (CI 0.70–0.93) 6 Related work where policy identity alone gives 0.87, and 0.78 on the 50 episodes without TurboVLA. Robometer scores 0.577 Robometer [5] scales a general-purpose reward model through trajectory comparisons, and TOPReward [1] on all 88, and policy identity 0.878. reads the token probabilities of a video-language model as hidden rewards. A survey of verifiers for robot policies [14] covers the wider family. FAIL-Detect [17] and SAFE

### 5 Judges and monitors on our rollouts (mean 0.049)

<!-- editlens chunk 0.049 lines 196-354 -->
<!-- editlens paragraph 0.081 lines 196-200 -->
[3] learn uncertainty- and feature-based failure scores for Table 2 gives each judge and monitor a threshold-free imitation and VLA policies. FARM [9] reads failure sigAUROC where one is defined, and the failures caught nals from the internal states of a frozen world model, as and successes flagged at its operating point, which for our world-model monitors do, and our risk head follows 0.942

<!-- editlens paragraph 0.125 lines 299-301 -->
no episode-bootstrap CI and it is missing from the truncation analysis, and a copy from that machine or a rescore of about $6 would restore both. TOPReward’s paper does not give its prefix count, frames per query or Yes/No wording, so those are our choices. The ArmnetBench result covers eight tasks, and the timeout is approximated by each task’s longest episode.

<!-- editlens paragraph 0.062 lines 344-351 -->
On ArmnetBench, where runs end at a time limit, episode length beat both reward models. On our operator-stopped rollouts length was at chance, and a Figure 3: Failures caught against successes flagged on the judge that saw the whole finished episode caught the fail50 rollouts. No monitor (circles) reaches its shaded bar; ures. When you evaluate a reward model as a failure dethe judges at rest (squares) sit at their in-sample operat- tector, report episode length within policy on the same ing point, where the monitor bar does not apply. rows and say how the episodes ended. successes flagged (of 42)

<!-- editlens paragraph 0.348 lines 352-354 -->
ReAP [6], which predicts action-conditioned risk. VLACorrector [13] verifies stages, Spotter [4] adds a reflecting VLM, and REMORA [15] tracks progress through errors and recovery. ArmnetBench [12] and a standardized SO-101 VLA benchmark [18] evaluate policies on the same arm. None of these works reports the elapsedlength baseline under the dataset’s stopping rule.
