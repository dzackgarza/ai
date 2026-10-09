# Recurring patterns

The universal themes seen in slop writing, based on this session and the
contributing document, are:

**1. Truncated ontology where the modern is derived/spectral.** Rings for
$\mathbb{E}_\infty$-ring spectra, modules for module spectra, categories
for $\infty$-categories, $K_0$ as group completion for $\pi_0 K(S)$, $K_0$
as a ring for $K(S)$ as an $\mathbb{E}_\infty$-ring spectrum (DEF-10,
DEF-13, DEF-8, DEF-9, DEF-14, SEC-6). Anchoring in a superseded framework
(1970s group completion vs $S_\bullet$ and Zakharevich/Campbell) and
working truncated without marking $\pi_0 HR$ or $H(\pi_0R)$.

**2. Prose paraphrase of a precise categorical statement** (PR-15 general
pattern). Vague English — "is an invariant of isomorphism classes," "is
functorial for …," "relating $\gamma$ to $\alpha$," "commuting with the
projections," "is what licenses $a_1\otimes\cdots\otimes a_n$," "is
additional data / does not follow from notation" — for a precise
factorization through $\pi_0$, a functor
$\mathbf{SymMonCat}\to\mathbf{Spectra}$, a hexagon diagram, a tuple
$(\mathcal{C},\otimes,\mathbf{1},\alpha,\lambda,\varrho)$, or a moduli of
equivalences ($\mathbf{LMod}_R\simeq\mathbf{RMod}_R$ as an invertible
bimodule). Wordier and less precise than the statement; names no domain,
codomain, or diagram.

**3. Binding, scoping, and notation.** Symbols used without being bound —
stating a type "symmetric monoidal category" does not bind $\otimes$; the
tuple does (SYM-1, SEC header). Overloaded $1$ for terminal object and
$\operatorname{id}$, maps without $\operatorname{dom}/\operatorname{cod}$,
symbols introduced after use in a "where" clause, $R^{(I)}$ invented
without the free functor $F\colon\mathbf{Sets}\to\mathbf{LMod}_R$
($F(I)=\bigoplus_I R$, not $R^I$), inconsistent
$A\text{-}\mathbf{Mod}$ vs $B^{\mathrm{op}}\text{-}\mathbf{Mod}$, and
strict $A=A^{\mathrm{op}}$ for the canonical $A\simeq A^{\mathrm{op}}$
of tuples (SYM-4–11, SYM-13, DEF-23, SYM-12 for $\otimes_A$ vs
$\otimes_A^L$, MA-14 for $M\times M\to W$ "bilinear" vs $M\otimes_A M\to
W$).

**4. Structural and scaffolding failures.** One block for many notions with
mixed logical status — unconditional replete full subcategories,
integral-domain-conditional torsion, and a meta-remark about general
rings — instead of one notion per fenced block (DEF-15, DEF-19, DEF-1);
reminder masquerading as definition that merely assigns notation
$A\text{-}\mathbf{Mod}$ without constructing $\mathbf{LMod}_R$ (DEF-17);
category defined pointwise by objects $(M,e)$ and
$\operatorname{Bas}_I(M)$ without morphisms or forgetful functors to
$\mathbf{LMod}_R/\mathbf{Sets}$ (DEF-25); missing scaffolding — free
functor before basis, generating family before freeness,
$\operatorname{Ann}_R(m)$ before torsion (DEF-23, MA-15); sections with no
fenced unit, arbitrary breaking that inverts dependency, and sections
that are entirely remarks with no primary unit to remark on (SEC-1–7).
The skeleton — fenced units with proofs — must be complete after deleting
glue; remarks are secondary pedagogy.

**5. Terminological slippage and characterization as definition.** Coinage
with no referent — "value module," "torsion theory," "homomorphism" for
"morphism/map in $\mathbf{CAlg}$," "carries," "data," "identifies
conventions" (TERM-2–4, EV-6, PR-20); compound terms by bullet order
("finitely generated projective: both conditions hold," DEF-21); "some
$R^n\twoheadrightarrow M$ is surjective" for $\exists$ (PR-22);
presenting a characteristic equivalence as the definition — projective as
direct summand of free instead of the lifting property, with
"$\text{direct summand iff projective}$" as a theorem (DEF-22).

**6. Rhetorical slop.** Manufactured negative parallelism — "their mere
existence supplies no order relation," "$a=b$ is a theorem, never a
definitional identity" (PR-2) — contentless because existence never
supplies structure unless defined, and patronizing strawman negation —
"does not follow merely from notation," "is additional data" negating a
premise no one held, with corrective dialectic for an audience that
already distinguishes $\mathbb{E}_1$ from $\mathbb{E}_\infty$ and
$\mathbf{LMod}_R$ from $\mathbf{RMod}_R$ (PR-16–18).

**7. Specialization with no new claim, and meta-requirement for a
theorem.** A general construction $B\otimes_A^L-$ already defined; its
specialization at $\mathbb Z\to\mathbb Z_p$ with no new definition,
theorem, or computation restates the definiens on objects and contributes
no fenced unit (SEC-8). Likewise, "a conclusion about $L$ from either
image requires a stated descent theorem with its hypotheses" says a
theorem must exist instead of stating it, with unquantified "a
conclusion" / "either image" and no hypothesis list (PR-28, PR-29); the
correct form states fpqc descent / Beauville–Laszlo with faithfully flat
/ finitely presented hypotheses, then applies it — and notes that one
image alone never suffices, only the compatible pair with gluing.

**8. Indefinite referent, tautological qualifier, and doctrine posing as
content.** "A conclusion" with no proposition is unfalsifiable (PR-30);
"with its hypotheses" is true of every theorem and adds no hypothesis
list, so it does no work (PR-31); together they are internal governance
leaking into the document — runtime control whose only coherent audience is
contributors/agents, not the mathematical reader, with a preemptive,
condescending tone that assumes the reader was about to make a mistake
never committed (PR-32). Standard prose states the theorem with
hypotheses and applies it; it does not tell the reader that a theorem is
required. Governance belongs in the writing policy, not in the
mathematical text (cf. PR-24, PR-16–18).

**9. "Are distinct constructions" tautology and "without $H$" vacuity.**
Two functors defined differently are distinct by definition, with or
without any hypothesis; the substantive claim is whether the canonical
comparison map $c_M\colon M\otimes^L_{\mathbb Z}\mathbb Z_p\to\widehat M_p$ is an
equivalence (PR-33). "Without the finite-generation hypothesis, $A$ and
$B$ are distinct" is true of every theorem $H\Rightarrow A\simeq B$ and
says nothing, with unquantified $H$ (finitely generated vs. presented
vs. perfect) and no map or counterexample (PR-34, PR-33). State the
quantified theorem ($c_M$ an iso for perfect $M$) and the quantified
failure with a counterexample ($\bigoplus_{\mathbb N}\mathbb Z$,
$\mathbb Q$), not that the definitions are distinct. Once the distinct
definitions and the positive theorem are stated, the complement without
$H$ is implicit and obvious and needs no separate sentence (PR-35).

