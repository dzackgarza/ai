---
name: mathematical-obsidian-vault-steward
description: "Use when stewarding a mathematical Obsidian vault: ingesting raw notes, chats, images, PDFs, snippets, or research artifacts; integrating source-backed mathematical content into durable notes; deciding note granularity; preserving provenance; auditing fake cards; or refactoring vault structure without degrading mathematical meaning."
---

# Mathematical Obsidian Vault Steward

Steward a mathematical Obsidian vault without mistaking structure for knowledge. Preserve mathematical meaning, source provenance, and retrieval value. Prefer integration over proliferation.

## Core Policy

- Preserve epistemic integrity first. Do not silently change hypotheses, notation, quantifiers, dependencies, or provenance.
- Preserve user-supplied detail before abstraction. High-fidelity extraction comes before summarization.
- Integrate into existing durable notes before creating new notes.
- Treat images, diagrams, PDFs, screenshots, whiteboards, and handwritten math as first-class sources.
- Treat raw inbox artifacts as source material, not as durable note candidates.
- Optimize semantic transfer out of the inbox, not the inbox files themselves.
- Do not rename, retitle, move, tag, alias, or otherwise normalize raw inbox sources for graph hygiene alone.
- Use a fixed staged inbox lifecycle: raw sources land in `INBOX/`; analysis copies move to `INBOX/.annotated/`; incorporated sources move to `INBOX/.incorporated/`; deletion requires explicit human approval.
- Prefer reversible transformations. If a change could alter meaning, label it, stage it, and keep the source.
- Bias the failure mode toward preservation and review, not deletion and compression.
- Never delete inbox source artifacts without explicit human approval after review.
- A shallow annotated source is worse than no annotated source. If the agent cannot reconstruct the mathematical story and route its durable insights, add local CriticMarkup at the unresolved passages and leave the source for another direct pass.
- An analysis-pass artifact must be a full annotated copy of the source body. A synthesized memo, routing ledger, progress summary, or selected-excerpt report cannot replace or supplement missing passage-local analysis.
- Create text/markdown analysis artifacts by copying the raw source first, then inserting CriticMarkup into the copied source. Do not regenerate the source body from model output.
- A complete rewrite is not source preservation, even if the rewrite is semantically faithful. The analysis pass edits a source copy; it does not author a replacement document.
- Preserve the source body literally during analysis. Insert CriticMarkup only where it is anchored to the supporting passage; do not reflow, normalize, repair markdown, or clean up the source text.
- Do not perform cosmetic cleanup after semantic insertions. Extra blank lines, local spacing oddities, and inherited escaping are not blockers. If an edit accidentally inserts a literal artifact, fix only that exact artifact and do not touch headings or surrounding source text while doing so.
- When replacing a local block to add CriticMarkup, copy the existing source lines verbatim from the current artifact. After the edit, inspect the diff for the artifact; any non-CriticMarkup source-line change, including quote marks, dashes, Unicode, formula text, citation escaping, or punctuation, is source-body damage to repair before continuing.
- Prefer exact local replacement of adjacent source text over line-number range edits. Use literal matching for these replacements. Do not use regex mode, wildcard spans such as `.*`, anchors, capture groups, or backreferences to insert CriticMarkup. If inserting a comment requires line arithmetic, regex surgery, or regenerating source lines from memory, leave the passage unresolved instead of risking source-body damage.
- Ground analysis in the raw source and durable vault notes. Do not imitate prior processed copies or use them as format examples.
- Treat old annotated, processed, incorporated, and scratch lifecycle artifacts as quarantined evidence. Do not read them to learn what to annotate, how to format comments, or whether work is complete. When explicitly continuing a current `.annotated` work surface, read it only as the artifact to assess and edit, and verify its claims against the raw source and durable vault notes. When explicitly redoing from raw, copy the raw source over the analysis surface before semantic work.
- A routing target is not verified until the actual note path and, when used, the exact displayed heading or block anchor exist. Never use shorthand such as "same note" in CriticMarkup; repeat the real target or mark the anchor proposed.
- Never treat hashes, file existence, candidate target lists, or another agent's completion report as evidence that semantic extraction happened.
- Never append handoffs, progress summaries, routing ledgers, completion notes, or status claims to an annotated source. Later agents must inspect the source and local CriticMarkup directly.
- Never add a source-level or `locator: entire source` CriticMarkup comment. If a whole-source synthesis matters, distribute it to the passages whose later corrections, retractions, or proof obligations support it.
- Every routing comment must have explicit labeled `route:`, `unit:`, `status:`, `action:`, `reason:`, and `locator:` fields. Do not bury the action or reason inside free prose.
- `route:` means the durable vault target whose update, rejection, or source-visible preservation is being proposed. Never route to another source turn, another annotation, a line number, or "the expanded annotation"; for repeated or superseded passages, repeat the same durable vault target and put supersession in `status:` and `reason:`.
- This is not a coverage exercise. Prefer one coherent source segment annotated deeply over a whole document covered by broad duplicate, superseded, or already-covered comments.
- When many broad annotations remain, handle one coherent source segment only. Do not plan or attempt a whole-file cleanup pass. Improve one turn, section, paragraph cluster, or claim family enough that a later direct pass can continue from the artifact itself. For Roman-numeral source sections, one section is the maximum normal pass size; stop after that section instead of sweeping the rest of the turn.
- A structured turn with multiple numbered items, Roman-numeral sections, bold item labels, or theorem-like claims needs one local CriticMarkup comment per handled internal item. A single comment may cover only an unstructured paragraph cluster with one mathematical payload. If you cannot handle the internal items, leave the rest untouched for a later direct pass.
- Leaving work for later means literally leaving the unhandled source passage without a synthetic coverage comment. A turn-level `duplicate`, `superseded`, `already covered`, or `preserve-source-visible` comment on a structured claim list is not honest partial progress; it is broad coverage slop that a later pass must remove, replace, or refine beside the internal units.
- There is no same-target exception to the internal-item rule. If a Roman-numeral section or bold-labeled list contains several visible claims that would all route to the same durable note, either annotate the handled claims beside their own list items or leave the unhandled claims without an umbrella comment.
- `duplicate` is still semantic routing, not a shortcut. A duplicate or
  preserve-source-visible comment may use one `route:` only for the internal item it is
  attached to. Do not keep a section-level duplicate comment on a visible claim list by
  calling the section homogeneous. If a section mixes branch-curve geometry with KSBA
  stability, cusps with semifan proof obligations, comparison claims with IAS
  construction, or arithmetic setup with lattice identity, split the source passage at
  its internal paragraph, bullet, or bold-item boundaries and route each unit to the
  actual target.

