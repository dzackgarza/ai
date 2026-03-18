---
name: programming-z3
description: "Use when building or reviewing Z3Py workflows and need source-backed guidance across interfaces, theories, solver APIs, tactics, or optimization."
---

# Programming Z3 (Comprehensive)

This skill documents practical Z3 usage from:
- https://theory.stanford.edu/~nikolaj/programmingz3.html

The prior short summary is replaced with a multi-document reference pack.

## How To Use This Skill

1. Start with the module matching your task.
2. Copy API patterns directly from the examples.
3. Keep solver/logical fragment choices explicit (`SolverFor(...)`, theory assumptions, objective mode).
4. If behavior is unclear, inspect solver state (`assertions`, `sexpr`, `statistics`) and re-check fragment fit.

## Document Map

- `reference/01-interfaces-and-ast.md`
  - Logical interfaces, sorts/signatures/terms/quantifiers/lambda, SMT-LIB mapping.
- `reference/02-theories-core.md`
  - EUF, arithmetic fragments, arrays, bit-vectors, floating point, datatypes, strings/sequences, special relations, transitive closure.
- `reference/03-solver-interfaces.md`
  - Incrementality, scopes, assumptions, cores, models, and solver introspection methods.
- `reference/04-solver-usage-patterns.md`
  - Blocking models, all-SMT style enumeration, MSS/MUS workflows, BMC, interpolation, monadic decomposition, subterm simplification.
- `reference/05-solver-implementations.md`
  - SMT core, SAT core, Horn, QSAT, NLSat architecture-level usage implications.
- `reference/06-tactics.md`
  - Tactic basics, tactic pipelines, solvers from tactics, and parallel knobs.
- `reference/07-optimization.md`
  - `Optimize`, soft constraints, objective combinations (box/lex/pareto), MaxSAT framing.
- `reference/08-parameter-and-debugging-playbook.md`
  - Practical parameter/checklist guidance from tutorial examples.

## Coverage Baseline

This pack maps to tutorial sections 2 through 8, with direct API emphasis and implementation-facing notes.

## Scope Boundaries

- This skill focuses on Z3Py usage and solver behavior.
- It does not attempt to re-prove all theory/algorithm details from the tutorial text.
- For deep algorithmic proofs, use the source tutorial and cited papers.
