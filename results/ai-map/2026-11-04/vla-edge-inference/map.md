# Paper AI map: paper-vla-edge-inference

EditLens `pangram/editlens_Llama-3.2-3B`; raw score in [0, 1] (0 = human, 1 = AI). No threshold is published, so there are no labels; read the scores next to the reference below. A map for the owner to rewrite by hand.

Human reference (3 papers from before 2022-11, same extraction): paper means 0.053, 0.055, 0.095; median 0.055; chunk scores 0.026 to 0.106 (max 0.106). AI reference: n/a (see notes).

## rendered source (numbers filled)

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| **Abstract** | 153 | 1 | 0.310 | 0.310 |  | 'Training-free tricks promise faster or smoother execution of flow-matching visio' | 9-17 |
| 1 Introduction | 156 | 1 | 0.278 | 0.278 |  | 'Robot-learning papers that speed up or smooth action chunking report their laten' | 21-28 |
| 2 Where the time goes | 112 | 1 | 0.298 | 0.298 |  | 'A chunk at ten Euler steps costs 237.5 ms end to end on the Orin at full power (' | 32-37 |
| **3 Seven tricks, one checkpoint** | 282 | 1 | 0.407 | 0.407 |  | '**Speculative chunk selection** [arXiv:2610.28019]. Choosing among four candidat' | 58-61 |
| **4 The recipe, and what does not transfer** | 117 | 1 | 0.420 | 0.420 |  | 'Turn on the prefix overwrite and the primitive projection with seam conditioning' | 85-91 |
| 5 Related work | 120 | 1 | 0.189 | 0.189 |  | 'Other chunking tricks are also reported on desktop-class GPUs: extending the exe' | 95-101 |
| 6 Limitations | 116 | 1 | 0.267 | 0.267 |  | 'One policy (SmolVLA, 450M); π0-class models do not fit the Orin, which is itself' | 105-110 |
| Appendix: from plain name to gate (short, noisy) | 18 | 1 | 0.172 | 0.172 |  | 'Every number in this paper is recomputable from the repository; this table maps ' | 114-114 |
| (figure and table captions) | 119 | 1 | 0.284 | 0.284 |  | "Fig. 1 — where a SmolVLA chunk's time goes on the Orin NX (vla.cpp, ten Euler st" | 39-81 |

Paper mean 0.317; 100 % of words in chunks above the human-reference maximum (0.106).

## built PDF

| section | words | chunks | mean | max | delta | worst paragraph | source lines |
|---|---|---|---|---|---|---|---|
| **Abstract** | 232 | 1 | 0.244 | 0.244 | +0.000 | 'Training-free tricks promise faster or smoother execution of flow-matching visio' | 12-26 |
| 3 Seven tricks, one checkpoint (short, noisy) | 17 | 1 | 0.201 | 0.201 | +0.000 | 'All offline effects use the same SmolVLA checkpoint and the same 20 recorded epi' | 62-64 |
| **1 Introduction** | 280 | 1 | 0.267 | 0.267 | +0.000 | 'per delay). Prefix overwrite vs exact real-time chunking (G13b). Robot-learning ' | 65-88 |
| 2 Where the time goes | 143 | 1 | 0.188 | 0.188 | +0.000 | 'dominates. Do not sample several chunks per decision on a sequential edge engine' | 112-118 |
| 5 Limitations (short, noisy) | 14 | 1 | 0.156 | 0.156 | +0.000 | 'Figure 2: Median boundary-jump cut against naive asynchronous execution, 254 bou' | 131-132 |
| 2 Euler steps | 257 | 1 | 0.177 | 0.177 | +0.000 | 'One policy (SmolVLA, 450M); π0 -class models do not fit the Orin, which is itsel' | 145-155 |
| **4 The recipe, and what does not transfer** | 60 | 1 | 0.228 | 0.228 | +0.000 | 'Turn on the prefix overwrite and the primitive projection with seam conditioning' | 186-191 |

Paper mean 0.223; 100 % of words in chunks above the human-reference maximum (0.106).
