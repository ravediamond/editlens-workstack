# Paper AI map: paper-register-reproducibility

EditLens `pangram/editlens_Llama-3.2-3B`; raw score in [0, 1] (0 = human, 1 = AI). No threshold is published, so there are no labels; read the scores next to the reference below. A map for the owner to rewrite by hand.

Human reference (3 papers from before 2022-11, same extraction): paper means 0.053, 0.055, 0.095; median 0.055; chunk scores 0.026 to 0.106 (max 0.106). AI reference: n/a (see notes).

## rendered source (numbers filled)

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| **Abstract** | 158 | 1 | 0.377 | 0.377 | +0.017 | 'Re-testing a robot-learning paper does not need a lab. For $45.10 of compute on ' | 7-7 |
| 1. The register | 288 | 1 | 0.322 | 0.322 | +0.033 | 'Before a learned model gets credit, the cheapest signal it must beat runs on the' | 17-17 |
| 2. Auditing our own pre-registration | 546 | 1 | 0.154 | 0.154 |  | 'A first pass by text search read the log very differently: 36 bar-first and 31 s' | 25-25 |
| 3. Results | 90 | 1 | 0.136 | 0.136 | -0.078 | 'Counted by paper, 4 of the 22 hold and 13 fail (Table 1); 3 are not proven, 1 wa' | 60-60 |
| **4. Three failure classes** | 232 | 1 | 0.341 | 0.341 | +0.011 | 'Class B covers zero-shot judges, models used without training on this rig to jud' | 66-66 |
| **5. Limitations** | 179 | 1 | 0.384 | 0.384 | -0.009 | 'With a single operator, the author, running the rig and labelling outcomes at re' | 72-72 |
| 6. Related work | 163 | 1 | 0.275 | 0.275 | +0.026 | 'Work on the same arm evaluates policies. A standardized real-world benchmark rep' | 76-76 |
| 7. Conclusion | 90 | 1 | 0.322 | 0.322 | +0.013 | 'A €1,350 rig and $45.10 of compute were enough to re-test these claims and publi' | 80-80 |
| (figure and table captions) (short, noisy) | 31 | 1 | 0.057 | 0.057 | +0.000 | 'Table 1: The register, one row per paper, generated from the register file (inte' | 33-33 |

Paper mean 0.266; 98 % of words in chunks above the human-reference maximum (0.106).

## built PDF

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| **(front matter)** | 55 | 1 | 0.262 | 0.262 | +0.022 | 'What survives when a paper leaves the lab: re-testing 22 robot-learning papers o' | 3-11 |
| **Abstract** | 317 | 1 | 0.164 | 0.164 | -0.024 | 'Before a learned model gets credit, the cheapest signal it must beat runs on the' | 12-35 |
| 1 The register | 1124 | 3 | 0.143 | 0.179 |  | 'With a single operator, the author, running the rig and labelling outcomes at re' | 121-135 |
| **4 Three failure classes** | 1515 | 4 | 0.166 | 0.236 | +0.052 | 'Chunk length chosen from the entropy of N sampled chunks follows the task’s phas' | 384-401 |

Paper mean 0.159; 69 % of words in chunks above the human-reference maximum (0.106).
