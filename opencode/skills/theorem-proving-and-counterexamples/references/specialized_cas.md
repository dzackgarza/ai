# Specialized Computer Algebra Systems (CAS)

Specialized tools for computational group theory, number theory, and commutative algebra.

## GAP (Group Theory)

Standard for computational group theory (permutation groups, finitely presented groups, polycyclic groups).

- **Strengths**: Character tables, representation theory, and homological algebra (HAP package).
- **Core Operations**: Structure constants, automorphisms, and subgroup lattices.
- **Example**:
  ```gap
  G := SymmetricGroup(5);
  Size(G);
  CharacterTable(G);
  ```

## PARI/GP (Number Theory)

Extremely fast engine for computational number theory and arithmetic geometry.

- **Strengths**: Algebraic number fields (discriminants, class groups, regulators), elliptic curves, and L-functions.
- **Data Engine**: Powers much of the LMFDB (L-functions and Modular Forms Database).
- **Example**:
  ```gp
  K = bnfinit(x^2 + 5);
  K.clgp  \\ Class group
  E = ellinit([0,0,0,0,1]); \\ Elliptic curve
  ellrank(E)
  ```

## Singular & Macaulay2 (Commutative Algebra)

Dedicated to commutative algebra and algebraic geometry.

- **Strengths**: Gröbner bases, syzygies, free resolutions, and resolution of singularities.
- **Geometric Applications**: Sheaf cohomology, primary decomposition, and Hilbert functions/polynomials.
- **Example (M2)**:
  ```m2
  R = QQ[x,y,z];
  I = ideal(x^2 - y, y^2 - z);
  G = gens gb I;
  res(R/I) -- Free resolution
  ```
