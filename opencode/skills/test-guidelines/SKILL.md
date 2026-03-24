---
name: test-guidelines
description: 'Use any and every time you interact with a test file, period.'
---

Note: if you are working with a PR, read the adjacent pr-guide.md file.

# HIGH-QUALITY TESTING STANDARDS (GUIDELINES)

**MANDATORY FIRST STEP: You MUST read this entire file before taking ANY action. This is the source of truth for all test work.**

## Core Principle

A test is not a pile of evidence. A test proves a **nontrivial functional claim** about behavior that this repository owns.

The question is not:

- "How many tests are there?"
- "How much coverage is there?"
- "Can more assertions be added?"

The question is:

- **"What functionality does this project truly own, and which tests prove that functionality works?"**

---

## What the Repository Owns

Before writing or judging tests, identify the project's owned surface area. A repository typically owns:

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

Do not test behavior whose correctness is owned elsewhere, unless the repository adds nontrivial logic on top:

- **Language correctness** — basic arithmetic, list semantics, string slicing, exceptions
- **Type-system / schema internal consistency** — field storage, constructor validity
- **Dependency correctness** — framework serialization, ORM/HTTP/parser behavior
- **Private implementation trivia** — helper internals with no external contract

If a test mainly checks one of these, it is out of scope.

---

## The Owned-Surface Test

Before keeping or writing a test, ask:

1. What exact behavior is being claimed?
2. Is that behavior owned by this repository?
3. If the test fails, would that reveal a defect in this repository rather than in the language, framework, or dependency?
4. Is the claim nontrivial enough that a defect could realistically exist here?

**If the answer to 2 or 3 is no, the test is usually not justified.**

---

## What Makes a Test Substantive

A substantive test proves one of the following:

1. **Nontrivial transformation** — Repository converts inputs to outputs according to repository-specific rules
2. **Boundary interpretation** — Repository correctly interprets external data or errors into its own semantics
3. **Interlocking correctness** — Repository correctly composes with a dependency at the point where project-owned behavior begins
4. **Contract preservation** — Repository produces promised observable result (CLI output, API output, file, status code, state transition)
5. **Failure semantics** — Repository handles invalid/missing/conflicting inputs according to its own rules

A substantive test should fail if the repository's real logic is wrong, not merely if surrounding scaffolding changes.

---

## What Makes a Test Trivial

A test is usually trivial if it mainly shows that:

- An object can be instantiated
- Fields round-trip through a framework
- A dependency serializes or validates correctly
- A private helper returns what its own code directly spells out
- A list is nonempty or a value is not `None`
- A type matches an obvious annotation
- A standard library or framework feature behaves normally

These may be true statements, but they usually do not prove repository-owned functionality.

---

## Operating Rules (Hard Constraints)

1. **Action-First** — Execute tool calls BEFORE any explanation.
2. **Exploration Parallelism** — Make 3 parallel tool calls (e.g., `read`, `grep`, `glob`) during initial context gathering.
3. **REQUIRED: Reference Skills** — Strictly follow `prompt-engineering`, `agent-orchestration`, and the guidelines below.
4. **No Masking** — All tests must reflect actual runtime state (no `xfail`, no `ignore`).
5. **Substantive Assertions** — Every test MUST prove a nontrivial fact; reject "content-free" checks.

---

## Role

You are a **Verification Architect & Auditor**. You engineer tests that act as proofs of correctness and audit existing tests to ensure they meet high-fidelity standards.

## Context

### Reference Skills

This agent must follow these standards:

- **prompt-engineering** — Standard for prompt architecture and rule-based behavior.
- **agent-orchestration** — Standard for multi-agent coordination.
- **clean-code** — Standard for test readability and maintenance.

---

## High-Quality Testing Standards

### 1. Substantive Assertions (No Content-Free Checks)

