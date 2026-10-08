# Cross-references (`XREF-*`)


## `XREF-1`: Reference by stable identifier

A reference to a definition, theorem, problem, or other numbered block uses
the block's stable identifier through the medium's resolver. A reference by
position ("above", "the previous theorem") breaks when the document is split,
transcluded, or reordered (`PROSE-03`). Use only reference syntax that the
resolver matches: a renderer can drop an unmatched reference silently and
leave the sentence around it dangling. The house conventions name the
resolver and its label format.

## `XREF-4`: Sections, pages, and figures

Link a page or section by its path and anchor, with link text that reads as
part of the sentence: "[Green's theorem](calculus.md#greens-theorem)". A
figure has an identifier and is referenced through it.

## `XREF-5`: Link every use of a defined term to its definition

Every use of a term that the document defines, where the use relies on the
defined meaning, links the term's defining occurrence. The link takes the
reader to the precise meaning (`DEF-1`); an unlinked use leaves the reader to
guess which definition applies and whether the term is used in its defined
sense. This applies to every such use, not only the first. A page or section
named after a mathematical term lets the reader reach the intended
definition: a local definition when it adds value for the document's
readers, otherwise the canonical external source.

**Banned:** "a torsion module" with no link to the torsion definition; "A
theorem that $F$ lands in $D_P$ is a factorization" with no link to the
definition of landing; "a basis indexed by $I$" with no link to the basis
definition; a page titled "Sylow theory" that never defines or links a
Sylow subgroup.

**Preferred:** "a [torsion](#def-torsion) module", in the document's link
syntax.

**Reading task:** for a page or section named after a mathematical term,
check that the reader can reach the intended definition.

## `XREF-6`: "Is defined in …; it is …" for recall

A defined term whose defining occurrence is elsewhere is referred back to
as "A generalized element with domain $T$ is defined in
@def-generalized-element; it is a morphism $T\to X$" — two clauses, the
first meta-commentary about where the definition lives, the second
restating the definiens. The standard rhetorical device in papers and
textbooks for a non-defining use that reminds the reader is "Recall."

**Banned:** "A generalized element with domain $T$ is defined in
@def-generalized-element; it is a morphism $T\to X$." — wordy, two
clauses where one does the work, with a semicolon joining meta-commentary
to definiens; $T$ unbound.

**Preferred:** "Recall that a generalized element with domain $T$
(\ref{def-generalized-element}) is a morphism $T\to X$" or "Recall
(@def-generalized-element) that a generalized element of $X$ with domain
$T$ is a morphism $T\to X$." One clause, "Recall" signals this is not the
defining occurrence but a reminder that cites it, and the parenthetical
`\ref` is the link.

**Banned:** "A normal family is defined in Definition 3.2; it is a family
of holomorphic functions in which every sequence has a locally uniformly
convergent subsequence."

**Preferred:** "Recall that a normal family (Definition 3.2) is a family
of holomorphic functions in which every sequence has a locally uniformly
convergent subsequence."

A reference label is a pointer to a block, not a name for the object
the block defines. "The twist of @def:form-twist by $-1$" makes the
label the noun; the object has a symbol, and the label follows it as
the link.

Observed in `dzackgarza/research`,
`research/lattice-theory/Lattices-and-Discriminant-Forms.md` (working
tree over `57c8eb1cb0`), definition "Signature subcategories".

**Banned:** "the twist of @def:form-twist by $-1$".

**Preferred:** "the twist $L(-1)$ (@def:form-twist)".

## `XREF-7`: Internal results have references, not nicknames

Refer to an internally authored theorem, lemma, proposition, corollary, or
definition through its resolver reference. Ordinary descriptive prose may
state how the cited result is used, but it does not give the result an
informal proper name. A nickname such as "the primitivity proposition"
creates a second, unstable identifier that is neither the title nor the
label.

**Banned:** "By the primitivity proposition, …" when that phrase names an
internal proposition.

**Preferred:** "By @prp:primitive-embedding, the embedding is primitive."

## `XREF-8`: Displayed mathematical objects use stable references

An equation, diagram, exact sequence, coexact sequence, fiber sequence, or
cofiber sequence that later prose uses has a label and is cited through the
resolver. Position is not an identifier. This applies to displayed objects
as well as statement blocks (`XREF-1`).

**Banned:** "the previous sequence", "the diagram above", or "applying
$F$ to the preceding equation".

**Preferred:** "Applying $F$ to @eq:unit-comparison" or "Exactness of
@eq:localization-sequence gives …".
