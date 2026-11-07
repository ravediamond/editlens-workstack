# editlens-workstack

One repository for one workflow: **improving four research papers, checking them with the open EditLens model, the writing rules that
came out of it, and the paper about the EditLens experiments.** It is built so that an AI agent can continue the work using this repository
and nothing else.

Start with [`AGENTS.md`](AGENTS.md) (rules and layout), then [`docs/WORKFLOW.md`](docs/WORKFLOW.md) (what was done and the current direction),
then [`workstack/QUEUE.md`](workstack/QUEUE.md) (what to do next).

```
workstack/      the queue, the owner's gates, one prompt per item
papers/         paper-jepa-world-model, paper-register-reproducibility, paper-reward-models-stopping-rule, paper-vla-edge-inference
editlens-paper/ the paper about the detector, and repro/<experiment>/ for each experiment (repro/human-dose/ is the open study)
tools/          score map, scoring server, prose gate, sync of the original repositories
rules/          writing rules, voice, lexicon
results/        pass report with every number, score maps of each run
docs/           workflow, results, the original prompts and skills
originals/      copies of the authors' EditLens code and data (the paper PDF goes here)
```

`make check` recomputes every stored number and regenerates every paper from its rows on a CPU, with no model and no network.
Scoring paragraphs needs `pangram/editlens_Llama-3.2-3B` (CC BY-NC-SA 4.0, non-commercial, access granted per Hugging Face account) on
`meta-llama/Llama-3.2-3B` and a CUDA GPU with about 9 GB free.

The score of the open model estimates how much AI editing a paragraph seems to hold. It does not say who wrote it. The four papers were
drafted with an AI assistant, and each says so.

Papers and results here are copies of the author's repositories (`papers/SYNC.json` gives the commit each was copied from). The author's
hand edits are replayed commit by commit with `tools/sync_papers.py`.
