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

### Labeling
**Label each finding** as `[PR BLOCKER]`, `[SHOULD FILE ISSUE]`, or `[NOTE]`.

Evidence requirements:
- Every finding must cite specific file paths and line numbers
- Every finding must state which exploration command surfaced it
- Generic config-drift findings without file-level evidence will be rejected

### Diff
```diff
{{DIFF}}
```

### Output Format
Produce findings as Symptom→Source→Consequence→Remedy with a Health Score (0-100) for the diff changes and separately for the full repo.
