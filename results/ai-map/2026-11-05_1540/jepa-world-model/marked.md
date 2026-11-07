# paper-jepa-world-model: chunks in paper order

## rendered source (numbers filled)

### Abstract (mean 0.086)

<!-- editlens chunk 0.086 lines 7-7 -->
<!-- editlens paragraph 0.086 lines 7-7 -->
We trained a small JEPA world model in the LeWorldModel recipe for $3.30 of rented GPU time. The training data are teleoperated demonstrations of one tabletop task on an SO-101 arm. We then re-tested on this model the uses of such models that recent papers propose. Each use has a threshold in a public register. We tested the encoder on policy rollouts the model never saw. A linear probe on its last-frame latent separates success from failure about as well as a hand-built colour judge. It does better than a frozen DINOv2 encoder and better than the commanded joints. The predictor adds nothing to this. At the grasp, the imagined latent reads the outcome at 0.70 and the current latent at 0.82. Every use that needs the predictor to roll forward misses its threshold at this data scale. The controls are exploratory and come from one rig and one model.

### Introduction (mean 0.178)

<!-- editlens chunk 0.178 lines 11-19 -->
<!-- editlens paragraph 0.335 lines 11-11 -->
LeWorldModel (LeWM) [1] trains a world model in two parts. The encoder maps camera frames to a latent vector. The predictor takes the current latent and a sequence of actions and imagines the latents that follow. Both are trained together from pixels with a joint-embedding predictive (JEPA) loss. Papers built on these models propose several uses. Most of them need the predictor. One ranks a policy's candidate action chunks by their imagined outcome. Others flag a failure when the observed latent drifts from the predicted one, read the outcome of a grasp before it happens, or plan over several time scales. Each paper reports the use that worked on its own robot and data.

<!-- editlens paragraph 0.091 lines 13-13 -->
We had one such model, trained on our own arm. We ran every use we could find on it. Each re-test is a row of a register with a threshold, a dataset, a result and a verdict. Where we managed it, the threshold and the decision rule went into the repository before the result existed. That commit order is what we mean by pre-registration. All 20 rows match a pre-registration record in the commit history. In 19 of them the bar was in place before the result. The two-level hierarchical progress use had it in the same commit. One more row is not a use of our model. It times the pretrained RoboJEPA [2] and V-JEPA 2.1 [3] encoders on our on-board computer. 14 of the 20 rows fail or are no-go. Table 1 lists all of them.

<!-- editlens paragraph 0.201 lines 15-15 -->
The first version of this paper argued something completely different. We read the failures as a sign that the latent mostly encodes the arm's pose. Then a frozen image encoder or the commanded joints would do at least as well. We ran these controls on 69 policy rollouts. The encoder read how the episode went better than either control. We modified the claim around the predictor.

<!-- editlens paragraph 0.226 lines 19-19 -->
The controls came after the data. Each readout is a linear probe with leave-one-session-out (LOSO) cross-validation on the 69 rollouts (44 success, 25 failure, 13 sessions). The labels were given at rest by the author. The model was trained on teleoperation only and never saw these rollouts. No threshold was committed for these comparisons. Everything this paper says about the split between encoder and predictor is therefore exploratory. 3 of the 3 register passes have their bar committed before the result. The register still marks the outcome-readout verdict as retrospective.

### Setup (mean 0.071)

<!-- editlens chunk 0.071 lines 23-27 -->
<!-- editlens paragraph 0.038 lines 23-23 -->
The robot is one SO-101 arm [4] driven through LeRobot [5], with a top and a wrist camera. The task is to put a bowl into another bowl. We trained our model on X, split by grid layout into 157 training and 25 validation episodes. The evaluation rollouts come from a separate dataset, X. They are SmolVLA [6] runs recorded after our model was trained.

