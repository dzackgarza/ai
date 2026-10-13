# Symbols and binding (`SYM-*`)

Mathematical text follows scoping and binding conventions analogous to those
in a formal language. A symbol is bound at the point where the object it
names is declared — with its type, domain, codomain, or constituent data.
Before that point, the symbol is unbound and the reader cannot determine
what it refers to. Naming a type ("let $\mathcal{C}$ be a monoidal
category") does not bind the symbols for that type's constituent data
($\otimes$, $\mathbf{1}$, $\alpha$, $\lambda$, $\varrho$); those are bound
by stating the tuple
$(\mathcal{C},\otimes,\mathbf{1},\alpha,\lambda,\varrho)$. A symbol used
before its binding is an unbound reference; a symbol that changes meaning
within a passage is a shadowing conflict.

## `SYM-1`: A symbol used without being bound

A passage uses a symbol before declaring the object it names. No type, no
domain, no codomain, and no constituent tuple is stated. The reader cannot
determine what the symbol refers to without external knowledge. Bind the
symbol first: state the object, its mathematical type (element, set, map,
space, group, ring, module, category, functor), and where it lives — the
map's domain and codomain, or the structure's tuple. Then use the symbol.
Introduce every object, map, index, and codomain before its first use.

**Banned:** "The map $f$ is surjective, where $X$ is the source."

**Preferred:** "For schemes $X$ and $Y$, let $f\colon X\to Y$ be a
morphism. Assume $f$ is surjective."

**Banned:** "A monoid in $(\mathbf{Ab},\otimes_{\mathbb Z},\mathbb Z)$ is a
ring, its multiplication being the bilinear map classified by $\mu$ and its
unit the image of $1$ under $\eta$." The symbols $\mu$ and $\eta$ are used
without being introduced; no abelian group $A$ is named; no domains or
codomains are stated.

**Banned:** "Let $S$ be a symmetric monoidal category. … Then $\otimes$
makes $S^{\mathrm{iso}}$ an abelian monoid." The tensor $\otimes$ is used
without being bound — stating the type "symmetric monoidal category" does
not introduce the symbol $\otimes$.

**Preferred:** "A monoid object in
$(\mathbf{Ab},\otimes_{\mathbb{Z}},\mathbb{Z})$ is a triple
$(A,\mu,\eta)$ where $A$ is an abelian group,
$\mu\colon A\otimes_{\mathbb{Z}}A\to A$ is a homomorphism, and
$\eta\colon\mathbb{Z}\to A$ is a homomorphism. The bilinear multiplication
$A\times A\to A$ is the map corresponding to $\mu$ under the tensor-hom
adjunction, and the unit element is $\eta(1)$." Name the data, then use the
symbols.

A symbol bound in the prose preamble of a chapter and used in a theorem
several blocks later is the same defect at chapter scale: the preamble
is not a block, and the theorem opens without the binding. The symbol is
bound inside the definition block that owns it, and the theorem recalls
it by citing that block (`SEC-6`, `SYM-15`).

Observed also in `dzackgarza/research` at `9cfdecf73d`:
`research/lattice-theory/Coxeter-Systems-and-Lattices.md`, the chapter
preamble binding $V$ and theorem "The radical of a parabolic system".

**Banned:** "let $V$ be the real vector space with basis
$\{\alpha_s\}_{s\in S}$" in the chapter preamble, with "Then $\radic(V)$
is spanned by a vector" in a theorem that does not bind $V$.

**Preferred:** "$V\definedas\bigoplus_{s\in S}\bR\alpha_s$" inside the
definition of the form, and "Let $(W,S)$ be irreducible and parabolic
with form $b$ on $V$ (@def:coxeter-form)." opening the theorem.

## `SYM-2`: Data referenced by role instead of by declaration

A passage refers to "the multiplication", "the unit", "the associator", or
"the classifying map" without first declaring the object that plays that
role. The role name presupposes the data without stating it. Declare the
data — the map, its domain, its codomain — then refer to it by name. A role
description is a comment on data that has been stated, not a substitute for
stating it.

**Banned:** "its multiplication being the bilinear map classified by $\mu$"
— "the multiplication" is a role; $\mu$ is undeclared; "the bilinear map
classified by $\mu$" describes what $\mu$ does without stating what $\mu$
is.

**Preferred:** "$\mu\colon A\otimes_{\mathbb{Z}}A\to A$ is a homomorphism;
the corresponding bilinear map $A\times A\to A$ is the multiplication."
Declare the map, then name its role.

## `SYM-3`: A tensor symbol has neither a bound monoidal structure nor an explicit base

A bare tensor symbol $\otimes$ is meaningful only after the monoidal product itself has been bound as constituent data, e.g. by a tuple $(\mathcal C,\otimes,\mathbf 1)$ (with any further associator, unitors, or braiding also named). In module, lattice, sheaf, or algebra contexts there is no such implicit binding: the base ring or structure sheaf is part of the type and must appear in every tensor expression.

Thus write $M\otimes_RN$, $L\otimes_{\mathbb Z}\mathbb Q$, $\mathcal L\otimes_{\mathcal O_X}\mathcal M$, $(f\otimes_R g)$, and $x\otimes_Ry$. The rule applies equally to tensor powers, pure tensors, tensors of morphisms, scalar extension, and derived tensor products (with the base displayed, e.g. $\otimes_R^L$).

**Banned:** "$M\otimes N$" in $\mathbf{Mod}_R$; "$L\otimes\mathbb Q$" for an integral lattice; "$\mathcal L^{\otimes 2}$" for a line bundle on $X$; "$(f\otimes f)^*$" in an $R$-linear module category.

**Preferred:** "$M\otimes_RN$"; "$L\otimes_{\mathbb Z}\mathbb Q$"; "$\mathcal L^{\otimes_{\mathcal O_X}2}$"; "$(f\otimes_Rf)^*$". Bare $\otimes$ is reserved for passages that first bind the monoidal structure itself, such as "let $(\mathcal C,\otimes,\mathbf1)$ be a monoidal category."

## `SYM-4`: A symbol overloaded within one passage

A single symbol is used for two distinct mathematical objects in the same
passage — a terminal object and an identity morphism, a unit element and a
unit map — so the reader cannot determine which referent is in force at
each occurrence. Each symbol has one meaning throughout the document
(`NOT-3`); within a single passage the constraint is tighter, because the
two referents appear side by side.

**Banned:** "Let $\mathcal C$ have finite products and a terminal object
$1$. … $\mu\circ(1\times\zeta)\circ\delta$" — the first $1$ is the
terminal object, the $1$ in $1\times\zeta$ is $\operatorname{id}_c$.

**Preferred:** use distinct symbols. Name the terminal object $e$ or
$\mathbf{1}$, and write $\operatorname{id}_c$ for the identity morphism.
No reader confuses $\operatorname{id}_c\times\zeta$ with
$e\times\zeta$.

## `SYM-5`: A map written without its domain and codomain

A morphism is written as a bare symbol in an equation — $1\times\zeta$,
$\mu\circ\delta$ — or named in prose as "the natural map $f$" without
stating its domain and codomain. The reader must infer the types from
context, and cannot check or compose the map until its source, target,
and construction are stated. The type is part of the mathematical
statement. Wherever the reader meets the maps for the first time, as in a
definition, state the domain and codomain of each map before using it in
an equation.

**Banned:** "$\mu\circ(1\times\zeta)\circ\delta=\eta\circ{!}_c$" with no
domain or codomain stated for $1\times\zeta$, $\delta$, or $!_c$ before
their use.

**Preferred:** "$\operatorname{id}_c\times\zeta\colon c\times c\to
c\times c$, $\delta\colon c\to c\times c$, and $!_c\colon c\to
\mathbf{1}$" stated before the equations that use them.

**Banned:** "Consider the natural map $f$."

**Preferred:** "Consider the natural morphism $f\colon X\to Y$ induced by
the ring map $A\to B$."

## `SYM-6`: A symbol introduced after its first use

A "where" clause defines $\delta$ after $\delta$ has already appeared in
the equations above it. In a definition, every symbol is introduced before
its first use. A "where" clause after an equation is a trailing gloss for
a reader who already knows the notation; it is not a substitute for
stating the data before using it.

**Banned:** equations using $\delta$, then "where
$\delta\colon c\to c\times c$ is the diagonal."

**Preferred:** "Let $\delta\colon c\to c\times c$ be the diagonal and
$!_c\colon c\to\mathbf{1}$ the unique map. Then …" — state the maps,
then write the equations.

## `SYM-7`: A tuple-defined structure referred to in prose instead of by its tuple

A structure that was defined as a tuple — a monoidal category
$(\mathcal{C},\otimes,\mathbf{1})$, an adjunction $(F,G,\eta,\epsilon)$,
a chain complex $(C_\bullet,d)$ — is referred to in prose instead of by
the tuple. The reader must assemble the structure from English instead of
recognizing the tuple that was defined. Refer to a tuple-defined structure
by its tuple.

**Banned:** "a monoid for the cartesian structure"; "the adjunction
between free and underlying"; "the complex with the standard
differential."

**Preferred:** "a monoid object in $(\mathcal{C},\times,\mathbf{1})$";
"the adjunction $(F,G,\eta,\epsilon)$"; "the chain complex
$(C_\bullet,d)$." Name the structure the same way it was defined.

## `SYM-8`: A mathematical object named by a prose qualifier instead of by its type

A mathematical object is named by a bare noun qualified by a prepositional
phrase — "a monoid for the cartesian structure", "a module for the group
action", "a sheaf for the topology" — instead of by its type and the
category it lives in. State the type and the category; do not qualify a
bare noun with prose.

**Banned:** "a monoid for the cartesian structure"; "a module for the
group action"; "a sheaf for the topology."

**Preferred:** "a monoid object in $(\mathcal{C},\times,\mathbf{1})$";
"a module over $R[G]$"; "a sheaf on $(X,\mathcal{O}_X)$." The type names
the kind of object; the category names where it lives.

## `SYM-9`: Parallel notions in uniform notation

Parallel notions use parallel notation. Left and right modules, left and
right actions, opposite categories — each pair has two sides that the
reader must distinguish at a glance. Using $A\text{-}\mathbf{Mod}$ for
left modules but $B^{\mathrm{op}}\text{-}\mathbf{Mod}$ for right modules
is inconsistent: the first names the side by position, the second by an
opposite. The same inconsistency appears in mixing
$\mathbf{LMod}_A$ with $A\text{-}\mathbf{Mod}$ in one passage.

**Banned:** "$A\text{-}\mathbf{Mod}$ for left $A$-modules but
$B^{\mathrm{op}}\text{-}\mathbf{Mod}$ for right $B$-modules in the same
passage."

**Preferred:** "$\mathbf{LMod}_A$ and $\mathbf{RMod}_A$" or
consistently "$A\text{-}\mathbf{Mod}$ and $\mathbf{Mod}\text{-}A$." Choose
one convention for sidedness and use it uniformly in the passage.

## `SYM-10`: Strict identity versus canonical equivalence

Strict identity ($=$), isomorphism ($\cong$), and equivalence ($\simeq$)
are distinct (NOT-2). "The identity $A=A^{\mathrm{op}}$" for a commutative
ring asserts strict identity where, in a document that adopts the derived
and homotopical ontology (DEF-13), the default structure is at most a
canonical equivalence: for an $\mathbb{E}_\infty$-ring spectrum $A$,
$A\simeq A^{\mathrm{op}}$ via the symmetry; for a discrete commutative
ring the equality is strict, but only after truncating to $\pi_0$. Do not
write $A=A^{\mathrm{op}}$ for the derived identification.

**Banned:** "When $A$ is commutative, the identity $A=A^{\mathrm{op}}$
identifies left and right $A$-module conventions."

**Preferred:** "When $A$ is a commutative ($\mathbb{E}_\infty$) ring
spectrum, the symmetry gives a canonical equivalence
$A\simeq A^{\mathrm{op}}$, hence
$\mathbf{LMod}_A\simeq\mathbf{RMod}_A$." Name the equivalence and how it
is produced.

## `SYM-11`: Structured object versus underlying set

A ring presented as a tuple $(|A|,+,0,\cdot,1,\ldots)$ and its opposite
$(|A|,+,0,\cdot^{\mathrm{op}},1,\ldots)$ share the underlying set $|A|$
but are not strictly equal as tuples: the multiplications are opposite,
related by the monoidal twist. Writing "the identity $A=A^{\mathrm{op}}$"
conflates equality of underlying sets with equality of structured objects.
For an $\mathbb{E}_\infty$-ring spectrum the two are canonically
equivalent via the symmetry, not strictly equal; for a discrete
commutative ring strict equality holds only after forgetting to the
underlying set or to $\pi_0$. State equality of the correct underlying
data, and name the canonical equivalence for the structured objects.

**Banned:** "the identity $A=A^{\mathrm{op}}$ identifies left and right
$A$-module conventions" — asserts strict identity of tuples whose
multiplications differ by a twist.

**Preferred:** "the underlying sets of $A$ and $A^{\mathrm{op}}$
coincide and the multiplications are opposite via the twist; for
$\mathbb{E}_\infty$ $A$ the symmetry gives a canonical equivalence
$A\simeq A^{\mathrm{op}}$, hence
$\mathbf{LMod}_A\simeq\mathbf{RMod}_A$." Distinguish the set, the
tuple, and the equivalence.

## `SYM-12`: Derived tensor product not distinguished from underived

In a document that adopts the derived and spectral ontology (DEF-13), $\otimes_A$ is the
derived tensor product $\otimes_A^L$; the underived tensor on discrete
modules is the further truncation $\pi_0(-\otimes_A^L-)$. Writing
$B\otimes_A M$ without stating whether it is derived or underived leaves
the reader unable to determine whether the construction is homotopically
correct. State the derived product; note when passage to $\pi_0$ recovers
the classical formula.

**Banned:** "$B\otimes_A M$" and "$b_B(c\otimes_A x,d\otimes_A y)=cd\otimes
b(x,y)$" with no indication whether $\otimes_A$ is $\otimes_A^L$.

**Preferred:** "$B\otimes_A^L M$ for derived extension of scalars; its
$\pi_0$ recovers the classical $B\otimes_A M$ for discrete $A,B,M$." Name
the derived product where it is meant.

## `SYM-13`: Classical module notation for $\infty$-categorical modules and terminological drift

Classical notation $R\text{-}\mathbf{Mod}$, $R^{(I)}$, and $R^n$ for
modules is the truncation to the heart. In a document that adopts the
derived ontology (DEF-13), the default is
$\mathbf{LMod}_R$, $\mathbf{RMod}_R$, ${}_A\mathbf{Bimod}_B$ (or
${}_A\mathbf{BiMod}_B$) for presentable stable $\infty$-categories of
module spectra, and $\bigoplus_{i\in I}R$ (coproduct in
$\mathbf{LMod}_R$) for the free module on a set $I$. $R^{(I)}$ and the
surjection $R^n\twoheadrightarrow M$ are the classical shadows; they are
correct only after truncating to $\pi_0$ or to discrete $R$. Allowing
$R\text{-}\mathbf{Mod}$, $\mathbf{LMod}_R$, $R^{(I)}$, $\bigoplus_I R$,
and $R^n$ to drift interchangeably is notational drift: fix one
convention for the $\infty$-categorical objects and use it uniformly and
repeatedly, stating the truncation explicitly when the classical shadow
is meant.

**Banned:** "$R\text{-}\mathbf{Mod}$ for the $\infty$-category;
$R^{(I)}$ for the free module spectrum; $R^n\twoheadrightarrow M$ for an
effective epimorphism in $\mathbf{LMod}_R$ without marking the
truncation" — or any of those notations alternating with
$\mathbf{LMod}_R$/$\bigoplus_I R$ in the same chapter.

**Preferred:** "$\mathbf{LMod}_R$ (resp. $\mathbf{RMod}_R$,
${}_A\mathbf{BiMod}_B$) for $\infty$-categories;
$\bigoplus_{i\in I}R\twoheadrightarrow M$ as an effective epimorphism for
finitely generated; $M\simeq\bigoplus_{i\in I}R$ for free." Fix the
$\infty$-categorical convention once and use it uniformly; note when
passage to $\pi_0$ recovers the classical $R\text{-}\mathbf{Mod}$ or
$R^{(I)}$.

