# Template for a looped-task subskill

Copy and adapt this only after inspecting local repo conventions. Remove irrelevant sections. Keep the final subskill shorter than this template when possible.

```markdown
---
name: <loop-name>
description: Repeated one-shot loop for <specific long-horizon goal>. Use when a cron/Hermes/human-launched subagent should read <state-file>, reconcile current repository state, make one bounded increment of progress, and leave a clean continuation state. Do not use for ordinary one-off implementation tasks or deterministic scripts.
---

# <Loop name>

Use this skill for repeated one-shot agent runs that advance <goal>. Each run should improve the repository or task state and leave the next run with less ambiguity.

## Scope

Use when:

- <condition 1>
- <condition 2>

Do not use when:

- The user expects a deterministic script or batch job.
- The task has no persistent status/progress state.
- The requested work is an ordinary one-off edit unrelated to this loop.

## Canonical state

Canonical status file: `<path>`

Optional run notes: `<path or “none”>`

The status file is a fallible memory aid. The repository state is primary evidence. At the start of every run, compare the status file to actual files, issue state, or other relevant local evidence before acting.

Recommended status fields:

- Goal:
- Current state: `RECONCILE | RECOVER | ADVANCE | BLOCKED | QUIESCENT | CONSOLIDATE`
- Last observed repository state:
- Last meaningful action:
- Open obligations:
- Known inconsistencies:
- Next useful continuation:
- Blockers requiring human input:
- Last updated:
- Transcript pointer, if available:

## State machine

Treat states as decision modes, not a checklist.

### RECONCILE

Entry: every run starts here.

Read `<state-file>`, local instructions, and the minimum relevant repository state. Decide whether the previous continuation is accurate.

Exit to:

- `RECOVER` if the repo and state file disagree, a previous run is partial, or status docs are stale.
- `ADVANCE` if state is coherent and useful work remains.
- `BLOCKED` if progress requires missing authority/access/decision.
- `QUIESCENT` if the goal is currently satisfied or no useful autonomous increment remains.

Common failure: trusting the log or a previous summary without checking files.

### RECOVER

Entry: inconsistent state, stale log, partial previous run, duplicate status files, or broken handoff.

Repair the continuation state. Finish or clean up obvious partial work. Merge or correct status documents. Preserve useful unlogged work. Do not start a new direction until the state is coherent enough to continue.

Exit to `ADVANCE`, `BLOCKED`, or `CONSOLIDATE`.

Common failure: adding new work before fixing the broken handoff.

### ADVANCE

Entry: coherent state and useful autonomous work remains.

Choose one bounded increment that moves <goal> forward. The increment should reduce uncertainty, complete a concrete obligation, improve an artifact, or clarify the next continuation. Avoid large speculative rewrites.

Exit to `CONSOLIDATE` after the increment is complete enough for a clean handoff.

Common failure: reporting instead of doing, or starting more work than can be handed off cleanly.

### BLOCKED

Entry: progress requires missing external access, missing authority, or a decision the agent should not invent.

Record the exact blocker and the smallest human action that would unblock the loop. Do not mark blocked just because the next step is difficult.

Exit to `CONSOLIDATE`.

Common failure: vague blockers such as “needs review” without a concrete request.

### QUIESCENT

Entry: the goal is currently satisfied or no useful autonomous increment remains.

Avoid inventing busywork. Confirm the state cheaply, keep logs clean, and record what would make the loop active again.

Exit to `CONSOLIDATE`.

Common failure: creating process artifacts merely because the orchestrator launched another run.

### CONSOLIDATE

Entry: closing state for every non-aborted run.

Update `<state-file>` concisely. Record the current state, concrete progress, remaining obligations, known inconsistencies, and the next best continuation. Do not overclaim success.

Common failure: leaving a vague or stale continuation note.

## Self-correction rules

- Reconcile before acting.
- Fix partial previous work before starting new work.
- Treat prior summaries as hypotheses, not facts.
- Correct stale logs and merge accidental duplicate status files.
- Preserve useful unlogged work.
- Leave a clean continuation note even if no substantive progress was possible.
- Do not create scripts, batch launchers, automatic scoreboards, or self-certifying checks for this loop.

## Clean continuation standard

At the end of each run, a later subagent should be able to answer:

- What is the current state?
- What changed in this run?
- What remains open?
- What is the next useful action?
- Is anything inconsistent, blocked, or deliberately deferred?

## Live testing before recurring launch

Before cron/Hermes promotion, test this subskill with monitored one-shot runs.

Use weaker/lighter subagents when practical, unless local model-selection guidance says otherwise. Read the full transcript. Do not trust only final summaries or artifacts.

Minimum live scenarios:

1. Clean continuation state: the agent should advance the goal.
2. Stale status file: the agent should correct the log or reconcile it with repo state.
3. Partial previous run: the agent should recover before advancing.
4. Unlogged repo progress: the agent should preserve and incorporate it.
5. Quiescent or blocked state: the agent should not invent busywork.

Revise this subskill only in response to observed failures. Keep corrections narrow.

## Promotion criteria

Promote to recurring orchestration only when repeated live transcripts show:

- Correct invocation and skill use.
- Reliable start-of-run reconciliation.
- Resilience to inconsistent state.
- Meaningful bounded progress when possible.
- Concise clean handoffs.
- No new scripts, batch jobs, automatic metrics, or self-certifying success claims.
- No significant behavior changes under the intended launch environment.
```
