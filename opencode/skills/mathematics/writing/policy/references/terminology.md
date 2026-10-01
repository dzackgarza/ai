# Terminology (`TERM-*`)

Use established mathematical terms in their standard meanings. Do not coin a
name for a notion that already has one. Do not import a term from another
field where the document owes a standard mathematical object. Do not overload a
standard word with a project-management or implementation meaning.

Terminology failures have three recurring forms:

- **Foreign-discipline substitution.** A technical term from another field is
  used where the document owes a standard mathematical object and definition.
- **Project coinage.** An undefined word is made to do mathematical work.
- **Colliding overload.** A standard word such as "kernel", "core", or
  "fiber" is reused with a project-management or implementation meaning.

The citation-backed recurring inventory lives in
`.agents/references/terminology-dictionary.md`. The following replacements
apply to the document:

| Term to avoid | Required mathematical statement |
| --- | --- |
| ontology | a specified functor, strict 2-functor, or pseudofunctor into $\mathbf{Cat}$; say *presentation of a category or 2-category by generators and relations* only after specifying those generators, relations, and closure operations |
| project lexicon | the defined categories, functors, predicates, and constructions, each with its type |
| corpus, when used for a generated object | the generated sub-2-category |
| graph or tree, when used for the whole object | a specified functor $I\to\mathbf{Cat}$, or a specified strict 2-functor or pseudofunctor $\mathcal I\to\mathbf{Cat}$; for a finite indexing poset $I$, say *tree-shaped* only when its undirected Hasse diagram is connected and acyclic |
| node | category or object, whichever is meant |
| edge | functor or morphism, whichever is meant |
| seed | generator |
| constructor | the named categorical construction or 2-functor |
| cut or axiom cut | a replete full subcategory defined by an object property, or a specified forgetful functor from structured objects |
| cut owner | the category whose objects satisfy the property, or the domain of the forgetful functor |
| cut instantiation | for $F\colon\mathcal D\to\mathcal C$ and a full subcategory $\mathcal C_P\hookrightarrow\mathcal C$, the full subcategory of $\mathcal D$ on objects $D$ satisfying $P(FD)$; or the pullback of $p\colon E\to B$ along a named map $f\colon X\to B$ |
| implication edge | the inclusion induced by a stated implication, with its proof |
| generation rule or square | the pullback of a replete full subcategory along a functor |
| minimal graph | an inclusion-minimal generating subdiagram relative to stated targets, permitted closure operations, and a specified equivalence relation on the class of presentations; uniqueness is a separate claim |
| Level-0 generic | the general construction and the parameter choice producing the instance |
| operation home | the domain, codomain, and type of the functor, natural transformation, object property, invariant, or operation |
| route | a composite or factorization of functors |
| preferred route or preferred functor | a distinguished functor or factorization with comparison maps, or an implementation dispatch policy confined to an implementation page |
| routing diamond | a commutative square, strictly or up to a specified natural isomorphism |
| tether or alignment | the specified equality, isomorphism, equivalence, natural isomorphism, or factorization |
| realization functor | the actual functor with source and target; use *forgetful functor* only when structure is forgotten and *realization* only for a defined realization construction |
| witness-level datum | the chosen basis, enumeration, presentation, section, or other auxiliary datum |
| free or torsion fiber | for a named functor $F\colon\mathcal D\to\mathcal C$, the full subcategory of $\mathcal D$ on objects mapped into the specified free or torsion full subcategory of $\mathcal C$; add finiteness only when it is a hypothesis |
| unified O | for an ordinary category $\mathcal C$, $\operatorname{Aut}\colon\mathcal C^{\simeq}\to\mathbf{Grp}$, with $O(X):=\operatorname{Aut}(X)$ as an instance |
| homsets-as-parents | the hom-bifunctor, the core groupoid, or $\operatorname{Iso}_{\mathcal C}(X,Y)$, which is a bitorsor under $\operatorname{Aut}(Y)$ on the left and $\operatorname{Aut}(X)$ on the right when $X\cong Y$ |
| residue | the missing definition or unformalized theorem |
| gap row | a documented missing formalization; this already has a precise implementation meaning |
| Synthetic layer | a provisional axiomatization, with its axioms and conjectures declared |
| base of an axiom | the property or structure and the category whose objects satisfy or support it; for a classifying fibration, its domain, codomain, and universal property |
| transport of an axiom | the pullback of the specified family along the named functor, when that family and its universal property have been defined |
| owned at or ownership, when used mathematically | the property of objects of the named category, or a chosen structured object in the fiber of a specified forgetful functor |

