# Writing rules for the papers

Rules for writing a short experimental paper that a reader can check and that sounds like the person who ran the work. They come from three places: the dimensions the slopscore linter scores (`slopscore-lint explain`), what the highest-scoring paragraphs of the four papers have in common (REWRITE_NOTES.md), and ordinary good practice for experimental writing. They are about writing well. None of them is a trick against a detector, and following all of them does not guarantee any score.

## A. Before writing a section

1. **Write from the record, not from the existing paragraph.** Open the result file, the notebook, the commit log and the plots for that section. Write what happened in the order you remember it. Compare with the old paragraph only afterwards, to catch missing facts.
2. **Know the one thing the section must leave the reader with.** One sentence, in plain words, before you write. If you cannot write it, the section is not ready.
3. **List the decisions in the section.** For each: what you chose, why, what you rejected. Reasons are the part nobody else can produce, and the part reviewers ask about.
4. **List what went wrong or surprised you, if anything did.** A failed run, a bug found late, a number you did not believe, a bar you almost changed. Include it where it explains a result. Never invent one.
5. **Decide the numbers the argument needs.** Everything else goes in a table. A paragraph carries two or three numbers; a table carries the rest.

## B. Paragraphs

6. **One idea per paragraph.** Open with the claim in plain words. End when the idea ends: no closing sentence that repeats it.
7. **Do not announce the structure.** "Three things follow. First, ... Second, ... Third, ..." and "The contribution is threefold" are for long papers that need a map. A four-page paper does not. Say the three things as three sentences in the order the reader needs them.
8. **Do not give parallel items the same paragraph shape.** Four methods described as label, citation, mechanism, "but", figure reference read as a template. Put what is parallel in a table. Write prose where something needs explaining: the surprising one, the failing one.
9. **Bold run-in labels belong to definitions and to list items.** Not to every paragraph of a section.
10. **Lists are for lists.** If the items are steps, a list is right. If they are an argument, write it as sentences with the connections spelled out ("because", "so", "which means").
11. **Put the reader's question first, the evidence second, the caveat last.** A limitation belongs next to the claim it limits, with the result that would change it, and not in a separate list of generalities.
12. **Introductions state the problem and the gap in the order you met them.** What was the question, what did the literature not answer, what did you do. Avoid a paragraph that summarises the whole paper before the paper starts.

## C. Sentences

13. ~~Vary sentence length on purpose.~~ (Deleted 2026-11-05, owner decision: the sentence-level EditLens scores of 2026-11-05 showed this kind of sentence raising the AI-editing score; see rule 78.) Uneven length is fine when it comes from the content (rule 78f); do not engineer a rhythm.
14. **One claim per sentence.** If a sentence has more than about three numbers, split it or move the numbers to a table.
15. **Do not repeat one bracket format.** "(value, CI, bar, n, verdict)" three times in a row is a table row written as prose. Write the one that matters in words; tabulate the rest.
16. **Use a real subject.** "We ran", "the model scored", "the arm dropped it" are better than "it is shown that", "was observed". Passive is right for procedures where the agent does not matter.
17. **Avoid trailing "-ing" clauses that gesture.** ", highlighting the importance of ...", ", underscoring ...", ", paving the way ..." add no fact. Either state the fact or cut the clause.
18. **Use "not X but Y" and rule-of-three only when the content is exactly that.** Otherwise they are a habit of the page, not of the facts.
19. **Cut restatements.** A conclusion that repeats the abstract sentence by sentence, or a paragraph that ends "In summary", can go.
20. **Vary what a sentence starts with, because the content varies.** If five sentences start with the same word, the five facts usually differ in a way the opening should show.

## D. Words

