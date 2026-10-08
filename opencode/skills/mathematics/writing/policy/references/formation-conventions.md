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

## `FORM-11`: Take limits, kernels, cokernels, and exact sequences in the relevant category

A structured category that has its own limits, colimits, or abelian
structure owns those constructions. Kernels, cokernels, quotients,
exact sequences, fibers, and subobjects of a structured object are
taken in the category the object lives in — the category of bilinear
modules, of lattices and integral maps, of quadratic forms — not in
the module category reached by silently applying the forgetful
functor. A construction computed "downstairs" on the underlying
modules has a different type: the cokernel of a map of lattices in
$R\text{-}\mathbf{Mod}$ is again an $R$-module, while the cokernel in
the structured category carries the induced structure, and the two are
related by the forgetful functor only after that functor is stated to
create or preserve the construction (`STR-1`). Applying the forgetful
functor first and presenting the module-level construction as the
result hides the structure the theorem asserts; the underlying-module
computation is a corollary, stated with the comparison that relates
the two (`STR-4`).

**Banned:** "the cokernel $A_L$ of the map $L\to L^\vee$, with the
induced form remembered" where $L\to L^\vee$ is a map of bilinear
modules and the cokernel belongs to the abelian category of bilinear
modules — the module cokernel plus a form remembered afterward is a
different object with a different universal property; "the kernel of
$\rho_L$" with no category, when $\rho_L$ is a map of groups, of
lattices, or of modules and the three kernels differ; "an exact
sequence of modules" standing in for the exact sequence in the
structured abelian category the theorem works in.

**Preferred:** "in the abelian category of $W$-valued $R$-bilinear
modules, $A_L:=\operatorname{coker}(b^\sharp)$ with its induced
pairing; applying the forgetful functor $U$ to the sequence gives the
module sequence, since $U$ creates kernels and cokernels"; "the
kernel of $\rho_L\colon\Orth(L)\to\operatorname{Aut}(D_L)$ in
$\mathbf{Grp}$". Name the category at the construction; state the
creation/preservation claim before computing downstairs
(`SEC-12`, `EV-9`).

