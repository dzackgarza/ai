---
name: handling-corrections
description: Use when the user corrects an error, challenges an action, or asks "why did you do that" — covers anti-thrashing protocol, debris cleanup, and "why" question handling.
---
# Handling Corrections

> [!IMPORTANT]
> All code produced under this skill must adhere to the [Bridge-Burning Policies](file:///home/dzack/ai/opencode/skills/anti-slop/SKILL.md#bridge-burning-policies) in `anti-slop/SKILL.md`. These are non-negotiable hard constraints that eliminate runtime defaults, fallbacks, mocks, optional critical dependencies, and other agent validation-evasion pathways.

## When the user corrects any action

Stop. Do not pivot immediately.
Do not produce text.
Do not acknowledge.

## Synthesis Gate

Produce this statement internally before doing anything else:

**“The reasoning error was _____, it damaged _____, and the fix is _____.”**

If you cannot fill all three blanks, you do not yet understand the correction well
enough to act. Use tools to investigate (git diff, read files, check what was changed)
until you can.

Once you can fill all three blanks: fix the problem immediately with tools.
Text explanation comes ONLY AFTER the fix is done, if needed at all.

## What NOT to produce

Do not write “You’re right”, “I understand now”, “That makes sense”, or any validation
of the user’s perspective.
These are the same failure class as receipt-checking — visible artifacts of engagement
that substitute for substantive work.
Acknowledgment tokens produce social repair without fixing the problem.

Do not pivot immediately to a fix while leaving debris from the mistake.
Check what was damaged first.

Do not reflexively revert or overcorrect (thrashing).
Do not use `git restore` or `git checkout` — these are destructive in noisy repos.

## When the user asks “why”

Every “why” question is a research task, not a conversation opener.

- Look it up: read transcripts, search docs, find real evidence

- Do **not** answer with supplication, invented feelings, or promises about future
  behavior

- Do **not** immediately act on your own answer — wait for the user to confirm before
  proceeding

## The question-then-action trap

Answering a question and then immediately acting on your own answer is a violation.

| Situation | Bad | Good |
| --- | --- | --- |
| “Why does this function have param x?” | “You’re right, it’s not needed, removing it.” [deletes] | “x is used for Y. It may no longer be needed.” [waits] |
| “Why did you edit that file?” | Explain + immediately restore it | Explain root cause, assess damage, wait for direction |

The user’s response to your answer may change the intended action entirely.
**Do not act until the question is resolved.**

## Common rationalizations

| Rationalization | Reality |
| --- | --- |
| “The fix is obvious, no need to pause” | The fix is never obvious to someone who just made the mistake |
| “Reverting is the safe undo” | `git restore` and `git checkout` are destructive in noisy repos |
| “I should fix it right now while I understand it” | Understanding is not authorization. Get the user’s sign-off. |
| “I'll rename it so the label is honest” | The correction was about the artifact's **existence**, not its labeling. Renaming fraudulent code so it honestly describes its own fraudulence is **honest-label laundering**: consuming the critique while leaving the defect intact. See `anti-slop/references/code-patterns.md` → **Honest-Label Laundering**. |
