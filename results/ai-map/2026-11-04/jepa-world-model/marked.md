# paper-jepa-world-model: chunks in paper order

## rendered source (numbers filled)

### Abstract (mean 0.198)

<!-- editlens chunk 0.198 lines 7-7 -->
<!-- editlens paragraph 0.198 lines 7-7 -->
We trained a small JEPA world model in the LeWorldModel recipe on teleoperated demonstrations of one tabletop task on a low-cost SO-101 arm. Then we re-tested on it every use of such a model that we found in recent world-model papers, each under a bar fixed in a public register. In exploratory probes on policy rollouts the model never saw in training, a linear readout of the encoder's final-frame latent separates success from failure as well as a hand-built colour judge (AUROC 0.95 vs 0.94) and better than a frozen DINOv2 encoder, the commanded joints or the policy's identity. The predictor does not add to it. At the grasp, the imagined latent reads the outcome worse than the current one (0.70 vs 0.82), and every use that needs a multi-step rollout — chunk ranking, surprise monitoring, risk prediction — misses its bar. One rig, one model, one data scale.

### Introduction (mean 0.257)

<!-- editlens chunk 0.257 lines 11-17 -->
<!-- editlens paragraph 0.128 lines 11-11 -->
A world model in the sense of LeWorldModel (LeWM) [1] has two parts: an encoder that maps camera frames to a latent vector, and a predictor that, given the current latent and a sequence of actions, imagines the latents that follow. Both are trained together from pixels with a joint-embedding predictive (JEPA) loss. Papers built on such models propose *uses* of them: ranking a policy's candidate action chunks by their imagined outcome, flagging a failure when the observed latent departs from the predicted one, reading the outcome of a grasp before it happens, planning over several time scales. Each paper reports the use that worked, on its own robot and data.

<!-- editlens paragraph 0.189 lines 13-13 -->
We take the opposite view of one model. One arm, one task, one small JEPA world model — and on it, every use we could take from the literature. Each re-test is a row of a register: a bar written down before the result where we could, a dataset, a result and a verdict. Pre-registration here means only that. The bar and the decision rule are committed to the repository before the number exists. Audited against the commit history, all 20 rows match a pre-registration record; 19 bars were committed before their result and 1 in the same commit as its result (the two-level hierarchical progress use). One row, the on-device latency of the pretrained RoboJEPA and V-JEPA 2.1 encoders [2, 3], is not a use of our model. Of the 20 rows, 3 pass, 1 is met as predicted, 2 are not proven, and the remaining 14 fail or are no-go.

<!-- editlens paragraph 0.524 lines 15-15 -->
On the 69 rollouts, and in exploratory probes only, the result splits along the model. The *encoder* reads the episode's outcome from the current frame, better than a frozen foundation encoder or the robot's own joint commands, and it does so at the grasp anchor too, 15 frames before the gripper first closes. The *predictor*, which every forecasting use relies on, does not improve on that reading by imagining forward. The contribution is threefold: the register itself, with an audit of how every use loaded the checkpoint (Table 1); exploratory controls that separate encoder from predictor (Table 2, Fig. 1); and the exploratory reading that, at this data scale, the predictor is the weak link.

<!-- editlens paragraph 0.364 lines 17-17 -->
**Caveats stated up front.** The encoder readouts are linear probes fit with leave-one-session-out (LOSO) cross-validation on 69 rollouts (44 success / 25 failure, 13 sessions) with operator labels. The model was trained on teleoperation only and never saw these rollouts, but the controls were chosen after the data and are **exploratory**. Among the 3 passes, 3 have bars committed before the result, and the bar of the outcome-readout use was written retrospectively. Ordered by commit alone, without the audit, the register reads 13 bar-first and 6 same-commit.

### Setup (mean 0.235)

<!-- editlens chunk 0.235 lines 21-25 -->
<!-- editlens paragraph 0.117 lines 21-21 -->
**Robot and data.** The robot is one SO-101 arm [4] driven through LeRobot [5], with two cameras (top and wrist) and one task family: put a bowl into another bowl. The world model is trained on X (157 training and 25 validation episodes, split by grid layout). The evaluation rollouts are X, a separate dataset of SmolVLA [6] rollouts recorded after the world model was trained.

