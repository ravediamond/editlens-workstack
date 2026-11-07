---
name: workstack
description: Run Ravindu's work stack (journal/workstack/QUEUE.md) through scripts/ws.py. Use when he says "begin / start / run / continue the work stack", "workstack", "/workstack", or any "go … WS-NNN".
---

# Work stack worker (harness v2)

You are Claude Code on the Jetson Orin NX, repo `~/workspace/road-to-robotics`. Ravindu queues items from claude.ai
chat; each points to a self-contained prompt file. You run them top to bottom, keep the queue current, and stop only
when nothing is runnable. The item and its prompt are the whole brief. **Read the queue through `scripts/ws.py`
(`ws` below), never as a file.**

## 1. Start
1. `git pull --rebase` (and in any repo an item names, e.g. `shissorobotics/lego-kitting`). The SessionStart hook has
   printed `ws next`, the rules, the active item's notes and free disk: do not re-read QUEUE.md or AGENTS.md.
2. An item that names a paper: read it from the library first (grep `~/workspace/papers/INDEX.md`; `papers-sync`
   refreshes it, then commit `journal/papers_library/INDEX.md`).
3. One-line plan (what runs now; what waits on Ravindu — `ws table`). Do not wait for approval: start.

## 1b. Parallel items (owner 2026-11-07: up to 3 at once)
Up to **3 items may be `doing` at the same time**. Pick the first three runnable items from `ws next` that touch different
surfaces (different paper repo, different `~/scratch/WS-NNN/`, different `projects/` folder, not both on the GPU or the arm).
Run each as its own subagent (`Agent`, background) whose prompt is the item id, its prompt path and this file's §3–§6; the
main session claims, commits, pushes and reports. Rules: each child commits only its own paths (`git add <paths>`, never
`-A`), `git pull --rebase --autostash` before every push, each uses its own `WS=WS-NNN` and scratch folder, and none touches
another item's notes. `needs` gates (`vast`, `arm`, `rig`, `go`) are checked per item as before; at most one item uses the arm
and at most one the GPU-heavy build/benchmark at a time. `runs/ACTIVE` names only the last claimed item, so a child
must export `WS=WS-NNN` for its own attribution. When one finishes, start the next runnable one: never more than 3 `doing`.

## 2. Runnable
`ws next` applies the rules, top to bottom: status `todo` or `doing` (resume a `doing` item from its notes and log);
every `depends` done (queue or archive); every `needs` met — `offline` always; `vast` / `arm` / `rig` / `go` / `post`
only with the line `go <kind> WS-NNN` (or `go WS-NNN`) in `journal/workstack/GO.txt`; `owner-file:<path>` committed
with no empty field or `___`; `disk: N GB` free. `rig`: Ravindu is at the robot (recording, staging); arm motion still
needs `arm`. A need with a step scope (`arm (trials only)`, `vast (Phase 4)`) is checked when that step is reached:
run everything before it, then `waiting-owner` there. Skipped states: waiting-owner, blocked, parked, proposed, done,
dropped; a typed `go … WS-NNN` makes a skipped item runnable — run it next.

**Proposed items from scheduled runs.** `cron/` jobs (PR digest, paper scan; see `cron/README.md`) run as scheduled
tasks in the Claude app and append items with `status: proposed`; they never reach `todo` on their own. Ravindu
promotes one with `ws set WS-NNN status=todo` or by typing `go WS-NNN`. Items titled `Fetch paper <id> …` follow
`journal/prompts/_templates/fetch_paper.md` (download through `scripts/papers_add.py`, library naming, Drive upload when
`gdrive-rw:` exists).

## 3. Running an item
1. **Claim:** `ws set WS-NNN status=doing` (fills `started:`, marks it active for the hooks); commit
   `workstack: WS-NNN doing`; push.
2. **Do exactly the scope** of the `prompt:` line. Read the prompt; read what it names **by pointer** (the file's
   `## Index`, `sed -n 'a,bp'`, `grep -n`) — never a whole file over 20 KB. The prompt's standing rules apply on top
   of this file; when they differ, the stricter rule wins.
3. **Commits:** after each task, `git -c user.name="Ravindu Somawansa" -c user.email="ravindu.somawansa@gmail.com"
   commit`, one line, **no Co-Authored-By, no session link, no AI mention**; `git pull --rebase` before every push.
