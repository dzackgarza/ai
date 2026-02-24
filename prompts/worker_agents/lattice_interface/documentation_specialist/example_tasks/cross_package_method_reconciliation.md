# Example Task: Cross-Package Method Reconciliation

## Goal

Pick one algorithm that appears across multiple packages (e.g., LLL, HNF, SVP). **Verify EVERY package's documentation has complete, package-specific signatures and caveats.** Do not stop until all packages are reconciled.

## Process

1. First, **select ONE algorithm** — e.g., `LLL`
2. Then, **identify ALL packages implementing it** — Sage, FLINT, NTL, fpylll, PARI/GP, GAP
3. Then, **for each package**, read its reference doc entry completely
4. Then, **extract all signature variations** — parameters, defaults, return types
5. Then, **extract all constraint differences** — domain restrictions, limitations
6. Then, **accumulate ALL discrepancies** — do NOT document one package at a time
7. Then, **batch-document all differences** — create comparison table for all packages
8. Then, **show evidence**: "Algorithm X appears in Y packages. Found Z signature variations. Here's specific evidence [list]..."

Show your reasoning at each step. Do not skip steps.

## Workflow

1. **Select a method** — e.g., `LLL`
2. **Inventory all packages implementing it:**
   - SageMath: `IntegralLattice.LLL()`, `IntegerLattice.LLL()`
   - FLINT: `fmpz_lll()`, `fmpz_lll_context_init()`
   - NTL: `LLL()`, `LLL_plus()`
   - fpylll: `LLL.reduction()`, `lll_reduction()`
   - PARI/GP: `qflll()`, `qflllgram()`
   - GAP: `LLLReducedBasis()`, `LLLReducedGramMat()`
3. **For each package:**
   - Verify full signature (all parameters, defaults, return types)
   - Document package-specific behavior differences
   - Capture domain constraints (e.g., "positive-definite only" vs. "works for indefinite")
4. **Note discrepancies:**
   - Different parameter names for same concept
   - Different default values
   - Different return value conventions
   - Package-specific limitations

## Example Output

```markdown
LLL parameter comparison:
- SageMath: `delta=0.99` (implicit), returns new lattice object
- FLINT: `delta ∈ (0.25, 1)` explicit constraint, in-place reduction
- fpylll: `delta=LLL_DEF_DELTA`, `eta=LLL_DEF_ETA` explicit constants
- PARI/GP: `flag` parameter controls output format
```

## Purpose

This task ensures cross-package method surfaces are precisely documented, not vaguely similar.