<!-- editlens paragraph 0.258 lines 23-23 -->
**Model.** Our world model, named W1 in the repository, follows the LeWM recipe [1]: a multi-view ViT encoder, an action-conditioned predictor and the SIGReg regulariser. It was trained on one rented GPU for $3.30. **Controls.** The frozen DINOv2-S control is a frozen DINOv2 small encoder [7], mean-pooled over the top and wrist views, the design of DINO-WM [8]. The joints control is the commanded joint vector. The colour judge is a hand-built rule on the final frame with no learning. The policy-identity control is the checkpoint that ran the episode.

<!-- editlens paragraph 0.348 lines 25-25 -->
**Load audit.** One early use loaded the checkpoint with X and so ran a random encoder. We therefore re-traced the load path of every use: 26 ran the trained model, 1 ran a random one (already voided) and none is unknown. The world-model block of VLA-JEPA, used in one diagnostic, loads 351 of 351 keys (0 missing).

### The register (mean 0.341)

<!-- editlens chunk 0.341 lines 29-58 -->
<!-- editlens paragraph 0.380 lines 56-56 -->
*Encoder reads.* The outcome readout at rest passes, with a retrospective bar; the current-latent arm of the grasp probe reads the grasp at the anchor (0.82). The pose probes [12] measure what else the latent holds: our encoder holds about half of the joint variance linearly (R² 0.565, against 0.867 for the frozen DINOv2-S control). Encoder uses that read progress or stage rather than outcome fail: progress monotonicity, two-level hierarchical progress [10], the latent stage tracker, and SURVEYOR's latent-distance scale [13] (τ 1.2488 against 0.20 in the paper).

<!-- editlens paragraph 0.354 lines 58-58 -->
*Predictor forecasts.* Open-loop prediction beats copying the last latent (0.31 vs 0.89 at K = 30): the predictor does predict its own latent. Every use of that prediction fails. Chunk ranking [1] reaches a top-1 accuracy of 0.60 against a bar of 0.8, while the commanded actions alone reach 0.68–0.90. The surprise monitor catches 2/8 at 2/42 failures. In the grasp probe the imagined latent (0.70) reads less than the current one. The hierarchical planner [14] shows no crossover, and the conformal surprise band, the re-ranking of chunk candidates, the action-conditioned risk head [11] and the calibrated surprise reflex all miss their bars.

### What the encoder knows (mean 0.309)

<!-- editlens chunk 0.309 lines 74-74 -->
<!-- editlens paragraph 0.309 lines 74-74 -->
In this exploratory comparison on the 69 rollouts, our world model is level with the colour judge at rest (the CIs overlap) and above the frozen encoder and the joints; at the grasp anchor, where no judge applies, it leads both controls. The anchor column depends on how the seeds are aggregated (exploratory): the AUROC of the 5-seed-averaged predictions is 0.8377 / 0.7175 / 0.5346 (ours / frozen DINOv2-S / joints), and seed 0 alone gives 0.7554 / 0.7024 / 0.5574, a smaller gap between our model and the frozen encoder; the ordering holds in both. The pose probes hold the joints better than our encoder does but the outcome worse, so on these rollouts the encoder holds outcome information they do not (exploratory). The original outcome-readout gate scored our model at 1.000, but against the colour judge's labels rather than the operator's, on 87 rollouts; the rerun here, on the 69 Orin rollouts against operator labels with the controls beside it, gives 0.9545.

### Where the predictor fails (mean 0.304)

<!-- editlens chunk 0.304 lines 78-92 -->
<!-- editlens paragraph 0.376 lines 78-78 -->
The cleanest contrast is the grasp probe, which ContactGuard [9] motivates: same encoder, same anchor, current latent 0.82 against imagined latent 0.70, where the bar was ≥ 0.85, ≥ +0.05 over the current latent. On these rollouts, imagining forward loses outcome information the encoder had; this pre-registered row fails, and the encoder/predictor reading built on it stays exploratory. On SURVEYOR's scale check, the frozen DINOv2-S control (τ 0.3601) and the joints (τ 0.0265) pass where our model fails, which points at our model's latent geometry rather than the task.