21. **Plain verbs.** "is", "has", "uses", "costs", "fails" when that is what happened. Drop "leverage", "utilise", "showcase", "delve", "underscore", "navigate the landscape".
22. **No stacks of abstract nouns.** "representation fidelity alignment" says less than "the encoder keeps the grasp state".
23. **Vary the wording of recurring terms.** Repeating "bar", "gate" or "result" in every sentence makes a section read flat. Rotate with words the reader cannot mistake for something else (bar, pass mark, threshold; gate, test, check; reproduce, hold up, replicate). Keep exact only the labels that are defined values: verdicts and classes as they appear in tables (pass, fail, not proven, bar-first, same-commit, class A), and model and dataset names. (Owner decision 2026-11-05: replaces "define a term once, then use it unchanged".)
24. **Name things.** Model and version, file, dataset and n, date, tool, the device, the clock speed. A sentence with no name, number or condition is generic.
25. **Hedge once, where the doubt is, and say how big or why.** "May" and "somewhat" stacked on every claim read as filler. "One rig, 69 episodes, one operator's labels" is a hedge that tells the reader something.
26. **No inflated significance.** "Crucial", "pivotal", "key insight", "groundbreaking", "a testament to". Let the number carry the weight.
27. **No writing about the writing.** "In this section we will", "as noted above", "the crux of the issue", "put simply:".
28. **No sincerity markers.** "To be honest", "honestly", "truth be told", "a candid limitation".
29. **No vague sources.** "Studies show", "experts agree", "it is widely believed". Cite the paper and say what it did.

## E. Evidence and citations

30. **Every number comes from a file you can open.** Quote it from the file, with its n. If you do not have the number, do not state a magnitude.
31. **For each cited work, say what you take from it or dispute.** "A reports X on Y; our setting differs in Z." A string of "A does P, B does Q, C does R" is a list, not related work.
32. **Cite what you read.** If you only read the abstract, say what the abstract claims, and nothing about its method.
33. **Say what each figure and table is for in the text.** A reader should know what to look at before looking.
34. **Limitations that name the claim and the missing test.** "The labels are one person's and not blind; a second reader would show whether verdicts flip" is a limitation. "Our results may not generalise" is not.

## F. Mechanics

35. **Em dashes and semicolons sparingly.** A semicolon chain of five clauses is five sentences. An em-dash aside in every paragraph is a tic.
36. **Same units and format throughout.** One way to write intervals, percentages, and sample sizes.
37. **Check the draft against the lab record last, not first.** The usual error in a rewrite is a number or a claim that drifted. Re-run the paper's own checks (`make check`) after every edit.

## G. Process

38. **Edit in passes.** First facts and structure (sections A and B), then sentences (C), then words (D), then numbers and citations (E, F). Do not polish words in a paragraph whose structure will change.
39. **Read each section aloud once.** Mark where you hesitate. Those are usually sentences written for the form of the paper rather than for the reader.
40. **Use the tools as a sanity check, after writing.** The prose check and the EditLens map point at paragraphs to reread; they are not a measure of quality and not the target.

## H. From the November 2026 rewrite of the four papers

What the 2026-11-04 rewrite and the 2026-11-05 EditLens rerun showed still needed changing, as rules. Each names the paper where it came up. Voice and tone: `MY_STYLE.md`.

### Content only the author has

41. **Rank the limitations.** Open with the one that could overturn the main claim, then say what would test it and what is stopping that test (arm time, money, a missing file). Cut the caveats no reviewer would ask about. A list of equal-weight caveats is the paragraph that scored highest in two papers (register 0.447, jepa 0.376).
42. **Say who did it, as a fact.** "Labelled by one person" hides that the person is the author. Write "a single operator, the author, labelled every episode": the fact in the method's terms, not a confession (rule 72). The same goes for the person who picked the papers and the person who chose a bar.
43. **Open from the belief being tested, not from the field.** "Papers report latencies on desktop GPUs" could open anyone's paper. Start with what a reader would assume (tricks transfer, the latent is pose, a reward model beats a trivial signal), and why you doubted it. The VLA introduction scored 0.338 with the generic opening.
44. **Give each verdict a reaction.** After a result, one sentence on whether you expected it and what you did next on the robot (kept ten Euler steps, dropped the monitor, switched the claim). A paragraph of number, bar and verdict alone reads as a table in prose (vla Euler steps, 0.356).
45. **Say why the work started.** One sentence in the introduction on the moment that started it: the paper you tried first, the result that surprised you, the bar you were tempted to move. If the record does not hold it, ask the owner (rule 4).
46. **Name the simple baseline as advice.** When copy-last, the joints, episode length or a fixed rule wins, say it as a practitioner would: what to check before building the learned method. This is the thesis of all four papers; do not hide it in a table.

### Missing data and admin

