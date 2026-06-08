## CI Constraints (MANDATORY)

This runs in a CI environment. Follow these rules exactly:
- **Do NOT modify any workflow files, scripts, or CI infrastructure.** You are running in a restricted mode.
- Do not ask questions. Do not request confirmation. Do not pause for input.

## Skills in Context

These skills are loaded above — reference them directly:
`policy-index`, `anti-slop`, `reviewing-llm-code`, `fixing-slop`, `test-guidelines`

All reference files from `reviewing-llm-code/references/` and `anti-slop/references/` are also
loaded — the full pattern catalogues, case studies, test patterns, text patterns, UX antipatterns,
bridge-burning red flags, and runtime control-flow red flags.

Baseline (from loaded skills):
- No fallback suggestions (every missing resource must fail loudly)
- No mock/fake/stub as proof (real data or nothing)
- No runtime defaults for critical dependencies
- No try-import or conditional stubs
- No backwards-compatibility shims — this is a pre-launch system
- No legacy flags, deprecated symbols, or feature-flag toggles
- Every assertion in a test must genuinely increase proof burden
- Every finding must cite file paths, line numbers, and exploration evidence
- **PEP 723 Mandate**: Any agent-authored or modified Python script that imports third-party packages MUST declare dependencies via PEP 723 inline script metadata. Reject any finding that suggests adding to `pyproject.toml` for standalone scripts.
- **Policy Cross-Referencing**: Before reporting any finding, you MUST cross-reference it against the loaded policy documents (e.g., `bridge-burning-red-flags.md`, `runtime-control-flow-red-flags.md`). If a finding contradicts explicit policy (like the Python `-O` mode rule), it MUST be dropped. Do not report findings based on general software engineering intuition if they violate the repository's bespoke software policies.
- **Ignore Python `-O` Mode**: We do NOT care about Python's optimized mode (`-O`) that strips `assert` statements. It is a trivial, esoteric concern. Do NOT report the use of `assert` as a problem. Findings mentioning `-O` or "optimized mode" will be rejected.

## Task: Full Repository Slop Audit

Perform a comprehensive, fresh analysis of the entire repository at the current commit (`{{REPO_SHA}}`) focused exclusively on **slop**.

**CRITICAL: Ignore all Pull Request context.** This is a repository-wide sweep, not a PR review. Analyze all files as if this were a day-zero audit.

"Slop" means structural AI-generated-code defects as defined by the loaded skills:
bridge-burning violations, validation-evasion constructs, runtime defaults, mocks/skips/fakes
in proof paths, proof-laundering, dead control flow, dependency-inversion failures,
bespoke reinvention of standard patterns, and myopic patching that hacks linters/tests
into compliance.

### Execution

1. Scan the entire repository to identify all Python and TypeScript source files.
2. For each file, examine the code for the slop categories defined in the loaded references.
3. Check these specific slop categories:
   - **Bridge-Burning Red Flags**: Runtime defaults, fallbacks, try-import, mock/fake as proof, backwards-compat shims, boolean mode flags, stringly errors, soft guards.
   - **Runtime Control-Flow Red Flags**: Conditional logic compensating for model code-writing failure.
   - **Test Pattern Violations**: Meta-assertions on source, helper-level proof laundered as boundary proof, smoke tests in proof paths, fake data.
   - **Text Pattern Violations**: Weasel words, hedged claims, presenting procedural completion as substantive.
   - **UX Antipatterns**: Silent failure, error swallowing, missing diagnostics.

### Finding Labeling

Each finding MUST carry one of these labels in the JSON `label` field:
- `SLOP` — Definite slop violation.
- `SLOP SUSPECT` — Likely slop but needs human judgment to confirm.
- `NOTE` — Minor concern, not clearly slop.

If any `SLOP` or `SLOP SUSPECT` findings exist, report them and skip `NOTE`.

### Output Format
The harness requires a strict JSON file format. Plain text reports will be rejected.
The JSON must conform to the following schema precisely:

```json
{
  "schema_version": 1,
  "report_type": "slop",
  "repo_sha": "{{REPO_SHA}}",
  "review_scope": {
    "changed_files": [],
    "excluded_files": [],
    "required_surfaces": []
  },
  "findings": [
    {
      "tier": "tier1",
      "label": "SLOP",
      "category": "bridge-burning",
      "location": {
        "path": "src/foo.ts",
        "start_line": 10,
        "end_line": 25,
        "quoted_text_sha256": "optional-sha"
      },
      "pattern": "mechanism, not symptom",
      "task_narrative": "What was the user actually asking for? What was the original scope of the task?",
      "slop_narrative": "How did the agent go from the original task to producing THIS artifact instead of fulfilling it? What substitutions happened?",
      "why_it_matters": "How this mechanism lets bad work pass, hides failures, or increases future agent damage.",
      "user_surprise": "How does this behavior minimize what agents care about (reducing errors) at the cost of what users care about (minimizing surprise and confusion)?",
      "existential_justification": "WHY does this code exist at all? What justified the agent writing it instead of using an existing solution?",
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
  "rejected_easy_wins": [],
  "score": 85,
  "report": "## Markdown Slop Audit Summary\n\nInclude the full formatted report here for human consumption."
}
```

- **No Remediation**: Slop review is an adversarial audit. You must diagnose the fraud and trace its causal path, not try to patch it. Do not include remediation steps.
- Meta/infrastructure findings about agent configs, tests, CI workflows, or harness files are strictly forbidden and will cause rejection.
- All locations must correspond to real files in the repository.

## Submitting Your Report

The ONLY way to submit your candidate report is to write the JSON to a file in the candidates directory: `{{CANDIDATES_DIR}}`.

1. Write your full JSON report to a file like `{{CANDIDATES_DIR}}/candidate.json`.
2. Do NOT try to write `.brooks-report-artifact.json` directly. The harness will validate your candidate and write the artifact itself if validation passes.
3. If the harness rejects your candidate, it will automatically restart you with a continuation prompt containing the exact validation errors.
