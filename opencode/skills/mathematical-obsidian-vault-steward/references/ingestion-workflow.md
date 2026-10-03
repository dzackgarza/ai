# Inbox Source Protocol and Ingestion Workflow

## Inbox Source Protocol

- Treat each inbox file as a source artifact to be mined, not as a note that needs its
  own graph identity.

- The inbox itself may remain inert and ignored by the user; the risk is accidental
  links from permanent notes or MOCs into inbox material.

- The job is to move semantic payload from the inbox into canonical notes, not to make
  inbox files pretty, searchable, or namespace-clean.

- Preserve the original filename of each inbox source.

- The only routine path transitions are `INBOX/<file>` -> `INBOX/.annotated/<file>`
  after the analysis pass, then `INBOX/.annotated/<file>` ->
  `INBOX/.incorporated/<file>` after durable note incorporation.

- A stable source ID belongs in a source record, manifest, or frontmatter field, not as
  a replacement for the original filename.

- Canonical tracking metadata may be added to a markdown source’s YAML frontmatter when
  it preserves the source body intact.
  For non-markdown sources, use a sidecar source record.

- Use CriticMarkup locally at the relevant passage to mark routing, non-import,
  uncertainty, demotion, merge, or objection-resolution suggestions.

- Do not create a durable note merely because an inbox file exists.

- Do not create wiki-links, MOC entries, aliases, or navigation routes pointing at inbox
  sources unless the user explicitly asks for source-visible links.

- Most inbox sources should eventually disappear only after their content has been
  decomposed into durable notes and a human approves deletion.


## Ingestion Workflow

1. **Capture raw source first**

   - Preserve the original text or attachment, filename, and path.

   - Assign a stable source ID in metadata or a source record, not as a forced filename
     replacement.

   - Hash files when practical.

   - Do not paraphrase yet.

2. **Read the source in isolation**

   - Read the source end-to-end before routing its content elsewhere.

   - Process one inbox source at a time.

   - For dense or high-risk sources, spend the time needed for a deep pass rather than
     batching for administrative convenience.

3. **Type the input**

   - Classify modality: text, image, PDF, chat, code, transcript, mixed batch.

   - Classify mathematical role: definition, theorem, proof, example, counterexample,
     calculation, diagram, bibliography, project decision.

   - Assign risk: low, medium, high, critical.

4. **Reconstruct the mathematical story**

   - Identify the objects, claims, corrections, proof ideas, gaps, dead ends, examples,
     computations, diagrams, and review-worthy ambiguities that matter after the whole
     source is read.

   - Distinguish what survived, what failed, what remains conjectural or open, and what
     should be preserved only as warning or provenance.

   - Record source-local locations for passages that change the final mathematical
     state.

   - Do not collapse a whole source into one generic summary note or one mechanical
     ledger.

5. **Extract with fidelity**

   - Normalize formatting only when mathematical meaning is unchanged.

   - Preserve uncertainty explicitly.

   - Use labels like `verbatim`, `normalized`, `ocr-uncertain`, `agent-inferred`,
     `illegible`, `external`.

6. **Search for integration targets**

   - Search exact names, aliases, notation variants, formulas, and nearby MOCs.

   - Inspect backlinks and surrounding notes before creating a new page.

   - Route each extracted unit, not each source file.

   - Existing canonical notes come first.

7. **Choose note granularity**

   - Inline small facts, caveats, proof steps, and local calculations into existing
     notes.

   - Use sections or block references for small but linkable content.

   - Create a new note only when it has a stable independent referent and real future
     retrieval value.

   - If a source only enriches existing notes, do not create a new note for the source
     itself.

8. **Stage source-backed edits**

   - Every durable claim must be traceable to a source record, user assertion, or
     explicitly labeled inference.

9. **Audit mathematical integrity**

   - Check hypotheses, notation, dependencies, examples, ambiguities, and visible gaps.

10. **Integrate into the graph**

- Add meaningful links, aliases, and minimal metadata.

- Update MOCs only when they genuinely improve navigation.

11. **Write back incorporation provenance**

- Use CriticMarkup as local editorial markup, not as a document-level memo.

- Attach short CriticMarkup comments to the exact passage being routed, rejected, or
  flagged.

- Mark local import decisions near the supporting text, e.g. route this paragraph to a
  canonical note, keep this table source-visible, or flag this claim for review.

- If several adjacent sentences share one routing decision, one nearby comment is
  enough; keep it passage-local.

- A comment that says only “accepted target”, “route to note”, or “merge into X” is not
  sufficient. It must identify the mathematical payload, target note or section, action,
  status, and source-grounded reason.

- Do not place a large CriticMarkup summary block at the top of the file.

- Do not use CriticMarkup to replace the extraction ledger or source record; it is a
  local audit trail inside the source.

12. **Retire or preserve dirty sources**

- Do not delete high-risk sources immediately.

- Leave unprocessed sources in `INBOX/`.

- After analysis is complete, move or copy the annotated source to `INBOX/.annotated/`
  while keeping the original filename.

- After durable incorporation is complete and audited, move the source to
  `INBOX/.incorporated/` while keeping the original filename.

- Do not rename or move an inbox source solely to avoid duplicate basenames in Obsidian.

- Moving a source through `.annotated` or `.incorporated` is a lifecycle decision, not a
  semantic rewrite; preserve basename, provenance metadata, and reviewability.

- Delete inbox sources only with explicit human approval after review.

