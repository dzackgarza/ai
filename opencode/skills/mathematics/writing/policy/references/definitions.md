# Definitions (`DEF-*`)


## `DEF-1`: One defining occurrence

Each mathematical notion has one defining occurrence in the document. Later
chapters cite it. They do not restate it, shadow it with a synonym, or write a
second local definition. When the document records a source's variant of a
definition, it states the variant's relation to the definition the document
uses.

**Banned:** defining "scheme" in an introduction, restating it in a remark,
and using both versions as if they had equal authority.

**Preferred:** one definition block, then a link to it and a statement of
consequences where they are used.

Multiple defining occurrences drift apart and make it unclear which
hypotheses govern later claims. One defining occurrence gives the term a
stable referent.

## `DEF-2`: Read the document before writing a dependent passage

Read the document's defining occurrence and its prerequisites before writing a
dependent passage. A definition reconstructed from training or an external
source is inadmissible even when it resembles a standard definition.

**Banned:** calling a space compact in the sense of sequential compactness
in a passage whose linked definition defines compactness by open covers.

**Preferred:** read the document's definition of compactness, link it, and
use the notion it defines.

## `DEF-3`: Correct at the defining occurrence

If the document's definition conflicts with the literature, correct it at the
defining occurrence and repair its dependents. Do not shadow it locally.

## `DEF-4`: Statements are numbered blocks

A definition, theorem, proposition, lemma, corollary, example, or remark is a
numbered block with a stable identifier, written in the medium's block
syntax. The identifier lets every later use link the block (`XREF-1`). The
house conventions of each document fix the syntax and the list of block
classes. Declare a block class in the house conventions before using it.

## `DEF-5`: A theorem presented as a definition

A construction is defined by a property or identification that is in fact
a theorem — a result that holds under hypotheses, or a consequence of a
deeper construction. The reader receives the theorem as the definition and
has no access to the construction it replaces. Present the construction;
state the theorem that identifies the construction with the simpler
description; do not substitute the theorem for the definition.

**Banned:** "$K_0^{\otimes}(S)$ is the group completion of the monoid of
isomorphism classes." The group completion of $\pi_0(S^\simeq)$ is
$\pi_0 K(S)$, but that identification is a theorem (the group completion
theorem), not the definition. The definition is $K_0(S) = \pi_0 K(S)$,
where $K(S)$ is the $K$-theory spectrum.

**Preferred:** "Let $K(S)$ denote the algebraic $K$-theory spectrum of
the symmetric monoidal category $S$. Define $K_0(S) = \pi_0 K(S)$. By the
group completion theorem, $K_0(S)$ is the group completion of
$\pi_0(S^\simeq)$ under the induced monoid operation." State the
construction, then state the theorem that identifies it with the simpler
description.

## `DEF-6`: A definition that suppresses the governing structure

A construction depends on a richer structure than the definition reveals.
The definition names only the downstream consequence and omits the
structure that governs it, so the reader has no access to the rest of
what that structure provides. State the governing structure; derive the
defined object as a component or consequence of it.

**Banned:** defining $K_0(S)$ as the group completion of a monoid
without introducing the $K$-theory spectrum $K(S)$. The reader has no
access to $K_n(S)$, the higher $K$-groups, or the spectrum-level
structure, because the spectrum was never stated.

**Preferred:** introduce the spectrum $K(S)$, define $K_0(S) = \pi_0
K(S)$, and then identify $\pi_0 K(S)$ with the group completion. The
spectrum governs all $K_n$; $K_0$ is one component.

## `DEF-7`: Nonstandard notation that marks a dependency the standard notation already encodes

A superscript or subscript is added to a standard symbol to mark a
dependency that the standard notation already encodes through its
arguments. The decoration is a project coinage that distinguishes
instances the standard notation does not distinguish, because the
standard notation already parameterizes by the input.

**Banned:** "$K_0^{\otimes}(S)$" — the $\otimes$ superscript marks the
dependency on the monoidal structure, but $K_0(S)$ already takes the
symmetric monoidal category $S$ (with its tensor) as input.

**Preferred:** use the standard notation. If a distinction is needed
between $K$-theories of the same category with different monoidal
structures, name the monoidal structure in the argument:
$K_0(S,\otimes)$, or use distinct symbols for the distinct monoidal
categories.

## `DEF-8`: A definition anchored in a superseded framework

A definition or construction is presented using a framework the field has
replaced, when a modern framework exists and is standard. The superseded
framework is not wrong — it is a shadow or special case of the modern one
— but presenting it as the definition teaches the reader a picture that the
field has moved past. This is especially acute in category theory, where
the modern framework is $\infty$-category theory, derived and spectral
algebraic geometry, and the constructions developed in the last 10-20
years. A construction whose modern home is an $\infty$-categorical or
spectral framework — $K$-theory, derived functors, cohomology, moduli,
intersections, traces — is presented in its classical, pre-derived,
pre-spectral form, and the reader has no access to the generality and
structure the modern framework provides. Anchor definitions in the current
understanding of the subject; present the classical formulation as a
special case or theorem if it is still useful.

**Banned:** defining $K_0(S)$ as the group completion of
$\pi_0(S^\simeq)$ without mentioning the $K$-theory spectrum. $K$ is a
functor from a subcategory of $\mathbf{Cat}$ to spectra; $K_0$ is $\pi_0$
of that functor. The group completion of the monoid is an even more
classical construction that the spectrum recovers. Presenting the
group completion as the definition is anchoring in a framework two stages
out of date.

**Preferred:** define $K$ as a functor to spectra, $K_0(S) = \pi_0 K(S)$,
and state the group completion theorem as a theorem. The
$S_\bullet$-construction [@Wal85] is the standard construction;
Zakharevich [@Zak17] constructs $K(\mathcal{V}_k)$ as a spectrum whose
$\pi_0$ is the Grothendieck ring of varieties, with higher homotopy
groups carrying geometric information; Campbell [@Cam17] produces
$K(\mathbf{Var}_{/k})$ via an $S_\bullet$-type construction with
liftings of motivic measures to the spectrum. A reader trained on the
modern definition can access the generality the functor to spectra
provides; a reader trained on the superseded one cannot.

## `DEF-9`: Classical structure presented where the modern framework gives a richer object

A construction carries additional structure in the modern framework that
the classical presentation suppresses entirely. The classical version
describes a shadow — $\pi_0$ of a richer object — and the reader has no
access to the structure the modern framework provides at higher levels.
Present the richer object; derive the classical structure as a
consequence.

**Banned:** "the group completion inherits a multiplication from it …
$K_0(R)$ is a commutative ring with unit $[R]$." A second symmetric
monoidal product distributing over the first makes $K(S)$ an
$\mathbb{E}_\infty$-ring spectrum, not just $K_0$ a commutative ring.
The ring structure on $K_0$ is $\pi_0$ of the ring spectrum; the higher
$K$-groups are modules over $K_0$; the unit spectrum's $\pi_0$ is $[R]$.
All of this is invisible.

**Preferred:** "A second symmetric monoidal product on $S$ that
distributes over the first makes $K(S)$ an $\mathbb{E}_\infty$-ring
spectrum; in particular $K_0(S)$ is a commutative ring and $K_n(S)$ are
modules over it." The ring spectrum is constructed from the multiplicative
monoidal structure via an $\mathbb{E}_\infty$-operad action
[@EKMM07, @HA]; for $\operatorname{Proj}(R)$ with $\oplus$ and
$\otimes$, $K(R)$ is an $\mathbb{E}_\infty$-ring spectrum whose $\pi_0$
is the classical $K_0(R)$ [@Wei13, §II.2]. State the ring spectrum;
derive the ring on $\pi_0$ from it.

## `DEF-10`: Working truncated while the modern theory is derived and spectral

Modern theory is derived and spectral by default: the objects are
$\infty$-categories, derived stacks, $\mathbb{E}_\infty$-ring spectra, and
module spectra, and the classical objects — ordinary categories, schemes,
commutative rings, abelian groups — are truncations. A passage that
discusses a modern construction entirely in classical terms — rings
instead of $\mathbb{E}_\infty$-ring spectra, abelian groups instead of
spectra, ordinary categories instead of $\infty$-categories — works
truncated without saying so, and the reader cannot recover the derived
structure. Work in the derived and $\infty$-categorical framework
throughout; state classical objects as truncations when the construction
truly requires them, and make the extraction explicit.

**Banned:** "Let $R$ be a commutative ring" — used where $HR$ (the
Eilenberg–Mac Lane $\mathbb{E}_\infty$-ring spectrum of $R$) is the
governing object, without saying whether $R$ is $\pi_0 HR$ or an
$\mathbb{E}_\infty$-ring. "Let $G$ be a group" — used where $BG$ (its
classifying $\infty$-groupoid) is the governing object.

**Preferred:** "Let $R$ be an $\mathbb{E}_\infty$-ring spectrum; write
$\pi_0 R$ for its underlying classical ring when the classical
construction is needed: $R = H(\pi_0 R)$ when $R$ is discrete." State the
derived object; extract the classical shadow explicitly when it is the
object under study, e.g. in the statement of a classical theorem.

## `DEF-11`: Truncation extraction named explicitly

Passing from a derived or spectral object to its classical shadow is a
specific construction, not a silent identification: $\pi_0 HR$ extracts the
classical ring $R$ from the Eilenberg–Mac Lane $\mathbb{E}_\infty$-ring
spectrum; $\Omega BG$ recovers the group $G$ from its classifying
$\infty$-groupoid; the underlying abelian group of an
$\mathbb{E}_\infty$-module spectrum is a further forgetful image. Each
extraction names the functor that performs it. A passage that uses the
classical object without naming the extraction hides the truncation.

**Banned:** "a commutative ring $R$ and its modules" — used where
$\mathbb{E}_\infty$-modules over $HR$ are the governing objects, with no
statement of the truncation.

**Preferred:** "an $\mathbb{E}_\infty$-ring spectrum $R$ and its module
spectra; its $\pi_0$ is the classical commutative ring, and the
heart of the t-structure recovers the classical module category." Name
the derived objects; state the truncation that yields the classical
ones. Do not belabour the extraction at every mention, but make it
explicit where the document first passes from derived to classical.

## `DEF-12`: Level of abstraction calibrated to modern courses and literature

The standard for how much $\infty$-categorical and spectral machinery the
book uses is not the classical textbook from which the author learned
the material, but the level at which the subject is currently taught and
practiced: undergraduate and graduate courses at Harvard, MIT, and
Princeton, and the work of Lurie, Scholze, Gaitsgory, and Haynes Miller.
When in doubt about whether a derived or $\infty$-categorical
presentation is warranted, survey how the notion is presented in those
courses and in that literature, and match their level. A construction
that Lurie's lectures present as a functor between $\infty$-categories
is not presented here as a functor between ordinary categories; a notion
that Scholze's course formulates via derived stacks is not formulated
here via classical schemes. This does not mean every detail is
re-derived — a construction is stated at the modern level, and classical
consequences are extracted — but it means the document does not implicitly
assume everything is truncated everywhere.

**Banned:** presenting a construction at the classical level because the
classical case is "simpler" or "more familiar", when the field's standard
presentation is derived or $\infty$-categorical.

**Preferred:** survey the modern courses and literature (e.g. Lurie's
*Higher Topos Theory* [@Lur09HTT] and *Higher Algebra* [@HA], Gaitsgory–
Rozenblyum, Scholze's courses and the Berkeley lectures, Haynes Miller's
spectral sequences courses) and match their level of abstraction and
presentation.

## `DEF-13`: Everything implicitly or explicitly derived and homotopical

The document works in the derived and homotopical ontology by default. Every
classical term has a derived analogue that is the default meaning; the
classical object is a truncation, and a passage that means the derived
object does not use the classical name. This applies uniformly:

