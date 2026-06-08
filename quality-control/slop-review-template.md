## CI Constraints (MANDATORY)

This runs in a CI environment. Follow these rules exactly:
- **Do NOT modify any workflow files or CI infrastructure.** You are running in a restricted mode.
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

## Task

You have ONE job — run a **slop-focused audit** on the PR diff below.

"Slop" means structural AI-generated-code defects as defined by the loaded skills:
bridge-burning violations, validation-evasion constructs, runtime defaults, mocks/skips/fakes
in proof paths, proof-laundering, dead control flow, dependency-inversion failures,
bespoke reinvention of standard patterns, and myopic patching that hacks linters/tests
into compliance.

### Scope: Diff-Impacted Code

Scan the diff below. For each file the diff touches, examine not just the changed lines
but also the **surrounding context** — the functions, classes, and test files affected.

Check these specific slop categories (from loaded references):

1. **Bridge-Burning Red Flags** (from `reviewing-llm-code/references/bridge-burning-red-flags.md`):
   Runtime defaults, fallbacks for missing dependencies, try-import patterns, mock/fake/skip
   as proof, backwards-compatibility shims, boolean mode flags, stringly errors, soft guards
   where hard assertions belong, and similar.

2. **Runtime Control-Flow Red Flags** (from `reviewing-llm-code/references/runtime-control-flow-red-flags.md`):
   Conditional logic that compensates for an AI model's inability to construct correct imports,
   function calls, or data shapes at code-writing time.

3. **Test Pattern Violations** (from `anti-slop/references/test-patterns.md`):
   Meta-assertions on source content, helper-level proof laundered as boundary proof,
   smoke tests in proof paths, fake/idealized data instead of real data.

4. **Text Pattern Violations** (from `anti-slop/references/text-patterns.md`):
   Weasel words, hedged claims, confusion between absence-of-evidence and
   evidence-of-absence, burying the lede, or presenting procedural completion as
   substantive completion.

5. **UX Antipatterns** (from `anti-slop/references/ux-antipatterns.md`):
   Silent failure modes, error swallowing, missing diagnostics, assumed user knowledge.

### Diff

```diff
{{DIFF}}
```

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
      "label": "SLOP",
      "category": "bridge-burning",
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

- Meta/infrastructure findings about agent configs, tests, CI workflows, or harness files are strictly forbidden and will cause rejection.
- All locations must correspond to real files in the repository.

## Submitting Your Report

The ONLY way to submit your candidate report is to write the JSON to a file in the candidates directory: `{{CANDIDATES_DIR}}`.

1. Write your full JSON report to `{{CANDIDATES_DIR}}/attempt-0.json`.
2. Do NOT try to write `.brooks-report-artifact.json` directly. The harness will validate your candidate and write the artifact itself if validation passes.
3. If the harness rejects your candidate, it will automatically restart you with a continuation prompt containing the exact validation errors.