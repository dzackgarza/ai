# Axioms (`AX-*`)


## `AX-1`: A definition that names axioms without stating them

A definition must fully determine the notion it introduces. Referencing
axioms by name — "satisfying the two hexagon conditions", "satisfying the
pentagon axiom" — without stating or drawing the diagrams is not a
definition. The reader cannot evaluate whether a given object satisfies the
definition, because the name of an axiom is not the axiom. State the
equations or draw the diagrams. If they are long, cite the exact diagrams
by reference to where they are written in full.

**Banned:** "A braiding on a monoidal category is a natural isomorphism
$\gamma_{a,b}\colon a\otimes b\cong b\otimes a$ satisfying the two hexagon
conditions relating $\gamma$ to $\alpha$."

**Preferred:** state or draw both hexagon diagrams. The definition names
each component and each axiom; the axioms are commutative diagrams, and a
definition either draws them or cites the exact reference where they are
written.

## `AX-2`: An axiom described by shape instead of by equation

"The hexagon conditions", "the pentagon axiom", "the triangle identities" —
the shape name is a mnemonic, not a mathematical condition. The condition
is a commutative diagram or an equation. Use the shape name alongside the
diagram, not in place of it. A reader who does not already know the shape
cannot reconstruct the axiom from its name.

**Banned:** "satisfying the two hexagon conditions relating $\gamma$ to
$\alpha$."

**Preferred:** draw the two hexagon diagrams, or write the equations they
commute. The name "hexagon" may appear as a label; it may not substitute
for the diagram.

## `AX-3`: "relating" an axiom to its components without stating the relation

"relating $\gamma$ to $\alpha$", "commuting with the projections",
"compatible with the tensor product" — each names a relationship without
stating the equation or diagram that expresses it. A definition or theorem
that invokes a relation states the relation: the commutative diagram, the
equation, or the naturality square. "Relating" and "compatible" gesture at
a mathematical statement that is not written.

**Banned:** "satisfying the two hexagon conditions relating $\gamma$ to
$\alpha$."

**Preferred:** state the relation — the hexagon diagrams express that
specific composites of $\gamma$, $\alpha$, and the tensor product's
functoriality are equal. Draw the diagrams or write the equations.

## `AX-4`: A definition that is not self-contained

A definition must be evaluable from the text plus its cited references. A
definition that references axioms by name without stating them and without
citing where they are written in full gives the reader neither the axioms
nor a pointer. The reader cannot determine whether a given object satisfies
the definition. Self-contained does not mean everything is derived from
first principles in one sentence — it means the text or its cited
references supply every component the definition requires.

**Banned:** "A braiding on a monoidal category is a natural isomorphism
$\gamma_{a,b}\colon a\otimes b\cong b\otimes a$ satisfying the two hexagon
conditions relating $\gamma$ to $\alpha$." No diagrams, no citation.

**Preferred:** draw the hexagon diagrams in the definition, or write
"[@MacLane, Chapter VII, (2.1) and (2.2)]" citing the exact diagrams. The
reader follows the citation and finds the axioms; or the reader reads the
diagrams in the text. Either way the definition is evaluable.

## `AX-5`: An axiom named by count without stating or citing the axioms

"The two hexagon conditions", "the three coherence axioms", "the five
simplicial identities" — a count of axioms without stating or citing them
combines AX-1 and AX-2 with a cardinality label. The count tells the reader
how many axioms to imagine without supplying them. Name each axiom, draw
each diagram, or cite the exact reference for all of them. The count is not
a substitute.

**Banned:** "satisfying the two hexagon conditions."

**Preferred:** draw both hexagon diagrams, or cite the reference where both
are written. The reader does not need to be told there are two; the reader
needs to see them.
