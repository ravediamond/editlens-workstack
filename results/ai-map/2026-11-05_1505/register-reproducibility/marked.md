# paper-register-reproducibility: chunks in paper order

## rendered source (numbers filled)

### Abstract (mean 0.361)

<!-- editlens chunk 0.361 lines 7-7 -->
<!-- editlens paragraph 0.361 lines 7-7 -->
We re-tested the central claims of recent robot-learning papers on an SO-101 arm with a Jetson Orin NX, a rig whose parts cost €1,350, for $45.10 of compute. Each re-test ran the cheapest baseline first, with its pass mark committed before the run, and every published number rebuilds from stored rows. Of the 37 paper claims we tested, 12 held on this hardware. We sort the failures into three proposed classes, named after the condition a claim did not survive. One is the clock, where a method misses the real-time budget on the edge GPU. The other two cover zero-shot judges beaten by a trivial signal and latent planners beaten by the commanded joints. A blind second reader still has to confirm the classes. We also audited our own pre-registration by commit ancestry, which shows the order of bar and result for most gates and not for the rest.

### 1. The register (mean 0.265)

<!-- editlens chunk 0.265 lines 11-19 -->
<!-- editlens paragraph 0.317 lines 11-11 -->
Most of the 22 papers in this study were shown on setups far from ours: 9 in simulation and 7 on rigs above X5k, which is where our rig falls. The appendix table gives the rig of each paper, including the 3 in between and the 1 that does not say. Our rig is an SO-101 arm and a Jetson Orin NX 16 GB, and the parts with a stated price cost €1,350 (2 small parts are not priced yet).

<!-- editlens paragraph 0.206 lines 15-15 -->
Here is one entry. An adaptive chunking paper claims that choosing the chunk length from the entropy of sampled chunks follows the task's phases, long in transport and short at the grasp. On our edge GPU one such decision takes 4,751 ms, and the budget is 298 ms. The entry records a fail on this rig, which says nothing about the method on the hardware it was shown on. Next to the verdict it keeps the claim in the paper's words, our pass mark, our measurement and the published rows.

<!-- editlens paragraph 0.300 lines 17-17 -->
For each claim we first run, on the same rows, the cheapest signal the learned model has to beat: copy-last for a predictor, the commanded joints for a latent and episode length for a judge. The pass mark is committed before the run, and §2 checks how often that held.

### 2. Auditing our own pre-registration (mean 0.136)

<!-- editlens chunk 0.136 lines 23-49 -->
<!-- editlens paragraph 0.160 lines 23-23 -->
A gate's pass mark had to be in version control before its result. Notes and commit dates can be edited by hand, but commit ancestry cannot be changed without rewriting history that others have already cloned. We therefore order each gate with X, between the first commit that contains its bar and the first commit that contains its result. Table 1 gives the classes for the 89 gates logged by 2026-10-31. Most are bar-first, and 0 are result-first. A same-commit gate is one where bar and result entered the repository together, which says nothing about which was written first.

<!-- editlens paragraph 0.247 lines 37-37 -->
Our first pass used text search and found 31 same-commit gates, mostly because of batch logging: a bar written earlier in a protocol, plan, scorer or specification often reached the log in the same commit as its result. We traced each same-commit gate back to that file. This moved 21 gates to bar-first and 4 to no-bar (their bar cell declares none), and 6 stayed same-commit. The audit table in the repository gives the evidence line for every move. We did not re-audit the gates that were already bar-first. One open candidate remains, the reward-model progress test of 2026-11-01, which is same-commit by text search although its protocol (X) is older than the log commit.

<!-- editlens paragraph 0.207 lines 39-39 -->
The early gates mixed point estimates and different intervals, so we recomputed 10 of them from stored rows with one statistic, the episode bootstrap (2,000 resamples, percentile 95 % CI). For 3 of them the bar falls inside the interval (Table 2). The colour judge is a fail on the point estimate, and its interval does not settle it. The false-intervention threshold was fitted to meet its rate, so that interval is only descriptive. The register keeps the pre-registered point verdicts and marks these three as fragile.

