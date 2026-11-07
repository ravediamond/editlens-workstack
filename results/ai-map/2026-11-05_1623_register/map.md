# Paper AI map: paper-register-reproducibility

EditLens `pangram/editlens_Llama-3.2-3B`; raw score in [0, 1] (0 = human, 1 = AI). No threshold is published, so there are no labels; read the scores next to the reference below. A map for the owner to rewrite by hand.

Human reference (3 papers from before 2022-11, same extraction): paper means 0.053, 0.055, 0.095; median 0.055; chunk scores 0.026 to 0.106 (max 0.106). AI reference: n/a (see notes).

## rendered source (numbers filled)

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| **Abstract** | 140 | 1 | 0.296 | 0.296 | -0.012 | 'We re-tested the main claims of new robot-learning papers on an SO-101 arm with ' | 7-7 |
| 1. The register | 277 | 1 | 0.127 | 0.127 | +0.000 | 'Most of the 22 papers in this study were shown on setups far from ours. 9 were s' | 11-11 |
| 2. Auditing our own pre-registration | 427 | 1 | 0.130 | 0.130 | -0.001 | 'The cold reruns start from a fresh clone with no credentials. 6 gates reran and ' | 75-75 |
| 3. Results | 45 | 1 | 0.162 | 0.162 | +0.000 | 'Table 3 counts the verdicts by paper and by claim row. On claims taken from pape' | 79-79 |
| 4. Three failure classes | 195 | 1 | 0.270 | 0.270 | +0.000 | 'In other entries a model judged outcomes without training on this rig. A learned' | 96-96 |
| **5. Limitations** | 159 | 1 | 0.274 | 0.274 | +0.000 | 'One operator, the author, ran the rig and labelled the outcomes. Labels were giv' | 102-102 |
| **6. Related work** | 157 | 1 | 0.291 | 0.291 | +0.000 | 'Two works use the same arm to evaluate policies. A standardized real-world bench' | 106-106 |
| 7. Conclusion | 78 | 1 | 0.247 | 0.247 | +0.000 | 'We re-tested 37 paper claims, and 12 held. The rig cost €1,350 and the compute $' | 110-110 |
| (figure and table captions) | 110 | 1 | 0.126 | 0.126 | +0.000 | 'Table 4: The register, one row per paper, generated from the register file (inte' | 116-116 |

Paper mean 0.198; 100 % of words in chunks above the human-reference maximum (0.106).

## built PDF

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| **(front matter)** | 62 | 1 | 0.171 | 0.171 |  | 'What survives when a paper leaves the lab: re-testing 22 robot-learning papers o' | 3-12 |
| Abstract | 279 | 1 | 0.126 | 0.126 | +0.012 | 'learned model has to beat, on the same rows. For a predictor this is copy-last. ' | 13-33 |
| **1 The register** | 586 | 1 | 0.152 | 0.152 |  | 'The adaptive chunking entry of §1 misses the real-time budget on the edge GPU. T' | 207-213 |
| **0.938. Judges of success, failure or progress that lose to** | 372 | 1 | 0.250 | 0.250 |  | 'The cold reruns start from a fresh clone with no credentials. 6 gates reran and ' | 230-239 |
| 3 Results | 629 | 2 | 0.078 | 0.085 | +0.017 | 'Two works use the same arm to evaluate policies. A standardized real-world bench' | 264-279 |
| Appendix: the register | 1136 | 3 | 0.142 | 0.430 | +0.000 | 'Chunk length chosen from the entropy of N sampled chunks follows the task’s phas' | 591-608 |

Paper mean 0.143; 79 % of words in chunks above the human-reference maximum (0.106).
