# What was done to the papers against the AI-editing analysis, 2026-11-04 to 2026-11-06

This file records, in order and with the numbers, everything done to lower the open EditLens score of the four research papers (register, reward models, VLA edge inference, JEPA world model), what the work showed about the detector, what is still unfinished, and where each piece lives. It was written on 2026-11-06 from the repositories and logs named below. Nothing in it is a claim about who wrote the papers.

## 1. Why this was done, and what a score means

alphaXiv runs Pangram's detector on uploaded papers and flagged the four papers as AI-written, although they pass the repository's own `slopscore` and `lmscan` checks. The owner uploaded the EditLens paper (Thai et al. 2025) and asked for a paragraph-by-paragraph loop that lowers the score, an analysis of what moves the model, and a paper about it.

EditLens regresses how much an AI edited a text, as a number between 0 and 1. It was trained on pairs of a source text and an AI-edited version of it, so it measures editing, and it does not say who wrote a text. We use the open model `pangram/editlens_Llama-3.2-3B`, a 3B model with a classification head that gives four buckets and a weighted-average score. It runs on the Orin at 25 W in about half a second per paragraph. The production detector that flagged the papers is a different and stronger model, and we did not run it. The open model is licensed CC BY-NC-SA 4.0, so it is used on the owner's own research papers only, and `scripts/paper_map.py` enforces that fence.

Three facts shape everything below. The papers were drafted with Claude Code, and the rewrites were written by Claude Code too, and the author has not yet read the rewrites paragraph by paragraph. A low score therefore says only that the open model sees little AI editing in a paragraph. It is a pointer to paragraphs worth rereading and never evidence that a person wrote them (rule 40 and rule 89 of `WRITING_RULES.md`). And no paper reached the human range, as section 7 shows.

## 2. Timeline

| date | what happened |
|---|---|
| 2026-11-04 and before | First map of the four papers: sentence-level scores of 311 sentences (`ai_phrase_scores.json`), a correlation table of which sentence features go with higher scores, and writing rules 41 to 70 from the November rewrite. |
| 2026-11-05 | Rewrite loop on the four papers (90 candidate rewrites in 50 paragraph-rounds), controlled edits on 62 paragraphs, 469-sentence leave-one-out, the lexicon, the human reference set, the trigger analysis, the style trial. Rule 78 (de-polish) was written and rules 13, 60, 61, 66 and 67 were deleted. The study got its own repository, `ravediamond/paper-editlens-sensitivity`, and the loop became a harness workflow (`ws paper-polish`, skill `paper-polish`). |
| 2026-11-06 | The human reference was recomputed after a bibliography fix. New text in the reward, VLA and JEPA papers was polished with the loop. The additivity test of the rewrites was run. The papers got the new layout (title panel, Finding boxes, schematic), and the register table was relabelled. |

## 3. The tools

The loop lives in `scripts/paper_polish.py`, called as `ws paper-polish` (the command is wired in `scripts/ws.py`). It keeps the open model loaded in a small server that reads requests from files, so a paragraph is scored in about half a second without reloading the model. The sub-commands are as follows.

| command | what it does |
|---|---|
| `serve`, `stop`, `status` | Load or unload the model (about 7 GB). |
| `list REPO --top N` | Scores every paragraph of the paper source that has at least 40 words, with the placeholders of the paper filled in, and prints the worst. The first call freezes the baseline in `polish/inventory.json` of the paper repository. |
| `loo REPO N` | Leave-one-out: what paragraph N loses when each sentence is removed, so the top one or two sentences can be fixed first. |
| `try REPO N cands.json --round R` | Scores candidate rewrites of paragraph N and logs every one to `polish/iterlog.jsonl`, which is the provenance of the rewrite. |
| `apply REPO N K` | Writes candidate K into the source. It refuses a candidate whose placeholders differ from the original, so a number or a claim cannot move. |
| `report REPO` | Word-weighted mean before and after, worst paragraph, paragraphs moved. |

