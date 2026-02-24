# Example Task: Interface Contract Audit

## Goal

Audit the interface contracts for a set of methods. Verify that contracts are explicit, mathematically correct, and complete.

## Workflow

1. **Select methods** from a reference doc or checklist (10-20 methods)
2. **For each method**, extract and verify:
   - Input types and constraints
   - Output types and guarantees
   - Mathematical preconditions
   - Mathematical postconditions
   - Error conditions and exceptions

## Contract Completeness Checklist

### Input Specification

- [ ] All parameters have explicit types
- [ ] Required vs optional parameters are clear
- [ ] Default values are documented
- [ ] Parameter constraints are explicit (e.g., "must be positive-definite")

### Output Specification

- [ ] Return type is explicit
- [ ] Return value meaning is clear
- [ ] Multiple return values are documented
- [ ] Return invariants are stated (e.g., "returns reduced basis")

### Preconditions

- [ ] Domain constraints explicit (ring, field, definiteness)
- [ ] Dimension/rank constraints explicit
- [ ] Non-degeneracy requirements stated
- [ ] Integrality requirements stated

### Postconditions

- [ ] What the method guarantees about output
- [ ] Invariants preserved (e.g., "lattice isomorphism class unchanged")
- [ ] Quality guarantees (e.g., "LLL-reduced with delta=0.99")

### Error Conditions

- [ ] What inputs cause errors
- [ ] What errors are raised
- [ ] Behavior on edge cases

## Common Contract Gaps

### Vague Types

```markdown
# Before (INADEQUATE)
- Input: matrix
- Output: lattice

# After (ADEQUATE)
- Input: `Matrix[Z]` — symmetric n×n integer matrix, non-degenerate
- Output: `IntegralLattice` — free ℤ-module with bilinear form given by input
```

### Missing Preconditions

```markdown
# Before (INADEQUATE)
`LLL()` — LLL reduction

# After (ADEQUATE)
`LLL()` — LLL reduction
- Preconditions: Gram matrix positive-semidefinite
- Postconditions: Returns δ-LLL-reduced basis with δ=0.99
```

### Implicit Constraints

```markdown
# Before (INADEQUATE)
`genus()` — returns genus representatives

# After (ADEQUATE)
`genus()` — returns genus representatives
- Preconditions: Lattice defined over ℤ
- Constraints: Only for positive-definite lattices
- Postconditions: Representatives are pairwise non-isometric
```

## What NOT To Do

- **Do NOT run code**
- **Do NOT implement methods** — only audit contracts
- **Do NOT add backward-compatibility constraints** — interface is still being defined
- **Do NOT preserve incorrect names** — rename if mathematically wrong

## Output

```markdown
## `<method_name>`

### COMPLETE
- Types: explicit and correct
- Preconditions: all stated
- Postconditions: all stated
- Errors: documented

### INCOMPLETE
- Missing: [e.g., "positive-definite precondition not stated"]
- Vague: [e.g., "'matrix' should be 'Matrix[Z]'"]
- Implicit: [e.g., "ℤ-only constraint not documented"]

### INCORRECT
- Wrong type: [e.g., "says Matrix[Q] but requires Matrix[Z]"]
- Wrong constraint: [e.g., "says works for indefinite, but only PD is correct"]
```

## Success Criteria

- All selected methods audited
- Missing/incorrect contracts identified
- Specific gaps named (not just "incomplete")