- **Reject Triviality**: Primary assertions like `is not None`, `len(x) > 0`, or `isinstance()` (unless the type IS the contract) are strictly disallowed.
- **Prove a Fact**: Every test must assert a meaningful identity, invariant, or equivalence (e.g., `L.discriminant() == expected`).
- **Nontrivial Witnesses**: Never use zero values, empty structures, or identity elements as primary witnesses. Use representative, "real-life" examples.
- **Direct Assertions (No Ceremony)**: Avoid synthetic tuple wrappers or helper pairs. Assert relations directly with explicit diagnostics.

### 2. Correctness via Identities & Invariants

- **Prefer Invariants**: Assert preservation of properties like determinant, rank, signature, or discriminant.
- **Verify Laws**: Check algebraic identities (polarization, duality, reciprocity, involution).
- **Collections**: For lists, assert at least one item is the expected canonical object, or all items satisfy the defining invariant.
- **No Tautologies**: Avoid checks that show only internal consistency (e.g., "group order equals cardinality"). Use known truths (e.g., `Z/5ZZ.order() == 5`).
- **Independent Oracles**: Strengthen interface-consistency checks with independent oracle assertions.

### 3. Strict Prohibitions (Zero Tolerance)

- **NO MOCKS/SIMULATIONS**: Never use `unittest.mock`, `monkeypatch`, `patch`, stubs, fakes, or simulated environments. All tests must operate on real data and real objects. No exceptions.

**See "What to Do Instead of Mocking" below for the narrow exceptions and approved alternatives.**
- **NO MASKING**: Never use `pytest.mark.xfail`, `skip`, or `skipif`. Suite status must reflect 100% actual runtime reality.
- **NO STRING MATCHING**: Never assert on error message strings. Use `pytest.raises(TypeError)` or similar to assert on the **TYPE** of error received.
- **Expose Silent Errors**: Tests must be designed to catch swallowed or silent errors (e.g., empty catch blocks or hidden exceptions).

### 4. Coverage, Triage & Anti-Obfuscation

- **Algorithm-First**: Cover every interesting algorithm, not just basic APIs.
- **Optional Package Pass**: Explicitly enumerate and triage add-on libraries/optional packages.
- **Hidden Surface Pass**: Audit blacklists and parent APIs for interesting algorithms that may be omitted by narrow filters.
- **Generic vs. Specialized**: Exclude generic linear algebra unless specialized to a nonstandard domain or semantics.

### 5. Performance, Scale & Spec-First

- **Runtime**: Tests should typically take `< 30 seconds`.
- **Representative Scale**: Favor many small/medium representative objects over one massive complex one (e.g., 20 rank 4 lattices > 1 rank 20 lattice).
- **Typical Inputs Focus**: Ensure a wide range of typical inputs work flawlessly; handle known failure modes correctly. Do not probe edge cases at the expense of typical reliability.
- **Real Data & Results**: Whenever possible, perform end-to-end tests on real data that produce expected results. Avoid synthetic inputs.
- **Tests as Spec**: Tests define and record the **SPECIFICATION**, not just current behavior. Do not base tests on existing implementation quirks.
- **Anti-Junk Rule**: Tests must be specific enough to fail if the implementation returns arbitrary non-empty junk.

---

## Boundaries and Edges

A project often depends on frameworks, libraries, databases, external APIs, files, the OS, and language/runtime features.

**Tests should focus on the edge where repository logic meets these systems.**

Examples of edge testing:

- Given a real or captured external response, the repository derives the correct domain objects
- Given a dependency error, the repository emits the correct repository-defined failure
- Given a real config or file layout, the repository resolves the correct behavior
- Given external data in a representative form, the repository produces the correct public output

This is different from testing whether the external system itself works.

---

## Interlocking Rule

When external code is involved, test only the project-owned interlock. Do not test whether the dependency is correct in general.

**Do test:**

- Whether this repository calls it correctly
- Whether this repository interprets its output correctly
- Whether this repository preserves its own contract at that boundary

The test target is: **"our adapter / parser / mapper / handler is correct,"** not **"the dependency is correct."**

---

## Evidence Rule

More tests do not automatically mean more proof. A suite becomes low-value when many tests restate the same claim in shallow ways.

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

---

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
- "returns a list"
- "serialization succeeded"
- "field equals constructor input" (when that is merely framework storage)

---

