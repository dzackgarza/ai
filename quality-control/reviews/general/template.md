## CI Constraints (MANDATORY)

This runs in a CI environment. Follow these rules exactly:
- **Do NOT modify any workflow files, scripts, or CI infrastructure.** You are running in a restricted mode.
- Do not ask questions. Do not request confirmation. Do not pause for input.

## Task

Analyze the code in scope (defined by the scope instructions above) for structural code defects, architectural decay, and quality regressions.

### Execution

1. Cover the code in scope following the coverage strategy from the scope instructions above.
2. Check test quality, dead code, architectural problems.
3. Apply the Six Decay Risks (R1-R6) to real files you read.
4. Record every file you read in `checked_surfaces` with the reason and lines examined.

### No Remediation

Diagnose only. Do not propose fixes, patches, or code changes — remediation is
handled by separate agents after disposition.

### Output Format

Write a JSON report to `.agents/review-runner/candidates/submitted.json`.

To get the exact schema (fields, types, constraints), run:
`submit-candidate --help`

Key rules every finding must satisfy:

- `violated_invariant`: The named contract, behavior, or invariant that was violated. "This file is too long" is insufficient — what behavior fails because of this length? A violated invariant names a required behavior that is provably impossible, silently skipped, unverifiable, or non-deterministic.
- `proof_command`: The exact command, grep pattern, or code path that proves the violation exists. A file path alone is not proof — show the command output, the code flow, or the diagnostic that demonstrates the failure.
- `symptom`, `source`, `consequence`: diagnosis only — what is observably wrong, what produces it, what breaks because of it.
- `evidence`: At least one entry with `kind`, `path`, and `lines` showing the exploration.

**Tier rules:**
- **Tier 1** (significant): Label as `[BLOCKER]` or `[SHOULD FILE ISSUE]`. Must have a non-low-signal category.
- **Tier 2** (cleanup): Label as `[NOTE]`. Lower-signal categories (code-style, naming, formatting, file-length, etc.) must be Tier 2.

**Forbidden:**
- Findings whose `category` contains `infra`, `infrastructure`, `ci`, `workflow`, or `config`.
- Findings about files in `.github/`, `.agents/`, `quality-control/`, or `opencode/skills/`.
- `score` and `report` fields — rejected by the validator.

## Submitting Your Report

Write your report to `.agents/review-runner/candidates/submitted.json`.
Then run `submit-candidate` (no arguments).

If the script exits 0, your report was accepted and you are done.
If it exits non-zero, read the errors, fix the SAME file, and re-run the script.
Repeat until the script exits 0.
