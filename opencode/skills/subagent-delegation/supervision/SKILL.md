---
name: supervising-agent-work
description: Use when asked to supervise, monitor, steer, audit, or periodically check another live agent running in tmux, especially when the task involves reading a pane, reviewing another agent's recent work, sending corrective messages, or using [[codex/SKILL|Codex]] PTY sleep timers for repeated supervision ticks.
---
# Supervising Agent Work

Supervise the other agent as a skeptical investigator and independent reviewer, not as a
relay for its status reports. The task is to keep the live work aligned with the user's
actual objective and intervene only when the observed work drifts, cheats, broadens, or
substitutes a weaker success condition.

Success means the user's intended simple task is fully complete. Partial completion is
an incompleteness signal with progress context, not a success signal.

## Core Policy

- Act as the skeptical translation layer between worker-internal language and the
  user's plain objective. If you cannot state the task in simple user-observable terms,
  ask the user before judging completion.
- Treat the other agent's summaries as claims to verify, not evidence.
- Read the live pane first; fetch transcripts only when the pane does not contain enough
  context to judge the current work.
- Send corrective messages only when there is a concrete drift signal or the user
  explicitly asks you to send a message.
- The supervising agent owns the review. Do not wait for the supervised agent to audit
  itself when the user asked you to supervise or review.
- Completion requires positive evidence that the intended task is correct, aligned, and
  minimal. "No obvious slop" is not enough.
- Worker success criteria and supervisor success criteria are different. The worker may
  need narrow QC, guardrails, and anti-gaming constraints; the supervisor must judge
  whether those artifacts actually deliver the simple task the user wanted.
- Repo-local automated QC, recipes, tests, and linters are worker-layer signals. The
  observer may inspect them as artifacts, but must not reproduce them as the review or
  treat green output as an improved epistemic status for task completion.
- Required worker self-review is also worker-layer evidence. Enforce it when required,
  then review the work independently; do not accept the worker's self-review as the
  observer review.
- Assume the worker may game narrow rules, self-certify, hide gaps behind fluent
  language, or present progress as completion. Inspect transcripts and artifacts for
  those behaviors as part of the supervision job.
- Keep repo philosophy, alignment rules, and documented LLM failure and gaming modes in
  active context so novel misalignment can be recognized instead of reduced to a known
  checklist item.
- Uncertainty is a temporary analysis state, not a supervisory status and not a reason
  to nudge the worker. Resolve it by inspecting the available evidence before taking
  action.
- When communicating status to the user, lead with complete or not complete. Do not
  bury an incomplete task behind slice-level success, partial milestones, or qualified
  completion language.

## Reference Skills

- [[reading-transcripts/SKILL|reading-transcripts]]: load before fetching historical or live agent transcripts.
- [[anti-slop/SKILL|anti-slop]], [[reviewing-llm-code/SKILL|reviewing-llm-code]], or [[reviewing-subagent-work/SKILL|reviewing-subagent-work]]: load when judging
  drift, reward hacking, or agent-produced work.
- [[llm-failure-modes/SKILL|llm-failure-modes]]: load when the review depends on recognizing gaming,
  self-certification, jargon capture, goal narrowing, or other adversarial agent
  behavior.
- [[ssh-workstation-and-tmux/SKILL|ssh-workstation-and-tmux]]: load when the target session is remote or the user asks
  about workstation tmux sessions.
- [[scheduling-tasks-and-subagents/SKILL|scheduling-tasks-and-subagents]]: load only when the user asks for external scheduled
  wakeups. For [[codex/SKILL|Codex]] self-supervision, prefer the PTY sleep timer below.

## Observe The Session

Start with read-only tmux commands:

```bash
tmux list-sessions
tmux list-windows -t <session>
tmux capture-pane -pt <session>:<window> -S -200
```

Use the target exactly as named by the user, such as `main:0`. Increase the capture
history when needed, but do not treat a pane tail as a full transcript. If the visible
pane references prior decisions, queued prompts, hidden scrollback, or a separate
session identifier, fetch the transcript through [[reading-transcripts/SKILL|reading-transcripts]].

When reading the pane:

- Identify the user's strongest live goal and the supervised agent's stated goal.
- Compare the current work against that goal, not against the agent's own narrowed
  framing.
- Translate worker jargon, proof-artifact names, commit messages, and QC claims into the
  user's frame: what user-visible outcome changed, and does it satisfy the original
  request?