<!-- editlens paragraph 0.187 lines 49-49 -->
All 29 write-ups rebuild from their published rows. We also reran gates cold, from a fresh clone with no credentials, and 6 reran and matched, 5 of them exactly. 12 more stop at the world-model environment, which is not published yet, and publishing it would unblock most of them. The remaining 11 need a larger GPU, a private checkpoint, the arm or a step the write-up leaves out. We checked the register's citations and paper-side fields against the papers' PDFs and corrected them. Of the 38 arXiv ids the register names, the ones missing from our papers mirror all belong to scheduled tests, and the one tested paper with no arXiv id was not checked against a PDF.

### 3. Results (mean 0.271)

<!-- editlens chunk 0.271 lines 53-53 -->
<!-- editlens paragraph 0.271 lines 53-53 -->
Table 3 counts the verdicts by paper and by claim row, and the appendix lists every entry. On claims taken from papers, 12 of 37 reproduce and 18 fail. The other 8 rows test our own baselines, for example that the commanded joints beat the world model, and 5 of those hold.

### 4. Three failure classes (mean 0.333)

<!-- editlens chunk 0.333 lines 68-72 -->
<!-- editlens paragraph 0.327 lines 68-68 -->
The adaptive chunking entry of §1 misses the real-time budget on the edge GPU, with one decision taking 4,751 ms against 298 ms. The method may work on faster hardware. We call this kind of failure class A, the clock.

<!-- editlens paragraph 0.256 lines 70-70 -->
In other entries a model judged outcomes without training on this rig. A learned reward model detects failures at AUROC 0.818, and episode length alone reaches 0.938. Judges of success, failure or progress that lose to a trivial signal like this form class B. Class C is about learned latents used to plan, rank or track progress that lose to the joints, to copy-last or to an action-only baseline. A world model, for example, ranks the executed chunk first in 0.60 of anchors, where its pass mark was 0.8 and an action-only baseline reaches 0.68–0.90.

<!-- editlens paragraph 0.116 lines 72-72 -->
These examples illustrate the classes and do not count them. Under a protocol committed before any labelling, the labels count only once a blind second reader labels the same 20 failed rows on the same form and agrees with the first reading at Cohen's κ ≥ 0.6. That reading has not happened yet.

### 5. Limitations (mean 0.397)

<!-- editlens chunk 0.397 lines 76-76 -->
<!-- editlens paragraph 0.397 lines 76-76 -->
One operator, the author, ran the rig and labelled the outcomes, at rest and not always blind to the arm, so observer bias is the main confound. Where commit order shows it, the pass mark predates the run and a label could not move the bar. A blind two-reader protocol for the failure classes is committed but has not run, so no verdict has a second reader yet. For 29 of the 89 gates the repository cannot show whether bar or result came first, and 21 of the bar-first verdicts rest on matching a bar text in an earlier file. Under the bootstrap 3 verdicts are fragile. Cold reruns cover 6 gates so far, and the unpublished world-model environment blocks most of the rest. A failure here describes this rig, not the paper in its own setting. Because the papers were chosen for one stack, the rate describes this register and not the field.

### 6. Related work (mean 0.273)

<!-- editlens chunk 0.273 lines 80-80 -->
<!-- editlens paragraph 0.273 lines 80-80 -->
Two works use the same arm to evaluate policies: a standardized real-world benchmark that reports a taxonomy of failures and recoveries for VLA policies [arXiv:2606.08881], and a fleet of SO-101 cells that evaluates policies at scale [arXiv:2607.24481]. The vla-eval tool runs VLAs across 14 simulation benchmarks [arXiv:2603.13966]. A benchmark of demonstration quality studies one method family [arXiv:2610.18869]. We test the claims behind methods (judges, world models, latency) against thresholds fixed before the run, and we audit our own pre-registration. RoboSeed [arXiv:2610.40026] is the closest work. It scores VLA and world-action models on five dimensions, including reproduction evidence and deployment affordability, and its reproduction-evidence score counts five audit milestones (configuration mapping, task records, task coverage, training records, seeds). Its authors state that this score is not a probability that a result is correct. We give one pass or fail per claim on a €1,350 rig.

