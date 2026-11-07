# Paper AI map: paper-jepa-world-model

EditLens `pangram/editlens_Llama-3.2-3B`; raw score in [0, 1] (0 = human, 1 = AI). No threshold is published, so there are no labels; read the scores next to the reference below. A map for the owner to rewrite by hand.

Human reference (3 papers from before 2022-11, same extraction): paper means 0.053, 0.055, 0.095; median 0.055; chunk scores 0.026 to 0.106 (max 0.106). AI reference: n/a (see notes).

## rendered source (numbers filled)

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| Abstract | 160 | 1 | 0.198 | 0.198 |  | 'We trained a small JEPA world model in the LeWorldModel recipe on teleoperated d' | 7-7 |
| Introduction | 482 | 1 | 0.257 | 0.257 |  | 'On the 69 rollouts, and in exploratory probes only, the result splits along the ' | 15-15 |
| Setup | 225 | 1 | 0.235 | 0.235 |  | '**Load audit.** One early use loaded the checkpoint with X and so ran a random e' | 25-25 |
| **The register** | 237 | 1 | 0.341 | 0.341 |  | '*Encoder reads.* The outcome readout at rest passes, with a retrospective bar; t' | 56-56 |
| **What the encoder knows** | 172 | 1 | 0.309 | 0.309 |  | 'In this exploratory comparison on the 69 rollouts, our world model is level with' | 74-74 |
| Where the predictor fails | 367 | 1 | 0.304 | 0.304 |  | '*Objection: the anticipation step of the outcome-readout gate is a predictive pa' | 92-92 |
| Related work | 178 | 1 | 0.236 | 0.236 |  | 'LeWorldModel [1] trains the JEPA recipe we use end to end from pixels and plans ' | 96-96 |
| Limitations | 124 | 1 | 0.299 | 0.299 |  | 'The controls are exploratory: 69 rollouts, operator labels, probes chosen after ' | 100-100 |
| **Conclusion** | 55 | 1 | 0.342 | 0.342 |  | 'On a small teleoperation dataset, a JEPA world model learns an encoder that read' | 104-104 |
| (figure and table captions) | 218 | 1 | 0.097 | 0.097 |  | 'Table 1: The register: every pre-registered use of our world model (and the froz' | 31-31 |

Paper mean 0.259; 90 % of words in chunks above the human-reference maximum (0.106).

## built PDF

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| Abstract | 162 | 1 | 0.184 | 0.184 | +0.000 | 'We trained a small JEPA world model in the LeWorldModel recipe on teleoperated d' | 10-21 |
| 1 Introduction | 505 | 1 | 0.125 | 0.125 | +0.000 | 'verdict. Pre-registration here means only that: the bar and the decision rule ar' | 45-78 |
| 2 Setup | 230 | 1 | 0.030 | 0.030 | +0.000 | 'Robot and data. The robot is one SO-101 arm [4] driven through LeRobot [5], with' | 80-90 |
| **3 The register** | 237 | 1 | 0.299 | 0.299 | +0.000 | 'Table 1 lists the 20 uses with what each takes from the model: the encoder alone' | 112-128 |
| 4 What the encoder knows | 211 | 1 | 0.164 | 0.164 | +0.000 | 'In this exploratory comparison on the 69 rollouts, our world model is level with' | 130-137 |
| 5 Where the predictor fails | 502 | 1 | 0.177 | 0.177 | +0.000 | 'The cleanest contrast is the grasp probe, which ContactGuard [9] motivates: same' | 187-208 |
| **6 Related work** | 177 | 1 | 0.224 | 0.224 | +0.000 | 'LeWorldModel [1] trains the JEPA recipe we use end to end from pixels and plans ' | 661-676 |
| **7 Limitations** | 123 | 1 | 0.273 | 0.273 | +0.000 | 'The controls are exploratory: 69 rollouts, operator labels, probes chosen after ' | 678-686 |
| 8 Conclusion | 478 | 2 | 0.095 | 0.146 | +0.000 | '[10] Wancong Zhang, Basile Terver, Michael Rabbat, Yann LeCun, and Randall Bales' | 734-758 |

Paper mean 0.157; 80 % of words in chunks above the human-reference maximum (0.106).
