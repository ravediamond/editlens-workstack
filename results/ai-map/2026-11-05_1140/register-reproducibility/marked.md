# paper-register-reproducibility: chunks in paper order

## rendered source (numbers filled)

### Abstract (mean 0.377)

<!-- editlens chunk 0.377 lines 7-7 -->
<!-- editlens paragraph 0.377 lines 7-7 -->
Re-testing a robot-learning paper does not need a lab. For $45.10 of compute on a €1,350 rig, an SO-101 arm with a Jetson Orin NX, we re-tested the central claims of recent papers under pass marks committed before each run, and every published number rebuilds from stored rows. Of the 37 paper claims tested, 12 held on this hardware. The failures fit three proposed classes, each named after the condition the claim did not survive. The clearest is the clock: methods that work on a desktop GPU but miss the real-time budget on the edge board. The other two are zero-shot judges beaten by a trivial signal and latent planners beaten by the commanded joints. A blind second reader still has to confirm the classes. We also audited our own pre-registration by commit ancestry, and the audit shows where our ordering holds and where the repository cannot prove it.

### 1. The register (mean 0.322)

<!-- editlens chunk 0.322 lines 11-19 -->
<!-- editlens paragraph 0.409 lines 11-11 -->
A robot-learning paper reports what happened on one setup. Of the 22 papers here, 9 were shown in simulation and 7 on rigs above X5–20k setup, 2 one below $5k, and 1 does not say. Ours costs €1,350: an SO-101 arm and a Jetson Orin NX 16 GB (2 small parts are not yet priced).

<!-- editlens paragraph 0.220 lines 15-15 -->
Take one entry. An adaptive chunking paper claims that choosing the chunk length from the entropy of sampled chunks follows the task's phases, long in transport and short at the grasp. On our edge GPU a single decision takes 4,751 ms. The budget is 298 ms. So the entry records a fail on this rig, which says nothing against the method on the hardware it was shown on, and beside the verdict it keeps the claim in the paper's words, our pass mark, our measurement and the published rows that rebuild it.

<!-- editlens paragraph 0.579 lines 17-17 -->
Before a learned model gets credit, the cheapest signal it must beat runs on the same rows: copy-last for a predictor, the commanded joints for a latent, episode length for a judge. A method that loses to that signal has not shown what it claims, however good its own number looks. The threshold itself is committed before the run, and §2 checks how often that held.

### 2. Auditing our own pre-registration (mean 0.154)

<!-- editlens chunk 0.154 lines 23-29 -->
<!-- editlens paragraph 0.257 lines 23-23 -->
To rule out moving the goalposts after the fact, a gate's threshold had to be in version control before its result. Notes and commit dates can be edited by hand. Commit ancestry cannot, short of rewriting history that others have already cloned, so the order of each gate is read from X alone, between the first commit that contains its bar and the first that contains its result. Of the 89 gates logged by 2026-10-31, **58 are bar-first** and 0 result-first. The rest split into 6 same-commit, 23 with no bar and 2 with a threshold but no result yet. Same-commit says nothing about which was written first. The log has since grown to 93 rows (61 bar-first, 7 same-commit, 0 result-first, 23 no-bar, 2 not-run).

<!-- editlens paragraph 0.307 lines 25-25 -->
A first pass by text search read the log very differently: 36 bar-first and 31 same-commit, with 19 no-bar and 3 unresolved. The cause was batch logging. A bar written earlier in a protocol, plan, scorer or specification often reached the log in the same commit as its result. Tracing each same-commit gate back to that earlier file moved 21 to bar-first and 4 to no-bar (their bar cell declares none), and 6 stayed same-commit; the audit table gives the evidence line for every move. Rows that were already bar-first were not re-audited for a result hidden elsewhere. One open candidate remains, the reward-model progress test of 2026-11-01: same-commit by text search, although its protocol (X) is older than the log commit.

<!-- editlens paragraph 0.271 lines 27-27 -->
Point estimates give clean verdicts, and intervals do not always agree with them. Recomputing 10 early gates from stored rows with one statistic (episode bootstrap, 2,000 resamples, percentile 95 % CI) leaves 3 with the bar inside the interval. The no-learning colour judge is the plainest case. It is right on 94.2 % of 87 episodes against a 95 % pass mark, a fail on the point, yet its interval runs from 89.6 to 98.9 %. The oscillation rate among 25 failed episodes is a pass (24.0 % against 10 %) with a lower bound of 8.0 %. A judge threshold's false-intervention rate is a pass at 2.4 % of 42 against a 5 % ceiling, with an upper bound of 7.1 %, and because that threshold was fitted to meet the rate, its interval only describes. The register keeps the pre-registered point verdicts and flags these three as fragile.

