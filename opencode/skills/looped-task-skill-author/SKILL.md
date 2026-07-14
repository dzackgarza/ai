---
name: looped-task-skill-author
description: Use when authoring or refining repo-local [[codex/SKILL|Codex]] skills for repeated one-shot agent loops that advance long-horizon or open-ended tasks through progress logs, self-correcting state machines, transcript-based manual testing, and cautious promotion to cron/Hermes-style orchestration. Do not use for ordinary one-off scripts or batch automation.
---
# Looped task skill authoring

Use this skill when creating or revising a repo-local subskill whose purpose is to guide
repeated one-shot agent invocations toward a long-horizon, possibly open-ended goal.
These subskills are meant for agents launched periodically by cron, Hermes, another
orchestration manager, or a human running the same one-shot prompt repeatedly.

The artifact you create is normally a repo-local skill under
`.agents/skills/<subskill-name>/SKILL.md`. Keep it instruction-only unless the user or
an existing repository convention explicitly requires otherwise.
For this class of work, scripts, batch launchers, auto-graders, and automatic
correctness checks usually damage the desired behavior by replacing agent judgment with
brittle proxies.

## Core philosophy

A looped task skill specifies a self-correcting behavior, not a deterministic program.

Each invocation is a bounded one-shot.
It should read the current state, reconcile prior notes with actual repository state,
make one meaningful increment of progress, and leave the repository and status documents
in a clean continuation state for the next invocation.
The loop converges because every run repairs small inconsistencies, updates shared
state, and narrows the remaining work.

Do not design these subskills around automatic success measurement, scripted
verification, or batch execution.
Do not teach the subagent to optimize for a metric, a green check, or a summary report.
Existing project commands may be used as local evidence when they are naturally part of
the work, but they must not become the definition of success for the loop.
Correctness comes from the repeated agent behavior becoming eventually consistent with
the repository, the progress log, and the goal.

The skill must preserve room for judgment.
Overly rigid instructions cause mechanical box-checking, verbose status churn, and
plausible-looking slop.
Under-specified instructions cause drift.
The right level of structure is an explicit but flexible state machine: enough to orient
the subagent, not enough to remove thought.

## First inspect the local environment

Before writing a subskill, inspect the repository and local agent configuration for
existing conventions.
Prefer local conventions over this generic default when they are more specific and
compatible with the loop philosophy.

Required companion skills:

- [[writing-for-agent-audiences/SKILL|writing-for-agent-audiences]] for audience control and concise agent-facing prose.

- [[creating-skills/SKILL|creating-skills]] for what belongs in a `SKILL.md`.

- [[subagent-delegation/authoring/SKILL|creating-subagents]] when the loop depends on repo-local agents or subagent
  descriptions.

- [[prompt-engineering/SKILL|prompt-engineering]] when editing system prompts or agent definitions adjacent to the
  skill.

Look for, as applicable:

- `AGENTS.md`, nested `AGENTS.md`, or `AGENTS.override.md` files.

- Existing `.agents/skills/*` skills, especially [[model-selection/SKILL|model-selection]], testing,
  orchestration, maintenance, or logging skills.

- Existing progress logs, runbooks, issue trackers, backlog documents, or planning
  documents.

- Existing cron/Hermes/orchestration docs and transcript locations.

- Existing expectations for how live agent trials are reviewed.

If a tested local method for developing and evaluating skills already exists, follow it.
Only use the method below when the environment has no better local convention.

## What to create

When asked to create a looped-task subskill, produce a concise repo-local skill with
these elements.

1. Clear front matter. The `description` must say that the subskill is for a repeated
   one-shot loop, name the long-horizon task, and include the main trigger words an
   agent or orchestrator will use.

2. A scope boundary. State when the subskill should and should not be used.
   Exclude ordinary one-off implementation work, broad research with no persistent
   state, and tasks where the user expects a deterministic script.

3. A canonical status location.
   Define exactly where the subagent should read and update progress state.
   Prefer a single canonical state file plus optional append-only run notes.
   Avoid scattering status across many documents.

4. A start-of-run reconciliation rule.
   Every run begins by reading the status file and comparing it to the actual repository
   state. The subagent must treat the repository as primary evidence and the log as a
   fallible memory aid.

5. A self-correcting state machine.
   Define named states, transition evidence, and typical behavior, but do not create a
   long checklist. The state machine should tell the subagent how to decide what mode it
   is in and how to leave the repo ready for the next run.

6. Clean continuation requirements.
   Every run should end with updated status, explicit remaining obligations, and a
   repository state that a later agent can continue without guessing.

7. Manual live-testing instructions.
   Include instructions for developing the subskill by observing live subagent
   transcripts, not by trusting subagent summaries or only checking generated artifacts.

