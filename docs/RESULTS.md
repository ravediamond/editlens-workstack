# Results: what was done, what worked, what did not

Dates 2026-11-04 to 2026-11-06. Model: `pangram/editlens_Llama-3.2-3B` (open, weaker than the production detector), run on a Jetson Orin NX at 25 W,
fp16 (the authors' script loads the base in 4-bit; scores are close to theirs, not identical). Every number below is in
`results/EDITLENS_PASS_REPORT.md` or in the stored rows of `editlens-paper/repro/<experiment>/expected/`.
Score = EditLens estimate of how much AI editing a paragraph holds, in [0, 1].

## 1. Starting point

| | |
|---|---|
| `slopscore` and `lmscan` on the four papers | pass |
| alphaXiv (Pangram production detector) | flags all four |
| first map, rendered text, paper means (jepa / register / reward / VLA) | 0.259 / 0.349 / 0.250 / 0.317 |
| human references (3 robot-learning papers from before 2022) | 0.053 / 0.055 / 0.095 |

The repository's own prose gates did not predict the detector.

## 2. The rewrites, run by run (rendered text, paper mean)

| run (2026-11-05) | what changed in the papers | jepa | register | reward | VLA |
|---|---|---|---|---|---|
| 07:45 | first rewrite after the review | 0.186 | 0.280 | 0.209 | 0.240 |
| 10:41 | rules 41 to 70 (limitations ranked, author named, belief-first openings, voice) | 0.175 | 0.277 | 0.226 | 0.248 |
| 11:40 | rules 13, 23, 71 to 74 | 0.180 | 0.266 | 0.205 | 0.236 |
| 14:19 | de-polish (rule 78) | 0.165 | 0.236 | 0.175 | 0.221 |
| 15:05 | merge pass on sentence rhythm (rule 78g) | 0.170 | 0.253 | 0.180 | 0.229 |
| 15:40 | author rewrite of the highest paragraph | 0.166 | 0.239 | 0.170 | 0.220 |

- Worked: the de-polish pass (all four fell); the author's own rewrite of the highest paragraph (all four fell, jepa line 11 from 0.409 to 0.335).
- Did not work: rules 41 to 70 (two papers rose); the rhythm merge pass (all four rose or stayed level, none by more than 0.02); the 11:40 rules
  (register's highest paragraph rose from 0.508 to 0.579).
- Register only: removing the six highest-contribution sentences took the mean from 0.239 to 0.200; adding the real code behind the method left it at 0.198.
- Human references stayed 0.053 / 0.055 / 0.095 in every run; the highest human chunk is 0.106. After the last run, 69 % to 100 % of the words of each paper sit in chunks above that chunk.

## 3. The paragraph-level loop (`polish/`, `editlens-paper/repro/rewrite-loop/`)

Procedure: score paragraphs, rank sentences by what the paragraph loses without them, write 2 to 4 candidates that keep every number placeholder,
score them, keep the lowest that keeps every fact. 90 candidates in 50 paragraph-rounds. 50 of the 90 scored lower than the text they replaced;
the best candidate of a round improved its paragraph in 64 % of rounds, by 0.032 on average. One candidate dropped a placeholder and was rejected by the check.

| paper | paragraphs | mean before | mean after |
|---|---|---|---|
| register | 23 | 0.211 | 0.153 |
| JEPA | 22 | 0.176 | 0.160 |
| reward | 21 | 0.202 | 0.189 |
| VLA | 18 | 0.233 | 0.207 |

**Moves that lowered a paragraph** (before to after): name the works instead of "papers propose several uses" 0.315 to 0.164; open from the concrete case and give the class
letter after it 0.253 to 0.145; split a list sentence into plain statements 0.253 to 0.139; move a generic sentence elsewhere or drop a duplicate 0.273 to 0.150 and 0.275 to 0.158;
"we ran X on Y" with the named thing 0.271 to 0.156, 0.292 to 0.206, 0.211 to 0.154; interval in its own sentence 0.285 to 0.212.

**Moves that did not work**: merging sentences into longer ones with "so" or "which means" (register limitations 0.275 to 0.360, 0.366, 0.365); a contrast sentence on a short paragraph
(0.214 to 0.338); naming the tricks in the VLA introduction (0.270 to 0.281 and 0.314); swapping words for synonyms; tuning rhythm, order or pronouns (no effect);
paragraphs made of numbers, bars and verdicts (stayed above the median human results paragraph whatever was done; number-dense paragraphs stalled between 0.15 and 0.20).

**New text polished on 2026-11-06**: JEPA data-scale section and conclusion, worst paragraphs 0.366 to 0.267, 0.343 to 0.199, 0.325 to 0.184 (paper mean 0.179 to 0.163);
reward two paragraphs (0.176 to 0.170); register and VLA runs changed no text.
**Readings of the tool on 2026-11-06** (after layout changes and new sentences; baseline of the tool, now): register 0.156, 0.159; reward 0.176, 0.176; VLA 0.200, 0.204; JEPA 0.179, 0.170.
Sentences added after the last loop (layout Finding paragraphs, the register's note on cancelled gates) raised register and VLA; which sentence caused each rise was not isolated.

## 4. The hypotheses from the first sentence map, tested as controlled edits (62 paragraphs, mean change, 95 % bootstrap CI)

The map (311 sentences, later 469 by leave-one-out) suggested five features: contrast framing +0.029, semicolons +0.028, advice +0.021, verdict words +0.020, colon set-ups +0.012,
and "we" doing something -0.020. As edits:

| edit | effect |
|---|---|
| upper-case and double spaces (null: the model lower-cases and collapses spaces) | 0.000 |
| shuffle or reverse sentences | within ±0.004 |
| "we/our" to "I/my" | +0.001 |
| append a real sentence from another paragraph (length control) | +0.003 (-0.005 to +0.011) |
| keep only the first half of the sentences | -0.029 (-0.044 to -0.015) |
| drop the parentheticals | -0.018 (-0.033 to -0.005) |
| split at ", and" and ", but" | -0.014 (-0.020 to -0.007) |
| mask every number with "many" | -0.021 (-0.030 to -0.012) |
| join sentence pairs with a semicolon | +0.047 (+0.039 to +0.056), 92 % of paragraphs rise |
| append a generic closer | +0.017 |
| append a contrast closer | +0.011 |
| append advice | +0.001 |
| append "We ran this on the Jetson Orin NX." | -0.001 |
| append a verdict ("The row fails.") | -0.015 |

Held: semicolons, contrast framing (smaller than the correlation said). Reversed: the verdict sentence. Did nothing: advice, "we". As a result, rules 13, 60, 61, 66 and 67 were deleted.
The first battery used the highest and lowest paragraphs as hosts and misled (regression to the mean); every later test used unselected hosts and a control.

## 5. Human reference (39 pre-2022 robot-learning papers; first 40 results of one arXiv query, one dropped)

1,365 paragraphs scored after excluding 116 of back matter. Paper means: median 0.071, range 0.033 to 0.123. Median paragraph 0.063; 15 % above 0.15, 5 % above 0.25.
Results paragraphs: median 0.045 (140 paragraphs, 90th percentile 0.169). Introductions: median 0.053 (167 paragraphs, 90th percentile 0.177).
Our four papers read the same way from their PDFs: register 0.182, reward 0.145, VLA 0.138, JEPA 0.130, all above the highest human paper mean (0.123);
56 % of the 50 scoreable paragraphs of our PDFs are above 0.15, against 15 % of the human ones. A first version counted bibliography entries as prose (median 0.085); corrected on 2026-11-06.

## 6. What the model reacts to (triggers on 62 of our paragraphs and 100 random human paragraphs, with a real-sentence control)

Raised: a language-model-style sentence (+0.038 appended, +0.024 prepended), a generic "important and challenging problem" opener (+0.015), the digits of our own prose (+0.042; dropping them lowered it,
replacing names changed nothing). Lowered: a neutral figure or table pointer (-0.04 to -0.06), a long specific technical paragraph. Single evaluative words did not matter.

## 7. Style statistics as a target: did not work

Human paragraphs: style features correlate with the score weakly (largest rank correlation 0.25 in absolute value). Ours differ most in numeric tokens (9.5 per 100 words against 4.5),
passive (0.4 against 1.1), contrast and connective words. Seven paragraphs from two papers rewritten toward those features ("but", "however", "while", "so", the passive):
five rose, two fell, mean +0.020 (register related work 0.194 to 0.280). One round, seven paragraphs. Recorded as rule 91.

## 8. Lexicon and additivity

- Lexicon (469 sentence effects, 2,042 word deletions in the 20 highest paragraphs): words that name a method for talking about itself (protocol, rule, committed, reports, CI) go with higher scores;
  plain task words and units (table, takes, tested, task, not) with lower ones. 19 words pass the strict test. Built on three papers it predicts the sentence effects of the fourth at r 0.116 against 0.096 for the 95th percentile of shuffled labels. Sentence and word sources agree in sign for 48 of 80 words.
- Additivity of a real rewrite: 26 changed paragraphs split into 46 sentence-level hunks, each applied alone. In the 14 paragraphs with two or more hunks the single effects summed to -0.067 against -0.063 for the whole rewrite
  (r 0.94, Spearman 0.86, mean gap 0.010 per paragraph); the largest hunk has the sign of the whole rewrite in all 14. 45 of the 46 hunks are reworded sentences.

## 9. Not done, not known

- The production detector was not run on the papers (about $3.2 per full pass at the listed rate). None of the effects above is shown to carry over to it.
- The rewrites were written by the same assistant that drafted the papers; the author had not read them paragraph by paragraph.
- All 62 test paragraphs come from four papers of one author; trigger edits use one language-model-style sentence and one figure pointer we wrote.
- The human set is the first 40 results of one query, not a sample of the field.
- All four papers are above the human range after every run. The part that stayed high in every test is the part only the author has: the decision and its reason.
- The human-dose study (`editlens-paper/repro/human-dose/`) has a protocol with proposed bars and no numbers yet.