<!-- editlens paragraph 0.222 lines 29-29 -->
All 29 write-ups rebuild from their published rows. Cold reruns are a stricter test. From a fresh clone with no credentials, 6 gates rerun and match, 5 of them exactly. Another 12 stop at the same place, the world-model environment, which is not published yet; publishing it would unblock most of them. The remaining 11 need a larger GPU, a private checkpoint, the arm or a step the write-up leaves out. Citations and paper-side fields were checked against the papers' PDFs and corrected. Of the 38 arXiv ids the register names, those missing from our papers mirror all belong to scheduled tests, and the one tested paper without an arXiv id was not checked against a PDF.

### 3. Results (mean 0.136)

<!-- editlens chunk 0.136 lines 60-60 -->
<!-- editlens paragraph 0.136 lines 60-60 -->
Counted by paper, 4 of the 22 hold and 13 fail (Table 1); 3 are not proven, 1 was not tested and 1 was withdrawn. By claim the picture is finer. Of 45 claim rows (42 tested), 8 test our own baselines rather than a paper, such as "the commanded joints beat the world model", and 5 of those reproduce. The 37 claims taken from papers split into 12 that reproduce and 18 that fail. Over all rows: 17 reproduce, 20 fail, 3 not proven, 4 not tested, 1 withdrawn.

### 4. Three failure classes (mean 0.341)

<!-- editlens chunk 0.341 lines 64-68 -->
<!-- editlens paragraph 0.333 lines 64-64 -->
We sort the 20 failed claim rows by the condition each claim did not survive. Class A, the clock, is the easiest to see. The method may be sound, but on the edge GPU it misses the real-time budget the claim needs, as the adaptive chunking entry of §1 does (4,751 ms per decision against 298 ms); for that entry nothing about the idea is refuted, the board is simply too slow for it.

<!-- editlens paragraph 0.350 lines 66-66 -->
Class B covers zero-shot judges, models used without training on this rig to judge success, failure or progress, that lose to a trivial signal on the same rows. A learned reward model detects failures at AUROC 0.818, where episode length alone reaches 0.938. Class C is quicker to state: a learned latent used to plan, rank or track progress does worse than the commanded joints or a copy-last or action-only baseline (a world model ranks the executed chunk first in 0.60 of anchors, against a pass mark of 0.8 and 0.68–0.90 for actions alone).

<!-- editlens paragraph 0.187 lines 68-68 -->
These examples illustrate the classes; they do not count them. A protocol committed before any labelling says the labels count only once a blind second reader, given the same 20 rows on the same form, agrees with the first reading at Cohen's κ ≥ 0.6. That reading has not happened yet.

### 5. Limitations (mean 0.384)

<!-- editlens chunk 0.384 lines 72-72 -->
<!-- editlens paragraph 0.384 lines 72-72 -->
With a single operator, the author, running the rig and labelling outcomes at rest and not always blind to the arm, observer bias is the main confound. Two things limit it. Where commit order shows it, the pass mark predates the run, so a label could not have moved the bar. A blind two-reader protocol for the failure classes is also committed and ready, though it has not run, and until it does no verdict has a second reader. Ordering is provable for most gates, not all: for 29 of the 89 (6 same-commit, 23 with no bar) the repository cannot show which came first, and 21 of the bar-first verdicts rest on matching a bar text in an earlier file. Under the bootstrap 3 verdicts are fragile. Cold reruns cover 6 gates so far, with the unpublished world-model environment as the main blocker. A failure here describes this rig, not the paper in its own setting, and because the papers were chosen for one stack the rate describes this register rather than the field.

### 6. Related work (mean 0.275)

<!-- editlens chunk 0.275 lines 76-76 -->
<!-- editlens paragraph 0.275 lines 76-76 -->
Work on the same arm evaluates policies. A standardized real-world benchmark reports a taxonomy of failures and recoveries for VLA policies [arXiv:2606.08881], and a fleet of SO-101 cells evaluates policies at scale [arXiv:2607.24481]. The vla-eval tool runs VLAs across 14 simulation benchmarks [arXiv:2603.13966]. A benchmark of demonstration quality studies one method family [arXiv:2610.18869]. We test something else. Our targets are the claims behind methods (judges, world models, latency), checked against thresholds fixed before the run, with our own pre-registration audited. The closest statement of our thesis [arXiv:2610.40026] scores VLA and world-action models on five dimensions, among them reproduction evidence and deployment affordability. Its reproduction-evidence score counts five audit milestones (configuration mapping, task records, task coverage, training records, seeds), and its authors state that it is not a probability that a result is correct. We give one pass or fail per claim on a €1,350 rig instead.

