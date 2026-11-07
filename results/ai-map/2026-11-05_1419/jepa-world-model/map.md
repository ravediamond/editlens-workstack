# Paper AI map: paper-jepa-world-model

EditLens `pangram/editlens_Llama-3.2-3B`; raw score in [0, 1] (0 = human, 1 = AI). No threshold is published, so there are no labels; read the scores next to the reference below. A map for the owner to rewrite by hand.

Human reference (3 papers from before 2022-11, same extraction): paper means 0.053, 0.055, 0.095; median 0.055; chunk scores 0.026 to 0.106 (max 0.106). AI reference: n/a (see notes).

## rendered source (numbers filled)

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| Abstract | 157 | 1 | 0.086 | 0.086 | -0.098 | 'We trained a small JEPA world model in the LeWorldModel recipe for $3.30 of rent' | 7-7 |
| Introduction | 468 | 1 | 0.176 | 0.176 | +0.013 | 'The first draft of this paper argued something else. We read the failures as a s' | 15-15 |
| Setup | 246 | 1 | 0.071 | 0.071 | -0.054 | 'In October we found a loading bug. A timing test on the on-board computer loaded' | 27-27 |
| **The register** | 226 | 1 | 0.221 | 0.221 | -0.030 | 'The predictor does predict its own latent. At K = 30 its open-loop error is 0.31' | 60-60 |
| What the encoder knows | 316 | 1 | 0.106 | 0.106 | -0.017 | 'At rest our model is level with the colour judge. The two CIs overlap. Our model' | 78-78 |
| Where the predictor fails | 362 | 1 | 0.186 | 0.186 | -0.001 | 'One pass in the register uses the imagined latent. In the anticipation step of t' | 106-106 |
| **Related work** | 183 | 1 | 0.238 | 0.238 | +0.018 | 'LeWorldModel [1] trains the recipe we use end to end from pixels and plans with ' | 110-110 |
| **Limitations** | 170 | 1 | 0.257 | 0.257 | +0.035 | 'The split between encoder and predictor is exploratory. We chose its probes afte' | 114-114 |
| Conclusion | 53 | 1 | 0.197 | 0.197 | -0.069 | 'We tested 20 published uses on a $3.30 world model. At this data scale the encod' | 118-118 |
| (figure and table captions) | 144 | 1 | 0.161 | 0.161 | -0.012 | 'Table 1: The register: every use of our world model re-tested here (with the fro' | 33-33 |

Paper mean 0.165; 69 % of words in chunks above the human-reference maximum (0.106).

## built PDF

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| **(front matter)** (short, noisy) | 30 | 1 | 0.136 | 0.136 | +0.002 | 'A small JEPA world model on a low-cost arm: the encoder reads the outcome, the p' | 3-8 |
| **Abstract** | 1454 | 3 | 0.138 | 0.207 | -0.003 | 'ContactGuard [9] finds that probes on the imagined latent beat probes on the cur' | 186-191 |
| **4 What the encoder knows** | 1019 | 2 | 0.105 | 0.168 |  | 'the frozen bar. One pass in the register uses the imagined latent. In the antici' | 641-648 |

Paper mean 0.125; 60 % of words in chunks above the human-reference maximum (0.106).