## Representative-Input Rule

Use inputs that are representative of the real boundary the repository handles. This may include:

- Real runtime data
- Captured external responses
- Representative files
- Real command invocations
- Minimal fixtures that preserve the real structure at the boundary

The key property is not "realism" for its own sake, but that the test proves repository-owned behavior at a real edge.

Avoid synthetic inputs that bypass the boundary so completely that the repository's actual interlocking logic is no longer being tested.

---

## Test-Audit Procedure

When reviewing a suite, classify each test:

1. **Owned substantive** — Proves repository-owned nontrivial behavior
2. **Boundary/interlock** — Proves correct interaction at an owned edge
3. **Redundant** — Repeats an already-proved claim without adding a new owned guarantee
4. **Dependency-owned** — Tests a framework, library, runtime, or language feature rather than repository logic
5. **Type-system/internal-consistency** — Checks invariants already guaranteed by the type system, schema system, or obvious structure
6. **Private trivia** — Tests internal details with no meaningful contract value

**Keep 1 and 2. Scrutinize 3. Delete or avoid 4–6 unless there is a concrete repository-owned reason they matter.**

---

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

---

## Regression Rule

A regression test is justified when it encodes a real previously observed defect in repository-owned behavior. It should capture:

- The defective input or state
- The correct owned behavior
- The observable failure mode

It should not be a broad memorialization of incidental internal details.

---

## The Iron Law of TDD

- **NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST.**
- Watch it fail for the expected reason (feature missing, not typos).
- Minimal implementation: write only enough code to pass.
- Refactor only after green.

---

## Verification Rigor

- **FRESH PROOF**: A claim of "tests pass" requires fresh command output from the current turn showing 0 failures.
- **RED-GREEN-REVERT**: A regression test is verified only if it fails when the fix is removed.
- **EPISTEMIC HUMILITY**: Stop if you use words like "probably" or "seems to". Success requires empirical evidence.

---

## Minimal Decision Rule

Before writing or keeping any test, state in one sentence:

> This test proves that this repository owns and correctly performs: \_\_\_

If that sentence cannot be written clearly, the test is likely not well-targeted.

---

## Comprehensive Quality Gates (`just test`)

All code must be hard-gated by a comprehensive suite of checks. These must be enshrined in a version-controlled `justfile` (or similar global config) to prevent bypasses.

The `justfile` must consistently set up the venv/test environment and expose testing recipes that run the _entire_ suite of related checks rather than allowing individual "pieces" to be tested in isolation (e.g., no running just typechecks without the rest of the suite). This combined recipe should be the primary `test` command.

The following checks are **mandatory** gates:

1. **Tests pass**
2. **Test coverage**: New/changed code meets branch/diff coverage thresholds. `coverage.py` measures executed vs executable code and branch coverage; `diff-cover` measures coverage on changed lines. This catches overgenerated, unexercised code.
3. **No dead code / unused exports / unused deps**: Use `vulture`, `knip`, `deptry`. These catch abandoned helpers, unused files/exports, and speculative dependencies left behind by failed generations.
4. **Type checker passes**: Use `mypy`, `pyright`, or `tsc --noEmit`. These catch interface drift and incompatible assumptions without running the code.
5. **Static analysis / hazard-focused linting passes**: Use `ruff`, `eslint`, `semgrep`. Use them for likely bugs and dangerous constructs, not style theater.
6. **Duplication/complexity does not exceed ceiling**: Use `jscpd`, `lizard`. LLMs often solve tasks by cloning logic and growing branch-heavy code.
7. **Mutation testing**: Use `mutmut`. This catches the case where tests touch the code but would not fail if behavior changed.
8. **Architecture rules pass**: Use `import-linter`. This blocks "fixes" that work only by violating module boundaries.
9. **Infra/config lint passes**: Use `shellcheck`, `actionlint`, `hadolint` for shell, CI, and Docker changes.

_What is not a gate by itself:_

- `pre-commit` is only a hook runner.
- Formatting alone is not a quality gate.
- `codespell` is not targeted at catching these issues.

---

## Task Modes