## `TERM-1`: Retired substitutions

These terms survived one round of editing and are withdrawn.

**Banned:** "multi-sorted signature"; "semantic interpretation"; "executable
interpretation"; Mathlib identifiers used as prose nouns.

**Preferred:** state the actual categories, functors, predicates, and
constructions. Name the mathematical functor or the implementation operation
actually meant. Restrict Mathlib identifiers to code-formatted implementation
anchors.

## `TERM-2`: "Homomorphism" for a morphism or map

Modern $\infty$-categorical and spectral literature writes "morphism" or
"map" in the relevant $\infty$-category — a morphism in $\mathbf{CAlg}$,
a map of $\mathbb{E}_\infty$-ring spectra, a morphism of commutative
algebra objects in $\mathbf{Sp}$ — not "homomorphism of commutative
rings." "Homomorphism" is classical universal-algebra language for a
set-map preserving operations, tied to the truncated story where a ring is
a set with addition and multiplication. In the document's ontology where
rings are $\mathbb{E}_\infty$-ring spectra (DEF-13) and maps are maps of
spectra with $\mathbb{E}_\infty$-structure, the standard word is
"morphism" or "map."

**Banned:** "Let $\varphi\colon A\to B$ be a homomorphism of commutative
rings."

**Preferred:** "Let $\varphi\colon A\to B$ be a morphism of commutative
rings" (in a genuinely classical passage where $A = \pi_0 HA$) or "let
$\varphi\colon A\to B$ be a map of $\mathbb{E}_\infty$-ring spectra" / "a
morphism in $\mathbf{CAlg}$." Use "morphism" or "map" with the
$\infty$-category stated; reserve "homomorphism" for no passage in this
book.

## `TERM-3`: "Value module" for codomain or target

"Value module" is a coinage for the codomain or target of a bilinear
form. The standard terms are codomain, target, or value object. Do not
coin a synonym for a standard categorical term.

**Banned:** "whose value module is $B\otimes_A W$."

**Preferred:** "with codomain $B\otimes_A W$" or "with target
$B\otimes_A W$."

## `TERM-4`: "Torsion theory" with no referent

"Torsion theory" is not a mathematical object. There are hereditary
torsion pairs, $t$-structures, and localizing subcategories with torsion
functors — each with a definition. A passage that writes "a torsion
theory has been specified" invents a term with no definition, no
citation, and no construction, and uses it as if it were standard.
Name the precise structure.

**Banned:** "Over a general ring, a torsion subcategory is used only
after a torsion theory has been specified."

**Preferred:** "Over a general $\mathbb{E}_1$-ring spectrum $R$, a
torsion subcategory is used only after a hereditary torsion pair
$(\mathcal{T},\mathcal{F})$ on $\mathbf{LMod}_R$ (see @def-torsion-pair)
has been specified" or "after a $t$-structure
$(\mathbf{LMod}_R^{\ge0},\mathbf{LMod}_R^{\le0})$ has been specified."

## `TERM-5`: Colloquial "lands", "property", "structure" without a precise definition

Colloquial terms "lands (in)", "property", "structure", "stuff" are used
as if their meaning were obvious — "a theorem that $F$ lands in $D_P$ is
a factorization," "being torsion-free is a property," "being a torsor is
structure" — without ever giving the precise categorical definition. In
the document each has a precise meaning: "$F$ lands in $D_P$" means a
factorization $F\simeq i\circ\bar F$ through the replete full inclusion
$i\colon D_P\hookrightarrow D$ (with $\bar F$ the corestriction and
$\alpha\colon F\simeq i\circ\bar F$ the specified equivalence);
"property" means the forgetful functor $U\colon\mathcal{S}\to\mathcal{C}$
is fully faithful, "structure" means $U$ is faithful, "stuff" means
$U$ is arbitrary (STR-1), each with its fiber condition. Do not use the
colloquial term in a definition, theorem, or title before the precise
term has been fenced and defined.

