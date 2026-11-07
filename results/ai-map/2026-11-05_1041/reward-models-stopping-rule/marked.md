# paper-reward-models-stopping-rule: chunks in paper order

## rendered source (numbers filled)

### Abstract (mean 0.379)

<!-- editlens chunk 0.379 lines 9-16 -->
<!-- editlens paragraph 0.379 lines 9-16 -->
Episode length is a failure detector that zero-shot reward models must beat, and how hard it is to beat depends on who stopped the episode. On public SO-101 rollouts that end at a time limit, length alone separates failure from success at AUROC 0.942 within policy. It does not need the timeout: watched only up to half of the longest episode, it still gives 0.851, because failed runs are slow rather than cut off. Both reward models we test score below it, the better one at 0.821. On our own rollouts, which an operator stopped by judgment, length falls to 0.56 and the picture reverses. Neither reward model beats the identity of the policy, a judge that sees the finished episode passes its bar (at a threshold chosen in-sample), and every mid-episode monitor misses. So report a within-policy length baseline, and name the dataset's stopping rule.

### 1 Introduction (mean 0.280)

<!-- editlens chunk 0.280 lines 20-33 -->
<!-- editlens paragraph 0.329 lines 20-25 -->
A reward model that scores robot rollouts is also a failure detector, and papers evaluate it as one, mostly against other learned detectors. The baseline that matters is often simpler. When a benchmark stops failed runs at a time limit, the length of an episode encodes its outcome, and so does the identity of the policy that ran (we call the second one the policy-identity null). When an operator stops each run by judgment, both signals collapse and the detection task changes with them. Which of the two a dataset uses is its *stopping rule*, and none of the reward-model papers in our library reports it or the length baseline it implies.

<!-- editlens paragraph 0.408 lines 27-29 -->
We started with a narrower claim, that elapsed time is the reward model to beat. Our own rollouts broke it: there, length is near chance and a robot-trained judge passed its bar. The stopping rule is what separates the two results, so it became the subject of the paper.

<!-- editlens paragraph 0.197 lines 31-33 -->
We measured length on a public SO-101 benchmark and on our own rollouts, with the length analyses frozen before any number existed, and set against it two zero-shot reward models and every judge and monitor we had run on our 88 operator-stopped rollouts.

### 2 Data and labels (mean 0.198)

<!-- editlens chunk 0.198 lines 37-42 -->
<!-- editlens paragraph 0.198 lines 37-42 -->
ArmnetBench v0.1 covers the SO-101 with 8 tasks and 7 policies. We use its 2,047 policy rollouts with a success or failure class (515 successes, 1,532 failures) and leave out the teleoperated episodes. One task, pushing a Displayport cable (270 rollouts), has rollouts of a single class and so no per-task AUROC. Our own data are 88 labelled bowls-task episodes on one SO-101 arm with a Jetson Orin NX, and the 50-episode subset (42 successes, 8 failures) that every monitor gate used. The author was the operator: he stopped each run and labelled it at rest, not blind to the policy.

### 3 The length baseline (mean 0.193)

<!-- editlens chunk 0.193 lines 46-56 -->
<!-- editlens paragraph 0.186 lines 46-48 -->
On ArmnetBench, episode length is a strong failure detector, and not only because it tells the policies apart (Table 1, Fig. 1). Pooled over policies it reaches 0.938. Within each policy it ranges from 0.91 to 0.96, or 0.942 pair-weighted, with a CI of 0.927–0.956.

<!-- editlens paragraph 0.215 lines 50-56 -->
Both reward models fall below it. Robometer-4B, run zero-shot as its authors ship it, scores 0.818 pooled and 0.821 within policy (pair-weighted over its per-policy scores, whose range stands in for a CI; §7 says why). TOPReward, with Qwen3-VL-8B and no training, scores 0.661 within policy, and its paired difference to length has a 95 % CI of -0.31 to -0.25. The protocols fixed each model's primary score before any score existed (Robometer's success probability, and the success score of TOPReward's paper). The two descriptive rows of Table 1, read from the same runs, score higher but still below length.

### 4 Is it the timeout? (mean 0.169)

