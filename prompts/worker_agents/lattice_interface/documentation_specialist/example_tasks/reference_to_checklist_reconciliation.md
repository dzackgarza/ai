# Example Task: Reference-to-Checklist Reconciliation

## Goal

Pick one package. **Ensure EVERY method in the reference doc has a checklist entry AND every checklist entry has a reference doc entry.** Do not stop until the entire package surface is reconciled.

## Process

1. First, **select ONE package** — e.g., `forms`
2. Then, **extract ALL methods from the reference doc** — parse the entire file
3. Then, **extract ALL entries from the checklist** — parse the entire file
4. Then, **compare the two lists** — find methods missing from checklist, entries missing from reference
5. Then, **accumulate ALL discrepancies** — do NOT fix one at a time
6. Then, **batch-add missing entries** — add all missing checklist entries, mark all missing reference entries for investigation
7. Then, **show evidence**: "Package X has Y methods in reference, Z entries in checklist. Found A gaps: [list]. Here's specific evidence [diff]..."

Show your reasoning at each step. Do not skip steps.

## Workflow

1. **Select a package** — e.g., `forms` (GAP package)
2. **Extract method lists:**
   - Parse `docs/forms/lattice/forms_lattice_reference.md` for all documented methods
   - Parse `docs/forms_methods_checklist.md` for all checklist entries
3. **Find discrepancies:**
   - Methods in reference doc but not in checklist → add checklist entries
   - Methods in checklist but not in reference doc → **mark for investigation**, do not delete:
     - Add `[INVESTIGATE]` tag to the checklist entry
     - Add a TODO.md item: "Investigate `<method_name>` — in checklist but not in reference doc or upstream"
     - Continue with other work; investigation requires git blame, internet research, upstream verification
4. **Verify alignment:**
   - Each checklist entry should cite the reference doc section
   - Each reference doc method should have corresponding checklist item

## Example Output

```markdown
Added to forms_methods_checklist.md:
- [ ] `OrthogonalComponentsOfSubgroup(U, n)` — missing from checklist

Flagged for investigation:
- [ ] `[INVESTIGATE] SomeLegacyMethod()` — in checklist but not in reference doc or upstream
  TODO.md: "Investigate SomeLegacyMethod — in checklist but not in reference doc or upstream"
```

## Purpose

This task ensures checklists and reference docs track the same method surface.

## Important Note

Do not delete checklist entries that lack reference doc coverage. Mark them for investigation instead — they may represent real methods that were documented incorrectly or removed from upstream.