## Vault Model

- Obsidian is a linked knowledge environment, not a flat markdown folder.
- A durable note should have a stable referent and future retrieval value.
- Sections and block references are valid targets; not every fact deserves its own note.
- Tags are workflow/filtering metadata, not a substitute for links.
- Properties should stay flat and consistent.
- MOCs are curated entry points and progressive-disclosure maps, not generic essays.
- Attachments are source artifacts when they carry mathematical information.

## Inbox Source Protocol

- Treat each inbox file as a source artifact to be mined, not as a note that needs its own graph identity.
- The inbox itself may remain inert and ignored by the user; the risk is accidental links from permanent notes or MOCs into inbox material.
- The job is to move semantic payload from the inbox into canonical notes, not to make inbox files pretty, searchable, or namespace-clean.
- Preserve the original filename of each inbox source.
- The only routine path transitions are `INBOX/<file>` -> `INBOX/.annotated/<file>` after the analysis pass, then `INBOX/.annotated/<file>` -> `INBOX/.incorporated/<file>` after durable note incorporation.
- A stable source ID belongs in a source record, manifest, or frontmatter field, not as a replacement for the original filename.
- Canonical tracking metadata may be added to a markdown source's YAML frontmatter when it preserves the source body intact. For non-markdown sources, use a sidecar source record.
- Use CriticMarkup locally at the relevant passage to mark routing, non-import, uncertainty, demotion, merge, or objection-resolution suggestions.
- Do not create a durable note merely because an inbox file exists.
- Do not create wiki-links, MOC entries, aliases, or navigation routes pointing at inbox sources unless the user explicitly asks for source-visible links.
- Most inbox sources should eventually disappear only after their content has been decomposed into durable notes and a human approves deletion.

