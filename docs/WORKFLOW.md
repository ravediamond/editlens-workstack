# The workflow

What was done to four research papers between 2026-11-04 and 2026-11-06, why, what it showed, and what is still open. The full
account with every number is `results/EDITLENS_PASS_REPORT.md`; this file is the map of it and the procedure to continue.

## 1. The situation

- Four short robotics papers (`papers/`): a register of re-tested claims, a reward-model stopping rule, VLA edge inference,
  a JEPA world model. They were drafted with an AI assistant, and each paper says so.
- alphaXiv runs Pangram's AI-editing detector and flagged the four papers. The repository's own prose gates (`slopscore`, `lmscan`)
  pass them, so those gates tell nothing about Pangram's detector.
- Pangram released the open weights of the model behind that detector's EditLens paper: `pangram/editlens_Llama-3.2-3B` (1024
  tokens, regresses how much AI editing a text holds, in [0, 1]). It is weaker than the production detector (their numbers:
  RAID binary F1 0.930 against 0.992) and is licensed CC BY-NC-SA 4.0, non-commercial: the owner's own papers only.

## 2. The four steps that were run

1. **Map** (`tools/paper_map.py`). Score each section and paragraph of each paper and of three human papers from before 2022. Output:
   `map.md` (section table with the change since the last run) and `marked.md` (every paragraph with its score and source lines),
   kept per run in `results/ai-map/<date>/<paper>/`. First map: paper means 0.22 to 0.32 against 0.05 to 0.10 for the human references.
2. **Rules** (`rules/WRITING_RULES.md`, 92 rules in groups A to L). Written from the sentence-level scores of the papers and from ordinary
   experimental-writing practice. Groups A to J are about writing a checkable paper in the author's voice. Groups K and L record
   what the detector reacted to; they are findings about the detector, not goals. Five rules (13, 60, 61, 66, 67) were deleted
   when controlled edits showed they raised the score. `rules/EDITLENS_LEXICON.md` lists words that go with higher and lower scores.
3. **Rewrite loop** (`editlens-paper/repro/rewrite-loop/`, `polish/` in each paper). Paragraph by paragraph: rank sentences by what
   the paragraph loses without them, write candidates that keep every number placeholder, score, keep the lowest that keeps
   every fact. 90 candidates in 50 paragraph-rounds; paper means moved by 0.013 to 0.058 and stayed above the human range.
   Its record: `editlens-paper/repro/rewrite-loop/` and `polish/` in each paper. The commands are in `tools/paper_polish.py`.
4. **Experiments on the detector** (`editlens-paper/repro/`). Controlled edits on 62 paragraphs (two of five suspected features held,
   one reversed, two did nothing), additivity of the rewrite (hunk effects sum to the rewrite effect, r 0.94), attribution (469
   sentences, 2,042 word deletions, a weak real lexicon), a human reference (39 pre-2022 robot-learning papers: paper-mean median
   0.071, results paragraphs median 0.045), triggers on unselected hosts (LM-style sentences, generic openers and the digits of
   the prose raise a paragraph; a neutral figure pointer and long specific technical detail lower it).

## 3. What the work says (details and numbers: `RESULTS.md`)

- Naming things and plain "we ran X on Y" sentences lower a paragraph; generic framing, list sentences, semicolons and generic
  closers raise it; rhythm, order and pronouns do nothing. Copying a human style by its statistics did not work (5 of 7 rose).
- What stays high is what only the author can write: the decision and its reason, what surprised him. No rewrite supplies it.
- The open model estimates how much AI editing a paragraph holds; it does not measure authorship. Nothing here shows that the effects carry
  over to the production detector.

## 4. The current direction (owner, 2026-11-06)

The EditLens paper was nearly dead ("the model is too good"). It is **kept and reframed as a measurement-validity study**:

> Same edit magnitude, opposite direction. Does the open EditLens 3B score fall when a human edits an AI-drafted paragraph as much
> as it rises when an AI edits a human paragraph, or does it track the last editor?

- *Human direction data*: the owner's own hand rewrites of the four papers, one commit per editing session, over the coming weeks.
- *AI direction data*: 600 rows of the authors' released dataset (`pangram/editlens_iclr`, test split) scored with the same model.
- *Metric*: EditLens's own magnitude (cosine of Qwen3-Embedding-0.6B embeddings, soft n-grams with MiniLM), five fixed bins.
- *Protocol and bars*: `editlens-paper/repro/human-dose/PROTOCOL.md`. The bars B1 to B4 are **proposed**; the owner confirms or changes
  them before the first number (item WS-001). Local 3B model only until the curve is readable; one production Pangram API run after
  that, under the gate in the protocol (cap $25).
- Every outcome is a result: the curves mirror (score measures magnitude), small human edits collapse it (it tracks the last editor),
  or human polish barely moves it (robust).

## 5. Loop to continue (per hand-edit batch)

```
owner: edits papers/<name>/paper/DRAFT_4p.src.md by hand (no scorer open), commits in the original repo, runs tools/sync_papers.py,
       then types `go WS-003` (a batch) in workstack/GO.txt
agent: WS-003 (see workstack/prompts/WS-003.md): snapshot, align, magnitude, score_versions, analyze --progress, commit expected/*.json
```

## 6. Open items from the pass report

1. Run the production Pangram detector once on the four PDFs (about $3.2 per full pass at the listed rate). Needs the owner's `go prod`.
2. The author reads the rewrites paragraph by paragraph and rewrites what he does not stand behind: the only step that changes who wrote the text.
3. One decision-and-reason per results section (rule 88): content only the author has.
4. The register, VLA and reward papers changed after the last loop pass; their current scores are in the 2026-11-06 reading of section 7 of the pass report.

## 7. Where things live

| need | file |
|---|---|
| every number of the history | `results/EDITLENS_PASS_REPORT.md` |
| what the model computes (score decoding, preprocessing, thresholds that are not published) | `results/WS-162-paper-map-notes.md` |
| score maps of every run | `results/ai-map/<date>/<paper>/{map,marked}.md` |
| reproducibility class of each paper number | `results/REPRO_STATUS.md`, `papers/*/REPRO_AUDIT.md` |
| the rules, the voice, the lexicon | `rules/` |
| the experiments | `editlens-paper/repro/<name>/{PROTOCOL,README,REPRODUCE}.md` |
| the owner's prompts that started it | `docs/original-prompts/` |