<!-- editlens paragraph 0.078 lines 25-25 -->
Our model follows the LeWM recipe [1], with a multi-view ViT encoder, an action-conditioned predictor and the SIGReg regulariser. We compare it with four cheaper signals. The frozen DINOv2-S control is a frozen DINOv2 small encoder [7], mean-pooled over the top and wrist views as in DINO-WM [8]. The joints control is the commanded joint vector. The colour judge is a hand-built rule on the final frame with no learning. Policy identity is the checkpoint that ran the episode.

<!-- editlens paragraph 0.231 lines 27-27 -->
In October we found a loading bug. A timing test on the on-board computer loaded our checkpoint with X. The image had transformers 5.5.4, and under that version 192 encoder tensors did not match. They were dropped without an error, so the test timed a random encoder. We voided its latents. We then traced how every other use loaded the model. 26 ran the trained model and 1 ran a random one (that test). The world-model block of VLA-JEPA, which one diagnostic below uses, loads all 351 of its keys.

### The register (mean 0.221)

<!-- editlens chunk 0.221 lines 31-60 -->
<!-- editlens paragraph 0.177 lines 58-58 -->
Among the encoder uses, reading the outcome works. The outcome readout at rest passes. At the grasp anchor the current latent reads the grasp at 0.82. Reading progress does not work. Four uses ask the latent for progress or task stage, and all four fail. They are progress monotonicity, two-level hierarchical progress [10], the latent stage tracker and SURVEYOR's latent-distance scale [13]. We also ran the pose probes of LeJEPA [12]. A linear readout recovers about half of the joint variance from our encoder (R² 0.565). It recovers more from the frozen DINOv2-S control (0.867).

<!-- editlens paragraph 0.254 lines 60-60 -->
The predictor does predict its own latent. At K = 30 its open-loop error is 0.31. Copying the last latent gives 0.89. The uses of this prediction fail. In chunk ranking [1] the model puts the executed chunk first in 0.60 of anchors. The threshold was 0.8. The commanded actions alone reach 0.68–0.90. The surprise monitor catches 2/8 at 2/42 failures. The hierarchical planner [14], the conformal surprise band, re-ranking, the risk head [11] and the calibrated reflex also miss their thresholds. Table 1 gives the margins.

### What the encoder knows (mean 0.106)

<!-- editlens chunk 0.106 lines 64-84 -->
<!-- editlens paragraph 0.060 lines 64-64 -->
We tested whether the encoder carries anything that a frozen encoder or the joints do not. Table 2 sets our model beside the four other signals on the same 69 rollouts. Every probe is a LOSO linear probe against the author's labels. At rest the interval is a 95 % episode-bootstrap CI. At the anchor it is a bootstrap of the mean over 5 seeds of the out-of-fold AUROC, with episodes resampled jointly across the seeds (2,000 resamples, percentile).

<!-- editlens paragraph 0.174 lines 78-78 -->
At rest our model is level with the colour judge. The two CIs overlap. Our model is above the frozen encoder and the joints. At the grasp anchor no judge applies, and our model is above both controls. The pose probes hold the joints better than our encoder does. They hold the outcome worse. On these rollouts the encoder has outcome information that the pose alone does not give.

<!-- editlens paragraph 0.116 lines 80-80 -->
The anchor column depends on how the five seeds are combined. If we average the predictions before scoring, our model gets 0.8377, frozen DINOv2-S 0.7175 and the joints 0.5346. With seed 0 alone they get 0.7554, 0.7024 and 0.5574. The gap to the frozen encoder is smaller with seed 0. The order is the same.

<!-- editlens paragraph 0.140 lines 82-82 -->
On SURVEYOR's scale check the controls do better than our model. Frozen DINOv2-S has τ 0.3601 and the joints τ 0.0265, and both pass. Our model has τ 1.2488 and fails. SURVEYOR reports 0.20. The task and the rollouts are the same for all three features. We take the failure as a property of our latent space.

### Where the predictor fails (mean 0.186)

