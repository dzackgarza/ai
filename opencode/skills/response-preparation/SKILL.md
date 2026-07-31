---
name: response-preparation
description: Use when preparing any end-of-turn response after substantive or multi-step work, or any completion, progress, status, handoff, or remaining-work synthesis. Continue safe live work instead of reporting it; when a response is due, emit gaps and exceptions. Skip direct answers, obvious corrections, and trivial edit acknowledgments.
---
# Response Preparation

## Why This Skill Exists

Forces theory-of-mind reasoning about what the user needs to hear vs what you are
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

## Success Is the Expected Outcome

Treat successful execution as the expected outcome of a turn. It has no reporting value
by itself. The commit, diff, test artifact, or requested deliverable already records it.

A response after substantive work is an exception report, not a retrospective. Completed
steps, verification transcripts, baseline counts, and explanations of why a finished fix
was correct are inadmissible unless omitting one would make a gap, blocker, surprise,
divergence, or required decision unintelligible. When such context is necessary, use the
shortest clause that makes the exception clear.

## Continue Before Reporting

Before drafting, determine whether safe in-scope work remains on the strongest live goal
and whether user input is actually required. If work remains and you can proceed, continue
working. A progress report is not continuation; it yields control and makes unfinished
work depend on another user prompt.

End the work phase only when the requested goal is complete, a concrete blocker requires
new authority or information, the user explicitly requested a status response, or the
assigned operation is an active wait or monitor. A local fix, green test, baseline match,
checkpoint, or newly explained defect is not an end condition while mandatory work
remains.

## Preserve the Live Queue

Prose does not preserve an obligation. Do not demote discovered work into a final
"not touched" paragraph, compressed subordinate clause, or optional "next steps" list.
Resolve it, continue it, place it in its canonical durable owner when another artifact
owns it, or report the exact blocker that prevents action.

"Pre-existing" describes provenance, not disposition. "Back to baseline" describes a
comparison, not completion. Never make the user mine a retrospective, reconstruct the
work graph, and re-issue work that remained executable.

## Label-Content Coherence

After deciding that a response is due, re-read every labeled section of your draft response.
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

## Gap-First Synthesis Gate

Before writing, ask internally:

**“Can I continue the strongest live goal without user input?”**

If yes, continue the work and do not draft a response yet. Do not redefine the strongest
live goal around the most recent local fix.

When a response is due, complete this statement:

**“The user needs to know _____ because it changes _____.”**

The first blank should normally name a gap, blocker, surprise, divergence, or decision.
The second should name the affected action, expectation, proof burden, or required user
choice. If the only completion is a description of what you did, delete it. If the task
is complete and no exception exists, point to the commit or result in one line.

Every remaining sentence must support that statement. Do not pad it with status,
summaries, verification output, or template sections. The user assigned work, not a
request for evidence that activity occurred.

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

## Positive Artifact Gate

Do not preserve correction history inside the artifact or answer unless the user asked
for the history. A final plan, spec, recommendation, or implementation note should state
what to do, not carry a scar tissue list of rejected alternatives.

If your draft contains "do not" bullets, caveats, or disclaimers that exist only because
earlier turns were wrong, rewrite the artifact as a positive contract. Keep negative
rules only when they are durable constraints a future worker must obey.

If a correction stripped the answer down to a simple solution, check that the response
still contains the concrete boundary the user needs: where action happens, what data
moves, what owns the result, and how correctness would be observed.

## Why Not Checklists

This skill deliberately avoids forcing questions, numbered steps, and item-by-item
checks. Those create optimization surfaces — the model fills each slot with plausible
content, producing something that *looks* like reflection without requiring it.
The synthesis gate above cannot be gamed this way: either you can state what the user
needs to know, or you can’t. There is no template to fill.

## Failure Severity

Judge response failures by the work they displace, not by whether the prose is accurate.

**Execution displacement** is most severe. The agent stops to narrate a local success
while safe mandatory work remains, turning an executable obligation into a future user
prompt.

**Queue destruction** follows. Open work is buried in prose without a durable owner,
priority, dependency, or continuation boundary, so later turns must rediscover it or lose
it.

**Semantic inversion** occurs when a label contradicts its content, such as completed
work under “Remaining.” The reader must detect the contradiction and guess which part is
wrong.

**Noise injection** includes visible-work summaries, raw verification output, resolved
items listed as open, and causal defenses of completed work. Accurate noise still spends
the attention needed to find live gaps.

**Scoping errors** declare a local subtask complete while the strongest live goal remains
open. A baseline match or “pre-existing” classification often performs this substitution.

Correct the trajectory before polishing the report: resume executable work, restore the
live queue to its durable owner, then remove retrospective prose.

## What Responses May Contain

Only items the user needs and can’t already see:

- Gaps that block the overall task

- Decisions that need user input

- Errors or surprises the user should know about

- Divergences between what was asked and what was done

- Remaining mandatory work in the overall task

## Content to Delete

Unless the user explicitly requested it or it is essential to an exception, delete:

- chronological “what changed and why” narration;

- successful verification commands, raw output, and example matrices or objects;

- baseline or test-count recaps used as closure;

- explanations that defend why the completed approach is now correct;

- file-by-file inventories of successful edits;

- “not touched” residue presented after the agent could have continued working.

Do not reward a discover-fix-explain episode with a report merely because it forms a
coherent story. Coherence is not a completion boundary. Keep working against the original
goal, and let commits and artifacts retain the history.
