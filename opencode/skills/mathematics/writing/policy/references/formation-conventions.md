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
