# Section structure (`SEC-*`)

A $\S$ is its fenced logical units. The document's logical units are fenced
blocks — Definition (`::: {#def-...}`), Theorem (`::: {.Theorem
#thm:...}`), Lemma, Proposition, Corollary, Example (`::: {#exm-...}`),
Remark (`::: {.Remark}`) — each with an ID and a title, citable via
`\ref`/`\longref` or `@`. Running prose that points at a definition
elsewhere, cites a theorem elsewhere, or paraphrases either in English is
not a logical unit that belongs to the document.

## `SEC-1`: A section with no fenced logical unit has no content

A $\S$ that contains only prose paragraphs — "Preservation, reflection,
and creation of limits are defined in @def-...," "A monadic functor
creates any limits [@Rie16]," "Hence a limit in $R\text{-}\mathbf{Mod}$
is computed on underlying sets," "The kernel … is a limit — the equalizer
… — so it is the set-theoretic kernel …," "Creation is a statement about
limit cones: a subgroup … need not be a submodule …" — has no Definition,
no Theorem, no Example, and no Remark that belongs to this $\S$. The
title "Creation of limits" is then a heading over filler. Every $\S$
introduces at least one fenced unit of its own; a $\S$ that only cites
and paraphrases is not a $\S$.

**Banned:** "## Creation of limits {#sec-creation}" followed by five
paragraphs, none fenced, that cite @def-preserve-reflect-create,
[@Rie16, Theorem 5.6.5], [@Rie16, Corollary 5.5.3], then "Hence …" and
"The kernel … so it is …" in prose.

**Preferred:** "::: {#def-create} ## Creation of limits — … :::" or
"::: {.Proposition #prp-limit-created} ### Limits in $R\text{-}\mathbf{Mod}$
— … :::" with proof that cites the monadicity theorem and explains how
it applies. The $\S$'s content is the fenced unit; the paragraphs are the
proof or the remarks that follow it, not the $\S$ itself.

## `SEC-2`: Example and remark inside a mathematical section must be fenced

"For example, the additive and multiplicative monoids of a ring define
distinct functors $\mathbf{Ring}\to\mathbf{Mon}$" is an example without
an `{#exm-...}` block. "If no comparison is specified, $F$ and $G$ remain
distinct" is a remark about parallel functors without a `{.Remark}`. An
example and a remark that belong to a $\S$ are fenced and typed, not
"For example, …" or "If … remain distinct" in running prose. An
extended remark that is fenced is fine to leave unlabeled as a Remark;
an unfenced paragraph is not a Remark.

**Banned:** "For example, the additive and multiplicative monoids …" as a
closing sentence of $\S$ Parallel functors.

**Preferred:** "::: {#exm-add-vs-mult} ## Additive versus multiplicative
— The functors $\mathbf{Ring}\to\mathbf{Mon}$ sending $R$ to
$(|R|,+,0)$ and to $(|R|,\cdot,1)$ are distinct; no natural isomorphism
is specified. :::"

## `SEC-3`: Writing requirement not inside a mathematical section

"A construction whose value happens to agree on underlying sets across
two categories names the functor along which it is created" and "If no
comparison is specified, $F$ and $G$ remain distinct" are writing
requirements about how to speak about constructions versus statements and
about when parallel functors are distinct. They belong in a requirements
section (@sec-statements-vs-constructions) or in CONTRIBUTING.md
(PR-15, PR-16), not as closing morals of $\S$ Creation and $\S$ Parallel
functors. A $\S$ that states a theorem about monadic functors does not
close with a style rule.

**Banned:** the last paragraph of each $\S$ in the quoted block as a
prose moral inside a mathematical $\S$.

**Preferred:** state the theorem, prove it, give the example and the
non-example (kernel versus subgroup — the latter as a fenced
non-example or Remark that a subgroup of the underlying abelian group
need not be a submodule), then close. Put the writing requirement in the
requirements $\S$ where it is defined and cite it.