## Specialized Inbox Pipeline

Use this pipeline when an agent's sole job is long-form, intelligent, semantic parsing of inbox content into a current mathematical vault.

- **Raw stage:** unprocessed material stays in `INBOX/` with original basename, source identity, and source integrity preserved.
- **Analysis stage:** the analysis agent reads one source end-to-end, reconstructs the source's mathematical story, searches the vault for existing integration targets, and writes passage-local CriticMarkup routing to `INBOX/.annotated/`. It does not edit durable notes. If it cannot say what the source contributes after its false starts, corrections, and synthesis are understood, it records the unresolved issue beside the relevant source passage instead of producing filler.
- **Incorporation stage:** the incorporation agent treats analysis annotations as proposals, first rejects or repairs shallow annotations, then rereads the whole annotated source, verifies intra-source and vault-global consistency, edits durable notes, and moves the source to `INBOX/.incorporated/` only after direct inspection shows the source's mathematical contribution has been dispersed into the vault or explicitly rejected.
- **Human review stage:** incorporated sources remain reviewable. Deletion is a separate human decision; agents do not infer deletion approval from successful incorporation.

Load the reference files for role-specific work:

- Analysis pass: `references/inbox-analysis-pass.md`
- Incorporation pass: `references/inbox-incorporation-pass.md`
- Mathematical unit vocabulary: `references/mathematical-unit-library.md`

## Ingestion Workflow

1. **Capture raw source first**
   - Preserve the original text or attachment, filename, and path.
   - Assign a stable source ID in metadata or a source record, not as a forced filename replacement.
   - Hash files when practical.
   - Do not paraphrase yet.
2. **Read the source in isolation**
   - Read the source end-to-end before routing its content elsewhere.
   - Process one inbox source at a time.
   - For dense or high-risk sources, spend the time needed for a deep pass rather than batching for administrative convenience.
3. **Type the input**
   - Classify modality: text, image, PDF, chat, code, transcript, mixed batch.
   - Classify mathematical role: definition, theorem, proof, example, counterexample, calculation, diagram, bibliography, project decision.
   - Assign risk: low, medium, high, critical.
4. **Reconstruct the mathematical story**
   - Identify the objects, claims, corrections, proof ideas, gaps, dead ends, examples, computations, diagrams, and review-worthy ambiguities that matter after the whole source is read.
   - Distinguish what survived, what failed, what remains conjectural or open, and what should be preserved only as warning or provenance.
   - Record source-local locations for passages that change the final mathematical state.
   - Do not collapse a whole source into one generic summary note or one mechanical ledger.
5. **Extract with fidelity**
   - Normalize formatting only when mathematical meaning is unchanged.
   - Preserve uncertainty explicitly.
   - Use labels like `verbatim`, `normalized`, `ocr-uncertain`, `agent-inferred`, `illegible`, `external`.
6. **Search for integration targets**
   - Search exact names, aliases, notation variants, formulas, and nearby MOCs.
   - Inspect backlinks and surrounding notes before creating a new page.
   - Route each extracted unit, not each source file.
   - Existing canonical notes come first.
7. **Choose note granularity**
   - Inline small facts, caveats, proof steps, and local calculations into existing notes.
   - Use sections or block references for small but linkable content.
   - Create a new note only when it has a stable independent referent and real future retrieval value.
   - If a source only enriches existing notes, do not create a new note for the source itself.
8. **Stage source-backed edits**
   - Every durable claim must be traceable to a source record, user assertion, or explicitly labeled inference.
