# Example Task: Test-Documentation Alignment Check

## Goal

For a set of methods, verify that tests align with documented contracts. Identify mismatches between what's documented and what's tested.

## Workflow

1. **Select methods** from a checklist (10-20 methods)
2. **For each method**:
   - Read the reference doc entry for contract/signature/constraints
   - Read the corresponding test
   - Compare test behavior to documented contract

## Alignment Checks

### Signature Alignment

- [ ] Test uses correct argument names
- [ ] Test uses correct argument types
- [ ] Test covers documented default values
- [ ] Test covers documented optional parameters

### Constraint Alignment

- [ ] Test respects documented domain constraints (e.g., positive-definite only)
- [ ] Test respects documented ring constraints (e.g., ℤ-only)
- [ ] Test covers edge cases mentioned in docs
- [ ] Test does NOT violate documented constraints

### Behavioral Alignment

- [ ] Test verifies the documented behavior (not some other behavior)
- [ ] Test covers documented return type
- [ ] Test covers documented edge-case behavior
- [ ] Test documents any undocumented behavior it relies on

### Coverage Gaps

- [ ] All documented variants are tested
- [ ] All documented constraints are exercised
- [ ] No tested behavior is absent from docs

## Mismatch Types

### Test-Missing-Constraint

Test violates a documented constraint:
```python
# Doc says: "Requires positive-definite Gram matrix"
# Test uses indefinite matrix without catching expected failure
L = IntegralLattice(matrix([[1,0],[0,-1]]))  # Indefinite!
L.lll()  # Should this fail? Doc says yes, test doesn't check.
```

### Test-Extra-Behavior

Test relies on undocumented behavior:
```python
# Doc says: "Returns shortest vector"
# Test asserts: result has norm 2
# But doc doesn't say which shortest vector or what norm to expect
assert v.norm() == 2  # Undocumented assumption
```

### Doc-Missing-Constraint

Doc omits a real constraint the test reveals:
```python
# Test only works over ℤ
L = IntegralLattice("A2")
# But doc doesn't say "integer lattices only"
```

### Signature-Mismatch

Test uses different signature than documented:
```python
# Doc: L.lll(delta=0.99)
# Test: L.lll(0.99)  # Positional, not keyword
```

## What NOT To Do

- **Do NOT run tests**
- **Do NOT fix code** — only identify mismatches
- **Do NOT assume test is wrong** — could be doc is wrong
- **Do NOT assume doc is wrong** — could be test is wrong
- **Do NOT add new tests or docs** — only flag mismatches

## Output

```markdown
## `<method_name>`

### MISMATCH: Test-Missing-Constraint
- Doc: "Requires positive-definite Gram matrix"
- Test: Uses indefinite matrix at line 45
- Fix direction: [unclear / add constraint check to test / remove constraint from doc]

### MISMATCH: Signature-Mismatch
- Doc: `method(a, b=1, c=2)`
- Test: `method(1, 2)` — uses positional for `c`
- Fix direction: Update test to use keyword args

### ALIGNED
- All constraints exercised
- Signature matches
- Behavior matches
```

## Success Criteria

- All selected methods checked
- Each mismatch identified with specific location
- Fix direction noted (even if uncertain which side is correct)
- No tests were run