### 7. Conclusion (mean 0.283)

<!-- editlens chunk 0.283 lines 84-84 -->
<!-- editlens paragraph 0.283 lines 84-84 -->
We re-tested 37 paper claims on a €1,350 rig, and 12 held. The compute cost $45.10, and every row behind the verdicts is published. Our own history cannot show the order of bar and result for 29 of 89 gates. If you re-test a paper on a cheap rig, run its cheapest baseline on the same rows first and commit the threshold before the run. Every number here can be rebuilt from the repository (X).

### (figure and table captions) (mean 0.089)

<!-- editlens chunk 0.089 lines 25-90 -->
Table 1: Commit-order class of each gate. The audited column is the one the paper uses; the first pass is what text search alone gave on the same gates.
Table 2: The three gates whose verdict flips somewhere inside its 95 % interval.
Table 3: Verdicts by paper and by claim row (claim rows include our own baseline comparisons).
Table 4: The register, one row per paper, generated from the register file (internal model and gate names kept). Read the verdict column against the rig each paper was shown on.

## built PDF

### Abstract (mean 0.166)

<!-- editlens chunk 0.171 lines 12-134 -->
<!-- editlens paragraph 0.364 lines 17-32 -->
We re-tested the central claims of recent robot-learning papers on an SO-101 arm with a Jetson Orin NX, a rig whose parts cost €1,350, for $45.10 of compute. Each retest ran the cheapest baseline first, with its pass mark committed before the run, and every published number rebuilds from stored rows. Of the 37 paper claims we tested, 12 held on this hardware. We sort the failures into three proposed classes, named after the condition a claim did not survive. One is the clock, where a method misses the real-time budget on the edge GPU. The other two cover zero-shot judges beaten by a trivial signal and latent planners beaten by the commanded joints. A blind second reader still has to confirm the classes. We also audited our own pre-registration by commit ancestry, which shows the order of bar and result for most gates and not for the rest.

<!-- editlens paragraph 0.278 lines 37-50 -->
Most of the 22 papers in this study were shown on setups far from ours: 9 in simulation and 7 on rigs above $20k. 2 used a setup under $5k, which is where our rig falls. The appendix table gives the rig of each paper, including the 3 in between and the 1 that does not say. Our rig is an SO101 arm and a Jetson Orin NX 16 GB, and the parts with a stated price cost €1,350 (2 small parts are not priced yet). The register grew out of our own write-ups, 29 so far, each published with its data. This paper collects them in one table and audits how the table was kept. Here is one entry. An adaptive chunking paper claims that choosing the chunk length from the entropy of sampled chunks follows the task’s phases, long in transport and short at the grasp. On our edge GPU one such decision takes 4,751 ms, and the budget is 298 ms. The entry records a fail on this rig, which says nothing about the

<!-- editlens paragraph 0.322 lines 89-101 -->
method on the hardware it was shown on. Next to the verdict it keeps the claim in the paper’s words, our pass mark, our measurement and the published rows. For each claim we first run, on the same rows, the cheapest signal the learned model has to beat: copy-last for a predictor, the commanded joints for a latent and episode length for a judge. The pass mark is committed before the run, and §2 checks how often that held. We chose the papers for the stack this rig runs (world models, VLA policies, failure monitors, chunking, edge latency) and entered each one in the register before its test. The register file lists the papers scheduled next.

