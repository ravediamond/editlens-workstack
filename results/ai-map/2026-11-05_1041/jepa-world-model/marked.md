# paper-jepa-world-model: chunks in paper order

## rendered source (numbers filled)

### Abstract (mean 0.116)

<!-- editlens chunk 0.116 lines 7-7 -->
<!-- editlens paragraph 0.116 lines 7-7 -->
A small JEPA world model trained on a low-cost arm reads how an episode ended, and its predictor adds nothing to that reading. We trained the model in the LeWorldModel recipe on teleoperated demonstrations of one tabletop task on an SO-101 arm, then re-tested on it every use of such a model we found in recent papers, each against a bar written into a public register. Every use that needs the predictor to roll forward misses its bar, chunk ranking, surprise monitoring and risk prediction among them. The encoder does better. On policy rollouts it never saw, a linear probe on its last-frame latent separates success from failure about as well as a hand-built colour judge (AUROC 0.95 against 0.94), and better than a frozen DINOv2 encoder or the commanded joints. At the grasp, the imagined latent reads the outcome worse than the current one (0.70 against 0.82). So before building on the predictor of a model this size, probe its encoder. The controls are exploratory, and everything comes from one rig, one model and one data scale.

### Introduction (mean 0.138)

<!-- editlens chunk 0.138 lines 11-19 -->
<!-- editlens paragraph 0.128 lines 11-11 -->
A world model is usually valued for its predictor. In the sense of LeWorldModel (LeWM) [1] it has two parts: an encoder that maps camera frames to a latent vector, and a predictor that takes the current latent and a sequence of actions and imagines the latents that follow, both trained together from pixels with a joint-embedding predictive (JEPA) loss. The uses proposed for it lean on the predictor: ranking a policy's candidate action chunks by their imagined outcome, flagging a failure when the observed latent drifts from the predicted one, reading the outcome of a grasp before it happens, planning over several time scales. Each paper reports the use that worked, on its own robot and data.

<!-- editlens paragraph 0.093 lines 13-13 -->
We had one such model, trained for $3.30 of rented GPU time on our own arm, and wanted to know which of these uses we could build on. So we ran every use we could find on that one model. Each re-test is a row of a register with a bar, a dataset, a result and a verdict, and where we managed it, the bar and the decision rule went into the repository before the result existed (that commit order is all we mean by pre-registration). Checked against the commit history, all 20 rows match a pre-registration record. In 19 the bar was committed before the result, and in 1 (the two-level hierarchical progress use) in the same commit. One row is not a use of our model: it times the pretrained RoboJEPA and V-JEPA 2.1 encoders on our on-board computer [2, 3]. Of the 20 rows, 3 pass and 1 is met as predicted. Another 2 are not proven, and the remaining 14 fail or are no-go.

<!-- editlens paragraph 0.281 lines 15-15 -->
The first draft of this paper argued something else. Our reading of the failures was that the latent mostly encodes the arm's pose, so a frozen image encoder or the commanded joints would do at least as well in every one of them. We ran those controls on 69 policy rollouts before writing it up, and they did not bear it out: the encoder reads how the episode went better than either control. We rewrote the claim. At this data scale the predictor, not the encoder, is the weak link.

<!-- editlens paragraph 0.313 lines 17-17 -->
One moment runs through the rest of the paper: the grasp anchor, 15 frames before the gripper first closes. There the current latent reads the outcome at 0.82 and the imagined latent at 0.70, and that gap is the argument in one row.

<!-- editlens paragraph 0.307 lines 19-19 -->
The controls came after the data, which limits what they can show. Each readout is a linear probe fit with leave-one-session-out (LOSO) cross-validation on the 69 rollouts (44 success, 25 failure, 13 sessions), scored against labels the author gave at rest. The model was trained on teleoperation only and never saw these rollouts. No bar was committed for these comparisons, so everything this paper says about the split between encoder and predictor is exploratory. Of the 3 register passes, 3 have their bar committed before the result, though the register marks the outcome-readout verdict as retrospective.

### Setup (mean 0.125)

