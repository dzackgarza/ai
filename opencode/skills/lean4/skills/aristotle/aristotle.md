---
name: aristotle
description: Use when formalizing mathematics, filling sorry placeholders in Lean projects, or proving theorems with automated theorem proving. Use for research-level math verification and formalization tasks.
---
# Aristotle: Automated Theorem Proving

Aristotle formalizes and proves graduate/research-level mathematics using [[lean4/skills/lean4/lean4|Lean 4]].

## When to Use

- Fill `sorry` placeholders in Lean projects

- Formalize natural language mathematics (papers, textbooks, notes)

- Prove theorems from plain English descriptions

- Find counterexamples to false statements

## Prompt Style

Express prompts in natural language. Describe the formalization goal plainly and let the model leverage its own training to decide how to achieve it — which tactics to use, how to structure the proof, and which Lean constructs fit.

Do **not** pre-specify Lean constructs, tactic sequences, or proof structure in the prompt unless the model is clearly stuck after a failed attempt. Over-constraining the prompt with implementation detail competes with the model's own judgment and typically produces worse results than a clear plain-English description of the mathematical goal.

Only introduce further constraints — specific Lean constructs, tactic hints, intermediate lemmas — as a fallback when the model has demonstrably failed on the natural-language version.

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
uvx --from aristotlelib@latest aristotle download <project-id>
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

**Critical:** Aristotle does not see comments inside proof blocks (`by ...`). Only
header comments work.

## Handling Results

### Success

- `sorry` placeholders filled with verified proofs

- Original file structure preserved

### False Statements

- Aristotle provides a proof of the negation

- Custom `negate_state` tactic included in file header

### Out of Budget

- Download partial results: `aristotle download <id>`

- Resume with `aristotle continue <id> "<instruction>"` (a new run spends credits)

## Common Traps

00. **Aristotle refuses Lean (since at least 2026-11-21).** With `aristotlelib` 3.4.0, a Lean
    project run ends COMPLETE with "Lean formalization projects aren't supported right now ...
    Lean support will return in the coming months". A prompt-only run ends with "No Verilog, C or
    Rust source files were uploaded". Neither spends credits. Read the run's
    `ARISTOTLE_SUMMARY.md` (or `output_summary` in `aristotle show ID --json`) before you trust
    a COMPLETE status: COMPLETE does not mean that a proof came back.

0. **An old client gets HTTP 404** — `aristotlelib` 1.x calls a project endpoint that the
   server no longer serves. Use 3.4.0 or later (`uv tool upgrade aristotlelib`). Free
   credits allow one active project per organization.


1. **Comments inside proofs ignored** — Hints must be in header comments (`/-- ... -/`),
   not inside `by ...` blocks

2. **Missing lakefile** — Projects without `lakefile.toml` will fail to parse

3. **Assuming context files modified** — Aristotle does not modify definitions in
   context files, only fills sorries

## Decision Procedures

### Waiting on a run

A run takes hours. Do not hold a turn on `--wait` and do not poll with `sleep`. Submit without
`--wait`, then start `aristotle show ID --non-interactive --json --destination FILE` as a
background command. It exits when the run ends and saves the result archive, and in an agent
harness its exit wakes the session. `aristotle list` shows which projects still run. A run cut
off OUT_OF_BUDGET keeps its partial result: `aristotle download ID`; `aristotle continue ID
Continue` resumes it once credits exist.

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

# List recent projects
aristotle list --limit 20

# Get result
aristotle download <id>

# Credit balance
aristotle balance

# Cancel
aristotle cancel <id>
```
