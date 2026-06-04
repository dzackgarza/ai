---
name: test-guidelines
description: 'Use any and every time you interact with a test file, period.'
---
Note: if you are working with a PR, read the adjacent pr-guide.md file.

# HIGH-QUALITY TESTING STANDARDS (GUIDELINES)

**MANDATORY FIRST STEP: You MUST read this entire file before taking ANY action.
This is the source of truth for all test work.**

## Core Principle

A test is not a pile of evidence.
A test proves a **nontrivial functional claim** about behavior that this repository
owns.

The question is not:

- “How many tests are there?”

- “How much coverage is there?”

- “Can more assertions be added?”

The question is:

- **“What functionality does this project truly own, and which tests prove that
  functionality works?”**

* * *

## What the Repository Owns

Before writing or judging tests, identify the project’s owned surface area.
A repository typically owns:

### 1. Domain Logic

- Calculations and transformations

- Parsing rules and decision procedures

- Reconciliation / merge logic

- Normalization and routing rules

- Policy enforcement

### 2. Boundary Logic

- How it interprets external inputs

- How it maps dependency outputs into project semantics

- How it handles failures at boundaries

- How it preserves its contract when interlocking with other systems

### 3. Public Contract

- CLI behavior and output schema

- File format and exported API behavior

- Observable state transitions

**Tests should primarily target these owned areas.**

## What the Repository Does NOT Own

Do not test behavior whose correctness is owned elsewhere, unless the repository adds
nontrivial logic on top:

- **Language correctness** — basic arithmetic, list semantics, string slicing,
  exceptions

- **Type-system / schema internal consistency** — field storage, constructor validity

- **Dependency correctness** — framework serialization, ORM/HTTP/parser behavior

- **Private implementation trivia** — helper internals with no external contract

If a test mainly checks one of these, it is out of scope.

* * *

## The Owned-Surface Test

Before keeping or writing a test, ask:

1. What exact behavior is being claimed?

2. Is that behavior owned by this repository?

3. If the test fails, would that reveal a defect in this repository rather than in the
   language, framework, or dependency?

4. Is the claim nontrivial enough that a defect could realistically exist here?

**If the answer to 2 or 3 is no, the test is usually not justified.**

* * *

## What Makes a Test Substantive

A substantive test proves one of the following:

1. **Nontrivial transformation** — Repository converts inputs to outputs according to
   repository-specific rules

2. **Boundary interpretation** — Repository correctly interprets external data or errors
   into its own semantics

3. **Interlocking correctness** — Repository correctly composes with a dependency at the
   point where project-owned behavior begins

4. **Contract preservation** — Repository produces promised observable result (CLI
   output, API output, file, status code, state transition)

5. **Failure semantics** — Repository handles invalid/missing/conflicting inputs
   according to its own rules

A substantive test should fail if the repository’s real logic is wrong, not merely if
surrounding scaffolding changes.

* * *

## What Makes a Test Trivial

A test is usually trivial if it mainly shows that:

- An object can be instantiated

- Fields round-trip through a framework

- A dependency serializes or validates correctly

- A private helper returns what its own code directly spells out

- A list is nonempty or a value is not `None`

- A type matches an obvious annotation

- A standard library or framework feature behaves normally

These may be true statements, but they usually do not prove repository-owned
functionality.

* * *

## Operating Rules (Hard Constraints)

1. **Action-First** — Execute tool calls BEFORE any explanation.

2. **Split by ownership in initial investigation** — For project-internal unknowns,
   start with `tree`/shape inspection. For external tool/API/compiler unknowns, load
   `known-solution-first` and search public contracts first. Do not force a rigid
   parallel tool-call pattern — use the appropriate model for the uncertainty type.

3. **REQUIRED: Reference Skills** — Strictly follow `prompt-engineering`,
   `agent-orchestration`, and the guidelines below.

4. **No Masking** — All tests must reflect actual runtime state (no `xfail`, no
   `ignore`).

5. **Substantive Assertions** — Every test MUST prove a nontrivial fact; reject
   “content-free” checks.

* * *

## Role

You are a **Verification Architect & Auditor**. You engineer tests that act as proofs of
correctness and audit existing tests to ensure they meet high-fidelity standards.

## Context

### Reference Skills

This agent must follow these standards:

- **prompt-engineering** — Standard for prompt architecture and rule-based behavior.

- **agent-orchestration** — Standard for multi-agent coordination.

