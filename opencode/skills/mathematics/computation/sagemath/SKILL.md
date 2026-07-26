---
name: sagemath
description: Use when working with [[mathematics/computation/sagemath/SKILL|SageMath]] for mathematical computations, algebraic geometry, or number theory
---
# [[mathematics/computation/sagemath/SKILL|SageMath]]

## Overview

Work with canonical mathematical objects, not manual constructions.
[[mathematics/computation/sagemath/SKILL|SageMath]] provides rich algebraic structures—use them.

## Forbidden Patterns

**Never construct objects manually when canonical alternatives exist:**

```sage
# ❌ BAD: Manual matrix/vector construction
M = matrix([[2, -1], [-1, 2]])
v = vector([1, 2, 3])

# ✅ GOOD: Use canonical objects from algebraic structures
R = RootSystem(['A', 2])
L = R.weight_lattice()
α = L.simple_roots()
```

**Never test against hardcoded values:**

```sage
# ❌ BAD: Testing specific values
assert result == 42
if gram[0][1] == -1:
    ...

# ✅ GOOD: Test mathematical properties
assert α[1].inner_product(α[2]) == -1
assert M.is_positive_definite()
```

**Principle:** Manual constructions hide mathematical meaning.
Canonical objects encode structure, enable verification, and make code self-documenting.

## Core Rules

> [!IMPORTANT]
> Code and test examples must satisfy the non-negotiable
> [[policy-index/SKILL|bridge-burning policies]], especially the canonical proof and
> assertion rules.

### 1. NO Manual Matrix Construction

**NEVER** create matrices like `matrix([[1,2],[3,4]])`. Always use [[mathematics/computation/sagemath/SKILL|SageMath]]’s built-in
objects:

```sage
# ❌ BAD: Manual construction
M = matrix([[2, -1, 0], [-1, 2, -1], [0, -1, 2]])

# ✅ GOOD: Canonical objects
R = RootSystem(['A', 3])           # Root system
W = WeylGroup(['B', 4])            # Weyl group
C = CartanMatrix(['E', 8])         # Cartan matrix
L = R.root_lattice()               # Lattice from SageMath
```

### 2. Canonical Examples Only

Use well-known mathematical objects from literature.
Reference standard sources:

```sage
# ✅ GOOD: Canonical objects with citations
R = RootSystem(['E', 8])
L = R.root_lattice()
assert len(L.roots()) == 240  # E8 has exactly 240 roots (Conway & Sloane)

# ✅ GOOD: Cite the mathematical fact
W = WeylGroup(['A', 2])
assert W.order() == 6  # |W(A2)| = 3! = 6 (Humphreys)
```

**References:** Conway & Sloane, Humphreys, Bourbaki, etc.

### 3. Assertion Format

Every assertion must be mathematically verifiable with clear documentation:

```sage
# Mathematical assertion: [What property is being tested]
# sage: R = RootSystem(['E', 8])
# sage: L = R.root_lattice()
# sage: len(L.roots())
# 240  # E8 has exactly 240 roots (Conway & Sloane)
```

**Format:**

- Comment states the mathematical assertion

- Code is runnable in sage blocks

- Result includes citation to mathematical fact

### 4. Compare Mathematical Objects, Not Enumeration Order

Never assert equality of ordered collections when the mathematical guarantee is
order-independent. In particular, do not sort two lists and assert that the resulting
lists are equal:

```sage
# ❌ BAD: Couples the assertion to a non-canonical ordering choice
assert sorted(actual_roots) == sorted(expected_roots)

# ✅ GOOD: Tests equality of the underlying mathematical sets
assert set(actual_roots) == set(expected_roots)
```

Use multiset equality instead when multiplicities are mathematically significant.
Assert sequence equality only when a canonical ordering or normal form is itself part of
the mathematics or the documented public contract, and state that canonicality in the
assertion's explanation.

Tests and examples must survive changes to enumeration and sorting algorithms whenever
those choices do not alter the underlying mathematical object.

### 5. Bind Generators with Sage Syntax

In Sage input, bind a parent and its named generators in the defining assignment:

```sage
# ✅ GOOD: Idiomatic Sage generator binding
R.<x, y> = PolynomialRing(QQ, 2)
```

Do not construct the parent and then name or unpack its generators separately:

```sage
# ❌ BAD: Repeats generator names and separates them from the parent definition
R = PolynomialRing(QQ, 2, names=("x", "y"))
x, y = R.gens()

# ❌ BAD: Spells out the preparser expansion
R = PolynomialRing(QQ, 2, names=("x", "y"))
x, y = R._first_ngens(2)
```

Use `R.<x, y> = ...` whenever the generators are known when the parent is constructed.
This keeps the mathematical declaration atomic and makes the intended Sage structure
immediately legible. The angle-bracket form is Sage preparser syntax for Sage input,
not ordinary Python syntax.

### 6. Make the Code Read Like Mathematics

Choose notation that makes the Sage source resemble the mathematical argument. Sage
supports Unicode identifiers; use standard mathematical symbols when the surrounding
mathematics gives them a clear meaning:

```sage
# ❌ BAD: Transliteration obscures the notation used in the mathematics
alpha1 = L.simple_root(1)
phi = Hom(A, B)(data)

# ✅ GOOD: The source uses the mathematical symbols directly
α_1 = L.simple_root(1)
φ = Hom(A, B)(data)
```

Prefer `α_1`, `φ`, `Δ`, or `W_I` to `alpha1`, `phi`, `delta`, or similarly transliterated
names when those symbols are the established notation. Keep indices visible with
underscores. Apply the same principle to expressions, object names, and the order of
computations: a mathematician should be able to compare the code directly with the
corresponding definition or proof.

Do not introduce symbolic names whose meaning is not established by the surrounding
mathematics. Mathematical readability, not Unicode decoration, is the criterion.
