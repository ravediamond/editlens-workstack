# Paper AI map: paper-jepa-world-model

EditLens `pangram/editlens_Llama-3.2-3B`; raw score in [0, 1] (0 = human, 1 = AI). No threshold is published, so there are no labels; read the scores next to the reference below. A map for the owner to rewrite by hand.

Human reference (3 papers from before 2022-11, same extraction): paper means 0.053, 0.055, 0.095; median 0.055; chunk scores 0.026 to 0.106 (max 0.106). AI reference: n/a (see notes).

## rendered source (numbers filled)

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| Abstract | 169 | 1 | 0.184 | 0.184 | +0.068 | 'For $3.30 of rented GPU time we trained a small JEPA world model in the LeWorldM' | 7-7 |
| Introduction | 539 | 1 | 0.163 | 0.163 | +0.025 | 'The controls came after the data, which limits what they can show. Each readout ' | 19-19 |
| Setup | 249 | 1 | 0.125 | 0.125 | +0.000 | 'In October, a timing test on the on-board computer loaded our checkpoint with X.' | 27-27 |
| **The register** | 254 | 1 | 0.251 | 0.251 | +0.019 | 'The predictor does predict its own latent: at K = 30 its open-loop error is 0.31' | 60-60 |
| What the encoder knows | 320 | 1 | 0.123 | 0.123 | -0.006 | 'The anchor column depends on how the five seeds are combined. Averaging the pred' | 80-80 |
| Where the predictor fails | 388 | 1 | 0.186 | 0.186 | +0.014 | 'A reader may object that one pass in the register is predictive. In the anticipa' | 106-106 |
| Related work | 206 | 1 | 0.220 | 0.220 | +0.015 | 'LeWorldModel [1] trains the recipe we use end to end from pixels and plans with ' | 110-110 |
| **Limitations** | 180 | 1 | 0.222 | 0.222 | -0.104 | 'The split between encoder and predictor is exploratory. Its probes were chosen a' | 114-114 |
| **Conclusion** | 66 | 1 | 0.266 | 0.266 | -0.107 | 'A $3.30 world model and 69 policy rollouts were enough to sort 20 published uses' | 118-118 |
| (figure and table captions) | 154 | 1 | 0.173 | 0.173 | +0.000 | 'Table 1: The register: every use of our world model re-tested here (with the fro' | 33-33 |

Paper mean 0.180; 100 % of words in chunks above the human-reference maximum (0.106).

## built PDF

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| **(front matter)** (short, noisy) | 30 | 1 | 0.134 | 0.134 | +0.000 | 'A small JEPA world model on a low-cost arm: the encoder reads the outcome, the p' | 3-8 |
| **Abstract** | 1115 | 2 | 0.141 | 0.179 | +0.018 | 'register with a pass mark, a dataset, a result and a verdict, and where we manag' | 49-75 |
| **3 The register** | 1486 | 3 | 0.136 | 0.240 |  | 'A $3.30 world model and 69 policy rollouts were enough to sort 20 published uses' | 680-686 |

Paper mean 0.138; 46 % of words in chunks above the human-reference maximum (0.106).
