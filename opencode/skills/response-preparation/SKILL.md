---
name: response-preparation
description: Use before writing any completion report, progress update, or status response to the user. 
---
# Response Preparation

## Why This Skill Exists

Forces theory-of-mind reasoning about what the user needs to hear vs what the you are
about to reflexively produce.
Models treat response templates ("Items NOT completed", “Gaps”, “Next actions”) as boxes
to fill. The result is mechanically correct but informationally useless:

- **“Not completed: none.”** — when the local sub-task was a tangent and the global task
  has many open items.
  The model scoped to the micro-task, declared victory, and the user had to say “That
  was all a tangent from the actual tests.”

- **Artifact-level status dumps** — listing file blockers, section counts, partial
  completion percentages — when the user assigned a process-level task.

- **“Next action: ...”** — framing unfinished mandatory work as an optional follow-up.

- **Resolved items listed as open** — padding a response with items that are already
  addressed, producing incoherent noise that the user must mentally filter.

The common mechanism: the model fills the response template by scanning its most recent
actions, not by asking **why the user would want each piece of information**.

## Label-Content Coherence (MUST run first)

Before anything else, re-read every labeled section of your draft response.
For each label ("Remaining", “Not completed”, “Open items”, “Next actions”, etc.):

**Does the content actually mean what the label says?**

- “Remaining” must contain work NOT YET DONE. If it contains a description of completed
  work, the label and content are semantically inverted — the output contradicts its own
  heading. This is worse than leaving the section empty.
  It is incoherent.

- “Open items” must contain items that are actually unresolved.
  Resolved items listed under “Open” are noise.
  Do not artificially restrict this to “locally” open items from only the last turn(s),
  which obfuscates higher-order global unfinished tasks.

- “Completed” must contain things that were done.
  Aspirational or planned items listed here are false claims.

This is not a table-lookup task.
You cannot check coherence by pattern-matching against examples.
You must read your own output and ask: **“Does this content mean what this label claims
it means?”** If the answer is no, delete the section entirely.
An absent section is better than an incoherent one.

## Synthesis Gate

After verifying label-content coherence, produce this single statement before writing
your response:

**“The user needs to know _____ because they cannot already see it.”**

If you cannot complete that sentence with something concrete, you have nothing to say.
Do not write a response.
The git commit is sufficient.

If you can complete it, that sentence IS your response (or the seed of it).
Do not pad it with status, summaries, or template sections.
The user asked for a task, not a report — only communicate what the task couldn’t
communicate for itself.

## Frame Fidelity Gate

Before answering, identify the object the user asked you to judge or transform.

Use this sentence internally:

**“The user asked about _____; the tempting adjacent object is _____; my response must
stay on _____.”**

If the user asked for a case study, postmortem, review, critique, or failure analysis,
do not answer by summarizing the object-level problem inside the source. The source
material is evidence. The requested output is the judgment about that evidence.

When the evidence is a correction sequence, the user usually needs the sequence-level
pattern: what each correction had to remove, which prior assumption survived too long,
and where the agent should have reset the frame. A final solution summary is not a
substitute for that analysis.

## Why Not Checklists

This skill deliberately avoids forcing questions, numbered steps, and item-by-item
checks. Those create optimization surfaces — the model fills each slot with plausible
content, producing something that *looks* like reflection without requiring it.
The synthesis gate above cannot be gamed this way: either you can state what the user
needs to know, or you can’t. There is no template to fill.

## Failure Severity

Not all response failures are equal.
Severity depends on the degree of incoherence, not on how easily the failure matches a
known pattern:

**Semantic inversion** (label contradicts content) is the most critical failure.
The output is not just unhelpful — it is self-contradictory.
Example: “Remaining: [description of completed work].” The reader must notice that the
label and content disagree, then guess which one is wrong.
This is worse than omitting the section entirely.

**Noise injection** (resolved items listed as open, summaries of visible work) wastes
the reader’s attention but is at least internally consistent.
The content isn’t wrong, it’s just useless.

**Scoping errors** ("Not completed: none" when the global task has open items) are the
least severe — the content is locally true, just at the wrong scope.

When self-correcting, address semantic inversions first.
Do not fixate on a scoping error while a semantic inversion sits unexamined — that is
table-lookup reasoning (the scoping error matches a known pattern; the inversion
requires judgment to see).

## What Good Responses Contain

Only items the user needs and can’t already see:

- Gaps that block the overall task

- Decisions that need user input

- Errors or surprises the user should know about

- Divergences between what was asked and what was done

- Remaining mandatory work in the overall task