**Banned:** "A theorem that $F\colon\mathcal{C}\to\mathcal{D}$ lands in a
replete full subcategory $i\colon D_P\hookrightarrow D$ is a factorization
$F=i\circ\bar F$" — uses "lands in" as if defined, with no fenced
definition of "lands in" as factorization.

**Preferred:** first define: "::: {#def-lands} ## Lands in — A functor
$F\colon\mathcal{C}\to\mathcal{D}$ **lands in** a replete full
subcategory $i\colon D_P\hookrightarrow\mathcal{D}$ if there exists a
functor $\bar F\colon\mathcal{C}\to D_P$ and a specified natural
equivalence $\alpha\colon F\simeq i\circ\bar F$. The triple
$(\bar F,\alpha)$ is a factorization of $F$ through $D_P$. :::" Then
later: "Proposition: The functor $F$ lands in $D_P$ via $\bar F$ with
$\alpha$."

## `TERM-6`: "Embedding" for "monomorphism" without definition or identification

"Monomorphism" and "embedding" are used interchangeably mid-passage —
"some monomorphism $A\to B$ exists" then "a construction that uses an
embedding names a particular monomorphism" — without ever defining
either term or stating the identification. In the document a monomorphism is
a $(-1)$-truncated map ($f$ is mono if …), an embedding is a fully
faithful functor (or, for spaces, an embedding as a $(-1)$-truncated
map with extra condition) — each with its fenced definition. Do not
switch terms without defining the identification.

**Banned:** "some monomorphism $A\to B$ exists … a construction that
uses an embedding names a particular monomorphism" — switches from
"monomorphism" to "embedding" with no definition of either and no link
between them.

**Preferred:** choose one term and define it, or define both and state
the identification: "A **monomorphism** ($f\colon A\rightarrowtail B$)
is … (\ref{def-mono}). An **embedding** is … (\ref{def-embedding}). In
$\mathbf{Sets}$, every monomorphism is an embedding; in general …" Link
each use to its defining occurrence (XREF-5).

## `TERM-7`: Colloquial term without definition, and confabulated term that hides necessary details

A term is used as if its meaning were obvious when it is not defined
anywhere in the document and is not obvious to an undergraduate. Colloquial
terms — "apex" for the vertex of a cone, "carries," "transports,"
"identifies conventions," "value module" — and confabulated terms that
sound technical but have no referent — "torsion theory," "apex" as a
standalone noun for a terminal cone — hide necessary details. "Apex"
alone names no cone and no universal property; its standard counterpart
is the (terminal) cone $(P\to X, P\to Z)$ over $X\to Y\leftarrow Z$ that
is terminal among cones, introduced once in the definition of pullbacks.
Every technical term beyond what an undergraduate would know is fenced
and defined before use; a colloquial term is not used in its place.

**Banned:** "the fiber … is the apex of the cartesian square";
"objects that carry both structures" (EV-2); "the discriminant package"
(EV-3); "a torsion theory has been specified" (TERM-4).

**Preferred:** "the fiber is the pullback $X\times_Y 1$ with its terminal
cone $(X\times_Y 1\to X, X\times_Y 1\to1)$"; "a structure on $X$ is a
chosen object in the fiber over $X$ of $U\colon\mathcal{S}\to\mathcal{C}$";
"a hereditary torsion pair $(\mathcal{T},\mathcal{F})$ has been
specified."

## `TERM-8`: Colloquial "cartesian square" and technical term not defined in the document

"Cartesian square" is colloquial for a pullback square and, when used
without definition, also hides a theorem: when a square's projection is
a (co)cartesian fibration and the square is a pullback in
$\mathbf{Cat}_\infty$, the projection is a (co)cartesian fibration. More
generally, any technical term beyond what an undergraduate would know —
"pullback," "cartesian fibration," "torsion pair," "annihilator," "basis"
— must be fenced and defined in the document before use, not used as if
its meaning were obvious or as if the reader will supply the definition
from prior knowledge. Colloquial and undefined technical terms are not
interchangeable with the precise defined terms.