- **clean-code** — Standard for test readability and maintenance.

* * *

## High-Quality Testing Standards

### 1. Substantive Assertions (No Content-Free Checks)

- **Reject Triviality**: Primary assertions like `is not None`, `len(x) > 0`, or
  `isinstance()` (unless the type IS the contract) are strictly disallowed.

- **Prove a Fact**: Every test must assert a meaningful identity, invariant, or
  equivalence (e.g., `L.discriminant() == expected`).

- **Nontrivial Witnesses**: Never use zero values, empty structures, or identity
  elements as primary witnesses.
  Use representative, “real-life” examples.

- **Direct Assertions (No Ceremony)**: Avoid synthetic tuple wrappers or helper pairs.
  Assert relations directly with explicit diagnostics.

### 2. Correctness via Identities & Invariants

- **Prefer Invariants**: Assert preservation of properties like determinant, rank,
  signature, or discriminant.

- **Verify Laws**: Check algebraic identities (polarization, duality, reciprocity,
  involution).

- **Collections**: For lists, assert at least one item is the expected canonical object,
  or all items satisfy the defining invariant.

- **No Tautologies**: Avoid checks that show only internal consistency (e.g., “group
  order equals cardinality”). Use known truths (e.g., `Z/5ZZ.order() == 5`).

- **Independent Oracles**: Strengthen interface-consistency checks with independent
  oracle assertions.

### 3. Strict Prohibitions (Zero Tolerance)

- **NO MOCKS/SIMULATIONS**: Never use `unittest.mock`, `monkeypatch`, `patch`, stubs,
  fakes, or simulated environments.
  All tests must operate on real data and real objects.
  No exceptions. A mock-based test proves only that you wrote code that calls the mock —
  it says nothing about whether the real system works.
  Every hour spent on mock infrastructure is net-negative: the tests pass, the system is
  unproven, and the mocks must now be maintained.

- **NO MASKING**: Never use `pytest.mark.xfail`, `pytest.mark.skip`, or
  `pytest.mark.skipif`. Suite status must reflect 100% actual runtime reality.
  `skipif` deserves special attention: it is almost always a hedge against a dependency
  not being installed or a service not being running.
  That is a *setup problem*, not a test design problem.
  Hard dependencies must be present; if they are not, the system is broken and the suite
  should fail loudly, not silently pass.

- **NO COVERAGE SUPPRESSION**: Never add `# pragma: no cover` to production code.
  Coverage gaps are diagnostic signals, not noise to silence.
  If a branch is flagged as uncovered, the correct responses are: (a) write a test that
  covers it, (b) delete the branch if it is genuinely unreachable given the system’s
  invariants, or (c) replace it with an `assert False` / `raise AssertionError` that
  documents the invariant explicitly.
  The only legitimate use of `# pragma: no cover` is entry-point boilerplate
  (`if __name__ == "__main__"` in `__main__.py`) that is structurally impossible to
  exercise in-process.

- **NO IMPOSSIBLE-CONDITION TESTS**: Do not test error conditions that cannot occur at
  runtime given the system’s hard dependencies and invariants.
  If `notify-send` is a required tool that `doctor` verifies on startup, writing a test
  for `FileNotFoundError: notify-send` is testing a condition that will never exist in
  production. It produces passing tests for behavior that is never exercised, creates
  maintenance burden, and gives false confidence.
  The regression rule applies: only add error-handling tests for specific,
  previously-observed failures.

- **NO STRING MATCHING**: Never assert on error message strings.
  Use `pytest.raises(TypeError)` or similar to assert on the **TYPE** of error received.

- **Expose Silent Errors**: Tests must be designed to catch swallowed or silent errors
  (e.g., empty catch blocks or hidden exceptions).

### 4. Coverage, Triage & Anti-Obfuscation

- **Algorithm-First**: Cover every interesting algorithm, not just basic APIs.

- **Optional Package Pass**: Explicitly enumerate and triage add-on libraries/optional
  packages.

- **Hidden Surface Pass**: Audit blacklists and parent APIs for interesting algorithms
  that may be omitted by narrow filters.

- **Generic vs. Specialized**: Exclude generic linear algebra unless specialized to a
  nonstandard domain or semantics.

### 5. Performance, Scale & Spec-First

- **Runtime**: Tests should typically take `< 30 seconds`.

- **Representative Scale**: Favor many small/medium representative objects over one
  massive complex one (e.g., 20 rank 4 lattices > 1 rank 20 lattice).