<!-- editlens chunk 0.169 lines 73-87 -->
<!-- editlens paragraph 0.306 lines 73-78 -->
If length only reflected the timeout, its signal would sit in the few runs that hit it. We take each task's longest episode as its timeout, and only 8.7 % of failures run that long. At half that length, 88 % of failures are still running but only 19 % of successes. Length observed up to that cut gives 0.851 within policy (CI 0.829–0.873; Fig. 2), and TOPReward on frames up to the same cut reaches 0.667. Failed rollouts are slow, not timed out. Both readings the protocol fixed in advance hold: length is a real within-policy null, and it is more than the timeout.

<!-- editlens paragraph 0.057 lines 82-87 -->
On our own operator-stopped rollouts the same baseline is at chance: 0.56 on the 69 rollouts TOPReward scored and 0.52 on all 88. The baseline that matters here is the policy-identity null, because 17 of the 25 failures in the 69 come from one policy, TurboVLA. Neither reward model beats it. TOPReward scores 0.82 (CI 0.70–0.93) against 0.87 for policy identity alone, and 0.78 on the 50 episodes without TurboVLA. Robometer scores 0.577 against 0.878 on all 88.

### 5 Judges and monitors on our rollouts (mean 0.193)

<!-- editlens chunk 0.193 lines 91-112 -->
<!-- editlens paragraph 0.112 lines 91-93 -->
Table 2 reports every judge and monitor the same way: a threshold-free AUROC where one is defined, then failures caught and successes flagged at the operating point. The judges at rest have their operating thresholds chosen in-sample on the same 50 episodes (their AUROCs are not).

<!-- editlens paragraph 0.289 lines 95-104 -->
A judge that sees the finished episode works on these rollouts, and the input format matters more than the robot fine-tune. A deterministic top-camera check (colour masks and geometry, no learning) is right on 94.3 % of judged episodes, with 0 false positives (Wilson 0–13 %) and 5 false negatives. Given a 64-frame two-view clip and NVIDIA's prompt, Flora-Rewarder-27B reaches a threshold-free AUROC of 1.00 (bootstrap CI 1.00–1.00). At its in-sample operating point it flags 8 of 8 failures at 2 of 42 successes (Wilson on the false alarms 1–16 %), which passes the pre-registered bar of at least 6 of 8 failures at no more than 2 of 42 successes. Its base model Qwen3.5-27B, without the robot fine-tune, passes the same bar on the same input: AUROC 0.91 (0.78–1.00), 7 of 8 at 2 of 42. The smaller Qwen3.5-9B and Gemini 3.8 Flash fail it, the 9B by flagging 16 successes and Gemini by one false alarm too many.

<!-- editlens paragraph 0.262 lines 106-112 -->
No mid-episode monitor meets its bar of at least 5 of 8 failures at no more than 1 of 20 false interventions (Fig. 3). The surprise of a separate world model, trained in the LeWorldModel recipe, comes closest with 2 of 8 at 2 of 42 (AUROC 0.86). A Gemini sliding-window judge catches 0. The action-conditioned risk head on the world model's latent has a history. Its first version reached AUROC 0.93, but it read elapsed time, so we withdrew that result and pre-registered a second version without time or length. The second version catches 3 of 8 at 5 of 42, with AUROC 0.79 against 0.71 when its actions are shuffled, and its MLP variant catches 6 of 8 but flags 13 of 42.

### 6 Related work (mean 0.260)

<!-- editlens chunk 0.260 lines 133-144 -->
<!-- editlens paragraph 0.260 lines 133-144 -->
Robometer and TOPReward are the two reward models we test. Robometer scales a general-purpose reward model through trajectory comparisons, and TOPReward reads the token probabilities of a video-language model as hidden rewards. A survey of verifiers for robot policies maps the wider family. Mid-episode failure detection is its own line of work, and our monitors borrow from it. FAIL-Detect and SAFE learn uncertainty- and feature-based failure scores for imitation and VLA policies. FARM reads failure signals from the internal states of a frozen world model, close to our world-model monitors, and ReAP predicts action-conditioned risk, the idea behind our risk head. VLA-Corrector, Spotter and REMORA add stage verification, a reflecting VLM and recurrent progress tracking. ArmnetBench and a standardized SO-101 VLA benchmark evaluate policies on the same low-cost arm. None of these works reports the elapsed-length baseline under the dataset's stopping rule, and that comparison is what this paper adds.

### 7 Limitations (mean 0.256)

