---
name: lean4
description: Use when working with theorem proving, formal mathematics, or computational
  counterexamples. Covers local Lean 4 development (proofs, mathlib, lake), cloud-based
  ATP via Aristotle (for offloading difficult proofs), and alternative theorem proving
  software/solvers (Coq, Isabelle, Z3, Prover9, GAP, PySAT).
---
# Theorem Proving and Formalization (Lean 4 & Beyond)

Start here when working on formal mathematics, theorem proving, or computational counterexamples. This skill routes to the appropriate toolchain for the formalization task.

Route to exactly one primary subskill based on the requested tool or workflow:

- [[lean4/skills/lean4/lean4|lean4 core]] — For all local, hands-on Lean 4 work. Use when editing `.lean` files, debugging builds, formalizing mathematics locally, searching mathlib, using Lean LSP tools, or working with lakefiles.
- [[lean4/skills/aristotle/aristotle|aristotle]] — For automated theorem proving in Lean projects using the Aristotle cloud service. Use to submit, offload, or poll parallel/difficult proofs and sorry-fillers without blocking local compute.
- [[lean4/skills/theorem-proving-and-counterexamples/theorem-proving-and-counterexamples|theorem-proving-and-counterexamples]] — For non-Lean formalization or specialized computation. Route here for Coq (Rocq), Isabelle/HOL, SMT solvers (Z3), combinatorial solvers (PySAT, MiniZinc), equational reasoning (Prover9/Mace4), or specialized CAS (GAP, PARI/GP).
- [[lean4/skills/lean4-workflows/lean4-workflows|lean4-workflows]] — For the cameronfreer/lean4-skills structured workflow pack: draft, formalize, autoformalize, prove, autoprove, disprove, checkpoint, review, refactor, golf, learn, diagnose. Use when the user asks for a Lean 4 workflow loop or invokes a `lean4-skills-*` wrapper. Helper runtime at `$LEAN4_SCRIPTS`.

## Before Formalizing Anything

Read before starting: *Mathematics in Lean*; the mathlib4 contribution guide and its
naming and style conventions; the mathlib overview of what is already formalized. Search
mathlib with Loogle, LeanSearch, or Moogle before defining anything, and check the Lean
Zulip for prior attempts at the same object.

These are the mistakes that cost the most on a formalization task, in the order they
usually occur.

**Prior art before code.** The landscape of existing formalizations is vast. Searching
mathlib, Lean community projects, and published formalizations for the objects you need
is not a delay on the way to writing code — it is the step that decides whether the
task is days or months. Rushing into Lean source cripples velocity on a long-horizon
formalization, because every definition written in ignorance of mathlib's must later be
reconciled with it. [[known-solution-first/SKILL|known-solution-first]] owns the search
discipline; the Lean-specific search tools are in the core leaf.

**No section of a paper is out of scope.** Formalizing a paper means formalizing
everything that lies between the paper and mathlib. A claim that some part is out of
scope is really one of two claims, and you must say which: either the foundational
material is already in mathlib — name it — or you are proposing to define the theory
away, which changes what the formalization proves. Silently narrowing scope to what is
reachable produces a document that looks like a formalization of the paper and is not.

**Definitions written by a model are not trustworthy.** There is no reason to trust a
definition a language model produced and every reason to distrust it: a plausible
definition that is subtly wrong makes every downstream theorem vacuous or false, and it
will typecheck. Every definition traces to a cited source — mathlib, the paper, a
textbook — or it is flagged as unverified. This is the highest-risk artifact in the
task, not the proofs.

Substituting a theorem for a definition is the sharpest form of this error. A
characterization that is provably equivalent under the paper's hypotheses is not the
definition, and installing it as one silently imports those hypotheses into everything
downstream — including the statements where they are exactly what is in question.

**Estimate against the dependency graph, not the statement.** A result whose statement
is one line can sit on a large graph of unformalized prerequisites. Look at the actual
graph before committing to a scope. One-shotting a large formalization in a session
produces reward-hacking — `sorry` chains, restated hypotheses, definitions bent to make
a proof close — and passing that off as a formalization is academic fraud, not a
shortcut. `[[difficulty-and-time-estimation/SKILL|difficulty-and-time-estimation]]` owns
the estimate; the honest move when the graph is large is to say so and scope a layer.
