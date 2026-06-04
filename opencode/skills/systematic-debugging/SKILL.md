---
name: systematic-debugging
description: 'Use when debugging any failure: forces visible hypothesis ledger, falsification,
  contradiction handling, and proof before fixes.'
license: MIT
metadata:
  hermes:
    tags:
    - debugging
    - troubleshooting
    - problem-solving
    - root-cause
    - investigation
    related_skills:
    - test-driven-development
    - writing-plans
    - subagent-driven-development
---

# Systematic Debugging

## Contents

- Iron Law
- When To Use
- Visible Ledger
- Operating Gates
- Formal Reasoning Rules
- Pattern And Contract Reconciliation
- Instrumentation Standards
- Bias Countermeasures
- Fix And Failed-Fix Gates
- Supporting References
- Forbidden Behaviors
- Minimal Response Format

## Iron Law

```
NO FIX WITHOUT A VISIBLE CAUSAL CASE
```

Private reasoning is not debugging evidence.
Before changing code, tests, config, processes, fixtures, timeouts, assertions, or project structure, create a visible debugging ledger in the task artifact, issue, PR comment, or local scratchpad.
If the user has not asked for a durable repo artifact, use a temporary scratchpad path and quote the relevant parts in the response.

The ledger must contain enough structure that another agent can inspect the reasoning, find contradictions, and continue without reading private chain-of-thought.
If a conclusion is not written in the ledger with its evidence and inference path, it is not established.

## When To Use

Use this for any bug, failed test, build failure, performance anomaly, flaky behavior, unexpected runtime state, failed fix, or problem with multiple unknowns.

Load `test-driven-development` before fixing a user-reported bug.
If project rules require a committed red test before any fix, that rule controls.
This skill governs the root-cause investigation after the failure is observable.

Use this especially when:

- A fix seems obvious before evidence has been gathered.
- A test has been run repeatedly without new observations.
- You have already tried one fix.
- The system has multiple layers, processes, configs, event paths, or external tools.
- You are relying on a memory of how a dependency, test adapter, framework, or CLI works.
- You catch yourself circling back to the same explanation.

## Visible Ledger

Create or update the ledger before the first experiment.
Do not keep these items only in private reasoning:

```markdown
## Problem
- Symptom:
- Exact command, input, or user action:
- Expected behavior:
- Actual behavior:
- Reproduction status:

## Observations
| ID | Observation | Source | Direct fact or inference |
| --- | --- | --- | --- |

## Data Shape
| Boundary | Actual value / schema / sample | How inspected |
| --- | --- | --- |

## Contracts And Patterns
| ID | Source | Contract or working pattern | Difference from failing path |
| --- | --- | --- | --- |

## Facts, Assumptions, And Inferences
| ID | Statement | Kind: fact / assumption / axiom / inference / speculation | Source or inference rule |
| --- | --- | --- | --- |

## Hypotheses
| ID | Hypothesis | Prediction if true | Falsifier | Status |
| --- | --- | --- | --- | --- |

## Experiments
| ID | Hypothesis tested | Observation to collect | Expected if true | Expected if false | Result | Eliminated |
| --- | --- | --- | --- | --- | --- | --- |

## Contradictions
| ID | Claims in conflict | Why both cannot be true | Resolution |
| --- | --- | --- | --- |

## Eliminations
| ID | Eliminated hypothesis or axiom | Falsifying observation | What this implies |
| --- | --- | --- | --- |

## Current Causal Case
- Proven facts:
- Eliminated hypotheses:
- Active hypotheses:
- Inference chain:
- Confidence:
- Gaps:
```

Every conclusion must point to rows in the ledger.
If a claim has no row, it is not established.

## Operating Gates

Move through these gates in order.
If a later observation contradicts an earlier claim, return to the contradiction gate before continuing.

### Establish The Failure

Do this before diagnosing:

- Record the exact failing command, UI action, input file, request, environment, and observed output.
- Preserve complete stderr, stack traces, console errors, logs, screenshots, artifacts, and exit metadata.
  Do not suppress stderr or replace it with synthetic text.
- State whether the failure is reproducible, intermittent, or not yet reproduced.
- If a command times out, record what was still running, what output existed, and whether the timeout came from the tool wrapper or the system under test.
- If the failure involves external tools or libraries, read the local docs, upstream docs, CLI help, source, or generated artifacts that define the behavior before asserting a contract.

Do not proceed if the only evidence is a summary, a passing unrelated test, a missing string, a hunch, or a single stale artifact.

### Inspect Real Data Shape

Before writing code that handles data, inspect the actual data at the boundary where it enters the system.

Required moves:

- Print or log the exact runtime value, type, keys, discriminants, path, status code, and length where relevant.
- Prefer structured inspection: JSON parser, schema dump, AST, DOM snapshot, database query, typed debugger, process tree, or protocol trace.
- Record both the raw observation and the normalized shape you believe the code should accept.
- Convert weakly typed guesses into explicit accepted shapes before implementing.
- If the data shape is unknown, stop at instrumentation.
  Do not write handler logic for imagined shapes.

Forbidden moves:

- Probing only the path that already fits the current theory.
- Inferring a whole data contract from one field or one successful call.
- Treating "not found" from a narrow search as proof that a concept does not exist.
- Adding `Any`, `unknown`, broad optionals, catch-all parsing, fallback defaults, or graceful acceptance of malformed data to make uncertainty disappear.

### Trace Back To The Source

When the failure appears deep in a call stack, event chain, subprocess tree, render pipeline, or test harness:

- Identify where the bad value, missing event, unexpected state, or wrong process state is first observable.
- Walk backward one boundary at a time.
- Record the caller, input, output, and invariant at each boundary.
- Stop only when the origin is observed or when the next boundary to inspect is explicit.
- Fix at the origin, not where the symptom happens to crash.

Do not add guards at the crash site unless the ledger proves the crash site owns the invariant.

### Reconcile Contracts And Working Patterns

Before asserting how something should work:

- Find a documented contract in local docs, upstream docs, CLI help, source, generated code, schema files, or checked-in working examples.
- Find at least one similar working path in the same codebase when one exists.
- Compare failing and working paths field by field, event by event, command by command, or process by process.
- List every material difference.
- Do not dismiss a difference as irrelevant until an observation eliminates it.

This gate preserves useful content from older debugging practice: pattern comparison is not a fix generator.
It is an evidence source that produces hypotheses and falsifiers.

### Build Competing Hypotheses

Before the first fix attempt, list at least two live hypotheses unless the failure is mechanically proven by a direct stack trace.

Each hypothesis must have:

- A precise causal statement.
- A prediction that would be observed if it is true.
- A falsifier that would eliminate it.
- The smallest observation that distinguishes it from at least one competing hypothesis.

Use this language:

- `Fact`: directly observed or read from a source.
- `Inference`: follows from stated facts.
- `Hypothesis`: plausible but unproven.
- `Speculation`: not yet connected to an observation.

Deduction eliminates hypotheses.
Abduction generates hypotheses.
Never treat the best available explanation as proven merely because it explains the observations.
Do not write "the only explanation" while any live hypothesis lacks a falsifier or any observed fact remains unexplained.

### Design Information-Gain Experiments

An experiment is valid only if it can eliminate or strengthen a specific hypothesis.
Rerunning a command unchanged is not an experiment unless the hypothesis is about reproducibility or flakiness.

Before running an experiment, add this to the ledger:

- Which hypothesis it tests.
- Which exact observation it will collect.
- What result is expected if the hypothesis is true.
- What result is expected if the hypothesis is false.
- What action will be taken for each outcome.

Prefer observations over mutations:

- Add boundary logs before changing behavior.
- Capture event traces before replacing event mechanisms.
- Inspect process trees before killing processes.
- Inspect resolved config before editing config.
- Inspect parsed data before changing parsers.
- Inspect generated output before editing generators.

Run one experiment at a time.
Do not change code and test configuration in the same experiment.
Do not add a workaround while diagnostics are still active unless the ledger states that the workaround itself is the experiment.

### Update Beliefs After Each Observation

After every experiment:

- Mark each affected hypothesis as `proven`, `eliminated`, `weakened`, `active`, or `invalid`.
- Record what the result implies.
- Remove or revise inferences whose premises are now false.
- Check whether any assumption or axiom must be proved, weakened, or discarded.
- Check whether the observation creates a contradiction.

Elimination is progress.
If an experiment does not change any hypothesis status, record it as a low-information observation and design a sharper experiment.

### Contradiction Gate

When two recorded claims cannot both be true, stop all fixes.

Required response:

- Add a contradiction row.
- State which claim is a fact, which is inference, which is assumption, and which is speculation.
- Identify the observation that would resolve the conflict.
- Run only that observation.
- Revise or delete the invalid inference in the ledger.

Examples of hard-stop contradictions:

- A trace says a function was not called, but a downstream-only state change happened.
- A test is said to reproduce a bug, but it would fail even if the bug did not exist.
- A process is said to be dead, but its child is still running.
- A type is said to be impossible, but real runtime data has that shape.
- A config is said to be loaded, but the runtime uses default values.
- A hypothesis is marked eliminated, then used again as the current explanation.

Do not patch around a contradiction.
Contradictions mean the model of the system is wrong.

## Formal Reasoning Rules

Use explicit reasoning labels:

- `fact`: directly observed in output, logs, source, docs, runtime data, or debugger state.
- `assumption`: temporarily accepted because the next experiment needs it.
- `axiom`: an assumption introduced specifically to derive a contradiction or eliminate a branch.
- `inference`: conclusion drawn from facts or assumptions by a named rule.
- `hypothesis`: possible causal explanation with predictions and falsifiers.
- `speculation`: idea not yet attached to evidence.

Use valid inference patterns:

- Modus ponens: if `P implies Q`, and `P` is true, infer `Q`.
- Modus tollens: if `P implies Q`, and `Q` is false, infer `not P`.
- Chain reasoning: if `P implies Q`, and `Q implies R`, infer `P implies R`.

Do not use invalid patterns:

- Affirming the consequent: `P implies Q`, `Q`, therefore `P`. This is invalid because other causes may produce `Q`.
- Denying the antecedent: `P implies Q`, `not P`, therefore `not Q`. This is invalid because `Q` may have other causes.
- Correlation as mechanism: two events move together, therefore one caused the other.
- Absence from a narrow search as nonexistence.
- Plausibility as proof.

For axioms:

- Mark them explicitly.
- State what contradiction or elimination they are meant to enable.
- Reduce them to facts before relying on them in the final causal case.
- If an axiom cannot be proved, keep the final confidence limited and state the gap.

## Pattern And Contract Reconciliation

Use documentation and working examples to increase information, not to confirm a preferred story.

Required sources, when available:

- Full stderr, stack traces, console errors, and logs.
- Local README, AGENTS, config schemas, generated files, and checked-in examples.
- Upstream docs, CLI help, source, or issue tracker for dependency-owned behavior.
- A working example in the same codebase that exercises the same layer.
- Recent diffs or commits that changed the failing area.

Record each source in the ledger.
If a source is not read completely enough to support a claim, write the claim with that limitation.

Standard comparison questions:

- What exact value, event, path, state, command, or process differs?
- Which layer first diverges from the working path?
- Which dependency contract is being relied on?
- Which assumption would be false if the working path and failing path were both correct?
- What observation would decide whether the difference matters?

## Instrumentation Standards

Use instrumentation that increases observable information instead of reducing it.

For multi-layer systems, log every boundary in one run:

- Caller action and arguments.
- Event handler entry and exit.
- Request or IPC command name and payload.
- Normalized data shape.
- Dependency call and returned status.
- State before and after mutation.
- Error object, stack, stderr, and exit code.

For browser/UI bugs:

- Log whether the DOM event fired.
- Log whether the framework handler entered.
- Log whether async work started and resolved.
- Log state before and after the event.
- Capture DOM snapshots, accessibility tree, screenshots, and console errors when relevant.
- Avoid fixed sleeps.
  Wait on a specific state transition, event, promise, process exit, file change, or log line.

For process/lifecycle bugs:

- Record parent PID, child PID, process group, command line, cwd, and environment source.
- Observe the tree before and after the lifecycle event.
- Send no kill signal as a diagnostic shortcut unless the experiment is explicitly about signal handling.

For type/config/build failures:

- Run typecheck and lint with full diagnostics.
- Do not hide type errors with `as any`, `@ts-ignore`, `@ts-nocheck`, weakened unions, or optional fields.
- If the type system rejects the code, either prove the type declaration is wrong from docs/source or fix the code/data shape.

For generated-output or render bugs:

- Capture the source input, normalized intermediate representation, generated output, served output, and runtime-rendered output.
- Compare generated artifacts against served artifacts before blaming runtime code.
- Do not edit templates, filters, serializers, or renderers until the boundary that first corrupts output is known.

### Debugging Surface Check

If evidence gathering requires guessed commands, repeated whole-system runs, stderr suppression, manual inspection of generated debris, or mutation of global code before isolation, the system lacks a debugging surface.

Before proposing a fix, add or use the smallest canonical surface that reveals the failing boundary:

- structured boundary logging
- exact command/env/cwd dump
- intermediate artifact dump
- one-unit runner through the real pipeline
- captured real API/data fixture
- schema/shape dump
- regression test at the repository-owned boundary

A local failure should improve future diagnosability. Do not spend multiple attempts probing the opaque global workflow.

## Bias Countermeasures

Bias names are not useful unless they force different behavior.
Apply these structural countermeasures:

- Confirmation bias: every hypothesis needs a falsifier before it can be tested.
- Congruence bias: generate competing hypotheses before testing the favored one.
- Anchoring and availability: re-read the actual error, logs, docs, and data shape after each failed experiment.
- Belief bias: label every statement as fact, assumption, axiom, inference, hypothesis, or speculation.
- Sunk cost and plan continuation: after a failed fix, ask whether the current approach would be chosen from scratch with the new evidence.
- Status quo and endowment bias: treat old code, new code, your code, and generated code as equally suspect.
- Illusion of explanatory depth: write the causal chain in the ledger before claiming understanding.
- Law of the instrument: choose the observation that distinguishes hypotheses, not the tool that is most familiar.
- Additive bias: prefer removing false assumptions, narrowing types, or deleting wrong branches over adding fallbacks.
- Outcome bias: a green test does not prove the diagnosis unless the test would have failed for the original root cause.

