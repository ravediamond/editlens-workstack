# Paper AI map: paper-jepa-world-model

EditLens `pangram/editlens_Llama-3.2-3B`; raw score in [0, 1] (0 = human, 1 = AI). No threshold is published, so there are no labels; read the scores next to the reference below. A map for the owner to rewrite by hand.

Human reference (3 papers from before 2022-11, same extraction): paper means 0.053, 0.055, 0.095; median 0.055; chunk scores 0.026 to 0.106 (max 0.106). AI reference: n/a (see notes).

## rendered source (numbers filled)

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| Abstract | 178 | 1 | 0.091 | 0.091 | -0.107 | 'We trained a small JEPA world model in the LeWorldModel recipe on 182 teleoperat' | 7-7 |
| Introduction | 516 | 1 | 0.195 | 0.195 | -0.062 | "Our first reading of the failures was that the latent mostly encodes the arm's p" | 15-15 |
| Setup | 246 | 1 | 0.132 | 0.132 | -0.103 | 'In October, a timing test on the on-board computer loaded our checkpoint with X.' | 25-25 |
| **The register** | 243 | 1 | 0.233 | 0.233 | -0.108 | 'The predictor does predict its own latent. At K = 30 its open-loop error is 0.31' | 58-58 |
| What the encoder knows | 278 | 1 | 0.184 | 0.184 | -0.125 | 'At rest our model is level with the colour judge, whose CI overlaps its own, and' | 76-76 |
| Where the predictor fails | 393 | 1 | 0.177 | 0.177 | -0.127 | 'A reader may object that one pass in the register is predictive. In the anticipa' | 104-104 |
| Related work | 210 | 1 | 0.205 | 0.205 | -0.031 | 'LeWorldModel [1] trains the recipe we use end to end from pixels and plans with ' | 108-108 |
| **Limitations** | 138 | 1 | 0.376 | 0.376 | +0.077 | 'Every statement about the split between encoder and predictor rests on 69 rollou' | 112-112 |
| **Conclusion** | 42 | 1 | 0.349 | 0.349 | +0.007 | 'Before building on the predictor of a world model this size, probe its encoder. ' | 116-116 |
| (figure and table captions) | 218 | 1 | 0.097 | 0.097 | +0.000 | 'Table 1: The register: every pre-registered use of our world model (and the froz' | 31-31 |

Paper mean 0.186; 84 % of words in chunks above the human-reference maximum (0.106).

## built PDF

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| **(front matter)** (short, noisy) | 30 | 1 | 0.134 | 0.134 |  | 'A small JEPA world model on a low-cost arm: the encoder reads the outcome, the p' | 3-8 |
| **Abstract** | 3076 | 6 | 0.091 | 0.140 | -0.093 | 'Each re-test is a row of a register with a bar, a dataset, a result and a verdic' | 50-81 |

Paper mean 0.091; 24 % of words in chunks above the human-reference maximum (0.106).
