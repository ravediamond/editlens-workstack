# Paper AI map: paper-register-reproducibility

EditLens `pangram/editlens_Llama-3.2-3B`; raw score in [0, 1] (0 = human, 1 = AI). No threshold is published, so there are no labels; read the scores next to the reference below. A map for the owner to rewrite by hand.

Human reference (3 papers from before 2022-11, same extraction): paper means 0.053, 0.055, 0.095; median 0.055; chunk scores 0.026 to 0.106 (max 0.106). AI reference: n/a (see notes).

## rendered source (numbers filled)

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| Abstract | 188 | 1 | 0.272 | 0.272 | -0.029 | 'Most robot-learning results are shown in simulation, on costly arms or on data-c' | 7-7 |
| **1. The register** | 239 | 1 | 0.297 | 0.297 | -0.125 | 'The register has one entry per paper. It records the claim as the paper states i' | 13-13 |
| 2. Method, and an audit of our own pre-registration | 595 | 1 | 0.245 | 0.245 | -0.120 | 'The early gates mixed point estimates with assorted intervals. We recomputed 10 ' | 23-23 |
| 3. Results | 98 | 1 | 0.198 | 0.198 | +0.055 | 'Table 1 lists the register. Counted by paper, 4 of the 22 reproduce and 13 fail,' | 56-56 |
| 4. Three failure classes | 223 | 1 | 0.283 | 0.283 | -0.088 | 'We propose three classes for the 20 failed claim rows, named after what beat the' | 60-60 |
| **5. Limitations** | 137 | 1 | 0.447 | 0.447 | +0.042 | 'Everything here comes from one rig, one arm and one operator, so a failure is a ' | 66-66 |
| 6. Related work | 169 | 1 | 0.272 | 0.272 | -0.027 | 'Work on the same arm evaluates policies. A standardized real-world benchmark rep' | 70-70 |
| **7. Conclusion** | 77 | 1 | 0.386 | 0.386 | +0.046 | 'On a €1,350 rig, 12 of 37 tested paper claims reproduce under bars fixed for thi' | 74-74 |
| (figure and table captions) (short, noisy) | 35 | 1 | 0.138 | 0.138 | +0.000 | 'Table 1: The register: one row per paper, generated from the register file (clai' | 29-29 |

Paper mean 0.280; 100 % of words in chunks above the human-reference maximum (0.106).

## built PDF

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| **(front matter)** | 63 | 1 | 0.254 | 0.254 |  | 'What survives when a paper leaves the lab: re-testing 22 robot-learning papers o' | 3-12 |
| Abstract | 356 | 1 | 0.028 | 0.028 | -0.283 | 'record §2 audits. We picked the papers for relevance to the stack this rig Most ' | 13-36 |
| **1 The register** | 1143 | 2 | 0.170 | 0.225 | +0.016 | 'Everything here comes from one rig, one arm and one operator, so a failure is a ' | 99-110 |
| **4 Three failure classes** | 1386 | 4 | 0.153 | 0.250 | -0.016 | 'Chunk length chosen from the entropy of N sampled chunks follows the task’s phas' | 376-393 |

Paper mean 0.147; 65 % of words in chunks above the human-reference maximum (0.106).
