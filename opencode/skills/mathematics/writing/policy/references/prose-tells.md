# Prose tells (`PR-*`)

Bad prose on its own terms. The fix is a rewrite.

## `PR-1`: Self-narration

The prose describes what the document is or does instead of doing it.

**Banned:** "This is the framework that situates the conversion; it is
mathematics, not procedure."

**Preferred:** "The specified forgetful functor, its pullbacks, and the
intersections of replete full subcategories used in the Sage-to-Lean
conversion." State the content; do not characterize the text.

## `PR-2`: Reflexive negative parallelism

A notion is characterized by contrast with the alternative it rejects:
"X, not Y" / "is X, never Y" / "not just X but Y" / "X rather than Y"
— including manufactured negative parallelism of the form "their mere
existence supplies no $X$," which negates an expectation no one held.
Existence of objects never supplies an order, a comparison, or extra
structure unless one is defined; stating that it does not is true by
default and adds no claim to the skeleton (SEC-6). The contrast sounds
substantive while carrying no content, and it wastes the reader's
attention on a strawman.

**Banned:** "$a = b$ is a theorem, never a definitional identity";
"Their mere existence supplies no order relation among them" — when
several targets are available, the comparison data are either a chosen
target or a functor comparing the targets; that existence alone supplies
no order is the default and states nothing.

**Preferred:** state the positive claim and stop. "When several targets
are available, the comparison data are either a chosen target or a
functor comparing the targets." If the contrast carries information
(e.g. a genuine non-example where an expected order fails), make it a
Remark and explain the precise obstruction in context.

## `PR-3`: Self-certification

The text asserts it satisfies a property — dependency order, completeness,
minimality, "the single source", "canonical", "self-contained" — which no
sentence can make true.

**Banned:** "The definitions and results, in dependency order."

**Preferred:** delete the assertion. If the property is required, record it
where an auditor checks it against the artifact.

## `PR-4`: Theory of mind

The prose tells the reader what the mathematics implies or how to read it.

**Banned:** "equality, isomorphism, and equivalence are distinguished and
named wherever the distinction is content."

**Preferred:** delete. Distinct definitions are already distinct.

## `PR-5`: Puffery and AI-vocabulary

Words that rate the mathematics or belong to the generic LLM register.

**Banned:** "crucial", "pivotal", "powerful", "elegant", "deep", "rich",
"intricate", "interplay", "robust", "seamless", "leverage", "delve",
"underscore", "showcase", "boasts", "foster", "meticulous", "tapestry",
"testament", "landscape", "realm", and the connectives "it is worth noting",
"importantly", "note that", "of course", "clearly" (where it is not).

**Preferred:** delete the word; state the content plainly.

## `PR-6`: Cadence padding

Structure produced for rhythm.

**Banned:** the reflexive rule of three, "not only … but also", formulaic
transitions opening successive sentences ("Additionally", "Moreover",
"Furthermore", "Notably"), conclusion-restatement ("in summary", "as we have
seen"), em-dash or parenthetical density.

**Preferred:** keep what is needed; cut what is there for cadence.

## `PR-7`: Concept defined by notational payoff

A theorem or property is characterized by its effect on notation rather than
by its mathematical content, using a conversational construction ("is what
licenses", "is what allows", "is what lets us") instead of stating the
theorem and deriving the convention from it.

**Banned:** "Coherence is what licenses the notation
$a_1\otimes\cdots\otimes a_n$ without parentheses."

**Preferred:** "By the coherence theorem, any two parenthesizations of
$a_1 \otimes \cdots \otimes a_n$ are connected by a unique composite of
associators, so the expression is independent of parenthesization;
parentheses are omitted." State the theorem — what is well-defined, and in
what sense — then let the notational convention follow as a consequence.
A standard text may explain that a theorem permits a notational shorthand;
it does not define the theorem as that shorthand's justification.

## `PR-8`: Superficial "-ing" analysis

A trailing participial clause performs analysis without adding content.

**Banned:** "the pullback is universal, underscoring the classifier's role."

**Preferred:** delete the clause, or replace it with the statement it gestures
at — a theorem, a cross-reference, an actual consequence.

## `PR-9`: Construction and verification in one sentence

A single sentence simultaneously constructs an object and verifies its
required properties, hiding the logical structure the reader needs to follow.

**Banned:** "A category with finite products is monoidal with
$a\otimes b$ a chosen product $a\times b$ and $e$ a terminal object, the
three isomorphisms being the unique ones commuting with the projections; this
is the cartesian monoidal structure."

**Preferred:** separate the construction from the verification. "The product
functor $\times\colon\mathcal{C}\times\mathcal{C}\to\mathcal{C}$, together
with a terminal object $\mathbf{1}$ as unit, defines a monoidal structure
on $\mathcal{C}$. The associator $\alpha_{a,b,c}$ and the unitors
$\lambda_a$, $\varrho_a$ are the unique isomorphisms supplied by the
universal property of the product." State the functor, then verify the
axioms. A reader follows construction, then verification; a semicolon-joined
sentence conflates them.

## `PR-10`: Undue emphasis

`**bold**` or `*italic*` used to weight a clause, or bold used to mark a
defined term, is undue emphasis. A term is marked only at its defining
occurrence, with the house mark for a definiendum (`DEF-26`). Bold appears
only as a run-in label that names a case at the start of a list item or
paragraph, and ends with a period. A remark, example, or proof is a numbered
block, not a paragraph with a run-in label (`SEC-2`).

**Banned:** "**Tonelli** applies when $f \geq 0$."; "the **ideal sheaf**
is …" outside its definition; "**Remark.** …" as a paragraph.

**Preferred:** "**Tonelli.** For $f\ge0$ and $\sigma$-finite measures, …";
"**In $\mathbf{Set}$.** …".

## `PR-11`: Formatting tells

**Banned:** Title Case in headings; curly quotes; emoji; collaborative or
meta language ("let me know", "I hope this helps"); bold-header bullet lists
where prose is clearer.

**Preferred:** sentence case in headings; straight quotes; no emoji; no
collaborative or meta language.

## `PR-12`: Project process inside mathematical exposition

A mathematical chapter pauses to discuss rulings, audit procedure,
implementation status, or editorial policy.

**Banned:** "This ruling guards the conversion pipeline and is enforced by
the audit."

**Preferred:** state the mathematical proposition. Project process belongs in
agent-facing files, not in a mathematical chapter.

## `PR-13`: "Is an invariant of X" for factoring through a quotient

A map that factors through a quotient or truncation — through
$\pi_0(S^\simeq)$, through a set of isomorphism classes, through a
coarse moduli space — is described in prose as "is an invariant of
isomorphism classes" or "is an invariant of $X$". The phrase names no
domain, no factorization, and no map; the reader cannot determine what
factors through what. State the factorization.

**Banned:** "so $K_0^{\otimes}$ is an invariant of isomorphism
classes."

**Preferred:** "$K_0\colon\mathbf{SymMonCat}\to\mathbf{Ab}$ factors
through $\pi_0\colon\mathbf{SymMonCat}\to\mathbf{Set}$,
$S\mapsto\pi_0(S^\simeq)$." Name the domain, the quotient, and the
factorization. If the factorization is the definition, do not restate it
as an additional property.

## `PR-14`: "Is functorial for X" for being a functor

A functor is described in prose as "is functorial for symmetric monoidal
functors" or "is functorial for $X$ morphisms" instead of being stated
as a functor with its source and target category. The phrase names no
domain, no codomain, and no action on morphisms. State the functor.

**Banned:** "and is functorial for symmetric monoidal functors."

**Preferred:** "$K\colon\mathbf{SymMonCat}\to\mathbf{Spectra}$ is a
functor (hence $K_0 = \pi_0\circ K\colon\mathbf{SymMonCat}\to\mathbf{Ab}$
is a functor)." State the source, the target, and the functor. If the
object was defined as a functor, functoriality is not an additional
property to be asserted in prose.

## `PR-15`: Prose paraphrase of a precise categorical statement

A precise categorical statement — a factorization through a quotient or
$\pi_0$, a functor with source and target, a commutative diagram, a tuple
with its constituents, a natural transformation with its naturality square
— is paraphrased in loose English instead of being stated precisely. The
prose is simultaneously wordier and less precise: it names no domain, no
codomain, no diagram, and the reader cannot reconstruct the precise
statement. State the precise statement.

**Banned:** "is an invariant of isomorphism classes and is functorial for
symmetric monoidal functors"; "relating $\gamma$ to $\alpha$"; "commuting
with the projections"; "is what licenses the notation
$a_1\otimes\cdots\otimes a_n$ without parentheses."

**Preferred:** "factors through $\pi_0\colon S\mapsto\pi_0(S^\simeq)$";
"$K\colon\mathbf{SymMonCat}\to\mathbf{Spectra}$ is a functor"; draw the
hexagon diagrams; state the tuple
$(\mathcal{C},\otimes,\mathbf{1},\alpha,\lambda,\varrho)$; "any two
parenthesizations are connected by a unique composite of associators."
PR-13, PR-14, EV-8, AX-1, and PR-7 are instances of this general pattern:
a precise statement was replaced by a loose English description that is
longer and carries less information.

## `PR-16`: "Additional data" for a precise moduli of equivalences

A passage states that a comparison "is additional data" or "does not
follow merely from notation" instead of stating what the extra structure
is and what classifies it. The phrase names no data and no moduli, and
"does not follow from notation" negates a premise no one holds: no
mathematician thinks an equivalence
$\mathbf{LMod}_R\simeq\mathbf{RMod}_R$ would follow from writing $R$ on
the left versus on the right. State the structure: there is no canonical
equivalence; an equivalence is equivalent to the data of an invertible
bimodule, a Morita equivalence, an
$\mathbb{E}_1$-equivalence $R\simeq R^{\mathrm{op}}$, or whichever
structure is relevant, and state the universal property that classifies
it.

**Banned:** "an equivalence between left and right module categories is
additional data; it does not follow merely from notation."

**Preferred:** "there is no canonical equivalence
$\mathbf{LMod}_R\simeq\mathbf{RMod}_R$; such an equivalence is equivalent
to the data of an invertible $(R,R)$-bimodule, and in particular to an
$\mathbb{E}_1$-equivalence $R\simeq R^{\mathrm{op}}$ when it is induced
by an anti-automorphism." Name the data and the classification; do not
paraphrase existence of structure as English about notation.

## `PR-17`: Negating a strawman premise about notation

A precise negative existence statement — "there is no canonical
equivalence $\mathbf{LMod}_R\simeq\mathbf{RMod}_R$" — is replaced by
meta-commentary negating a premise no one holds: "it does not follow
merely from notation that …" No mathematician thinks notation produces
equivalences; the notation $\mathbf{LMod}_R$ versus $\mathbf{RMod}_R$
already distinguishes them. The strawman is fabricated — it exists only
to be corrected — and the sentence is incoherent because the premise it
negates is not a view anyone holds. The default for a general
($\mathbb{E}_1$) $R$ is not that an equivalence exists and needs data; it
is that no such equivalence exists. State the precise negative existence
and the moduli when an equivalence does exist.

**Banned:** "it does not follow merely from notation that left and right
module categories are equivalent" — negates a strawman; no one claimed
notation would make them equivalent. "An equivalence is additional data;
it does not follow from notation" — frames existence as the default that
merely needs data, when the default is non-existence.

**Preferred:** "there is no canonical equivalence
$\mathbf{LMod}_R\simeq\mathbf{RMod}_R$; an equivalence, when it exists,
is equivalent to …" State the theorem, not commentary on what notation
does not do.

## `PR-18`: Patronizing dialectic for a sophisticated audience

The reader is the audience that the house conventions declare. Where a
document adopts DEF-12 and DEF-13, that reader is comfortable with
$\infty$-categories, $\mathbb{E}_1$- and $\mathbb{E}_\infty$-ring spectra,
$\mathbf{LMod}_R$ versus $\mathbf{RMod}_R$, derived stacks, and
homotopy types. That reader already distinguishes $\mathbb{E}_1$ from
$\mathbb{E}_\infty$ and left modules from right modules. A passage that
manufactures a naive reader — "you might think $R$ on the left versus on
the right gives an equivalence, but it does not follow merely from
notation" — and then corrects that reader is patronizing. Even if the
premise were coherent, the corrective "you might think $X$, but you would
be wrong" positions the author above a reader who needs to be warned not
to confuse notation with mathematics. A mathematician does not need that
warning; the precise statement already trusts the reader to understand it.

**Banned:** "it does not follow merely from notation that …" — lectures a
reader who already knows $\mathbf{LMod}_R\neq\mathbf{RMod}_R$ as
$\infty$-categories over a general $\mathbb{E}_1$-ring. "For a general
ring, one might expect left and right modules to coincide, but this
requires additional data."

**Preferred:** state the precise theorem and trust the reader:
"there is no canonical equivalence
$\mathbf{LMod}_R\simeq\mathbf{RMod}_R$ for a general
$\mathbb{E}_1$-ring spectrum $R$." Do not manufacture a naive position to
knock down; do not explain what notation does not do. The document assumes
the sophistication of its intended audience (modern graduate courses at
Harvard, MIT, and Princeton; Lurie, Scholze, Gaitsgory, Haynes Miller)
and does not rehearse warnings appropriate to a first encounter with the
distinction.

## `PR-19`: Logical connective without entailment

A logical connective — "therefore," "hence," "so," "it follows that" —
asserts a consequence. A passage that writes "An $(A,B)$-bimodule
therefore has forgetful functors …" asserts that the bimodule has
forgetful functors as a consequence of the previous line (that a right
module is a left $A^{\mathrm{op}}$-module). The functors are part of the
definition of a bimodule, not a consequence. Do not join a definition to
its own constituent data with a consequence marker.

**Banned:** "A right $A$-module is a left $A^{\mathrm{op}}$-module. An
$(A,B)$-bimodule therefore has forgetful functors …"

**Preferred:** "A right $A$-module is a left $A^{\mathrm{op}}$-module. An
$(A,B)$-bimodule is … It has forgetful functors …" State the definition;
state its data. Use "therefore" only for an actual entailment.

## `PR-20`: "Identifies conventions" with no mathematical content

A passage states that an identity or equivalence "identifies $X$ and $Y$
conventions" or "identifies the two notions" without naming any functor,
equivalence, or natural isomorphism. "Identifies conventions" names no
mathematical object — no map, no domain, no codomain — and has no
mathematical meaning. The precise statement is a canonical equivalence of
categories or a natural isomorphism, with source, target, and how it is
produced.

**Banned:** "the identity $A=A^{\mathrm{op}}$ identifies left and right
$A$-module conventions."

**Preferred:** "the symmetry induces a canonical equivalence
$\mathbf{LMod}_A\simeq\mathbf{RMod}_A$." Name the functor or equivalence;
do not describe it as "identifying conventions."

## `PR-21`: Definition missing "is … if …" and quantifier, redundant qualifier

A property is defined as "finitely generated: some $R^n\twoheadrightarrow
M$ is surjective" — no "M is … if …", no quantifier for $M$ or $n$, and
redundant "is surjective" after $\twoheadrightarrow$ (which already means
surjective). A property that defines a replete full subcategory is stated
as "$M$ is $P$ if …" with $M$ bound and the quantifiers explicit; the
surjection is written $R^n\to M$ or declared surjective without doubling
the word.

**Banned:** "finitely generated: some $R^n\twoheadrightarrow M$ is
surjective" — $M$ unbound, no "is … if …", redundant "is surjective."

**Preferred:** "$M\in\mathbf{LMod}_R$ is finitely generated if there
exists a finite set $I$ and an effective epimorphism
$\bigoplus_{i\in I}R\twoheadrightarrow M$." Bind $M$, state the
quantifiers, and do not double the surjectivity marker.

## `PR-22`: "Some … is …" for $\exists$

A property quantified by "there exists" is written as "some
$R^n\twoheadrightarrow M$ is surjective" — colloquial quantification that
picks a morphism $R^n\to M$ and then asks whether that already-surjective
arrow is surjective. Standard sources write the quantifier explicitly and
do not double the surjectivity marker ($\twoheadrightarrow$ already means
surjective).

**Banned:** "finitely generated: some $R^n\twoheadrightarrow M$ is
surjective."

**Preferred:** "there exists a finite set $I$ and an effective
epimorphism $\bigoplus_{i\in I}R\twoheadrightarrow M$" (classical shadow:
"there exists $n$ and a surjection $R^n\to M$"). State "there exists"
and the surjection once; do not write "$\twoheadrightarrow$ is
surjective."

## `PR-23`: "Accompanied by its comparison" for a specified $2$-cell

An alternative factorization's comparison with the distinguished one is
described as "is accompanied by its comparison with this composite"
instead of naming the natural transformation or equivalence and its source
and target. "Is accompanied by" is the "carries"/"transports" metaphor
(EV-7) for an unnamed $2$-cell and hides whether the comparison is a
morphism of factorizations, a natural transformation, or an equivalence.

**Banned:** "An alternative forgetful functor is accompanied by its
comparison with this composite."

**Preferred:** "An alternative factorization
$(H',G',\alpha')$ of the same $F$ comes with a specified comparison
$2$-cell $\gamma\colon(H',G',\alpha')\Rightarrow
(H_{\mathrm{dist}},G_{\mathrm{dist}},\alpha_{\mathrm{dist}})$ in
$\mathbf{Fact}_D(F)$, i.e. natural equivalences
$H'\simeq H_{\mathrm{dist}}$ and $G'\simeq G_{\mathrm{dist}}$ compatible
with $\alpha',\alpha$." Name the $2$-cell, its source, and its target.

## `PR-24`: Self-referential meta-prose about the text's structure, notation, or theorems

A professional mathematics text extremely rarely is self-referential,
describes its own structure, notation, or what its theorems do or do not
do. If ever such things are included, they are at best very small
footnotes, but should be avoided altogether. Prose that talks about the
text — "is defined in @def-…; it is …" (where the definition lives),
"This theorem does not redefine $F$ or $D_P$" (what the theorem does not
do), "Their mere existence supplies no order relation" (what existence
does not do), "is what licenses the notation $a_1\otimes\cdots\otimes a_n$"
(what the theorem does for notation), "A construction whose value happens
to agree on underlying sets … names the functor" and "If no comparison is
specified, $F$ and $G$ remain distinct" (writing requirements as closing
morals), "is additional data; it does not follow merely from notation"
(what notation does not do, with strawman) — is meta-prose, not
mathematics. The text states the mathematics via fenced units and links;
it does not describe its own structure.

Concrete standard: Hartshorne, EGA, Lurie *Higher Topos Theory* and
*Higher Algebra*, Riehl *Category Theory in Context* state definitions,
theorems, and examples with fenced units and parenthetical `\ref`s; they
do not narrate where a definition lives, what a theorem does not
redefine, or what notation does not imply. Cross-references via
`\ref`/`\longref`/`@` are not self-reference; they are citations.

**Banned:** all of the above meta-sentences as running prose inside
mathematical $\S$'s.

**Preferred:** state the mathematics — a fenced `::: {#def-...}` with the
term in italics, a Proposition with proof exhibiting the factorization, an
Example, a Remark attached to its primary unit — and link with
`(\ref{def-...})` or "Recall that … (\ref{def-...})". If a notational
clarification is truly needed, put it in a footnote `[^1]` and keep it to
one clause, but prefer to avoid it by stating the mathematics precisely.

## `PR-25`: "Names the …" for specifies/exhibits/is equipped with

"Names" has no established mathematical meaning — nothing in mathematics
"names" anything else. A construction does not "name the functor along
which it is created," "name the comparison," or "name the factorization."
The standard verbs for extra structure on a construction each have a clear
a priori mathematical meaning: **specifies** (gives the data),
**exhibits** (provides a witness), **is given by** (is presented as),
**is equipped with** / **comes with** (carries as extra structure),
**determines** / **is determined by** (is equivalent to the data),
**is witnessed by**, **is classified by** (when there is a classifying
object). If a verb is used for extra structure, it must have that clear
meaning.

**Banned:** "names the functor along which it is created"; "names the
comparison with this composite"; "names the factorization"; "names a
particular monomorphism."

**Preferred:** "specifies the functor $\bar F$ and the equivalence
$\alpha\colon F\simeq i\circ\bar F$"; "exhibits the factorization
$(\bar F,\alpha)$"; "is equipped with the comparison $2$-cell
$\gamma$"; "is determined by the invertible bimodule"; "comes with a
specified natural equivalence"; "specifies a particular monomorphism
$f\colon A\rightarrowtail B$ with $\operatorname{isMono}(f)$" / "is
equipped with a chosen monomorphism." Use "determines" / "is determined
by" only when the data are equivalent.

## `PR-26`: "Some … exists is a proposition" with unbound variables and no truncation

An existence statement "some monomorphism $A\to B$ exists is a
proposition" leaves $A,B$ unbound (SYM-1), writes "some … exists" for
$\exists$ (PR-22), and calls the existence "a proposition" without
stating the truncation level. In the document a proposition is a
$(-1)$-truncated type (a mere proposition); the structure is the type
$\sum_{f\colon A\to B}\operatorname{isMono}(f)$, and the proposition
(mere existence) is its $(-1)$-truncation
$\bigl\|\sum_{f}\operatorname{isMono}(f)\bigr\|_{-1}$.

**Banned:** "The assertion that some monomorphism $A\to B$ exists is a
proposition" — $A,B$ unbound, "some … exists" for $\exists$, no type for
the monomorphisms, no $(-1)$-truncation.

**Preferred:** "Let $A,B\in\mathcal{C}$. The type
$\sum_{f\colon A\to B}\operatorname{isMono}(f)$ is the structure of a
monomorphism $A\rightarrowtail B$; its $(-1)$-truncation
$\bigl\|\sum_{f}\operatorname{isMono}(f)\bigr\|_{-1}$ is the proposition
that there merely exists a monomorphism $A\rightarrowtail B$."

## `PR-27`: Long prose where concise notation already exists

Concise notation already encodes the universal property. "Pullback of $f$
along $y$" and $X\times_Y 1$, $M\otimes_A N$ for $\operatorname{Hom}(M\otimes_A
M,W)$, $\bigoplus_{i\in I}R$ for $R^{(I)}$, a tuple
$(\mathcal{C},\otimes,\mathbf{1},\alpha,\lambda,\varrho)$ for a monoidal
category — each replaces a paragraph of English. Using long prose where
that notation exists bloats the text and is the general pattern behind
"the apex of the cartesian square" for $X\times_Y 1$, "a map
$M\times M\to W$ that is $A$-bilinear" for $M\otimes_A M\to W$ (MA-14),
and "a choice of $a\otimes b$ for every $a,b$" for the functor
$\otimes\colon\mathcal{C}\times\mathcal{C}\to\mathcal{C}$ (MA-13).

**Banned:** "the fiber of $f$ over $y$ is the apex of the cartesian
square"; "let $b\colon M\times M\to W$ be $A$-bilinear" for
$b\colon M\otimes_A M\to W$; "a monoid for the cartesian structure."

**Preferred:** "the fiber is the pullback $X\times_Y 1$ of $f$ along $y$";
"$b\colon M\otimes_A M\to W$"; "a monoid object in
$(\mathcal{C},\times,\mathbf{1})$." Use the concise notation that already
exists for the precise object.

## `PR-28`: "Requires a stated descent/local-to-global theorem with its hypotheses" is not a theorem

Meta-commentary that a conclusion requires a theorem with hypotheses
contributes no fenced unit to the skeleton (SEC-6) and says a theorem
must exist instead of stating it. The standard is to state the descent
theorem with its hypotheses once, then apply it — not to warn that one
is needed.

Vacuous generality is the other half: "a conclusion about $L$ from
either image" quantifies over no specified conclusion (isomorphism,
projectivity, rank, form, basis), no specified images (under which
functors $B\otimes_A^L-$), and no specified hypotheses (faithfully flat,
finite presentation, etc.). Each conclusion has different hypotheses; no
single sentence covers them. "Either image" is false as stated — one
image $L\otimes_{\mathbb Z}\mathbb Z_p$ alone never recovers $L$; descent
recovers $L$ from the collection plus gluing.