<!-- editlens paragraph 0.309 lines 80-80 -->
*Three further exploratory lines.* (1) On the inverse-dynamics term of the distillation probe (pooled, 25 teleoperation validation episodes), the trained model (0.7476) is not distinguishable from its own random initialisation (0.7974): the difference is −0.0499, with a 95 % paired episode-bootstrap CI of [−0.7403, +0.6559] (X). The term is sensitive to BLAS and ridge conditioning: the same untrained network scored 1.4383 on one machine and 0.7974 / 0.8042 on two others. (2) The surprise scorer that gives our model a failure-class AUROC of 0.775, below its sanity bar, reproduces the open-loop corruption ratios at K = 30 (cross-episode 3.428 vs 3.341, constant-first 2.558 vs 2.543; X), so that AUROC is a real value and not a load or scorer bug. (3) The predictor of VLA-JEPA is close to action-blind (exploratory, 5 anchors; Table 3): action tokens from another episode change the tokens by 21–28 % (relative L2) and the loss by about 0.05 %; zeroing the tokens changes the loss by about 1.05 % on average (|Δ| 0.4–2.2 %), and the forward pass is deterministic. Its failure-class AUROC of 0.501, below the same sanity bar, is therefore a real value, and its table stays unread under the frozen bar.

<!-- editlens paragraph 0.428 lines 92-92 -->
*Objection: the anticipation step of the outcome-readout gate is a predictive pass.* There the imagined latent beat policy identity by +0.179, but that bar is retrospective, and the two bar-first reruns of the same idea, the grasp probe and the calibrated surprise reflex, both fail.

### Related work (mean 0.236)

<!-- editlens chunk 0.236 lines 96-96 -->
<!-- editlens paragraph 0.236 lines 96-96 -->
LeWorldModel [1] trains the JEPA recipe we use end to end from pixels and plans with it in Push-T and in simulation; its planning uses fail here (chunk ranking, re-ranking). The identifiability analysis of LeJEPA [12] predicts that SIGReg latents identify the state up to anisotropy, which holds here partially. DINO-WM [8] plans on frozen DINOv2 [7] patches, the design of our frozen control. V-JEPA 2.1 [3] and RoboJEPA [2] are too slow on our on-board computer. ContactGuard [9] finds that imagined-latent probes beat current-latent ones on grasp tasks; we find the opposite. ReAP [11] predicts action-conditioned risk, and its re-test misses its bar here, as do the hierarchical planners of HWM [14] and H-JEPA [10] and the latent-distance scale of SURVEYOR [13]. Two results agree with ours from the control side: SaiVLA-JEPA [15] finds that a training-only future-latent head adds +0.03 points to control on 10,030 paired episodes, and HIJP [16] finds LeWM below goal-conditioned behaviour cloning in simulation.

### Limitations (mean 0.299)

<!-- editlens chunk 0.299 lines 100-100 -->
<!-- editlens paragraph 0.299 lines 100-100 -->
The controls are exploratory: 69 rollouts, operator labels, probes chosen after the data. Fresh rollouts scored under a bar committed first are the test, and until it runs every statement of the encoder/predictor split above is exploratory. One rig, one model, one data scale: a second scale point (653 episodes) is costed and queued separately, and the scale curve belongs to a longer version. Not run: the surprise monitor and the imagined-latent grasp probe with the frozen DINOv2-S control or the joints (each needs its own predictor), and progress monotonicity with the controls (it needs a reimplementation). The bar of the outcome-readout use is retrospective, and the one same-commit bar is that of the two-level hierarchical progress use.

### Conclusion (mean 0.342)

<!-- editlens chunk 0.342 lines 104-104 -->
<!-- editlens paragraph 0.342 lines 104-104 -->
On a small teleoperation dataset, a JEPA world model learns an encoder that reads how the episode went, a short horizon ahead included — and, in exploratory probes on the 69 rollouts, a predictor whose imagination adds nothing to that reading. One habit made this visible. We report every pre-registered use, not the best one.

### (figure and table captions) (mean 0.097)

<!-- editlens chunk 0.097 lines 31-82 -->
<!-- editlens paragraph 0.118 lines 31-31 -->
Table 1: The register: every pre-registered use of our world model (and the frozen-DINOv2 and RoboJEPA rows beside it), the paper it re-tests, what it takes from the model, whether the bar was committed before the result (audited against the commit history), the bar, the result and the verdict. Bar, result and verdict are quoted from repro/register/expected/FEASIBILITY.md §2 with the model names made plain; the code names the repro folder.

<!-- editlens paragraph 0.067 lines 62-62 -->
Table 2: Outcome AUROC on the same 69 rollouts. Exploratory (controls chosen after the data), LOSO linear probes, operator labels. At rest: 95 % episode-bootstrap CI. At the anchor: 95 % episode-bootstrap CI on the mean over 5 seeds of the out-of-fold AUROC (episodes resampled jointly across the seeds, 2,000 resamples, percentile).

