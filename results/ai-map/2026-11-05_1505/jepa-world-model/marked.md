# paper-jepa-world-model: chunks in paper order

## rendered source (numbers filled)

### Abstract (mean 0.131)

<!-- editlens chunk 0.131 lines 7-7 -->
<!-- editlens paragraph 0.131 lines 7-7 -->
We trained a small JEPA world model in the LeWorldModel recipe for $3.30 of rented GPU time, on teleoperated demonstrations of one tabletop task on an SO-101 arm. On this model we then re-tested the uses of such models that recent papers propose, each with a threshold written into a public register. On policy rollouts the model never saw, a linear probe on the encoder's last-frame latent separates success from failure about as well as a hand-built colour judge, and better than a frozen DINOv2 encoder or the commanded joints. The predictor adds nothing to this. At the grasp the imagined latent reads the outcome at 0.70 and the current latent at 0.82, and every use that needs the predictor to roll forward misses its threshold at this data scale. The controls are exploratory and come from one rig and one model.

### Introduction (mean 0.149)

<!-- editlens chunk 0.149 lines 11-19 -->
<!-- editlens paragraph 0.220 lines 11-11 -->
LeWorldModel (LeWM) [1] trains a world model in two parts. The encoder maps camera frames to a latent vector, and the predictor takes the current latent and a sequence of actions and imagines the latents that follow. Both are trained together from pixels with a joint-embedding predictive (JEPA) loss. Most of the uses proposed for these models need the predictor. One ranks a policy's candidate action chunks by their imagined outcome, and others flag a failure when the observed latent drifts from the predicted one, read the outcome of a grasp before it happens, or plan over several time scales. Each paper reports the use that worked on its own robot and data.

<!-- editlens paragraph 0.100 lines 13-13 -->
We had one such model, trained on our own arm, and ran every use we could find on it. Each re-test is a row of a register with a threshold, a dataset, a result and a verdict. Where we managed it, the threshold and the decision rule went into the repository before the result existed, which is all we mean by pre-registration. All 20 rows match a pre-registration record in the commit history. In 19 of them the bar was in place before the result, and the two-level hierarchical progress use had it in the same commit. One more row is not a use of our model, since it times the pretrained RoboJEPA [2] and V-JEPA 2.1 [3] encoders on our on-board computer. 14 of the 20 rows fail or are no-go (Table 1).

<!-- editlens paragraph 0.319 lines 15-15 -->
The first draft of this paper argued something else. We had read the failures as a sign that the latent mostly encodes the arm's pose, in which case a frozen image encoder or the commanded joints would do at least as well in each use. Before writing it up we ran these controls on 69 policy rollouts, and the encoder read how the episode went better than either of them. We rewrote the claim around the predictor.

<!-- editlens paragraph 0.289 lines 19-19 -->
The controls came after the data. Each readout is a linear probe with leave-one-session-out (LOSO) cross-validation on the 69 rollouts (44 success, 25 failure, 13 sessions), scored against labels the author gave at rest. The model was trained on teleoperation only and never saw these rollouts. Because no threshold was committed for these comparisons, everything this paper says about the split between encoder and predictor is exploratory. 3 of the 3 register passes have their bar committed before the result, and the register still marks the outcome-readout verdict as retrospective.

### Setup (mean 0.061)

<!-- editlens chunk 0.061 lines 23-27 -->
<!-- editlens paragraph 0.057 lines 23-23 -->
The robot is one SO-101 arm [4] driven through LeRobot [5], with a top and a wrist camera, and the task is to put a bowl into another bowl. We trained our model on X, split by grid layout into 157 training and 25 validation episodes. The evaluation rollouts come from a separate dataset, X, which holds SmolVLA [6] runs recorded after our model was trained.

<!-- editlens paragraph 0.079 lines 25-25 -->
Our model follows the LeWM recipe [1], with a multi-view ViT encoder, an action-conditioned predictor and the SIGReg regulariser. We compare it with four cheaper signals. The frozen DINOv2-S control is a frozen DINOv2 small encoder [7], mean-pooled over the top and wrist views as in DINO-WM [8], and the joints control is the commanded joint vector. The colour judge is a hand-built rule on the final frame with no learning. Policy identity is the checkpoint that ran the episode.

