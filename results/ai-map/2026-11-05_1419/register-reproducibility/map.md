# Paper AI map: paper-register-reproducibility

EditLens `pangram/editlens_Llama-3.2-3B`; raw score in [0, 1] (0 = human, 1 = AI). No threshold is published, so there are no labels; read the scores next to the reference below. A map for the owner to rewrite by hand.

Human reference (3 papers from before 2022-11, same extraction): paper means 0.053, 0.055, 0.095; median 0.055; chunk scores 0.026 to 0.106 (max 0.106). AI reference: n/a (see notes).

## rendered source (numbers filled)

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| **Abstract** | 152 | 1 | 0.333 | 0.333 | -0.044 | 'We re-tested the central claims of recent robot-learning papers on an SO-101 arm' | 7-7 |
| 1. The register | 308 | 1 | 0.270 | 0.270 | -0.052 | 'Most of the 22 papers in this study were shown on setups far from ours. 9 were s' | 11-11 |
| 2. Auditing our own pre-registration | 437 | 1 | 0.126 | 0.126 | -0.028 | 'Our first pass used text search and found 31 same-commit gates. The cause was ba' | 37-37 |
| 3. Results | 50 | 1 | 0.271 | 0.271 | +0.136 | 'Table 3 counts the verdicts by paper and by claim row. The appendix lists every ' | 53-53 |
| **4. Three failure classes** | 204 | 1 | 0.324 | 0.324 | -0.017 | 'The adaptive chunking entry of §1 misses the real-time budget on the edge GPU. O' | 68-68 |
| 5. Limitations | 159 | 1 | 0.274 | 0.274 | -0.110 | 'One operator, the author, ran the rig and labelled the outcomes. Labels were giv' | 76-76 |
| **6. Related work** | 157 | 1 | 0.291 | 0.291 | +0.016 | 'Two works use the same arm to evaluate policies. A standardized real-world bench' | 80-80 |
| 7. Conclusion | 78 | 1 | 0.247 | 0.247 | -0.075 | 'We re-tested 37 paper claims, and 12 held. The rig cost €1,350 and the compute $' | 84-84 |
| (figure and table captions) | 90 | 1 | 0.089 | 0.089 | +0.032 | 'Table 1: Commit-order class of each gate. The audited column is the one the pape' | 25-90 |

Paper mean 0.236; 94 % of words in chunks above the human-reference maximum (0.106).

## built PDF

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| Abstract | 1010 | 2 | 0.139 | 0.198 | -0.026 | 'Most of the 22 papers in this study were shown on setups far from ours. 9 were s' | 34-48 |
| **0.938. Judges of success, failure or progress that lose to** | 263 | 1 | 0.275 | 0.275 |  | 'a trivial signal like this form class B. Class C is about learned latents. A wor' | 212-223 |
| **3 Results** | 101 | 1 | 0.204 | 0.204 |  | 'in its own setting. The papers were chosen for one stack, Table 3 counts the ver' | 240-249 |
| 4 Three failure classes | 698 | 2 | 0.133 | 0.237 | -0.033 | 'of SO-101 cells evaluates policies at scale [14]. The vlaThe adaptive chunking e' | 250-256 |
| **Appendix: the register** | 1116 | 3 | 0.145 | 0.430 |  | 'Chunk length chosen from the entropy of N sampled chunks follows the task’s phas' | 569-586 |

Paper mean 0.153; 85 % of words in chunks above the human-reference maximum (0.106).
