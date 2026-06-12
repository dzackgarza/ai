---
name: jules-anti-slop-report-review
description: Use when launching Jules as an asynchronous anti-slop review scout. Jules receives the full anti-slop/reviewing-LLM-code curriculum and writes a candidate JSON report file. Do not use this workflow for immediate fixing, PR thread resolution, or implementation.
---

# Jules Anti-Slop Report Review

Jules is not trusted to complete complex work independently.
Use Jules as an asynchronous review scout: prime it with the full anti-slop curriculum,
ask it to inspect a PR/branch/commit range thoroughly, and require it to write a
candidate JSON report file matching the `submit-candidate` validation schema (which exposes review-type-specific schemas via `--help`).

The Jules report is not an implementation instruction.
It is a durable review artifact for later human/agent triage.

Do not pipe Jules findings back into implementation without independent review.
Addressing findings is a separate PR workflow.

## Workflow Separation

### Phase A — Asynchronous report generation

1. **Identify the target**:
   - repo (owner/name)
   - PR URL, branch, or commit range
   - original issue/task/PR contract if available
   - known constraints and non-goals

2. **Build a large Jules prompt containing**:
   - full anti-slop guidance
   - `reviewing-llm-code` guidance
   - pattern catalog and failure-mode references
   - `test-guidelines` if tests/QC are in scope
   - `known-solution-first` if dependency/reinvention is in scope
   - the target PR/branch/diff context
   - the JSON schema and validation rules below

3. **Launch Jules asynchronously**.

4. **Jules performs the review and writes a candidate JSON report file**.

5. **The controller records the Jules session link and stops**.

No code is changed in this phase.
No PR is opened.
No issue is created.

### Phase B — Later remediation

A later PR may address the Jules report findings.

That PR must:
1. Load `pr-feedback-triage`, `reviewing-llm-code`, `anti-slop`, and `test-guidelines`
   as applicable.
2. Triage each finding independently.
3. Accept, accept-with-modified-remediation, reject, or investigate each finding.
4. Implement only accepted findings.
5. Close the report only when accepted findings are fixed or all findings are visibly
   dispositioned.

Do not assume Jules findings are correct.
Do not treat the report as a task list until triaged.

## Prompt Construction

The prompt must heavily constrain Jules:

```
You are Jules.
You are NOT implementing code in this task.
You are performing an anti-slop review of LLM-produced work.
Your only deliverable is a JSON report file written to the repo at
`slop-report.json` (or a name matching `*slop-report*.json`).

Do not edit source files.
Do not open a PR.
Do not create any issue.
Do not fix findings.
Do not approve or reject the target PR.
Do not perform a generic code review.

You must output valid JSON matching the schema below.
Validation is performed by `submit-candidate`.
If validation fails, the report is rejected and you will be re-prompted with
the exact validation errors.

The JSON file must be at the repo root and named `slop-report.json`.
```

Then provide:

```
Target:
- Repository:
- PR / branch / commit range:
- Original task / PR contract:
- Known constraints:
- Out-of-scope areas:

Curriculum:
<full anti-slop/reviewing-llm-code/pattern-catalog/failure-mode text>

JSON Schema and Validation Rules:
<schema and rules below>
```

The review curriculum must be fully embedded into the prompt since Jules cannot be
trusted to discover or apply it from memory.

## JSON Schema

The report must be valid JSON conforming to the following schema.
Validation is performed by `submit-candidate --help` (displays schema) followed by `submit-candidate` (validates the report).

### Top-level fields

| Field | Type | Required |
|---|---|---|
| `schema_version` | integer | yes |
| `repo_sha` | string (commit SHA) | yes |
| `review_scope` | object | yes |
| `findings` | array of finding objects | yes |
| `checked_surfaces` | array of surface objects | yes |
| `score` | integer | yes |
| `report` | string (markdown) | yes |
| `report_type` | `"slop"` | yes |

