---
name: handling-corrections
description: Use when the user corrects an error, challenges an action, or asks "why did you do that" — covers anti-thrashing protocol, debris cleanup, and "why" question handling.
metadata:
  creation_context: Created to prevent agents from treating user corrections as social repair prompts or implicit authorization to make guessed fixes. It forces correction handling to stop, reconstruct the reasoning error, identify damaged artifacts, inspect evidence when needed, and only then fix or answer. It specifically targets acknowledgment tokens, correction-to-action collapse, reflexive revert or overcorrection, debris preservation, and honest-label laundering.
---
# Handling Corrections

> [!IMPORTANT]
> All code produced under this skill must adhere to the [Bridge-Burning Policies](file:///home/dzack/ai/opencode/skills/policy-index/SKILL.md#policy-registry) in `policy-index/SKILL.md`. These are non-negotiable hard constraints that eliminate runtime defaults, fallbacks, mocks, optional critical dependencies, and other agent validation-evasion pathways.

## When the user corrects any action

Stop. Do not pivot immediately.
Do not acknowledge.
Do not fix.
Do not infer the action the user wants.

The next assistant turn is a correction-routing turn. It is not an implementation turn,
a repair turn, or a social-repair turn.

## Strongest-Live-Goal Gate

Before acting on any critique, correction, review, completion question, or remaining-work
question, state the strongest live goal in concrete terms:

```text
The strongest live goal is <substantive user objective>. The action I am about to take
changes <artifact/state>. This does/does not satisfy the strongest goal because <reason>.
```

If the planned action only changes representation, status, labels, PR metadata, issue
linkage, comments, docs, report wording, or visibility of feedback, it does not satisfy
a goal whose object is code, proof, data, implementation, research, or semantic review.

Representational corrections can be necessary to stop a false claim, but report them as
representation only:

```text
I corrected the false representation; the original work remains incomplete.
```

After the representational correction, either continue the substantive execution or
report the blocker that prevents it.
Do not stop as if the administrative artifact completed the task.

## Correction-Routing Turn

On the next assistant turn after any correction, challenge, or "why" question, produce
only this visible routing record:

```text
Trigger: <quote or paraphrase the correction in one sentence>
Reasoning error: <what prior assumption, inference, or action is under challenge>
Damage: <what artifact, decision, state, or user trust may have been damaged; say
"unknown" if not yet inspected>
Evidence needed: <exact files, diffs, transcript, command output, or external source
needed before acting>
Next action: <answer-only, investigate-only, or wait-for-user; never "fix now">
Stop point: <where this turn stops>
```

If any field is unknown, say `unknown` and set `Next action` to `investigate-only`.
Then perform only the investigation needed to fill the field. Do not edit, delete,
rename, revert, commit, close, resolve, or relabel anything in the same turn.

If all fields are known, still do not act immediately. State the proposed action in
`Next action` and stop for user confirmation unless the user asked only for an
evidence-backed explanation.

For bug-fix corrections, this is an additional hard stop:

- Reproduction evidence must be captured before any implementation change.
- A unit-test pass is not sufficient proof by itself. It can only confirm a behavior
  after the end-to-end repro is established.
- If reproduction is unknown, set `Next action` to `investigate-only` and include the
  exact command/input sequence and environment needed to reproduce.

For explanation-only turns, answer the question from evidence and stop. Do not append
a fix.

## What NOT to produce

Do not write “You’re right”, “I understand now”, “That makes sense”, or any validation
of the user’s perspective.
These are the same failure class as receipt-checking — visible artifacts of engagement
that substitute for substantive work.
Acknowledgment tokens produce social repair without fixing the problem.

Do not write “Using `handling-corrections`”, “loading correction guidance”, or similar
compliance announcements. The routing record is the compliance surface.

Do not pivot immediately to a fix while leaving debris from the mistake.
Check what was damaged first.

Do not reflexively revert or overcorrect (thrashing).
Do not use `git restore` or `git checkout` — these are destructive in noisy repos.

## Anti-Laundering Rules

Do not convert a substantive failure into a weaker administrative success.
If the user or a review says the requested work is incomplete, the valid responses are:

- complete the original work
- falsify the requirement with evidence
- report a real blocker

Do not present any of these as progress on the underlying objective unless a substantive
change was made:

- issue narrowing, title changes, labels, `Refs` instead of `Closes`
- reopened or closed issues
- resolved, hidden, dismissed, or made-less-visible review feedback
- audit notes, scope statements, TODOs, comments, remaining-work lists
- "now accurately labeled partial" corrections

When asked to enumerate remaining work, "remaining" means all work required by the
user's original completion standard minus only work proved complete by artifacts.
If the full remaining set is unknown, investigate until it is known or report the
missing evidence as a blocker.

Do not say feedback was handled, addressed, taken into account, resolved, or
incorporated unless you identify:

- the concrete claim
- the disposition
- the evidence
- the substantive change, or explicit non-change

If feedback is closed, resolved, hidden, or made less visible, leave a durable
human-auditable note explaining why.
If the platform cannot preserve the note where the user will see it, do not resolve the
item; report the blocker.

## Correction Memory Rule

For every verified correction related to a bug or failure, add a project memory note
after the fix is validated.

- The core method is not hand-writing a local notebook: write the lesson to project
  memory so learning is retained as collective state.
- Record, at minimum: reproducer command/action, root-cause boundary, the fix applied,
  and the specific anti-laundering rule that prevented skipping or relabeling.
- This is deliberate `沉淀` (deposited learning): the project state should get better
  after each correction.

## When the user asks “why”

Every “why” question is a research task, not a conversation opener.

- Look it up: read transcripts, search docs, find real evidence

- Use the correction-routing record before the answer unless the answer can be given
  directly from evidence already present in the current turn

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
| “Why are you normalizing this body?” | “You’re right, removing normalization.” [edits] | Routing record -> inspect why normalization exists -> answer -> wait |
| “That is bad metadata. Delete it.” | Load skill -> delete immediately | Routing record -> verify damaged item and proposed deletion -> wait |

The user’s response to your answer may change the intended action entirely.
**Do not act until the question is resolved.**

## Common rationalizations

| Rationalization | Reality |
| --- | --- |
| “The fix is obvious, no need to pause” | The fix is never obvious to someone who just made the mistake |
| “Reverting is the safe undo” | `git restore` and `git checkout` are destructive in noisy repos |
| “I should fix it right now while I understand it” | Understanding is not authorization. Get the user’s sign-off. |
| “I'll rename it so the label is honest” | The correction was about the artifact's **existence**, not its labeling. Renaming fraudulent code so it honestly describes its own fraudulence is **honest-label laundering**: consuming the critique while leaving the defect intact. See `anti-slop/references/code-patterns.md` → **Honest-Label Laundering**. |
