# Paper AI map: paper-reward-models-stopping-rule

EditLens `pangram/editlens_Llama-3.2-3B`; raw score in [0, 1] (0 = human, 1 = AI). No threshold is published, so there are no labels; read the scores next to the reference below. A map for the owner to rewrite by hand.

Human reference (3 papers from before 2022-11, same extraction): paper means 0.053, 0.055, 0.095; median 0.055; chunk scores 0.026 to 0.106 (max 0.106). AI reference: n/a (see notes).

## rendered source (numbers filled)

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| Abstract | 147 | 1 | 0.175 | 0.175 | -0.026 | 'Reward models that score robot rollouts are also used as failure detectors. We c' | 9-16 |
| 1 Introduction | 208 | 1 | 0.176 | 0.176 | -0.053 | 'Papers that evaluate a reward model as a failure detector normally compare it wi' | 20-25 |
| **2 Data and labels** | 108 | 1 | 0.211 | 0.211 | -0.005 | 'ArmnetBench v0.1 has 8 tasks and 7 policies on the SO-101. We use its 2,047 poli' | 37-42 |
| 3 The length baseline | 173 | 1 | 0.125 | 0.125 | -0.035 | 'On ArmnetBench, episode length is a strong failure detector within each policy (' | 46-48 |
| 4 Length is more than the timeout | 168 | 1 | 0.189 | 0.189 | +0.019 | "We take each task's longest episode as its timeout. Only 8.7 % of failures run t" | 73-76 |
| 5 Judges and monitors on our rollouts | 344 | 1 | 0.173 | 0.173 | -0.002 | 'The bar for mid-episode monitors is at least 5 of 8 failures at no more than 1 o' | 102-108 |
| **6 Related work** | 125 | 1 | 0.301 | 0.301 | +0.056 | 'Robometer scales a general-purpose reward model through trajectory comparisons. ' | 129-137 |
| 7 Limitations | 188 | 1 | 0.121 | 0.121 | -0.031 | 'The judge pass on our own rollouts rests on 8 failures. Its operating thresholds' | 141-150 |
| 8 Conclusion | 61 | 1 | 0.193 | 0.193 | +0.000 | 'On ArmnetBench, where runs end at a time limit, episode length beat both reward ' | 154-157 |
| **Appendix: from plain name to analysis** (short, noisy) | 15 | 1 | 0.240 | 0.240 | +0.000 | 'Every number is recomputable from the repository; this table maps each analysis ' | 161-161 |
| (figure and table captions) | 140 | 1 | 0.084 | 0.084 | +0.000 | 'Table 1: ArmnetBench, failure AUROC with 95 % episode-bootstrap CIs. Read down t' | 58-125 |

Paper mean 0.170; 92 % of words in chunks above the human-reference maximum (0.106).

## built PDF

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| **(front matter)** | 1647 | 4 | 0.060 | 0.078 | +0.005 | 'Papers that evaluate a reward model as a failure detector normally compare it wi' | 32-46 |
| **Appendix: from plain name to analysis** | 156 | 1 | 0.104 | 0.104 |  | 'farm. arXiv preprint arXiv:2607.24481, 2026. [13] Chang Song, Bin Qian, Yan Feng' | 511-530 |

Paper mean 0.064; 0 % of words in chunks above the human-reference maximum (0.106).