<!-- editlens paragraph 0.245 lines 106-127 -->
A gate’s pass mark had to be in version control before its result. Notes and commit dates can be edited by hand, but commit ancestry cannot be changed without rewriting history that others have already cloned. We therefore order each gate with git merge-base --is-ancestor, between the first commit that contains its bar and the first commit that contains its result. Table 1 gives the classes for the 89 gates logged by 2026-10-31. Most are bar-first, and 0 are result-first. A same-commit gate is one where bar and result entered the repository together, which says nothing about which was written first. Our first pass used text search and found 31 same∗ Every commit gates, mostly because of batch logging: a bar with source number its file: github.com/ravediamond/paper-register-reproducibility. written earlier in a protocol, plan, scorer or specification github.com/ravediamond/paper-register-reproducibility · 90fcdbd

<!-- editlens chunk 0.155 lines 159-218 -->
<!-- editlens paragraph 0.154 lines 159-188 -->
often reached the log in the same commit as its result. We traced each same-commit gate back to that file. This moved 21 gates to bar-first and 4 to no-bar (their bar cell declares none), and 6 stayed same-commit. The audit table in the repository gives the evidence line for every move. We did not re-audit the gates that were already bar-first. One open candidate remains, the reward-model progress test of 2026-11-01, which is same-commit by text search although its protocol (6241570) is older than the log commit. The early gates mixed point estimates and different intervals, so we recomputed 10 of them from stored rows with one statistic, the episode bootstrap (2,000 resamples, percentile 95 % CI). For 3 of them the bar falls inside the interval (Table 2). The colour judge is a fail on the point estimate, and its interval does not settle it. The false-intervention threshold was fitted to meet its rate, so that interval is only descriptive. The register keeps the pre-registered point verdicts and marks these three as fragile. All 29 write-ups rebuild from their published rows. We also reran gates cold, from a fresh clone with no credentials, and 6 reran and matched, 5 of them exactly. 12 more stop at the world-model environment, which is not published yet, and publishing it would unblock most of them. The remaining 11 need a larger GPU, a private checkpoint, the arm or a step the write-up leaves out. We checked the register’s citations and paper-side fields against the papers’ PDFs and corrected them. Of the 38 arXiv ids the register names, the ones missing from our papers mirror all belong to scheduled tests, and the one tested paper with no arXiv id was not checked against a PDF.

### 0.938. Judges of success, failure or progress that lose to (mean 0.354)

<!-- editlens chunk 0.354 lines 219-246 -->
<!-- editlens paragraph 0.233 lines 219-230 -->
a trivial signal like this form class B. Class C is about learned latents used to plan, rank or track progress that lose to the joints, to copy-last or to an action-only baseline. A world model, for example, ranks the executed chunk first in 0.60 of anchors, where its pass mark was 0.8 and an action-only baseline reaches 0.68–0.90. These examples illustrate the classes and do not count them. Under a protocol committed before any labelling, the labels count only once a blind second reader labels the same 20 failed rows on the same form and agrees with the first reading at Cohen’s κ ≥ 0.6. That reading has not happened yet.

<!-- editlens paragraph 0.396 lines 235-246 -->
One operator, the author, ran the rig and labelled the outcomes, at rest and not always blind to the arm, so observer bias is the main confound. Where commit order shows it, the pass mark predates the run and a label could not move the bar. A blind two-reader protocol for the failure classes is committed but has not run, so no verdict has a second reader yet. For 29 of the 89 gates the repository cannot show whether bar or result came first, and 21 of the bar-first verdicts rest on matching a bar text in an earlier file. Under the bootstrap 3 verdicts are fragile. Cold reruns cover 6 gates so far, and the unpublished world-model environment blocks most of the rest. A failure here describes this rig, not the paper in

### 3 Results (mean 0.272)

<!-- editlens chunk 0.272 lines 247-255 -->
<!-- editlens paragraph 0.272 lines 247-255 -->
its own setting. Because the papers were chosen for one Table 3 counts the verdicts by paper and by claim row, stack, the rate describes this register and not the field. and the appendix lists every entry. On claims taken from papers, 12 of 37 reproduce and 18 fail. The other 8 rows test our own baselines, for example that the commanded 6 Related work joints beat the world model, and 5 of those hold. Two works use the same arm to evaluate policies: a standardized real-world benchmark that reports a taxonomy of failures and recoveries for VLA policies [13], and a

