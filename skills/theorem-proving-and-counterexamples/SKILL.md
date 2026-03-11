---
name: theorem-proving-and-counterexamples
description: Formalize and solve mathematical problems using ITPs (Lean 4/Mathlib, Coq, Isabelle/HOL), Automated Theorem Provers (Prover9/FOL), SMT solvers (Z3), SAT/Combinatorial solvers (PySAT, MiniZinc), and Specialized CAS (GAP, PARI/GP, Singular/M2). Use when Gemini CLI needs to formalize proofs, find counterexamples, or perform specialized computations across analysis, topology, algebra, and number theory.
---

# Theorem Proving and Counterexamples

A comprehensive framework for Interactive Theorem Proving (ITP), Automated Theorem Proving (ATP), model finding, and specialized algebraic computation.

## Choosing a Tool

| Tool | Domain / Strength | Use Case |
| :--- | :--- | :--- |
| **Lean 4 / Mathlib** | Formalization of Modern Math | Analysis, topology, PFR conjecture, Liquid Tensor. |
| **Coq (Rocq)** | Foundational Proofs / CS | Four Color Theorem, Feit-Thompson (Odd Order). |
| **Isabelle/HOL** | Math & Verification | Kepler Conjecture (Flyspeck), Prime Number Theorem. |
| **Prover9 / Mace4** | FOL / Equational | Human-readable proofs, finite models, lattices. |
| **Z3 / SMT** | Arithmetic / Optimization | Number theory, additive combinatorics, knots. |
| **PySAT / MiniZinc** | Combinatorial Solvers | SAT-encoding, Latin squares, extremal set theory. |
| **GAP / PARI / M2** | Specialized CAS | Group theory, Number theory, Algebraic geometry. |

## Workflow

1.  **Select Tool**: Match the problem to the tool's power. Use ITPs for modern math (analysis, measure theory) and ATPs/Solvers for finite/equational search.
2.  **Formalize**: Convert mathematical problem into the target system (Lean code, SMT-LIB, MiniZinc, etc.).
3.  **Execute**:
    -   `lake build` (Lean 4)
    -   `prover9 -f problem.in`
    -   `python script_using_z3.py`
    -   `gap script.g`
4.  **Analyze**: Verify the formal proof (ITP) or extract the model/result (Mace4/Z3/CAS).

## Reference Materials

-   **[itp_systems.md](references/itp_systems.md)**: Lean 4, Coq, and Isabelle/HOL (Modern math formalization).
-   **[prover9_mace4.md](references/prover9_mace4.md)**: FOL syntax and equational reasoning.
-   **[z3_smt.md](references/z3_smt.md)**: SMT-LIB v2, arithmetic, and optimization.
-   **[combinatorial_solvers.md](references/combinatorial_solvers.md)**: SAT (PySAT) and Constraint Programming (MiniZinc).
-   **[specialized_cas.md](references/specialized_cas.md)**: GAP, PARI/GP, and Singular/M2.
