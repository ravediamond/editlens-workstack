# AGENTS.md — rules for any AI agent working in this repository

This repository is self-contained. Work only from what is in it. Do not look for, clone, or ask for any other repository, and do
not rely on files outside it (the owner's other machines and private repositories are out of reach by design).

Owner: Ravindu Somawansa. Everything here is his own research; the four papers and the EditLens study are his.

## 1. What this repository is

A work stack plus everything it needs, for one workflow: **improving four research papers, checking them with the open EditLens
model, keeping the writing rules that came out of that, and finishing the paper about the EditLens experiments**.

| folder | what it holds |
|---|---|
| `workstack/` | `QUEUE.md` (the items, WS-NNN), `GO.txt` (the owner's gates), `prompts/` (one self-contained prompt per item), `notes/` |
| `papers/paper-*/` | the four papers (source, `numbers.json`, `make_paper.py`, `repro/` rows, built PDF). `papers/SYNC.json` records which commit of each original repo they were copied from |
| `editlens-paper/` | the paper about the detector (`paper/`), and every experiment as `repro/<name>/` (protocol, scripts, stored results, `l0_check.py`). `repro/human-dose/` is the open study |
| `tools/` | `paper_map.py` (per-section score map), `paper_polish.py` (scoring server + `list`, `loo`, `try`, `apply`, `report`), `paper_sentences.py`, `prose_check.py` (slopscore + lmscan gate), `sync_papers.py` (owner only) |
| `rules/` | `WRITING_RULES.md`, `MY_STYLE.md`, `EDITLENS_LEXICON.md`, `REWRITE_NOTES.md` |
| `results/` | `EDITLENS_PASS_REPORT.md` (the full history with numbers), score maps of every run (`ai-map/`), `REPRO_STATUS.md`, notes on the model |
| `originals/` | copies of the EditLens authors' code, configs and data (CC BY-NC-SA); the paper PDF goes here |
| `docs/` | `WORKFLOW.md` (the workflow, step by step), `RESULTS.md` (what was done, what worked, what did not), `original-prompts/` (the prompts this was built from; they name an Orin and a private repo you cannot reach: context only) |

Read `docs/WORKFLOW.md` and `docs/RESULTS.md` first, then `workstack/QUEUE.md`.

## 2. Notes that apply to every item

1. **What was done, what worked, what did not** is in `docs/RESULTS.md`. Read it before choosing an approach; the numbers behind it are
   in `results/EDITLENS_PASS_REPORT.md` and in each `editlens-paper/repro/<experiment>/expected/`.
2. **Protocols are the owner's.** A bar, threshold or success criterion is written before the data it judges, by the owner. If one is missing,
   set the item to `waiting-owner` with one actionable line. Anything decided after seeing data is labelled *exploratory*. A frozen protocol
   changes through a numbered deviation signed by the owner.
3. **Numbers come from files.** Quote a number from a file you can open, with its n, and write its path next to it. `paper/make_paper.py` is how
   numbers reach a paper; a new number is a new anchored entry there.
4. **Model, licence and tokens.** `pangram/editlens_Llama-3.2-3B` (on `meta-llama/Llama-3.2-3B`) is CC BY-NC-SA 4.0, non-commercial, gated per
   account. `tools/paper_map.py` has a path fence (`papers/`, `editlens-paper/`, `results/`, `refs/` or `EDITLENS_REFS`) that enforces the licence
   scope. Tokens come from `HF_TOKEN` or the Hugging Face cache and are never printed, logged or committed.
5. **Paid calls.** The production Pangram API costs money: it runs after `go prod WS-NNN` in `workstack/GO.txt` (cap $25 in the protocol).
6. **Commits.** One line, no `Co-Authored-By`, no session links, no mention of an AI. Author as in the owner's git config; if none is set,
   `-c user.name="Ravindu Somawansa" -c user.email="ravindu.somawansa@gmail.com"`. `git pull --rebase` before every push.
7. **No secrets in the repository.** Run `git diff --cached` and look before every commit.

## 3. How to run an item

1. Read `workstack/QUEUE.md`: take the first item with `status: todo` whose `depends` are done and whose `needs` are met
   (`offline` is always met; `gpu` means a CUDA machine with the gated model; `go` / `go prod` need a line in `workstack/GO.txt`).
2. Set `status: doing`, commit `workstack: WS-NNN doing`, push. Read its prompt (`workstack/prompts/WS-NNN.md`) completely.
3. Do exactly its scope. Keep `workstack/notes/WS-NNN.md` current: numbers with their files, paths created, open question, next step.
4. Commit at every milestone. Run `make check` before closing an item that touched a paper, a protocol or a result.
5. End in one state and commit `workstack: WS-NNN <status>`:
   - `done`: add `result:` with the file and the key number (n, verdict wording asked for).
   - `waiting-owner`: `owner-type:` (review, validate, do, decide) and `needs-from-owner:` one actionable line with its time.
   - `blocked`: `blocker:` the error, what you tried twice, what would unblock it.
6. Append follow-ups at the end of the queue with `status: proposed`; never reorder, delete or rewrite other items.
7. Report in one paragraph per item: the result, the file, one next step. No recap of the steps.

## 4. Commands (from the repository root)

```bash
pip install -r tools/requirements-editlens.txt          # torch is assumed installed; GPU needed only for scoring
make check                                               # all L0 checks and every paper regenerated from its stored rows (CPU, no model)
git restore 'papers/*/paper/fig' 'editlens-paper/paper/fig'  # after make check: it regenerates figure binaries byte-differently; keep the committed ones unless you changed a figure on purpose
python tools/paper_polish.py serve                       # load the 3B scorer (about a minute, about 7 GB GPU); `stop` when done
python tools/paper_polish.py list papers/paper-X --top 10   # paragraph scores, baseline frozen in papers/paper-X/polish/
python tools/paper_polish.py loo|try|apply|report ...     # sentence leave-one-out, candidate scoring, apply a candidate, before/after
python tools/paper_map.py papers/paper-X                 # per-section map of one paper (writes under runs/, copy into results/ai-map/<date>/)
python tools/prose_check.py <file.md>                    # slopscore + lmscan gate on a text (needs tools/requirements-prose.txt)
```

Everything that needs the gated model or a GPU is **L1** and is written as a command in the experiment's `REPRODUCE.md`; everything
that recomputes from stored rows is **L0** and must pass on a laptop.
