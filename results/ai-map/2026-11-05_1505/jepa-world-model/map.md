# Paper AI map: paper-jepa-world-model

EditLens `pangram/editlens_Llama-3.2-3B`; raw score in [0, 1] (0 = human, 1 = AI). No threshold is published, so there are no labels; read the scores next to the reference below. A map for the owner to rewrite by hand.

Human reference (3 papers from before 2022-11, same extraction): paper means 0.053, 0.055, 0.095; median 0.055; chunk scores 0.026 to 0.106 (max 0.106). AI reference: n/a (see notes).

## rendered source (numbers filled)

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| Abstract | 150 | 1 | 0.131 | 0.131 | +0.045 | 'We trained a small JEPA world model in the LeWorldModel recipe for $3.30 of rent' | 7-7 |
| Introduction | 465 | 1 | 0.149 | 0.149 | -0.027 | 'The first draft of this paper argued something else. We had read the failures as' | 15-15 |
| Setup | 247 | 1 | 0.061 | 0.061 | -0.010 | 'In October we found a loading bug. A timing test on the on-board computer loaded' | 27-27 |
| **The register** | 229 | 1 | 0.224 | 0.224 | +0.003 | 'The predictor does predict its own latent: at K = 30 its open-loop error is 0.31' | 60-60 |
| What the encoder knows | 311 | 1 | 0.115 | 0.115 | +0.009 | 'At rest our model is level with the colour judge, whose CI overlaps its own, and' | 78-78 |
| Where the predictor fails | 369 | 1 | 0.184 | 0.184 | -0.002 | 'One pass in the register uses the imagined latent: in the anticipation step of t' | 106-106 |
| **Related work** | 179 | 1 | 0.304 | 0.304 | +0.067 | 'LeWorldModel [1] trains the recipe we use end to end from pixels and plans with ' | 110-110 |
| **Limitations** | 175 | 1 | 0.263 | 0.263 | +0.006 | 'The split between encoder and predictor is exploratory. We chose its probes afte' | 114-114 |
| Conclusion | 53 | 1 | 0.221 | 0.221 | +0.025 | 'We tested 20 published uses on a $3.30 world model. At this data scale the encod' | 118-118 |
| (figure and table captions) | 144 | 1 | 0.161 | 0.161 | +0.000 | 'Table 1: The register: every use of our world model re-tested here (with the fro' | 33-33 |

Paper mean 0.170; 89 % of words in chunks above the human-reference maximum (0.106).

## built PDF

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| **(front matter)** (short, noisy) | 30 | 1 | 0.136 | 0.136 | +0.000 | 'A small JEPA world model on a low-cost arm: the encoder reads the outcome, the p' | 3-8 |
| **Abstract** | 1434 | 3 | 0.109 | 0.167 | -0.029 | 'rows match a pre-registration record in the commit history. In 19 of them the ba' | 38-61 |
| **4 What the encoder knows** | 986 | 2 | 0.146 | 0.280 | +0.041 | 'uses its actions, and with a failure-class AUROC of 0.501, below the same sanity' | 623-631 |

Paper mean 0.124; 30 % of words in chunks above the human-reference maximum (0.106).