### 4 Three failure classes (mean 0.131)

<!-- editlens chunk 0.089 lines 256-284 -->
<!-- editlens paragraph 0.113 lines 256-260 -->
fleet of SO-101 cells that evaluates policies at scale [14]. The adaptive chunking entry of §1 misses the real-time The vla-eval tool runs VLAs across 14 simulation benchbudget on the edge GPU, with one decision taking 4,751 marks [8]. A benchmark of demonstration quality studms against 298 ms. The method may work on faster hard- ies one method family [22]. We test the claims behind methods (judges, world models, latency) against threshware. We call this kind of failure class A, the clock. github.com/ravediamond/paper-register-reproducibility · 90fcdbd

<!-- editlens paragraph 0.109 lines 263-276 -->
olds fixed before the run, and we audit our own pre- [11] Adaptive Action Chunking at Inference-time registration. RoboSeed [27] is the closest work. It scores for Vision-Language-Action Models, 2026. VLA and world-action models on five dimensions, inarXiv:2604.04161. cluding reproduction evidence and deployment affordability, and its reproduction-evidence score counts five [12] When Does LeJEPA Learn a World Model?, 2026. arXiv:2605.26379. audit milestones (configuration mapping, task records, task coverage, training records, seeds). Its authors state [13] Benchmarking Vision-Language-Action Models on that this score is not a probability that a result is correct. SO-101: Failure and Recovery Analysis, 2026. We give one pass or fail per claim on a €1,350 rig. arXiv:2606.08881.

<!-- editlens chunk 0.153 lines 285-343 -->
<!-- editlens paragraph 0.097 lines 285-328 -->
We re-tested 37 paper claims on a €1,350 rig, and 12 held. The compute cost $45.10, and every row behind the [15] TurboVLA: Real-Time Vision-Language-Action Model at 32 Hz on an RTX 4090 with <1 GB verdicts is published. Our own history cannot show the VRAM, 2026. arXiv:2607.27205. order of bar and result for 29 of 89 gates. If you re-test a paper on a cheap rig, run its cheapest baseline on the [16] ContactGuard: Pre-Contact Execution Monitoring same rows first and commit the threshold before the run. with Action-Conditioned Latent World Models, Every number here can be rebuilt from the repository 2026. arXiv:2608.13438. (github.com/ravediamond/paper-register-reproducibility). [17] VLA-Corrector: Stage-Aware Observable State Understanding for Prompt-Based Closed-Loop ReReferences covery of Vision-Language-Action Policies, 2026. arXiv:2609.06508. [1] DINO-WM: World Models on Pre-trained Visual Features enable Zero-shot Planning, 2024. [18] D-JEPA: A Decision-Aligned Latent World Model, 2026. arXiv:2609.24749. arXiv:2411.04983. [2] Can We Detect Failures Without Failure Data? [19] H-JEPA: End-to-End Learning of Hierarchical World Models for Visual Planning, 2026. Uncertainty-Aware Runtime Failure Detection for arXiv:2610.06805. Imitation Learning Policies, 2025. arXiv:2503.08558. [20] RoboJEPA: Scaling Robotic Latent World Models, [3] SmolVLA: A Vision-Language-Action Model 2026. arXiv:2610.10515. for Affordable and Eﬀicient Robotics, 2025. [21] ReAP: From Visual Failure Recognition to ActionarXiv:2506.01844. Conditioned Risk Prediction for Runtime Failure [4] Real-Time Execution of Action Chunking Flow PoliMonitoring, 2026. arXiv:2610.16309. cies, 2025. arXiv:2506.07339. [22] What Matters in Quality-Aware VLA Pretraining: A Benchmark and Empirical Study, 2026. [5] SAFE: Multitask Failure Detection for VisionarXiv:2610.18869. Language-Action Models, 2025. arXiv:2506.09937. [6] VLA-JEPA: Enhancing Vision-Language- [23] REKI: Registering Knowledge in VLAs, 2026. arXiv:2610.22178. Action Model with Latent World Model, 2026. arXiv:2602.10098. [24] PACT-VLA: Speculative Action-Chunk Verification with Pre-Commit Observations, 2026. [7] Robometer: Scaling General-Purpose Robotic RearXiv:2610.28019. ward Models via Trajectory Comparisons, 2026. arXiv:2603.02115.

