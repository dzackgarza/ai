# Example Task: Mathematical Contract Audit

## Goal

Pick one reference doc. **Audit EVERY method in that doc** — verify all mathematical assumptions and constraints are explicitly stated with upstream citations. Do not stop until the ENTIRE reference doc is verified.

## Process

1. First, **select ONE reference doc** — e.g., `docs/sage/lattice/research_readme.md`
2. Then, **read the doc line by line** — do not skim
3. Then, **for each method**, grep the upstream docs to verify constraints exist
4. Then, **accumulate ALL gaps** — list every method missing constraints (do NOT fix individually)
5. Then, **batch-fix all gaps** — add constraints to all missing methods in one pass
6. Then, **show evidence**: "Verified X methods, found Y gaps in [list], here's specific evidence from upstream [file] that constraints were missing..."

Show your reasoning at each step. Do not skip steps.

## Workflow

1. **Select a reference doc** — e.g., `docs/sage/lattice/sagemath_lattice_reference.md`
2. **For each method entry, verify:**
   - **Domain constraints**: positive-definite only? indefinite OK? degenerate forms?
   - **Ring/field restrictions**: ℤ-only? ℚ? arbitrary fields?
   - **Non-degeneracy requirements**: does method require non-degenerate form?
   - **Signature constraints**: definite, indefinite, or both?
   - **Integrality constraints**: does method require integral Gram matrix?
3. **Flag missing contracts:**
   - Methods with no domain tag (e.g., `[PD]`, `[INDEF]`, `[DEG]`)
   - Methods with vague caveats ("usually", "typically")
   - Methods with unstated ring assumptions
4. **Add explicit contract language:**
   - Replace vague deferrals with exact truth values from upstream
   - Add tag legend entries for each constraint type

## Example Output

```markdown
# Before: Multiple methods in sage/lattice reference doc lacked domain constraints

After: Added [PD] tag to 23 methods (LLL, isom, genus, etc.), [INT] tag to 8 methods 
(twist, rescale, etc.), [DEFINITE] tag to 5 methods (mass, signature_pair). 
All with upstream source citations from docs/sage/upstream/*.html

This matters because users calling indefinite lattices into PD-only methods 
would encounter silent failures or incorrect results.
```

## Purpose

This task ensures mathematical precision, not vague approximations.

## Anti-Patterns

- Vague claims: `usually`, `typically`, `often`, `most of the time` — replace with exact truth values
- Weak deferrals: `unknown`, `unverified`, `needs testing` — answer through docs/source/web research where reasonably possible
