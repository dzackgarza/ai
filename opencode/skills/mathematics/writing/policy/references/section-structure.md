# Section structure (`SEC-*`)

A $\S$ is its fenced logical units. The document's logical units are
numbered blocks — Definition, Theorem, Lemma, Proposition, Corollary,
Example, Remark — each with a label and a title, linked through the
house's reference syntax (`XREF-1`). Running prose that points at a definition
elsewhere, cites a theorem elsewhere, or paraphrases either in English is
glue between units. It is not a logical unit that belongs to the document.

## `SEC-1`: A section with no fenced logical unit has no content

A $\S$ that contains only prose paragraphs — "Preservation, reflection,
and creation of limits are defined in @def-...," "A monadic functor
creates any limits [@Rie16]," "Hence a limit in $R\text{-}\mathbf{Mod}$
is computed on underlying sets," "The kernel … is a limit — the equalizer
… — so it is the set-theoretic kernel …," "Creation is a statement about
limit cones: a subgroup … need not be a submodule …" — has no Definition,
no Theorem, no Example, and no Remark that belongs to this $\S$. The
title "Creation of limits" is then a heading over filler. Every $\S$
introduces at least one primary fenced unit of its own — a definition,
theorem, example, counterexample, or worked calculation — and uses
remarks and references to support it. A $\S$ that only cites and
paraphrases is not a $\S$: it is navigation or process prose disguised
as exposition.

On an ordinary concept page, a bare run of included or linked units is
the same defect. Connect the definitions and theorems by their
hypotheses, consequences, proof strategy, or technique. Intentional
review sheets, theorem and definition compendia, resource indexes, and
problem banks are lists by design and are not this defect.

**Banned:** "## Creation of limits {#sec-creation}" followed by five
paragraphs, none fenced, that cite @def-preserve-reflect-create,
[@Rie16, Theorem 5.6.5], [@Rie16, Corollary 5.5.3], then "Hence …" and
"The kernel … so it is …" in prose.

**Banned:** a $\S$ that contains only "This is useful for the next
chapter" and a list of links.

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
section (@sec-statements-vs-constructions) or in the writing guide
(here `PR-15`, `PR-16`), not as closing morals of $\S$ Creation and $\S$ Parallel
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

The underlying skeleton of a paper or book is the set of numbered
statement blocks — Definition, Theorem, Lemma, Proposition, Corollary,
and Example — each with its label, title, hypotheses, quantifiers,
types, and conclusion. Their dependency graph is the work: every term
used in a theorem is defined in a prior definition, every result used in
a proof or solution is stated before it, linked, or cited, and every
example instantiates a definition. Under the house's proof obligation,
each claim is proved earlier or cited. The skeleton must be
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
not define every term, do not state every claim, or do not prove or cite
every theorem as the proof obligation requires.

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
in the requirements $\S$ or in the writing guide.

A Remark is reader-facing copy. It may explain a reference to a result in
a source, note which part of a source a problem uses, or record an
erratum: a false statement and its corrected hypotheses. It never
discusses provenance bookkeeping, internal status, what is or is not
included, collection membership, missing sources, or any other curation
concern (`PROSE-11`).

A remark, or a sentence inside a block, that describes the shape of
the mathematics instead of stating mathematics — which object a
condition is a condition on, that two properties are additional, that
constructions proceed from an object, that notions are recalled —
states nothing the reader can use or check. The test is that of
`SEC-6`: delete the sentence; if no definition, claim, or example is
lost, the sentence was commentary (`PROSE-17`, `PR-36`).

Observed in `dzackgarza/research`:
`research/lattice-theory/Lattices-and-Discriminant-Forms.md` at
`57c8eb1cb0`, example "Determinant order does not imply
2-elementarity", and at `ab530c1dcc`, the untitled remark at the head
of the file; `research/lattice-theory/lattice-theory.md` (working tree
over `57c8eb1cb0`), convention "Integral lattice specialization", and
at `ab530c1dcc`, the remark under "Basic Theory".