<!-- editlens paragraph 0.088 lines 82-82 -->
Table 3: VLA-JEPA world-model loss at 5 anchors with the true action tokens, tokens from another episode (Δ shuffled) and zeroed tokens; the token change is the relative L2 of the shuffled tokens. Exploratory, a spot check, not a power analysis. Source: repro/gaps/expected/M3_diag_action_shuffle.json.

## built PDF

### Abstract (mean 0.184)

<!-- editlens chunk 0.184 lines 10-21 -->
<!-- editlens paragraph 0.184 lines 10-21 -->
We trained a small JEPA world model in the LeWorldModel recipe on teleoperated demonstrations of one tabletop task on a low-cost SO-101 arm, and re-tested on it every use of such a model that we found in recent world-model papers, each under a bar fixed in a public register. In exploratory probes on policy rollouts the model never saw in training, a linear readout of the encoder’s final-frame latent separates success from failure as well as a hand-built colour judge (AUROC 0.95 vs 0.94) and better than a frozen DINOv2 encoder, the commanded joints or the policy’s identity. The predictor does not add to it: at the grasp, the imagined latent reads the outcome worse than the current one (0.70 vs 0.82), and every use that needs a multi-step rollout, from chunk ranking to surprise monitoring and risk prediction, misses its bar. One rig, one model, one data scale.

### 1 Introduction (mean 0.125)

<!-- editlens chunk 0.125 lines 23-78 -->
<!-- editlens paragraph 0.121 lines 23-42 -->
A world model in the sense of LeWorldModel (LeWM) [1] has two parts: an encoder that maps camera frames to a latent vector, and a predictor that, given the current latent and a sequence of actions, imagines the latents that follow. Both are trained together from pixels with a joint-embedding predictive (JEPA) loss. Papers built on such models propose uses of them: ranking a policy’s candidate action chunks by their imagined outcome, flagging a failure when the observed latent departs from the predicted one, reading the outcome of a grasp before it happens, planning over several time scales. Each paper reports the use that worked, on its own robot and data. We take the opposite view of one model. We trained a single small JEPA world model on one arm and one task, and re-tested on it every use we could take from the literature. Each re-test is a row of a register: a bar written down before the result where we could, a dataset, a result and a ∗ Code, data pointers and every number’s source: https://github. com/ravediamond/paper-jepa-world-model.

<!-- editlens paragraph 0.220 lines 45-78 -->
verdict. Pre-registration here means only that: the bar and the decision rule are committed to the repository before the number exists. Audited against the commit history, all 20 rows match a pre-registration record; 19 bars were committed before their result and 1 in the same commit as its result (the two-level hierarchical progress use). One row, the on-device latency of the pretrained RoboJEPA and V-JEPA 2.1 encoders [2, 3], is not a use of our model. Of the 20 rows, 3 pass, 1 is met as predicted, 2 are not proven, and the remaining 14 fail or are no-go. On the 69 rollouts, and in exploratory probes only, the result splits along the model. The encoder reads the episode’s outcome from the current frame, better than a frozen foundation encoder or the robot’s own joint commands, and it does so at the grasp anchor too, 15 frames before the gripper first closes. The predictor, which every forecasting use relies on, does not improve on that reading by imagining forward. The contribution is threefold: the register itself, with an audit of how every use loaded the checkpoint (Table 1); exploratory controls that separate encoder from predictor (Table 2, Fig. 1); and the exploratory reading that, at this data scale, the predictor is the weak link. Caveats stated up front. The encoder readouts are linear probes fit with leave-one-session-out (LOSO) cross-validation on 69 rollouts (44 success / 25 failure, 13 sessions) with operator labels. The model was trained on teleoperation only and never saw these rollouts, but the controls were chosen after the data and are exploratory. Among the 3 passes, 3 have bars committed before the result, and the bar of the outcome-readout use was written retrospectively. Ordered by commit alone, without the audit, the register reads 13 bar-first and 6 same-commit.

### 2 Setup (mean 0.030)

<!-- editlens chunk 0.030 lines 80-110 -->
<!-- editlens paragraph 0.069 lines 80-90 -->
Robot and data. The robot is one SO-101 arm [4] driven through LeRobot [5], with two cameras (top and wrist) and one task family: put a bowl into another bowl. The world model is trained on ravediamond/so101_bowls_all_trimmed (157 training and 25 validation episodes, split by grid layout). The evaluation rollouts are ravediamond/so101-bowls-policy-rollouts, a

