---
name: mathematical-writing-policy
description: Use when writing, editing, or reviewing reader-facing mathematical prose in any repository (exposition, definitions, theorems, examples, remarks, resource annotations, docs books, wikis, papers), or when a contribution, commit, or review cites a writing-policy code such as PR-30, DEF-26, SYM-1, or STANCE-05.
---

# Mathematical writing policy

This is the one catalogue of mathematical writing rules for every repository
that points here. Each rule has a stable code, a banned example, and the
preferred replacement. Cite the codes in contributions, commit messages, and
review.

## The single principle

Mathematical writing is the economical, logically organized presentation
of objects, constructions, relationships, and proofs in the native
language and established conventions of the subject. It is not
explanatory prose made rigorous by adding notation, categorical
vocabulary, construction detail, or citations, and it is not notation
made readable by adding prose. Notation, diagrams, sequences, and
displayed formulas are the primary language. Prose carries only what the
notation does not already state: hypotheses, the claim, the reason a step
holds, and the consequence drawn.

One test decides every sentence, in both directions: **does the sentence
state information the reader cannot recover from the notation already on
the page?**

- If the notation is absent, the sentence is a paraphrase and owes the
  object. "$A$ sits inside $B$" owes the mono; "the two constructions
  agree" owes the comparison morphism or the commuting diagram; "$M$
  admits an embedding" owes the point of the embedding object; "the
  mixed terms vanish" owes the zeroed map (`STR-5`, `STR-6`, `DIA-7`,
  `MA-17`, `PR-74`).
- If the notation is present, the sentence is bookkeeping and is deleted.
  An arrow written $\iota\colon S\injects M$ is a monomorphism; writing
  "the image subobject" or "the underlying monomorphism" beside it adds
  no information (`PR-76`). A display enlarges nothing: it exposes
  structure the sentence cannot hold (`PR-75`).

The same test fixes the level at which the mathematics is stated. The
level is the one at which the claim is a theorem of the subject: the
category in which the construction has its universal property
(`FORM-11`, `FORM-12`), and the hypotheses the claim needs rather than
the hypotheses a proof found convenient (`STR-8`). At that level the
mathematics has a definite shape:

- Constructions arise from universal properties, functors, and coherent
  diagrams, not from elementwise descriptions (`EV-5`, `EV-8`, `DIA-7`).
- The general construction comes first, and its variants are recovered
  by established categorical operations: fibers, pullbacks, factorization
  through a monomorphism (`DEF-42`, `TERM-18`, `SEC-12`).
- Kernels, cokernels, exact sequences, and obstructions are stated
  through the relationships they stand in, never as isolated symbols
  (`EV-9`, `PR-75`, `CITE-7`).
- The conventional textbook formulation is the floor, not the ceiling.
  A notion the document has placed in a more structured setting is
  stated there, and the elementary formulation is the proposition
  recovered from it (`DEF-41`, `TERM-16`).
- Concision follows from structure: an established construction carries
  its meaning, so prose that re-explains it is deleted (`PR-76`), and
  standard terminology and notation record that the writer recognizes
  the established theory (`NOT-4`, `NOT-5`).

Categorical vocabulary is not categorical reasoning: naming a forgetful
functor, calling a map a morphism, or writing "underlying" does not
place the argument in the category; computing the kernel, cokernel, or
splitting there does (`MA-18`).
The style presupposes a writer who knows the theory at the generality
where its constructions are native. A rewrite of sentences toward its
surface — the vocabulary without the construction, its category, and its
standard source — reproduces the appearance and not the mathematics.

Six judgments apply the test. Each is answered by a cited rule, never by
the writer's recollection of what rigorous writing looks like.

| Judgment | Rule |
| --- | --- |
| Which formulation states the mathematics | `TERM-16`, `DEF-39`, `DEF-41`, `DEF-42`, `DEF-43`, `PR-15` |
| Which hypotheses are intrinsic and which are proof artifacts | `STR-3`, `STR-8`, `CITE-6` |
| Which notation is standard, which is necessary, which is redundant | `NOT-4`, `NOT-5`, `NOT-6`, `NOT-10`, `SYM-14`, `SYM-16` |
| Which relation earns a diagram or sequence, which an equation | `DIA-7`, `DEF-40`, `PR-75`, `PR-77` |
| Which construction is foundational, which an immediate consequence | `DEF-16`, `DEF-22`, `SEC-16`, `SEC-18`, `STR-6` |
| Which fact is obvious, which needs a proof or a citation | `PR-9`, `EV-1`, `CITE-1`, `CITE-7`, `SEC-6` |

