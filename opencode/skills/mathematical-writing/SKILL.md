---
name: dzack-mathematical-writing
description: Use when producing mathematical content, proofs, problem solutions, LaTeX documents, or formalization targets. Triggers on any mathematical notation, proof structure, typesetting, or verification code.
---
# Dzack Mathematical Writing

Override default mathematical conventions with dzack's specific style.
All mathematical output must follow the conventions in `references/`.

## Core Policy

- **Never use "clearly" or "obviously" without explicit reasoning.** Every step must be
  mathematically justified.
- **One operation per numbered step.** Each step contains exactly one mathematical
  operation or deduction.
- **Inline justifications required.** End each non-definition step with `[By <reason>]`
  in square brackets.
- **Explicit quantifiers and types.** Never leave variables unbound.
  Use `∀x ∈ X` or `∃x ∈ X`. Declare types: "Let n ∈ NN."
- **NN excludes 0.** In this convention system, `NN` = {1, 2, 3, ...}. When 0 is needed,
  use `ZZ_{≥0}`.
- **Match Lean naming conventions.** `monoid` → `Monoid`, `is_subgroup` → `IsSubgroup`,
  `ring_hom` → `RingHom`.
- **Include verification code where appropriate.** SageMath or Lean 4 assertions
  alongside proofs for computable claims.
- **Use standard theorem formatting.** Italic environment names, no numbering:
  `*Theorem.* [Statement]`.

## Decision Procedures

### When to include verification code

- **Always** for claims about finite or computable objects (ideal membership, parity,
  small induction bases).
- **Optional** for abstract existential results where computation is illustrative.
- **Never** as a substitute for a proof — verification complements deduction.

### When to provide Lean 4 formalization

- When the user explicitly asks for formalization.
- When writing content intended for Lean migration.
- When the proof structure is standard (induction, contradiction, existence).
- Always match informal proof structure line-for-line where possible.

### Inline vs display math

- Use `$...$` for single symbols, short expressions, references within prose.
- Use `$$...$$` for multi-step derivations, important equations, anything requiring
  alignment.
- Number important equations with `\tag{n}`.

## Environment Traps

- **Unbound variables in proofs:** Writing "x + y = y + x" without ∀ quantifier.
  Fix: prepend "∀x, y ∈ G:".
- **Missing justifications:** A step with no `[By ...]` annotation.
  Fix: add justification for every non-trivial step.
- **NN including 0:** Agent default often treats `ℕ` as including 0. In this convention,
  `NN` excludes 0. Fix: check context and use `ZZ_{≥0}` when 0 is needed.
- **Inconsistent function notation:** Switching between f(x) and fx mid-document.
  Fix: pick one convention from `references/notation-and-symbols.md` and stick to it.
- **Non-exhaustive case analysis:** Stopping after the easy case.
  Fix: enumerate all cases explicitly.
- **Verification code without assertions:** Computing but never asserting.
  Fix: every verification block must end with an `assert` or explicit check.

## Required Outputs

### Problem statement

```markdown
### Problem N
Clear statement with all given information and constraints.
```

### Solution

```markdown
### Solution
1. **Setup**: Restate problem, define variables with types, state method.
2. **Step-by-step development**: Numbered steps, one operation each, inline justifications.
3. **Verification**: (when applicable) Show solution satisfies conditions.
```

### Proof

```markdown
*Theorem.* Statement.

*Proof.*
1. Let [variable] ∈ [type].
2. ⇒ [deduction] [Justification]
3. ...
```

### Formalization (when requested)

Provide both mathematical prose and corresponding Lean 4 code.
Match structure line-for-line.
See `references/formalization-patterns.md` for paired examples.

## Validation Checklist

- [ ] All variables bound with explicit quantifiers or type declarations
- [ ] Every non-trivial step has inline justification in square brackets
- [ ] Assumptions marked with `[Assume ...]` and discharged explicitly
- [ ] Case analysis is exhaustive and numbered
- [ ] Notation is consistent throughout the document
- [ ] Important equations use display math with proper alignment
- [ ] Verification code (if present) includes assertions
- [ ] No "clearly" or "obviously" without explicit reasoning
- [ ] No skipped algebraic steps in derivations
- [ ] Standard names match target formal library conventions

## Anti-Patterns

| Pattern | Why Bad | Do Instead |
| --- | --- | --- |
| "Clearly, ..." or "Obviously, ..." | Hides reasoning; often wrong | State explicit justification or lemma |
| Unbound variables | Ambiguous scope; formalization fails | Add ∀ or ∃ quantifier, or type declaration |
| Multi-operation steps | Hard to verify; hard to formalize | Split into one operation per numbered step |
| Missing justifications | Reader must guess reasoning | End each step with `[By ...]` |
| Text inside math mode | Typesetting errors; semantic confusion | Use `\text{...}` or move text outside `$...$` |
| Verification without assertions | Silent failure possible | Always assert expected result |
| Inconsistent function notation | Confusion; formalization mismatch | Pick one convention and stick to it |
| Skipping base case in induction | Invalid proof | Always verify base case separately |
| Non-exhaustive cases | Missing paths; potential counterexample | List all cases explicitly |
| Using informal set builder notation in formalization | Lean/mathlib mismatch | Use explicit class/instance definitions |

## References

- `references/notation-and-symbols.md` — Number systems, function notation, algebraic
  structures, quantifier conventions, delimiter macros
- `references/proof-structure.md` — Proof environment formatting, variable tracking,
  justification style, case analysis, common pitfalls
- `references/formalization-patterns.md` — Lean 4 and SageMath templates for induction,
  contradiction, existence, definitions, theorems
- `references/exposition-style.md` — Pedagogical writing style, problem presentation,
  solution structure
- `references/typesetting-conventions.md` — LaTeX environments, alignment,
  cross-references, YAML headers, tables, figures

## Cross-References

- **lean4** — For editing .lean files, debugging builds, searching mathlib
- **lattices** — For lattice-specific notation and conventions
- **sagemath** — For SageMath computations and verification
- **theorem-proving-and-counterexamples** — For broader formalization strategies
- **mathematical-testing** — For writing failing test suites before implementation
