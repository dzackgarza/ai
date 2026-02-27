# Evaluator Notes

This file records what to look for; it is not agent-visible.

## Failure Modes

Worst models:

- Paraphrase abstract/intro.
- Produce a generic algebraic-geometry proof outline ("construct compactification", "analyze boundary", "use degeneration") without the paper-specific steps.
- Confidently invent details.

Medium models:

- Correctly locate/cite the main theorem.
- Give a proof "summary" that is mostly a grab-bag of nearby results.
- Miss the critical argument that actually forces the conclusion.

Best models:

- Describe the actual mechanism of the proof.
- Specifically mention:
  - normalization toroidal over cusps 2 and 4
  - semitoroidal over remaining cusps
  - the critical double-curve counting argument

## Scoring Anchors

- 0-2: abstract-only / speculative / wrong.
- ~5: cites the right theorem, but proof description lacks the key mechanism.
- 8-10: includes cusp-by-cusp toroidal/semitoroidal statement + double-curve counting as a real argument.
