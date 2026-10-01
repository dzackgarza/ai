---
name: mathematical-writing-policy
description: Use when writing, editing, or reviewing reader-facing mathematical prose in any repository (exposition, definitions, theorems, examples, remarks, resource annotations, docs books, wikis, papers), or when a contribution, commit, or review cites a writing-policy code such as PR-30, DEF-26, SYM-1, or STANCE-05.
---

# Mathematical writing policy

This is the one catalogue of mathematical writing rules for every repository
that points here. Each rule has a stable code, a banned example, and the
preferred replacement. Cite the codes in contributions, commit messages, and
review.

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
| Section structure | `SEC-*` | Statement blocks as the skeleton of a section. | [section-structure](references/section-structure.md) |

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
- For a stance defect, say who is judged, supervised, or spoken for, and which
  authority the writer assumes. Show why repeated helpful-looking sentences
  are severe, and do not reduce the defect to verbosity or a missing citation.
- Make the preferred form show the actual correction. A softer command, a
  first-person suggestion, or "Suggested reading" can keep the same hierarchy.
- Ground every preferred form in a standard formulation found in textbooks
  and papers. Do not invent it from memory.
- When a later correction shows that an earlier rule has the wrong model,
  rewrite or delete the earlier rule. An appended stronger rule that leaves
  the contradiction authoritative keeps the defect.
- Integrate a new rule into its family under the next free code. Never reuse
  or renumber a code: repositories and commit histories cite them.
- Keep evidence apart from proposals. A preferred form must not invent
  coverage, history, or facts about a source.
- Do not quote a private message. Quote repository prose only.