- **Typical Inputs Focus**: Ensure a wide range of typical inputs work flawlessly;
  handle known failure modes correctly.
  Do not probe edge cases at the expense of typical reliability.

- **Real Data & Results**: Whenever possible, perform end-to-end tests on real data that
  produce expected results.
  Avoid synthetic inputs.

- **Tests as Spec**: Tests define and record the **SPECIFICATION**, not just current
  behavior. Do not base tests on existing implementation quirks.

- **Anti-Junk Rule**: Tests must be specific enough to fail if the implementation
  returns arbitrary non-empty junk.

* * *

## Boundaries and Edges

A project often depends on frameworks, libraries, databases, external APIs, files, the
OS, and language/runtime features.

**Tests should focus on the edge where repository logic meets these systems.**

Examples of edge testing:

- Given a real or captured external response, the repository derives the correct domain
  objects

- Given a dependency error, the repository emits the correct repository-defined failure

- Given a real config or file layout, the repository resolves the correct behavior

- Given external data in a representative form, the repository produces the correct
  public output

This is different from testing whether the external system itself works.

* * *

## Interlocking Rule

When external code is involved, test only the project-owned interlock.
Do not test whether the dependency is correct in general.

**Do test:**

- Whether this repository calls it correctly

- Whether this repository interprets its output correctly

- Whether this repository preserves its own contract at that boundary

The test target is: **“our adapter / parser / mapper / handler is correct,”** not **“the
dependency is correct.”**

* * *

## Evidence Rule

More tests do not automatically mean more proof.
A suite becomes low-value when many tests restate the same claim in shallow ways.

**Prefer:**

- Fewer tests

- Each tied to a distinct owned guarantee

- Each with substantive assertions

- Each capable of falsifying a real defect

**Do not optimize for:**

- Raw test count

- Coverage theater

- Duplicated variations

- Many weak assertions instead of one decisive proof

* * *

## Behavioral and Competence Evaluation Tests

When tests are evaluating an LLM or agent rather than ordinary repository code, the
owned behavior is the agent’s response to the task frame.
The test must therefore prove a behavioral claim: generalization beyond visible
examples, resistance to red herrings, correction localization, evidence-based review, or
instruction adherence.

Use adversarial, property-based, and metamorphic cases when the failure mode is test
gaming. Visible examples alone are not enough: they train the agent toward the answer
shape. The benchmark must contain checks that a hard-coded, pattern-matched, or
report-shaped solution will fail.

The local fixture source for these tests is
`model-selection/model-strength-testing/behavioral-evaluations/`.

* * *

## Assertion Rule

Assertions should express the nontrivial claim being proven.

**Prefer:**

- Exact transformed values

- Exact contract output

- Exact interpretation of representative external input

- Exact failure behavior

- Exact repository-owned semantics

**Avoid primary assertions like:**

- `is not None`

- `len(x) > 0`

- “returns a list”

- “serialization succeeded”

- “field equals constructor input” (when that is merely framework storage)

* * *

## Representative-Input Rule

Use inputs that are representative of the real boundary the repository handles.
This may include:

- Real runtime data

- Captured external responses

- Representative files

- Real command invocations

- Minimal fixtures that preserve the real structure at the boundary

The key property is not “realism” for its own sake, but that the test proves
repository-owned behavior at a real edge.

Avoid synthetic inputs that bypass the boundary so completely that the repository’s
actual interlocking logic is no longer being tested.

* * *

## Test-Audit Procedure

When reviewing a suite, classify each test:

1. **Owned substantive** — Proves repository-owned nontrivial behavior

2. **Boundary/interlock** — Proves correct interaction at an owned edge

3. **Redundant** — Repeats an already-proved claim without adding a new owned guarantee

4. **Dependency-owned** — Tests a framework, library, runtime, or language feature
   rather than repository logic

5. **Type-system/internal-consistency** — Checks invariants already guaranteed by the
   type system, schema system, or obvious structure

6. **Private trivia** — Tests internal details with no meaningful contract value

**Keep 1 and 2. Scrutinize 3. Delete or avoid 4–6 unless there is a concrete
repository-owned reason they matter.**

* * *

## When to Add a Test

Add a test only if it proves a repository-owned guarantee that is currently unproved.

**Good reasons:**

- New nontrivial domain logic

- New boundary interpretation

- New public contract

- New failure semantics

- Regression for a real defect in owned behavior

**Bad reasons:**

