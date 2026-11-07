---
name: paper-polish
description: The paragraph-level EditLens loop for the owner's own research papers. Use after drafting or rewriting any section of a paper repo (ravediamond/paper-*), or when the owner says "polish", "lower the AI score", "run the loop on the paper". Scores each paragraph with the open EditLens 3B model on the Orin, ranks the sentences that push a paragraph up, and keeps the lowest rewrite that preserves every number.
---

# Paper polish (the loop)

Written 2026-11-05 from the rewrite of four papers (`journal/papers/ai-map/2026-11-05_rewrite/RESULTS.md`, paper repo `ravediamond/paper-editlens-sensitivity`). Read `journal/papers/ai-map/WRITING_RULES.md` groups L (rules 79 to 90) first; this skill is the procedure, the rules are the content. The lexicon is `journal/papers/ai-map/EDITLENS_LEXICON.md`.

**What the score is.** EditLens (`pangram/editlens_Llama-3.2-3B`) estimates how much AI editing a paragraph holds, in [0, 1]. It is the open model, weaker than the production detector, so a low score predicts little about alphaXiv or Pangram. It says nothing about who wrote a paragraph: these papers are drafted with an AI assistant, and the paper says so (rule 89). The model is CC BY-NC-SA 4.0: owner's own research papers only; `scripts/paper_map.py`'s fence enforces it. Reference: 39 human robot-learning papers from before November 2022 have paper means with a median of 0.071 (0.033 to 0.123) and results paragraphs with a median of 0.045 and a 90th percentile of 0.169 (`paper-editlens-sensitivity`, `repro/human-reference`); our rewritten result paragraphs stalled near 0.15, high for a human one.

## Procedure (one paper repo, one section or the whole paper)

1. **Draft first, against the rules.** Write the section under the `paper-writing` skill (named things, "we ran X on Y", one claim and at most two numbers per sentence, intervals in their own sentence, no list of four, no semicolons, no appended closers, the case before the class label). Do not start the loop on a paragraph whose structure will still change (rule 38).
2. **Start the model.** `ws paper-polish serve` (about a minute, about 7 GB, 0.5 s per paragraph at 25 W; keep the quiet power profile). `ws paper-polish stop` when the paper is done.
3. **Baseline.** `ws paper-polish list ~/scratch/paper-repos/paper-X --top 10`. The first call freezes `polish/inventory.json` in the repo (the "before"). Paragraph numbers are stable while paragraphs are only rewritten, not added or removed.
4. **For each paragraph above 0.20, highest first:**
   1. `ws paper-polish loo REPO N`: the sentences that push the paragraph up. Fix the top one or two, not the whole paragraph (rule 80).
   2. Write two to four candidates as a JSON list of source texts (placeholders kept, rule 30) using the measured moves below.
   3. `ws paper-polish try REPO N cands.json --round r1`, then `ws paper-polish apply REPO N K` for the lowest candidate that keeps every fact. `apply` refuses a candidate whose placeholders differ.
   4. Up to three rounds. Stop at a plateau (the best candidate gains less than 0.01), under 0.20, or when only the author's own content would lower it (rule 88); a paper mean under 0.13 is inside the human range.
5. **Moves that worked, with their size** (this paper set): name the works or the thing in place of "papers propose several uses" (0.315 to 0.164); split a list sentence into plain statements (0.253 to 0.139); open with the concrete case and give the class label after it (0.253 to 0.145); "we ran X on Y [cite]" for a bare description (0.271 to 0.156); put the interval or figure reference in its own sentence (0.285 to 0.212); move a generic sentence to where it belongs or drop one that repeats another (0.273 to 0.150).
6. **Triggers measured on unselected hosts with a control (rule 92):** language-model-style sentences, generic "important and challenging problem" openers and the digits of the prose raise a paragraph; a neutral figure or table pointer and long specific technical detail lower it; single evaluative words do not matter. Never test a move on the highest or lowest paragraphs only (regression to the mean).
6b. **Moves that did not work, do not repeat:** merging sentences into longer ones with "so" or "which means" (0.275 to 0.36); adding a contrast or generic closer (raises); joining with a semicolon (raises, +0.047); tuning rhythm, order or pronouns (no effect); swapping a word for a synonym for the score alone; copying the style features of human papers (adding "but", "however", "while", "so" or the passive: 5 of 7 paragraphs rose, rule 91).
7. **Never:** change a number, a placeholder or a verdict; invent a decision, a surprise or a reason (rule 4); drop a fact to lower a score (move it, or say in the repo's CHANGELOG what was dropped and why).
8. **Ask the owner for what only the owner has.** Before polishing a results section, ask for one decision-and-reason per section (what was chosen and why; what went wrong). If there is none, leave it out. That is what lowers result paragraphs below the floor, and no rewrite supplies it.

## After the loop

- `ws paper-polish report REPO`: mean before and after, worst paragraph, paragraphs moved.
- Port the changed paragraphs to the tex twin and rebuild (rule 90): `main.src.tex` via `md2tex.py` or by hand, `python3 paper/make_paper.py`, restore regenerated figure binaries (`git restore paper/fig`), `git add paper`, `make l0 paper`, `make pdf`. `numbers.json` must not change. `ws prose-check` must pass.
- Commit `polish/` with the paper: `polish/iterlog.jsonl` is the provenance of the rewrite, `polish/inventory.json` the baseline.
- CHANGELOG line: which sections were polished, the mean before and after, anything moved or dropped.
- If the paper repo has moved on upstream, do not merge generated files: `git fetch`, branch from `origin/main`, replay the paragraph rewrites onto the source (`repro/rewrite-loop/scripts/reapply.py` in `paper-editlens-sensitivity` is the pattern), regenerate, check, push.
- Log it in the item's `log:` line: sections polished, mean before and after, the paper-repo commit. Never present the score as evidence of human writing.
