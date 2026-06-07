## Task

You have two jobs — do BOTH:

### 1. PR Review
Review the diff below. Produce Symptom→Source→Consequence→Remedy findings for anything wrong in the changed code.

### 2. Full Codebase Sweep
Independently scan the entire repository for issues: dead code, missing tests, security risks, architectural problems, tech debt, config drift. Produce Symptom→Source→Consequence→Remedy findings for each issue found.

### Labeling
**Label each finding** as `[PR BLOCKER]`, `[SHOULD FILE ISSUE]`, or `[NOTE]`.

### Diff
```diff
{{DIFF}}
```

### Output Format
Produce findings as Symptom→Source→Consequence→Remedy with a Health Score (0-100) for the diff changes and separately for the full repo.