The forgetful functor also decides where a property is defined. A
module-theoretic property of a structured object $(L,b)$ — primitivity
of a sublattice, torsion-freeness of a cokernel, finite generation —
is the property of $U(L,b)$, defined once for modules and applied to
the underlying module (`DEF-45`); re-spelling it per structure with
$U$ in the sentence ("the cokernel sequence of $U(f)$ in
$R\text{-}\mathbf{Mod}$ … has torsion-free $Q_f$") names the functor
the definition should have made invisible and takes the cokernel
downstairs where the structured cokernel exists (`PR-76`, `NOT-5`).

Observed in `dzackgarza/research`,
`research/lattice-theory/Isometries-and-Arithmetic-Invariants.md`
(working tree over `57c8eb1cb0`), definition "Primitive embeddings".

**Banned:** "is a *primitive embedding* when the cokernel sequence of
$U(f)$ in $R\text{-}\mathbf{Mod}$ … has torsion-free $Q_f$".

**Preferred:** "a morphism $f\colon S\to L$ of $\mathbf{Lat}_R$ is
**primitive** when $\operatorname{coker}(f)$ is torsion-free" — the
cokernel taken in $\mathbf{Bil}_R$, torsion-freeness the property of
its underlying module.

## `FORM-12`: Hom-objects, functors, and non-linear maps keep their ambient category

A Hom-object carries the structure its category gives it:
$\Hom_{R\text{-}\mathbf{Mod}}(M,N)$ is an $R$-module and an object of
$R\text{-}\mathbf{Mod}$; $\Orth(L)$ is a group; $\Emb(L,M)$ is an
$\Orth(L)\times\Orth(M)$-set. A forgetful functor is a functor between
named categories, and a statement about it is a statement about a
functor — faithful, conservative, creating limits — not about
"forgetful functions" that are "monomorphisms in $\mathbf{Set}$".
Descending to $\mathbf{Set}$ is legitimate only when $\mathbf{Set}$ is
the category the claim lives in. Conversely, a construction that is not
a morphism of the category at hand is placed in the category where it is
one, not asserted to be a morphism there, not dropped, and not left as
a bare function: the diagonal $x\mapsto x\otimes x$ is not $R$-linear,
and its structural account is a natural transformation
$\Delta\colon U\Rightarrow U\circ(-)^{\otimes2}$ of underlying-set
functors, or a quadratic map, with the category stated (`SYM-14`,
`MA-18`).

Observed in `dzackgarza/research`,
`research/lattice-theory/Isometries-and-Arithmetic-Invariants.md`
(working tree over `26d4e303bc`), proposition "Lattice morphisms are
monomorphisms"; the preferred diagonal is the same repository's
`research/category-theory/framework/Bilinear-and-Quadratic-Forms.md`,
definition "Symmetry, alternation, and evenness".

**Banned:** "the forgetful functions
$j_{L,M}\colon\operatorname{PrimEmb}(L,M)\injects\Hom_{\mathbf{Lat}_R}(L,M)$,
$U_{L,M}\colon\Hom_{\mathbf{Lat}_R}(L,M)\injects\Hom_{R\text{-}\mathbf{Mod}}(UL,UM)$
are monomorphisms in $\mathbf{Set}$", with
$\Hom_{R\text{-}\mathbf{Mod}}(UL,UM)$ treated as a set; "the diagonal
$M\to M\otimes_RM$, $x\mapsto x\otimes x$" written as a morphism of
$R\text{-}\mathbf{Mod}$.

**Preferred:** "$U\colon\mathbf{Lat}_R\to R\text{-}\mathbf{Mod}$ is
faithful, and $\operatorname{PrimEmb}(L,M)\hookrightarrow\Hom_{\mathbf{Lat}_R}(L,M)$
is the subobject on which $\operatorname{coker}(Uf)$ is torsion-free"
(`STR-5`); "let $U\colon R\text{-}\mathbf{Mod}\to\mathbf{Set}$ be the
forgetful functor and $\Delta_M\colon U(M)\to U(M\otimes_RM)$,
$x\mapsto x\otimes x$, the natural diagonal of underlying sets", with
$q_b:=U(b)\circ\Delta_M$ — the map in the category where it is a map.

## `FORM-13`: "Underlying" names a forgetful functor, and only a named one

"Underlying" presupposes one forgetful functor to one base. An object
of a category of bilinear modules is a pair $(M,b)$ whose form
$b\colon M\otimes_RM\to W$ has a value module $W$; both $M$ and $W$
are $R$-modules, and a morphism between objects with different value
modules is a pair of module maps. Two forgetful functors leave the
pair, so "the underlying module", "the underlying morphism", and "the
underlying set" have no referent: the reader cannot tell which
component is meant, and the sentence cannot be checked. The object is
the pair, the morphism is the pair of maps, and a component is named
by its symbol — $M$, $W$, $f$ — or by the functor that extracts it,
$U(M)$ with $U$ defined once at its owner (`NOT-7`, `MA-18`).
"Underlying" beside an arrow that already shows its category is
restatement (`PR-76`); "underlying" in place of a component's symbol
is an unresolved reference; a sentence that defines "the underlying
set of $X$" as $U(X)$ defines a word the document then uses as if it
were primitive, when the functor is the primitive and the word is
deleted.

Observed in `dzackgarza/research`:
`research/category-theory/framework/Bilinear-and-Quadratic-Forms.md`
at `57c8eb1cb0`, definition "Form categories";
`research/lattice-theory/discriminant-forms-and-genus.md` (working
tree over `57c8eb1cb0`), definition "Discriminant bilinear and
quadratic forms";
`research/lattice-theory/Lattices-and-Discriminant-Forms.md` at
`ab530c1dcc`, example "Subobjects under extension of scalars";
`research/category-theory/framework/Categorical-Foundations.md` at
`ab530c1dcc`, definition "Concrete categories".

**Banned:** "A morphism $(M,b_M)\to(N,b_N)$ has underlying morphism
$f\in\Hom_{R\text{-}\mathbf{Mod}}(M,N)$ and satisfies $f^*b_N=b_M$.";
"Their common underlying $\bZ$-module is $A_L^\sharp$."; "The
inclusion $\bZ v\hookrightarrow L$ represents a subobject of the
underlying $\bZ$-module."; "The set $U(X)$ is the underlying set of
$X$."

**Preferred:** "a morphism $(M,b_M)\to(N,b_N)$ is
$f\in\Hom_{R\text{-}\mathbf{Mod}}(M,N)$ with $f^*b_N=b_M$"; "$A_L$ and
$A_{L,q}$ are forms on the one module $A_L^\sharp$";
"$\iota_v\colon\langle v\rangle_\bZ\injects L$ in
$\bZ\text{-}\mathbf{Mod}$"; "a concrete category is a pair
$(\category{C},U)$ with $U\colon\category{C}\to\mathbf{Set}$
faithful", and $U(X)$ thereafter.
