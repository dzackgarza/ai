# Formation conventions (`FORM-*`)


## `FORM-1`: Working 2-category

State the universe. In $\mathbf{Cat}_{\mathcal U}$, objects are
$\mathcal U$-small categories, 1-morphisms are functors, and 2-morphisms are
natural transformations.

## `FORM-2`: Pullbacks

Use pseudo-pullbacks unless the relevant leg is an isofibration. A strict
pullback along an isofibration presents the pseudo-pullback up to
equivalence. A replete full inclusion is an isofibration.

## `FORM-3`: Repleteness

A full subcategory defined by an isomorphism-invariant object property is
replete. A predicate that is not isomorphism-invariant can define a full
subcategory that is not replete.

## `FORM-4`: Categories of elements

Fix one variance convention and state whether the projection is a fibration
or an opfibration. For a presheaf $F$, define its category of elements and its
projection once; a natural transformation of presheaves induces the functor
between categories of elements.

## `FORM-5`: Nerves

The ordinary nerve of a category is the simplicial set of composable chains.
For a simplicial category, use the homotopy coherent nerve ([Kerodon
`00KS`](https://kerodon.net/tag/00KS)); on an ordinary category with discrete
mapping spaces it agrees with the ordinary nerve.

## `FORM-6`: Truncation

Set-level and groupoid-level constructions are not interchangeable. Apply
$\pi_0$ to a homotopy pullback only under hypotheses where $\pi_0$ preserves
the construction; otherwise keep the groupoid-level or space-level object.

## `FORM-7`: Generated functors

A composite, induced functor, inclusion, projection, or whiskered natural
transformation cites the constructions it is obtained from. Natural
transformations are whiskered; functors are composed.

## `FORM-8`: Abelian characterizations

In an abelian category, monicity, epicity, or isomorphism can be expressed by
the kernel and cokernel vanishing criteria. Outside an additive or abelian
setting, use the categorical definition.

## `FORM-9`: Form presheaves

A family of forms is a named presheaf with its codomain stated. If comparison
identities use $R$-module operations, state the presheaf as
$F\colon\mathcal C^{\mathrm{op}}\to R\text{-}\mathbf{Mod}$ and type every
natural transformation in the identity.

## `FORM-10`: Keep the quotient level visible

For a group $G$ acting on a set or space $X$, the object $X$, the action
groupoid $X\!/\!\!/G$, the orbit set $\pi_0(X\!/\!\!/G)=X/G$, and any coarse
or stack quotient are distinct objects at distinct truncation levels. Prose
never collapses them: "classifying embeddings" does not silently pass
between $\Emb(S,L)$, the groupoid $\mathbf{PrimEmb}(S,L)$, the orbit set
$\Orth(L)\backslash\Emb(S,L)$, and the double quotient
$\Orth(L)\backslash\Emb(S,L)/\Orth(S)$. State which object a claim or
count is about, and state the quotient map that relates two levels when
both appear (FORM-6).

**Banned:** "$\Emb(S,L)$ classifies embeddings up to isometry of the
ambient lattice" and, later in the same passage, using $\Emb(S,L)$ to
count $\Orth(L)$-orbits; "the set of equivalence classes of primitive
embeddings is denoted $\Emb(S,L)$" with $\Emb(S,L)$ defined elsewhere as
the set of embeddings.

**Preferred:** name the level at each use: "the set $\Emb(S,L)$ of
primitive embeddings", "the orbit set $\Orth(L)\backslash\Emb(S,L)$",
"the double quotient
$\Orth(L)\backslash\Emb(S,L)/\Orth(S)$, which is not the same object as
$\Orth(L)\backslash\Emb(S,L)$".