<!-- editlens chunk 0.186 lines 88-106 -->
<!-- editlens paragraph 0.235 lines 88-88 -->
ContactGuard [9] finds that probes on the imagined latent beat probes on the current latent for grasp tasks. We expected the same at our grasp anchor. The pre-registered threshold asked the imagined latent for ≥ 0.85, ≥ +0.05 over the current one. We find the reverse. With the same encoder and the same anchor, the current latent reads the outcome at 0.82 and the imagined latent at 0.70. The row fails.

<!-- editlens paragraph 0.146 lines 90-90 -->
We also ran the distillation probe on our model's inverse-dynamics term, pooled over the 25 teleoperation validation episodes. The trained model scores 0.7476. Its random initialisation scores 0.7974. The difference is −0.0499, with a 95 % paired episode-bootstrap CI of [−0.7403, +0.6559] (X). The term depends on the machine. The same untrained network scored 1.4383 on one machine and 0.7974 and 0.8042 on two others. It is sensitive to the BLAS library and to ridge conditioning.

<!-- editlens paragraph 0.212 lines 92-92 -->
The surprise monitor has a failure-class AUROC of 0.775, below its sanity bar. We checked it for a loading or scoring bug. The same scorer reproduces the open-loop corruption ratios at K = 30 (X). Cross-episode gives 3.428, against 3.341 in the original run. Constant-first gives 2.558, against 2.543. We found no bug.

<!-- editlens paragraph 0.193 lines 94-94 -->
We ran an action-shuffle check on the predictor of VLA-JEPA at 5 anchors (Table 3, from X). Action tokens from another episode differ from the true ones by 21–28 % in relative L2. They move the loss by about 0.05 %. Zeroing the tokens moves it by about 1.05 % on average. The forward pass is deterministic. The predictor barely uses its actions. Its failure-class AUROC is 0.501, below the same sanity check, and we leave its table unread under the frozen bar.

<!-- editlens paragraph 0.311 lines 106-106 -->
One pass in the register uses the imagined latent. In the anticipation step of the outcome-readout gate, the imagined latent beat policy identity by +0.179. That bar is retrospective. We reran the same idea twice with the threshold committed first, in the grasp probe and in the calibrated surprise reflex. Both fail.

### Related work (mean 0.238)

<!-- editlens chunk 0.238 lines 110-110 -->
<!-- editlens paragraph 0.238 lines 110-110 -->
LeWorldModel [1] trains the recipe we use end to end from pixels and plans with it in Push-T and in simulation. We tested its two planning uses on our arm, and both fail. LeJEPA's identifiability analysis [12] predicts that SIGReg latents identify the state up to anisotropy. Our pose probes support this in part. DINO-WM [8] plans on frozen DINOv2 [7] patches, and our frozen control uses the same design. We timed V-JEPA 2.1 [3] and RoboJEPA [2] on our on-board computer, and both are too slow. ContactGuard [9] finds imagined-latent probes better than current-latent ones on grasp tasks. On our arm we find the reverse. We also re-tested ReAP's action-conditioned risk [11], the hierarchical planners of HWM [14] and H-JEPA [10], and SURVEYOR's latent-distance scale [13]. All of them miss here, at this data scale. SaiVLA-JEPA [15] reports that a training-only future-latent head adds +0.03 points to control on 10,030 paired episodes. HIJP [16] finds LeWM below goal-conditioned behaviour cloning in simulation.

### Limitations (mean 0.257)

<!-- editlens chunk 0.257 lines 114-114 -->
<!-- editlens paragraph 0.257 lines 114-114 -->
The split between encoder and predictor is exploratory. We chose its probes after the data and fit them on 69 rollouts labelled by a single operator, the author. The model never saw these rollouts, and every probe is cross-validated by session. A fresh set of rollouts scored under a threshold committed first would confirm or reject the split. That needs a day on the arm. All results come from one model at one data scale. A second point at 653 episodes is costed and queued. We did not run three controls. The surprise monitor and the imagined arm of the grasp probe would each need a predictor trained on frozen DINOv2-S features or on the joints. Progress monotonicity with the controls would need a reimplementation. In the register, the outcome-readout verdict is retrospective. The two-level hierarchical progress use has its bar in the same commit as its result. Ordered by commit alone, without the audit, the register reads 13 bar-first and 6 same-commit rows.