<!-- editlens chunk 0.125 lines 23-27 -->
<!-- editlens paragraph 0.051 lines 23-23 -->
The robot is one SO-101 arm [4] driven through LeRobot [5], with a top and a wrist camera. The task is to put a bowl into another bowl. Our model is trained on X, split by grid layout into 157 training and 25 validation episodes. The evaluation rollouts come from a separate dataset, X: SmolVLA [6] runs recorded after our model was trained.

<!-- editlens paragraph 0.084 lines 25-25 -->
Our model follows the LeWM recipe [1], with a multi-view ViT encoder, an action-conditioned predictor and the SIGReg regulariser. We set it beside four signals, each chosen because it is cheaper than a world model. The frozen DINOv2-S control is a frozen DINOv2 small encoder [7] mean-pooled over the top and wrist views (the design of DINO-WM [8]). The joints control is the commanded joint vector. The colour judge is a hand-built rule on the final frame with no learning, and policy identity is the checkpoint that ran the episode.

<!-- editlens paragraph 0.308 lines 27-27 -->
In October, a timing test on the on-board computer loaded our checkpoint with X. Under the transformers version on that image (5.5.4), 192 encoder tensors did not match and were silently dropped, so the test timed a random encoder. We voided its latents and traced how every other use loaded the model: 26 ran the trained model, 1 ran a random one (that test) and none is unknown. The world-model block of VLA-JEPA, which one diagnostic below uses, loads all 351 of its keys.

### The register (mean 0.233)

<!-- editlens chunk 0.233 lines 31-60 -->
<!-- editlens paragraph 0.270 lines 58-58 -->
Among the encoder uses, reading the outcome works and reading progress does not. The outcome readout at rest passes, and at the grasp anchor the current latent reads the grasp at 0.82. The four uses that ask the latent for progress or task stage all fail: progress monotonicity, two-level hierarchical progress [10], the latent stage tracker and the latent-distance scale of SURVEYOR [13]. The pose probes of LeJEPA [12] say what else the latent holds. A linear readout recovers about half of the joint variance from our encoder (R² 0.565), less than from the frozen DINOv2-S control (0.867).

<!-- editlens paragraph 0.333 lines 60-60 -->
The predictor does predict its own latent: at K = 30 its open-loop error is 0.31, against 0.89 for copying the last latent. What fails is every use of that prediction. Chunk ranking [1] puts the executed chunk first in 0.60 of anchors against a bar of 0.8, while the commanded actions alone reach 0.68–0.90 (so the cheapest signal in the table beats the use built on imagination). The surprise monitor catches 2/8 at 2/42 failures. The hierarchical planner [14] shows no crossover. The conformal surprise band, the re-ranking of chunk candidates, the action-conditioned risk head [11] and the calibrated surprise reflex each miss their bar by the margin in Table 1.

### What the encoder knows (mean 0.129)

<!-- editlens chunk 0.129 lines 64-84 -->
<!-- editlens paragraph 0.071 lines 64-64 -->
Does the encoder carry anything that a frozen encoder or the joints do not? Table 2 sets our model beside the four other signals on the same 69 rollouts. Every probe is a LOSO linear probe against the author's labels. At rest the interval is a 95 % episode-bootstrap CI; at the anchor it is a bootstrap of the mean over 5 seeds of the out-of-fold AUROC (episodes resampled jointly across the seeds, 2,000 resamples, percentile).

<!-- editlens paragraph 0.191 lines 78-78 -->
At rest our model is level with the colour judge (the CIs overlap) and above the frozen encoder and the joints. At the grasp anchor no judge applies, and our model leads both controls. Since the pose probes hold the joints better than our encoder does but the outcome worse, the encoder carries outcome information they lack, at least on these rollouts.

<!-- editlens paragraph 0.211 lines 80-80 -->
The anchor column depends on how the five seeds are combined. Averaging the predictions before scoring gives 0.8377, 0.7175 and 0.5346 for our model, frozen DINOv2-S and the joints. Seed 0 alone gives 0.7554, 0.7024 and 0.5574, a smaller gap between our model and the frozen encoder. The order holds either way.

