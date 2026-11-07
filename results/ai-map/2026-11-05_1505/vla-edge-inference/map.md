# Paper AI map: paper-vla-edge-inference

EditLens `pangram/editlens_Llama-3.2-3B`; raw score in [0, 1] (0 = human, 1 = AI). No threshold is published, so there are no labels; read the scores next to the reference below. A map for the owner to rewrite by hand.

Human reference (3 papers from before 2022-11, same extraction): paper means 0.053, 0.055, 0.095; median 0.055; chunk scores 0.026 to 0.106 (max 0.106). AI reference: n/a (see notes).

## rendered source (numbers filled)

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| Abstract | 144 | 1 | 0.267 | 0.267 | +0.026 | 'We re-measured seven training-free methods for action chunking in flow-matching ' | 9-16 |
| 1 Introduction | 194 | 1 | 0.218 | 0.218 | -0.015 | 'Several training-free chunking tricks for flow-matching VLAs were published this' | 20-23 |
| **2 Where the time goes** | 114 | 1 | 0.326 | 0.326 | +0.043 | "Two power modes appear in this paper because each gate's protocol froze the mode" | 39-40 |
| 3 Seven tricks, one checkpoint | 424 | 1 | 0.196 | 0.196 | +0.011 | 'Two tricks act on the seam between chunks, and both pass. The first overwrites t' | 49-54 |
| **4 What transfers to the board** | 116 | 1 | 0.346 | 0.346 | +0.048 | 'The prefix overwrite and the primitive projection with seam conditioning act on ' | 93-98 |
| 5 Related work | 131 | 1 | 0.135 | 0.135 | -0.066 | 'Other chunking tricks are also reported on desktop-class GPUs, and we did not re' | 102-108 |
| 6 Limitations | 158 | 1 | 0.174 | 0.174 | +0.025 | 'The sampling result depends on the engine. vla.cpp samples sequentially, and we ' | 112-119 |
| Appendix: from plain name to gate (short, noisy) | 18 | 1 | 0.172 | 0.172 | +0.000 | 'Every number in this paper is recomputable from the repository; this table maps ' | 123-123 |
| **(figure and table captions)** | 113 | 1 | 0.300 | 0.300 | +0.000 | "Fig. 1 — where one SmolVLA chunk's time goes on the Orin NX (vla.cpp, ten Euler " | 42-89 |

Paper mean 0.229; 100 % of words in chunks above the human-reference maximum (0.106).

## built PDF

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| **Abstract** | 229 | 1 | 0.159 | 0.159 | +0.022 | 'We re-measured seven training-free methods for action chunking in flow-matching ' | 12-26 |
| 1 Introduction | 405 | 1 | 0.032 | 0.032 | -0.058 | 'denoising loop works on at most a quarter of the chunk. Two power modes appear i' | 66-94 |
| **2 Euler steps** | 620 | 1 | 0.170 | 0.170 | +0.089 | 'The sampling result depends on the engine. vla.cpp samples sequentially, and we ' | 204-212 |
| 4 What transfers to the board | 151 | 1 | 0.113 | 0.113 | -0.021 | 'and for the overwrite in the robot client have not run. We The prefix overwrite ' | 213-218 |
| **Appendix: from plain name to gate** | 301 | 1 | 0.120 | 0.120 | +0.001 | '[4] vla.cpp. https://github.com/VinRobotics/vla. cpp. C++ inference engine for V' | 250-283 |

Paper mean 0.122; 76 % of words in chunks above the human-reference maximum (0.106).
