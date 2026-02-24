# Example Task: Checklist Annotation

## Goal

Take one checklist file. **For EVERY method entry**, find its exact location in the local upstream docs and add a citation. Do not stop until ALL entries in the checklist are annotated.

## Process

1. First, **select ONE checklist file** — e.g., `docs/forms_methods_checklist.md`
2. Then, **identify all upstream source files** for that package
3. Then, **for each checklist entry**, grep the upstream files to find the method
4. Then, **record the exact file and section** for each method found
5. Then, **accumulate ALL citations needed** — do NOT add them one at a time
6. Then, **batch-add all source citations** to the checklist in one pass
7. Then, **show evidence**: "Verified X checklist entries, added Y citations from [upstream files], here's specific evidence [grep output showing method in upstream]..."

Show your reasoning at each step. Do not skip steps.

## Workflow

1. **Select a checklist** — e.g., `docs/flint_methods_checklist.md`
2. **For each checklist entry:**
   - Search upstream sources for the method signature
   - Record the exact file and section/line where it appears
   - Add a source citation to the checklist entry
3. **Flag discrepancies:**
   - Method in checklist but not in upstream docs → mark as unverified
   - Method in upstream docs but not in checklist → add missing entry
   - Signature mismatch → note the correct upstream form

## Example Output

```markdown
# Added source citations to all 47 PARI/GP checklist entries

Each entry now points to docs/pari_gp/upstream/vectors_matrices_linear_algebra.html
with section references. Previously only 12/47 had citations.

This matters because Goal 2 requires every checklist entry to have a cited 
local source for its documented signature and constraints.
```

## Purpose

This task ensures every checklist entry is grounded in actual upstream evidence.
