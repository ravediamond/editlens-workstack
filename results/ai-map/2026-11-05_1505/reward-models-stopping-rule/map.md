# Paper AI map: paper-reward-models-stopping-rule

EditLens `pangram/editlens_Llama-3.2-3B`; raw score in [0, 1] (0 = human, 1 = AI). No threshold is published, so there are no labels; read the scores next to the reference below. A map for the owner to rewrite by hand.

Human reference (3 papers from before 2022-11, same extraction): paper means 0.053, 0.055, 0.095; median 0.055; chunk scores 0.026 to 0.106 (max 0.106). AI reference: n/a (see notes).

## rendered source (numbers filled)

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| Abstract | 150 | 1 | 0.202 | 0.202 | +0.026 | 'Reward models that score robot rollouts are also used as failure detectors, and ' | 9-16 |
| **1 Introduction** | 195 | 1 | 0.229 | 0.229 | +0.011 | 'Papers that evaluate a reward model as a failure detector usually compare it wit' | 20-24 |
| 2 Data and labels | 109 | 1 | 0.216 | 0.216 | +0.005 | 'ArmnetBench v0.1 has 8 tasks and 7 policies on the SO-101. We use its 2,047 poli' | 36-41 |
| 3 The length baseline | 170 | 1 | 0.160 | 0.160 | +0.035 | 'On ArmnetBench, episode length is a strong failure detector within each policy (' | 45-47 |
| 4 Length is more than the timeout | 169 | 1 | 0.170 | 0.170 | -0.019 | "We take each task's longest episode as its timeout, and only 8.7 % of failures r" | 72-75 |
| 5 Judges and monitors on our rollouts | 341 | 1 | 0.174 | 0.174 | +0.002 | 'No mid-episode monitor reaches its bar of at least 5 of 8 failures at no more th' | 101-107 |
| **6 Related work** | 127 | 1 | 0.246 | 0.246 | -0.056 | 'Robometer scales a general-purpose reward model through trajectory comparisons, ' | 128-136 |
| 7 Limitations | 192 | 1 | 0.151 | 0.151 | +0.031 | 'The judge pass on our own rollouts rests on 8 failures and on operating threshol' | 140-149 |
| 8 Conclusion | 61 | 1 | 0.193 | 0.193 | +0.000 | 'On ArmnetBench, where runs end at a time limit, episode length beat both reward ' | 153-156 |
| **Appendix: from plain name to analysis** (short, noisy) | 15 | 1 | 0.240 | 0.240 | +0.000 | 'Every number is recomputable from the repository; this table maps each analysis ' | 160-160 |
| (figure and table captions) | 140 | 1 | 0.084 | 0.084 | +0.000 | 'Table 1: ArmnetBench, failure AUROC with 95 % episode-bootstrap CIs. Read down t' | 57-124 |

Paper mean 0.180; 92 % of words in chunks above the human-reference maximum (0.106).

## built PDF

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| **(front matter)** | 1014 | 2 | 0.055 | 0.055 | -0.026 | 'Papers that evaluate a reward model as a failure detector usually compare it wit' | 30-44 |
| **4 Length is more than the timeout** | 338 | 1 | 0.107 | 0.107 |  | 'of 8 failures at no more than 1 of 20 false interventions on these 50 rollouts (' | 177-195 |
| **5 Judges and monitors on our rollouts** | 324 | 1 | 0.049 | 0.049 |  | 'ReAP [6], which predicts action-conditioned risk. VLACorrector [13] verifies sta' | 352-354 |

Paper mean 0.064; 20 % of words in chunks above the human-reference maximum (0.106).
