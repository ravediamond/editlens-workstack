# paper-jepa-world-model: chunks in paper order

## rendered source (numbers filled)

### Abstract (mean 0.091)

<!-- editlens chunk 0.091 lines 7-7 -->
<!-- editlens paragraph 0.091 lines 7-7 -->
We trained a small JEPA world model in the LeWorldModel recipe on 182 teleoperated demonstrations of one tabletop task on an SO-101 arm, for $3.30 of rented GPU time. We then took every use of such a model that we found in recent world-model papers and re-tested it on ours, each against a bar written into a public register. Every use that needs a multi-step rollout of the predictor misses its bar, among them chunk ranking, surprise monitoring and risk prediction. The encoder does better. In exploratory probes on policy rollouts the model never saw in training, a linear readout of the last-frame latent separates success from failure about as well as a hand-built colour judge (AUROC 0.95 against 0.94), and better than a frozen DINOv2 encoder, the commanded joints or the identity of the policy. At the grasp, the imagined latent reads the outcome worse than the current one does (0.70 against 0.82). All of it comes from one rig, one model and one data scale.

### Introduction (mean 0.195)

<!-- editlens chunk 0.195 lines 11-17 -->
<!-- editlens paragraph 0.163 lines 11-11 -->
A world model in the sense of LeWorldModel (LeWM) [1] has two parts. The encoder maps camera frames to a latent vector. The predictor takes the current latent and a sequence of actions and imagines the latents that follow. Both are trained together from pixels with a joint-embedding predictive (JEPA) loss. Papers built on such models propose uses for them: ranking a policy's candidate action chunks by their imagined outcome, flagging a failure when the observed latent drifts from the predicted one, reading the outcome of a grasp before it happens, planning over several time scales. Each paper reports the use that worked, on its own robot and data.

<!-- editlens paragraph 0.108 lines 13-13 -->
We had one such model, trained on our own arm, and wanted to know which of these uses we could build on. So we ran every use we could find on that one model. Each re-test is a row of a register with a bar, a dataset, a result and a verdict, and where we managed it, the bar and the decision rule went into the repository before the result existed. That commit order is all we mean by pre-registration. Checked against the commit history, all 20 rows match a pre-registration record. In 19 the bar was committed before the result, and in 1 (the two-level hierarchical progress use) in the same commit. One row is not a use of our model: it times the pretrained RoboJEPA and V-JEPA 2.1 encoders on our on-board computer [2, 3]. Of the 20 rows, 3 pass and 1 is met as predicted. Another 2 are not proven, and the remaining 14 fail or are no-go.

<!-- editlens paragraph 0.361 lines 15-15 -->
Our first reading of the failures was that the latent mostly encodes the arm's pose, so a frozen image encoder or the commanded joints would do at least as well in each of them. We ran those controls on 69 policy rollouts, and they did not bear it out. The encoder reads how the episode went from the current frame better than either control, and it still does at the grasp anchor, 15 frames before the gripper first closes. The predictor, which every forecasting use relies on, does not improve that reading by imagining forward. We changed the claim of the paper to match: at this data scale the predictor, not the encoder, is the weak link.

<!-- editlens paragraph 0.321 lines 17-17 -->
The controls came after the data, and that limits what they can show. Each readout is a linear probe fit with leave-one-session-out (LOSO) cross-validation on the 69 rollouts (44 success, 25 failure, 13 sessions) and scored against the operator's labels. The model was trained on teleoperation only and never saw these rollouts. No bar was committed for these comparisons, so everything this paper says about the split between encoder and predictor is exploratory. Of the 3 register passes, 3 have their bar committed before the result, though the register marks the outcome-readout verdict as retrospective. Without the audit, ordering by commit alone gives 13 bar-first and 6 same-commit rows.

### Setup (mean 0.132)

<!-- editlens chunk 0.132 lines 21-25 -->
<!-- editlens paragraph 0.051 lines 21-21 -->
The robot is one SO-101 arm [4] driven through LeRobot [5], with a top and a wrist camera. The task is to put a bowl into another bowl. Our model is trained on X, split by grid layout into 157 training and 25 validation episodes. The evaluation rollouts come from a separate dataset, X: SmolVLA [6] runs recorded after our model was trained.

