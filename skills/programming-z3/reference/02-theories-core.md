# 02 - Core Theories and Modeling Choices

Source anchors: section 3 and subsections 3.1-3.8 (approx lines 379-938 in text dump).

## EUF (Equality + Uninterpreted Functions)

EUF is foundational for symbolic encodings:

```python
from z3 import *

S = DeclareSort("S")
f = Function("f", S, S)
x = Const("x", S)

solve(f(f(x)) == x, f(f(f(x))) == x)
solve(f(f(x)) == x, f(f(f(x))) == x, f(x) != x)
```

Key takeaway from tutorial: congruence closure drives equalities through function applications.

## Arithmetic Fragments Matter

Tutorial distinguishes fragments and their solving styles (LRA, LIA, mixed, difference logics, NRA, NIA). Practical implication:
- model in the strongest supported simple fragment you can;
- avoid accidentally introducing harder nonlinear structures.

Example linear real arithmetic style:

```python
from z3 import *

x, y = Reals("x y")
solve([x >= 0,
       Or(x + y <= 2, x + 2*y >= 6),
       Or(x + y >= 2, x + 2*y > 4)])
```

## Arrays

Core combinators:
- `Select(a, i)` / `a[i]`
- `Store(a, i, v)`
- `K(domain, value)`
- `Map(f, a)`
- extensional reasoning (`Ext` in theory notes)

```python
from z3 import *

x, y = Ints("x y")
A = Array("A", IntSort(), IntSort())
solve(A[x] == x, Store(A, x, y) == A)
```

Tutorial emphasizes reduction to EUF with instantiated store/extensionality constraints.

## Bit-Vectors and Floating Point

Bit-vectors are solved mainly by bit-blasting to SAT-level structure.

```python
from z3 import *

def is_power_of_two(x):
    return And(x != 0, (x & (x - 1)) == 0)

x = BitVec("x", 4)
prove(is_power_of_two(x) == Or([x == 2**i for i in range(4)]))
```

Floating point values are bit-vectors with IEEE interpretation:

```python
from z3 import *

x = FP("x", FPSort(3, 4))
print(10 + x)
```

## Algebraic Datatypes

Use ADTs for finite-tree structures with occurs-check/no-junk/no-confusion properties.

```python
from z3 import *

Tree = Datatype("Tree")
Tree.declare("Empty")
Tree.declare("Node", ("left", Tree), ("data", IntSort()), ("right", Tree))
Tree = Tree.create()

t = Const("t", Tree)
solve(t != Tree.Empty)
prove(t != Tree.Node(t, 0, t))
```

## Sequences and Strings

Z3 supports sequence/string operations (`PrefixOf`, `SuffixOf`, `Length`, `Concat`, `Unit`).

```python
from z3 import *

s, t, u = Strings("s t u")
prove(Implies(And(PrefixOf(s, t),
                  SuffixOf(u, t),
                  Length(t) == Length(s) + Length(u)),
              t == Concat(s, u)))
```

String backend parameter from tutorial:
- `s.set("smt.string_solver", "seq")`
- `s.set("smt.string_solver", "z3str3")`

## Special Relations

Tutorial warns against expensive axiom expansions for partial/total/tree-like orders.
Prefer built-in relation constructors when available:
- `PartialOrder(A, idx)`
- `TotalLinearOrder(A, idx)`
- `TreeOrder(A, idx)`
- `PiecewiseLinearOrder(A, idx)`

This avoids large transitive-closure axiom blowups.

## Transitive Closure

Use `TransitiveClosure(R)` for quantifier-free reachability over relation symbols.

```python
from z3 import *

A = DeclareSort("A")
B = BoolSort()
R = Function("R", A, A, B)
TC_R = TransitiveClosure(R)

s = Solver()
a, b, c = Consts("a b c", A)
s.add(R(a, b), R(b, c), Not(TC_R(a, c)))
print(s.check())  # unsat
```

## Modeling Heuristics

- Prefer built-ins over manual axiom systems when the tutorial provides one.
- Keep fragment boundaries intentional (especially arithmetic/nonlinear and finite-domain choices).
- When combining theories, keep terms purified/simple where possible to reduce integration overhead.