<!-- editlens paragraph 0.250 lines 27-27 -->
In October we found a loading bug. A timing test on the on-board computer loaded our checkpoint with X, and under the transformers version on that image (5.5.4) 192 encoder tensors did not match and were dropped without an error, so the test timed a random encoder. We voided its latents and traced how every other use loaded the model: 26 ran the trained model and 1 ran a random one (that test). The world-model block of VLA-JEPA, which one diagnostic below uses, loads all 351 of its keys.

### The register (mean 0.224)

<!-- editlens chunk 0.224 lines 31-60 -->
<!-- editlens paragraph 0.250 lines 58-58 -->
Among the encoder uses, reading the outcome works. The outcome readout at rest passes, and at the grasp anchor the current latent reads the grasp at 0.82. Reading progress does not work. Four uses ask the latent for progress or task stage (progress monotonicity, two-level hierarchical progress [10], the latent stage tracker and SURVEYOR's latent-distance scale [13]), and all four fail. We also ran the pose probes of LeJEPA [12], where a linear readout recovers about half of the joint variance from our encoder (R² 0.565) and more from the frozen DINOv2-S control (0.867).

<!-- editlens paragraph 0.308 lines 60-60 -->
The predictor does predict its own latent: at K = 30 its open-loop error is 0.31, against 0.89 for copying the last latent. The uses of this prediction fail. In chunk ranking [1] the model puts the executed chunk first in 0.60 of anchors, below the threshold of 0.8, while the commanded actions alone reach 0.68–0.90. The surprise monitor catches 2/8 at 2/42 failures. The hierarchical planner [14], the conformal surprise band, re-ranking, the risk head [11] and the calibrated reflex also miss their thresholds, by the margins in Table 1.

### What the encoder knows (mean 0.115)

<!-- editlens chunk 0.115 lines 64-84 -->
<!-- editlens paragraph 0.074 lines 64-64 -->
We tested whether the encoder carries anything that a frozen encoder or the joints do not, by setting our model beside the four other signals on the same 69 rollouts (Table 2). Every probe is a LOSO linear probe against the author's labels. At rest the interval is a 95 % episode-bootstrap CI, and at the anchor it is a bootstrap of the mean over 5 seeds of the out-of-fold AUROC, with episodes resampled jointly across the seeds (2,000 resamples, percentile).

<!-- editlens paragraph 0.224 lines 78-78 -->
At rest our model is level with the colour judge, whose CI overlaps its own, and above the frozen encoder and the joints. At the grasp anchor no judge applies, and our model is above both controls. The pose probes hold the joints better than our encoder does and the outcome worse, so on these rollouts the encoder has outcome information that the pose alone does not give.

<!-- editlens paragraph 0.138 lines 80-80 -->
The anchor column depends on how the five seeds are combined. If we average the predictions before scoring, our model gets 0.8377, frozen DINOv2-S 0.7175 and the joints 0.5346. Seed 0 alone gives 0.7554, 0.7024 and 0.5574, with a smaller gap to the frozen encoder. The order is the same.

<!-- editlens paragraph 0.182 lines 82-82 -->
On SURVEYOR's scale check the controls do better than our model. Frozen DINOv2-S (τ 0.3601) and the joints (τ 0.0265) pass, and our model fails with τ 1.2488, where SURVEYOR reports 0.20. The task and the rollouts are the same for all three features, so we take the failure as a property of our latent space.

### Where the predictor fails (mean 0.184)

<!-- editlens chunk 0.184 lines 88-106 -->
<!-- editlens paragraph 0.262 lines 88-88 -->
ContactGuard [9] finds that probes on the imagined latent beat probes on the current latent for grasp tasks, and we expected the same at our grasp anchor. The pre-registered threshold asked the imagined latent for ≥ 0.85, ≥ +0.05 over the current one. We find the reverse. With the same encoder and the same anchor, the current latent reads the outcome at 0.82 and the imagined latent at 0.70, so the row fails.

<!-- editlens paragraph 0.123 lines 90-90 -->
We also ran the distillation probe on our model's inverse-dynamics term, pooled over the 25 teleoperation validation episodes. The trained model scores 0.7476 and its random initialisation 0.7974, a difference of −0.0499 with a 95 % paired episode-bootstrap CI of [−0.7403, +0.6559] (X). The term also depends on the machine. The same untrained network scored 1.4383 on one machine and 0.7974 and 0.8042 on two others, because it is sensitive to the BLAS library and to ridge conditioning.

<!-- editlens paragraph 0.187 lines 92-92 -->
The surprise monitor has a failure-class AUROC of 0.775, below its sanity bar, so we checked it for a loading or scoring bug. The same scorer reproduces the open-loop corruption ratios at K = 30 (X): cross-episode gives 3.428 against 3.341 in the original run, and constant-first 2.558 against 2.543. We found no bug.

<!-- editlens paragraph 0.214 lines 94-94 -->
We ran an action-shuffle check on the predictor of VLA-JEPA at 5 anchors (Table 3, from X). Action tokens from another episode differ from the true ones by 21–28 % in relative L2, yet they move the loss by about 0.05 %, and zeroing the tokens moves it by about 1.05 % on average. The forward pass is deterministic. The predictor barely uses its actions, and with a failure-class AUROC of 0.501, below the same sanity check, we leave its table unread under the frozen bar.

<!-- editlens paragraph 0.409 lines 106-106 -->
One pass in the register uses the imagined latent: in the anticipation step of the outcome-readout gate, it beat policy identity by +0.179. That bar is retrospective. We reran the same idea twice with the threshold committed first, in the grasp probe and in the calibrated surprise reflex, and both fail.

### Related work (mean 0.304)

<!-- editlens chunk 0.304 lines 110-110 -->
<!-- editlens paragraph 0.304 lines 110-110 -->
LeWorldModel [1] trains the recipe we use end to end from pixels and plans with it in Push-T and in simulation. We tested its two planning uses on our arm, and both fail. LeJEPA's identifiability analysis [12] predicts that SIGReg latents identify the state up to anisotropy, which our pose probes support in part. DINO-WM [8] plans on frozen DINOv2 [7] patches, and our frozen control uses the same design. We timed V-JEPA 2.1 [3] and RoboJEPA [2] on our on-board computer, and both are too slow. ContactGuard [9] finds imagined-latent probes better than current-latent ones on grasp tasks, and on our arm we find the reverse. ReAP's action-conditioned risk [11], the hierarchical planners of HWM [14] and H-JEPA [10], and SURVEYOR's latent-distance scale [13] also miss here, at this data scale. SaiVLA-JEPA [15] reports that a training-only future-latent head adds +0.03 points to control on 10,030 paired episodes, and HIJP [16] finds LeWM below goal-conditioned behaviour cloning in simulation.

### Limitations (mean 0.263)

<!-- editlens chunk 0.263 lines 114-114 -->
<!-- editlens paragraph 0.263 lines 114-114 -->
The split between encoder and predictor is exploratory. We chose its probes after the data and fit them on 69 rollouts labelled by a single operator, the author. The model never saw these rollouts, and every probe is cross-validated by session. A fresh set of rollouts scored under a threshold committed first would confirm or reject the split, and that needs a day on the arm. All results come from one model at one data scale, and a second point at 653 episodes is costed and queued. We did not run three controls, because the surprise monitor and the imagined arm of the grasp probe would each need a predictor trained on frozen DINOv2-S features or on the joints, and progress monotonicity with the controls would need a reimplementation. In the register the outcome-readout verdict is retrospective, and the two-level hierarchical progress use has its bar in the same commit as its result. Ordered by commit alone, without the audit, the register reads 13 bar-first and 6 same-commit rows.

### Conclusion (mean 0.221)

<!-- editlens chunk 0.221 lines 118-118 -->
<!-- editlens paragraph 0.221 lines 118-118 -->
We tested 20 published uses on a $3.30 world model. At this data scale the encoder reads the outcome, and the predictor adds nothing to that reading. In chunk ranking the commanded actions did better than the predictor, so they are worth keeping as a baseline for any model of this size.

### (figure and table captions) (mean 0.161)

<!-- editlens chunk 0.161 lines 33-96 -->
<!-- editlens paragraph 0.173 lines 33-33 -->
Table 1: The register: every use of our world model re-tested here (with the frozen-DINOv2 and RoboJEPA rows beside it), what it takes from the model, whether its bar came before the result, and the verdict. Read the takes column against the verdict: the predictor uses fail. Bar, result and verdict are quoted from repro/register/expected/FEASIBILITY.md §2.

## built PDF

### (front matter) (mean 0.136)

<!-- editlens chunk 0.136 lines 3-8 -->
A small JEPA world model on a low-cost arm: the encoder reads the outcome, the predictor adds nothing to it Ravindu Somawansa∗ Shisso Robotics, Paris ravindu.somawansa@shissorobotics.com

### Abstract (mean 0.109)

<!-- editlens chunk 0.097 lines 10-61 -->
<!-- editlens paragraph 0.135 lines 10-20 -->
We trained a small JEPA world model in the LeWorldModel recipe for $3.30 of rented GPU time, on teleoperated demonstrations of one tabletop task on an SO-101 arm. On this model we then re-tested the uses of such models that recent papers propose, each with a threshold written into a public register. On policy rollouts the model never saw, a linear probe on the encoder’s lastframe latent separates success from failure about as well as a hand-built colour judge, and better than a frozen DINOv2 encoder or the commanded joints. The predictor adds nothing to this. At the grasp the imagined latent reads the outcome at 0.70 and the current latent at 0.82, and every use that needs the predictor to roll forward misses its threshold at this data scale. The controls are exploratory and come from one rig and one model.

<!-- editlens paragraph 0.084 lines 25-37 -->
LeWorldModel (LeWM) [1] trains a world model in two parts. The encoder maps camera frames to a latent vector, and the predictor takes the current latent and a sequence of actions and imagines the latents that follow. Both are trained together from pixels with a joint-embedding predictive (JEPA) loss. Most of the uses proposed for these models need the predictor. One ranks a policy’s candidate action chunks by their imagined outcome, and others flag a failure when the observed latent drifts from the predicted one, read the outcome of a grasp before it happens, or plan over several time scales. Each paper reports the use that worked on its own robot and data. We had one such model, trained on our own arm, and ran every use we could find on it. Each re-test is a row of a register with a threshold, a dataset, a result and a verdict. Where we managed it, the threshold and the decision rule went into the repository before the result existed, which is all we mean by pre-registration. All 20

<!-- editlens paragraph 0.167 lines 38-61 -->
rows match a pre-registration record in the commit history. In 19 of them the bar was in place before the result, and the two-level hierarchical progress use had it in the same commit. One more row is not a use of our model, since it times the pretrained RoboJEPA [2] and V-JEPA 2.1 [3] encoders on our on-board computer. 14 of the 20 rows fail or are no-go (Table 1). The first draft of this paper argued something else. We had read the failures as a sign that the latent mostly encodes the arm’s pose, in which case a frozen image encoder or the commanded joints would do at least as well in each use. Before writing it up we ran these controls on 69 policy rollouts, and the encoder read how the episode went better than either of them. We rewrote the claim around the predictor. We come back several times to one moment, the grasp anchor, 15 frames before the gripper first closes. There the current latent reads the outcome at 0.82 and the imagined latent at 0.70. The controls came after the data. Each readout is a linear probe with leave-one-session-out (LOSO) crossvalidation on the 69 rollouts (44 success, 25 failure, 13 sessions), scored against labels the author gave at rest. The model was trained on teleoperation only and never saw these rollouts. Because no threshold was committed for these comparisons, everything this paper says about the split between encoder and predictor is exploratory. 3 of the 3 register passes have their bar committed before the result, and the register still marks the outcomereadout verdict as retrospective.

<!-- editlens chunk 0.092 lines 66-157 -->
<!-- editlens paragraph 0.079 lines 66-77 -->
The robot is one SO-101 arm [4] driven through LeRobot [5], with a top and a wrist camera, and the task is to put a bowl into another bowl. We trained our model on ravediamond/so101_bowls_all_trimmed, split by grid layout into 157 training and 25 validation episodes. The evaluation rollouts come from a separate dataset, ravediamond/so101-bowls-policy-rollouts, which holds SmolVLA [6] runs recorded after our model was trained. ∗ Code, data pointers and every number’s source: https://github. com/ravediamond/paper-jepa-world-model. Our model follows the LeWM recipe [1], with a multigithub.com/ravediamond/paper-jepa-world-model · c05ab4d

<!-- editlens paragraph 0.113 lines 80-95 -->
view ViT encoder, an action-conditioned predictor and the SIGReg regulariser. We compare it with four cheaper signals. The frozen DINOv2-S control is a frozen DINOv2 small encoder [7], mean-pooled over the top and wrist views as in DINO-WM [8], and the joints control is the commanded joint vector. The colour judge is a hand-built rule on the final frame with no learning. Policy identity is the checkpoint that ran the episode. In October we found a loading bug. A timing test on the on-board computer loaded our checkpoint with strict=False, and under the transformers version on that image (5.5.4) 192 encoder tensors did not match and were dropped without an error, so the test timed a random encoder. We voided its latents and traced how every other use loaded the model: 26 ran the trained model and 1 ran a random one (that test). The world-model block of VLA-JEPA, which one diagnostic below uses, loads all 351 of its keys.

<!-- editlens paragraph 0.162 lines 130-157 -->
Figure 1: Table 2 as a dot plot. Left: at rest, with the 95 % CI. Right: at the grasp anchor, with the seed range (not a CI). with episodes resampled jointly across the seeds (2,000 resamples, percentile). At rest our model is level with the colour judge, whose CI overlaps its own, and above the frozen encoder and the joints. At the grasp anchor no judge applies, and our model is above both controls. The pose probes hold the joints better than our encoder does and the outcome worse, so on these rollouts the encoder has outcome information that the pose alone does not give. The anchor column depends on how the five seeds are combined. If we average the predictions before scoring, our model gets 0.8377, frozen DINOv2-S 0.7175 and the joints 0.5346. Seed 0 alone gives 0.7554, 0.7024 and 0.5574, with a smaller gap to the frozen encoder. The order is the same. On SURVEYOR’s scale check the controls do better than our model. Frozen DINOv2-S (τ 0.3601) and the joints (τ 0.0265) pass, and our model fails with τ 1.2488, where SURVEYOR reports 0.20. The task and the rollouts are the same for all three features, so we take the failure as a property of our latent space. The register’s own outcome-readout row reports 1.000, but that number was scored against the colour judge’s labels on 87 rollouts. Against the author’s labels on the 69 rollouts, the same readout gives 0.9545.

<!-- editlens chunk 0.167 lines 158-177 -->
<!-- editlens paragraph 0.167 lines 158-177 -->
Table 1 lists the 20 uses. The takes column says what each one needs from our model: the encoder alone (7), the predictor (8) or both (5). Among the encoder uses, reading the outcome works. The outcome readout at rest passes, and at the grasp anchor the current latent reads the grasp at 0.82. Reading progress does not work. Four uses ask the latent for progress or task stage (progress monotonicity, twolevel hierarchical progress [10], the latent stage tracker and SURVEYOR’s latent-distance scale [13]), and all four fail. We also ran the pose probes of LeJEPA [12], where a linear readout recovers about half of the joint variance from our encoder (R2 0.565) and more from the frozen DINOv2-S control (0.867). The predictor does predict its own latent: at K = 30 its open-loop error is 0.31, against 0.89 for copying the last latent. The uses of this prediction fail. In chunk ranking [1] the model puts the executed chunk first in 0.60 of anchors, below the threshold of 0.8, while the commanded actions alone reach 0.68–0.90. The surprise mon- 5 Where the predictor fails itor catches 2/8 at 2/42 failures. The hierarchical planner [14], the conformal surprise band, re-ranking, the ContactGuard [9] finds that probes on the imagined larisk head [11] and the calibrated reflex also miss their tent beat probes on the current latent for grasp tasks, thresholds, by the margins in Table 1. and we expected the same at our grasp anchor. The preregistered threshold asked the imagined latent for ≥ 0.85, ≥ +0.05 over the current one. We find the reverse. With

### 4 What the encoder knows (mean 0.146)

<!-- editlens chunk 0.050 lines 178-631 -->
<!-- editlens paragraph 0.061 lines 178-188 -->
the same encoder and the same anchor, the current latent reads the outcome at 0.82 and the imagined latent at 0.70, We tested whether the encoder carries anything that so the row fails. a frozen encoder or the joints do not, by setting our We also ran the distillation probe on our model’s model beside the four other signals on the same 69 roll- inverse-dynamics term, pooled over the 25 teleoperation outs (Table 2). Every probe is a LOSO linear probe validation episodes. The trained model scores 0.7476 and against the author’s labels. At rest the interval is a 95 its random initialisation 0.7974, a difference of −0.0499 % episode-bootstrap CI, and at the anchor it is a boot- with a 95 % paired episode-bootstrap CI of [−0.7403, strap of the mean over 5 seeds of the out-of-fold AUROC, +0.6559] (gap5_pooled_rerun.json). The term also degithub.com/ravediamond/paper-jepa-world-model · c05ab4d

<!-- editlens paragraph 0.159 lines 191-195 -->
Table 1: The register: every use of our world model re-tested here (with the frozen-DINOv2 and RoboJEPA rows beside it), what it takes from the model, whether its bar came before the result, and the verdict. Read the takes column against the verdict: the predictor uses fail. Bar, result and verdict are quoted from repro/register/expected/FEASIBILITY.md §2. use

<!-- editlens paragraph 0.124 lines 559-586 -->
The surprise monitor has a failure-class AUROC Table 2: Outcome AUROC of each signal on the same 69 of 0.775, below its sanity bar, so we checked it for rollouts (exploratory: controls chosen after the data). No a loading or scoring bug. The same scorer reprojudge applies at the anchor. duces the open-loop corruption ratios at K = 30 feature at rest grasp anchor (65 scored, 21 fail) (M1_diag_g0_repro.json): cross-episode gives 3.428 our world model 0.9545 [0.9023, 0.9908] 0.8199 [0.7141, 0.9041] against 3.341 in the original run, and constant-first 2.558 colour judge (no learning) 0.9432 [0.8919, 0.9878] — frozen DINOv2-S 0.8655 [0.7767, 0.9405] 0.7067 [0.5816, 0.8269] against 2.543. We found no bug. commanded joints 0.7573 [0.6084, 0.8880] 0.5305 [0.3709, 0.6855] policy identity 0.5882 [0.4084, 0.7515] — We ran an action-shuffle check on the predictor of VLA-JEPA at 5 anchors (Table 3, from M3_diag_action_shuffle.json). Action tokens from pends on the machine. The same untrained network another episode differ from the true ones by 21–28 % in scored 1.4383 on one machine and 0.7974 and 0.8042 on relative L2, yet they move the loss by about 0.05 %, and two others, because it is sensitive to the BLAS library and zeroing the tokens moves it by about 1.05 % on average. to ridge conditioning. The forward pass is deterministic. The predictor barely github.com/ravediamond/paper-jepa-world-model · c05ab4d

<!-- editlens paragraph 0.344 lines 623-631 -->
uses its actions, and with a failure-class AUROC of 0.501, below the same sanity check, we leave its table unread under the frozen bar. One pass in the register uses the imagined latent: in the anticipation step of the outcome-readout gate, it beat policy identity by +0.179. That bar is retrospective. We reran the same idea twice with the threshold committed first, in the grasp probe and in the calibrated surprise reflex, and both fail.

<!-- editlens chunk 0.280 lines 636-686 -->
<!-- editlens paragraph 0.343 lines 636-651 -->
LeWorldModel [1] trains the recipe we use end to end from pixels and plans with it in Push-T and in simulation. We tested its two planning uses on our arm, and both fail. LeJEPA’s identifiability analysis [12] predicts that SIGReg latents identify the state up to anisotropy, which our pose probes support in part. DINO-WM [8] plans on frozen DINOv2 [7] patches, and our frozen control uses the same design. We timed V-JEPA 2.1 [3] and RoboJEPA [2] on our on-board computer, and both are too slow. ContactGuard [9] finds imagined-latent probes better than current-latent ones on grasp tasks, and on our arm we find the reverse. ReAP’s action-conditioned risk [11], the hierarchical planners of HWM [14] and HJEPA [10], and SURVEYOR’s latent-distance scale [13] also miss here, at this data scale. SaiVLA-JEPA [15] reports that a training-only future-latent head adds +0.03 points to control on 10,030 paired episodes, and HIJP [16] finds LeWM below goal-conditioned behaviour cloning in simulation.

<!-- editlens paragraph 0.217 lines 656-668 -->
The split between encoder and predictor is exploratory. We chose its probes after the data and fit them on 69 rollouts labelled by a single operator, the author. The model never saw these rollouts, and every probe is crossvalidated by session. A fresh set of rollouts scored under a threshold committed first would confirm or reject the split, and that needs a day on the arm. All results come from one model at one data scale, and a second point at 653 episodes is costed and queued. We did not run three controls, because the surprise monitor and the imagined arm of the grasp probe would each need a predictor trained on frozen DINOv2-S features or on the joints, and github.com/ravediamond/paper-jepa-world-model · c05ab4d

<!-- editlens paragraph 0.187 lines 669-675 -->
progress monotonicity with the controls would need a reimplementation. In the register the outcome-readout verdict is retrospective, and the two-level hierarchical progress use has its bar in the same commit as its result. Ordered by commit alone, without the audit, the register reads 13 bar-first and 6 same-commit rows.

<!-- editlens paragraph 0.221 lines 680-686 -->
We tested 20 published uses on a $3.30 world model. At this data scale the encoder reads the outcome, and the predictor adds nothing to that reading. In chunk ranking the commanded actions did better than the predictor, so they are worth keeping as a baseline for any model of this size.
