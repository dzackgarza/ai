# Properties and structure (`STR-*`)


## `STR-1`: Use the forgetful functor

For a specified forgetful functor $U\colon\mathcal S\to\mathcal C$, full
faithfulness gives at most property, faithfulness gives at most structure, and
an arbitrary functor gives at most stuff. Repleteness is a separate condition
when an essential image is replaced by a full subcategory. Property language is
used only when each homotopy fiber of $U$ is empty or a contractible groupoid;
otherwise name the chosen structured object over $X$.

## `STR-2`: Name every chosen structure

A structure on $X$ is a chosen object in the fiber over $X$ of a specified
forgetful functor. When several choices exist, name the one used by the
construction. For example, for a commutative ring $R$, tensor product and
direct sum give the different monoidal structures $(R\text{-}\mathbf{Mod},
\otimes_R,R)$ and $(R\text{-}\mathbf{Mod},\oplus,0)$. Over a noncommutative
ring, state the bimodule, left-module, or right-module setting. A ring is a
group under addition, not under multiplication.

## `STR-3`: State every hypothesis

A theorem states every object property, characteristic restriction, limit
assumption, flatness assumption, and equality of named morphisms used in its
conclusion. If a construction uses a basis, embedding, section, presentation,
or other witness, name that witness in the construction.

## `STR-4`: Strict equality versus specified natural equivalence for a factorization

A factorization is described as "an equality $F=G\circ H$ or a specified
natural isomorphism $F\Rightarrow G\circ H$" as alternatives, conflating a
property (strict equality, which does not exist under an
$\infty$-categorical default where $\mathbf{Cat}:=\mathbf{Cat}_\infty$, as in
a document that adopts DEF-13)
with extra structure (a specified $2$-cell). In $\mathbf{Cat}_\infty$ a
factorization is always a tuple $(H,G,\alpha)$ with $\alpha$ a specified
natural equivalence.

**Banned:** "together with an equality $F=G\circ H$ or a specified natural
isomorphism $F\Rightarrow G\circ H$."

**Preferred:** "together with a specified natural equivalence
$\alpha\colon F\simeq G\circ H$." If the $1$-categorical strict case is
meant, state it as the truncation "$F=G\circ H$ on the nose, i.e.
$\alpha=\operatorname{id}$ in $\mathbf{Cat}_1$," not as an alternative to
the $\infty$-categorical structure.

## `STR-5`: Set containment never stands for categorical structure

$\subseteq$ is a set-level relation. It does not exhibit the subobject,
the map, or the universal property, and a reader cannot recover the
ambient category from it. Write the typed map whose existence or
property the containment shadows. A subobject is a monomorphism
$\iota\colon S\rightarrowtail M$; a common subobject is a pullback; a
fixed object is an equalizer; an orthogonal complement is a kernel of
the adjoint, $N^{\perp_b}:=\ker(\,b^{\sharp}\circ i\,)$ for
$i\colon N\rightarrowtail M$ (`PR-57`); a subspace arrangement is a
diagram. Even where an ambient set exists, the mathematical content is
the categorical object, not the containment (`PR-56`, `DEF-40`).

The same holds between construction-spaces:
$\operatorname{PrimEmb}(L,M)\subseteq\Hom(L,M)$ shadows the defining
square — the mono into the hom-set and the predicate it cuts out — or,
at the level the theory uses, the fiber, the subspace, or the map of
sets that relates them. Exhibit the relevant map; do not write the
containment in its place.

**Banned:** "a submodule $N\subseteq M$" with no map named;
"$\operatorname{PrimEmb}(L,M)\subseteq\Hom(L,M)$" as the definition of
the space of primitive embeddings; "the common sublattice"; "the fixed
sublattice"; "$N^{\perp}\subseteq M$" with no ambient, form, or mono.

