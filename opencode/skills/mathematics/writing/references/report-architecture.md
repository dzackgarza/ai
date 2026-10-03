# Document Architecture for Mathematical Reports

Load when producing or revising a multi-section mathematical document for an expert
reader: a research report, research note, project specification, survey, or set of
graduate notes. This is the document-scale companion to `exposition-style.md` (which
governs a single problem-solution) and `structured-proofs.md` (which governs a single
proof). It governs how the whole document is organized.

## Contents

- [The master rule: theorem-driven, not status-driven](#the-master-rule)
- [Pick one genre and one audience first](#genre-and-audience)
- [Statement taxonomy](#statement-taxonomy)
- [Definitions must be closed](#closed-definitions)
- [Negative statements need positive content](#negative-statements)
- [Notation for structural compression](#notation)
- [Proof detail is proportional to risk](#proof-detail)
- [Motivation before construction](#motivation)
- [Computations tie to propositions and are reproducible](#computations)
- [Strategies are conditional implications](#strategies)
- [Citations at the level of dependence](#citations)
- [Obsolete mistakes leave the main line](#obsolete)
- [Reproducible bundle](#bundle)
- [Report skeleton](#skeleton)

* * *

## The master rule: theorem-driven, not status-driven {#the-master-rule}

Organize the document by **mathematical dependency**, never by the logical status of
claims or the history of previous mistakes.

The dominant failure mode is a document whose architecture is built from status
categories — "Required theorem," "Candidate construction," "Warning," "Computational
record," plus a warning catalogue, a dependency graph, a status ledger, and a
self-audit. Symptom to catch mechanically: **count the blocks.** If warning/problem/TODO
blocks outnumber theorem/lemma/proposition blocks, the document is a project ledger
wearing a paper's clothes. Rebuild it around this spine:

```
objects  →  principal conjecture/theorem  →  proved results
         →  exact reductions  →  computational and historical appendices
```

The main text carries the canonical theory and argument. Computations, obsolete
approaches, audit logs, version history, and internal error records go to appendices or
a separate research diary — not into the theorem statements, and not into the narrative.

**The reader test.** At any point in the document, the reader must be able to tell, of
the construction in front of them, which of four things it is: essential to the principal
theorem, an autonomous *alternative* to it, an *abandoned* attempt, or an *illustration*.
If the ordering makes that impossible to tell, the ordering is wrong — no amount of
later status labeling repairs it.

**Standards and models to imitate.**

- *Halmos* — the object is communication of one idea to a **specified reader**;
  everything below serves that, through deliberate organization and order.
- *Gillman's standard topics* — treat as a checklist for the document as a whole:
  general organization; prerequisites; notation and terminology; **state a result before
  proving it**; keep the reader continuously informed (signpost where the argument is and
  where it is going, not only in the introduction).
- *Knuth–Larrabee–Roberts* — excessive subscripts/superscripts are a writing defect;
  documentation of algorithms, and effective use of tables and diagrams, is part of
  mathematical presentation, not ancillary.
- *Stacks Project* — the local unit is a one-line transition, a precise definition or
  result, and a proof whose sentences cite exact prior tags; each result has **one**
  canonical statement and a stable reference that later uses point to instead of
  paraphrasing.
- *Lamport* — structured proofs for the proof interior (already the default — see
  `structured-proofs.md`).

A **dependency graph** is legitimate as an appendix supplement *after* the narrative has
established what the nodes mean. It is not legitimate as a substitute for the narrative
(it cannot supply one retroactively), and it must not become one of several overlapping
status systems (see the reproducible-bundle and skeleton sections).

## Pick one genre and one audience first {#genre-and-audience}

Before writing sections, fix two things and hold them:

1. **Genre.** One of: research paper, research note, specification, survey, graduate
   notes. Do not alternate among a paper, an issue tracker, a correction log, a referee
   report, and a consistency audit. If material genuinely belongs to a second genre
   (a backlog, a changelog, an audit), it goes in a labeled appendix, not interleaved.

2. **Declared reader, and honor it.** State what the reader already knows, then:
   - For **standard objects** the reader knows, do not re-teach. Fix conventions in one
     sentence instead: "We write `M(n)` for the form on `M` scaled by `n`, and `O^+`
     for the subgroup preserving the chosen component of the positive cone."
   - For **nonstandard objects** (the document's own constructions, distinguished
     divisors, unusual normalizations, competing meanings of a term, any object whose
     category affects a theorem), give complete definitions.

   Explanatory space is allocated *inversely to standardness*: expand the novel, cite
   the familiar. The common failure is the reverse — a textbook paragraph on a standard
   domain, and a schematic gesture at the new construction that actually controls the
   moduli problem.

**When the prompt demands both exhaustive capture and a clean read-through.** A prompt
that asks you to collect *all* the ontology, *every* attempted strategy, *all* the
footguns and failures, *and* an adversarial audit — while also producing a pedagogical
monograph — is issuing two conflicting instructions. Archival completeness pulls toward
retaining everything; a monograph pulls toward selection and narrative. Do **not** split
the difference by retaining everything and surrounding each claim with status
qualifications — that is exactly the failure this reference exists to prevent. Resolve it
by **splitting surfaces**: the main text carries the canonical theory and argument; the
exhaustive capture (every strategy, every footgun, every failure, the audit) goes to
labeled appendices. You satisfy both demands, in different places.

## Statement taxonomy {#statement-taxonomy}

Use ordinary mathematical environments, one meaning each. Never a project-management
environment.

| Environment | Meaning |
| --- | --- |
| **Known theorem** | Imported result — exact source and theorem number required |
| **Theorem / Proposition / Lemma** | Proved *in this document* |
| **Conjecture** | Exact assertion believed true |
| **Question** | Genuinely open; no preferred answer asserted |
| **Conditional theorem** | Exact conclusion under named unproved hypotheses |
| **Construction** | Explicit input, output, functoriality |
| **Computational proposition** | Exact finite assertion certified by a specified computation |
| **Remark** | Interpretation or comparison |
| **Warning** | Rare local exceptional case or counterexample |

Rules:

- **One environment, one provenance.** Do not let "Theorem" mean *imported* in one place
  and *computed* in another. The reader must know from the label whether to expect a
  citation, a proof, or a certificate.
- **No "Required theorem: Prove X = Y."** The mathematical content is the equality;
  "prove it" is backlog language. Write `**Conjecture.** X = Y.` then, in prose,
  "Strategy A proves this by establishing Lemmas 4.1–4.3."
- **State conjectures at their strongest justified level.** If the discussion supports an
  expected answer, assert it: `A = B = C = D`, not "determine the relation among these."
  The strong form is more informative, permits conditional deductions, and does not make
  the proof harder. Reserve **Question** for when the expected answer is genuinely
  unknown.
- **One encoding per block.** Do not let the block class say `problem`, the anchor say
  `conj-…`, and the title say "Theorem." Pick one and make all three agree.

## Definitions must be closed {#closed-definitions}

A definition states conditions that determine membership in a class. Its terms cannot
depend on unspecified future theory.

Banned inside a definition: "the controlled singularities allowed by the period
problem," "a suitable class," and any adjective whose meaning is deferred. Also fix the
**category** of every datum — a "degree-2 class" must be declared Cartier bundle,
reflexive sheaf, or numerical class; leaving it undetermined leaves every downstream
moduli functor undetermined.

If the object is not yet closed, label it honestly instead of calling it a Definition:

- **Provisional moduli template** — intended data listed, category unresolved.
- **Construction problem** — the object is not yet defined uniformly.
- **Conjecture** — an exact expected equivalence can be stated even if the object cannot.

For a families/moduli definition, specify the category of families, the relative
singularity condition, the marking/polarization equivalence, and the base-change
behavior. A groupoid-of-families definition (`M(S) =` the groupoid of such-and-such flat
families over `S` with such-and-such isomorphisms) is closed; a list of fiberwise
conditions is not.

The word **"datum"/"data" is not a license to defer.** It must be followed *immediately*
by a complete tuple and the equivalence relation on it. It may not float as a generic
label for "whatever information a later theorem turns out to need," and the same name may
not silently denote two inequivalent tuples (e.g. a resolved-cover datum and a singular
datum have different automorphism theories — give them different names and state the
conjectured equivalence).

## Negative statements need positive content {#negative-statements}

"X is not Y" and "one must not infer Y from X" are appropriate **once**, to correct a
genuinely plausible ambiguity. They must not become the principal mode of exposition.

**Gate.** A negative statement is admissible only if it is immediately followed by at
least one of:

- a counterexample;
- an obstruction class;
- a missing hypothesis;
- a precise converse that fails;
- a theorem giving sufficient conditions;
- a reference to the exact argument in which the false implication had been used.

Without one of these it records anxiety, not mathematics — delete it and state the
positive reduction instead.

Replace, don't accumulate:

> ✗ "A diagram of rational domains is not automatically a diagram of arithmetic
> quotients." (repeated in five sections)

> ✓ The inclusion `D(T) ↪ D(T')` descends to a morphism of arithmetic quotients exactly
> after one specifies a homomorphism `Γ → Γ'` compatible with the embedded lattices.
> Proposition X constructs it; Proposition Y identifies its image with `Stab_{Γ'}(Zα)/⟨w_α⟩`.

Same discipline for a repeated "finite is not integral" caveat: state one exact positive
result and one exact missing result.

> ✓ **Proposition.** Reduction mod `T` gives a map `r_k` from integral orbits to finite
> orbits; Appendix A determines its target.
> **Conjecture.** `r_k` is bijective for `k = 1, 2`.
> To prove it, it suffices to compute the image of each integral parabolic stabilizer in
> the corresponding finite stabilizer and prove transitivity on the fibers.

That removes the need for five standalone warnings.

**Replace "X is not a complete Y" with the exact conditions that would upgrade X to Y.**
When the caveat is that a partial object falls short of a claimed one, do not warn —
enumerate the remaining obligations as a proposition.

> ✗ "A sliced wall arrangement is not a Coxeter chamber." (repeated in five sections)

> ✓ Proposition N constructs the sliced arrangement. To identify it with a Coxeter
> chamber it remains to prove: (i) every displayed normal is a reflective root; (ii) the
> displayed roots are simple; (iii) their chamber is fundamental; (iv) every reflective
> wall meeting the chamber is displayed.

**Warnings are local and rare.** A warning is justified only for a genuinely surprising
local exception (e.g. a quotient singularity of group order 4 but canonical index 2),
placed immediately after the object it modifies. Do not hoist warnings into a global
catalogue detached from the arguments they govern.

## Notation for structural compression {#notation}

The standard is not maximal symbol density — excessive sub/superscripts are themselves a
writing defect. The standard is: **name the objects and maps that recur or enter a
diagram, then use those names consistently.**

- Name parameter spaces, acting groups, period maps, normalization maps `ν`, reduction
  maps `r_k`, stabilizer homomorphisms, classifying maps. Replace prose like "the image
  of the stabilizer of the root inside the degree-2 arithmetic group" with a symbol.
- **Distinct objects get distinct symbols.** Do not let `E` mean `U ⊕ E_8` in one
  section and an exceptional curve in another.
- **Introduce an undecorated name only after the decorated incarnations are proved
  equal,** or under an explicit standing convention. Using `F` before `F^dir = F^Hdg` is
  proved smuggles in an unproven identification.
- A notation table lists **globally recurring** symbols only, not every local variable.

Worked compression — a parameter-count that hides its group action:

> ✓ Let `F = Y^τ`; for `p ∈ F` let `U_p` be the invariant curves with one node at `p`.
> Put `U = ⋃_p U_p`, `G = Z_Aut(Y)(τ)`, `G_p = Stab_G(p)`. Then `G` acts on `U`, `G_p`
> acts on `U_p`, and the presentation stack is `[U/G]` (or one component `[U_p/G_p]`).

The symbols expose the choice the prose concealed: the full centralizer acts on the
union over all fixed points, not on the component indexed by one chosen `p`.

## Proof detail is proportional to risk {#proof-detail}

Allocate detail by novelty and danger, not inversely. Elementary local calculations are
concise for an expert reader. Spend the detail on the steps where a plausible sentence
hides a false implication:

- integral vs. rational lattice decompositions (a rational eigenspace split does **not**
  give the integral one — the intersection with the lattice and discriminant gluing must
  be computed);
- primitive closures and discriminant gluing;
- descent of a group action to an arithmetic quotient;
- family-level simultaneous resolution;
- extension of a combinatorial/affine symmetry to an algebraic morphism;
- finiteness and no-further-coarsening arguments.

A **proof sketch is a verifiable chain of reductions**, not a suggestive verb. It names
(1) the exact intermediate statements, (2) which are standard and where proved, (3) which
integral/descent/gluing/finiteness issue is nonformal, (4) why they imply the result.
Banned as load-bearing: "by separating," "the same argument works," "one checks,"
"standard transitivity gives," "the construction is natural" — unless the decomposition,
check, theorem, or universal property is stated on the spot.

**"natural," "canonical," "standard," "compatible" are claims.** Each names a category,
action, or diagram the property holds relative to, or it is deleted.

## Motivation before construction {#motivation}

Introduce the task a construction solves before the construction. Each construction
answers, locally:

```
input  →  construction  →  output  →  role in the main argument
```

State the role in one sentence first. "Fix `p`, subtract `dim Z_Aut(Y)(τ)`" is arbitrary
until the reader is told the centralizer is the automorphism group of the presentation
`(Y, τ, B)`, so the presentation stack is `[U/G]`. The reflection twist `I' = w_α I` is
arbitrary until the reader is told it flips the eigenvalue of the distinguished root
while fixing `α^⊥`, converting the vanishing cycle from anti-invariant to invariant.

## Computations tie to propositions and are reproducible {#computations}

Before a computation, state what it will establish; after, state exactly what follows. A
computation with no attached proposition is diagnostic noise in the main text.

A computational appendix supplies:

```
input  →  algorithm  →  certificate  →  mathematical consequence
```

- **Orbit tables:** representative, intrinsic invariants, `|O|`, `|Stab|`, geometric
  interpretation/status — one row each. Anonymous internal labels (`A, B, C, D`, `AAA,
  ABC, …`) may not appear in the main text; if their intrinsic meaning is unknown, that
  fact sends the whole table to an appendix.
- **Gröbner / CAS computations:** the ideals, charts, coefficient field, monomial order,
  software and version, and the script or certificate identifier. "Gröbner-basis
  computations on four charts were performed" is not reproducible.
- **Wall / Coxeter computations:** the complete Gram matrix and the explicit map from
  graph labels to lattice vectors.

## Strategies are conditional implications {#strategies}

A list of everything that would eventually help is a backlog, not a strategy. Rebuild
each strategy as a **conditional theorem plus its proof**:

1. state the conditional theorem (conclusion under a short list of named hypotheses);
2. prove the conditional implication;
3. name the exact unproved inputs;
4. name the principal nonformal bottleneck;
5. contrast with competing strategies (which shared hypotheses each establishes).

> ✓ **Conditional theorem.** Assume (i) the open stack is the normalization of the chosen
> component; (ii) at each cusp the normalized closure is the toroidal embedding of the
> saturated fan; (iii) local normalizations glue along 1-cusps; (iv) the classifying map
> is finite and generically injective. Then the normalized KSBA closure is the induced
> semitoroidal compactification.

Then say which hypothesis is expected hardest. "With A1–A8 the conclusion follows by
normality and finite birationality" is too compressed for a central argument — it hides
whether A1–A8 are minimal, independent, or jointly sufficient.

## Citations at the level of dependence {#citations}

Cite what is imported, at the point of use. Distinguish, explicitly:

- "standard terminology; see [Author, §…]";
- "this exact classification is [Author, Theorem N]";
- "the following adaptation is new and proved here";
- "we expect [Author, §…] to adapt, but have not checked Step k."

> ✗ "Standard transitivity results imply the following [Wall; DK]."
> ✓ "By Wall [Thm X], `O(I_{2,9})` acts transitively on primitive isotropic vectors;
> applying [DK, Lem Y] to isotropic planes gives the second assertion."

A broad "source map" (Author ↦ which sections they cover) may remain as an annotated
bibliography, but it does not replace theorem-level citations.

## Obsolete mistakes leave the main line {#obsolete}

Never embed internal version history in theorem statements or narrative ("an earlier
calculation used 2 rather than 4"). Three legitimate dispositions:

1. **Delete** the obsolete assertion; state the corrected result with proof.
2. **Keep as counterexample/obstruction** only if the failed argument teaches something
   structural — i.e. it supplies a counterexample, a structural obstruction, evidence
   discriminating between competing conjectures, a reusable partial lemma, or a warning
   against a *genuinely tempting* false theorem. Otherwise it is not worth keeping.
3. **Move to a "Research history and discarded approaches" appendix**, each entry in a
   fixed three-field form — **Discarded claim** / **Failure** (the exact false assumption)
   / **Correction** (the proposition that replaces it) — with the obsolete version noted.

> ✓ **Lemma.** `(α_20, α_21) = 4`. *Proof.* [derivation]; substituting `4` gives corank
> 2, as required; the value `2` gives corank 0 and is incompatible with the ambient
> lattice. ∎
> (If provenance matters: one changelog line — "corrects the input used before v3.")

Avoid "an earlier agent assumed…" and warnings against mistakes no reader would make.

## Reproducible bundle {#bundle}

The document is not operationally self-contained unless it ships together with: the
source, the bibliography, the cross-reference configuration, all figures, computational
scripts and input data, a build command, a rendered PDF/HTML, and a short version
history. Cross-references must resolve in the distributed form — a raw `@sec:…` or an
empty references section makes the note harder to use than necessary.

## Report skeleton {#skeleton}

A genre-neutral order that satisfies the master rule:

1. **Introduction and main statements** — the objects in minimal terms, the principal
   conjecture/theorem, the strongest proved partial results, the one unresolved
   obstruction, and a one-paragraph roadmap (which section supplies which ingredient).
2. **Objects and constructions** — complete definitions of the nonstandard objects only.
3. **The core theory** — sections ordered by dependency; each opens by stating its role:
   *what object, why needed, what it establishes, where it is used*, then result, then
   proof, then interpretation (state → prove → interpret, in that order).
4. **The conditional main theorem** — reduce the principal conjecture to a short list of
   precise hypotheses, and prove the reduction.
5. **Comparison of strategies** — which hypotheses each approach establishes.
6. **Appendices** — computational data and scripts; candidate/auxiliary data; research
   history, corrections, and discarded approaches; a single status table and notation
   index; the bibliography.

There is exactly **one** retrospective status surface (the appendix status table), not a
warning catalogue *and* a dependency graph *and* a ledger *and* a self-audit repeating
each other.