## Gradients

Each axis below runs from an underspecified formulation through an
overshoot to the target. The overshoot is a defect of the same rank as
the underspecification: a revision that lands there has moved along the
axis without reaching the mathematics. The rules column names the tests
that decide the position.

| Axis | Underspecified | Overshoot | Target | Rules |
| --- | --- | --- | --- | --- |
| Maps | "the map factors through the kernel" | the lift, its triangle, and a sentence restating each, at every occurrence | the lift and its triangle where the argument uses them; the kernel's notation thereafter | `EV-11`, `EV-8`, `DIA-7`, `PR-76` |
| Ambient category | a morphism by its "underlying function"; a Hom-object as a set | arrows and "forgetful" around an argument that runs on elements | the construction in the category where it has its universal property; Hom-objects with their structure | `FORM-11`, `FORM-12`, `MA-18` |
| Precision | "the image subobject determined by $f$" | "injective monomorphism"; a paragraph of category terminology | $\operatorname{im}(f)$; the signature with its defining equation | `PR-76`, `PR-77`, `NOT-10` |
| Set theory | "the underlying set of the cokernel consists of classes" | categorical vocabulary as a reformulation after the fact | the adjoint and its kernel; the structure organizes the argument | `MA-18`, `DEF-39`, `STR-1` |
| Diagrams | prose for a pullback | a display for every declaration; one construction over several displays | the square when the relation is diagrammatic; one display per construction | `DIA-7`, `PR-75`, `PR-77` |
| Constructions | variants by near-identical formulas | named variants with no relation between them | one general construction; variants as fibers and pullbacks; the standard construction at its owner | `DEF-42`, `SEC-12`, `DEF-41` |
| Definitions | a formula-dependent definition; consequences inside the block | a characterization through machinery the notion is not an instance of | the definition in the framework where the notion is an instance; consequences as propositions | `DEF-41`, `DEF-16`, `DEF-22` |
| Theorems | a recipe as the statement | notation setup as the statement | the assertion; the construction in the proof | `SEC-16`, `SEC-18` |
| Hypotheses | an unjustified restriction | the hypotheses one proof used | the claim's hypotheses, in the block | `STR-8`, `STR-3`, `CITE-6` |
| Notation | $Q_f$, $b(\lambda)$ beside $M(\lambda)$, "the primitivity proposition" | a name for every map | standard, minimal, stable | `NOT-4`, `NOT-5`, `NOT-6`, `NOT-10`, `XREF-7` |
| Sameness | "the same", "agree canonically" | "canonical" asserted after a choice | the specified isomorphism; naturality; independence of the choice | `EV-11`, `MA-1` |
| Classification | elementary conditions | a local classification with no global object | the global structural formulation, with the local description as its consequence | `DEF-41`, `TERM-16` |
| Provenance | an unsupported claim | a citation in place of the statement or construction | the complete statement with its provenance | `CITE-1`, `CITE-6`, `CITE-7`, `EV-9` |
| Density | pedagogical overexplanation | technical density with no reader | economy calibrated to the reader | `PR-18`, `PR-9`, `PR-76` |
| Register | "objects satisfying $P$ form a subcategory" | formal register with no formal content | "the $P$-objects form a full subcategory", when that is the claim | `PR-15`, `TERM-16` |
| Generality | the lattice defined before the pairing; nondegeneracy inside the definition of a lattice; unimodularity before $I$-modularity; the signature as a pair of integers | general hypotheses over the special case's proof: "for a ring $R$" where the argument uses $\mathbb Z$ | general pairings, then bilinear modules, then lattices; nondegenerate lattices as a full subcategory; $I$-modular with $I=R$ the unimodular case; the signature indexed by the real places; an invariant defined on the structured object and restricted | `TERM-18`, `DEF-42`, `SEC-12`, `SEC-9`, `STR-8` |
| Families | a form defined pointwise; the quadratic module by inline relations; one $f^*$ as "functoriality" | a representing object named and never used; the fibers still defined one by one | $\mathbf{Bil}_{R,W}(M)=\operatorname{Hom}(T_R(M)_2,W)$ and $\mathbf{Quad}_{R,W}(M)=\operatorname{Hom}(\Gamma^2_R(M),W)$; the category over all $W$ with the fixed-value categories as its fibers; pullback as the contravariant functor; $\Gamma^2_R(M)$ at its owner | `PR-41`, `PR-55`, `DEF-42`, `SEC-12`, `TERM-10` |
| Categories | "the category of lattices" with no morphisms; a functor as a "function"; $\perp$ as an operation | the names with the data absent: "monoidal" with no unit, "natural" with no square, "functor" with no action on morphisms | objects, morphisms, composition, identities; the functor with its action on morphisms at the defining occurrence; the monoidal tuple with its coherence; the naturality square | `MA-13`, `PR-14`, `PR-67`, `FORM-12`, `MA-18` |
| Obstructions | "$b^\sharp$ is injective"; "$\rho_L$ is surjective" | a sequence truncated to the fragment a computation needs; "exact" with an undefined term | the four-term sequence with its radical and coradical; the arithmetic sequence with $\operatorname{MM}(L)$ and $g(L)$; the extension class and its splitting | `DEF-39`, `EV-9`, `EV-11`, `CITE-7` |
| Counting | a representative per class; "the number of classes"; "class group" for a set | a groupoid named and then counted by hand; "groupoid cardinality" for a plain count | the groupoid as a construction; embeddings, comparison morphisms, and classes distinguished; $\Cl(L)=\pi_0\operatorname{Gen}(L)$, $\cl(L)$ its cardinality, the mass its groupoid cardinality | `DEF-43`, `DEF-40`, `NOT-4`, `TERM-7` |
| Ontology | the set-level statement with no derived object | "homotopy pullback" or "derived" with the projections and coherence absent | the derived or higher-categorical object with its projections and coherence; the classical statement as its truncation | `DEF-9`, `DEF-36`, `DEF-32`, `STR-4` |
| Coordinates | the form as a matrix; nondegeneracy by $\det\neq0$; perfectness by $\det\in R^\bullet$; $\mathbb Q/\mathbb Z$ for a codomain the construction determines | "intrinsic" asserted over an argument that computes in a basis | the form as a morphism; the Gram matrix after a basis is chosen; nondegeneracy and perfectness through the adjoint's sequence; the codomain the construction determines, with the monomorphism into the coarse object named | `DEF-39`, `PR-58`, `PR-61`, `SYM-16`, `EV-10` |
| Fluency | "finite free"; $b(\lambda)$; "anti-isometry"; a zero-argument macro | a local name recorded beside the standard one | "finitely generated free"; $M(\lambda)$; the isometry to $L(-1)$; $L[n]$; semantic macros with their operands | `TERM-16`, `TERM-17`, `NOT-4`, `NOT-6`, `NOT-7` |
| Architecture | a catch-all chapter; a fact filed where it was first needed | chapters named after theories whose bodies are lists of facts | general pairings, bilinear modules, lattices, discriminant forms, then the definite, indefinite, hyperbolic, embedding, and arithmetic theories; Eichler and Miranda–Morrison theory as developments of their own | `SEC-9`, `SEC-12`, `SEC-13`, `SEC-14`, `SEC-15` |
| Blocks | a Proposition as a container for a definition, a computation, and a remark | typed blocks with the wrong types: a Theorem for a computation, a Lemma for a definition's consequence | claim and hypotheses in the block, the construction in the proof; a definition's consequences as a proposition after it; a computation as an example; a failed implication as a counterexample; a characterization as a proposition, not the definition | `SEC-16`, `SEC-18`, `DEF-16`, `DEF-22`, `EX-2`, `PR-64` |
| Commentary | "contains additional information"; "is different from the previous one"; "the rank adds and the determinant multiplies"; "the classical theorem guarantees" | the commentary kept with a formula appended | the statement with its hypotheses and citation; the equations; the map that separates the two notions | `PR-51`, `PR-52`, `PR-74`, `EV-11`, `CITE-4` |

