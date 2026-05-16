# Notation and Symbols

Standard notation for mathematical objects, functions, and algebraic structures.

## Number Systems

| Notation | Meaning | Formalization |
| --- | --- | --- |
| ZZ | Integers | `ℤ` in Lean, `ZZ` in SageMath |
| QQ | Rationals | `ℚ` in Lean, `QQ` in SageMath |
| RR | Reals | `ℝ` in Lean, `RR` in SageMath |
| CC | Complex numbers | `ℂ` in Lean, `CC` in SageMath |
| NN | Positive integers {1, 2, 3, ...} | `ℕ` in Lean (note: Lean `ℕ` includes 0) |
| ZZ_{≥0} | Non-negative integers {0, 1, 2, ...} | `ℕ` in Lean |
| 2ZZ | Even integers {..., -4, -2, 0, 2, 4, ...} | `2 * ℤ` |
| 2ZZ + 1 | Odd integers {..., -3, -1, 1, 3, ...} | `2 * ℤ + 1` |
| PP | Prime numbers | `Nat.Primes` in Lean |

**Note on NN:** In this notation system, NN excludes 0. When 0 is needed, use ZZ_{≥0} or
specify explicitly. Lean's `ℕ` includes 0 — adjust statements accordingly when
formalizing.

## Function Notation

### Definition Syntax

- **Map declaration:** f: X → Y, x ↦ x²
- **Element declaration:** f ∈ Hom_Ring(R, S) for ring homomorphisms
- **General morphism:** f ∈ Hom_Category(A, B)

### Piecewise Definitions

```
sgn(x) := { 1  if x > 0
            0  if x = 0
           -1  if x < 0 }
```

In LaTeX:
```latex
\mathrm{sgn}(x) \coloneqq \begin{cases}
  1 & \text{if } x > 0 \\
  0 & \text{if } x = 0 \\
  -1 & \text{if } x < 0
\end{cases}
```

## Algebraic Structures

Always be explicit about operations:

- **Ring:** (ZZ/6ZZ, +, ×) — never write just ZZ/6ZZ when the ring structure matters
- **Group:** (G, ·, e) or (G, +, 0) — specify operation and identity
- **Field:** (F, +, ×, 0, 1) — all operations and distinguished elements
- **Module:** M as an R-module — specify the scalar ring

## Subsets and Operations

| Notation | Meaning |
| --- | --- |
| H ⊆ G | H is a subset of G |
| H ≤ G | H is a subgroup of G |
| H ⊲ G | H is a normal subgroup of G |
| [G : H] | Index of H in G |
| G / H | Quotient group (when H ⊲ G) |
| gH | Left coset |
| Hg | Right coset |

## Type Annotations in Definitions

When defining functions, always include domain and codomain:

- **Correct:** f: RR → RR, x ↦ x²
- **Correct:** φ: G → G, g ↦ a·g (for fixed a ∈ G)
- **Incorrect:** Let f(x) = x² (unless domain/codomain are clear from context)

## Quantifier Conventions

- **Universal:** ∀x ∈ X: P(x) or ∀x ∈ X, P(x)
- **Existential:** ∃x ∈ X such that P(x)
- **Unique existence:** ∃!x ∈ X: P(x)

Always include the type/set membership in the quantifier.
Never write bare quantifiers like "∀x" without specifying where x lives.

## Common Abbreviations

| Abbreviation | Expanded Meaning |
| --- | --- |
| wlog | without loss of generality |
| w.r.t. | with respect to |
| s.t. | such that |
| resp. | respectively |
| iff | if and only if |
| RHS / LHS | right-hand side / left-hand side |

## Delimiter Macros

Use these LaTeX macros for consistent delimiter sizing:

| Macro | Output | Use For |
| --- | --- | --- |
| `\qty{x+y}` | (x+y) | Parentheses |
| `\bqty{a,b}` | [a,b] | Square brackets |
| `\Bqty{1,2,3}` | {1,2,3} | Curly braces (sets) |
| `\abs{x}` |  | x |
| `\eval{f(x)}_{x=a}^b` | f(x)\|_{x=a}^b | Evaluation bar |

Note: These are custom macros.
Include them in document YAML headers or preamble.
See [typesetting-conventions.md](typesetting-conventions.md) for YAML header template.
