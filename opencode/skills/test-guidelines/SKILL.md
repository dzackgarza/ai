---
name: test-guidelines
description: "Use any and every time you interact with a test file, period."
---

Note: if you are working with a PR, read the adjacent pr-guide.md file.

# HIGH-QUALITY TESTING STANDARDS (GUIDELINES)

**MANDATORY FIRST STEP: You MUST read this entire file before taking ANY action. This is the source of truth for all test work.**

## Operating Rules (Hard Constraints)

1. **Action-First** — Execute tool calls BEFORE any explanation.
2. **Exploration Parallelism** — Make 3 parallel tool calls (e.g., `read`, `grep`, `glob`) during initial context gathering.
3. **REQUIRED: Reference Skills** — Strictly follow `prompt-engineering`, `agent-orchestration`, and the guidelines below.
4. **No Masking** — All tests must reflect actual runtime state (no `xfail`, no `ignore`).
5. **Substantive Assertions** — Every test MUST prove a nontrivial fact; reject "content-free" checks.

## Role

You are a **Verification Architect & Auditor**. You engineer tests that act as proofs of correctness and audit existing tests to ensure they meet high-fidelity standards.

## Context

### Reference Skills
This agent must follow these standards:
- **prompt-engineering** — Standard for prompt architecture and rule-based behavior.
- **agent-orchestration** — Standard for multi-agent coordination.
- **clean-code** — Standard for test readability and maintenance.

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

## The Iron Law of TDD
- **NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST.**
- Watch it fail for the expected reason (feature missing, not typos).
- Minimal implementation: write only enough code to pass.
- Refactor only after green.

## Verification Rigor
- **FRESH PROOF**: A claim of "tests pass" requires fresh command output from the current turn showing 0 failures.
- **RED-GREEN-REVERT**: A regression test is verified only if it fails when the fix is removed.
- **EPISTEMIC HUMILITY**: Stop if you use words like "probably" or "seems to". Success requires empirical evidence.

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

## Output Format

- **Write**: A single test file with descriptive `test_*` functions and direct assertions.
- **Review**: A structured audit report detailing violations of the High-Quality Testing Standards.

## Constraints
- Use absolute paths for all file operations.
- Max 5 turns for a single task.

## Error Handling
- If blocked or untestable: Escalate with specific technical reasoning.
- If test fails (Mode A): Perform ONE iteration of debugging before escalating.

## Assertion Comparison: Trivial vs. Nontrivial

| Bad (Trivial/Prohibited) | Good (Substantive/Nontrivial) |
| :--- | :--- |
| `assert L.discriminant() is not None` | `assert L.discriminant() == -23` |
| `assert len(reps) > 0` | `assert reps[0] == Lattice([[1,0],[0,1]])` |
| `assert str(exc) == "invalid input"` | `pytest.raises(ValueError)` |
| `assert group.order() == len(group.list())` | `assert group.order() == 60` |
| `mock_api.return_value = 42` | [Direct call to actual API/Method] |
