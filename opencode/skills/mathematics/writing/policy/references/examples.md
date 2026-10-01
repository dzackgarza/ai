# Examples (`EX-*`)


## `EX-1`: An example mirrors the definition's form

An example instantiates each slot of the structure it exemplifies. If a
monoidal category was defined as a tuple
$(\mathcal{C}, \otimes, \mathbf{1}, \alpha, \lambda, \varrho)$, the example
presents the tuple: "Let $\mathcal{C}$ be a category with finite products
and terminal object $e$. Then $(\mathcal{C}, \times, e)$ is a monoidal
category." The reader who just read the definition sees which slot is
which without parsing prose. Listing the components in a sentence instead
of presenting the tuple is readable but does not mirror the definition's
grammar.

**Banned:** "A category with finite products is monoidal with $a\otimes b$ a
chosen product $a\times b$ and $e$ a terminal object, the three isomorphisms
being the unique ones commuting with the projections; this is the cartesian
monoidal structure."

**Preferred:** "Let $\mathcal{C}$ be a category with finite products and
terminal object $e$. Then $(\mathcal{C}, \times, e)$ is a monoidal category,
with associator and unitors the canonical isomorphisms supplied by the
universal property of the product."

## `EX-2`: An example is an example, not a proposition

If there is nothing to prove, do not present the passage as a proposition
with a proof. A category with finite products is an example of a monoidal
category, not a theorem. State the definition, then give the example in an
example block. Reserve proposition and proof blocks for statements that
require verification beyond unpacking the definition.
