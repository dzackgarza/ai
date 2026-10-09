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
($\operatorname{coker}(f)$, with the property the theorem imposes on
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

## `EV-11`: A relationship phrase asserts nothing until the map is written

"Identifies with", "agree canonically", "is canonically isomorphic to",
"the symmetry isomorphism", "the canonical map", "differs from", and
"there is a decomposition $G\cong N\rtimes H$" sound like mathematics
and assert nothing checkable: the reader cannot tell which map is
meant, cannot verify it, and cannot cite it. The negative phrase is the
same defect: "this differs from $Y$" owes the statement of what $X$ is
in terms of $Y$, or the invariant that separates them. Each is owed a specific object — the map
with source, target, and formula; the equation between two named maps;
or the exact sequence with its section. A definite article on a map is
the tell: "the symmetry isomorphism" of a fourfold tensor product names
a family of permutations, not one map. A decomposition claim is a
construction: $G\cong N\rtimes H$ owes the normal subgroup, the quotient
map, the section, and the action (`STR-6`, `DEF-40`); where only
existence is proved, write "the sequence $1\to N\to G\to H\to1$ splits"
and cite the proof. "The map factors through the kernel" owes the lift
$\bar f\colon X\to\ker(g)$ with $k\circ\bar f=f$, drawn as the triangle
when the lift is what the argument uses (`DIA-7`). "Canonical" after a
choice — of a section, a representative, a basis — owes the statement
that the result is independent of the choice, or the dependence kept
explicit in the notation. "Unique up to isometry" owes the uniqueness
it asserts: between which two objects, which isometry, compatible with
which maps; where no two objects are compared, the phrase is deleted and
the object is named (`DEF-32`). `MA-1` governs the related substitution
of $=$ for a constructed isomorphism.

Observed in `dzackgarza/research`:
`research/category-theory/framework/Bilinear-and-Quadratic-Forms.md`
(working tree over `26d4e303bc`), the tensor product of forms;
`research/dissertation/sections/1-part-combinatorial/2-chapter-lattice-theory/700-folding.md`
at `26d4e303bc`, "Examples of Classical Foldings";
`research/dissertation/sections/1-part-combinatorial/2-chapter-lattice-theory/200-examples.md`
(working tree over `2b758e124b`), "Type $D$";
`src/dzack_research/preamble/categories/modules/framed/formed/discriminant_modules.py`
at `76d4ef22ae`, the docstring of `has_same_image_as`.

**Banned:** "after the symmetry isomorphism carrying
$(M\tensor_RN)^{\tensor2}$ to $M\tensor_RM\tensor_RN\tensor_RN$"; "there
is a decomposition $\Orth(L)\cong W(L)\semidirect P$ where
$P\leq\Sym(G_{\Phi(L)})$ is some subgroup of diagram symmetries"; "the
two constructions agree canonically"; "$A$ identifies with $B$"; "the
lattice $dL:=\{d\cdot v\mid v\in L\}$, noting that this differs from
the twist $L(d)$"; "a subgroup of the same discriminant module with the
same image" — "same" for two subobjects names neither the equation of
images nor the isomorphism over $A$ that witnesses it.

**Preferred:**
"$\sigma\colon(M\otimes_RN)^{\otimes2}\xrightarrow{\sim}M^{\otimes2}\otimes_RN^{\otimes2}$,
$x\otimes u\otimes y\otimes v\mapsto x\otimes y\otimes u\otimes v$, and
$b_M\otimes b_N:=(b_M\otimes b_N)\circ\sigma$"; for a root lattice
$L=\langle\Phi\rangle$: "fix a base $\Delta\subseteq\Phi$; the
stabilizer $\operatorname{Stab}_{\Orth(L)}(\Delta)$ maps isomorphically
onto the automorphism group of the Dynkin diagram of $\Delta$ and splits
$1\to W(L)\to\Orth(L)\to\Orth(L)/W(L)\to1$, so
$\Orth(L)=W(L)\rtimes\operatorname{Stab}_{\Orth(L)}(\Delta)$
[Humphreys, *Introduction to Lie Algebras and Representation Theory*,
§12.2]"; "$dL=\operatorname{im}(d\cdot\colon L\to L)$, and
$x\mapsto dx$ is an isometry $L(d^2)\xrightarrow{\sim}dL$" — the
relation to the twist stated as the map that realizes it; "two
subobjects $\iota\colon H\hookrightarrow A$ and
$\iota'\colon H'\hookrightarrow A$ are equal when
$\operatorname{im}(\iota)=\operatorname{im}(\iota')$, equivalently when
there is an isomorphism $\varphi\colon H\xrightarrow{\sim}H'$ with
$\iota'\circ\varphi=\iota$"; the comparison morphism
$\theta\colon A\to B$ with its formula and the statement that it is an
isomorphism (`DIA-7`, `PR-74`).

"Agree canonically" for two constructions defined on different sides
— the left and right orthogonal complements of a symmetric form — owes
the inducing map and the proof: for $b\circ\tau=b$ the swap $\tau$
induces an isomorphism between the two kernels over $M$, and that map
is the content. "Identifies $A$ with $B$" and "the geometric
identification of" are the same phrase with the map in a different
grammatical slot.

Observed in `dzackgarza/research`:
`research/category-theory/framework/Bilinear-and-Quadratic-Forms.md`
(working tree over `57c8eb1cb0`), definition "Left and right
orthogonal complements";
`research/lattice-theory/embeddings/orthogonal-complements.md`
(working tree over `57c8eb1cb0`), proposition "Primitive isotropic
complements";
`research/lattice-theory/special-lattices-and-transformations.md` at
`ab530c1dcc`, proof under "The scaled hyperbolic plane $U(2)$".

**Banned:** "For a symmetric bilinear module over the commutative base
ring $R$, the two kernel objects agree canonically."; "The morphism
$\lambda_v$ identifies $\generators{v}_{\bZ}$ with"; "geometric
identification of".

**Preferred:** "for $b\circ\tau=b$, the swap $\tau$ induces the
isomorphism ${}^{\perp_b}T\isoto T^{\perp_b}$ over $M$", with its
square drawn (`DIA-7`);
"$\lambda_v\colon\langle v\rangle_\bZ\injects v^{\perp_L}$ is the
unique morphism with $\kappa_v\circ\lambda_v=\iota_v$"; the map named.

"Canonical" asserts a universal property — a (co)limit, a unique
isomorphism, an adjunction — and written without that proof it asserts
nothing while hiding the map that does the work. "Coincide", "are the
same", and "are isomorphic" for two constructions are the same defect
with the map hidden, and as equalities they are usually false: two
constructions that differ by a symmetry of the ambient structure are
related by the isomorphism that symmetry induces, and that isomorphism
is the content. "Factors through" is deleted at every occurrence: it
gestures at a lift in a diagram the text has not drawn, and the lift
with its commuting triangle is written instead (`DIA-7`). A block whose
only content is such a phrase — one named map called canonical — is a
diagram, not a definition, and a sentence about that map's injectivity
or surjectivity is its exact sequence with the vanishing term named
(`DEF-40`, `DEF-39`).

Observed in `dzackgarza/research`:
`research/category-theory/framework/Bilinear-and-Quadratic-Forms.md`
(working tree over `57c8eb1cb0`), definitions "Adjoints, radicals, and
nondegeneracy" and "Left and right orthogonal complements";
`research/lattice-theory/Lattices-and-Discriminant-Forms.md` at
`ab530c1dcc`, definition "The canonical map to the dual lattice", at
`57c8eb1cb0`, definition "The canonical bilinear-module map to the
dual lattice", and (working tree over `57c8eb1cb0`), the definition
of $I$-integrality;
`research/category-theory/framework/Categorical-Foundations.md` at
`ab530c1dcc`, definition "Concrete categories".

**Banned:** "If $b$ is symmetric, $b^\sharp={}^\sharp b$, so the two
exact sequences are the same"; "Equivalently, $\iota$ factors through
both orthogonal-complement kernel morphisms."; "The lattice is
**$I$-integral** when $$L\too L_K$$ factors through
$L^{\# I}\too L_K$."; "the least positive integer for which
multiplication by $N_b(L)$ on $L^\#$ factors through
$$\iota_L\colon L\injects L^\#.$$"; "the *canonical map to the dual
lattice* is the morphism $$\iota_L\colon L\too L^{\#}$$" … "The
morphism $\iota_L$ is injective, so it is an isomorphism exactly when
$A_L=0$"; "Any further underlying-set construction is stated as a
factorization through this functor."

**Preferred:** "for $b\circ\tau=b$, the swap $\tau$ induces an
isomorphism between the kernel sequences of $b^\sharp$ and
${}^\sharp b$", with its square drawn; the lift
$\bar\iota\colon N\to T^{\perp}$ with $\kappa\circ\bar\iota=\iota$ as
a triangle; "$L$ is **$I$-integral** when there is
$\bar\jmath\colon L\to L^{\#I}$ with $\kappa_I\circ\bar\jmath=\jmath$",
the triangle drawn for $\jmath\colon L\injects L_K$ and
$\kappa_I\colon L^{\#I}\injects L_K$; "$N_b(L)\definedas\exp(A_L)$"
(`DEF-40`); the sequence
$0\to L\xrightarrow{\iota_L}L^\#\to A_L\to0$ displayed where the block
stood, with "$\iota_L$ is an isomorphism exactly when $A_L=0$" as the
sentence after it.
