## CI Constraints (MANDATORY)

This runs in a CI environment. Follow these rules exactly:
- **Do NOT modify any workflow files, scripts, or CI infrastructure.** You are running in a restricted mode.
- Do not ask questions. Do not request confirmation. Do not pause for input.

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
- **PEP 723 Mandate**: Any agent-authored or modified Python script that imports third-party packages MUST declare dependencies via PEP 723 inline script metadata. Reject any finding that suggests adding to `pyproject.toml` for standalone scripts.
- **Ignore Python `-O` Mode**: We do NOT care about Python's optimized mode (`-O`) that strips `assert` statements. It is a trivial, esoteric concern. Do NOT report the use of `assert` as a problem. Findings mentioning `-O` or "optimized mode" will be rejected.

## Task: Full Repository Audit

Perform a comprehensive, fresh analysis of the entire repository at the current commit (`{{REPO_SHA}}`). 

**CRITICAL: Ignore all Pull Request context.** This is a repository-wide sweep, not a PR review. Analyze all files as if this were a day-zero audit.

Follow the **CI Sweep Protocol** below:
- Start with `tree -L 3` to understand structure
- Find hotspots: most-churned files (last 3 months), oldest untouched files, recently modified files
- Read key configs, docs, justfile commands
- Read source code from high-churn and old files
- Check test quality, dead code, architectural problems
- Apply the Six Decay Risks (R1-R6) to real files you read

Identify and report structural code defects, architectural decay, and bridge-burning violations anywhere in the codebase.

### Output Format
The harness requires a strict JSON file format. Plain text reports will be rejected.
The JSON must conform to the following schema precisely:

```json
{
  "schema_version": 1,
  "report_type": "brooks",
  "repo_sha": "{{REPO_SHA}}",
  "review_scope": {
    "changed_files": [],
    "excluded_files": [],
    "required_surfaces": []
  },
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
  "report": "## Markdown Audit Report Summary\n\nInclude the full formatted report here for human consumption."
}
```

- **No Remediation**: Brooks review is an adversarial audit. You must diagnose defects and trace their causal path, not prescribe fixes. Finding fixes separately is the maintainer's job. Do not include remediation steps.
- **Tier 1** (significant): Label as `[BLOCKER]` or `[SHOULD FILE ISSUE]`.
- **Tier 2** (cleanup): Label as `[NOTE]`. Append ONLY if Tier 1 is empty.
- Meta/infrastructure findings about agent configs, tests, CI workflows, or harness files are strictly forbidden and will cause rejection.
- All locations must correspond to real files in the repository.

## Submitting Your Report

The ONLY way to submit your candidate report is to write the JSON to a file in the candidates directory: `{{CANDIDATES_DIR}}`.

1. Write your full JSON report to a file like `{{CANDIDATES_DIR}}/candidate.json`.
2. Do NOT try to write `.brooks-report-artifact.json` directly. The harness will validate your candidate and write the artifact itself if validation passes.
3. If the harness rejects your candidate, it will automatically restart you with a continuation prompt containing the exact validation errors.
