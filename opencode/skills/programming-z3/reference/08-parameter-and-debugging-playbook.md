# 08 - Parameter and Debugging Playbook

Source anchors: sections 4.6, 6.1, 6.2, 7.4, and 8 examples.

## First-Line Diagnostics

When solver behavior is surprising:

```python
print(s.assertions())
print(s.sexpr())
print(s.statistics())
```

Use these before changing modeling strategy.

## Core/Assumption Diagnostics

- Ensure `check()` returned `unsat` before reading `unsat_core()`.
- Use `assert_and_track` labels that map to meaningful business constraints.
- If cores are too large, test minimization settings:

```python
s.set("sat.core.minimize", "true")
s.set("smt.core.minimize", "true")
```

## Quantifier Behavior Triage

In complex quantified scenarios, toggle quantifier engines deliberately:

```python
s.set("smt.auto_config", False)
s.set("smt.mbqi", False)
s.set("smt.ematching", False)
```

Then re-enable one path at a time to isolate effects.

## String Solver Backend Triage

```python
s.set("smt.string_solver", "seq")
# or
s.set("smt.string_solver", "z3str3")
```

Switch when one backend struggles on a concrete family.

## SAT-Core Finite-Domain Knobs

For `QF_FD` style workloads:

```python
s.set("sat.cardinality.solver", True)
s.set("sat.pb.solver", "solver")
```

Evaluate against clause-encoding alternatives if performance regresses.

## Parallelism Knobs

```python
set_param("parallel.enable", True)
set_param("parallel.threads.max", 8)
```

Also review SAT co-processing settings (`sat.threads`, `sat.local_search_threads`, etc.) for finite-domain workloads.

## Context and Cloning Safety

- Objects in the same context are not thread-safe together.
- Clone with `translate(ctx)` for independent parallel use.

## Engine Selection Checklist (Fast)

1. General mixed SMT -> `Solver()` / SMT core.
2. Finite domain bit-vector/enum/PB -> `SolverFor("QF_FD")`.
3. Horn rules -> `SolverFor("HORN")`.
4. Quantified elimination-friendly logics -> `SolverFor("LIA")`/`SolverFor("LRA")`/`Tactic("qsat").solver()`.
5. Quantifier-free nonlinear reals -> `SolverFor("QF_NRA")`.

## Failure Pattern Cheat Sheet

- Too many persistent blocking lemmas in model enumeration -> switch to scope-based recursive blocking.
- Unknown or stalled cubing -> verify solver supports cubing and inspect resource limits.
- Unexpected model values -> inspect function `else` branches and use `m.eval` on target terms.
- Exploding arithmetic numerals -> simplify coefficients/representation and reconsider fragment fit.