<!-- editlens paragraph 0.090 lines 23-23 -->
Our model follows the LeWM recipe [1], with a multi-view ViT encoder, an action-conditioned predictor and the SIGReg regulariser, and was trained on one rented GPU. We compare it with four signals. The frozen DINOv2-S control is a frozen DINOv2 small encoder [7] mean-pooled over the top and wrist views, the design of DINO-WM [8]. The joints control is the commanded joint vector. The colour judge is a hand-built rule on the final frame with no learning, and policy identity is the checkpoint that ran the episode.

<!-- editlens paragraph 0.308 lines 25-25 -->
In October, a timing test on the on-board computer loaded our checkpoint with X. Under the transformers version on that image (5.5.4), 192 encoder tensors did not match and were silently dropped, so the test timed a random encoder. We voided its latents and traced how every other use loaded the model: 26 ran the trained model, 1 ran a random one (that test) and none is unknown. The world-model block of VLA-JEPA, which one diagnostic below uses, loads all 351 of its keys.

### The register (mean 0.233)

<!-- editlens chunk 0.233 lines 29-58 -->
<!-- editlens paragraph 0.270 lines 56-56 -->
Among the encoder uses, reading the outcome works and reading progress does not. The outcome readout at rest passes, and at the grasp anchor the current latent reads the grasp at 0.82. The four uses that ask the latent for progress or task stage all fail: progress monotonicity, two-level hierarchical progress [10], the latent stage tracker and the latent-distance scale of SURVEYOR [13]. The pose probes of LeJEPA [12] say what else the latent holds. A linear readout recovers about half of the joint variance from our encoder (R² 0.565), less than from the frozen DINOv2-S control (0.867).

<!-- editlens paragraph 0.308 lines 58-58 -->
The predictor does predict its own latent. At K = 30 its open-loop error is 0.31, against 0.89 for copying the last latent. What fails is every use of that prediction. Chunk ranking [1] puts the executed chunk first in 0.60 of anchors against a bar of 0.8, while the commanded actions alone reach 0.68–0.90. The surprise monitor catches 2/8 at 2/42 failures. The hierarchical planner [14] shows no crossover. The conformal surprise band, the re-ranking of chunk candidates, the action-conditioned risk head [11] and the calibrated surprise reflex each miss their bar by the margin in Table 1.

### What the encoder knows (mean 0.184)

<!-- editlens chunk 0.184 lines 62-82 -->
<!-- editlens paragraph 0.117 lines 62-62 -->
Table 2 sets our model beside the four other signals on the same 69 rollouts, at rest and at the grasp anchor. The question is whether the encoder adds anything a frozen encoder or the joints do not already carry.

<!-- editlens paragraph 0.286 lines 76-76 -->
At rest our model is level with the colour judge, whose CI overlaps its own, and above the frozen encoder and the joints. At the grasp anchor no judge applies, and our model leads both controls. Since the pose probes hold the joints better than our encoder does but the outcome worse, the encoder carries outcome information they lack, at least on these rollouts.

<!-- editlens paragraph 0.211 lines 78-78 -->
The anchor column depends on how the five seeds are combined. Averaging the predictions before scoring gives 0.8377, 0.7175 and 0.5346 for our model, frozen DINOv2-S and the joints. Seed 0 alone gives 0.7554, 0.7024 and 0.5574, a smaller gap between our model and the frozen encoder. The order holds either way.

<!-- editlens paragraph 0.177 lines 80-80 -->
One control does beat our model. On SURVEYOR's scale check, frozen DINOv2-S (τ 0.3601) and the joints (τ 0.0265) pass where our model fails (τ 1.2488, against 0.20 reported by SURVEYOR). The same task and the same rollouts pass with other features, so the failure points at the geometry of our latent space rather than at the task.

<!-- editlens paragraph 0.158 lines 82-82 -->
The register's own outcome-readout row reports 1.000. That number was scored against the colour judge's labels, on 87 rollouts, so it partly measures agreement with the judge. Against the operator's labels on the 69 rollouts, with the controls beside it, the same readout gives 0.9545.

### Where the predictor fails (mean 0.177)

<!-- editlens chunk 0.177 lines 86-104 -->
<!-- editlens paragraph 0.336 lines 86-86 -->
ContactGuard [9] finds that probes on the imagined latent beat probes on the current one for grasp tasks, so we expected the imagined latent to help at our grasp anchor. The bar asked it for ≥ 0.85, ≥ +0.05 over the current latent. With the same encoder and the same anchor, the current latent reads the outcome at 0.82 and the imagined one at 0.70. This pre-registered row fails: on these rollouts, imagining forward loses outcome information the encoder had. The encoder and predictor reading we build on it stays exploratory.

