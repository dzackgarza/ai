# Examples (`EX-*`)


## `EX-1`: An example mirrors the definition's form

An example instantiates each slot of the structure it exemplifies. If a
monoidal category was defined as a tuple
$(\mathcal{C}, \otimes, \mathbf{1}, \alpha, \lambda, \varrho)$, the example
presents the tuple: "Let $\mathcal{C}$ be a category with finite products
and terminal object $e$. Then $(\mathcal{C}, \times, e)$ is a monoidal
category." The reader who just read the definition sees which slot is
which without parsing prose. Listing the components in a sentence instead
of presenting the tuple is readable but does not mirror the definition's
grammar. Calling something an example without showing the instance gives
the reader no mathematical test.

**Banned:** "Affine space is an important example of a scheme."

**Preferred:** "For a ring $A$, the locally ringed space
$\operatorname{Spec}(A)$ is an affine scheme. When $A=k[x_1,\ldots,x_n]$, it
is affine $n$-space over $k$."

**Banned:** "A category with finite products is monoidal with $a\otimes b$ a
chosen product $a\times b$ and $e$ a terminal object, the three isomorphisms
being the unique ones commuting with the projections; this is the cartesian
monoidal structure."

**Preferred:** "Let $\mathcal{C}$ be a category with finite products and
terminal object $e$. Then $(\mathcal{C}, \times, e)$ is a monoidal category,
with associator and unitors the canonical isomorphisms supplied by the
universal property of the product."

A definition or theorem that partitions a constructed finite set — the
class set $\Cl(L)$ into spinor genera, a genus into classes, the
isotropic vectors into orbits — is followed by an example that
enumerates the set and its partition for one $L$: the reader sees the
blocks of the partition as objects, and a partition with no computed
instance is an unexercised definition [@CS99, Ch. 15].

Observed in `dzackgarza/research`,
`research/lattice-theory/discriminant-forms-and-genus.md` (working
tree over `57c8eb1cb0`), definition "Spinor genera".

**Banned:** "resulting equivalence classes partition $\Cl(L)$; their
set is denoted $\operatorname{SpinGen}(L)$." with no example in which
$\Cl(L)$ and $\operatorname{SpinGen}(L)$ are listed.

**Preferred:** the definition followed by "**Example.** For $L=\dots$,
$\Cl(L)=\{[L_1],\dots,[L_h]\}$ and
$\operatorname{SpinGen}(L)=\{\{[L_1],\dots\},\dots\}$ [@CS99, Ch.
15]" with a genus whose spinor genera are not all singletons.

## `EX-2`: An example is an example, not a proposition

### Yes/no example: an indefinite lattice with infinitely many isometries

**No:** "Neither conclusion holds for indefinite lattices" as a
proposition, followed by a specific Pell equation.

**Yes:** **Example.** Let $L=\langle1\rangle\perp\langle-2\rangle$
with its standard ordered basis $e,f$. Define $g\colon L\to L$ by
$g(e)=3e+2f$ and $g(f)=4e+3f$. Then
$$
[g]_{e,f}^{\mathsf T}
\begin{pmatrix}1&0\\0&-2\end{pmatrix}
[g]_{e,f}=\begin{pmatrix}1&0\\0&-2\end{pmatrix},
\qquad [g]_{e,f}=\begin{pmatrix}3&4\\2&3\end{pmatrix}.
$$
Its determinant is $1$, so $g\in\Orth(L)$. The eigenvalue
$3+2\sqrt2>1$ proves that $g$ has infinite order. Moreover,
$g^n(e)=x_ne+y_nf$ gives distinct points of $L[1]$, since
$x_n+y_n\sqrt2=(3+2\sqrt2)^n$ for $n\geq0$.

**Test:** the example names the failed conclusions and gives an
explicit lattice, isometry, and infinite family. Sources: live Zettlr
annotations `248133a2-6f7c-4264-9f58-eda15241361a` and
`b94eea71-2c18-4c2b-b19e-70c0bad4c71e`, quoted manuscript passages.

If there is nothing to prove, do not present the passage as a proposition
with a proof. A category with finite products is an example of a monoidal
category, not a theorem. State the definition, then give the example in an
example block. Reserve proposition blocks for statements that say more
than the definition, and give each one the proof or citation that the
house's proof obligation requires.

## `EX-3`: A non-exhaustive list is an example, never a classification theorem

An example block that lists instances — "the following lattices arise:
$D_{16}^+$, …" — carries no completeness claim, and a theorem block
that lists instances carries an implicit exhaustiveness claim. Do not
present a partial list as a classification theorem: the reader cannot
distinguish "these are all of them" from "here are some". A
classification is a theorem whose statement specifies its scope and its
completeness ("the isometry classes of even unimodular lattices of
rank $n\le 24$ are …"); anything less is an example (`EX-1`) or a
computation, and it lives in the examples section (`SEC-15`).

**Banned:** "Theorem: the following even unimodular lattices exist …"
with a list the text elsewhere admits is partial; a "Classification"
section whose list omits whether it is complete; an example list
presented with theorem numbering.

**Preferred:** "::: {#exm-even-unimodular-low-rank} ## Even unimodular
lattices, rank $\le 24$ — the classes represented by
$E_8^{\perp 3}$, $D_{16}^+$, … ; the complete list at this rank is
[@Kin03] (classification subtree). :::" — an example block, with the
completeness claim either stated with its scope as a theorem in the
classification subtree or cited to its source (`CITE-4`).