<!-- editlens paragraph 0.038 lines 93-110 -->
separate dataset of SmolVLA [6] rollouts recorded after the world model was trained. Model. Our world model, named W1 in the repository, follows the LeWM recipe [1]: a multi-view ViT encoder, an actionconditioned predictor and the SIGReg regulariser. It was trained on one rented GPU for $3.30. Controls. The frozen DINOv2-S control is a frozen DINOv2 small encoder [7], mean-pooled over the top and wrist views, the design of DINO-WM [8]. The joints control is the commanded joint vector. The colour judge is a hand-built rule on the final frame with no learning. The policy-identity control is the checkpoint that ran the episode. Load audit. One early use loaded the checkpoint with strict=False and so ran a random encoder. We therefore re-traced the load path of every use: 26 ran the trained model, 1 ran a random one (already voided) and none is unknown. The world-model block of VLA-JEPA, used in one diagnostic, loads 351 of 351 keys (0 missing).

### 3 The register (mean 0.299)

<!-- editlens chunk 0.299 lines 112-128 -->
<!-- editlens paragraph 0.299 lines 112-128 -->
Table 1 lists the 20 uses with what each takes from the model: the encoder alone (7), the predictor (8) or both (5). Encoder reads. The outcome readout at rest passes, with a retrospective bar; the current-latent arm of the grasp probe reads the grasp at the anchor (0.82). The pose probes [12] measure what else the latent holds: our encoder holds about half of the joint variance linearly (R2 0.565, against 0.867 for the frozen DINOv2-S control). Encoder uses that read progress or stage rather than outcome fail: progress monotonicity, two-level hierarchical progress [10], the latent stage tracker, and SURVEYOR’s latent-distance scale [13] (τ 1.2488 against 0.20 in the paper). Predictor forecasts. Open-loop prediction beats copying the last latent (0.31 vs 0.89 at K = 30): the predictor does predict its own latent. Every use of that prediction fails. Chunk ranking [1] reaches a top-1 accuracy of 0.60 against a bar of 0.8, while the commanded actions alone reach 0.68–0.90. The surprise monitor catches 2/8 at 2/42 failures. In the grasp probe the imagined latent (0.70) reads less than the current one. The hierarchical planner [14] shows no crossover, and the conformal surprise band, the re-ranking of chunk candidates, the action-conditioned risk head [11] and the calibrated surprise reflex all miss their bars.

### 4 What the encoder knows (mean 0.164)

<!-- editlens chunk 0.164 lines 130-185 -->
<!-- editlens paragraph 0.219 lines 130-137 -->
In this exploratory comparison on the 69 rollouts, our world model is level with the colour judge at rest (the CIs overlap) and above the frozen encoder and the joints; at the grasp anchor, where no judge applies, it leads both controls. The anchor column depends on how the seeds are aggregated (exploratory): the AUROC of the 5-seed-averaged predictions is 0.8377 / 0.7175 / 0.5346

<!-- editlens paragraph 0.162 lines 170-185 -->
Figure 1: The controls table as a dot plot. Left: AUROC at rest with its 95 % bootstrap CI. Right: AUROC at the grasp anchor, mean of 5 seeds with the seed range (not a CI). Exploratory, LOSO, operator labels. (ours / frozen DINOv2-S / joints), and seed 0 alone gives 0.7554 / 0.7024 / 0.5574, a smaller gap between our model and the frozen encoder; the ordering holds in both. The pose probes hold the joints better than our encoder does but the outcome worse, so on these rollouts the encoder holds outcome information they do not (exploratory). The original outcome-readout gate scored our model at 1.000, but against the colour judge’s labels rather than the operator’s, on 87 rollouts; the rerun here, on the 69 Orin rollouts against operator labels with the controls beside it, gives 0.9545.

### 5 Where the predictor fails (mean 0.177)

