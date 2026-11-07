# paper-register-reproducibility: chunks in paper order

## rendered source (numbers filled)

### Abstract (mean 0.296)

<!-- editlens chunk 0.296 lines 7-7 -->
<!-- editlens paragraph 0.296 lines 7-7 -->
We re-tested the main claims of new robot-learning papers on an SO-101 arm with a Jetson Orin NX. The pieces cost €1,350 and the compute $45.10. Each re-test ran the cheapest baseline first, and its pass mark was committed before the run. Of the 37 paper claims we tested, 12 were valid on our hardware. Three proposed classes cover the failures: edge latency (a method misses the real-time budget on the edge GPU), zero-shot judges (a judge loses to a trivial signal) and latent planners (a planner loses to the commanded joints). A blind second reader still has to confirm the classes. We also verified our own pre-registration by commit history. For most gates the order of bar and result can be read from the repository, and for some it cannot.

### 1. The register (mean 0.127)

<!-- editlens chunk 0.127 lines 11-19 -->
<!-- editlens paragraph 0.166 lines 11-11 -->
Most of the 22 papers in this study were shown on setups far from ours. 9 were shown in simulation and 7 on rigs above X5k, which is where our rig falls. The appendix table gives the rig of each paper, including the 3 in between and the 1 that does not say. Our rig is an SO-101 arm and a Jetson Orin NX 16 GB.

<!-- editlens paragraph 0.141 lines 13-13 -->
The register grew out of our own write-ups. Each re-test on this rig was published with its data, and there are 29 so far. This paper collects them in one table and audits how the table was kept.

<!-- editlens paragraph 0.141 lines 15-15 -->
Here is one entry. An adaptive chunking paper claims that choosing the chunk length from the entropy of sampled chunks follows the task's phases, long in transport and short at the grasp. On our edge GPU one such decision takes 4,751 ms. The budget is 298 ms. The entry records a fail on this rig. It says nothing about the method on the hardware it was shown on. Next to the verdict, the entry keeps the claim in the paper's words, our pass mark, our measurement and the published rows.

<!-- editlens paragraph 0.085 lines 17-17 -->
For each claim we first run the cheapest signal the learned model has to beat, on the same rows. For a predictor this is copy-last. For a latent it is the commanded joints. For a judge it is episode length.

### 2. Auditing our own pre-registration (mean 0.130)

<!-- editlens chunk 0.130 lines 23-75 -->
<!-- editlens paragraph 0.128 lines 23-23 -->
A gate's pass mark had to be in version control before its result. Notes and commit dates can be edited by hand. Commit ancestry cannot be changed without rewriting history that others have already cloned. For each gate we find the first commit that contains its bar and the first that contains its result, and compare them (X, abridged):

<!-- editlens paragraph 0.074 lines 37-37 -->
Table 1 gives the classes for the 89 gates logged by 2026-10-31. Most are bar-first and 0 are result-first. A same-commit gate is one where bar and result entered the repository together. It says nothing about which was written first.

<!-- editlens paragraph 0.193 lines 51-51 -->
Our first pass used text search and found 31 same-commit gates. The cause was batch logging. We traced each same-commit gate back to the earlier file that holds its bar. This moved 21 gates to bar-first and 4 to no-bar, because their bar cell declares none. 6 stayed same-commit. The audit table in the repository gives the evidence line for every move. We did not re-audit the gates that were already bar-first. One open candidate remains, the reward-model progress test of 2026-11-01. It is same-commit by text search, although its protocol (X) is older than the log commit.

<!-- editlens paragraph 0.190 lines 53-53 -->
The early gates mixed point estimates and different intervals. We recomputed 10 of them from stored rows with one statistic, the episode bootstrap (2,000 resamples, percentile 95 % CI). For 3 of them the bar falls inside the interval (Table 2). The colour judge is a fail on the point estimate, and its interval does not settle it. The false-intervention threshold was fitted to meet its rate, so that interval is only descriptive. The register keeps the pre-registered point verdicts and marks these three as fragile.

