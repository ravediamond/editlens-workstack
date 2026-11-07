# Paper AI map: paper-reward-models-stopping-rule

EditLens `pangram/editlens_Llama-3.2-3B`; raw score in [0, 1] (0 = human, 1 = AI). No threshold is published, so there are no labels; read the scores next to the reference below. A map for the owner to rewrite by hand.

Human reference (3 papers from before 2022-11, same extraction): paper means 0.053, 0.055, 0.095; median 0.055; chunk scores 0.026 to 0.106 (max 0.106). AI reference: n/a (see notes).

## rendered source (numbers filled)

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| **Abstract** | 170 | 1 | 0.329 | 0.329 |  | 'Reward models that score robot rollouts are also used as failure detectors, and ' | 9-17 |
| **1 Introduction** | 205 | 1 | 0.390 | 0.390 |  | 'A reward model that scores robot rollouts is also a failure detector, and papers' | 21-31 |
| 2 Data and labels | 86 | 1 | 0.189 | 0.189 |  | 'ArmnetBench v0.1 (SO-101, 8 tasks, 7 policies): 2,047 policy rollouts with a suc' | 35-39 |
| 3 The length baseline | 187 | 1 | 0.144 | 0.144 |  | 'Table 1 carries the numbers. Pooled over policies, length gives 0.938 (CI 0.925–' | 43-53 |
| 4 Is it the timeout? | 180 | 1 | 0.227 | 0.227 |  | "Only 8.7 % of failures run to the task's longest episode. Observing length only " | 70-80 |
| 5 Judges and monitors on our rollouts | 353 | 1 | 0.273 | 0.273 |  | '**Mid-episode.** A Gemini sliding-window judge catches 0 of 8 failures at 1 of 4' | 100-107 |
| **6 Related work** | 160 | 1 | 0.357 | 0.357 |  | 'Reward models are increasingly proposed as zero-shot failure detectors for manip' | 128-138 |
| 7 Limitations | 156 | 1 | 0.180 | 0.180 |  | "Two task families (ArmnetBench's eight tasks, our bowls task); our labels are th" | 142-149 |
| Appendix: from plain name to analysis (short, noisy) | 15 | 1 | 0.240 | 0.240 |  | 'Every number is recomputable from the repository; this table maps each analysis ' | 153-153 |
| (figure and table captions) | 216 | 1 | 0.127 | 0.127 |  | 'Fifty own rollouts: failures caught (of 8) against successes flagged (of 42). Ci' | 124-124 |

Paper mean 0.250; 100 % of words in chunks above the human-reference maximum (0.106).

## built PDF

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| (front matter) (short, noisy) | 30 | 1 | 0.092 | 0.092 | +0.000 | 'What a reward model can show depends on who stopped the episode: failure judges ' | 3-8 |
| **Abstract** | 162 | 1 | 0.343 | 0.343 | +0.000 | 'Reward models that score robot rollouts are also used as failure detectors, and ' | 10-23 |
| **1 Introduction** | 249 | 1 | 0.212 | 0.212 | +0.000 | 'numbers, and set every learned judge and monitor we ran against it. Contribution' | 43-50 |
| **2 Data and labels** | 87 | 1 | 0.239 | 0.239 | +0.000 | 'ArmnetBench v0.1 [12] (SO-101, 8 tasks, 7 policies): 2,047 policy rollouts with ' | 52-58 |
| 3 The length baseline | 261 | 1 | 0.091 | 0.091 | +0.000 | 'Table 1: ArmnetBench, failure AUROC with 95 % episode-bootstrap CIs. The Robomet' | 113-118 |
| 5 Judges and monitors on our rollouts | 838 | 2 | 0.051 | 0.065 | +0.000 | 'Table 2: Judges and monitors on 50 own operator-stopped rollouts (42 successes, ' | 297-298 |
| 7 Limitations | 335 | 1 | 0.066 | 0.066 | +0.000 | 'Two task families (ArmnetBench’s eight tasks, our bowls task); our labels are th' | 372-375 |
| Appendix: from plain name to analysis | 154 | 1 | 0.099 | 0.099 | +0.000 | '[13] Chang Song, Bin Qian, Yan Feng, and Zhijie Song. Vla-corrector: Stage-aware' | 531-550 |

Paper mean 0.111; 24 % of words in chunks above the human-reference maximum (0.106).