47. **Fix a missing number before explaining it.** If a number is missing because data sits on another machine or a cheap rerun was not done, rerun or copy it first. Robometer's per-episode scores (about $6 to re-score) cost a body paragraph that scored 0.367. If it cannot be fixed, one line in Limitations.
48. **Admin goes to the appendix.** Provenance, why a CI is absent, which commit a protocol is in, how a file was copied: appendix or Limitations, not the body of a results section.
49. **Tell a failure once, where it changed something.** The `strict=False` load belongs where it triggered the load audit, not as an aside in Setup. A withdrawn result goes next to the version that replaced it.

### Facts that drifted

50. **Check every claim about your own role and tools.** Who wrote the engine, whose fork, who contributed what: from the record, precisely ("we contribute to vla.cpp; the overwrite runs on our fork"). "The author's own port" was wrong in the VLA paper. A conflict of interest is stated, not implied.
51. **Say how the evaluation data relates to the training data.** Training episodes, held-out episodes, a different dataset, recorded after training: in Setup, once. The VLA paper evaluated on training demonstrations and did not say so.
52. **Mark in-sample choices where the number appears.** A threshold, a probe or a control chosen after seeing the data is labelled in the same sentence or table row as its number, not only in Limitations (the reward paper does this; keep it).

### Captions, abstract, headings

53. **Captions say what to look at.** One sentence on what the figure or table shows, one on the thing to see. Method detail lives in the text once and is not repeated in every caption (two reward captions scored 0.36).
54. **The abstract leads with the finding, not the field.** At most four numbers. The first sentence is the result or the belief it overturns; the setup comes second.
55. **One pronoun per paper.** "I" or "we", chosen once. A single author may use either; mixing them reads as two authors.

### Build

56. **A blank line in the source is a paragraph in the PDF.** After `make_paper.py`, check that `main.tex` has blank lines between paragraphs; the jepa and register converters dropped them until 2026-11-04 and every section built as one block.
57. **Keep the twins in step.** Where a repo has both `DRAFT_4p.src.md` and `main.src.tex`, edit both or regenerate one from the other (`md2tex.py` in the reward repo), then diff the two texts. The VLA PDF in the repo was a stale twin with an older title.
58. **A new number is a new placeholder with an anchor.** Never type a number into prose. Add it to `make_paper.py` with a `lit_file` or file anchor, so `numbers.json` records where it came from.
59. **Rebuild and commit the PDF with the source.** A source change without a rebuilt `main.pdf` leaves the uploaded paper behind the repo.

## I. Voice (Ravindu's style in paper mode)

From two of his posts (prompt caching, 2024; enterprise agents, 2025); traits, sources and examples in `MY_STYLE.md`. Rules 43 and 46 already carry two of them (open from the belief being tested; the simple baseline as advice). These rules decide how the text sounds; groups A to H still decide what it may say.

60. ~~Contrast with the familiar first.~~ (Deleted 2026-11-05, owner decision: the sentence-level EditLens scores of 2026-11-05 showed this kind of sentence raising the AI-editing score; see rule 78.) Contrast only where a result contradicts something (rule 78d).
61. ~~Join the argument with "So".~~ (Deleted 2026-11-05, owner decision: the sentence-level EditLens scores of 2026-11-05 showed this kind of sentence raising the AI-editing score; see rule 78.)
62. **Parentheses carry a reason or an admission.** "(because the encoder never saw these rollouts)", "(the threshold was fitted on the same episodes)", "(sometimes the hardest part)". Not a second example, never a list of numbers.
63. **One lived detail per section, from the record.** A concrete cost or scene stands in for a general claim: three machines to get one stable number, scores left on another machine, a load that silently dropped 192 tensors. Never invented (rule 4); if the record has none, write none.
64. **One running example per paper.** Pick one episode, one anchor or one chunk and follow it from method to result to limitation, the way "The cat is on the mat" runs through the caching post.
65. **No questions in the prose or the headings.** State what a test checks as a declarative sentence ("The test is whether length still separates the outcomes before the timeout."). A paper answers; it does not ask. (Owner decision 2026-11-05: replaces "write each test as the question it answers".)
66. ~~A short judgement may end a sentence.~~ (Deleted 2026-11-05, owner decision: the sentence-level EditLens scores of 2026-11-05 showed this kind of sentence raising the AI-editing score; see rule 78.)
67. ~~End on what to use when.~~ (Deleted 2026-11-05, owner decision: the sentence-level EditLens scores of 2026-11-05 showed this kind of sentence raising the AI-editing score; see rule 78.) One practical sentence in the conclusion remains allowed (rule 78c).
68. **Simple on purpose, plain on purpose.** Short common words, technical terms only where they are the name of the thing. Show the simplicity; do not announce it ("we will keep it simple").
69. **Keep the blog out.** No "let's", no recaps, no stock phrases ("here's the truth", "the kicker", "sink or swim", "purgatory", "the lesson?"), no enumerated frames ("four walls", "the big three"). They read as model text, not as you.
70. **Fix the slips, never fake them.** Correct "a LLM", agreement errors ("does ... happens"), French spellings ("pourcentage") and the space before "?" and "!". Never add an error to sound human.
71. **No tidy triads; give depth by importance.** When describing categories, rules or results, do not give each the same grammar and length. Spend two sentences on the one that caused trouble or carries the claim, and half a sentence on the obvious one. Lists of three inside one sentence count too. "Two rules govern each entry. ..." scored 0.508, the worst paragraph of the four papers (register, 2026-11-05 map).

