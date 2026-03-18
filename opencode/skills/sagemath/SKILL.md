---
name: sagemath
description: Use when working with SageMath for mathematical computations, algebraic geometry, or number theory
---

# SageMath

## Overview

Work with canonical mathematical objects, not manual constructions. SageMath provides rich algebraic structures—use them.

## Forbidden Patterns

**Never construct objects manually when canonical alternatives exist:**

```sage
# ❌ BAD: Manual matrix/vector construction
M = matrix([[2, -1], [-1, 2]])
v = vector([1, 2, 3])

# ✅ GOOD: Use canonical objects from algebraic structures
R = RootSystem(['A', 2])
L = R.weight_lattice()
alpha = L.simple_roots()
```

**Never test against hardcoded values:**

```sage
# ❌ BAD: Testing specific values
assert result == 42
if gram[0][1] == -1:
    ...

# ✅ GOOD: Test mathematical properties
assert alpha[1].inner_product(alpha[2]) == -1
assert M.is_positive_definite()
```

**Principle:** Manual constructions hide mathematical meaning. Canonical objects encode structure, enable verification, and make code self-documenting.

## Core Rules

### 1. NO Manual Matrix Construction

**NEVER** create matrices like `matrix([[1,2],[3,4]])`. Always use SageMath's built-in objects:

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

Use well-known mathematical objects from literature. Reference standard sources:

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

