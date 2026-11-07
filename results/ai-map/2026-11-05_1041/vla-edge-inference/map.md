# Paper AI map: paper-vla-edge-inference

EditLens `pangram/editlens_Llama-3.2-3B`; raw score in [0, 1] (0 = human, 1 = AI). No threshold is published, so there are no labels; read the scores next to the reference below. A map for the owner to rewrite by hand.

Human reference (3 papers from before 2022-11, same extraction): paper means 0.053, 0.055, 0.095; median 0.055; chunk scores 0.026 to 0.106 (max 0.106). AI reference: n/a (see notes).

## rendered source (numbers filled)

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| **Abstract** | 160 | 1 | 0.281 | 0.281 | +0.014 | "On an edge GPU, most of a VLA's action chunk goes to vision, so a trick that spe" | 9-16 |
| 1 Introduction | 215 | 1 | 0.265 | 0.265 | -0.038 | 'With several training-free chunking tricks published this year for flow-matching' | 20-24 |
| 2 Where the time goes | 110 | 1 | 0.219 | 0.219 | -0.013 | 'Follow one chunk. At ten Euler steps and full power (MAXN_SUPER) it costs 237.5 ' | 35-38 |
| 3 Seven tricks, one checkpoint | 434 | 1 | 0.234 | 0.234 | +0.014 | 'Cutting the Euler steps from ten to two [arXiv:2610.32102] saves 41 ms per chunk' | 60-65 |
| 4 What transfers to the board | 129 | 1 | 0.198 | 0.198 | -0.005 | 'On this board, the prefix overwrite and the primitive projection with seam condi' | 94-100 |
| 5 Related work | 131 | 1 | 0.182 | 0.182 | -0.001 | 'Other chunking tricks are also reported on desktop-class GPUs, and we did not re' | 104-110 |
| **6 Limitations** | 193 | 1 | 0.309 | 0.309 | +0.046 | 'The finding most likely to move is that sampling does not transfer, because it d' | 114-123 |
| Appendix: from plain name to gate (short, noisy) | 18 | 1 | 0.172 | 0.172 | +0.000 | 'Every number in this paper is recomputable from the repository; this table maps ' | 127-127 |
| **(figure and table captions)** | 109 | 1 | 0.293 | 0.293 | +0.009 | "Fig. 1 — where one SmolVLA chunk's time goes on the Orin NX (vla.cpp, ten Euler " | 43-90 |

Paper mean 0.248; 100 % of words in chunks above the human-reference maximum (0.106).

## built PDF

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| **Abstract** | 447 | 1 | 0.099 | 0.099 | -0.030 | 'Figure 1: Where one SmolVLA chunk’s time goes on the Orin NX (vla.cpp, ten Euler' | 55-61 |
| 3 Seven tricks, one checkpoint | 160 | 1 | 0.057 | 0.057 |  | 'board. Ours is an SO-101 arm [3, 5] with a Jetson Orin NX All offline effects us' | 80-94 |
| **2 Euler steps** | 853 | 2 | 0.223 | 0.276 | +0.059 | 'in vla.cpp, where it adds 0.4 ms per chunk. Movementprimitive chunking [13] pass' | 151-178 |
| **Appendix: from plain name to gate** | 280 | 1 | 0.115 | 0.115 | +0.001 | '[2] NVIDIA Jetson Orin NX 16 GB. https:// Every number in this paper is recomput' | 263-295 |

Paper mean 0.159; 65 % of words in chunks above the human-reference maximum (0.106).
