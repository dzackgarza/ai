# 07 - Optimization, Multiple Objectives, and MaxSAT

Source anchors: section 8, subsections 8.1-8.2 (approx lines 2618-2812).

## Optimize Context Basics

Use `Optimize()` when satisfiability alone is insufficient.

```python
from z3 import *

o = Optimize()
x, y = Ints("x y")
u, v = BitVecs("u v", 32)

o.maximize(x + 2*y)
o.minimize(u + v)
o.add_soft(x > 4, 4)
```

Tutorial highlights two objective styles:
- direct maximize/minimize over arithmetic/bit-vector expressions,
- soft constraints with optional weights.

## Soft Constraints and 0-1 View

Tutorial shows equivalence between weighted soft constraints and minimization of indicator penalties (via `If` terms).

## Multiple Objective Combination Modes

Tutorial identifies three combination strategies:
- box,
- lex,
- pareto.

Pareto pattern:

```python
from z3 import *

x, y = Ints("x y")
opt = Optimize()
opt.set(priority="pareto")
opt.add(x + y == 10, x >= 0, y >= 0)
mx = opt.maximize(x)
my = opt.maximize(y)

while opt.check() == sat:
    print(mx.value(), my.value())
```

## MaxSAT Notes

Tutorial describes MaxRes-style core-based weakening as default MaxSAT/MaxSMT strategy in Z3, with algorithmic intuition and weighted-handling notes.

Practical implication:
- for many soft-constraint workloads, using `Optimize` soft assertions is usually the right high-level entry.

## Guidance

- Pick objective priority mode explicitly; do not rely on defaults in critical workflows.
- Keep objective semantics separate from feasibility constraints.
- For weighted soft constraints, verify whether weight scaling/truncation assumptions are intended.
- Inspect objective values (`handle.value()`) and not only final model assignments.
