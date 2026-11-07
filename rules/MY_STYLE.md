# Ravindu's writing style, in paper mode

Extracted from two posts: "How Prompt Caching Works" (Medium / metadocs.co, 2024-10-17) and "The Real Reason Enterprise Agents Are So Hard (And It's Not the AI)" (Towards AI, 2025-10-06). Only the parts that read as written by hand count: openings, transitions, asides, lived details. Use with WRITING_RULES.md; where the two disagree, the resolution is stated below.

## The signature: the simple thing first

Both posts argue that the plain solution is underrated. Prompt caching "is not just classic caching". In the agents post, a whole section is a "don't" (classic code, a classifier or a few LLM calls often beat an agent), and an aside asks "(if you even need this level of agentic)". This is also the thesis of the four papers: copy-last, the commanded joints, episode length or a colour judge often beat the learned method. Say it in that voice, as a practitioner's warning, not as a gotcha.

## What the style is

1. **Open with why it matters and the wrong assumption.** "why it is not just classic caching"; "the AI is not the hardest part." The first lines name what the reader probably believes and say it is wrong.
2. **Contrast with what the reader expects.** Define the thing against the familiar one before defining it on its own.
3. **"So" as the joint of the argument.** "So let's explain how a LLM handles inputs and then see where prompt caching happens." One short sentence says what must be understood first.
4. **Honest parentheses.** They carry a reason or an admission: "(so with different results)", "(because the embedding vectors will be still the same)", "(and completely avoided)", "(sometimes the hardest part)", "(they don't have time !)".
5. **A lived detail as evidence.** "you will need 3 days just to understand what it is being used for"; a quoted aside from a meeting: "Oh, but for client X we do it differently." One concrete cost or scene is worth a paragraph of general claims.
6. **One running example carried through.** "The cat is on the mat" is tokenized, attended over, then cached.
7. **Questions as the test.** Evaluation is written as the questions it must answer: "Did the agent complete the workflow as defined?", "Did we catch all the process in errors?"
8. **A judgement at the end of a sentence.** "...which is the real starting point of the model." A short opinion, not a summary.
9. **Mechanisms as numbered steps.** Dot product, softmax, weighted sum: each step named, one or two sentences each.
10. **A practical verdict.** "ideal for prompts where large, static content is reused"; "agents are best reserved for messy, multi-step, dynamic workflows." The end says what to use when.
11. **Plain words, "we", simple on purpose.**

## Paper-mode filter

**Update 2026-11-05 (owner):** rules 60, 61, 66 and 67 are deleted and rule 78 (de-polish) added. In papers, drop the contrast opening, the "So" joint, the end-of-sentence judgement and the practical verdict (except one practical sentence in the conclusion). Keep the lived details, honest parentheses that give a reason, the running example and plain words.

| keep | how it looks in a paper |
|---|---|
| the signature | The introduction names the simple baseline as a serious competitor from the first paragraph, and the conclusion says when the learned method is not worth it on this rig. |
| 1. why + wrong assumption first | The introduction opens with the belief the paper tests (the latent is just pose; tricks transfer to any GPU; a reward model beats a trivial signal), then why it matters on a cheap rig. |
| 2. contrast with the familiar | Only where the content is a contrast (encoder vs predictor, desktop vs edge, time limit vs operator stop). Rule 18 still holds: not as a habit. |
| 3. "So" joint | One per section at most, as logic ("So the question is which part of the chunk a trick touches."), never as a table of contents. Rule 27 forbids "In this section we will"; a "so" sentence that states what must be true first is allowed. |
| 4. honest parentheses | Keep. They are the best carrier of reasons and admissions (rules 3 and 4). Reasons only; numbers go to tables. |
| 5. lived detail | One per section where the record has one: the strict=False load, the scores left on another machine, the three machines for one number, the $6 re-score. Never invented (rule 4). |
| 6. running example | One per paper: one episode, one anchor or one chunk followed through method, result and limitation. |
| 7. questions as the test | Think in questions, write in statements: each gate opens with the test it runs, as a declarative sentence ("The test is whether length still separates the outcomes before the timeout."). No questions in the prose or headings (rule 65, owner decision 2026-11-05). |
| 8. end-of-sentence judgement | At most one per paragraph, only where it is your view. |
| 9. numbered mechanism steps | For procedures only (rule 10). |
| 10. practical verdict | Conclusions and "what transfers" sections end with what a reader with the same rig should do. |
| 11. plain words, "we" | Keep. "I" is also correct for a single author; pick one per paper. |

| drop | why |
|---|---|
| "let's get to it!", "Let's break these down", "So let's recap", "I hope you really loved this post", "cool", "deep dive" | blog register; a recap is a restatement (rule 19) |
| "Here's the truth", "here's the kicker", "sink or swim", "prototype purgatory", "while you sip a latte", "shiny demos", "The lesson? ..." | stock phrases that read as model text in the 2025 post, not as you |
| "four walls", "the big three", labels like "(the what) / (the how) / (the proof)" | enumerated frames (rules 7 and 18); the 2025 post even lost count (four walls, "the big three", the fourth called "the third") |
| questions in the prose or as headings | owner decision 2026-11-05: a paper answers, it does not ask (rule 65) |
| "we will try to be as simple as possible" | a paper shows simplicity, it does not promise it |
| the language slips ("a LLM", "does ... happens", "pourcentage", a space before "?" and "!") | fix them; never add errors to look human |
| the definition bullets of the 2024 post ("Query (Q) — Represents the 'question'...") and its "Whether you use..." close | model-like, unlike the rest of the post |

## Example (vla-edge-inference, introduction opening, numbers unchanged)

Before (EditLens 0.338):
> Papers that speed up or smooth action chunking report their latencies on desktop and data-centre GPUs (RTX 4090, A100, H100, RTX 5090). There a chunk costs tens of milliseconds, and spare compute can hide an extra pass. The robots people can buy run their policies on edge GPUs.

After (signature, traits 1, 3, 4):
> With several training-free chunking tricks published this year for flow-matching VLAs, it is tempting to think they make a policy faster or smoother on any robot. They are measured on desktop and data-centre GPUs (RTX 4090, A100, H100, RTX 5090), where a chunk costs tens of milliseconds and spare compute can hide an extra pass. A robot people can buy runs its policy on an edge GPU, where most of the chunk goes to a part the tricks never touch (the vision encoder). So the useful question is not whether a trick works, but how much of it is left on that board.