## Oscillation gate

A one-directional instruction, "write the structure," produces the
opposite defect: verbalized formalism, gratuitous displays, categorical
vocabulary in place of categorical reasoning. A revision that patches a
reported defect with its opposite does not converge. The gate is
mandatory and has no judgment clause.

**Trigger.** A review reports, at a location revised in response to an
earlier review, a defect in the opposite family from the earlier report:
precision asked and formalism reported, or the reverse; a symbol asked
and overdefined notation reported, or the reverse; a display asked and
unreadable displays reported, or the reverse.

**Consequence.** Stop editing the sentence. Write down three facts
before the rewrite: the object or claim in the notation of the subject's
standard source; what the reader must know at this point that the
notation does not state; the hypotheses the claim needs. Rewrite the
passage from those facts, then apply the test above to each sentence of
the rewrite.

A writer who cannot name the standard source's formulation has not
reached the rewrite step (`TERM-16`, `DEF-41`).

## Scope

The rules govern contributor-written mathematical copy: chapters, pages,
definition and theorem blocks, examples, remarks, solutions, resource
descriptions, headings, introductions, and public project descriptions. They
govern structure, exposition, rigour, precision, linking, and the relationship
that the copy sets up with its readers and with other authors.

They do not decide which definition, generality, or foundations a document
adopts. That mathematics comes from the sources the document draws on and from
its house conventions. A quoted source statement, such as an exam problem,
keeps the source's wording and notation.

