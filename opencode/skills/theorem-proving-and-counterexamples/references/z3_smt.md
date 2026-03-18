# Z3 (SMT Solver)

Z3 is a Satisfiability Modulo Theories (SMT) solver. It decides satisfiability of formulas in combined first-order theories with built-in decision procedures for arithmetic, bitvectors, arrays, and more.

## Strengths in Pure Math

- **Native Arithmetic**: Directly reason about ℤ, ℝ, divisibility, modular arithmetic, and polynomial equations.
- **Finite Combinatorics**: Combine "choose a configuration" with "satisfying these numeric bounds."
- **Optimization**: Supports `minimize`/`maximize` for extremal combinatorics.
- **Quantifier Reasoning**: Can handle ∀∃ statements in decidable fragments.

## Applications

- **Additive Combinatorics**: Finding cap sets, sum-free sets, and other extremal configurations (e.g., 3-term AP-free sets).
- **Number Theory**: Searching for integer solutions to systems of Diophantine equations.
- **Knot Theory**: Rasmussen invariant and concordance constraints.
- **Graph Theory**: Chromatic bounds and graph coloring.

## SMT-LIB v2 Syntax (S-expressions)

```smt2
(declare-const x Int)
(declare-const y Int)
(assert (> (+ x (* 2 y)) 20))
(assert (forall ((z Int)) (=> (> z x) (> z y))))
(check-sat)
(get-model)
```

## Python Interface (z3-solver)

```python
from z3 import *
x, y = Ints('x y')
s = Solver()
s.add(x + y > 10, x > 0, y > 0)
if s.check() == sat:
    print(s.model())
```

## Limitations

- **Nonlinear Integer Arithmetic**: Undecidable. Z3 uses heuristics and may return `unknown`.
- **Quantified Theories**: Generally incomplete.
- **Proof Structure**: Reports `sat`/`unsat`, but not structured mathematical proofs like Prover9.
