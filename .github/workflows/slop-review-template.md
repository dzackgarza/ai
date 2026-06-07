## CI Constraints (MANDATORY)

This runs in a CI environment. Follow these rules exactly:
- **Do NOT output the report to stdout.** The recipe is the only submission path.
- Do not ask questions. Do not request confirmation. Do not pause for input.
- Run `just -f .agents/justfile` to discover available recipes — do not guess paths.

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

Each finding MUST carry one of these labels:

- `[SLOP]` — Definite slop violation (one of the 5 categories above). Must cite the
  specific reference pattern and file:line.
- `[SLOP SUSPECT]` — Likely slop but needs human judgment to confirm.
- `[NOTE]` — Minor concern, not clearly slop.

### Priority rule

If any `[SLOP]` or `[SLOP SUSPECT]` findings exist, report them and skip `[NOTE]`.
Only report `[NOTE]` findings when the diff has zero definite or suspected slop.

### Output Format

```
## Slop Review — {{DIFF_SHA}}

**Scope**: Diff analysis ({{DIFF_FILES}} files changed)

### Findings

- [LABEL] `file/path.py:NN` — description of the slop pattern, which reference catalog
  defines it (e.g. "Bridge-burning red flag R3: runtime default for X"), and what the
  correct replacement should look like.

### Health Score: NN/100

Score reflects slop density: 100 = zero slop.
Subtract 10 per `[SLOP]` finding, 5 per `[SLOP SUSPECT]`.

### Summary

X findings total: Y definite slop, Z suspects, W notes (if any).
```

## Submitting Your Report

The ONLY way to submit a report is through the validation recipe:

1. Write your report and score to a **temporary JSON file** (e.g. `/tmp/slop-report.json`):
   ```json
   {"report": "<full report text with all findings>", "score": <0-100>}
   ```

2. Run the recipe:
   ```
   just -f .agents/justfile post-brooks-review /tmp/slop-report.json {{PR_NUMBER}}
   ```

3. If the recipe **fails** (exit non-zero): read the validation errors, fix the report, and retry.

4. If the recipe **succeeds**: it creates `.brooks-report-artifact.json` with the validated report.

Do NOT write to `.brooks-report-artifact.json` directly — only the recipe can create it.
Do NOT output the report to stdout — the recipe is the only submission path.

