# Example Task: Method Test Coverage Verification

## Goal

Pick 20-50 specific methods from checklists. For each, verify that a corresponding test exists and is mathematically sound according to `TEST_QUALITY.md`.

## Workflow

1. **Select methods**: Pick 20-50 methods from any checklist (e.g., `docs/sage_methods_checklist.md`)
2. **For each method**:
   - Locate the checklist entry
   - Find the test identifier tag: `[test: <module>::<test_name>]`
   - Open the test file and verify the test exists
   - Audit the test against TEST_QUALITY.md criteria

3. **Record findings**:
   - Methods without test tags → flag as uncovered
   - Methods with broken test references → flag as broken
   - Methods with inadequate tests → flag with specific deficiency

## Test Quality Audit Checklist

For each test found, verify:

### Nontrivial Assertions
- [ ] Asserts a meaningful mathematical property, identity, invariant, or equivalence
- [ ] Not just `is not None`, `hasattr`, `isinstance`, or non-emptiness checks
- [ ] Uses nontrivial primary witnesses (not zero/identity/empty)
- [ ] Would fail on mathematically wrong output, not just missing output

### Mathematical Correctness
- [ ] Uses a genuinely nontrivial mathematical example
- [ ] Expected values are verifiable (not just "something returned")
- [ ] Tests what the method is documented to do
- [ ] Not just blind code-level consistency between two APIs

### Invocation Correctness
- [ ] Invocation matches documented signature
- [ ] All invocation variants are tested (if applicable)
- [ ] Input types match method contracts

### Proper Structure
- [ ] Is a proper pytest test (or subprocess wrapper to GAP/etc)
- [ ] Asserts equality of numbers, vectors, matrices, isomorphisms
- [ ] Not just asserting return codes or non-empty results
- [ ] No `xfail` or expected-failure masking

## What NOT To Do

- **Do NOT run tests** — this is a code audit, not execution
- **Do NOT fix environment issues** — irrelevant to this task
- **Do NOT make tests pass** — unless clear doc/invocation mismatch
- **Do NOT add new tests** — only verify existing ones
- **Do NOT change test logic** — only fix obvious code errors

## Fixes Allowed (Only These)

- Incorrect invocation (doesn't match documented signature)
- Typos in method names
- Missing imports
- Obvious doc mismatches where code clearly intended something else

## Output

For each method, record:
```markdown
## `<method_name>`
- Checklist: `docs/<pkg>_methods_checklist.md`
- Test: `tests/<path>::<test_name>`
- Status: [COVERED/UNCOVERED/BROKEN/INADEQUATE]
- Issues: [list specific deficiencies if INADEQUATE]
```

## Success Criteria

- All 20-50 methods audited
- Each has coverage status recorded
- Specific deficiencies identified for inadequate tests
- No tests were run during this task
