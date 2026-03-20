---
name: aristotle
description: Use when formalizing mathematics, filling sorry placeholders in Lean projects, or proving theorems with automated theorem proving. Use for research-level math verification and formalization tasks.
---

# Aristotle: Automated Theorem Proving

Aristotle formalizes and proves graduate/research-level mathematics using Lean 4.

## When to Use

- Fill `sorry` placeholders in Lean projects
- Formalize natural language mathematics (papers, textbooks, notes)
- Prove theorems from plain English descriptions
- Find counterexamples to false statements

## Core Workflow

### 1. Submit a Project

```bash
# Simple prompt
uvx --from aristotlelib@latest aristotle submit "Prove sqrt(2) is irrational" --wait

# With project directory (for sorry-filling or context)
uvx --from aristotlelib@latest aristotle submit "Fill in the sorries" \
  --project-dir ./my-lean-project --wait --destination output.tar.gz
```

### 2. Check Status

```bash
uvx --from aristotlelib@latest aristotle list
uvx --from aristotlelib@latest aristotle list --status IN_PROGRESS COMPLETE
```

### 3. Download Results

```bash
uvx --from aristotlelib@latest aristotle result <project-id> --destination output.tar.gz
```

## Project Requirements

Lean projects must include:

- `lakefile.toml` (or `lakefile.lean`)
- `lean-toolchain` file
- Proper import structure

Aristotle automatically skips build artifacts (`.olean`, `.lake/packages/`).

## Guiding Proofs

Include natural language hints in header comments, tagged with `PROVIDED SOLUTION`:

```lean
/-- Show that cos(sqrt(x^2 + y^2)) ≤ cos x * cos y.
PROVIDED SOLUTION
Set r := sqrt(x^2 + y^2). If r > π/2, inequality holds trivially.
Otherwise write x = r cos φ, y = r sin φ and analyze F(φ)...
-/
theorem my_theorem (x y : ℝ) ... := by sorry
```

**Critical:** Aristotle does not see comments inside proof blocks (`by ...`). Only header comments work.

## Handling Results

### Success

- `sorry` placeholders filled with verified proofs
- Original file structure preserved

### False Statements

- Aristotle provides a proof of the negation
- Custom `negate_state` tactic included in file header

### Out of Budget

- Download partial results: `aristotle result <id> --destination partial.tar.gz`
- Resume by submitting partial output as new project

## Common Traps

1. **Comments inside proofs ignored** — Hints must be in header comments (`/-- ... -/`), not inside `by ...` blocks
2. **Missing lakefile** — Projects without `lakefile.toml` will fail to parse
3. **Assuming context files modified** — Aristotle does not modify definitions in context files, only fills sorries

## Decision Procedures

### When to use `--wait` vs polling

- Use `--wait` for immediate feedback on small projects
- Skip `--wait` and poll with `aristotle list` for long-running proofs

### When to provide context

- Always provide project directory for sorry-filling
- Provide papers/notes as context for formalization tasks
- Can work from prompt alone for well-known results

### Counterexample handling

- When Aristotle proves negation, review the `negate_state` proof
- Check for logical errors, edge cases, or misformalizations

## Validation Checklist

- [ ] Lean project has `lakefile.toml` and `lean-toolchain`
- [ ] Provided hints are in header comments, not proof blocks
- [ ] `--wait` used appropriately for project size
- [ ] Results extracted and reviewed before further work
- [ ] Partial results saved if out-of-budget

## Quick Commands

```bash
# Submit and wait
aristotle submit "prompt" --wait

# Submit with directory
aristotle submit "prompt" --project-dir ./dir --wait

# Formalize a document
aristotle formalize paper.tex --wait

# List recent projects
aristotle list --limit 20

# Get result
aristotle result <id> --destination out.tar.gz

# Cancel
aristotle cancel <id>
```