### 7. Conclusion (mean 0.322)

<!-- editlens chunk 0.322 lines 80-80 -->
<!-- editlens paragraph 0.322 lines 80-80 -->
A €1,350 rig and $45.10 of compute were enough to re-test these claims and publish every row behind the verdicts, and 12 of 37 held. Money was never the constraint. Order was: keeping each pass mark ahead of its result, which our own history cannot prove for 29 of 89 gates. If you re-test a paper on a cheap rig, start with its cheapest baseline on the same rows, and commit the threshold before you look. Every number here can be rebuilt from the repository (X).

### (figure and table captions) (mean 0.057)

<!-- editlens chunk 0.057 lines 33-33 -->
Table 1: The register, one row per paper, generated from the register file (internal model and gate names kept). Read the verdict column against the rig each paper was shown on.

## built PDF

### (front matter) (mean 0.262)

<!-- editlens chunk 0.262 lines 3-11 -->
<!-- editlens paragraph 0.262 lines 3-11 -->
What survives when a paper leaves the lab: re-testing 22 robot-learning papers on a €1,350 rig, and auditing our own pre-registration Ravindu Somawansa Shisso Robotics ravindu.somawansa@gmail.com∗ verdict it keeps the claim in the paper’s words, our pass mark, our measurement and the published rows that rebuild it.

### Abstract (mean 0.164)

<!-- editlens chunk 0.164 lines 12-35 -->
<!-- editlens paragraph 0.164 lines 12-35 -->
Before a learned model gets credit, the cheapest signal it must beat runs on the same rows: copy-last for Re-testing a robot-learning paper does not need a lab. a predictor, the commanded joints for a latent, episode For $45.10 of compute on a €1,350 rig, an SO-101 arm length for a judge. A method that loses to that signal has with a Jetson Orin NX, we re-tested the central claims of not shown what it claims, however good its own number recent papers under pass marks committed before each looks. The threshold itself is committed before the run, run, and every published number rebuilds from stored and §2 checks how often that held. rows. Of the 37 paper claims tested, 12 held on this hardWe chose the papers for the stack this rig runs (world ware. The failures fit three proposed classes, each named models, VLA policies, failure monitors, chunking, edge after the condition the claim did not survive. The clearlatency) and entered each one before testing it. The next est is the clock: methods that work on a desktop GPU but ones are already listed in the register file. miss the real-time budget on the edge board. The other two are zero-shot judges beaten by a trivial signal and latent planners beaten by the commanded joints. A blind 2 Auditing our own pre-registration second reader still has to confirm the classes. We also audited our own pre-registration by commit ancestry, and To rule out moving the goalposts after the fact, a gate’s the audit shows where our ordering holds and where the threshold had to be in version control before its result. Notes and commit dates can be edited by hand. Comrepository cannot prove it. mit ancestry cannot, short of rewriting history that others have already cloned, so the order of each gate is

### 1 The register (mean 0.143)

<!-- editlens chunk 0.083 lines 36-61 -->
<!-- editlens paragraph 0.083 lines 36-61 -->
read from git merge-base --is-ancestor alone, between the first commit that contains its bar and the first A robot-learning paper reports what happened on one that contains its result. Of the 89 gates logged by 2026-10setup. Of the 22 papers here, 9 were shown in simulation 31, 58 are bar-first and 0 result-first. The rest split into 6 and 7 on rigs above $20k, while 3 used a $5–20k setup, 2 same-commit, 23 with no bar and 2 with a threshold but one below $5k, and 1 does not say. Ours costs €1,350: an no result yet. Same-commit says nothing about which SO-101 arm and a Jetson Orin NX 16 GB (2 small parts was written first. The log has since grown to 93 rows (61 are not yet priced). bar-first, 7 same-commit, 0 result-first, 23 no-bar, 2 notThe register grew out of our own write-ups, 29 so far, run). each published with its data. This paper collects them in A first pass by text search read the log very differently: one table and audits how the table was kept. 36 bar-first and 31 same-commit, with 19 no-bar and 3 Take one entry. An adaptive chunking paper claims unresolved. The cause was batch logging. A bar written that choosing the chunk length from the entropy of sam- earlier in a protocol, plan, scorer or specification often pled chunks follows the task’s phases, long in transport reached the log in the same commit as its result. Tracing and short at the grasp. On our edge GPU a single deci- each same-commit gate back to that earlier file moved 21 sion takes 4,751 ms. The budget is 298 ms. So the entry to bar-first and 4 to no-bar (their bar cell declares none), records a fail on this rig, which says nothing against the and 6 stayed same-commit; the audit table gives the evimethod on the hardware it was shown on, and beside the dence line for every move. Rows that were already bar∗ Every with source number its file: first were not re-audited for a result hidden elsewhere. github.com/ravediamond/paper-register-reproducibility. One open candidate remains, the reward-model progress github.com/ravediamond/paper-register-reproducibility · 5801819