<!-- editlens paragraph 0.177 lines 82-82 -->
One control does beat our model. On SURVEYOR's scale check, frozen DINOv2-S (τ 0.3601) and the joints (τ 0.0265) pass where our model fails (τ 1.2488, against 0.20 reported by SURVEYOR). The same task and the same rollouts pass with other features, so the failure points at the geometry of our latent space rather than at the task.

<!-- editlens paragraph 0.139 lines 84-84 -->
The register's own outcome-readout row reports 1.000. That number was scored against the colour judge's labels, on 87 rollouts, so it partly measures agreement with the judge. Against the author's labels on the 69 rollouts, with the controls beside it, the same readout gives 0.9545.

### Where the predictor fails (mean 0.172)

<!-- editlens chunk 0.172 lines 88-106 -->
<!-- editlens paragraph 0.323 lines 88-88 -->
ContactGuard [9] finds that probes on the imagined latent beat probes on the current one for grasp tasks, so we expected the imagined latent to help at our grasp anchor. The bar asked it for ≥ 0.85, ≥ +0.05 over the current latent. With the same encoder and the same anchor, the current latent reads the outcome at 0.82 and the imagined one at 0.70. This pre-registered row fails: on these rollouts, imagining forward loses outcome information the encoder had.

<!-- editlens paragraph 0.136 lines 90-90 -->
Our model's inverse-dynamics term is no better than that of its own untrained network. On the distillation probe, pooled over the 25 teleoperation validation episodes, the trained model scores 0.7476 and its random initialisation 0.7974, a difference of −0.0499 with a 95 % paired episode-bootstrap CI of [−0.7403, +0.6559] (X). The term itself is fragile: the same untrained network scored 1.4383 on one machine and 0.7974 and 0.8042 on two others (it is sensitive to the BLAS library and to ridge conditioning).

<!-- editlens paragraph 0.222 lines 92-92 -->
A low score can also come from a bug, so we checked the surprise monitor's failure-class AUROC (0.775, below its sanity bar) for one in loading or scoring. The same scorer reproduces the open-loop corruption ratios at K = 30: cross-episode 3.428 against 3.341 in the original run, constant-first 2.558 against 2.543 (X). The low AUROC is a real value.

<!-- editlens paragraph 0.249 lines 94-94 -->
The predictor of VLA-JEPA barely uses its actions. At 5 anchors (Table 3, from X), action tokens taken from another episode differ from the true ones by 21–28 % in relative L2 but move the loss by only about 0.05 %. Zeroing the tokens moves it by about 1.05 % on average, and the forward pass is deterministic. Its failure-class AUROC of 0.501, below the same sanity bar, is therefore real, and we leave its table unread under the frozen bar.

<!-- editlens paragraph 0.344 lines 106-106 -->
A reader may object that one pass in the register is predictive. In the anticipation step of the outcome-readout gate, the imagined latent beat policy identity by +0.179. That bar is retrospective, though, and the two reruns of the same idea with the bar committed first, the grasp probe and the calibrated surprise reflex, both fail.

### Related work (mean 0.205)

<!-- editlens chunk 0.205 lines 110-110 -->
<!-- editlens paragraph 0.205 lines 110-110 -->
LeWorldModel [1] trains the recipe we use end to end from pixels and plans with it in Push-T and in simulation. Its two planning uses, chunk ranking and re-ranking, fail on our arm. LeJEPA's identifiability analysis [12] predicts that SIGReg latents identify the state up to anisotropy; our pose probes support that only in part. DINO-WM [8] plans on frozen DINOv2 [7] patches, which is why our frozen control is built that way. V-JEPA 2.1 [3] and RoboJEPA [2] are too slow on our on-board computer; timing them is the one register row that is not a use of our model. ContactGuard [9] is the result we contradict most directly: it finds imagined-latent probes better than current-latent ones on grasp tasks, and we find the reverse. The re-tests of ReAP's action-conditioned risk [11], the hierarchical planners of HWM [14] and H-JEPA [10] and SURVEYOR's latent-distance scale [13] all miss their bars here. Two papers agree with us from the control side. SaiVLA-JEPA [15] reports that a training-only future-latent head adds +0.03 points to control on 10,030 paired episodes, and HIJP [16] finds LeWM below goal-conditioned behaviour cloning in simulation.

