# HIGH-QUALITY TESTING STANDARDS (GUIDELINES)

**MANDATORY FIRST STEP: You MUST read this entire file before taking ANY action. This is the source of truth for all test work.**

## 1. The Iron Law of TDD
- **NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST.**
- Watch it fail for the expected reason (feature missing, not typos).
- Minimal implementation: write only enough code to pass.
- Refactor only after green.

## 2. Absolute Prohibitions (Zero Tolerance)
- **NO MOCKS/SIMULATIONS**: Never use `unittest.mock`, `monkeypatch`, `patch`, stubs, fakes, or simulated environments. All tests must operate on real data and real objects. No exceptions.
- **NO MASKING**: Never use `xfail`, `skip`, or `ignore`.
- **NO STRING MATCHING**: Never assert on error strings. Assert on the **TYPE** of error (e.g., `pytest.raises(TypeError)`).

## 3. Substantive Assertions
- **REJECT TRIVIALITY**: `is not None`, `len(x) > 0`, or `isinstance()` are disallowed.
- **PROVE A FACT**: Assert a meaningful identity, invariant, or equivalence (e.g., `L.discriminant() == -23`).
- **NONTRIVIAL WITNESSES**: Use representative examples, never zero values or identity elements as primary witnesses.

## 4. Verification Rigor
- **FRESH PROOF**: A claim of "tests pass" requires fresh command output from the current turn showing 0 failures.
- **RED-GREEN-REVERT**: A regression test is verified only if it fails when the fix is removed.

## 5. Architectural & Behavioral Controls
- **TESTS AS SPEC**: Tests define the specification, not current implementation quirks.
- **PERFORMANCE**: Tests should typically take < 30 seconds.
- **EPISTEMIC HUMILITY**: Stop if you use words like "probably" or "seems to". Success requires empirical evidence.

## 6. Report-Only Review
- When asked to review, do NOT actually edit the doc or code. REPORT the review only.