**Banned:** "Membership is a condition on the group $A_S$, while its
order is only the scalar invariant $\abs{\disc{S}}=p^a$."; "Positive
definiteness and unimodularity are additional properties."; "and
scalar extensions are formed from this integral object."; "We recall
the basic lattice-theoretic notions and arithmetic invariants used
throughout this section."

**Preferred:** the sentences deleted; the example closes with its
computation, the convention with its definition, and the section opens
with its first block.

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

**Preferred:** a Proposition with an actual claim: "For a finitely
generated $\mathbb Z$-module $L$, the natural map
$L\otimes_{\mathbb Z}\mathbb Z_p\to\varprojlim_n L/p^nL$ is an
isomorphism."

## `SEC-9`: A chapter is placed by its dependencies and its subject

The order of chapters is the work's reading order. A chapter's position
claims that everything it uses is defined above it, and that the part it
sits in names its subject. Place a chapter by reading it: what it defines,
what it uses, and which of the two the rest of the part does. Appending to
the end of a part, or putting it next to a file with a similar name,
decides neither question. File order is unrelated to dependency order.

Check three things:

- **Dependency.** Find where each result the chapter references is
  stated. A few forward references are normal; a chapter whose targets
  are mostly later is in the wrong place.
- **Subject.** State in one clause what the part is about, and check that
  the chapter is about that. General machinery and a project's own results
  are different subjects and go in different parts, however closely they
  are related.
- **Size.** A part of a dozen chapters is no longer a group. Split it at
  the seam the mathematics already has.

**Banned:** three chapters on one lattice sorted by file name, which put
them in the reverse of the order their own references require, inside the
run of general lattice theory whose results they use.

**Preferred:** the general lattice theory first, then the three chapters
in the order of their references, in the part about that lattice.

## `SEC-10`: Title a unit with its subject, never with its format

A title names the mathematics the unit is about. A title that names the
form of the text ("Summary", "Notes", "Overview", "Details") tells the
reader nothing and hides the subject from the table of contents.

**Banned:** "Lattice Summary" as the title of a chapter about Baily--Borel
embeddings.

**Preferred:** "Baily--Borel embeddings".

## `SEC-11`: Each fenced environment carries its typed content

A fenced block's class is semantic, not typographic. A `definition` block
contains a definition (DEF-4); an `example` block contains an example; a
`remark` contains a mathematical remark — a warning, an alternative
viewpoint, a real subtlety — never transitional prose (SEC-7). A class of
objects that recurs is collected where its type lives: examples in the
examples section, classification results in the classification subtree. A
block that carries content of the wrong type, and a section that scatters
one class across the document, both hide the unit from the skeleton
(SEC-6).

**Banned:** a `::: {.Remark}` whose body is "We next collect the
classification theorems"; an example stated as a closing sentence of a
section instead of as an `{#exm-...}` block amongst the section's other
examples (SEC-2); classification theorems for overlattices spread across
three chapters instead of one subtree.

**Preferred:** the remark contains the actual remark; each example is a
fenced `{#exm-...}` unit collected in the examples section of its chapter;
the classification theorems form one subtree whose $\S$ order is the
dependency order.

The block type is the logical status of its content. A definition
introduces a term and imposes no proof obligation; a proposition,
lemma, theorem, or corollary asserts a claim, carries a proof
obligation, and is citable by its label; an example instantiates; a
remark is unproved commentary the skeleton does not depend on. Content
in the wrong block changes what the reader must verify and may cite: a
claim inside a definition is asserted with no proof and no label, a
definition inside an example or in unfenced prose cannot be cited, a
result inside a remark is cited as if proved, and a sentence of
commentary inside a definition is read as part of the definiens. The
test is the proof obligation: a sentence with one is a proposition, or
an example with its computation; a sentence with none that defines a
term is a definition; a sentence with none that defines nothing is a
remark, or is deleted (`SEC-7`, `DEF-44`, `EX-2`).

