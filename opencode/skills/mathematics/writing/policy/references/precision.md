# Precision (`PRECISION-*`)

These policies prevent prose from taking the place of a typed mathematical statement.
The general reason is the same in each case: a reader must be able to identify the objects, maps, hypotheses, and conclusion without guessing.
The tell is stylistic; the defect is that a definition was not written or an object not named, and the remediation is the missing mathematics, never a nicer phrase.

## `PRECISION-01`: Replace mood words with definitions

**Banned:** “A scheme is a geometrically complete space.”; “The subcategory is structurally complete under sameness.”

**Preferred:** “A scheme is a locally ringed space locally isomorphic to the spectrum of a commutative ring.”; “A full subcategory $\mathcal D\subseteq\mathcal C$ is *replete* if every object of $\mathcal C$ isomorphic to an object of $\mathcal D$ belongs to $\mathcal D$.”

Vibe adjectives and impressive qualifiers sound technical while leaving the defining conditions unknown.
Use the standard term and state its definition; the definition is the work.

## `PRECISION-02`: Replace vague qualifiers with exact scope

### Yes/no example: evenness does not supply unimodularity

**No:** "If $L$ is even, then $p-q\equiv0\pmod8$."

**Yes:** "For $L=\langle2\rangle$, $\operatorname{sign}(L)=1$ and
$A_L^\sharp\cong\mathbb Z/2\mathbb Z$." This even lattice is a
counterexample to the stated implication. A signature theorem must
include its unimodularity hypothesis and use the document's defined
signature invariant.

**Test:** $b(ne,ne)=2n^2$ proves evenness; the Gram matrix $(2)$ has
signature $1$. Source: live Zettlr annotation
`ad9ab9a4-1e9b-4380-82df-bac3c73b2289`, quoted manuscript passage.

**Banned:** “This holds essentially for finite type schemes.”

**Preferred:** “This holds for schemes locally of finite type over a field.”

Words such as “essentially”, “basically”, “morally”, “roughly”, and “in some sense” hide the hypothesis or weaken a claim without saying how.
State the exact scope, or name a genuine approximation such as “up to isomorphism” or “to first order”.

## `PRECISION-03`: Name objects instead of using empty collective nouns

**Banned:** “The construction carries the required structure.”; “the discriminant package”; “the forms frame”; “the equality slice”.

**Preferred:** “The pullback sheaf has restriction maps satisfying the sheaf axiom.”; “the discriminant construction and its exact sequences”; the exact chapter, section, or construction meant.

Process and software nouns — “package”, “frame”, “pipeline”, “suite”, “layer”, a vague “slice”, “framework” — gather mathematical objects without naming them.
Mass nouns — “information”, “data”, “setting”, “condition”, “hypotheses”, “conclusion”, “notion”, “structure”, “property” — do the same when they have no fixed referent, so a sentence can be defended as true under some interpretation while naming nothing to check.
Detect the problem by what the noun does, not by a word list.
A clause is weasel-wording when any one of these holds:

- **No fixed referent.** The noun names no defined object: no defining occurrence, no type, no stated list.

- **Meaning depends on a context that is never fixed.** “Retains additional information” is true of any true statement; “with its hypotheses” is true of every theorem; “in the discriminant setting” is true in whatever ambient the reader imagines.

- **Unfalsifiable.** Any counterexample can be deflected as “not the intended information / setting / condition”, because no quantified proposition was stated (`PR-30`).

- **Abuse of colloquial understanding.** The reader is expected to supply the mathematical meaning from ordinary English.

- **Occupies the slot of a named object.** The noun sits where a map, submodule, category, or diagram is owed.

Replace the noun by the object that already has a name:

- **Banned:** “quadratic forms retain more information than their bilinear forms.”
  **Preferred:** “distinct quadratic forms can have the same associated bilinear form: over $\mathbb F_2$, $x^2+xy+y^2$ and $xy$ both have polar form $b(u,v)=u_1v_2+u_2v_1$.”

- **Banned:** “in the discriminant setting.”
  **Preferred:** “for the discriminant form $q_L\colon L^\vee/L\to\mathbb Q/2\mathbb Z$ of an even nondegenerate lattice $L$.”

- **Banned:** “with its hypotheses”; “satisfies the evenness condition.”
  **Preferred:** “for $2$ a unit in $R$”; “$b$ is even” (`PR-50`).

