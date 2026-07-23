## Pattern 11: Post-Commit Regression After Cleanup Commits

**Symptom:** A card’s review passes because the code is clean at the time of the cleanup
commit. Later, an unrelated implementation commit modifies the same files, reintroducing
lint/fmt/findings. The card’s evidence is now stale and its claims are false.

**Detection:** Before accepting any review claim that “all checks pass,” re-run the
validation commands against the CURRENT HEAD, not the historical commit.
A subagent reviewing a card from 6 hours ago must verify the card’s claims hold now, not
just at the time the work was done.

**Root cause:** Commit sequence:

1. Commit A: “style: clear remaining E501” — all clean

2. Commit B: “fix: repair 6 implementation bugs” — modifies same files, adds long import
   alias (92 chars → E501) and unsorted import block (→ I001)

3. Card claims “ruff check passes” based on state at commit A — stale

**Fix:** The subagent reviews against the workspace as it exists now.
If the card claims validation passes but the current workspace fails, the card fails
Gate 2 or Gate 6. Fix the findings and update the evidence, or mark the card as
`revision-required` with the specific findings.

**Prevention:** When a cleanup card depends on no other implementation work being done
on the same files, record that as a known risk.
If implementation work on the same branch may follow, use a dedicated cleanup branch to
isolate the cleanup from subsequent changes.
