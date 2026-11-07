# paper-jepa-world-model: chunks in paper order

## rendered source (numbers filled)

### Abstract (mean 0.184)

<!-- editlens chunk 0.184 lines 7-7 -->
<!-- editlens paragraph 0.184 lines 7-7 -->
For $3.30 of rented GPU time we trained a small JEPA world model in the LeWorldModel recipe on teleoperated demonstrations of one tabletop task on an SO-101 arm, then re-tested on it every use of such a model that recent papers propose, each against a threshold written into a public register. Its encoder reads how an episode ended. On policy rollouts the model never saw, a linear probe on the last-frame latent separates success from failure about as well as a hand-built colour judge, and better than a frozen DINOv2 encoder or the commanded joints. The predictor adds nothing to that reading: at the grasp, the imagined latent reads the outcome worse than the current one (0.70 against 0.82), and at this data scale every use that needs it to roll forward misses its pass mark. So before building on the predictor of a model this size, probe its encoder. The controls are exploratory and come from one rig and one model.

### Introduction (mean 0.163)

<!-- editlens chunk 0.163 lines 11-19 -->
<!-- editlens paragraph 0.221 lines 11-11 -->
A world model is usually valued for its predictor. In the sense of LeWorldModel (LeWM) [1] it has two parts: an encoder that maps camera frames to a latent vector, and a predictor that takes the current latent and a sequence of actions and imagines the latents that follow, both trained together from pixels with a joint-embedding predictive (JEPA) loss. Most applications proposed for it lean on the predictor. The best known ranks a policy's candidate action chunks by their imagined outcome; others flag a failure when the observed latent drifts from the predicted one, read a grasp's outcome before it happens, or plan over several time scales. Each paper reports the use that worked, on its own robot and data.

<!-- editlens paragraph 0.100 lines 13-13 -->
We had one such model, trained for $3.30 of rented GPU time on our own arm, and wanted to know which of these uses we could build on. So we ran every use we could find on that one model. Each re-test is a row of a register with a pass mark, a dataset, a result and a verdict, and where we managed it, the threshold and the decision rule went into the repository before the result existed (that commit order is all we mean by pre-registration). Checked against the commit history, all 20 rows match a pre-registration record. In 19 the bar was committed before the result, and in 1 (the two-level hierarchical progress use) in the same commit. One row is not a use of our model: it times the pretrained RoboJEPA and V-JEPA 2.1 encoders on our on-board computer [2, 3]. Of the 20 rows, 3 pass and 1 is met as predicted. Another 2 are not proven, and the remaining 14 fail or are no-go.

<!-- editlens paragraph 0.281 lines 15-15 -->
The first draft of this paper argued something else. Our reading of the failures was that the latent mostly encodes the arm's pose, so a frozen image encoder or the commanded joints would do at least as well in every one of them. We ran those controls on 69 policy rollouts before writing it up, and they did not bear it out: the encoder reads how the episode went better than either control. We rewrote the claim. At this data scale the predictor, not the encoder, is the weak link.

<!-- editlens paragraph 0.313 lines 17-17 -->
One moment runs through the rest of the paper: the grasp anchor, 15 frames before the gripper first closes. There the current latent reads the outcome at 0.82 and the imagined latent at 0.70, and that gap is the argument in one row.

<!-- editlens paragraph 0.325 lines 19-19 -->
The controls came after the data, which limits what they can show. Each readout is a linear probe fit with leave-one-session-out (LOSO) cross-validation on the 69 rollouts (44 success, 25 failure, 13 sessions), scored against labels the author gave at rest. The model was trained on teleoperation only and never saw these rollouts. No threshold was committed for these comparisons, so everything this paper says about the split between encoder and predictor is exploratory. Of the 3 register passes, 3 have their bar committed before the result, though the register marks the outcome-readout verdict as retrospective.

### Setup (mean 0.125)