### Conclusion (mean 0.197)

<!-- editlens chunk 0.197 lines 118-118 -->
<!-- editlens paragraph 0.197 lines 118-118 -->
We tested 20 published uses on a $3.30 world model. At this data scale the encoder reads the outcome and the predictor adds nothing to that reading. In chunk ranking the commanded actions did better than the predictor, so they are worth keeping as a baseline for any model of this size.

### (figure and table captions) (mean 0.161)

<!-- editlens chunk 0.161 lines 33-96 -->
<!-- editlens paragraph 0.173 lines 33-33 -->
Table 1: The register: every use of our world model re-tested here (with the frozen-DINOv2 and RoboJEPA rows beside it), what it takes from the model, whether its bar came before the result, and the verdict. Read the takes column against the verdict: the predictor uses fail. Bar, result and verdict are quoted from repro/register/expected/FEASIBILITY.md §2.

## built PDF

### (front matter) (mean 0.136)

<!-- editlens chunk 0.136 lines 3-8 -->
A small JEPA world model on a low-cost arm: the encoder reads the outcome, the predictor adds nothing to it Ravindu Somawansa∗ Shisso Robotics, Paris ravindu.somawansa@shissorobotics.com

### Abstract (mean 0.158)

<!-- editlens chunk 0.135 lines 10-65 -->
<!-- editlens paragraph 0.086 lines 10-23 -->
We trained a small JEPA world model in the LeWorldModel recipe for $3.30 of rented GPU time. The training data are teleoperated demonstrations of one tabletop task on an SO-101 arm. We then re-tested on this model the uses of such models that recent papers propose. Each use has a threshold in a public register. We tested the encoder on policy rollouts the model never saw. A linear probe on its last-frame latent separates success from failure about as well as a hand-built colour judge. It does better than a frozen DINOv2 encoder and better than the commanded joints. The predictor adds nothing to this. At the grasp, the imagined latent reads the outcome at 0.70 and the current latent at 0.82. Every use that needs the predictor to roll forward misses its threshold at this data scale. The controls are exploratory and come from one rig and one model.

<!-- editlens paragraph 0.220 lines 28-42 -->
LeWorldModel (LeWM) [1] trains a world model in two parts. The encoder maps camera frames to a latent vector. The predictor takes the current latent and a sequence of actions and imagines the latents that follow. Both are trained together from pixels with a joint-embedding predictive (JEPA) loss. Papers built on these models propose several uses. Most of them need the predictor. One ranks a policy’s candidate action chunks by their imagined outcome. Others flag a failure when the observed latent drifts from the predicted one, read the outcome of a grasp before it happens, or plan over several time scales. Each paper reports the use that worked on its own robot and data. We had one such model, trained on our own arm. We ran every use we could find on it. Each re-test is a row of a register with a threshold, a dataset, a result and a verdict. Where we managed it, the threshold and the decision rule went into the repository before the result existed.