## J. Tone (owner decision 2026-11-05)

72. **Limitations in the method's voice, not as confessions.** State the confound, what already controls it, and the test planned: "With a single operator, observer bias is a confound; where commit order shows it, every bar predates its run, and a blind two-reader protocol is committed." Never "the weakest point is", "we failed to", "only". Do not overstate the control (rule 30): say for how many gates it holds.
73. **Frame a failure by the condition it failed under.** Say what did not transfer and under which constraint (an edge latency budget, a trivial baseline on the same rows, this data scale), and that the method may hold in its own setting. Do not claim why a method failed beyond what was tested: an unvalidated class is a proposal, not a cause.
74. **Put the strengths first, with their cost.** What worked, what it cost and what anyone can rebuild: total compute, rig price, how many results rebuild from published rows. A negative result reads as a contribution when the reader can redo it for that price.
75. **Counts go in a table, and the prose names one.** Three or more counts of the same kind (commit classes, verdicts, rig types, interval checks) form a small table; the sentence around it says which count carries the point ("most are bar-first and none result-first, Table 1"). A sentence that lists five counts in one grammar ("9 in simulation, 7 above $20k, 3 at $5-20k, 2 below $5k and 1 unstated") reads as a table row in prose (register, 2026-11-05).
76. **Long tables of text go to the appendix.** A table whose cells are sentences (the register: claim, bar, result for every paper) sits after the references, in one column; the body keeps the counts and one worked example. Flattened to text, such a table reads as fragments, not prose.
77. **Introduce categories through their example, not their label.** "Class A, the clock, is the easiest to see. Class B covers ... Class C is quicker to state" is a template however the openings vary. Start from the case (the adaptive chunking entry), say what happened, and give the class letter after it.

## K. De-polish (owner decision 2026-11-05)

EditLens estimates how much a text was edited by AI, not whether a machine wrote it. On 311 sentences of the four papers (2026-11-05, `ai_phrase_scores.json`), contrast framing (+0.029), semicolons (+0.028), advice or imperatives (+0.021), verdict words (+0.020) and colon set-ups (+0.012) raised a paragraph's score; short sentences (-0.014), named things (-0.015), "we"/"our" doing something (-0.020) and citations in the sentence (-0.025) lowered it. Polish reads as AI editing.

Controlled edits on 62 paragraphs the same evening (`2026-11-05_rewrite/RESULTS.md`, section 3) tested these correlations. Semicolons (+0.047 when two sentences are joined) and contrast framing (+0.011) held. Advice (+0.001), "we"/"our" (−0.001) and verdict words (an appended "The row fails." gave −0.015) did not; keep rules 78c and 78e for style, not for score. Group L has the rules that the controlled tests and the rewrite loop support.

