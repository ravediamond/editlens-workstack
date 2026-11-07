# Paper AI map: paper-register-reproducibility

EditLens `pangram/editlens_Llama-3.2-3B`; raw score in [0, 1] (0 = human, 1 = AI). No threshold is published, so there are no labels; read the scores next to the reference below. A map for the owner to rewrite by hand.

Human reference (3 papers from before 2022-11, same extraction): paper means 0.053, 0.055, 0.095; median 0.055; chunk scores 0.026 to 0.106 (max 0.106). AI reference: n/a (see notes).

## rendered source (numbers filled)

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| Abstract | 185 | 1 | 0.301 | 0.301 |  | 'Robot-learning papers are mostly shown in simulation, on costly arms or on data-' | 7-16 |
| **1. The register** | 303 | 1 | 0.422 | 0.422 |  | 'A claim shown on a Franka-class arm, in simulation or on a data-centre GPU does ' | 20-31 |
| 2. Method, and an audit of our own pre-registration | 493 | 1 | 0.365 | 0.365 |  | '**One statistic.** The early gates mixed point estimates and other intervals, so' | 59-66 |
| 3. Results | 83 | 1 | 0.143 | 0.143 |  | 'Table 1 lists the register. Of the 22 papers, 4 reproduce, 13 fail, 3 are not pr' | 104-109 |
| **4. Three failure classes** | 210 | 1 | 0.371 | 0.371 |  | 'We propose three classes for the 20 failed claim rows. **A, edge latency:** the ' | 113-123 |
| **5. Limitations** | 135 | 1 | 0.405 | 0.405 |  | 'One rig, one arm, one operator. A failure here is a rig finding, not a refutatio' | 127-134 |
| 6. Related work | 174 | 1 | 0.299 | 0.299 |  | 'A standardized real-world benchmark on the same arm reports a failure and recove' | 138-147 |
| 7. Conclusion | 85 | 1 | 0.341 | 0.341 |  | 'On a €1,350 rig, 12 of 37 tested paper claims reproduce under bars fixed for thi' | 151-155 |
| (figure and table captions) (short, noisy) | 35 | 1 | 0.138 | 0.138 |  | 'Table 1: The register: one row per paper, generated from the register file (clai' | 77-77 |

Paper mean 0.349; 100 % of words in chunks above the human-reference maximum (0.106).

## built PDF

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| **Abstract** | 395 | 1 | 0.311 | 0.311 | +0.000 | 'the result; §2 audits how far that holds. The papers were picked for relevance t' | 12-25 |
| 1 The register | 669 | 2 | 0.154 | 0.160 | +0.000 | '11-01 (the reward-model progress test) is same-commit by text search, but its pr' | 69-93 |
| **5 Limitations** | 135 | 1 | 0.399 | 0.399 | +0.000 | 'One rig, one arm, one operator. A failure here is a rig finding, not a refutatio' | 101-112 |
| **6 Related work** (short, noisy) | 28 | 1 | 0.194 | 0.194 | +0.000 | 'A standardized real-world benchmark on the same arm reports a failure and recove' | 115-117 |
| 3 Results | 181 | 1 | 0.060 | 0.060 | +0.000 | 'scale [14]. The vla-eval tool decouples VLA inference from 14 simulation benchma' | 118-129 |
| 4 Three failure classes | 1434 | 3 | 0.169 | 0.206 | +0.000 | 'Chunk length chosen from the entropy of N sampled chunks follows the task’s phas' | 378-395 |

Paper mean 0.189; 92 % of words in chunks above the human-reference maximum (0.106).