<!-- editlens paragraph 0.191 lines 43-65 -->
That commit order is what we mean by pre-registration. All 20 rows match a pre-registration record in the commit history. In 19 of them the bar was in place before the result. The two-level hierarchical progress use had it in the same commit. One more row is not a use of our model. It times the pretrained RoboJEPA [2] and V-JEPA 2.1 [3] encoders on our on-board computer. 14 of the 20 rows fail or are no-go. Table 1 lists all of them. The first version of this paper argued something completely different. We read the failures as a sign that the latent mostly encodes the arm’s pose. Then a frozen image encoder or the commanded joints would do at least as well. We ran these controls on 69 policy rollouts. The encoder read how the episode went better than either control. We modified the claim around the predictor. We come back several times to one moment, the grasp anchor. It is 15 frames before the gripper first closes. There the current latent reads the outcome at 0.82 and the imagined latent at 0.70. The controls came after the data. Each readout is a linear probe with leave-one-session-out (LOSO) crossvalidation on the 69 rollouts (44 success, 25 failure, 13 sessions). The labels were given at rest by the author. The model was trained on teleoperation only and never saw these rollouts. No threshold was committed for these comparisons. Everything this paper says about the split between encoder and predictor is therefore exploratory. 3 of the 3 register passes have their bar committed before the result. The register still marks the outcome-readout verdict as retrospective.

<!-- editlens chunk 0.105 lines 70-124 -->
<!-- editlens paragraph 0.123 lines 70-81 -->
The robot is one SO-101 arm [4] driven through LeRobot [5], with a top and a wrist camera. The task is to put a bowl into another bowl. We trained our model on ravediamond/so101_bowls_all_trimmed, split by grid layout into 157 training and 25 validation episodes. The evaluation rollouts come from a separate dataset, ravediamond/so101-bowls-policy-rollouts. They are SmolVLA [6] runs recorded after our model was trained. ∗ Code, data pointers and every number’s source: https://github. Our model follows the LeWM recipe [1], with a multicom/ravediamond/paper-jepa-world-model. view ViT encoder, an action-conditioned predictor and github.com/ravediamond/paper-jepa-world-model · 43bc65a

<!-- editlens paragraph 0.141 lines 84-99 -->
the SIGReg regulariser. We compare it with four cheaper signals. The frozen DINOv2-S control is a frozen DINOv2 small encoder [7], mean-pooled over the top and wrist views as in DINO-WM [8]. The joints control is the commanded joint vector. The colour judge is a hand-built rule on the final frame with no learning. Policy identity is the checkpoint that ran the episode. In October we found a loading bug. A timing test on the on-board computer loaded our checkpoint with strict=False. The image had transformers 5.5.4, and under that version 192 encoder tensors did not match. They were dropped without an error, so the test timed a random encoder. We voided its latents. We then traced how every other use loaded the model. 26 ran the trained model and 1 ran a random one (that test). The worldmodel block of VLA-JEPA, which one diagnostic below uses, loads all 351 of its keys.

<!-- editlens paragraph 0.207 lines 104-124 -->
Table 1 lists the 20 uses. The takes column says what each one needs from our model: the encoder alone (7), the predictor (8) or both (5). Among the encoder uses, reading the outcome works. The outcome readout at rest passes. At the grasp anchor the current latent reads the grasp at 0.82. Reading progress does not work. Four uses ask the latent for progress or task stage, and all four fail. They are progress monotonicity, two-level hierarchical progress [10], the latent stage tracker and SURVEYOR’s latent-distance scale [13]. We also ran the pose probes of LeJEPA [12]. A linear readout recovers about half of the joint variance from our encoder (R2 0.565). It recovers more from the frozen DINOv2-S control (0.867). The predictor does predict its own latent. At K = 30 its open-loop error is 0.31. Copying the last latent gives 0.89. The uses of this prediction fail. In chunk ranking [1] the model puts the executed chunk first in 0.60 of anchors. The threshold was 0.8. The commanded actions alone reach 0.68–0.90. The surprise monitor catches 2/8 at 2/42 failures. The hierarchical planner [14], the conformal surprise band, re-ranking, the risk head [11] and the calibrated reflex also miss their thresholds. Table 1 gives the margins.