### Limitations (mean 0.325)

<!-- editlens chunk 0.325 lines 114-114 -->
<!-- editlens paragraph 0.325 lines 114-114 -->
The claim most likely to move is the split between encoder and predictor, because it rests on probes chosen after the data and on 69 rollouts labelled by the author. Fresh rollouts scored under a bar committed first would test it. They need a day on the arm, which is not scheduled yet. The second risk is scale: everything comes from one model at one data scale, and a second point at 653 episodes is costed and queued. Three controls were not run (the surprise monitor and the imagined arm of the grasp probe would each need a predictor trained on frozen DINOv2-S features or on the joints, and progress monotonicity with the controls would need a reimplementation). The outcome-readout verdict is retrospective, and the two-level hierarchical progress use has its bar in the same commit as its result. Ordered by commit alone, without the audit, the register would read 13 bar-first and 6 same-commit rows.

### Conclusion (mean 0.373)

<!-- editlens chunk 0.373 lines 118-118 -->
<!-- editlens paragraph 0.373 lines 118-118 -->
Before building on the predictor of a world model this size, probe its encoder and keep the commanded actions as a baseline. On our 182 demonstrations the current latent read the grasp outcome better than the imagined one, the commanded actions alone ranked chunks better than the predictor, and every forecasting use missed its bar. A predictor may earn its place at a larger data scale, which is the next point we will measure.

### (figure and table captions) (mean 0.173)

<!-- editlens chunk 0.173 lines 33-96 -->
<!-- editlens paragraph 0.173 lines 33-33 -->
Table 1: The register: every use of our world model re-tested here (with the frozen-DINOv2 and RoboJEPA rows beside it), what it takes from the model, whether its bar came before the result, and the verdict. Read the takes column against the verdict: the predictor uses fail. Bar, result and verdict are quoted from repro/register/expected/FEASIBILITY.md §2.

## built PDF

### (front matter) (mean 0.134)

<!-- editlens chunk 0.134 lines 3-8 -->
A small JEPA world model on a low-cost arm: the encoder reads the outcome, the predictor adds nothing to it Ravindu Somawansa∗ Shisso Robotics, Paris ravindu.somawansa@gmail.com

### Abstract (mean 0.123)

<!-- editlens chunk 0.131 lines 10-76 -->
<!-- editlens paragraph 0.106 lines 10-25 -->
A small JEPA world model trained on a low-cost arm reads how an episode ended, and its predictor adds nothing to that reading. We trained the model in the LeWorldModel recipe on teleoperated demonstrations of one tabletop task on an SO-101 arm, then re-tested on it every use of such a model we found in recent papers, each against a bar written into a public register. Every use that needs the predictor to roll forward misses its bar, chunk ranking, surprise monitoring and risk prediction among them. The encoder does better. On policy rollouts it never saw, a linear probe on its last-frame latent separates success from failure about as well as a handbuilt colour judge (AUROC 0.95 against 0.94), and better than a frozen DINOv2 encoder or the commanded joints. At the grasp, the imagined latent reads the outcome worse than the current one (0.70 against 0.82). So before building on the predictor of a model this size, probe its encoder. The controls are exploratory, and everything comes from one rig, one model and one data scale.

<!-- editlens paragraph 0.151 lines 30-42 -->
A world model is usually valued for its predictor. In the sense of LeWorldModel (LeWM) [1] it has two parts: an encoder that maps camera frames to a latent vector, and a predictor that takes the current latent and a sequence of actions and imagines the latents that follow, both trained together from pixels with a joint-embedding predictive (JEPA) loss. The uses proposed for it lean on the predictor: ranking a policy’s candidate action chunks by their imagined outcome, flagging a failure when the observed latent drifts from the predicted one, reading the outcome of a grasp before it happens, planning over several time scales. Each paper reports the use that worked, on its own robot and data.

