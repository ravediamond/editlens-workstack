# Paper AI map: paper-register-reproducibility

EditLens `pangram/editlens_Llama-3.2-3B`; raw score in [0, 1] (0 = human, 1 = AI). No threshold is published, so there are no labels; read the scores next to the reference below. A map for the owner to rewrite by hand.

Human reference (3 papers from before 2022-11, same extraction): paper means 0.053, 0.055, 0.095; median 0.055; chunk scores 0.026 to 0.106 (max 0.106). AI reference: n/a (see notes).

## rendered source (numbers filled)

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| **Abstract** | 154 | 1 | 0.360 | 0.360 | +0.088 | 'Most robot-learning claims are shown in simulation, on costly arms or on data-ce' | 7-7 |
| 1. The register | 330 | 1 | 0.289 | 0.289 | -0.008 | 'Two rules govern each entry. Before a learned model gets credit, the trivial sig' | 17-17 |
| 2. Method, and an audit of our own pre-registration | 581 | 1 | 0.219 | 0.219 | -0.027 | 'Did each bar come before its result? Each gate of the experiment log has a bar a' | 23-23 |
| 3. Results | 95 | 1 | 0.213 | 0.213 | +0.015 | 'Counted by paper, 4 of the 22 reproduce and 13 fail (Table 1), while 3 are not p' | 60-60 |
| **4. Three failure classes** | 221 | 1 | 0.330 | 0.330 | +0.047 | 'What beat the method? We propose three classes for the 20 failed claim rows, nam' | 64-64 |
| **5. Limitations** | 166 | 1 | 0.393 | 0.393 | -0.054 | 'The weakest point is that one person stands behind every verdict. The author ran' | 70-70 |
| 6. Related work | 161 | 1 | 0.249 | 0.249 | -0.023 | 'Work on the same arm evaluates policies. A standardized real-world benchmark rep' | 74-74 |
| 7. Conclusion | 109 | 1 | 0.310 | 0.310 | -0.077 | 'On a €1,350 rig, 12 of 37 tested paper claims reproduce under bars fixed for thi' | 78-78 |
| (figure and table captions) (short, noisy) | 31 | 1 | 0.057 | 0.057 | -0.081 | 'Table 1: The register, one row per paper, generated from the register file (inte' | 33-33 |

Paper mean 0.277; 98 % of words in chunks above the human-reference maximum (0.106).

## built PDF

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| **(front matter)** | 67 | 1 | 0.239 | 0.239 | -0.015 | 'What survives when a paper leaves the lab: re-testing 22 robot-learning papers o' | 3-12 |
| **Abstract** | 1584 | 3 | 0.188 | 0.193 | +0.160 | 'The weakest point is that one person stands behind every verdict. The author ran' | 142-153 |
| **4 Three failure classes** | 1722 | 4 | 0.114 | 0.148 | -0.039 | 'Chunk length chosen from the entropy of N sampled chunks follows the task’s phas' | 410-427 |

Paper mean 0.152; 94 % of words in chunks above the human-reference maximum (0.106).
