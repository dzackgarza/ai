# PySAT (SAT Solver Wrapper)

PySAT is a Python wrapper around high-performance SAT solvers (MiniSat, Glucose, CaDiCaL). It works with propositional logic in Conjunctive Normal Form (CNF).

## Strengths in Pure Math

- **Raw Combinatorial Power**: Modern CDCL solvers handle millions of variables/clauses.
- **Finite Combinatorial Exhaustion**: Most powerful engine for finite state spaces.
- **Proof Certificates**: Can output DRAT proofs for machine-verifiable results.
- **MaxSAT**: Supports weighted/partial MaxSAT for optimization.

## CNF Encoding (DIMACS style)

- Variables: Positive integers (1, 2, 3...)
- Clauses: Lists of integers, e.g., `[1, -2, 3]` ($x_1 \vee \neg x_2 \vee x_3$).

## PySAT Python Interface

```python
from pysat.solvers import Solver
with Solver(name='g4') as s:
    s.add_clause([1, 2])
    s.add_clause([-1, 2])
    if s.solve():
        print(s.get_model())
```

## Applications

- **Extremal Set Theory**: Searching for subsets with specific intersection properties.
- **Combinatorial Exhaustion**: Proving results like "there is no $N \times N$ matrix such that..." for specific $N$.
- **Graph Coloring**: Brute-force graph coloring on large instances.

## Limitations

- **Propositional Only**: No built-in arithmetic or quantifiers. Everything must be encoded as Boolean variables.
- **Encoding Fragility**: Poor encoding leads to intractability.
- **Strictly Finite**: Cannot handle infinite structures.
# MiniZinc (Constraint Modeling)

MiniZinc is a high-level constraint modeling language that compiles to backend solvers (Gecode, Chuffed, OR-Tools).

## Strengths in Pure Math

- **High-level Models**: Syntax is close to mathematical notation.
- **Global Constraints**: `alldifferent`, `table`, `circuit` constraints exploit deep combinatorial structure.
- **Domain Reduction**: Solvers use sophisticated propagation (arc consistency) often more efficient than brute SAT for structured problems.

## MiniZinc Syntax

```minizinc
int: n = 4;
array[1..n, 1..n] of var 1..n: x;

% Latin Square constraints
include "alldifferent.mzn";
constraint forall(i in 1..n) (alldifferent([x[i, j] | j in 1..n]));
constraint forall(j in 1..n) (alldifferent([x[i, j] | i in 1..n]));

solve satisfy;
```

## Applications

- **Latin Squares & Orthogonal Latin Squares**: Natural for $N \times N$ array models.
- **Magic Squares, Sudoku Variants**: Uses `alldifferent` and arithmetic constraints.
- **Combinatorial Designs**: BIBD, Steiner systems, resolvable designs.
- **Graph Theory**: Hamilton cycles (`circuit`), vertex coloring, independence numbers.
- **Finite Geometry**: Constructing or ruling out incidence structures.
- **Tiling & Scheduling**: Polyomino tiling and geometric constraints.

## Limitations

- **Finite Domains Only**: Cannot reason about infinite structures or symbolic algebra.
- **Less Raw Power**: For pure combinatorial exhaustion on unstructured problems compared to SAT.
- **No Proof Certificates**: Unlike SAT solvers with DRAT output.
