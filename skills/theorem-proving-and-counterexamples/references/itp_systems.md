# Interactive Theorem Proving (ITP)

Interactive Theorem Proving (ITP) systems allow for the formalization of modern mathematics, covering full mathematical complexity (analysis, topology, homological algebra, etc.).

## Lean 4 & Mathlib

Lean 4 is currently the leading system for formalizing contemporary mathematics, supported by **Mathlib**, which contains over 170k+ formal theorems.

- **Strengths**: Extensive library (algebra, analysis, topology, measure theory, number theory).
- **Recent Highlights**:
  - **Polynomial Freiman-Ruzsa (PFR) Conjecture**: Formalized by Tao et al. (2023-24).
  - **Liquid Tensor Experiment**: Scholze's challenge completed by the community.
  - **Sphere Eversion**: Formal verification of a deep topological result.
- **Workflow**: Managed via `lake` (Lean's package manager).
- **Example (Lean 4)**:
  ```lean
  import Mathlib.Data.Real.Basic
  theorem square_nonneg (x : ℝ) : 0 ≤ x^2 := by
    exact pow_two_nonneg x
  ```

## Coq (Rocq)

Historically the first major proof assistant for deep mathematics and CS.

- **Strengths**: Robust foundations, strong community in software verification and constructive logic.
- **Key Results**:
  - **Four Color Theorem**: First fully formal proof (Gonthier, 2005).
  - **Feit-Thompson Theorem**: Proof of the Odd Order Theorem (Gonthier, 2012).
  - **HoTT Library**: Extensive support for Univalent Foundations.

## Isabelle/HOL

Widely used in both pure mathematics and system verification.

- **Strengths**: Extremely powerful automation (Sledgehammer), readable "Isar" proof language, and the **Archive of Formal Proofs (AFP)** with 700+ entries.
- **Key Results**:
  - **Kepler Conjecture (Flyspeck)**: Formal verification by Hales et al. (2014-17).
  - **Prime Number Theorem**: Formalization of its complex analytic proof.

## HOL Light

Lightweight system used for the Flyspeck project and analytic number theory verification.

- **Strengths**: Minimal kernel, extremely reliable, used by Hales for the most critical parts of the Kepler proof.
