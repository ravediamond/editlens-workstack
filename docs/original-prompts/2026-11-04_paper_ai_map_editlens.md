# Claude Code prompt — paper AI map: Open Pangram EditLens 3B on the Orin, papers only, a map for the owner

Owner (chat 2026-11-04): his papers pass `scripts/prose_check.py` (slopscore + lmscan, WS-158/WS-161) but alphaXiv
flags them as AI-written. alphaXiv runs Pangram's production detector, a trained classifier; slopscore and lmscan only
see surface phrases and stylometry, so a pass there predicts nothing about Pangram. He wants Pangram's **open** model
run locally on the Orin, **for the papers only**.

What this item builds is a **map for the owner**: which sections and paragraphs of each paper read as AI to EditLens,
so he can rewrite those by hand. The open model is weaker than the production one, so a local score predicts little about alphaXiv.

## The model (facts from Pangram's own pages, checked 2026-11-04)

- Open Pangram release: https://www.pangram.com/blog/introducing-open-pangram — two open-weight EditLens detectors;
  we use **`pangram/editlens_Llama-3.2-3B`** (QLoRA adapter, 1024-token max sequence). Code: GitHub
  `pangramlabs/EditLens`; paper arXiv 2510.03154 (ICLR 2026); dataset `pangram/editlens_iclr`.
- The HF repo is **gated** (accept conditions while logged in) and holds only the adapter (`adapter_model.safetensors`
  ~49 MB) + tokenizer; the model card's example loads the base **`meta-llama/Llama-3.2-3B`** (also gated, Meta
  license) with `AutoModelForSequenceClassification`, then `PeftModel.from_pretrained(base, "pangram/editlens_Llama-3.2-3B")`.
- License **CC BY-NC-SA 4.0, non-commercial**. Use it only on the owner's own research papers. Never on Shisso
  commercial content, never shipped in a product, never published as a service. Pangram's page says it is not meant
  for enforcing AI-use policies; we only use it on our own text.
- Output: EditLens predicts how much AI editing a text holds, a score in [0, 1] (paper: classification over n bins of
  the edit magnitude, decoded to a continuous score by a probability-weighted average of the bin values). Pure human
  text sits near 0, AI-edited text high. The paper's ternary labels (human / AI-edited / AI-generated) come from
  calibrated thresholds whose values are **not on the pages we read**.
- Their reported numbers: in-domain ternary macro-F1 0.895 for this 3B vs 0.920 for production Pangram 3.2; RAID
  binary macro-F1 0.930 vs 0.992. So it is close, not equal, to what alphaXiv runs.

Standing rules: no `rm`/`sudo`/interactive (rm only in `~/scratch/WS-162/`); no vast, no arm; nothing posted; never
call the Pangram paid API; the HF token is never printed, logged or committed; commits as Ravindu Somawansa, one line,
no AI mention, no session links; `git pull --rebase` before every push. **Do not edit any paper text in this item.**

## A. Access and environment (step 1, stop early if blocked)

1. Check the HF login on the Orin (`huggingface_hub` `whoami`, no token printed). Try to fetch `config.json` /
   `adapter_config.json` of both repos. If either returns 401/403 (gated, not accepted): `ws set WS-162
   status=waiting-owner`, `needs-from-owner:` "accept the conditions on https://huggingface.co/pangram/editlens_Llama-3.2-3B
   and https://huggingface.co/meta-llama/Llama-3.2-3B with the account the Orin is logged in as, then say WS-162 go
   (~3 min)", add the HUMAN.md line, stop. Do not look for mirrors or re-uploads of either model.
2. Environment: a **separate venv** `~/venvs/editlens` created with `--system-site-packages` so it reuses the
   JetPack CUDA torch already on the Orin; install only `peft`, `transformers`, `accelerate`, `safetensors`
   (+ `huggingface_hub` if missing) into it. Do not touch any other environment (LeRobot, TurboVLA, vla.cpp envs stay
   exactly as they are — the transformers-5 breakage seen in WS-008 is why). Pin what got installed in
   `requirements-editlens.txt`. If the current transformers/peft cannot load the adapter, pin to the versions named in
   the EditLens repo's requirements and note it.
3. Read the EditLens repo README and its inference code / notebook linked from the model card: take from there, not
   from memory, the number of labels of the head, how logits become the continuous score, the input formatting
   (any prompt template, truncation side), and **any published thresholds**. Write what you found, with the file and
   line it came from, in the notes.
4. Load in **fp16 on the GPU**, no quantization (bitsandbytes on aarch64 is not worth the risk for a 3B; ~6.5 GB of
   weights fits the 16 GB Orin NX). Before loading: if free memory is < 9 GB (another job is running — robot pilot,
   a gate run), wait up to 10 min, then stop with a log line; never kill another process. Unload after each run.

