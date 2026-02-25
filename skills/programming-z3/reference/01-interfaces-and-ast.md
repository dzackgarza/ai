# 01 - Logical Interfaces and AST Basics

Source anchors: Programming Z3 sections 2, 2.1, 2.2, 2.3, 2.4 (approx lines 171-378 in text dump).

## Core Mental Model

Z3 consumes many-sorted first-order formulas with theory symbols. In Z3Py:
- You build terms/formulas as expression trees.
- You assert Bool-sorted formulas into a solver.
- You call `check()` and inspect `model()` for sat states.

## Minimal Propositional Pattern

```python
from z3 import *

Tie, Shirt = Bools("Tie Shirt")
s = Solver()
s.add(Or(Tie, Shirt), Or(Not(Tie), Shirt), Or(Not(Tie), Not(Shirt)))
print(s.check())
print(s.model())
```

## Mixed-Theory Formula Pattern

The tutorial highlights composing arithmetic + arrays + uninterpreted functions:

```python
from z3 import *

Z = IntSort()
f = Function("f", Z, Z)
x, y = Ints("x y")
A = Array("A", Z, Z)

fml = Implies(x + 2 == y, f(Store(A, x, 3)[y - 2]) == f(y - x + 1))
solve(Not(fml))
```

## SMT-LIB Interoperability

Z3Py expressions correspond to SMT-LIB2 formulas. Useful for debugging interoperability:

```python
from z3 import *

x, y = Ints("x y")
s = Solver()
s.add((x % 4) + 3 * (y / 2) > x - y)
print(s.sexpr())
```

## Sorts You Should Reach For

From tutorial coverage:
- `BoolSort()`, `IntSort()`, `RealSort()`
- `BitVecSort(n)`
- `Array(IndexSort, ElemSort)`
- `StringSort()` and `SeqSort(S)`
- `DeclareSort("S")` for uninterpreted sorts

Uninterpreted sort domains are non-empty. This matters for satisfiability reasoning.

## Signatures and Symbols

- Constants are nullary functions.
- Free function symbols are declared with explicit domain/range sorts.
- Boolean-range functions can be used directly as formula-producing predicates.

```python
from z3 import *

B = BoolSort()
Z = IntSort()
f = Function("f", B, Z)
g = Function("g", Z, B)
a = Bool("a")
solve(g(1 + f(a)))
```

## Terms, Formulas, and AST Inspection

A Bool-sorted expression is a formula. Inspect AST shape with:
- `num_args()`
- `children()`
- `arg(i)`
- `decl()`
- `decl().name()`

```python
from z3 import *

x, y = Ints("x y")
n = x + y >= 3
print(n.num_args(), n.children(), n.arg(0), n.arg(1), n.decl(), n.decl().name())
```

## Quantifiers and Lambda Notes

- `ForAll` / `Exists` bind variables in local scope.
- Bound names are not assignments; they are scoped binders.
- Lambda terms are supported and represented through array/function-space mechanisms.

Example pattern from tutorial:

```python
from z3 import *

x, y, z = Ints("x y z")
m = Array("m", IntSort(), IntSort())

def memset(lo, hi, v, arr):
    return Lambda([x], If(And(lo <= x, x <= hi), v, Select(arr, x)))

m1 = memset(1, 700, z, m)
solve(Select(m1, 6) != z)
```

## Practical Guidance

- Keep sort discipline explicit; most subtle bugs are sort mismatches.
- Prefer small helper constructors for repeated expression templates.
- Use `sexpr()` when model/query behavior is surprising; inspect the exact asserted form.