<!-- editlens paragraph 0.158 lines 88-88 -->
Our model's inverse-dynamics term is no better than that of its own untrained network. On the distillation probe, pooled over the 25 teleoperation validation episodes, the trained model scores 0.7476 and its random initialisation 0.7974, a difference of −0.0499 with a 95 % paired episode-bootstrap CI of [−0.7403, +0.6559] (X). The term itself is fragile: the same untrained network scored 1.4383 on one machine and 0.7974 and 0.8042 on two others, because it is sensitive to the BLAS library and to ridge conditioning.

<!-- editlens paragraph 0.187 lines 90-90 -->
We checked whether the surprise monitor's poor failure-class AUROC (0.775, below its sanity bar) came from a bug in loading or scoring. It did not. The same scorer reproduces the open-loop corruption ratios at K = 30: cross-episode 3.428 against 3.341 in the original run, constant-first 2.558 against 2.543 (X). The low AUROC is a real value.

<!-- editlens paragraph 0.233 lines 92-92 -->
The predictor of VLA-JEPA barely uses its actions. At 5 anchors (Table 3), action tokens taken from another episode differ from the true ones by 21–28 % in relative L2 but move the loss by only about 0.05 %. Zeroing the tokens moves it by about 1.05 % on average, and the forward pass is deterministic. Its failure-class AUROC of 0.501, below the same sanity bar, is therefore real, and we leave its table unread under the frozen bar.

<!-- editlens paragraph 0.344 lines 104-104 -->
A reader may object that one pass in the register is predictive. In the anticipation step of the outcome-readout gate, the imagined latent beat policy identity by +0.179. That bar is retrospective, though, and the two reruns of the same idea with the bar committed first, the grasp probe and the calibrated surprise reflex, both fail.

### Related work (mean 0.205)

<!-- editlens chunk 0.205 lines 108-108 -->
<!-- editlens paragraph 0.205 lines 108-108 -->
LeWorldModel [1] trains the recipe we use end to end from pixels and plans with it in Push-T and in simulation. Its two planning uses, chunk ranking and re-ranking, fail on our arm. LeJEPA's identifiability analysis [12] predicts that SIGReg latents identify the state up to anisotropy; our pose probes support that only in part. DINO-WM [8] plans on frozen DINOv2 [7] patches, which is why our frozen control is built that way. V-JEPA 2.1 [3] and RoboJEPA [2] are too slow on our on-board computer; timing them is the one register row that is not a use of our model. ContactGuard [9] is the result we contradict most directly: it finds imagined-latent probes better than current-latent ones on grasp tasks, and we find the reverse. The re-tests of ReAP's action-conditioned risk [11], the hierarchical planners of HWM [14] and H-JEPA [10] and SURVEYOR's latent-distance scale [13] all miss their bars here. Two papers agree with us from the control side. SaiVLA-JEPA [15] reports that a training-only future-latent head adds +0.03 points to control on 10,030 paired episodes, and HIJP [16] finds LeWM below goal-conditioned behaviour cloning in simulation.

### Limitations (mean 0.376)

<!-- editlens chunk 0.376 lines 112-112 -->
<!-- editlens paragraph 0.376 lines 112-112 -->
Every statement about the split between encoder and predictor rests on 69 rollouts, labels from one operator and probes chosen after the data. Fresh rollouts scored under a bar committed first would test it, and until that runs the split stays exploratory. All results come from one rig, one model and one data scale. A second scale point at 653 episodes is costed and queued, and a scale curve belongs to a longer version. Three controls were not run. The surprise monitor and the imagined arm of the grasp probe would each need a predictor trained on frozen DINOv2-S features or on the joints, and progress monotonicity with the controls would need a reimplementation. The outcome-readout verdict is retrospective, and the two-level hierarchical progress use has its bar in the same commit as its result.

### Conclusion (mean 0.349)

<!-- editlens chunk 0.349 lines 116-116 -->
<!-- editlens paragraph 0.349 lines 116-116 -->
Before building on the predictor of a world model this size, probe its encoder. On our 182 demonstrations, the current latent read the grasp outcome better than the imagined one, and every use that needed the predictor to forecast missed its bar.

### (figure and table captions) (mean 0.097)