<!-- editlens paragraph 0.253 lines 75-75 -->
The cold reruns start from a fresh clone with no credentials. 6 gates reran and matched, 5 of them exactly. 12 more stop at the world-model environment, which is not published yet. Publishing it would unblock most of them. The remaining 11 need a larger GPU, a private checkpoint, the arm or a step the write-up leaves out. We checked the register's citations and paper-side fields against the papers' PDFs and corrected them. The register names 38 arXiv ids. The ones missing from our papers mirror all belong to scheduled tests. One tested paper has no arXiv id and was not checked against a PDF.

### 3. Results (mean 0.162)

<!-- editlens chunk 0.162 lines 79-79 -->
<!-- editlens paragraph 0.162 lines 79-79 -->
Table 3 counts the verdicts by paper and by claim row. On claims taken from papers, 12 of 37 reproduce and 18 fail. The other 8 rows test our own baselines, for example that the commanded joints beat the world model. 5 of those hold.

### 4. Three failure classes (mean 0.270)

<!-- editlens chunk 0.270 lines 94-98 -->
<!-- editlens paragraph 0.253 lines 96-96 -->
In other entries a model judged outcomes without training on this rig. A learned reward model detects failures at AUROC 0.818. Episode length alone reaches 0.938. Judges of success, failure or progress that lose to a trivial signal like this form class B. Class C is about learned latents. A world model ranks the executed chunk first in 0.60 of anchors. Its pass mark was 0.8, and an action-only baseline reaches 0.68–0.90. Class C holds latents used to plan, rank or track progress that lose to the joints, to copy-last or to an action-only baseline.

<!-- editlens paragraph 0.163 lines 98-98 -->
These examples illustrate the classes. They do not count them. A protocol committed before any labelling sets the rule for counting. The labels count only once a blind second reader labels the same 20 failed rows on the same form and agrees with the first reading at Cohen's κ ≥ 0.6. That reading has not happened yet.

### 5. Limitations (mean 0.274)

<!-- editlens chunk 0.274 lines 102-102 -->
<!-- editlens paragraph 0.274 lines 102-102 -->
One operator, the author, ran the rig and labelled the outcomes. Labels were given at rest and not always blind to the arm. Observer bias is therefore the main confound. Where commit order shows it, the pass mark predates the run, so a label could not move the bar. A blind two-reader protocol for the failure classes is committed. It has not run yet, so no verdict has a second reader. For 29 of the 89 gates the repository cannot show whether bar or result came first. 21 of the bar-first verdicts rest on matching a bar text in an earlier file. Under the bootstrap 3 verdicts are fragile. Cold reruns cover 6 gates so far, and the unpublished world-model environment blocks most of the rest. A failure here describes this rig, not the paper in its own setting. The papers were chosen for one stack, so the rate describes this register and not the field.

### 6. Related work (mean 0.291)

<!-- editlens chunk 0.291 lines 106-106 -->
<!-- editlens paragraph 0.291 lines 106-106 -->
Two works use the same arm to evaluate policies. A standardized real-world benchmark reports a taxonomy of failures and recoveries for VLA policies [arXiv:2606.08881]. A fleet of SO-101 cells evaluates policies at scale [arXiv:2607.24481]. The vla-eval tool runs VLAs across 14 simulation benchmarks [arXiv:2603.13966]. A benchmark of demonstration quality studies one method family [arXiv:2610.18869]. We test the claims behind methods (judges, world models, latency) against thresholds fixed before the run, and we audit our own pre-registration. RoboSeed [arXiv:2610.40026] is the closest work. It scores VLA and world-action models on five dimensions, including reproduction evidence and deployment affordability. Its reproduction-evidence score counts five audit milestones (configuration mapping, task records, task coverage, training records, seeds). Its authors state that this score is not a probability that a result is correct. We give one pass or fail per claim on a €1,350 rig.