- Treat worker self-review, green recipes, and passed tests as inputs to investigate,
  not as conclusions. Ask what they fail to observe, whether they were suppressed, and
  whether they prove the user's simple outcome.
- Check the transcript for process alignment: goal narrowing, proof laundering,
  self-certification, suppressed failures, jargon capture, or status reports that turn
  progress into completion.
- Resolve uncertainty from evidence before intervening. Use the full available record:
  pane state, parsed transcript, git log, commits, staged and unstaged diffs, recently
  modified files, and filesystem state.
- Distinguish expected red evidence from task-failure evidence.
- Check recent commits or diffs when the agent treats them as progress, but do not infer
  correctness from commit existence.

## Independent Review Layer

The observer is the independent reviewer. Do not duplicate the worker's automated
[[quality-control/SKILL|quality-control]] loop and call that supervision.

Worker layer:

- implement the requested task;
- run required recipes, tests, linters, and QC;
- perform required self-review or drift audit;
- report its own claimed completion.

Observer layer:

- recover the user's simple intended outcome;
- inspect the worker transcript for alignment and gaming behavior;
- inspect artifacts to determine whether they actually deliver that outcome;
- decide whether the worker's evidence proves correctness beyond reasonable doubt;
- communicate the status in the user's frame.

The worker layer must not be skipped. If a worker obligation applies, missing or failed
worker-layer evidence blocks observer completion. Passing the worker layer is never
sufficient for the observer goal. The observer goal is complete only when all applicable
worker-layer obligations and the independent observer review both pass.

## Periodic [[codex/SKILL|Codex]] Supervision Timer

When the user wants repeated supervision from this [[codex/SKILL|Codex]] session, use a long-running PTY
sleep as the timer:

```bash
sleep 600; printf '\n__SUPERVISION_TICK__\n'
```

Run it in a PTY session and poll until the marker appears. At each tick:

- Capture the pane.
- Inspect relevant recent repo state or transcript context.
- Decide whether an intervention is required.
- Start the next PTY timer only if supervision still needs to continue.

Do not replace this with `at`, `opx`, or external scheduler commands unless the user
explicitly asks for external persistence.

## Sending Messages Into Tmux

Use literal `send-keys` for message text, then submit it with Enter:

```bash
tmux send-keys -t <session>:<window> -l "<message>"
tmux send-keys -t <session>:<window> Enter
```

The Enter key is required. Without it, the text can remain in the TUI input line and the
agent may never receive it.

After sending:

```bash
tmux capture-pane -pt <session>:<window> -S -40
```

Verify whether the message was submitted, queued, or merely left in the input area. If
the TUI explicitly says a queued message requires Tab, send Tab only after the message
and Enter:

```bash
tmux send-keys -t <session>:<window> Tab
```

Do not send Tab as a generic submit command. It can insert or select unrelated default
prompts. If accidental unsent input appears in the target TUI, clear it without
submitting:

```bash
tmux send-keys -t <session>:<window> C-u
```

## Intervention Content

Keep interventions short and actionable. A good intervention states:

- the observed drift or risk;
- the exact goal or invariant it violates;
- the correction expected before continuing.

Intervene only after analysis establishes a concrete drift finding. Do not send
"double-check", "maybe", "ensure", "be careful", or other uncertainty-based nudges. If
the evidence is not yet decisive, inspect more evidence. If a required evidence source
is unavailable, report that blocker to the user instead of nudging the worker.

Example:

```text
Stop after the current command. The current patch appears to reintroduce method-name
satisfaction filtering, which violates the simple bridge objective. Do not present this
as aligned; repair the design so ordinary Python/Sage lookup supplies concrete methods
and missing obligations remain visible.
```

Do not send praise, acknowledgments, motivational language, or vague "be careful"
messages. If no drift is visible, let the agent work.

## User Status Reports

The user-facing report is the observer's judgment, not the worker's evidence bundle.
Use one of these shapes:

```text
Yes. The intended task is complete.
Original simple intention: <one-sentence user-facing outcome>.
Why I believe this: <high-level analysis showing artifacts and process imply completion>.
```

```text
No. The intended task is not complete.
Original simple intention: <one-sentence user-facing outcome>.
Gap: <the specific difference between current work and full completion>.
What the partial work shows: <only the progress needed to understand the gap>.
Next supervisory action: <how the worker should be redirected, if still active>.
```

If evidence is insufficient, report it as incomplete:

```text
No. I do not yet have proof that the intended task is complete.
Missing proof: <exact claim not yet established>.
```

