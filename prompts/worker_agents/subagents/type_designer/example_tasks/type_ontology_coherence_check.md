# Example Task: Type Ontology Coherence Check

## Goal

Verify that type definitions across the interface surface are coherent, non-contradictory, and form a consistent ontology.

## Workflow

1. **Inventory all types** used in interface contracts
2. **Build type hierarchy** — which types subsume which
3. **Check for contradictions** — same name, different meaning
4. **Check for gaps** — referenced types that aren't defined
5. **Check for redundancy** — multiple names for same concept

## Coherence Checks

### Type Definition Existence

Every type referenced in contracts must be defined somewhere:
```markdown
# GAP: `IntegralLattice` referenced but never defined
# FLINT: `fmpz_mat_t` used but not in type glossary
```

### Type Hierarchy Consistency

Subtype relationships must be consistent:
```markdown
# CONSISTENT
- `IntegralLattice` ⊂ `QuadraticLattice` ⊂ `FreeModule`
- Every `IntegralLattice` is a `QuadraticLattice`

# CONTRADICTION
- Doc A: `IntegralLattice` is over ℤ only
- Doc B: `IntegralLattice` accepts ℤ[√2] coefficients
```

### Cross-Package Type Mapping

Same concept should map consistently:
```markdown
# CONSISTENT
| Concept | SageMath | FLINT | GAP |
|---------|----------|-------|-----|
| Integer matrix | `Matrix(ZZ)` | `fmpz_mat_t` | `IsIntMatrix` |

# CONTRADICTION
| Concept | SageMath | FLINT |
|---------|----------|-------|
| Lattice | `IntegralLattice` | `fmpz_lll_context_t` |
# These are NOT the same thing — FLINT type is reduction context, not lattice
```

### Naming Consistency

Same mathematical concept should have consistent naming:
```markdown
# INCONSISTENT
- SageMath: `discriminant_group`
- GAP: `DiscriminantForm` 
- Oscar: `discriminant_module`
# All mean the same thing — should reconcile or explicitly distinguish
```

## Common Issues

### Phantom Types

Types referenced but never defined:
```python
def method() -> LatticeResult:  # LatticeResult undefined
```

### Type Drift

Same type name meaning different things in different places:
```markdown
# Type drift example
- `Lattice` in module A: free ℤ-module with bilinear form
- `Lattice` in module B: periodic arrangement in ℝ^n (physics sense)
```

### Missing Abstraction

Concrete types where abstract types would clarify:
```python
def isometry(L1, L2) -> Matrix:  # What kind of matrix? What constraints?
def isometry(L1, L2) -> Isometry:  # Better — defined type with contract
```

## What NOT To Do

- **Do NOT implement types** — only audit definitions
- **Do NOT add backward-compatibility aliases**
- **Do NOT preserve contradictory definitions** — flag for resolution

## Output

```markdown
## Type Ontology Report

### UNDEFINED TYPES
- `LatticeResult` — referenced in `method()` but not defined
- `ReductionContext` — used in FLINT wrapper, not in type glossary

### CONTRADICTIONS
- `IntegralLattice`: Doc A says ℤ-only, Doc B shows ℤ[√2] example
- `Lattice`: Module A means bilinear-form lattice, Module B means physics lattice

### INCONSISTENT NAMING
- Discriminant concept: `discriminant_group`, `DiscriminantForm`, `discriminant_module`
- Recommendation: Standardize on ONE name or document distinction

### HIERARCHY GAPS
- `QuadraticLattice` is defined but `FreeModule` parent type is not
```

## Success Criteria

- All referenced types inventoried
- Contradictions identified with specific locations
- Naming inconsistencies flagged
- Hierarchy gaps documented