<!-- editlens chunk 0.286 lines 155-187 -->
<!-- editlens paragraph 0.175 lines 155-178 -->
Figure 1: Table 2 as a dot plot. Left: at rest, with the 95 % CI. Right: at the grasp anchor, with the seed range (not a CI). At rest our model is level with the colour judge. The two CIs overlap. Our model is above the frozen encoder and the joints. At the grasp anchor no judge applies, and our model is above both controls. The pose probes hold the joints better than our encoder does. They hold the outcome worse. On these rollouts the encoder has outcome information that the pose alone does not give. The anchor column depends on how the five seeds are combined. If we average the predictions before scoring, our model gets 0.8377, frozen DINOv2-S 0.7175 and the joints 0.5346. With seed 0 alone they get 0.7554, 0.7024 and 0.5574. The gap to the frozen encoder is smaller with seed 0. The order is the same. On SURVEYOR’s scale check the controls do better than our model. Frozen DINOv2-S has τ 0.3601 and the joints τ 0.0265, and both pass. Our model has τ 1.2488 and fails. SURVEYOR reports 0.20. The task and the rollouts are the same for all three features. We take the failure as a property of our latent space. The register’s own outcome-readout row reports 1.000. That number was scored against the colour judge’s labels on 87 rollouts. Scored against the author’s labels on the 69 rollouts, the same readout gives 0.9545.

<!-- editlens paragraph 0.184 lines 183-187 -->
ContactGuard [9] finds that probes on the imagined latent beat probes on the current latent for grasp tasks. We expected the same at our grasp anchor. The preregistered threshold asked the imagined latent for ≥ 0.85, ≥ +0.05 over the current one. We find the reverse. With the same encoder and the same anchor, the current latent

### 4 What the encoder knows (mean 0.107)

<!-- editlens chunk 0.045 lines 188-599 -->
<!-- editlens paragraph 0.070 lines 188-200 -->
reads the outcome at 0.82 and the imagined latent at 0.70. The row fails. We tested whether the encoder carries anything that a We also ran the distillation probe on our model’s frozen encoder or the joints do not. Table 2 sets our model inverse-dynamics term, pooled over the 25 teleoperation beside the four other signals on the same 69 rollouts. Ev- validation episodes. The trained model scores 0.7476. ery probe is a LOSO linear probe against the author’s la- Its random initialisation scores 0.7974. The difference bels. At rest the interval is a 95 % episode-bootstrap CI. is −0.0499, with a 95 % paired episode-bootstrap CI At the anchor it is a bootstrap of the mean over 5 seeds of of [−0.7403, +0.6559] (gap5_pooled_rerun.json). The the out-of-fold AUROC, with episodes resampled jointly term depends on the machine. The same untrained netacross the seeds (2,000 resamples, percentile). work scored 1.4383 on one machine and 0.7974 and 0.8042 github.com/ravediamond/paper-jepa-world-model · 43bc65a

<!-- editlens paragraph 0.159 lines 203-207 -->
Table 1: The register: every use of our world model re-tested here (with the frozen-DINOv2 and RoboJEPA rows beside it), what it takes from the model, whether its bar came before the result, and the verdict. Read the takes column against the verdict: the predictor uses fail. Bar, result and verdict are quoted from repro/register/expected/FEASIBILITY.md §2. use

<!-- editlens paragraph 0.140 lines 571-599 -->
scoring bug. The same scorer reproduces the open-loop Table 2: Outcome AUROC of each signal on the same 69 corruption ratios at K = 30 (M1_diag_g0_repro.json). rollouts (exploratory: controls chosen after the data). No Cross-episode gives 3.428, against 3.341 in the original judge applies at the anchor. run. Constant-first gives 2.558, against 2.543. We found feature at rest grasp anchor (65 scored, 21 fail) no bug. our world model 0.9545 [0.9023, 0.9908] 0.8199 [0.7141, 0.9041] colour judge (no learning) 0.9432 [0.8919, 0.9878] — We ran an action-shuffle check on the prefrozen DINOv2-S 0.8655 [0.7767, 0.9405] 0.7067 [0.5816, 0.8269] dictor of VLA-JEPA at 5 anchors (Table 3, from commanded joints 0.7573 [0.6084, 0.8880] 0.5305 [0.3709, 0.6855] policy identity 0.5882 [0.4084, 0.7515] — M3_diag_action_shuffle.json). Action tokens from another episode differ from the true ones by 21–28 % in relative L2. They move the loss by about 0.05 %. Zeroing on two others. It is sensitive to the BLAS library and to the tokens moves it by about 1.05 % on average. The ridge conditioning. forward pass is deterministic. The predictor barely uses The surprise monitor has a failure-class AUROC of its actions. Its failure-class AUROC is 0.501, below the 0.775, below its sanity bar. We checked it for a loading or same sanity check, and we leave its table unread under github.com/ravediamond/paper-jepa-world-model · 43bc65a