78. **De-polish.**
    a. **Split dense sentences.** One claim, at most two numbers, few subordinate clauses. Move the rest of the numbers to a table (rule 75).
    b. **Drop most semicolons and colon set-ups.** Write two plain sentences instead. A colon before a list or a definition is fine.
    c. **No neat closers, aphorisms or advice.** No "So ...", no "A method that loses ... has not shown what it claims", no "probe the encoder first". One practical sentence is allowed in each conclusion, nowhere else.
    d. **Contrast only where a result contradicts something.** "ContactGuard finds X; we find the reverse" is a real contrast. "The method may be sound, but ..." is framing.
    e. **Plain description over interpretation.** "We ran X on Y [cite]; it gave Z." Name the model, the dataset, the file and the paper in the sentence. Let the reader draw the meaning.
    f. **Some unevenness is fine.** A slightly flat or repetitive sentence is better than a perfectly balanced one. Do not tune rhythm, synonyms or sentence openings for effect.
    g. **No framing joints; length is free.** Do not join two facts with a colon or an "X, with Y" construction that sets up the second ("One pass uses the imagined latent: in the anticipation step ...", "misses the budget, with one decision taking ..."). Write them as two sentences, or as one plain sentence with "and". Sentence length and rhythm do not matter: across 487 sentences, length and score correlated at 0.07. (Owner decision 2026-11-05, replacing "don't over-split": the 15:01 run scored the merged text higher than the split text in all four papers, jepa 0.189 to 0.211, register 0.236 to 0.268, reward 0.205 to 0.216, vla 0.241 to 0.256, and 4 of the 5 sentences that pushed the score most were colon or "with" joins introduced by the merge. The merge was reverted.)

## L. Drafting against EditLens (2026-11-05)

Evidence: `2026-11-05_rewrite/RESULTS.md` (90 candidate rewrites, 62 paragraphs of controlled edits, 469 sentences by leave-one-out) and `EDITLENS_LEXICON.md`. EditLens here is the open 3B model; its score is a pointer to paragraphs to reread (rule 40), not a measure of authorship or quality. These rules are about getting a paper out of the first draft at or below 0.20 per paragraph.