Do not leave "I am uncertain" as the final status. Convert it into one of:

- a resolved `Yes` judgment;
- a resolved `No` judgment with the gap;
- a blocker stating which evidence source could not be accessed.

Rules:

- Lead with `Yes` or `No` when the user asks whether the task is done.
- Treat partial completion as a failure to finish the intended task.
- Mention successes only when they explain the remaining gap or support the full
  completion judgment.
- Do not make the user infer completion from proof artifacts, commits, tests, QC, or
  worker-internal milestones.
- Do not use "slice", "accepted", "mostly", "likely", "non-goal gaps", or similar
  qualifiers to make an incomplete state sound success-shaped.

## Completion Standard

Before calling supervision complete, prove beyond reasonable doubt that the supervised
work satisfies the user's actual intended task and that the worker process stayed
aligned while producing it.

First write the task as one plain sentence with user-observable success criteria. If the
sentence requires worker jargon, internal guardrail names, or QC labels to be
understandable, the completion frame is not ready; read more or ask the user to pin it
down.

Required evidence:

- the original goal or plain task statement has been recovered from user messages,
  plans, issues, or transcripts;
- current artifacts satisfy that goal directly, not merely a narrowed slice;
- the process did not rely on goal narrowing, self-certification, jargon capture,
  success-shaped partials, or other agent-gaming behaviors;
- required worker-layer QC or self-review was performed when required, and the observer
  independently reviewed the resulting artifacts and process;
- automated checks were connected to the task proposition by observer analysis instead
  of treated as generic green signals;
- the implementation is minimal for the objective and does not add substitute
  satisfaction systems, validators, hidden fallbacks, or status laundering;
- runtime behavior or other object-level evidence proves the intended result;
- remaining red checks or failures are classified by relation to the task, not treated
  generically as success or failure.

Do not mark the supervision goal complete because:

- the supervised agent claims it is done;
- focused checks passed but the positive intended relation was not proven;
- no known slop signatures remain;
- repo-local recipes, tests, linters, or QC passed;
- required worker self-review was performed;
- the worker satisfied its own narrow QC or anti-gaming success criteria;
- the observer can enumerate proof artifacts but has not analyzed whether they imply the
  user's simple desired outcome;
- meaningful progress was made but the intended simple task is still incomplete;
- the public status, handoff, or goal text was made more accurate;
- remaining work was reclassified as future work without proving it is outside the
  user's original objective.

## Do/Do-Not One-Shot Examples

Use these as direct replacements for common supervision mistakes:

- **Live goal recovery**
  - Do: "The task is the user's plain request: `<objective>`. I will judge the
    artifacts against that request."
  - Do not: Treat defensive guardrails, the supervised agent's plan, or a review-gate
    label as the task.

- **Skeptical translation**
  - Do: Translate "QC passed, drift audit clean, proof artifacts present" into "the user
    can now do `<observable outcome>`" or "the user still cannot do `<observable
    outcome>`."
  - Do not: Relay the worker's internal milestone language as if it answered the user's
    completion question.

- **Frame separation**
  - Do: Keep two frames separate: the worker's anti-gaming criteria and the supervisor's
    plain user-facing success criterion.
  - Do not: Adopt the worker's narrow success criteria as your own standard for marking
    supervision complete.

- **Independent review layer**
  - Do: Enforce required worker QC and self-review, then perform a separate observer
    review for semantic correctness and alignment.
  - Do not: Re-run or relay repo-local automated QC as if it were the independent
    observer review.

- **Uncertainty resolution**
  - Do: Resolve uncertainty by reading the transcript, git history, diffs, recent files,
    and filesystem state before deciding whether to intervene.
  - Do not: Nudge the worker because something "might" be wrong.

- **Automated signals**
  - Do: Use green checks only after explaining which user-facing claim they prove and
    why the worker could not have satisfied them by gaming or suppressing failures.
  - Do not: Treat green recipes, passed tests, or lint as proof that the intended task is
    complete.

- **Adversarial worker model**
  - Do: Inspect whether the worker gamed the task by satisfying narrow rules, using
    fluent self-promotion, or turning partial progress into a completion claim.
  - Do not: Assume passing worker-side QC or meeting a checklist means the worker stayed
    aligned with the user's intended task.

- **Context stewardship**
  - Do: Keep repo philosophy, alignment constraints, and LLM failure modes active while
    reviewing for novel forms of misalignment.
  - Do not: Limit the review to known slop signatures or issues the worker already
    named.

