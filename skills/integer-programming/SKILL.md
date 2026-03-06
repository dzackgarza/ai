---
name: integer-programming
description: Solve integer programming and constraint satisfaction problems using OR-Tools CP-SAT, with focus on pure mathematics applications.
metadata:
  author: dzack
  version: "0.1.0"
---

# Integer Programming for Pure Mathematics

## Overview

OR-Tools CP-SAT solver can be applied to problems in number theory, arithmetic geometry, and lattice theory. The key insight is that many mathematical search problems can be encoded as constraint satisfaction or optimization over integers.

**Key constraint:** All constraints must be defined using integers. Multiply by a large integer if necessary to convert non-integer terms.

## Installation

```bash
pip install ortools
```

## Basic Workflow

1. **Create model** - `model = cp_model.CpModel()`
2. **Create variables** - `x = model.new_int_var(0, max, "x")`
3. **Add constraints** - `model.add(x != y)`
4. **Solve** - `solver = cp_model.CpSolver(); status = solver.solve(model)`
5. **Check status** - `OPTIMAL`, `FEASIBLE`, `INFEASIBLE`, `MODEL_INVALID`, or `UNKNOWN`

## Mathematical Applications

### Number Theory

#### Finding Solutions to Diophantine Equations

```python
from ortools.sat.python import cp_model

def find_diophantine_solutions(a, b, c, max_val=100):
    """Find integer solutions to ax + by = c"""
    model = cp_model.CpModel()

    x = model.new_int_var(-max_val, max_val, "x")
    y = model.new_int_var(-max_val, max_val, "y")

    model.add(a * x + b * y == c)

    solver = cp_model.CpSolver()
    status = solver.solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        return solver.value(x), solver.value(y)
    return None
```

#### Pythagorean Triples

```python
def find_pythagorean_triples(limit=100):
    """Find all a^2 + b^2 = c^2 with c <= limit"""
    model = cp_model.CpModel()

    a = model.new_int_var(1, limit, "a")
    b = model.new_int_var(1, limit, "b")
    c = model.new_int_var(1, limit, "c")

    model.add(a * a + b * b == c * c)

    solver = cp_model.CpSolver()
    solutions = []

    class SolutionPrinter(cp_model.CpSolverSolutionCallback):
        def __init__(self):
            super().__init__()
            self.count = 0
        def on_solution_callback(self):
            self.count += 1
            solutions.append((self.value(a), self.value(b), self.value(c)))

    solver.parameters.enumerate_all_solutions = True
    solver.solve(model, SolutionPrinter())
    return solutions
```

#### Finding Representations in Sums of Squares

```python
def representations_as_sum_of_squares(n, k=2, max_val=100):
    """Find representations of n as sum of k squares"""
    model = cp_model.CpModel()

    vars = [model.new_int_var(0, max_val, f"x{i}") for i in range(k)]

    # x1^2 + x2^2 + ... + xk^2 = n
    # Linearize using products
    squares = [model.new_int_var(0, max_val*max_val, f"s{i}") for i in range(k)]
    for i in range(k):
        model.add(squares[i] == vars[i] * vars[i])

    model.add(sum(squares) == n)

    solver = cp_model.CpSolver()
    solver.parameters.enumerate_all_solutions = True

    solutions = []
    class Printer(cp_model.CpSolverSolutionCallback):
        def __init__(self):
            super().__init__()
        def on_solution_callback(self):
            solutions.append([solver.value(v) for v in vars])

    solver.solve(model, Printer())
    return solutions
```

### Arithmetic Geometry

#### Finding Rational Points on Curves

For curves defined by polynomial equations, search for rational/integer points:

```python
def find_points_on_conic(a, b, c, d, e, f, bound=10):
    """Find integer points on ax^2 + bxy + cy^2 + dx + ey + f = 0"""
    model = cp_model.CpModel()

    x = model.new_int_var(-bound, bound, "x")
    y = model.new_int_var(-bound, bound, "y")

    model.add(a*x*x + b*x*y + c*y*y + d*x + e*y + f == 0)

    solver = cp_model.CpSolver()
    solutions = []

    class Printer(cp_model.CpSolverSolutionCallback):
        def __init__(self):
            super().__init__()
        def on_solution_callback(self):
            solutions.append((solver.value(x), solver.value(y)))

    solver.parameters.enumerate_all_solutions = True
    solver.solve(model, Printer())
    return solutions
```

#### Searching for Elliptic Curve Points

```python
def find_elliptic_curve_points(a, b, bound=10):
    """Find integer points on y^2 = x^3 + ax + b"""
    # Ensure valid curve (discriminant != 0)
    model = cp_model.CpModel()

    x = model.new_int_var(-bound, bound, "x")
    y = model.new_int_var(-bound, bound, "y")

    model.add(y*y == x*x*x + a*x + b)

    solver = cp_model.CpSolver()
    solutions = []

    class Printer(cp_model.CpSolverSolutionCallback):
        def __init__(self):
            super().__init__()
        def on_solution_callback(self):
            solutions.append((solver.value(x), solver.value(y)))

    solver.parameters.enumerate_all_solutions = True
    solver.solve(model, Printer())
    return solutions
```

### Lattice Problems

#### Finding Short Vectors

