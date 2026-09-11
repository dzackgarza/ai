---
name: objects-in-code
description: Use when writing, reviewing, or reviewing tests for code that represents mathematical objects — modules, morphisms, categories, functors, rings, posets, products. Teaches the house mental model: an object is not its presentation, constructions come from universal properties, and every formulation is written at the generality that survives dropping a hypothesis. Load before naming a class, choosing a return type, or deciding how to test a mathematical claim.
---
# Mathematical Objects in Code

The recurring defect in mathematical code here is not a bug. It is a wrong mental
model of what the object *is*, which then produces code that is locally plausible and
mathematically incoherent. This leaf teaches the model.

Each section is one general design principle as it lands in mathematics; the principles
themselves, with their instances in other domains, are in
`code-patterns/references/first-principles.md`. The mapping is exact — the
representation is not the thing, the level where the statement is true, compose before
you construct, behavior belongs with what it governs, one fact one owner, the standard
pattern already exists — which is why recognizing one of these here should transfer,
and why recognizing it only here means it was not learned.

Related: [[mathematics/objects-in-code/references/categorical-architecture|categorical architecture]] for
kernels built on functors and dynamic inheritance;
[[mathematics/research/mathematical-testing/mathematical-testing|mathematical testing]] for what a
test of such an object may assert.

## 1. The Representation Is Not the Thing

A module is not a matrix. A morphism is not its matrix. A group is not a
presentation. A lattice is not a Gram matrix. Presentations are coordinates chosen for
a computation; the object is what survives changing them.

The concrete failure this produces: taking a morphism, extracting its matrix, and
building a second morphism from that matrix. The result is unauditable — nothing in
the code records which bases were in play, so nothing can check that the composite
means anything.

- Compare objects by isomorphism, never by tuples of invariants. Equal invariants are
  a consequence of isomorphism, not a definition of it, and the implication runs one
  way. Two non-isomorphic objects can agree on every invariant you computed.
- Compare morphisms by universal properties they satisfy, not by matrix entries.
- When the data genuinely determines the object on the nose, say so on the nose: if
  `S = S'`, then `Free_R(S) = Free_R(S')` — the same object, equal, not merely
  isomorphic. Do not weaken a strict equality to an isomorphism test because the
  isomorphism test is the one you know how to write.
- Coordinates should be *hard* to reach. If a construction needs a basis, that is a
  fact worth flagging at the call site, not a convenience to expose.

## 2. Stay Inside the Mathematical Universe

Once a value becomes a `tuple`, a `list`, or an `int` length, it has left the
category you were working in and no further statement about it is a mathematical
statement. `len`, indexing, and tuple unpacking are the visible symptoms.

A valence that is an element of the product monoid `NN^k` is not a Python tuple that
happens to hold numbers. If the repository has no object for it yet, the missing
object is the defect. The minimum acceptable repair is a named semantic type at a
single centralized site, documented with the mathematics it denotes:

```python
# In the centralized typing layer:
ProductOfNaturalNumbers = Any  # an element (n_1, ..., n_k) of the product monoid NN^k

def tensor_valence(self) -> ProductOfNaturalNumbers: ...
```

That is worse than a real object and far better than `tuple[int, ...]`: it names what
is meant, it localizes the compromise to one line, and it is greppable when the real
object arrives. The same rule governs `Any` generally — when ambiguity is genuine,
create the type that means what you intend and alias it once.

## 3. Write at the Level Where the Statement Is True

House style runs toward formulations that keep working when a hypothesis is dropped:
finiteness, freeness, projectivity, commutativity, rings to semirings, groups to
monoids. An argument that silently uses the special case in front of you is not a
weaker proof of the general claim — it is a proof of a different claim.

The canonical instance: testing injectivity by comparing ranks of kernels. It is
correct only because the modules at hand are free, the code says nothing about that,
and it breaks silently on the first torsion module. Write the statement that is true
in general:

```python
def is_injective(f):
    return f.kernel() == 0            # or: f.kernel().is_isomorphism(Modules(R).ZeroModule())
```

Before committing a mathematical function or assertion, name the hypothesis your
argument uses, drop it, and see what fails. If the answer is "everything", the
formulation is timid and belongs at higher generality.

## 4. Compose Before You Construct: Universal Properties

Universal objects are unique up to unique isomorphism, so there is exactly one
construction to implement, and constructing it twice returns the same object.

- `C * D` returns a product, whatever the arguments are — categories, objects,
  morphisms. It lives in the common category of its factors (or a routed common
  ancestor: a finite set times a set is a set). It has every method that category's
  objects have, plus projections and the ability to lift morphisms.
- The cartesian product is the fiber product over the terminal object. A design with
  separate interfaces for products and fiber products has duplicated one notion; a
  design with hard-coded `first` and `second` projections has fixed an arbitrary
  indexing that the universal property does not supply.
- A slice `C/X` is a category. Its API — the structure morphism, the transported
  methods — comes from structure functors on that category, recovered by composing
  constructions that already exist, not from new bespoke wiring.

When a desired API falls out as a composition of existing primitives, that is the
good outcome: less code to write, and the result inherits correctness from the
primitives instead of asserting its own.

## 5. Build the Most Structured Object, Then Forget

`ZZ` is simultaneously a ring, a rank-1 `ZZ`-module, a rank-1 `ZZ`-algebra, a monoid,
a group, and a set. These are not competing classifications to choose between. Every
ring `R` is a rank-1 `R`-algebra and a rank-1 `R`-module.

Construct the object with the maximal structure it actually has, and let the routing
present it as the forgotten structure where that is what is wanted. Code that picks
one classification and builds a separate object per view has multiplied the object
and will need equalities between the copies that nothing can supply.

## 6. Structure Versus Property

A poset is not a relation. It is a set equipped with the *data* of a relation. That
makes "poset" a structure, not a property, and structures are declared by giving the
data and the functors that carry it, never by asserting a predicate.

The same distinction decides how a leaf is written: a category whose objects are sets
with extra data defines that data and the functors to the categories it wants methods
from. Note that a forgetful direction need not be unique — a poset category can admit
two different functors to sets that do not agree — and when two paths to the same
target exist, something must say whether they are equal. An implicit assumption that
every such diamond commutes is a mathematical assertion made by omission.

## 7. Behavior Belongs With What It Governs

`A.localization(f)`, not `Localization(A, f)`. A construction performed on an object
is a method of that object: it dispatches on the object's actual category, it is
discoverable from the object, and it cannot be applied to something that does not
support it. A free function takes the construction out of the mathematical structure
and puts it in a module namespace, where nothing routes it.

Declare a catalogue of available objects once, in the place that owns it. Do not
declare it in one file and assert its contents in another — the assertion then tests
that two hand-written lists agree, which is a statement about typing, not mathematics.

## 8. The Standard Vocabulary Is the Standard Model

If you need a noun that is not standard mathematics — a "carrier", a "receiver", a
"role", a "retained composite" — the design is wrong. The noun exists because the
architecture has a thing that mathematics does not name, which means the architecture
has a thing that should not exist. Deleting the word is not the repair; the structure
that demanded it is the repair.

Standard vocabulary is available for everything real here: object, morphism,
underlying set, structure functor, forgetful functor, fiber, section, 2-cell. Use it,
and when a user names one of these, build that thing rather than a proxy with a
different name.