- **Independent audit**
  - Do: Read the pane, transcript, diff, tests, and runtime evidence yourself when the
    user asks you to supervise or review.
  - Do not: Ask the supervised agent to audit itself and then relay its conclusion.

- **Message delivery**
  - Do: Send the literal message, send `Enter`, then capture the pane to verify the
    message was submitted.
  - Do not: Assume text sitting in the TUI input line was received, or use `Tab` as a
    generic submit key.

- **[[codex/SKILL|Codex]] supervision timer**
  - Do: Use a [[codex/SKILL|Codex]] PTY sleep marker for repeated checks from the current [[codex/SKILL|Codex]]
    session.
  - Do not: Switch to `at`, `opx`, or an [[opencode/SKILL|OpenCode]] wakeup unless the user asked for
    external persistence.

- **Positive completion evidence**
  - Do: State the exact proposition that would make the task complete, then cite
    object-level evidence that proves it.
  - Do not: Mark complete because no obvious slop remains, focused checks passed, or
    the observed work looks plausible.

- **Negative evidence**
  - Do: Say "I have not found evidence of failure" when that is all the evidence
    supports.
  - Do not: Convert that into "the task succeeded as intended."

- **Status language**
  - Do: Say "not complete; missing proof of `<claim>`" or "complete; facts `<A>`,
    `<B>`, and `<C>` entail `<claim>`."
  - Do not: Hedge with "likely," "accepted slice," "non-goal gaps," or "narrowed
    objective" when the user asked whether the intended task is done.

- **Partial progress**
  - Do: Say "No, the intended task is not complete; the current work only establishes
    `<partial result>`, and the remaining gap is `<gap>`."
  - Do not: Lead with the partial result or describe it as success when full completion
    is still missing.

- **Scope preservation**
  - Do: If only part of the task was verified, say which part and leave the full goal
    open.
  - Do not: Rename the verified portion as "the slice" or "the plain task" and mark
    the overall supervision achieved.

- **Expected red evidence**
  - Do: Classify each red check by its relation to the goal: expected proof of a visible
    gap, unrelated repo debt, or real task failure.
  - Do not: Treat any red output generically as either success or failure.

- **Proof standard**
  - Do: Accept a proof made from a conjunction of observed facts when those facts entail
    the intended result.
  - Do not: Require one integrated automated test artifact if the relevant facts have
    already been directly observed.

- **Proof-artifact communication**
  - Do: Perform artifact analysis internally, then tell the user the completion status
    in the user's frame.
  - Do not: Give the user an inventory of commits, tests, QC checks, or proof components
    and leave them to infer whether the original task is complete.

- **Repo QC**
  - Do: Use repo checks only as supporting evidence after the task proposition is clear.
  - Do not: Substitute broad QC, lint, or test-suite status for proof that the user's
    objective was met.

- **Correction handling**
  - Do: Convert a user correction into a changed action and a sharper completion
    standard.
  - Do not: Reload correction procedures or restate alignment language as a substitute
    for changing the work.

- **Administrative cleanup**
  - Do: Distinguish "I corrected a false status/report" from "the supervised work is
    now correct."
  - Do not: Count a clearer handoff, queued warning, reopened status, or corrected goal
    label as substantive progress on the implementation or proof.

## Anti-Patterns

| Pattern | Why It Fails | Do Instead |
| --- | --- | --- |
| Sending text without Enter | The target TUI may not submit the message | Always send text, then `Enter`, then verify with capture |
| Trusting the supervised agent's final report | It is self-certification | Inspect pane, transcript, code, commits, and runtime evidence |
| Treating absence of drift as completion | Negative evidence is not proof of success | Prove the intended positive behavior |
| Reporting partial progress as success | It hides the fact that the intended task is incomplete | Lead with `No`, then state the gap to full completion |
| Re-running repo QC as review | Automated signals are the worker layer and may be gamed or suppressed | Perform independent semantic and process review |
| Accepting worker self-review | It is the worker's own layer, not the observer layer | Enforce it, then review independently |
| Using Tab indiscriminately | It can queue or insert unintended prompts | Use Tab only when the TUI visibly requires it |
| Supervising by pane tail only | Scrollback may omit the decisive context | Fetch and parse transcripts when current context is insufficient |
| Intervening while uncertain | Uncertainty is an unresolved investigation state, not evidence of drift | Resolve from transcript, git, and filesystem evidence before acting |