**10. Negative framing as bloat, tone, and structural defect.** Every
"is not," "does not follow," "without $H$ distinct," "requires a
theorem with hypotheses," "mere existence supplies no …" is a negative
standing for a positive Definition/Theorem not stated (PR-36, general
form of PR-2, PR-16–18, PR-24, PR-28, PR-30–35, SEC-8). Each doubles the
text (infinitely many true negatives per positive theorem), assumes a
reader mistake never made and scolds preemptively instead of addressing
an equal, and contributes no fenced unit with a named map and quantified
$H$ — hiding that the actual proof obligation was not met. Standard
exposition is positive: definitions as tuples, theorems as quantified
implications with the comparison map, proofs, then boundary
counterexamples when they teach.

**11. Sign-posting that fixes variables for "below."** "Fix $R$ and $W$,
the value module of the forms below" is not a unit; it holds variables
outside any fenced Definition and forward-references an unspecified
"below," with a single fixed $W$ where $W$ must vary over
$\mathbf{LMod}_R$ as the codomain $b\colon M\otimes_R M\to W$ (PR-37,
TERM-9). Correct is quantified fenced units — "Let $R$ be …, let
$W,M\in\mathbf{LMod}_R$; a $W$-valued bilinear form is
$b\colon M\otimes_R M\to W$" — or a section header that quantifies $R$
once while $W$ varies; the skeleton is then complete after deleting
glue.

**12. Tautological "with pointwise operations" for the canonical
enrichment.** "With pointwise operations" / "with its $R$-module
structure via $W$" does zero work: for commutative $R$,
$\mathbf{Mod}_R$ is closed symmetric monoidal and self-enriched, so
$\operatorname{Hom}_R(M,N)\in\mathbf{Mod}_R$ is the internal hom, full
stop (PR-38); $\operatorname{Bil}_{R,W}(M)=\operatorname{Hom}_R(M\otimes_R
M,W)$ already is the $R$-module. The clause mislocates the structure in
$W$ and restates what the ambient enrichment already gives. Put the
closed structure once as fenced scaffolding in the module-theory setup
and every later "with pointwise operations" is obviated.

**13. Hom notation vs. prose paraphrase, and tensor product as
scaffolding.** "The $R$-module of $R$-bilinear maps $M\times M\to W$,
with pointwise operations" is prose for one symbol that already is that
$R$-module with its structure — $\operatorname{Hom}_R(M\otimes_RM,W)$
(PR-39, PR-27 general form). $R$-bilinear $M\times M\to W$ is not
primitive to re-describe each time; it is classified by $M\otimes_RM$
defined once with its universal property $\operatorname{Hom}_R(M\otimes_R
M,W)\cong R\text{-Bil}(M\times M,W)$, and from then on a $W$-valued
form is just $b\colon M\otimes_RM\to W$ (PR-40). Define the tensor
once, then use homs from the tensor to encode bilinearity implicitly.
Calling the resulting functoriality "defines a presheaf
$\mathbf{Mod}_R^{\mathrm{op}}\to\mathbf{Mod}_R$" overloads the generic
name for $\mathbf{Mod}_R^{\mathrm{op}}\to\mathbf{Set}$ and adds no
content beyond "functor" — name the enrichment when needed as
$\mathbf{Mod}_R$-valued / $\mathbf{Mod}_R$-enriched presheaf (TERM-10).

**14. Bare "maps $M\to W$" with no category.** "Maps $q\colon M\to W$"
unqualified in $\mathbf{Mod}_R$ means $R$-linear; a quadratic $q$ is not
$R$-linear — it is a function $U(M)\to U(W)$ in $\mathbf{Set}$ for the
forgetful $U\colon\mathbf{Mod}_R\to\mathbf{Set}$ (TERM-11). The
classifier $\Gamma^2_R$ already gives $\operatorname{Quad}_{R,W}(M):=
\operatorname{Hom}_R(\Gamma^2_R(M),W)$ as $R$-module; never write bare
"maps $M\to W$" or "$M\times M\to W$" once $\otimes$, $\operatorname{Sym}^2$,
$\Gamma^2$ classify the flavour. Name $\mathbf{Set}$ / $U$ when the map
is not $R$-linear.

**15. "Pullback defines a presheaf" type error and hand-waving functor
data.** Pullback is a limit / slice functor, presheaf is
$\mathcal C^{\mathrm{op}}\to\mathbf{Set}$ — types do not match, and one
$f^*b(x,y)=b(fx,fy)$ does not define a functor (PR-41). Every functor
owes on objects with type, on morphisms $(f\colon M\to N)\mapsto
(f\otimes_R f)^*\colon\operatorname{Bil}(N)\to\operatorname{Bil}(M)$ with
domain/codomain, element unwrapping if useful, and
$\mathrm{id}^*/(g\circ f)^*$ — not "defines a presheaf" with only an
element formula (PR-42). Unwrapping $f^*b(x,y)=b(fx,fy)$ *after* the
Hom is pedagogically fine; the incoherence is claiming that formula
defines the presheaf.

**16. Element-wise $b(x,y)=b(y,x)$ for $b\circ\tau=b$ — concrete shadow
for the categorical diagram.** $b(x,y)=b(y,x)$, $b(x,x)=0$, $q(rx)=r^2q(x)$
as definitions tie the notion to $\mathbf{Set}$-concrete $M$ with
$U(M)$ and hide the single non-lax symmetric monoidal
$(\otimes,1,\tau)$ that makes it portable (PR-43). Standard is the
diagram $b\colon M\otimes_RM\to W$, $b\circ\tau=b$ / $b\circ\tau=-b$ /
$b\circ\Delta=0$ / lift through $\Gamma^2_R(M)$, with element formulas
only as the evaluation on $x\otimes y\colon R\to M\otimes_R M$ when $U$
exists. "$b$ is even if $b(x,x)\in2W$" collapses the $W$-parameter
abstraction just built for $W$-valued forms to $U(W)$ and "$\in2W$"
(PR-44); even is the lift through $\Gamma^2_R(M)$, and carrying
$b(x,x)\in2W$ everywhere instead of naming $\operatorname{Val}(b)\subseteq
W$ once is local thinking for a global object (PR-45). In general "for
every $x$, a choice of …" is the unwrapping of one global functor /
bundle / section / natural transformation / $R$-submodule; name it once
and "for every $x$" is its evaluation on $U$-points (PR-46). Quantifying
$\forall x\in M$ in the *definition* presupposes $U\colon\mathcal
C\to\mathbf{Set}$ and blocks the one general concept from applying to
$\mathcal O_X\text{-}\mathbf{Mod}$, $\mathbf{Sp}$, stacks, etc., where
no such $U(M)$ exists (PR-47) — the diagram $b\circ\tau=b$ works in every
symmetric monoidal $\mathcal C$, the element formula only in the concrete
ones. A definition is not the minimal element condition that lets the next
paragraph proceed; it is the general building block — $b^{\sharp}$,
$\ker(b^{\sharp})$, $\ker(b\circ\Delta)=0$ — that later theory
($N^{\perp}$, isotropic, anisotropic, $M^\vee$, $D_L$) reuses in every
$\mathcal C$ (PR-53), and that long-term applicability must be written
down or no agent will know it (PR-54).

