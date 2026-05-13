# Manual observation rubric for looped-task subskills

Use this rubric by reading the live subagent transcript. Do not rely on the subagent's summary, artifacts alone, or a computed pass/fail result.

The purpose is to discover behavioral corrections for the subskill. Record only corrections grounded in actual observed failures.

## Trial setup

Use single monitored runs. Prefer weaker, cheaper, or lighter subagents during development unless a local model-selection skill says otherwise. The point is to expose behavioral fragility before recurring deployment.

Run scenarios one at a time:

1. Normal clean continuation.
2. Stale status file.
3. Partial previous run.
4. Unlogged repository progress.
5. Duplicate or conflicting status notes.
6. Genuinely blocked state.
7. Quiescent state where no useful autonomous work remains.

## What to inspect in the transcript

### Invocation and context loading

Good:

- The subagent uses the intended skill.
- It notices local instructions and the canonical status path.
- It does not invent a different process.

Failure patterns:

- Skill does not trigger.
- Description is too vague or too broad.
- The agent misses local conventions.
- The agent starts work before reading required state.

Possible correction:

- Tighten the skill description or opening scope paragraph.
- Name the canonical status file earlier.
- Add one sentence requiring local instruction inspection.

### Reconciliation

Good:

- The subagent compares the log with actual repository state.
- It treats prior summaries as hypotheses.
- It notices stale, missing, or contradictory information.

Failure patterns:

- Trusts the log blindly.
- Skips file inspection.
- Repeats old status without checking reality.
- Creates a new status file instead of updating the canonical one.

Possible correction:

- Add or sharpen the start-of-run reconciliation rule.
- State that the repository is primary evidence and the log is fallible.

### Recovery behavior

Good:

- The subagent repairs partial previous work before starting new work.
- It merges duplicate state notes or corrects stale docs.
- It preserves useful unlogged work.

Failure patterns:

- Ignores an inconsistent state.
- Deletes useful work just because it was unlogged.
- Starts a new branch of work while prior work is broken.
- Reports a problem but leaves the handoff dirty.

Possible correction:

- Clarify the `RECOVER` state entry evidence and exit condition.
- Add a narrow self-correction rule for the observed inconsistency type.

### Progress quality

Good:

- The subagent chooses a bounded increment that materially advances the goal.
- It reduces an obligation, resolves uncertainty, or improves a target artifact.
- It sizes the work so it can consolidate cleanly.

Failure patterns:

- Merely summarizes or plans without acting.
- Starts a large speculative rewrite.
- Optimizes for visible activity rather than useful progress.
- Marks success without changing the state of the problem.

Possible correction:

- Define examples of meaningful increments for this specific loop.
- Add a warning against reporting-only runs when action is available.

### Overcompliance

Good:

- The subagent uses the state machine as orientation.
- It skips irrelevant ritual while preserving the key behavior.
- It explains deviations briefly when they matter.

Failure patterns:

- Restates every state and rule instead of working.
- Performs irrelevant steps to prove compliance.
- Bloats the log with process language.
- Refuses useful work because the exact case is not enumerated.

Possible correction:

- Replace procedural checklists with decision-mode language.
- Add “progress over ritual” wording.
- Remove low-value rules that caused box-checking.

### Undercompliance

Good:

- The subagent follows the core behavior even when details are not prescribed.
- It leaves a clean continuation state.

Failure patterns:

- Skips reconciliation.
- Leaves no status update.
- Invents scripts, metrics, or batch jobs.
- Trusts its own final summary as proof.
- Fails to recover from inconsistent state.

Possible correction:

- Add one precise rule for the missed core behavior.
- Move critical instructions earlier in the skill.

### Consolidation and handoff

Good:

- The state file is concise and concrete.
- It names current state, actual changes, remaining obligations, known inconsistencies, and next continuation.
- It avoids overclaiming.

Failure patterns:

- Vague “continue improving” notes.
- No explanation of what changed.
- Missing blockers or unresolved inconsistencies.
- Long diary-style logs that obscure the next action.

Possible correction:

- Provide a compact status-field template.
- State that logs are continuation aids, not diaries.

### Orchestrated launch behavior

Good:

- Cron/Hermes launches the same skill from the right working directory.
- Transcripts are captured and inspectable.
- The subagent behaves like it did in live trials.

Failure patterns:

- Different environment mutates context or cwd.
- Skill is not available or not invoked.
- Permissions change the agent's behavior.
- No transcript is available, so behavior cannot be audited.

Possible correction:

- Fix launch cwd, prompt, model-selection, or skill path.
- Do not compensate by adding batch runs or automated success scripts.

## Scoring without automation

Do not convert this rubric into a script or scoreboard for the loop. A small handwritten trial note is enough:

- Scenario:
- Model/subagent:
- Transcript pointer:
- Observed behavior:
- Overcompliance/undercompliance signs:
- Convergence/self-healing signs:
- Correction to skill, if any:
- Ready for another live trial? yes/no

The only durable output should be targeted skill edits grounded in observed behavior.