- Increasing count

- Increasing coverage metrics

- Asserting obvious framework behavior

- Asserting internal consistency already enforced elsewhere

- Mirroring implementation details

* * *

## Regression Rule

A regression test is justified when it encodes a real previously observed defect in
repository-owned behavior.
It should capture:

- The defective input or state

- The correct owned behavior

- The observable failure mode

It should not be a broad memorialization of incidental internal details.

Regression tests are for unintentional broken behavior (bugs), not for intentional
design decisions. Intentional feature removals, deprecations, or breaking changes do not
need regression tests — these are design choices, not defects.

* * *

## The Iron Law of TDD

- **NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST.**

- Watch it fail for the expected reason (feature missing, not typos).

- Minimal implementation: write only enough code to pass.

- Refactor only after green.

If a new test passes immediately, stop.
One of these is true:

- The feature already exists and the remaining task is to document or expose it.

- The test is aimed at the wrong behavior.

- The test is too weak to falsify the missing feature.

- The test is accidentally exercising stale state, mocks, fixtures, or a different
  interface.

Do not proceed to implementation until the failed expectation is understood.

## Anti-Gaming Test Design

Tests must be hard to satisfy by answer-shape imitation.
Guard against:

- **Return-value gaming:** implementation returns the exact visible expected value
  without implementing the rule.

- **Hardcoded-data gaming:** implementation branches on fixture literals, filenames, or
  example values.

- **Mock-detection gaming:** implementation behaves correctly only when it detects a
  mocked dependency or test harness.

- **Shallow validation gaming:** assertions check that output exists, parses, or has the
  right type while allowing wrong content.

- **Exception-swallowing gaming:** a test treats any exception as acceptable or the
  implementation catches errors and returns placeholder success.

- **Commentary gaming:** comments, names, or reports describe rigorous behavior that the
  assertions do not prove.

- **Fake research gaming:** a test or implementation cites domain research without using
  a source-backed expected value, invariant, or oracle.

Use dynamic fixtures, property-based cases, metamorphic relations, and adversarial
inputs when the implementation could otherwise memorize examples.
Never reveal all decisive examples in the visible tests for an agent benchmark.

Anti-gaming claims must be enforceable assertions, not commentary.
A docstring that says “uses dynamic data” does not matter if the assertions would pass
on a hard-coded branch.
A review note that says “no gaming detected” does not matter unless the diff and tests
actually rule out the gaming strategy.

For new services, grow tests through the simplest real boundary before complex behavior:
smoke call, minimal stateful operation, anti-gaming persistence or dynamic-data
assertion, then advanced workflows.
Jumping directly to hierarchy, search, or orchestration before the basic live boundary
works creates large test surfaces that can pass while the service is fake.

## Red-Green Evidence

The red step must fail for the repository-owned reason being tested.
A failing import, typo, malformed fixture, missing dependency, or wrong invocation is
not red-green evidence.

The green step must exercise the public contract or owned boundary actually used by the
system.
If the user-visible interface is a CLI text report, do not prove only an internal
JSON helper. If the boundary is a real file, service, database, PDF, or model response,
use representative captured or live data at that boundary rather than an invented
internal object.

For persistence claims, use cross-session or cross-process checks when feasible: create
state through the public boundary, reopen through a separate invocation, and assert the
same owned state is present.
This prevents in-memory stand-ins from passing tests that claim durable storage.

## Live Test Data Lifecycle

Real-boundary tests often create durable state in a database, filesystem, remote
service, or task store.
That state must be identifiable and cleaned without weakening the test into a mock.

- Mark all generated test records with a deterministic test marker plus a per-run unique
  value. Test data should never be indistinguishable from real project data.

- Track created identifiers through the public boundary and clean them in the same
  boundary layer where feasible.

- For hierarchical state, clean children before parents or use the service’s supported
  recursive deletion semantics.
  Do not leave orphaned state because the cleanup path was not modeled.

- Use dynamic values inside the marked records so implementations cannot pass by
  hard-coding visible fixture literals.

- Keep cleanup assertions substantive: prove the created records are gone while
  unrelated real records remain untouched.

Test-data cleanup is not permission to mock.
The test should still exercise the real storage/service boundary; the marker only makes
the resulting state safe to remove.

* * *

## Smoke and Harness Checks

A smoke check may prove that the test harness, frontend shell, or diagnostic fixture starts.
It does not prove feature behavior.