<!-- editlens chunk 0.125 lines 23-27 -->
<!-- editlens paragraph 0.051 lines 23-23 -->
The robot is one SO-101 arm [4] driven through LeRobot [5], with a top and a wrist camera. The task is to put a bowl into another bowl. Our model is trained on X, split by grid layout into 157 training and 25 validation episodes. The evaluation rollouts come from a separate dataset, X: SmolVLA [6] runs recorded after our model was trained.

<!-- editlens paragraph 0.084 lines 25-25 -->
Our model follows the LeWM recipe [1], with a multi-view ViT encoder, an action-conditioned predictor and the SIGReg regulariser. We set it beside four signals, each chosen because it is cheaper than a world model. The frozen DINOv2-S control is a frozen DINOv2 small encoder [7] mean-pooled over the top and wrist views (the design of DINO-WM [8]). The joints control is the commanded joint vector. The colour judge is a hand-built rule on the final frame with no learning, and policy identity is the checkpoint that ran the episode.

<!-- editlens paragraph 0.308 lines 27-27 -->
In October, a timing test on the on-board computer loaded our checkpoint with X. Under the transformers version on that image (5.5.4), 192 encoder tensors did not match and were silently dropped, so the test timed a random encoder. We voided its latents and traced how every other use loaded the model: 26 ran the trained model, 1 ran a random one (that test) and none is unknown. The world-model block of VLA-JEPA, which one diagnostic below uses, loads all 351 of its keys.

### The register (mean 0.251)

<!-- editlens chunk 0.251 lines 31-60 -->
<!-- editlens paragraph 0.304 lines 58-58 -->
Among the encoder uses, reading the outcome works and reading progress does not. The outcome readout at rest passes, and at the grasp anchor the current latent reads the grasp at 0.82. All four uses that ask the latent for progress or task stage fail, from progress monotonicity and two-level hierarchical progress [10] to the latent stage tracker and SURVEYOR's latent-distance scale [13]. The pose probes of LeJEPA [12] show some of what else it holds. A linear readout recovers about half of the joint variance from our encoder (R² 0.565), less than from the frozen DINOv2-S control (0.867).

<!-- editlens paragraph 0.314 lines 60-60 -->
The predictor does predict its own latent: at K = 30 its open-loop error is 0.31, against 0.89 for copying the last latent. Every application of that prediction fails, and chunk ranking [1] shows why most clearly. It puts the executed chunk first in 0.60 of anchors against a pass mark of 0.8, while the commanded actions alone reach 0.68–0.90, so the cheapest signal in the table beats the one built on imagination. The surprise monitor catches 2/8 at 2/42 failures. The rest (the hierarchical planner [14], the conformal surprise band, re-ranking, the risk head [11] and the calibrated reflex) miss their thresholds by the margins in Table 1.

### What the encoder knows (mean 0.123)

<!-- editlens chunk 0.123 lines 64-84 -->
<!-- editlens paragraph 0.061 lines 64-64 -->
The test here is whether the encoder carries anything that a frozen encoder or the joints do not. Table 2 sets our model beside the four other signals on the same 69 rollouts. Every probe is a LOSO linear probe against the author's labels. At rest the interval is a 95 % episode-bootstrap CI; at the anchor it is a bootstrap of the mean over 5 seeds of the out-of-fold AUROC (episodes resampled jointly across the seeds, 2,000 resamples, percentile).

<!-- editlens paragraph 0.191 lines 78-78 -->
At rest our model is level with the colour judge (the CIs overlap) and above the frozen encoder and the joints. At the grasp anchor no judge applies, and our model leads both controls. Since the pose probes hold the joints better than our encoder does but the outcome worse, the encoder carries outcome information they lack, at least on these rollouts.

<!-- editlens paragraph 0.211 lines 80-80 -->
The anchor column depends on how the five seeds are combined. Averaging the predictions before scoring gives 0.8377, 0.7175 and 0.5346 for our model, frozen DINOv2-S and the joints. Seed 0 alone gives 0.7554, 0.7024 and 0.5574, a smaller gap between our model and the frozen encoder. The order holds either way.