<!-- editlens paragraph 0.207 lines 43-76 -->
We had one such model, trained for $3.30 of rented GPU time on our own arm, and wanted to know which of these uses we could build on. So we ran every use we could find on that one model. Each re-test is a row of a register with a bar, a dataset, a result and a verdict, and where we managed it, the bar and the decision rule went into the repository before the result existed (that commit order is all we mean by pre-registration). Checked against the commit history, all 20 rows match a preregistration record. In 19 the bar was committed before the result, and in 1 (the two-level hierarchical progress use) in the same commit. One row is not a use of our model: it times the pretrained RoboJEPA and V-JEPA 2.1 encoders on our on-board computer [2, 3]. Of the 20 rows, 3 pass and 1 is met as predicted. Another 2 are not proven, and the remaining 14 fail or are no-go. The first draft of this paper argued something else. Our reading of the failures was that the latent mostly encodes the arm’s pose, so a frozen image encoder or the commanded joints would do at least as well in every one of them. We ran those controls on 69 policy rollouts before writing it up, and they did not bear it out: the encoder reads how the episode went better than either control. We rewrote the claim. At this data scale the predictor, not the encoder, is the weak link. One moment runs through the rest of the paper: the grasp anchor, 15 frames before the gripper first closes. There the current latent reads the outcome at 0.82 and the imagined latent at 0.70, and that gap is the argument in one row. The controls came after the data, which limits what they can show. Each readout is a linear probe fit with leave-one-session-out (LOSO) cross-validation on the 69 rollouts (44 success, 25 failure, 13 sessions), scored against labels the author gave at rest. The model was trained on teleoperation only and never saw these rollouts. No bar was committed for these comparisons, so everything this paper says about the split between encoder and predictor is exploratory. Of the 3 register passes, 3 have their bar committed before the result, though the register marks the outcome-readout verdict as retrospective.

<!-- editlens chunk 0.093 lines 94-185 -->
<!-- editlens paragraph 0.091 lines 94-117 -->
The robot is one SO-101 arm [4] driven through LeRobot [5], with a top and a wrist camera. The task is to put a bowl into another bowl. Our model is trained on ravediamond/so101_bowls_all_trimmed, split by grid layout into 157 training and 25 validation episodes. The evaluation rollouts come from a separate dataset, ravediamond/so101-bowls-policy-rollouts: SmolVLA [6] runs recorded after our model was trained. Our model follows the LeWM recipe [1], with a multiview ViT encoder, an action-conditioned predictor and the SIGReg regulariser. We set it beside four signals, each chosen because it is cheaper than a world model. The frozen DINOv2-S control is a frozen DINOv2 small encoder [7] mean-pooled over the top and wrist views (the design of DINO-WM [8]). The joints control is the commanded joint vector. The colour judge is a hand-built rule on the final frame with no learning, and policy identity is the checkpoint that ran the episode. In October, a timing test on the on-board computer loaded our checkpoint with strict=False. Under the transformers version on that image (5.5.4), 192 encoder tensors did not match and were silently dropped, so the test timed a random encoder. We voided its latents and traced how every other use loaded the model: 26 ran the trained model, 1 ran a random one (that test) and none is unknown. The world-model block of VLA-JEPA, which one diagnostic below uses, loads all 351 of its keys.

<!-- editlens paragraph 0.127 lines 147-152 -->
Figure 1: Table 2 as a dot plot: level with the colour judge at rest, ahead of both controls at the anchor. The right panel shows the seed range, not a CI. risk head [11] and the calibrated surprise reflex each miss their bar by the margin in Table 1.