**Preferred:** "$\iota\colon N\hookrightarrow M$ in
$R\text{-}\mathbf{Mod}$"; "the pullback $S_1\times_M S_2$ of
$\iota_1,\iota_2$"; "the equalizer of $f,g\colon M\to T$";
"$N^{\perp_b}:=\ker(b^{\sharp}\circ i)$ for $i\colon N\hookrightarrow(M,b)$";
"the fiber of the evaluation map
$\operatorname{ev}\colon\Emb(L,M)\times M\to W$" or the square that
defines $\operatorname{PrimEmb}(L,M)$, drawn once
(`DIA-7`, `PR-56`).

A subobject is a monomorphism, and a definition that begins with a
subset has no map to construct with: every construction on the
subobject — its saturation, its complement, its cokernel — is a
function of the monomorphism.

Observed in `dzackgarza/research`,
`research/lattice-theory/embeddings-and-overlattices.md` at
`ab530c1dcc`, definition "Saturation".

**Banned:** "Let $S\iscontainedin L$ be a sublattice."

**Preferred:** "Let $\iota\colon S\injects L$ be a monomorphism in
$\mathbf{Lat}_\bZ$."

## `STR-6`: Existence prose is a point of the construction object

"$M$ admits an embedding into $N$" replaces a point of the embedding
object by prose asserting existence. The embedding is the datum:
$\iota\in\Emb_{\mathcal C}(M,N)$, a point of the embedding object
(with $\mathcal C$ the ambient category, named). Existence prose
discards the very datum the mathematics needs — which embedding, in
which category, satisfying which predicate — and invites the reader to
reconstruct all three. The same defect generalizes: "admits a
decomposition," "admits a complement" — each is a point of, or a
subobject of, the construction object that classifies the datum
(`STR-1`). State the point or the subobject; keep existence as its
corollary.

**Banned:** "$M$ admits an embedding into $N$" with no category and no
map; "$L$ admits a primitive embedding" standing in for
$\iota\in\operatorname{PrimEmb}(L,M)$ (`STR-5`); "admits an orthogonal
decomposition" with no decomposition named.

**Preferred:** "$\iota\colon(M,b)\hookrightarrow(N,c)$ in
$\mathbf{Lat}_{\mathbb Z}$" or
"$\iota\in\operatorname{PrimEmb}(L,M)$, the fiber of the evaluation
map drawn once (`STR-5`)"; "there exists $\iota\in\Emb(L,M)$" when bare
existence is all that is claimed, with $\Emb(L,M)$ defined (`EV-5`).

## `STR-7`: A side-sensitive setting exposes every side

`STR-2` asks authors to name the left-, right-, or bimodule setting;
this rule governs what the mathematics itself must then expose. In a
setting where left and right versions of a construction can differ —
noncommutative rings; a bilinear form $b\colon M\otimes_R M\to W$ with
distinct left and right radicals, distinct left and right adjoints
$b^\sharp\colon M\to\operatorname{Hom}_R(M,W)$ and
$b^{\sharp\,\mathrm{op}}$; kernels, images, and annihilators taken on
each side — each claim states *both* sides, or states the one side it
asserts and names the symmetry that identifies it with the other.
"Nondegenerate" is stated in the side-appropriate joint form: over a
noncommutative ring, nondegeneracy of $b$ is a condition on the left
and right adjoints together, not on one chosen adjoint, unless the
stated hypothesis is explicitly the one-sided condition. Never import a
symmetric or commutative convention — "the" radical, "the" adjoint,
"the" kernel — into a side-sensitive context: the definite article is
the tell that a symmetry was silently assumed. Where the symmetry
exists ($R$ commutative, $b$ symmetric, the twist identifying
$\mathbf{LMod}$ with $\mathbf{RMod}$), state it once and cite it at
each identification (`STR-3`, `TERM-15`).

**Banned:** "the radical of $b$" for a noncommutative form whose left
and right radicals differ; "$b$ is nondegenerate" over a noncommutative
ring with no statement of which adjoint is an isomorphism;
"$\ker b^\sharp$" standing in for both
$\ker(b^\sharp)\neq0$ and $\ker(b^{\sharp\,\mathrm{op}})\neq0$.