<!-- editlens chunk 0.097 lines 31-94 -->
<!-- editlens paragraph 0.118 lines 31-31 -->
Table 1: The register: every pre-registered use of our world model (and the frozen-DINOv2 and RoboJEPA rows beside it), the paper it re-tests, what it takes from the model, whether the bar was committed before the result (audited against the commit history), the bar, the result and the verdict. Bar, result and verdict are quoted from repro/register/expected/FEASIBILITY.md §2 with the model names made plain; the code names the repro folder.

<!-- editlens paragraph 0.067 lines 64-64 -->
Table 2: Outcome AUROC on the same 69 rollouts. Exploratory (controls chosen after the data), LOSO linear probes, operator labels. At rest: 95 % episode-bootstrap CI. At the anchor: 95 % episode-bootstrap CI on the mean over 5 seeds of the out-of-fold AUROC (episodes resampled jointly across the seeds, 2,000 resamples, percentile).

<!-- editlens paragraph 0.088 lines 94-94 -->
Table 3: VLA-JEPA world-model loss at 5 anchors with the true action tokens, tokens from another episode (Δ shuffled) and zeroed tokens; the token change is the relative L2 of the shuffled tokens. Exploratory, a spot check, not a power analysis. Source: repro/gaps/expected/M3_diag_action_shuffle.json.

## built PDF

### (front matter) (mean 0.134)

<!-- editlens chunk 0.134 lines 3-8 -->
A small JEPA world model on a low-cost arm: the encoder reads the outcome, the predictor adds nothing to it Ravindu Somawansa∗ Shisso Robotics, Paris ravindu.somawansa@gmail.com

### Abstract (mean 0.091)

<!-- editlens chunk 0.140 lines 10-81 -->
<!-- editlens paragraph 0.091 lines 10-24 -->
We trained a small JEPA world model in the LeWorldModel recipe on 182 teleoperated demonstrations of one tabletop task on an SO-101 arm, for $3.30 of rented GPU time. We then took every use of such a model that we found in recent world-model papers and re-tested it on ours, each against a bar written into a public register. Every use that needs a multi-step rollout of the predictor misses its bar, among them chunk ranking, surprise monitoring and risk prediction. The encoder does better. In exploratory probes on policy rollouts the model never saw in training, a linear readout of the last-frame latent separates success from failure about as well as a hand-built colour judge (AUROC 0.95 against 0.94), and better than a frozen DINOv2 encoder, the commanded joints or the identity of the policy. At the grasp, the imagined latent reads the outcome worse than the current one does (0.70 against 0.82). All of it comes from one rig, one model and one data scale.

<!-- editlens paragraph 0.128 lines 29-47 -->
A world model in the sense of LeWorldModel (LeWM) [1] has two parts. The encoder maps camera frames to a latent vector. The predictor takes the current latent and a sequence of actions and imagines the latents that follow. Both are trained together from pixels with a joint-embedding predictive (JEPA) loss. Papers built on such models propose uses for them: ranking a policy’s candidate action chunks by their imagined outcome, flagging a failure when the observed latent drifts from the predicted one, reading the outcome of a grasp before it happens, planning over several time scales. Each paper reports the use that worked, on its own robot and data. We had one such model, trained on our own arm, and wanted to know which of these uses we could build on. So we ran every use we could find on that one model. ∗ Code, data pointers and every number’s source: https://github. com/ravediamond/paper-jepa-world-model.

<!-- editlens paragraph 0.285 lines 50-81 -->
Each re-test is a row of a register with a bar, a dataset, a result and a verdict, and where we managed it, the bar and the decision rule went into the repository before the result existed. That commit order is all we mean by preregistration. Checked against the commit history, all 20 rows match a pre-registration record. In 19 the bar was committed before the result, and in 1 (the two-level hierarchical progress use) in the same commit. One row is not a use of our model: it times the pretrained RoboJEPA and V-JEPA 2.1 encoders on our on-board computer [2, 3]. Of the 20 rows, 3 pass and 1 is met as predicted. Another 2 are not proven, and the remaining 14 fail or are no-go. Our first reading of the failures was that the latent mostly encodes the arm’s pose, so a frozen image encoder or the commanded joints would do at least as well in each of them. We ran those controls on 69 policy rollouts, and they did not bear it out. The encoder reads how the episode went from the current frame better than either control, and it still does at the grasp anchor, 15 frames before the gripper first closes. The predictor, which every forecasting use relies on, does not improve that reading by imagining forward. We changed the claim of the paper to match: at this data scale the predictor, not the encoder, is the weak link. The controls came after the data, and that limits what they can show. Each readout is a linear probe fit with leave-one-session-out (LOSO) cross-validation on the 69 rollouts (44 success, 25 failure, 13 sessions) and scored against the operator’s labels. The model was trained on teleoperation only and never saw these rollouts. No bar was committed for these comparisons, so everything this paper says about the split between encoder and predictor is exploratory. Of the 3 register passes, 3 have their bar committed before the result, though the register marks the outcome-readout verdict as retrospective. Without the audit, ordering by commit alone gives 13 bar-first and 6 same-commit rows.

