---
name: test-guidelines
description: 'Use any and every time you interact with a test file, period.'
---
Note: if you are working with a PR, read the adjacent pr-guide.md file.

# HIGH-QUALITY TESTING STANDARDS (GUIDELINES)

Before writing, reviewing, or modifying tests or Quality Control configurations, consult the central policy index:
[policy-index](file:///home/dzack/ai/opencode/skills/policy-index/SKILL.md)

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

## Proof-Only Assertion Policy

A project test is admitted only if every assertion increases confidence in a repository-owned behavior.
A test line is admissible only if it increases the epistemic status of a repository-owned proof burden.
If an assertion would still pass on a plausibly broken app, it is banned.
No assertion without discrimination.

A test line is banned if it would pass when:
- the app is not wired to the real boundary;
- the implementation returns arbitrary non-empty junk;
- the helper under test is no longer used by production;
- the error is wrong but the string matches;
- the UI shell renders but the feature is broken;
- the code was merely reshaped to appease a reviewer;
- the assertion checks existence, visibility, type, or structure without semantics.

Project tests prove behavior.
Global QC enforces code-shape policy.
Issues record unresolved proof burdens.
Nothing else belongs in the test suite.

For the canonical catalog of banned test shapes and their allowed replacements, see the [Banned Test Shapes Catalog](file:///home/dzack/ai/opencode/skills/policy-index/references/test-proof-rules.md).

## Try/Catch Ban

Do not write try/catch/except/rescue blocks in tests or owned runtime code.

Banned:
- Python `try/except`
- JavaScript/TypeScript `try/catch`
- Ruby `begin/rescue`
- shell `cmd || fallback`, `set +e` around normal execution, or fallback branches
- Rust `let _ =`, `.ok()`, `unwrap_or`, `unwrap_or_else`, `match Err(_) => fallback`

Expected failures must be asserted by structured test-framework mechanisms or structured error values. Unexpected failures must propagate.

The only possible exception is an explicitly approved boundary renderer whose sole job is to translate a structured internal error into a user-facing protocol. That boundary must not continue execution, must not default, and must not return partial success.


## Line Admission Gate

Before keeping any assertion line, answer:

1. What exact proof burden does this line raise confidence in?
2. What plausible broken implementation would this line fail on?
3. Does it exercise the real owned boundary?
4. Is it asserting product semantics rather than existence, visibility, type, string, structure, or review compliance?
5. Would it still pass if production stopped using the helper or artifact under test?

If no plausible broken implementation is excluded, delete the line.
If the claim is code-shape policy, move it to global QC.
If the burden remains unproved, record the proof debt; do not add a low-information assertion.


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
For bug-fix work, the first proof is end-to-end reproduction of the failing path;
unit tests should follow and should be derived from the reproduced failure, not replace it.
For E2E or full-system reproductions, save an evidence bundle in the test artifact directory:
- a screenshot of the observable failure state and post-repro state,
- a video or trace of the end-to-end flow when browser tooling supports it, and
- command/session logs that show the boundary inputs, outputs, and errors.

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
For E2E or GUI-facing behavior, green proof requires attached evidence artifacts (at least
one screenshot, one persisted log stream, and one replayable trace or video where
available).

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

## Web Application and Frontend Testing

To test local web applications, write native Python Playwright scripts.

**Helper Scripts Available**:
- `scripts/with_server.py` (in `test-guidelines/`) - Manages server lifecycle (supports multiple servers)

**Always run scripts with `--help` first** to see usage. DO NOT read the source until you try running the script first and find that a customized solution is absolutely necessary. These scripts exist to be called directly as black-box scripts rather than ingested into your context window.

### Decision Tree: Choosing Your Approach

1. **Is it static HTML?**
   - **Yes** → Read HTML file directly to identify selectors → Write Playwright script using selectors.
   - **No/Fails** → Treat as dynamic (below).

2. **Is the server already running?**
   - **No** → Run `python scripts/with_server.py --help` → Use the helper + write simplified Playwright script.
   - **Yes** → Reconnaissance-then-action:
     1. Navigate and wait for `networkidle`.
     2. Take screenshot or inspect DOM.
     3. Identify selectors from rendered state.
     4. Execute actions with discovered selectors.

### Reconnaissance-Then-Action Pattern

1. **Inspect rendered DOM**:
   ```python
   page.screenshot(path='/tmp/inspect.png', full_page=True)
   content = page.content()
   page.locator('button').all()
   ```

2. **Identify selectors** from inspection results.

3. **Execute actions** using discovered selectors.

### Common Pitfalls and Best Practices

- ❌ **Don't** inspect the DOM before waiting for `networkidle` on dynamic apps.
- ✅ **Do** wait for `page.wait_for_load_state('networkidle')` before inspection.
- **Use bundled scripts as black boxes** - Use `scripts/with_server.py` to handle common, complex workflows reliably without cluttering the context window.
- Use `sync_playwright()` for synchronous scripts and always close the browser when done.
- Use descriptive selectors: `text=`, `role=`, CSS selectors, or IDs.
- Add appropriate waits: `page.wait_for_selector()` or `page.wait_for_timeout()`.

For pattern examples, see:
- `references/webapp-testing/element_discovery.py`
- `references/webapp-testing/static_html_automation.py`
- `references/webapp-testing/console_logging.py`

* * *

## Smoke and Harness Checks

If it is test-shaped and in the test suite, it must be proof-bearing. Non-proof smoke/harness diagnostics belong in a diagnostic command outside the QC proof path.

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

Correct response after triage: See `policy-index/references/remediations.md` → **Remediation: Boundary Test Bypass**.

* * *

## Verification Rigor
- **FRESH PROOF**: A claim of “tests pass” requires fresh command output from the
  current turn showing 0 failures.

- **REPRO-FIRST**: For bug claims, the end-to-end reproduction must be captured and
  verified before test-green is treated as proof of correction.

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
These gates are owned by the global QC system at `~/ai-review-ci` — see the
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

The important move is to stop treating this as a case-by-case review problem. Agents are too good at finding local, linguistically plausible exceptions. The right response is to make whole classes of evasive code unrepresentable.

> [!IMPORTANT]
> **Core Principle:** Prefer blanket constraints that make bad states impossible over review rules that ask agents to judge bad states later.

The recurring pattern is that an agent first tries to satisfy checking/validation surfaces (such as the compiler/typechecker, QC gates, PR review, or user queries) by manipulating the validation surface (e.g. by adding fallbacks, defaults, mocks, try/except blocks, or bypass comments) instead of reconstructing the original obligation and solving it. The policy answer is to remove the vocabulary that enables that manipulation.

Adhering to the [Bridge-Burning Policies](file:///home/dzack/ai/opencode/skills/policy-index/SKILL.md#policy-registry) defined in `policy-index/SKILL.md` is a non-negotiable hard constraint for all development. These rules eliminate common agent validation-evasion pathways (such as runtime defaults, fallbacks, mocks, and diagnostic smoke tests in proof paths). Refer to them as hard boundaries.

> [!IMPORTANT]
> **Bridge-Burning Red Flags:** If the original review concern is boundary-level, helper-level tests cannot resolve it. They may supplement proof, but they do not close the burden. If a construct would let an agent preserve the appearance of correctness while weakening the obligation, treat it as a red flag even if the code currently works. For a detailed list of testing red flags (such as mock/fake/stub/simulation usage, smoke tests in the suite, exact string assertions, etc.), see the [Bridge-Burning Red Flags Reference Catalog](file:///home/dzack/ai/opencode/skills/policy-index/references/red-flags.md) and the [Runtime Control-Flow Red Flags Catalog](file:///home/dzack/ai/opencode/skills/policy-index/references/runtime-control-flow.md).

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
