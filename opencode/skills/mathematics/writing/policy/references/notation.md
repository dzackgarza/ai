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

## `NOT-2`: Typed equality symbols

Literal equality ($=$), isomorphism ($\cong$), and equivalence ($\simeq$) are
written with distinct symbols. An isomorphism is not written as an
equality. $\hookrightarrow$ denotes a stated inclusion,
embedding, or monomorphism; fullness, faithfulness, and repleteness are
asserted separately. Strict pullbacks and pseudo-pullbacks are not identified
by notation.

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
defined once and used once.

**Preferred:** $M(2)$, $\Orth(L)$, $L^{\mathrm{prim}}[n]$ written out at
each occurrence — the construction stays visible and linked to its owner.

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
form" re-defined locally in one chapter and cited from another.

**Preferred:** one defining occurrence per construction, one macro or
symbol reused everywhere, every use linked (`DEF-26`, `NOT-3`,
`SEC-12`).

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