### 7. Conclusion (mean 0.247)

<!-- editlens chunk 0.247 lines 110-110 -->
<!-- editlens paragraph 0.247 lines 110-110 -->
We re-tested 37 paper claims, and 12 held. The rig cost €1,350 and the compute $45.10. Every row behind the verdicts is published. Our own history cannot show the order of bar and result for 29 of 89 gates. If you re-test a paper on a cheap rig, run its cheapest baseline on the same rows first and commit the threshold before the run. Every number here can be rebuilt from the repository (X).

### (figure and table captions) (mean 0.126)

<!-- editlens chunk 0.126 lines 39-116 -->
<!-- editlens paragraph 0.118 lines 116-116 -->
Table 4: The register, one row per paper, generated from the register file (internal model and gate names kept). The rig price of €1,350 counts the parts with a stated price; 2 small parts are not priced yet. Read the verdict column against the rig each paper was shown on.

## built PDF

### (front matter) (mean 0.171)

<!-- editlens chunk 0.171 lines 3-12 -->
<!-- editlens paragraph 0.171 lines 3-12 -->
What survives when a paper leaves the lab: re-testing 22 robot-learning papers on a €1,350 rig, and auditing our own pre-registration Ravindu Somawansa Shisso Robotics ravindu.somawansa@shissorobotics.com∗ the entry keeps the claim in the paper’s words, our pass mark, our measurement and the published rows. For each claim we first run the cheapest signal the

### Abstract (mean 0.126)

<!-- editlens chunk 0.126 lines 13-33 -->
<!-- editlens paragraph 0.126 lines 13-33 -->
learned model has to beat, on the same rows. For a predictor this is copy-last. For a latent it is the commanded We re-tested the main claims of new robot-learning pa- joints. For a judge it is episode length. pers on an SO-101 arm with a Jetson Orin NX. The pieces We chose the papers for the stack this rig runs (world cost €1,350 and the compute $45.10. Each re-test ran the models, VLA policies, failure monitors, chunking, edge cheapest baseline first, and its pass mark was committed latency). Each one went into the register before its test. before the run. Of the 37 paper claims we tested, 12 were The register file lists the papers scheduled next. valid on our hardware. Three proposed classes cover the failures: edge latency (a method misses the real-time budget on the edge GPU), zero-shot judges (a judge loses 2 Auditing our own pre-registration to a trivial signal) and latent planners (a planner loses to the commanded joints). A blind second reader still A gate’s pass mark had to be in version control before has to confirm the classes. We also verified our own pre- its result. Notes and commit dates can be edited by registration by commit history. For most gates the order hand. Commit ancestry cannot be changed without of bar and result can be read from the repository, and for rewriting history that others have already cloned. For each gate we find the first commit that contains its bar some it cannot. and the first that contains its result, and compare them (repro/prereg-check/scripts/prereg_audit.py, abridged):

### 1 The register (mean 0.152)

<!-- editlens chunk 0.152 lines 34-213 -->
<!-- editlens paragraph 0.184 lines 34-48 -->
Most of the 22 papers in this study were shown on setups far from ours. 9 were shown in simulation and 7 on rigs above $20k. 2 used a setup under $5k, which is where our rig falls. The appendix table gives the rig of each paper, including the 3 in between and the 1 that does not say. Our rig is an SO-101 arm and a Jetson Orin NX 16 GB. The register grew out of our own write-ups. Each retest on this rig was published with its data, and there are 29 so far. This paper collects them in one table and audits how the table was kept. Here is one entry. An adaptive chunking paper claims that choosing the chunk length from the entropy of sampled chunks follows the task’s phases, long in transport and short at the grasp. On our edge GPU one such decision takes 4,751 ms. The budget is 298 ms. The entry records a fail on this rig. It says nothing about the method on the hardware it was shown on. Next to the verdict,

