# Notation (`NOT-*`)


## `NOT-1`: State the mathematical type

State the mathematical type of every named entity. Distinguish objects and
morphisms in a specified category, categories and functors, natural
transformations, object properties, chosen structures, invariants, sections,
and obstructions.

An obstruction is a specified class or map together with a theorem stating
whether its vanishing is necessary, sufficient, or equivalent to the stated
lifting or extension problem under the given hypotheses. A set-valued
isomorphism invariant has the form $\pi_0(\mathcal C^{\simeq})\to S$; a
functorial invariant with a richer codomain states that codomain and its
functoriality.

The type of a symbol's argument is part of the type: $L^G$ is defined
for a group $G$ acting on $L$, so "$L^I$" for an involution $I$ is
$L^{\langle I\rangle}$ or $\ker(I-\id_L)$, and $L^I$ as written has no
defining occurrence.

Observed in `dzackgarza/research`,
`research/lattice-theory/invariant-and-coinvariant-lattices.md` at
`57c8eb1cb0`, proposition `prop:coinvariant_involution_2elementary`.

**Banned:** "$L^I$" for an involution $I$ where $L^G$ is defined for
groups $G$.

**Preferred:** "$L^{\langle I\rangle}$", or "$\ker(I-\id_L)$".

## `NOT-2`: Typed equality symbols

Literal equality ($=$), isomorphism ($\cong$), and equivalence ($\simeq$) are
written with distinct symbols. An isomorphism is not written as an
equality. $\hookrightarrow$ denotes a stated inclusion,
embedding, or monomorphism; fullness, faithfulness, and repleteness are
asserted separately. Strict pullbacks and pseudo-pullbacks are not identified
by notation.

$\xrightarrow{\sim}$ is written on a map that has been shown to be an
isomorphism, and on nothing else: "$L\isoto E_{10}\perp E_{10}^{\perp L}$"
where the text has constructed only the inclusion
$E_{10}\perp E_{10}^{\perp L}\injects L$ asserts the isomorphism by
decoration, in the wrong direction, with no argument.

Observed in `dzackgarza/research`,
`research/coble/lattices-and-moduli/lattices.md` (working tree over
`57c8eb1cb0`), proof under "Period domain embeddings and
normalization".

**Banned:** "$L\isoto E_{10}\perp E_{10}^{\perp L}$" with only the
inclusion constructed.

**Preferred:** "$E_{10}\perp E_{10}^{\perp L}\injects L$, an
isomorphism since $E_{10}$ is unimodular" — the arrow in the direction
of the map, the isomorphism as a claim with its reason.

## `NOT-3`: One symbol, one meaning

The same symbol has the same type and meaning throughout the document,
including every unit the document includes from elsewhere. Within a single
passage the constraint is tighter (`SYM-4`). Nonstandard notation is
introduced at its defining occurrence, after the standard construction it
abbreviates has been stated.

## `NOT-4`: Standard names

Use established names in their standard meanings: category of elements,
Grothendieck construction, core, arrow category, full subcategory, replete,
natural isomorphism, automorphism group, torsor, monoidal category, abelian
category, preadditive category, kernel, cokernel, discriminant form, genus,
isometry, classifying object, classifying space, classifying category, total
category. Do not coin a name for a notion that already has one.

A standard name is also used for exactly its standard extension. The
discriminant form of a lattice is $\operatorname{coker}(b^\sharp)$
with its induced form, so "discriminant" names the torsion forms that
arise as cokernels; the category of all nondegenerate torsion
quadratic modules is $\mathbf{TorQuad}$, and which of its objects are
discriminant forms of lattices of a given signature is a theorem
[@Nik80, Thm. 1.10.1], not a definition. "Polarization" names the
bilinear form $b_q$ of a quadratic form $q$ (`TERM-12`); a label that
uses it for the adjoint morphisms of a bilinear form reassigns a
standard name.

