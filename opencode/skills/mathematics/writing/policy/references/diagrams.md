# Diagrams (`DIA-*`)


## `DIA-1`: Draw the square

Draw a universal construction as its square. Label every morphism. Mark it
cartesian or cocartesian. Name the resulting object and structure morphism in
the diagram. The prose may state the universal property after the diagram; it
never replaces the diagram.

## `DIA-2`: Every arrow is typed

Every arrow in an authored diagram is labeled with the functor, natural
transformation, or map it denotes, and its source and target are the
displayed objects. A construction defined only on cores is drawn
from the cores. An invariant on isomorphism classes is drawn as a map from
$\pi_0$. Membership of an object in a category is not drawn as a functor
between categories.

## `DIA-3`: A classifying object with its universal property

A classifying object, classifying category, or universal family is named only
together with the represented functor or its explicit universal property.

## `DIA-4`: Display an adjunction

An adjunction $F\dashv G$ is displayed with its source and target categories
and both functors, drawn with the document's one shared adjunction diagram.

## `DIA-5`: A comparison of functors is a 2-cell

A comparison between functors is a natural transformation or another
specified 2-cell. A morphism between objects is a morphism in the stated
category.

## `DIA-6`: Landing in a subcategory is a factorization

A theorem that a functor lands in a replete full subcategory is a proved
factorization through its inclusion. Any other landing statement names the
actual codomain.

## `DIA-7`: A diagram whenever the relation is diagrammatic

When the mathematical content is a commutativity, compatibility,
factorization, comparison of embeddings, or a universal construction,
represent it by a labeled commuting diagram, not by prose and not by an
isolated equation between composites. An equation $\varphi\circ\iota_1
=\iota_2$ states that two elements of a hom-set agree; the triangle with
vertices $S$, $M_1$, $M_2$ and arrows $\iota_1$, $\iota_2$, $\varphi$
exhibits the objects and the maps, which is the mathematical type of the
relation (DIA-2). If a diagram expresses the type more faithfully than an
equation, the diagram is owed. The converse holds with the same test: a
declaration whose content is a source and a target is an arrow in prose,
and a diagram with one arrow, or a display holding one signature, is
typography standing where a relation would be (`PR-75`, `PR-77`). A
pullback is drawn when a pullback is defined; an exact sequence is
displayed when exactness is the assertion; a map is written
$f\colon M\to N$ when the assertion is that it exists.

**Banned:** "An equivalence of embeddings is an isometry $\varphi\colon
M_1\isoto M_2$ with $\varphi\circ\iota_1=\iota_2$" standing alone; "the
construction is compatible with base change" with no square; a
`tikzcd` environment containing one arrow $L\to M$ where the sentence
"let $f\colon L\to M$ be a morphism" says the same.

**Preferred:** the triangle or square, drawn once, referenced thereafter:
```tikzcd
& S \arrow[dl,"\iota_1"'] \arrow[dr,"\iota_2"] & \\
M_1 \arrow[rr,"\varphi"'] && M_2
```

## `DIA-8`: A diagram is authored in the accepted source form, with its metadata where the renderer reads it

A `tikzcd` diagram is authored in one of the accepted source forms —
a fenced `tikz`/`tikzcd` code block whose info string is bare, a raw
`\begin{tikzcd} … \end{tikzcd}` block, or an `\input{...}` of a shared
diagram file — never in an invented form. Two invented forms are
banned as recurring: attributes on the fence's info string, and the
environment embedded inside `$$` display math. Both break silently:
an info string with attributes turns the fence into ordinary inline
code, so the diagram renders as literal text and no compiler error is
raised; `$$\begin{tikzcd} … \end{tikzcd}$$` parses as display *math*,
so the diagram source reaches the math renderer instead of the
diagram compiler. A figure that needs an ID, title, or
cross-reference carries them where the renderer reads them: a Pandoc
attribute block on the fence, or a fenced figure div around the
diagram, per the house's syntax.

**Banned:** ```` ```tikzcd id="main-square" ```` and any other
attribute on the fence info string; `$$\begin{tikzcd} ... \end{tikzcd}$$`
in place of the fence or raw block.

**Preferred:** a bare ```` ```tikzcd ```` fence (or the raw
environment, or `\input{diagrams/example.tikzcd}`); metadata in the
house's accepted form — `::: {#fig-square caption="…"}` around the
diagram — where the cross-reference resolver finds it (`XREF-1`).
