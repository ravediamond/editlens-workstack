# Paper AI map: paper-register-reproducibility

EditLens `pangram/editlens_Llama-3.2-3B`; raw score in [0, 1] (0 = human, 1 = AI). No threshold is published, so there are no labels; read the scores next to the reference below. A map for the owner to rewrite by hand.

Human reference (3 papers from before 2022-11, same extraction): paper means 0.053, 0.055, 0.095; median 0.055; chunk scores 0.026 to 0.106 (max 0.106). AI reference: n/a (see notes).

## rendered source (numbers filled)

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| **Abstract** | 146 | 1 | 0.307 | 0.307 | -0.055 | 'We re-tested the main claims of new robot-learning papers on an SO-101 arm with ' | 7-7 |
| 1. The register | 277 | 1 | 0.127 | 0.127 | -0.144 | 'Most of the 22 papers in this study were shown on setups far from ours. 9 were s' | 11-11 |
| 2. Auditing our own pre-registration | 420 | 1 | 0.131 | 0.131 | +0.005 | 'Our first pass used text search and found 31 same-commit gates. The cause was ba' | 37-37 |
| 3. Results | 45 | 1 | 0.162 | 0.162 | -0.109 | 'Table 3 counts the verdicts by paper and by claim row. On claims taken from pape' | 53-53 |
| 4. Three failure classes | 195 | 1 | 0.270 | 0.270 | -0.054 | 'In other entries a model judged outcomes without training on this rig. A learned' | 70-70 |
| **5. Limitations** | 159 | 1 | 0.274 | 0.274 | +0.000 | 'One operator, the author, ran the rig and labelled the outcomes. Labels were giv' | 76-76 |
| **6. Related work** | 157 | 1 | 0.291 | 0.291 | +0.000 | 'Two works use the same arm to evaluate policies. A standardized real-world bench' | 80-80 |
| 7. Conclusion | 78 | 1 | 0.247 | 0.247 | +0.000 | 'We re-tested 37 paper claims, and 12 held. The rig cost €1,350 and the compute $' | 84-84 |
| (figure and table captions) | 110 | 1 | 0.126 | 0.126 | +0.037 | 'Table 4: The register, one row per paper, generated from the register file (inte' | 90-90 |

Paper mean 0.200; 100 % of words in chunks above the human-reference maximum (0.106).

## built PDF

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| **Abstract** | 1374 | 3 | 0.114 | 0.160 | -0.033 | 'We re-tested the main claims of new robot-learning papers on an SO-101 arm with ' | 11-23 |
| **3 Results** | 524 | 2 | 0.061 | 0.073 | -0.143 | 'We re-tested 37 paper claims, and 12 held. The rig cost €1,350 and the compute $' | 272-298 |
| **Appendix: the register** | 1136 | 3 | 0.142 | 0.430 | -0.003 | 'Chunk length chosen from the entropy of N sampled chunks follows the task’s phas' | 570-587 |

Paper mean 0.115; 64 % of words in chunks above the human-reference maximum (0.106).
