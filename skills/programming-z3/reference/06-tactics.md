# 06 - Tactics and Tactic-Based Solvers

Source anchors: section 7, subsections 7.1-7.4 (approx lines 2553-2617).

## Tactic Role

Tactics transform goals into subgoals. They are preprocessing/strategy building blocks, not just final satisfiability calls.

## Discover Available Tactics

```python
from z3 import *

print(tactics())
for name in tactics():
    t = Tactic(name)
    print(name)
    print(t.help())
    print(t.param_descrs())
```

## Build and Compose Pipelines

```python
from z3 import *

x, y = Reals("x y")
g = Goal()
g.add(2 < x, Exists(y, And(y > 0, x == y + 2)))

pipeline = Then(Tactic("qe-light"), Tactic("simplify"))
print(pipeline(g))
```

## Solvers from Tactics

Given tactic `t`, use `t.solver()` to get a solver that runs tactic reductions before sat/unsat reporting.

```python
from z3 import *

t = Then(Tactic("simplify"), Tactic("smt"))
s = t.solver()
```

## Tactics from Solvers

Tutorial notes there is no direct generic "solver to tactic" conversion API.
Use built-in tactic names corresponding to major engines (for example `sat`, `smt`, `qsat`, `nlsat`, `qffd`) when you need tactic-level composition.

## Parallel Z3 Knobs

Tutorial points to:

```python
from z3 import *

set_param("parallel.enable", True)
set_param("parallel.threads.max", 8)
```

Additional parallel behavior appears via tactic variants (`psat`, `psmt`, `pqffd`) and cube-and-conquer internals.

## Practical Guidance

- Start simple: `simplify -> smt` is often enough.
- Add quantifier or bit-vector specific steps only when needed.
- Check determinism/stability when enabling parallel mode.
- If using cubing/parallel, inspect resource/time behavior and unknown outcomes carefully.