The skill `.claude/skills/paper-polish/SKILL.md` holds the procedure, the moves that worked and the moves that did not. `CLAUDE.md` and `docs/HARNESS.md` point to it, so any later paper starts the same way: draft under the `paper-writing` skill, then run the loop on the section, then port the paragraphs to the LaTeX twin and rebuild. The writing rules are in `journal/papers/ai-map/WRITING_RULES.md`, groups K and L (rules 78 to 92) being the ones that come from this work.

## 4. What was done, step by step

### 4.1 The sentence map (2026-11-04 and 2026-11-05)

Every sentence of the four papers was scored with and without its paragraph, giving a table of 311 sentences (later 469 by leave-one-out) and a correlation of five sentence features with the paragraph score. Contrast framing (+0.029), semicolons (+0.028), advice or imperatives (+0.021), verdict words (+0.020) and colon set-ups (+0.012) went with higher scores, and a sentence in which "we" does something went with lower ones (−0.020). These correlations produced rule 78. They were hypotheses, and section 4.3 shows that three of the five did not survive a controlled test.

### 4.2 The rewrite loop (2026-11-05)

For each paragraph the sentences were ranked by what the paragraph loses without them. Two to four candidate rewrites were written for the top sentences with every placeholder kept, rendered, scored, and the lowest candidate that preserved every fact was kept. This ran for one to three rounds per paragraph. There were 90 candidates in 50 paragraph-rounds. Fifty of the 90 scored lower than the text they replaced, and the best candidate of a round improved its paragraph in 64 % of the rounds, by 0.032 on average. One candidate dropped a placeholder (a confidence interval) and was rejected by the check. In the register paper one sentence moved to a different paragraph and one that repeated another was dropped. No number, placeholder or verdict changed, `numbers.json` of each paper is unchanged, and `make l0 paper` passes.

Word-weighted mean paragraph score, original texts against the end of the rewrite:

| paper | paragraphs | before | after |
|---|---|---|---|
| register of re-tested claims | 23 | 0.211 | 0.153 |
| JEPA world model | 22 | 0.176 | 0.160 |
| reward models and a stopping rule | 21 | 0.202 | 0.189 |
| VLA edge inference | 18 | 0.233 | 0.207 |

The moves that lowered a paragraph most:

| move | case | before | after |
|---|---|---|---|
| name the works in place of "papers propose several uses" | JEPA introduction (ContactGuard, HWM and H-JEPA named) | 0.315 | 0.164 |
| open from the concrete case and give the class letter after it | register, classes B and C (the AUROC example first) | 0.253 | 0.145 |
| split a list sentence into plain statements | register, cold reruns ("a larger GPU, a private checkpoint, the arm, or a step the write-up leaves out") | 0.253 | 0.139 |
| move a generic sentence to where it belongs, or drop a duplicate | register, one sentence moved and limitations lost two | 0.273 and 0.275 | 0.150 and 0.158 |
| "we ran X on Y" with the named thing | VLA Euler steps, VLA power modes, reward data paragraph | 0.271, 0.292, 0.211 | 0.156, 0.206, 0.154 |
| put the interval in its own sentence | reward truncation paragraph | 0.285 | 0.212 |

The moves that did not work: merging sentences into longer ones with "so" or "which means" (the register limitations went from 0.275 to 0.360, 0.366 and 0.365 in three variants), adding a contrast sentence to a short paragraph (0.214 to 0.338), and naming the tricks in the VLA introduction (0.270 to 0.281 and 0.314). Paragraphs made of numbers, bars and verdicts stayed above the median of human results paragraphs whatever we did. Number-dense paragraphs (results, related work, setup) stalled between 0.15 and 0.20.

### 4.3 Controlled edits on 62 paragraphs (2026-11-05)

The correlation table could be wrong, so each suspected feature was tested as an edit on the same 62 paragraphs of at least 40 words, changing one thing at a time. Change in the paragraph score, mean over paragraphs with a 95 % bootstrap CI:

| edit | effect |
|---|---|
| upper-case and double spaces (a null: the model lower-cases and collapses spaces) | 0.000 exactly |
| shuffle or reverse the sentences | within ±0.004, CI contains 0 |
| "we/our" to "I/my" | +0.001 |
| append a real sentence from another paragraph of the same paper (a length control) | +0.003 (−0.005 to +0.011) |
| keep only the first half of the sentences | −0.029 (−0.044 to −0.015) |
| drop the parentheticals | −0.018 (−0.033 to −0.005) |
| split at ", and" and ", but" | −0.014 (−0.020 to −0.007) |
| mask every number with "many" | −0.021 (−0.030 to −0.012) |
| join sentence pairs with a semicolon | +0.047 (+0.039 to +0.056), 92 % of paragraphs rise |
| append a generic closer ("The result holds on this rig.") | +0.017 |
| append a contrast closer ("This is a limit of the setting, not of the method.") | +0.011 |
| append advice ("Check the simple baseline first.") | +0.001 |
| append "We ran this on the Jetson Orin NX." | −0.001 |
| append a verdict ("The row fails.") | −0.015 |

Two of the five features held (semicolons and contrast framing, the latter smaller than the correlation said). Advice and "we" did nothing, and the verdict sentence reversed its sign. This is why the writing rules that told us to vary sentence length and to end on what to use when were deleted: rhythm, order and pronouns do nothing to this model. The baseline texts had their semicolons and colons removed beforehand, so only adding them could be tested. The first battery used the highest and lowest paragraphs as hosts and misled us, because at the ends of the score any edit seems to pull a paragraph toward the middle (regression to the mean). Every later test used unselected hosts and a control sentence.

### 4.4 The human reference (2026-11-05, recomputed 2026-11-06)

To know what a low score looks like, we scored 39 human robot-learning papers submitted before November 2022 (the first 40 results of one arXiv query for 2018 to 2021, one dropped). Their PDFs were read with the same extractor used on our four PDFs, back matter was excluded by a year-and-venue rule, and each paragraph of at least 40 words was scored. The first version counted bibliography entries as prose and put the median at 0.085, so the rule was refined on 2026-11-06 and the numbers recomputed. The corrected values:

| quantity | value |
|---|---|
| paragraphs scored (after excluding 116 of back matter) | 1,365 |
| paper means | median 0.071, range 0.033 to 0.123 |
| median paragraph | 0.063; 15 % of paragraphs above 0.15, 5 % above 0.25 |
| results paragraphs | median 0.045 (140 paragraphs, 90th percentile 0.169) |
| introductions | median 0.053 (167 paragraphs, 90th percentile 0.177) |
| our four papers, read the same way from their PDFs | register 0.182, reward 0.145, VLA 0.138, JEPA 0.130 |

All four of our papers sit above all 39 human papers (the highest human paper mean is 0.123 and the lowest of ours is 0.130). Of the 50 scoreable paragraphs in our four PDFs, 56 % score above 0.15, against 15 % of the human paragraphs. The human set is the first 40 results of one query, not a sample of the field, and its section types are rough. Rule 88 and the skill carried the stale first numbers (median 0.085) until 2026-11-06 and were corrected in the same commit as this file.

### 4.5 What the open model reacts to (2026-11-05)

To find triggers, we added sentences to 62 of our paragraphs and to 100 random human paragraphs (not chosen by score), with a real-sentence control. A sentence in the style of a language model (a generic claim about how important a method is for the structure of the data, with stock verbs) raised ours by 0.038 appended and 0.024 prepended. A generic opener about an important and challenging problem raised them by 0.015. The digits of our own prose raised the score by 0.042 (dropping them lowered it, and replacing names changed nothing). A neutral pointer sentence ("Figure 3 shows the result for each of the five tasks.") lowered ours by 0.04 to 0.06, and a long specific technical paragraph lowered them most, by 0.14 to 0.17. Single evaluative words (important, essential, novel) hardly mattered (0.005), and the gradient of the score shows no single trigger word. This became rule 92.

### 4.6 A human style as a target (2026-11-05)