4. **Milestones:** `ws log WS-NNN "<what, with its file>"`, commit, push. K3 and K4 items (reviews, patches, memos, drafts): commit at **every** milestone — a folder written, a section finished — so a turn-cap stop loses nothing. Keep `journal/workstack/notes/WS-NNN.md`
   current (numbers with their files, paths created, open question, next step): a resumed session reads it.
5. **End in one state**, commit `workstack: WS-NNN <status>`, push, `ws close WS-NNN`:
   - `done`: `ws set WS-NNN result="<path> — <key number, its n, the verdict wording asked for>"`, then
     `ws set WS-NNN status=done` (runs `ws verify`: refuses a number with no file, or one absent from the cited file). A number tagged `unsourced:` is never cited by a paper draft, a register entry or a post; cite only numbers `ws verify` resolves to a file.
   - `waiting-owner`: a stop point, gate, missing owner file, blank bar or decision; `owner-type=` (review · validate ·
     do · decide) and `needs-from-owner=` **one actionable line**: the verb, the exact file or command, the expected
     time (`review journal/papers/b/DRAFT.md §3, then type "go WS-133" (~20 min)`).
   - `blocked`: an error not fixed in two honest attempts; `owner-type=` too; `blocker=` the error, what you tried,
     what would unblock it (one actionable line with its time).
   Either status (and `proposed`) refreshes `journal/workstack/HUMAN.md` in the same commit.
6. **Send the one-paragraph result** as soon as it exists, then the next item. Do not stop after one item.
7. **Book:** after a commit under `journal/book/`, use the `book-epub` skill.
8. **Papers live in their own repos** (`ravediamond/paper-*`): edit there, `make check` passes, push, record the
   paper-repo commit in the `log:` line. `journal/papers/<slug>/` keeps memos, reviews, history.
9. **Memory cap:** the Orin has 16 GB shared by CPU and GPU. Run any torch / training / build job through
   `scripts/memcap.sh [-m 11G] <cmd>` (cgroup cap, no swap, first OOM victim) so an OOM kills the job and not remote
   control, sshd or Wi-Fi; the hook blocks it otherwise. A job that hits the cap is not retried bigger: shrink it or
   go `needs: vast`.
10. **vast:** before launching, print the offer, $/h and worst-case cost; the item's cap applies.
11. **Board:** the board in Shisso-Site-Data is mirrored by `ws set`; an item that analyses a paper not named in its
    title adds `papers:` before claiming.

## 4. Never
- Never write or change a bar, protocol field, decision rule or success criterion. Missing → `waiting-owner`,
  `needs-from-owner: bar for <step>`. Anything decided after seeing data is labelled **exploratory**.
- Never spend on vast, move the arm, or post outside Ravindu's repos (issues, PRs, comments, Hub discussions) without
  the matching go. Drafts only.
- Never read a status, decision or go from Todoist; QUEUE.md, HUMAN.md and GO.txt are the only truth. Never touch a Todoist
  project other than the board.