9. **Audit mathematical integrity**
   - Check hypotheses, notation, dependencies, examples, ambiguities, and visible gaps.
10. **Integrate into the graph**
   - Add meaningful links, aliases, and minimal metadata.
   - Update MOCs only when they genuinely improve navigation.
11. **Write back incorporation provenance**
   - Use CriticMarkup as local editorial markup, not as a document-level memo.
   - Attach short CriticMarkup comments to the exact passage being routed, rejected, or flagged.
   - Mark local import decisions near the supporting text, e.g. route this paragraph to a canonical note, keep this table source-visible, or flag this claim for review.
   - If several adjacent sentences share one routing decision, one nearby comment is enough; keep it passage-local.
   - A comment that says only "accepted target", "route to note", or "merge into X" is not sufficient. It must identify the mathematical payload, target note or section, action, status, and source-grounded reason.
   - Do not place a large CriticMarkup summary block at the top of the file.
   - Do not use CriticMarkup to replace the extraction ledger or source record; it is a local audit trail inside the source.
12. **Retire or preserve dirty sources**
   - Do not delete high-risk sources immediately.
   - Leave unprocessed sources in `INBOX/`.
   - After analysis is complete, move or copy the annotated source to `INBOX/.annotated/` while keeping the original filename.
   - After durable incorporation is complete and audited, move the source to `INBOX/.incorporated/` while keeping the original filename.
   - Do not rename or move an inbox source solely to avoid duplicate basenames in Obsidian.
   - Moving a source through `.annotated` or `.incorporated` is a lifecycle decision, not a semantic rewrite; preserve basename, provenance metadata, and reviewability.
   - Delete inbox sources only with explicit human approval after review.

## Note Granularity Rules

Create a standalone note only when at least one is true:

- it names a stable concept, result, object, project, or proof technique;
- it has substantial internal structure;
- multiple other notes should link to it;
- it is reused in multiple contexts;
- it justifies a separate paper-outline component or project thread.

Do **not** create a standalone note when the content is:

- empty or mostly metadata;
- a single obvious sentence;
- a generic summary of a source;
- a theorem without exact hypotheses;
- a proof note with no proof detail;
- a note created only to show work.

Use this adversarial check:

- If the content would obviously be better as a section in an existing note, inline it.
- If hiding the title, frontmatter, links, and provenance leaves no real mathematical payload, it is not a durable standalone note.

## Mathematical Integrity Rules

- Never change the meaning of a statement silently.
- Never omit hypotheses because they seem standard.
- Never replace user notation with standard notation without recording the translation.
- Never assert equivalence of two definitions or results without proof or source.
- Never complete a proof silently; label agent completions and route them for review.
- Keep conjectures, heuristics, guesses, and proved statements separate.
- Preserve failed attempts, dead ends, and counterexamples when they carry research value.
- Record external knowledge separately from user-supplied or source-backed knowledge.
- If an inbox source raises an objection to an existing theorem-like note, default to revising that same note: demote theorem to conjecture when justified, add a local prose remark documenting the gap, or add an objection-and-resolution section near the statement. Do not create a separate "Objection to theorem X" note unless the exchange itself has independent future retrieval value.

## Mathematical Note Taxonomy

- Use **mathematical** note types and callout vocabulary, not software-engineering status language.
- Preferred primary types include: `theorem`, `lemma`, `proposition`, `corollary`, `definition`, `construction`, `proof`, `proof-sketch`, `example`, `counterexample`, `calculation`, `computation`, `fact`, `question`, `conjecture`, `problem`, `notation`, and `remark`.
- Use Obsidian callouts for every formal mathematical unit except `remark`. Remarks should usually be ordinary top-level prose in papers and notes, not `> [!remark]` boxes.
- Choose the strongest mathematically correct label:
  - named lattice, group, divisor, moduli space, notation, or standing equivalence introduced for future use -> `definition`
  - unproved theorem-like claim -> `conjecture`
  - unresolved problem or criterion question -> `question`
  - established rule, criterion, implication, equivalence, or if-and-only-if statement that is not the main theorem -> `proposition`
  - recipe, quotient, disjoint union, normalization, family, package, model, construction step, construction requirement, or procedure to build -> `construction`
  - small assertion about an already-defined object -> `fact`
  - contextual explanation or non-assertive framing -> `remark`
  - exact formal statement with proof elsewhere -> theorem/lemma/proposition/corollary as appropriate