**Preferred:** "with $R$ commutative, $b^\sharp$ and
$b^{\sharp\,\mathrm{op}}$ are identified by the symmetry $\tau$ of
$\mathbf{Mod}_R$, so 'the' adjoint is unambiguous (`TERM-15`)"; over a
general ring: "the left radical
$\operatorname{rad}_l(b):=\ker(b^\sharp)$ and the right radical
$\operatorname{rad}_r(b):=\ker(b^{\sharp\,\mathrm{op}})$; $b$ is
nondegenerate when both vanish" — every side named, the joint
condition stated, the symmetry that would identify them cited, not
assumed (`STR-2`, `STR-3`).

## `STR-8`: State the hypotheses the claim needs, not the ones a proof used

A statement block carries the hypotheses under which its conclusion is
a theorem, at that strength. A hypothesis that one proof route finds
convenient — perfectness where nondegeneracy or nothing is needed,
freeness where finite generation suffices, a field where a domain
suffices — is a proof artifact. Stated in the block, it narrows the
theorem, breaks the generality `DEF-38` asks for, and misleads every
later citation of the block. The tell is a proof, remark, or later
block that removes the hypothesis it was stated under. The test is to
ask, for each hypothesis, which step of the proof uses it and whether
the conclusion fails without it: a hypothesis that no step uses in full
strength is weakened to what the step uses, and a hypothesis removed
later in the same block was never a hypothesis. `STR-3` governs the
opposite defect, a hypothesis used and not stated.

Observed in `dzackgarza/research`,
`research/category-theory/framework/Bilinear-and-Quadratic-Forms.md`
(working tree over `26d4e303bc`), theorem "Sylvester's law of inertia".

**Banned:** "Let $F$ be an ordered field and let $b$ be a perfect
symmetric bilinear form on a finite-dimensional $F$-vector space $V$.
Then $V\cong V^{+}\perp V^{-}$ …" followed, inside the same block, by
"For a degenerate $b$, choose a complement $N$ to $\radic(V)$ … hence
perfect because $N$ is finite dimensional. Applying the above to $N$
gives $V\cong V^{+}\perp V^{-}\perp\radic(V)$" — the hypothesis the
block opens with is removed by the block's last paragraph.

**Preferred:** "Let $F$ be an ordered field and $(V,b)$ a
finite-dimensional symmetric bilinear space over $F$. Then
$V\cong V^{+}\perp V^{-}\perp\radic(V)$ with $b$ positive definite on
$V^{+}$ and negative definite on $V^{-}$, and
$(\dim V^{+},\dim V^{-},\dim\radic(V))$ depends only on the isomorphism
class of $(V,b)$"; the nondegenerate case is the case $\radic(V)=0$,
and the reduction to it is the first step of the proof.

The evenness hypothesis repeated at every block that mentions a
quadratic discriminant form is the same defect in the other direction: a
hypothesis owned by one definition restated at each use. Every bilinear
form has the quadratic form $q_b(x)=b(x,x)$; evenness is the hypothesis
of the $\bQ/2\bZ$-valued refinement alone, stated once at the definition
of $A_{L,q}$ (`DEF-42`). A block states the bilinear and the quadratic
case in one display, under that definition's hypothesis.

Observed also in `dzackgarza/research` at `9cfdecf73d`:
`research/lattice-theory/automorphism-lifting-through-a-gluing.md`,
observation "Discriminant action on an orthogonal sum", definition "The
gluing datum of a pair of primitive inclusions", and corollary "Lifting
across a unimodular overlattice".

**Banned:** "If $M$ and $N$ are even, likewise"; "If $L,M,N$ are even,
$h$ refines to"; "If $L,M,N$ are even, $\gamma$ refines to".

**Preferred:** the hypothesis once at the definition of $A_{L,q}$, and
"$A_{M\perp N}\isoto A_M\perp A_N$, and likewise for $A_{-,q}$" as one
display.