<!-- editlens paragraph 0.132 lines 157-185 -->
Does the encoder carry anything that a frozen encoder or the joints do not? Table 2 sets our model beside the four other signals on the same 69 rollouts. Every probe is a LOSO linear probe against the author’s labels. At rest the interval is a 95 % episode-bootstrap CI; at the anchor it is a bootstrap of the mean over 5 seeds of the out-of-fold AUROC (episodes resampled jointly across the seeds, 2,000 resamples, percentile). At rest our model is level with the colour judge (the CIs overlap) and above the frozen encoder and the joints. At the grasp anchor no judge applies, and our model leads both controls. Since the pose probes hold the joints better than our encoder does but the outcome worse, the encoder carries outcome information they lack, at least on these rollouts. The anchor column depends on how the five seeds are combined. Averaging the predictions before scoring gives 0.8377, 0.7175 and 0.5346 for our model, frozen DINOv2-S and the joints. Seed 0 alone gives 0.7554, 0.7024 and 0.5574, a smaller gap between our model and the frozen encoder. The order holds either way. One control does beat our model. On SURVEYOR’s scale check, frozen DINOv2-S (τ 0.3601) and the joints (τ 0.0265) pass where our model fails (τ 1.2488, against 0.20 reported by SURVEYOR). The same task and the same rollouts pass with other features, so the failure points at the geometry of our latent space rather than at the task. The register’s own outcome-readout row reports 1.000. That number was scored against the colour judge’s labels, on 87 rollouts, so it partly measures agreement with the judge. Against the author’s labels on the 69 rollouts, with the controls beside it, the same readout gives 0.9545.

<!-- editlens chunk 0.124 lines 186-215 -->
<!-- editlens paragraph 0.158 lines 186-208 -->
Table 1 lists the 20 uses and what each takes from our model: the encoder alone (7), the predictor (8) or both (5). Read that column against the verdicts. Among the encoder uses, reading the outcome works and reading progress does not. The outcome readout at rest passes, and at the grasp anchor the current latent reads the grasp at 0.82. The four uses that ask the latent for progress or task stage all fail: progress monotonicity, two-level hierarchical progress [10], the latent stage tracker and the latent-distance scale of SURVEYOR [13]. The pose probes of LeJEPA [12] say what else the latent holds. A linear readout recovers about half of the joint variance from our encoder (R2 0.565), less than from the frozen DINOv2-S control (0.867). The predictor does predict its own latent: at K = 30 its open-loop error is 0.31, against 0.89 for copying the last latent. What fails is every use of that prediction. Chunk ranking [1] puts the executed chunk first in 0.60 of anchors against a bar of 0.8, while the commanded actions alone reach 0.68–0.90 (so the cheapest signal in the table beats the use built on imagination). The surprise monitor 5 Where the predictor fails catches 2/8 at 2/42 failures. The hierarchical planner [14] shows no crossover. The conformal surprise band, the ContactGuard [9] finds that probes on the imagined lare-ranking of chunk candidates, the action-conditioned tent beat probes on the current one for grasp tasks, so we github.com/ravediamond/paper-jepa-world-model · 82dc90d

<!-- editlens paragraph 0.159 lines 211-215 -->
Table 1: The register: every use of our world model re-tested here (with the frozen-DINOv2 and RoboJEPA rows beside it), what it takes from the model, whether its bar came before the result, and the verdict. Read the takes column against the verdict: the predictor uses fail. Bar, result and verdict are quoted from repro/register/expected/FEASIBILITY.md §2. use

<!-- editlens chunk 0.106 lines 579-664 -->
<!-- editlens paragraph 0.081 lines 579-606 -->
ined one at 0.70. This pre-registered row fails: on these rollouts, imagining forward loses outcome information the encoder had. Our model’s inverse-dynamics term is no better than feature at rest grasp anchor (65 scored, 21 fail) that of its own untrained network. On the distillaour world model 0.9545 [0.9023, 0.9908] 0.8199 [0.7141, 0.9041] colour judge (no learning) 0.9432 [0.8919, 0.9878] — tion probe, pooled over the 25 teleoperation validation frozen DINOv2-S 0.8655 [0.7767, 0.9405] 0.7067 [0.5816, 0.8269] episodes, the trained model scores 0.7476 and its rancommanded joints 0.7573 [0.6084, 0.8880] 0.5305 [0.3709, 0.6855] policy identity 0.5882 [0.4084, 0.7515] — dom initialisation 0.7974, a difference of −0.0499 with a 95 % paired episode-bootstrap CI of [−0.7403, +0.6559] (gap5_pooled_rerun.json). The term itself is fragile: expected the imagined latent to help at our grasp anchor. the same untrained network scored 1.4383 on one maThe bar asked it for ≥ 0.85, ≥ +0.05 over the current la- chine and 0.7974 and 0.8042 on two others (it is sensitive tent. With the same encoder and the same anchor, the to the BLAS library and to ridge conditioning). current latent reads the outcome at 0.82 and the imagA low score can also come from a bug, so we Table 2: Outcome AUROC of each signal on the same 69 rollouts (exploratory: controls chosen after the data). Look at the anchor column, where no judge applies.