External correction signals are hard stops.
If the user, reviewer, or another agent says "stop guessing", "is that happening?", "will it show us", "what would falsify this", or otherwise points to missing evidence, return to the ledger and add the missing observation or contradiction before continuing.

## Fix Gate

No implementation fix is allowed until the ledger contains:

- Reproduction evidence.
- Actual data shape or runtime state at the failing boundary.
- Contract or working-pattern comparison when a comparable source exists.
- At least one eliminated competing hypothesis.
- No unresolved contradiction.
- A causal chain from facts to root cause.
- A test or proof surface that will fail for the root cause, not merely for absence of the intended fix.

The fix must change one causal factor.
Do not bundle refactors, cleanup, formatting-only changes, test rewrites, dependency changes, and behavior changes unless the ledger proves they are the same causal factor.

For user-reported bugs:

- Create the red test or proof surface before fixing when project policy requires it.
- The test must fail because the bug exists, not because the proposed fix is absent.
- A mock proves only the mock unless the ledger proves the mock is observing the same boundary as the real failure.

## Failed-Fix Gate

If a fix fails:

- Do not add another fix on top.
- Mark the hypothesis as eliminated or weakened.
- Record what the failed fix proved.
- Reopen the ledger at the contradiction or missing-observation point.

After two failed fix attempts, stop implementation and return to hypothesis construction.
After three failed fix attempts, report that the architecture or diagnosis is not understood and ask for review before further mutation.

Architecture escalation is required when:

- Each fix reveals a different shared-state, coupling, lifecycle, or data-shape problem.
- The fix requires broad refactoring to make a local invariant hold.
- One fix creates symptoms elsewhere.
- The tests can only be made green by weakening the proof surface.
- The intended architecture cannot explain the observed runtime behavior.

Do not call an architecture problem a failed hypothesis.
State the architectural contradiction and stop for review.

## Supporting References

Load these only when the main procedure needs more detail:

- [debugging-patterns.md](references/debugging-patterns.md): older root-cause debugging checklist, red flags, pattern-analysis prompts, correction signals, and architecture-escalation criteria.
- [deductive-reasoning.md](references/deductive-reasoning.md): formal hypothesis ledger mechanics, proof labels, inference rules, axioms, fallacies, and worked experiment structure.
- [cognitive-biases.md](references/cognitive-biases.md): large bias catalog for postmortems or difficult investigations where a specific bias needs naming.

## Forbidden Behaviors

These are process violations:

- Running the same failing test repeatedly while expecting insight to appear.
- Changing code because a theory "seems likely" before writing predictions and falsifiers.
- Making multiple simultaneous changes and then asking which one helped.
- Adding sleeps instead of waiting for a named event or state.
- Killing processes, clearing caches, restarting services, deleting artifacts, or changing ports as a way to avoid understanding lifecycle state.
- Suppressing stderr, console output, type errors, linter diagnostics, stack traces, or failed command output.
- Replacing diagnostics with synthetic fallback output.
- Editing tests to match current behavior before proving the test was wrong.
- Treating mocks, probes, or monkey patches as evidence before proving the instrumentation itself observes the real path.
- Converting hard failures into graceful fallbacks.
- Replacing strict types with broad types to make diagnostics disappear.
- Declaring root cause from a single compatible observation.
- Continuing after a contradiction because a nearby workaround appears to pass.
- Re-proposing an eliminated hypothesis without explaining which eliminating evidence was wrong.
- Treating "no root cause found" as a conclusion before the ledger shows contract checks, data-shape inspection, competing hypotheses, and eliminations.
- Bypassing documented project test commands to get a faster but weaker signal.

When the issue appears environmental, timing-dependent, or external, the standard is higher, not lower.
Document the evidence that local code is not the source, the external contract involved, the monitoring or diagnostic signal that will catch recurrence, and the remaining uncertainty.

## Minimal Response Format

When reporting debugging progress, lead with blockers and evidence:

```markdown
## Current causal case
- Root cause status: proven / likely / unknown
- Proven facts:
- Assumptions or axioms still unproved:
- Eliminated hypotheses:
- Active hypotheses:
- Contradictions:
- Contract or pattern sources checked:
- Next experiment:
```

Do not report "fixed" until the proof surface that reproduces the original failure is green and no contradictions remain.

For a negative finding, use the project epistemic format:

```markdown
- Searched:
- Found:
- Conclusion:
- Confidence:
- Gaps:
```