## `SEC-4`: Arbitrary breaking of a work into sections

A work is broken into titled $\S$'s that do not reflect logical
dependency or coherent grouping of units, but partition prose arbitrarily
to create length or satisfy a template. Standard textbooks and papers
organize $\S$'s around dependency: foundations (what a functor,
natural transformation, and comparison are) before general notions
(preservation/reflection/creation), before theorems (monadic functors
create limits), before applications (limits in $R\text{-}\mathbf{Mod}$
computed on underlying sets). A titled $\S$ that exists to house a few
paragraphs of paraphrase is not a $\S$.

Concrete standard (amsthm): a $\S$ title names the mathematics its fenced
units develop, and its position in the chapter reflects what those units
define and what they use. Hartshorne, EGA, Lurie *Higher Topos Theory* and
*Higher Algebra*, Riehl *Category Theory in Context* each place
$2$-categorical foundations (parallel functors, natural isomorphisms)
before any use of monadicity; creation via monadicity is in the
monadicity chapter, not adjacent to the definition of a comparison.

**Banned:** the quoted block's consecutive siblings "Creation of limits
{#sec-creation}" and "Parallel functors {#sec-parallel-functors}" — the
first is a specific application of monadicity, the second is a
foundational $2$-categorical distinction that belongs in foundations, and
neither contains a primary fenced unit of its own.

**Preferred:** place "Parallel functors / comparisons / natural
isomorphisms" in categorical foundations before any use of preservation
or creation; place "Creation of limits via monadic functors" after the
monadicity theorem, with its corollary (limits in algebraic categories)
and its example (kernel) and non-example (subgroup need not be
submodule), in the chapter where limits in algebraic categories are
developed, at the point where the dependency is satisfied.

## `SEC-5`: A section that is entirely remarks

A $\S$ whose only content would be Remarks — or whose unfenced prose is
all remarks, morals, and writing requirements ("Creation is a statement
about limit cones: a subgroup … need not be a submodule …", "If no
comparison is specified, $F$ and $G$ remain distinct," "A construction
whose value happens to agree … names the functor …") — has no primary
mathematical content. In amsthm style a Remark is secondary to a
Definition, Theorem, Lemma, Proposition, Corollary, or Example; a $\S$ of
only Remarks has nothing to remark on. If there is a precise claim, state
it as the $\S$'s primary unit; if there is not, the $\S$ should not
exist.

**Banned:** a titled $\S$ whose paragraphs are all of the form "Creation
is a statement about …" / "A construction whose value happens to agree
…" / "If no comparison is specified …" — remarks without a primary
Definition/Theorem/Example that belongs to this $\S$.

**Preferred:** either state the primary claim as a fenced Proposition,
Example, or Remark attached to a primary unit ("The forgetful
$U\colon R\text{-}\mathbf{Mod}\to\mathbf{Sets}$ creates limits; the
underlying set of a kernel carries a unique $R$-module structure making
it the kernel" as Corollary with proof), or do not create the $\S$. A
genuine meta-remark about how to speak about created limits versus
underlying-set agreement belongs in the requirements $\S$ or in a
Remark attached to the corollary, not as a standalone $\S$.

## `SEC-6`: The skeleton is the fenced logical units

The underlying skeleton of a paper or book is the set of fenced logical
units — Definition (`::: {#def-...}`), Theorem (`::: {.Theorem
#thm:...}`), Lemma, Proposition, Corollary, and Example (`:::
{#exm-...}`) — each with its ID, title, hypotheses, quantifiers, and
types. Their dependency graph is the work: every term used in a theorem
is defined in a prior definition, every lemma used in a proof is proved
earlier, every example instantiates a definition. The skeleton must be
logically coherent and mathematically complete when every non-unit is
removed — connecting prose, motivation, transitions, and Remarks. If the
skeleton is not coherent on its own, the work is incomplete.

Concrete standard (amsthm): Hartshorne, EGA, Lurie *Higher Topos Theory*
and *Higher Algebra*, Riehl *Category Theory in Context* each present a
chapter as a sequence of fenced units with proofs; the prose between them
is glue. Deleting the glue and the Remarks leaves a citable, checkable
graph that still defines every term and proves every claim. A section
contributes to that graph only through its fenced units.

**Banned:** a manuscript where the fenced units alone — Definitions,
Theorems, and Examples with their IDs stripped of surrounding prose — do
not define every term, do not state every claim, or do not prove every
theorem.

**Preferred:** write the fenced units first as the skeleton; then add
prose and Remarks as glue. Test by deleting every non-unit: the remaining
fenced units with their proofs still form a complete, dependency-ordered
mathematical text.

## `SEC-7`: Remarks are for pedagogy, not for primary claims

A Remark (`::: {.Remark}`) is secondary to the skeleton: pedagogy,
intuition, a warning that a subgroup of the underlying abelian group need
not be a submodule, a note that two parallel functors are distinct unless
a comparison is specified, an alternative viewpoint. A Remark does not
introduce a new definition, a new theorem, or a new example that belongs
to the document. A $\S$ whose fenced content would be only Remarks, or whose
unfenced prose is all remarks and morals, has no primary claim and is out
of place in a standard text.

**Banned:** a titled $\S$ that would contain no Definition, Theorem,
Lemma, Proposition, Corollary, or Example even after fencing — only
"Creation is a statement about limit cones …" and "If no comparison is
specified, $F$ and $G$ remain distinct" as Remarks.

**Preferred:** attach the remark to its primary unit: the subgroup
non-example as a Remark following the Corollary that $U$ creates limits
(and the kernel Example), the parallel-functors distinction as a Remark
following the definition of a natural transformation. If there is no
primary unit to attach to, the $\S$ should not exist; the remark belongs
in the requirements $\S$ or in CONTRIBUTING.md.

## `SEC-8`: Specialization of a general construction with no new claim

A general construction is already defined — extension of scalars
$B\otimes_A^L-\colon\mathbf{LMod}_A\to\mathbf{LMod}_B$ left adjoint to
restriction along $A\to B$, base change of a bilinear form as
$B\otimes_A^L b$, etc. Stating its specialization at specific constants
with no new definition, theorem, or computation is filler: it restates
the definiens on objects ("sends $L$ to $L\otimes_{\mathbb Z}\mathbb
Z_p$") that is already the definition of the functor on objects, and
contributes no fenced unit to the skeleton (SEC-6).

Concrete standard: define $B\otimes_A^L-$ once as the left adjoint to
$\operatorname{Res}_\varphi$; then write $L\otimes_{\mathbb Z}\mathbb Z_p$
or $L\otimes_{\mathbb Z}^L\mathbb Z_p$ without a separate sentence
announcing that this is what the functor does for $\mathbb Z\to\mathbb
Z_p$.

**Banned:** "Extension of scalars along $\mathbb Z\to\mathbb Z_p$ sends a
$\mathbb Z$-module $L$ to $L\otimes_{\mathbb Z}\mathbb Z_p$" as a
standalone sentence.

**Preferred:** define $B\otimes_A^L-$ once; then use
$L\otimes_{\mathbb Z}\mathbb Z_p$ inline. If the specialization has a
claim, make it a fenced unit: "::: {#exm-extension-Zp} ## Extension to
$\mathbb Z_p$ — For $L\in\mathbf{LMod}_{\mathbb Z}$, $L\otimes_{\mathbb
Z}^L\mathbb Z_p$ is $p$-adic completion when $L$ is finitely generated;
$\operatorname{Tor}_1^{\mathbb Z}(L,\mathbb Z_p)=0$ iff … :::" — a
Proposition/Example with a precise claim, not a restatement of the
general definiens.