<!-- editlens paragraph 0.177 lines 82-82 -->
One control does beat our model. On SURVEYOR's scale check, frozen DINOv2-S (τ 0.3601) and the joints (τ 0.0265) pass where our model fails (τ 1.2488, against 0.20 reported by SURVEYOR). The same task and the same rollouts pass with other features, so the failure points at the geometry of our latent space rather than at the task.

<!-- editlens paragraph 0.139 lines 84-84 -->
The register's own outcome-readout row reports 1.000. That number was scored against the colour judge's labels, on 87 rollouts, so it partly measures agreement with the judge. Against the author's labels on the 69 rollouts, with the controls beside it, the same readout gives 0.9545.

### Where the predictor fails (mean 0.186)

<!-- editlens chunk 0.186 lines 88-106 -->
<!-- editlens paragraph 0.344 lines 88-88 -->
ContactGuard [9] finds that probes on the imagined latent beat probes on the current one for grasp tasks, so we expected the imagined latent to help at our grasp anchor. The pre-registered threshold asked it for ≥ 0.85, ≥ +0.05 over the current latent. With the same encoder and the same anchor, the current latent reads the outcome at 0.82 and the imagined one at 0.70. This pre-registered row fails: on these rollouts, imagining forward loses outcome information the encoder had.

<!-- editlens paragraph 0.136 lines 90-90 -->
Our model's inverse-dynamics term is no better than that of its own untrained network. On the distillation probe, pooled over the 25 teleoperation validation episodes, the trained model scores 0.7476 and its random initialisation 0.7974, a difference of −0.0499 with a 95 % paired episode-bootstrap CI of [−0.7403, +0.6559] (X). The term itself is fragile: the same untrained network scored 1.4383 on one machine and 0.7974 and 0.8042 on two others (it is sensitive to the BLAS library and to ridge conditioning).

<!-- editlens paragraph 0.222 lines 92-92 -->
A low score can also come from a bug, so we checked the surprise monitor's failure-class AUROC (0.775, below its sanity bar) for one in loading or scoring. The same scorer reproduces the open-loop corruption ratios at K = 30: cross-episode 3.428 against 3.341 in the original run, constant-first 2.558 against 2.543 (X). The low AUROC is a real value.

<!-- editlens paragraph 0.257 lines 94-94 -->
The predictor of VLA-JEPA barely uses its actions. At 5 anchors (Table 3, from X), action tokens taken from another episode differ from the true ones by 21–28 % in relative L2 but move the loss by only about 0.05 %. Zeroing the tokens moves it by about 1.05 % on average, and the forward pass is deterministic. Its failure-class AUROC of 0.501, below the same sanity check, is therefore real, and we leave its table unread under the frozen bar.

<!-- editlens paragraph 0.374 lines 106-106 -->
A reader may object that one pass in the register is predictive. In the anticipation step of the outcome-readout gate, the imagined latent beat policy identity by +0.179. That bar is retrospective, though, and the two reruns of the same idea with the threshold committed first, the grasp probe and the calibrated surprise reflex, both fail.

### Related work (mean 0.220)

<!-- editlens chunk 0.220 lines 110-110 -->
<!-- editlens paragraph 0.220 lines 110-110 -->
LeWorldModel [1] trains the recipe we use end to end from pixels and plans with it in Push-T and in simulation. Its two planning uses fail on our arm. LeJEPA's identifiability analysis [12] predicts that SIGReg latents identify the state up to anisotropy, which our pose probes support only in part. DINO-WM [8] plans on frozen DINOv2 [7] patches; our frozen control copies that design. V-JEPA 2.1 [3] and RoboJEPA [2] are too slow on our on-board computer, and timing them is the one register row that is not a use of our model. ContactGuard [9] is the result we contradict most directly. It finds imagined-latent probes better than current-latent ones on grasp tasks, and on our arm the reverse holds. The re-tests of ReAP's action-conditioned risk [11], the hierarchical planners of HWM [14] and H-JEPA [10] and SURVEYOR's latent-distance scale [13] also miss here, at this data scale. Two papers agree with us from the control side: SaiVLA-JEPA [15] reports that a training-only future-latent head adds +0.03 points to control on 10,030 paired episodes, and HIJP [16] finds LeWM below goal-conditioned behaviour cloning in simulation.