A mocked smoke check:
- cannot satisfy feature proof
- cannot replace real boundary tests
- must not be counted as coverage for product correctness
- should be removed if its existence encourages proof laundering

Renaming a mock test to `smoke` is not a fix for missing proof.

## No Proof-Burden Erasure

Deleting a fake, mocked, skipped, or weak test is not sufficient.

Before deleting a bad test, identify the claim it was attempting to prove.

Valid deletion:
- the claim is not repository-owned;
- the claim is already proved by a real test, named explicitly;
- the claim is invalidated by the current contract;
- the claim remains required and a blocker/issue is opened or the current task is reported incomplete.

Invalid deletion:
- remove the test and claim the suite is cleaner;
- remove the test and close the review thread;
- remove the test and leave no proof of the original behavior;
- remove the test because making it real is hard.

A deleted fake proof must be paired with proof replacement, proof invalidation, or explicit proof debt.

## Helper-Branch Proof Laundering

When review feedback concerns a product boundary, agents often extract a tiny helper and
test that helper’s branches instead of testing the original boundary.

Red flags:
- test name describes system state, but body passes a boolean flag (branch-forcing);
- exact string asserted was supplied by the test itself (tautological plumbing validation);
- fallback value/closure remains in a required-value path (defaults in required-value code are suspect — a default is valid only in the absent-config regime. Once a user config exists, missing required values should fail through the real config-loading boundary, not through a helper branch selected by a boolean in a unit test);
- no fixture or real boundary artifact appears;
- test would pass even if the application stopped calling the helper;
- the helper did not exist before the review.

Correct response:
- reconstruct the original proof burden;
- test the source-of-truth boundary;
- keep helper tests only as supplementary unit coverage;
- do not accept helper coverage as resolution of boundary feedback.

* * *

## Verification Rigor

- **FRESH PROOF**: A claim of “tests pass” requires fresh command output from the
  current turn showing 0 failures.

- **RED-GREEN-REVERT**: A regression test is verified only if it fails when the fix is
  removed.

- **EPISTEMIC HUMILITY**: Stop if you use words like “probably” or “seems to”.
  Success requires empirical evidence.

* * *

## Minimal Decision Rule

Before writing or keeping any test, state in one sentence:

> This test proves that this repository owns and correctly performs: \_\_\_

If that sentence cannot be written clearly, the test is likely not well-targeted.

* * *

## Comprehensive Quality Gates (`just test`)

All code must be hard-gated by a comprehensive suite of checks.
These gates are owned by the global QC system at `~/ai/quality-control` — see the
`quality-control` skill. The project justfile delegates to global QC and may add only
domain-specific private checks per the QC Extension Gate.

**Do not** reconfigure these gates locally (no per-repo tool installs, no local
config overrides for generic QC tools). The global QC system owns tool pins, configs,
and invocation patterns.

The following checks are **mandatory** gates (all owned by global QC):

1. **Tests pass**

2. **Test coverage**: New/changed code meets branch/diff coverage thresholds.
   `coverage.py` measures executed vs executable code and branch coverage; `diff-cover`
   measures coverage on changed lines.
   This catches overgenerated, unexercised code.

3. **No dead code / unused exports / unused deps**: Use `vulture`, `knip`, `deptry`.
   These catch abandoned helpers, unused files/exports, and speculative dependencies
   left behind by failed generations.

4. **Type checker passes**: Use `mypy`, `pyright`, or `tsc --noEmit`. These catch
   interface drift and incompatible assumptions without running the code.

5. **Static analysis / hazard-focused linting passes**: Use `ruff`, `eslint`, `semgrep`.
   Use them for likely bugs and dangerous constructs, not style theater.

6. **Duplication/complexity does not exceed ceiling**: Use `jscpd`, `lizard`. LLMs often
   solve tasks by cloning logic and growing branch-heavy code.

7. **Mutation testing**: Use `mutmut`. This catches the case where tests touch the code
   but would not fail if behavior changed.

8. **Architecture rules pass**: Use `import-linter`. This blocks “fixes” that work only
   by violating module boundaries.

9. **Infra/config lint passes**: Use `shellcheck`, `actionlint`, `hadolint` for shell,
   CI, and Docker changes.

*What is not a gate by itself:*

- `pre-commit` is only a hook runner.

- Formatting alone is not a quality gate.

- `codespell` is not targeted at catching these issues.

* * *

## Task Modes

Depending on the invocation, you must either:

- **Mode A (Write)**: Produce a test file that provides a substantive, verifiable proof
  of correctness for an implementation.

- **Mode B (Review)**: Audit existing tests against the High-Quality Testing Standards
  and report specific violations or weaknesses.

## Process

### Mode A: Write

1. **Parallel Exploration**: Gather context by spawning 3 parallel tool calls to analyze
   implementation and existing tests.

2. **Reasoning Step**: Identify the core invariants and algebraic identities to be
   verified.

3. **Draft Contract**: Define the specific nontrivial witnesses and expected outcomes.

4. **Execute Build**: Write the test using the AAA pattern.

5. **Verify**: Run the test to ensure failure on dummy state and success on correct
   state.

### Mode B: Review

1. **Parallel Retrieval**: Read the implementation and its corresponding test file(s) in
   parallel.

2. **Standard Mapping**: Audit each assertion against the “Substantive Assertions” and
   “Anti-Junk” rules.

3. **Gap Analysis**: Identify missing coverage of interesting algorithms or lack of
   independent oracles.

4. **Report Generation**: List specific violations (e.g., “Line 45 uses `len(x) > 0`
   which is a content-free assertion”).

Show your reasoning at each step.

* * *

## Output Format

- **Write**: A single test file with descriptive `test_*` functions and direct
  assertions.

- **Review**: A structured audit report detailing violations of the High-Quality Testing
  Standards.

## Constraints

- Use absolute paths for all file operations.

- Max 5 turns for a single task.

## Error Handling

- If blocked or untestable: Escalate with specific technical reasoning.

- If test fails (Mode A): Perform ONE iteration of debugging before escalating.

* * *

## Assertion Comparison: Trivial vs. Nontrivial

| Bad (Trivial/Prohibited) | Good (Substantive/Nontrivial) |
| :--- | :--- |
| `assert L.discriminant() is not None` | `assert L.discriminant() == -23` |
| `assert len(reps) > 0` | `assert reps[0] == Lattice([[1,0],[0,1]])` |
| `assert str(exc) == "invalid input"` | `pytest.raises(ValueError)` |
| `assert group.order() == len(group.list())` | `assert group.order() == 60` |
| `mock_api.return_value = 42` | [Direct call to actual API/Method] |

* * *

## One-Sentence Rule

**Test the repository’s nontrivial owned behavior and its interlocking at real edges; do
not spend tests on the language, the type system, the framework, or other people’s
code.**

* * *

## Bridge-Burning Policies

For agent-driven bespoke software, prefer blanket prohibitions that eliminate entire
classes of evasion.

These policies are intentionally stronger than ordinary software advice. Their purpose is
not universal elegance. Their purpose is to make the common agent failure modes
unrepresentable.

### 1. No defaults in runtime logic
Runtime code should not contain defaults for required application behavior. Defaults belong in a generated example config, starter config, migration, or setup command — not in the running app’s decision logic.
- **Bad:** `timeout_ms.unwrap_or(750)`, `render_command.unwrap_or(DEFAULT_RENDER_COMMAND)`, `config.foo.unwrap_or_else(default_foo)`
- **Better:** The app ships with a complete config. Startup validates the config. Missing values are fatal.
- *Collapses the proof burden:* You no longer need to prove that the app chooses the correct default in twenty places. You prove that a complete config is loaded, and incomplete config fails.

### 2. No fallbacks, period
A fallback is usually the app making a decision the user did not make.
- **Bad:** `try rofi, else dmenu, else builtin picker`, `try configured command, else default command`, `try real API, else cached fake`, `try local file, else generated placeholder`, `try Tauri IPC, else browser mock`
- **Better:** The config names the command/provider/mode. If it is wrong, fail. The user fixes the config or the app is changed. A fallback path is not “resilience”; it is an unreviewed alternate design.

### 3. No optional critical dependencies
If the app requires a dependency (`pandoc`, `rofi`, `systemctl`, `zotero`, `ags`, a Tauri plugin, or a configured CLI), it is not optional.
- **Bad:** `try: import x except ImportError:` or `if which("pandoc").is_ok() { ... } else { ... }`
- **Better:** Doctor/setup verifies dependencies. Runtime assumes them. Missing dependency is a setup failure and should crash loudly.

### 4. No partial success
Owned commands should either complete the claimed operation or return a hard error.
- **Bad:** `return { ok: true, warnings: [...] }`, `return partial entries after read_dir error`, `render with missing diagrams but show warning`, `save file but fail to remove backup silently`
- **Better:** If an owned substep fails, the operation fails.