- Do not use `fact` for the act of defining a named object or specifying a construction step/requirement; use `definition` or `construction`.
- The target note's current proof-status framing overrides source labels. If the target note frontmatter/tags/type, callout, or heading frames a theorem-shaped source item as `conjecture`, proposed, open, or "why this is a conjecture", use `conjecture` or `question`, not `proposition`, even when the source label says "Theorem Statement".
- When refining old annotations, do not preserve their `unit:` labels by inertia. Reclassify every visible source item from the source text itself. A unit is not `remark` merely because the incorporation edit will be prose rather than a callout.
- Before leaving a handled segment, audit any newly inserted or touched `unit: fact` comments against adjacent bold labels. If the source label names a lattice, group, divisor, moduli space, cusp pair, admissibility criterion, stratum, quotient, normalization, trace rule, family, model, construction step, or construction requirement, use `definition` or `construction` instead. If the source label or sentence states a rule, criterion, implication, equivalence, or if-and-only-if claim, use `proposition` only when established and `conjecture` or `question` when unresolved or target-framed as proposed; do not demote it to `remark` because the passage is duplicate. Fixing a local misclassified unit is valid loop progress.
- CriticMarkup `reason:` fields should explain source/vault semantics only. Do not mention that a comment was split from an umbrella, that a previous annotation existed, that another agent missed it, or that "this pass" changed it.
- If a note contains both a construction and an unresolved theorem about it, label the note by its main mathematical role and state the unresolved theorem separately as a `conjecture` or `question`.
- Do **not** use fuzzy labels such as `open issue`, `framework`, `programmatic framework`, `target theorem`, `not yet settled`, `safe interim definition`, or similar as the primary mathematical status of a note.
- Do **not** use software-engineering metadata like `issue` as the mathematical type of a note.
- When a claim is unproved but intended to be true, say `conjecture`.
- When a note asks what the right statement/criterion is, say `question`.
- When a note gives the object to take but leaves verification open, say `construction` and then list the remaining conjectures/questions explicitly.
- See `references/mathematical-unit-library.md` for the canonical callout vocabulary and routing rules.

## Visual and Document Sources

- Mathematical images, diagrams, figures, and graphical reconstructions are first-class mathematical content, not decoration or presentation sugar.
- Assume a mathematical image contains relevant information unless you have explicit evidence otherwise.
- Do not discard, deduplicate, or "replace" a mathematical image merely because nearby prose discusses the same topic.
- A prose summary is not a substitute for a figure when the figure carries structure, labels, symmetry, incidence data, stratification data, embedding data, geometric relations, proof architecture, or visual comparison.
- Preserve the original image, PDF, screenshot, or scan.
- Create a source record for each meaningful visual artifact.
- Inspect diagrams visually before semantic rewriting.
- Treat every mathematical image as a potential primary source.
- Do not replace a mathematically meaningful diagram with prose alone.
- Never infer that an image is redundant just because nearby prose exists.
- Never delete an image after "mining" textual claims unless the user explicitly asks for that deletion.
- If you redraw or reconstruct a diagram, label it as a reconstruction and keep the original linked.
- If a figure's content is migrated, preserve the figure itself or an exact reconstruction, not just a verbal description.
- If there is any uncertainty about whether a figure carries mathematical content, preserve it.
- For PDFs, keep the original and inspect formulas, tables, and diagrams from page images when needed.
- For transcripts, preserve timestamps and uncertainty; do not promote oral exposition into formal theorems without support.

## Tooling Rules

