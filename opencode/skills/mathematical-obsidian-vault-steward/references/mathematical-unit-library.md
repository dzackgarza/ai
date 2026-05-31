# Mathematical Unit Library

Use these units when classifying source material and shaping durable Obsidian notes.
The vocabulary is mathematical, not project-management or software-status language.

## Callout Policy

Use Obsidian callouts for formal mathematical units except remarks.

Preferred callout forms:

```markdown
> [!definition] Name
> ...

> [!theorem] Name
> ...

> [!lemma] Name
> ...

> [!proposition] Name
> ...

> [!corollary] Name
> ...

> [!conjecture] Name
> ...

> [!question] Name
> ...

> [!problem] Name
> ...

> [!construction] Name
> ...

> [!fact] Name
> ...

> [!example] Name
> ...

> [!counterexample] Name
> ...

> [!calculation] Name
> ...

> [!computation] Name
> ...

> [!proof] Name
> ...

> [!proof-sketch] Name
> ...
```

Do not use `> [!remark]` for new content.
A remark is ordinary prose in the surrounding note, usually under the relevant heading
or immediately after the formal unit it comments on.

Do not rewrite historical notes solely to remove existing remark callouts.
Apply the no-remark-callout rule to new or touched content.

## Unit Definitions

- `definition`: introduces terminology, notation, named lattices, groups, divisors,
  moduli spaces, object classes, equivalences used as definitions, or standing
  hypotheses.

- `notation`: fixes symbols, conventions, coordinate choices, normalizations, or
  translation between source notation and vault notation.

- `theorem`: a proved central result with exact hypotheses and a proof in the note,
  source, or clearly linked reference.

- `lemma`: a proved supporting result used inside a larger proof or construction.

- `proposition`: a proved result of intermediate scope that is more self-contained than
  a lemma but not the main theorem.

- `corollary`: a result that follows directly from a named prior result.

- `conjecture`: a theorem-shaped claim intended to be true but not proved in the
  available source and vault context.

- `question`: an unresolved mathematical query, criterion, or choice where the correct
  statement is not yet known.

- `problem`: a larger open task or research problem with multiple subquestions or proof
  obligations.

- `construction`: an explicit recipe, quotient, disjoint union, normalization, family,
  package, diagram, model, construction step, construction requirement, or procedure to
  build.

- `fact`: a small source-backed assertion about an already-defined object that is useful
  but not theorem-shaped.

- `example`: a concrete instance illustrating a definition, construction, theorem, or
  phenomenon.

- `counterexample`: a concrete instance that refutes a claim or shows a hypothesis is
  necessary.

- `calculation`: a hand calculation, local computation, displayed derivation, table
  derivation, or formula check.

- `computation`: a machine-assisted or algorithmic computation whose inputs and outputs
  should be reproducible.

- `proof`: complete proof of a formal unit.

- `proof-sketch`: incomplete proof architecture, proof strategy, or outline that should
  not be treated as a proof.

- `remark`: contextual, caveat-like, comparative, historical, motivational, or
  provenance prose.

## Status Rules

- If a statement lacks proof but is intended as a result, classify it as `conjecture`.

- If the source is deciding what the correct result should be, classify it as `question`
  or `problem`.

- If the source states a rule, criterion, implication, equivalence, or if-and-only-if
  result, classify it as `proposition` when established and as `conjecture` or
  `question` when unresolved; do not use `remark` only because the durable edit will be
  prose.

- If a target note’s frontmatter, tags, type line, callout, or heading frames a
  theorem-shaped item as conjectural, proposed, or open, preserve that status in the
  annotation; do not upgrade it to `proposition` because the source label says “Theorem
  Statement”.

- If a source item introduces a named lattice, group, divisor, moduli space, or standing
  identification, classify it as `definition`.

- If the source gives an object to build while its properties remain unproved, classify
  the object as `construction` and list the unproved properties as conjectures or
  questions.

- If the source states a required construction step, such as choosing compatible
  auxiliary data, classify it as `construction`, even when the existence or
  compatibility proof remains open.

- Do not use `fact` for the act of defining or constructing a named object.

- If a proof is partial, classify it as `proof-sketch` or a prose remark about a proof
  gap, not as `proof`.

- If a small assertion is source-backed but not structurally important, classify it as
  `fact`.

- If a claim is refuted later in the same source, do not incorporate it as a durable
  claim. Preserve it as an objection-resolution remark only when useful.

## Routing Rules

- Route units to the note for the mathematical object they modify.

- Definitions and notation belong near the concept or construction that uses them.

- Objections to theorem-like statements belong near the theorem-like statement, not in a
  standalone objection note by default.

- Proof gaps belong near the proof or statement they affect.

- Examples and counterexamples belong near the definition or result they illuminate
  unless they are reused in multiple contexts.

- Calculations belong near the formula, cusp, lattice, divisor, diagram, or construction
  they compute.

- Computations need input data, command or method, output, and provenance.
  Do not turn computational output into theorem status without proof.

- Remarks should improve local interpretation of a nearby unit.
  They are not dumping grounds for unrelated source residue.

## New Note Test

Create a new durable note only when the unit has a stable referent and future retrieval
value independent of the source file.

Do not create a new note for:

- a single objection to an existing theorem;

- a proof gap that belongs under an existing conjecture or theorem;

- a generic summary of an inbox source;

- a source-local conversational turn;

- a bundle of unrelated extracted facts;

- a theorem-shaped claim with missing hypotheses.

When a separate objection-resolution note is justified, link it from the affected
theorem or conjecture and state why it deserves standalone retrieval.
