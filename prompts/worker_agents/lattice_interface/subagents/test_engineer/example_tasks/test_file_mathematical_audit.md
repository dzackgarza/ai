# Example Task: Test File Mathematical Audit

## Goal

Take one test file. Audit every test in it against `TEST_QUALITY.md` requirements. Identify and flag all inadequacies.

## Workflow

1. **Select a test file** — e.g., `tests/sage/sage_doc/test_lattice_invariants.py`
2. **For each test function**:
   - Read the test code
   - Identify the method being tested
   - Check the method's documented contract (in reference docs)
   - Audit against TEST_QUALITY.md criteria
3. **Classify each test**:
   - **ADEQUATE**: Meets all quality requirements
   - **INADEQUATE**: Fails one or more requirements (specify which)
   - **ORPHAN**: Tests a method not in any checklist
   - **MISSING**: Method in checklist but no test found

## Audit Criteria (from TEST_QUALITY.md)

### Content-Free Assertions (Section 3)

Flag tests whose primary assertion is:
- `is not None`
- `hasattr(...)`
- `isinstance(...)` without mathematical assertion
- `len(x) > 0`, `len(x) >= 1`, `bool(x)`, `x != []`
- Representative placeholders: `assert len(reps) > 0`

### Trivial Primary Witnesses (Section 3.1)

Flag tests using only:
- Zero vectors/elements
- Identity maps/group elements
- Empty/default structural objects

These are acceptable only as secondary checks, not primary assertions.

### Assertion Ceremony (Section 4.5)

Flag tests with:
- Synthetic tuple wrappers: `(actual, baseline) == (expected, baseline)`
- Redundant baseline terms that hide what's being tested

### Interoperability-Only Tests (Section 5.5)

Flag tests that only check:
- `root.method(...) == lattice.method(root, ...)`
- Two APIs returning same result without independent oracle

These need strengthening with independent mathematical assertions.

### Masking (Section 6)

Flag any use of:
- `pytest.mark.xfail`
- `pytest.mark.skip` on failing behavior
- Any pass-by-design marker on known breakage

## What NOT To Do

- **Do NOT run tests**
- **Do NOT fix test logic** — only flag issues
- **Do NOT add assertions** — only identify what's missing
- **Do NOT remove tests** — even inadequate tests document something

## Output

```markdown
## Test File: `<path>`

### ADEQUATE
- `test_<name>`: Tests `<method>` with nontrivial assertion `<specific assertion>`

### INADEQUATE
- `test_<name>`: Tests `<method>` — ISSUE: trivial witness (zero vector)
- `test_<name>`: Tests `<method>` — ISSUE: content-free assertion (`is not None`)
- `test_<name>`: Tests `<method>` — ISSUE: interoperability-only, no independent oracle

### ORPHAN
- `test_<name>`: Tests `<method>` — not in any checklist

### MISSING (methods from checklist with no test)
- `<method>`: No test found
```

## Success Criteria

- Every test in file classified
- Specific inadequacy identified for each INADEQUATE test
- Orphan tests identified (may be intentional, but should be flagged)
- Missing tests identified for checklist methods
