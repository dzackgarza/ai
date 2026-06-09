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

### No Remediation

Slop review is an adversarial audit. Diagnose the fraud and trace its causal path, not patch it. Do not include remediation steps.

### Output Format

Write a JSON report to `.agents/review-runner/candidates/submitted.json`.

To get the exact schema (fields, types, constraints), run:
`quality-control/ci/submit-candidate --help`

Key rules every finding must satisfy:

- `violated_invariant`: The named contract, behavior, or invariant that was violated. A slop finding's violated invariant names a required behavior that is provably impossible, silently swallowed, replaced by a fake, or non-deterministic.
- `proof_command`: The exact command, grep pattern, or code path that proves the violation exists. Not a file path — the actual command output or code flow that demonstrates the failure.
- All seven slop-specific narrative fields (`pattern`, `task_narrative`, `slop_narrative`, `why_it_matters`, `user_surprise`, `existential_justification`, `failure_mode`).
- `evidence`: At least one entry with `kind`, `path`, and `lines`.

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