| Classical name | Default meaning in the document |
| --- | --- |
| ring | $\mathbb{E}_\infty$-ring spectrum |
| module | module spectrum |
| category | $\infty$-category |
| functor | total derived functor (e.g. derived tensor product is $\otimes^L$) |
| stack | derived stack |
| space | homotopy type, anima, or $\infty$-topos; write $\mathbf{Top}$ when actual topological spaces are meant |
| topology | Grothendieck topology |
| group | $\infty$-group or loop space; write $\Omega BG$ to recover a discrete group |

A passage that means the derived object does not use the classical name
and rely on the reader to supply the derived upgrade. A passage that
means the classical truncation states it as a truncation — $\pi_0 HR$
for the classical ring $R$, $\tau_{\leq 0}\mathcal{C}$ for the ordinary
category, the heart of the t-structure for classical modules — and makes
the extraction explicit. Do not belabour every derived detail at every
mention, but do not implicitly assume everything is truncated everywhere.

**Banned:** "Let $R$ be a commutative ring and $M$ an $R$-module …
consider the tensor product $M\otimes_R N$" — used where $R$ is an
$\mathbb{E}_\infty$-ring spectrum, $M$ and $N$ are module spectra, and
$\otimes$ is the derived tensor product.

**Preferred:** "Let $R$ be an $\mathbb{E}_\infty$-ring spectrum and $M$
an $R$-module spectrum … consider the derived tensor product
$M\otimes_R^L N$; its $\pi_0$ recovers the classical tensor product of
$\pi_0 R$-modules." Or, in a genuinely classical passage: "Let
$R = \pi_0 HR$ be a classical commutative ring" — state the truncation.

## `DEF-14`: "General ring" without specifying the $\mathbb{E}_n$ level

"Ring" in the document is an $\mathbb{E}_\infty$-ring spectrum by default
(DEF-13). For an $\mathbb{E}_\infty$-ring spectrum $R$,
$\mathbf{LMod}_R\simeq\mathbf{RMod}_R$ canonically via the symmetry. For a
general associative ($\mathbb{E}_1$) ring spectrum the two
$\infty$-categories $\mathbf{LMod}_R$ and $\mathbf{RMod}_R$ (equivalently
$\mathbf{LMod}_R$ and $\mathbf{RMod}_{R^{\mathrm{op}}}$ for a classical
noncommutative ring) are distinct. A passage that says "for a general
ring, left and right module categories are not canonically equivalent"
without stating the $\mathbb{E}_n$ level is ambiguous on the document's
default reading — and false if read as $\mathbb{E}_\infty$.

**Banned:** "For a general ring, an equivalence between left and right
module categories is additional data."

**Preferred:** "For a general associative ($\mathbb{E}_1$) ring spectrum
$R$, there is no canonical equivalence
$\mathbf{LMod}_R\simeq\mathbf{RMod}_R$." If the $\mathbb{E}_\infty$ case
is meant, state that the symmetry gives the canonical identification, so
the distinction is only for $\mathbb{E}_1$.

## `DEF-15`: One notion per definition block

A definition block introduces one notion with its single defining
occurrence. A block that defines left modules, right modules as left
modules over the opposite, bimodules, forgetful functors, the commutative
identification, and a warning about the noncommutative case in one go is
a grab bag, not a definition. Each notion has one block with its type,
data, and universal property; related notions have separate blocks that
cite the first. Where the house allows it, one block may define an
explicitly enumerated family of predicates on the same data, such as
symmetric, skew-symmetric, and alternating bilinear forms. A block never
defines notions of different types together.

**Banned:** "::: {#def-modules-over-ring} ## Modules over a ring — For a
ring $A$, $A\text{-}\mathbf{Mod}$ is … A right $A$-module is … An
$(A,B)$-bimodule therefore has … When $A$ is commutative … For a general
ring, an equivalence …"

**Preferred:** "::: {#def-left-modules} ## Left modules — Let $A$ be an
associative ($\mathbb{E}_1$) ring spectrum. $\mathbf{LMod}_A$ is … :::"
and then separately "::: {#def-right-modules} ## Right modules —
$\mathbf{RMod}_A := \mathbf{LMod}_{A^{\mathrm{op}}}$ :::" and so on, each
with its own defining occurrence.

A lemma, proposition, theorem, or remark is never inside a definition block,
not even as a trailing sentence. Each statement has its own block with its own
logical status. An implication between defined notions is a proposition with a
proof.

**Banned:** a definition block for alternating bilinear forms that ends
"alternating forms are skew-symmetric; the converse holds when $2$ is
invertible."

**Preferred:** close the definition block, then a proposition block that
states that alternating forms are skew-symmetric and that the converse holds
when $2$ is a unit, with its proof.

## `DEF-16`: Remark or warning inside a definition block

A definition block defines a notion. A remark about a different notion —
a warning that left and right module categories are not equivalent for a
general ring, a comment on additional data, a pointer to a subtlety —
belongs in a Remark block or in the paragraph following the definition,
not inside the definition block. An example belongs in its own Example
block, and a comparison of alternative formulations in its own Remark block
(`DEF-28`). A consequence of the definition — an implication between
the notions just defined, a condition under which two of them coincide —
is a proposition with its proof or citation, placed after the block
(`SEC-16`). A definition that contains its own counterexample, warning,
example, or consequences cannot be cited, linked, or included elsewhere
as the defining occurrence without dragging them along.

**Banned:** a "::: {#def-modules-over-ring}" block whose last sentence is
"For a general ring, an equivalence between left and right module
categories is additional data …"; a definition block for symmetric,
alternating, and even forms that closes with "Alternating forms are
skew-symmetric. The converse holds when multiplication by $2$ on $W$ is
a monomorphism. When multiplication by $2$ is an epimorphism, every
bilinear form is even" (`dzackgarza/research`,
`research/category-theory/framework/Bilinear-and-Quadratic-Forms.md`,
working tree over `26d4e303bc`, definition "Symmetry, alternation, and
evenness").

**Preferred:** close the definition after its defining sentences, then
write "::: {.Remark}" or a plain paragraph for the warning. The
definition is citable; the remark is separate.

Observed also in `dzackgarza/research`,
`research/category-theory/framework/Bilinear-and-Quadratic-Forms.md`
(working tree over `57c8eb1cb0`), definition "Rank one forms, the
hyperbolic plane, and split forms": the block defines *split* and
continues with a classification theorem and its specialization to
fields.

**Banned:** "A perfect symmetric form $b$ on $M$ is *split* if $M$ has
a direct summand $N$ with $N=N^{\perp_b}$ [@MH73, I §6.1]. Over a ring
whose finitely generated projective modules are free and in which $2$
is a unit, a split form is an orthogonal sum of hyperbolic planes
[@MH73, I §6.3]; this applies to a field of characteristic other than
$2$." as one definition block.

**Preferred:** the definition of *split* closed after its defining
sentence; the theorem of [@MH73, I §6.3] in its own block with its
hypotheses; the field case as its corollary.

## `DEF-17`: Reminder masquerading as a definition

A paragraph that writes "For a ring $A$, write $A\text{-}\mathbf{Mod}$
for the category of left $A$-modules" does not define left $A$-modules.
It presupposes the reader already knows what a left $A$-module is and
what the category is — its objects, morphisms, composition, forgetful
functor — and merely assigns notation. No construction is stated, no
universal property is given, no data are introduced. A definition
defines: it states the objects, the structure, and the property that
determines the notion. A reminder says "recall" and cites the defining
occurrence where the notion was defined. If the notion is prerequisite,
write "Recall (@def-left-modules) that …" and cite; if it is being
defined here, construct it. Do not summon a category into existence by
naming its notation.

**Banned:** "For a ring $A$, write $A\text{-}\mathbf{Mod}$ for the
category of left $A$-modules. A right $A$-module is a left
$A^{\mathrm{op}}$-module." — no definition of "module," no construction
of the category, no objects or morphisms stated.

**Preferred:** "Let $A$ be an associative ($\mathbb{E}_1$) ring spectrum.
An $A$-module is … The $\infty$-category $\mathbf{LMod}_A$ has objects …
morphisms are … with forgetful functor …" Or, if prerequisite:
"Recall that $\mathbf{LMod}_A$ denotes … as in @def-left-modules, with
…"

## `DEF-18`: Element formula on pure tensors for a functorial construction

A construction that is functorially $B\otimes_A(-)$ — extension of scalars
on modules, base change of a bilinear form as $B\otimes_A b$ — is defined
by an elementwise recipe $b_B(c\otimes_A x,d\otimes_A y)=cd\otimes_A b(x,y)$ on
pure tensors $c\otimes_A x$. The recipe names no functor, no canonical
isomorphisms, and is well-defined only by $B$-bilinear extension; it fails
outside free modules and hides whether $\otimes_A$ is the derived
($\otimes_A^L$) or underived product. The element formula, when it holds,
is a consequence of the functorial construction, not the definition.
State the functor and the canonical isomorphisms. The construction is
$$
(B\otimes_A M)\otimes_B(B\otimes_A M)\simeq
B\otimes_A(M\otimes_A M)\xrightarrow{B\otimes_A b} B\otimes_A W,
$$
i.e. $b_B$ is $B\otimes_A b$ composed with the canonical
$(B\otimes_A M)\otimes_B(B\otimes_A M)\simeq B\otimes_A(M\otimes_A M)$;
on pure tensors this is $b_B(c\otimes_A x,d\otimes_A y)=cd\otimes_A b(x,y)$
when $B$-bilinear extension is well-defined.

**Banned:** "Its base change is the $B$-bilinear map
$b_B(c\otimes_A x,d\otimes_A y)=cd\otimes_A b(x,y)$, whose value module is
$B\otimes_A W$."

**Preferred:** "Let $M,W\in\mathbf{LMod}_A$ and
$b\colon M\otimes_A M\to W$ be $A$-bilinear. Its base change is
$b_B:=(B\otimes_A b)\circ\text{can}\colon
(B\otimes_A M)\otimes_B(B\otimes_A M)\to B\otimes_A W$." State the
functor and the canonical map; derive the pure-tensor formula as a
consequence.

## `DEF-19`: Unconditional, conditional, and meta-remark mixed in one definition block

A definition block mixes notions with different logical status: unconditional
replete full subcategories (finitely generated, projective, free), properties
defined only under a hypothesis (torsion and torsion-free over an integral
domain), and a meta-remark about usage over a general ring. Each status has
its own block: unconditional notions have unconditional blocks; a notion
defined only under a hypothesis states the hypothesis in its block; a usage
rule is a Remark. Do not list them as parallel bullets under "The following
isomorphism-invariant properties define replete full subcategories" when the
list is not uniform.

Concrete standard (establishing the conventions named above): for an
associative ($\mathbb{E}_1$) ring spectrum $R$, $\mathbf{LMod}_R$ is the
presentable stable $\infty$-category of left $R$-module spectra.
$M\in\mathbf{LMod}_R$ is finitely generated if there exists a finite set
$I$ and an effective epimorphism $\bigoplus_{i\in I}R\twoheadrightarrow M$;
projective if $M$ is a retract of a free module
$\bigoplus_{i\in I}R$ for some set $I$; free if $M\simeq\bigoplus_{i\in
I}R$ for some set $I$; finitely generated projective if both hold, i.e.
$\mathbf{LMod}_R^{\mathrm{fg,proj}}=
\mathbf{LMod}_R^{\mathrm{fg}}\cap\mathbf{Proj}_R$, each replete full.
Torsion and torsion-free as stated below are defined only over an
integral domain $R$ (classical, i.e. $R=\pi_0 HR$ discrete): $M$ is
torsion if $\forall m\in M\,\exists\,0\neq r\in R$ with $r\cdot m=0$,
torsion-free if $\forall\,0\neq r\in R$, $r\cdot\colon M\to M$ is
injective. Over a general $\mathbb{E}_1$-ring spectrum a torsion
subcategory is not a property but a torsion theory — a hereditary torsion
pair, a $t$-structure — and is used only after that extra structure has
been specified (DEF-20).