Concrete standards (state one, then apply it):

* **fpqc descent for $\mathbf{LMod}$** [@Stacks-023N, Tag 023N; Lurie
  DAG, descent for $\mathbf{LMod}_R$]: for faithfully flat
  $R\to S$, $\mathbf{LMod}_R \xrightarrow{\sim}
  \lim\bigl(\mathbf{LMod}_S \rightrightarrows \mathbf{LMod}_{S\otimes_R
  S} \substack{\to\\ \to\\ \to} \cdots\bigr)$ via
  $M\mapsto S\otimes_R^L M$ with descent datum. In particular,
  $M\simeq N$ in $\mathbf{LMod}_R$ iff $S\otimes_R^L M\simeq
  S\otimes_R^L N$ compatibly.

* **Beauville–Laszlo / Milnor patching for $\mathbb Z$**:
  for $M\in\mathbf{LMod}_{\mathbb Z}$ finitely presented,
  $M \simeq (M\otimes_{\mathbb Z}^L\mathbb Z_p)\times_{M\otimes_{\mathbb
  Z}^L\mathbb Q_p}(M\otimes_{\mathbb Z}^L\mathbb Q)$ as a pullback in
  $\mathbf{LMod}_{\mathbb Z}$; equivalently $M$ is recovered from the
  pair $(M\otimes_{\mathbb Z}\mathbb Z_p, M\otimes_{\mathbb Z}\mathbb Q)$ plus an identification
  over $\mathbb Q_p$. Hypotheses: finite presentation (or perfect) for
  the pullback to be exact; without it the square need not be cartesian.

* **Local-to-global for lattices:** $L\simeq L'$ as $\mathbb Z$-lattices
  iff $L\otimes_{\mathbb Z}\mathbb Z_p\simeq L'\otimes_{\mathbb Z}\mathbb Z_p$ for all $p$ and
  $L\otimes_{\mathbb Z}\mathbb Q\simeq L'\otimes_{\mathbb Z}\mathbb Q$ compatibly over
  $\mathbb Q_p$ — a conjunction, not "either image."

**Banned:** "A conclusion about $L$ from either image requires a stated
descent or local-to-global theorem with its hypotheses."

