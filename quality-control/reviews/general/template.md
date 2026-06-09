## CI Constraints (MANDATORY)

This runs in a CI environment. Follow these rules exactly:
- **Do NOT modify any workflow files, scripts, or CI infrastructure.** You are running in a restricted mode.
- Do not ask questions. Do not request confirmation. Do not pause for input.

## Skills in Context

These skills are loaded above — reference them directly:
`policy-index`, `bespoke-software-policy`, `test-guidelines`

Baseline:
- No fallback suggestions (every missing resource must fail loudly)
- No mock/fake/stub as proof (real data or nothing)
- No runtime defaults for critical dependencies
- No try-import or conditional stubs
- Every assertion must genuinely increase proof burden
- Every finding must cite file paths, line numbers, and exploration evidence
- Findings about CI infrastructure are rejected (see sweep protocol exclusions)
- **PEP 723 Mandate**: Any agent-authored or modified Python script that imports third-party packages MUST declare dependencies via PEP 723 inline script metadata. Reject any finding that suggests adding to `pyproject.toml` for standalone scripts.
- **No blanket affirmative claims.** Every statement about a file must cite specific evidence (code read, diff, analysis). "All other code passed without violations" is rejected — if you have nothing to say about a file, say nothing. Do not pad reports with unsubstantiated "clean" assertions.

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

Identify and report structural code defects, architectural decay, and quality regressions anywhere in the codebase.

### Output Format
The harness requires a strict JSON file format. Plain text reports will be rejected.
The JSON must conform to the following schema precisely:

```json
{
  "schema_version": 1,
  "report_type": "general",
  "repo_sha": "{{REPO_SHA}}",
  "review_scope": [
    "src/main.ts",
    "src/utils.ts",
    "tests/test_main.ts"
  ],
  "findings": [
    {
      "tier": "tier1",
      "label": "BLOCKER",
      "category": "semantic-regression",
      "location": {
        "path": "src/foo.ts",
        "start_line": 10,
        "end_line": 25,
        "quoted_text_sha256": "optional-sha"
      },
      "symptom": "...",
      "source": "...",
      "consequence": "...",
      "remedy": "...",
      "evidence": [
        {
          "kind": "file-read",
          "path": "src/foo.ts",
          "lines": [1, 80]
        }
      ]
    }
  ],
  "checked_surfaces": [
    {
      "path": "src/foo.ts",
      "reason": "high-churn",
      "lines_read": [1, 120],
      "result": "finding"
    }
  ],
  "rejected_easy_wins": [],
  "score": 85,
  "report": "## Findings\n\nFull formatted report here. No Scope section — use checked_surfaces for that."
}
```

- **Tier 1** (significant): Label as `[BLOCKER]` or `[SHOULD FILE ISSUE]`.
- **Tier 2** (cleanup): Label as `[NOTE]`. Append ONLY if Tier 1 is empty.
- Meta/infrastructure findings about agent configs, tests, CI workflows, or harness files are strictly forbidden and will cause rejection.
- All locations must correspond to real files in the repository.
- **No "Scope" section in the report markdown.** The `checked_surfaces` array documents what files you read and why. The `report` field is for findings only.

## Submitting Your Report

Write your report to `.agents/review-runner/candidates/submitted.json`.
Then run `quality-control/ci/submit-candidate` (no arguments).

If the script exits 0, your report was accepted and you are done.
If it exits non-zero, read the errors, fix the SAME file, and re-run the script.
Repeat until the script exits 0.