<!-- editlens chunk 0.256 lines 148-157 -->
<!-- editlens paragraph 0.256 lines 148-157 -->
The result most likely to move is the judge pass on our own rollouts. It rests on 8 failures, labels the author gave without being blind to the policy, and operating thresholds chosen on the same 50 episodes; fresh rollouts scored at those frozen thresholds would test it. Policy identity is the next concern: 17 of the 25 failures in our 69 rollouts are TurboVLA's, so any score that reads the policy gets the policy-identity null for free. The risk head is trained and tested on the same 50 episodes (five folds by episode keep episodes from leaking, but tasks and policies do leak). Robometer's within-policy number has no episode-bootstrap CI and Robometer is missing from the truncation analysis, because its per-episode scores stayed on an older machine; a copy from that machine or a re-score of about $6 would restore both. TOPReward's paper does not give its prefix count, frames per query or Yes/No wording, so those are our choices. The ArmnetBench result covers eight tasks, and the timeout is approximated by each task's longest episode.

### 8 Conclusion (mean 0.303)

<!-- editlens chunk 0.303 lines 161-164 -->
<!-- editlens paragraph 0.303 lines 161-164 -->
Before evaluating a reward model as a failure detector, run episode length within policy on the same rows, and say how the episodes ended. On a benchmark that stops at a time limit, length was the detector to beat, and neither reward model beat it. On rollouts an operator stopped, length was useless, and what caught failures was a judge that saw the whole finished episode in the right input format.

### Appendix: from plain name to analysis (mean 0.240)

<!-- editlens chunk 0.240 lines 168-168 -->
Every number is recomputable from the repository; this table maps each analysis to its files.

### (figure and table captions) (mean 0.084)

<!-- editlens chunk 0.084 lines 58-129 -->
Table 1: ArmnetBench, failure AUROC with 95 % episode-bootstrap CIs. Read down the within-policy column: no reward-model score reaches length.
Failure AUROC on ArmnetBench: episode length against two zero-shot reward models. Length leads both, pooled and within policy (95 % CIs where available).
Length observed up to a fraction of the task's longest episode, AUROC within policy: most of the signal is there by half the episode (band: 95 % CI).
Table 2: Judges and monitors on the 50 operator-stopped rollouts (42 successes, 8 failures). Judges see the finished episode; monitors are held to ≥ 5/8 caught at ≤ 1/20 false interventions.
Failures caught against successes flagged on the 50 rollouts. No monitor (circles) reaches its shaded bar; the judges at rest (squares) sit at their in-sample operating point, where the monitor bar does not apply.

## built PDF

### (front matter) (mean 0.064)

<!-- editlens chunk 0.064 lines 3-11 -->
<!-- editlens paragraph 0.064 lines 3-11 -->
What a reward model can show depends on who stopped the episode: failure judges and monitors on a low-cost arm Ravindu Somawansa Shisso Robotics, Paris ravindu.somawansa@gmail.com∗ passed its bar. The stopping rule is what separates the two results, so it became the subject of the paper. We measured length on a public SO-101 benchmark

### Abstract (mean 0.076)

<!-- editlens chunk 0.074 lines 12-65 -->
<!-- editlens paragraph 0.095 lines 12-29 -->
[12] and on our own rollouts, with the length analyses frozen before any number existed, and set against it Episode length is a failure detector that zero-shot reward two zero-shot reward models [5, 1] and every judge and models must beat, and how hard it is to beat depends monitor we had run on our 88 operator-stopped rollouts. on who stopped the episode. On public SO-101 rollouts that end at a time limit, length alone separates failure from success at AUROC 0.942 within policy. It does 2 Data and labels not need the timeout: watched only up to half of the longest episode, it still gives 0.851, because failed runs ArmnetBench v0.1 [12] covers the SO-101 with 8 tasks are slow rather than cut off. Both reward models we and 7 policies. We use its 2,047 policy rollouts with a test score below it, the better one at 0.821. On our own success or failure class (515 successes, 1,532 failures) and rollouts, which an operator stopped by judgment, length leave out the teleoperated episodes. One task, pushing a falls to 0.56 and the picture reverses. Neither reward Displayport cable (270 rollouts), has rollouts of a single model beats the identity of the policy, a judge that sees class and so no per-task AUROC. Our own data are 88 the finished episode passes its bar (at a threshold cho- labelled bowls-task episodes on one SO-101 arm with a sen in-sample), and every mid-episode monitor misses. Jetson Orin NX, and the 50-episode subset (42 successes, So report a within-policy length baseline, and name the 8 failures) that every monitor gate used. The author was dataset’s stopping rule. the operator: he stopped each run and labelled it at rest, not blind to the policy.

