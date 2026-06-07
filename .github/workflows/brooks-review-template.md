## CI Constraints (MANDATORY)

This runs in a CI environment. Follow these rules exactly:
- **Do NOT output the report to stdout.** The recipe is the only submission path.
- Do not ask questions. Do not request confirmation. Do not pause for input.
- Run `just -f .agents/justfile` to discover available recipes — do not guess paths.

## Skills in Context

These skills are loaded above — reference them directly:
`policy-index`, `bespoke-software-policy`, `anti-slop`, `reviewing-llm-code`, `test-guidelines`

Baseline:
- No fallback suggestions (every missing resource must fail loudly)
- No mock/fake/stub as proof (real data or nothing)
- No runtime defaults for critical dependencies
- No try-import or conditional stubs
- Every assertion must genuinely increase proof burden
- Every finding must cite file paths, line numbers, and exploration evidence
- Findings about CI infrastructure are rejected (see sweep protocol exclusions)

## Task

You have two jobs — do BOTH:

### 1. PR Review
Review the diff below. Produce Symptom→Source→Consequence→Remedy findings for anything wrong in the changed code.

### 2. Full Codebase Sweep
Scan the entire repository for issues following the **CI Sweep Protocol** above:
- Start with `tree -L 3` to understand structure
- Find hotspots: most-churned files (last 3 months), oldest untouched files, recently modified files
- Read key configs, docs, justfile commands
- Read source code from high-churn and old files
- Check test quality, dead code, architectural problems
- Apply the Six Decay Risks (R1-R6) to real files you read

### Labeling and Priority
Follow the **Finding Classification Tiers** in the CI Sweep Protocol:
- **Tier 1** (significant): full Symptom→Source→Consequence→Remedy with decay-risk label. Label as `[PR BLOCKER]` or `[SHOULD FILE ISSUE]`.
- **Tier 2** (cleanup): single-line list only. Label as `[NOTE]`.
- **Priority rule**: if any Tier 1 findings exist, report them and skip Tier 2. Only report cleanup notes when the repo has zero significant issues.

### Diff
```diff
{{DIFF}}
```

### Output Format
Follow the sweep protocol's format: Tier 1 findings get full Symptom→Source→Consequence→Remedy with Health Score (0-100) for the diff changes and separately for the full repo. Tier 2 findings get a single-line cleanup list appended only if Tier 1 is empty.

## Submitting Your Report

The ONLY way to submit a report is through the validation recipe:

1. Write your report and score to a **temporary JSON file** (e.g. `/tmp/brooks-report.json`):
   ```json
   {"report": "<full report text with all findings>", "score": <0-100>}
   ```

2. Run the recipe:
   ```
   just -f .agents/justfile post-brooks-review /tmp/brooks-report.json {{PR_NUMBER}}
   ```

3. If the recipe **fails** (exit non-zero): read the validation errors, fix the report, and retry.

4. If the recipe **succeeds**: it creates `.brooks-report-artifact.json` with the validated report.

Do NOT write to `.brooks-report-artifact.json` directly — only the recipe can create it.
Do NOT output the report to stdout — the recipe is the only submission path.