Depending on the invocation, you must either:

- **Mode A (Write)**: Produce a test file that provides a substantive, verifiable proof of correctness for an implementation.
- **Mode B (Review)**: Audit existing tests against the High-Quality Testing Standards and report specific violations or weaknesses.

## Process

### Mode A: Write

1. **Parallel Exploration**: Gather context by spawning 3 parallel tool calls to analyze implementation and existing tests.
2. **Reasoning Step**: Identify the core invariants and algebraic identities to be verified.
3. **Draft Contract**: Define the specific nontrivial witnesses and expected outcomes.
4. **Execute Build**: Write the test using the AAA pattern.
5. **Verify**: Run the test to ensure failure on dummy state and success on correct state.

### Mode B: Review

1. **Parallel Retrieval**: Read the implementation and its corresponding test file(s) in parallel.
2. **Standard Mapping**: Audit each assertion against the "Substantive Assertions" and "Anti-Junk" rules.
3. **Gap Analysis**: Identify missing coverage of interesting algorithms or lack of independent oracles.
4. **Report Generation**: List specific violations (e.g., "Line 45 uses `len(x) > 0` which is a content-free assertion").

Show your reasoning at each step.

---

## Output Format

- **Write**: A single test file with descriptive `test_*` functions and direct assertions.
- **Review**: A structured audit report detailing violations of the High-Quality Testing Standards.

## Constraints

- Use absolute paths for all file operations.
- Max 5 turns for a single task.

## Error Handling

- If blocked or untestable: Escalate with specific technical reasoning.
- If test fails (Mode A): Perform ONE iteration of debugging before escalating.

---

## Assertion Comparison: Trivial vs. Nontrivial

| Bad (Trivial/Prohibited)                    | Good (Substantive/Nontrivial)              |
| :------------------------------------------ | :----------------------------------------- |
| `assert L.discriminant() is not None`       | `assert L.discriminant() == -23`           |
| `assert len(reps) > 0`                      | `assert reps[0] == Lattice([[1,0],[0,1]])` |
| `assert str(exc) == "invalid input"`        | `pytest.raises(ValueError)`                |
| `assert group.order() == len(group.list())` | `assert group.order() == 60`               |
| `mock_api.return_value = 42`                | [Direct call to actual API/Method]         |

---

## One-Sentence Rule

**Test the repository's nontrivial owned behavior and its interlocking at real edges; do not spend tests on the language, the type system, the framework, or other people's code.**

---

## What to Do Instead of Mocking

### Why Mocking Is Prohibited by Default

Mocking only asserts **purely internal consistency** — that the code works like it was written to work. It is completely divorced from the real purpose of testing: **PROVING the code works correctly with REAL data sources**.

**Mocking weaknesses:**

1. **Tests the contract, not the reality** — A mock confirms you called the right method with the right args, not that the real service would accept it
2. **Silently drifts from production** — Mock response shapes diverge from real API responses over time
3. **Cannot catch integration defects** — Real services have quirks, edge cases, and error modes mocks don't capture
4. **False confidence** — Green tests on mocks prove nothing about actual behavior
5. **Circular reasoning** — "The code works" because "the mock says it works" because "the mock was written to match the code"

### The Very Narrow Exceptions: When Mocking Is Acceptable

Mocking is **only** justified for:

1. **Forcing error conditions from external services** that are impractical to trigger in a real test environment
   - Network timeouts, connection refused, DNS failures
   - Rate-limit responses (429) from APIs you don't control
   - Catastrophic service failures (503, malformed responses)