<!-- editlens paragraph 0.392 lines 37-48 -->
A reward model that scores robot rollouts is also a failure detector, and papers evaluate it as one, mostly against other learned detectors. The baseline that matters is often simpler. When a benchmark stops failed runs at a time limit, the length of an episode encodes its outcome, and so does the identity of the policy that ran (we call the second one the policy-identity null). When an operator stops each run by judgment, both signals collapse and the detection task changes with them. Which of the two a dataset uses is its stopping rule, and none of the rewardmodel papers in our library reports it or the length baseline it implies. We started with a narrower claim, that elapsed time is the reward model to beat. Our own rollouts broke it: there, length is near chance and a robot-trained judge

<!-- editlens paragraph 0.156 lines 49-65 -->
On ArmnetBench, episode length is a strong failure detector, and not only because it tells the policies apart (Table 1, Fig. 1). Pooled over policies it reaches 0.938. Within each policy it ranges from 0.91 to 0.96, or 0.942 pair-weighted, with a CI of 0.927–0.956. Both reward models fall below it. Robometer-4B [5], run zero-shot as its authors ship it, scores 0.818 pooled and 0.821 within policy (pair-weighted over its perpolicy scores, whose range stands in for a CI; §7 says why). TOPReward [1], with Qwen3-VL-8B [11] and no training, scores 0.661 within policy, and its paired difference to length has a 95 % CI of -0.31 to -0.25. The protocols fixed each model’s primary score before any score existed (Robometer’s success probability, and the success score of TOPReward’s paper). The two descriptive rows ∗ Code, result files and the checks that regenerate every number: of Table 1, read from the same runs, score higher but still github.com/ravediamond/paper-reward-models-stopping-rule. The frozen protocols are copied verbatim under repro/; the bar below length. commits named in the paper belong to the authors’ research repository ravediamond/road-to-robotics.

<!-- editlens chunk 0.050 lines 136-196 -->
<!-- editlens paragraph 0.140 lines 177-193 -->
If length only reflected the timeout, its signal would sit in the few runs that hit it. We take each task’s longest episode as its timeout, and only 8.7 % of failures run that long. At half that length, 88 % of failures are still running but only 19 % of successes. Length observed up to that cut gives 0.851 within policy (CI 0.829–0.873; Fig. 2), and TOPReward on frames up to the same cut reaches 0.667. Failed rollouts are slow, not timed out. Both readings the protocol fixed in advance hold: length is a real withinpolicy null, and it is more than the timeout. On our own operator-stopped rollouts the same baseline is at chance: 0.56 on the 69 rollouts TOPReward scored and 0.52 on all 88. The baseline that matters here is the policy-identity null, because 17 of the 25 failures in the 69 come from one policy, TurboVLA [16]. Neither reward model beats it. TOPReward scores 0.82 (CI 0.70–0.93) against 0.87 for policy identity alone, and 0.78 on the 50 episodes without TurboVLA. Robometer scores 0.577 against 0.878 on all 88.