### Limitations (mean 0.222)

<!-- editlens chunk 0.222 lines 114-114 -->
<!-- editlens paragraph 0.222 lines 114-114 -->
The split between encoder and predictor is exploratory. Its probes were chosen after the data and fit on 69 rollouts labelled by a single operator, the author. Two things limit the risk. The model never saw these rollouts, and every probe is cross-validated by session. The confirming test is a fresh set of rollouts scored under a threshold committed first, which needs a day on the arm. Scale is the other open condition. All of this comes from one model at one data scale, and a second point at 653 episodes is costed and queued. Three controls were not run, because the surprise monitor and the imagined arm of the grasp probe would each need their own predictor (trained on frozen DINOv2-S features or on the joints) and progress monotonicity would need a reimplementation. In the register, the outcome-readout verdict is retrospective and the two-level hierarchical progress use has its bar in the same commit as its result; ordered by commit alone, without the audit, the register reads 13 bar-first and 6 same-commit rows.

### Conclusion (mean 0.266)

<!-- editlens chunk 0.266 lines 118-118 -->
<!-- editlens paragraph 0.266 lines 118-118 -->
A $3.30 world model and 69 policy rollouts were enough to sort 20 published uses into those this model supports and those it does not. At this data scale the encoder carries the outcome and the predictor adds nothing to it. Probe the encoder before building on the predictor, and keep the commanded actions as a baseline: here they ranked chunks better than imagination did.

### (figure and table captions) (mean 0.173)

<!-- editlens chunk 0.173 lines 33-96 -->
<!-- editlens paragraph 0.173 lines 33-33 -->
Table 1: The register: every use of our world model re-tested here (with the frozen-DINOv2 and RoboJEPA rows beside it), what it takes from the model, whether its bar came before the result, and the verdict. Read the takes column against the verdict: the predictor uses fail. Bar, result and verdict are quoted from repro/register/expected/FEASIBILITY.md §2.

## built PDF

### (front matter) (mean 0.134)

<!-- editlens chunk 0.134 lines 3-8 -->
A small JEPA world model on a low-cost arm: the encoder reads the outcome, the predictor adds nothing to it Ravindu Somawansa∗ Shisso Robotics, Paris ravindu.somawansa@gmail.com

### Abstract (mean 0.141)

<!-- editlens chunk 0.179 lines 10-75 -->
<!-- editlens paragraph 0.184 lines 10-24 -->
For $3.30 of rented GPU time we trained a small JEPA world model in the LeWorldModel recipe on teleoperated demonstrations of one tabletop task on an SO-101 arm, then re-tested on it every use of such a model that recent papers propose, each against a threshold written into a public register. Its encoder reads how an episode ended. On policy rollouts the model never saw, a linear probe on the last-frame latent separates success from failure about as well as a hand-built colour judge, and better than a frozen DINOv2 encoder or the commanded joints. The predictor adds nothing to that reading: at the grasp, the imagined latent reads the outcome worse than the current one (0.70 against 0.82), and at this data scale every use that needs it to roll forward misses its pass mark. So before building on the predictor of a model this size, probe its encoder. The controls are exploratory and come from one rig and one model.

<!-- editlens paragraph 0.138 lines 29-46 -->
A world model is usually valued for its predictor. In the sense of LeWorldModel (LeWM) [1] it has two parts: an encoder that maps camera frames to a latent vector, and a predictor that takes the current latent and a sequence of actions and imagines the latents that follow, both trained together from pixels with a joint-embedding predictive (JEPA) loss. Most applications proposed for it lean on the predictor. The best known ranks a policy’s candidate action chunks by their imagined outcome; others flag a failure when the observed latent drifts from the predicted one, read a grasp’s outcome before it happens, or plan over several time scales. Each paper reports the use that worked, on its own robot and data. We had one such model, trained for $3.30 of rented GPU time on our own arm, and wanted to know which of these uses we could build on. So we ran every use we could find on that one model. Each re-test is a row of a ∗ Code, data pointers and every number’s source: https://github. com/ravediamond/paper-jepa-world-model.

