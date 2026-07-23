# Mathematical Note Taxonomy

Unit-labeling rules for durable notes and CriticMarkup `unit:` fields.
See `mathematical-unit-library.md` for the canonical callout vocabulary.

- Use **mathematical** note types and callout vocabulary, not software-engineering
  status language.

- Preferred primary types include: `theorem`, `lemma`, `proposition`, `corollary`,
  `definition`, `construction`, `proof`, `proof-sketch`, `example`, `counterexample`,
  `calculation`, `computation`, `fact`, `question`, `conjecture`, `problem`, `notation`,
  and `remark`.

- Use [[obsidian/SKILL|Obsidian]] callouts for every formal mathematical unit except `remark`. Remarks
  should usually be ordinary top-level prose in papers and notes, not `> [!remark]`
  boxes.

- Choose the strongest mathematically correct label:

  - named lattice, group, divisor, moduli space, notation, or standing equivalence
    introduced for future use -> `definition`

  - unproved theorem-like claim -> `conjecture`

  - unresolved problem or criterion question -> `question`

  - established rule, criterion, implication, equivalence, or if-and-only-if statement
    that is not the main theorem -> `proposition`

  - recipe, quotient, disjoint union, normalization, family, package, model,
    construction step, construction requirement, or procedure to build -> `construction`

  - small assertion about an already-defined object -> `fact`

  - contextual explanation or non-assertive framing -> `remark`

  - exact formal statement with proof elsewhere -> theorem/lemma/proposition/corollary
    as appropriate

- Do not use `fact` for the act of defining a named object or specifying a construction
  step/requirement; use `definition` or `construction`.

- The target note’s current proof-status framing overrides source labels.
  If the target note frontmatter/tags/type, callout, or heading frames a theorem-shaped
  source item as `conjecture`, proposed, open, or “why this is a conjecture”, use
  `conjecture` or `question`, not `proposition`, even when the source label says
  “Theorem Statement”.

- If the target note records an item as a checklist, proof obligation, verification
  still needing proof, or migrated research claim awaiting corroboration, do not label
  the source assertion as `fact` merely because the source states it declaratively.
  Use `question` with `status: open` for obligations to prove or verify, or `conjecture`
  with `status: conjectural` for intended theorem-like claims.

- A claim can be already present in the vault and still be conjectural or open.
  When choosing the single `status:` value, prefer the mathematical proof status
  (`conjectural`, `open`, `disputed`, `needs-human`) over `duplicate` whenever the
  target section says the claim is pending verification, conjectural, or still needs
  proof. Put “already recorded in the target” in the `reason:` instead.

- When refining old annotations, do not preserve their `unit:` labels by inertia.
  Reclassify every visible source item from the source text itself.
  A unit is not `remark` merely because the incorporation edit will be prose rather than
  a callout.

- Before leaving a handled segment, audit every CriticMarkup comment in that source
  segment, including comments that were already present.
  If the source label names a lattice, group, divisor, moduli space, cusp pair,
  admissibility criterion, stratum, quotient, normalization, trace rule, family, model,
  construction step, or construction requirement, use `definition` or `construction`
  instead of `fact`. If the source label or sentence states a rule, criterion,
  implication, equivalence, or if-and-only-if claim, use `proposition` only when
  established and `conjecture` or `question` when unresolved or target-framed as
  proposed; do not demote it to `remark` because the passage is duplicate.
  Fixing a local misclassified unit is valid loop progress.

- If a comment reason names an existing target section as the place where the payload
  already lives, the `route:` link should include that verified `#Heading`; otherwise
  omit the section claim or mark the section as proposed.

- CriticMarkup `reason:` fields should explain source/vault semantics only.
  Do not mention that a comment was split from an umbrella, that a previous annotation
  existed, that another agent missed it, or that “this pass” changed it.

- If a note contains both a construction and an unresolved theorem about it, label the
  note by its main mathematical role and state the unresolved theorem separately as a
  `conjecture` or `question`.

- Do **not** use fuzzy labels such as `open issue`, `framework`,
  `programmatic framework`, `target theorem`, `not yet settled`,
  `safe interim definition`, or similar as the primary mathematical status of a note.

- Do **not** use software-engineering metadata like `issue` as the mathematical type of
  a note.

- When a claim is unproved but intended to be true, say `conjecture`.

- When a note asks what the right statement/criterion is, say `question`.

- When a note gives the object to take but leaves verification open, say `construction`
  and then list the remaining conjectures/questions explicitly.

- See `references/mathematical-unit-library.md` for the canonical callout vocabulary and
  routing rules.

