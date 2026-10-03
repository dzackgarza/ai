# Parentheticals (`PAR-*`)

A semantic parenthetical is a compression. Prefer expansion over compression:
expanding into explicit mathematics is reversible, whereas a compression is
lossy and usually smuggles an undefined term or an unstated theorem.

## `PAR-1`: Compression artifact

Terse to the point of inscrutability, standing in for a notion that needs
spelling out.

**Banned:** "weak homotopy equivalence (holds; inverts/ignores
directionality) versus categorical equivalence (fails; preserves it)."

**Preferred:** expand into prose or a definition that states the
distinction.

## `PAR-2`: Smuggled theorem or equivalence

"(equivalently, $X$)", an "iff" asserted in a parenthesis, often over
undefined terms.

**Banned:** "full and faithful (equivalently, a replete full subcategory)"
— a functor is identified with its essential image and an equivalence is
asserted aside.

**Preferred:** "If $F\colon\mathcal C\to\mathcal D$ is fully faithful, then
$F$ induces an equivalence from $\mathcal C$ to its replete full essential
image in $\mathcal D$." Cite the result and define any term not already
established. A parenthetical that only unfolds the definition of the
term it qualifies asserts no theorem and is `PAR-4`. The expanded statement can later be demoted to a remark, cited
theorem, or footnote.

## `PAR-3`: Smuggled example

"(e.g. …)" carrying a genuine example.

**Banned:** "several distinct lifts (e.g. several monoidal structures on one
category)."

**Preferred:** promote to a first-class example block.

## `PAR-4`: Legitimate qualification

A small, correct, load-bearing modifier that restricts or identifies the
claim. Keep inline.

**Fine as is:** "fibers are (possibly nontrivial) groupoids."; "The map is
finite (equivalently, the target coordinate ring is a finite module over
the source coordinate ring)." The second parenthetical unfolds the
definition of a finite morphism of affine schemes; it asserts no theorem
(`PAR-2`).

**Banned:** "The map is finite (and this is important, as we will see
below)."

A parenthetical that only announces future explanation, motivation, or
emphasis is padding (`PAR-5`). Move its mathematical content into the
main sentence or delete it.

## `PAR-5`: Padding or tangent

Carries no load.

**Preferred:** delete. A parenthetical is usually wrong when it is a
tangent.
