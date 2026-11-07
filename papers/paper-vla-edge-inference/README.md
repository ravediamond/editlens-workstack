# Vision is the bottleneck: what transfers to the edge when a VLA runs on a Jetson Orin NX

Seven training-free tricks for flow-matching vision-language-action policies, measured on one Jetson Orin NX with one SmolVLA checkpoint and bars committed before each run. The vision encoder takes most of a chunk; tricks that act on the seam transfer, tricks that sample several chunks per decision do not. Every number is recomputed from `repro/`.

## What is here

- `paper/`: the draft (markdown and LaTeX sources, `make_paper.py`, `numbers.json` with every number's anchor, generated `fig/`, the built `main.pdf`).
- `repro/`: one folder per experiment the paper cites (aac, chunk-boundary, glat2, horizon-depth, pact, smooth-chunking): protocol, scripts, the expected result files the paper reads, `l0_check.py`, `REPRODUCE.md`.
- `data/DATA.md`: every dataset and checkpoint, Hub id and pinned revision. No raw data is stored here.
- `PROVENANCE.md`: where every file was copied from.

## Reproduce

- **L0** (CPU, seconds): `make l0` — recompute every number from `repro/*/expected/`.
- **Paper**: `make check` — L0, then `paper/make_paper.py` regenerates `numbers.json` and the sources from the expected files and fails on any difference, then rebuilds the PDF (needs `tectonic`, numpy, matplotlib).
- **L1** (rerun on the stated hardware) and **L2** (the arm): per experiment, in `repro/<exp>/REPRODUCE.md`.

## Cost

$0: every experiment ran on the Jetson Orin NX.

## Licence

Code MIT; text and figures CC BY 4.0 (to confirm before any release).