<!-- editlens chunk 0.168 lines 602-694 -->
<!-- editlens paragraph 0.123 lines 602-613 -->
is retrospective. The two-level hierarchical progress use Table 3: VLA-JEPA world-model loss at 5 anchors with has its bar in the same commit as its result. Ordered by true, shuffled (Δ shuffled) and zeroed action tokens (ex- commit alone, without the audit, the register reads 13 ploratory spot check). The token change is the relative bar-first and 6 same-commit rows. L2 of the shuffled tokens. anchor (episode / frame) true loss Δ shuffled (%) token change (%) Δ zeroed (%) 8 / 402 10 / 227 23 / 327 59 / 302 65 / 302

<!-- editlens paragraph 0.291 lines 638-645 -->
the frozen bar. One pass in the register uses the imagined latent. In the anticipation step of the outcome-readout gate, the imagined latent beat policy identity by +0.179. That bar is retrospective. We reran the same idea twice with the threshold committed first, in the grasp probe and in the calibrated surprise reflex. Both fail.

<!-- editlens paragraph 0.262 lines 650-666 -->
LeWorldModel [1] trains the recipe we use end to end from pixels and plans with it in Push-T and in simulation. We tested its two planning uses on our arm, and both fail. LeJEPA’s identifiability analysis [12] predicts that SIGReg latents identify the state up to anisotropy. Our pose probes support this in part. DINO-WM [8] plans on frozen DINOv2 [7] patches, and our frozen control uses the same design. We timed V-JEPA 2.1 [3] and RoboJEPA [2] on our on-board computer, and both are too slow. ContactGuard [9] finds imagined-latent probes better than current-latent ones on grasp tasks. On our arm we find the reverse. We also re-tested ReAP’s action-conditioned risk [11], the hierarchical planners of HWM [14] and H-JEPA [10], and SURVEYOR’s latentdistance scale [13]. All of them miss here, at this data scale. SaiVLA-JEPA [15] reports that a training-only future-latent head adds +0.03 points to control on 10,030 paired episodes. HIJP [16] finds LeWM below goalconditioned behaviour cloning in simulation.

<!-- editlens paragraph 0.254 lines 671-683 -->
The split between encoder and predictor is exploratory. We chose its probes after the data and fit them on 69 rollouts labelled by a single operator, the author. The model never saw these rollouts, and every probe is crossvalidated by session. A fresh set of rollouts scored under a threshold committed first would confirm or reject the split. That needs a day on the arm. All results come from one model at one data scale. A second point at 653 episodes is costed and queued. We did not run three controls. The surprise monitor and the imagined arm of the grasp probe would each need a predictor trained on frozen DINOv2-S features or on the joints. Progress monotonicity with the controls would need a reimplementation. In the register, the outcome-readout verdict github.com/ravediamond/paper-jepa-world-model · 43bc65a

<!-- editlens paragraph 0.197 lines 688-694 -->
We tested 20 published uses on a $3.30 world model. At this data scale the encoder reads the outcome and the predictor adds nothing to that reading. In chunk ranking the commanded actions did better than the predictor, so they are worth keeping as a baseline for any model of this size.
