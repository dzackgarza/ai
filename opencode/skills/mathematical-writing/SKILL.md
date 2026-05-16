---
name: mathematical-writing
description: Use when producing any mathematical content, notation, proofs, problem solutions, or LaTeX-formatted documents. Covers standard number system notation, proof step structure, explicit quantifiers, formalization patterns for Lean 4 and SageMath, pedagogical exposition style, and Markdown/LaTeX typesetting conventions.
---
# Mathematical Writing

Behavioral policy for all mathematical content: proofs, solutions, definitions, problem
sets, and formalization targets.

* * *

## Core Policy

- **Precision over brevity.** Every step must be mathematically justified.
  Never use "clearly" or "obviously" without explicit reasoning.
- **Never leave variables unbound.** Use explicit quantifiers: ∀x ∈ X or ∃x ∈ X.
- **Annotate types and domains.** Include domain/codomain: f: X → Y. Declare variable
  types when introduced: "Let n ∈ NN."
- **One operation per numbered step.** Each atomic step contains exactly one
  mathematical operation or deduction.
- **Inline justifications.** End each non-definition step with a brief justification in
  square brackets: [By ...].
- **Mark and discharge assumptions explicitly.** Use [Assume ...] and note when
  discharged.
- **Use standard names matching formal libraries.** E.g., monoid → Monoid, is_subgroup →
  IsSubgroup, ring_hom → RingHom.
  See [references/notation-and-symbols.md](references/notation-and-symbols.md) for full
  symbol table.
- **Number cases explicitly.** Ensure exhaustive case analysis with clear discharge.
- **Include verification code where appropriate.** SageMath or Lean 4 code blocks
  alongside proofs. See
  [references/formalization-patterns.md](references/formalization-patterns.md) for
  templates.

* * *

## Decision Procedures

### Inline math ($...$) vs display math ($$...$$)

- Use inline for single symbols, short expressions, and references within prose.
- Use display for multi-step derivations, important equations, and anything requiring
  alignment.
- Number important equations with \tag{n}.

### When to include verification code

- **Always** for claims about finite or computable objects (ideal membership, parity,
  small induction bases).
- **Optional** for abstract existential results where computation is illustrative.
- **Never** as a substitute for a proof — verification complements, does not replace,
  deduction.

### When to provide Lean 4 formalization

- When the user explicitly asks for formalization.
- When writing content intended for Lean migration.
- When the proof structure is standard (induction, contradiction, existence) and a Lean
  template exists in
  [references/formalization-patterns.md](references/formalization-patterns.md).

### Proof technique selection

| Goal structure | Default technique | See |
| --- | --- | --- |
| ∀n ∈ NN: P(n) | Induction | [references/formalization-patterns.md](references/formalization-patterns.md) |
| ¬∃x: P(x) | Contradiction | [references/formalization-patterns.md](references/formalization-patterns.md) |
| ∃x: P(x) | Constructive witness or bijection | [references/formalization-patterns.md](references/formalization-patterns.md) |
| H ≤ G, [G:H]=2 ⇒ H ⊲ G | Case analysis on cosets | [references/formalization-patterns.md](references/formalization-patterns.md) |
| Finite domain → field | Injectivity + finiteness → surjectivity | [references/notation-and-symbols.md](references/notation-and-symbols.md) |

* * *

## Environment Traps

- **Unbound variables in proofs:** Writing "x + y = y + x" without ∀ quantifier.
  Fix: prepend "∀x, y ∈ G:".
- **Missing justifications:** A step with no [By ...] annotation.
  Fix: add justification for every non-trivial step.
- **Mixing text and math modes without spacing:** Text inside math mode or math
  operators outside math mode.
  Fix: use proper \, spacing; keep operators in $...$.
- **Inconsistent notation:** Switching between f(x) and fx for function application
  mid-document. Fix: pick one convention from
  [references/notation-and-symbols.md](references/notation-and-symbols.md) and stick to
  it.