```json
{
  "schema_version": 1,
  "report_type": "slop",
  "repo_sha": "abc123...",
  "review_scope": {
    "changed_files": ["src/foo.ts", "src/bar.py"],
    "excluded_files": [],
    "required_surfaces": ["src/"]
  },
  "findings": [
    {
      "tier": "tier1",
      "label": "SLOP",
      "category": "bridge-burning",
      "location": {
        "path": "src/foo.ts",
        "start_line": 10,
        "end_line": 25
      },
      "pattern": "mechanism, not symptom",
      "task_narrative": "What was the user actually asking for?",
      "slop_narrative": "How did the agent produce this instead of fulfilling the task?",
      "why_it_matters": "How this mechanism lets bad work pass or hides failures.",
      "user_surprise": "How this minimizes agent errors at the cost of user surprise.",
      "existential_justification": "Why does this code exist at all?",
      "failure_mode": "name from loaded failure-mode skills",
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
      "reason": "slop-scan",
      "lines_read": [1, 120],
      "result": "finding"
    }
  ],
  "score": 75,
  "report": "## Slop Audit Summary\n\nFull formatted markdown report for human consumption."
}
```

### Finding fields (for `report_type: "slop"`)

Each finding object must have exactly these fields:

| Field | Type | Constraints |
|---|---|---|
| `tier` | string | `"tier1"` or `"tier2"` |
| `label` | string | `"SLOP"`, `"SLOP SUSPECT"`, or `"NOTE"` |
| `category` | string | must NOT contain any forbidden category (see below) |
| `location` | object | must have `path`, `start_line`, `end_line`; path must exist in commit |
| `pattern` | string | mechanism-level pattern name, not symptom |
| `task_narrative` | string | what the user originally asked for |
| `slop_narrative` | string | how the agent substituted the artifact for the task |
| `why_it_matters` | string | how this lets bad work pass |
| `user_surprise` | string | cost to user vs cost to agent |
| `existential_justification` | string | why this code exists instead of using existing solutions |
| `failure_mode` | string | name from loaded failure-mode skills |
| `evidence` | array of objects | each with `kind`, `path`, `lines`; at least one required |

### `report` field — mandatory markdown markers

The `report` string must contain all of the following markers (as regex patterns):

- `Finding \d+`
- `Pattern:`
- `Concrete evidence:`
- `Original requested task narrative:`
- `Descent into slop narrative:`
- `Why this matters:`
- `User surprise analysis:`
- `Existential justification:`
- `Failure mode:`

The report must be at least 200 characters of substantive analysis.

### Forbidden categories

Findings in these categories will be rejected:

- `meta`
- `infrastructure`
- `ci-workflow`
- `agent-config`
- `harness`
- `environment`

### Forbidden paths

Findings against files under these paths will be rejected:

- `.github/`
- `.agents/`
- `quality-control/`
- `opencode/`
- `.opencode/`
- `.serena/`
- `.claude/`
- `.git/`
- `nginx.conf`
- `.envrc`
- `justfile`
- `home-justfile`
- `pyproject.toml`
- `package.json`
- `package-lock.json`
- `uv.lock`
- `.gitignore`

### Tier rules

- If any `tier1` finding exists, no `tier2` findings are allowed.
  All tier2 findings must be dropped; only fix the tier1 issues first.

### Rejected patterns

The following concerns must NEVER appear as findings:

- Python's `-O` (optimized) mode or `assert` removal. This is an esoteric concern that
  does not apply. Findings mentioning `-O` or "optimized mode" will be rejected.

## File Output

The report must be written to a JSON file at a path matching `*slop-report*.json` in
the repo root (e.g., `slop-report.json`).

Do not write to any other location.
Do not write non-JSON formats.
Do not create issues, PRs, or any other artifact.

The pre-commit hook will validate that staged files matching `*slop-report*.json`
or `*brooks-report*.json` pass `submit-candidate`.

## Addressing a Jules Report

This is a separate task. Use `pr-feedback-triage`, `reviewing-llm-code`, `anti-slop`,
and `test-guidelines`.

A remediation PR should:
1. Reference the Jules report.
2. Select one or more findings to triage.
3. For each selected finding, state:
   - Jules claim
   - disposition
   - evidence
   - remediation or rejection rationale
4. Implement only accepted findings.
5. Leave untriaged findings in the report.