Across the human paragraphs, style features go with the score only weakly (the largest rank correlation is 0.25 in absolute value). Ours differ most in numeric tokens (9.5 per 100 words against 4.5), passive constructions (0.4 against 1.1) and contrast and connective words. We rewrote seven paragraphs from two papers toward those features, with "but", "however", "while", "so" and the passive. Five of the seven went up and two went down, with a mean change of +0.020 (the register related-work paragraph went from 0.194 to 0.280). The hypothesis that copying human style statistics lowers the score failed, and it is recorded as a negative result (rule 91). It is one round of seven paragraphs and features we chose, so it does not rule the idea out.

### 4.7 The lexicon (2026-11-05)

From the 469 sentence effects and 2,042 single-word deletions in the 20 highest paragraphs we built `EDITLENS_LEXICON.md`. Words that name a method for talking about itself (protocol, rule, committed, reports, CI) go with higher scores, and plain task words and units go with lower ones (table, takes, tested, task, not). Only 19 words pass the strict test. A lexicon built on three papers predicts the sentence effects of the fourth with a correlation of 0.116, against 0.096 for the 95th percentile of shuffled labels, so it is real and weak. The word-deletion source and the sentence source agree in sign for 48 of 80 words. One word changes a paragraph by +0.013 on average and by 0.157 at most. The lexicon is a tie-breaker between synonyms and a pointer to a sentence that needs a more specific noun, and it is never a target.

### 4.8 Additivity of the rewrite (2026-11-06)

The paper said we had not tested whether the changes of a real rewrite add up. For the 26 paragraphs the loop changed, each rewrite was split into sentence-level hunks (46 in all, found with `difflib` on the sentence lists), each hunk was applied alone to the original paragraph and scored. The protocol was committed before any score. In the 14 paragraphs with two or more hunks the single effects summed to −0.067 on average against −0.063 for the whole rewrite. The correlation between the two is 0.94 (Spearman 0.86), the mean gap is 0.010 per paragraph, and in each of the 14 the hunk with the largest effect has the sign of the whole rewrite. Forty-five of the 46 hunks are reworded sentences, so the test shows that sentence-level changes add up and does not separate named moves such as naming the works or splitting a list. Files: `repro/additivity` in `paper-editlens-sensitivity`.

### 4.9 Polishing the new text of each paper (2026-11-06)

New sections were written after the first rewrite, so the loop was run again on them.

| paper | what was polished | result |
|---|---|---|
| JEPA | The data-scale section and the conclusion. The worst paragraphs went from 0.366 to 0.267 (the ranking paragraph), from 0.343 to 0.199 (the encoder paragraph) and from 0.325 to 0.184 (the conclusion). The rewrites state each result as a plain sentence about what we ran, keep every number in the same placeholder, and drop the verdict sentence that opened the paragraph. | Paper mean 0.179 to 0.163 on the polish tool's reading at that moment. |
| reward | Two paragraphs (commit `f87e333`). | Mean 0.176 to 0.170 at that time. |
| register | Log only. The polish run changed no text. | Unchanged. |
| VLA | Log only. The run changed no text. | Unchanged. |

The sentences added later, for the layout and for the register label, were not polished.

## 5. Changes to the tooling and the rules

The study moved to its own repository, `ravediamond/paper-editlens-sensitivity`, with one folder per experiment under `repro/` (controlled edits, rewrite loop, additivity, attribution, human reference, triggers). Each folder has a protocol, scripts, the stored results, an L0 check that recomputes the numbers from them, and a reproduce file. The paper of that repository (which is about the detector and is written like the other papers) is the public record of the method.

In `road-to-robotics`:

- The `ws paper-polish` command and `scripts/paper_polish.py`, described in section 3.
- The skill `paper-polish`, and the pointers in `CLAUDE.md`, `docs/HARNESS.md` and the `paper-writing` and `workstack` skills.
- `WRITING_RULES.md`: rules 41 to 70 (November rewrite and voice), 71 to 77 (tone), 78 (de-polish), 79 to 92 (drafting against EditLens). Rules 13, 60, 61, 66 and 67 were deleted because the sentence-level scores showed that they raised the score.
- `EDITLENS_LEXICON.md` and the `2026-11-05_rewrite` folder with the tools, data and `RESULTS.md`.
- The human-reference numbers in rule 88 and in the skill were corrected on 2026-11-06 together with the `paper_polish.py` message that prints them.