## `SYM-14`: Adjectival map prose instead of the typed membership

A map is characterized by an adjective — "$R$-linear", "the inclusion",
"the restriction", "the projection", "the natural map", "the induced
map", "the dual map" — instead of the typed membership that fixes its
source, target, and ambient Hom-set or category. The adjective asks the
reader to reconstruct the map; the membership exhibits it. Every map is
typed: write $f\in\operatorname{Hom}_{\mathcal C}(M,N)$, or
$f\colon M\to N$ in $\mathcal C$, with the ambient category named at the
first use. "The matrix of $f$" does not exist until bases are chosen
(`PR-58`, `PR-59`); "regarded inside" and "restricts to" name no
monomorphism, no pullback, and no subobject. "Restricts to" is the
shadow of a stated mono $i\colon N\rightarrowtail M$ and the pullback of
a map along $i$; write the mono and the pullback.

**Banned:** "the inclusion $S\subseteq L$"; "the map $f$ is
$R$-linear"; "the matrix of $f$"; "$M$ regarded inside $N$" with no map;
"$f$ restricts to a map $S\to T$."

**Preferred:** "$\iota\colon S\hookrightarrow L$ a monomorphism in
$R\text{-}\mathbf{Mod}$"; "$f\in\operatorname{Hom}_{R\text{-}\mathbf{Mod}}(M,N)$";
"for ordered bases $e$ of $M$ and $e'$ of $N$, the matrix
$[f]_{e,e'}\in M_n(R)$"; "the pullback of $f$ along $i$ in the square
$S\times_M N\to S$, $S\times_M N\to N$" (`EV-5`).

## `SYM-15`: Recall distant bespoke notation at substantive reuse

When notation defined far away re-enters a theorem, proposition, or other
self-contained unit, gloss it at the first substantive reuse. Cite the
defining occurrence and state what the symbol denotes. A bare
cross-reference supplies provenance but does not make a dense symbolic
statement locally readable (`XREF-6`). Standard notation needs no gloss.

**Banned:** a theorem that uses $N_b(L)$ after many sections with only a
bare reference to its definition.

**Preferred:** "where $N_b(L)=\exp(A_L^\sharp)$ is the bilinear
denominator of $L$ (@def:discriminant)."

Observed in `dzackgarza/research`,
`research/lattice-theory/embeddings/orthogonal-complements.md`
(working tree over `57c8eb1cb0`), proposition "Discriminants of
orthogonal sums".

**Banned:** "$N\definedas\operatorname{lcm}_{1\leq i\leq n}N_b(L_i)$"
in a proposition far from the definition of $N_b$, with no gloss.

**Preferred:** "$N:=\operatorname{lcm}_iN_b(L_i)$, where
$N_b(L_i)=\exp(A_{L_i}^\sharp)$ is the bilinear denominator of $L_i$
(@def:discriminant)".

## `SYM-16`: A map's codomain is the value object its construction determines

The codomain of a map is part of its type. When a construction
determines a value object — a finite-exponent quotient
$\tfrac1N\mathbb Z/\mathbb Z$, a submodule $\operatorname{Val}(b)$,
an ideal $J$ — the map is written into that object, and a coarser
ambient object such as $\mathbb Q/\mathbb Z$ is reached through the
monomorphism that the construction supplies, named where the comparison
with a source that uses the coarse codomain is made (`NOT-1`,
`TERM-3`). Writing the map into the coarse object discards the type
information the construction produced: the exponent, the level, the
parity data that the later theory reads off the codomain. The same
holds for the domain: a bilinear form is a map out of
$M\otimes_RM$, not out of $M\times M$ (`MA-14`).

Observed in `dzackgarza/research`,
`research/dissertation/sections/1-part-combinatorial/2-chapter-lattice-theory/100-foundations.md`
(working tree over `2b758e124b`), definition "Discriminant Forms"; the
preferred form is the same repository's
`research/lattice-theory/Lattices-and-Discriminant-Forms.md`, definition
"Bilinear and quadratic discriminant forms".

**Banned:** "the **discriminant bilinear form** is
$\beta_{A_L}\colon A_L\times A_L\to\QQ/\ZZ$, given by
$\beta_{A_L}(\bar x,\bar y)=\beta(x,y)\bmod\ZZ$ for any lifts" — the
exponent $N_b(L)$ that the construction determines is dropped from the
type, and the domain is a product.

**Preferred:** "the pairing of $A_L$ is the unique morphism
$\bar\beta_L\colon A_L^\sharp\otimes_{\mathbb Z}A_L^\sharp\to\tfrac1{N_b(L)}\mathbb Z/\mathbb Z$
with
$\bar\beta_L\circ(\pi_L\otimes\pi_L)=(\tfrac1{N_b(L)}\mathbb Z\twoheadrightarrow\tfrac1{N_b(L)}\mathbb Z/\mathbb Z)\circ\beta_{L^\#}$",
with the monomorphism
$\tfrac1{N_b(L)}\mathbb Z/\mathbb Z\hookrightarrow\mathbb Q/\mathbb Z$
written at the point where a $\mathbb Q/\mathbb Z$-valued source is
compared.

The same rule applies to a value computed in a proof: "vanishes in
$\QQ/2\ZZ$" for the quadratic discriminant form of a twisted
unimodular lattice reads the value in the coarse codomain, when the
definition of $q_L$ gives $\tfrac2{N_q(L)}\bZ/J_L$ and the vanishing
is a statement there.

Observed in `dzackgarza/research`,
`research/lattice-theory/special-lattices-and-transformations.md` at
`ab530c1dcc`, proof under "The discriminant form of a twisted
unimodular lattice".

**Banned:** "vanishes in $\QQ/2\ZZ$ precisely".

**Preferred:** "$q_L(x)=0$ in $\tfrac2{N_q(L)}\bZ/J_L$", the codomain
the definition of $q_L$ gives.

## `SYM-17`: A map is written in the direction its construction gives

### Yes/no example: a decomposition supplied by inclusions

**No:** "$L\isoto E_{10}\perp E_{10}^{\perp L}$" when only an
embedding of the unimodular lattice $E_{10}$ into $L$ has been given.

**Yes:** Let $i\colon E_{10}\hookrightarrow L$ be the given embedding
and $k\colon E_{10}^{\perp L}\hookrightarrow L$ the orthogonal complement.
Then
$$
\begin{aligned}
i\perp k\colon E_{10}\perp E_{10}^{\perp L}&\xrightarrow{\sim}L,\\
(x,y)&\longmapsto i(x)+k(y).
\end{aligned}
$$
Unimodularity gives, for each $z\in L$, a unique $x\in E_{10}$ with
$b_{E_{10}}(x,-)=b_L(z,i(-))$; then $z-i(x)\in E_{10}^{\perp L}$.
This proves surjectivity; nondegeneracy of $E_{10}$ proves injectivity.

**Test:** the displayed arrow is the map just constructed, and its
isomorphism claim has a reason. Source: live Zettlr annotation
`1c13aa15-84e0-4104-bb03-09511178c9ae`, quoted manuscript passage.

A decomposition of $L$ into sublattices $M_i$ is the map $\perp_iM_i\too
L$ induced by the inclusions; it is written in that direction and
decorated $\isoto$ once the proof shows it is an isomorphism (`NOT-2`).
The reverse arrow, $L\isoto\perp_iM_i$, asserts a projection onto each
factor, and the statement gives no formula for one. The test: write the
formula of the map on an element. If the formula exists only for the
inclusions, the arrow points from the sum. An arrow that has a formula
in neither direction is a relationship phrase written in symbols
(`EV-11`).

Observed in `dzackgarza/research` at `9cfdecf73d`:
`research/lattice-theory/special-lattices-and-transformations.md`,
proposition "Standard special lattice relations";
`research/lattice-theory/classification/two-elementary-lattices.md`,
theorem "Primitive isotropic vectors in a hyperbolic $2$-elementary
lattice".

**Banned:** "$L_{2d}\isoto\generators{-2d}\perp U^{\perp2}\perp
E_8^{\perp2}$"; "If $v$ is odd, $S\isoto
U\perp\qty{v^{\perp_S}}^{\mathrm{nd}}$".

**Preferred:** "$\generators{-2d}\perp U^{\perp2}\perp
E_8^{\perp2}\isoto L_{2d}$"; "$U\perp U^{\perp_S}\isoto S$ for the
hyperbolic plane $\iota\colon U\injects S$ through $v$, by
@prop:unimodular-splits, and $U^{\perp_S}\injects
v^{\perp_S}\twoheadrightarrow\qty{v^{\perp_S}}^{\mathrm{nd}}$ is an
isomorphism".