## House conventions

Each repository's `CONTRIBUTING.md` fixes what depends on its medium and
audience:

- the syntax of numbered blocks and the list of block classes (`DEF-4`);
- the reference resolver, its label format, and the link syntax (`XREF-1`,
  `XREF-4`, `XREF-5`);
- the mark for a term at its defining occurrence (`DEF-26`);
- the audience, and so the level that `PR-18` protects;
- the default ontology. `DEF-8` to `DEF-14` apply where the house adopts the
  derived and homotopical ontology;
- the proof obligation: whether every claim in a statement block is proved,
  or whether a standard result may be stated with a citation and no proof
  (`SEC-6`, `EX-2`);
- whether one definition block may define an explicitly enumerated family of
  predicates on the same data (`DEF-15`);
- whether a pullback square is drawn where fiber-product notation is used, or
  is reached through the linked definition of the fiber product (`MA-8`);
- where open problems and deferred generalizations are recorded outside the
  document (`PR-72`);
- rules that exist only for that repository, under that repository's own
  codes.

A house convention adds a mechanism. It does not restate, weaken, or renumber
a rule here. Examples in the references use one house's syntax (`\ref`,
`::: {#def-…}`, `@def-…`); read them with the house's own mechanism.

## Families

Load the family file for the defect under review. Each file is a list of rules
in code order.

| Family | Codes | Governs | File |
| --- | --- | --- | --- |
| Authorial stance | `STANCE-*` | The relationship that copy sets up with readers, authors, and institutions. | [authorial-stance](references/authorial-stance.md) |
| Prose | `PROSE-*` | Sentences that spend attention on an imagined teaching situation instead of mathematics. | [prose](references/prose.md) |
| Resource descriptions | `RESOURCE-*`, `PROVENANCE-*` | Resource pages, bibliographic annotations, and source claims. | [resource-descriptions](references/resource-descriptions.md) |
| Precision | `PRECISION-*` | Prose that stands in for a definition, scope, object, or universal property. | [precision](references/precision.md) |
| Prose tells | `PR-*` | Sentence-level defects in mathematical writing. | [prose-tells](references/prose-tells.md) |
| Evasion | `EV-*` | Prose that stands in for mathematical work not done. | [evasion](references/evasion.md) |
| Mathematical tells | `MA-*` | Colloquial or reinvented parlance for a standard notion. | [mathematical-tells](references/mathematical-tells.md) |
| Terminology | `TERM-*` | Foreign, coined, colliding, or shifting terms. | [terminology](references/terminology.md) |
| Definitions | `DEF-*` | Defining occurrences, the form of a definition, and the default ontology. | [definitions](references/definitions.md) |
| Cross-references | `XREF-*` | Links to blocks, pages, and defining occurrences. | [cross-references](references/cross-references.md) |
| Citations | `CITE-*` | Bibliographic citation. | [citations](references/citations.md) |
| Diagrams | `DIA-*` | Authored commutative diagrams. | [diagrams](references/diagrams.md) |
| Formation conventions | `FORM-*` | Universes, pullbacks, repleteness, nerves, truncation, and induced functors. | [formation-conventions](references/formation-conventions.md) |
| Notation | `NOT-*` | Meaning and consistency of symbols. | [notation](references/notation.md) |
| Symbols and binding | `SYM-*` | Declaring symbols, maps, and data before use. | [symbols-and-binding](references/symbols-and-binding.md) |
| Properties and structure | `STR-*` | Chosen structures and stated hypotheses. | [properties-and-structure](references/properties-and-structure.md) |
| Examples | `EX-*` | The form and status of examples. | [examples](references/examples.md) |
| Axioms | `AX-*` | Stating axioms inside definitions. | [axioms](references/axioms.md) |
| Parentheticals | `PAR-*` | What a parenthetical may carry. | [parentheticals](references/parentheticals.md) |
| Section structure | `SEC-*` | Statement blocks as the skeleton of a section; the placement and titles of chapters. | [section-structure](references/section-structure.md) |