Observed in `dzackgarza/research`:
`research/lattice-theory/discriminant-forms-and-genus.md` (working
tree over `57c8eb1cb0`), the definition of the spinor genus;
`research/dissertation/sections/1-part-combinatorial/2-chapter-lattice-theory/100-foundations.md`
at `ab530c1dcc`, definition "Scaled Lattices";
`research/category-theory/framework/Categorical-Foundations.md` at
`ab530c1dcc`, definition "Schemes as locally ringed spaces";
`research/category-theory/framework/Bilinear-and-Quadratic-Forms.md`
(working tree over `57c8eb1cb0`), definition "Rank one forms, the
hyperbolic plane, and split forms";
`research/dissertation/sections/1-part-combinatorial/2-chapter-lattice-theory/200-examples.md`
at `ab530c1dcc`, the unfenced prose under "The Hyperbolic Plane $U$".

**Banned:** inside a definition, "This condition is independent of
the choice of $\alpha$ because $\Orth(\widehat L)$ is the stabilizer
of $\widehat L$."; inside a definition, "If $L$ is unimodular and
$m>1$, $L(m)$ is not unimodular."; inside a definition, "The smooth
manifold definition of @def:smooth-manifold transfers to algebraic
geometry by substituting the ambient category and local models.";
inside one definition, "A perfect symmetric form $b$ on $M$ is *split*
if $M$ has a direct summand $N$ with $N=N^{\perp_b}$ [@MH73, I §6.1].
Over a ring whose finitely generated projective modules are free and
in which $2$ is a unit, a split form is an orthogonal sum of
hyperbolic planes [@MH73, I §6.3]"; as unfenced prose in an examples
section, "A vector $v \in U$ is called **isotropic** if $v^2 = 0$."

**Preferred:** the independence of $\alpha$ as a remark after the
definition, or as the lemma it is; "$L(m)$ is unimodular exactly when
$m$ is a unit" as a proposition after the definition of $L(m)$; the
transfer sentence as a remark; the definition of "split" alone, and
the classification over such rings as a theorem with its citation;
"isotropic" defined at its owner and the example citing it.

## `SEC-12`: A construction is introduced at its natural owner

Every concept has one owner: the section at its level of generality in the
abstraction lattice, where it first exists naturally. Introduce a
construction there, not at the place where it happens to be first needed.
Exposition order follows the dependency lattice, and $L[n]=q^{-1}(n)$,
twists, and classification results each live at their mathematical owner —
a general pairing or bilinear-module construction is not deferred to the
lattice chapter because the lattice chapter was written first.

**Banned:** defining $W$-valued $R$-bilinear modules inside the lattice
chapter because that is where the discriminant form is needed; defining
$L[n]$ only inside the MM-theory section, after it has already been used;
a classification theorem stated far from the classification subtree.

**Preferred:** locate each definition and theorem at the least specialized
section where it is defined, and let the specialized sections cite it
(`DEF-1`, `XREF-5`). Sections form a chain in the abstraction lattice:
pairings, then $W$-valued bilinear modules, then $W$-valued lattices,
then torsion forms, then definite, indefinite, and hyperbolic lattices,
then embedding theory.

Invariants and coinvariants of a group action are owned by the section
on isotypic decomposition — $L^G=\Hom_{\bZ[G]}(\bZ,L)$ and $L_G$ as
the fixed and the complementary parts of a $\bZ[G]$-module — and the
lattice section recalls them; a definition that builds $L^G$ as "the
common equalizer in $\bZ\text{-}\mathbf{Mod}$" inside the lattice
chapter constructs a module-theoretic object at the wrong owner, under
a local name (`TERM-16`, `DEF-45`).

Observed in `dzackgarza/research`,
`research/lattice-theory/invariant-and-coinvariant-lattices.md`
(working tree over `9be9b833a6`), definition "Invariant and
coinvariant lattices".

**Banned:** "Define $\iota^G\colon L^G\injects L$ to be the common
equalizer in $\bZ\text{-}\mathbf{Mod}$ of".

**Preferred:** "Recall (@def-invariants) that
$L^G=\Hom_{\bZ[G]}(\bZ,L)$ is the module of invariants of the
$\bZ[G]$-module $L$. The **invariant lattice** of
$\rho\colon G\to\Orth(L)$ is $L^G$ with the restricted form."

## `SEC-13`: Complexity is monotone through the exposition

A reader meets each notion after its prerequisites and before the
machinery that depends on it. An elementary construction is not
introduced for the first time inside a substantially more sophisticated
argument; an advanced section does not stop to define basic notation.
Complexity and abstraction increase through the document.

