# Prover9/Mace4 Syntax

## Connectives & Quantifiers

- `&` (AND), `|` (OR)
- `->` (Implication), `<->` (Equivalence)
- `-` (Negation)
- `all x (formula)`: Universal Quantifier ($\forall x$)
- `exists x (formula)`: Existential Quantifier ($\exists x$)

## Variables & Constants

- **Variables**: By default, `u, v, w, x, y, z` (any name starting with these letters) are treated as variables.
- **Constants/Functions**: Anything not starting with `u..z` is a constant or function.

## Equality

- `=` (Equality)
- `!=` (Inequality)
- Natively supported by Paramodulation. No additional axioms required.

## List Structures

```prover9
formulas(assumptions).
  % Axioms go here
end_of_list.

formulas(goals).
  % Theorem to prove
end_of_list.

% Mace4-specific: force distinct elements
list(distinct).
  [a, b, c, d].
end_of_list.
```

## Operator Precedence

Use `op(precedence, type, name)` to define custom infix operators:
```prover9
op(400, infix, "*").
op(300, infix, "+").
```
Lower precedence numbers bind tighter.
# Prover9/Mace4 Examples

## 1. Group Theory: Self-Inverse Implies Commutativity

Prove that if $x^2 = e$ for all $x$, then $x \cdot y = y \cdot x$.

```prover9
op(400, infix, "*").

formulas(assumptions).
  % Group Axioms
  (x * y) * z = x * (y * z).  % Associativity
  x * e = x.                  % Right Identity
  e * x = x.                  % Left Identity
  x * i(x) = e.               % Right Inverse
  i(x) * x = e.               % Left Inverse

  % Hypothesis
  x * x = e.
end_of_list.

formulas(goals).
  x * y = y * x.              % Goal: Commutativity
end_of_list.
```

## 2. Lattice Theory: Distributivity Counterexample (Mace4)

Find a non-distributive lattice.

```prover9
formulas(assumptions).
  % Join and Meet are commutative
  join(x,y) = join(y,x).
  meet(x,y) = meet(y,x).
  
  % Associative
  join(x, join(y,z)) = join(join(x,y), z).
  meet(x, meet(y,z)) = meet(meet(x,y), z).
  
  % Absorption laws
  join(x, meet(x,y)) = x.
  meet(x, join(x,y)) = x.
end_of_list.

formulas(goals).
  % This goal will be violated by M3 or N5 lattices
  meet(x, join(y,z)) = join(meet(x,y), meet(x,z)).
end_of_list.
```

## 3. First-Order Logic: Syllogism

```prover9
formulas(assumptions).
  all x (man(x) -> mortal(x)).
  man(socrates).
end_of_list.

formulas(goals).
  mortal(socrates).
end_of_list.
```
