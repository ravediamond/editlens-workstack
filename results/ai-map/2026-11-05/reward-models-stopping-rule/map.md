# Paper AI map: paper-reward-models-stopping-rule

EditLens `pangram/editlens_Llama-3.2-3B`; raw score in [0, 1] (0 = human, 1 = AI). No threshold is published, so there are no labels; read the scores next to the reference below. A map for the owner to rewrite by hand.

Human reference (3 papers from before 2022-11, same extraction): paper means 0.053, 0.055, 0.095; median 0.055; chunk scores 0.026 to 0.106 (max 0.106). AI reference: n/a (see notes).

## rendered source (numbers filled)

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| **Abstract** | 179 | 1 | 0.343 | 0.343 | +0.013 | 'Reward models that score robot rollouts are also used as failure detectors, and ' | 9-18 |
| **1 Introduction** | 183 | 1 | 0.299 | 0.299 | -0.091 | 'When a benchmark stops failed runs at a time limit, the length of an episode enc' | 25-28 |
| 2 Data and labels | 101 | 1 | 0.154 | 0.154 | -0.035 | 'ArmnetBench v0.1 covers the SO-101 with 8 tasks and 7 policies. We use its 2,047' | 37-42 |
| 3 The length baseline | 211 | 1 | 0.212 | 0.212 | +0.069 | "Robometer's within-policy number has no episode-bootstrap CI. Its per-episode sc" | 58-60 |
| 4 Is it the timeout? | 220 | 1 | 0.174 | 0.174 | -0.053 | 'If length only reflected the timeout, its signal would sit in the few runs that ' | 77-82 |
| 5 Judges and monitors on our rollouts | 366 | 1 | 0.184 | 0.184 | -0.089 | 'A judge that sees the finished episode works on these rollouts, and the input fo' | 100-109 |
| **6 Related work** | 178 | 1 | 0.290 | 0.290 | -0.067 | 'Robometer and TOPReward are the two reward models we test. Robometer scales a ge' | 138-149 |
| 7 Limitations | 178 | 1 | 0.120 | 0.120 | -0.060 | "The results cover two task families, ArmnetBench's eight tasks and our bowls tas" | 153-161 |
| Appendix: from plain name to analysis (short, noisy) | 15 | 1 | 0.240 | 0.240 | +0.000 | 'Every number is recomputable from the repository; this table maps each analysis ' | 165-165 |
| (figure and table captions) | 216 | 1 | 0.127 | 0.127 | +0.000 | 'Fifty own rollouts: failures caught (of 8) against successes flagged (of 42). Ci' | 134-134 |

Paper mean 0.209; 100 % of words in chunks above the human-reference maximum (0.106).

## built PDF

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| **(front matter)** | 61 | 1 | 0.166 | 0.166 | +0.074 | 'What a reward model can show depends on who stopped the episode: failure judges ' | 3-10 |
| **Abstract** | 1551 | 3 | 0.103 | 0.145 | -0.240 | 'Figure 3: Fifty own rollouts: failures caught (of 8) against successes flagged (' | 291-296 |

Paper mean 0.106; 59 % of words in chunks above the human-reference maximum (0.106).