## 6. What the work says about writing for this detector

Specific naming and plain "we ran X on Y" sentences lower a paragraph. Generic framing, list sentences, semicolons, generic closers and contrast closers raise it. A neutral pointer to a figure or table lowers it, and a language-model-style sentence raises it. Rhythm, sentence order and pronouns do nothing. Dropping parentheticals and splitting at ", and" and ", but" lower a paragraph a little, and masking numbers lowers it more, which is why one or two digits per paragraph in the prose and the rest in a table is the working rule. Copying a human style by its statistics did not work. The part that remains high is the part only the author can write: the decision and its reason, the thing that went wrong, the scene (rules 3, 4 and 63). We do not invent those, and where the record has none we write none.

## 7. Where the papers stand now

Readings of the polish tool on 2026-11-06, after the layout and the new text. The paragraph sets differ from section 4.2, because the tool scores only paragraphs of at least 40 words in the markdown source and skips tables and captions, so the numbers are comparable within a row and not across the two tables.

| paper | baseline of the tool | now | worst paragraph before and now |
|---|---|---|---|
| register | 0.156 | 0.159 | 0.218 and 0.273 |
| reward | 0.176 | 0.176 | 0.299 and 0.268 |
| VLA | 0.200 | 0.204 | 0.270 and 0.302 |
| JEPA | 0.179 | 0.170 | 0.366 and 0.331 |

The register and the VLA paper rose slightly, the reward paper is unchanged and JEPA fell. The rises come from sentences added after the last loop (the layout's Finding paragraphs, the register's explanation of cancelled gates), and I did not isolate which sentence caused each one. The JEPA reading was 0.163 right after its polish and 0.170 when read again after the layout. All four papers are still above the human range of section 4.4, so the loop lowered them without bringing them into it.

## 8. Limits

The open 3B model is weaker than the production detector, so none of these effects is shown to carry over to it. Running the production model on the four papers would cost about 3.2 dollars per full pass at the listed API rate. We did not spend it. The rewrites were written by the same assistant that drafted the papers, and the author has not read them paragraph by paragraph. All 62 test paragraphs come from four papers of one author, and the trigger edits use one language-model-style sentence and one figure pointer that we wrote. A score is not read as a statement about authorship anywhere.

## 9. Open items

- Run the loop again on the register, VLA and reward papers, because their text changed after the last pass (section 7).
- Run the production Pangram detector once on the four PDFs, which needs the owner's approval of the spend.
- The author reads the rewrites paragraph by paragraph and rewrites what he does not stand behind. This is the only step that changes who wrote the text.
- Ask for one decision-and-reason per results section (rule 88), since content only the author has is what lowered the remaining paragraphs most in every test.

## 10. Where everything is

| what | where |
|---|---|
| the study and its paper | `github.com/ravediamond/paper-editlens-sensitivity` (main at `840c082`), one `repro/<experiment>` folder each |
| polish logs per paper | `polish/inventory.json` and `polish/iterlog.jsonl` in each paper repository |
| the four papers | `ravediamond/paper-register-reproducibility` (`5753ec2`), `paper-reward-models-stopping-rule` (`e3fa6f1`), `paper-vla-edge-inference` (`30bd650`), `paper-jepa-world-model` (`7730133`) |
| the loop | `scripts/paper_polish.py`, `ws paper-polish`, `.claude/skills/paper-polish/SKILL.md` |
| the rules and the lexicon | `journal/papers/ai-map/WRITING_RULES.md` (groups I to L), `EDITLENS_LEXICON.md` |
| the first rewrite's data and tools | `journal/papers/ai-map/2026-11-05_rewrite/` (`RESULTS.md`, `tools/`, `data/`) |
