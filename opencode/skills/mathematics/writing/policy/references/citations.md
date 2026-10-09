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
used. The converse holds: a sentence that calls an object "standard",
"classical", or "the usual one" is a citation owed and not given. The
word asserts that a source exists; the citation at the definition is
what records it, and a remark about what a database or implementation
stores is not mathematics the reader of the chapter uses (`SEC-17`).

Observed in `dzackgarza/research`,
`research/lattice-theory/lattice-theory.md` at `f80def8175`, remark
"What the database stores".

**Banned:** "We refer to: [@Vin85]; [@Vin75]."; "The quadratic
character itself is standard; the database field
`integral.quadratic_character` stores its conductor-discriminant datum
$d_L$, not a table of character values."

**Preferred:** "The structure theorem for the automorphism group we use
is [@Vin85, Theorem 2.1]; the arithmeticity result is [@Nik80, Prop.
1.15.1]" — each citation at the claim it supports, with a locator; the
definition block of $\chi_L$ carrying the citation to the source that
defines the discriminant character, and no remark about storage.

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

## `CITE-7`: A citation defines no symbol and supplies no construction

Every object that a statement uses is defined in the document's own
notation, at a defining occurrence the statement can cite (`DEF-26`,
`SYM-1`). "In the notation of [@X, Thm. n], let $\operatorname{MM}(L)$
be …", "the subgroup appearing in [@X]", and "as constructed in [@X]"
define nothing: the reader must leave the page to learn what the symbol
denotes, and the document's theorem is a theorem about an object it
never introduced. The citation records where the object was first
constructed or the result first proved; the construction itself is
transcribed into the document (`DEF-2`) in the document's conventions,
and the cited theorem is stated with the hypotheses it needs
(`CITE-6`). A result whose objects are defined only by reference is a
borrowed assertion, not a statement the document makes.

Observed in `dzackgarza/research`,
`research/lattice-theory/Isometries-and-Arithmetic-Invariants.md`
(working tree over `26d4e303bc`), theorem "The Miranda–Morrison exact
sequence".

**Banned:** "In the notation of [@MM09, Thm. V.5.1], let
$\delta_L\colon\Orth(A_{L,q})\too\operatorname{MM}(L)$ be the
Miranda–Morrison connecting morphism and let $g(L)$ be the genus group";
"If $K_L\injects\Sigma(L)$ denotes the pullback subgroup appearing in
[@MM09, Thm. V.5.1], then …".

**Preferred:** definition blocks for $\Sigma(L)$, $\Sigma^\#(L)$, and
$K_L$ transcribed from the source into the document's notation, with
$\operatorname{MM}(L)$ defined as the cokernel the document's own
sequence $1\to K_L\Sigma^\#(L)\to\Sigma(L)\to\operatorname{MM}(L)\to1$
exhibits and $g(L)$ defined as the genus group of the genus chapter
(`SEC-12`); then the theorem, with [@MM09, Thm. V.5.1] cited at the
exactness claim.

## `CITE-8`: Every assertion has an argument, a referent, or a citation

A sentence that asserts a mathematical fact carries one of three
things: an argument on the page, a reference to a block of the
document that proves it, or a citation with a locator. "Consequently",
"hence", "classical", and "well known" are not a fourth kind of
support; a consequence with no antecedent on the page, and a theorem
named by description — "the classical finiteness theorem for
representations by an indefinite integral quadratic form" — are
appeals to authority with no statement, no hypotheses, and no locator
the reader can open. A display asserts in the same way as a sentence:
writing a group as a semidirect product asserts that a specific
extension splits, which is a theorem with a proof or a citation, and
writing it without either is the appeal to authority in notation
(`EV-11`, `DEF-40`). The boundary with `CITE-4`: that rule governs the
word "standard" at a definition; this one governs assertions. The
boundary with `PR-9`: that rule governs "clearly" before an argument
that exists; this one the assertion whose argument does not exist on
the page. `EV-9` governs the sequence stated below the strength the
source proves.

