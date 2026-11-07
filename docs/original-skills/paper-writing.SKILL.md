---
name: paper-writing
description: The writing rules for Ravindu's papers. Read before writing or rewriting any paper prose (abstract, introduction, method, results, related work, limitations, conclusion, a paper repo README), whether in a paper repo or under journal/papers, and apply them while generating the text.
---

# Paper writing (the rules)

The rules are in `journal/papers/ai-map/WRITING_RULES.md` (groups A to L; group L, drafting against EditLens; group I is the voice, from `MY_STYLE.md`; group J the tone; group K, rule 78, de-polish: it overrides the voice rules where they conflict). Read the whole file before you write or edit paper prose; it is short. Also read `journal/papers/ai-map/MY_STYLE.md`: Ravindu's own voice in paper mode (what to keep, what to drop). The rules decide what is allowed; the style decides how it sounds. Then:

1. **Order of work.** Follow group A before writing a section (write from the record: the result files, notebook, commit log and plots; one sentence for what the section must leave; the decisions with their reasons; what went wrong or surprised, only if it did). Then write the section against groups B to F. Edit in passes (rule 38): facts and structure, then sentences, then words, then numbers and citations.
2. **What the rules do not touch.** Numbers, claims, bars, results and citations come from the files and the protocol; a rewrite never changes them (rule 30). Tables and figures keep their numbers. Edit the source files of the paper repo, never `main.tex` or `DRAFT_4p.md`; run `python3 paper/make_paper.py` and `make check` after every edit.
3. **Never invent.** A surprise, a mistake or a reason for a decision goes in only if the record shows it (rule 4). If the record does not say why something was chosen, ask the owner or leave the sentence out.
4. **Draft against EditLens** (group L, rules 79 to 90; `journal/papers/ai-map/EDITLENS_LEXICON.md`). Write each section in the plain forms the rules list: named things, "we ran X on Y", one claim and at most two numbers per sentence, intervals in their own sentence, no list of four, no semicolons, no appended closers, the case before the class label. Then run the `paper-polish` skill on the section (`ws paper-polish list|loo|try|apply|report REPO`): score its paragraphs, fix the top one or two sentences of any paragraph above 0.20, rescore. Result paragraphs of ours stalled near 0.15 (human results paragraphs: median 0.046); ask the owner for one decision-and-reason per section instead of rewriting past it (rule 88).
5. **Checks after writing** (rule 40): `ws prose-check <source file>` must pass; `ws paper-map <repo>` is an optional pointer to paragraphs to reread, not a target. After a prose pass follow rule 90 (twins, figures, `make l0 paper`, PDF).
6. **Log it.** In the item's log line say that the paper prose followed `WRITING_RULES.md` and name the sections written.
