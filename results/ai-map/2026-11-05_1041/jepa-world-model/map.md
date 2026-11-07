# Paper AI map: paper-jepa-world-model

EditLens `pangram/editlens_Llama-3.2-3B`; raw score in [0, 1] (0 = human, 1 = AI). No threshold is published, so there are no labels; read the scores next to the reference below. A map for the owner to rewrite by hand.

Human reference (3 papers from before 2022-11, same extraction): paper means 0.053, 0.055, 0.095; median 0.055; chunk scores 0.026 to 0.106 (max 0.106). AI reference: n/a (see notes).

## rendered source (numbers filled)

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| Abstract | 187 | 1 | 0.116 | 0.116 | +0.025 | 'A small JEPA world model trained on a low-cost arm reads how an episode ended, a' | 7-7 |
| Introduction | 534 | 1 | 0.138 | 0.138 | -0.057 | 'One moment runs through the rest of the paper: the grasp anchor, 15 frames befor' | 17-17 |
| Setup | 249 | 1 | 0.125 | 0.125 | -0.007 | 'In October, a timing test on the on-board computer loaded our checkpoint with X.' | 27-27 |
| **The register** | 256 | 1 | 0.233 | 0.233 | -0.001 | 'The predictor does predict its own latent: at K = 30 its open-loop error is 0.31' | 60-60 |
| What the encoder knows | 316 | 1 | 0.129 | 0.129 | -0.055 | 'The anchor column depends on how the five seeds are combined. Averaging the pred' | 80-80 |
| Where the predictor fails | 386 | 1 | 0.172 | 0.172 | -0.006 | 'A reader may object that one pass in the register is predictive. In the anticipa' | 106-106 |
| Related work | 210 | 1 | 0.205 | 0.205 | +0.000 | 'LeWorldModel [1] trains the recipe we use end to end from pixels and plans with ' | 110-110 |
| **Limitations** | 161 | 1 | 0.325 | 0.325 | -0.051 | 'The claim most likely to move is the split between encoder and predictor, becaus' | 114-114 |
| **Conclusion** | 74 | 1 | 0.373 | 0.373 | +0.024 | 'Before building on the predictor of a world model this size, probe its encoder a' | 118-118 |
| (figure and table captions) | 154 | 1 | 0.173 | 0.173 | +0.076 | 'Table 1: The register: every use of our world model re-tested here (with the fro' | 33-33 |

Paper mean 0.175; 100 % of words in chunks above the human-reference maximum (0.106).

## built PDF

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| **(front matter)** (short, noisy) | 30 | 1 | 0.134 | 0.134 | +0.000 | 'A small JEPA world model on a low-cost arm: the encoder reads the outcome, the p' | 3-8 |
| **Abstract** | 2589 | 5 | 0.123 | 0.170 | +0.032 | 'Before building on the predictor of a world model this size, probe its encoder a' | 690-698 |

Paper mean 0.123; 58 % of words in chunks above the human-reference maximum (0.106).
