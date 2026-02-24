# Example Task: Unified Interface Type Design

## Goal

Design unified interface types based on the unified method surface checklist (`docs/unified_method_surface.md`). That checklist groups same-operation methods across packages; this task designs the unified type abstractions that correspond to those groupings.

## Prerequisite

This task requires `docs/unified_method_surface.md` to exist. If it doesn't, the doc_coverage task `unified_method_surface_construction.md` must be completed first.

## Workflow

1. **Read unified method surface** — `docs/unified_method_surface.md`
2. **For each grouped operation**, design a unified type:
   - Identify the mathematical concept
   - Extract common operations from all implementations
   - Design the unified protocol/interface
   - Document how it maps to each concrete package type

## Example

From unified method surface:
```markdown
## LLL Reduction
- SageMath: `IntegralLattice.LLL()` → sage_methods_checklist.md
- FLINT: `fmpz_lll()` → flint_methods_checklist.md
- fpylll: `LLL.reduction()` → fpylll_methods_checklist.md
- NTL: `LLL()` → ntl_methods_checklist.md
- PARI/GP: `qflll()` → pari_gp_methods_checklist.md
- GAP: `LLLReducedBasis()` → gap_methods_checklist.md
```

Design unified interface:
```markdown
## `LLLReduction` — Unified Interface

LLL basis reduction operation.

### Implementations (from unified method surface)

| Package | Method | Signature |
|---------|--------|-----------|
| SageMath | `IntegralLattice.LLL()` | `delta=0.99` |
| FLINT | `fmpz_lll()` | `delta, eta` explicit |
| fpylll | `LLL.reduction()` | `delta, eta, float_type` |
| NTL | `LLL()` | `delta, Deep=false` |
| PARI/GP | `qflll()` | `flag` for variants |
| GAP | `LLLReducedBasis()` | `delta, eta` |

### Unified Contract

```python
class LLLReduction(Protocol):
    def __call__(
        self, 
        basis: Matrix, 
        delta: float = 0.99,
        eta: float = 0.501
    ) -> tuple[Matrix, Matrix]:
        """Returns (reduced_basis, transformation_matrix)"""
```

### Parameter Mapping

| Unified | SageMath | FLINT | fpylll | GAP |
|---------|----------|-------|--------|-----|
| `delta` | implicit 0.99 | explicit | `delta` | `delta` |
| `eta` | implicit 0.501 | explicit | `eta` | `eta` |
```

## What NOT To Do

- **Do NOT remove existing types or methods**
- **Do NOT design without referencing unified method surface**
- **Do NOT create types for operations not in unified surface**
- **Do NOT claim any existing type is "wrong"**

## Output

For each unified operation group in the method surface, produce a unified interface specification with:
- Concrete implementations mapped
- Unified contract (signature, parameters, return type)
- Parameter mapping across packages
- Any gaps where an implementation differs significantly

## Success Criteria

- Every grouped operation in unified method surface has corresponding interface design
- Each design maps to all concrete implementations listed in the surface
- Unified contracts capture common semantics across packages
