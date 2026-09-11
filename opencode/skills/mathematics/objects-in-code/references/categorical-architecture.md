# Categorical Architecture: Kernels Built on Functors

Use when working in a repository whose category system is the architecture — a
categorical kernel, a catalogue of categories with objects and morphisms, leaves that
declare new categories. Parent:
[[mathematics/objects-in-code/objects-in-code|objects in code]].

The mental model below is what such kernels are for. Code that contradicts it is not
a style deviation; it reintroduces by hand the obligation the kernel exists to remove.

## Structure Functors Are the Inheritance Mechanism

A leaf writer defines a category `C` and declares a structure functor `F: C -> D`.
That declaration is the whole interface. From it:

- `C.ObjectType` becomes a subclass of `D.ObjectType`, and likewise for morphisms and
  elements — dynamic classes with dynamic inheritance, linearized by the kernel.
- For `X` in `C` and a method `f` defined on objects of `D`, the leaf writer gets
  `X.f()` meaning `F(X).f()` for free.

The leaf writer never names a Python implementation class, never writes an explicit
base-class list, never resolves a diamond, and never reasons about Liskov
substitution. Dispatch may be composition on the backend; the functorial surface must
*read* as mathematics.

Consequences that are easy to get wrong:

- **Manually wiring `super().__init__` chains is a defect, not diligence.** The kernel
  obviates it. Hand-wiring means the leaf has stopped using the mechanism and has
  started re-implementing it.
- **An inverse direction is not needed and usually is not meaningful.** Declaring
  `F: C -> D` gives objects of `C` the methods of `D`. There is no general reason to
  regard an object of `D` as an object of `C`, and asking for one signals that
  transport was modeled as conversion.
- **Selecting a structure functor is not declaring a subcategory.** `F: C -> D` says
  objects of `C` carry the structure `D` describes. It does not say `C` is `D` with
  extra axioms, and conflating the two reproduces exactly the super-category defect
  such kernels exist to avoid.
- **The kernel does not prevent nonsense.** A leaf writer can declare a functor that
  is mathematically false, and the result will be false. Correctness of the
  declaration is the leaf writer's burden; the kernel's burden is that a correct
  declaration produces correct transport.

## Transport Moves Constructor Data

The purpose of a functor is to transport literal constructor data. Writing a leaf
therefore means: decide which categories you want to map into, understand exactly
those categories' constructors, provide constructors on your own objects and
morphisms, and supply the rule that turns one of your constructions into theirs.

Nothing about that is Python programming, which is the point: a mathematician who
does not program should be able to reason to correct code from the categories and
functors alone. Getting a leaf running should be thin and quick. If a leaf is
accumulating boilerplate, the kernel has a gap, and the gap is the finding — not the
boilerplate.

## Points, Diamonds, and 2-Cells

- A point is a functor `* -> C`. If `NN: * -> Sets` is a point, then `NN` is an object
  of `Sets`, its elements are elements of a set, and every set is a discrete category.
  Points propagate by the same transport rule as everything else; they are not a
  special case needing its own mechanism.
- A leaf may lift a point through several categories in sequence — a point in
  countable sets, lifted to magmas in two different ways so that `+` and `*` are both
  available, then to monoids, then to semirings.
- Two lifts of the same object give two paths to one target. Whether the resulting
  composites agree is a mathematical fact that something must state. Assuming every
  diamond commutes is an assertion by omission. The honest design has leaf writers
  supply a 2-cell, with identity 2-cells trivial to declare, and installs methods from
  both paths when no cell is given.
- This is where additive and multiplicative structure actually conflict: one category
  of magmas supplies implementation methods, but one lift wants `X.zero()` and the
  other wants `X.one()`. Solve it with the cell, not by special-casing names.

## Scope of Formalization

These kernels are 1-categorical almost everywhere — everything imported from a general
CAS certainly is — with a small reach into 2-categories because functor categories and
natural transformations are formalized. That reach does not create an obligation to
*prove* coherence in code. Proving mathematical results is Lean's job, not Python's.

The obligation is narrower and firm: be mathematically principled, and define nothing
that is mathematically ill-defined. Maintaining rigour is not a licence to add large
amounts of code to satisfy a self-imposed mandate that the repository's stated purpose
does not require.

## Enforcing Declarations

A category must declare its `ObjectType`, `MorphismType`, and similar. Python cannot
enforce that a class contains a nested class. The workable pattern is a top-level
abstract base class with an abstract method returning the type, so that a missing
declaration fails at instantiation with a message naming the obligation.

"Raise unless overridden" written by hand is the wart, not the solution: abstract base
classes exist to communicate exactly this contract, and inheriting a contract should
make the obligations legible from a single attempted instantiation.
