# 05 - Solver Implementations and Selection

Source anchors: section 6 and subsections 6.1-6.5 (approx lines 1633-2552).

## Why This Matters

Z3 has multiple engines. Correct engine selection often matters more than micro-tuning formulas.

Main families in tutorial:
- SMT Core
- SAT Core
- Horn Clause Solver
- QSAT
- NLSat

## 6.1 SMT Core (General-Purpose)

Architecture: CDCL(T) with SAT+EUF core and theory plugins.

Use when:
- mixed-theory formulas,
- general SMT workloads,
- incremental interaction patterns.

Quantifier knobs (tutorial examples):

```python
s.set("smt.auto_config", False)
s.set("smt.mbqi", False)
s.set("smt.ematching", False)
```

Default behavior normally keeps both MBQI and e-matching available.

## 6.1.1 CDCL(T) Practical Consequence

The tutorial's simulated CDCL(T) loop shows:
- propositional abstraction candidate from SAT side,
- theory check over corresponding literals,
- unsat-core-derived blocking clause back to SAT side.

Operational insight:
- strong assumptions/core wiring can make custom hybrid loops practical in Python.

## 6.1.2 Theory Combination

Tutorial explains Nelson-Oppen style constraints (disjointness, stable infiniteness, convexity assumptions).

Practical implication:
- keep signatures/facts cleanly separable where possible,
- avoid unnecessary cross-theory entanglement terms,
- remember bit-vectors are finite-domain and do not fit stable-infinite assumptions.

## 6.1.3 / 6.1.4 Quantifier Engines

- E-matching: syntax/pattern-driven instantiation from ground terms.
- MBQI: model-driven instantiation loop.

Guideline:
- if quantifier behavior is unstable, test with controlled toggles to understand which engine helps/hurts.

## 6.2 SAT Core (`SolverFor("QF_FD")`)

Use when formulas are finite-domain and mostly Boolean/bit-vector/PB/cardinality heavy.

Tutorial example uses enum + bit-vectors + `AtLeast(...)` under `QF_FD`.

Boolean theory handlers and knobs:
- cardinality solver: `sat.cardinality.solver`
- PB solver: `sat.pb.solver`
- local search/co-processing thread knobs in `sat.*`

## 6.3 Horn Clause Solver (`SolverFor("HORN")`)

Use for constrained Horn clauses, recursion/invariant synthesis style tasks.

Tutorial McCarthy-91 example illustrates proving contract properties by relational encoding.

## 6.4 QSAT

Use for quantified formulas in supported logics with quantifier-elimination style support (LIA/LRA/NRA, booleans, some ADT scenarios through tactics).

Tutorial examples:
- stamp denomination quantified LIA,
- dense reals style LRA query,
- quantified NRA,
- ADT game example via `Tactic("qsat").solver()`.

## 6.5 NLSat (`SolverFor("QF_NRA")`)

Specialized nonlinear real arithmetic engine for quantifier-free polynomial formulas.

Use when your formula is genuinely QF_NRA and you want specialized handling.

## Selection Checklist

1. Mixed theories + general constraints -> SMT core / `Solver()`.
2. Finite-domain heavy (`QF_FD`) -> SAT core path.
3. Horn rules/invariants -> `SolverFor("HORN")`.
4. Quantified elimination-friendly logics -> QSAT route.
5. Quantifier-free nonlinear real polynomials -> NLSat.

When in doubt, prototype with explicit `SolverFor(...)` variants and compare `statistics()` and result stability.
