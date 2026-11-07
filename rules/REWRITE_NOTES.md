# Rewrite notes for the owner: why the highest-scoring paragraphs read as machine text

Source: the EditLens maps of 2026-11-04 (`<paper>/map.md`, `<paper>/marked.md` in this folder), scored on the rendered markdown (`paper/DRAFT_4p.md`, numbers filled in). Line numbers are the same in `DRAFT_4p.md` and in the source (`DRAFT_4p.md.in` or `DRAFT_4p.src.md`): edit the source, then rebuild.

The model that scored them is weaker than the production detector, and a paragraph can score low and still be generic, or score high and be fine.

Human reference for scale (three pre-2022 robot-learning papers): paragraph and paper means 0.05 to 0.10. Paper means now: rendered text 0.26 (jepa-world-model), 0.35 (register-reproducibility), 0.25 (reward-models-stopping-rule), 0.32 (vla-edge-inference); built PDF 0.16, 0.19, 0.11, 0.22.

## What the high-scoring paragraphs have in common (measured on the paragraphs below)

1. **Every sentence the same length.** Sentence-length standard deviation of 1 to 4 words in five of them (vla-edge "4 The recipe": four sentences, mean 28, sd 1; jepa "Where the predictor fails" at lines 78 and 56: mean 29 to 30, sd 3 to 4). People vary.
2. **A repeated paragraph shape.** vla-edge section 3 has four paragraphs built identically: bold label, bracketed arXiv id, one sentence of mechanism, one clause of "but" and a figure reference. Four in a row reads as a template.
3. **Parallel triples and stacked imperatives.** "Turn on ... Keep ... Do not ..."; "Three things follow. First ... Second ... Third"; "It rests on three conditions"; three bold labels in a row.
4. **One parenthesis format, repeated.** register "One statistic": three consecutive clauses of the form (value, CI, bar, n, verdict). Identical bracket grammar, three times in one sentence.
5. **No trace of the person.** No first-person decision, no thing that went wrong, no reason for a choice. Every paragraph states a result in a neutral voice, including the limitations.
6. **Closing and framing sentences that say nothing new.** "The register stays open." "The input format, not the robot fine-tune, decided the result." "The recipe is short."

## vla-edge-inference (`DRAFT_4p.md`)

| lines | score | what stands out |
|---|---|---|
| 58-61 speculative chunk selection | 0.445 | 62 words, 3 sentences, 5 numbers; first of four same-shape paragraphs (point 2); a very long middle sentence (sd 22) |
| 46-49 prefix overwrite vs real-time chunking | 0.436 | same shape; "passes ... at every delay" is a summary of a table, not an observation |
| 63-65 entropy-adaptive length | 0.420 | shortest of the four, still the same shape; "sits at its floor in both task phases" is stated without saying what you looked at |
| 85-91 the recipe | 0.420 | four sentences of identical length (sd 1), three imperatives in a row, no numbers in the whole paragraph |
| 51-53 primitive projection | 0.400 | "Both pass their bars" opens with a verdict; one number in 48 words |
| 9-17 abstract | 0.310 | nine sentences, lengths 16 mean, steady; "What survives acts on the chunk seam." |

## register-reproducibility (`DRAFT_4p.md`)

| lines | score | what stands out |
|---|---|---|
| 59-66 one statistic | 0.426 | 120 words, 3 sentences, 19 numbers, one bracket grammar three times (point 4); mean sentence 40 words, sd 28 |
| 68-73 reproducibility of this study | 0.424 | a run of semicolon-separated counts, no sentence with a subject doing anything |
| 127-134 limitations | 0.405 | eight short declaratives; "One rig, one arm, one operator." then results-style sentences |
| 20-31 the register | 0.399 | three bold labels, a list of three conditions, "They are not a sample of the field" |
| 113-123 three failure classes | 0.371 | A / B / C with the same sentence frame each |
| 151-155 conclusion | 0.341 | "The register stays open." and a restating "both numbers belong in the same paper" |

## reward-models-stopping-rule (`DRAFT_4p.md`)

| lines | score | what stands out |
|---|---|---|
| 100-107 mid-episode | 0.393 | 147 words, 33 numbers, one long list of (catch, flag, AUROC, interval) |
| 21-31 introduction | 0.390 | 11 sentences of mean length 18, sd 7; a "Three things follow. First, Second, Third" outline of the paper |
| 124 and 109, captions | 0.364 / 0.361 | captions with legends in three parallel sentences |
| 128-138 related work | 0.357 | three sentences of 40 to 60 words, each a list of works with a verb |
| 90-98 at rest | 0.340 | 35 numbers in 160 words, nested parentheses |

## jepa-world-model (`DRAFT_4p.md`)

| lines | score | what stands out |
|---|---|---|
| 15 introduction | 0.524 | highest paragraph of all four papers; italic *encoder* / *predictor* contrast, then "The contribution is threefold" with a three-part list |
| 92 objection | 0.428 | one sentence of 45 words |
| 56 encoder reads | 0.380 | three sentences, sd 3; the same frame twice ("passes ... reads ...") |
| 78 grasp probe | 0.376 | sd 4; "On these rollouts, ... this pre-registered row fails" |
| 17 caveats | 0.364 | bold label, then a run of counts |
| 58 predictor forecasts | 0.354 | 16 numbers in 116 words, six short claims |

## Practical order
Start with the paragraph at the top of each table; rewrite it from what you remember, then run `ws paper-map <repo> --refs ~/scratch/WS-162/refs` to see whether that section moved (nothing reads the score automatically). Paragraph scores under about 40 words are noisy (a one-sentence paragraph scores on one sentence).