<!-- editlens paragraph 0.088 lines 59-75 -->
Table 1 gives the classes for the 89 gates logged by 2026-10-31. Most are bar-first and 0 are result-first. A same-commit gate is one where bar and result entered the repository together. It says nothing about which was written first. Our first pass used text search and found 31 samecommit gates. The cause was batch logging. We traced each same-commit gate back to the earlier file that holds its bar. This moved 21 gates to bar-first and 4 to nobar, because their bar cell declares none. 6 stayed samecommit. The audit table in the repository gives the evi∗ Every with source number its file: dence line for every move. We did not re-audit the gates github.com/ravediamond/paper-register-reproducibility. that were already bar-first. One open candidate remains, github.com/ravediamond/paper-register-reproducibility · a49a1e6

<!-- editlens paragraph 0.117 lines 153-171 -->
the reward-model progress test of 2026-11-01. It is samecommit by text search, although its protocol (6241570) is older than the log commit. The early gates mixed point estimates and different intervals. We recomputed 10 of them from stored rows with one statistic, the episode bootstrap (2,000 resamples, percentile 95 % CI). For 3 of them the bar falls inside the interval (Table 2). The colour judge is a fail on the point estimate, and its interval does not settle it. The false-intervention threshold was fitted to meet its rate, so that interval is only descriptive. The register keeps the pre-registered point verdicts and marks these three as fragile. All 29 write-ups rebuild from their published rows. The check for the cold reruns prints: $ python3 repro/cold-reproduction/l0_check.py ok posts: 29 (report 29) ok L0 PASS: 29 (report 29) ok L1 REPRO: 6 (report 6) ok L1 DIFF: 0 (report 0) ok L1 classes: {'REPRO': 6, —'': 3, 'SKIP': 8, 'FAIL-ENV': 12} L0 PASS

<!-- editlens paragraph 0.310 lines 207-213 -->
The adaptive chunking entry of §1 misses the real-time budget on the edge GPU. The method may work on faster hardware. We call this kind of failure class A, the clock. In other entries a model judged outcomes without training on this rig. A learned reward model detects failures at AUROC 0.818. Episode length alone reaches

### 0.938. Judges of success, failure or progress that lose to (mean 0.250)

<!-- editlens chunk 0.250 lines 214-251 -->
<!-- editlens paragraph 0.270 lines 214-225 -->
a trivial signal like this form class B. Class C is about learned latents. A world model ranks the executed chunk first in 0.60 of anchors. Its pass mark was 0.8, and an action-only baseline reaches 0.68–0.90. Class C holds latents used to plan, rank or track progress that lose to the joints, to copy-last or to an action-only baseline. These examples illustrate the classes. They do not count them. A protocol committed before any labelling sets the rule for counting. The labels count only once a blind second reader labels the same 20 failed rows on the same form and agrees with the first reading at Cohen’s κ ≥ 0.6. That reading has not happened yet.

<!-- editlens paragraph 0.285 lines 230-239 -->
The cold reruns start from a fresh clone with no credentials. 6 gates reran and matched, 5 of them exactly. 12 more stop at the world-model environment, which is not published yet. Publishing it would unblock most of them. The remaining 11 need a larger GPU, a private checkpoint, the arm or a step the write-up leaves out. We checked the register’s citations and paper-side fields against the papers’ PDFs and corrected them. The register names 38 arXiv ids. The ones missing from our papers mirror all belong to scheduled tests. One tested paper has no arXiv id and was not checked against a PDF.

<!-- editlens paragraph 0.174 lines 240-251 -->
One operator, the author, ran the rig and labelled the outcomes. Labels were given at rest and not always blind to the arm. Observer bias is therefore the main confound. Where commit order shows it, the pass mark predates the run, so a label could not move the bar. A blind tworeader protocol for the failure classes is committed. It has not run yet, so no verdict has a second reader. For 29 of the 89 gates the repository cannot show whether bar or result came first. 21 of the bar-first verdicts rest on matching a bar text in an earlier file. Under the bootstrap 3 verdicts are fragile. Cold reruns cover 6 gates so far, and the unpublished world-model environment blocks most of the rest. A failure here describes this rig, not the paper