- **Forgetting type declarations:** "Let a be an element..." Fix: "Let a ∈ R" or "Let a:
  R".
- **Non-exhaustive case analysis:** Stopping after the easy case.
  Fix: enumerate all cases explicitly and verify exhaustiveness.
- **Verification code without assertions:** SageMath code that computes but never
  asserts the expected result.
  Fix: every verification block must end with an assertion or explicit check.

* * *

## Required Outputs

### Problem statement format

```markdown
### Problem N
Clear statement with all given information and constraints.
```

### Solution format

```markdown
### Solution
1. **Setup**: Restate problem, define variables with types, state method.
2. **Step-by-step development**: Numbered steps, one operation each, inline justifications.
3. **Verification**: (when applicable) Show solution satisfies conditions.
```

### Proof format

```markdown
*Theorem.* Statement.

*Proof.*
1. Let [variable] ∈ [type].
2. ⇒ [deduction] [Justification]
3. ...
```

### Formalization format (when requested)

Provide both the mathematical prose and the corresponding Lean 4 code.
Match structure line-for-line where possible.
See [references/formalization-patterns.md](references/formalization-patterns.md) for
paired examples.

* * *

## Validation Checklist

Before finishing any mathematical content:

- [ ] All variables bound with explicit quantifiers or type declarations
- [ ] Every non-trivial step has an inline justification in square brackets
- [ ] Assumptions marked with [Assume ...] and discharged explicitly
- [ ] Case analysis is exhaustive and numbered
- [ ] Notation is consistent throughout the document
- [ ] Important equations use display math with proper alignment
- [ ] Verification code (if present) includes assertions
- [ ] No "clearly" or "obviously" without explicit reasoning
- [ ] No skipped algebraic steps in derivations
- [ ] Standard names match target formal library conventions (Lean mathlib, SageMath)

* * *

## Anti-Patterns

| Pattern | Why Bad | Do Instead |
| --- | --- | --- |
| "Clearly, ..." or "Obviously, ..." | Hides reasoning; often wrong | State the explicit justification or lemma used |
| Unbound variables | Ambiguous scope; formalization fails | Add ∀ or ∃ quantifier, or type declaration |
| Multi-operation steps | Hard to verify; hard to formalize | Split into one operation per numbered step |
| Missing justifications | Reader must guess reasoning | End each step with [By ...] |
| Text inside math mode | Typesetting errors; semantic confusion | Use \text{...} or move text outside $...$ |
| Verification without assertions | Silent failure possible | Always assert expected result |
| Inconsistent function notation | Confusion; formalization mismatch | Pick one: f(x) or fx, stick to it |
| Skipping base case in induction | Invalid proof | Always verify base case separately |
| Non-exhaustive cases | Missing paths; potential counterexample | List all cases explicitly |
| Using informal set builder notation in formalization | Lean/mathlib mismatch | Use explicit class/instance definitions |

* * *

## Cross-References

- **lean4** — For editing .lean files, debugging builds, searching mathlib
- **lattices** — For lattice-specific notation and conventions
- **sagemath** — For SageMath computations and verification
- **theorem-proving-and-counterexamples** — For broader formalization strategies
- **mathematical-testing** — For writing failing test suites before implementation

* * *

## References

All detailed source material is in `references/`:

- [references/notation-and-symbols.md](references/notation-and-symbols.md) — Standard
  number systems, function notation, algebraic structure conventions
- [references/proof-structure.md](references/proof-structure.md) — Proof environment
  formatting, variable tracking, justification style, case analysis
- [references/formalization-patterns.md](references/formalization-patterns.md) —
  Induction, contradiction, existence templates with Lean 4 and SageMath code pairs
- [references/exposition-style.md](references/exposition-style.md) — Pedagogical writing
  style, problem presentation, solution structure, proof techniques
- [references/typesetting-conventions.md](references/typesetting-conventions.md) — LaTeX
  environments, alignment, cross-references, YAML headers, tables, figures
