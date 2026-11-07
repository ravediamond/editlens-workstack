# Paper AI map: paper-reward-models-stopping-rule

EditLens `pangram/editlens_Llama-3.2-3B`; raw score in [0, 1] (0 = human, 1 = AI). No threshold is published, so there are no labels; read the scores next to the reference below. A map for the owner to rewrite by hand.

Human reference (3 papers from before 2022-11, same extraction): paper means 0.053, 0.055, 0.095; median 0.055; chunk scores 0.026 to 0.106 (max 0.106). AI reference: n/a (see notes).

## rendered source (numbers filled)

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| **Abstract** | 161 | 1 | 0.393 | 0.393 | +0.014 | 'Episode length is the failure detector that zero-shot reward models must beat, a' | 9-16 |
| **1 Introduction** | 214 | 1 | 0.252 | 0.252 | -0.027 | 'A reward model that scores robot rollouts is also a failure detector, and papers' | 20-25 |
| 2 Data and labels | 109 | 1 | 0.198 | 0.198 | +0.000 | 'ArmnetBench v0.1 covers the SO-101 with 8 tasks and 7 policies. We use its 2,047' | 37-42 |
| 3 The length baseline | 169 | 1 | 0.187 | 0.187 | -0.006 | 'Both reward models, run zero-shot, fall below it on this benchmark. Robometer-4B' | 50-56 |
| 4 Length is more than the timeout | 187 | 1 | 0.141 | 0.141 |  | 'If length only reflected the timeout, its signal would sit in the few runs that ' | 73-77 |
| 5 Judges and monitors on our rollouts | 357 | 1 | 0.183 | 0.183 | -0.010 | 'A judge that sees the finished episode works on these rollouts, and the input fo' | 93-102 |
| 6 Related work | 156 | 1 | 0.219 | 0.219 | -0.041 | 'Robometer and TOPReward are the two reward models we test. Robometer scales a ge' | 131-140 |
| 7 Limitations | 196 | 1 | 0.159 | 0.159 | -0.096 | 'The judge pass on our own rollouts rests on 8 failures and on operating threshol' | 144-153 |
| **8 Conclusion** | 71 | 1 | 0.303 | 0.303 | +0.000 | 'Before evaluating a reward model as a failure detector, run episode length withi' | 157-160 |
| Appendix: from plain name to analysis (short, noisy) | 15 | 1 | 0.240 | 0.240 | +0.000 | 'Every number is recomputable from the repository; this table maps each analysis ' | 164-164 |
| (figure and table captions) | 140 | 1 | 0.084 | 0.084 | +0.000 | 'Table 1: ArmnetBench, failure AUROC with 95 % episode-bootstrap CIs. Read down t' | 58-127 |

Paper mean 0.205; 92 % of words in chunks above the human-reference maximum (0.106).

## built PDF

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| **(front matter)** (short, noisy) | 30 | 1 | 0.092 | 0.092 | +0.027 | 'What a reward model can show depends on who stopped the episode: failure judges ' | 3-8 |
| **Abstract** | 850 | 2 | 0.136 | 0.170 | +0.060 | 'Episode length is the failure detector that zero-shot reward models must beat, a' | 10-21 |
| **0.667. Failed rollouts are slow, not timed out, and both** | 993 | 2 | 0.075 | 0.118 |  | 'ward reads the token probabilities of a video-language model as hidden rewards, ' | 383-399 |
| Appendix: from plain name to analysis | 58 | 1 | 0.052 | 0.052 | -0.002 | 'Every number is recomputable from the repository; this [13] Chang Song, Bin Qian' | 576-582 |

Paper mean 0.102; 50 % of words in chunks above the human-reference maximum (0.106).
