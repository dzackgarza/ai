---
name: lean4
description: Use when working with theorem proving, formal mathematics, or computational counterexamples. Covers local Lean 4 development (proofs, mathlib, lake), cloud-based ATP via Aristotle (for offloading difficult proofs), and alternative theorem proving software/solvers (Coq, Isabelle, Z3, Prover9, GAP, PySAT).
---
# Theorem Proving and Formalization (Lean 4 & Beyond)

Start here when working on formal mathematics, theorem proving, or computational counterexamples. This skill routes to the appropriate toolchain for the formalization task.

Route to exactly one primary subskill based on the requested tool or workflow:

- [[lean4/skills/lean4/SKILL|lean4 core]] — For all local, hands-on Lean 4 work. Use when editing `.lean` files, debugging builds, formalizing mathematics locally, searching mathlib, using Lean LSP tools, or working with lakefiles.
- [[lean4/skills/aristotle/SKILL|aristotle]] — For automated theorem proving in Lean projects using the Aristotle cloud service. Use to submit, offload, or poll parallel/difficult proofs and sorry-fillers without blocking local compute.
- [[lean4/skills/theorem-proving-and-counterexamples/SKILL|theorem-proving-and-counterexamples]] — For non-Lean formalization or specialized computation. Route here for Coq (Rocq), Isabelle/HOL, SMT solvers (Z3), combinatorial solvers (PySAT, MiniZinc), equational reasoning (Prover9/Mace4), or specialized CAS (GAP, PARI/GP).
