# Evasion (`EV-*`)

Prose that substitutes for mathematical work not done. The tell is stylistic;
the defect is that a definition was not written or an object not named. The
remediation is never a nicer phrase — it is the work.

## `EV-1`: Vibe-adjectives for a definition

Impressive qualifiers replace the definition itself.

**Banned:** "The subcategory is structurally complete under sameness."

**Preferred:** write the definition — "A full subcategory
$\mathcal D \subseteq \mathcal C$ is *replete* if every object of
$\mathcal C$ isomorphic to an object of $\mathcal D$ belongs to
$\mathcal D$." "Structurally complete under sameness" is a mood; the
definition is the work.

## `EV-2`: Carrier / "carries"

"carries" and "carrier" suppress the data that constitute a structure.

**Banned:** "objects that carry both structures"; "an object together with a
carried structure"; "the underlying set carries the operation."

**Preferred:** name the operations, relations, and axioms, or specify the
forgetful functor and the chosen object in its fiber. A structure on $X$ is a
chosen object in the fiber over $X$ of a specified forgetful functor
$U\colon \mathcal S\to\mathcal C$; the underlying set is the value $U(X)$.

## `EV-3`: Engineering collective nouns

"package", "frame", "pipeline", "suite", "layer", and a vague "slice" gather
mathematical objects under a process or software noun instead of naming them.

**Banned:** "the discriminant package"; "the forms frame"; "the equality
slice".

**Preferred:** "the discriminant construction and its exact sequences"; "the
categories $\mathcal B_{R,W}$ and $\mathcal Q_{R,W}$"; the exact chapter,
section, or mathematical construction meant.

## `EV-4`: Vague hedges for precision

**Banned:** "essentially", "basically", "morally", "roughly", "in some sense"
used where an exact statement is owed.

**Preferred:** state it exactly, or, if a genuine approximation is meant,
name the sense ("up to isomorphism", "to first order").

## `EV-5`: Universal construction left in prose

A construction defined by a pullback, pushout, or another universal square is
abbreviated as "obtained by pulling back" or an equivalent prose instruction.

**Banned:** "Define $E\to X$ by pulling back $p\colon U\to B$ along
$f\colon X\to B$."

**Preferred:** draw the actual commutative square, label every morphism, mark
it cartesian or cocartesian, and name the resulting object and structure
morphism in the diagram. The prose may state the universal property after
the diagram; it never replaces the diagram.

## `EV-6`: "Data" for a mathematical object

A construction operates on objects, morphisms, 2-cells, or elements of a
specified category. "Data" names none of them; it is a programmer's
abstraction standing where a mathematical object belongs.

**Banned:** "a construction that transports data along $\alpha$, $\lambda$,
or $\varrho$."

**Preferred:** name the things the construction operates on — "a construction
that composes a cell with $\alpha$, $\lambda$, or $\varrho$." The word "data"
erases the type; the replacement names it.

## `EV-7`: Metaphor for an unnamed operation

A sentence says something "transports", "carries", "flows", or "moves" along
a map or cell without naming the categorical operation — composition,
whiskering, application, base change, conjugation — that performs it.

**Banned:** "transports data along $\alpha$."

**Preferred:** name the operation — "composes with $\alpha$", "applies
$\alpha$ to the cell", "whiskers $\alpha$ against $F$." The metaphor hides
which operation; the replacement states it.

## `EV-8`: Universal property invoked but not stated

A sentence appeals to "the projections", "the universal property", or "the
unique map" without stating which universal property, from which object, to
which target. The uniqueness is real, but the reader cannot verify it
without the property identified.

**Banned:** "the three isomorphisms being the unique ones commuting with the
projections."

**Preferred:** "the associator $\alpha_{a,b,c}$ and the unitors
$\lambda_a$, $\varrho_a$ are the unique isomorphisms supplied by the
universal property of the product." Name the universal property and the
object that supplies it.

## `EV-9`: An exact sequence at the theorem's strength, not a convenient truncation

A theorem supplies structure — a factorization, a group, a functor, a
quotient with meaning beyond its bare existence. Do not replace it by an
ad hoc short exact sequence merely because some image makes one
formally available, and do not compress a theory to the fragment a
local computation needs. Name the object the theorem actually produces
($Q_f$ as the cokernel of $f$, with the property the theorem imposes on
it), and state the surrounding structure — the epi–mono factorization,
the kernel, the invariant the theorem computes — at the strength the
source proves. An injectivity claim after base change comes from the
kernel/exactness statement, not from prose about it.

The type case is the discriminant representation: a short exact
sequence on an image $I_L$ does not stand in for Miranda–Morrison
theory. Preserve the mathematically meaningful objects — $\rho_L$, the
epi–mono factorization through $I_L$, and the genus invariant $g(L)$ —
and cite the source theorem; do not truncate it to a sequence that
carries less information.

**Banned:** "there is a short exact sequence
$1\to K\to\Orth(L)\to I_L\to 1$" presented as the theorem when the
source proves a factorization with further structure; "the sequence
shows injectivity after base change" with no kernel named; "there is a
short exact sequence" for an object ($Q_f$) never defined as a
cokernel.

**Preferred:** "$\rho_L\colon\Orth(L)\to\operatorname{Aut}(D_L)$ is the
discriminant representation; it factors as an epi–mono factorization
$\Orth(L)\twoheadrightarrow I_L\hookrightarrow\operatorname{Aut}(D_L)$
([@MM99, Theorem 4.2]), and the quotient $g(L):=I_L/\rho_L(\Orth(L))$
is the genus invariant" — the theorem's structure, stated at its
strength, with the citation at the claim (`CITE-4`).

## `EV-10`: A computational surrogate for the structural statement

When the claimed mathematical object has a direct structural
description — a diagonalization, a maximal definite subspace, a
canonical decomposition, an invariant — a calculation does not stand
in for it. An eigenvalue computation proves a numerical consequence of
diagonalization; it does not exhibit the decomposition, the subspace,
or the isometry the statement is about. Prove the structural statement
directly; state the calculation as its evaluation in the concrete case.
The surrogate is the same defect as `EV-9` one level down: a theorem
truncated to the fragment a local computation can reach.

**Banned:** an eigenvalue computation of $G_e(b)$ presented as the
proof that a form is definite, with no maximal definite subspace or
diagonalization named; a determinant calculation standing in for the
statement that $b^{\sharp}$ is an isomorphism (`DEF-39`).

**Preferred:** the structural proof — the orthogonal decomposition
$V\cong P\perp Q\perp\operatorname{rad}(V)$ with $b_{|P}>0$, or
$G_e(b)\cong\operatorname{diag}(1^p,-1^q,0^r)$ via an exhibited
isometry (`PR-69`) — with the eigenvalue computation, if kept, as a
verification of the exhibited structure.
