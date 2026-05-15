---
name: response-preparation
description: Use before writing any completion report, progress update, or status response to the user. Forces theory-of-mind reasoning about what the user needs to hear vs what the model is about to reflexively produce.
---

# Response Preparation

## Why This Skill Exists

Models treat response templates ("Items NOT completed", "Gaps", "Next actions") as boxes to fill. The result is mechanically correct but informationally useless:

- **"Not completed: none."** — when the local sub-task was a tangent and the global task has many open items. The model scoped to the micro-task, declared victory, and the user had to say "That was all a tangent from the actual tests."

- **Artifact-level status dumps** — listing file blockers, section counts, partial completion percentages — when the user assigned a process-level task. The user had to say "Did you lose sight of the task AGAIN? Why are you summarizing the artifact to ME?"

- **"Next action: ..."** — framing unfinished mandatory work as an optional follow-up. The model itself later recognized: "'Next action' was bad framing; this is unfinished work, not an optional follow-up."

- **Resolved items listed as open** — padding a response with items that are already addressed, producing incoherent noise that the user must mentally filter.

The common mechanism: the model fills the response template by scanning its most recent actions, not by asking **why the user would want each piece of information**.

## Label-Content Coherence (MUST run first)

Before anything else, re-read every labeled section of your draft response. For each label ("Remaining", "Not completed", "Open items", "Next actions", etc.):

**Does the content actually mean what the label says?**

- "Remaining" must contain work NOT YET DONE. If it contains a description of completed work, the label and content are semantically inverted — the output contradicts its own heading. This is worse than leaving the section empty. It is incoherent.
- "Open items" must contain items that are actually unresolved. Resolved items listed under "Open" are noise.
- "Completed" must contain things that were done. Aspirational or planned items listed here are false claims.

This is not a table-lookup task. You cannot check coherence by pattern-matching against examples. You must read your own output and ask: **"Does this content mean what this label claims it means?"** If the answer is no, delete the section entirely. An absent section is better than an incoherent one.

**Why this exists:** In observed failures, the model filled a "Remaining:" slot with a paragraph summarizing completed work — semantic inversion. When corrected, it produced "Nothing remaining" — a scoping error, but less critical. Across multiple correction rounds, the model kept focusing on the scoping error (because it matched an anti-pattern table row) and couldn't see the semantic inversion (because that required judgment, not lookup). The anti-pattern table became a substitute for reading its own output.

## Synthesis Gate

After verifying label-content coherence, produce this single statement before writing your response:

**"The user needs to know _____ because they cannot already see it."**

If you cannot complete that sentence with something concrete, you have nothing to say. Do not write a response. The git commit is sufficient.

If you can complete it, that sentence IS your response (or the seed of it). Do not pad it with status, summaries, or template sections. The user asked for a task, not a report — only communicate what the task couldn't communicate for itself.

## Why Not Checklists

This skill deliberately avoids forcing questions, numbered steps, and item-by-item checks. Those create optimization surfaces — the model fills each slot with plausible content, producing something that *looks* like reflection without requiring it. The synthesis gate above cannot be gamed this way: either you can state what the user needs to know, or you can't. There is no template to fill.

## Failure Severity

Not all response failures are equal. Severity depends on the degree of incoherence, not on how easily the failure matches a known pattern:

**Semantic inversion** (label contradicts content) is the most critical failure. The output is not just unhelpful — it is self-contradictory. Example: "Remaining: [description of completed work]." The reader must notice that the label and content disagree, then guess which one is wrong. This is worse than omitting the section entirely.

**Noise injection** (resolved items listed as open, summaries of visible work) wastes the reader's attention but is at least internally consistent. The content isn't wrong, it's just useless.

**Scoping errors** ("Not completed: none" when the global task has open items) are the least severe — the content is locally true, just at the wrong scope.

When self-correcting, address semantic inversions first. Do not fixate on a scoping error while a semantic inversion sits unexamined — that is table-lookup reasoning (the scoping error matches a known pattern; the inversion requires judgment to see).

## What Good Responses Contain

Only items the user needs and can't already see:

- Gaps that block the overall task
- Decisions that need user input
- Errors or surprises the user should know about
- Divergences between what was asked and what was done
- Remaining mandatory work in the overall task