[Recurring patterns](references/recurring-patterns.md) groups the rules by the
failure that produced them.

## Applying the policy

- A tell is stylistic; the defect is usually missing mathematics. The fix for
  an `EV-*`, `PRECISION-*`, or `PR-30`-type finding is the definition, the
  named map, or the stated theorem, not a nicer phrase.
- Read the whole artifact for `STANCE-*`. The defect is a relationship that
  many small sentences set up, not one adjective.
- Before applying a writing correction, find the rule it instantiates and
  cite it. If no rule covers it, record the new rule here in the same change.
- Apply the sentence test in both directions. A finding of missing structure
  and a finding of verbalized formalism are one defect seen from two sides; a
  fix that trades one for the other triggers the oscillation gate.
- Never write a definition or a citation from memory. Read the source and
  transcribe from it (`DEF-2`, `CITE-1`).
- The [[policy-index/SKILL#policy-registry|Bridge-Burning Policies]] also
  apply to every artifact that this policy governs.

## Not flags

Standard mathematical hedging and signposting that carry real content are not
violations: "provided", "up to isomorphism", "without loss of generality", a
genuine sign or normalization convention, and a remark that explains a real
subtlety in context. The test is whether removing the phrase removes
information. A tagline removes none.

## Maintaining this policy

A change to this policy requires the same work it demands of other writing.

- Start from an observed defect. Quote the passage with its repository, file,
  revision, and heading. An invented caricature is easier to recognize than
  the plausible prose in which the defect occurred.
- Extract the general mechanism. One page supplies the evidence; the rule
  states the pattern at the level where it applies.
- Cover every correction since the last update, not only the last one.
- When reading a document for any purpose, look for new instances of the
  recorded patterns, and record each new pattern as a general rule with the
  example that shows it.
- For a stance defect, say who is judged, supervised, or spoken for, and which
  authority the writer assumes. Teach recognition and severity: show how
  repeated helpful-looking sentences set up sustained condescension or
  professional contempt. Address the temptation to reduce the defect to
  verbosity, a missing citation, or an isolated mistake.
- Make the preferred form show the actual correction. A softer command, a
  first-person suggestion, or "Suggested reading" can keep the same hierarchy.
  Replace a prescription with the knowledge it displaced and the reasons that
  support it.
- Ground every preferred form in a standard formulation, structure, or
  convention found by reading textbooks and papers. Read the standard source
  and transcribe from it. Do not invent the preferred form from memory.
- When a later correction shows that an earlier rule has the wrong model,
  rewrite or delete the earlier rule. An appended stronger rule that leaves
  the contradiction authoritative keeps the defect.
- A rule states the test that decides both directions. A rule that only
  pushes toward more formalism, or only toward less, reproduces the
  oscillation it was written to stop.
- Keep one source of truth. Integrate a new rule into its family under the
  next free code. Do not start an overlapping catalogue or a parallel policy
  document. Never reuse or renumber a code: repositories and commit histories
  cite them.
- Keep evidence apart from proposals. Observed quotations establish the
  finding. A preferred form must not invent coverage, history, or facts about
  a source.
- Do not quote a private message. Quote repository prose only.

The policy must make a difficult recognition reproducible for a later
contributor. Recording agreement, adding prohibitions, or adding policy text
does not show that it does.