<!-- editlens chunk 0.064 lines 201-236 -->
<!-- editlens paragraph 0.170 lines 201-230 -->
Table 2 reports every judge and monitor the same way: a threshold-free AUROC where one is defined, then failures caught and successes flagged at the operating point. The judges at rest have their operating thresholds chosen in-sample on the same 50 episodes (their AUROCs are not). A judge that sees the finished episode works on these rollouts, and the input format matters more than the robot fine-tune. A deterministic top-camera check (colour masks and geometry, no learning) is right on 94.3 % of judged episodes, with 0 false positives (Wilson 0–13 64-frame two-view clip and NVIDIA’s prompt, Flora-Rewarder-27B [8] reaches a threshold-free AUROC of 1.00 (bootstrap CI 1.00–1.00). At its in-sample operating point it flags 8 of 8 failures at 2 of 42 successes (Wilson on the false alarms 1–16 bar of at least 6 of 8 failures at no more than 2 of 42 successes. Its base model Qwen3.5-27B [10], without the robot fine-tune, passes the same bar on the same input: AUROC 0.91 (0.78–1.00), 7 of 8 at 2 of 42. The smaller Qwen3.5-9B [10] and Gemini 3.8 Flash [2] fail it, the 9B by flagging 16 successes and Gemini by one false alarm too many. No mid-episode monitor meets its bar of at least 5 of 8 failures at no more than 1 of 20 false interventions (Fig. 3). The surprise of a separate world model, trained in the LeWorldModel recipe [7], comes closest with 2 of 8 at 2 of 42 (AUROC 0.86). A Gemini sliding-window judge catches 0. The action-conditioned risk head on the world model’s latent has a history. Its first version reached AUROC 0.93, but it read elapsed time, so we withdrew that result and pre-registered a second version without time or length. The second version catches 3 of 8 at 5 of 42, with AUROC 0.79 against 0.71 when its actions are shuffled, and its MLP variant catches 6 of 8 but flags 13 of 42.

<!-- editlens chunk 0.105 lines 322-392 -->
<!-- editlens paragraph 0.061 lines 322-359 -->
Table 2: Judges and monitors on the 50 operator-stopped rollouts (42 successes, 8 failures). Judges see the finished episode; monitors are held to ≥ 5/8 caught at ≤ 1/20 false interventions. gave without being blind to the policy, and operating thresholds chosen on the same 50 episodes; fresh rollouts Qwen3.5-27B scored at those frozen thresholds would test it. Policy risk MLP v2 6 identity is the next concern: 17 of the 25 failures in our 69 rollouts are TurboVLA’s, so any score that reads the pol4 icy gets the policy-identity null for free. The risk head is risk head v2 trained and tested on the same 50 episodes (five folds by WM surprise 2 episode keep episodes from leaking, but tasks and poliGemini windows cies do leak). Robometer’s within-policy number has no 0 episode-bootstrap CI and Robometer is missing from the WM drift 0 2 4 6 8 10 12 14 16 truncation analysis, because its per-episode scores stayed successes flagged (of 42) on an older machine; a copy from that machine or a rescore of about $6 would restore both. TOPReward’s paper does not give its prefix count, frames per query or Figure 3: Failures caught against successes flagged on the Yes/No wording, so those are our choices. The Armnet50 rollouts. No monitor (circles) reaches its shaded bar; Bench result covers eight tasks, and the timeout is apthe judges at rest (squares) sit at their in-sample operatproximated by each task’s longest episode. ing point, where the monitor bar does not apply. monitor bar

<!-- editlens paragraph 0.141 lines 366-377 -->
purpose reward model through trajectory comparisons, and TOPReward reads the token probabilities of a videolanguage model as hidden rewards. A survey of verifiers for robot policies [14] maps the wider family. Midepisode failure detection is its own line of work, and our monitors borrow from it. FAIL-Detect [17] and SAFE [3] learn uncertainty- and feature-based failure scores for imitation and VLA policies. FARM [9] reads failure signals from the internal states of a frozen world model, close to our world-model monitors, and ReAP [6] predicts action-conditioned risk, the idea behind our risk head. VLA-Corrector [13], Spotter [4] and REMORA [15] add stage verification, a reflecting VLM and recurrent progress tracking. ArmnetBench [12] and a standardized SO-101 VLA benchmark [18] evaluate policies on the same low-cost arm. None of these works reports the elapsed-length baseline under the dataset’s stopping rule, and that comparison is what this paper adds.

<!-- editlens paragraph 0.303 lines 384-392 -->
Before evaluating a reward model as a failure detector, run episode length within policy on the same rows, and say how the episodes ended. On a benchmark that stops at a time limit, length was the detector to beat, and neither reward model beat it. On rollouts an operator stopped, length was useless, and what caught failures was a judge that saw the whole finished episode in the right input format.

### Appendix: from plain name to analysis (mean 0.053)

<!-- editlens chunk 0.053 lines 553-559 -->
<!-- editlens paragraph 0.053 lines 553-559 -->
Every number is recomputable from the repository; this [13] Chang Song, Bin Qian, Yan Feng, and Zhijie Song. table maps each analysis to its files. Vla-corrector: Stage-aware observable state understanding for prompt-based closed-loop recovery of vision-language-action policies. arXiv preprint arXiv:2609.06508, 2026. github.com/ravediamond/paper-reward-models-stopping-rule · be24544