Observed in `dzackgarza/research`,
`research/lattice-theory/Lattices-and-Discriminant-Forms.md` at
`57c8eb1cb0`, definition "Discriminant quadratic forms", and (working
tree over `57c8eb1cb0`) definition "Lattices".

**Banned:** "Let $\mathbf{DiscQuad}_{\bZ}$ be the category of
nondegenerate quadratic modules"; "@def:polarization" cited for the
adjoint morphisms $b^\sharp$.

**Preferred:** "$\mathbf{TorQuad}_\bZ$, the category of nondegenerate
torsion quadratic modules; the discriminant form $A_{L,q}$ of an even
lattice is an object of it, and the objects of a given signature
modulo $8$ that arise are those of [@Nik80, Thm. 1.10.1]"; "the
adjoint $b^\sharp$ (@def:adjoint)".

## `NOT-5`: No gratuitous temporary notation

New notation earns its place by exposing structure or supporting repeated
use — never by saving characters. A proposition about $M(2)$ does not
introduce $L:=M(2)$; write $M(2)$ at each use. Introducing a local alias
hides the object under discussion, breaks the link to the construction it
restricts (`MA-4`), and multiplies symbols the reader must track
(`SYM-1`). Introduce notation for a *new object* at its defining
occurrence (`DEF-26`), not for an *old object* under a shorter name. A
standard construction with a standard symbol keeps it (`NOT-4`,
`TERM-16`).

**Banned:** "In this section write $L:=M(2)$" with $M(2)$ used three
times; "put $G:=\Orth(L)$" to avoid repeating $\Orth(L)$; a local alias
defined once and used once; "$Q_f$" for $\operatorname{coker}(Uf)$ in
the displayed sequence $0\to UL\to UM\to Q_f\to0$ and then
"$0\to Q_f\to Q_{gf}\to Q_g\to0$" (`dzackgarza/research`,
`research/lattice-theory/Isometries-and-Arithmetic-Invariants.md`,
working tree over `26d4e303bc`, definition of primitive embeddings).

**Preferred:** $M(2)$, $\Orth(L)$, $L^{\mathrm{prim}}[n]$,
$\operatorname{coker}(Uf)$, $\operatorname{coker}(U(gf))$ written out at
each occurrence — the construction stays visible and linked to its
owner, and a standard construction keeps its standard symbol
(`NOT-4`).

A symbol defined by cases whose only role is to reproduce an expression
the field already writes is an alias for that expression and is
deleted.

Observed in `dzackgarza/research`,
`research/lattice-theory/definite/minima-and-regularity.md` at
`57c8eb1cb0`, definition "Minimum, minimal vectors, and kissing
number".

**Banned:** "Let $L$ be definite and put
$$\varepsilon_L\definedas\begin{cases}1,&L\text{ positive definite},\\ \dots\end{cases}$$".

**Preferred:** $\abs{b(x,x)}$ at each use.

## `NOT-6`: Macros encode mathematical normalization, not just typography

A repeated canonical object or construction — discriminant, hyperbolic
lattice, $p$-adic completion, primitive norm-$n$ vectors, discriminant
form, genus invariant — is written through one uniform macro or
definition everywhere it appears, so that equivalent constructions look
equivalent and local notational drift is impossible to introduce. This
is a mathematical requirement, not a typesetting convenience: two
spellings of one construction present it as two objects, and a local
re-derivation (`MA-1`) can silently change the normalization. Define the
macro once at the natural owner (`SEC-12`), link every use to it
(`XREF-5`), and re-derive nothing locally.

