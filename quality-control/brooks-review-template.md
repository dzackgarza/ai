## CI Constraints (MANDATORY)

This runs in a CI environment. Follow these rules exactly:
- **Do NOT modify any workflow files or CI infrastructure.** You are running in a restricted mode.
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

### Diff
```diff
{{DIFF}}
```

### Output Format
The harness requires a strict JSON file format. Plain text reports will be rejected.
The JSON must conform to the following schema precisely:

```json
{
  "schema_version": 1,
  "repo_sha": "HEAD",
  "pr_number": {{PR_NUMBER}},
  "review_scope": {
    "changed_files": ["src/example.py"],
    "excluded_files": [],
    "required_surfaces": []
  },
  "findings": [
    {
      "tier": "tier1",
      "label": "PR BLOCKER",
      "category": "semantic-regression",
      "location": {
        "path": "src/example.py",
        "start_line": 10,
        "end_line": 25,
        "quoted_text_sha256": ""
      },
      "symptom": "...",
      "source": "...",
      "consequence": "...",
      "remedy": "...",
      "evidence": [
        {
          "kind": "file-read",
          "path": "src/example.py",
          "lines": [1, 80]
        }
      ]
    }
  ],
  "checked_surfaces": [
    {
      "path": "src/example.py",
      "reason": "changed-file",
      "lines_read": [1, 120],
      "result": "finding"
    }
  ],
  "rejected_easy_wins": [],
  "score": 95,
  "report": "Fallback markdown report summary here..."
}
```

- Tier 2 findings are not allowed if any Tier 1 findings exist.
- Meta/infrastructure findings about agent configs, tests, CI workflows, or harness files are strictly forbidden and will cause rejection.
- All locations must correspond to real files in the repository.

## Submitting Your Report

The ONLY way to submit your candidate report is to write the JSON to a file in the candidates directory: `{{CANDIDATES_DIR}}`.

1. Write your full JSON report to `{{CANDIDATES_DIR}}/attempt-0.json`.
2. Do NOT try to write `.brooks-report-artifact.json` directly. The harness will validate your candidate and write the artifact itself if validation passes.
3. If the harness rejects your candidate, it will automatically restart you with a continuation prompt containing the exact validation errors.