8. Promotion criteria. The subskill is not ready for cron/Hermes until repeated live
   trials show stable behavior, resilience to inconsistent state, and no significant new
   behavior when launched through the intended orchestrator.

Use `references/subskill-template.md` as a compact template and
`references/manual-observation-rubric.md` as the default live-test rubric.

## What to exclude from subskills

The subskill text is injected into every subagent’s context verbatim.
Keep it free of meta-pollution that causes the agent to optimize for the wrong thing.
The subskill is not a memo to the orchestrator; it is instructions that run inside the
agent’s head.

### Leaked orchestration concepts

Do not tell the subagent it is a “run,” that it is one of many “invocations,” that it
should “stop” or “complete its run,” or that it has a bounded turn.
These concepts belong to the orchestrator—not the subagent.

A subagent that knows it is bounded will reward-hack “completing the run” instead of
pursuing the goal. The orchestrator handles launches, timeouts, and stopping silently.
The subskill must not discuss these.

What the subskill CAN define: when the agent should not proceed further—because
authority is missing, a human decision is needed, or no useful autonomous increment
remains. Define these as blockers to record (BLOCKED) or recognition that the goal is
currently satisfied (QUIESCENT). Never frame these as “stop working” or “your run is
over.”

### Evaluation and self-assessment

Do not include instructions that ask the subagent to evaluate its own work, declare
success, rate quality, or assess correctness.
Self-evaluation produces plausible-looking self-certification, not actual verification.
The loop converges through repeated reconciliation with real repository state, not
through the agent claiming progress.

Do not ask the subagent to decide whether the loop as a whole is succeeding, converging,
or worthy of promotion.
Those are human/author judgments made by observing transcripts.

Do include artifact-quality criteria the worker needs in order to do good work.
Examples: preserve source text, update the canonical state file, verify target paths, or
leave continuation state in the artifact.
These are not evaluator leakage; they are the production definition of the desired
artifact or state.

Do not include harness facts, run numbers, transcript postmortems, model comparisons, or
evaluator complaints unless the loop’s object-level task is to operate on those
materials. Convert observed failures into task-facing invariants before adding them to
the subskill.

### Tool restrictions

Do not enumerate forbidden tools or capabilities in the subskill.
If a subagent should lack certain tools, restrict them through the harness—for example,
an opencode primary agent definition that omits the Write tool.
Skills describe what to do; permissions are a harness-layer concern that should never be
negotiated inside the agent’s context.

### Meta-language about the skill itself

Do not write prose about what the skill covers, how it was designed, why it works, or
what philosophy it follows.
The subskill is an instruction set, not a design document.
Any paragraph that begins with “This skill …” or “The purpose of this skill …” is a
signal that the author is writing commentary instead of instructions.

## No handoff documents, summaries, or self-reports

Do not design loops around handoff documents that record what a previous run
accomplished or how much progress it made.
Do not ask subagents to write completion reports, success metrics, or quality
self-assessments for the next agent to read.

Subagents will overstate completion.
They will claim success when they have produced slop.
They will describe plausible work they did not do.
These claims are worse than useless: they are fabricated evidence that corrupts the next
run.

When a subsequent agent reads a handoff summary that says “Tasks 1–4 completed, 85%
progress,” it will not verify.
It will treat the claim as a premise and plan from it.
The claim becomes the foundation, not the hypothesis.
Across many runs, fabricated claims compound: each agent optimizes for the next agent’s
expectations rather than the underlying goal.
This is a Jerryboree — agents validating agents without epistemic independence.
See `jerry-behaviour` for the full failure mode.

### The Markov loop design

The loop must be Markov: the information needed to decide what to do next lives in the
artifacts themselves and in the subskill’s guidelines, not in any agent’s self-report
about what it did.

Design every state transition so that a fresh agent with no knowledge of prior runs can
read the current artifacts, apply the subskill’s rules, and independently determine what
stage the work is in and what increment to make.

Completion is not known because a status file says `completed`. Completion is known
because an agent inspects an artifact, applies the subskill’s quality criteria, and
finds nothing left to do.
The same agent, on seeing substandard work filed under a “completed” heading, should
reject it back to an earlier stage — no markup needed, just the artifact itself.

### Resilience to half-complete and reward-hacked work

Expect agents to produce partial, lazy, or reward-hacked output.
This is normal. The loop survives because every run starts with the same protocol:

1. Assess the current artifacts against the subskill’s documented quality standards.

2. Purge or repair work that is obviously sloppy, incomplete, or inconsistent.

3. Continue from the honest state, not from a prior agent’s claim about what state
   exists.