**Banned:** a chapter that re-derives $L\otimes_{\mathbb Z}\mathbb Z_p$
as "the completion" with fresh local notation, when the $p$-adic
completion macro was defined in the foundations chapter; "discriminant
form" re-defined locally in one chapter and cited from another; "the
*twist* $b(\lambda)$ of $(M,b)$ is the form $\lambda b$ on the same
module, written $M(\lambda)$" — two symbols introduced in one sentence
for one object (`dzackgarza/research`,
`research/category-theory/framework/Bilinear-and-Quadratic-Forms.md`,
working tree over `26d4e303bc`, the twist); "the corresponding
invariants of $T_{-1}(L)$" in a document whose definition of the
signature subcategories writes the same functor as $(-)(-1)$ and whose
twist definition writes $M(\lambda)$ — a third spelling, introduced
where the construction is used rather than where it is defined
(`research/lattice-theory/definite/minima-and-regularity.md` at
`76d4ef22ae`, definitions "Minimum, minimal vectors, and kissing number"
and "Regular and spinor-regular ternary lattices").

**Preferred:** one defining occurrence per construction, one macro or
symbol reused everywhere — the symbol of the defining occurrence at
every later occurrence — every use linked (`DEF-26`, `NOT-3`,
`SEC-12`).

The same rule fixes the spelling of a category, of an operation, and
of a generated subobject. A category is written through one macro at
every occurrence; two spellings present two objects. An operation is
written on the object the field attaches it to, never on one of its
components. A generated subobject is written as the subobject, never
as a set of multiples, which names no object.

Observed in `dzackgarza/research`:
`research/category-theory/framework/Categorical-Foundations.md` at
`ab530c1dcc`, definition "Category of elements", beside the $\mcc$ of
the surrounding definitions;
`research/category-theory/framework/Bilinear-and-Quadratic-Forms.md`
at `57c8eb1cb0`, definition "Twisting";
`research/lattice-theory/Lattices-and-Discriminant-Forms.md` at
`ab530c1dcc`, example "Subobjects under extension of scalars".

**Banned:** "Let $F\colon C^{\opop}\to\mathbf{Set}$ be a presheaf.";
"For $\lambda\in R$ the *twist* $b(\lambda)$ of $(M,b)$ is the form
$\lambda b$ on the same module, written $M(\lambda)$."; "The inclusion
$\bZ v\hookrightarrow L$" and "$\bR v\hookrightarrow L\tensor_{\bZ}\bR$".

**Preferred:** "Let $F\colon\category{C}^{\opop}\to\mathbf{Set}$ be a
presheaf."; "For $\lambda\in R$ the **twist** $M(\lambda)$ of $(M,b)$
is $(M,\lambda b)$."; "$\langle v\rangle_\bZ\injects L$" and
"$\langle v\rangle_\bR\injects L\otimes_\bZ\bR$".

## `NOT-7`: A semantic macro is an atomic object-valued API

`NOT-6` requires one macro per canonical construction; this rule fixes
the macro's call shape. A macro that names a mathematical construction
takes the construction's semantic operands inside its argument list:
the macro *is* the object, and its arguments are the semantic boundary
of the object. `\disc{L}` names the discriminant of the lattice $L$;
`\padiccompletion{R}{p}` names the completed ring;
`\cardinality{X}` names the cardinality of $X$. A zero-argument
invocation followed by an adjacent operand — `\disc` then a
neighboring $L$ in the source — is a typographic fragment: it renders
the same glyphs while making the source a decorated glyph plus
free-floating operands, so the macro no longer records which object
the author means and a cleanup pass can discard the operand
(`NOT-6`: two spellings present one object as two). The same applies
to completions, localizations, quotients, base changes, and derived
constructions: if the construction has operand/base/index data, that
data belongs in the argument list. Only genuinely typographic helpers
(absolute-value bars, delimiter sizing) are exempt.

**Banned:** `$\disc L$`-style zero-argument use where the macro denotes
a construction on $L$; `\padiccompletion` invoked with the ring left in
adjacent source; a semantic macro migrated to lower arity because the
rendered glyphs looked unchanged.

