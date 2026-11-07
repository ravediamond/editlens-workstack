# Paper AI map: paper-vla-edge-inference

EditLens `pangram/editlens_Llama-3.2-3B`; raw score in [0, 1] (0 = human, 1 = AI). No threshold is published, so there are no labels; read the scores next to the reference below. A map for the owner to rewrite by hand.

Human reference (3 papers from before 2022-11, same extraction): paper means 0.053, 0.055, 0.095; median 0.055; chunk scores 0.026 to 0.106 (max 0.106). AI reference: n/a (see notes).

## rendered source (numbers filled)

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| **Abstract** | 143 | 1 | 0.267 | 0.267 | -0.044 | 'Training-free tricks that make flow-matching vision-language-action policies fas' | 9-16 |
| **1 Introduction** | 156 | 1 | 0.303 | 0.303 | +0.025 | 'Papers that speed up or smooth action chunking report their latencies on desktop' | 20-22 |
| 2 Where the time goes | 114 | 1 | 0.232 | 0.232 | -0.065 | 'Vision dominates the chunk. At ten Euler steps and full power (MAXN_SUPER), a ch' | 32-35 |
| 3 Seven tricks, one checkpoint | 420 | 1 | 0.220 | 0.220 | -0.186 | 'Cutting the Euler steps from ten to two [arXiv:2610.32102] saves 41 ms per chunk' | 57-61 |
| 4 What transfers to the board | 132 | 1 | 0.202 | 0.202 |  | 'On this board, the prefix overwrite and the primitive projection with seam condi' | 90-96 |
| 5 Related work | 136 | 1 | 0.183 | 0.183 | -0.006 | 'Other chunking tricks are also reported on desktop-class GPUs, and we did not re' | 100-107 |
| 6 Limitations | 178 | 1 | 0.263 | 0.263 | -0.003 | 'Everything runs one policy, SmolVLA at 450M. π0-class models do not fit on the O' | 111-119 |
| Appendix: from plain name to gate (short, noisy) | 18 | 1 | 0.172 | 0.172 | +0.000 | 'Every number in this paper is recomputable from the repository; this table maps ' | 123-123 |
| **(figure and table captions)** | 119 | 1 | 0.284 | 0.284 | +0.000 | "Fig. 1 — where a SmolVLA chunk's time goes on the Orin NX (vla.cpp, ten Euler st" | 40-86 |

Paper mean 0.240; 100 % of words in chunks above the human-reference maximum (0.106).

## built PDF

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| **Abstract** | 234 | 1 | 0.129 | 0.129 | -0.115 | 'Training-free tricks that make flow-matching visionlanguage-action policies fast' | 12-23 |
| **1 Introduction** | 367 | 1 | 0.189 | 0.189 | -0.078 | 'Two power modes appear because each gate’s protocol froze the mode it ran in. Th' | 65-96 |
| **2 Euler steps** | 587 | 1 | 0.164 | 0.164 | -0.013 | 'Figure 2: Median boundary-jump cut against naive asynchronous execution (254 bou' | 149-172 |
| 4 What transfers to the board | 220 | 1 | 0.086 | 0.086 |  | 'sequential-sampling costs. In particular, a batched samOn this board, the prefix' | 212-220 |
| Appendix: from plain name to gate | 340 | 1 | 0.114 | 0.114 |  | '[2] NVIDIA Jetson Orin NX 16 GB. https:// Every number in this paper is recomput' | 238-278 |

Paper mean 0.145; 87 % of words in chunks above the human-reference maximum (0.106).