### 3 Results (mean 0.078)

<!-- editlens chunk 0.085 lines 252-335 -->
<!-- editlens paragraph 0.108 lines 252-257 -->
in its own setting. The papers were chosen for one stack, Table 3 counts the verdicts by paper and by claim row. so the rate describes this register and not the field. On claims taken from papers, 12 of 37 reproduce and 18 fail. The other 8 rows test our own baselines, for example github.com/ravediamond/paper-register-reproducibility · a49a1e6

<!-- editlens paragraph 0.288 lines 264-279 -->
Two works use the same arm to evaluate policies. A standardized real-world benchmark reports a taxonomy of failures and recoveries for VLA policies [13]. A fleet of SO-101 cells evaluates policies at scale [14]. The vlaeval tool runs VLAs across 14 simulation benchmarks [8]. A benchmark of demonstration quality studies one method family [22]. We test the claims behind methods (judges, world models, latency) against thresholds fixed before the run, and we audit our own pre-registration. RoboSeed [27] is the closest work. It scores VLA and world-action models on five dimensions, including reproduction evidence and deployment affordability. Its reproduction-evidence score counts five audit milestones (configuration mapping, task records, task coverage, training records, seeds). Its authors state that this score is not a probability that a result is correct. We give one pass or fail per claim on a €1,350 rig.

<!-- editlens paragraph 0.093 lines 303-330 -->
We re-tested 37 paper claims, and 12 held. The rig cost [15] TurboVLA: Real-Time Vision-Language-Action €1,350 and the compute $45.10. Every row behind the Model at 32 Hz on an RTX 4090 with <1 GB verdicts is published. Our own history cannot show the VRAM, 2026. arXiv:2607.27205. order of bar and result for 29 of 89 gates. If you re-test a paper on a cheap rig, run its cheapest baseline on the [16] ContactGuard: Pre-Contact Execution Monitoring same rows first and commit the threshold before the run. with Action-Conditioned Latent World Models, Every number here can be rebuilt from the repository 2026. arXiv:2608.13438. (github.com/ravediamond/paper-register-reproducibility). [17] VLA-Corrector: Stage-Aware Observable State Understanding for Prompt-Based Closed-Loop ReReferences covery of Vision-Language-Action Policies, 2026. arXiv:2609.06508. [1] DINO-WM: World Models on Pre-trained Visual Features enable Zero-shot Planning, 2024. [18] D-JEPA: A Decision-Aligned Latent World Model, arXiv:2411.04983. 2026. arXiv:2609.24749. [2] Can We Detect Failures Without Failure Data? [19] H-JEPA: End-to-End Learning of HierarchiUncertainty-Aware Runtime Failure Detection for cal World Models for Visual Planning, 2026. Imitation Learning Policies, 2025. arXiv:2503.08558. arXiv:2610.06805. [3] SmolVLA: A Vision-Language-Action Model for Affordable and Eﬀicient Robotics, 2025. arXiv:2506.01844. [4] Real-Time Execution of Action Chunking Flow Policies, 2025. arXiv:2506.07339.

<!-- editlens chunk 0.056 lines 336-359 -->
<!-- editlens paragraph 0.064 lines 336-349 -->
[5] SAFE: Multitask Failure Detection for Vision- [22] What Matters in Quality-Aware VLA PretrainLanguage-Action Models, 2025. arXiv:2506.09937. ing: A Benchmark and Empirical Study, 2026. arXiv:2610.18869. [6] VLA-JEPA: Enhancing Vision-LanguageAction Model with Latent World Model, 2026. [23] REKI: Registering Knowledge in VLAs, 2026. arXiv:2602.10098. arXiv:2610.22178. [7] Robometer: Scaling General-Purpose Robotic Re- [24] PACT-VLA: Speculative Action-Chunk Verifiward Models via Trajectory Comparisons, 2026. cation with Pre-Commit Observations, 2026. arXiv:2603.02115. arXiv:2610.28019. github.com/ravediamond/paper-register-reproducibility · a49a1e6