```python
def find_short_vectors(basis, norm_bound=10):
    """Find non-zero integer vector with L1 norm <= bound"""
    n = len(basis)
    model = cp_model.CpModel()

    coeffs = [model.new_int_var(-norm_bound, norm_bound, f"c{i}") for i in range(n)]

    # v = sum(coeffs[i] * basis[i])
    # Find v with small norm
    v = [sum(coeffs[i] * basis[j][i] for i in range(n)) for j in range(n)]

    # At least one coefficient must be non-zero
    model.add(sum(c != 0 for c in coeffs) >= 1)

    # Minimize L1 norm
    abs_v = [model.new_int_var(0, norm_bound * n, f"abs{i}") for i in range(n)]
    for i in range(n):
        model.add(abs_v[i] >= v[i])
        model.add(abs_v[i] >= -v[i])

    model.minimize(sum(abs_v))

    solver = cp_model.CpSolver()
    status = solver.solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        return [solver.value(v[i]) for i in range(n)]
    return None
```

#### Solving Linear Diophantine Equations

```python
def solve_linear_diophantine(coefficients, rhs, bound=100):
    """Find integer solution to a1*x1 + ... + an*xn = rhs"""
    n = len(coefficients)
    model = cp_model.CpModel()

    vars = [model.new_int_var(-bound, bound, f"x{i}") for i in range(n)]

    model.add(sum(coefficients[i] * vars[i] for i in range(n)) == rhs)

    solver = cp_model.CpSolver()

    solutions = []
    class Printer(cp_model.CpSolverSolutionCallback):
        def __init__(self):
            super().__init__()
        def on_solution_callback(self):
            solutions.append([solver.value(v) for v in vars])

    solver.parameters.enumerate_all_solutions = True
    solver.solve(model, Printer())
    return solutions
```

#### Subset Sum / Knapsack

```python
def subset_sum(values, target):
    """Find subset of values that sums to target"""
    n = len(values)
    model = cp_model.CpModel()

    # x[i] = 1 if values[i] is selected, 0 otherwise
    x = [model.new_int_var(0, 1, f"x{i}") for i in range(n)]

    model.add(sum(values[i] * x[i] for i in range(n)) == target)

    solver = cp_model.CpSolver()
    status = solver.solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        return [values[i] for i in range(n) if solver.value(x[i]) == 1]
    return None
```

### Number Theoretic Applications

#### Chinese Remainder Theorem Solutions

```python
def solve_congruences(congruences, bounds):
    """Solve system: x ≡ a_i (mod m_i) for relatively prime moduli"""
    # congruences = [(a1, m1), (a2, m2), ...]
    n = len(congruences)
    M = 1
    for _, m in congruences:
        M *= m

    model = cp_model.CpModel()
    x = model.new_int_var(0, M - 1, "x")

    for a, m in congruences:
        model.add(x % m == a)

    solver = cp_model.CpSolver()
    status = solver.solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        return solver.value(x)
    return None
```

#### Finding Modular Inverses

```python
def modular_inverse(a, m):
    """Find x such that ax ≡ 1 (mod m)"""
    model = cp_model.CpModel()

    x = model.new_int_var(0, m - 1, "x")
    k = model.new_int_var(-m, m, "k")  # For ax = 1 + km

    model.add(a * x == 1 + k * m)

    solver = cp_model.CpSolver()
    status = solver.solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        return solver.value(x)
    return None
```

## Common Constraint Patterns

| Mathematical Concept | Code                                                   |
| -------------------- | ------------------------------------------------------ |
| Equality             | `model.add(x == y)`                                    |
| Inequality           | `model.add(x != y)`                                    |
| Bounded variable     | `model.new_int_var(lo, hi, "name")`                    |
| Boolean variable     | `model.new_int_var(0, 1, "b")`                         |
| Sum constraint       | `model.add(x + y + z == n)`                            |
| Product (linearize!) | Create `p = x * y` as separate IntVar with constraints |
| Modulo               | `model.add(x % m == r)`                                |
| Absolute value       | `model.add(abs_x >= x); model.add(abs_x >= -x)`        |
| AllDifferent         | `model.add_all_different([x, y, z])`                   |
| Implication          | `model.add(x == 0).only_enforce_if(y == 1)`            |

## Handling Non-Linear Expressions

CP-SAT is a **linear** solver. For nonlinear constraints:

1. **For products of variables**: Create intermediate variables and add constraints
2. **For squares**: Use `model.add(square == x * x)` or linearize
3. **For divisions**: Use integer division constraints

```python
# Example: z = x * y with bounded x, y
z = model.new_int_var(lo * lo, hi * hi, "z")
# Add constraints to enforce z == x*y through domain propagation
# (CP-SAT handles this automatically for bounded integers)
```

## Optimization

```python
# Minimize
model.minimize(objective)

# Maximize
model.maximize(objective)

status = solver.solve(model)
print(f"Optimal value: {solver.objective_value}")
```

## Solver Parameters

```python
solver = cp_model.CpSolver()
solver.parameters.max_time_in_seconds = 60
solver.parameters.num_workers = 4
solver.parameters.log_search_progress = True
```

## Return Values

| Status          | Meaning                               |
| --------------- | ------------------------------------- |
| `OPTIMAL`       | Optimal solution found                |
| `FEASIBLE`      | Feasible solution, not proven optimal |
| `INFEASIBLE`    | Problem proven unsolvable             |
| `MODEL_INVALID` | Model validation failed               |
| `UNKNOWN`       | Hit limits before resolution          |

## When to Use CP-SAT vs MILP

- **CP-SAT**: Exhaustive search, counting, feasibility, many binary constraints
- **MPSolver (MILP)**: Linear objectives, continuous relaxations useful, large linear programs
