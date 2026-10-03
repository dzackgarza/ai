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
(`DEF-28`). A definition that contains its own counterexample, warning, or
example cannot be cited, linked, or included elsewhere as the defining
occurrence without dragging them along.

**Banned:** a "::: {#def-modules-over-ring}" block whose last sentence is
"For a general ring, an equivalence between left and right module
categories is additional data …"

**Preferred:** close the definition after its defining sentences, then
write "::: {.Remark}" or a plain paragraph for the warning. The
definition is citable; the remark is separate.

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