<!-- editlens chunk 0.179 lines 64-135 -->
<!-- editlens paragraph 0.246 lines 64-93 -->
test of 2026-11-01: same-commit by text search, although its protocol (6241570) is older than the log commit. Point estimates give clean verdicts, and intervals do not always agree with them. Recomputing 10 early gates from stored rows with one statistic (episode bootstrap, 2,000 resamples, percentile 95 % CI) leaves 3 with the bar inside the interval. The no-learning colour judge is the plainest case. It is right on 94.2 % of 87 episodes against a 95 % pass mark, a fail on the point, yet its interval runs from 89.6 to 98.9 %. The oscillation rate among 25 failed episodes is a pass (24.0 % against 10 %) with a lower bound of 8.0 %. A judge threshold’s false-intervention rate is a pass at 2.4 % of 42 against a 5 % ceiling, with an upper bound of 7.1 %, and because that threshold was fitted to meet the rate, its interval only describes. The register keeps the pre-registered point verdicts and flags these three as fragile. All 29 write-ups rebuild from their published rows. Cold reruns are a stricter test. From a fresh clone with no credentials, 6 gates rerun and match, 5 of them exactly. Another 12 stop at the same place, the world-model environment, which is not published yet; publishing it would unblock most of them. The remaining 11 need a larger GPU, a private checkpoint, the arm or a step the write-up leaves out. Citations and paper-side fields were checked against the papers’ PDFs and corrected. Of the 38 arXiv ids the register names, those missing from our papers mirror all belong to scheduled tests, and the one tested paper without an arXiv id was not checked against a PDF.

<!-- editlens paragraph 0.123 lines 98-105 -->
Counted by paper, 4 of the 22 hold and 13 fail (Table 1); 3 are not proven, 1 was not tested and 1 was withdrawn. By claim the picture is finer. Of 45 claim rows (42 tested), 8 test our own baselines rather than a paper, such as ”the commanded joints beat the world model”, and 5 of those reproduce. The 37 claims taken from papers split into 12 that reproduce and 18 that fail. Over all rows: 17 reproduce, 20 fail, 3 not proven, 4 not tested, 1 withdrawn.

<!-- editlens paragraph 0.284 lines 106-116 -->
state: a learned latent used to plan, rank or track progress does worse than the commanded joints or a copy-last or action-only baseline (a world model ranks the executed chunk first in 0.60 of anchors, against a pass mark of 0.8 and 0.68–0.90 for actions alone). These examples illustrate the classes; they do not count them. A protocol committed before any labelling says the labels count only once a blind second reader, given the same 20 rows on the same form, agrees with the first reading at Cohen’s κ ≥ 0.6. That reading has not happened yet.

<!-- editlens paragraph 0.338 lines 121-135 -->
With a single operator, the author, running the rig and labelling outcomes at rest and not always blind to the arm, observer bias is the main confound. Two things limit it. Where commit order shows it, the pass mark predates the run, so a label could not have moved the bar. A blind tworeader protocol for the failure classes is also committed and ready, though it has not run, and until it does no verdict has a second reader. Ordering is provable for most gates, not all: for 29 of the 89 (6 same-commit, 23 with no bar) the repository cannot show which came first, and 21 of the bar-first verdicts rest on matching a bar text in an earlier file. Under the bootstrap 3 verdicts are fragile. Cold reruns cover 6 gates so far, with the unpublished world-model environment as the main blocker. A failure here describes this rig, not the paper in its own setting, and because the papers were chosen for one stack the rate describes this register rather than the field.