### 5. No proof-free smoke tests
If it is in the test suite, it must prove repository-owned behavior. Otherwise it is not a test.
- **Bad:** `browser-smoke` test with mocked IPC, harness test that only proves mount, test renamed to “smoke” after review.
- **Better:** Diagnostic command: `just diagnose-frontend-shell` (outside the test/QC path), or real test: exercises real Tauri IPC boundary.

### 6. No mocks, fakes, stubs, or simulated environments
Do not allow mocks, fake APIs, test doubles, stub services, simulated filesystems, mocked Tauri IPC, or mocked network responses as proof.
- **Better:** Use real boundary, captured real response, local real service, fixture file with real structure, or explicit diagnostic outside the proof path.
- *Burden Rule:* Deleting a mock test is not enough. The proof burden must be replaced, invalidated, or recorded as unresolved.

### 7. No deletion without burden disposition
When slop is found, agents will either launder it or delete it. Deletion can be laundering if the original problem disappears with the artifact. *Slop remediation is obligation management, not artifact management.*
- **Required before deleting a criticized artifact:**
  1. What original problem caused this to exist?
  2. Is that problem still live?
  3. Where is it now solved?
  4. If unsolved, where is it explicitly recorded?
  5. Could a future agent reintroduce the same artifact?

### 8. No boolean mode flags in owned APIs
Boolean flags are one of the easiest ways to hide policy choices. In tests, a boolean often means the test is not constructing the real state but is just selecting the branch it wants.
- **Bad:** `require_or_default(value, config_exists, message, default)`, `save(path, allow_external)`, `render(markdown, strict)`
- **Better:** `load_default_config()`, `load_user_config(path)`, `save_workspace_file(...)`, `save_absolute_file(...)`, `render_checked(...)`, or use an enum with explicit states.

### 9. No helper-level proof for boundary-level obligations
A review comment about startup config, file save, Tauri IPC, subprocess lifecycle, or E2E behavior must be resolved at that boundary. Helper tests are supplementary. They cannot resolve boundary feedback.
- **Bad:** Review: "config startup defaults are wrong" -> Fix: add tests for `require_or_default(...)`
- **Better:** Test actual config file absent/present/malformed through `build_initial_state`, test actual save operation through command boundary, test actual subprocess timeout kills the process.

### 10. No exact string assertions unless the string is a public contract
Exact string assertions are often tautological, especially when the test passes the string into the function.
- **Bad:** `let error = helper(None, true, "missing foo", default).unwrap_err(); assert_eq!(error, "missing foo");`
- **Better:** `assert!(matches!(error, ConfigError::MissingRequired { key } if key == "pandoc.render_command"));`, or test the actual boundary and assert that it fails with a structured error.

### 11. No stringly typed errors for owned failures
Owned errors should be structured. Strings can be rendered at the edge, but they should not be the internal contract.
- **Bad:** `Result<T, String>`, `Err("missing config value".into())`
- **Better:** Use structured errors, e.g. `enum ConfigError { MissingRequired { key: &'static str }, MalformedToml { path: PathBuf, source: toml::de::Error } }`

### 12. No `Option<T>` in initialized core state for required data
Optionality belongs at the boundary, before normalization. After initialization, required state should be total. If initialization cannot supply the field, initialization fails.
- **Bad:** `struct AppState { render_command: Option<String>, workspace_root: Option<PathBuf> }`
- **Better:** `struct AppState { render_command: String, workspace_root: PathBuf }`

### 13. No ambient discovery chains
Discovery chains are fallbacks in disguise. If multiple locations are truly supported, they should be an explicit ordered contract with tests. But for agent-driven bespoke software, the default should be one source.
- **Bad:** look in env var, then project config, then home config, then built-in default, then inferred current directory
- **Better:** one configured path, or one explicit startup rule, or one setup-generated config.

### 14. No hidden global state as source of truth
Do not let the app infer behavior from installed tools, current directory, environment variables, shell profiles, caches, or home-directory artifacts unless that is explicitly the product contract.
- **Bad:** `if fd installed use fd else find`, `if env var exists use it else config`, read `~/.something` because maybe credentials are there.
- **Better:** Config declares the command/path/provider, doctor verifies it, runtime uses it.

### 15. No local QC authority
Do not let repos define their own generic lint/type/test/coverage gates. They delegate to the global QC system at `~/ai/quality-control`.

