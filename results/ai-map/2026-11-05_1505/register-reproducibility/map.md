# Paper AI map: paper-register-reproducibility

EditLens `pangram/editlens_Llama-3.2-3B`; raw score in [0, 1] (0 = human, 1 = AI). No threshold is published, so there are no labels; read the scores next to the reference below. A map for the owner to rewrite by hand.

Human reference (3 papers from before 2022-11, same extraction): paper means 0.053, 0.055, 0.095; median 0.055; chunk scores 0.026 to 0.106 (max 0.106). AI reference: n/a (see notes).

## rendered source (numbers filled)

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| **Abstract** | 158 | 1 | 0.361 | 0.361 | +0.028 | 'We re-tested the central claims of recent robot-learning papers on an SO-101 arm' | 7-7 |
| 1. The register | 294 | 1 | 0.265 | 0.265 | -0.005 | 'Most of the 22 papers in this study were shown on setups far from ours: 9 in sim' | 11-11 |
| 2. Auditing our own pre-registration | 443 | 1 | 0.136 | 0.136 | +0.010 | 'Our first pass used text search and found 31 same-commit gates, mostly because o' | 37-37 |
| 3. Results | 52 | 1 | 0.271 | 0.271 | -0.001 | 'Table 3 counts the verdicts by paper and by claim row, and the appendix lists ev' | 53-53 |
| **4. Three failure classes** | 201 | 1 | 0.333 | 0.333 | +0.009 | 'The adaptive chunking entry of §1 misses the real-time budget on the edge GPU, w' | 68-68 |
| **5. Limitations** | 157 | 1 | 0.397 | 0.397 | +0.123 | 'One operator, the author, ran the rig and labelled the outcomes, at rest and not' | 76-76 |
| 6. Related work | 161 | 1 | 0.273 | 0.273 | -0.018 | 'Two works use the same arm to evaluate policies: a standardized real-world bench' | 80-80 |
| 7. Conclusion | 79 | 1 | 0.283 | 0.283 | +0.036 | 'We re-tested 37 paper claims on a €1,350 rig, and 12 held. The compute cost $45.' | 84-84 |
| (figure and table captions) | 90 | 1 | 0.089 | 0.089 | +0.000 | 'Table 1: Commit-order class of each gate. The audited column is the one the pape' | 25-90 |

Paper mean 0.253; 94 % of words in chunks above the human-reference maximum (0.106).

## built PDF

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| **Abstract** | 1010 | 2 | 0.166 | 0.171 | +0.027 | 'We re-tested the central claims of recent robot-learning papers on an SO-101 arm' | 17-32 |
| **0.938. Judges of success, failure or progress that lose to** | 258 | 1 | 0.354 | 0.354 | +0.079 | 'One operator, the author, ran the rig and labelled the outcomes, at rest and not' | 235-246 |
| **3 Results** | 103 | 1 | 0.272 | 0.272 | +0.068 | 'its own setting. Because the papers were chosen for one Table 3 counts the verdi' | 247-255 |
| 4 Three failure classes | 704 | 2 | 0.131 | 0.153 | -0.002 | 'fleet of SO-101 cells that evaluates policies at scale [14]. The adaptive chunki' | 256-260 |
| Appendix: the register | 1116 | 3 | 0.145 | 0.430 | +0.000 | 'Chunk length chosen from the entropy of N sampled chunks follows the task’s phas' | 572-589 |

Paper mean 0.170; 93 % of words in chunks above the human-reference maximum (0.106).