New weasel nouns will appear; audit by the indicators, not the list.
When one is found, replace it by the object that already has a name, or define that object at a defining occurrence; do not add the noun to a list and keep the sentence.

## `PRECISION-04`: State universal constructions and universal properties

**Banned:** “Define $E\to X$ by pulling back $U\to B$ along $X\to B$.”; “the three isomorphisms being the unique ones commuting with the projections.”

**Preferred:** “Let $E$ be the pullback in the Cartesian square $E\to U$, $E\to X$, $U\to B$, $X\to B$.”; “the associator $\alpha_{a,b,c}$ and the unitors $\lambda_a$, $\varrho_a$ are the unique isomorphisms supplied by the universal property of the product.”

“Obtained by pulling back” is an instruction without the square, maps, or universal property.
Appeals to “the projections”, “the universal property”, or “the unique map” leave the reader unable to verify the uniqueness until the property, the object supplying it, and the target are identified.
Give the diagram or state the property that characterizes the object, and name the object that supplies it.

## `PRECISION-05`: Value objects at the precision the mathematics permits

A value object — the codomain of a form, a character, a pairing, a
torsion invariant — is written at the precision the mathematics
produces, not at the precision of the nearest available ambient group.
Writing a coarser ambient object because it exists is a loss of
information in the type: the statement becomes weaker than the theorem,
and constructions that need the finer structure cannot be transported.
State the value module the construction produces; state coarser
presentations as corollaries with the map that relates them. Evenness
and similar normalization conditions are stated through the value
module $\operatorname{Val}(b)\subseteq W$ once, not re-derived as
integer-valued formulas at each use (`PR-45`, `DEF-39`).

**Banned:** "the discriminant form takes values in $\mathbb Q/\mathbb
Z$" when the form factors through $\tfrac1N\mathbb Z/\mathbb Z$ with
$N$ the level, stated nowhere; "there is a homomorphism
$D_L\to\mathbb Q/2\mathbb Z$" as the whole statement where the
structure theorem supplies the exponent and the factorization.

**Preferred:** for an integral nondegenerate lattice $L$, put
$N=\exp(A_L^\sharp)$. Its discriminant pairing has type
$\bar b_L\colon A_L^\sharp\otimes_{\mathbb Z}A_L^\sharp
\to\tfrac1N\mathbb Z/\mathbb Z$ and satisfies
$\bar b_L([x]\otimes[y])=b_{L_{\mathbb Q}}(x,y)+\mathbb Z$.
Indeed, $Nx\in L$ for $x\in L^\#$, so $Nb(x,y)\in\mathbb Z$.
The inclusion $\tfrac1N\mathbb Z/\mathbb Z\hookrightarrow
\mathbb Q/\mathbb Z$ gives the ambient-valued pairing (`PR-56`).

### Yes/no example: bilinear and quadratic values differ

**No:** "$q_L^{(2)}\colon A_L^\sharp\to\mathbb Z/2\mathbb Z$"
obtained by replacing the value module of $q_L$ without a map.

**Yes:** For $L=\langle2\rangle$ with generator $e$, set $a=[e/2]$.
In the convention $q_L([x])=b(x,x)+2\mathbb Z$,
$$
\begin{aligned}
\bar b_L\colon A_L^\sharp\otimes_{\mathbb Z}A_L^\sharp
&\longrightarrow\tfrac12\mathbb Z/\mathbb Z,\\
a\otimes a&\longmapsto\tfrac12+\mathbb Z,\\[4pt]
q_L\colon A_L^\sharp&\longrightarrow\tfrac12\mathbb Z/2\mathbb Z,\\
a&\longmapsto\tfrac12+2\mathbb Z.
\end{aligned}
$$
The displayed bilinear value module has order $2$; the quadratic one
has order $4$. An isomorphism of value modules must be supplied before
postcomposition can change a codomain.

**Test:** calculate the value of the discriminant generator in the
stated quotient. Source: live Zettlr annotation
`e1474cc5-872d-4013-bb31-16eebdbd35f7`, quoted manuscript passage;
the conventions are those of [Hecke, Discriminant groups](https://docs.hecke.thofma.com/v0.28/quad_forms/discriminant_group/).
