## CI Constraints (MANDATORY)

This runs in a CI environment. Follow these rules exactly:
- **Write ALL findings to stdout.** Do not write any files.
- Do not reference files you wrote — they do not persist after the job.
- Do not ask questions. Do not request confirmation. Do not pause for input.
- Output the complete report as text to stdout. Every finding, every score, every recommendation.

## Mandatory Skill Loading

Before any analysis, use the `skill()` tool to load these skills IN ORDER.
If a skill fails to load, do not continue — report the failure.

1. `policy-index` — policy routing: determines which rule owns each finding
2. `bespoke-software-policy` — bespoke-software rules: filters out portability, compatibility, enterprise, and meta findings
3. `anti-slop` — structural technical debt detection: runtime defaults, fallbacks, mocks, fakes, stubs, proof-laundering, deletion-laundering, bridge-burning violations
4. `reviewing-llm-code` — LLM-produced code review patterns: validation-evasion constructs, dead control flow, myopic patching
5. `test-guidelines` — proof obligations: banned assertion shapes, helper-level proof, smoke/proof boundary rules
6. `reviewing-llm-code/references/bridge-burning-red-flags.md` — red-flag inventory for bridge-burning policy violations

After loading all six, you have this baseline:
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