<!-- editlens paragraph 0.067 lines 329-343 -->
[25] Coupling Execution Horizon and Sampling Depth in Flow-Matching VLA Policies, 2026. [8] vla-eval: A Unified Evaluation Harness for VisionarXiv:2610.32102. Language-Action Models, 2026. arXiv:2603.13966. [26] Tracking Task Progress Through Errors and Re[9] LeWorldModel: Stable End-to-End Jointcovery:A Benchmark and Recurrent Distributional Embedding Predictive Architecture from Pixels, Model, 2026. arXiv:2610.39125. 2026. arXiv:2603.19312. [27] Xin Ma et al. RoboSeed: Multidimensional Evalu[10] Hierarchical Planning with Latent World Models, ation of Vision-Language-Action and World-Action 2026. arXiv:2604.03208. Models, 2026. arXiv:2610.40026. github.com/ravediamond/paper-register-reproducibility · 90fcdbd

### Appendix: the register (mean 0.145)

<!-- editlens chunk 0.161 lines 377-549 -->
<!-- editlens paragraph 0.228 lines 377-406 -->
A small JEPA world model learns the Dynamics: beat copy-last, every arm’s dynamics well enough to plan corruption ≥ 1.3 at K = 30. Planwith it. ning: rank the executed chunk first among 8 in ≥ 0.8 of anchors. A predictor on frozen DINOv2 G1b top-1 ≥ 0.8 at some target dispatches plans better than one on a tance. learned latent. Pretrained RoboJEPA predicts our la- 9-step L1 ≥ 15 % below copy-last tents, uses the actions, and runs on (300M) and ≥ 5 % below shuffled the robot’s computer. actions; 2-view encoder ≤ 200 ms on the Orin. A slow second level makes latent dis- Progress monotonicity Spearman tance track task progress. ρ ≤ −0.80; false stalls ≤ 10 %. A decision-aligned ranking operator G1b regret ≤ 0.10 and ≤ the on a frozen world model picks better action-only baseline + 0.05. action chunks. An event-anchored probe on imag- AUROC ≥ 0.85 and ≥ 0.05 above ined latents predicts grasp failure the current latent. better than the current latent. A conformal band on a learned fail- Successes flagged ≤ 1/20; failures ure score keeps false alarms at α flagged ≥ 50 %. while catching failures. A risk head on an action-conditioned ≥ 5/8 failures caught at ≤ latent warns before failures. 1/20 false interventions; actionconditioned iff true ≥ shuffled + 0.05. A verifier on observable history flags ≥ 5/8 failures at ≤ 1/20 false ina failing rollout early enough to cor- terventions. rect it.

<!-- editlens paragraph 0.186 lines 430-439 -->
A 4B reward model judges SO-101 Pooled AUROC ≥ 0.85 and rollouts zero-shot. within-policy ≥ 0.8 on ≥ 5 of 7 policies. A 450M VLA succeeds on an SO-101 10-trial operator-judged gate (no task and can run on low-cost hard- numeric pass mark registered); ware. chunk inference within the async budget (667 ms).

<!-- editlens paragraph 0.193 lines 470-484 -->
22.7 % of successes flagged at α = fail 5 %; 46 % of failures caught v1 AUROC 0.93 came from time fail and length; v2 0.789 vs 0.708 shuffled, 3/8 at 5/42 the paper’s verifier family on our fail rollouts (a GRU on pooled RGB statistics and actions): 2/8 caught at 3/42 false interventions, AUROC 0.59; cosine drift of the W1 latent 0/8, AUROC 0.30 pooled AUROC 0.818 on 2099 fail ArmnetBench rollouts; episode length alone 0.938 9/10 on bowls; 974 ms in PyTorch, reproduces 238 ms with vla.cpp on the Orin NX