<!-- editlens chunk 0.098 lines 86-174 -->
<!-- editlens paragraph 0.117 lines 89-114 -->
is to put a bowl into another bowl. Our model is trained on ravediamond/so101_bowls_all_trimmed, split by grid layout into 157 training and 25 validation episodes. The evaluation rollouts come from a separate dataset, ravediamond/so101-bowls-policy-rollouts: SmolVLA [6] runs recorded after our model was trained. Our model follows the LeWM recipe [1], with a multiview ViT encoder, an action-conditioned predictor and the SIGReg regulariser, and was trained on one rented GPU. We compare it with four signals. The frozen DINOv2-S control is a frozen DINOv2 small encoder [7] mean-pooled over the top and wrist views, the design of DINO-WM [8]. The joints control is the commanded joint vector. The colour judge is a hand-built rule on the final frame with no learning, and policy identity is the checkpoint that ran the episode. In October, a timing test on the on-board computer loaded our checkpoint with strict=False. Under the transformers version on that image (5.5.4), 192 encoder tensors did not match and were silently dropped, so the test timed a random encoder. We voided its latents and traced how every other use loaded the model: 26 ran the trained model, 1 ran a random one (that test) and none is unknown. The world-model block of VLA-JEPA, which one diagnostic below uses, loads all 351 of its keys.

<!-- editlens paragraph 0.177 lines 119-137 -->
Table 1 lists the 20 uses and what each takes from our model: the encoder alone (7), the predictor (8) or both (5). Read that column against the verdicts. Among the encoder uses, reading the outcome works and reading progress does not. The outcome readout at rest passes, and at the grasp anchor the current latent reads the grasp at 0.82. The four uses that ask the latent for progress or task stage all fail: progress monotonicity, two-level hierarchical progress [10], the latent stage tracker and the latent-distance scale of SURVEYOR [13]. The pose probes of LeJEPA [12] say what else the latent holds. A linear readout recovers about half of the joint variance from our encoder (R2 0.565), less than from the frozen DINOv2-S control (0.867). The predictor does predict its own latent. At K = 30 its open-loop error is 0.31, against 0.89 for copying the last latent. What fails is every use of that prediction. Chunk ranking [1] puts the executed chunk first in 0.60 of anchors against a bar of 0.8, while the commanded actions alone reach 0.68–0.90. The surprise monitor catches 2/8 at 2/42 failures. The hierarchical planner [14] shows no crossover. The conformal surprise band, the re-ranking of chunk candidates, the actionconditioned risk head [11] and the calibrated surprise reflex each miss their bar by the margin in Table 1.

<!-- editlens chunk 0.081 lines 179-629 -->
<!-- editlens paragraph 0.204 lines 179-205 -->
Table 2 sets our model beside the four other signals on the same 69 rollouts, at rest and at the grasp anchor. The question is whether the encoder adds anything a frozen encoder or the joints do not already carry. At rest our model is level with the colour judge, whose CI overlaps its own, and above the frozen encoder and the joints. At the grasp anchor no judge applies, and our model leads both controls. Since the pose probes hold the joints better than our encoder does but the outcome worse, the encoder carries outcome information they lack, at least on these rollouts. The anchor column depends on how the five seeds are combined. Averaging the predictions before scoring gives 0.8377, 0.7175 and 0.5346 for our model, frozen DINOv2-S and the joints. Seed 0 alone gives 0.7554, 0.7024 and 0.5574, a smaller gap between our model and the frozen encoder. The order holds either way. One control does beat our model. On SURVEYOR’s scale check, frozen DINOv2-S (τ 0.3601) and the joints (τ 0.0265) pass where our model fails (τ 1.2488, against 0.20 reported by SURVEYOR). The same task and the same rollouts pass with other features, so the failure points at the geometry of our latent space rather than at the task. The register’s own outcome-readout row reports 1.000. That number was scored against the colour judge’s labels, on 87 rollouts, so it partly measures agreement with the judge. Against the operator’s labels on the 69 rollouts, with the controls beside it, the same readout gives 0.9545.