**Preferred:** "::: {#thm-descent} **Theorem (fpqc descent).** For
faithfully flat $R\to S$, $R\to S$ is of effective descent for
$\mathbf{LMod}$: $M\mapsto S\otimes_R^L M$ induces
$\mathbf{LMod}_R\simeq\lim \mathbf{LMod}_{S^{\otimes_R\bullet+1}}$. In
particular, for finitely presented $M,N$, $M\simeq N$ iff the base
changes are compatibly isomorphic. :::" Then: "::: {#cor-ZpQ} By
Beauville–Laszlo, for finitely presented $M$,
$M\simeq (M_p)\times_{M_{\mathbb Q_p}}(M_{\mathbb Q})$. Hence
$L\simeq L'$ iff … :::" State which conclusion, which images, which
theorem, which hypotheses; then apply it. Do not state that a theorem is
required.

## `PR-29`: Vague "either" / "a conclusion" with unquantified hypotheses

"A conclusion," "either image," "some theorem with its hypotheses" are
unbound: no domain, no codomain, no quantifier, no hypothesis list. This
is the general form of PR-28 and of PR-22 ("some … is …" for $\exists$):
using English indefinite for a mathematical quantifier so that no claim
is falsifiable. Each "a" hides a $\forall$ or $\exists$ and a condition.

**Banned:** "A conclusion about $L$ from either image requires a stated
descent or local-to-global theorem with its hypotheses"; "some
$R^n\twoheadrightarrow M$ is surjective" (PR-22); "the relevant
pullbacks" (DEF-31).

**Preferred:** quantify: "For every finitely presented $M$ and every
faithfully flat $R\to S$, $M\simeq0$ iff $S\otimes_R^L M\simeq0$";
"There exists a finite set $I$ and an effective epimorphism
$\bigoplus_{i\in I}R\twoheadrightarrow M$"; "For the pullback squares
exhibiting $X\times_Y 1$ in {#def-pullback}." Write $\forall$/$\exists$
and the hypothesis list; do not use "a"/"either"/"relevant"/"some"
standing for them.

## `PR-30`: Indefinite "a conclusion" with no proposition is unfalsifiable

"A conclusion about $L$" names no proposition: no quantified statement,
no domain, no codomain, no property (isomorphism, projectivity, rank,
form, freeness). Any counterexample can be deflected as "not the
intended conclusion," and any true fact can be claimed ex post as the
intended one. A mathematical sentence is falsifiable because it states
which proposition is claimed; an indefinite noun phrase is not.

This is the general form behind PR-28/PR-29 and PR-22 ("some
$R^n\twoheadrightarrow M$ is surjective") and DEF-31 ("the relevant
pullbacks"): an English indefinite standing for a quantifier so that no
checkable claim is made.

**Banned:** "A conclusion about $L$ from either image requires …";
"A result about $M$ follows from …"

**Preferred:** state the proposition with quantifiers: "For finitely
presented $M$, $M\simeq0$ iff $S\otimes_R^L M\simeq0$ for faithfully
flat $R\to S$"; "For $\mathbb Z$-lattices $L,L'$,
$L\simeq L'$ iff $L\otimes_{\mathbb Z}\mathbb Z_p\simeq L'\otimes_{\mathbb Z}\mathbb Z_p$ for
all $p$ and $L\otimes_{\mathbb Z}\mathbb Q\simeq L'\otimes_{\mathbb Z}\mathbb Q$ compatibly
over $\mathbb Q_p$." Name the conclusion; do not use "a conclusion" /
"a result."

## `PR-31`: Tautological "with its hypotheses" does no mathematical work

"With its hypotheses" is true of every stated theorem and adds no
hypothesis list, no condition, and no check. It occupies the grammatical
slot where the hypotheses belong while stating none, so the sentence
cannot be used: a reader cannot verify, apply, or falsify it. It is the
same device as "under the appropriate conditions" or "where defined"
standing for the actual conditions.

**Banned:** "requires a stated descent or local-to-global theorem with
its hypotheses"; "holds with its hypotheses / under its hypotheses."

**Preferred:** either list the hypotheses ("for faithfully flat $R\to S$
and finitely presented $M$") or state the theorem that carries them
({#thm-descent} above). Do not add a clause that is true of every
theorem and therefore says nothing. If no specific hypotheses are meant,
delete the clause.

## `PR-32`: Internal doctrine and preemptive correction posing as mathematical content

A sentence whose only coherent audience is an internal contributor or
agent — "requires a stated theorem," "must be justified," "with its
hypotheses" as a reminder to include them — is contributor governance,
not mathematics. Importing it into the document leaks runtime control into
the text. Its rhetoric is a preemptive scolding: it assumes a frame in
which the reader has made or is about to make a mistake and corrects
that mistake before it is committed, though the reader never made it or
thought about making it. It does not address the reader as an equal
pursuing the mathematics, but as a lesser to be controlled, steered, and
corrected.

Standard mathematical prose never does this. A textbook states the
theorem with hypotheses, proves it, and applies it; it does not tell the
reader that a theorem is required or that hypotheses are required. The
governance belongs in `CONTRIBUTING.md`, not in the document.

This generalizes PR-24 (self-referential meta-prose about the text's
structure) and PR-16–18 (strawman negation of a premise no one held):
here the premise is that the reader would draw a conclusion about $L$
from one image without a theorem, which no reader in the document's
audience was going to do.

**Banned:** "A conclusion about $L$ from either image requires a stated
descent or local-to-global theorem with its hypotheses" in a
mathematical section; any sentence that tells the reader that a theorem,
proof, or hypothesis is required instead of giving it.

**Preferred:** in the document, state the mathematics: "::: {#thm-descent}
**Theorem.** … :::" then "By {#thm-descent}, for finitely presented $L$,
… holds because $R\to S$ is faithfully flat." In `CONTRIBUTING.md`,
state the governance once: "Every local-to-global conclusion is a
fenced Theorem with quantified hypotheses; do not draw it from one image
alone."

## `PR-33`: "Are distinct constructions" is true by definition — the claim is about the comparison map

$M\mapsto M\otimes_{\mathbb Z}^L\mathbb Z_p$ and
$M\mapsto \widehat M_p:=\lim_n M\otimes_{\mathbb Z}^L\mathbb Z/p^n$ are
different functors, defined differently. Saying they "are distinct
constructions" without or with a hypothesis states a tautology that
holds regardless. The substantive mathematics is whether the canonical
comparison map is an equivalence.

Concrete standards:

* **Scalar extension:** $-\otimes_{\mathbb Z}^L\mathbb Z_p\colon
  \mathbf{LMod}_{\mathbb Z}\to\mathbf{LMod}_{\mathbb Z_p}$ (underived
  $-\otimes_{\mathbb Z}\mathbb Z_p$ on discrete modules). Left adjoint
  to restriction.

* **$p$-adic completion:** $\widehat{(-)}_p:=\lim_n (-\otimes_{\mathbb
  Z}^L\mathbb Z/p^n)$ in $\mathbf{LMod}_{\mathbb Z}$, resp.
  $\lim_n M/p^nM$ for discrete $M$.

* **Comparison map:** the natural $c_M\colon M\otimes_{\mathbb Z}^L
  \mathbb Z_p \to \widehat M_p$ induced by
  $\mathbb Z_p\simeq\lim_n\mathbb Z/p^n$ and
  $M\otimes^L_{\mathbb Z}\lim_n\mathbb Z/p^n\to\lim_n(M\otimes^L_{\mathbb Z}\mathbb Z/p^n)$.

Do not state that the functors are distinct. State what $c_M$ does.

**Banned:** "Without the finite-generation hypothesis, scalar extension
and completion are distinct constructions."

**Preferred:** "::: {#thm-complete-vs-basechange} **Theorem.** For
$M\in\mathbf{LMod}_{\mathbb Z}$ perfect (in particular, for discrete
finitely generated $M$ over Noetherian $\mathbb Z$), $c_M\colon
M\otimes_{\mathbb Z}^L\mathbb Z_p \xrightarrow{\sim}\widehat M_p$ is an
equivalence; in particular $M\otimes_{\mathbb Z}\mathbb Z_p\simeq\widehat
M_p$ for discrete finitely generated $M$. :::" Then apply or refute:
"$c_M$ is not an equivalence in general: for
$M=\bigoplus_{\mathbb N}\mathbb Z$,
$M\otimes_{\mathbb Z}\mathbb Z_p=\bigoplus_{\mathbb N}\mathbb Z_p$ (finite support)
while $\widehat M_p$ strictly contains it; for $M=\mathbb Q$,
$\mathbb Q\otimes_{\mathbb Z}\mathbb Z_p\simeq\mathbb Q_p$ while
$\widehat{\mathbb Q}_p\simeq0$ [@Stacks-0A05, Tag 0A05; Lurie DAG, formal
completion]." Name the functors, the map, and the quantified
equivalence; do not say the definitions are distinct.

## `PR-34`: "Without the $H$ hypothesis" is true of every theorem with hypothesis $H$

"Without the finite-generation hypothesis, $A$ and $B$ are distinct / do
not coincide / fail" is true of any theorem "$H\Rightarrow A\simeq B$"
and therefore says nothing: it restates that the theorem has a
hypothesis (PR-31) while naming neither the theorem, the quantified $H$
(finitely generated vs. finitely presented vs. perfect vs. coherent),
nor the quantified claim $A\simeq B$ (which $A$, which $B$, which map),
so it is unfalsifiable (PR-30) and can be deflected to any intended
meaning.

This is the general form behind PR-28/PR-31: a sentence that is true
by definition of "distinct constructions" or true by logic of
"theorems have hypotheses," and hence vacuous.

**Banned:** "Without the finite-generation hypothesis, scalar extension
and completion are distinct constructions"; "Without $H$, $A$ and $B$
are different."

**Preferred:** state the quantified theorem with $H$ and the comparison
map (PR-33), then state the quantified failure without $H$ with a
counterexample: "Without finite generation $c_M$ need not be an
equivalence; e.g. $M=\bigoplus_{\mathbb N}\mathbb Z$ as above." Do not
use "without $H$, $A$ and $B$ are distinct" standing for a theorem plus
a counterexample.

## `PR-35`: Stating the complement of a positive coincidence theorem is obviated

Once $A$ and $B$ are presented as distinct constructions — here
$-\otimes_{\mathbb Z}^L\mathbb Z_p$ and $\widehat{(-)}_p$ with different
definitions — their distinctness as definitions is already established;
no sentence is needed to say they are distinct. Stating the positive
quantified theorem with the comparison map (PR-33) — "$c_M\colon
M\otimes^L_{\mathbb Z}\mathbb Z_p\to\widehat M_p$ is an equivalence for $M$ perfect
(in particular discrete finitely generated over Noetherian $\mathbb Z$)"
— already makes the complement implicit and obvious to any reader: without
$H$, the theorem does not apply and $c_M$ need not be an equivalence.
Adding "Without $H$, $A$ and $B$ are distinct" is structurally redundant:
it repeats what presentation already shows and what the quantified
theorem already delimits.

This is the general scaffolding principle behind SEC-8 and PR-33/PR-34:
present distinct objects as distinct, state when the canonical comparison
is an equivalence with quantified $H$ and the map, and stop — the
failure outside $H$ is then understood without being stated, and a
counterexample is given only when it teaches (e.g. $M=\bigoplus_{\mathbb
N}\mathbb Z$, $M=\mathbb Q$ in PR-33), not as a separate tautological
sentence.

**Banned:** "Without the finite-generation hypothesis, scalar extension
and completion are distinct constructions" alongside the definitions and
"For finitely generated $M$, $M\otimes_{\mathbb Z}\mathbb Z_p\simeq\widehat M_p$."

**Preferred:** present the two functors with different definitions (hence
distinct), then state one quantified theorem with the map:
"::: {#thm-complete-vs-basechange} **Theorem.** … $c_M$ is an
equivalence for $M$ perfect … :::" No additional sentence is needed to
say they differ without $H$; the quantified theorem already obviates it.
Give a counterexample only as an illustration of the boundary, not as a
restatement that the definitions are distinct.

## `PR-36`: Negative framing bloats the text, ruins the tone, and undermines standard exposition structure

The general device behind PR-2, PR-16–18, PR-24, PR-28, PR-30–35, and
SEC-8: instead of the positive quantified statement the mathematics
requires, the text adds a negative sentence — "$a=b$ is a theorem,
never a definitional identity," "does not follow merely from notation,"
"is additional data," "their mere existence supplies no order relation,"
"requires a stated descent theorem with its hypotheses," "without $H$,
$A$ and $B$ are distinct constructions," "a conclusion about $L$ from
either image requires …" Each is a negation, a "without," or a
"requires" standing for a positive Definition or Theorem not stated.

Three costs, all general:

**1. Bloat.** A positive theorem $H\Rightarrow (c_M\text{ is an
equivalence via the named map})$ has infinitely many true negatives you
could state — without $H$ it need not hold, without $H_1$ it fails,
without notation it is not defined, existence alone supplies no relation,
etc. Stating any of them doubles the text while adding no fenced unit to
the skeleton (SEC-6). Standard exposition states the quantified positive
once and stops; the complements are implicit and obvious to any reader
who has read the definitions as distinct and the theorem as quantified.

**2. Tone.** Each negative assumes a reader who was about to make a
mistake — conflate $A$ and $B$, think notation supplies structure, draw
a conclusion from one image, think existence supplies order — and
corrects that mistake before it is made, though the reader never made it
or thought about making it. It does not address the reader as an equal
pursuing the mathematics, but as a lesser to be controlled, steered, and
corrected (PR-32). Standard prose never scolds preemptively; it states
the mathematics and lets the reader use it.

**3. Structure.** A negative sentence is not a Definition, Theorem, or
Example with a named map, quantified $H$ (perfect / finitely presented /
finitely generated, faithfully flat, etc.), and a checkable claim. It is
unfalsifiable (PR-30) — "a conclusion" names no proposition, "either
image" names no functor, "with its hypotheses" names no list — and often
true by definition ("are distinct constructions," PR-33) or true by logic
of "theorems have hypotheses" (PR-34, PR-31) and therefore contributes no
proof obligation while hiding that the actual obligation (name the map,
quantify $H$, state iso vs. not, give the boundary counterexample only
when it teaches) was not met. It is doctrine posing as content, leaking
contributor governance into the document.

Concrete standard: standard mathematical exposition is positive and
constructive — definitions as data/tuples
$(\mathcal{C},\otimes,\mathbf{1},\alpha,\lambda,\varrho)$ with
diagrams (SYM-1), theorems as quantified implications with the comparison
map, proofs, then boundary examples/counterexamples at the quantified
edge when they teach. Stacks Project, EGA, Serre, Hartshorne, Lurie
HTT/HA, EKMM never write "without $H$, $A$ and $B$ are distinct" or
"this requires a theorem with hypotheses"; they write
"::: {#thm-descent} **Theorem (fpqc descent).** For faithfully flat
$R\to S$, … :::" and "::: {#thm-complete-vs-basechange} **Theorem.**
$c_M$ is an equivalence for $M$ perfect … :::" and apply them.

**Banned:** "Without the finite-generation hypothesis, scalar extension
and completion are distinct constructions"; "A conclusion about $L$ from
either image requires a stated descent or local-to-global theorem with
its hypotheses"; "$a=b$ is a theorem, never a definitional identity";
"does not follow merely from notation"; "is additional data"; "their mere
existence supplies no order relation."

**Preferred:** delete every negative standing for a positive not stated,
and state the positive once, quantified, with the named map: present
$-\otimes^L_{\mathbb Z}\mathbb Z_p$ and $\widehat{(-)}_p$ with different
definitions (hence distinct), then one fenced theorem with $c_M$ and
quantified $H$ (PR-33), then apply it. No sentence is needed to say what
does not follow, what is not supplied, what is distinct without $H$, or
what is required. The positive theorem already says it, without bloat,
without condescension, and with a checkable claim.

## `PR-37`: Sign-posting "Fix $R$ and $W$, the value module of the forms below" is not a mathematical unit

A setup sentence that fixes variables for upcoming material — "Fix a
commutative ring $R$ and an $R$-module $W$, the $*$-module of the $*$s
below" — is an imperative to the reader to hold variables across a
section, not a Definition/Theorem/Example with a checkable claim. Delete
all glue and the skeleton must remain complete (SEC-6); here every form
below would then lose its $R,W$ quantifier, so the skeleton is
incomplete without glue. "Of the forms below" is a forward reference to
no specified label, names $W$ by a future description, and fixes a single
$W$ where the mathematics requires a *parameter* quantifying over
$\mathbf{LMod}_R$.

This is the general form behind SEC-8/PR-33: prose that holds variables
outside any fenced unit instead of quantifying them inside the unit that
uses them. It creates ambiguous scope — is $W$ fixed for the section,
the chapter, or one definition? — and forces later text to rely on
ambient context.

Concrete standards:

* **$W$-valued bilinear form:** for $R$ an $\mathbb E_\infty$-ring
  spectrum and $W,M\in\mathbf{LMod}_R$,
  a $W$-valued bilinear form on $M$ is a morphism
  $b\colon M\otimes_R M\to W$ in $\mathbf{LMod}_R$ (equivalently,
  $M\otimes_R^L M\to W$). For $R$ discrete and $M,W$ discrete, this is
  an $R$-bilinear $M\times M\to W$. The datum is the map $b$; $W$ is its
  codomain, varying with $b$, not a once-fixed module. Similarly a
  quadratic or symmetric form is a map from the appropriate
  classifying object for that flavour, valued in varying $W$.

* **Quantification belongs inside the unit.** Standard texts never write
  a free-floating "Fix $R$ and $W$ for below." They quantify inside
  each fenced unit or make the section header the formal quantifier.

**Banned:** "Fix a commutative ring $R$ and an $R$-module $W$, the value
module of the forms below" as a standalone setup sentence; "Fix $R$ for
the forms below; let $W$ be the value module."

**Preferred:** quantify inside the fenced unit, with varying $W$:

"::: {#def-bilinear} **Definition.** Let $R$ be a commutative ring (resp.
$\mathbb E_\infty$-ring spectrum) and let $W,M\in\mathbf{LMod}_R$. A
**$W$-valued bilinear form** on $M$ is a morphism
$b\colon M\otimes_R M\to W$ in $\mathbf{LMod}_R$. :::"

Or, when a section works over one $R$, make the header the quantifier
once and keep $W$ varying:

"::: {.Remark} Throughout §2, $R$ denotes a fixed commutative ring;
$W$ varies over $\mathbf{LMod}_R$ and all forms are $W$-valued as in
{#def-bilinear}. :::"

Do not fix a single $W$ for "the forms below"; let $W$ be a parameter
of the form. Do not forward-reference "below"; label the definitions
and refer to them.

## `PR-38`: "With pointwise operations" / "with its $R$-module structure via $W$" does zero work — $\mathbf{Mod}_R$ is enriched over itself

The $R$-module structure on a Hom is not an extra datum imposed pointwise
via the codomain $W$ that needs to be announced. For commutative $R$,
$\mathbf{Mod}_R$ is closed symmetric monoidal, hence enriched over
itself; $\operatorname{Hom}_R(M,N)\in\mathbf{Mod}_R$ is the internal hom,
full stop (stably $\mathbf{LMod}_R$ is closed symmetric monoidal for
$\mathbb E_\infty$ $R$; for general $\mathbb E_1$ $R$,
$\mathbf{LMod}_R$ is enriched over $\mathbf{Sp}$ and tensored over it).
Its underlying set is the set of $R$-linear maps and its $R$-action is
the canonical one — no "via $W$" and no alternative to contrast
"pointwise" with. "With pointwise operations" therefore occupies the slot
where a non-trivial structure would be specified while specifying no
choice, and mislocates the structure in the codomain.

This is the general form of PR-31 (tautological "with its hypotheses"):
a clause that restates what the ambient closed structure already gives,
so deleting it leaves the mathematics unchanged.

Concrete standard — state the closed structure once as scaffolding, then
there is nothing to say at the point of use:

* **Scaffolding (once, fenced, in the module-theory setup):**
  "::: {#thm-mod-closed} **Theorem.** For commutative $R$,
  $\mathbf{Mod}_R$ (resp. stably $\mathbf{LMod}_R$ for
  $\mathbb E_\infty$ $R$) is closed symmetric monoidal and self-enriched.
  In particular $\operatorname{Hom}_R(M,N)\in\mathbf{Mod}_R$ is the
  internal hom. :::" [@Stacks-0B8A; Lurie HA 4.2.1]

* **At the point of use:** no clause needed:
  "::: {#def-bil} **Definition.** Let $R$ be commutative and
  $W,M\in\mathbf{Mod}_R$. Put
  $\operatorname{Bil}_{R,W}(M):=\operatorname{Hom}_R(M\otimes_R M,W)$ as
  $R$-module. Its elements are the $R$-bilinear $M\times M\to W$. :::"
  The "as $R$-module" already is the self-enrichment; no "with
  pointwise operations" and no "structure via $W$."

The missing one-time scaffolding is what forced the filler: without
{#thm-mod-closed}, every Hom later needs a tautological qualifier to
compensate. Put the enrichment once where it belongs and every later
"with pointwise operations" / "with its $R$-module structure" is
obviated.

**Banned:** "Let $\operatorname{Bil}_{R,W}(M)$ be the $R$-module of
$R$-bilinear maps $M\times M\to W$, with pointwise operations";
"with its $R$-module structure via $W$ / induced by $W$."

**Preferred:** state {#thm-mod-closed} once in the module-theory setup;
then "Let $\operatorname{Bil}_{R,W}(M):=\operatorname{Hom}_R(M\otimes_R
M,W)$ be the $R$-module of $R$-bilinear maps $M\times M\to W$." No
trailing clause. If the reader needs the formula,
"$(b_1+b_2)(x,y)=b_1(x,y)+b_2(x,y)$" is a property of the internal hom,
not part of the definition.

## `PR-39`: Prose "the $R$-module of $R$-bilinear maps $M\times M\to W$" for $\operatorname{Hom}_R(M\otimes_R M,W)$

One symbol already is the $R$-module with its structure; the prose
paraphrase re-spells it in English and then needs a filler clause to
rebuild the structure (PR-38).

**Banned:** "Let $\operatorname{Bil}_{R,W}(M)$ be the $R$-module of
$R$-bilinear maps $M\times M\to W$, with pointwise operations."

**Preferred:** "Put $\operatorname{Bil}_{R,W}(M):=
\operatorname{Hom}_R(M\otimes_R M,W)$ as $R$-module" — or, if a name is
unneeded, just $\operatorname{Hom}_R(M\otimes_R M,W)$. Domain
($M\otimes_RM$), codomain ($W$), linearity, and $R$-module structure via
the self-enrichment ({#thm-mod-closed}) are already in the symbol; no
"$R$-bilinear," no "$M\times M\to W$," no "with pointwise operations"
to add. Stably
$\operatorname{Bil}_{R,W}(M):=\mathbf{RHom}_R(M\otimes^L_RM,W)$. This is
the standard: Stacks, Bourbaki, Lurie HA define $W$-valued bilinears as
the hom object from the tensor square and stop (PR-27 is the general
form: concise notation obviates prose).

## `PR-40`: Discussing "$R$-bilinear maps $M\times M\to W$" instead of standing on the tensor product

$R$-bilinear $M\times M\to W$ is not a primitive notion to re-describe
on each use; it is classified by the tensor product, defined once with
its universal property. Re-describing bilinears in prose on every
occurrence — checking "$R$-bilinear," listing "$M\times M\to W$," adding
"with pointwise operations" to make the set an $R$-module — chooses not
to stand on that one-time scaffolding and replicates it each time.

Concrete standards — state the scaffolding once, then use homs from the
tensor to encode bilinearity from then on:

* **Scaffolding (once, fenced, before any form):**
  "::: {#def-tensor} **Definition/Theorem.** For $M,N\in\mathbf{Mod}_R$
  there is $M\otimes_R N\in\mathbf{Mod}_R$ with a universal $R$-bilinear
  $M\times N\to M\otimes_R N$, i.e.
  $\operatorname{Hom}_R(M\otimes_R N,W)\cong R\text{-Bil}(M\times N,W)$
  naturally in $W\in\mathbf{Mod}_R$. :::"
  [@Stacks-0B8A; Lurie HA 4.2.1]

* **From then on, no "bilinear maps" prose:** a $W$-valued bilinear
  form on $M$ is a morphism $b\colon M\otimes_R M\to W$; its $R$-module
  of all such is $\operatorname{Hom}_R(M\otimes_R M,W)$ as $R$-module.
  Bilinearity, domain, codomain, and $R$-module structure are already in
  the Hom from the tensor; nothing to spell out, no clause to add.

Stably the same: $M\otimes^L_RM$ classifies derived bilinears,
$\mathbf{RHom}_R(M\otimes^L_RM,W)$ is the $R$-module of them.

**Banned:** "the $R$-module of $R$-bilinear maps $M\times M\to W$" as a
recurring definition; "$R$-bilinear maps $M\times M\to W$ with pointwise
operations" (PR-38) on each use.

**Preferred:** define $M\otimes_R M$ once via {#def-tensor}; then
"a $W$-valued bilinear form on $M$ is $b\colon M\otimes_R M\to W$"
and "$\operatorname{Bil}_{R,W}(M):=\operatorname{Hom}_R(M\otimes_R M,W)$."
Never re-describe bilinearity in prose once the tensor classifies it.

## `PR-41`: "Pullback … defines a presheaf $\mathbf{Mod}_R^{\mathrm{op}}\to\mathbf{Mod}_R$" is incoherent — pullback is not a presheaf, and one $f^*$ is not a functor

Unwrapping the abstract $(f\otimes_R f)^*$ as $f^*b(x,y)=b(fx,fy)$ is
pedagogically fine *after* the Hom is defined (PR-39/PR-40) — the
incoherence is not the element formula but the clause that the
pullback/formula "defines a presheaf."

* **Pullback** is a limit of $A\to C\leftarrow B$ in $\mathcal C$,
  $A\times_C B$, or as an operation the functor
  $f^*\colon\mathcal C_{/Y}\to\mathcal C_{/X}$ for $f\colon X\to Y$
  (more generally $\operatorname{Span}(\mathcal C)\to\mathcal C$). It is
  not a functor $\mathcal C^{\mathrm{op}}\to\mathbf{Set}$.

* **Presheaf** on $\mathcal C$ is a functor
  $\mathcal C^{\mathrm{op}}\to\mathbf{Set}$ (stably $\to\mathcal S$);
  $\mathcal C^{\mathrm{op}}\to\mathbf{Mod}_R$ is an
  $\mathbf{Mod}_R$-valued / $\mathbf{Mod}_R$-enriched presheaf via
  {#thm-mod-closed} (TERM-10). A limit / slice functor cannot be a
  presheaf — types do not match — and a single
  $f^*b(x,y)=b(fx,fy)$ for one $f$ cannot be a functor
  $\mathbf{Mod}_R^{\mathrm{op}}\to\mathbf{Set}$ / $\to\mathbf{Mod}_R$.

What is intended is the functoriality already in the Hom:
$M\mapsto\operatorname{Bil}_{R,W}(M)$ with
$(f\colon M\to N)\mapsto (f\otimes_R f)^*$. The element formula is the
unwrapping of that $(f\otimes_R f)^*$, not its definition.

Concrete standards [@Stacks-04E9, Tag 04E9; Lurie HTT 6.1] — state the
functor data explicitly, with types, domains, codomains, and referents:

**Banned:** "Pullback along $f\colon M\to N$ sends $b$ to
$f^*b(x,y)=b(fx,fy)$, and defines a presheaf
$\operatorname{Bil}_{R,W}\colon(R\text{-}\mathbf{Mod})^{\mathrm{op}}\to
R\text{-}\mathbf{Mod}$."

**Preferred:** "Put $\operatorname{Bil}_{R,W}(M):=
\operatorname{Hom}_R(M\otimes_R M,W)$ as $R$-module. For $f\colon M\to N$
in $\mathbf{Mod}_R$, put $f^*:=(f\otimes_R f)^*\colon
\operatorname{Bil}_{R,W}(N)\to\operatorname{Bil}_{R,W}(M)$. As a
functor $\mathbf{Mod}_R^{\mathrm{op}}\to\mathbf{Mod}_R$
($\mathbf{Mod}_R$-valued presheaf via {#thm-mod-closed}) it satisfies
$\mathrm{id}^*=\mathrm{id}$ and $(g\circ f)^*=f^*\circ g^*$ by Hom. On
elements, $(f^*b)(x,y)=b(f(x),f(y))$." Name on objects, on morphisms with
domain/codomain, and the element unwrapping; do not say a pullback or a
single $f^*$ "defines" the presheaf/functor.

## `PR-42`: Hand-waving a functor without naming types, domains, codomains, and referents

The general form behind PR-41, PR-30/PR-31, PR-37, and SYM-4–11: a
sentence that says a construction "defines a …" while naming no object
assignment, no morphism assignment with domain/codomain, no variance, no
enrichment, and no referent for each symbol ($b\in\operatorname{Bil}(N)$
vs. $f^*b\in\operatorname{Bil}(M)$, $f\colon M\to N$ in which
$\mathcal C$). The same device as "with its hypotheses" occupying the
hypothesis slot while stating none — here occupying the functor-data slot
while stating only one element formula.

Every functor $\mathcal C^{\mathrm{op}}\to\mathcal D$ owes, fenced where
it is introduced: (i) on objects $M\mapsto F(M)$ with its type in
$\mathcal D$, (ii) on morphisms $(f\colon M\to N)\mapsto F(f)\colon
F(N)\to F(M)$ with domain/codomain, (iii) element formula if
pedagogically useful as unwrapping of (ii), (iv) $\mathrm{id}$ and
composition. "Defines a presheaf/functor" with only (iii) for one $f$
does not define it.

**Banned:** any "…defines a presheaf/functor $\mathcal C^{\mathrm{op}}\to
\mathcal D$" with only an element formula and no object/morphism
assignments with types.

**Preferred:** as in PR-41 — state (i)–(iv) with types; reserve
"presheaf" for $\mathcal C^{\mathrm{op}}\to\mathbf{Set}$ ($\to\mathcal S$
stably) and otherwise say "$\mathbf{Mod}_R$-valued presheaf" / "functor
$\mathbf{Mod}_R^{\mathrm{op}}\to\mathbf{Mod}_R$" with the enrichment
from {#thm-mod-closed} named when needed.

## `PR-43`: Element-wise $b(x,y)=b(y,x)$, $b(x,x)=0$, $q(rx)=r^2q(x)$ for $b\circ\tau=b$, $b\circ\Delta=0$ — concrete shadow for the categorical diagram

Listing symmetric / skew / alternating / even as equalities on elements
$x,y\in M$ ties the notion to $\mathbf{Set}$-concrete $M$ with an
underlying set $U(M)$ and makes it inextensible to non-concrete
$\mathcal C$ — $\mathcal O_X\text{-}\mathbf{Mod}$, local systems,
$\mathbf{Sp}$, $\mathbf{Grpd}$, $\infty$-categories,
$\mathbf{Sch}_{/S}$, etc., where $x,y\colon 1\to M$ may not exist as set
elements. The element formulas are the *evaluation* of one diagram on
generalized elements, not the definition, and they elide the single
non-lax symmetric monoidal structure $(\otimes,1,\tau)$ that makes the
notion portable.

This is the general form of PR-39/PR-40 and TERM-11: re-describing in
prose on elements what the tensor classifier and the symmetry already
encode as a morphism.

Concrete standards — state the diagrammatic notion once via the
symmetric monoidal structure (non-lax: $\tau\colon M\otimes_R M\to
M\otimes_R M$ is an isomorphism with $\tau^2=\mathrm{id}$, not a lax
comparison), then derive the element formula as its unwrapping when
$U$ exists:

* **Scaffolding (once, fenced):** $(\mathbf{Mod}_R,\otimes_R,R,\tau)$
  (stably $(\mathbf{LMod}_R,\otimes^L_R,R,\tau)$) symmetric monoidal
  closed and self-enriched {#thm-mod-closed}, with $M\otimes_R M$
  classifying bilinears {#def-tensor}. Let $\tau_{M,M}\colon M\otimes
  M\to M\otimes_R M$ be the symmetry, $\Delta\colon M\to M\otimes_R M$ the
  diagonal for alternating, and $\Gamma^2_R(M)\xrightarrow{\gamma}
  \operatorname{Sym}^2_R(M)\to M\otimes_R M$ the divided-power classifier
  for even/quadratic.

* **$W$-valued bilinear $b\colon M\otimes_R M\to W$ is:**
  — **symmetric** if $b\circ\tau = b\colon M\otimes_R M\to W$;
  — **skew-symmetric** if $b\circ\tau = -b$;
  — **alternating** if $b\circ\Delta =0$ (equivalently $b\circ\tau=-b$
  and $b\circ\Delta=0$; in $2$ invertible alternating $=$ skew);
  — **even** if $b$ factors through $\operatorname{Sym}^2_R(M)$ and
  $b(x,x)\in2W$ is the element shadow of the factorization through
  $\Gamma^2_R(M)$ — never as primary.

  Stably the same with $\tau$ the symmetric monoidal braiding in
  $\mathbf{LMod}_R$.

* **Element unwrapping (only after, when $U$ exists):** for $x,y\colon
  R\to M$ in $\mathbf{Mod}_R$ (i.e. $x,y\in U(M)$), $b\circ\tau=b$
  evaluates to $b(x,y)=b(y,x)$, etc. This is a property of the diagram,
  not the definition.

**Banned:** "For $b\colon M\times M\to W$: $b$ is *symmetric* if
$b(x,y)=b(y,x)$; $b$ is *skew* if $b(x,y)=-b(y,x)$; $b$ is *alternating*
if $b(x,x)=0$; $b$ is *even* if $b(x,x)\in2W$" as definitions.

**Preferred:** "Let $b\colon M\otimes_R M\to W$ be $W$-valued bilinear.
$b$ is **symmetric** if $b\circ\tau=b$, **skew** if $b\circ\tau=-b$,
**alternating** if $b\circ\Delta=0$, **even** if $b$ lifts through
$\Gamma^2_R(M)$." Then, if pedagogically useful: "On elements this is
$b(x,y)=b(y,x)$, $b(x,x)=0$, etc., as the evaluation of those equalities
on $x\otimes y\colon R\to M\otimes_R M$."

## `PR-44`: "$b$ is *even* if $b(x,x)\in2W$" breaks the value-module abstraction just built

$W$ was introduced as a *parameter* varying over $\mathbf{Mod}_R$ (stably
$\mathbf{LMod}_R$) via $\operatorname{Hom}_R(M\otimes_RM,W)$ as
$R$-module ({#thm-mod-closed}, {#def-tensor}) — no elements, no
"$\in$." "$b(x,x)\in2W$" immediately concretizes that $W$ to
$U(W)$ with a subset $2W:=\operatorname{im}(2\colon W\to W)$, i.e. the
$\mathbf{Set}$-shadow of a diagram, meaningless stably (for
$\mathbf{LMod}_R$, $\mathbf{Sp}$, $\mathcal O_X\text{-}\mathbf{Mod}$
there is no "$\in$") and tied to $R=\mathbb Z$ with $2\in\mathbb Z$ acting
via $\mathbb Z\to R$. It re-describes as an element condition what the
classifier already encodes as a factorization.

This is the general form of PR-43 and PR-37/TERM-9: prose on elements
that collapses the abstraction just built for $W$-valued forms.

Concrete standard — evenness is a lift of the morphism
$b\colon M\otimes_R M\to W$, not a pointwise divisibility:

* **Classifiers (once, fenced):**
  $\Gamma^2_R(M)\xrightarrow{\gamma}\operatorname{Sym}^2_R(M)
  \twoheadrightarrow M\otimes_R M$ with $\tau$ on $M\otimes_R M$ as in
  PR-43; stably $\mathbf{\Gamma}^2_R(M)\to\mathbf{Sym}^2_R(M)$. Then
  $\operatorname{Quad}_{R,W}(M):=\operatorname{Hom}_R(\Gamma^2_R(M),W)$,
  $\operatorname{Sym}_{R,W}(M):=\operatorname{Hom}_R(\operatorname{Sym}^2_R(M),W)$,
  $\operatorname{Bil}_{R,W}(M):=\operatorname{Hom}_R(M\otimes_RM,W)$.

* **$W$-valued symmetric $b\colon M\otimes_RM\to W$ is even** if $b$
  factors through $\operatorname{Sym}^2_R(M)$ and lifts through
  $\Gamma^2_R(M)$ — equivalently $b$ is in the image of
  $\operatorname{Hom}_R(\operatorname{Sym}^2_R(M),W)$ and of
  $\operatorname{Hom}_R(\Gamma^2_R(M),W)$ via $\gamma^*$. No
  $b(x,x)\in2W$ to state; its evaluation on $x\colon R\to M$ when
  $U$ exists is $b(x,x)=2\cdot\tilde b(x)$ for some
  $\tilde b\in\operatorname{Hom}_R(\Gamma^2_R(M),W)$, whose shadow is
  "$\in2W$" only for discrete $W$ with $U$.

**Banned:** "$b$ is *even* if $b(x,x)\in2W$ for every $x$" as
definition while $W$ is the varying value module of
$\operatorname{Hom}_R(M\otimes_RM,W)$.

**Preferred:** "$b\colon M\otimes_RM\to W$ symmetric is **even** if it
lifts through $\Gamma^2_R(M)$ (i.e. $b$ is in the image of
$\operatorname{Hom}_R(\Gamma^2_R(M),W)\xrightarrow{\gamma^*}
\operatorname{Hom}_R(M\otimes_R M,W)$)." Then, only after and only for
discrete $W$ with $U$: "On elements this is $b(x,x)\in2W$."

## `PR-45`: Carrying $b(x,x)\in2W$ on every use instead of naming the governing $R$-submodule $\operatorname{Val}(b)\subseteq W$ — local thinking for a global object

The element condition is the unpacked shadow of one global $R$-submodule
of $W$. Carrying the shadow on every occurrence — "for every $x$,
$b(x,x)\in2W$," "check $b(x,x)\in2W$," etc. — never names the object that
governs the condition, so every argument must drop to $U(M)$ and re-check
at a point $x$. That re-expansion is where hand-waving enters: is $x$ in
$M$, in $U(M)$, in $M\otimes_R\kappa(p)$? Is $2W$ the image
$2\colon W\to W$ or the subset? Does it vary functorially in $W$? With
no $\operatorname{Val}(b)$ as an $R$-submodule there is nothing to make
precise, and the quantifier "for every $x$" can slide, exactly as "a
conclusion from either image" slid.

Naming the object once is the scaffolding that lets a long-form textbook
not drop to first principles cognitively: the abstraction is introduced,
internalized, and then carries the load — like a scheme for its points,
a section of the tangent bundle for a "continuously varying choice," a
groupoid for a group.

Concrete standard — name the value / scale submodule once, fenced, as a
categorical image, then evenness and all later uses are containments of
$R$-submodules, not pointwise checks:

* **Scaffolding (once, fenced):**
  "::: {#def-val} **Definition.** Let $R$ be commutative and $b\colon
  M\otimes_RM\to W$ $W$-valued bilinear. Put
  $\operatorname{Val}(b):=\langle b(x,x)\mid x\in M\rangle_R\subseteq W$
  the $R$-submodule spanned by the diagonal — equivalently the image
  $R$-submodule of $b\circ\Delta\colon M\to W$ for
  $\Delta\colon M\to M\otimes_R M$, i.e. the image of
  $\operatorname{Hom}_R(\Gamma^2_R(M),W)\xrightarrow{\gamma^*}W$ under
  evaluation. It is an $R$-submodule of $W$, functorial in $W$ via
  $\operatorname{Hom}$. :::" Stably the image $R$-submodule of
  $b\colon M\otimes^L_RM\to W$ in $\mathbf{LMod}_R$.

  Similarly $\mathfrak s(b)$, $N(b)$, $\operatorname{scale}(b)$ per
  flavour; the name is the point — one governing object.

* **From then on:** "$b$ is **even** if $\operatorname{Val}(b)\subseteq
  2W$ as $R$-submodules of $W$" (for $2W:=\operatorname{im}(2\colon
  W\to W)$). No $x$, no "for every $x$," no "$\in$." Functoriality
  $\operatorname{Val}(f^*b)\subseteq\operatorname{Val}(b)$,
  $\operatorname{Val}(b\perp b')$, containments, etc., are then statements
  about $R$-submodules, not re-expansions.

This is the global (scheme / Hom from $\Gamma^2$ / $\operatorname{Val}$)
versus local (set of points $x\in U(M)$) move: collect all points once
as the object, then work with the object — 50+ years standard since
Grothendieck.

**Banned:** " $b$ is *even* if $b(x,x)\in2W$ for every $x$" as the
recurring definition and every later "check $b(x,x)\in2W$ for every $x$."

**Preferred:** define $\operatorname{Val}(b)\subseteq W$ once via
{#def-val}; then "$b$ is **even** if $\operatorname{Val}(b)\subseteq2W$."
Never carry $b(x,x)\in2W$ on every use once $\operatorname{Val}(b)$ is
available — use the submodule.

## `PR-46`: "For every $x$, a choice of …" for the global functor / bundle / section / natural transformation

"For every $x$, a choice of $b_x$ / basis / complement / $b(x,x)\in2W$ /
isomorphism $M_x\simeq N_x$" is the element-wise unwrapping of one global
object that already has a name. Carrying the unwrapping instead of naming
the object leaves the quantifier, topology/continuity, and functoriality
($x\mapsto b_x$ natural in $x$, $f\mapsto f^*$) unspecified, so there is
nothing to check — exactly where hand-waving enters. It is the local
(points $x\in U(M)$) for global (scheme / Hom from $\Gamma^2$ /
$\operatorname{Val}$ / section) move, 50+ years standard since
Grothendieck (PR-45 is the case $\operatorname{Val}(b)$).

This is the general form of PR-37/PR-43/PR-45 and PR-30/PR-41: prose on
elements that collapses the abstraction just built for a $W$-valued,
$\mathbf{Mod}_R$-valued, or sheaf-valued construction.

Concrete standards — name the global object once, fenced, then "for every
$x$" is its evaluation on $U$-points $x\colon 1\to M$ when $U$ exists:

* **Functor, not family:** $M\mapsto\operatorname{Bil}_{R,W}(M):=
  \operatorname{Hom}_R(M\otimes_RM,W)$ as functor
  $\mathbf{Mod}_R^{\mathrm{op}}\to\mathbf{Mod}_R$ with
  $f\mapsto(f\otimes_R f)^*$ — not "for every $M$, the $R$-module …
  and for every $f\colon M\to N$, $f^*b(x,y)=b(fx,fy)$."

* **Submodule, not pointwise membership:** $\operatorname{Val}(b)\subseteq
  W$ as $R$-submodule for $b\colon M\otimes_R M\to W$ — not "for every
  $x$, $b(x,x)\in2W$."

* **Section, not pointwise choice:** a "continuously varying choice of
  basis / complement / $b_x$ for every $x\in X$" is a section of the
  frame / Grassmann / Hom-bundle $\operatorname{Fr}(E)\to X$ /
  $\underline{\operatorname{Hom}}(E,F)\to X$ — an object in
  $\mathbf{Bun}_X$, not a family $x\mapsto b_x$.

* **Sheaf morphism, not stalkwise isomorphisms:** "for every $x$, an
  isomorphism $M_x\simeq N_x$" is an isomorphism $M\simeq N$ in
  $\mathbf{Sh}(X)$ (stalkwise iso + gluing), not a family on stalks.

* **Natural transformation, not pointwise maps:** "for every $x$, a map
  $F(x)\to G(x)$" functorial in $x$ is a natural transformation
  $F\Rightarrow G$ / morphism in $\operatorname{Fun}(\mathcal C,\mathcal D)$.

In each case $x$ is a $U$-point $x\colon 1\to M$ (or $x\colon\ast\to X$)
for $U\colon\mathcal C\to\mathbf{Set}$ ($\to\mathcal S$ stably). State
the global object with its type in $\mathcal C$ ($R$-submodule, functor,
bundle, section, natural transformation), then "for every $x$" is its
evaluation, if pedagogically useful.

**Banned:** "for every $x$, choose $b_x$ / $b(x,x)\in2W$ / a complement /
an isomorphism $M_x\simeq N_x$" as the definition and every later use
without ever naming the functor / bundle / section / $R$-submodule /
natural transformation that it unwraps.

**Preferred:** name the global object once, fenced, with its category and
universal property ( $\operatorname{Val}(b)\subseteq W$ as $R$-submodule,
$\operatorname{Bil}_{R,W}\colon\mathbf{Mod}_R^{\mathrm{op}}\to\mathbf{Mod}_R$
as functor, section $s\colon X\to\operatorname{Fr}(E)$ as object in
$\mathbf{Bun}_X$, natural transformation $\eta\colon F\Rightarrow G$);
then, only after and only when $U$ exists: "On $U$-points this is for
every $x$, $b(x,x)\in2W$ / $b_x$ / $f^*b(x,y)=b(fx,fy)$."

## `PR-47`: Element quantifiers $\forall x\in M$ in the *definition* are anathema to generalization — $b\circ\tau=b$ works in every symmetric monoidal $\mathcal C$, $b(x,y)=b(y,x)$ only in $\mathbf{Set}$-concrete $\mathcal C$

"$\forall x\in M$, $b(x,y)=b(y,x)$ / $b(x,x)=0$ / $q(rx)=r^2q(x)$ /
$b(x,x)\in2W$" presupposes a concretization
$U\colon\mathcal C\to\mathbf{Set}$ with points $x\colon1\to M$
($x\in U(M)$) and the definition *is* that concretization. There is then
nothing to interpret when $U$ does not exist — $\mathrm{QCoh}(X)$ has no
underlying set of global points, $\mathbf{Sp}$ has no elements $x$, a
stack / $\infty$-category / sheaf has $U$-points only over a test
object — so the notion must be re-defined separately for
$\mathcal O_X\text{-}\mathbf{Mod}$, local systems, $\mathbf{Sp}$,
$\mathbf{Grpd}$, $\infty\text{-}\mathbf{Cat}$, $\mathbf{Sch}_{/S}$, and
functoriality / base change proved anew each time.

The diagram $b\colon M\otimes M\to W$ with $b\circ\tau=b$ /
$b\circ\tau=-b$ / $b\circ\Delta=0$ / lift through $\Gamma^2_R(M)$ names
no $x$ and no $U$ — it is a commuting diagram in the non-lax symmetric
monoidal $(\mathcal C,\otimes,1,\tau)$ ($\tau\colon M\otimes M\to M\otimes
M$ an isomorphism, $\tau^2=\mathrm{id}$). It *is* the definition in every
symmetric monoidal $\mathcal C$ at once, and its evaluation on
$U$-points $x\otimes y\colon1\to M\otimes M$ when $U$ *does* exist
recovers the element formula as a theorem, not a definition, so one
general concept does the work everywhere.

This is the general form behind PR-43/PR-44 and PR-39/PR-40/TERM-11: the
tensor classifier $M\otimes_R M$ and $\tau$ already encode bilinears and
symmetry; re-spelling them as "$\forall x,y\in M$" concretizes the
abstraction just built.

Concrete standards — define diagrammatically once, derive elements as
shadow when $U$ exists:

* **Scaffolding (once, fenced):** $(\mathbf{Mod}_R,\otimes_R,R,\tau)$
  (stably $(\mathbf{LMod}_R,\otimes^L_R,R,\tau)$) symmetric monoidal
  closed and self-enriched {#thm-mod-closed}, with $M\otimes_RM$
  classifying bilinears {#def-tensor} and $\tau_{M,M}$ the symmetry,
  $\Delta$, $\Gamma^2_R$ as in PR-43. The same structure exists in
  $(\mathrm{QCoh}(X),\otimes_{\mathcal O_X},\mathcal O_X,\tau)$,
  $(\mathbf{Sp},\wedge,\mathbb S,\tau)$, etc. — no $U$ needed.

* **$W$-valued $b\colon M\otimes_RM\to W$ is symmetric / skew /
  alternating / even** as in PR-43: $b\circ\tau=b$, $b\circ\tau=-b$,
  $b\circ\Delta=0$, lift through $\Gamma^2_R(M)$. No $x,y$.

* **Element shadow (only after, when $U\colon\mathcal C\to\mathbf{Set}$
  exists):** for $x,y\colon1\to M$ (i.e. $x,y\in U(M)$),
  $b\circ\tau=b$ evaluates to $b(x,y)=b(y,x)$, etc. This is a property of
  the diagram, proved by applying $U$ to $x\otimes y\colon1\to M\otimes
  M$, not the definition.

**Banned:** definitions quantified as "for every $x\in M$, $b(x,y)=b(y,x)$
/ $b(x,x)=0$ / $q(rx)=r^2q(x)$ / $b(x,x)\in2W$ for every $x$."

**Preferred:** "Let $b\colon M\otimes_RM\to W$ be $W$-valued bilinear. $b$
is **symmetric** if $b\circ\tau=b$ (resp. skew if $b\circ\tau=-b$,
alternating if $b\circ\Delta=0$, even if it lifts through
$\Gamma^2_R(M)$)." Then, if pedagogically useful and only when
$U$ exists: "On $U$-points this is $b(x,y)=b(y,x)$ $\forall x,y\in
U(M)$."

## `PR-48`: Mixing a Lemma / Proposition / Remark about $\operatorname{Alt}\Rightarrow\operatorname{Skew}$ and $2$-obstructions into the definition block

"Alternating $\Rightarrow$ skew" is not a definition and not a comment —
it is a Lemma ($\operatorname{AltBil}\subseteq\operatorname{SkewBil}$ as
$R$-submodules, proved from $\tau$ and $\Delta$: $b\circ\Delta=0\Rightarrow
b\circ\tau=-b$ via $b(x+y,x+y)$). "Converse holds when $2$ injective on
$W$" and "when $2W=W$ every $b$ is even; quadratic refinements retain
…" are a more nuanced Proposition / Remark about the map induced by
$2\colon W\to W$ and its obstruction to being iso — each warrants its
own fenced block with quantified hypothesis and proof, not two sentences
appended to `{#def-form-axioms}`.

This is the general form of DEF-15/DEF-19 and SEC-6: one fenced block per
notion with one logical status. A Definition block defines; implications
between defined subobjects are Lemmas/Propositions with proofs; side
observations are Remarks.

Concrete standard — define the four named $R$-submodules once, then
containments are $R$-submodule inclusions and the $2$-discussion is a map
between named objects:

* **Scaffolding (once, fenced):**
  $\operatorname{Bil}_{R,W}(M):=\operatorname{Hom}_R(M\otimes_RM,W)$ as
  $R$-module. Put
  $\operatorname{SymBil}_{R,W}(M):=\ker(\tau^*-\mathrm{id})$,
  $\operatorname{SkewBil}_{R,W}(M):=\ker(\tau^*+\mathrm{id})$,
  $\operatorname{AltBil}_{R,W}(M):=\ker(\Delta^*)$,
  $\operatorname{EvBil}_{R,W}(M):=
  \operatorname{im}(\operatorname{Hom}_R(\operatorname{Sym}^2_R(M),W)\to
  \operatorname{Bil})$ (i.e. image of
  $\operatorname{Hom}_R(\Gamma^2_R(M),W)\xrightarrow{\gamma^*}\operatorname{Bil}$
  for the even lift), all $R$-submodules of $\operatorname{Bil}_{R,W}(M)$
  via $b\mapsto b\circ\tau$, $b\mapsto b\circ\Delta$.

* **Then, separate fenced units:**
  "::: {#lem-alt-skew} **Lemma.** $\operatorname{AltBil}_{R,W}(M)
  \subseteq\operatorname{SkewBil}_{R,W}(M)$ as $R$-submodules. *Proof.*
  … :::"
  "::: {#prop-skew-alt} **Proposition.** The $R$-linear
  $2_*\colon\operatorname{Bil}_{R,W}(M)\to\operatorname{Bil}_{R,W}(M)$,
  $(2_*b)(x,y)=2b(x,y)$ induced by $2\colon W\to W$, controls the converse:
  $\operatorname{SkewBil}=\operatorname{AltBil}$ iff $2\colon W\to W$ is
  injective; the obstruction to
  $\operatorname{EvBil}\xrightarrow{\sim}\operatorname{Bil}$ is
  $\ker/\operatorname{coker}(2_*)$. In particular if $2W=W$ then every
  $b$ is even as an element condition, but the quadratic refinement
  $\operatorname{Quad}_{R,W}(M)=\operatorname{Hom}_R(\Gamma^2_R(M),W)$
  retains information via $\gamma^*$. :::"

  No Lemma/Proposition inside the Definition; no "Alternating forms are
  skew" as a comment.

**Banned:** the three sentences appended to `{#def-form-axioms}` — neither
fenced nor proved, with no named $\operatorname{AltBil}$ /
$\operatorname{SkewBil}$ / $\operatorname{EvBil}$ or $2_*$ to refer to.

**Preferred:** keep `{#def-form-axioms}` to the four diagrammatic
definitions $b\circ\tau=b$ / $b\circ\tau=-b$ / $b\circ\Delta=0$ / lift
through $\Gamma^2$; then separate `Lemma` for
$\operatorname{Alt}\subseteq\operatorname{Skew}$ and `Proposition/Remark`
for the $2$-obstruction with the named $R$-submodules and the map
$2_*$ between named objects.

## `PR-49`: Pithy prose that avoids naming $\operatorname{Bil}^{ev}$, $\operatorname{AltBil}$, $\operatorname{SkewBil}$, $\operatorname{SymBil}$ and the map $2_*$ between them, and restates $b\colon M\times M\to W$ instead of $b\in\operatorname{Bil}$

Once $\operatorname{Bil}_{R,W}(M):=\operatorname{Hom}_R(M\otimes_RM,W)$ is
named, membership $b\in\operatorname{Bil}_{R,W}(M)$ *is* the signature
$b\colon M\otimes_RM\to W$ — no "$b\colon M\times M\to W$" to restate.
More generally, definitions should state objects and $R$-submodule
containments, not signatures. Pithy prose "Alternating forms are skew;
converse holds when $2$ injective; when $2W=W$ every $b$ is even"
avoids ever naming
$\operatorname{AltBil}_{R,W}(M)$, $\operatorname{SkewBil}_{R,W}(M)$,
$\operatorname{SymBil}_{R,W}(M)$, $\operatorname{EvBil}_{R,W}(M)$ and the
$R$-linear $2_*\colon\operatorname{Bil}\to\operatorname{Bil}$
(resp. $\operatorname{Hom}_R(\Gamma^2,W)\xrightarrow{\gamma^*}
\operatorname{Bil}$) induced by $2\colon W\to W$, whose (non-)isomorphism
is the actual content. The categorical definitions are then phrased as
$R$-submodule isomorphisms/equalities of those named objects, not as
element conditions on an unwrapped $b$.

This is the general form of PR-40/PR-45 and PR-30: eliding the governing
object that would make the statement checkable, so hand-waving can occupy
its place.

**Banned:** "For $b\colon M\times M\to W$: $b$ is symmetric if …;
Alternating forms are skew-symmetric. The converse holds when $2$
injective …" with no named $\operatorname{AltBil}$ / $\operatorname{SkewBil}$
/ $\operatorname{EvBil}$ and no $2_*$.

**Preferred:** "Let $b\in\operatorname{Bil}_{R,W}(M)$. $b$ is
**symmetric** if $b\in\operatorname{SymBil}_{R,W}(M)$ ($b\circ\tau=b$),
**skew** if $b\in\operatorname{SkewBil}_{R,W}(M)$, **alternating** if
$b\in\operatorname{AltBil}_{R,W}(M)$, **even** if
$b\in\operatorname{EvBil}_{R,W}(M)$." Then
"$\operatorname{AltBil}\subseteq\operatorname{SkewBil}\subseteq\operatorname{Bil}$
as $R$-submodules; $2_*$ induces …; $\operatorname{EvBil}= \operatorname{Bil}$
iff …" — objects and containments, not signatures and element formulas.

## `PR-50`: Nominalizing the adjective/verb — "satisfies the evenness / injectivity / exactness / commutativity condition" for "is even / injective / exact" / "commutes / factors"

"Even" is an adjective on $b$ ($b$ **is even**,
$b\in\operatorname{EvBil}$); "commutes" / "factors" are verbs on the
diagram. Nominalizing to "evenness," "injectivity," "exactness,"
"commutativity," "factorization" + "condition" forces a light verb
"satisfies / has / exhibits / possesses" to re-predicate it — one
checkable predicate becomes three words for no new content, with no
named subobject to check (same device as "with its hypotheses," PR-31).
Standard is the un-nominalized predicate.

Concrete bad / standard pairs (transcribe, do not invent):

* **Banned:** "When $2W=W$, every bilinear form satisfies the evenness
  condition."
  **Preferred:** "When $2W=W$, every $W$-valued bilinear $b$ is even"
  (i.e. $\operatorname{EvBil}_{R,W}(M)=\operatorname{Bil}_{R,W}(M)$ as
  $R$-submodules; element shadow "$b(x,x)\in2W$ $\forall x$" vacuous) —
  or, for the non-vacuous content: "the quadratic refinement
  $\operatorname{Quad}_{R,W}(M)=\operatorname{Hom}_R(\Gamma^2_R(M),W)$
  still distinguishes forms via $\gamma^*$." One adjective, one membership
  $b\in\operatorname{EvBil}$.

* **Banned:** " $f$ satisfies the injectivity condition / satisfies
  injectivity."
  **Preferred:** "$f$ is injective" ($f\colon M\hookrightarrow N$ as
  monomorphism, $\ker f=0$).

* **Banned:** "the sequence satisfies exactness at $M$."
  **Preferred:** "the sequence is exact at $M$" ($\operatorname{im}=\ker$).

* **Banned:** "the diagram satisfies the commutativity condition /
  exhibits commutativity."
  **Preferred:** "the diagram commutes" ($g\circ f = h$).

* **Banned:** " $b$ satisfies the factorization condition through
  $\Gamma^2$."
  **Preferred:** "$b$ factors through $\Gamma^2_R(M)$"
  / "$b$ lifts through $\Gamma^2_R(M)$."

In each case delete the noun "…ness / …ivity / …ion" + "condition" + light
verb, and keep the adjective/verb that already is the claim with its
named subobject/diagram.

## `PR-51`: "Retain additional information" is empty filler — not a submodule, kernel, fiber, or invariant

"Information" is not an $R$-submodule, kernel, cokernel, fiber, or
invariant, so "retain additional information" cannot be true or false;
additional *relative to what* — to $\operatorname{EvBil}$, to
$\operatorname{SymBil}$, to the element condition $b(x,x)\in2W$ just
declared vacuous? The precise content is the (non-)isomorphism between
*named* $R$-modules and its obstruction.

Concrete standard — state the (non-)isomorphism and its fiber:

"::: {#prop-quad-vs-bil} **Proposition.** $\gamma^*$ is not an
isomorphism in general; when $2\colon W\to W$ is invertible,
$\operatorname{EvBil}_{R,W}(M)=\operatorname{Bil}_{R,W}(M)$ as element
condition but $\gamma^*\colon\operatorname{Quad}_{R,W}(M)\to
\operatorname{EvBil}_{R,W}(M)$ still has non-trivial fiber: the set of
quadratic refinements of $b$ is a torsor under
$\operatorname{Hom}_R(M,W/2W)$ (discrete case), with obstruction
$\ker(\gamma^*)/\operatorname{coker}(\gamma^*)$. :::"

**Banned:** "quadratic refinements retain additional information."

**Preferred:** "$\gamma^*$ is not an isomorphism; its fiber over $b$
(retaining the extra invariant) is …" / "$\ker(\gamma^*)$ is …" — name
the $R$-module map and its fiber/kernel, not "information."

## `PR-52`: Weasel mass nouns — "information," "data," "setting," "condition," "property," "structure," "notion," … with no fixed referent

The instances we know today — "information" (PR-51),
"data" (EV-6, PR-20), "setting" (TERM-13), "condition" / "hypotheses"
(PR-31, PR-50), "conclusion" (PR-30), "value module" (TERM-9), "torsion
theory" (TERM-4), "operations / structure via $W$" (PR-38),
"presheaf" for $\mathbf{Mod}_R^{\mathrm{op}}\to\mathbf{Mod}_R$ (TERM-10) —
will change. The underlying problem is timeless and is detected by
semantic indicators, not by a word list: a mass noun with no fixed
extension in $\mathbf{Mod}_R$ / $\mathbf{Cat}_\infty$ that exploits
colloquial understanding so the sentence can be defended as "true under
some interpretation" while naming no $R$-submodule, functor, category, or
invariant to check.

Timeless indicators that a clause is weasel-wording (any one suffices to
flag):

* **No fixed referent in the document.** The noun has no fenced definition
  with a type — no $R$-submodule $\operatorname{Val}(b)\subseteq W$ for
  "information," no $W\in\mathbf{Mod}_R$ for "value module," no category
  $\mathbf{TorBil}_{R,W}$ for "setting," no list "$2\colon W\hookrightarrow
  W$ injective" for "hypotheses."

* **Truth / meaning is context-dependent where the context is never fixed
  or stated.** "Retain additional information" is true of any true
  statement; "with its hypotheses" is true of every theorem; "in the
  discriminant setting" is true in any ambient the reader imagines.

* **Unfalsifiable.** Any counterexample can be deflected as "not the
  intended information / setting / condition" because no quantified
  proposition was stated (PR-30).

* **Abuse of colloquial understanding.** The reader is expected to supply
  the mathematical meaning from ordinary English ("information" = "something
  true," "setting" = "where this happens") instead of from a defined
  morphism.

* **Occupies the slot where a named object belongs.** The noun sits where
  an $R$-submodule, functor, category, or diagram is owed, so the sentence
  is unfalsifiable without ever being precise (PR-30–32).

Concrete bad / standard pairs are instances of the same timeless check —
replace the mass noun by the named object that already has a type:

* **Banned:** "quadratic refinements retain additional information."
  **Preferred:** "$\gamma^*\colon\operatorname{Quad}_{R,W}(M)\to
  \operatorname{EvBil}_{R,W}(M)$ is not an isomorphism; its fiber over $b$
  is a torsor under $\operatorname{Hom}_R(M,W/2W)$" (PR-51).

* **Banned:** "is additional data / does not follow from notation."
  **Preferred:** "$b\in\operatorname{EvBil}_{R,W}(M)$ is the lift through
  $\Gamma^2_R(M)$" (EV-6, PR-20).

* **Banned:** "in the discriminant setting."
  **Preferred:** "in $\mathbf{TorQuad}_{R,W}$, for $(D_L,\bar q)$ with
  $D_L:=L^\vee/L$" (TERM-13).

* **Banned:** "with its hypotheses / satisfies the evenness condition."
  **Preferred:** "for $2\colon W\hookrightarrow W$ injective" /
  "$b$ is even ($b\in\operatorname{EvBil}$)" (PR-31, PR-50).

New weasel nouns will appear; audit by the indicators, not the list.
When a new mass noun is found, replace it by the $R$-submodule / functor /
category that already has a name, or define that object fenced if it does
not yet exist — do not add the noun to a list and keep the sentence.

## `PR-53`: A definition is a general building block, not the minimal element condition that lets the next paragraph type-check

"$\{x\mid b(x,N)=0\}$ / $b(x,x)=0$ / $\forall x\in M$" is the cheapest
sentence that lets this page proceed for $\mathbf{Mod}_R$ and matches the
classical $b(x,N)=0$ literature, but it is not a building block — it
names no $R$-linear $b^{\sharp}\colon M\to\underline{\operatorname{Hom}}(M,W)$,
no kernel, no dual, no $\operatorname{Val}(b)$, no $\Gamma^2_R$ — so every later
notion (radical, nondegenerate, $L^\vee$, $D_L$, discriminant form) must
be rebuilt elementwise and cannot be transported to
$\mathrm{QCoh}(X)$, $\mathbf{Sp}$, sheaves, $\infty\text{-}\mathbf{Cat}$,
$\mathbf{Sch}_{/S}$ without re-defining. The time saved today is the
applicability lost tomorrow, next week, and across a research career.

A definition in a long-form book is the reusable interface the rest of
the document *and* future work build on: state it once, diagrammatically,
with its universal property, so that later definitions are instances and
element formulas are shadows, not re-definitions.

Concrete standard — name the adjoint and its kernel as the building
blocks (all do the work of the elementwise $N^{\perp}$ / isotropic), then
later theory is immediate:

* **Scaffolding (once, fenced):**
  $\operatorname{Hom}_R(M\otimes_RM,W)\cong\operatorname{Hom}_R(M,
  \underline{\operatorname{Hom}}_R(M,W))$ via the closed structure
  {#thm-mod-closed} / {#def-tensor}. For $b\colon M\otimes_RM\to W$ put
  $b^{\sharp_{\!L}},b^{\sharp_{\!R}}\colon M\to\underline{\operatorname{Hom}}_R(M,W)$,
  $x\mapsto b(x,-)$ and $x\mapsto b(-,x)$, the two adjoints. When $b$
  symmetric they agree and are written $b^{\sharp}$.

* **Then, as $R$-submodules / kernels (no $x$):**
  $N^{\perp_{\!L}}:=\ker(M\xrightarrow{b^{\sharp_{\!L}}}
  \underline{\operatorname{Hom}}_R(N,W))$ (and $\perp_{\!R}$ via the other
  adjoint), the $R$-submodule classified by the universal property for
  "$b(x,N)=0$";
  $Q_{R,W}(M):=\ker(M\xrightarrow{\Delta}M\otimes_R M\xrightarrow{b}W)$ for
  $q:=b\circ\Delta$ (quadratic diagonal) — $x$ isotropic iff
  $x\in\ker(q)$ as $U$-shadow, and $b$ anisotropic iff $\ker(q)=0$ as
  subobject of $M$ (not "$0$ is the only isotropic element");
  $M$ nondegenerate iff $b^{\sharp}$ is iso; $M^\vee:=
  \underline{\operatorname{Hom}}_R(M,R)$; $D_L:=L^\vee/L$ with
  $\bar b$ / $\bar q$ induced via $b^{\sharp}$ — all as kernels /
  cokernels of the named $b^{\sharp}$, not as sets $\{x\mid\ldots\}$.

* **Element shadow (only after, when $U$ exists):** for $x\colon R\to M$
  ($x\in U(M)$), $x\in N^{\perp}$ evaluates to $\forall n\in U(N)$,
  $b(x,n)=0$, and $x\in\ker(q)$ to $b(x,x)=0$.

**Banned:** "$N^{\perp}:=\{x\in M\mid b(x,N)=0\}$" / "$x$ isotropic if
$b(x,x)=0$, $b$ anisotropic if $0$ is its only isotropic element" as the
*definitions* that later theory must reuse.

**Preferred:** define $b^{\sharp}$ once, then
$N^{\perp}:=\ker(b^{\sharp})$, " $x$ isotropic if $x\in\ker(b\circ\Delta)$,"
"$b$ anisotropic if $\ker(b\circ\Delta)=0$ as subobject of $M$." The element
formulas are the $U$-evaluation of those kernels, proved as a property,
not the building block.

## `PR-54`: Long-term general applicability is an explicit design goal — write it down or no agent will know it

The implicit goal behind PR-43/PR-47/PR-53 — one definition that works
in every symmetric monoidal abelian $\mathcal C$ at once ($\mathbf{Mod}_R$,
$\mathbf{LMod}_R$, $\mathrm{QCoh}(X)$, $\mathbf{Sp}$-modules, sheaves,
$\infty\text{-}\mathbf{Cat}$, $\mathbf{Sch}_{/S}$) so that later theory
($\operatorname{Val}(b)$, $b^{\sharp}$, $M^\vee$, $D_L$, discriminant
forms) is an instance, not a re-definition — is not inferable from the
current page's minimal needs. No agent can know it unless it is written
down in this document and in the document's scaffolding section.

When a definition admits an easy, no-harder generalization that
immediately recovers the classical element formula (here
$b\circ\tau=b$ for $b(x,y)=b(y,x)$, $b^{\sharp}$ for $N^{\perp}$,
$\ker(b\circ\Delta)$ for isotropic) and drastically increases
applicability down the line, the general form *is* the definition.
Saving time today with the minimal "$\forall x\in M$" costs re-definition
for every future $\mathcal C$ and degrades a forward-thinking research
program that will live with these interfaces for years.

**Standard:** in the document's introduction / scaffolding preamble and in
this `CONTRIBUTING.md`, state explicitly: "All bilinear/quadratic
notions are defined diagrammatically via $(\otimes,1,\tau)$ and
$b^{\sharp}$ in a closed symmetric monoidal abelian $\mathcal C$, so as
to apply to $\mathbf{Mod}_R$, $\mathrm{QCoh}(X)$, $\mathbf{Sp}$, etc.,
with element formulas only as the $U$-evaluation when $\mathcal C$ is
$\mathbf{Set}$-concrete. Minimal elementwise definitions are not the
goal; reusable building blocks are." Then enforce it: every new
definition is reviewed against that stated goal, not against the cheapest
sentence that lets the next paragraph proceed.

## `PR-55`: Hygiene and foresight — building on the $\mathbf{Set}$-shadow instead of on the named categorical object that classifies it

The lack of hygiene in "$M=N\oplus N^{\perp}$," "$b(x,y)=b(y,x)$," "$b(x,x)\in2W$," "$\{x\mid b(x,N)=0\}$," "$b$ satisfies the evenness condition," "pullback defines a presheaf," "retain additional information in the discriminant setting" is one pattern: the definition / theorem is stated on the evaluation of a categorical object on $U$-points $x\colon1\to M$ ($U\colon\mathcal C\to\mathbf{Set}$), not on the object that classifies that evaluation. The shadow is locally correct for $\mathbf{Mod}_R$ and matches classical $b(x,N)=0$ literature, but it names no $b^{\sharp}$, no $\ker$, no $\operatorname{Val}(b)$, no $\operatorname{Bil}_{R,W}$, no $\Gamma^2_R$, so it cannot be reused and cannot be transported: every later notion must be re-spelled elementwise and every $\mathcal C$ without $U$ (e.g. $\mathrm{QCoh}(X)$, $\mathbf{Sp}$-modules, sheaves, $\infty\text{-}\mathbf{Cat}$) needs a new definition.

Foresight is stating the scaffolding and the governing object once, diagrammatically, with its universal property, so that the element formula is its shadow — not its definition — and later theory is an instance.

Concrete scaffolding that was owed once, fenced, before any $b(x,y)$ or $N^{\perp}$:

* $(\mathbf{Mod}_R,\otimes_R,R,\tau)$ symmetric monoidal closed and self-enriched, $M\otimes_RM$ classifying $R$-bilinears, $\underline{\operatorname{Hom}}_R(M,W)\in\mathbf{Mod}_R$ as internal hom {#thm-mod-closed}/{#def-tensor}; $\operatorname{Hom}_R(M\otimes_R M,W)\cong\operatorname{Hom}_R(M,\underline{\operatorname{Hom}}_R(M,W))$ giving $b^{\sharp_{\!L}},b^{\sharp_{\!R}}\colon M\to\underline{\operatorname{Hom}}_R(M,W)$.
* $\operatorname{Bil}_{R,W}(M):=\operatorname{Hom}_R(M\otimes_R M,W)$ and its named $R$-submodules $\operatorname{SymBil}:=\ker(\tau^*-\mathrm{id})$, $\operatorname{SkewBil}:=\ker(\tau^*+\mathrm{id})$, $\operatorname{AltBil}:=\ker(\Delta^*)$, $\operatorname{EvBil}:=\operatorname{im}(\gamma^*)$ with $\Gamma^2_R\xrightarrow{\gamma}\operatorname{Sym}^2_R\to M\otimes_R M$; $\operatorname{Quad}_{R,W}(M):=\operatorname{Hom}_R(\Gamma^2_R(M),W)$ and $\gamma^*\colon\operatorname{Quad}\to\operatorname{Bil}$.
* $\operatorname{Val}(b)\subseteq W$ as $R$-submodule $\langle b(x,x)\rangle$ i.e. image of $\gamma^*$; $N^{\perp}:=\ker(M\xrightarrow{b^{\sharp}}\underline{\operatorname{Hom}}_R(N,W))$; isotropic as $\ker(M\xrightarrow{\Delta}M\otimes_R M\xrightarrow{b}W)$, anisotropic as $\ker=0$; nondegenerate as $b^{\sharp}$ iso; $M^\vee:=\underline{\operatorname{Hom}}_R(M,R)$; $(M,b)\perp(N,c)$ as orthogonal sum in $\mathbf{Bil}_{R,W}$.

With those named, hygiene is: every definition is membership in a named $R$-submodule / kernel of a named $R$-linear map; every theorem is a containment of named subobjects or a statement about a named map $2_*$ / $\gamma^*$ being (non-)iso with obstruction $\ker/\operatorname{coker}$; every "for every $x$" is the $U$-evaluation of that diagram when $U$ exists. The minimal "$\forall x\in M$, $b(x,y)=b(y,x)$ / $b(x,N)=0$ / $b(x,x)\in2W$" is then never the definition.

**Banned:** any definition / theorem that quantifies $\forall x\in M$ / $\{x\mid\ldots\}$ / "$b\colon M\times M\to W$" / "$b$ satisfies the … condition" / "pullback … defines a presheaf" / "retain additional information in the … setting" / "$M=N\oplus N^{\perp}$ and the sum is orthogonal" as prose without the named $b^{\sharp}$, $\ker$, $\operatorname{Bil}$ / $\operatorname{Alt}/\operatorname{Skew}/\operatorname{EvBil}$, $\operatorname{Val}(b)$, $\Gamma^2_R$, and the proved biproduct $\perp$ vs. $\oplus$ in $\mathbf{Bil}_{R,W}$ vs. $R\text{-}\mathbf{Mod}$.

**Preferred:** state the scaffolding once; then every bilinear/quadratic notion is a named $R$-submodule / kernel / image with its universal property, every implication is a Lemma/Proposition about containments of those named subobjects or about $\gamma^*$ / $2_*$ between named objects with quantified hypotheses and proof, and element formulas appear only as "on $U$-points $x\colon R\to M$ this is $b(x,y)=b(y,x)$."

## `PR-56`: "$N\subseteq M$ be a submodule" / "$M/N$" for $i\colon N\hookrightarrow M$ and $\operatorname{coker}(i)$ — subobjects as monos and quotients as cokernels

"$N\subseteq M$" is the $\mathbf{Set}$-shadow of a mono $i\colon
N\hookrightarrow M$ ($U(i)\colon U(N)\hookrightarrow U(M)$ injective for
$U\colon\mathbf{Mod}_R\to\mathbf{Set}$), and "$M/N$" the shadow of its
cokernel $M\twoheadrightarrow\operatorname{coker}(i)$ (the set of cosets
$[x]=x+N$). The elementwise induced form
"$\bar b([x],[y]):=b(x,y)$ well-defined iff $b(N,M)=0$" re-spells the
universal property of the cokernel on representatives $x,y\in U(M)$.

Stated with $i$ and $\operatorname{coker}(i)$ the notion is one diagram
in any abelian $\mathcal C$ (stably any stable $\mathcal C$) — no $U$,
no representatives — and $N$ need not be a subset: a subobject is an
equivalence class of monos, not $N\subseteq U(M)$ ($\mathrm{QCoh}(X)$,
$\mathbf{LMod}_R$ stably, $\mathbf{Sp}$-modules, sheaves have no
underlying set $M/N$).

Concrete standards — name the mono and its cokernel, then the induced
form is the unique factorization through $\pi\otimes_R\pi$:

* **Scaffolding (once, fenced):** in abelian $\mathcal C$, a subobject of
  $M$ is a mono $i\colon N\hookrightarrow M$ up to iso over $M$; its
  **quotient** is $\operatorname{coker}(i)\colon M\twoheadrightarrow
  \operatorname{coker}(i)$ with universal property: $f\colon M\to T$
  factors uniquely through $\operatorname{coker}(i)$ iff $f\circ i=0$.

* **Forms on quotients:** for $b\colon M\otimes_R M\to W$ symmetric (or
  any $b$), and $i\colon N\hookrightarrow M$, the **restriction** is
  $i^*b:=b\circ(i\otimes_R i)\colon N\otimes_R N\to W$; $i$ is **isotropic**
  ($N\subseteq N^{\perp}$) iff $b\circ(i\otimes_R\mathrm{id}_M)=0\colon
  N\otimes_R M\to W$ (i.e. $i^*b$ and the cross terms vanish as $b\circ
  (i\otimes_R\mathrm{id})=0$). Then $b$ **induces** $\bar b\colon
  \operatorname{coker}(i)\otimes\operatorname{coker}(i)\to W$ iff
  $i^*b=0$ in that sense, and $\bar b$ is the unique $R$-linear with
  $\bar b\circ(\pi\otimes_R\pi)=b$ for $\pi:=\operatorname{coker}(i)$. No
  $[x]$ to choose, no well-definedness to check.

  Stably $\operatorname{cofib}(i)$ for $i\colon N\to M$ in
  $\mathbf{LMod}_R$.

**Banned:** "Let $b$ be symmetric on $M$ and let $N\subseteq M$ be a
submodule. … forms on quotients $M/N$ … $\bar b([x],[y])=b(x,y)$."

**Preferred:** "Let $b\colon M\otimes_R M\to W$ be symmetric and let
$i\colon N\hookrightarrow M$ be a mono (a subobject). Put
$\pi\colon M\twoheadrightarrow\operatorname{coker}(i)$ for the quotient.
Then $b$ induces $\bar b\colon\operatorname{coker}(i)\otimes
\operatorname{coker}(i)\to W$ iff $i^*b=0$ (i.e. $b\circ(i\otimes
\mathrm{id}_M)=0$), uniquely with $\bar b\circ(\pi\otimes_R\pi)=b$."
Then, only after and only when $U$ exists: "On $U$-points this is
$\bar b([x],[y])=b(x,y)$ for $[x]=\pi(x)$."

## `PR-57`: "$N^{\perp}$" alone is not well-defined — even when $N$ abstractly a submodule of $M$ — it is $(M,b,i\colon N\hookrightarrow M)^{\perp}$

"$N^{\perp}$" as written suggests a function of the abstract $R$-module
$N$ (or of $N$ up to isometry as lattice), but
$N^{\perp}:=\ker(M\xrightarrow{b^{\sharp}}\underline{\operatorname{Hom}}_R(N,W))$
with $b^{\sharp}=b\circ(i\otimes_R\mathrm{id}_M)$ depends on the triple
$(M,b,i)$ — the ambient $M$, the $W$-valued
$b\colon M\otimes_R M\to W$, and the mono $i\colon N\hookrightarrow M$ that
makes $N$ a *subobject*, not on $N$ abstractly. Change $b$ or change $i$
and the kernel moves while abstract $N$ does not. "Abstractly a submodule
of $M$" (i.e. $N\cong N'$ as $R$-module / as lattice) does not determine
$i$, and even $N\subseteq M$ as a *subset* (so $i$ is the inclusion) does
not determine $b$.

Concrete standards — name the triple, and keep $N^{\perp}$ with its
ambient:

* **Object:** for $i\colon N\hookrightarrow M$ and
  $b\colon M\otimes_R M\to W$, put
  $N^{\perp_{b}}:=N^{\perp_{i}}:=
  (i\colon N\hookrightarrow(M,b))^{\perp}:=
  \ker(M\xrightarrow{b^{\sharp}}\underline{\operatorname{Hom}}_R(N,W))\subseteq M$
  as $R$-submodule of $M$ (stably fiber in $\mathbf{LMod}_R$). Write
  $N^{\perp_b}$ / $N^{\perp_i}$ / $(i)^{\perp}$, never bare
  "$N^{\perp}$."

* **Lattices where the distinction matters:**

  — $M=U:=\mathbb Z e\oplus\mathbb Z f$, $b(e,f)=1$, $b(e,e)=0=b(f,f)$.
  $i_1\colon N_1:=\mathbb Z e\hookrightarrow M$, $N_1\cong\langle0\rangle$
  isotropic, $N_1^{\perp}=N_1$ ($b(ae+bf,e)=b$).
  $i_2\colon N_2:=\mathbb Z(e+f)\hookrightarrow M$, $N_2\cong\langle2\rangle$
  as lattice but $U(N_2)\cong\mathbb Z\cong U(N_1)$ as $\mathbb Z$-module —
  abstractly the same $N$ — yet
  $N_2^{\perp}=\mathbb Z(e-f)\cong\langle-2\rangle\neq N_1^{\perp}$.

  — Same $M=\mathbb Z^2$, same $N=\mathbb Z(1,0)\subseteq M$ as subset, but
  $b_1=\operatorname{diag}(1,1)$ gives $N^{\perp_{b_1}}=\mathbb Z(0,1)$ while
  hyperbolic $b_2(e_i,e_j)=\delta_{i\neq j}$ gives
  $N^{\perp_{b_2}}=\mathbb Z(1,-1)$ as $R$-submodules of the same $M$;
  $N^{\perp}$ moved with $b$ while $N$ did not.

  — Primitive vs. non-primitive embeddings of the same abstract
  $A_1\langle-2\rangle$ in $U$ or $E_8$ have different $N^{\perp}$ (different
  rank, different $D_{N^{\perp}}$), so "$N^{\perp}$" without $i$ is
  ambiguous even up to isometry.

**Banned:** "$N^{\perp}$" with $N\subseteq M$ understood as abstract
$N$, or "$N^{\perp}$" with $b$ left implicit.

**Preferred:** "$N^{\perp_b}$" / "$N^{\perp_i}$" / "$(i\colon
N\hookrightarrow(M,b))^{\perp}\subseteq M$ as $R$-submodule" and, when
quoting the lattice, "the abstract lattice $N\cong\langle2\rangle$ embeds
via $i_1,i_2$ with $N^{\perp_{i_1}}\not\cong N^{\perp_{i_2}}$."

## `PR-58`: $\operatorname{Gram}(b)$ is ill-defined on $(M,b)\in\mathbf{Bil}_{R,W}$, well-defined on $((M,e),b)$ in $\mathbf{Bil}_{R,W}^{\mathrm{fr}}$ — it is $e^*b$, not a property of $(M,b)$

"$\operatorname{Gram}(b)$" as a matrix $(b(e_i,e_j))$ presupposes a finite
ordered basis $e\colon R^n\xrightarrow{\sim}M$, i.e. an object of
$\mathbf{FMod}_R^{\mathrm{fr}}$ / $\mathbf{BMod}_R$, not of
$\mathbf{Mod}_R$. An object $(M,b\colon M\otimes_R M\to W)$ in
$\mathbf{Bil}_{R,W}$ has $M$ arbitrary — $M=\mathbb Q$,
$\mathbb Q/\mathbb Z$, $\bigoplus_{\mathbb N}\mathbb Z$, non-free
projective all carry $W$-valued $b$ with no $n$ and no $(e_i)$ — so no
$n\times n$ matrix exists. The functor $(M,b)\mapsto\operatorname{Gram}(b)$
has no domain on $\mathbf{Bil}_{R,W}$.

On $\mathbf{Lat}_R\subseteq\mathbf{Bil}_{R,W}$ — finite free over $\mathbb Z$
(resp. $\mathbb Z_{(p)}$) with nondegenerate $b$ — an $n$ *does* exist, but
still no distinguished $e$: the $n\times n$ matrix is defined only *after*
choosing an ordered basis. Framed, it is well-typed as the pullback
$G_e(b):=e^*b:=b\circ(e\otimes_R e)\in M_n(W)=\operatorname{Hom}_R(R^n\otimes_R R^n,W)$,
i.e. $(b(e_i,e_j))$, and then $\det$, $\operatorname{rk}$, etc. are
$\operatorname{GL}_n(R)$-invariants of the isometry class $[G_e(b)]$.

Concrete standards — name the framing, then Gram is the pullback:

* **Bare $(M,b)$:** no Gram matrix.
* **Framed $((M,e),b)$:** for ordered basis $e=(e_1,\dots,e_n)\colon R^n\xrightarrow{\sim}M$,
  put $G_e(b):=e^*b\in M_n(W)$, $G_e(b)_{ij}:=b(e_i,e_j)$.

**Banned:** "$\operatorname{Gram}(b)$" for $(M,b)\in\mathbf{Bil}_{R,W}$
with no $e$.

**Preferred:** "Let $((M,e),b)$ be framed, $e\colon R^n\xrightarrow{\sim}M$.
Put $G_e(b):=e^*b\in M_n(W)$."

## `PR-59`: Without an explicit ordered basis / generating set, $\operatorname{Gram}(b)$ is well-defined only up to $\operatorname{GL}_n(R)$-congruence

Without the ordered frame $e$ the matrix has no size and no value; with
$e$ it is $G_e(b)=e^*b$ and changes by congruence when $e$ changes.
For ordered bases $e' = e\circ P$ with
$P\in\operatorname{GL}_n(R)=\operatorname{Aut}_R(R^n)$,
$G_{e'}(b)=P^{\!t}G_e(b)P$ in $M_n(W)$. So without $e$, $\operatorname{Gram}(b)$
is well-defined only as the isometry class $[G_e(b)]\in M_n(W)/\operatorname{GL}_n(R)$
— i.e. up to $\operatorname{GL}_n(R)$-congruence, with $n=\operatorname{rk}M$ itself
defined only after the framing — not as a matrix. With only a generating
set $S$ and $F(S)\twoheadrightarrow M$, the $|S|\times|S|$ matrix on
$F(S)$ is well-defined only up to $\operatorname{Aut}_R(F(S))$ and up to
stabilization by the relations of $M$; different $S$ give different sizes,
so the assignment is a function on $((M,e_S),b)$ in $\mathbf{Mod}_R^{\mathrm{fr}}$,
not on $(M,b)$.

**Banned:** "$\operatorname{Gram}(b)$" for $(M,b)$ with no $e$ (PR-58);
"the Gram matrix of $(M,b)$ is …" with no $e$ / $S$ to make the congruence
class a matrix.

**Preferred:** always name $e$: "$G_e(b)$," "$G_{e'}(b)=P^{\!t}G_e(b)P$ for
$P\in\operatorname{GL}_n(R)$," "the isometry class $[G_e(b)]$."

## `PR-60`: When a construction *chooses* data, state how it varies with the choice — or form the category whose objects carry the choice

Choosing an ordered basis $e$, a generating set $S$, a presentation
$F_2\to F_1\to X$, a point $x_0\in X$, a trivialization, etc., is not an
innocent "let $e$ be …" — it is extra data. The standard pattern is
always one of the two, stated explicitly:

* **(A) Comment on the choice:** after $G_e(b):=e^*b$, state how $G_e(b)$
  varies — $G_{e'}(b)=P^{\!t}G_e(b)P$ for $e'=e\circ P$, so $G_e(b)$ is
  well-defined up to $\operatorname{GL}_n(R)$-congruence (similarity,
  conjugacy, isometry, etc., per flavour), and invariants ($\det$,
  isometry class $[G_e(b)]$, $\operatorname{Val}(b)$) are independent of
  $e$. Without that, "$\operatorname{Gram}(b)$" with no $e$ is ill-typed
  (PR-58/PR-59).

* **(B) Form the category whose objects *carry* the choice, define the
  construction there, and study fibers/sections:** the Grothendieck
  construction whose objects are $(M,e)$ with $e$ the chosen data — e.g.
  framed $R$-modules $\mathbf{FMod}_R^{\mathrm{fr}}$ (objects $(M,e\colon
  R^n\xrightarrow{\sim}M)$), based modules (objects $(M,e)$ with $e$ a
  basis), pointed spaces $(X,x_0)$, presented modules/algebras/groups
  ($F_2\to F_1\to X$ with $X=\operatorname{coker}(F_2\to F_1)$), etc. Define
  e.g. $G\colon\mathbf{FMod}_R^{\mathrm{fr}}\to M_n(W)$,
  $((M,e),b)\mapsto G_e(b)$, then well-definedness on
  $\mathbf{Mod}_R$ is the study of the fiber over $M$ (the
  $\operatorname{GL}_n(R)$-torsor of frames) and its $\operatorname{GL}_n$-orbits,
  sections picking a frame, descent for the construction.

Either (A) or (B) is required whenever a construction chooses data.
Stating "$\operatorname{Gram}(b)$," "choose a presentation," "choose a
point" with no variance clause and no named $\mathbf{FMod}^{\mathrm{fr}}$ /
$\mathbf{PresMod}$ to host it leaves the construction ill-defined and its
dependence on the choice unfalsifiable.

**Banned:** "Put $G(b):=(b(e_i,e_j))$" with no $e$ and no
"$G_{e'}=P^{\!t}G_eP$ / well-defined up to $\operatorname{GL}_n$-congruence";
"choose a presentation $F_1\to X$ and define …" with no category whose
objects are $(X,F_1\to X)$ and no fiber/section discussion.

**Preferred:** (A) "For ordered basis $e\colon R^n\xrightarrow{\sim}M$, put
$G_e(b):=e^*b$. For $e'=e\circ P$, $G_{e'}(b)=P^{\!t}G_e(b)P$, so $[G_e(b)]$
is well-defined up to $\operatorname{GL}_n(R)$-congruence." Or (B) "Let
$\mathbf{FMod}_R^{\mathrm{fr}}\xrightarrow{U}\mathbf{Mod}_R$,
$(M,e)\mapsto M$ be the Grothendieck construction for frames. Define
$G\colon\mathbf{FMod}_R^{\mathrm{fr}}\to M_n(W)$ by $G((M,e),b):=G_e(b)$.
Then $G$ factors through $U$-fibers as $[G_e(b)]\in M_n(W)/\operatorname{GL}_n$."

## `PR-61`: $\operatorname{Gram}$ as written is overfit to free finite $W=R$ — $b\in\mathbf{Bil}_{R,W}(M)$ is a $W$-valued $(0,2)$-tensor, not a matrix, and $b(v,w)=\sum a_iG_{ij}c_j$ assumes $M=R^{(I)}$ and discrete finite support

The block "Let $M$ be free on $E=\{e_i\}_{i\in I}$, $b$ with values in $R$, $G_{ij}=b(e_i,e_j)$, $b(v,w)=\sum_{i,j}a_iG_{ij}c_j$ finite by finite support, every $(G_{ij})$ arises" is the $W=R$, free, $M=R^{(I)}$ specialization of $b\in\mathbf{Bil}_{R,W}(M):=\operatorname{Hom}_R(M\otimes_RM,W)$ written as if it were $\mathbf{Bil}_{R,W}$. An arbitrary $(M,b)$ — $M=\mathbb Q$, $\mathbb Q/\mathbb Z$, $\bigoplus_{\mathbb N}\mathbb Z$, $\mathcal O_X$-module, $\mathbf{Sp}$-module — has no $E$ and no $I\times I$ matrix, and a $W\neq R$ even on a free $M$ has $G_{ij}\in W$, not $R$.

Philosophy — never overfit to finite / finitely generated / finitely presented subcategories, never assume convergence or that topologies are discrete, never conflate a tensor with a multidimensional array or matrix unless extremely specific about the map from a matrix algebra to a Hom space / space of tensors, in which case its kernel and cokernel are the content (well-definedness, ambiguity).

Concrete standards:

* **$b$ as $W$-valued $(0,2)$-tensor.** For $R$ commutative and $W,M\in\mathbf{Mod}_R$, $b\colon M\otimes_RM\to W$ is $W$-valued covariant $2$-tensor — in index notation $b_{ij}$ with two *down* indices. When $W=R$ and $M\cong R^n$ finite free, $\operatorname{Hom}_R(M\otimes_R M,R)\cong M^\vee\otimes_R M^\vee$ is the $(0,2)$-tensor $b_{ij}$; an endomorphism is $(1,1)$-tensor $T^i_j\in\operatorname{Hom}_R(M,M)\cong M\otimes_R M^\vee$. $G_{ij}=b(e_i,e_j)$ as $(0,2)$ transforms by **congruence** $G_{e'}=P^{\!t}G_eP$ for $e'=eP$, $P\in\operatorname{GL}_n(R)$, i.e. $G_{e'\,kl}=\sum_{i,j}P^i_kP^j_lG_{e\,ij}$, while $(1,1)$ transforms by **similarity** $T_{e'}=P^{-1}T_eP$, $T^i_j\mapsto\sum_{k,l}(P^{-1})^i_kT^k_lP^l_j$. Writing both as "$G_{ij}$" and "$\sum a_iG_{ij}c_j$" conflates $(0,2)$ with $(1,1)$ (and with $(2,0)$ $W^\vee$-valued) and hides which $P$ acts on which side and whether $W$ is involved.

* **The map from matrices to tensors, not the identification.**
  Fix an ordered basis $e\colon R^n\xrightarrow{\sim}M$ (framed $((M,e),b)$). The $R$-linear $\Phi_e\colon M_{n\times n}(W):=W^{I\times I}\to\operatorname{Hom}_R(M\otimes_R M,W)$, $\Phi_e((G_{ij})):=e^*b$ with $b(e_i,e_j)=G_{ij}$, is an *isomorphism* only when $M=R^{(I)}$ free on $I$ and $W$ is discrete with $M^{(I)}$-finite support; its kernel/cokernel are the well-definedness/ambiguity content. For general $M$ the domain $M_{n\times n}(W)$ has no map to $\operatorname{Hom}_R(M\otimes_R M,W)$ at all — the matrix algebra and the space of $W$-valued $(0,2)$-tensors are not the same object.

* **The sum and $(L^2(\mathbb R),\int)$.** "$b(v,w)=\sum_{i,j}a_iG_{ij}c_j$, finite by finite support" is the coordinate shadow of $b\circ(e\otimes_R e)$ for $v=\sum_ia_ie_i$ with $a_i$ finitely supported — i.e. $M=R^{(I)}$ as *algebraic* free module with discrete topology. $(L^2(\mathbb R),\langle f,g\rangle:=\int_{\mathbb R}fg\in\mathbb R)$ is a perfectly reasonable $\mathbb R$-valued bilinear $\mathbb R$-module — $M:=L^2(\mathbb R)\in\mathbf{Mod}_{\mathbb R}$, $b(f,g):=\int fg\in\mathbb R$, $b\in\operatorname{Hom}_{\mathbb R}(L^2\otimes_{\mathbb R} L^2,\mathbb R)$ stably — but $L^2$ is not $\mathbb R^{(I)}$ for any $I$ (no Hamel basis gives $f=\sum a_ie_i$ finitely; no orthonormal basis gives algebraic finite sums; $f=\sum\langle f,e_i\rangle e_i$ is $L^2$-convergent, not finite). No $I\times I$ family $G_{ij}\in\mathbb R$ and no finite $\sum a_iG_{ij}c_j$ computes $\int fg$; the Gram "matrix" is the integral kernel $K$ with $\int fg=\iint f(x)K(x,y)g(y)$, i.e. the $(0,2)$-tensor as distribution, whose map $M_{I\times I}(\mathbb R)\to\operatorname{Hom}(L^2\otimes_{\mathbb R} L^2,\mathbb R)$ has huge kernel/cokernel. Never assume finite support / discrete topology.

**Banned:** the block as stated in $\mathbf{Bil}_{R,W}$ — "$M$ free on $E$, $b$ with values in $R$, $G_{ij}=b(e_i,e_j)$, $b(v,w)=\sum a_iG_{ij}c_j$ finite, every $(G_{ij})$ arises" as the definition of $\operatorname{Gram}$ for $(M,b)\in\mathbf{Bil}_{R,W}$.

**Preferred:** for $R$ commutative and $W,M\in\mathbf{Mod}_R$, put $b\in\mathbf{Bil}_{R,W}(M):=\operatorname{Hom}_R(M\otimes_R M,W)$ as $W$-valued $(0,2)$-tensor $b_{ij}$ with two down indices; for framed $((M,e),b)$, $e\colon R^n\xrightarrow{\sim}M$, put $G_e(b)_{ij}:=b(e_i,e_j)\in W$ and state $\Phi_e$ and its variance $G_{e'}=P^{\!t}G_eP$ (congruence, not similarity), with kernel/cokernel of $\Phi_e$ as the well-definedness content. Never write $G_{ij}$ for a $(1,1)$-tensor and a $(0,2)$-tensor without distinguishing, and never assume $M=R^{(I)}$ or finite $I$.

## `PR-62`: "$b(v,w)=\sum_{i,j}a_iG_{ij}c_j$" smuggles a Riesz theorem and the canonical $\langle v,w\rangle_0:=\sum_ia_ic_i$ on $F=R^{(I)}$ — eliding its hypotheses, completions, and the operator form $b(v,w)=\langle v,Aw\rangle$

The double sum as *definition* of how $b$ is evaluated assumes the
theorem "$\Phi_e\colon W^{I\times I}\xrightarrow{\sim}\operatorname{Hom}_R(R^{(I)}\otimes_R R^{(I)},W)$ and
$b(v,w)=\sum_{i,j}a_iG_{ij}c_j$" — i.e. that $b$ is determined by
$G_{ij}$ and evaluation pulls through the finite $a_i,c_j$. For
$F:=R^{(I)}$ algebraic free with discrete $W$, $\sum a_iG_{ij}c_j$ is
finite by finite support, so the statement holds with no convergence.
For non-free / non-algebraic $M$ it is a Riesz-type identification that
need not hold without honest hypotheses (finite $I$, $M$ finitely
generated projective, $W$ discrete, continuity, completeness).

What is elided is that $F$ already carries the *canonical* $R$-bilinear
$\langle v,w\rangle_0:=\sum_{i\in I}a_ic_i$ for $v=\sum a_ie_i$,
$w=\sum c_ie_i$ ($G_{ij}=\delta_{ij}$) — itself a $(0,2)$-tensor — well-defined
only with those finiteness/discreteness hypotheses ($a_i,c_i$ finitely
supported; for $I$ infinite or after completion to $\widehat F$,
$\sum a_ic_i$ is an infinite series whose existence *is* convergence in
$R$'s topology). Given that $\langle\,,\,\rangle_0$, any $b$ is
$b(v,w)=\langle v,Aw\rangle_0$ where $A\colon F\to F$ is the $R$-linear
with matrix $G_{ij}$ — $(Aw)_i=\sum_jG_{ij}c_j$ — i.e. $G$ is the
$(1,1)$-tensor $A$ seen as $(0,2)$ via $\langle\,,\,\rangle_0$:
$b_{ij}=\langle e_i,Ae_j\rangle_0$. The double sum is the coordinate
expansion of the single operator evaluation $\langle v,Aw\rangle_0$, and
"every $(G_{ij})$ arises" is the Riesz identification
$\mathbf{Bil}_{R,R}(F)\cong\operatorname{Hom}_R(F,F)$ via $\langle\,,\,\rangle_0$,
which is perfect on $F$.

Riesz as usually stated never writes the double sum: it is
"$b(v,w)=\langle v,Aw\rangle$ for a unique $A$ with … (symmetric $\iff$
$A$ self-adjoint, bounded / Hilbert-Schmidt / Fredholm / elliptic per the
topological hypotheses)," with the map $W^{I\times I}\to\operatorname{Hom}(F\otimes_R F,W)$
and its kernel/cokernel, and the convergence/completion hypotheses, made
explicit. The "$b(v,w)=\sum a_iG_{ij}c_j$ finite by finite support" elides
all of that, and defers the research extensions — completions,
topological tensor products, continuity — that will be needed anyway for
e.g. $(L^2(\mathbb R),\int)$ where $f=\sum\langle f,e_i\rangle e_i$ is
$L^2$-convergent, not finite.

Concrete standard — make the canonical form and the operator form
explicit, with hypotheses:

"::: {#rmk-canonical} **Remark.** $F:=R^{(I)}$ carries the tautological
$\langle v,w\rangle_0:=\sum_{i\in I}a_ic_i$ for $v=\sum a_ie_i$,
$w=\sum c_ie_i$ with $a_i,c_i$ finitely supported; it is the
$(0,2)$-tensor $\delta_{ij}$, well-defined only for $F$ algebraic free
discrete. For $b\in\mathbf{Bil}_{R,R}(F)$, put $A$ with
$A(e_j):=\sum_iG_{ij}e_i$; then $b(v,w)=\langle v,Aw\rangle_0$. Stably /
topologically this is $b\in\operatorname{Hom}_{\mathrm{cont}}(\widehat
F\hat\otimes\widehat F,W)\cong\{\text{matrices with summability}\}$. :::"

**Banned:** "$b(v,w)=\sum_{i,j}a_iG_{ij}c_j$, a finite sum by finite support
of the coordinates. Every family $(G_{ij})$ arises uniquely" as the
*definition* of evaluation for $(M,b)\in\mathbf{Bil}_{R,W}$.

**Preferred:** for $F=R^{(I)}$ state the Proposition with honest
hypotheses — "$\Phi_e\colon W^{I\times I}\xrightarrow{\sim}
\operatorname{Hom}_R(F\otimes_R F,W)$ via $G_{ij}=b(e_i,e_j)$ is an iso for
$F$ free on finite $I$ (resp. algebraic $R^{(I)}$ discrete), with
$b(v,w)=\langle v,Aw\rangle_0$ for $A$ as above" — and for general
$(M,b)$ keep $b\colon M\otimes_R M\to W$ as $(0,2)$-tensor, not a double
sum.

## `PR-63`: One bilinear setup must simultaneously generalize the arithmetic local, the geometric global, and the analytic — do not overfit to finite / discrete and defer the extensions that will be needed anyway

The Gram block as written is overfit to the arithmetic *finite* free
$W=R$ case ($M=R^{(I)}$ algebraic, $I$ finite, $W$ discrete,
$b(v,w)=\sum a_iG_{ij}c_j$ finite) and elides that the same $b\colon
M\otimes_R M\to W$ must already work for the geometric and analytic
specializations that the document will need anyway. Any definition that does
not immediately generalize to topological groups/modules/algebras,
schemes/stacks, sheaves, derived categories, infinite-dimensional/rank
modules should be taken as a sign the definition is overfit.

Philosophy — never overfit to finite / finitely generated / finitely
presented subcategories, never assume convergence or that topologies are
discrete (PR-61/PR-62), and always ask if the statement immediately
generalizes:

* **Arithmetic local theory:** finitely generated $R$-modules, tensors
  $M\otimes_RM$, $W$-valued forms $b\colon M\otimes_R M\to W$,
  $\operatorname{Val}(b)$, $b^{\sharp}$, $M^\vee$, $D_L$, Grothendieck–Witt
  theory as the study of $(M,b)$ over local $R$ (strict henselizations,
  completions).

* **Geometric global theory:** schemes/stacks, $\mathrm{QCoh}(X)$,
  $M\in\mathrm{QCoh}(X)$ with $\mathcal W$-valued $b\colon M\otimes_{\mathcal
  O_X}M\to\mathcal W$, where taking stalks / local rings recovers the
  arithmetic theory, or manifolds with bundles $E\to X$ assembling the
  local $(V,b_V)$ continuously/smoothly — symplectic manifolds as the
  geometric instance of a nondegenerate alternating $b$ on $TX$, etc.

* **Analytic theory:** functional analysis, $L^p$/Hardy spaces,
  (partial) differential operators, Banach/Hilbert $R$-modules
  $(L^2(\mathbb R),\int)$, $b(f,g)=\int fg$, where
  $b(v,w)=\langle v,Aw\rangle$ is Riesz with $A$ bounded / self-adjoint /
  Hilbert-Schmidt / Fredholm / elliptic and the double sum is $L^2$-convergent,
  not finite.

One conjoined general categorical setup — $M\in\mathcal C$ in a closed
symmetric monoidal $\mathcal C$ with $b\colon M\otimes M\to W$ as
$W$-valued $(0,2)$-tensor, self-enrichment, $\Gamma^2_R$, etc. — does all
three at once, and recovers symplectic manifolds as the geometric theory,
Grothendieck–Witt as the arithmetic local, and Riesz theorems as the
analytic. Overfitting to $M=R^{(I)}$ finite, $W=R$ discrete with
$\sum a_iG_{ij}c_j$ finite defers the geometric/analytic extensions that
will be needed anyway and forces a rewrite.

**Standard:** define $b\in\mathbf{Bil}_{R,W}(M)$ once as above for
$W,M\in\mathcal C$ arbitrary; prove the finite free $W=R$ Gram matrix
and the finite-sum evaluation as the *specialization* to
$M=R^n$ discrete, not as the definition. Then ask of every new statement:
does it hold for $\mathrm{QCoh}(X)$, for $L^2(\mathbb R)$ with its
Hilbert topology, and for $M$ not finitely generated? If not, the
statement is overfit.

## `PR-64`: Definitions are atomic units — one definition per fenced block, with only rare grouping of tightly related definitions; Lemmas / Propositions / Remarks are never in a Definition block

A fenced `Definition` is an atomic unit with one logical status: it
introduces one notion (or one tightly related family, e.g. the four
flavours symmetric / skew / alternating / even via the same
$b\colon M\otimes_R M\to W$, $\tau$, $\Delta$, $\Gamma^2$). Grouping
several *related* definitions in one block is the rare exception and
requires each to be clearly enumerated as a definition. A Lemma,
Proposition, Theorem, or Remark is never in that block — not even as a
trailing sentence.

This is the explicit form of DEF-15/DEF-19 and SEC-6 (one notion per
fenced block, skeleton complete after deleting glue): a Definition block
defines; implications between defined subobjects ($\operatorname{Alt}\subseteq
\operatorname{Skew}$, converse when $2$ injective), obstructions
($2_*$ / $\gamma^*$), and side observations ("when $2W=W$ every $b$ is
even") are separate fenced `Lemma` / `Proposition` / `Remark` blocks
with quantified hypotheses and proofs, even when the material is "not
hard to prove — but that does not give license to hand-wave it" (PR-48).

**Banned:** `::: {#def-form-axioms} For b: … - b symmetric if …; …;
Alternating forms are skew-symmetric. The converse holds when 2 injective.
When 2W=W, every b satisfies …; quadratic refinements retain … :::`
— four definitions plus a Lemma plus a Proposition plus a Remark in one
`Definition`.

**Preferred:** `::: {#def-symmetric} b is symmetric if $b\circ\tau=b$ :::`
(and similarly for skew / alternating / even, either as four fenced
`Definition`s or as one fenced `Definition` that clearly enumerates the
four related definitions), then separate
`::: {#lem-alt-skew} Lemma. AltBil⊆SkewBil. Proof. … :::`,
`::: {#prop-skew-alt} Proposition. Skew=Alt iff 2:W↪W injective. … :::`,
`::: {.Remark} When 2W=W the element condition is vacuous; the content
is the fiber of γ^* … :::` — one status per block.

## `PR-65`: A free-floating "`**Remark.**` … $G_e(b)=\begin{pmatrix}0&1\\1&0\end{pmatrix}$ … $b(e_1+e_2,e_1+e_2)=2$" with no claim has almost no epistemic status and is not self-contained

A fenced unit has epistemic status only as an instance or counterexample
*to* a quantified proposition. The block as written gives data
$((\mathbb Z^2,e),b)$ with $G_e(b)=\begin{pmatrix}0&1\\1&0\end{pmatrix}$
and computes $b(e_i,e_i)=0$ ($G_{ii}=0$) and $b(e_1+e_2,e_1+e_2)=2$, but
states no universal it exemplifies — not "there exists $b$ symmetric with
$G_{ii}=0$ but $b\notin\operatorname{AltBil}$," not "vanishing on a basis
does not imply $b\circ\Delta=0$," not
"$\{b\mid\forall i\,b(e_i,e_i)=0\}\not\subseteq\operatorname{AltBil}$ as
$R$-submodules" — so deleting it leaves the skeleton unchanged (SEC-6) and
meeting it alone a reader cannot tell why the calculation is being done or
what it shows.

It is also not self-contained: a self-contained `Example` states what it
is an example *of*, why the calculation is done, and what it shows,
without external prose. And it repeats the $((M,e),b)$ vs. $(M,b)$
conflation (PR-58/60): "$\operatorname{Gram}$" with no $e$, "$\mathbb Z^2$
with Gram matrix …" instead of "$((\mathbb Z^2,e),b)$ with
$G_e(b)=\dots$," and "$b(e_1+e_2,e_1+e_2)=2$" as the $U$-evaluation of
$b\circ\Delta\neq0$ instead of "$b\notin\operatorname{AltBil}$."

Concrete standard — fenced, labelled, with the quantified claim and its
negated containment made explicit:

"::: {#exm-U-not-alternating} **Example.** Vanishing on a basis does not
imply alternating. Let $e=(e_1,e_2)\colon\mathbb Z^2\xrightarrow{\sim}
\mathbb Z^2$ be the standard ordered basis and put
$G_e(b):=\begin{pmatrix}0&1\\1&0\end{pmatrix}=e^*b\in M_2(\mathbb Z)$ for
$b\colon\mathbb Z^2\otimes_{\mathbb Z}\mathbb Z^2\to\mathbb Z$. Then $b$ is symmetric
($b\circ\tau=b$) with $G_{ii}=b(e_i,e_i)=0$ for $i=1,2$, but
$b\notin\operatorname{AltBil}_{\mathbb Z,\mathbb Z}(\mathbb Z^2)$ since
$(b\circ\Delta)(e_1+e_2)=b(e_1+e_2,e_1+e_2)=2\neq0$. Hence
$\{b\mid\forall i\,b(e_i,e_i)=0\}\not\subseteq\operatorname{AltBil}$ as
$R$-submodules. :::"

A `Remark` is secondary pedagogy *after* the primary Definition/Lemma/
Proposition/Example it remarks on, not a primary Example smuggled as a
bold-`Remark.` sentence.

**Banned:** "`**Remark.**` The symmetric form on $\mathbb Z^2$ with Gram
matrix $\begin{pmatrix}0&1\\1&0\end{pmatrix}$ has vanishing diagonal and
$b(e_1+e_2,e_1+e_2)=2$."

**Preferred:** the fenced `Example` above — names $((\mathbb Z^2,e),b)$ and
$G_e(b)$, states the quantified universal it refutes, shows
$b\notin\operatorname{AltBil}$ via $b\circ\Delta$, and is self-contained.

## `PR-66`: Every definition must be valid in the functional-analytic setting — finite collapse is a Proposition, not a definition, and is why diagrammatic / categorical definitions are preferable

A definition that is correct for $R^n$ ($W^{I\times I}\to\operatorname{Hom}(R^{(I)}\otimes R^{(I)},W)$ is an iso, $x^{\!t}Ay:=\sum_{i,j}x_iG_{ij}y_j$ finite, every $G$ bounded, symmetric $=$ self-adjoint, $\det$ defined on all $G$) need not be correct for $L^2(\mathbb R)$, $\mathrm{QCoh}(X)$, $\mathbf{Sp}$-modules — where $b(f,g)=\int fg$ has no finite $G_{ij}$, no finite $\sum a_iG_{ij}c_j$, and bounded $\neq$ symmetric $\neq$ self-adjoint $\neq$ normal thread apart, $x^{\!t}Ay$ has no $x_i$, and the matrix is replaced by the kernel $K$ with $b(f,g)=\iint f(x)K(x,y)g(y)$ and $K$ is $L^2$ / distribution per summability (Schwartz kernel theorem). All definitions in the document must work at that precision — i.e. as stated they must be equally valid for $L^2(\mathbb R)$ / $C^0$ / $\mathcal S$ / $\mathrm{QCoh}(X)$ / $\mathbf{LMod}_R$ — and when they do collapse in the finite ($I$ finite, $R^n$ discrete, $M$ finitely generated projective) specialization, that collapse is a *Proposition* to be stated with honest hypotheses and either cited or proved, not the definition.

This is why categorical / diagrammatic definitions are preferable when available: $b\colon M\otimes M\to W$ with $b\circ\tau=b$ / $b^{\sharp}\colon M\to\underline{\operatorname{Hom}}(M,W)$ / $\ker(b^{\sharp})$ / $\Gamma^2_R(M)$ are already valid in every closed symmetric monoidal $\mathcal C$ (arithmetic, geometric, analytic) and their $U$-evaluation on $x\otimes y$ recovers the finite $b(x,y)=b(y,x)$ / $\sum a_iG_{ij}c_j$ as a theorem, not a definition; the converse — defining by the finite sum and hoping it generalizes — does not work.

**Banned:** a definition quantified as "$\forall x\in M$, $b(x,y)=b(y,x)$ / $b(x,x)\in2W$ / $M$ free on $E$, $G_{ij}=b(e_i,e_j)$, $b(v,w)=\sum a_iG_{ij}c_j$" that is correct only for $R^n$ / $R^{(I)}$ discrete and is used as the general $W$-valued bilinear on $M\in\mathbf{Bil}_{R,W}$.

**Preferred:** define $b\colon M\otimes_RM\to W$ as $W$-valued $(0,2)$-tensor, $b^{\sharp}$, $\Gamma^2_R$, $\operatorname{Val}(b)$, $N^{\perp}:=\ker(b^{\sharp})$, etc., diagrammatically in a closed symmetric monoidal $\mathcal C$ so that the statement is valid for $L^2(\mathbb R)$ / $\mathrm{QCoh}(X)$ / $\mathbf{LMod}_R$; then prove as a *Proposition* (with hypotheses: $I$ finite, $M\cong R^n$, $M$ finitely generated projective, $W$ discrete, continuity / boundedness): "$\Phi_e\colon W^{I\times I}\xrightarrow{\sim}\operatorname{Hom}_R(R^{(I)}\otimes R^{(I)},W)$ is an iso, every $b$ has a $G_{ij}$, $b(v,w)=\sum a_iG_{ij}c_j$ finite, and $x^{\!t}Ay$ is $b(v,w)=\langle v,Aw\rangle$ with $A$ symmetric $\iff$ self-adjoint," etc. — the finite accident as a theorem, not the definition.

## `PR-67`: Twist is any $\varphi\colon W\to W'$ — $\mathbf{Bil}_R(-)$ is functorial in $W$ — not just $\lambda\in R$ and not just $\lambda\in R^\times$ / $\mathbf{Pic}$

For $R$ commutative, $\mathbf{Bil}_{R,W}$ is functorial in the *value
module* $W\in\mathbf{Mod}_R$: any $R$-linear $\varphi\colon W\to W'$
induces $\varphi_*\colon\mathbf{Bil}_{R,W}\to\mathbf{Bil}_{R,W'}$,
$(M,b\colon M\otimes_R M\to W)\mapsto(M,\varphi\circ b\colon M\otimes_R M\to W')$
by post-composition. When $W'=W$, an endomorphism $\varphi\colon W\to W$
induces an endofunctor $\varphi_*$ on $\mathbf{Bil}_{R,W}$; *any*
$\varphi\in\operatorname{End}_R(W)$ defines a twist. The usual
"$\lambda b$" is the specialization $\varphi:=\lambda\cdot_W\colon W\to W$,
$w\mapsto\lambda w$ via the $R$-action $R\to\operatorname{End}_R(W)$ — one
endomorphism among all $\operatorname{End}_R(W)$, and not requiring
$W=R$ or $\lambda$ invertible.

Stating twist as "$\lambda\in R$, $b(\lambda):=\lambda b$ on the same
$M$, $G\mapsto\lambda G$" fixes $W=R$ and a global element $\lambda$ and
hides the functoriality that is already in the type $b\colon M\otimes_R M\to W$.

Concrete standard — name $\varphi$ and $\varphi_*$:

"::: {#def-twist} **Definition.** For $\varphi\colon W\to W'$ in
$\mathbf{Mod}_R$, put
$\varphi_*\colon\mathbf{Bil}_{R,W}\to\mathbf{Bil}_{R,W'}$,
$\varphi_*(M,b):=(M,\varphi\circ b)$. When $W'=W$, $\varphi_*$ is the
**twist by $\varphi$** of the $W$-valued form. In particular for
$\lambda\in R$, $\varphi:=\lambda\cdot_W$ gives $(M,b)(\lambda):=
(M,\lambda b)$ with $\lambda b:=\varphi\circ b$ and
$G_e(\lambda b)=\lambda G_e(b)$, $(\lambda b)^{\sharp}=\lambda\cdot b^{\sharp}$.
:::"

**Banned:** "For $\lambda\in R$ the twist $b(\lambda)$ of $(M,b)$ is
$\lambda b$ on the same module, $M(\lambda)$, with $\lambda G$ and
$\det(b(\lambda))=\lambda^n\det(b)$" as the *definition* of twist for
$(M,b)\in\mathbf{Bil}_{R,W}$.

**Preferred:** define $\varphi_*$ for any $\varphi\colon W\to W'$ as above;
then note $\lambda\cdot_W$ as the case $\varphi:=\lambda\cdot_W$, and
prove $G_e(\lambda b)=\lambda G_e(b)$ and, only for framed finite free
$M\cong R^n$ with $W=R$, $\det(G_e(\lambda b))=\lambda^n\det(G_e(b))$ as a
*consequence* with hypotheses, not as the definition.

## `PR-68`: Heuristic that makes the generalization obvious — read the type of every parameter as an object, then ask variance

The twist generalization is not a trick to remember — it is forced by
one habit: read every parameter of a definition as an *object* of a
category, then ask how the construction varies functorially in that
parameter. That habit, applied systematically, rediscovers the
generalisations in this document without remembering them.

Timeless heuristics that generalize (use on every new definition):

* **Functoriality in the parameter.** $b\colon M\otimes_R M\to W$ exhibits
  $W$ as the codomain object $W\in\mathbf{Mod}_R$ of
  $\operatorname{Hom}_R(M\otimes_R M,W)=\mathbf{Bil}_{R,W}(M)$. Any
  $R$-linear $\varphi\colon W\to W'$ post-composes to
  $\varphi_*\colon\operatorname{Hom}(M\otimes_R M,W)\to\operatorname{Hom}(M\otimes_R M,W')$,
  $b\mapsto\varphi\circ b$. So $\mathbf{Bil}_R(-)$ is a functor
  $\mathbf{Mod}_R\to\mathbf{Cat}$ in $W$ by definition — $W\mapsto\mathbf{Bil}_{R,W}$,
  $\varphi\mapsto\varphi_*$ — and a twist is $\varphi_*$ when $W'=W$.

* **Element $\to$ morphism.** "$\lambda\in R$" acting as "$\lambda b(x,y)$"
  is the shadow of the morphism $\varphi:=\lambda\cdot_W\colon W\to W$
  in $\mathbf{Mod}_R$ ($R\to\operatorname{End}_R(W)$). Replace the element
  by the morphism it names; the general is any $\varphi\in\operatorname{End}_R(W)$,
  not just $\lambda\cdot_W$.

* **Variance.** $\mathbf{Bil}_{R,W}(M)=\operatorname{Hom}_R(M\otimes_R M,W)$ is
  covariant in $W$ (post-composition) and contravariant in $M$
  ($(f\otimes_R f)^*$), so $W\to W'$ gives $\mathbf{Bil}_W\to\mathbf{Bil}_{W'}$
  and $f\colon M\to N$ gives $\mathbf{Bil}(N)\to\mathbf{Bil}(M)$.

* **Grothendieck construction for the parameter.** The categories
  $\mathbf{Bil}_{R,W}$ assemble to the fibered category
  $\int_{W\in\mathbf{Mod}_R}\mathbf{Bil}_{R,W}$ whose fiber over $W$ is
  $\mathbf{Bil}_{R,W}$ and whose cartesian transport is $\varphi_*$. A
  definition that fixes $W$ and $\lambda$ is the fiber at one $W$ with one
  $\varphi$.

To rediscover a forgotten generalization: re-read the definition as a Hom
in its codomain, list the categories of its parameters ($W\in\mathbf{Mod}_R$,
$M\in\mathbf{Mod}_R$, $b\in\operatorname{Hom}(M\otimes_R M,W)$), and ask "what
$\operatorname{Hom}$-maps in those categories could act here?" The answer is
forced by type: $W\to W'$ must act by $\varphi\circ b$, $M\to N$ by
$b\circ(f\otimes_R f)$, and the special $\lambda$ is the single $\varphi$
coming from $R\to\operatorname{End}(W)$.

## `PR-69`: Prose "greatest dimension of a subspace on which $b$ is positive definite" for the hard equations $V\cong P\perp Q\perp\operatorname{rad}(V)$ and $G_e(b)\cong\operatorname{diag}(1^p,-1^q,0^r)$ — Sylvester's law hand-waved as language

"Write $p$ for the greatest dimension of a subspace on which $b$ is
positive definite" looks like a definition by a set-theoretic $\max$,
but the content is the *existence* of an orthogonal decomposition
$V\cong P\perp Q\perp\operatorname{rad}(V)$ in $\mathbf{Bil}_{F,F}$ with
$b_{|P}>0$, $b_{|Q}<0$, and its invariance — Sylvester's law — i.e.
$G_e(b)\cong\operatorname{diag}(1^p,-1^q,0^r)$ for a framed $((V,e),b)$
and $(p,q,r)$ with $p+q+r=n$ as the $\operatorname{GL}_n(F)$-congruence
invariant, with $p=\max\{\dim U\mid b_{|U}>0\}$ *attained* and
$p+q+r=n$. The prose hides that a maximum (not just supremum) exists,
that $p,q$ are well-defined (independent of the $U$ attaining them),
that $p+q+r=n$, and that $(p,q,r)$ classifies $b$ up to isometry — all
of which are the orthogonal diagonalization, not language.

Concrete standard — state the equations, then $p,q,r$ are the normal
form:

"::: {#def-signature} **Definition.** Let $F$ be ordered, $V\in\mathbf{Vect}_F$
finite-dimensional, $b\colon V\otimes V\to F$ symmetric. Put
$\operatorname{rad}(V):=\ker(V\xrightarrow{b^{\sharp}}V^\vee)$,
$r:=\dim_F\operatorname{rad}(V)$. By Sylvester there exists an orthogonal
$V\cong P\perp Q\perp\operatorname{rad}(V)$ with $b_{|P}>0$,
$b_{|Q}<0$; put $p:=\dim_FP$, $q:=\dim_FQ$. Then $p+q+r=\dim_FV$ and
$G_e(b)\cong\operatorname{diag}(1^p,-1^q,0^r)$ for any ordered basis $e$.
The triple $(p,q,r)$ is the **signature** of $b$. In particular
$p=\max\{\dim U\mid b_{|U}>0\}$ and $q=\max\{\dim U\mid b_{|U}<0\}$ are
attained. :::"

**Banned:** the block as stated — "$p$ is the greatest dimension of a
subspace on which $b$ is positive definite" with no $V\cong P\perp
Q\perp\operatorname{rad}$, no $G_e(b)\cong\operatorname{diag}(1^p,-1^q,0^r)$,
no Sylvester.

**Preferred:** define $p,q,r$ via the orthogonal sum and the Gram normal
form as above, with $b_{|P}>0$ / $b_{|Q}<0$ as $R$-submodule conditions,
then note $p,q$ as the attained maxima as a *consequence*.

## `PR-70`: Overly restricted hypotheses to avoid the sup — $F$ ordered, $V$ finite-dimensional, "$\max$" instead of "$\sup$" on $F$ / the flag variety

"Let $F$ be an ordered field and $V$ finite-dimensional, $p:=\max\dim U$
with $b_{|U}>0$" restricts to the case where the invariant is a
*maximum* over subspaces, so it can be stated as "$\max$" with
$p+q+r=n<\infty$ without ever saying "sup." The general
($F$ ordered, $b\colon V\otimes V\to F$ symmetric, $V$ arbitrary
$F$-vector space, possibly infinite-dimensional) is not harder: put

* $p:=\sup\{\dim_FU\mid U\subseteq V,\ b_{|U}>0\}$ and
  $q:=\sup\{\dim_FU\mid b_{|U}<0\}$ as suprema in $\mathbf{Card}$ (or
  $\mathbb N\cup\{\infty\}$ in the countable case), $r:=\dim_F\operatorname{rad}(V)$
  with $\operatorname{rad}(V):=\ker(b^{\sharp})$,

as suprema over the flag variety $\operatorname{Gr}(V)$ of subspaces /
over $F$-points of the variety of $b$-positive flags — i.e. a sup in $F$
with its order topology / on $\mathrm{Fl}(V)$. The signature is
$(p,q,r)\in\mathbf{Card}^3$.

Then the finite-dimensional case is the *remark* that the suprema are
attained and $p+q+r=\dim_FV=n$, so "$\sup$" can be written "$\max$" and
$G_e(b)\cong\operatorname{diag}(1^p,-1^q,0^r)$ via Sylvester; the
definition itself needs no finiteness.

Stating it only for $V$ finite-dimensional and as "$\max$" avoids ever
saying "sup" (in $F$ or on $\mathrm{Fl}(V)$) and lets well-definedness be
the elementary "$\max$ over finitely many dimensions" instead of the
one-line sup that already works generally.

**Banned:** the block as stated with "$F$ ordered, $V$ finite-dimensional,
$p$ is the greatest dimension …" as the *definition* of signature.

**Preferred:** define $(p,q,r)$ via the suprema as above for arbitrary
$V$ (fenced, with $\operatorname{rad}(V)$ via $b^{\sharp}$), then add:
"::: {.Remark} When $\dim_FV=n<\infty$, the suprema are attained, $p$ and
$q$ are the greatest dimensions, $p+q+r=n$, and $G_e(b)\cong\operatorname{diag}
(1^p,-1^q,0^r)$. :::" The finite case as specialization, not the
definition.

## `PR-71`: For any stated result or definition, ask if it can be reasonably extended — if "hypothesis $X$ relaxed, is it that much harder?" is no, do it and recover the special case

For every Definition / Proposition / Theorem as stated, go through all
permutations of its hypotheses and ask: "Is the statement with $X$
relaxed / removed that much harder to state or prove?" If the answer is
no — and it is surprisingly often no — state the general form and
recover the desired specialization as a Remark / Corollary. Choosing the
restricted form to avoid the general sup / infinite-dimensional / $W\neq
R$ / non-free case saves nothing and forces a rewrite when the
geometric / analytic specialization is needed anyway (PR-63, PR-66, PR-70).

This is the general form behind PR-61/PR-63 (free $W=R$ finite $M=R^{(I)}$
discrete vs. $M\in\mathbf{Mod}_R$ arbitrary with $b\colon M\otimes_R M\to W$),
PR-66/PR-70 ($V$ finite-dimensional ordered $F$ with $\max$ vs. $V$
arbitrary with $\sup$ in $\mathbf{Card}$ / on $\mathrm{Fl}(V)$),
PR-58/60 (no framing vs. framed $((M,e),b)$ with variance clause), and
PR-69 (prose $\max$ vs. hard $V\cong P\perp Q\perp\operatorname{rad}$).

Concrete check — on every new unit, ask explicitly:

* Finite $\to$ arbitrary ($n<\infty$ vs. $I$ arbitrary, $M$ finite free vs.
  $M\in\mathbf{Mod}_R$, $V$ finite-dimensional vs. arbitrary, $\max$ vs.
  $\sup$)?
* $W=R$ vs. $W\in\mathbf{Mod}_R$ varying (PR-37)?
* Free $M=R^{(I)}$ vs. $M$ arbitrary (projective / not free vs. $L^2$)?
* Discrete topology / finite support vs. topological / $L^2$-convergent
  (PR-61/PR-62)?
* $R$ commutative / $2$ invertible vs. general $R$ / $2$ not invertible
  (PR-48)?

If the general $W$-valued $(0,2)$-tensor $b\colon M\otimes_R M\to W$ as
$R$-module, or the sup $(p,q,r)\in\mathbf{Card}^3$ on $\mathrm{Gr}(V)$,
is one line more and the proof is Sylvester with the same $b^{\sharp}$
/ $\Gamma^2_R$, state the general and add "::: {.Remark} When
$\dim_FV=n<\infty$, this gives $p=\max\ldots$, $p+q+r=n$, and
$G_e(b)\cong\operatorname{diag}(1^p,-1^q,0^r)$. :::" — the special case
desired is recovered without loss.

**Banned:** the block as stated with "$F$ ordered, $V$ finite-dimensional,
$M$ free on $E$, $b$ with values in $R$, $p$ is the greatest dimension …"
as the *definition*, when the sup / $W$-valued / $M$ arbitrary form is
one line more and the same proof works.

**Preferred:** state the general $b\colon M\otimes_R M\to W$ / $\sup$ /
$M$ arbitrary / $W$ varying form fenced, then the finite $W=R$ / $V$
finite-dimensional / $M=R^n$ / $G_{ij}$ / $\max$ specialization as a
fenced Remark / Corollary that recovers the desired case. Always perform
the permutation check; if not much harder, the general is the definition.

## `PR-72`: Premature specialization as the definition — signature $(p,q,r)$ for $F$ ordered finite-dimensional, and $\operatorname{sig}(L)$ for $L\in\mathbf{Lat}_R$ — and the explicit scope that was owed

The block "`$F$ ordered, $V$ finite-dimensional, $p:=\max\dim U$ with
$b_{|U}>0$" is *sound* for $F$ a field — every field has IBN, so
$\dim_FU$ is well-defined and $\{\dim U\mid b_{|U}>0\}\subseteq
\{0,\dots,n\}$ has a $\max$ — and Sylvester's law makes $(p,q,r)$ an
isometry invariant, so it does define the expected $GW(F)\to\mathbb Z$
(for the fixed ordering, $r:=\dim\operatorname{rad}$) for any ordered
field. It is not ill-typed in its stated scope. What it *is* is a
one-real-place, finite-dimensional, $W=F$ specialization presented as
*the* definition, so it quietly fixes the document to $F=\mathbb Q$ / $\mathbb R$
and cuts off the arithmetic the lattice theory is about.

Concretely:

* **Soundness vs. IBN.** "$\dim$" in the definition assumes IBN for $F$.
  Every field has IBN, so for $F$ a field the $\max$ is well-defined; if
  the same "$\max\dim$" were used for an ordered *ring* $R$ without IBN,
  "$\dim_RU$" would have no referent and $(p,q,r)$ would be ill-defined.
  Soundness as written is exactly the field case.

* **$\operatorname{sig}(L)$ not over $R$.** For $L\in\mathbf{Lat}_R$ ($R$ a
  domain, e.g. $\mathbb Z$, $\mathcal O_K$, $\mathbb Z_p$) the $R$-linear
  $b\colon L\otimes_RL\to R$ has no "$b_{|U}>0$" — $R$ is not ordered.
  The invariant is $\operatorname{sig}(L):=\operatorname{sig}(L\otimes_RF,
  b_F)$ for $F:=\operatorname{Frac}(R)$ via change-of-rings
  $-\otimes_RF\colon\mathbf{Mod}_R\to\mathbf{Vect}_F$, $b_F:=b\otimes_RF
  \colon L_F\otimes_FL_F\to F$ (PR-69/70 with $F$ ordered, $L_F$ finite-
  dimensional where the $\max$ is attained). Writing "$\operatorname{sig}(L)$"
  without the $-\otimes_RF$ is ill-typed.

* **Specialization, not the notion.** As the definition of signature it
  rules out the cases where signature has no meaning and hides the cases
  where it has a *family* of meanings:

  — $F=\mathbb F_q$ ($\operatorname{Frac}(R)=\mathbb F_q$ for
  $R=\mathbb F_q$) is a field but not ordered, so "$b_{|U}>0$" is not
  typed and there is no $(p,q,r)$; $W(\mathbb F_q)$ is detected by
  $\dim\bmod2$ and discriminant in $\mathbb F_q^\times/(\mathbb F_q^\times)^2$
  (Arf when $2=0$), not a signature — correctly ruled out.

  — $F=\mathbb C$ is a field but not ordered, so no $(p,q,r)$;
  $W(\mathbb C)\cong\mathbb Z/2$ via $\dim\bmod2$.

  — $F=\operatorname{Frac}(R)$ for $R=\mathcal O_K$, $K$ a number field,
  has $[K:\mathbb Q]$ real embeddings $\sigma\colon K\hookrightarrow\mathbb R$
  (and complex pairs). The $F$-linear $b_F$ has no single $(p,q,r)$; it
  has a family $(p_\sigma,q_\sigma,r_\sigma)_{\sigma\text{ real}}$ with
  $p_\sigma:=\sup\dim_{K_\sigma}U$ where $\sigma(b)_{|U}>0$ in the ordered
  $K_\sigma\cong\mathbb R$ — i.e. $\operatorname{sig}_\sigma(L):=
  \operatorname{sig}(L\otimes_RK\xrightarrow{\sigma}L\otimes_R\mathbb R)$.
  Lattices over $\mathcal O_K$ are the arithmetic case where signature is a
  vector over the real places.

* **Explicit scope that was owed, and flagging.** The local/arithmetic
  object is $L\in\mathbf{Lat}_R$ for $R$ a Dedekind domain — $\mathbb Z$,
  $\mathbb Z_{(p)}$, $\mathbb Z_p$, $\mathcal O_K$ (often
  $\operatorname{cl}(R)=1$ so $L\cong R^n$ as $R$-module, but the theory must
  not assume it), $R=\mathbb Z_p$, $\mathbb Q_p$, $\mathbb C_p$,
  $\mathbb A_{\mathbb Q,f}$, $\mathbb A_K$, etc. — with $b\colon L\otimes_RL
  \to R$ (or $W$ invertible). For $R=\mathbb Z_p$, $\operatorname{Frac}(R)=
  \mathbb Q_p$ is not ordered, so again no $(p,q,r)$; the $p$-adic
  invariants are rank, discriminant, Hasse. A definition fitted to
  "$\mathbb Z\to\mathbb Q$ plus a little more" ($F$ ordered finite-dimensional
  with $\max$) therefore presents the $\mathbb R$-specialization as if it
  were the notion and lets the document proceed without ever naming the general
  $W$-valued $b\colon M\otimes_R M\to W$ over a Dedekind $R$, its base changes
  $L\otimes_RF$, $L\otimes_RK_\sigma$, $L\otimes_R\mathbb Q_p$,
  $L\otimes_R\mathbb A$, and the invariants that actually do the work there.
  It should have been flagged at the point of writing as *needs research* /
  *needs generalization* — not as a definition to build on — with the
  explicit note that the arithmetic local theory (arbitrary Dedekind $R$,
  $p$-adic $R$, adeles) requires the sup-on-$\mathrm{Fl}$ / $b^{\sharp}$ /
  $\Gamma^2_R$ setup and a separate treatment of $(p,q,r)$ as the
  $\mathbb R$-fiber of that setup.

**Standard:** in the document's scaffolding and in this `CONTRIBUTING.md`,
state the explicit generalization scope most definitions should be at:

> "Bilinear/quadratic notions are $W$-valued $b\colon M\otimes_RM\to W$
> for $R$ a Dedekind domain (in particular $\mathbb Z$, $\mathcal O_K$,
> $\mathbb Z_p$) and $W\in\mathbf{Mod}_R$ invertible, with
> $M\in\mathbf{Mod}_R$ arbitrary; signature $(p,q,r)$ is the
> $\mathbb R$-fiber $L\mapsto(L\otimes_RF_\sigma,b_{F_\sigma})_{\sigma
> \text{ real}}$ for $F=\operatorname{Frac}(R)$ ordered at $\sigma$,
> $p_\sigma:=\sup\dim_{F_\sigma}U$ on $\mathrm{Gr}(L_{F_\sigma})$, and is
> not defined for $F=\mathbb C$, $\mathbb F_q$, $\mathbb Q_p$."

Then every new definition is reviewed against that scope, and a block that
only does $F$ ordered finite-dimensional with $\max$ is flagged *outside*
the document (GitHub issue with `needs-research`, not a fenced Definition)
until the $R$ Dedekind / $\mathbb Z_p$ / $\mathbb A$ / $W$-varying form is
supplied. The finite $W=R$, $V$ finite-dimensional, $\max$ specialization
is then a fenced Remark / Corollary that recovers the desired case.

**Banned:** the block as stated with "$F$ ordered, $V$ finite-dimensional,
$p$ is the greatest dimension … triple $(p,q,r)$ is the signature" as the
*definition* of signature for $L\in\mathbf{Lat}_R$.

**Preferred:** define $(p,q,r)$ via the suprema on $\mathrm{Gr}(V)$ /
$\mathrm{Fl}(V)$ for $F$ ordered arbitrary $V$ as in PR-70, then add the
fenced scope note above and the flagged `needs-research` for the
Dedekind / $p$-adic / adele generalization; define
$\operatorname{sig}(L):=\operatorname{sig}(L\otimes_R\operatorname{Frac}(R))$
only when $\operatorname{Frac}(R)$ is ordered at the relevant $\sigma$,
with $r:=\dim\operatorname{rad}$ via $b^{\sharp}$, and note that for
$F=\mathbb C$, $\mathbb F_q$, $\mathbb Q_p$ the invariant is not
$(p,q,r)$.

## `PR-73`: Prefer intrinsic invariants of $\mathcal C$ — $M\in\mathbf{Mod}_R$ as $R$-module, not $M\otimes_RF\in\mathbf{Vect}_F$ — and flag once-removed definitions that need research

When possible an invariant of $M\in\mathcal C$ should be defined
*intrinsically* as a functor $\mathcal C\to\mathbf{Set}$ / $\mathbf{Card}$
/ $\mathbf{Ab}$ out of $\mathcal C$ itself, not as an invariant of
$\mathcal D$ transported via a functor $F\colon\mathcal C\to\mathcal D$.
Defining it once-removed — $\operatorname{inv}_{\mathcal C}(M):=
\operatorname{inv}_{\mathcal D}(F(M))$ for $F\colon\mathcal C\to\mathcal D$
— is sometimes necessary in a pinch (e.g. while $\mathcal C$'s intrinsic
theory is not yet available), but it is not elegant, it hides the
$R$-structure, and it makes the special case look primary and the
general case derived, when it should be the reverse.

The type case is rank. One *can* define, for $R$ a domain with
$F:=\operatorname{Frac}(R)$,
$\operatorname{rk}_R(M):=\dim_F(M\otimes_RF)$ for $M\in\mathbf{Mod}_R$.
This is technically correct when $M\otimes_RF$ is finite-dimensional and
recovers a "well known" notion from the classical $\dim_F$, but it is
stylistically poor: it defines an invariant of $R$-modules by bootstrapping
an invariant of $F$-vector spaces. What is wanted is the reverse — define
$\operatorname{rk}$ (resp. $\dim$) once, intrinsically for $R$-modules
(resp. $F$-vector spaces as the special case $R=F$ a field), e.g. via
localizations $M_{\mathfrak p}$, via $\operatorname{rk}_R(M):=
\sup\{n\mid R^n\hookrightarrow M\}$ / $\inf\{n\mid M\twoheadrightarrow R^n\}$
with IBN, or via $M\cong R^n$ when $M$ is finite free — and *recover*
"$\dim_FV$ is $\operatorname{rk}_F(V)$" as the well-known specialization,
not the other way around.

The same holds for signatures. One *can* define, while the intrinsic
$R$-theory is missing, $\operatorname{sig}(L):=\operatorname{sig}(L\otimes_RF,
b_F)$ for $F=\operatorname{Frac}(R)$ ordered ( PR-72), but the preferred
form is intrinsic to $R$ — via places/completions $R\to\widehat R_{\mathfrak p}$,
$R\to R_\sigma$, real places $\sigma\colon R\to\mathbb R$, and the family
$(p_\sigma,q_\sigma,r_\sigma)$ as invariants of $(L,b)$ in
$\mathbf{Lat}_R$ itself, with $L\otimes_RF$ as the intermediate step that
is *not* ideal in a pinch. The once-removed definition is admissible
temporarily, but it must be flagged.

This requires honest judgement, taste, and usually interactive research,
and should be flagged *outside* the document when found: it is the
difference between a definition that will age well and one that will have
to be rewritten when the intrinsic $R$-theory is supplied.

**Standard:** on first encountering an invariant that is naturally
$F:=\operatorname{Frac}(R)$ or $F$ a field, ask: can this be defined
intrinsically for $M\in\mathbf{Mod}_R$ / $(M,b)\in\mathbf{Bil}_{R,W}$ as
a functor of $R$ (resp. of $(R,W)$) itself — e.g. $\operatorname{rk}_R$,
$\operatorname{Val}_R(b)\subseteq W$, $(p_\sigma,q_\sigma,r_\sigma)$
via $R\to\mathbb R$ at $\sigma$ — with $\dim_F$ / $\operatorname{sig}_F$
as the specialization to $R=F$ a field? If yes, define it intrinsically
and note $\dim_F:=\operatorname{rk}_F$, $\operatorname{sig}_F$ as the
field fiber. If the intrinsic form is not yet available and the
once-removed $M\mapsto\operatorname{inv}_F(M\otimes_RF)$ is used in a
pinch, flag it outside the document (GitHub issue `needs-research` with the
label "intrinsic invariant needed") and do not present the $F$-transport
as the definition.

**Banned:** "$\operatorname{rk}_R(M):=\dim_F(M\otimes_RF)$" as the
*definition* of rank for $M\in\mathbf{Mod}_R$; "$\operatorname{sig}(L):=
\operatorname{sig}(L\otimes_RF)$" as the *definition* of signature for
$L\in\mathbf{Lat}_R$ without flagging that the intrinsic $R$-invariant
(via $R\to\widehat R_{\mathfrak p}$, $R\to\mathbb R$ at $\sigma$) is owed.

**Preferred:** define $\operatorname{rk}_R$ / $\operatorname{sig}_R$
intrinsically for $R$-modules / $R$-lattices (with $W$ varying), then
note "$\dim_FV=\operatorname{rk}_F(V)$ for $F$ a field" and
"$\operatorname{sig}(L\otimes_RF)$ is the $F$-fiber of
$\operatorname{sig}_R(L)$" as specializations.