<!-- editlens paragraph 0.210 lines 49-75 -->
register with a pass mark, a dataset, a result and a verdict, and where we managed it, the threshold and the decision rule went into the repository before the result existed (that commit order is all we mean by pre-registration). Checked against the commit history, all 20 rows match a pre-registration record. In 19 the bar was committed before the result, and in 1 (the two-level hierarchical progress use) in the same commit. One row is not a use of our model: it times the pretrained RoboJEPA and VJEPA 2.1 encoders on our on-board computer [2, 3]. Of the 20 rows, 3 pass and 1 is met as predicted. Another 2 are not proven, and the remaining 14 fail or are no-go. The first draft of this paper argued something else. Our reading of the failures was that the latent mostly encodes the arm’s pose, so a frozen image encoder or the commanded joints would do at least as well in every one of them. We ran those controls on 69 policy rollouts before writing it up, and they did not bear it out: the encoder reads how the episode went better than either control. We rewrote the claim. At this data scale the predictor, not the encoder, is the weak link. One moment runs through the rest of the paper: the grasp anchor, 15 frames before the gripper first closes. There the current latent reads the outcome at 0.82 and the imagined latent at 0.70, and that gap is the argument in one row. The controls came after the data, which limits what they can show. Each readout is a linear probe fit with leave-one-session-out (LOSO) cross-validation on the 69 rollouts (44 success, 25 failure, 13 sessions), scored against labels the author gave at rest. The model was trained on teleoperation only and never saw these rollouts. No threshold was committed for these comparisons, so everything this paper says about the split between encoder and predictor is exploratory. Of the 3 register passes, 3 have their bar committed before the result, though the register marks the outcome-readout verdict as retrospective.

<!-- editlens chunk 0.070 lines 80-151 -->
<!-- editlens paragraph 0.122 lines 83-105 -->
is to put a bowl into another bowl. Our model is trained on ravediamond/so101_bowls_all_trimmed, split by grid layout into 157 training and 25 validation episodes. The evaluation rollouts come from a separate dataset, ravediamond/so101-bowls-policy-rollouts: SmolVLA [6] runs recorded after our model was trained. Our model follows the LeWM recipe [1], with a multiview ViT encoder, an action-conditioned predictor and the SIGReg regulariser. We set it beside four signals, each chosen because it is cheaper than a world model. The frozen DINOv2-S control is a frozen DINOv2 small encoder [7] mean-pooled over the top and wrist views (the design of DINO-WM [8]). The joints control is the commanded joint vector. The colour judge is a hand-built rule on the final frame with no learning, and policy identity is the checkpoint that ran the episode. In October, a timing test on the on-board computer loaded our checkpoint with strict=False. Under the transformers version on that image (5.5.4), 192 encoder tensors did not match and were silently dropped, so the test timed a random encoder. We voided its latents and traced how every other use loaded the model: 26 ran the trained model, 1 ran a random one (that test) and none is unknown. The world-model block of VLA-JEPA, which one diagnostic below uses, loads all 351 of its keys.

<!-- editlens paragraph 0.061 lines 144-151 -->
The test here is whether the encoder carries anything that a frozen encoder or the joints do not. Table 2 sets our model beside the four other signals on the same 69 rollouts. Every probe is a LOSO linear probe against the author’s labels. At rest the interval is a 95 % episodebootstrap CI; at the anchor it is a bootstrap of the mean over 5 seeds of the out-of-fold AUROC (episodes resampled jointly across the seeds, 2,000 resamples, percentile). At rest our model is level with the colour judge (the CIs overlap) and above the frozen encoder and the joints. At

### 3 The register (mean 0.136)

