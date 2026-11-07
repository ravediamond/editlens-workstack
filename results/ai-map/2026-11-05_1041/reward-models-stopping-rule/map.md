# Paper AI map: paper-reward-models-stopping-rule

EditLens `pangram/editlens_Llama-3.2-3B`; raw score in [0, 1] (0 = human, 1 = AI). No threshold is published, so there are no labels; read the scores next to the reference below. A map for the owner to rewrite by hand.

Human reference (3 papers from before 2022-11, same extraction): paper means 0.053, 0.055, 0.095; median 0.055; chunk scores 0.026 to 0.106 (max 0.106). AI reference: n/a (see notes).

## rendered source (numbers filled)

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| **Abstract** | 156 | 1 | 0.379 | 0.379 | +0.036 | 'Episode length is a failure detector that zero-shot reward models must beat, and' | 9-16 |
| **1 Introduction** | 210 | 1 | 0.280 | 0.280 | -0.020 | 'We started with a narrower claim, that elapsed time is the reward model to beat.' | 27-29 |
| 2 Data and labels | 109 | 1 | 0.198 | 0.198 | +0.044 | 'ArmnetBench v0.1 covers the SO-101 with 8 tasks and 7 policies. We use its 2,047' | 37-42 |
| 3 The length baseline | 166 | 1 | 0.193 | 0.193 | -0.020 | 'Both reward models fall below it. Robometer-4B, run zero-shot as its authors shi' | 50-56 |
| 4 Is it the timeout? | 200 | 1 | 0.169 | 0.169 | -0.004 | 'If length only reflected the timeout, its signal would sit in the few runs that ' | 73-78 |
| 5 Judges and monitors on our rollouts | 366 | 1 | 0.193 | 0.193 | +0.009 | 'A judge that sees the finished episode works on these rollouts, and the input fo' | 95-104 |
| 6 Related work | 162 | 1 | 0.260 | 0.260 | -0.030 | 'Robometer and TOPReward are the two reward models we test. Robometer scales a ge' | 133-144 |
| 7 Limitations | 187 | 1 | 0.256 | 0.256 | +0.135 | 'The result most likely to move is the judge pass on our own rollouts. It rests o' | 148-157 |
| **8 Conclusion** | 71 | 1 | 0.303 | 0.303 |  | 'Before evaluating a reward model as a failure detector, run episode length withi' | 161-164 |
| Appendix: from plain name to analysis (short, noisy) | 15 | 1 | 0.240 | 0.240 | +0.000 | 'Every number is recomputable from the repository; this table maps each analysis ' | 168-168 |
| (figure and table captions) | 140 | 1 | 0.084 | 0.084 | -0.043 | 'Table 1: ArmnetBench, failure AUROC with 95 % episode-bootstrap CIs. Read down t' | 58-129 |

Paper mean 0.226; 92 % of words in chunks above the human-reference maximum (0.106).

## built PDF

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| **(front matter)** | 59 | 1 | 0.064 | 0.064 | -0.101 | 'What a reward model can show depends on who stopped the episode: failure judges ' | 3-11 |
| **Abstract** | 1834 | 4 | 0.076 | 0.105 | -0.027 | 'A reward model that scores robot rollouts is also a failure detector, and papers' | 37-48 |
| **Appendix: from plain name to analysis** | 58 | 1 | 0.053 | 0.053 |  | 'Every number is recomputable from the repository; this [13] Chang Song, Bin Qian' | 553-559 |

Paper mean 0.075; 0 % of words in chunks above the human-reference maximum (0.106).