<!-- editlens paragraph 0.218 lines 210-216 -->
ContactGuard [9] finds that probes on the imagined latent beat probes on the current one for grasp tasks, so we expected the imagined latent to help at our grasp anchor. The bar asked it for ≥ 0.85, ≥ +0.05 over the current latent. With the same encoder and the same anchor, the current latent reads the outcome at 0.82 and the imagined one at 0.70. This pre-registered row fails: on these rollouts, imagining forward loses outcome information 2

<!-- editlens paragraph 0.108 lines 217-222 -->
Table 1: The register: every pre-registered use of our world model (and the frozen-DINOv2 and RoboJEPA rows beside it), the paper it re-tests, what it takes from the model, whether the bar was committed before the result (audited against the commit history), the bar, the result and the verdict. Bar, result and verdict are quoted from repro/register/expected/FEASIBILITY.md §2 with the model names made plain; the code names the repro folder. use

<!-- editlens paragraph 0.088 lines 582-588 -->
Table 2: Outcome AUROC on the same 69 rollouts. Exploratory (controls chosen after the data), LOSO linear probes, operator labels. At rest: 95 % episode-bootstrap CI. At the anchor: 95 % episode-bootstrap CI on the mean over 5 seeds of the out-of-fold AUROC (episodes resampled jointly across the seeds, 2,000 resamples, percentile). feature

<!-- editlens paragraph 0.120 lines 617-629 -->
the encoder had. The encoder and predictor reading we build on it stays exploratory. Our model’s inverse-dynamics term is no better than that of its own untrained network. On the distillation probe, pooled over the 25 teleoperation validation episodes, the trained model scores 0.7476 and its random initialisation 0.7974, a difference of −0.0499 with a 95 % paired episode-bootstrap CI of [−0.7403, +0.6559] (gap5_pooled_rerun.json). The term itself is fragile: the same untrained network scored 1.4383 on one machine and 0.7974 and 0.8042 on two others, because it is sensitive to the BLAS library and to ridge conditioning. We checked whether the surprise monitor’s poor failure-class AUROC (0.775, below its sanity bar) came 3

<!-- editlens chunk 0.051 lines 630-728 -->
in simulation. Table 3: VLA-JEPA world-model loss at 5 anchors with the true action tokens, tokens from another episode (Δ shuffled) and zeroed tokens; the token change is 7 Limitations the relative L2 of the shuffled tokens. Exploratory, a spot check, not a power analysis. Source: re- Every statement about the split between encoder and predictor rests on 69 rollouts, labels from one operator pro/gaps/expected/M3_diag_action_shuffle.json. anchor (episode / frame) true loss Δ shuffled (%) token change (%) Δ zeroed (%) and probes chosen after the data. Fresh rollouts scored 8 / 402 1.3031 +0.014 21.1 +2.22 under a bar committed first would test it, and until that 10 / 227 1.4641 +0.088 27.6 +0.50 runs the split stays exploratory. All results come from 23 / 327 1.4215 +0.036 21.1 +0.87 59 / 302 1.4637 +0.030 25.5 +1.28 one rig, one model and one data scale. A second scale 65 / 302 1.5236 −0.070 22.0 −0.38 point at 653 episodes is costed and queued, and a scale curve belongs to a longer version. Three controls were from a bug in loading or scoring. It did not. The not run. The surprise monitor and the imagined arm of same scorer reproduces the open-loop corruption ra- the grasp probe would each need a predictor trained on tios at K = 30: cross-episode 3.428 against 3.341 frozen DINOv2-S features or on the joints, and progress in the original run, constant-first 2.558 against 2.543 monotonicity with the controls would need a reimple(M1_diag_g0_repro.json). The low AUROC is a real mentation. The outcome-readout verdict is retrospective, and the two-level hierarchical progress use has its bar in value. The predictor of VLA-JEPA barely uses its actions. At the same commit as its result. 5 anchors (Table 3), action tokens taken from another episode differ from the true ones by 21–28 % in relative 8 Conclusion L2 but move the loss by only about 0.05 %. Zeroing the tokens moves it by about 1.05 % on average, and the for- Before building on the predictor of a world model this ward pass is deterministic. Its failure-class AUROC of size, probe its encoder. On our 182 demonstrations, the 0.501, below the same sanity bar, is therefore real, and current latent read the grasp outcome better than the we leave its table unread under the frozen bar. imagined one, and every use that needed the predictor A reader may object that one pass in the register is pre- to forecast missed its bar. dictive. In the anticipation step of the outcome-readout gate, the imagined latent beat policy identity by +0.179. That bar is retrospective, though, and the two reruns of References the same idea with the bar committed first, the grasp [1] Lucas Maes, Quentin Le Lidec, Damien Scieur, probe and the calibrated surprise reflex, both fail. Yann LeCun, and Randall Balestriero. LeWorldModel: Stable end-to-end joint-embedding pre6 Related work dictive architecture from pixels. arXiv preprint arXiv:2603.19312, 2026. LeWorldModel [1] trains the recipe we use end to end [2] Artem Zholus, Nicolas Beltran-Velez, Jianhao from pixels and plans with it in Push-T and in simuYuan, Sarath Chandar, Tushar Nagarajan, Daniel lation. Its two planning uses, chunk ranking and reSevero, Koustuv Sinha, Michal Drozdzal, Adriranking, fail on our arm.