**Banned:** "::: {#def-module-subcategories} The following
isomorphism-invariant properties define replete full subcategories of
$R\text{-}\mathbf{Mod}$: [four bullets] If $R$ is an integral domain, $M$
is torsion when … Over a general ring, a torsion subcategory is used
only after a torsion theory has been specified. :::"

**Preferred:** separate blocks: "::: {#def-fg-modules} ## Finitely
generated modules — Let $R$ be an $\mathbb{E}_1$-ring spectrum and
$M\in\mathbf{LMod}_R$. $M$ is finitely generated if … :::" and
"::: {#def-torsion-modules} ## Torsion modules (integral domain) — Let
$R$ be an integral domain (discrete) and $M\in\mathbf{LMod}_R$. $M$ is
torsion if … :::" and a separate Remark for the general $\mathbb{E}_1$
usage rule.

## `DEF-20`: Torsion over a general ring is extra structure, not a property

Over an integral domain $R$ (discrete, $R=\pi_0 HR$), torsion and
torsion-free are properties of $M\in\mathbf{LMod}_R$: $M$ is torsion if
$\forall m\,\exists\,0\neq r$ with $r\cdot m=0$, equivalently
$\operatorname{Ann}_R(m)\neq0$ for every $m$ (see MA-15); $M$ is
torsion-free if $\operatorname{Ann}_R(m)=0$ for $m\neq0$. Over a general
associative ($\mathbb{E}_1$) ring spectrum $R$, a "torsion subcategory"
is not a property of $M$ but extra structure: a hereditary torsion pair
$(\mathcal{T},\mathcal{F})$, a $t$-structure, or a localizing
subcategory with its torsion functor — not "a torsion theory," which has
no referent (TERM-4). The last sentence of {#def-module-subcategories}
is a prose usage rule with no construction. State the precise structure
and cite its definition; put the usage rule in a Remark, not in the
definition of finitely generated projective modules.

**Banned:** the last sentence of {#def-module-subcategories} as part of
the definition of $R\text{-}\mathbf{Mod}$ subcategories, and "a torsion
theory has been specified" with no definition of "torsion theory."

**Preferred:** "::: {.Remark} Over a general $\mathbb{E}_1$-ring spectrum
$R$, a torsion subcategory means a hereditary torsion pair
$(\mathcal{T},\mathcal{F})$ on $\mathbf{LMod}_R$ (see @def-torsion-pair)
or the corresponding $t$-structure, and is used only after that pair has
been specified. :::"

## `DEF-21`: Compound term defined by "both conditions hold"

A new term "finitely generated projective" is introduced as "both of the
first two conditions hold," referencing bullet order, instead of defining
"finitely generated" and "projective" and noting the subcategory of
objects satisfying both is the intersection. The compound is not
primitive; its meaning is the conjunction, and the equivalence with other
characterizations (dualizable, compact projective) is a theorem.

**Banned:** "finitely generated projective: both of the first two
conditions hold."

**Preferred:** "An $R$-module $M$ is finitely generated projective if it
is finitely generated and projective, i.e.
$M\in\mathbf{LMod}_R^{\mathrm{fg}}\cap\mathbf{Proj}_R$, each replete
full." Define each property separately; the conjunction is the
intersection, not a new primitive.

## `DEF-22`: Characterization presented as definition, freely interchanging equivalent definitions

A notion is defined by a characterization whose equivalence with the
defining property is a theorem — often a theorem that is not proved or
cited here, and whose equivalence is assumed to still hold in this highly
specialized context (e.g. $\infty$-categorical, derived) without
argument. "$M$ is a direct summand of a free module" is the theorem
"projective iff retract of free," not the definition. Freely
interchanging such characterizations as if they were the same definition
hides the theorem and its hypotheses. When a passage uses a characterization
other than the linked definition, it links or states the theorem that proves
the equivalence, with its hypotheses.

Concrete standard: $M\in\mathbf{LMod}_R$ is **projective** if
$\operatorname{Hom}_R(M,-)$ preserves effective epimorphisms,
equivalently every diagram
$$
\begin{tikzcd}
& M\arrow[d]\\
N\arrow[r,two heads]&P
\end{tikzcd}
$$
with $N\twoheadrightarrow P$ lifts, equivalently every surjection
$N\twoheadrightarrow M$ splits. Theorem: $M$ is projective iff it is a
retract of $\bigoplus_{i\in I}R$ for some set $I$ — stated and proved or
cited, and checked to hold in the $\infty$-categorical/derived context
where it is used. Similarly, $M$ is finitely generated if
$\operatorname{Hom}_R(M,-)$ preserves filtered colimits, equivalently the
surjection condition above; state the definition, then cite the
characterization as a theorem and do not freely substitute one for the
other.

**Banned:** "projective: $M$ is a direct summand of a free module" as the
definition; "finitely generated: some $R^n\twoheadrightarrow M$ is
surjective" as the definition without the generating-set or compactness
formulation; using either characterization later as if it were the
definition without citing the equivalence.

**Preferred:** define $M$ projective by the lifting property; then
"Theorem: $M$ is projective iff it is a retract of a free module
$\bigoplus_{i\in I}R$." Define $M$ finitely generated by the generating
set; then "iff there exists a finite $I$ and an effective epimorphism
$\bigoplus_{i\in I}R\twoheadrightarrow M$." State which is the definition
and which is the theorem, and ensure the cited equivalence holds in the
specialized context where it is used.

## `DEF-23`: Specialized notion without scaffolding from general notions

A specialized notion — a basis, a based module — is defined without first
defining the general notions it depends on: the free module functor,
the universal property of freeness, what a generating family is, and
whether "being a basis" is a property of a family, a chosen structure, or
an existence statement. The definition jumps to "a basis indexed by $I$ is
an isomorphism $e\colon R^{(I)}\xrightarrow{\sim}M$" without ever saying
what $R^{(I)}$ is. Scaffold from the general: define the free functor,
then the generating notions, then freeness, then basis.

Concrete standard: the free $R$-module functor
$F\colon\mathbf{Sets}\to\mathbf{LMod}_R$, $I\mapsto R^{(I)}:=
\bigoplus_{i\in I}R$, is defined by the universal property
$\operatorname{Hom}_R(F(I),M)\cong\operatorname{Hom}_{\mathbf{Sets}}(I,
U(M))$ where $U\colon\mathbf{LMod}_R\to\mathbf{Sets}$ is the underlying-
set functor. $R^{(I)}$ means the finite-support sum
$\bigoplus_{i\in I}R$, not the product $R^I:=\prod_{i\in I}R$; they are
not equal without a finiteness hypothesis on $I$, and a generating family
as a map $\bigoplus_{i\in I}R\to M$ requires $I$ to be a set with that
finite-support condition.

**Banned:** "A basis of an $R$-module $M$ indexed by $I$ is an
isomorphism $e\colon R^{(I)}\xrightarrow{\sim}M$" with no prior definition
of $R^{(I)}$ or of $F$.

**Preferred:** "Let $F\colon\mathbf{Sets}\to\mathbf{LMod}_R$,
$F(I):=\bigoplus_{i\in I}R$, be the free functor. For $M\in\mathbf{LMod}_R$
and a set $I$, a family $(m_i)_{i\in I}$ in $M$ is a basis if the induced
$F(I)\to M$ is an equivalence; equivalently the $R$-linear map is an
isomorphism."

## `DEF-24`: Property versus structure versus existence for a basis

"Being a basis" is used without stating whether it is a property of a
family ($ (m_i)_{i\in I}$ is a basis iff the induced map is an iso), a
chosen structure (a specific isomorphism $e\colon F(I)\xrightarrow{\sim}M$),
or an existence statement ($M$ is free if there exist a set $I$ and an
isomorphism $F(I)\xrightarrow{\sim}M$). Freeness is a property of $M$;
a basis is a family or a chosen isomorphism, never a set $I$ that exists. The same English — "a basis indexed
by $I$ is an isomorphism $e$" — collapses the family $(e(1_i))_{i\in I}\subset
M$ with its classifying map $e$, and the quantifier ("there exists $e$" vs
"a chosen $e$") is not stated.

**Banned:** "A basis of an $R$-module $M$ indexed by $I$ is an
isomorphism $e\colon R^{(I)}\xrightarrow{\sim}M$, and a based module is a
pair $(M,e)$" — unclear whether "is" means property, chosen structure, or
existence, and conflates the elements $e(1_i)\in M$ with the map $e$.

**Preferred:** state which is meant. Property: "A family $(m_i)_{i\in I}$
in $M$ is a basis if the induced $F(I)\to M$ is an equivalence." Structure:
"A based $R$-module is a pair $(M,e)$ with $M\in\mathbf{LMod}_R$ and a
chosen equivalence $e\colon F(I)\xrightarrow{\sim}M$; write the underlying
family as $e_i:=e(1_i)$." Existence: "$M$ is free if there exist a set
$I$ and an equivalence $F(I)\xrightarrow{\sim}M$."

## `DEF-25`: A category defined pointwise by its objects

A structure that should be a category — based $R$-modules — is defined
only by its objects $(M,e)$, with no morphisms, no composition, no
identities, and no forgetful functors. The set $\operatorname{Bas}_I(M)$
of bases is introduced as an afterthought for fixed $I$. A category has
objects and morphisms; defining only the objects is pointwise, not
categorical, and the functoriality in $I$ is lost.

**Banned:** "A basis … is an isomorphism $e\colon R^{(I)}\xrightarrow{\sim}M$,
and a based module is a pair $(M,e)$. Write $\operatorname{Bas}_I(M)$ for
the set of such isomorphisms."

**Preferred:** define the category $\mathbf{BMod}_R$ of based $R$-modules:
objects are pairs $(M,e)$ with $M\in\mathbf{LMod}_R$ and
$e\colon F(I)\xrightarrow{\sim}M$ for some set $I$; a morphism
$(M,e)\to(N,e')$ over $\varphi\colon I\to J$ is an $R$-linear
$f\colon M\to N$ with $f\circ e = e'\circ F(\varphi)$, with
$F(\varphi)\colon F(I)\to F(J)$. The forgetful functors
$\mathbf{BMod}_R\to\mathbf{LMod}_R$, $(M,e)\mapsto M$, and
$\mathbf{BMod}_R\to\mathbf{Sets}$, $(M,e)\mapsto I$, are part of the
data. Then put $\operatorname{Bas}_I(M):=\operatorname{Iso}(F(I),M)$,
which is a torsor under $\operatorname{Aut}(F(I))$ when nonempty.

## `DEF-26`: Mark the term being defined

In a definition, the term being defined carries the house mark for a
definiendum (italics, or a macro such as `\dfn{…}`) at its defining
occurrence, and nowhere else (`PR-10`). Every definiendum in one document
has the same mark. The surrounding text states the quantifiers and
conditions; the mark shows which word is introduced. A later use links the
defining occurrence (`XREF-5`).

**Banned:** "An $R$-module $M$ is torsion when …", with the term
unmarked; "An $R$-module $M$ is **torsion** if …".

**Preferred:** "Let $R$ be an integral domain. An $R$-module $M$ is
*torsion* if every $m\in M$ is annihilated by some nonzero $r\in R$."
Similarly, "A family $(m_i)_{i\in I}$ in $M$ is a *basis* if …", "A *based
module* is a pair $(M,e)$ …", "A $t$-structure is *hereditary* if …": the
mark falls on the introduced noun, noun phrase, or adjective, and on nothing
else.

## `DEF-27`: Distinguished object introduced only in the title

A block titled `{#def-distinguished-factorization}` defines "a
factorization of $F\colon\mathcal{C}\to\mathcal{E}$ through $\mathcal{D}$"
but never defines what "distinguished" means. The title is not the
definition. A distinguished, canonical, or standard object is a chosen
object in its category — here a chosen factorization
$(H_{\mathrm{dist}},G_{\mathrm{dist}},\alpha_{\mathrm{dist}})$ among all
factorizations of $F$ through $\mathcal{D}$ — with its construction and
the universal property or comparison that makes it distinguished stated
explicitly.

Concrete standard: for $R$ an associative ($\mathbb{E}_1$) ring spectrum,
the distinguished underlying-set functor is the composite of forgetful
functors
$$
\mathbf{LMod}_R \xrightarrow{U_{R/\mathbf{Ab}}}
\mathbf{Ab}\xrightarrow{U_{\mathbf{Ab}/\mathbf{Grp}}}
\mathbf{Grp}\xrightarrow{U_{\mathbf{Grp}/\mathbf{Sets}}}
\mathbf{Sets},
$$
each $U$ with its left adjoint $F$ (free $R$-module, free abelian group,
free group), and the factorization is distinguished among factorizations
of $U_{\mathbf{LMod}_R/\mathbf{Sets}}$ (see @def-factorization).

**Banned:** "::: {#def-distinguished-factorization} A factorization of
$F\colon\mathcal{C}\to\mathcal{E}$ through $\mathcal{D}$ consists of …
The underlying-set functor of an $R$-module is the composite
$R\text{-}\mathbf{Mod}\to\mathbf{Ab}\to\mathbf{Grp}\to\mathbf{Set}$. :::"
— the distinguished composite is asserted inside the general definition and
never defined as the distinguished object.

**Preferred:** separate blocks: "::: {#def-factorization} ## Factorization
— A factorization of $F\colon\mathcal{C}\to\mathcal{E}$ through
$\mathcal{D}$ is a tuple $(H,G,\alpha)$ with $H\colon\mathcal{C}\to
\mathcal{D}$, $G\colon\mathcal{D}\to\mathcal{E}$, and a specified natural
equivalence $\alpha\colon F\simeq G\circ H$. :::" and "::: 
{#exm-distinguished-underlying-set} ## Distinguished underlying-set
factorization — The distinguished factorization of
$U_{\mathbf{LMod}_R/\mathbf{Sets}}$ is
$(U_{\mathbf{LMod}_R/\mathbf{Ab}},U_{\mathbf{Ab}/\mathbf{Grp}}\circ
U_{\mathbf{Grp}/\mathbf{Sets}},\operatorname{id})$ as above. :::"

## `DEF-28`: Example and remark inside a definition block

A general definition, its example (the underlying-set functor as the
composite through $\mathbf{Ab}$ and $\mathbf{Grp}$), and a remark about
alternative factorizations are in one fenced `{#def-...}`. Each has its
own block: the general notion has a definition block, the composite has
an example block that cites the definition, and the comparison of
alternative factorizations has a remark.

**Banned:** the quoted `{#def-distinguished-factorization}` block that
contains both the general factorization definition and the two paragraphs
about $R\text{-}\mathbf{Mod}\to\mathbf{Ab}\to\mathbf{Grp}\to\mathbf{Set}$.

**Preferred:** close the definition after the tuple
$(H,G,\alpha)$, then "::: {.Example}" for the distinguished composite,
then "::: {.Remark}" for alternative factorizations and their comparison
$2$-cells.

## `DEF-29`: Definition in running prose without a fenced block is not a definition

A sentence in running prose that looks like a definition — "A
factorization of $F$ through $D$ consists of functors $H$ and $G$
together with …," "A theorem that $F$ lands is a factorization" — is not
a definition. A definition is a numbered definition block with a stable
identifier (`DEF-4`), with the definiendum marked at its defining
occurrence (`DEF-26`); it is the single defining occurrence (`DEF-1`), and
every later use links it (`XREF-1`, `XREF-5`). Running prose
cannot be cited, linked, or included elsewhere, has no ID, and has no
logical status. Colloquial
"property," "structure," and "lands" definitions in prose are not
definitions.

**Banned:** "## Landing statements and constructions {#sec-statements-vs-
constructions} A theorem that $F\colon\mathcal{C}\to\mathcal{D}$ lands in
$D_P$ is a factorization $F=i\circ\bar F$. This theorem does not redefine
$F$ or $D_P$." — two sentences of prose, no fenced `{#def-lands}` or
`{.Theorem}`, no marked definiendum.

**Preferred:** "::: {#def-lands} ## Lands in — … :::" as above, and
"::: {.Proposition #prp-lands} ### Landing — … :::" with proof exhibiting
$\bar F$ and $\alpha$. The prose between fenced units is glue, not the
definition.

## `DEF-30`: Circular definition via diagram label

The definiendum appears as a label in the diagram that is supposed to
define it — the square's apex is already labeled $f^{-1}(y)$ and then the
text says "the fiber of $f$ over $y$ is the apex." The diagram
presupposes the notation being defined. Label the apex neutrally (e.g.
$P$) in the diagram that defines it; introduce the notation
$f^{-1}(y):=P$ after the universal property is stated.

**Banned:** the quoted square with apex $f^{-1}(y)$ and the sentence
"The fiber of $f$ over $y$ is the apex of the cartesian square" — the
apex is already called $f^{-1}(y)$.

**Preferred:** "The **fiber** $f^{-1}(y)$ is the pullback $X\times_Y 1$,
i.e. an object $f^{-1}(y)$ equipped with projections
$p_1\colon f^{-1}(y)\to X$, $p_2\colon f^{-1}(y)\to1$ and a specified
equivalence $f\circ p_1\simeq y\circ p_2$ exhibiting the square as
(homotopy) cartesian. In the diagram write the apex as $X\times_Y 1$ or
$P$, then put $f^{-1}(y):=X\times_Y 1$."

## `DEF-31`: "The relevant pullbacks" as a hypothesis

A definition assumes "let $\mathcal{C}$ have a terminal object $1$ and
the relevant pullbacks" without stating which pullbacks are assumed to
exist. "The relevant" names no class of diagrams and the reader cannot
determine whether the particular pullback needed for the definition
exists. State the hypothesis: either "$\mathcal{C}$ has all pullbacks"
or "assume the pullback of $f$ along $y$ exists."

**Banned:** "Let $\mathcal{C}$ have a terminal object $1$ and the
relevant pullbacks, let $f\colon X\to Y$, and let $y\colon1\to Y$ be a
point."

**Preferred:** "Let $\mathcal{C}$ be an $\infty$-category with terminal
object $1$ and assume the pullback of $f\colon X\to Y$ along
$y\colon1\to Y$ exists" or "Let $\mathcal{C}$ be an $\infty$-category
with all pullbacks, terminal object $1$, $f\colon X\to Y$, and
$y\colon1\to Y$."

## `DEF-32`: Fiber as apex alone, without its projections and homotopy

The fiber is defined as "the apex of the cartesian square," naming only
the object $f^{-1}(y)$. The fiber is the object *equipped with* its
projections $f^{-1}(y)\to X$, $f^{-1}(y)\to1$ and the specified
equivalence $f\circ\mathrm{pr}_X\simeq y\circ\mathrm{pr}_1$ that exhibits
the square as cartesian. In the document's default
$\mathcal{C}:=\mathbf{Cat}_\infty$ the square is a homotopy pullback,
unique up to a contractible space of equivalences, not a strict pullback
with a unique apex on the nose.

Concrete standard: for $f\colon X\to Y$ and $y\colon1\to Y$ in an
$\infty$-category with pullbacks, the **fiber** is the homotopy pullback
$f^{-1}(y):=X\times_Y 1$ with its projections and the specified
$2$-cell $f\circ p_1\Rightarrow y\circ p_2$ (marked $\lrcorner$).

**Banned:** "The fiber of $f$ over $y$ is the apex of the cartesian
square" with the square's two projections and $2$-cell unstated.

**Preferred:** "The **fiber** of $f$ over $y$ is the homotopy pullback
$X\times_Y 1$, i.e. the object $f^{-1}(y)$ with $p_1\colon f^{-1}(y)\to X$,
$p_2\colon f^{-1}(y)\to1$, and $\alpha\colon f\circ p_1\simeq y\circ p_2$
exhibiting the square as cartesian."

## `DEF-33`: Special case without scaffolding from the general notion

A general construction is introduced at its special case. The fiber
$f^{-1}(y)$ is a special case of a fiber product (pullback); freeness is
a special case of the free-forgetful adjunction; being a basis is a
special case of a generating family. The standard is to state the general
construction first, with its universal property and notation, and then
specialize by reference — not to use the special case as the place to
introduce the general construction. Defining the special case without the
general notion repeats the cone's universal property that belongs in the
general definition and leaves the general notion undefined.

Concrete standard: define pullbacks as limits of cospans (\ref{def-pullback}):
for $f\colon X\to Y$ and $g\colon Z\to Y$ in an $\infty$-category with
pullbacks, the **pullback** is the limit $X\times_Y Z$ with its cone
$(X\times_Y Z\to X, X\times_Y Z\to Z)$ terminal among cones over the
cospan. Then: "The **fiber** of $f$ over $y\colon1\to Y$ is the pullback
$X\times_Y 1$ of $f$ along $y$ (\ref{def-pullback})." This pattern is
general: the free module functor $F\colon\mathbf{Sets}\to\mathbf{LMod}_R$,
the notion of generating family, and freeness are defined before
"basis" and "based module" (DEF-23).

**Banned:** "Let $\mathcal{C}$ have a terminal object $1$ and the
relevant pullbacks, let $f\colon X\to Y$, and let $y\colon1\to Y$ be a
point. The fiber of $f$ over $y$ is the apex of the cartesian square …"
— defines the special case without the general notion.

**Preferred:** define $X\times_Y Z$ once via terminal cones; then "the
fiber is $X\times_Y 1$, the pullback of $f$ along $y$."

## `DEF-34`: "Finite-generation hypothesis" with no quantified finiteness notion

"Finite-generation hypothesis" names no notion: finitely generated vs.
finitely presented vs. perfect (compact in $\mathbf{LMod}_{\mathbb Z}$)
vs. coherent are distinct, and over a general $\mathbb E_1$-ring
spectrum $R$ the correct condition is perfectness, not discrete finite
generation. The document's default is $\mathbf{LMod}_R$ stable; discrete
finite generation is a property of $\pi_0M$ after truncating.

**Banned:** "the finite-generation hypothesis" unqualified.

**Preferred:** quantify: "for $M$ perfect in $\mathbf{LMod}_{\mathbb Z}$
(in particular, for discrete $M$ finitely generated over Noetherian
$\mathbb Z$)" or "for $M$ finitely presented" — name which finiteness,
in which category, and whether derived or discrete, at each use.

## `DEF-35`: Localization at a submonoid

**Banned:** "Let $S\subseteq R$ be a multiplicatively closed subset" where
the construction uses $1\in S$.

**Preferred:** "Let $S$ be a submonoid of the multiplicative monoid
$(R,\cdot)$." A nonempty subset closed under multiplication need not
contain $1$, so it need not be a submonoid.

The rule governs authored prerequisites and definitions. A problem statement
quoted from a source keeps the source's wording.

## `DEF-36`: Higher-categorical primitive first

For a notion intrinsic to higher categories, first fix the universe, the model
of higher categories, and the standard name of the category that model
defines. Define the primitive construction there, with the type of every
object, morphism, and comparison cell. If the familiar formulation lives in
$\mathbf{Spaces}$, name the functor from the chosen category of higher
categories to spaces, and cite the theorem that identifies the image of the
primitive construction with the published space-level definition. The
space-level formulation is a specialization, not the definition.

Representable, Yoneda, mapping-space, and detection criteria are theorems
stated after the definition, with their hypotheses. Recovery of an ordinary
or strict special case is a lemma or remark after the general construction.

## `DEF-37`: Mathematics before its realization

A mathematical chapter defines its categories, functors, morphisms, and
universal properties without implementation names. A realization section can
then name the Lean, Sage, or Mathlib object that represents the defined
mathematics. Lean, Mathlib, and Sage identifiers are code-formatted and are
never prose nouns.

## `DEF-38`: Define at maximal generality, then specialize

A construction is defined at the maximal generality at which it exists,
and a special case is introduced as a restriction of the general object,
not as the defining occurrence. Do not define a bilinear form over
$\mathbf R$ when the construction exists over an arbitrary ring $R$; do
not define a general notion with an "even only" hypothesis accidentally
baked in; do not define lattice-specific language before the corresponding
bilinear-module construction exists to restrict (cf. PR-63, PR-72).

**Banned:** "A $W$-valued lattice is a free $\mathbb Z$-module $L$ with a
bilinear form $b\colon L\times L\to W$ such that $b(x,x)\in 2W$" as the
definition of bilinear forms, when the ring is general and evenness is a
property, not part of the construct; a lattice-specific term whose
underlying bilinear-module notion was never defined.

**Preferred:** define the pairing or bilinear form over an arbitrary base
ring $R$ and value module $W$; then "an *even* form is …" as a property
(SEC-12); then the lattice as the case $R=\mathbb Z$ with its finiteness
and integrality hypotheses stated (`PR-71`).

## `DEF-39`: Structural definition before elementwise characterization

When a canonical module, map, functor, fiber, or adjoint exists, define the
notion through that object. An elementwise condition is a theorem to be
proved equivalent — not the defining occurrence (DEF-22). The structural
definition names the object the theory reuses; the elementwise formula is
its evaluation in the concrete case (PR-47). A property of a map —
injective, surjective, an isomorphism — is stated as the vanishing of
the term of its exact sequence that measures the failure: the kernel,
the cokernel, the obstruction class (`DEF-40`, `MA-17`, `NOT-1`). The
sequence exhibits the adjoint, the radical, and the coradical at once,
and every later property is a statement about one of its terms.

**Banned:** "$b$ is *nondegenerate* if $b(x,y)=0$ for all $y$ implies
$x=0$" as the definition of nondegeneracy, never naming the adjoint
$b^{\sharp}\colon M\to\operatorname{Hom}_R(M,W)$; "$b^\sharp$ is
injective" as the whole account of nondegeneracy, with no radical named.

**Preferred:** the exact sequence
$0\to\radic(M)\to M\xrightarrow{b^\sharp}\operatorname{Hom}_R(M,W)\to\operatorname{corad}(M)\to0$
defining the radical and the coradical; "$b$ is *nondegenerate* when
$\radic(M)=0$ and *perfect* when
$\radic(M)=0=\operatorname{corad}(M)$" — then the elementwise
characterization as a proposition. Likewise: reframe a notion in terms of the value group
$\operatorname{Val}(b)\subseteq W$ instead of carrying $b(x,x)\in 2W$
through every use (PR-45).

A surjectivity claim is the same statement from the other end:
"$\Orth(L)\to\Orth(T)$ is surjective" is "the cokernel, or the
obstruction group, of a stated sequence vanishes", and the sequence,
not the adjective, is what the later theory uses — the next question
is always the kernel, and a surjectivity sentence leaves it unnamed
(`DEF-40`, `CITE-8`).

Observed in `dzackgarza/research`:
`research/coble/lattices-and-moduli/lattices.md` (working tree over
`57c8eb1cb0`), proof under "Period domain embeddings and
normalization";
`research/lattice-theory/discriminant-forms-and-genus.md` at
`57c8eb1cb0`, theorem "$\Orth(H)\to\Orth(A_{H,q})$ is surjective for
indefinite $2$-elementary $H$".

**Banned:** "the homomorphism $\Orth(\lkt)\to \Orth(T_\Co)$ is
surjective."; a theorem whose statement ends "is surjective." with no
sequence stated.

**Preferred:** "for the restriction $r\colon\Orth(\lkt)\to\Orth(T_\Co)$,
the sequence $1\to\ker(r)\to\Orth(\lkt)\xrightarrow{r}\Orth(T_\Co)$
with $\ker(r)$ identified, and the claim $\operatorname{im}(r)=\Orth(T_\Co)$
with the extension criterion that proves it cited at the step"; the
exact sequence $1\to\widetilde\Orth(H)\to\Orth(H)\to\Orth(A_{H,q})\to1$,
the theorem being exactness at the last term.

## `DEF-40`: Give the complete structural construction

A construction that comes as a fiber, cofiber, or short exact sequence is
given in full. State the sequence $A\to B\to C$ with its maps; never write
an isolated quotient $B/A$, an isolated kernel $\ker(f)$, or an isolated
cokernel $\operatorname{coker}(f)$ as though it were the construction.
The same applies at the categorical level: an embedding problem is
formulated in the relevant category with its equivalences as
$2$-morphisms (DIA-5); a correspondence of overlattices with isotropic
subgroups is stated at the level it actually has — as an equivalence of
posets, categories, or groupoids, when that is what the source proves —
not decategorified to a bare bijection (STR-4).

**Banned:** "$M/N$" used as the object under discussion with no
mention of the map $N\to M$ or the cofiber sequence that produces it;
"the set of overlattices of $L$ is in bijection with the isotropic
subgroups of $D_L$" where the source proves an order isomorphism of
posets or an equivalence of groupoids.

**Preferred:** the cofiber sequence
$N\hookrightarrow M\twoheadrightarrow M/N$ with its maps named (PR-56);
"the map $K\mapsto K/L$ is an order isomorphism from the overlattice
poset to the isotropic-subgroup poset of $D_L$" — the statement at the
structure level the theorem has.

The same rule fixes the terms. The codomain of the morphism is its
natural codomain, and the sequence continues to the cokernel:
$0\to\ker f\to M\xrightarrow{f}N\to\operatorname{coker}f\to0$.
Truncating at $\operatorname{im}(f)$ specializes early; the image is
recovered from the full sequence by epi–mono factorization and need
not be a term (`PR-76`). A two-sided construction is given on both
sides (`STR-7`). An object produced by a kernel or cokernel is defined
by its place in the sequence — "$B^{\mathrm{nd}}$ is defined by the
exact sequence $0\to\radic(B)\xrightarrow{\rho_B}B\to B^{\mathrm{nd}}\to0$
in $\mathbf{BilMod}_R$" — not by a separate "Define
$B^{\mathrm{nd}}:=\coker(\rho_B)$" that restates the sequence as a
formula (`PR-75`, `NOT-10`). And a condition on a morphism is a
condition on a term: "when there is a short exact sequence
$0\to S\to L\to Q\to0$" conditions on the existence of a cokernel,
which every morphism of modules has, where the intended condition is
on $\operatorname{coker}(f)$ (`DEF-39`).

Observed in `dzackgarza/research`:
`research/category-theory/framework/Bilinear-and-Quadratic-Forms.md`
(working tree over `57c8eb1cb0`), definitions "Left and right
orthogonal complements" and "Nondegenerate reduction";
`research/lattice-theory/Isometries-and-Arithmetic-Invariants.md` at
`ab530c1dcc`, definition "Primitive embeddings".

**Banned:** "Define the **left orthogonal complement**
\({}^{\perp_b}T\) and the **right orthogonal complement**
\(T^{\perp_b}\) by the kernel exact sequences
$$0\too{}^{\perp_b}T\xrightarrow{\kappa_{\iota}^{\mathrm L}}M\xrightarrow{\lambda_{\iota}^{\mathrm L}}\operatorname{im}(\lambda_{\iota}^{\mathrm L})\too0$$
and" — the codomain truncated to the image, the right complement
promised and not displayed; "Let $B$ be a symmetric bilinear module
and let $$\rho_B\colon\radic(B)\too B$$ be its radical morphism.
Define $$B^{\mathrm{nd}}\definedas\coker_{\mathbf{BilMod}_R}(\rho_B).$$";
a primitive embedding defined "when there is a short exact sequence".

**Preferred:**
"$0\to{}^{\perp_b}T\to M\xrightarrow{\iota^*\circ b^\sharp_{\mathrm L}}\Hom_R(T,W)\to\operatorname{coker}\to0$,
and $T^{\perp_b}$ by the same sequence with $b^\sharp_{\mathrm R}$" —
both sides, the natural codomain, the cokernel named;
"$B^{\mathrm{nd}}$ is defined by the exact sequence
$0\to\radic(B)\xrightarrow{\rho_B}B\to B^{\mathrm{nd}}\to0$ in
$\mathbf{BilMod}_R$"; "$\iota\colon S\to L$ is **primitive** when
$\operatorname{coker}(\iota)$ is torsion-free".

A quotient written as $X/Y$, or an isolated kernel written as
$\ker(f)$, names the object without the sequence that defines it, so
the reader cannot see which map it is the cokernel or kernel of,
whether the quotient carries the structure the sentence then uses, or
that the object already has a name. The named object is used, and a
new one is defined by its place in a (co)fiber sequence, never as an
isolated kernel, cokernel, or quotient.

Observed in `dzackgarza/research`:
`research/lattice-theory/Lattices-and-Discriminant-Forms.md` at
`57c8eb1cb0`, definition "The canonical bilinear-module map to the
dual lattice";
`research/lattice-theory/discriminant-forms-and-genus.md` at
`57c8eb1cb0`, definition "Image and coset space of the quadratic
discriminant representation";
`research/lattice-theory/lattice-theory.md` at `ab530c1dcc`,
definition "The spinor norm and the special orthogonal group".

**Banned:** "Define the **bilinear denominator**
$$N_b(L)\definedas\exp(L^\#/L).$$"; "Define the pointed left-coset set
$$\mathcal C_{L,q}\definedas\Orth(A_{L,q})/I_{L,q},$$ pointed by
$I_{L,q}$. It is a quotient group exactly when
$I_{L,q}\trianglelefteq\Orth(A_{L,q})$."; "The **special orthogonal
group** is
$$\SO(L)\definedas\ker\qty{\det\colon\Orth(L)\too\theset{\pm1}}.$$"

**Preferred:** "$N_b(L)\definedas\exp(A_L)$", with $A_L$ the cokernel
in $0\to L\to L^\#\to A_L\to0$; the sequence
$1\to I_{L,q}\to\Orth(A_{L,q})\to\mathcal C_{L,q}$ with
$\mathcal C_{L,q}$ its cofiber, and the normality of $I_{L,q}$ as the
proposition under which the cofiber is a group; the sequence
$1\to\SO(L)\to\Orth(L)\xrightarrow{\det}\theset{\pm1}$ as the
definition of $\SO(L)$, with the surjectivity of $\det$ stated where
it holds.

A sequence whose middle arrow is unlabelled and whose last term is the
cokernel of that unlabelled arrow is the same defect: the map is named,
and the cokernel is the cokernel of the name.

Observed also in `dzackgarza/research`,
`research/lattice-theory/invariant-and-coinvariant-lattices.md`
(annotated review proposal over `9cfdecf73d`), the proposition on the
invariant–coinvariant inclusion.

**Banned:** "$0\too L^G\perp L_G\longrightarrow L
\twoheadrightarrow\operatorname{coker}\qty{L^G\perp L_G\to L} \too0$".

**Preferred:** "$0\too L^G\perp L_G\xrightarrow{j_G}L\too
\operatorname{coker}(j_G)\too0$".

## `DEF-41`: An established notion is defined by its established formulation

A notion the literature defines is defined here by a formulation the
literature recognizes, stated in the most structured framework the
document has set up; every other formulation is a proposition with the
equivalence proved or cited (`DEF-22`). The textbook formulation is the
floor, not the ceiling. A document that has introduced the adelic group
$\Orth(V_{\mathbb A_f})$, the category $\mathbf{Bil}_R$, or the
universal quadratic module $\Gamma_R^2(M)$ states each notion that lives
there in those terms — the genus as an orbit, the discriminant form as a
cokernel in $\mathbf{Bil}_R$ — and recovers the elementary formulation as
a proposition. The test that separates the structured definition from a
gratuitous one: a framework in which the notion is an instance of a
general construction is where the notion is defined; a framework that
merely detects the notion supplies a characterization. Evenness is a
condition on the values of $b$ in $W$, so it is defined in $W$; the
quadratic refinement that detects it is the proposition. Three
substitutions fail this rule: a characterization through machinery the
notion is not an instance of, presented as its definition; a standard
universal construction presented as an improvised list of relations in
running prose, with no name, no block, and no citation; and a retreat
to the elementary textbook formulation for a notion the document has
already placed in a more structured framework. Each hides where the
notion comes from. The third also makes the document's architecture
inconsistent: once $\widehat L$ and $\Orth(V_{\mathbb A_f})$ are
introduced, every notion that lives in them is stated in them. An ad hoc
reformulation is also where errors enter: a place-by-place condition
rewritten from memory can quantify over the wrong objects. Before
writing a definition, read the standard source's formulation (`DEF-2`)
and name the object the source names (`TERM-16`).

Observed in `dzackgarza/research` (working tree over `26d4e303bc`):
`research/category-theory/framework/Bilinear-and-Quadratic-Forms.md`,
definition "Symmetry, alternation, and evenness" and the running text
that introduces $\Gamma_R^2(M)$;
`research/lattice-theory/discriminant-forms-and-genus.md`, definition
"Genus and class set".

**Banned:** "the form $b$ is **even** when there is a quadratic map
$\widetilde q_b\in\operatorname{Quad}_{R,2W}(M)$ for which
$q_b=U(2W\injects W)\circ U(\widetilde q_b)$" as the definition of
evenness; "let $\Gamma_R^2(M)$ be the quotient of the free $R$-module on
symbols $[x]$ … by the relations …" in running text, with
$\operatorname{Quad}_{R,W}(M):=\Hom(\Gamma_R^2(M),W)$ derived from it
and no source named; "the full subgroupoid on lattices $M$ satisfying
$M\otimes_RK_v\isoto L\otimes_RK_v$ for every place $v$ of $K$" as the
definition of the genus, in a document whose spinor genus is defined
through $\widehat L$ and $\Orth(V_{\mathbb A_f})$ — and which, with
$K_v$ at the finite places, states isometry of the completed spaces
rather than of the completed lattices.

**Preferred:** "$b$ is **even** if $b(x,x)\in2W$ for all $x\in M$",
equivalently $\operatorname{Val}(b)\subseteq2W$ (`PR-45`), with the
lift to $\operatorname{Quad}_{R,2W}(M)$ as a proposition; a definition
block "the universal quadratic module $\Gamma_R^2(M)$, the module of
degree-two divided powers, with $\gamma_M\colon M\to\Gamma_R^2(M)$
universal among quadratic maps out of $M$", and its presentation by
generators and relations as a proposition with the citation; for
lattices $L,M$ on one quadratic space $V$ over $K$: "$M$ lies in the
genus of $L$ if $\widehat M=\alpha\widehat L$ for some
$\alpha\in\Orth(V_{\mathbb A_f})$", with the local condition
$M\otimes_RR_v\cong L\otimes_RR_v$ at every finite place $v$ as the
proposition that connects it (`TERM-16`, `DEF-22`).

The generators of the finite $2$-elementary quadratic forms are the same
defect: four letters introduced as realizations of discriminant forms,
with the generation statement and the relations stated as prose about
the letters. The letters are defined as the discriminant forms of named
lattices, and the generation and the relations are one theorem.

Observed also in `dzackgarza/research` at `9cfdecf73d`:
`research/lattice-theory/classification/two-elementary-discriminant-forms.md`,
the paragraph introducing $p$, $q$, $u$, $v$.

**Banned:** "Here $p$ and $q$ are the two rank-one forms on $\ZZ/2\ZZ$,
realized as the discriminant forms of $\generators{2}$ and
$\generators{-2}$, while $u$ and $v$ are the two rank-two forms on
$(\ZZ/2\ZZ)^2$, realized as the discriminant forms of $U(2)$ and of $V =
V_1$ respectively.".

**Preferred:** a definition block "$p\definedas A_{\generators{2},q}$,
$q\definedas A_{\generators{-2},q}$, $u\definedas A_{U(2),q}$,
$v\definedas A_{V,q}$ for the lattice $V$ of [@Nik80, Prop. 1.8.1]" with
the Gram matrix of $V$ displayed and the names $q^{(2)}_{\pm1}(2)$,
$u^{(2)}_+(2)$, $v^{(2)}_+(2)$ of the source given once; then the
theorem that these generate the finite $2$-elementary quadratic forms
under $\perp$, with the relations displayed [@Nik80, §1.8].

## `DEF-42`: Variants of one construction are its fibers and parameter values

Several notions defined by nearly identical paragraphs — the same
construction for bilinear and for quadratic forms, for each value module,
for each type of lattice — are one construction with a parameter. Define
the general construction once, at its owner (`SEC-12`), and obtain each
variant by an established categorical operation: the fiber of a
projection over a parameter value, the pullback along a monomorphism,
the category of elements of a presheaf, the factorization of a map
through a subobject. "Define $\mathcal Q$ similarly" and a second
paragraph that repeats the first with one letter changed both hide that
the variants are related, and they make every later statement about the
relation a comparison of two unrelated definitions. The elementary
variant is recovered as a proposition from the general construction, not
defined first and generalized later (`DEF-38`, `TERM-18`).

Observed in `dzackgarza/research` (working tree over `26d4e303bc`):
`research/category-theory/framework/Bilinear-and-Quadratic-Forms.md`,
definition "Form categories";
`research/lattice-theory/Isometries-and-Arithmetic-Invariants.md`,
definition "Bilinear and quadratic discriminant representations".

**Banned:** "define $\mathcal B_{R,W}$ to have pairs $(M,b)$ with
$b\in\Bil_{R,W}(M)$ and morphisms … satisfying $b_M=b_N\circ(f\otimes_Rf)$.
Define $\mathcal Q_{R,W}$ similarly from $\operatorname{Quad}_{R,W}$";
two parallel paragraphs "Let $I_L\injects\Orth(A_L)$ be the image
subobject. Then $1\to\widetilde\Orth(L)\to\Orth(L)\to I_L\to1$ is exact"
and "Let $I_{L,q}\injects\Orth(A_{L,q})$ be the image subobject. … Then
$1\to\widetilde\Orth(L)\to\Orth(L)\to I_{L,q}\to1$ is exact".

**Preferred:** "$\mathcal B_{R,W}:=\int\Bil_{R,W}$ and
$\mathcal Q_{R,W}:=\int\operatorname{Quad}_{R,W}$, the categories of
elements of the presheaves $\Bil_{R,W}$ and $\operatorname{Quad}_{R,W}$
on $R\text{-}\mathbf{Mod}$", with $\mathcal B_{R,W}$ also the fiber of
$p_{\mathrm{Bil}}\colon\mathbf{BilMod}_R\to R\text{-}\mathbf{Mod}$ over
$W$; "$\rho_{L,q}$ is the factorization of $\rho_L$ through the
monomorphism $j_q\colon\Orth(A_{L,q})\hookrightarrow\Orth(A_L)$, and its
exact sequence is the pullback of the sequence for $\rho_L$ along $j_q$"
— one construction, the variant as an operation on it.

Two notions defined by one pattern are written by one pattern, in one
display. Defining one as an instance of the pattern and the other by a
different route — one as a representable functor and the other
pointwise, one declared functorial and the other not — hides that the
two theories are parallel, and turns the comparison map between them,
which is one map between representing objects, into a comparison of two
unrelated definitions (`PR-77`).

Observed in `dzackgarza/research`,
`research/category-theory/framework/Bilinear-and-Quadratic-Forms.md`
(working tree over `57c8eb1cb0`), definition "Bilinear and quadratic
form presheaves".

**Banned:** "define
$$\Bil_{R,W}(M)\definedas\Hom_{R\text{-}\mathbf{Mod}}(M\tensor_RM,W).$$"
beside "Let $\operatorname{Quad}_{R,W}(M)$ be the $R$-module, under
pointwise operations, of maps $q\colon M\to W$ for which
$q(rx)=r^2q(x)$ and" … "Pullback defines the presheaf
$\operatorname{Quad}_{R,W}\colon(R\text{-}\mathbf{Mod})^{\opop} \to R\text{-}\mathbf{Mod}$."
with no presheaf declared for $\Bil_{R,W}$.

**Preferred:** one display,
```latex
\begin{aligned}
\Bil_{R,W}(M)&\definedas\Hom_{R\text{-}\mathbf{Mod}}(M\otimes_RM,W),\\
\operatorname{Quad}_{R,W}(M)&\definedas\Hom_{R\text{-}\mathbf{Mod}}(\Gamma^2_R(M),W),
\end{aligned}
```
"both presheaves $(R\text{-}\mathbf{Mod})^{\opop}\to R\text{-}\mathbf{Mod}$
by pullback", with the citation for the second divided power
$\Gamma^2_R$ [Roby, *Lois polynômes et lois formelles en théorie des
modules*, 1963] at its first occurrence, and the polarization
$\operatorname{Quad}_{R,W}\to\Bil_{R,W}$ as precomposition with the one
map $M\otimes_RM\to\Gamma^2_R(M)$.

The norm shell and its primitive part are the same pair: the shell is a
hom-set in $\mathbf{BilMod}_\bZ$ and the primitive shell is its
subobject of primitive morphisms, and defining the shell as a fiber of
$q_L$ and the primitive shell as a set of embeddings makes two unrelated
objects of one inclusion (`DEF-48`).

Observed also in `dzackgarza/research`,
`research/lattice-theory/basic-invariants.md` (review working text over
`9cfdecf73d`), the definition of the norm shells.

**Banned:** "$L[n]\definedas q_L^{-1}(n), \qquad
L^{\mathrm{prim}}[n]\definedas\operatorname{PrimEmb}(\generators{n},L)$".

**Preferred:**
"$L[n]\definedas\Hom_{\mathbf{BilMod}_\bZ}(\generators{n},L)$, with
$L[n]\isoto q_L^{-1}(n)$, $f\mapsto f(1)$, and
$L^{\mathrm{prim}}[n]\definedas\operatorname{PrimEmb}(\generators{n},L)\subseteq
L[n]$ the subobject of primitive morphisms".

## `DEF-43`: A counting invariant is defined from the structure it counts

A class set, class number, mass, or orbit count is a shadow of a
classifying structure: the set of isomorphism classes is $\pi_0$ of a
groupoid, the class number is the cardinality of that set, the mass is
the groupoid cardinality $\sum_{[x]}1/\cardinality{\operatorname{Aut}(x)}$.
Define the structure first — the groupoid, with its objects and
morphisms, in the framework the document uses for the equivalence
relation (`DEF-41`) — and derive each count from it by the standard
operation (`NOT-1`, `DEF-9`). A count defined directly as "the number
of classes" has no object to be an invariant of, cannot be compared
with the stabilizers it secretly weights, and leads to a "weighted
count" being introduced as a new construction when it is the groupoid
cardinality of a structure already on the page (`NOT-4`). A set called
a group is the same defect in a word (`TERM-7`).

Observed in `dzackgarza/research`,
`research/dissertation/sections/1-part-combinatorial/2-chapter-lattice-theory/300-classification.md`
at `2b758e124b`, definition "Genus of a Lattice"; the preferred form is
the same repository's `research/lattice-theory/Isometries-and-Arithmetic-Invariants.md`
(working tree over `2b758e124b`), definition "Genus and class set", and
`research/lattice-theory/discriminant-forms-and-genus.md`, definition
"Mass of a lattice genus".

**Banned:** "We define the **class group** $\cl(L)$ to be the set of
isometry classes within a genus, and the **class number** as the size
of $\cl(L)$" — a set named a group, a count with no structure under it,
and a genus that is an equivalence relation on lattices rather than a
groupoid of them.

**Preferred:** "the **genus groupoid** $\operatorname{Gen}(L)$ is the
full subgroupoid of $\mathbf{Lat}_R^{\mathrm{nd},\simeq}$ on the
lattices in the genus of $L$; its **class set** and **class number**
are $\Cl(L):=\pi_0\operatorname{Gen}(L)$ and
$\cl(L):=\cardinality{\Cl(L)}$"; "when $\operatorname{Gen}(L)$ is
essentially finite, its **mass** is the groupoid cardinality
$\cardinality{\operatorname{Gen}(L)}=\sum_{[M]\in\Cl(L)}1/\cardinality{\Orth(M)}$"
[Baez–Dolan, *From finite sets to Feynman diagrams*, 2001; Conway–Sloane,
*Sphere Packings, Lattices and Groups*, Ch. 16] — each count an
operation on the groupoid, with the genus itself defined as in `DEF-41`.

The same distinction governs the embedding object: $\Emb(S,L)$, its
orbit set $\Orth(L)\backslash\Emb(S,L)$, and the double quotient
$\Orth(L)\backslash\Emb(S,L)/\Orth(S)$ are three objects, and
"describing $\Emb(S,L)$ amounts to classifying the $\Orth(L)$-orbits"
passes from the first to the second in a verb (`FORM-10`).

Observed in `dzackgarza/research`,
`research/lattice-theory/embeddings-and-overlattices.md` at
`ab530c1dcc`, the remark under "Equivalence of embeddings".

**Banned:** "Since an equivalence identifies $\iota_1(S)$ with
$\iota_2(S)$ as sublattices of $L$, describing $\Emb(S, L)$ amounts to
classifying the $\Orth(L)$-orbits of primitive sublattices of $L$
isometric to $S$, together with the choice of isometry onto each such
sublattice."

**Preferred:** "$\Orth(L)\backslash\operatorname{PrimEmb}(S,L)$ is the
set of $\Orth(L)$-orbits of primitive embeddings;
$\Orth(L)\backslash\operatorname{PrimEmb}(S,L)/\Orth(S)$ is the set of
orbits of primitive sublattices isometric to $S$" — each quotient
named, the passage between them a map.

## `DEF-44`: A block has one lede, and the lede comes first

A fenced block exists for one sentence: the definiens, the assertion, or
the instance. That sentence is the first sentence after the hypotheses
needed to parse it. Auxiliary objects the sentence uses are defined in
their own earlier block or recalled with a link (`XREF-6`, `DEF-45`);
the construction that witnesses the assertion is the proof (`SEC-16`,
`SEC-18`); consequences are propositions after the block (`DEF-16`); a
second claim is a second sentence, not a subordinate clause. The test:
delete every sentence of the block but one. If no single surviving
sentence is the block's reason to exist, the block is setup, a
construction, or a remark wearing a block type (`PR-64`, `EX-2`). The
tells: the defined term or the claim arrives after "Then" at the end of
a paragraph of "Put" and "Define" constructions; the content-carrying
sentence is subordinated to a construction — "under this isomorphism,
$\id_X$ corresponds to …", "therefore … is determined by …"; "the
analogous statement holds for $Y$" closes the block and asserts nothing
checkable, where the statement for $Y$ is one more sentence.

Observed in `dzackgarza/research`:
`research/lattice-theory/embeddings/orthogonal-complements.md` (working
tree over `57c8eb1cb0`), propositions "Splitting an isotropic
orthogonal complement" and "Discriminants of orthogonal sums";
`research/lattice-theory/discriminant-forms-and-genus.md` at
`57c8eb1cb0`, definition "Spinor genera and their class numbers";
`research/category-theory/framework/Categorical-Foundations.md` at
`ab530c1dcc`, definition "Representable presheaves" and theorem "The
Yoneda lemma".

**Banned:** a proposition whose statement reads "By
@prop:primitive-characterization there exists a retraction
$$\epsilon\colon L\too\bZ,\qquad\epsilon\circ\iota_v=\id_{\bZ}.$$ Put
$$\epsilon_v\definedas\epsilon\circ\kappa_v\colon v^{\perp_L}\too\bZ.$$
Then $$\epsilon_v\circ\lambda_v=\id_{\bZ},$$ so the exact sequence of
@prop:primitive-isotropic-complement splits in
$\bZ\text{-}\mathbf{Mod}$." — the claim is the last clause, and the
construction before it is the proof; "Then $N_q(L)=N_q$ and the
analogous orthogonal-sum isometry holds for the quadratic discriminant
forms after postcomposition by the $u_{q,i}$."; a definition block that
opens "Define $\Theta(V_p)$ by the short exact sequence" and reaches the
spinor genus several sentences later; "The presheaf $F$ is
*representable* if there is an object $X$ and a natural isomorphism
$F\cong\Hom_C(-,X)$. Under this isomorphism, $\id_X$ corresponds to the
universal element." — the universal element defined in a subordinate
clause; a theorem block whose assertion is its trailing sentence "A
representation is therefore determined by its universal element, and
two representations of the same functor are related by a unique
isomorphism compatible with the universal elements."

**Preferred:** "**Proposition.** The exact sequence of
@prop:primitive-isotropic-complement splits in
$\bZ\text{-}\mathbf{Mod}$." with the retraction $\epsilon$ and the
section constructed in the proof; two stated claims,
"$N_q(L_1\perp\dots\perp L_n)=\operatorname{lcm}_iN_q(L_i)$, and
$u_q\colon A_{L_1\perp\dots\perp L_n,q}\isoto\perp_iA_{L_i,q}$ is an
isometry"; $\Theta(V_p)$ in its own definition block, then
"**Definition.** The **spinor genus** of $L$ is …" as the first
sentence of the next; "the **universal element** of a representation
$\eta\colon\Hom_C(-,X)\isoto F$ is $\eta_X(\id_X)\in F(X)$"; a theorem
opening "A representation $(X,\eta)$ of $F$ is determined by its
universal element: for representations $(X,\eta)$ and $(X',\eta')$
there is a unique isomorphism $X\isoto X'$ carrying $\eta_X(\id_X)$ to
$\eta'_{X'}(\id_{X'})$."

## `DEF-45`: Recall a notion at its general owner; define the special case through it

A notion already defined on a class that contains the current objects
or their components — the length of a module, an elementary $p$-group,
the divisibility ideal of a vector, the exponent of a finite group — is
not defined again where a lattice-theoretic instance of it is needed.
The general notion is recalled with a link to its defining occurrence
(`XREF-6`), and the lattice notion is defined as the general notion
evaluated on the component: "$\ell(L):=\ell(A_L)$"; "$L$ is
**$p$-elementary** when $A_L$ is an elementary $p$-group
(@def-elementary-module)". A local redefinition creates a second
defining occurrence of one notion (`NOT-6`, `NOT-3`), detaches the
lattice notion from the theory that owns the general one, and can
define a different notion under the owner's symbol: a gloss "the
minimal number of generators" written beside $\ell$, when $\ell$
denotes composition length at its owner, puts two invariants that agree
only on elementary abelian $p$-groups under one symbol. When the
lattice theory needs the other invariant — the minimal number of
generators of $A_L$ of [@Nik80] — that invariant is defined at its own
owner under its own name, and the lattice notion is defined through it.
The same mechanism governs a property of a structured object that is a
property of its underlying module (`FORM-11`, `TERM-19`): it is
defined once for modules and applied, not re-spelled per structure.
The companion rule `SEC-19` governs classical notions that need no
definition in the document at all.

Observed in `dzackgarza/research` (working tree over `57c8eb1cb0`):
`research/lattice-theory/discriminant-forms-and-genus.md`, the
definition of the discriminant length beside definition "Discriminant
bilinear and quadratic forms";
`research/lattice-theory/Lattices-and-Discriminant-Forms.md`,
definition "$p$-elementary lattices".

**Banned:** "The **discriminant length** is
$$\ell(L)\definedas\ell\qty{A_L^\sharp},$$ the minimal number of
generators of the finite-length $\bZ$-module $A_L^\sharp$." — $\ell$ on
the right is the length of a module, defined elsewhere, and the gloss
redefines it; "A $\bZ$-lattice $S$ is **$p$-elementary** when its
discriminant carrier module is elementary:" followed by a restatement
of the elementary condition.

**Preferred:** "Recall (@def-length) that $\ell(A)$ is the length of a
finite-length $\bZ$-module $A$. The **discriminant length** of $L$ is
$\ell(L):=\ell(A_L)$."; "$L$ is **$p$-elementary** when $A_L$ is an
elementary $p$-group (@def-elementary-module), equivalently when
$pA_L=0$" — the general notion owned elsewhere, the lattice notion as
its evaluation.

## `DEF-46`: A local–global condition is one adelic condition over the base ring

A condition quantified over places — "for every place $v$ of $K$", "for
every prime $p$", "$\sigma_p$ for every prime $p$, with $\sigma_p$ the
identity for almost all $p$" — is one condition on one object over the
adelic ring: the profinite completion
$\widehat R=\prod_{\mathfrak p}R_{\mathfrak p}$, the restricted product,
or the adele ring $\mathbb A_K$. The place-by-place family is the
projection of that object onto its components, a corollary of the
adelic statement, and the construction is stated over the document's
base ring $R$ with $\bZ$ as the specialization (`PR-72`, `PR-71`,
`DEF-38`, `TERM-18`). Writing the family in place of the object leaves
the group that acts, the double coset that counts, and the exact
sequence that measures the obstruction unnamed, so the theory built on
them — class sets, spinor genera, the Hasse principle — is reached by
prose instead of by the standard constructions. A quantifier over
places where a module over the adelic ring is meant is the tell;
"lattices in the same rational quadratic space" is a second: it names
no map, where the datum is an isometry $L\otimes_RK\isoto M\otimes_RK$
(`EV-11`).

Observed in `dzackgarza/research`:
`research/lattice-theory/Isometries-and-Arithmetic-Invariants.md`
(working tree over `57c8eb1cb0`), definition "Genus and class set";
`research/lattice-theory/discriminant-forms-and-genus.md` at
`57c8eb1cb0`, definition "Spinor genera and their class numbers".

**Banned:** the genus as the "full subgroupoid on lattices $M$
satisfying $M\otimes_RK_v\isoto L\otimes_RK_v$ for every place $v$ of
$K$"; "elements $\sigma_p\in\Theta(V_p)$ for every prime $p$, with
$\sigma_p$ equal to the identity for almost all $p$, such that"; "in
the same rational quadratic space" for two lattices with no isometry of
their ambient spaces named.

**Preferred:** "$\operatorname{Gen}(L)$ is the full subgroupoid of
$\mathbf{Lat}_R^{\mathrm{nd},\simeq}$ on the lattices $M$ with
$M\otimes_R\widehat R\cong L\otimes_R\widehat R$ in
$\mathbf{Lat}_{\widehat R}$ and
$M\otimes_RK_\sigma\cong L\otimes_RK_\sigma$ at the archimedean places
$\sigma$"; the class set as the double coset space
$O(V)\backslash O(V_{\mathbb A})/O(L_{\mathbb A})$ [O'Meara,
*Introduction to Quadratic Forms*, §§101–102]; the spinor genus through
the spinor norm on $O^+(V_{\mathbb A})$, an element of the restricted
product $\prod'_{\mathfrak p}\Theta(V_{\mathfrak p})$ being one object;
"for an isometry $\varphi\colon L\otimes_RK\isoto M\otimes_RK$".

## `DEF-47`: A property is defined on the structure, never through a derived invariant or a witness

A derived invariant is computed from the structure by a construction
that is itself a theorem of the subject, under hypotheses of its own.
Defining a property through the invariant inverts the dependency: the
property exists only where the invariant does, the proposition that the
invariant detects the property becomes vacuous, and the definition does
not transfer to the category where the construction is native
(`DEF-41`, `DEF-39`, `TERM-18`). The same inversion defines a property
by the existence of auxiliary data — a lift, a refinement, a chosen map
— when the property is a condition on the structure already present.
The definition is the condition on the structure's own components,
stated as a containment, an equality of maps, or the vanishing of a
term in a sequence, never as a quantified statement about elements. The
invariant characterization and the existence of the witness follow as
propositions, each with the hypotheses under which it holds, and a
chapter that specializes the structure instantiates the condition and
restates nothing (`DEF-45`, `PR-45`).

Observed in `dzackgarza/research`:
`research/category-theory/framework/Bilinear-and-Quadratic-Forms.md`
at `57c8eb1cb0`, definition "Definiteness", and (working tree over
`57c8eb1cb0`) definition "Symmetry, alternation, and evenness";
`research/lattice-theory/Lattices-and-Discriminant-Forms.md` at
`ab530c1dcc`, and (working tree over `57c8eb1cb0`), definition "Even
lattices".

**Banned:** "- *degenerate* if $r>0$;" with $r$ read off the
signature; "Let multiplication by $2$ have image factorization
$$W\xrightarrow{2}W=W\twoheadrightarrow2W\injects W.$$ The form $b$
is **even** when there is a quadratic map
$\widetilde q_b\in\operatorname{Quad}_{R,2W}(M)$ for which"; "A
$\bZ$-lattice is *even* if $b(x,x)\in2\bZ$ for every $x\in L$."; "An
integral lattice $L$ is **even** when $$q_{\beta_L}\colon L\too\bZ$$
factors through $$2\bZ\injects\bZ$$".

**Preferred:** "$b$ is **degenerate** when $\radic(b)\neq0$" with the
radical in its sequence (`DEF-39`), and "over a field,
$\operatorname{rank}\radic(b)$ is the third entry $r$ of the
signature" as the proposition; at the owner of bilinear modules, "$b$
is **even** when $\operatorname{Val}(b)\subseteq2W$", and "when $2$ is
a nonzerodivisor on $W$, $b$ is even exactly when $b=b_q$ for a unique
$q\in\operatorname{Quad}_{R,W}(M)$" as the proposition; at the lattice
chapter, "an **even lattice** is a lattice whose form is even
(@def:form-axioms)", with $W=\bZ$ instantiated and nothing restated.

The parity invariant $\delta$ of a $2$-elementary lattice is the same
defect with a quadratic morphism as the witness: the definition
quantifies over morphisms $q_L^{(2)}$ into $\bZ/2\bZ$ whose existence a
proposition decides, and the witness reads $q_L$ in a codomain it does
not have (`SYM-16`). The invariant is defined by the values of $q_L$,
and the factorization through $i_{2,L}$ is the proposition.

Observed also in `dzackgarza/research` at `9cfdecf73d`:
`research/lattice-theory/classification/two-elementary-lattices.md`,
theorem "Nikulin's classification of indefinite even $2$-elementary
lattices".

**Banned:** "Define $\delta(L)=0$ when there exists a quadratic morphism
$q_L^{(2)}\colon A_L^\sharp\too\bZ/2\bZ$ for which" the triangle
"commutes, and set $\delta(L)=1$ otherwise.".

**Preferred:** "$\delta(L)=0$ when $\operatorname{Val}(q_L)\subseteq
i_{2,L}(\bZ/2\bZ)$, and $\delta(L)=1$ otherwise [@Nik80, §3.6]" in a
definition block, and "$\delta(L)=0$ if and only if $q_L$ factors
through $i_{2,L}$" as the proposition.

## `DEF-48`: The general construction, its composite with the reduction functor, then the special cases as examples

A construction native to a general category is defined there once,
with its universal property and its sequence. The version on a
subcategory is not a second definition: it is the composite of the
general construction with the reduction functor into the subcategory,
and it is defined for every object the general version is, not only for
the objects the special case has in view. The cases the literature
names are then examples of the composite, and every later statement —
exactness, functoriality, idempotence, a double-complement identity —
is proved once for the composite and inherited by every case. Two
defects lie on this gradient. The special case is defined first,
elementwise and in the subcategory alone, so that nothing is inherited
and the general case is never recovered (`DEF-41`, `TERM-18`). Or the
general case is stated and the special case is then re-defined beside
it, by a formula and a sentence saying what the formula "is", so that
the relation between the two is prose the reader must verify (`SEC-12`,
`DEF-42`, `PR-76`). The orthogonal complement below is one instance;
the same gradient governs every construction that a specialization
restricts.

Observed in `dzackgarza/research`:
`research/dissertation/sections/1-part-combinatorial/2-chapter-lattice-theory/100-foundations.md`
at `ab530c1dcc`, proposition "Primitive Isotropic Vectors,
Divisibility, and Hyperbolic Splittings";
`research/category-theory/framework/Bilinear-and-Quadratic-Forms.md`
(working tree over `57c8eb1cb0`), definition "Nondegenerate
reduction".

**Banned:** "$$T\definedas S^{\perp}=\theset{v\in L\st\beta(v,S)=0}$$"
as the definition of the orthogonal complement; "If $L$ is
nondegenerate and $$\iota\colon T\injects L$$ is an isotropic
sublattice over the commutative ring $R$, then in lattice-theoretic
notation
$$T^\perp\definedas\bigl(T^\perp_{\mathbf{BilMod}_R}\bigr)^{\mathrm{nd}}.$$
Thus the orthogonal complement in the lattice category is the
nondegenerate reduction of the right orthogonal-complement kernel in
$\mathbf{BilMod}_R$."

**Preferred:** the kernel sequence of $\iota^*\circ b^\sharp$ as the
definition of $N^{\perp_M}$ in $\mathbf{BilMod}_R$; the display
$$(-)^{\perp}\definedas(-)^{\mathrm{nd}}\circ(-)^{\perp_{\mathbf{BilMod}_R}}$$
as the definition of the orthogonal complement on monomorphisms of
$\mathbf{Lat}_R$, for every sublattice; the example "for
$\iota\colon J\injects L$ primitive and isotropic,
$J^{\perp_L}=(J^{\perp_{\mathbf{BilMod}_R}})^{\mathrm{nd}}$, and
$J\injects\radic(J^{\perp_{\mathbf{BilMod}_R}})$ is an isomorphism"
with its proof.

## `DEF-49`: A theory is developed at the base ring of its objects

### Yes/no example: integral eigensublattices

**No:** "Then $(L^G)_{\mathbb Q}$ and $(L_G)_{\mathbb Q}$ are the
images of the complementary idempotents" as the entire conclusion
of a proposition about integral invariant and coinvariant lattices.

**Yes:** Let $L=\langle1\rangle\perp\langle1\rangle$, with orthogonal
basis $e_1,e_2$, and let $I(e_1)=e_2$, $I(e_2)=e_1$.
For $G=\langle I\rangle$, the integral kernels are
$$
\begin{aligned}
L^G=\ker(I-\mathrm{id}_L)&=\langle e_1+e_2\rangle_{\mathbb Z},\\
L_G=\ker(I+\mathrm{id}_L)&=\langle e_1-e_2\rangle_{\mathbb Z}.
\end{aligned}
$$
Here $L_G$ denotes $(L^G)^{\perp L}$. For the sum of the inclusions
$j\colon L^G\perp L_G\hookrightarrow L$, the module sequence is
$$
0\longrightarrow U_{\mathrm{mod}}(L^G\perp L_G)
\xrightarrow{U_{\mathrm{mod}}(j)}U_{\mathrm{mod}}(L)
\xrightarrow{\pi}\mathbb Z/2\mathbb Z\longrightarrow0,
\qquad \pi(ae_1+be_2)=a+b\pmod2.
$$
The rational projections $\tfrac12(\mathrm{id}\pm I)$ send $e_1$ to
$\tfrac12(e_1\pm e_2)$. These are outside $L$, and
$\operatorname{coker}(U_{\mathrm{mod}}(j))\cong\mathbb Z/2\mathbb Z$
records the failure of the integral direct-sum decomposition.

**Test:** the conclusion computes the integral sublattices and the
integral obstruction before discussing rational projections.
$U_{\mathrm{mod}}$ is the forgetful functor to
$\mathbb Z\text{-}\mathbf{Mod}$. Sources: live Zettlr annotations
`d9d3d866-9291-46ae-9a8e-73f2436fa3b2`,
`31b67515-5436-44c4-8531-4b8bff568a2f`, and
`8a731c50-e3e5-4c4d-bf38-10b32dff2a2f`, quoted manuscript passages.

A theory of $R[G]$-modules is developed by constructions available over
$R$: kernels and images of $R[G]$-endomorphisms, saturations, orthogonal
complements, and the sublattices they cut out. Scalar extension to
$K=\operatorname{Frac}(R)$, the primitive central idempotents of $K[G]$,
auxiliary cokernels, their torsion, and pullbacks along them are steps
of a proof or the content of a base-change proposition (`MA-16`); they
are not the objects a definition displays. The test: the first object a
definition block displays lives in the category the chapter's theorems
are stated in. Renaming the ring, $A_G\definedas\bZ[G]$, while every
construction still passes through $\bQ\otimes_\bZ A_G$ is the overshoot:
the notation changed and the level did not. The vocabulary follows the
level: the objects are $\bZ[G]$-modules, not "rational
$G$-representations"; the algebra whose idempotents a proof uses is
named, "the group algebra $\bQ[G]$", with the isotypic decomposition
cited [@Ser77, §2.6]; the involution's idempotents $\tfrac12(1\pm g)$
are the case $G=\bZ/2$ of that decomposition (`TERM-18`). The boundary
with `DEF-41`: that rule asks for the global object in place of its
local description; this rule asks for the object over the ring the
theorem names in place of the object over its field of fractions.

Observed in `dzackgarza/research`,
`research/lattice-theory/invariant-and-coinvariant-lattices.md` (review
working text over `9cfdecf73d`), definition "Integral isotypic
sublattices" and the proof following it; (annotated review proposal over
`9cfdecf73d`) the proposition on the complementary idempotents and the
definition opening with $V\definedas L_\bQ$.

**Banned:** "let $A_G\definedas\bZ[G]$ be its group ring regarded as a
$\bZ$-algebra" followed by "For each simple $\bQ\tensor_\bZ A_G$-module
class $\chi$, let $e_\chi$ be the corresponding primitive central
idempotent of $\bQ\tensor_\bZ A_G$. Choose $d_\chi\in\bZ_{>0}$ such that
$a_\chi\definedas d_\chi e_\chi$ belongs to $A_G$, and let $f_\chi\colon
L\to L$ be the induced $A_G$-module endomorphism. Put
$Q_\chi\definedas\operatorname{coker}(f_\chi)$ and let
$t_\chi\colon\operatorname{tor}(Q_\chi)\hookrightarrow Q_\chi$ be its
torsion submodule" as the definition of the isotypic sublattice; "the
simple rational $G$-representations" for the simple $\bQ[G]$-modules;
"Then $(L^G)_\bQ$ and $(L_G)_\bQ$ are the images of the complementary
idempotents" as a proposition about $L^G$ and $L_G$; "$e_\chi\in
Z(\bQ[G])$" with the algebra $\bQ[G]$ unnamed; "Put $V\definedas L_\bQ$,
and" opening a definition of integral objects.

**Preferred:** "$L^G=\Hom_{\bZ[G]}(\bZ,L)$ and $L_G=(L^G)^{\perp_L}$" as
the definitions (`SEC-12`); for the isotypic sublattices,
"$L_\chi\definedas\ker\qty{d_\chi-a_\chi\colon L\to L}$" for the element
$a_\chi=d_\chi e_\chi\in\bZ[G]$, with "$(L_\chi)_\bQ=e_\chi L_\bQ$" as
the proposition that follows it; Maschke's theorem cited [@Ser77, §1.3]
at the step of the proof that uses the complement.
