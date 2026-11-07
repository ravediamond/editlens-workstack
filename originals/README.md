# Originals (copies)

Copies of material this work is built on. The real ones stay where they are; nothing here is edited.

| what | copy here | where the original is | retrieved |
|---|---|---|---|
| EditLens paper: Thai, Emi, Masrour, Iyyer, "EditLens: Quantifying the Extent of AI Editing in Text" (ICLR 2026) | not stored (see below) | https://arxiv.org/abs/2510.03154 | — |
| the authors' code, configs and part of their data | `pangramlabs-EditLens/` | https://github.com/pangramlabs/EditLens (branch `main`) | 2026-11-07 |
| the open model (adapter, gated) | not stored | https://huggingface.co/pangram/editlens_Llama-3.2-3B (base `meta-llama/Llama-3.2-3B`) | — |
| the dataset | `pangramlabs-EditLens/data/{test,human_detectors,nonnative_english}.csv` | https://huggingface.co/datasets/pangram/editlens_iclr | 2026-11-07 |
| the owner's four papers before the 2026-11-05 rewrite | `../editlens-paper/repro/rewrite-loop/sources/*.orig.md` | the owner's repositories | 2026-11-05 |
| the original skills and prompts of the harness this came out of | `../docs/original-skills/`, `../docs/original-prompts/` | the owner's road-to-robotics repository | 2026-11-07 |

**The EditLens paper PDF is not in this folder.** arXiv was not reachable from the session that built this repository. Put the PDF at
`originals/EditLens-2510.03154.pdf` (arXiv, version 1 or 2) and commit it.

**What is in `pangramlabs-EditLens/`.** `scripts/inference.py` (how the score is decoded), `scripts/preprocess.py` (`clean_text`),
`scripts/train.py` (the `NormedLinear` head), `scripts/scoring/` (the two magnitude metrics that `editlens-paper/repro/human-dose/scripts/magnitude.py`
vendors), `scripts/eval/` (the ternary and binary evaluation, the threshold calibration), `configs/` (the `lo_threshold` 0.03 and `hi_threshold`
0.15 bucket edges), and three data files: `data/test.csv` (6,115 rows, each with its `source_text`; columns include `text`, `cosine_score`, `soft_ngrams_score`, `label` (values -1, 0, 1,
about 2,040 each) and the scores of other detectors, among them the authors' own Llama-3.2-3B and RoBERTa EditLens scores), `data/human_detectors.csv` (300 rows)
and `data/nonnative_english.csv` (91 rows, with the same score columns).
Not copied for size: `data/val.csv` (9.7 MB), `data/test_enron.csv` (15.6 MB), `data/test_llama.csv` (24.9 MB), `data/raid_10k.csv` (18.3 MB);
they are in the same GitHub folder.

**Licence.** The authors' repository is licensed CC BY-NC-SA 4.0 (their README): non-commercial, attribution, share-alike. Everything in
`pangramlabs-EditLens/` stays under that licence and under their citation:

```
@misc{thai2025editlensquantifyingextentai,
  title={EditLens: Quantifying the Extent of AI Editing in Text},
  author={Katherine Thai and Bradley Emi and Elyas Masrour and Mohit Iyyer},
  year={2025}, eprint={2510.03154}, archivePrefix={arXiv}, primaryClass={cs.CL}, url={https://arxiv.org/abs/2510.03154}}
```