<!-- editlens chunk 0.104 lines 152-191 -->
<!-- editlens paragraph 0.078 lines 152-184 -->
the grasp anchor no judge applies, and our model leads both controls. Since the pose probes hold the joints betTable 1 lists the 20 uses and what each takes from our ter than our encoder does but the outcome worse, the enmodel: the encoder alone (7), the predictor (8) or both coder carries outcome information they lack, at least on (5). Read that column against the verdicts. these rollouts. Among the encoder uses, reading the outcome works The anchor column depends on how the five seeds and reading progress does not. The outcome readout at are combined. Averaging the predictions before scorrest passes, and at the grasp anchor the current latent ing gives 0.8377, 0.7175 and 0.5346 for our model, frozen reads the grasp at 0.82. All four uses that ask the latent DINOv2-S and the joints. Seed 0 alone gives 0.7554, for progress or task stage fail, from progress monotonic- 0.7024 and 0.5574, a smaller gap between our model and ity and two-level hierarchical progress [10] to the latent the frozen encoder. The order holds either way. stage tracker and SURVEYOR’s latent-distance scale [13]. One control does beat our model. On SURVEYOR’s The pose probes of LeJEPA [12] show some of what else scale check, frozen DINOv2-S (τ 0.3601) and the joints (τ it holds. A linear readout recovers about half of the joint 0.0265) pass where our model fails (τ 1.2488, against 0.20 variance from our encoder (R2 0.565), less than from the reported by SURVEYOR). The same task and the same frozen DINOv2-S control (0.867). rollouts pass with other features, so the failure points at The predictor does predict its own latent: at K = 30 the geometry of our latent space rather than at the task. its open-loop error is 0.31, against 0.89 for copying the The register’s own outcome-readout row reports 1.000. last latent. Every application of that prediction fails, and That number was scored against the colour judge’s labels, chunk ranking [1] shows why most clearly. It puts the ex- on 87 rollouts, so it partly measures agreement with the ecuted chunk first in 0.60 of anchors against a pass mark judge. Against the author’s labels on the 69 rollouts, with of 0.8, while the commanded actions alone reach 0.68– the controls beside it, the same readout gives 0.9545. 0.90, so the cheapest signal in the table beats the one built on imagination. The surprise monitor catches 2/8 at 2/42 failures. The rest (the hierarchical planner [14], the con- 5 Where the predictor fails formal surprise band, re-ranking, the risk head [11] and the calibrated reflex) miss their thresholds by the mar- ContactGuard [9] finds that probes on the imagined latent beat probes on the current one for grasp tasks, so gins in Table 1. we expected the imagined latent to help at our grasp anchor. The pre-registered threshold asked it for ≥ 0.85, ≥ github.com/ravediamond/paper-jepa-world-model · d067f64

<!-- editlens paragraph 0.159 lines 187-191 -->
Table 1: The register: every use of our world model re-tested here (with the frozen-DINOv2 and RoboJEPA rows beside it), what it takes from the model, whether its bar came before the result, and the verdict. Read the takes column against the verdict: the predictor uses fail. Bar, result and verdict are quoted from repro/register/expected/FEASIBILITY.md §2. use

<!-- editlens chunk 0.074 lines 555-637 -->
<!-- editlens paragraph 0.057 lines 555-581 -->
come information the encoder had. Our model’s inverse-dynamics term is no better than that of its own untrained network. On the distillation probe, pooled over the 25 teleoperation validation feature at rest grasp anchor (65 scored, 21 fail) episodes, the trained model scores 0.7476 and its ranour world model 0.9545 [0.9023, 0.9908] 0.8199 [0.7141, 0.9041] colour judge (no learning) 0.9432 [0.8919, 0.9878] — dom initialisation 0.7974, a difference of −0.0499 with a frozen DINOv2-S 0.8655 [0.7767, 0.9405] 0.7067 [0.5816, 0.8269] 95 % paired episode-bootstrap CI of [−0.7403, +0.6559] commanded joints 0.7573 [0.6084, 0.8880] 0.5305 [0.3709, 0.6855] policy identity 0.5882 [0.4084, 0.7515] — (gap5_pooled_rerun.json). The term itself is fragile: the same untrained network scored 1.4383 on one machine and 0.7974 and 0.8042 on two others (it is sensitive +0.05 over the current latent. With the same encoder and to the BLAS library and to ridge conditioning). the same anchor, the current latent reads the outcome at A low score can also come from a bug, so we 0.82 and the imagined one at 0.70. This pre-registered checked the surprise monitor’s failure-class AUROC row fails: on these rollouts, imagining forward loses out- (0.775, below its sanity bar) for one in loading or scorTable 2: Outcome AUROC of each signal on the same 69 rollouts (exploratory: controls chosen after the data). Look at the anchor column, where no judge applies.

