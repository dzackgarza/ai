# Notation and Symbols

Dzack-specific conventions that differ from common defaults.

## Number Systems

| Notation | Meaning | Note |
| --- | --- | --- |
| `NN` | Positive integers {1, 2, 3, ...} | **Excludes 0.** Lean's `ℕ` includes 0 — adjust statements when formalizing |
| `ZZ_{≥0}` | Non-negative integers {0, 1, 2, ...} | Use when 0 is needed |
| `2ZZ` | Even integers | `{..., -4, -2, 0, 2, 4, ...}` |
| `2ZZ + 1` | Odd integers | `{..., -3, -1, 1, 3, ...}` |
| `PP` | Prime numbers | `{2, 3, 5, 7, 11, ...}` |

## Explicit Operations

Always be explicit about operations when the structure matters:

- **Ring:** `(ZZ/6ZZ, +, ×)` — never write just `ZZ/6ZZ`
- **Group:** `(G, ·, e)` or `(G, +, 0)` — specify operation and identity
- **Field:** `(F, +, ×, 0, 1)` — all operations and distinguished elements

## Delimiter Macros

Use these custom LaTeX macros for consistent delimiter sizing:

| Macro | Output | Use For |
| --- | --- | --- |
| `\qty{x+y}` | (x+y) | Parentheses |
| `\bqty{a,b}` | [a,b] | Square brackets |
| `\Bqty{1,2,3}` | {1,2,3} | Curly braces (sets) |
| `\abs{x}` | \|x\| | Absolute value |
| `\eval{f(x)}_{x=a}^b` | f(x)\|_{x=a}^b | Evaluation bar |

**Include in YAML header or preamble.** See `typesetting-conventions.md` for YAML
template with all macros pre-defined.

## Function Notation Conventions

### Arrow Syntax

Always use explicit arrow notation for function definitions:

- **Correct:** `f: X → Y, x ↦ x²`
- **Incorrect:** `Let f(x) = x²` (unless domain/codomain are clear from context)

### Type Annotations

When defining functions, always include domain and codomain:

- **Correct:** `f: RR → RR, x ↦ x²`
- **Correct:** `φ: G → G, g ↦ a·g` (for fixed `a ∈ G`)
- **Incorrect:** `Let f(x) = x²` (unless domain/codomain are clear from context)

### Hom Notation

For structure-preserving maps, use `Hom` notation:

- **Example:** `f ∈ Hom_Ring(R, S)` for ring homomorphisms
- **General:** `f ∈ Hom_C(X, Y)` for morphisms in category `C`

### Piecewise Functions

Use explicit piecewise definitions with cases:

```markdown
$$\mathrm{sgn}(x) \coloneqq \begin{cases}
1 & \text{if } x > 0 \\
0 & \text{if } x = 0 \\
-1 & \text{if } x < 0
\end{cases}$$
```

## Abbreviations

| Abbreviation | Expanded Meaning |
| --- | --- |
| wlog | without loss of generality |
| w.r.t. | with respect to |
| s.t. | such that |
| resp. | respectively |
| iff | if and only if |
| RHS / LHS | right-hand side / left-hand side |