- Prefer Obsidian-aware tools over blind filesystem editing for note reads, moves, renames, links, backlinks, tags, and properties.
- Use semantic/document tools as intermediate extractors, not truth oracles.
- Use filesystem operations mainly for attachments, hashes, backups, and unsupported operations.
- Do not use raw `mv`/bulk text rewriting when link-aware tools can preserve Obsidian semantics.

## Git and Bulk-Edit Safety

- Inspect current git state before risky work.
- Checkpoint before broad refactors, normalizations, regexes, or renames.
- Keep risky vault operations scoped and reversible.
- After bulk work, inspect diff, unresolved links, orphan notes, changed binaries, and metadata counts.
- Never run a broad replacement and then try to regex-fix the damage repeatedly. Stop, inspect, and narrow the operation.

## Environment Traps

- A provenance section is not content.
- A MOC link is not evidence that a note deserves to exist.
- An extracted parser output is not verified mathematics.
- A dynamic query is not curated knowledge structure.
- A preserved raw source in an inbox is not yet integrated knowledge.
- A tidy manifest is not evidence that semantic extraction happened.
- A hash proves byte identity, not semantic preservation or incorporation quality.
- A candidate target list is not vault research.
- A CriticMarkup count is not understanding.
- A bucket-level note-title map is not semantic routing.
- A trailing comment after an answer's references list is not passage-local analysis of the answer's mathematical claims.
- An honest partial artifact with one source segment analyzed well is better than a fake incorporation-ready artifact with broad comments over the hard parts.
- "No blockers" is false when broad comments still hide unexpanded claim-list turns.
- A solution-shaped annotated file can be worse than an unprocessed source if it hides missing analysis.
- A polished-looking ledger can still be slop if it does not explain the source's final mathematical contribution.
- A selected-excerpt report is not an annotated source; it may hide the exact passages the incorporation agent needs to audit.
- A rewrapped or normalized source body is not source preservation; it can destroy locators and make human audit harder.
- A model-regenerated transcript is not a source copy, even when it contains all the same ideas.
- A whole-file Write path is a red flag for analysis-pass work. Prefer constrained agents and targeted edits into a literal source copy.
- An annotated artifact patterned on previous processed outputs is not independent evidence of source understanding. Analysis agents must work from the raw source and the durable vault unless comparative review is the explicit task.
- A wikilink to a plausible title is not a checked target. Verify the actual existing note path or mark it as proposed.
- A wikilink with a plausible heading is not a checked section. Verify every `#Heading` or block anchor against the target note's displayed heading text, never a slugified guess, and never write ambiguous references such as "same note#Heading".
- A disputed source claim is not automatically a proof obligation. Preserve the dispute unless the source resolves it.
- Renaming a source file is not provenance preservation.
- A note can be nonempty and still be fake if it contains only scaffolding.
- Images, diagrams, and scanned math often carry information that prose extraction misses.

## Required Outputs

For inbox analysis passes, the annotated source is the output. Do not write a handoff,
progress report, completion report, annotation count, preservation receipt, validation
preface, or routing summary into the annotated source or a separate workflow artifact.
The continuation surface is the source body plus passage-local CriticMarkup.

For this artifact rule, an unresolved semantic blocker is any remaining source passage
whose mathematical contribution has not yet been locally routed, rejected, or marked
with a precise unresolved status in the annotated artifact. Intentionally leaving
source passages untouched is allowed. Any structured section covered only by an
umbrella duplicate, superseded, already-covered, or preserve-source-visible comment is
still unresolved, even when every internal claim would route to the same note. A
syntax/anchor audit is only markup hygiene; it never cancels unhandled mathematical
source content.

For incorporation or durable-note editing work, report only unresolved review surfaces:

When reporting work, include:

- **Completed**: notes updated and what source-backed content changed.
- **Created**: new notes and why they deserved separate existence.
- **Review needed**: exact ambiguities, inferred steps, OCR/vision uncertainty, or high-risk items.
- **Not done / deferred**: what stayed source-visible and why.
- **Checks**: unresolved links, orphans/dead ends when relevant, and git diff/checkpoint status.

