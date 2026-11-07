# Paper AI map: paper-vla-edge-inference

EditLens `pangram/editlens_Llama-3.2-3B`; raw score in [0, 1] (0 = human, 1 = AI). No threshold is published, so there are no labels; read the scores next to the reference below. A map for the owner to rewrite by hand.

Human reference (3 papers from before 2022-11, same extraction): paper means 0.053, 0.055, 0.095; median 0.055; chunk scores 0.026 to 0.106 (max 0.106). AI reference: n/a (see notes).

## rendered source (numbers filled)

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| **Abstract** | 174 | 1 | 0.339 | 0.339 | +0.058 | "On an edge GPU, most of a VLA's action chunk goes to vision, so a method that sp" | 9-17 |
| **1 Introduction** | 211 | 1 | 0.256 | 0.256 | -0.009 | 'With several training-free chunking tricks published this year for flow-matching' | 21-25 |
| 2 Where the time goes | 110 | 1 | 0.219 | 0.219 | +0.000 | 'Follow one chunk. At ten Euler steps and full power (MAXN_SUPER) it costs 237.5 ' | 36-39 |
| 3 Seven tricks, one checkpoint | 447 | 1 | 0.222 | 0.222 | -0.013 | 'Cutting the Euler steps from ten to two [arXiv:2610.32102] saves 41 ms per chunk' | 62-67 |
| 4 What transfers to the board | 136 | 1 | 0.207 | 0.207 | +0.009 | 'Turn on the prefix overwrite and the primitive projection with seam conditioning' | 96-102 |
| 5 Related work | 131 | 1 | 0.182 | 0.182 | +0.000 | 'Other chunking tricks are also reported on desktop-class GPUs, and we did not re' | 106-112 |
| 6 Limitations | 160 | 1 | 0.191 | 0.191 | -0.118 | 'The sampling result is conditional on the engine. vla.cpp samples sequentially, ' | 116-123 |
| Appendix: from plain name to gate (short, noisy) | 18 | 1 | 0.172 | 0.172 | +0.000 | 'Every number in this paper is recomputable from the repository; this table maps ' | 127-127 |
| **(figure and table captions)** | 109 | 1 | 0.293 | 0.293 | +0.000 | "Fig. 1 — where one SmolVLA chunk's time goes on the Orin NX (vla.cpp, ten Euler " | 44-92 |

Paper mean 0.236; 100 % of words in chunks above the human-reference maximum (0.106).

## built PDF

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| **Abstract** | 448 | 1 | 0.162 | 0.162 | +0.062 | 'Figure 1: Where one SmolVLA chunk’s time goes on the Orin NX (vla.cpp, ten Euler' | 56-62 |
| 3 Seven tricks, one checkpoint | 162 | 1 | 0.068 | 0.068 | +0.011 | 'is how much of each trick is left on that board. Ours is an SO-101 arm [3, 5] wi' | 80-93 |
| **2 Euler steps** | 636 | 1 | 0.076 | 0.076 | -0.147 | 'Turn on the prefix overwrite and the primitive projection with seam conditioning' | 165-196 |
| 6 Limitations | 287 | 1 | 0.067 | 0.067 |  | 'the clearest miss. One 20-sample decision takes 4,751 ms on the Orin against a t' | 197-207 |
| **Appendix: from plain name to gate** | 251 | 1 | 0.131 | 0.131 | +0.016 | '[4] vla.cpp. https://github.com/VinRobotics/vla. cpp. C++ inference engine for V' | 248-274 |

Paper mean 0.103; 39 % of words in chunks above the human-reference maximum (0.106).
