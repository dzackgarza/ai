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

## Forcing Questions

Before writing any response that reports status, completion, or progress, answer:

**Q1: "What is the user's OVERALL task, not just what I last worked on?"**

A: [restate the global task]

**Q2: "For each item I'm about to include — would the user learn something they don't already know?"**

- If it's something the user can see (file exists, commit was made, test output) → omit
- If it's something only I know (a decision I made, a gap I noticed, an error I encountered) → include
- If it's already resolved → omit entirely, it is noise

**Q3: "Am I scoping 'not completed' to my local sub-task, or to the overall task?"**

"Not completed: none" is almost never correct. The local sub-task may be done, but the overall task has outstanding items. The user wants to know about the OVERALL task — that's why the response template exists. If you can't identify outstanding items in the overall task, you have lost track of the overall task.

**Q4: "Is 'Next action' framing unfinished work as optional?"**

If the task is not done, there is no "next action" — there is **remaining work**. "Next action" implies discretion; remaining work implies obligation. Use the framing that matches reality.

## The Theory of Mind Test

For every item in your response, ask:

**"Why would the user want to read this?"**

Possible answers:
- **To know what's still broken** → include, prominently
- **To make a decision I can't make** → include, with the decision framed clearly
- **To verify I did what they asked** → the git commit does this; omit from response
- **To feel assured work was done** → this is social compliance, not information; omit
- **No reason — I'm filling a template** → omit

If more than half your response items fail this test, your response is template-filling, not communication.

## Anti-Patterns

| Pattern | Problem | Fix |
|---|---|---|
| "Not completed: none" | Scoped to micro-task, ignoring global task | Restate the global task; list what's outstanding globally |
| Listing resolved items as "open" | Padding with noise | Only include items that require action |
| Artifact-level status dump | Wrong abstraction level | Report on the process, not the file |
| "Next action: X" for mandatory work | Frames obligation as optional | "Remaining work: X" or just continue doing it |
| Summarizing what was done | User can see git log | Only report what the user CAN'T see |

## What Good Responses Contain

Only items the user needs and can't already see:

- Gaps that block the overall task
- Decisions that need user input
- Errors or surprises the user should know about
- Divergences between what was asked and what was done
- Remaining mandatory work in the overall task