<!-- editlens paragraph 0.233 lines 620-637 -->
ing. The same scorer reproduces the open-loop corruption ratios at K = 30: cross-episode 3.428 against 3.341 in the original run, constant-first 2.558 against 2.543 (M1_diag_g0_repro.json). The low AUROC is a real value. The predictor of VLA-JEPA barely uses its actions. At 5 anchors (Table 3, from M3_diag_action_shuffle.json), action tokens taken from another episode differ from the true ones by 21–28 % in relative L2 but move the loss by only about 0.05 %. Zeroing the tokens moves it by about 1.05 % on average, and the forward pass is deterministic. Its failure-class AUROC of 0.501, below the same sanity check, is therefore real, and we leave its table unread under the frozen bar. A reader may object that one pass in the register is predictive. In the anticipation step of the outcome-readout gate, the imagined latent beat policy identity by +0.179. That bar is retrospective, though, and the two reruns of the same idea with the threshold committed first, the grasp probe and the calibrated surprise reflex, both fail.

<!-- editlens chunk 0.240 lines 642-686 -->
<!-- editlens paragraph 0.253 lines 642-656 -->
LeWorldModel [1] trains the recipe we use end to end from pixels and plans with it in Push-T and in simulation. Its two planning uses fail on our arm. LeJEPA’s identifiability analysis [12] predicts that SIGReg latents identify the state up to anisotropy, which our pose probes support only in part. DINO-WM [8] plans on frozen DINOv2 [7] patches; our frozen control copies that design. V-JEPA 2.1 [3] and RoboJEPA [2] are too slow on our onboard computer, and timing them is the one register row that is not a use of our model. ContactGuard [9] is the result we contradict most directly. It finds imagined-latent probes better than current-latent ones on grasp tasks, and on our arm the reverse holds. The re-tests of ReAP’s action-conditioned risk [11], the hierarchical planners of HWM [14] and H-JEPA [10] and SURVEYOR’s latentdistance scale [13] also miss here, at this data scale. Two papers agree with us from the control side: SaiVLAJEPA [15] reports that a training-only future-latent head adds +0.03 points to control on 10,030 paired episodes, and HIJP [16] finds LeWM below goal-conditioned behaviour cloning in simulation.

<!-- editlens paragraph 0.211 lines 663-675 -->
The split between encoder and predictor is exploratory. Its probes were chosen after the data and fit on 69 rollouts labelled by a single operator, the author. Two things limit the risk. The model never saw these rollouts, and every probe is cross-validated by session. The confirming test is a fresh set of rollouts scored under a threshold committed first, which needs a day on the arm. Scale is the other open condition. All of this comes from one model at one data scale, and a second point at 653 episodes is costed and queued. Three controls were not run, because the surprise monitor and the imagined arm of the grasp probe would each need their own predictor (trained on frozen DINOv2-S features or on the joints) and progress monotonicity would need a reimplementation. In the register, the outcome-readout verdict is retrospective and the two-level hierarchical progress use has its bar in the same commit as its result; ordered by commit alone, without the audit, the register reads 13 barfirst and 6 same-commit rows.

<!-- editlens paragraph 0.266 lines 680-686 -->
A $3.30 world model and 69 policy rollouts were enough to sort 20 published uses into those this model supports and those it does not. At this data scale the encoder carries the outcome and the predictor adds nothing to it. Probe the encoder before building on the predictor, and keep the commanded actions as a baseline: here they ranked chunks better than imagination did.