<!-- editlens chunk 0.177 lines 187-619 -->
<!-- editlens paragraph 0.336 lines 187-208 -->
The cleanest contrast is the grasp probe, which ContactGuard [9] motivates: same encoder, same anchor, current latent 0.82 against imagined latent 0.70, where the bar was ≥ 0.85, ≥ +0.05 over the current latent. On these rollouts, imagining forward loses outcome information the encoder had; this pre-registered row fails, and the encoder/predictor reading built on it stays exploratory. On SURVEYOR’s scale check, the frozen DINOv2-S control (τ 0.3601) and the joints (τ 0.0265) pass where our model fails, which points at our model’s latent geometry rather than the task. Three further exploratory lines. (1) On the inverse-dynamics term of the distillation probe (pooled, 25 teleoperation validation episodes), the trained model (0.7476) is not distinguishable from its own random initialisation (0.7974): the difference is −0.0499, with a 95 % paired episode-bootstrap CI of [−0.7403, +0.6559] (gap5_pooled_rerun.json). The term is sensitive to BLAS and ridge conditioning: the same untrained network scored 1.4383 on one machine and 0.7974 / 0.8042 on two others. (2) The surprise scorer that gives our model a failure-class AUROC of 0.775, below its sanity bar, reproduces the open-loop corruption ratios at K = 30 (cross-episode 3.428 vs 3.341, constant-first 2.558 vs 2.543; M1_diag_g0_repro.json), so that AUROC is a real value and not a load or scorer bug. (3) The predictor of VLA-JEPA is close to action-blind (exploratory, 5 anchors; Table 3): action tokens from another episode

<!-- editlens paragraph 0.108 lines 211-216 -->
Table 1: The register: every pre-registered use of our world model (and the frozen-DINOv2 and RoboJEPA rows beside it), the paper it re-tests, what it takes from the model, whether the bar was committed before the result (audited against the commit history), the bar, the result and the verdict. Bar, result and verdict are quoted from repro/register/expected/FEASIBILITY.md §2 with the model names made plain; the code names the repro folder. use

<!-- editlens paragraph 0.088 lines 580-586 -->
Table 2: Outcome AUROC on the same 69 rollouts. Exploratory (controls chosen after the data), LOSO linear probes, operator labels. At rest: 95 % episode-bootstrap CI. At the anchor: 95 % episode-bootstrap CI on the mean over 5 seeds of the out-of-fold AUROC (episodes resampled jointly across the seeds, 2,000 resamples, percentile). feature

<!-- editlens paragraph 0.272 lines 611-619 -->
change the tokens by 21–28 % (relative L2) and the loss by about 0.05 %; zeroing the tokens changes the loss by about 1.05 % on average (|Δ| 0.4–2.2 %), and the forward pass is deterministic. Its failure-class AUROC of 0.501, below the same sanity bar, is therefore a real value, and its table stays unread under the frozen bar. Objection: the anticipation step of the outcome-readout gate is a predictive pass. There the imagined latent beat policy identity by +0.179, but that bar is retrospective, and the two barfirst reruns of the same idea, the grasp probe and the calibrated surprise reflex, both fail.

### 6 Related work (mean 0.224)

<!-- editlens chunk 0.224 lines 661-676 -->
<!-- editlens paragraph 0.224 lines 661-676 -->
LeWorldModel [1] trains the JEPA recipe we use end to end from pixels and plans with it in Push-T and in simulation; its planning uses fail here (chunk ranking, re-ranking). The identifiability analysis of LeJEPA [12] predicts that SIGReg latents identify the state up to anisotropy, which holds here partially. DINO-WM [8] plans on frozen DINOv2 [7] patches, the design of our frozen control. V-JEPA 2.1 [3] and RoboJEPA [2] are too slow on our on-board computer. ContactGuard [9] finds that imagined-latent probes beat current-latent ones on grasp tasks; we find the opposite. ReAP [11] predicts action-conditioned risk, and its re-test misses its bar here, as do the hierarchical planners of HWM [14] and H-JEPA [10] and the latent-distance scale of SURVEYOR [13]. Two results agree with ours from the control side: SaiVLA-JEPA [15] finds that a training-only future-latent head adds +0.03 points to control on 10,030 paired episodes, and HIJP [16] finds LeWM below goalconditioned behaviour cloning in simulation.

### 7 Limitations (mean 0.273)

<!-- editlens chunk 0.273 lines 678-686 -->
<!-- editlens paragraph 0.273 lines 678-686 -->
The controls are exploratory: 69 rollouts, operator labels, probes chosen after the data. Fresh rollouts scored under a bar committed first are the test, and until it runs every statement of the encoder/predictor split above is exploratory. One rig, one model, one data scale: a second scale point (653 episodes) is costed and queued separately, and the scale curve belongs to a longer version. Not run: the surprise monitor and the imaginedlatent grasp probe with the frozen DINOv2-S control or the joints (each needs its own predictor), and progress monotonicity with the controls (it needs a reimplementation). The bar of the outcome-readout use is retrospective, and the one same-commit bar is that of the two-level hierarchical progress use.