79. **Score each paragraph once, right after drafting it.** `ws paper-polish` (skill `paper-polish`, `scripts/paper_polish.py`) keeps the open model loaded (`serve`), lists a paper's paragraphs with their scores (`list`), ranks a paragraph's sentences (`loo`), scores candidate rewrites with the placeholders rendered (`try`) and writes the chosen one into the source (`apply`, which refuses changed placeholders). About half a second per paragraph on the Orin at 25 W. Score the paragraphs above 40 words, not every sentence. The original workbench of 2026-11-05 is in `2026-11-05_rewrite/tools/`.
80. **Fix the highest sentence, not the paragraph.** Rank the sentences by what the paragraph loses without them (`loo.py`) and rewrite the top one or two. Whole-paragraph rewrites moved scores by about 0.03; replacing one generic or list sentence moved one paragraph from 0.253 to 0.139. A sentence that carries an interval or a figure reference ranked first more than once (+0.166).
81. **Name the thing; do not label the procedure.** Words such as protocol, rule, committed, reports, threshold, baseline, claims raise a sentence (`EDITLENS_LEXICON.md`). Write the file, the commit, the paper's name, the model's name or the number. Where the label is the defined term of the paper, keep it once, where it is defined (rule 23).
82. **Split lists of alternatives into statements.** "A larger GPU, a private checkpoint, the arm, or a step the write-up leaves out" was +0.147 in its paragraph. Two or three plain sentences, one thing each, cost nothing in content. Never a list of four in one grammar (rule 71).
83. **Open a paragraph with the case, give the class or label after it.** The jepa introduction went from 0.315 to 0.164 when the works were named (ContactGuard, HWM, H-JEPA) in place of "papers propose several uses"; register classes B and C went from 0.253 to 0.145 with the AUROC example first. Name only what the record shows (rule 50).
84. **No semicolons, no appended closers.** Joining two sentences with a semicolon raised 92 % of paragraphs (+0.047). A generic closer ("The result holds on this rig.") raised them by 0.017, a contrast closer ("a limit of the setting, not of the method") by 0.011. A short verdict sentence did not raise them (−0.015); a verdict may stay where the result needs it.
85. **Put an interval, a figure reference or a long number list in its own sentence.** "Length observed up to that cut gives X within policy (CI a–b; Fig. 2)." was the top sentence of its paragraph; with the CI in the next sentence the paragraph fell from 0.285 to 0.212. Counts of one kind go in a table (rule 75).
86. **Do not merge sentences to cut the count.** Joining facts with "so", "which means" or a comma chain raised the register limitations from 0.275 to 0.360 in three variants (rule 78g). Plain "We ran X on Y" sentences with the named thing lowered paragraphs most (vla Euler steps 0.271 to 0.156).
87. **Do not tune rhythm, order or pronouns.** Shuffling or reversing sentences, "we" against "I", sentence length and added words of the same paper all changed the score by less than 0.01. Dropping the parentheticals gave −0.018 and splitting at ", and" and ", but" −0.014, so write those as plain sentences when the content allows; do not do it for the score alone.
88. **Know where a human paper sits, and what rewriting cannot add.** In a reference set of 39 human robot-learning papers from before November 2022 (`paper-editlens-sensitivity`, `repro/human-reference`) the paper means have a median of 0.071 (0.033 to 0.123) and results paragraphs a median of 0.045 with a 90th percentile of 0.169 (after the bibliography fix of 2026-11-06). Our four papers, read the same way from their PDFs, are at 0.130 to 0.182, and result paragraphs of ours stopped near 0.15 in the rewrite: high for a human results paragraph, not a natural limit. Paragraphs made of numbers, bars and verdicts did not go lower by rewriting. What lowers them further is content only the author has: the decision and its reason, the thing that went wrong, the scene (rules 3, 4, 63). Before drafting a results section, ask the owner for one such detail per section and leave it out if there is none. Never invent one.
89. **A low score is not a claim about authorship.** The papers are drafted with an AI assistant; say so in the paper where the venue asks for it, and never present a score as evidence of human writing. The model is licensed CC BY-NC-SA 4.0: use it on the owner's own research papers only (`scripts/paper_map.py` fences this), and do not publish scores as a service.
90. **Build hygiene after a prose pass.** Edit the markdown source; port the same paragraphs to a `main.src.tex` twin where there is one (`2026-11-05_rewrite/tools/tw.py` does it for the vla paper; `md2tex.py` for reward); run `make_paper.py`; restore the regenerated figure binaries with `git restore paper/fig` (they change on every run and are not part of the edit); `git add paper` and `make l0 paper`; `make pdf`; `ws prose-check`. `numbers.json` must not change.
91. **Do not copy a human style by its statistics.** Across the paragraphs of 39 pre-2022 human papers (1,365 once back matter is excluded, earlier counted as 1,480), style features go with the score only weakly (largest rank correlation 0.25 in absolute value). Ours differ most in numeric tokens (9.5 against 4.5 per 100 words), passive constructions (0.4 against 1.1), and contrast and connective words (0.1 and 0.2 against 0.35 and 0.28). Rewriting seven paragraphs toward those features, with "but", "however", "while", "so" and the passive, raised five of them and lowered two, mean change +0.020 (the register related-work paragraph went from 0.194 to 0.280). A feature that goes with low scores in other people's text is not a move. Test an edit on your own paragraph with `ws paper-polish try` before it becomes a habit, and keep the moves of rules 80 to 87, which were measured as edits. Fewer numbers per paragraph did lower scores (masking numbers, −0.021), so keep to rules 14 and 75: one or two numbers in the prose and the rest in a table. Data: `paper-editlens-sensitivity`, `repro/human-reference`.
92. **What the open model reacts to, measured with a control.** On 62 of our paragraphs and 100 random human ones (not chosen by score, with a real-sentence control; `paper-editlens-sensitivity`, `repro/triggers`): a sentence in the style of a language model raised ours by 0.038 appended and 0.024 prepended ("plays a crucial role in leveraging the underlying structure of the data"); a generic opener ("an important and challenging problem") by 0.015; the digits of our own prose by 0.042 (dropping them lowered ours, while replacing names changed nothing). A neutral pointer sentence ("Figure 3 shows the result for each of the five tasks.") lowered ours by 0.04 to 0.06, and a long specific technical paragraph lowered them most (0.14 to 0.17). Single evaluative words (important, essential, novel) hardly mattered (0.005), and the gradient of the score shows no single trigger word. So write procedure, architecture and measurement in words and point to the figure or table that shows the number; keep generic framing and stock phrasing out; keep to one or two digits per paragraph and put the rest in a table. Method: choosing hosts at the ends of the score makes every edit look like it pulls the paragraph toward the middle (appending a neutral sentence to the highest hosts "lowered" them by 0.17), so test an edit on unselected hosts and against a control sentence.