<!-- editlens chunk 0.113 lines 572-644 -->
<!-- editlens paragraph 0.405 lines 572-589 -->
Chunk length chosen from the entropy of N sampled chunks follows the task’s phases (long in transport, short at the grasp), lowers the boundary jump, and costs little with batched sampling. Picking among N sampled chunks by their flow residual under the precommit observation fits what happens next better than a random or stale pick, with no added controlstep delay. With long open-loop commitment, cutting a flow-matching VLA’s Euler steps from 10 to 2 contracts the action cloud around an unchanged centroid, saves most of the inference time and avoids edge-GPU thermal throttling. Reading a progress distribution out at the supported peak nearest the previous estimate steadies the estimate and lets it fall during real setbacks, with no worse detection of the stages.

<!-- editlens paragraph 0.184 lines 594-639 -->
upstream’s own trainer on our withdrawn data: task swap 0.020°, per-layout 38.9 %; control, their released LIBERO checkpoint run here: 0.105 (≈ 5.5° of pan) 10-trial operator-judged gate (no 9/10 for $9.7; 355 ms per chunk reproduces numeric pass mark registered); for on the Orin NX; reranking no-go reranking (H0): oracle / mean er- (0.76, 1.84×) ror ≤ 0.7 and N = 8 ≤ 1.5× the latency. ≥ 10 % of failed episodes oscillate 20.3 % of all episodes, 24.0 % of reproduces (their criterion). failures; REKI trained on my data: 19/20 + 19/20 on the arm, oscillates in 1/40 Best gradient-free method cuts the prefix overwrite cuts the jump 71– not median jump ≥ 50 % against naive 73 % against naive async at +0.4 proven async, drift ≤ +10 %, within 667 ms; tuned LeRobot identity mode ms. is close Crossover in [1.0, 2.0] s; at 2 s high- no crossover: W1 0.382 ± 0.005 → not level error ≤ 0.95 × low-level; 0.563 ± 0.007, high level 0.769 ± proven learned macro-actions ≥ net joint 0.009 → 0.759 ± 0.009 (0.73–2 s); displacement on cosine. cosine 0.608 ± 0.007 vs 0.551 ± 0.006 W1’s mean R2 from latent to joints W1 mean R2 0.565, anisotropy reproduces < 0.80; anisotropy (max − min 0.639 (shoulder lift 0.91, wrist flex per-joint R2 ) ≥ 0.20; the higher-R2 0.27); frozen DINOv2-S 0.867 / 0.301 model has the higher G1b top-1. τ below the 10th percentile of non- τ = 1.249 on W1 latents of 69 real fail equivalent pairs and ≤ 0.40; as a rollouts; as a monitor 3/8 at 6/42 monitor ≥ 5/8 failures at ≤ 2/42; (S = 30), AUROC 0.756 vs shuffled ≥ 0.05 AUROC over a shuffled 0.560 drafter. median h* in transport ≥ grasp h* 2 in transport and 2 at the grasp fail window + 2; jump with AAC + (86 % of decisions at the floor); overwrite ≤ fixed + overwrite at d jump 0.973 vs 0.940; N = 20 deci= 8; an N = 20 decision ≤ 298 ms sion 4,751 ms (sequential) on the on the Orin. Orin PACT beats a random pick and the stale-observation residual at d = 8 (CIs < 0); its delay on the Orin ≤ the naive delay; at that delay it still beats a single sample.

<!-- editlens chunk 0.430 lines 658-661 -->
Against per-frame argmax: premature not higher and missed ≤ +2 points (P1); flips halved, CI upper ≤ 0.7 (P2); a decrease inside ≥ 50 % of the reversal windows with ≤ 20 % false regressions (P3).