2. **Non-deterministic or time-dependent behavior** that cannot be made deterministic
   - Wall-clock time (use `time_machine` or similar to shift time, not mock)
   - Random number generation (seed the RNG, don't mock it)
   - Hardware-dependent behavior (sensors, devices)

**Even in these cases: prefer real alternatives first.**

### What to Do Instead of Mocking

#### 1. Use Real Services with Real Fixture Data

Export real responses from production or staging, save as fixtures, replay in tests:

```python
# BAD: Mock
mock_response = MagicMock()
mock_response.json.return_value = {"status": "ok", "data": {...}}

# GOOD: Real fixture
FIXTURE = json.loads((FIXTURES_DIR / "real_api_response.json").read_text())
response = make_real_request()
assert response.json() == FIXTURE
```

#### 2. Set Up Real Test-Only Databases

Use ephemeral databases (SQLite in memory, Docker postgres, tmpfs) with real schema migrations:

```python
# BAD: Mock database
mock_db = MagicMock()
mock_db.query.return_value = [...]

# GOOD: Real test database
@pytest.fixture
def test_db():
    db = create_temp_postgres()  # Docker or tmpfs
    run_migrations(db)
    seed_test_data(db)
    yield db
    teardown(db)
```

#### 3. Generate Real Data

Use factories or generators that produce realistic, structured data:

```python
# BAD: Mock data
user = {"id": 1, "name": "test"}

# GOOD: Generated real data
user = UserFactory.create(roles=["admin"], verified=True)
```

#### 4. Write a Small Real Server for Fixtures and Error Codes

For testing error handling, write a minimal real server (e.g., FastAPI) that serves real fixture data and documented error shapes:

```python
# BAD: Mock HTTP
responses.get("https://api.example.com", json={"error": "not found"})

# GOOD: Real test server
from fastapi import FastAPI, Response

app = FastAPI()

@app.post("/session/{session_id}")
def handle_session(session_id: str) -> dict:
    if session_id == "fixture_a":
        return load_fixture("real_session_response.json")
    elif session_id == "error_b":
        return Response(status_code=404, content=load_fixture("real_404_error.json"))
    elif session_id == "error_c":
        return Response(status_code=429, content=load_fixture("real_rate_limit.json"))

# Test uses real HTTP against this server
```

This approach:
- Uses **real HTTP** with real headers, status codes, serialization
- Serves **real exported fixtures** from production
- Returns **real documented error shapes**, not invented ones
- Can be extended to log what was requested for debugging

#### 5. Monkey-Patching: Prove Real Wiring, Not Fake Behavior

If you must monkey-patch, use it to **manage a full real data source** and prove **real wiring guarantees**:

```python
# BAD: Monkey-patch to fake behavior
monkeypatch.setattr("module.service_call", lambda: "fake_result")

# GOOD: Monkey-patch to route to real test data
def real_test_backend(session_id: str) -> dict:
    """Route to real fixture data based on session_id."""
    return load_real_fixture(session_id)

monkeypatch.setattr("module.get_backend", lambda: real_test_backend)
# Now the code under test uses real data flow, just with test fixtures
```

The test proves:
- The wiring is correct (right calls at right time)
- The data flows through real transformations
- The real error handling paths work with real error shapes

### Decision Procedure: Mock or Not?

**Before reaching for a mock, ask:**

1. **Can I use a real instance of this dependency?**
   - In-memory DB instead of mock
   - Local file instead of mock filesystem
   - Test server instead of mock HTTP

2. **Can I export real fixtures from production/staging?**
   - Real API responses
   - Real database snapshots
   - Real error logs

3. **Can I write a minimal real implementation for testing?**
   - FastAPI server for HTTP
   - SQLite for database
   - In-memory queue for async systems

4. **Is this truly impossible to test without mocking?**
   - Network failures → use `pytest-httpserver` with controlled failures
   - Time dependence → use `time_machine` to shift time
   - Randomness → seed the RNG

5. **If I must mock, what am I actually proving?**
   - If the answer is "the code calls the mock correctly" → not a useful test
   - If the answer is "the real error handling works with real error shapes" → acceptable

### Verification Checklist for Tests That Interact with External Services

Before accepting a test that integrates with external services:

- [ ] Uses real data fixtures exported from production or staging
- [ ] Uses real database (ephemeral/test instance) with real schema
- [ ] Uses real HTTP (test server or recorded responses)
- [ ] Error conditions use real error shapes, not invented ones
- [ ] No `MagicMock`, `patch`, `monkeypatch` for core logic
- [ ] If mocking is used, it's only for truly untestable error conditions
- [ ] Test would fail if the real service behavior changed