**Banned:** "the apex of the cartesian square"; "a torsion theory has
been specified" (TERM-4); "$\mathbf{Sh}_\Sigma$ for a diagram category"
(MA-3) without definition.

**Preferred:** "the pullback square exhibiting $X\times_Y 1$" (with
`{#def-pullback}` defined) or "the square exhibiting the pullback."
Reserve "cartesian fibration" for the fibration property and prove when a
pullback square has that property. Define every non-undergraduate
technical term in a fenced block before its first use.

## `TERM-9`: "Value module" with no definition, fixing a single $W$

"Value module" is not a standard term with a defined referent and, as
used in "the value module of the forms below," asserts a single $W$
fixed for a section where the mathematics requires $W$ varying over
$\mathbf{LMod}_R$ (PR-37). Forms are $W$-valued for varying $W$; the
codomain is part of the datum $b\colon M\otimes_R M\to W$, not a global
choice.

**Banned:** "the value module $W$ of the forms below"; "fix the value
module $W$."

**Preferred:** "let $W\in\mathbf{LMod}_R$ and let $b\colon M\otimes_R
M\to W$ be a $W$-valued bilinear form" (PR-37); or "a bilinear form
valued in $W$" with $W$ quantified in the definition. Do not reify "the
value module" as a once-fixed object.

## `TERM-10`: "Presheaf" overloaded for $\mathbf{Mod}_R^{\mathrm{op}}\to\mathbf{Mod}_R$ / "$R$-module of maps" functor

