## CI Constraints (MANDATORY)

This runs in a CI environment. Follow these rules exactly:
- **Do NOT modify any workflow files, scripts, or CI infrastructure.** You are running in a restricted mode.
- Do not ask questions. Do not request confirmation. Do not pause for input.

## Skills in Context

These skills are loaded above — reference them directly:
`policy-index`, `bespoke-software-policy`, `test-guidelines`

## Task

Analyze the repository at commit `{{REPO_SHA}}` for structural code defects, architectural decay, and quality regressions.

**CRITICAL: Ignore all Pull Request context.** This is not a PR review.

### Execution

1. Run `tree -L 3` to understand directory layout.
2. Identify hotspots: most-churned files (last 3 months), oldest untouched files, recently modified files.
3. Read key configs, docs, justfile commands.
4. Read source code from high-churn and old files.
5. Check test quality, dead code, architectural problems.
6. Apply the Six Decay Risks (R1-R6) to real files you read.
7. Record every file you read in `checked_surfaces` with the reason and lines examined.

### Output Format

Write a JSON report to `.agents/review-runner/candidates/submitted.json`.

To get the exact schema (fields, types, constraints), run:
`quality-control/ci/submit-candidate --help`

Key rules every finding must satisfy:

- `violated_invariant`: The named contract, behavior, or invariant that was violated. "This file is too long" is insufficient — what behavior fails because of this length? A violated invariant names a required behavior that is provably impossible, silently skipped, unverifiable, or non-deterministic.
- `proof_command`: The exact command, grep pattern, or code path that proves the violation exists. A file path alone is not proof — show the command output, the code flow, or the diagnostic that demonstrates the failure.
- `symptom`, `source`, `consequence`, `remedy`: Standard Brooks structure.
- `evidence`: At least one entry with `kind`, `path`, and `lines` showing the exploration.

**Tier rules:**
- **Tier 1** (significant): Label as `[BLOCKER]` or `[SHOULD FILE ISSUE]`. Must have a non-low-signal category.
- **Tier 2** (cleanup): Label as `[NOTE]`. Lower-signal categories (code-style, naming, formatting, file-length, etc.) must be Tier 2.

**Forbidden:**
- Findings whose `category` contains `infra`, `infrastructure`, `ci`, `workflow`, or `config`.
- Findings about files in `.github/`, `.agents/`, `quality-control/`, or `opencode/skills/`.
- `score` and `report` fields — the renderer derives the score from findings and builds the comment markdown automatically.

## Submitting Your Report

Write your report to `.agents/review-runner/candidates/submitted.json`.
Then run `quality-control/ci/submit-candidate` (no arguments).

If the script exits 0, your report was accepted and you are done.
If it exits non-zero, read the errors, fix the SAME file, and re-run the script.
Repeat until the script exits 0.