## B. `scripts/paper_map.py` (+ `ws paper-map`) — the map

`python3 scripts/paper_map.py <paper-repo-dir | file.md | file.pdf> [--out DIR]`, run with `~/venvs/editlens/bin/python`.

1. **Inputs.** Paper repos are in `~/scratch/paper-repos/*/` (source `paper/DRAFT_4p.src.md` or `paper/DRAFT_4p.md.in`,
   see `journal/workstack/notes/WS-161.md`). Also accept the built PDF (`pdftotext -layout`) so the owner can score
   exactly what is on arXiv / alphaXiv; given both, score both and show them side by side.
2. **Extract prose** with the same stripping as `scripts/prose_check.py` (import its extractor; do not write a second
   one): no front matter, code, math, tables, figure/table captions kept separately, citation keys removed, link
   URLs dropped. Keep section headings and the source line of every paragraph. Drop the reference list.
3. **Chunk** per section, then by paragraphs packed into chunks of ≤ 900 tokens of the model's tokenizer (headroom
   under 1024); a paragraph longer than that is split at sentence boundaries. No chunk crosses a section boundary.
   Chunks under 40 words are merged into their neighbour in the same section (very short input is noisy).
4. **Score** every chunk: the continuous score as the EditLens code computes it, plus the bin probabilities.
   Section score = word-weighted mean of its chunks; also the max chunk. Paper score = word-weighted mean.
5. **Labels.** If step A.3 found Pangram's published thresholds, label each chunk human / AI-edited / AI-generated
   with them and cite where the numbers came from. If not, **do not invent a threshold** (and never set one: bars are
   the owner's). Report the raw score only, next to two reference points scored the same way in this item:
   - human reference: 3 papers from the owner's library `~/workspace/papers/` (see `INDEX.md`) published **before
     2022-11** (pre-ChatGPT), same extraction, ~1 500 words each;
   - AI reference: 3 sections of one of his paper drafts as the oldest commit in its repo has them, *if* the git log
     shows that commit was model-written; otherwise ask the owner in HUMAN.md which text to use and leave this
     reference out of the first run.
   Print the reference medians and ranges in every map so the raw score is readable.
6. **Outputs** in `runs/paper_map/<repo>/<YYYY-MM-DD>/`:
   - `map.md`: one table per paper — section · words · chunks · mean score · max score · first 80 chars of the worst
     chunk · source lines — sorted in paper order, the top 3 sections by mean score in bold; then the reference block;
     then one line: paper mean, % of words in chunks above the human-reference max.
   - `marked.md`: the extracted text, each chunk preceded by `<!-- editlens <score> lines <a>-<b> -->` and, if
     labels exist, the label; the owner reads this to find what to rewrite.
   - `scores.json`: everything (chunks, offsets, bin probs, versions, model ids, runtime).
   - Runtime and peak GPU memory in the JSON and in the notes.
7. A second run on the same paper diffs against the previous map (per-section delta), so after the owner rewrites a
   section he sees whether it moved. That diff is for him; nothing reads it automatically.

## C. Scope fence

The script refuses any path outside `~/scratch/paper-repos/`, `journal/papers/`, `~/workspace/papers/` (reference only)
or an explicit `.pdf` the owner passes, with the message "paper_map is for research papers only (CC BY-NC-SA,
non-commercial)".

## D. Tests

`tests/harness/test_paper_map.py` with a fake model (no GPU, no download): chunker never exceeds 900 tokens and never
crosses a section; short chunks merge; section and paper means are word-weighted; source line mapping is right;
the scope fence refuses a Shisso site path; the diff between two fake runs is per section; no threshold label appears
when none was found. Whole harness suite stays green.

## E. Run it

Run the map on the four paper repos in `~/scratch/paper-repos/` (source and built PDF each), plus the references.
Do not change any paper. In `journal/workstack/notes/WS-162.md`: versions and ids, what A.3 found (score decoding,
thresholds or their absence, with file:line), the reference block, one summary table — repo · words · paper mean ·
worst section · its mean · % words above human-reference max — runtime per paper, peak GPU memory, and links to the
four `map.md` files. Then `ws human` one line: "paper AI map ready: rewrite the bold sections by hand, worst first —
runs/paper_map/" with owner-type review.

## Done when

- Access works (or the item waits on the owner with the two URLs), venv isolated and pinned.
- `scripts/paper_map.py` + `ws paper-map`, scope fence, tests green.
- Four paper maps + references written, notes as in F, HUMAN.md line added, no paper text changed.
- One-line `result:`: `paper AI map: 4 papers scored, worst <repo> <section> <score>; refs human <median> / AI <median or n/a>; <runtime>/paper`.