### 8 Conclusion (mean 0.095)

<!-- editlens chunk 0.062 lines 688-731 -->
<!-- editlens paragraph 0.074 lines 694-731 -->
[2] Artem Zholus, Nicolas Beltran-Velez, Jianhao Yuan, Sarath Chandar, Tushar Nagarajan, Daniel Severo, Koustuv Sinha, Michal Drozdzal, Adriana Romero Soriano, Jeannette Bohg, Nicolas Ballas, and Mahmoud Assran. RoboJEPA: Scaling robotic latent world models. arXiv preprint arXiv:2610.10515, 2026. [3] Lorenzo Mur-Labadia, Matthew Muckley, Amir Bar, Mido Assran, Koustuv Sinha, Mike Rabbat, Yann LeCun, Nicolas Ballas, and Adrien Bardes. V-JEPA 2.1: Unlocking dense features in video self-supervised learning. arXiv preprint arXiv:2603.14482, 2026. [4] TheRobotStudio and Hugging Face. SO-ARM100 / SO-101: Standard open arm. https://github. com/TheRobotStudio/SO-ARM100, 2025. [5] Remi Cadene, Simon Alibert, Alexander Soare, et al. LeRobot: State-of-the-art machine learning for real-world robotics in PyTorch. https://github. com/huggingface/lerobot, 2024. Not in the paper library. [6] Mustafa Shukor, Dana Aubakirova, Francesco Capuano, Pepijn Kooijmans, Steven Palma, Adil Zouitine, Michel Aractingi, Caroline Pascal, Martino Russi, Andres Marafioti, Simon Alibert, Matthieu Cord, Thomas Wolf, and Remi Cadene. SmolVLA: A vision-language-action model for affordable and eﬀicient robotics. arXiv preprint arXiv:2506.01844, 2025. [7] Maxime Oquab, Timothée Darcet, Théo Moutakanni, et al. DINOv2: Learning robust visual features without supervision. arXiv preprint arXiv:2304.07193, 2023. Not in the paper library. [8] Gaoyue Zhou, Hengkai Pan, Yann LeCun, and Lerrel Pinto. DINO-WM: World models on pre-trained visual features enable zero-shot planning. arXiv preprint arXiv:2411.04983, 2024. [9] Gehan Zheng, Matthew Johnson-Roberson, and Weiming Zhi. ContactGuard: Pre-contact execution monitoring with action-conditioned latent world models. arXiv preprint arXiv:2608.13438, 2026.

<!-- editlens chunk 0.146 lines 734-758 -->
<!-- editlens paragraph 0.146 lines 734-758 -->
[10] Wancong Zhang, Basile Terver, Michael Rabbat, Yann LeCun, and Randall Balestriero. H-JEPA: Endto-end learning of hierarchical world models for visual planning. arXiv preprint arXiv:2610.06805, 2026. [11] Jingyuan Liu, Yunpeng Qing, Changxu Wei, and Zhi Hou. ReAP: From visual failure recognition to action-conditioned risk prediction for runtime failure monitoring. arXiv preprint arXiv:2610.16309, 2026. [12] David Klindt, Yann LeCun, and Randall Balestriero. When does LeJEPA learn a world model? arXiv preprint arXiv:2605.26379, 2026. [13] Anonymous. SURVEYOR: Certified speculative plan consumption for latent world-model planning, 2026. NeurIPS 2026 submission; no arXiv identifier known. [14] Wancong Zhang, Basile Terver, Artem Zholus, Soham Chitnis, Harsh Sutaria, Mido Assran, Randall Balestriero, Amir Bar, Yann LeCun, and Nicolas Ballas. Hierarchical planning with latent world models. arXiv preprint arXiv:2604.03208, 2026. [15] Rufeng Xiao, Ruihao Xiao, Wei Chen, and Xinhai Sun. SaiVLA-JEPA: Evaluating future latent prediction in JEPA-conditioned VLA control. arXiv preprint arXiv:2610.38508, 2026. [16] HIJP authors. HIJP (arxiv:2610.23615). arXiv preprint arXiv:2610.23615, 2026. arXiv:2610.23615. Not in the paper library: authors and title to confirm from the PDF.
