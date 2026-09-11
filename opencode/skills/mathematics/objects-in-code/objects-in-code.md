---
name: objects-in-code
description: Use when writing, reviewing, or testing code that represents mathematical objects — modules, morphisms, categories, functors, rings, posets, products, parents and elements. Hooks the situations where agent priors produce mathematically incoherent code (objects confused with presentations, constructions invented instead of taken from universal properties, values dropped into Python containers) and routes each to the Sage and category-theory literature that settles it.
---
# Mathematical Objects in Code

Mathematical code here goes wrong when the object in the model is not the object in the
mathematics. The correct models are documented — in Sage's own category framework
documentation and in standard category theory — so this file routes to those and records
only the house deviations, which no external source states.

Related: [[mathematics/objects-in-code/references/categorical-architecture|categorical architecture]] for
kernels built on functors and dynamic inheritance;
[[mathematics/research/mathematical-testing/mathematical-testing|mathematical testing]] for what a
test of such an object may assert; `code-patterns/references/situation-to-source.md` for
the general design subjects.

## Parents, elements, and where a method belongs

**Situation.** Deciding whether something is a parent, an element, or a category; writing
a free function that takes an object and returns a construction on it; hand-wiring
initializer chains; wondering how a method reaches an object at all.

**Read.**

- *How to implement new algebraic structures in Sage* (Sage thematic tutorial,
  `thematic_tutorials/coercion_and_categories`) — the category framework and coercion
  model worked through one complete example.
- *Tutorial: Implementing Algebraic Structures* (Sage thematic tutorial,
  `thematic_tutorials/tutorial-implementing-algebraic-structures`).
- The Sage reference manual, *Category Framework* — `ParentMethods`, `ElementMethods`,
  axioms, and how methods are installed by category.
- `sage.structure.parent` and `sage.structure.element`.

**House deviation.** A construction on an object is a method of that object:
`A.localization(f)`, not `Localization(A, f)`. A method true of everything at a
categorical level is defined at that level, not copied into members.

## Objects versus presentations

**Situation.** About to compare two objects; about to extract a matrix, basis, generator
list, or invariant tuple; about to build a morphism out of coordinates.

**Read.**

- Riehl, *Category Theory in Context* (free from the author) — isomorphism, universal
  properties, and why a construction is determined rather than chosen.
- nLab: universal property, structure versus property, forgetful functor, and the
  entries for the specific structures in play.

**House deviation.** Compare by isomorphism, never by tuples of invariants — equal
invariants follow from isomorphism and do not imply it. Never extract a matrix from a
morphism and build another morphism from it; nothing then records which bases were in
play. When data determines the object on the nose, state the equality on the nose: if
`S = S'` then `Free_R(S) = Free_R(S')`. Coordinates should be hard to reach, and a
construction that needs a basis should say so at the call site.

## Products, limits, slices, and other universal constructions

**Situation.** Implementing a product, coproduct, fiber product, quotient, slice, or
graded piece; writing separate interfaces for products and fiber products; hard-coding
`first` and `second` projections.

**Read.**

- Riehl, *Category Theory in Context*, on limits and colimits — including the cartesian
  product as the fiber product over the terminal object, and uniqueness up to unique
  isomorphism.
- Sage's category framework documentation on `CartesianProducts`, `Subquotients`, and the
  other covariant functorial constructions, which is the framework's own answer to where
  such constructions live.

**House deviation.** `C * D` returns a product for any arguments — categories, objects,
morphisms — living in the common category of its factors or a routed common ancestor, and
carrying that category's methods plus projections and morphism lifting. When an API falls
out as a composition of existing primitives, that is the result, not a shortfall.

## Generality

**Situation.** A test or function that works because the objects at hand are free,
finite, commutative, or projective; treating an example offered as illustration as a
ruling.

**Read.** The relevant structure's own entry in a standard algebra reference — Lang,
*Algebra*, or the Stacks Project for the commutative-algebraic and categorical statements
— to find the hypotheses the statement actually needs.

**House deviation.** The direction is toward formulations that survive dropping
finiteness, freeness, projectivity, commutativity, rings to semirings, groups to monoids.
Injectivity is `f.kernel() == 0`, never a comparison of ranks, which is correct only for
free modules and says so nowhere. Name the hypothesis your argument uses, drop it, and see
what fails.

## Values that leave the mathematics

**Situation.** A method about to return a `tuple`, `list`, or `int`; reaching for `len`
or indexing; needing a type for something the repository has no object for.

**House deviation** (this one is local policy, not a documented convention). Once a value
is a Python container it has left the category and nothing further said about it is a
mathematical statement. If the repository has no object for the thing — an element of the
product monoid `NN^k`, say — the missing object is the defect. The minimum acceptable
repair is one named semantic type at a centralized site, documented with the mathematics
it denotes:

```python
# In the centralized typing layer:
ProductOfNaturalNumbers = Any  # an element (n_1, ..., n_k) of the product monoid NN^k

def tensor_valence(self) -> ProductOfNaturalNumbers: ...
```

That is worse than a real object and far better than `tuple[int, ...]`: it names what is
meant, localizes the compromise, and is greppable when the real object arrives.

## Vocabulary

**Situation.** About to introduce a noun that is not standard mathematics — a carrier, a
role, a receiver, a retained composite.

**Read.** nLab or the Stacks Project for the standard name of the thing you are modelling.

**House deviation.** An invented noun means the architecture contains something
mathematics does not name, which means it should not exist. Deleting the word repairs
nothing; the structure that demanded it is the defect.
