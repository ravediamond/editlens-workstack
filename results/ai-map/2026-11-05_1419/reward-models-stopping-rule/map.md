# Paper AI map: paper-reward-models-stopping-rule

EditLens `pangram/editlens_Llama-3.2-3B`; raw score in [0, 1] (0 = human, 1 = AI). No threshold is published, so there are no labels; read the scores next to the reference below. A map for the owner to rewrite by hand.

Human reference (3 papers from before 2022-11, same extraction): paper means 0.053, 0.055, 0.095; median 0.055; chunk scores 0.026 to 0.106 (max 0.106). AI reference: n/a (see notes).

## rendered source (numbers filled)

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| Abstract | 147 | 1 | 0.175 | 0.175 | -0.217 | 'Reward models that score robot rollouts are also used as failure detectors. We c' | 9-16 |
| **1 Introduction** | 198 | 1 | 0.218 | 0.218 | -0.035 | 'Papers that evaluate a reward model as a failure detector usually compare it wit' | 20-24 |
| 2 Data and labels | 108 | 1 | 0.211 | 0.211 | +0.013 | 'ArmnetBench v0.1 has 8 tasks and 7 policies on the SO-101. We use its 2,047 poli' | 36-41 |
| 3 The length baseline | 173 | 1 | 0.125 | 0.125 | -0.061 | 'On ArmnetBench, episode length is a strong failure detector within each policy (' | 45-47 |
| 4 Length is more than the timeout | 168 | 1 | 0.189 | 0.189 | +0.048 | "We take each task's longest episode as its timeout. Only 8.7 % of failures run t" | 72-75 |
| 5 Judges and monitors on our rollouts | 344 | 1 | 0.173 | 0.173 | -0.011 | 'The bar for mid-episode monitors is at least 5 of 8 failures at no more than 1 o' | 101-107 |
| **6 Related work** | 125 | 1 | 0.301 | 0.301 | +0.082 | 'Robometer scales a general-purpose reward model through trajectory comparisons. ' | 128-136 |
| 7 Limitations | 188 | 1 | 0.121 | 0.121 | -0.038 | 'The judge pass on our own rollouts rests on 8 failures. Its operating thresholds' | 140-149 |
| 8 Conclusion | 61 | 1 | 0.193 | 0.193 | -0.110 | 'On ArmnetBench, where runs end at a time limit, episode length beat both reward ' | 153-156 |
| **Appendix: from plain name to analysis** (short, noisy) | 15 | 1 | 0.240 | 0.240 | +0.000 | 'Every number is recomputable from the repository; this table maps each analysis ' | 160-160 |
| (figure and table captions) | 140 | 1 | 0.084 | 0.084 | +0.000 | 'Table 1: ArmnetBench, failure AUROC with 95 % episode-bootstrap CIs. Read down t' | 57-124 |

Paper mean 0.175; 92 % of words in chunks above the human-reference maximum (0.106).

## built PDF

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| **(front matter)** (short, noisy) | 30 | 1 | 0.081 | 0.081 | -0.011 | 'What a reward model can show depends on who stopped the episode: failure judges ' | 3-8 |
| **Abstract** | 1601 | 4 | 0.054 | 0.075 | -0.082 | 'Papers that evaluate a reward model as a failure detector usually compare it wit' | 48-63 |
| **Appendix: from plain name to analysis** | 156 | 1 | 0.053 | 0.053 | +0.001 | 'farm. arXiv preprint arXiv:2607.24481, 2026. [13] Chang Song, Bin Qian, Yan Feng' | 528-547 |

Paper mean 0.055; 0 % of words in chunks above the human-reference maximum (0.106).
