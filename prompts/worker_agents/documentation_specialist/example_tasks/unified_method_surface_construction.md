# Example Task: Unified Method Surface Construction

## Goal

**Consolidate ALL per-package checklist methods into a single unified surface.** Ensure EVERY method from EVERY package is included, with duplicates grouped. Do not stop until all packages are unified.

## Process

1. First, **inventory ALL checklist files** — list every `docs/*_methods_checklist.md`
2. Then, **extract ALL methods from each checklist** — parse every file completely
3. Then, **identify ALL duplicate operations** — methods across packages that do the same thing
4. Then, **group ALL methods by operation** — LLL together, HNF together, SVP together, etc.
5. Then, **create unified entries** — one entry per unique operation, pointing to all source checklists
6. Then, **verify complete coverage** — ensure no method is missing
7. Then, **show evidence**: "Unified Y packages with Z total methods. Grouped into W operations. Here's the complete mapping [table]..."

Show your reasoning at each step. Do not skip steps.

## What This Is

Take every method from every package checklist. If two or more methods from different packages perform the same mathematical operation, they become one entry pointing to those checklists.

This is an index — detailed source/doc information lives in the original checklists.

## Workflow

1. **Extract all methods** from all package checklists
2. **Identify duplicates**: Methods from different packages that perform the same mathematical operation
3. **Build unified entries**: One entry per unique mathematical operation, referencing original checklists:

   ```markdown
   ## LLL Reduction
   - SageMath: `IntegralLattice.LLL()` → sage_methods_checklist.md
   - FLINT: `fmpz_lll()` → flint_methods_checklist.md
   - fpylll: `LLL.reduction()` → fpylll_methods_checklist.md
   - NTL: `LLL()` → ntl_methods_checklist.md
   - PARI/GP: `qflll()` → pari_gp_methods_checklist.md
   - GAP: `LLLReducedBasis()` → gap_methods_checklist.md
   
   ## HNF
   - FLINT: `fmpz_mat_hnf()` → flint_methods_checklist.md
   - SageMath: `hermite_form()` → sage_methods_checklist.md
   - GAP: `HermiteNormalForm()` → gap_methods_checklist.md
   ```

4. **Unique methods**: If a method has no equivalent, single entry pointing to its checklist

## Output

`docs/unified_method_surface.md` — union of all methods with grouped implementations, each pointing to its source checklist for details.

## Success Criteria

- Every method from every checklist appears
- Same-operation methods grouped under one heading
- Each entry links to original checklist (not to upstream docs directly)