<!-- editlens paragraph 0.092 lines 352-359 -->
[25] Coupling Execution Horizon and Sampling Depth in Flow-Matching VLA Policies, 2026. arXiv:2610.32102. [26] Tracking Task Progress Through Errors and Recovery:A Benchmark and Recurrent Distributional Model, 2026. arXiv:2610.39125. [27] Xin Ma et al. RoboSeed: Multidimensional Evaluation of Vision-Language-Action and World-Action Models, 2026. arXiv:2610.40026.

### Appendix: the register (mean 0.142)

<!-- editlens chunk 0.155 lines 395-568 -->
<!-- editlens paragraph 0.228 lines 395-424 -->
A small JEPA world model learns the Dynamics: beat copy-last, every arm’s dynamics well enough to plan corruption ≥ 1.3 at K = 30. Planwith it. ning: rank the executed chunk first among 8 in ≥ 0.8 of anchors. A predictor on frozen DINOv2 G1b top-1 ≥ 0.8 at some target dispatches plans better than one on a tance. learned latent. Pretrained RoboJEPA predicts our la- 9-step L1 ≥ 15 % below copy-last tents, uses the actions, and runs on (300M) and ≥ 5 % below shuffled the robot’s computer. actions; 2-view encoder ≤ 200 ms on the Orin. A slow second level makes latent dis- Progress monotonicity Spearman tance track task progress. ρ ≤ −0.80; false stalls ≤ 10 %. A decision-aligned ranking operator G1b regret ≤ 0.10 and ≤ the on a frozen world model picks better action-only baseline + 0.05. action chunks. An event-anchored probe on imag- AUROC ≥ 0.85 and ≥ 0.05 above ined latents predicts grasp failure the current latent. better than the current latent. A conformal band on a learned fail- Successes flagged ≤ 1/20; failures ure score keeps false alarms at α flagged ≥ 50 %. while catching failures. A risk head on an action-conditioned ≥ 5/8 failures caught at ≤ latent warns before failures. 1/20 false interventions; actionconditioned iff true ≥ shuffled + 0.05. A verifier on observable history flags ≥ 5/8 failures at ≤ 1/20 false ina failing rollout early enough to cor- terventions. rect it.

<!-- editlens paragraph 0.186 lines 448-457 -->
A 4B reward model judges SO-101 Pooled AUROC ≥ 0.85 and rollouts zero-shot. within-policy ≥ 0.8 on ≥ 5 of 7 policies. A 450M VLA succeeds on an SO-101 10-trial operator-judged gate (no task and can run on low-cost hard- numeric pass mark registered); ware. chunk inference within the async budget (667 ms).

<!-- editlens paragraph 0.193 lines 488-502 -->
22.7 % of successes flagged at α = fail 5 %; 46 % of failures caught v1 AUROC 0.93 came from time fail and length; v2 0.789 vs 0.708 shuffled, 3/8 at 5/42 the paper’s verifier family on our fail rollouts (a GRU on pooled RGB statistics and actions): 2/8 caught at 3/42 false interventions, AUROC 0.59; cosine drift of the W1 latent 0/8, AUROC 0.30 pooled AUROC 0.818 on 2099 fail ArmnetBench rollouts; episode length alone 0.938 9/10 on bowls; 974 ms in PyTorch, reproduces 238 ms with vla.cpp on the Orin NX