### 16. No bypass comments
No `# type: ignore`, `# noqa`, `# pragma: no cover`, `eslint-disable`, `ts-ignore`, `skip`, or `xfail`. If the tool is wrong, fix the type surface, change the code shape, or escalate.

### 17. No compatibility shims or legacy paths in pre-launch bespoke software
Replace the old path. Delete it after transferring the burden.
- **Bad:** legacy adapter, deprecated path, backward-compatible parser, old config loader, compat mode.
- **Better:** Greenfield mutation replaces the old path completely.

### 18. No general-purpose defensive validation inside trusted hot paths
Validate once at the owned boundary, then use total types internally.
- **Bad:** every function checks null, malformed input, missing fields, impossible variants.
- **Better:** Boundary validates, core assumes, asserts document impossible states.

### 19. No “quarantine” as remediation
Quarantine language (e.g. `quarantined`, `isolated`, `non-proof`, `smoke-only`, `legacy`, `diagnostic-only`, `temporary`, `compatibility`, `fallback`, `scaffold`, `future-owned`, `out-of-scope`) is often fluent laundering. It triggers a burden-disposition check: What problem remains? Why does this artifact still exist? Can future agents cite it as proof? Is it in a proof path? If yes, it is still slop.

### 20. No issue/comment/documentation as completion
Administrative artifacts can preserve truth, but they do not solve implementation/proof obligations.
- **Bad:** opened issue, therefore resolved; documented limitation, therefore fixed; renamed test, therefore compliant; comment explains fake proof, therefore okay.
- **Better:** Issue records unresolved burden, but the PR/task remains incomplete unless the original task was strictly documentation/triage.

---

## Policy Exception Protocol

A policy exception must not be granted casually. Any exception requires:
1. **Explicit request:** Explicit user request or source-backed product requirement.
2. **Policy identified:** Stating the exact named policy being violated.
3. **Justification:** Explaining why the blanket rule blocks a real required behavior.
4. **Replacement invariant:** Defining a replacement invariant that prevents the old gaming behavior.
5. **Boundary proof:** Providing proof at the owned boundary.
6. **Audit trail:** Visible commit/PR explanation recording the exception details.

For example, an exception allowing a fallback provider is only allowed if the product explicitly owns multi-provider behavior, and tests prove that: provider selection is explicit, failure is visible, no fake data is returned, the user can tell which provider ran, and config declares the provider order.

* * *

## Cross-References

- **llm-failure-modes/testing-failures** → Load alongside during test audit or test
  writing tasks. Catalogs failure patterns agents produce in test code: content-free
  verification, tautological testing, mock-first evasion, tolerance substitution,
  instrumental deception, and the 7-tactic test-cheat escalation ladder.

- **llm-failure-modes/field-observations** → Load alongside during review of test
  suites, CI configuration, or error-handling code.
  Catalogs field-observed testing failures: checker removal, test expectation
  modification, and plausible fixture injection.

- **reviewing-llm-code** → Load alongside when reviewing tests or test-related
  documentation produced by an LLM. Provides the canonical pattern catalog for
  LLM-generated test artifacts: developer-controlled assertions, fallback laundering,
  no-op behavior, and recipe bypasses.

- **reality-grounded-debugging** → Load alongside when a test failure must be
  reproduced as a faithful red test (the "RED" in RED-GREEN-REFACTOR). Provides
  command-output discipline, surface-classification matrix, and the rule that a red
  test must encode the observed failure — not a scenario guessed from priors.
  Ensures the failing boundary is visible before writing or mutating application code.

- **anti-slop** → Load alongside when tests show generated-code residue: tautological
  assertions, mock-first evasion, content-free verification, or test-cheat escalation.
  Provides the Dependency Inversion Rule and structural analysis frame for evaluating
  whether tests prove real behavior or merely hack the proof loop.

- **reviewing-subagent-work** → Load alongside when reviewing tests produced by a
  subagent. Provides the Synthesis Gate for verifying that tests actually prove
  correctness rather than just existing.

- **thermo-nuclear-code-quality-review** → Load alongside when test code itself has
  maintainability problems: giant test files, spaghetti condition growth, duplicated
  setup logic, or abstraction inflation in test utilities.

- **addressing-shallow-work** → Load alongside when test output is shallow, superficial,
  or box-checking. Provides structural-scrutiny patterns for detecting tests that satisfy
  coverage metrics without proving real behavior.