**Preferred:** `$\disc{L}$, $\padiccompletion{R}{p}$,
$\cardinality{X}$, $\fiberprod{X}{S}{Y}$ — every semantic operand
inside the argument list at every call site. A macro whose arity must
change is migrated together with all its authored call sites, in one
change.

The same rule governs functor application in prose mathematics: a
functor applied to a morphism is written as application, $T(k)$ and
$S(h)$, not by juxtaposition $Tk$, $Sh$, which the reader parses as a
product or a two-letter symbol. And a semantic macro with no operand
at all — `\radic` standing alone in "$G_2\ \text{splits as}\
\radic\perp\langle-2\rangle$" — is a fragment of the same kind: the
construction has an operand, the radical of a specific form, and the
source does not record it.

Observed in `dzackgarza/research` (working tree over `ab530c1dcc`):
`research/category-theory/framework/Categorical-Foundations.md`,
definition "Comma categories";
`research/lattice-theory/Lattices-and-Discriminant-Forms.md`, the
example of two degenerate forms given by Gram matrices.

**Banned:** "$f'\circ Tk=Sh\circ f$"; "$$G_2\ \text{splits as}\
\radic\perp\langle-2\rangle,\qquad G_3\ \text{splits as}\
\radic\perp\begin{pmatrix}-2&1\\1&-2\end{pmatrix},$$".

**Preferred:** "$f'\circ T(k)=S(h)\circ f$";
"$(\bZ^2,G_2)\cong\radic{G_2}\perp\langle-2\rangle$ and
$(\bZ^3,G_3)\cong\radic{G_3}\perp A_2(-1)$" — the operand inside the
macro, the splitting written as an isometry between named objects.

## `NOT-8`: Cardinality is not absolute value

Cardinality and scalar magnitude are different mathematical notions
and are notated differently. The cardinality of a set, group, or
module is written $\cardinality{X}$ (or the house's one fixed
cardinality symbol, stated at its defining occurrence); single and
double bars are reserved for absolute value and norms of scalar- or
vector-like elements: $\abs{x}$, $\norm{v}$, $\pnorm{v}{p}$. Writing
$|X|$ or $\abs{X}$ for the number of elements overloads the
absolute-value notation with a different type — a set has no
magnitude — and collides with uses where the same object legitimately
carries both notions: $\abs{g}$ the absolute value of a scalar $g$
versus $\cardinality{G}$ the order of its group, or the underlying-set
bars of `SYM-11`. State which notion by which notation, once, and
keep them distinct (`NOT-3`).

**Banned:** $|L|$ for the number of elements of a lattice or
$\abs{M}$ for the number of elements of a module (write
$\cardinality{M}$); "$\abs{G}<\infty$" where the claim is that $G$ is
a finite group.

**Preferred:** $\cardinality{L}$, $\cardinality{D_L}$,
$\cardinality{G}$ for counts; $\abs{d_L}$ for the absolute value of
the discriminant integer; the set-theoretic corollary spelled
"therefore $\cardinality{M}<\infty$" (`TERM-17`).

## `NOT-9`: House delimiter macros, not manual sizing

Authored mathematics is written through the house delimiter API —
`\qty{…}`, `\bqty{…}`, `\Bqty{…}`, `\abs{…}` — and not through
hand-sized `\bigl(…\bigr)`, `\left(…\right)`, or raw `|…|`. The
macros are the semantic record: `\qty` says "this parenthesis is a
parenthesized argument", `\abs` says "these bars are a magnitude"
(`NOT-8`), and each renders with the automatic sizing the house
settled, so two authors cannot drift apart on the same expression.
Manual `\bigl`/`\Bigl` choices are per-site typography that encodes
no mathematics and breaks under edit; raw delimiter primitives
reappear in the source as noise the reader must parse. Raw bars are
the special case of `NOT-8`: `$|v|$` in source is indistinguishable
from a magnitude after editing; `\abs{v}` survives it.

**Banned:** `\bigl( b^\sharp \bigr)^{-1}` in authored prose;
`$\left| \det(G_e(b)) \right|$` where the house writes
`$\abs{\det(G_e(b))}$`; a document mixing `\qty{}` and `\left(
… \right)` for the same parenthesization.

**Preferred:** `\qty{b^\sharp}^{-1}`;
`\abs{\det(G_e(b))}`; `\bqty{0,1}`; the house macro at every
delimiter that carries mathematical structure, with manual sizing
reserved for genuine typographic fixes inside macro *definitions*.

## `NOT-10`: A map is named only where later mathematics uses the name

A symbol for a map, object, or set is introduced when a later sentence,
display, proof, or block refers to it. A map that occurs once is
written as an arrow or a formula at that occurrence. A map whose only
later use is a sentence restating its type has no later use (`PR-76`).
Subscripted names for a family of forgetful or inclusion maps —
$j_{L,M}$, $U_{L,M}$ — index nothing unless the family is quantified
over later. Naming is bookkeeping, and bookkeeping that nothing reads
is deleted. `NOT-5` governs aliases for objects that already have a
name; this rule governs names for objects that need none.

Observed in `dzackgarza/research`,
`research/lattice-theory/Isometries-and-Arithmetic-Invariants.md`
(working tree over `26d4e303bc`), proposition "Lattice morphisms are
monomorphisms".

**Banned:** displaying
"$j_{L,M}\colon\operatorname{PrimEmb}(L,M)\injects\Hom_{\mathbf{Lat}_R}(L,M)$,
$U_{L,M}\colon\Hom_{\mathbf{Lat}_R}(L,M)\injects\Hom_{R\text{-}\mathbf{Mod}}(UL,UM)$"
when the only later occurrence of either name is "faithfulness of the
forgetful functor gives the monomorphism $U_{L,M}$, while $j_{L,M}$ is
the defining inclusion of the primitive-embedding subobject".

**Preferred:** nothing, when $\operatorname{PrimEmb}(L,M)$ is defined as
a subset of $\Hom_{\mathbf{Lat}_R}(L,M)$ and faithfulness of $U$ is
stated at $U$'s definition; otherwise the one sentence that states the
fact the later text uses, with no symbol attached.

## `NOT-11`: A graded functor is used as the functor, not by extracted components

Homotopy groups $\pi_*$, homology $H_*$, the terms of a long exact
sequence, a family indexed by the places of a field: each is one
functor to a graded or indexed category, and the statement that uses
it is a statement about the functor — the long exact sequence of
$\pi_*$ for a fiber sequence [@May99, Ch. 9], the family as one adelic
object (`DEF-46`). Extracting components — $\pi_0$ and $\pi_1$ listed,
a four-term fragment displayed — and then stating what the extracted
components fail to determine is a truncation followed by a negative
(`PR-36`): the reader is told that the fiber of $\pi_0(E)\to\pi_0(B)$
"need not equal" $\pi_0(F)$, where the long exact sequence states what
it is, the orbit set of $\pi_0(F)$ under $\pi_1(B,b)$. The components
are written when the argument reads one of them off; the functor is
written when the statement is about the sequence.

Observed in `dzackgarza/research`,
`research/category-theory/framework/Categorical-Foundations.md`
(working tree over `ab530c1dcc`), the paragraph on fiber sequences and
$\pi_0$ in the groupoid material.

**Banned:** "For a fiber sequence $F\to E\to B$, the associated exact
sequence of pointed sets contains
$$\pi_1(B,b)\too\pi_0(F)\too\pi_0(E)\too\pi_0(B).$$ Consequently, the
fiber of $\pi_0(E)\to\pi_0(B)$ need not equal $\pi_0(F)$ [@May99]."

**Preferred:** "A fiber sequence $F\to E\to B$ has a long exact
sequence
$$\cdots\to\pi_1(E,e)\to\pi_1(B,b)\to\pi_0(F)\to\pi_0(E)\to\pi_0(B)$$
[@May99, Ch. 9]; exactness at $\pi_0(F)$ is the statement that the
fiber of $\pi_0(E)\to\pi_0(B)$ over the base point is
$\pi_0(F)/\pi_1(B,b)$, the orbit set of the connecting action."