- Never reorder, delete or rewrite other items; append follow-ups at the end of `## Queue` with `status: proposed`.
- No `rm` (except inside `~/scratch/WS-NNN/`, logged by the hook), no `sudo` (power commands are the owner's), no
  interactive commands. Discard with `mv` to an `archive/` folder.
- Never touch protected environments (`~/venvs/wm`, `lerobot-jetson:rc` / `:public`, `~/gate/lerobot`, the TurboVLA
  plugin pin) unless the item says so. AGENTS.md §1: never imitate failed actions; judge only at rest; sentinel B10.
The hooks enforce the mechanical half of this list; the judgement half is yours.

## 5. Context (every token in the window is re-read by every later call — MEASURE_2026-11-01.md)
1. **Pointers, not files**: the section a step needs, when it needs it; never the same range twice.
2. **Write once, never echo back** (measured: 31 % of context was the worker's own heredocs and file bodies): write a
   file with the Write tool once; never `cat` or Read a file you just wrote; reuse the scripts under `scripts/` (and
   the project's own) instead of re-writing them inline; no long heredocs.
3. **Long output to disk**: tests, installs, docker, training, `gh … --json`, tegrastats through
   `scripts/cc/cc.py <mode> --ws WS-NNN -- <cmd>` (full log in `journal/workstack/runs/WS-NNN/`), or `| tail -n 40`.
4. **Images only when the step needs the pixels** (~2.5k tokens each, carried).
5. **Item boundary = context boundary**: after an item, `ws handoff WS-NNN` and suggest `/compact` to Ravindu (or
   the dispatcher starts a fresh child).
6. **Facts from files**: datasets, label counts, revisions, rig versions from `data/FACTS.json` or the file itself,
   cited by key or path — never typed from a prompt or from memory.
7. **Brevity**: results as tables; do not restate the prompt; no narration between tool calls; one paragraph per item.
8. **Numbers in a protocol, result line or README are commanded**: any count, default, label total or constant that
   goes into one is produced by a command run in the same turn (grep of the code or a count over the file) and
   written with its path. Numbers from earlier notes or memory are not typed.

## 6. Disk
Temporaries only under `~/scratch/WS-NNN/` (`scratch_gb:` in the item, default 5). Below the floor (`disk_floor_gb` in `journal/harness/BUDGET.json`: 6 GB while WS-090 is open, then 10 GB) the hook blocks
downloads, pulls, builds and copies: free your scratch or go `waiting-owner` with the size needed. At `done`, free
the scratch unless the item keeps a named artefact (name it and its size).

## 7. Session commands from Ravindu
| he types | you do |
|---|---|
| `go vast …` / `go arm …` / `go rig …` / `go post …` / `go WS-NNN` | append the line to GO.txt, commit, run the item next |
| `skip WS-NNN` | leave it, continue |
| `park WS-NNN` | `ws set WS-NNN status=parked` |
| `stop` | finish the commit, `ws log`, push, report |
| `human` | `ws human`; relay the screen as printed |
| `done H-NNN` | `ws human done H-NNN` |
| `improve` / `improve dry` | `ws improve` / `ws improve --dry`; relay the one screen as printed (journal/harness/README.md) |
| `board` | `ws todoist-sync` (the cron tick is `ws todoist-watch`); relay its one line |

## 8. Concurrency
QUEUE.md is also edited from chat; `ws` pulls before every write. On a conflict keep both sides and re-apply only your
own field changes; never drop someone else's item. Done items live in `ARCHIVE.md` (`ws archive`).

## 9. End of run
Nothing runnable, or `stop`: update the `Last run` line, push, run `ws todoist-sync`, print `ws table` (WS · status · title · the exact command
or file needed from Ravindu) and free disk; then `ws human --write` (commit `HUMAN.md` if changed) and print its
`--short` screen after the table.

## 10. Helpers
Skills: `frozen-protocol` (writing a PROTOCOL.md), `gate-run` (running a frozen one), `book-epub`. Subagents
(`.claude/agents/`): `reader`, `number-checker`, `protocol-readback`, `site-checker` — for read-heavy steps that
return little.

## 11. Prose for readers (WS-158)
Every text people will read (commit messages, PR / issue / release titles and bodies, Hub posts, READMEs, docs, papers, posts, book; never code)
passes the prose check before it leaves the Orin: the hooks check commit messages and posts when they are written, the Stop hook and
`ws verify` check changed prose files (`ws prose-check FILE`), 3 rounds per file. `scripts/prose_allow.txt` is the owner's; never edit it.
- Fix a `[MUST]` line by saying something more specific (a number from a file with its path, a name, a concrete
  condition), or by cutting the sentence. Never by swapping in a synonym of the flagged phrase.
- Never change a number, claim, bar, result or citation to pass; never add a `slopscore-disable` comment (only the owner does).
- `[consider]` lines (lmscan) are optional: change them only if the sentence is also vague.
- After the third failed round stop rewriting; the owner reviews `runs/prose/<slug>.review.md`.
- Paper text is written under the `paper-writing` skill (`journal/papers/ai-map/WRITING_RULES.md`), read before generating it. After a section is drafted the `paper-polish` skill runs the paragraph-level EditLens loop on it (`ws paper-polish`); the paper-repo commit and the mean before and after go in the `log:` line.

## 12. Robot sessions: the agent pilots (WS-159)
The owner sets the scene and gives feedback in plain words; nothing waits for Enter or space. One call per trial:
`scripts/robot_pilot.py next --out DIR --ws WS-NNN --feedback "<the owner's sentence about the last trial>"` (needs the owner's `go arm WS-NNN`).
It labels the last trial, starts the server if needed, waits for both bowls within 1 cm of the layout and a still scene (or says what to move), runs the
trial between two rest moves and prints one line. `robot_pilot.py check --layout N` reads the placement without the arm; `stop` ends a trial and rests the arm.
