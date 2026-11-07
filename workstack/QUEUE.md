# Work stack

Items for an AI agent working in this repository only. Rules: `../AGENTS.md`. Workflow and background: `../docs/WORKFLOW.md`.

**To run it:** open an agent session in the repository root and say "begin the work stack". The agent takes the first runnable item.
**Gates** are lines the owner types in `GO.txt`: `go WS-NNN`, `go prod WS-NNN` (the paid production API), `go gpu WS-NNN`.
**Status:** todo · doing · waiting-owner · blocked · done · parked · proposed · dropped.
**Needs:** `offline` (always met) · `gpu` (a CUDA machine with access to the gated model, about 9 GB free) · `go` (a `go WS-NNN` line) · `go prod`.
**Fields:** status, needs, prompt, depends, added, why; filled by the agent: started, log, result, needs-from-owner, owner-type, blocker.
**To add an item (owner or a chat assistant):** write `prompts/WS-NNN.md` (self-contained, nothing left blank for the owner to fill in),
append a block at the end of `## Queue` with the next number, commit `workstack: push WS-NNN <title>`.

## Queue

### WS-001 · Confirm or change the bars of the human-dose protocol (carried from WS-166, step 0)
- status: waiting-owner
- owner-type: decide
- needs: go
- prompt: `prompts/WS-001.md`
- depends: —
- added: 2026-11-07
- needs-from-owner: read `editlens-paper/repro/human-dose/PROTOCOL.md` §3 (bin edges) and §5 (B1 to B4, the production gate), write your changes or "as proposed" in `workstack/notes/WS-001-owner.md`, then type `go WS-001` in GO.txt (~20 min)
- why: the bars were drafted by an assistant on 2026-11-06; a bar the owner did not give is not a bar, and no number may be read before the protocol is frozen.

### WS-002 · Freeze the protocol, set up the pipeline, score the baselines and the AI direction
- status: todo
- owner-type: —
- needs: gpu, go
- prompt: `prompts/WS-002.md`
- depends: WS-001
- added: 2026-11-07
- why: the human-dose study cannot start until the protocol is frozen and the baselines and AI-direction rows exist.

### WS-003 · One hand-edit batch through the pipeline (repeatable)
- status: parked
- needs: gpu, go
- prompt: `prompts/WS-003.md`
- depends: WS-002
- added: 2026-11-07
- why: after each editing session of the owner, add the new versions, score them and report coverage. Re-park after each run; the owner types `go WS-003` again.

### WS-004 · Audit the EditLens paper against its own numbers and write the section skeleton
- status: todo
- owner-type: review
- needs: offline
- prompt: `prompts/WS-004.md`
- depends: —
- added: 2026-11-07
- why: the paper is being reframed; before the owner rewrites it by hand he needs to know which statements the stored numbers still support, and what each section has to say.

### WS-005 · Audit the four papers: numbers, claims about own role, train/eval relation, source twins
- status: todo
- owner-type: review
- needs: offline
- prompt: `prompts/WS-005.md`
- depends: —
- added: 2026-11-07
- why: rules 30, 50, 51 and 57 of the writing rules are about facts that drift; a check against the stored files is cheap and the owner should fix what it finds himself.

### WS-006 · Score map of the current drafts of the four papers and of the EditLens paper
- status: todo
- owner-type: —
- needs: gpu
- prompt: `prompts/WS-006.md`
- depends: —
- added: 2026-11-07
- why: the register, VLA and reward papers changed after the last map (pass report §7, §9); the new map is the "before" of the owner's hand edits and a pointer to paragraphs to reread. No text is changed.

### WS-007 · Production Pangram API run, once, under the gate
- status: parked
- needs: go prod
- prompt: `prompts/WS-007.md`
- depends: WS-003
- added: 2026-11-07
- why: the study's headline should use the production detector if the local curve is readable; cap $25, one run.
