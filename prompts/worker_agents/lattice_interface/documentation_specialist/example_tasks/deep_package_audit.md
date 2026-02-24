# Example Task: Deep Package Audit

## Goal

Pick one in-scope package. **Read ALL upstream documentation for that package, then verify the ENTIRE reference doc and ENTIRE checklist.** Do not stop until the full package surface is audited.

## Process

1. First, **select ONE in-scope package** — e.g., `forms`
2. Then, **identify ALL upstream source files** for that package — list every file in `docs/<pkg>/upstream/`
3. Then, **read each upstream file completely** — do not skip
4. Then, **for each method found**, verify it appears in the reference doc with full signature
5. Then, **for each reference entry**, verify it appears in the checklist
6. Then, **accumulate ALL gaps** — methods missing from ref, methods missing from checklist, missing constraints
7. Then, **batch-fix all gaps** — add all missing entries in one pass
8. Then, **show evidence**: "Audited package X, read Y upstream files, verified Z methods, found W gaps [list], here's the specific evidence..."

Show your reasoning at each step. Do not skip steps.

## Workflow

1. **Select a package** — e.g., `flint`
2. **Identify ALL upstream sources** — List every documentation file or chapter available for that package.
3. **Iterate through EVERY source file:**
   - Read the file.
   - Identify every relevant lattice method.
   - **Verify against reference doc:** Does it have a full typed signature and constraints?
   - **Verify against checklist:** Is it present?
   - **Accumulate Gaps:** Do NOT stop after finding one. List *all* gaps found in this file.
4. **Batch Fix:** Apply fixes for all accumulated gaps.
5. **Repeat** until all identified source files are processed.

## Critical Points

- **ForAll, Not Exists:** You are verifying the *entire* package, not looking for *a* gap.
- Do not stop after the first fix.
- Do not skip reading upstream sources.
- Do not assume reference docs are complete.
- Every method must have full typed signature and constraints.
- Every checklist entry must correspond to a documented method.