Handoff documents damage this protocol.
They give the agent a shortcut — read the summary, skip the artifacts — and a liability
— trust the summary, propagate the error.
Strip them out. The artifacts are the only handoff.

## Status and progress logs

The subskill should define one canonical state file, usually one of:

- `.agents/state/<loop-name>.md` for agent-private operational state.

- `docs/agent-loops/<loop-name>.md` when humans should read the loop status.

- An existing project planning file, when the repository already has a clear convention.

Use the smallest state format that supports continuation.
A good state file usually contains:

- Goal and scope.

- Current mode/state.

- Last observed repository state.

- Last meaningful action.

- Open obligations and known inconsistencies.

- Next useful action, phrased as a direction rather than a script.

- Blockers requiring human input, if any.

- Last updated timestamp and, if available, transcript pointer.

The log is not a source of truth.
At the start of every run, the subagent must reconcile it with the actual repository.
If the log says a change exists and it does not, correct the log and either restore the
missing work or continue from the real state.
If the repository contains unlogged progress, incorporate it.
If a previous run stopped mid-change, repair and finish that partial work before
starting a new thread of work.

End-of-run updates must be concise.
The state file should make the next run easier, not become a diary.
Avoid generic statements such as “made progress” or “continue improving.”
Record concrete state and the next best continuation.

## Designing the state machine

Every looped-task subskill needs an explicit state machine, but it must not be a rigid
procedural cage. Use states as decision modes.

A default state machine is:

`RECONCILE -> RECOVER | ADVANCE | BLOCKED | QUIESCENT -> CONSOLIDATE`

`RECONCILE` is always the opening mode.
Read the status file, relevant repo files, and any local instructions.
Compare stated progress with actual state.
Decide whether the run is recovering, advancing, blocked, or quiescent.

`RECOVER` is used when the prior run left an inconsistent or partial state.
Repair the partial work, clean contradictory docs, finish an obvious interrupted action,
or roll the state forward to match reality.
Do not start a new speculative direction until the continuation state is sane.

`ADVANCE` is used when the state is clean enough to make progress.
Choose one useful increment that reduces uncertainty, completes a concrete obligation,
improves an artifact, or otherwise moves the long-horizon goal forward.
The increment should be sized so the run can finish with a clean handoff.

`BLOCKED` is used only when progress requires missing authority, unavailable external
access, or a real decision the agent should not invent.
A blocked state must name the exact blocker and the smallest human action that would
unblock the loop. Do not use `BLOCKED` merely because the next step is difficult.

`QUIESCENT` is used when the goal is currently satisfied or no useful autonomous
increment remains. The subagent should keep logs clean and avoid inventing busywork.
If the orchestrator continues launching runs, the run should cheaply confirm state and
exit with a clear note.

`CONSOLIDATE` is the closing mode for every non-aborted run.
Update the canonical state, clean stale notes, state the next continuation, and avoid
overclaiming.

The subskill may add task-specific states, but each added state must have a purpose,
entry evidence, exit evidence, and common failure mode.
Avoid more states than the task needs.
A five-state machine followed intelligently is better than a twelve-state checklist
followed mechanically.

## Autocorrecting behavior to encode in each subskill

Include explicit self-healing rules.
At minimum, tell the subagent to:

- Reconcile the status log against repository state before acting.

- Prefer fixing a partial previous run over starting a new branch of work.

- Correct stale or contradictory progress notes when discovered.

- Treat summaries from earlier subagents as hypotheses, not facts.

- Preserve useful unlogged work rather than discarding it to match the log.

- Avoid duplicating state files; merge accidental parallel logs into the canonical one.

- Leave a clean continuation note even when no substantive progress was possible.

- Record recurring behavioral failures as proposed subskill improvements, not as excuses
  to add broad speculative rules immediately.

Self-correction is not self-certification.
Do not ask the subagent to declare the loop correct.
Ask it to make the next state more coherent than the previous state.

## Avoiding overcompliance and undercompliance

Write instructions that reward progress and judgment, not ritual.

Signs of overcompliance:

- The subagent spends most of the run restating the state machine.

- It updates logs without improving the underlying work.

- It refuses useful action because the exact case is not listed.

- It performs every listed item even when some are irrelevant.

- It creates verbose reports, redundant files, or process artifacts to prove compliance.

- It treats the log format as more important than the task.

Signs of undercompliance:

- The subagent skips log reconciliation.

- It starts new work while previous partial work remains broken.

- It trusts a prior summary without checking files.

- It changes the repo but leaves no continuation state.

- It creates new scripts, metrics, or batch jobs despite instructions not to.

- It declares success without reducing an actual obligation.

Good behavior:

- It checks the minimum necessary state.

- It notices and repairs inconsistencies.

- It chooses a sensible bounded increment.

- It leaves the next run with less ambiguity.

- It explains deviations only when the deviation matters.

When revising a subskill, add only instructions that address observed failures.
Do not preemptively add rules for hypothetical problems; that is how skills become
compliance traps.

## Manual live-testing method

Use the repository’s existing skill/eval practice when available.
Otherwise use this live method.

Start with a barebones subskill.
Include the task goal, log location, state machine, and clean continuation rule.
Do not add a long list of prohibitions or edge cases before seeing actual agent
behavior.

Use minimal, trivial prompts for testing.
The test prompt should trigger the skill with the barest possible instruction—a single
sentence naming the task.
If you frontload the prompt with detailed directions, constraints, and expected
behaviors, you are testing the prompt, not the skill.
To measure whether the skill shapes behavior, give the agent only the task name and
observe what the skill causes it to do and avoid.

Reset context and clean up between trials.
Between tests, uniformize the environment: start a fresh agent session (no prior
transcript), remove or reset the status log and any artifacts produced by the previous
trial, and restore the repository to the same initial state.
If the agent can see debris from a prior evaluation—stale logs, leftover files, or a
transcript that hints at what happened—you are no longer testing the skill in isolation.
Scientific integrity requires that each trial begins from equivalent conditions.

Run single live trials with the subskill explicitly invoked.
Prefer weaker, cheaper, or lighter subagents during development unless a local
[[model-selection/SKILL|model-selection]] skill says otherwise.
Examples include small [[codex/SKILL|Codex]] configurations, free or low-cost OpenRouter models through
opencode, local/workhorse models, or whatever [[model-selection/SKILL|model-selection]] guidance the repo already
defines. The point is to find behavioral weaknesses before promotion, not to hide them
with the strongest available model.

Observe the transcript.
Actually read what the subagent did and why.
Do not rely on the subagent’s final summary, an artifact diff alone, or a claimed
pass/fail result. The transcript is evidence for the skill author, not material to paste
into the subskill. Use it to identify failure modes, then express fixes as normal
worker-facing rules about the artifact, state, or decision procedure.

Assess at least these dimensions:

- Did the skill trigger or get invoked correctly?

- Did the subagent begin by reconciling the status log with current state?

- Did it repair inconsistent or partial prior work when present?

- Did it make a meaningful bounded increment rather than merely reporting?

- Did it avoid scripts, batch jobs, automatic metrics, and self-certifying checks?

- Did it show judgment, or did it mechanically box-check?

- Did it leave concise, useful continuation state?

- Did it avoid inventing work when the loop was quiescent or genuinely blocked?

Test inconsistent states deliberately.
Create or simulate a stale log, a partial previous run, an unlogged repo change, or a
conflicting state note.
Then watch whether the subagent heals the state without being micromanaged.

After each observed failure, revise the subskill narrowly.
A correction belongs in the subskill only if it is grounded in actual observed behavior.
Prefer one precise sentence that changes behavior over a paragraph of generic cautions.
If the failure is caused by test harness mechanics, fix the harness or test notes
instead of teaching the worker about the harness.
If the failure reveals a durable artifact-quality requirement, encode that requirement
without mentioning the test run.

Repeat until multiple live trials show stable behavior.
The target is not perfect obedience; the target is convergent, thoughtful, self-healing
work.

## Promotion to cron, Hermes, or another orchestrator

Promote only after live trials show that the subskill works under direct observation.

The recurring integration should be trivial: launch the correct agent, from the correct
working directory, with the correct skill available, and capture transcripts.
Do not add a separate script that tries to decide whether the task succeeded.
Do not batch many runs to compensate for uncertainty.

After the first orchestrated launches, inspect transcripts again.
Confirm that no significant new behavior appears because of changed environment, missing
context, different working directory, different permissions, truncated instructions, or
model substitution. If orchestrated runs behave differently from live runs, return to
live testing and update the subskill or launch environment.

Recurring launch is deployment, not development.
Behavioral issues should be ironed out with monitored live subagents before the loop is
entrusted to cron/Hermes.

## Output standard when authoring a subskill

When your task is to create or revise a looped-task subskill, provide:

- The skill path and files created or changed.

- The canonical status/progress file path the subskill uses.

- The state machine and why it is no stricter than needed.

- The live-test prompts or scenarios to run.

- The transcript-observation rubric.

- Promotion criteria for recurring orchestration.

- Any local conventions discovered and followed.

Do not create scripts, cron entries, or orchestration configs unless explicitly asked
after the subskill has passed live observation.
Even then, keep orchestration separate from the subskill’s convergence logic.
