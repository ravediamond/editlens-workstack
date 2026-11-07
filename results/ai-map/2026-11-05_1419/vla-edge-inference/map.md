# Paper AI map: paper-vla-edge-inference

EditLens `pangram/editlens_Llama-3.2-3B`; raw score in [0, 1] (0 = human, 1 = AI). No threshold is published, so there are no labels; read the scores next to the reference below. A map for the owner to rewrite by hand.

Human reference (3 papers from before 2022-11, same extraction): paper means 0.053, 0.055, 0.095; median 0.055; chunk scores 0.026 to 0.106 (max 0.106). AI reference: n/a (see notes).

## rendered source (numbers filled)

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| Abstract | 147 | 1 | 0.242 | 0.242 | -0.097 | 'We re-measured seven training-free methods for action chunking in flow-matching ' | 9-16 |
| 1 Introduction | 196 | 1 | 0.233 | 0.233 | -0.023 | 'Several training-free chunking tricks for flow-matching VLAs were published this' | 20-23 |
| **2 Where the time goes** | 114 | 1 | 0.283 | 0.283 | +0.065 | "Two power modes appear in this paper. Each gate's protocol froze the mode it ran" | 39-40 |
| 3 Seven tricks, one checkpoint | 418 | 1 | 0.185 | 0.185 | -0.037 | 'Cutting the Euler steps from ten to two [arXiv:2610.32102] saves 41 ms per chunk' | 59-64 |
| **4 What transfers to the board** | 113 | 1 | 0.298 | 0.298 | +0.091 | 'The prefix overwrite and the primitive projection with seam conditioning act on ' | 92-97 |
| 5 Related work | 129 | 1 | 0.201 | 0.201 | +0.019 | 'Other chunking tricks are also reported on desktop-class GPUs. We did not re-mea' | 101-107 |
| 6 Limitations | 157 | 1 | 0.148 | 0.148 | -0.043 | 'The sampling result depends on the engine. vla.cpp samples sequentially. We cont' | 111-118 |
| Appendix: from plain name to gate (short, noisy) | 18 | 1 | 0.172 | 0.172 | +0.000 | 'Every number in this paper is recomputable from the repository; this table maps ' | 122-122 |
| **(figure and table captions)** | 113 | 1 | 0.300 | 0.300 | +0.007 | "Fig. 1 — where one SmolVLA chunk's time goes on the Orin NX (vla.cpp, ten Euler " | 42-88 |

Paper mean 0.221; 100 % of words in chunks above the human-reference maximum (0.106).

## built PDF

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| **Abstract** | 232 | 1 | 0.136 | 0.136 | -0.025 | 'We re-measured seven training-free methods for action chunking in flow-matching ' | 12-26 |
| 1 Introduction | 407 | 1 | 0.090 | 0.090 |  | 'denoising loop works on at most a quarter of the chunk. Two power modes appear i' | 66-96 |
| 2 Euler steps | 609 | 1 | 0.080 | 0.080 | +0.004 | 'Other chunking tricks are also reported on desktop-class GPUs. We did not re-mea' | 191-201 |
| **4 What transfers to the board** | 148 | 1 | 0.134 | 0.134 |  | 'smoothing and for the overwrite in the robot client have The prefix overwrite an' | 213-218 |
| **Appendix: from plain name to gate** | 301 | 1 | 0.119 | 0.119 | -0.012 | '[4] vla.cpp. https://github.com/VinRobotics/vla. cpp. C++ inference engine for V' | 250-283 |

Paper mean 0.102; 40 % of words in chunks above the human-reference maximum (0.106).