<!-- editlens paragraph 0.118 lines 503-506 -->
Table 4: The register, one row per paper, generated from the register file (internal model and gate names kept). The rig price of €1,350 counts the parts with a stated price; 2 small parts are not priced yet. Read the verdict column against the rig each paper was shown on.

<!-- editlens chunk 0.113 lines 591-663 -->
<!-- editlens paragraph 0.405 lines 591-608 -->
Chunk length chosen from the entropy of N sampled chunks follows the task’s phases (long in transport, short at the grasp), lowers the boundary jump, and costs little with batched sampling. Picking among N sampled chunks by their flow residual under the precommit observation fits what happens next better than a random or stale pick, with no added controlstep delay. With long open-loop commitment, cutting a flow-matching VLA’s Euler steps from 10 to 2 contracts the action cloud around an unchanged centroid, saves most of the inference time and avoids edge-GPU thermal throttling. Reading a progress distribution out at the supported peak nearest the previous estimate steadies the estimate and lets it fall during real setbacks, with no worse detection of the stages.

<!-- editlens paragraph 0.184 lines 613-658 -->
upstream’s own trainer on our withdrawn data: task swap 0.020°, per-layout 38.9 %; control, their released LIBERO checkpoint run here: 0.105 (≈ 5.5° of pan) 10-trial operator-judged gate (no 9/10 for $9.7; 355 ms per chunk reproduces numeric pass mark registered); for on the Orin NX; reranking no-go reranking (H0): oracle / mean er- (0.76, 1.84×) ror ≤ 0.7 and N = 8 ≤ 1.5× the latency. ≥ 10 % of failed episodes oscillate 20.3 % of all episodes, 24.0 % of reproduces (their criterion). failures; REKI trained on my data: 19/20 + 19/20 on the arm, oscillates in 1/40 Best gradient-free method cuts the prefix overwrite cuts the jump 71– not median jump ≥ 50 % against naive 73 % against naive async at +0.4 proven async, drift ≤ +10 %, within 667 ms; tuned LeRobot identity mode ms. is close Crossover in [1.0, 2.0] s; at 2 s high- no crossover: W1 0.382 ± 0.005 → not level error ≤ 0.95 × low-level; 0.563 ± 0.007, high level 0.769 ± proven learned macro-actions ≥ net joint 0.009 → 0.759 ± 0.009 (0.73–2 s); displacement on cosine. cosine 0.608 ± 0.007 vs 0.551 ± 0.006 W1’s mean R2 from latent to joints W1 mean R2 0.565, anisotropy reproduces < 0.80; anisotropy (max − min 0.639 (shoulder lift 0.91, wrist flex per-joint R2 ) ≥ 0.20; the higher-R2 0.27); frozen DINOv2-S 0.867 / 0.301 model has the higher G1b top-1. τ below the 10th percentile of non- τ = 1.249 on W1 latents of 69 real fail equivalent pairs and ≤ 0.40; as a rollouts; as a monitor 3/8 at 6/42 monitor ≥ 5/8 failures at ≤ 2/42; (S = 30), AUROC 0.756 vs shuffled ≥ 0.05 AUROC over a shuffled 0.560 drafter. median h* in transport ≥ grasp h* 2 in transport and 2 at the grasp fail window + 2; jump with AAC + (86 % of decisions at the floor); overwrite ≤ fixed + overwrite at d jump 0.973 vs 0.940; N = 20 deci= 8; an N = 20 decision ≤ 298 ms sion 4,751 ms (sequential) on the on the Orin. Orin PACT beats a random pick and the stale-observation residual at d = 8 (CIs < 0); its delay on the Orin ≤ the naive delay; at that delay it still beats a single sample.

<!-- editlens chunk 0.430 lines 677-680 -->
Against per-frame argmax: premature not higher and missed ≤ +2 points (P1); flips halved, CI upper ≤ 0.7 (P2); a decrease inside ≥ 50 % of the reversal windows with ≤ 20 % false regressions (P3).
