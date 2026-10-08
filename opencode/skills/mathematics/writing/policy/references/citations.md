# Citations (`CITE-*`)


## `CITE-1`: Cite through the bibliography

Every citation goes through the document's bibliography, with a stable
citation key and a locator: `[@OR23, Definition 1.5.1]`. The bibliography
database is the source of truth for bibliographic metadata. If a work is not
in it, add it there first, and take its metadata from an external record such
as the publisher, DOI, or arXiv entry, never from memory. The citation style
renders author, title, and year: never repeat them in prose, and never write
an inline author-year citation such as "(Author, Year)". Such a citation
fabricates metadata that the bibliography already owns. A stable permalink
whose job is to take the reader to a canonical definition or theorem is
navigation, not a citation; bibliographic claims about that work still go
through the bibliography.

## `CITE-2`: No inline URLs as citations

**Banned:** an inline URL to arXiv, a DOI, or nLab in place of a citation.

## `CITE-3`: Cite a tagged reference by its tag

Cite a reference whose results carry stable tags, such as the Stacks
Project, by the tag of the result: "[Stacks, Tag 02LS]". Read the tag's
page before you cite it. A wrong tag still renders, and it sends the
reader to a different result.

## `CITE-4`: Every citation has a local referent

A citation is attached to the specific definition, theorem, construction,
computation, or attribution it supports, with a locator that reaches it
(CITE-1). A bare list of works at the end of a passage — names and years
with no stated result — is a reading list, not a citation: the reader
cannot tell which work proves which claim. Cite each result where it is
used.

**Banned:** "We refer to: [@Vin85]; [@Vin75]."

**Preferred:** "The structure theorem for the automorphism group we use
is [@Vin85, Theorem 2.1]; the arithmeticity result is [@Nik80, Prop.
1.15.1]" — each citation at the claim it supports, with a locator.

## `CITE-5`: Attribution belongs to the statement, not appended to it

Provenance is metadata of the theorem or definition it belongs to, not
a trailing clause after a proof sketch. Do not write "this is due to X"
after a vague sketch — the attribution then certifies prose rather
than a stated result, and the reader cannot tell which claim is X's.
Put attribution in the statement block: in the theorem's title, in a
provenance field, or as the citation attached to the precise
mathematical claim it supports (`CITE-4`). A vague claim with a famous
name attached is still a vague claim.

**Banned:** "…and the map is injective. This is due to Kitaoka." with no
theorem block and no locator; a proof sketch followed by "see Miranda
and Morrison for this."

**Preferred:** the theorem block with the citation at the claim —
"::: {.Theorem} ### Discriminant factorization — $\rho_L$ factors …
([@MM99, Theorem 4.2]) :::" — and the proof either present or omitted
per the house's proof obligation (`SEC-6`); provenance claims in the
statement's metadata, never in trailing prose.

## `CITE-6`: Hypotheses are stated in the block, never delegated to a citation

A citation records where a result is proved. It does not carry the
hypotheses of the block that cites it. "If $L$ satisfies the hypotheses
of [@X, Thm. n]" states no hypothesis: the reader must open the source
to learn what the block assumes, the block cannot be checked against
its own text, and a different edition or numbering silently changes the
theorem. Transcribe the hypotheses from the source into the block
(`DEF-2`, `STR-3`) and keep the citation as provenance at the claim
(`CITE-4`). "In particular" after such a clause is the tell: it lists
one hypothesis and hides the rest.

Observed in `dzackgarza/research`,
`research/lattice-theory/Isometries-and-Arithmetic-Invariants.md`
(working tree over `26d4e303bc`), corollary "Nikulin stable-range
vanishing", and
`research/lattice-theory/classification/two-elementary-lattices.md` at
`26d4e303bc`.

**Banned:** "If $L$ satisfies the hypotheses of [@Nik80, Thm. 1.14.2],
in particular $\rank L\geq\ell(A_L)+2$, then $\operatorname{MM}(L)=0$";
"… subject to the admissibility conditions of [@Nik80, Thm. 3.6.2]".

**Preferred:** the block opens with every hypothesis of the cited
theorem in its own words — the parity and signature conditions on $L$
and the rank-versus-length inequality at each prime, transcribed from
[@Nik80, Thm. 1.14.2] — and then states "$\operatorname{MM}(L)=0$ and
$g(L)=1$" with the citation at the claim; the admissibility conditions
of the classification theorem listed in the block, the citation after
them.