**Banned:** "twists of a lattice" first defined inside the
automorphism-lifting argument that uses them; the notation $L[n]$
explained for the first time three sections after its first use.

**Preferred:** the elementary construction in its own earlier section,
cited where used (`SEC-9`, `SEC-12`).

## `SEC-14`: One coherent mathematical subject per chapter

A chapter accumulates one subject; it is not a catch-all for whatever
was nearby when it was written. Theory is split by natural mathematical
ownership — general pairings, bilinear modules, lattices, torsion
forms, definite theory, indefinite unimodular theory, hyperbolic
theory, embedding theory, classification, examples — and a chapter
that discusses many unrelated things has no subject and therefore no
place (`SEC-9`, `SEC-12`). A catch-all chapter hides its units from
the skeleton's dependency graph (`SEC-6`): its content is cited by
nothing, because nothing can name what it is about. Test a chapter by
stating its subject in one clause; if the clause needs "and", the
chapter is two chapters.

**Banned:** a chapter "special lattices and transformations" that
treats hyperbolic lattices, an automorphism-lifting theorem, and a
list of concrete examples, with no single owner for the dependency
graph; a "miscellaneous lattice theory" chapter used as the default
destination for new results; a chapter "Isometries and arithmetic
invariants" whose sections run from the discriminant representation
through reflections, matrix realizations, and the index of a subgroup
to the Miranda–Morrison exact sequence and the definition of the genus
(`dzackgarza/research`,
`research/lattice-theory/Isometries-and-Arithmetic-Invariants.md`,
working tree over `2b758e124b`) — Miranda–Morrison theory and the genus
are subjects with their own chapters, not facts about isometries.

**Preferred:** split at the seams the mathematics already has — each
chapter's subject is one node of the abstraction lattice
(`SEC-12`), titled by that subject (`SEC-10`), placed by its
dependencies (`SEC-9`).

## `SEC-15`: Classification and examples live in dedicated places

Classification theorems — statements of the form "the isometry classes
of $X$ are exactly the following list" — are collected in the
classification subtree, and concrete lattices, computations, and
examples in the examples sections of their chapters (`SEC-11`). A
classification theorem that interrupts foundational theory, or an
example that interrupts a theorem's development, breaks both
(`SEC-13`): the classification subtree is where a reader looks for the
complete statement, and the examples section is where a reader verifies
a definition against data. A non-exhaustive list must not masquerade
as a classification theorem — "for example, the following lattices
are…" is an example, not a theorem (`EX-3`).

**Banned:** a complete classification theorem for even unimodular
lattices stated as a mid-chapter aside inside the embedding chapter; a
section titled "Classification" whose content is a list of concrete
lattices with no theorem; "Theorem: the following list classifies …"
where the list is stated to be non-exhaustive.

**Preferred:** the classification theorems in the classification
subtree, one per fence, with completeness stated in the hypotheses;
concrete lattices in fenced `{#exm-...}` blocks in the examples
section (`SEC-2`, `SEC-11`); an explicitly partial list presented as
an Example block, never as a Theorem.

## `SEC-16`: A statement block contains the claim, not its proof construction

A theorem or proposition block states its hypotheses and its
conclusion, tersely. The construction that verifies the claim — a
retraction, a section, an explicit representative calculation, a
witness-building algorithm — belongs to the proof, unless the witness
itself is part of the theorem's asserted data: "there exists a
retraction $r$ with $r\circ\iota=\operatorname{id}$" asserts a named
map, and naming $r$ in the statement is then the content
(`STR-3`); "…and the retraction is given by the following
computation" is a proof folded into the claim. A block whose body
carries the construction as well fails the type test `SEC-11` applies:
the reader who cites the proposition by number cites the whole
paragraph, not a proposition; the skeleton's unit is the claim, and
the verification lives in the proof block or a cited construction
(`PR-9`, `PROSE-10`). `EX-2` draws the adjacent line: if there is
nothing to prove, the passage is an example or a definition, not a
proposition with proof-shaped prose inside it.