<!-- editlens paragraph 0.305 lines 645-664 -->
checked the surprise monitor’s failure-class AUROC (0.775, below its sanity bar) for one in loading or scoring. The same scorer reproduces the open-loop corruption ratios at K = 30: cross-episode 3.428 against 3.341 in the original run, constant-first 2.558 against 2.543 (M1_diag_g0_repro.json). The low AUROC is a real value. The predictor of VLA-JEPA barely uses its actions. At 5 anchors (Table 3, from M3_diag_action_shuffle.json), action tokens taken from another episode differ from the true ones by 21–28 % in relative L2 but move the loss by only about 0.05 %. Zeroing the tokens moves it by about 1.05 % on average, and the forward pass is deterministic. Its failure-class AUROC of 0.501, below the same sanity bar, is therefore real, and we leave its table unread under the frozen bar. A reader may object that one pass in the register is predictive. In the anticipation step of the outcome-readout gate, the imagined latent beat policy identity by +0.179. That bar is retrospective, though, and the two reruns of the same idea with the bar committed first, the grasp probe and the calibrated surprise reflex, both fail.

<!-- editlens chunk 0.170 lines 673-718 -->
<!-- editlens paragraph 0.325 lines 673-685 -->
The claim most likely to move is the split between encoder and predictor, because it rests on probes chosen after the data and on 69 rollouts labelled by the author. Fresh rollouts scored under a bar committed first would test it. They need a day on the arm, which is not scheduled yet. The second risk is scale: everything comes from one model at one data scale, and a second point at 653 episodes is costed and queued. Three controls were not run (the surprise monitor and the imagined arm of the grasp probe would each need a predictor trained on frozen DINOv2-S features or on the joints, and progress monotonicity with the controls would need a reimplementation). The outcome-readout verdict is retrospective, and the two-level hierarchical progress use has its bar in the same commit as its result. Ordered by commit alone, without the audit, the register would read 13 bar-first and 6 same-commit rows.

<!-- editlens paragraph 0.373 lines 690-698 -->
Before building on the predictor of a world model this size, probe its encoder and keep the commanded actions as a baseline. On our 182 demonstrations the current latent read the grasp outcome better than the imagined one, the commanded actions alone ranked chunks better than the predictor, and every forecasting use missed its bar. A predictor may earn its place at a larger data scale, which is the next point we will measure.

<!-- editlens paragraph 0.195 lines 701-718 -->
LeWorldModel [1] trains the recipe we use end to end from pixels and plans with it in Push-T and in simulation. Its two planning uses, chunk ranking and reranking, fail on our arm. LeJEPA’s identifiability analysis [12] predicts that SIGReg latents identify the state up to anisotropy; our pose probes support that only in part. DINO-WM [8] plans on frozen DINOv2 [7] patches, which is why our frozen control is built that way. V-JEPA 2.1 [3] and RoboJEPA [2] are too slow on our on-board computer; timing them is the one register row that is not a use of our model. ContactGuard [9] is the result we contradict most directly: it finds imaginedlatent probes better than current-latent ones on grasp tasks, and we find the reverse. The re-tests of ReAP’s action-conditioned risk [11], the hierarchical planners of HWM [14] and H-JEPA [10] and SURVEYOR’s latentdistance scale [13] all miss their bars here. Two papers agree with us from the control side. SaiVLA-JEPA [15] reports that a training-only future-latent head adds +0.03 points to control on 10,030 paired episodes, and HIJP [16] finds LeWM below goal-conditioned behaviour cloning github.com/ravediamond/paper-jepa-world-model · 82dc90d