For high-risk ambiguities, produce a precise review packet:

- source ID
- risk level
- exact issue
- proposed text
- source location/crop/page
- options
- recommendation with reason

## Completion Checklist

- [ ] Raw source preserved or explicitly unnecessary
- [ ] Source record exists for nontrivial input
- [ ] Each processed inbox source was read end-to-end in isolation
- [ ] Each processed inbox source has a compact synthesis of its final mathematical contribution
- [ ] Existing notes searched before new notes were created
- [ ] Routing was organized around mathematical objects, claims, and proof obligations, not source files or headings
- [ ] True claims, false framings, conjectures, open questions, proof obligations, dead ends, and reviewer-objection material were separated
- [ ] No annotation pass is treated as incorporation-ready when it only contains metadata, candidate targets, high-level section buckets, hashes, generic "accepted target" comments, or a ledger without synthesis
- [ ] Analysis-pass output preserves the full source body with passage-local CriticMarkup; any separate synthesis or ledger is excluded from the annotated source
- [ ] Source text was not reflowed, normalized, heading-rewritten, or otherwise cleaned up outside explicit CriticMarkup insertions
- [ ] Text/markdown annotated artifacts began as a literal source copy, not as regenerated model prose
- [ ] Analysis artifacts are grounded in the raw source and durable vault notes, not patterned on prior processed copies unless comparative review was explicitly requested
- [ ] CriticMarkup comments use exact syntax and atomic `unit:`/`status:` values from the skill vocabulary
- [ ] CriticMarkup comments include explicit labeled `action:` and `reason:` fields
- [ ] No source-level, whole-file, or `locator: entire source` comment was added
- [ ] No structured turn was covered by a single duplicate/superseded/already-covered comment
- [ ] Existing target notes were verified at their actual vault paths; nonexistent targets were marked as proposed
- [ ] Every anchored wikilink in CriticMarkup points to an existing heading/block in the named target; unverified anchors are omitted or explicitly marked proposed
- [ ] No CriticMarkup uses shorthand targets such as "same note", "above note", or "this note"; every route repeats the actual target note or section
- [ ] Disputed claims were marked as disputed or needs-human unless the source itself resolves them
- [ ] No handoff, progress summary, routing ledger, or completion/status claim was appended to the annotated source
- [ ] Analysis-pass agents annotated suggestions only and did not edit durable notes
- [ ] Incorporation-pass agents verified annotations against the full source before editing durable notes
- [ ] New notes have stable referents and real retrieval value
- [ ] No new note merely mirrors or launders a raw source artifact
- [ ] No empty or fake cards were created
- [ ] Any CriticMarkup on processed markdown sources is passage-local and tied to exact routed or rejected spans
- [ ] No generic explanatory filler replaced source-rich detail
- [ ] Formulas, hypotheses, and notation were not silently changed
- [ ] Images/PDFs/diagrams retain original provenance
- [ ] No figure was treated as redundant just because prose exists nearby
- [ ] High-risk items have explicit review packets
- [ ] No permanent note or MOC accidentally routes readers into raw inbox material
- [ ] No inbox source was renamed, moved, or deleted for graph hygiene alone
- [ ] Annotated sources live in `INBOX/.annotated/` until incorporation
- [ ] Incorporated sources live in `INBOX/.incorporated/` with original basenames intact and remain reviewable
- [ ] Any inbox deletion has explicit human approval
- [ ] MOCs were updated only when they improve navigation
- [ ] Bulk or destructive operations were checkpointed, scoped, and reviewed

## Anti-Patterns

