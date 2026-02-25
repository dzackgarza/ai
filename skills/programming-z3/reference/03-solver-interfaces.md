# 03 - Solver Interfaces (Incremental Use, Cores, Models, State)

Source anchors: section 4, subsections 4.1-4.6.7 (approx lines 939-1238).

## Incrementality and Scope

Tutorial workflow:
- add baseline assertions,
- call `check()`,
- add temporary assumptions under `push()` scope,
- `pop()` to retract local additions.

```python
from z3 import *

p, q = Bools("p q")
s = Solver()
s.add(Implies(p, q), Not(q))
print(s.check())

s.push()
s.add(p)
print(s.check())
s.pop()
print(s.check())
```

## Assumptions API

Alternative to scopes for one-off checks:
- `s.check(lit1, lit2, ...)`
- `assert_and_track(formula, tracker_literal)`

```python
from z3 import *

p, q = Bools("p q")
s = Solver()
s.add(Not(q))
s.assert_and_track(q, p)
print(s.check())
```

## Unsat Cores

Use tracked assumptions to retrieve explanatory subsets.

```python
from z3 import *

p, q, r, v = Bools("p q r v")
s = Solver()
s.add(Not(q))
s.assert_and_track(q, p)
s.assert_and_track(r, v)

if s.check() == unsat:
    print(s.unsat_core())
```

Important tutorial constraints:
- `unsat_core()` valid only after `check()` returned `unsat`.
- core minimization is optional (`sat.core.minimize`, `smt.core.minimize`).

## Models and Evaluation

```python
from z3 import *

Z = IntSort()
f = Function("f", Z, Z)
x, y = Ints("x y")

s = Solver()
s.add(f(x) > y, f(f(y)) == y)

if s.check() == sat:
    m = s.model()
    for d in m:
        print(d, m[d])
    print(m.eval(x), m.eval(f(3)), m.eval(f(4)))
```

Interpretation notes from tutorial:
- constants map to values;
- functions map to finite entries + default `else` interpretation.

## Other Solver Methods Worth Keeping Handy

From tutorial section 4.6:
- `s.statistics()` - search/procedure counters
- `s.proof()` (requires `produce-proofs`)
- `s.assertions()`, `s.units()`, `s.non_units()`
- `s.sexpr()` - SMT-LIB dump of solver state
- `s.translate(ctx)` - clone solver state into new context
- `s.from_file(...)`, `s.from_string(...)`
- `s.consequences(assumptions, candidates)`
- `s.cube()` for cube-and-conquer style case splits

## Consequences / Backbone Pattern

```python
from z3 import *

a, b, c, d = Bools("a b c d")
s = Solver()
s.add(Implies(a, b), Implies(c, d))
print(s.consequences([a, c], [b, c, d]))
```

## Cubing Pattern

Tutorial presents recursive cube-and-conquer style usage; practical notes:
- empty cube can indicate unsupported cubing or resource limits,
- SAT/SMT core support cubing; generic tactic-based solvers may not.

## Interface Checklist

Before heavy loops:
- decide if assumptions or push/pop is cleaner;
- decide whether core extraction is required;
- decide if context cloning (`translate`) is needed for parallel search.

During diagnosis:
- inspect `statistics()` and `sexpr()` before changing encoding.