**Banned:** a `::: {.proposition}` whose body runs "…and the
retraction sends each summand to its representative, computed as
follows: …" followed by witness arithmetic inside the statement
block; a theorem whose final sentence is the algorithm that
constructs the asserted object.

**Preferred:** the proposition states hypotheses and conclusion —
"every exact overlattice $L$ of $M$ with $L^{\perp_b}=0$ arises as
$\pi^{-1}(\Gamma)$ for an isotropic $\Gamma\subseteq D_L$
(`STR-5`)" — and the `.proof` block exhibits the section, the
representative calculation, and the algorithm; a construction that is
itself asserted data is named in the statement and built in the proof
(`STR-3`, `PROSE-10`).

## `SEC-17`: Reader-facing mathematics contains no audit metadata

Contributor workflow, dependency audits, corpus references, review state,
and completion state live in repository metadata or tooling. They are not
authored mathematical content. A fenced block such as `meta`,
`corpus-references`, `depends-on`, or `audited` exposes internal work state
to the reader and interrupts the mathematical dependency order.

**Banned:** a reader-facing fenced block that records source audit status,
contributors, dependencies, review completion, or corpus provenance.

**Preferred:** keep machine-readable workflow and audit data in the
repository's metadata surface; express a mathematical dependency in the
text through the stable reference that the argument uses (`XREF-1`).

## `SEC-18`: State the claim before its auxiliary machinery

A theorem, lemma, or proposition opens with its mathematical conclusion.
Place only the hypotheses and notation needed to parse that conclusion
before it. Auxiliary constructions, calculations, and proof notation are
subordinate to the claim and belong after it, usually in the proof
(`SEC-16`). Several paragraphs of setup before the assertion bury the
logical unit that the block exists to state.

**Banned:** a proposition that first builds an auxiliary module, chooses
representatives, and defines three maps before it states what those data
prove.

**Preferred:** state the conclusion with its necessary quantified data;
then define the auxiliary objects in the proof or in a cited construction.

## `SEC-19`: Classical background at the declared audience level is cited and used, not re-exposed

A document declares its reader by its subject: a research monograph on
lattices addresses a reader who knows the representability of a
functor, the Yoneda lemma, the underlying set of an object of a
concrete category, and the definition of a Grothendieck topology. A
notion at or below that level is used with a citation at its first
occurrence ([@Mac98, §III.2]) and is defined in the document only when
the document's usage is nonstandard, bespoke, or a choice among
conventions the reader cannot infer (`DEF-26`, `NOT-4`). Re-exposing
the classical notion has three costs: the reader is addressed as a
student (`PR-32`); the skeleton fills with blocks that no later block
cites (`SEC-6`); and material reproduced from memory is wrong where a
citation would have been right — a table assigning a class of
geometric objects to each Grothendieck topology is a claim about
several theories at once, each with its own literature. The boundary
with `CITE-7`: an object constructed by a particular source is
transcribed into the document's notation, because the document's
theorems are about it; a classical notion is cited, because the
document's theorems only use it. The boundary with `DEF-45`: a general
notion the document owns is recalled, not redefined, at its special
cases.

Observed in `dzackgarza/research`,
`research/category-theory/framework/Categorical-Foundations.md` at
`ab530c1dcc`, definitions "Representable presheaves", "Concrete
categories", and "Generalization by Grothendieck topology", and
theorem "The Yoneda lemma".

**Banned:** "The presheaf $F$ is *representable* if there is an object
$X$ and a natural isomorphism $F\cong\Hom_C(-,X)$. Under this
isomorphism, $\id_X$ corresponds to the universal element. The dual
convention applies to corepresentable covariant functors." as a
definition block in a monograph on lattices; "The set $U(X)$ is the
underlying set of $X$."; a theorem block stating the Yoneda lemma with
its proof; a table headed "| Admissible morphisms $\mca$ | Topology |
Geometric objects |" assigning a class of geometric objects to each
topology.

**Preferred:** "a representable presheaf [@Mac98, §III.2]" at the first
use, with the universal element named where the argument uses it; the
Yoneda lemma cited at the step that applies it; the Grothendieck
topology the document uses named with its covering families and a
citation, and no survey of the others.
