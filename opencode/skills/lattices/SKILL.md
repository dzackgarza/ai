---
name: lattices
description: Use when working with lattices, quadratic forms, or discrete subgroups of Euclidean space
---

# Lattices

## Overview

# Mathematical and Implementation Conventions

## Mathematical Conventions

### Bilinear Forms vs Inner Products

- **Bilinear Form**: An additive, linear map B: V × V → K.
- **Inner Product**: A positive-definite, symmetric bilinear form.
  - Symmetric: B(x, y) = B(y, x)
  - Positive definite: B(x, x) > 0 for all x ≠ 0
  - Non-degenerate: B(x, y) = 0 for all y ⇒ x = 0

**Do not confuse inner products (which require positive definiteness and symmetry) with more general bilinear forms. Use precise terminology:**

- "Bilinear form" for general case
- "Bilinear pairing" for anti-symmetric/skew forms
- "Quadratic form" specifically for norm-like quantities B(x, x)

**Examples of forms that are NOT inner products:**

- Indefinite forms (mixed signature)
- Skew-symmetric forms
- Degenerate forms
- Hermitian sesquilinear forms

### Gram vs Cartan Matrices

- **Gram Matrix (G):** G*{ij} = ⟨e_i, e_j⟩ for some basis {e_i}; symmetric; G*{ii} = -2 (our convention)
- **Cartan Matrix (A):** A*{ij} = 2⟨α_i, α_j⟩/⟨α_j, α_j⟩ for simple roots α_i; usually A*{ii} = 2, not symmetric in general
- **Relation:**
  - ADE types: A = -G
  - General types: Relation depends on root length ratios (BCFG, G₂ etc)

### Orthogonality Behavior

- **Symmetric forms:** Orthogonality is symmetric, complements are well-defined
- **Skew-symmetric forms:** Every element is orthogonal to itself, no norm
- **Non-symmetric forms:** Distinction between left/right orthogonality, complements may not exist

### Signature-Based Classification

- **Convention:** B*{ij} = 2 × cos(π/M*{ij}) (our Gram matrix)

- **Definiteness criteria (inverted from literature):**

| Group type | Standard literature         | Our convention              |
| ---------- | --------------------------- | --------------------------- |
| Finite     | Positive definite (λ > 0)   | Negative definite (λ < 0)   |
| Affine     | Positive semidefinite (λ=0) | Negative semidefinite (λ=0) |
| Hyperbolic | Indefinite (mixed signs)    | Indefinite (mixed signs)    |

- **Classification (mathematically):**
  - Elliptic/Finite: -G positive definite (i.e., B(v,v) < 0 for all nonzero v)
  - Parabolic/Affine: -G positive semidefinite with exactly one zero (i.e., B(v,v) ≤ 0)
  - Hyperbolic: -G indefinite, some B(v,v) positive, some negative

**Definiteness is defined by the signs and behavior of B(v,v), not by eigenvalue analysis. This applies even for infinite modules, or over rings (ℤ, etc.), where spectral concepts do not apply. Always use algebraic and form-based criteria for classification—never rely solely on eigenvalue counts or numerical spectra.**

### Exact Arithmetic Principles

- Work over ℤ, ℚ, or exact rings. Never use floating point or ε comparisons for mathematical criteria.
- Eigenvalues/algebraic invariants are symbolic except for final visualization.

### Field Extensions for Non-Crystallographic Types

- Crystallographic: ℤ, ℚ
- Non-crystallographic:
  - H₃: ℤ[φ] (φ² - φ - 1 = 0)
  - H₄: ℤ[τ] (τ = 2cos(π/5))
  - I₂(p): ℤ[2cos(π/p)]
- Always determine minimal field automatically; treat Galois orbits/invariants accordingly.

## Implementation Advice (SageMath/Software)

- Do not use "inner product" for general bilinear forms in code or API.
- Always define matrix/data structures mathematically—don't guess or hard-code!
- Use symbolic computation for Gram matrices, never list notation or hard-coded lists (e.g., ['A', 2] is discouraged; use LaTeX 'A_2').
- For indefinite forms, use `IntegralLattice` (not `IntegerLattice` or Sage's length routines).
- For lattices with symmetric bilinear forms, `inner_product`, norm-type quantities, and orthogonal complements are well-defined. Reserve the stronger warning for code that has widened to arbitrary bilinear forms or pairings.
- Avoid floating-point epsilon comparisons at any stage.

## Mathematical Pitfalls and Misconceptions

When reasoning about general bilinear forms on free ℤ-modules, distinguish that setting from lattices in the strict sense:

- Many familiar vector-space definitions and operations are only mathematically valid in special cases:
  - For lattices with symmetric bilinear forms, `orthogonal_complement` is well-defined. For a general bilinear form, orthogonality may fail to be symmetric, so left/right complements must be treated separately.
  - For lattices with symmetric bilinear forms, norm-style quantities from B(v,v) are well-defined. There is no geometric norm notion for a general bilinear form without symmetry or definiteness.
  - The `reflection` operation (across a subspace/module) only makes sense when the form is symmetric, as it depends on the geometric notion of orthogonality and norm.

**Critical mathematical error:** Extending lattice-specific constructions to arbitrary free ℤ-modules with bilinear forms can lead to incorrect mathematics. The warning is about general bilinear-form APIs, not about ordinary lattices equipped with symmetric bilinear forms.

## References

See these for further mathematical and implementation guidance:

- `/docs/api-planning/BILINEAR_FORMS_MATHEMATICAL_NOTES.md`
- `/docs/MATHEMATICAL_THEORY.md`
- `/docs/REQUIREMENTS.md`
- `/docs/api-planning/`

**Reminder:** Mathematical definitions are primary. Implement algorithms based on mathematical structure (e.g. definiteness), not just eigenvalue counting.