**17. Mixing Lemma/Proposition into the Definition and not naming the
subobjects and the map $2_*$ between them.** "Alternating $\Rightarrow$
skew" is a Lemma
$\operatorname{AltBil}\subseteq\operatorname{SkewBil}$ as $R$-submodules,
and "converse when $2$ injective" / "when $2W=W$ every $b$ even" is a
Proposition about $2_*\colon\operatorname{Bil}\to\operatorname{Bil}$
induced by $2\colon W\to W$ and its obstruction (PR-48); neither belongs
in the Definition block, which is atomic — one definition per fenced
block, rarely a tightly related family, never a Lemma/Proposition/Remark
(PR-64). Pithy prose avoids naming
$\operatorname{SymBil}$, $\operatorname{SkewBil}$, $\operatorname{AltBil}$,
$\operatorname{EvBil}$ and $2_*$ between named $R$-submodules of
$\operatorname{Bil}_{R,W}(M):=\operatorname{Hom}_R(M\otimes_R M,W)$, and
restates $b\colon M\times M\to W$ instead of $b\in\operatorname{Bil}$
(PR-49) — definitions as objects and containments, not signatures and
element formulas.

**29. Free-floating Remark with a calculation but no claim has no
epistemic status and is not self-contained.** "`**Remark.**` The symmetric
form on $\mathbb Z^2$ with Gram matrix $\begin{pmatrix}0&1\\1&0\end{pmatrix}$
has vanishing diagonal and $b(e_1+e_2,e_1+e_2)=2$" gives $G_e(b)$ and two
equalities but states no quantified universal it exemplifies — not
"$\exists b$ symmetric with $G_{ii}=0$ but $b\notin\operatorname{AltBil}$"
(PR-65). It is not a Definition, Lemma, or Example, contributes no
fenced unit to the skeleton, and is not self-contained (does not say what
it is an example *of* or what the calculation shows). Standard is a fenced,
labelled `Example` that names $((\mathbb Z^2,e),b)$ and $G_e(b)$, states
"vanishing on a basis does not imply $b\circ\Delta=0$," and shows
$b\notin\operatorname{AltBil}$ via $b\circ\Delta$.

**18. Nominalizing the adjective/verb — "satisfies the evenness
condition."** "Even" is an adjective ($b$ is even,
$b\in\operatorname{EvBil}$); nominalizing to "evenness" + "condition" +
"satisfies" makes one predicate three words with no named subobject to
check (PR-50). Standard is "is even / injective / exact" / "commutes /
factors," with bad/standard pairs: "satisfies the evenness condition"
$\to$ "is even ($\operatorname{EvBil}=\operatorname{Bil}$)"; "satisfies
injectivity" $\to$ "is injective"; "satisfies exactness" $\to$ "is
exact"; "exhibits commutativity" $\to$ "commutes"; "satisfies the
factorization condition" $\to$ "factors through $\Gamma^2$."

**19. "Quadratic refinements retain additional information in the
discriminant setting."** "Refinement" with no named
$\gamma^*\colon\operatorname{Quad}\to\operatorname{Bil}$ has no defined
relation to check (TERM-12); "retain additional information" names no
$R$-submodule, kernel, fiber, or invariant and is not falsifiable
(PR-51); "in the discriminant setting" is not a mathematical object —
the object is the category $\mathbf{TorBil}_{R,W}$ /
$\mathbf{TorQuad}_{R,W}$ of torsion forms, with discriminant object
$D_L:=L^\vee/L$ (TERM-13) — and sign-posting it in the general
$\operatorname{Bil}/\operatorname{Quad}$ section before lattices and
$L^\vee/L$ exist inverts dependency order and violates theory-of-mind.
All three are the weasel mass-noun pattern (PR-52).

**20. Hygiene and foresight — the Set-shadow vs. the categorical
object.** Every "$b(x,y)=b(y,x)$ / $b(x,x)\in2W$ / $\{x\mid b(x,N)=0\}$ /
$b$ satisfies the evenness condition / pullback defines a presheaf /
retain additional information / $M=N\oplus N^{\perp}$" in the block is
the same failure: the statement on $U$-points $x\colon1\to M$ instead of
on the named object that classifies it — $b^{\sharp}$, $\ker(b^{\sharp})$,
$\ker(b\circ\Delta)$, $\operatorname{Bil}_{R,W}$, $\operatorname{Val}(b)$,
$\Gamma^2_R$, $\perp$ as biproduct in $\mathbf{Bil}_{R,W}$ vs. $\oplus$
in $R\text{-}\mathbf{Mod}$ (PR-55). Locally correct for $\mathbf{Mod}_R$,
it bypasses the adjoint/dual/orthogonal subtheory, avoids one general
building block ($b^{\sharp}$, $\ker$, $\operatorname{Val}$) that later
theory and every non-concrete $\mathcal C$ would reuse, and trades
applicability tomorrow for the minimal sentence that lets this page
proceed — the opposite of long-term hygiene.

**21. Submodules and set quotients $N\subseteq M$, $M/N$ vs. monos and
cokernels $i\colon N\hookrightarrow M$, $\operatorname{coker}(i)$.** "$N\subseteq
M$ be a submodule" is the $U$-shadow of a mono, "$M/N$" of its cokernel;
the elementwise $\bar b([x],[y])=b(x,y)$ re-spells the universal property
of the cokernel on representatives (PR-56). Stated with $i$ and
$\operatorname{coker}(i)$, the induced $W$-valued form $\bar b$ on the
quotient is the unique factorization of $b$ through
$\pi\otimes_R\pi$ for $\pi:=\operatorname{coker}(i)$ when $i^*b=0$ —
immediate in $\mathrm{QCoh}(X)$, $\mathbf{LMod}_R$, $\mathbf{Sp}$, sheaves,
where $N\subseteq M$ has no meaning as a subset.

**22. "$N^{\perp}$" alone is not well-defined.** $N^{\perp}$ depends on
the triple $(M,b,i\colon N\hookrightarrow M)$ — ambient, $W$-valued form,
and mono making $N$ a subobject — not on abstract $N$ (PR-57).
$M=U$ with $N_1:=\mathbb Z e$ vs. $N_2:=\mathbb Z(e+f)$ has
$U(N_1)\cong U(N_2)\cong\mathbb Z$ abstractly but
$N_1^{\perp}=N_1\cong\langle0\rangle$ vs.
$N_2^{\perp}=\mathbb Z(e-f)\cong\langle-2\rangle$; same $N\subseteq
\mathbb Z^2$ has $N^{\perp_{b_1}}\neq N^{\perp_{b_2}}$ for
$b_1\neq b_2$ on the same $M$. Write $N^{\perp_b}$ /
$N^{\perp_i}$ / $(i\colon N\hookrightarrow(M,b))^{\perp}\subseteq M$,
never bare "$N^{\perp}$."