A presheaf on $\mathcal C$ is a functor $\mathcal C^{\mathrm{op}}\to
\mathbf{Set}$ (stably $\mathcal C^{\mathrm{op}}\to\mathcal S$). An
$R$-module-valued functor $\mathcal C^{\mathrm{op}}\to\mathbf{Mod}_R$
is an $\mathbf{Mod}_R$-valued presheaf, or an $\mathbf{Mod}_R$-enriched
presheaf when the enrichment from {#thm-mod-closed} is meant — not a
"presheaf" unqualified. Overloading the generic name hides which
enrichment and which $\operatorname{Bil}$ is named (the $R$-module
$\operatorname{Bil}_{R,W}(M)$ vs. the functor
$M\mapsto\operatorname{Bil}_{R,W}(M)$) and adds no content beyond
"functor," since
$\operatorname{Bil}_{R,W}(M)=\operatorname{Hom}_R(M\otimes_R M,W)$ is
already functorial in $M$ by the Hom — $f\mapsto (f\otimes_R f)^*$.

Concrete standards:

* **Presheaf:** $\operatorname{PSh}(\mathcal C):=
  \operatorname{Fun}(\mathcal C^{\mathrm{op}},\mathbf{Set})$, stably
  $\operatorname{Fun}(\mathcal C^{\mathrm{op}},\mathcal S)$ [@Stacks-00VG;
  Lurie HTT 0.6.5].

* **$R$-module-valued:** a functor $\mathbf{Mod}_R^{\mathrm{op}}\to
  \mathbf{Mod}_R$ is an $\mathbf{Mod}_R$-valued presheaf on
  $\mathbf{Mod}_R$, equivalently an $\mathbf{Mod}_R$-enriched presheaf via
  the self-enrichment {#thm-mod-closed}. Name the enrichment when it
  matters.

* **At the point of use:** no "defines a presheaf" to name functoriality
  that is already the Hom's.

**Banned:** "Pullback along $f\colon M\to N$ sends $b$ to
$f^*b(x,y)=b(fx,fy)$, and defines a presheaf
$\operatorname{Bil}_{R,W}\colon(R\text{-}\mathbf{Mod})^{\mathrm{op}}\to
R\text{-}\mathbf{Mod}$."

**Preferred:** "$\operatorname{Bil}_{R,W}(M):=
\operatorname{Hom}_R(M\otimes_R M,W)$ as $R$-module, functorial in $M$
by $(f\colon M\to N)\mapsto (f\otimes_R f)^*\colon
\operatorname{Hom}_R(N\otimes_R N,W)\to\operatorname{Hom}_R(M\otimes_R
M,W)$, $f^*b(x,y)=b(fx,fy)$ as the element formula for $(f\otimes_R f)^*b$."
If the word is needed, "as an $\mathbf{Mod}_R$-valued presheaf on
$\mathbf{Mod}_R$ (resp. $\mathbf{Mod}_R$-enriched presheaf via
{#thm-mod-closed})"; otherwise just "as a functor
$\mathbf{Mod}_R^{\mathrm{op}}\to\mathbf{Mod}_R$."

## `TERM-11`: Bare "maps $M\to W$" with no category — egregiously imprecise, and wrong for quadratics

"Map $M\to W$" unqualified in $\mathbf{Mod}_R$ means morphism in
$\mathbf{Mod}_R$ — i.e. $R$-linear. A quadratic $q\colon M\to W$ is
*not* $R$-linear (and not a morphism in $\mathbf{Mod}_R$); it is a
function on underlying sets for the forgetful
$U\colon\mathbf{Mod}_R\to\mathbf{Set}$ satisfying $q(rx)=r^2q(x)$ and
$R$-bilinearity of the polarization
$b_q(x,y):=q(x+y)-q(x)-q(y)$. "Maps $M\to W$" without "of sets" / "of
underlying sets" / "in $\mathbf{Set}$ after $U$" therefore names the
wrong hom, hides which forgetful is meant (Set vs. $\mathcal S$ vs.
anima stably matters), and leaves no object to enrich — the later "as
$R$-module, under pointwise operations" then has no category to attach
to.

This is the general form behind PR-37/PR-38: a set-level datum
described as if it were a morphism in the ambient $R$-linear category,
mislocating structure and forcing filler.

Concrete standards — name the category, and use the classifier so no
"maps $M\to W$" is needed:

* **Underlying sets:** let $U\colon\mathbf{Mod}_R\to\mathbf{Set}$ be the
  forgetful. A quadratic function is a map $U(M)\to U(W)$ in
  $\mathbf{Set}$ with those two conditions. Stably $U\colon\mathbf{LMod}_R
  \to\mathcal S$.

* **Classifier (so no "maps $M\to W$" to describe):** fix the divided
  power (Whitehead) classifier $\Gamma^2_R$ once, fenced, with its
  universal property. Then
  $\operatorname{Quad}_{R,W}(M):=\operatorname{Hom}_R(\Gamma^2_R(M),W)$
  as $R$-module (stably
  $\mathbf{RHom}_R(\mathbf{\Gamma}^2_R(M),W)$). Its underlying set is the
  set of functions $U(M)\to U(W)$ satisfying the quadratic condition;
  its $R$-module structure is the self-enrichment {#thm-mod-closed} on
  that Hom, not "pointwise via $W$" on a set of maps whose category was
  never named. Similarly $\operatorname{Sym}_{R,W}(M):=
  \operatorname{Hom}_R(\operatorname{Sym}^2_R(M),W)$ for symmetric,
  $\operatorname{Bil}_{R,W}(M)=\operatorname{Hom}_R(M\otimes_R M,W)$ as
  above — each Hom classifies the flavour, no element-level "maps
  $M\times M\to W$ / $M\to W$" to re-spell.

**Banned:** "of maps $q\colon M\to W$ for which $q(rx)=r^2q(x)$ and …"
with no "of sets / of underlying sets / in $\mathbf{Set}$ after $U$";
"Let $\operatorname{Quad}_{R,W}(M)$ be the $R$-module, under pointwise
operations, of maps $M\to W$ …"

**Preferred:** "Let $U\colon\mathbf{Mod}_R\to\mathbf{Set}$ be the
forgetful. A **quadratic form** on $M$ valued in $W$ is a function
$q\colon U(M)\to U(W)$ with $q(rx)=r^2q(x)$ and $b_q(x,y)$ $R$-bilinear"
— or, classifier-first and with no "maps $M\to W$": "Put
$\operatorname{Quad}_{R,W}(M):=\operatorname{Hom}_R(\Gamma^2_R(M),W)$ as
$R$-module. Its elements are the functions $U(M)\to U(W)$ with that
condition." Name $\mathbf{Set}$ / $U$ when the map is not $R$-linear;
for bilinear/symmetric/quadratic never write bare "maps $M\to W$" or
"$M\times M\to W$" once the classifier ($\otimes$, $\operatorname{Sym}^2$,
$\Gamma^2$) is defined.

## `TERM-12`: "Quadratic refinements" with no defined refinement relation — fossilized adjective with no map

"Refinement" is plausible because the polar
$b_q(x,y):=q(x+y)-q(x)-q(y)$ does give a map
$\gamma^*\colon\operatorname{Quad}_{R,W}(M)\to\operatorname{Bil}_{R,W}(M)$,
$q\mapsto b_q$, so a $q$ with $b_q=b$ can be called a quadratic refinement
of $b$. That meaning requires the named $R$-linear
$\gamma^*\colon\operatorname{Hom}_R(\Gamma^2_R(M),W)\to\operatorname{Hom}_R(M\otimes_RM,W)$
(induced by $\Gamma^2_R(M)\xrightarrow{\gamma}\operatorname{Sym}^2_R(M)\to M\otimes_R M$)
to be defined, with its (non-)injectivity/surjectivity and fiber discussed —
is a refinement a section, a lift, a fiber over $b$? No $\gamma^*$ was named
and no $\ker(\gamma^*)/\operatorname{coker}(\gamma^*)$ was stated, so there
is no sense, even informally, in which either direction could be called a
refinement, and "quadratic refinements" is just "quadratics" preceded by a
math-adjacent word with no referent. It is also nonstandard in the
direction used here: the associated object is the bilinear *polar* $b_q$
of $q$, not $q$ "refining" $b$ without the map.

Concrete standard — name $\gamma^*$ and its fiber, then "refinement" is
the fiber:

"::: {#def-quad-polar} **Definition.** Put
$\operatorname{Quad}_{R,W}(M):=\operatorname{Hom}_R(\Gamma^2_R(M),W)$ and
$\operatorname{Bil}_{R,W}(M):=\operatorname{Hom}_R(M\otimes_RM,W)$ as
$R$-modules. The $R$-linear
$\gamma^*\colon\operatorname{Quad}_{R,W}(M)\to\operatorname{Bil}_{R,W}(M)$
sends $q$ to its polar $b_q(x,y)=q(x+y)-q(x)-q(y)$. A **quadratic
refinement** of $b\in\operatorname{Bil}_{R,W}(M)$ is a $q$ with
$\gamma^*(q)=b$ — i.e. a point in the fiber over $b$. :::"

**Banned:** "quadratic refinements retain …" with no $\gamma^*$,
no $b$, no fiber.

**Preferred:** "the fiber of $\gamma^*\colon\operatorname{Quad}_{R,W}(M)\to
\operatorname{Bil}_{R,W}(M)$ over $b$" / "the set of $q$ with $b_q=b$"
with $\gamma^*$ named; or just "$q\in\operatorname{Quad}_{R,W}(M)$."

## `TERM-13`: "Discriminant setting" is not a mathematical object — the object is the category of torsion bilinear/quadratic modules

There is no mathematical object called a "setting." What is meant is a
*category* — torsion $R$-modules with nondegenerate $W$-valued forms,
e.g. finite $\mathcal O_X$-modules, $D_L:=L^\vee/L$ with
$\mathbb Q/\mathbb Z$- or $\mathbb Q/2\mathbb Z$-valued form — which
has not been defined. Sign-posting it here in a sentence about $2W=W$
also inverts dependency order and violates theory-of-mind: only
$\operatorname{Bil}_{R,W}(M)$ for general $M\in\mathbf{Mod}_R$ has been
defined; lattices, duals $L^\vee:=\operatorname{Hom}_R(L,R)$, finite
quotients $D_L$, and their induced torsion forms are later, so the
reader does not yet know what "discriminant" means. A general
$\operatorname{Bil}/\operatorname{Quad}$ cannot be motivated by a
specialization that has not been introduced.

Concrete standards:

* **Object, not setting:**
  "::: {#def-disc-cat} **Definition.** Let $\mathbf{TorBil}_{R,W}$ (resp.
  $\mathbf{TorQuad}_{R,W}$) be the category whose objects are pairs
  $(T,\bar b)$ with $T\in\mathbf{Mod}_R$ torsion of finite length and
  $\bar b\colon T\otimes_R T\to W/\operatorname{Val}$ nondegenerate
  $W$-valued torsion bilinear (resp. quadratic) form. :::"

* **Discriminant as object of that category, defined later:**
  "::: {#def-discriminant} For a lattice $L$ with $b\colon L\otimes L\to R$
  nondegenerate, put $D_L:=L^\vee/L$ and let $\bar b$ / $\bar q\colon
  D_L\to\mathbb Q/\mathbb Z$ ($\to\mathbb Q/2\mathbb Z$ for quadratic) be
  the induced torsion form. :::"

**Banned:** "in the discriminant setting."

**Preferred:** name the category
$\mathbf{TorBil}_{R,W}$ / $\mathbf{TorQuad}_{R,W}$ when it is defined,
and the object $(D_L,\bar q)$ when $L$ is defined; do not sign-post
discriminants in the general $\operatorname{Bil}/\operatorname{Quad}$
section before lattices and $L^\vee/L$ exist.

## `TERM-14`: "Index" always means $p-q$, "signature" always means the full tuple $(p,q)$ or $(p,q,r)$ — not vice versa

Competing conventions abound — manifold theory / $L$-theory
($\sigma(M)=p-q$ called "signature"), arithmetic lattices (often
"signature $(p,q)$" called "index"), Sterk-style indefinite lattices
("signature $(p,q)$" vs. "$2$-elementary $(r,a,\delta)$"), etc. —
but in the document **index** always means the integer

$$ \operatorname{ind}(b):=p-q\in\mathbb Z, $$

and **signature** always means the full tuple

$$ \operatorname{sig}(b):=(p,q)\quad\text{or}\quad(p,q,r)\in\mathbb Z^2\text{ resp. }\mathbb Z^3 $$

(with $r:=\dim\operatorname{rad}$, $p+q+r=n$ when defined). This abuse
is not pedantry: the Hodge index theorem computes $p-q$ and *deduces*
$(p,q)$ (since $p+q=n-r$ is known), so calling $p-q$ the *index* is
philosophically correct — it is the Fredholm / operator-theoretic index
$\operatorname{ind}= \dim\ker_+ - \dim\ker_-$ (number of positive minus
negative eigenvalues of $G_e(b)$), i.e. the $L^2$-index that Hodge
computes, while $(p,q)$ is the more refined *signature* that follows
from it. Manifold-theoretic "$\sigma(M)=p-q$ is the signature"
conflates the two; here $\sigma(M)=p-q$ is the index and $(p,q)$ is the
signature.

**Banned:** "the signature $p-q$" / "the index $(p,q)$" / "signature
$(p,q)$ called the index."

**Preferred:** "The form $b$ has **signature** $(p,q)$ (resp.
$(p,q,r)$) and **index** $p-q$." / "Hodge computes the index
$p-q$ and hence the signature $(p,q)$ since $p+q=n-r$."

## `TERM-15`: Module and algebra bilinear forms

A *module bilinear form* is an element of
$\operatorname{Hom}_{R\text{-}\mathbf{Mod}}(M\otimes_R M,R)$
(@def:module-bilinear-form). An *algebra bilinear form* is an element of
$\operatorname{Hom}_{R\text{-}\mathbf{Alg}}(A\otimes_R A,R)$ with the tensor
product of $R$-algebras (@def:algebra-bilinear-form). An associative pairing
on a unital algebra is a condition on a module bilinear form on $U(A)$,
equivalently a trace pairing $\varepsilon\circ\mu$.