Observed in `dzackgarza/research` at `57c8eb1cb0`:
`research/lattice-theory/definite/minima-and-regularity.md`,
proposition "Finiteness in the definite and indefinite cases";
`research/lattice-theory/discriminant-forms-and-genus.md`, the proof
that names "the classical finiteness theorem";
`research/lattice-theory/Isometries-and-Arithmetic-Invariants.md`,
proposition "The orthogonal group of a degenerate form".

**Banned:** "Consequently $\Orth(L)$ is finite." with no antecedent
that bounds $\Orth(L)$; "the classical finiteness theorem for
representations by an indefinite integral quadratic form." as the
whole citation; "Hence
$$\Orth(M)\isoto\Hom_{R\text{-}\mathbf{Mod}}\qty{M^{\mathrm{nd}},\radic(M)}\rtimes\qty{\Aut_{R\text{-}\mathbf{Mod}}(\radic(M))\times\Orth(M^{\mathrm{nd}})}.$$"
as the end of a proof that exhibited no splitting.

**Preferred:** "For a basis $e_1,\dots,e_n$ of $L$, evaluation
$\Orth(L)\to\prod_iL[e_i^2]$, $g\mapsto(ge_i)_i$, is injective; for $L$
definite each shell $L[m]$ is finite, so $\Orth(L)$ is finite."; the
theorem in its own block, with hypotheses, and the citation with a
locator at the block; the exact sequence
$$1\to\Hom_R(M^{\mathrm{nd}},\radic(M))\to\Orth(M)\to\Aut_R(\radic(M))\times\Orth(M^{\mathrm{nd}})\to1$$
with the section induced by a splitting
$M\cong\radic(M)\oplus M^{\mathrm{nd}}$ written out, and only then the
semidirect product.

## `CITE-9`: A cited result is transcribed into the document's conventions; the translation is not narrated

A result taken from a source is stated in the document's own sign,
notation, and vocabulary, with the source cited for the result. The
source's convention, the sign that relates it to the document's, and the
sentence telling the reader how to read the source are not part of the
statement: a sentence that instructs the reader how to read is `PR-32`,
and a statement that holds only after the reader applies a translation
is not a statement of the document. The translation is recorded once, at
the document's definition of the object, as the equation that relates
the two forms. A hypothesis labelled by its source — "the condition of
[@Hum90, §6.8]" — is an undefined term (`TERM-7`): the condition is
stated, and the source is cited for the theorem that uses it. The
boundary with `CITE-7`: that rule asks that an object constructed by a
source be transcribed; this rule asks that the transcription leave no
trace of the source's convention in the statement.

Observed in `dzackgarza/research` at `9cfdecf73d`:
`research/lattice-theory/Coxeter-Systems-and-Lattices.md`, definition
"The form of a Coxeter system" and definition "Hyperbolic Coxeter
systems";
`research/lattice-theory/Isometries-and-Arithmetic-Invariants.md`,
theorem "The Miranda–Morrison exact sequence".

**Banned:** "The source [@Hum90, §5.3] uses
$B(\alpha_s,\alpha_t)=-\cos(\pi/m(s,t))$, so $B(\alpha_s,\alpha_s)=1$
and $b=-2B$." followed by "Every definiteness statement quoted from that
source is therefore read here with the sign reversed, in the convention
of @def:definiteness."; "**The condition of [@Hum90, §6.8].**" as the
name of a hypothesis; "In the notation of [@MM09, Thm. V.5.1], let
$\delta_L\colon\Orth(A_{L,q})\too\operatorname{MM}(L)$ be the
Miranda--Morrison connecting morphism" inside a theorem statement.

**Preferred:** "$b=-2B$ for the form $B$ of the geometric representation
[@Hum90, §5.3]" once, in the definition of $b$, and every later
statement in the sign of $b$; "$(W,S)$ is *hyperbolic* when $b$ has
signature $(1,n-1,0)$ and $b(\lambda,\lambda)>0$ for every $\lambda\in
C$ [@Hum90, §6.8]"; $\delta_L$ and $\operatorname{MM}(L)$ defined in the
document's own definition block (`CITE-7`), the theorem stating the
sequence in that notation, and [@MM09, Thm. V.5.1] cited for its
exactness.