**23. $\operatorname{Gram}(b)$ is not a function of $(M,b)$.** $M$ in
$\mathbf{Bil}_{R,W}$ need not be free and has no distinguished basis, so
no $n\times n$ matrix exists; $\operatorname{Gram}(b)$ as $(b(e_i,e_j))$
is $G_e(b)=e^*b$ for a framed $((M,e),b)$ with ordered basis
$e\colon R^n\xrightarrow{\sim}M$, and without $e$ is well-defined only
up to $\operatorname{GL}_n(R)$-congruence $G_{e'}=P^{\!t}G_eP$ (PR-58,
PR-59). Write $G_e(b)$ and $[G_e(b)]$, never "$\operatorname{Gram}(b)$"
for $(M,b)$.

**24. Choosing data in a construction requires the variance clause or the
category that carries the choice.** Any construction that chooses an
ordered basis $e$, generating set $S$, presentation $F_2\to F_1\to X$,
point $x_0$, trivialization, etc., owes either (A) how the result varies
with the choice — well-defined up to $\operatorname{GL}_n$-congruence /
similarity / conjugacy, with invariants independent of the choice — or
(B) the Grothendieck construction whose objects are $(M,e)$ / $(X,F_1\to X)$
/ $(X,x_0)$ on which the construction is a functor, with well-definedness
as the study of its fibers / $\operatorname{GL}_n$-orbits / sections
(PR-60). Without (A) or (B) the construction is ill-defined and its
dependence on the choice unfalsifiable.