<!-- editlens chunk 0.136 lines 140-145 -->
<!-- editlens paragraph 0.136 lines 140-145 -->
Work on the same arm evaluates policies. A standardized real-world benchmark reports a taxonomy of failures and recoveries for VLA policies [13], and a fleet of SO-101 cells evaluates policies at scale [14]. The vla-eval tool runs VLAs across 14 simulation benchmarks [8]. A benchmark of demonstration quality studies one method family [22]. We test something else. Our targets are the

### 4 Three failure classes (mean 0.166)

<!-- editlens chunk 0.104 lines 146-251 -->
<!-- editlens paragraph 0.068 lines 146-156 -->
claims behind methods (judges, world models, latency), We sort the 20 failed claim rows by the condition each checked against thresholds fixed before the run, with claim did not survive. Class A, the clock, is the easi- our own pre-registration audited. The closest statement est to see. The method may be sound, but on the edge of our thesis [27] scores VLA and world-action modGPU it misses the real-time budget the claim needs, as els on five dimensions, among them reproduction evithe adaptive chunking entry of §1 does (4,751 ms per de- dence and deployment affordability. Its reproductioncision against 298 ms); for that entry nothing about the evidence score counts five audit milestones (configuration mapping, task records, task coverage, training idea is refuted, the board is simply too slow for it. Class B covers zero-shot judges, models used without records, seeds), and its authors state that it is not a probtraining on this rig to judge success, failure or progress, ability that a result is correct. We give one pass or fail per that lose to a trivial signal on the same rows. A learned claim on a €1,350 rig instead. reward model detects failures at AUROC 0.818, where episode length alone reaches 0.938. Class C is quicker to github.com/ravediamond/paper-register-reproducibility · 5801819

<!-- editlens paragraph 0.228 lines 189-218 -->
A small JEPA world model learns the Dynamics: beat copy-last, every arm’s dynamics well enough to plan corruption ≥ 1.3 at K = 30. Planwith it. ning: rank the executed chunk first among 8 in ≥ 0.8 of anchors. A predictor on frozen DINOv2 G1b top-1 ≥ 0.8 at some target dispatches plans better than one on a tance. learned latent. Pretrained RoboJEPA predicts our la- 9-step L1 ≥ 15 % below copy-last tents, uses the actions, and runs on (300M) and ≥ 5 % below shuffled the robot’s computer. actions; 2-view encoder ≤ 200 ms on the Orin. A slow second level makes latent dis- Progress monotonicity Spearman tance track task progress. ρ ≤ −0.80; false stalls ≤ 10 %. A decision-aligned ranking operator G1b regret ≤ 0.10 and ≤ the on a frozen world model picks better action-only baseline + 0.05. action chunks. An event-anchored probe on imag- AUROC ≥ 0.85 and ≥ 0.05 above ined latents predicts grasp failure the current latent. better than the current latent. A conformal band on a learned fail- Successes flagged ≤ 1/20; failures ure score keeps false alarms at α flagged ≥ 50 %. while catching failures. A risk head on an action-conditioned ≥ 5/8 failures caught at ≤ latent warns before failures. 1/20 false interventions; actionconditioned iff true ≥ shuffled + 0.05. A verifier on observable history flags ≥ 5/8 failures at ≤ 1/20 false ina failing rollout early enough to cor- terventions. rect it.

<!-- editlens paragraph 0.186 lines 242-251 -->
A 4B reward model judges SO-101 Pooled AUROC ≥ 0.85 and rollouts zero-shot. within-policy ≥ 0.8 on ≥ 5 of 7 policies. A 450M VLA succeeds on an SO-101 10-trial operator-judged gate (no task and can run on low-cost hard- numeric pass mark registered); ware. chunk inference within the async budget (667 ms).

<!-- editlens chunk 0.215 lines 282-401 -->
<!-- editlens paragraph 0.193 lines 282-296 -->
22.7 % of successes flagged at α = fail 5 %; 46 % of failures caught v1 AUROC 0.93 came from time fail and length; v2 0.789 vs 0.708 shuffled, 3/8 at 5/42 the paper’s verifier family on our fail rollouts (a GRU on pooled RGB statistics and actions): 2/8 caught at 3/42 false interventions, AUROC 0.59; cosine drift of the W1 latent 0/8, AUROC 0.30 pooled AUROC 0.818 on 2099 fail ArmnetBench rollouts; episode length alone 0.938 9/10 on bowls; 974 ms in PyTorch, reproduces 238 ms with vla.cpp on the Orin NX

