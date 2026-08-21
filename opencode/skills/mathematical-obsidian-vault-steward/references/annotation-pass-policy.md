# Annotation-Pass Policy

Binding constraints for analysis-pass and CriticMarkup work on inbox sources.
Load together with `inbox-analysis-pass.md` before annotating any source.

- A shallow annotated source is worse than no annotated source.
  If the agent cannot reconstruct the mathematical story and route its durable insights,
  add local CriticMarkup at the unresolved passages and leave the source for another
  direct pass.

- An analysis-pass artifact must be a full annotated copy of the source body.
  A synthesized memo, routing ledger, progress summary, or selected-excerpt report
  cannot replace or supplement missing passage-local analysis.

- Create text/markdown analysis artifacts by copying the raw source first, then
  inserting CriticMarkup into the copied source.
  Do not regenerate the source body from model output.

- A complete rewrite is not source preservation, even if the rewrite is semantically
  faithful. The analysis pass edits a source copy; it does not author a replacement
  document.

- Preserve the source body literally during analysis.
  Insert CriticMarkup only where it is anchored to the supporting passage; do not
  reflow, normalize, repair markdown, or clean up the source text.

- Do not perform cosmetic cleanup after semantic insertions.
  Extra blank lines, local spacing oddities, and inherited escaping are not blockers.
  If an edit accidentally inserts a literal artifact, fix only that exact artifact and
  do not touch headings or surrounding source text while doing so.

- When replacing a local block to add CriticMarkup, copy the existing source lines
  verbatim from the current artifact.
  After the edit, inspect the diff for the artifact; any non-CriticMarkup source-line
  change, including quote marks, dashes, Unicode, formula text, citation escaping, or
  punctuation, is source-body damage to repair before continuing.

- Prefer exact local replacement of adjacent source text over line-number range edits.
  Use literal matching for these replacements.
  Do not use regex mode, wildcard spans such as `.*`, anchors, capture groups, or
  backreferences to insert CriticMarkup.
  If inserting a comment requires line arithmetic, regex surgery, or regenerating source
  lines from memory, leave the passage unresolved instead of risking source-body damage.

- Ground analysis in the raw source and durable vault notes.
  Do not imitate prior processed copies or use them as format examples.

- Treat old annotated, processed, incorporated, and scratch lifecycle artifacts as
  quarantined evidence.
  Do not read them to learn what to annotate, how to format comments, or whether work is
  complete. When explicitly continuing a current `.annotated` work surface, read it only
  as the artifact to assess and edit, and verify its claims against the raw source and
  durable vault notes.
  When explicitly redoing from raw, copy the raw source over the analysis surface before
  semantic work.

- A routing target is not verified until the actual note path and, when used, the exact
  displayed heading or block anchor exist.
  Never use shorthand such as “same note” in CriticMarkup; repeat the real target or
  mark the anchor proposed.

- Never treat hashes, file existence, candidate target lists, or another agent’s
  completion report as evidence that semantic extraction happened.

- Never append handoffs, progress summaries, routing ledgers, completion notes, or
  status claims to an annotated source.
  Later agents must inspect the source and local CriticMarkup directly.

- Never add a source-level or `locator: entire source` CriticMarkup comment.
  If a whole-source synthesis matters, distribute it to the passages whose later
  corrections, retractions, or proof obligations support it.

- Every routing comment must have explicit labeled `route:`, `unit:`, `status:`,
  `action:`, `reason:`, and `locator:` fields.
  Do not bury the action or reason inside free prose.

- `route:` means the durable vault target whose update, rejection, or source-visible
  preservation is being proposed.
  Never route to another source turn, another annotation, a line number, or “the
  expanded annotation”; for repeated or superseded passages, repeat the same durable
  vault target and put supersession in `status:` and `reason:`.

- This is not a coverage exercise.
  Prefer one coherent source segment annotated deeply over a whole document covered by
  broad duplicate, superseded, or already-covered comments.

- When many broad annotations remain, handle one coherent source segment only.
  Do not plan or attempt a whole-file cleanup pass.
  Choose one turn, section, paragraph cluster, or claim family and improve it enough
  that a later direct pass can continue from the artifact itself.
  For Roman-numeral source sections, one section is the maximum normal pass size.
  After a coherent improvement inside the chosen segment, do not edit a second segment
  in the same source; leave similar defects visible as future continuation state.

- A structured turn with multiple numbered items, Roman-numeral sections, bold item
  labels, or theorem-like claims needs one local CriticMarkup comment per handled
  internal item. A single comment may cover only an unstructured paragraph cluster with
  one mathematical payload.
  If you cannot handle the internal items, leave the rest untouched for a later direct
  pass.

- Leaving work for later means literally leaving the unhandled source passage without a
  synthetic coverage comment.
  A turn-level `duplicate`, `superseded`, `already covered`, or
  `preserve-source-visible` comment on a structured claim list is not honest partial
  progress; it is broad coverage slop that a later pass must remove, replace, or refine
  beside the internal units.

- There is no same-target exception to the internal-item rule.
  If a Roman-numeral section or bold-labeled list contains several visible claims that
  would all route to the same durable note, either annotate the handled claims beside
  their own list items or leave the unhandled claims without an umbrella comment.

- `duplicate` is still semantic routing, not a shortcut.
  A duplicate or preserve-source-visible comment may use one `route:` only for the
  internal item it is attached to.
  Do not keep a section-level duplicate comment on a visible claim list by calling the
  section homogeneous.
  If a section mixes branch-curve geometry with KSBA stability, cusps with semifan proof
  obligations, comparison claims with IAS construction, or arithmetic setup with lattice
  identity, split the source passage at its internal paragraph, bullet, or bold-item
  boundaries and route each unit to the actual target.