<!-- editlens chunk 0.067 lines 630-745 -->
<!-- editlens paragraph 0.102 lines 731-740 -->
real-world robotics in PyTorch. https://github. com/huggingface/lerobot, 2024. Not in the paper library. [6] Mustafa Shukor, Dana Aubakirova, Francesco Capuano, Pepijn Kooijmans, Steven Palma, Adil Zouitine, Michel Aractingi, Caroline Pascal, Martino Russi, Andres Marafioti, Simon Alibert, Matthieu Cord, Thomas Wolf, and Remi Cadene. SmolVLA: A vision-language-action model for affordable and eﬀicient robotics. arXiv preprint arXiv:2506.01844, 2025.

<!-- editlens chunk 0.088 lines 746-783 -->
<!-- editlens paragraph 0.088 lines 746-783 -->
[7] Maxime Oquab, Timothée Darcet, Théo Moutakanni, et al. DINOv2: Learning robust visual features without supervision. arXiv preprint arXiv:2304.07193, 2023. Not in the paper library. [8] Gaoyue Zhou, Hengkai Pan, Yann LeCun, and Lerrel Pinto. DINO-WM: World models on pre-trained visual features enable zero-shot planning. arXiv preprint arXiv:2411.04983, 2024. [9] Gehan Zheng, Matthew Johnson-Roberson, and Weiming Zhi. ContactGuard: Pre-contact execution monitoring with action-conditioned latent world models. arXiv preprint arXiv:2608.13438, 2026. [10] Wancong Zhang, Basile Terver, Michael Rabbat, Yann LeCun, and Randall Balestriero. H-JEPA: Endto-end learning of hierarchical world models for visual planning. arXiv preprint arXiv:2610.06805, 2026. [11] Jingyuan Liu, Yunpeng Qing, Changxu Wei, and Zhi Hou. ReAP: From visual failure recognition to action-conditioned risk prediction for runtime failure monitoring. arXiv preprint arXiv:2610.16309, 2026. [12] David Klindt, Yann LeCun, and Randall Balestriero. When does LeJEPA learn a world model? arXiv preprint arXiv:2605.26379, 2026. [13] Anonymous. SURVEYOR: Certified speculative plan consumption for latent world-model planning, 2026. NeurIPS 2026 submission; no arXiv identifier known. [14] Wancong Zhang, Basile Terver, Artem Zholus, Soham Chitnis, Harsh Sutaria, Mido Assran, Randall Balestriero, Amir Bar, Yann LeCun, and Nicolas Ballas. Hierarchical planning with latent world models. arXiv preprint arXiv:2604.03208, 2026. [15] Rufeng Xiao, Ruihao Xiao, Wei Chen, and Xinhai Sun. SaiVLA-JEPA: Evaluating future latent prediction in JEPA-conditioned VLA control. arXiv preprint arXiv:2610.38508, 2026. [16] Guanchen Du, Jinhao Du, Yanpeng Sun, Shan Zhang, Na Zhao, and Zechao Li. Beyond action github.com/ravediamond/paper-jepa-world-model · 2c76058