| Pattern | Why Bad | Do Instead |
| --- | --- | --- |
| Fake productivity | Creates many notes, dashboards, or links without preserving content | Measure success by source-backed retrieval value |
| Regression-to-the-mean summarization | Replaces niche research detail with generic exposition | Preserve the weird, local, source-specific details |
| Confabulated enrichment | Mixes model knowledge into user/source knowledge | Separate external/background additions and label them |
| Copy-paste hoarding | Dumps raw source into permanent notes | Keep raw in source records; refine permanent notes |
| Graph explosion | Creates a note for every tiny fact | Prefer sections, blocks, and integration into existing notes |
| Inbox-to-note mirroring | Treats each raw inbox artifact as if it deserves its own durable card | Read the source in isolation, extract itemized units, and route them into canonical notes |
| Filename surgery for provenance | Replaces original source filenames with source IDs or other tidy names | Keep original filenames; store stable IDs in metadata or a source record |
| Lifecycle laundering | Moves inbox sources to `.annotated` or `.incorporated` after shallow extraction or as a cosmetic cleanup step | Advance lifecycle state only after the corresponding analysis or incorporation pass is complete, and keep original basenames plus reviewability |
| Document-level CriticMarkup dump | Puts a large provenance memo at the top of the file | Use short passage-local CriticMarkup comments at the exact text being routed, rejected, or flagged |
| Bucketed duplicate dismissal | Marks a long claim inventory or proof-obligation list as "already covered" without unit-level actions | Route or reject the internal mathematical units at their own subsection or paragraph-cluster boundaries |
| Repetition shortcut | Marks a repeated or condensed claim-list turn as duplicate because another turn was annotated | Check the repeated turn for differences and annotate its internal sections, or mark it `needs-human` locally |
| End-of-answer routing | Places the only comment after a long answer's references/source list | Attach comments beside the internal mathematical sections they classify |
| Completion pressure | Compresses hard sections to make the artifact look done | Finish one coherent segment well and leave unresolved passages for a fresh direct pass |
| Handoff laundering | Adds a progress summary, routing ledger, or completion claim that later agents may trust instead of reading the source | Put material facts only in passage-local CriticMarkup beside the source text that supports them |
| Premature retirement | Says "fully mapped", "no blockers", or "ready to retire" while broad annotations remain | Keep the source in `.annotated` until a fresh direct pass finds no further local semantic work |
| Opaque processing | Advances a source lifecycle without showing which exact passages were routed, imported, rejected, or blocked | Mark local routing and non-import decisions beside the relevant source passages |
| Reward-hacked cleanup | Renames or deletes sources after creating fake notes that preserve little content | Preserve the source and prove semantic transfer item by item before any human-approved deletion |
| Silent semantic drift | “Cleans up” notation or wording and changes meaning | Preserve notation or record the translation explicitly |
| Software-status leakage | Uses labels like “open issue” or “framework” instead of mathematical types | Normalize to conjecture, question, construction, remark, theorem, etc. |
| Dirty-source deletion | Deletes images/PDFs/chats after extraction | Keep originals until audit and retirement criteria pass |
| Tool-blind editing | Breaks links/properties with plain file edits | Prefer Obsidian-aware tools and controlled scripts |
| Regex cascade corruption | Uses repeated broad regexes to fix earlier broad regexes | Revert, inspect, narrow scope, and re-run safely |

## Re-Derivation Principles

- If a transformation might change meaning, make it reversible and label it.
- If a source is hard to reconstruct, preserve it longer.
- If a claim matters mathematically, attach provenance or visible uncertainty.
- If a note would not be searched for, linked to, or maintained, do not create it.
- If content belongs to an existing object, integrate there.
- If a graph operation changes many files, treat it as critical-risk engineering work.
- If OCR/vision/PDF parsing produced content, treat it as interpretation, not truth.
- If unsure, preserve, label, stage, and route for precise review.

## Reference Files

- `references/inbox-analysis-pass.md`: analysis-agent constraints and CriticMarkup rules.
- `references/inbox-incorporation-pass.md`: incorporation-agent consistency rules, durable-note editing contract, and retirement criteria.
- `references/mathematical-unit-library.md`: canonical mathematical unit and callout vocabulary.
- `references/original-draft.md`: original long-form draft. Treat it as background material, not the primary execution policy.