<!-- editlens paragraph 0.405 lines 384-401 -->
Chunk length chosen from the entropy of N sampled chunks follows the task’s phases (long in transport, short at the grasp), lowers the boundary jump, and costs little with batched sampling. Picking among N sampled chunks by their flow residual under the precommit observation fits what happens next better than a random or stale pick, with no added controlstep delay. With long open-loop commitment, cutting a flow-matching VLA’s Euler steps from 10 to 2 contracts the action cloud around an unchanged centroid, saves most of the inference time and avoids edge-GPU thermal throttling. Reading a progress distribution out at the supported peak nearest the previous estimate steadies the estimate and lets it fall during real setbacks, with no worse detection of the stages.

<!-- editlens chunk 0.174 lines 406-473 -->
<!-- editlens paragraph 0.184 lines 406-451 -->
upstream’s own trainer on our withdrawn data: task swap 0.020°, per-layout 38.9 %; control, their released LIBERO checkpoint run here: 0.105 (≈ 5.5° of pan) 10-trial operator-judged gate (no 9/10 for $9.7; 355 ms per chunk reproduces numeric pass mark registered); for on the Orin NX; reranking no-go reranking (H0): oracle / mean er- (0.76, 1.84×) ror ≤ 0.7 and N = 8 ≤ 1.5× the latency. ≥ 10 % of failed episodes oscillate 20.3 % of all episodes, 24.0 % of reproduces (their criterion). failures; REKI trained on my data: 19/20 + 19/20 on the arm, oscillates in 1/40 Best gradient-free method cuts the prefix overwrite cuts the jump 71– not median jump ≥ 50 % against naive 73 % against naive async at +0.4 proven async, drift ≤ +10 %, within 667 ms; tuned LeRobot identity mode ms. is close Crossover in [1.0, 2.0] s; at 2 s high- no crossover: W1 0.382 ± 0.005 → not level error ≤ 0.95 × low-level; 0.563 ± 0.007, high level 0.769 ± proven learned macro-actions ≥ net joint 0.009 → 0.759 ± 0.009 (0.73–2 s); displacement on cosine. cosine 0.608 ± 0.007 vs 0.551 ± 0.006 W1’s mean R2 from latent to joints W1 mean R2 0.565, anisotropy reproduces < 0.80; anisotropy (max − min 0.639 (shoulder lift 0.91, wrist flex per-joint R2 ) ≥ 0.20; the higher-R2 0.27); frozen DINOv2-S 0.867 / 0.301 model has the higher G1b top-1. τ below the 10th percentile of non- τ = 1.249 on W1 latents of 69 real fail equivalent pairs and ≤ 0.40; as a rollouts; as a monitor 3/8 at 6/42 monitor ≥ 5/8 failures at ≤ 2/42; (S = 30), AUROC 0.756 vs shuffled ≥ 0.05 AUROC over a shuffled 0.560 drafter. median h* in transport ≥ grasp h* 2 in transport and 2 at the grasp fail window + 2; jump with AAC + (86 % of decisions at the floor); overwrite ≤ fixed + overwrite at d jump 0.973 vs 0.940; N = 20 deci= 8; an N = 20 decision ≤ 298 ms sion 4,751 ms (sequential) on the on the Orin. Orin PACT beats a random pick and the stale-observation residual at d = 8 (CIs < 0); its delay on the Orin ≤ the naive delay; at that delay it still beats a single sample.

<!-- editlens chunk 0.236 lines 489-508 -->
<!-- editlens paragraph 0.236 lines 489-508 -->
[14] ArmnetBench v0.1: Parallel Real-World Evaluation of Manipulation Policies on a Low-Cost Arm Farm, A €1,350 rig and $45.10 of compute were enough to 2026. arXiv:2607.24481. re-test these claims and publish every row behind the verdicts, and 12 of 37 held. Money was never [15] TurboVLA: Real-Time Vision-Language-Action Model at 32 Hz on an RTX 4090 with <1 GB the constraint. Order was: keeping each pass mark VRAM, 2026. arXiv:2607.27205. ahead of its result, which our own history cannot prove for 29 of 89 gates. If you re-test a paper on [16] ContactGuard: Pre-Contact Execution Monitoring a cheap rig, start with its cheapest baseline on the with Action-Conditioned Latent World Models, same rows, and commit the threshold before you look. 2026. arXiv:2608.13438. Every number here can be rebuilt from the repository (github.com/ravediamond/paper-register-reproducibility). [17] VLA-Corrector: Stage-Aware Observable State Understanding for Prompt-Based Closed-Loop Recovery of Vision-Language-Action Policies, 2026.