**25. Never overfit to free / finite / finitely generated, never assume
discrete topology / finite support, never conflate a $W$-valued
$(0,2)$-tensor with a matrix.** The block "$M$ free on $E$, $b$ with
values in $R$, $G_{ij}=b(e_i,e_j)$, $b(v,w)=\sum a_iG_{ij}c_j$ finite,
every $(G_{ij})$ arises" is the $W=R$, $M=R^{(I)}$ specialization of
$b\in\mathbf{Bil}_{R,W}(M):=\operatorname{Hom}_R(M\otimes_R M,W)$ as
$W$-valued $(0,2)$-tensor $b_{ij}$ (two down indices, $G_{e'}=P^{\!t}G_eP$
congruence) conflated with a $(1,1)$-tensor $T^i_j$ ($P^{-1}T_eP$
similarity) and with the matrix algebra $M_{I\times I}(W)$ itself
(PR-61). The map $\Phi_e\colon M_{I\times I}(W)\to\operatorname{Hom}_R(M\otimes_R M,W)$
is an isomorphism only for $M=R^{(I)}$ discrete; its kernel/cokernel are
the well-definedness content, and $(L^2(\mathbb R),\int)$ is a valid
$\mathbb R$-valued bilinear $\mathbb R$-module with no finite $G_{ij}$
and no finite $\sum a_iG_{ij}c_j$.

**26. The double sum smuggles a Riesz theorem and the canonical
$\langle v,w\rangle_0$ on $F=R^{(I)}$; the operator form
$b(v,w)=\langle v,Aw\rangle$ is the honest statement.** "$b(v,w)=\sum
a_iG_{ij}c_j$" as definition assumes
$\Phi_e\colon W^{I\times I}\xrightarrow{\sim}\operatorname{Hom}_R(F\otimes_R F,W)$
and hides that $F$ already carries $\langle v,w\rangle_0:=\sum a_ic_i$
($\delta_{ij}$) well-defined only for $a_i,c_i$ finitely supported
discrete; for $\widehat F$ / $L^2$ the sum is infinite and convergence
in $R$'s topology / completion is the content (PR-62). Standard is
"$b(v,w)=\langle v,Aw\rangle$ for a unique $A\colon F\to F$ with $A$
self-adjoint / bounded / Hilbert-Schmidt / Fredholm per the
topological hypotheses" — the double sum is the coordinate expansion of
that single operator evaluation.

**27. One setup must do arithmetic local, geometric global, and analytic
at once.** Overfitting to finite free $W=R$ discrete with $\sum
a_iG_{ij}c_j$ finite defers the extensions that will be needed anyway
(PR-63). Always ask if the statement immediately generalizes to
topological modules/algebras, $\mathrm{QCoh}(X)$ / schemes/stacks /
sheaves where stalks recover the arithmetic, and $L^p$ / Hilbert /
Banach with (partial) differential operators — symplectic manifolds as
the geometric, Grothendieck–Witt as the arithmetic local, Riesz theorems
as the analytic instance of the same $b\colon M\otimes M\to W$ in a
closed symmetric monoidal $\mathcal C$.

**28. Every definition must work in the functional-analytic setting;
finite collapse is a Proposition.** A definition correct for $R^n$ with
finite $G_{ij}$ and $\sum a_iG_{ij}c_j$ need not be correct for
$L^2(\mathbb R)$ / $\mathrm{QCoh}(X)$ where no finite $G_{ij}$ and no
finite sum computes $\int fg$, and bounded $\neq$ symmetric $\neq$
self-adjoint $\neq$ normal thread apart (PR-66). Define diagrammatically
($b\colon M\otimes_R M\to W$, $b^{\sharp}$, $\ker$, $\Gamma^2_R$) so the
statement is valid in every $\mathcal C$; then prove the finite
specialization ($W^{I\times I}\cong\operatorname{Hom}(R^{(I)}\otimes
R^{(I)},W)$, $b(v,w)=\langle v,Aw\rangle$ with $A$ symmetric $\iff$
self-adjoint) as a Proposition with honest hypotheses, not as the
definition. The diagram is preferable because it already is the general
case.

**31. Signature as prose "greatest dimension" vs. hard equations, and
overly restricted $V$ finite-dimensional.** "$p$ is the greatest dimension
of a subspace on which $b$ is positive definite" hand-waves the
orthogonal $V\cong P\perp Q\perp\operatorname{rad}(V)$ and
$G_e(b)\cong\operatorname{diag}(1^p,-1^q,0^r)$ (Sylvester's law) that
makes $p,q,r$ well-defined and isometry-invariant (PR-69). The general
$F$ ordered, $V$ arbitrary, is no harder: $p:=\sup\{\dim U\mid b_{|U}>0\}$,
$q:=\sup\{\dim U\mid b_{|U}<0\}$ in $\mathbf{Card}$ / on
$\mathrm{Gr}(V)$ / $\mathrm{Fl}(V)$, $r:=\dim\operatorname{rad}(V)$,
$(p,q,r)\in\mathbf{Card}^3$ (PR-70); the finite $V$ with "$\max$" and
$p+q+r=n$ is the specialization where the suprema are attained, not the
definition.

**32. Signature is not over $R$; premature specialization to one
ordered $F$ hides the arithmetic scope.** The block as the definition of
signature quietly fixes the document to $F=\mathbb Q$ / $\mathbb R$ (one real
place, $W=F$, $V$ finite-dimensional). In fact $(p,q,r)$ is sound for
$F$ a field (IBN) and defines $GW(F)\to\mathbb Z$, but it is a
specialization: $\operatorname{sig}(L)$ for $L\in\mathbf{Lat}_R$ is
$\operatorname{sig}(L\otimes_R\operatorname{Frac}(R),b_{\operatorname{Frac}(R)})$
when $\operatorname{Frac}(R)$ is ordered at the relevant place, not
$\max\dim_RU$ over $R$; it rules out (correctly) $F=\mathbb F_q$,
$\mathbb C$ where no order exists, and for $R=\mathcal O_K$ it is a
family $(p_\sigma,q_\sigma,r_\sigma)_{\sigma\text{ real}}$ over the real
places $\sigma\colon K\hookrightarrow\mathbb R$, not a single triple.
The local theory belongs over arbitrary Dedekind $R$ ($\mathbb Z$,
$\mathcal O_K$ with $\operatorname{cl}(R)=1$ not assumed, $\mathbb Z_p$,
$\mathbb Q_p$, $\mathbb C_p$, $\mathbb A$) with $b\colon L\otimes_RL\to
W$ $W$-varying — a scope that should be stated explicitly and, when the
$W\neq R$ / $\mathbb Z_p$ / adele form is not yet supplied, recorded as
an open problem outside the document (PR-72).

**32. Always ask if the statement generalizes without much more
difficulty — if not, state the general and recover the special case.**
For every Definition / Proposition, go through all permutations of its
hypotheses ("finite $\to$ arbitrary," "$W=R$ $\to$ $W$ varying," "free
$M=R^{(I)}$ $\to$ $M$ arbitrary," "discrete / finite support $\to$
topological / $L^2$-convergent," "$2$ invertible $\to$ general $R$")
and ask "is it that much harder with $X$ relaxed?" If no, the general
is the definition and the desired special case is a Remark / Corollary
(PR-71) — as with $b\colon M\otimes_R M\to W$ vs. $M$ free $W=R$ finite,
and $\sup$ vs. $\max$ for signature.

**33. Premature specialization of signature hides the Dedekind /
$p$-adic / adele scope and should be recorded as an open problem.**
The quick "$F$ ordered, $V$ finite-dimensional, $p:=\max\dim U$" as the
definition of signature fixes the document to $F=\mathbb Q$ / $\mathbb R$
and presents the one-real-place specialization as if it were the notion,
when the notion for $L\in\mathbf{Lat}_R$ is
$\operatorname{sig}(L):=\operatorname{sig}(L\otimes_R\operatorname{Frac}(R))$
only when $\operatorname{Frac}(R)$ is ordered, is a family
$(p_\sigma,q_\sigma,r_\sigma)_{\sigma\text{ real}}$ for $R=\mathcal O_K$,
is not defined for $F=\mathbb C$, $\mathbb F_q$, $\mathbb Q_p$ (which
have $\dim\bmod2$ / discriminant / Hasse, not $(p,q,r)$), and belongs
over arbitrary Dedekind $R$ (in particular $\operatorname{cl}(R)=1$ not
assumed), $\mathbb Z_p$, $\mathbb Q_p$, $\mathbb C_p$, $\mathbb A$
(PR-72). State the explicit scope most definitions should be at and flag
a block that only does the ordered-field finite case outside the document
until the $R$ Dedekind / $p$-adic / adele generalization is supplied.

**34. Prefer intrinsic invariants of $\mathcal C$ over once-removed via
$\mathcal C\to\mathcal D$.** $\operatorname{rk}_R(M):=\dim_F(M\otimes_RF)$
and $\operatorname{sig}(L):=\operatorname{sig}(L\otimes_RF)$ are
technically correct in a pinch but stylistically poor — they bootstrap a
classical $F$-invariant to define an $R$-invariant, when the elegant
form defines $\operatorname{rk}_R$ / $\operatorname{sig}_R$ intrinsically
for $R$-modules / $R$-lattices (via $R\to\widehat R_{\mathfrak p}$,
$R\to\mathbb R$ at $\sigma$) and recovers $\dim_F:=\operatorname{rk}_F$
as the field specialization (PR-73). Flag once-removed definitions
outside the document until the intrinsic $R$-theory is supplied; they require
judgement and interactive research.

**35. "Index" is $p-q$, "signature" is $(p,q)$ / $(p,q,r)$ — never the
reverse.** Competing conventions (manifold / $L$-theory "$\sigma(M)=p-q$
is the signature," arithmetic Sterk-style "$\sigma=(p,q)$ vs. index")
conflate the two; here index always means the integer $p-q$ (Fredholm /
operator-theoretic index, Hodge computes $p-q$ and deduces $(p,q)$ since
$p+q=n-r$) and signature always means the full tuple $(p,q)$ or
$(p,q,r)$ (TERM-14).

**36. The object replaced by prose *about* the object.** A single
principle covers most annotation feedback: write the mathematical object
itself, at its natural level of generality and in its natural categorical
location — never explanatory prose about the object, implementation
details about it, or a lower-structure approximation to it. Its recurring
forms: fenced environments carrying the wrong content type — definitions
in prose, examples scattered, remarks that are transitional filler,
classification results not collected in their subtree (SEC-11);
constructions introduced where first needed instead of at the least
specialized section where they exist — the abstraction lattice
($R$-pairings before $W$-valued bilinear modules before lattices,
definite / indefinite / hyperbolic before embedding theory) is the owner
map (SEC-12); definitions below their maximal generality — over $\mathbf R$
when $R$ is arbitrary, "even" smuggled into the general notion,
lattice-specific language before the bilinear-module construction it
restricts (DEF-38); elementwise conditions as definitions when the
canonical map / adjoint / value group exists — nondegeneracy as
$b^{\sharp}$ injective, not a $\forall\,y$ sentence (DEF-39); isolated
quotients, kernels, and decategorified bijections where the source has a
cofiber sequence, a poset isomorphism, or an equivalence of groupoids
(DEF-40); equations between composites where a commuting diagram is the
mathematical type of the relation (DIA-7); database field names and
corpus bookkeeping leaking into theory prose — theory, implementation,
and provenance are three layers (PROSE-16); sentences whose subject is
the document — "this name is a convention", "the character itself is
standard" — self-announcing slop that states nothing (PROSE-17);
bibliography dumps with no local referent (CITE-4); local coinages where
the standard rep-theory or lattice terminology and the standard symbols
$\widetilde\Orth$, $\Orth^+$, $\widetilde\Orth^+$, $L[n]$ already encode
the distinction (TERM-16); silent passage between $\Emb(S,L)$, its
groupoid, its orbit set, and its double quotient (FORM-10); and
complexity that is non-monotone through the document — twists first met
inside the lifting argument (SEC-13).

**29. Twist is any $\varphi\colon W\to W'$, not just $\lambda\in R$.**
$\mathbf{Bil}_{R,W}$ is functorial in $W$ — $\varphi\colon W\to W'$
gives $\varphi_*\colon(M,b\colon M\otimes_R M\to W)\mapsto(M,\varphi\circ
b)$ by post-composition, and a twist is $\varphi_*$ when $W'=W$
(PR-67); $\lambda b$ is the case $\varphi:=\lambda\cdot_W$. State
$\varphi_*$ for any $\varphi$, then note $\lambda\cdot_W$ as a
specialization.

**30. Heuristic: read every parameter as an object and ask variance.**
The twist is forced by reading $W$ as $W\in\mathbf{Mod}_R$ and
$b\in\operatorname{Hom}_R(M\otimes_R M,W)$ and asking how $\operatorname{Hom}$
varies covariantly in $W$ ($\varphi\circ b$) and contravariantly in $M$
($b\circ(f\otimes_R f)$) — i.e. replace "$\lambda\in R$" / "$\forall x\in
M$" by the morphisms $\varphi\colon W\to W'$ / $x\colon1\to M$ they
shadow (PR-68). That habit rediscovers $\varphi_*\colon\mathbf{Bil}_W\to
\mathbf{Bil}_{W'}$, $W\mapsto\mathbf{Bil}_{R,W}$ as a fibered category,
and the element $\lambda$ as the single $\varphi:=\lambda\cdot_W$ among
all $\operatorname{End}_R(W)$ without remembering it.
All three are instances of the timeless weasel mass-noun problem:
"information," "data," "setting," "condition," … with no fixed referent,
context-dependent truth where the context is never stated, and no named
$R$-submodule / functor / category to check (PR-52) — audit by those
semantic indicators, not by the word list, which will change.

**37. Write the internal representation, not a description of it — the
recovery criterion.** The 18-point annotation synthesis sharpens the
single principle into a checkable criterion: a reader must be able to
recover the ambient category, objects, morphisms, universal properties,
exact sequences, chosen bases, value modules, and equivalence relations
directly from the notation (policy, "The single principle"). The forms
not coded before this tranche: adjectival map prose — "$R$-linear",
"the inclusion", "the matrix of $f$" — instead of the typed membership
$f\in\operatorname{Hom}_{\mathcal C}(M,N)$ (SYM-14); set containment
standing for categorical structure — subobjects as monos, common
subobjects as pullbacks, fixed objects as equalizers, orthogonal
complements as kernels, and construction-space containments like
$\operatorname{PrimEmb}(L,M)\subseteq\Hom(L,M)$ (STR-5); an exact
sequence at the theorem's strength rather than a convenient truncation
— Miranda–Morrison's factorization, $g(L)$, and the epi–mono structure
preserved, not compressed to an ad hoc sequence on the image (EV-9);
actual mathematics compressed into English — "the morphism $e\mapsto
e, f\mapsto f$", "the remaining summands give", "multiplies pairings by
$4$" instead of the exhibited isometry $L\to L(4)$ (PR-74); value
objects coarser than the mathematics permits — $\mathbb Q/\mathbb Z$
where the form factors through $\tfrac1N\mathbb Z/\mathbb Z$
(PRECISION-05); set-theoretic adjectives for algebraic properties —
"finite module" where the proof uses finitely generated torsion or
finite length (TERM-17); gratuitous temporary notation — $L:=M(2)$ to
save two characters (NOT-5); macros that encode mathematical
normalization — one uniform spelling of discriminant, hyperbolic
lattice, $p$-adic completion, primitive norm-$n$ vectors, so equivalent
constructions look equivalent (NOT-6); attribution appended to a sketch
instead of belonging to the statement (CITE-5); catch-all chapters with
no single subject — theory split by natural ownership: pairings,
bilinear modules, lattices, torsion forms, definite, indefinite
unimodular, hyperbolic, embedding theory, classification, examples
(SEC-14); non-exhaustive lists masquerading as classification theorems
(SEC-15, EX-3).

**38. Loss of type information through prose — the flattening ladder,
and the economy rule.** The 81-annotation synthesis across five
annotated documents confirms the single principle is a *general*
mathematical-writing style, not a lattice-specific one: the recurring
defect is that a precise construction is flattened one or more levels —
diagram/functor/exact sequence $\to$ isolated map/property $\to$
set-theoretic description $\to$ English paraphrase — and the preferred
direction is the reverse. If a sentence says "$A$ sits inside $B$", ask
for the mono (STR-5, SYM-14); if it says "$f$ is injective", ask for
the exact sequence with vanishing kernel (DEF-40, EV-9); if two
constructions "agree", ask for the comparison morphism or commuting
diagram (DIA-7, PR-74); if a result "transports", ask for the functor
(MA-16); if a collection is described elementwise, ask whether it is
already a fiber, preimage, Hom-object, embedding object, orbit object,
kernel, or subcategory (PR-46, STR-6). Forms coded by this tranche:
existence prose replacing a point of the construction object —
"$M$ admits an embedding" for $\iota\in\Emb(L,M)$ (STR-6); the
parametrized notion before its special cases — $I$-modular before
unimodular, the real-place family before the single-place signature
(TERM-18); base change and transport stated as adjectives instead of
the functor applied to the diagram (MA-16); computational surrogates —
eigenvalue calculations where diagonalization or the maximal definite
subspace is the mathematical object (EV-10). The paired economy rule:
formalism is wanted exactly when it carries mathematical information
that removes ambiguity — explicit categories, functors, sequences,
diagrams, formulas (STR-5, SYM-14, DEF-40, DIA-7); extra notation,
announcing prose, trivial remarks, redundant adjectives, and
low-level calculations are rejected when they add none (PROSE-17,
PR-27, NOT-5, EV-10). The style is maximum semantic density, minimum
narration — not "more formal notation everywhere."

**39. The annotation corpus's second tranche: source-level conventions
and the categorical location of constructions.** The discriminant-
annotation round exposed gaps the first tranche left implicit, in two
groups. Source-level conventions that the annotations treated as
systematic but no rule stated: display mathematics that had not earned
display status — isolated signatures and one-line identities broken
out of their sentences (PR-75); the atomic semantic-macro rule —
`\disc` followed by an adjacent operand is a typographic fragment,
because every semantic operand belongs in the argument list, as the
pandoc macro repository's own policy already required (NOT-7);
cardinality written with absolute-value bars (NOT-8); manual
`\bigl(…\bigr)` sizing where the house delimiter API exists
(NOT-9); invented diagram-source syntax — attributes on the tikzcd
fence info string, `\begin{tikzcd}` embedded in `$$` — both of which
parse as something other than a diagram (DIA-8); and vanishing verbs
with no typed referent — "the mixed terms vanish" where
$\beta(L_i,L_j)=0$ is the claim (MA-17). Mathematical structure the
annotations demanded but the catalogue only implied: limits, kernels,
cokernels, and exact sequences taken in the relevant structured
category, not silently downstairs after a forgetful functor — the
cokernel in the abelian category of bilinear modules is not the
module cokernel with a form remembered afterward (FORM-11); the
statement/proof boundary — a proposition contains the claim, and the
retraction, section, representative calculation, or witness-building
algorithm belongs to the proof unless the witness is asserted data
(SEC-16); and side-sensitive settings that must expose every side —
left and right radicals and adjoints both stated, nondegeneracy as
the joint condition, no symmetry imported silently (STR-7). Two
placements were deliberate: the atomic-macro rule extends NOT-6 from
"one macro per construction" to the macro's call shape, and the
structured-category rule extends the single principle's "natural
categorical location" to where limits are computed, so both cite the
rules they sharpen rather than founding a parallel family. The
`getHelp` API surface carrying the writing policy is recorded with
the API guide, not here: an agent reading only the Pandoc mechanics
can comply with the syntax while reproducing every mathematical-style
failure, so the help points at this policy as normative.

**40. One missing model, two opposite defects.** The lattice-theory and
bilinear-form documents in `dzackgarza/research` (working tree over
`26d4e303bc`) show corrections toward precision producing verbalized
formalism — "the image subobject" beside $I_L\hookrightarrow\Orth(A_L)$,
"underlying monomorphism" and "monomorphisms in $\mathbf{Set}$" around
an injectivity claim, forgetful maps named $j_{L,M}$ and $U_{L,M}$ that
nothing later reads — and corrections toward economy producing the
earlier flattening again. The revisions oscillated because the single
principle was read one-directionally ("write the structure") and the
economy rule as a separate, weaker counterweight. This tranche rewrites
the principle around one test that decides both directions — does the
sentence state what the notation on the page does not — adds the
oscillation gate to the policy, tabulates the six editorial judgments
against the rules that answer them, and codes the forms the documents
show: prose restating a written arrow (PR-76); categorical vocabulary
around an elementwise argument, the mirror of FORM-11's downstairs
construction (MA-18); relationship phrases and decomposition claims
with no map or splitting — "the symmetry isomorphism", "identifies
with", $\Orth(L)\cong W(L)\rtimes P$ (EV-11); established notions
defined by a characterization, an improvised presentation, or an
elementary reformulation that the document's own adelic framework
supersedes — evenness through a $\operatorname{Quad}_{R,2W}$ lift,
$\Gamma_R^2(M)$ as inline relations, the genus place by place with
$K_v$ where the lattice condition is local-integral (DEF-41);
hypotheses at a proof's strength — Sylvester's law stated for perfect
forms and extended to degenerate ones inside the same block (STR-8);
hypotheses delegated to a citation — "satisfies the hypotheses of
[@Nik80, Thm. 1.14.2]" (CITE-6); and names for maps that no later
sentence uses (NOT-10).

**41. Fifteen gradients, one overshoot each.** A second review of the
same documents organized the defects of pattern 40 as axes, each with
an underspecified end, a target, and an overshoot between them that a
one-directional fix lands on: a map described in words, then a lift
restated at every occurrence; a morphism by its underlying function,
then "forgetful" and "$\mathbf{Set}$" around an elementwise argument;
variants by near-identical formulas, then variants named and unrelated;
an unsupported claim, then a citation in place of the construction.
This tranche adds the gradients table to the policy, states the
structural commitments the target positions share — constructions from
universal properties, the general construction before its fibers,
sequences through their relationships, the textbook formulation as floor
and not ceiling — and codes the forms the documents show: Hom-objects
treated as sets and the diagonal asserted $R$-linear (FORM-12);
$\mathcal B_{R,W}$ and $\mathcal Q_{R,W}$, $\rho_L$ and $\rho_{L,q}$
defined by parallel paragraphs (DEF-42); a signature on one display and
its condition on the next (PR-77); $\operatorname{MM}(L)$, $g(L)$, and
$K_L$ introduced "in the notation of [@MM09, Thm. V.5.1]" (CITE-7);
consequences closing a definition block (DEF-16); $Q_f$ for
$\operatorname{coker}(Uf)$ and $b(\lambda)$ beside $M(\lambda)$ (NOT-5,
NOT-6); "canonical" after a choice and "unique up to isometry" with no
two objects compared (EV-11); and the diagram or display for a plain
declaration (DIA-7). MA-18 and DEF-41 are rewritten so that neither
reads as a preference for the elementwise or textbook formulation: the
test is whether the argument uses a categorical property, and whether
the notion is an instance of the framework it is defined in.

**42. The standards behind the gradients.** A corrected addendum to
pattern 41 restated the axes as the structural commitments their target
positions share, with the general construction and its specializations
first: general pairings before bilinear modules before lattices; the
genus as a groupoid before its class set and class number, and the mass
as its groupoid cardinality (DEF-43); the discriminant pairing into the
value object its construction determines, not into $\mathbb Q/\mathbb Z$
(SYM-16); nondegeneracy and perfectness as vanishing terms of the
radical–coradical sequence (DEF-39); a category with its morphisms and a
functor with its action on morphisms at the defining occurrence
(MA-13); "finitely generated free" for "finite free" (TERM-17) and the
isometry to a twist for "anti-isometry" (TERM-16); the invariant-factor
condition written out for "the homocyclic case" (TERM-7); the defining
occurrence's symbol for
$T_{-1}(L)$ (NOT-6); the citation for "the quadratic character itself
is standard" (CITE-4); the equation of images for "the same image"
(EV-11); the genus and
Miranda–Morrison theory out of the isometries chapter (SEC-14); two
equations for "the rank adds and the determinant multiplies" (PR-74);
the map that realizes $dL$ for "differs from the twist" (EV-11); and the
aligned two-line display for a map with a signature and an assignment
(PR-77). The gradients table gains the axes of generality, families,
categories, obstructions, counting, ontology, coordinates, fluency,
architecture, blocks, and commentary, and the principle records that
the style presupposes a writer who knows the theory at the generality
where its constructions are native.

**43. The annotation round on the lattice and foundations chapters.** A
reading of the review annotations across the lattice-theory,
bilinear-form, and categorical-foundations documents in
`dzackgarza/research` (working trees over `ab530c1dcc`, `57c8eb1cb0`,
and `9be9b833a6`) exposed mechanisms the catalogue had stated only for
their first instances. New codes: a block has one lede and the lede
comes first — the claim after a paragraph of "Put" constructions, the
defined term in a subordinate clause, "the analogous statement holds"
(DEF-44); a general notion recalled at its owner and the special case
defined through it — length, $p$-elementary (DEF-45); a local–global
condition as one adelic object over the base ring, not a quantifier
over places (DEF-46); classical background at the audience level cited
and not re-exposed — representability, Yoneda, the underlying set, a
table of topologies (SEC-19); later statements written in the
structure the document has established — $L[n]/\Orth(L)$,
$\operatorname{PrimEmb}(U^{\perp2},L)$, $[v^*]$,
$\operatorname{Gen}(L)$, $\Cl(\mathrm{II}_{0,24})$ (MA-19); a functor
in a Hom-set used on both sides — the twist on morphisms, so
similarities compose (MA-20); the field's sentence for the field's
statement — "where $L$ is a finitely generated projective $R$-module",
"the full subcategory on", "there is a unique", "the wide
subcategory", an injective $G\injects\Orth(L)$ (TERM-19); logical
relations in logical vocabulary, objects not agents (PR-78); every
assertion with an argument, a referent, or a citation —
"Consequently … is finite", "the classical finiteness theorem", a
semidirect product displayed with no splitting (CITE-8); a graded
functor used as the functor — the long exact sequence of $\pi_*$, not
$\pi_0$ and $\pi_1$ with a "need not equal" (NOT-11). Extensions: the
natural codomain and the continuation cokernel, the object defined by
its place in the sequence, the condition on a term and not on the
existence of a sequence (DEF-40); the functor applied to the defining
sequence with the vanishing kernel named (MA-16); "$X$ is distinct
from $Y$" as the implication that holds and the counterexample to the
one that fails (PR-36); a module-theoretic property of a structured
object defined once on its underlying module (FORM-11); the level of
each summand glossed at the lcm (SYM-15); a reference label as a
pointer, not a noun (XREF-6); parallel displays as one `aligned`
display, and a family of parallel identities as one display (PR-77,
PR-75); functor application as $T(k)$, and a semantic macro with no
operand (NOT-7); type nouns and "underlying" as restatement (PR-76); a
value read in the coarse codomain (SYM-16); "discriminant" for
cokernels only, and "polarization" for the bilinear form of a
quadratic form (NOT-4); the monoidal tuple with $b_M\perp b_N$ as a
composite, for "the mixed terms vanish" and the sentence asserting the
structure (MA-13); an example enumerating a partitioned class set
(EX-1); surjectivity as a vanishing term (DEF-39); a classification
theorem inside the block defining "split" (DEF-16); the coinages
"carrier module", "adjoint cokernel", "common equalizer", "dual form",
"finite module", "$q(v)\neq0$", and "split" for a decomposition
(TERM-16); "the local homothetic condition" (TERM-7); "$R$-linear" as
a type (TERM-11); "refining its length" with no map (TERM-12); "agree
canonically", "identifies", "geometric identification" (EV-11);
$\isoto$ on an inclusion (NOT-2); $L^I$ for an involution (NOT-1);
$\Emb(S,L)$ for its orbit set (DEF-43); invariants built at the
lattice chapter (SEC-12); commentary sentences whose deletion loses
nothing (SEC-7); a heading naming the coordinate shadow (PR-61).

**44. The preferences under the annotation round.** A second pass over
the annotations on the lattice and foundations chapters, read for the
preferences behind them. The reader is an expert who shares the
literature, and the cost of a sentence is its decoding load: a standard
name with its citation, a label, a compact object, and a defined symbol
are recalled; a coinage, a nickname, a first-principles re-derivation,
a family written out in place of the compact object, and an unpacking
are parsed and link to nothing (TERM-20, XREF-7, SEC-19, DEF-45,
DEF-46). Compression is lossless: "canonical", "coincide", "the same",
"factors through", "underlying", and a relative construction without
its ambient each drop a datum the reader must reconstruct (EV-11,
FORM-13, PR-57, STR-5, MA-17). The level is the structure: a property
is a condition on the structure, with the invariant and the witness as
propositions; the general construction is defined once, the
subcategory's version is its composite with the reduction functor, and
the named special cases are examples; parallel notions are written by
one pattern (DEF-47, DEF-48, DEF-40, DEF-42). Form is content: the
block type as logical status, a display for a structural unit, a map
with its full assignment, a sequence whole, one spelling per object,
the field's sentence (SEC-11, PR-75, PR-77, NOT-6, NOT-5, TERM-19,
TERM-16).

**45. The self-report after the annotation round.** A frontier model's
account of why its proposals under the annotation round went sideways
names five mechanisms, each a rule of this policy. Machinery in place of
level: the ring renamed to $\bZ[G]$ while the isotypic sublattices were
still defined through idempotents of $\bQ\otimes_\bZ\bZ[G]$, auxiliary
cokernels, and their torsion; the invariant and coinvariant lattices
described as images of idempotents on $L_\bQ$; $V$ bound to $L_\bQ$ for
one block (DEF-49, MA-16, NOT-5, TERM-18). Notation in place of
recognition: a precision annotation answered with a temporary symbol, a
named comparison morphism, a square in $\mathbf{BilMod}_\bZ$ with a
forgotten corner, an unlabelled arrow, a cokernel of an unnamed map, a
stabilizer as a bare monomorphism, a determinant of a form, a fraction
in place of $v^*$ (NOT-5, FORM-11, DIA-7, DEF-40, PR-57, PR-61, MA-19,
DEF-42). Formalization in place of structure: a factorization narrated
in prose where its triangle belongs, and a commuting square written as
an equation (DIA-7). Statements with no consumer: the two-elementarity
of $L^{\generators{I}}$ and $L_{\generators{I}}$ as the last block of
its chapter, the surjectivity of $\rho_{L,q}$ as a block of its own, two
chapters with one block each, the sections of the root-systems chapter
out of dependency order, the basic-invariants chapter outside the book
(SEC-20, SEC-14, SEC-13, SEC-9). The manuscript's own language
overlooked: the Coxeter graph re-defined, Maschke's theorem re-derived,
the source's sign convention narrated inside a definition, a hypothesis
named after its source, "canonical" on a quotient, a monomorphism, and a
form, $\oplus$ on morphisms beside $\perp$ on objects, evenness restated
at every block, "even ordinary" used in a theorem with no link to its
defining occurrence, "data" for a graph (SEC-19, CITE-9, EV-11, NOT-6,
STR-8, XREF-5, TERM-7). Behind the five is one gap: the classification
units state fragments — "Otherwise $b$ takes both signs.", the
congruence $p-q\equiv0\pmod8$ as the whole of a chapter, $\delta$
defined by the existence of a witness inside the theorem, the generators
$p,q,u,v$ introduced as realizations in a paragraph (SEC-21, SEC-11,
DEF-47, DEF-41, EX-3). The annotation gate records the class, the sweep,
the notation ledger, the transformation scope, and the level and
consumer of a proposal before it is written.
