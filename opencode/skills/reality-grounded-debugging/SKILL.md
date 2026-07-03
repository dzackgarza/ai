---
name: reality-grounded-debugging
description: Use when debugging, exploring unfamiliar repositories/APIs, handling build/test failures, or after any failed probe/fix where the agent may be reasoning from priors instead of observed data.
---

# Reality-Grounded Debugging

## Core Policy

Debugging must start from observed reality, not expected reality.

A local failure is not merely a thing to patch. It is evidence about missing observability, missing isolation, missing canonical recipes, missing logs, missing artifact dumps, missing fixtures, or missing proof loops.

Before patching a symptom, ask what debugging surface would have made the cause visible.

## Synthesis Gate

Before proposing or applying a fix, produce this statement internally and make it explicit in reports when nontrivial:

"The raw observation that changed my prior is ____.
The smallest reproducible surface is ____.
The missing or weak debugging surface is ____.
The fix will be verified through ____ rather than by repeating the original opaque failure."

If any blank cannot be filled with concrete command output, source text, logs, artifact paths, API responses, or test results, do not patch yet. Surface data first.

## Feedback Loop Quality Gate

The first substantive artifact for a bug is a tight, red-capable feedback loop: one
agent-runnable command, script, test, fixture, trace replay, browser script, or
measurement harness that has already been run and can catch the user's exact symptom.

Before hypothesizing, make the loop sharper:

- assert the specific symptom rather than no-crash success;
- isolate unrelated setup, global state, filesystem, network, and time;
- for flaky bugs, raise the reproduction rate with repetition, stress, pinned seeds or
  clocks, and narrowed timing windows;
- if the bug is performance, build a timing/profiling baseline before adding logs.

If no red-capable loop can be built, stop and report what was tried plus the missing
artifact, environment, trace, log, recording, or instrumentation permission needed. Do not
continue with code reading as a substitute for the loop.

## Observed Bug Protocol

When the user reports a project-owned bug, do not fix it first.
First construct a faithful red test or reproducer that fails because of the observed
bug.

The red proof must record:

- exact command or workflow run
- actual output, diff, exception, API response, or UI state
- why the failure is caused by the observed bug rather than by a guessed scenario
- the real owned boundary exercised by the test
- the class of missing test/QC surface that allowed the bug through

Mocks, simulations, stubs, and tests that assert on the absence of a proposed fix are
not bug proof.
If the test would still fail in a world where the user-reported bug did not exist, the
test is invalid.

Commit the red test before touching implementation code.
Only after the red proof is committed should implementation change begin, and the green
change should be a separate commit.

For dependency-owned symptoms such as compiler errors, provider/API failures, package
version mismatches, or external-library behavior, load `known-solution-first` while
building the reproducer.
Establish the public contract or known upstream failure before treating local code as
the explanation.

If the existing suite passed while the bug existed, treat that as a process failure:
identify the missing proof class and add the real boundary test before patching.

## Reality-First Discovery

When entering an unfamiliar repo, API, CLI, data format, or pipeline:

- First expose the actual shape.
- Then narrow.

**Split by ownership.** For project-internal code, "actual shape" means the local
directory, configs, entrypoints, and invocation chain. For external
tools/compilers/libraries/APIs, "actual shape" means the public contract — docs, release
notes, issues, known working examples — not the local cache or wrapper. Load
`known-solution-first` for the latter case.

Correct first moves for project-internal unknowns:

- `pwd`, `git status --short`, shallow `tree`/`find`/`fd`
- `just --list`, package scripts, Makefile targets, CI commands
- CLI `--help`, config files, entrypoints, source-of-truth wrappers
- API status, headers, schema/list/root endpoints, full redacted response bodies
- data shape dumps: top-level JSON keys, representative records, schema, raw error bodies

Do not begin by grepping for the symbol, flag, field, route, or file you expect to exist unless you have already surfaced the broader structure.

Inventories are evidence, not findings. Never report "many files" or "no grep hit" as a conclusion without structural interpretation.

## Command Output Discipline

Never hide the only evidence.

Forbidden as diagnostic evidence:

```bash
cmd --guessed-flag 2>/dev/null || echo "not found"
rg expected_string . || true
curl endpoint | jq '.expected.path'
test_command >/dev/null 2>&1
```

These commands replace system feedback with the agent's prior.

Required for diagnostic commands:

* preserve stdout
* preserve stderr
* preserve exit code
* preserve cwd and relevant environment/config
* show enough output to update the hypothesis
* treat empty output as data requiring interpretation, not as confirmation

Use `set -o pipefail` for shell pipelines. Use `tee` or explicit temp files when output matters.

## Local Failure → Surface Upgrade

After any failed fix, repeated failed probe, or "this might work" moment, stop and classify the missing surface:

* no exact reproduction command
* no isolated fixture
* no way to run one unit through the real pipeline
* no structured logs at the failing boundary
* no dump of intermediate artifacts
* no schema/data-shape inspection
* no source-of-truth command recipe
* no test that proves the owned behavior
* no visibility into subprocess arguments, cwd, env, or generated files

The next action should usually build or use that surface.

Do not keep mutating global application code to make one local symptom disappear.

## Canonical Isolation

An isolated reproducer must call the same source-of-truth code path as the global workflow.

Bad:

* one-off script that reimplements part of the pipeline
* direct CLI invocation with flags copied from memory
* fixture runner that bypasses filters/config/loaders used in production
* test that asserts on generated debris rather than the real output

Good:

* `render_one(path)` calls the same renderer as full build
* `compile_fixture(markdown)` writes a temp source and invokes the same Pandoc wrapper
* debug command dumps the exact command, env, cwd, input, output, stdout, stderr, and exit code
* API fixture uses captured real response shape at the repository-owned boundary

If no such seam exists, create the seam before fixing the bug when feasible.

## Pipeline Debugging Rule

For compilers, SSGs, document renderers, code generators, bundlers, and multi-stage transforms:

1. Run the canonical command once and capture raw failure.
2. Identify the source-of-truth invocation.
3. Add or use an isolated single-unit runner through the same invocation.
4. Dump intermediate artifacts at each owned boundary.
5. Reduce to a minimal representative fixture.
6. Fix the root cause.
7. Verify with the minimal fixture, the original failing unit, and the global test/build command.

Do not repeatedly run the entire pipeline as the only diagnostic. Do not mutate the full document/app while the failing boundary is still opaque.

## API/Data Debugging Rule

Before querying expected fields:

1. capture status and headers
2. dump the raw redacted body
3. inspect top-level shape
4. inspect representative records
5. identify the schema or contract if available
6. only then write targeted extraction code

A missing expected field is not evidence until the actual shape has been observed.

## Stop Rules

Stop patching and add/repair a debug surface when:

* two fix attempts have failed
* a command returns empty output unexpectedly
* stderr was suppressed
* a probe used a guessed flag/path/field/endpoint
* the fix requires changing global pipeline code before a minimal reproducer exists
* the agent cannot state what observation would falsify the current hypothesis
* the agent is about to violate any of the [Bridge-Burning Policies](file:///home/dzack/ai/opencode/skills/policy-index/SKILL.md#policy-registry) defined in `policy-index/SKILL.md` (e.g. adding a fallback, runtime default, mock, try/except, bypass comment, or legacy shim).

## Completion Evidence

A debugging task is not complete until the report includes:

* the original failure command and raw relevant output
* the root cause at the owned boundary
* the tight feedback loop command and why it is red-capable for this symptom
* the smallest reproducer or fixture, minimized until every remaining element is load-bearing
* the observability/isolation surface added or used
* the targeted verification result
* the global verification result
* any remaining unobservable boundary or known limitation

## Cross-References

Load alongside:

- `systematic-debugging` — hypothesis ledger, falsification, formal reasoning
- `known-solution-first` — external-tool/API/compiler problems: search public contract
  before local reverse-engineering. Required when the unknown is owned by an external
  project.
- `llm-failure-modes` — cognitive failure modes (premature solution, thrashing,
  prior-shaped inspection, tool output blindness, local-artifact laundering)
- `anti-slop` — implementation-quality analysis, patch accretion, myopic fixes
- **policy-index → Bridge-Burning Policies** — Any debugging activity must respect the [Bridge-Burning Policies](file:///home/dzack/ai/opencode/skills/policy-index/SKILL.md#policy-registry) defined in `policy-index/SKILL.md` as non-negotiable architectural constraints.
- `test-guidelines` — substantive assertions, owned-surface discipline
- `quality-control` — global QC as single source of truth, no-bypass policy
- `justfile` — recipe list as project API, source-of-truth commands
