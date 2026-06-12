# Debugging Patterns Reference

Use this when the main skill says to reconcile working patterns, trace a failure backward, or stop after repeated failed fixes.

## Root-Cause Investigation Checklist

Before any fix:

- Read the full error, warning, stack trace, console log, stderr, and failing assertion.
- Record the exact reproduction command or user action.
- Check recent diffs, commits, dependency changes, config changes, and environment changes.
- Gather boundary evidence in the layer where the failure is observed.
- Trace the bad value, missing event, failed process, or wrong output back to its source.

Do not skip a diagnostic because it looks noisy.
Noise is often the only evidence that distinguishes two hypotheses.

## Multi-Component Boundary Pass

For systems with multiple layers, instrument all relevant boundaries in one run:

- Workflow or caller.
- Build script, server, command handler, or IPC boundary.
- Dependency call, renderer, database, subprocess, or external tool.
- Output artifact, served artifact, UI state, or final assertion.

At each boundary, record:

- Input.
- Normalized shape.
- Output.
- Environment or config source.
- Error object, stack, stderr, and exit code.

The purpose is to find where the first divergence occurs.
Only then investigate that component.

## Pattern Analysis

Find working examples before changing code:

- Similar working code in the same repo.
- A passing test exercising the same layer.
- A documented example from the dependency or framework.
- A generated artifact known to be correct.

Compare the working and failing paths:

- Inputs and file paths.
- Config resolution.
- Event sequence.
- Process lifecycle.
- Data shape and type.
- Output artifact.
- Error handling.

List every material difference.
Do not assume a difference is irrelevant until an experiment eliminates it.

## Red Flags

Stop and return to the ledger when any of these appear:

- "Just try changing X and see if it works."
- "One more test run" without a new observation.
- "It is probably X" without a falsifier.
- "I do not understand this, but the patch might work."
- Multiple changes are bundled before running the proof surface.
- A test is edited before proving the test was wrong.
- A type error, linter error, console error, or stderr output is hidden.
- A fallback is added to make the failure disappear.
- The same eliminated explanation returns without addressing the eliminating evidence.

## External Correction Signals

These user or reviewer prompts are hard stops:

- "Stop guessing."
- "Is that happening?"
- "Will it show us...?"
- "What would falsify this?"
- "Why are you running the same thing again?"
- "You are stuck."

When a signal appears:

- Add a contradiction or missing-observation row.
- State which claim lacked evidence.
- Design the smallest observation that would resolve it.
- Do not produce acknowledgment text as a substitute for the observation.

## Common Rationalizations And Required Responses

| Rationalization | Required response |
| --- | --- |
| "Issue is simple." | Record reproduction and the causal chain anyway. |
| "Emergency, no time." | Run the fastest discriminating experiment, not a guessed fix. |
| "Try this first, investigate later." | Write the hypothesis, prediction, and falsifier first. |
| "Multiple fixes save time." | Split into one causal mutation per experiment. |
| "Reference is too long." | Read the specific contract or source range that owns the behavior. |
| "I see the problem." | Show the fact row and inference chain. |
| "The test is probably bad." | Prove the test would fail without the bug before editing it. |

## Repeated Failed Fixes

If a fix fails:

- Stop.
- Mark the hypothesis weakened or eliminated.
- Record what the failed fix proved.
- Return to missing observations before another mutation.

After two failed fixes, rebuild the hypothesis set.
After three failed fixes, escalate architecture.

Architecture escalation is required when:

- Each fix reveals a different coupling or shared-state problem.
- The architecture cannot explain observed runtime behavior.
- Fixes require broad refactoring to preserve a local invariant.
- Tests only pass after the proof surface is weakened.
- A symptom moves rather than disappears.

State the architectural contradiction.
Do not call it a local bug until the architecture can explain it.

## Environmental Or External Causes

"External" is a conclusion, not a default.
Before claiming it:

- Show the local code path and data shape are correct.
- Show the external contract.
- Show the runtime observation violates or depends on that contract.
- Preserve diagnostics that would catch recurrence.
- State remaining uncertainty.

Most "no root cause" outcomes are incomplete investigations.
