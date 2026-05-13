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
- A shallow annotated source is worse than no annotated source. If the agent cannot reconstruct the mathematical story and route its durable insights, mark the source blocked and leave it for a stronger pass.
- An analysis-pass artifact must be a full annotated copy of the source body. A synthesized memo, routing ledger, or selected-excerpt report may supplement it but cannot replace it.
- Never treat hashes, file existence, candidate target lists, or another agent's completion report as evidence that semantic extraction happened.

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
- **Analysis stage:** the analysis agent reads one source end-to-end, reconstructs the source's mathematical story, searches the vault for existing integration targets, and writes passage-local CriticMarkup routing to `INBOX/.annotated/`. It does not edit durable notes. If it cannot say what the source contributes after its false starts, corrections, and synthesis are understood, it marks the source blocked instead of producing filler.
- **Incorporation stage:** the incorporation agent treats analysis annotations as proposals, first rejects or blocks shallow annotations, then rereads the whole annotated source, verifies intra-source and vault-global consistency, edits durable notes, and moves the source to `INBOX/.incorporated/` only after the source's mathematical contribution has been dispersed into the vault or explicitly rejected.
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
  - unproved theorem-like claim -> `conjecture`
  - unresolved problem or criterion question -> `question`
  - explicit object/recipe/divisor/package to build -> `construction`
  - contextual explanation or non-assertive framing -> `remark`
  - exact formal statement with proof elsewhere -> theorem/lemma/proposition/corollary as appropriate
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
- A solution-shaped annotated file can be worse than an unprocessed source if it hides missing analysis.
- A complete-looking ledger can still be slop if it does not explain the source's final mathematical contribution.
- A selected-excerpt report is not an annotated source; it may hide the exact passages the incorporation agent needs to audit.
- A wikilink to a plausible title is not a checked target. Verify the actual existing note path or mark it as proposed.
- A disputed source claim is not automatically a proof obligation. Preserve the dispute unless the source resolves it.
- Renaming a source file is not provenance preservation.
- A note can be nonempty and still be fake if it contains only scaffolding.
- Images, diagrams, and scanned math often carry information that prose extraction misses.

## Required Outputs

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

## Validation Checklist

- [ ] Raw source preserved or explicitly unnecessary
- [ ] Source record exists for nontrivial input
- [ ] Each processed inbox source was read end-to-end in isolation
- [ ] Each processed inbox source has a compact synthesis of its final mathematical contribution
- [ ] Existing notes searched before new notes were created
- [ ] Routing was organized around mathematical objects, claims, and proof obligations, not source files or headings
- [ ] True claims, false framings, conjectures, open questions, proof obligations, dead ends, and reviewer-objection material were separated
- [ ] No annotation pass is marked complete when it only contains metadata, candidate targets, high-level section buckets, hashes, generic "accepted target" comments, or a ledger without synthesis
- [ ] Analysis-pass output preserves the full source body with inline CriticMarkup; any synthesis or ledger is supplementary
- [ ] CriticMarkup comments use exact syntax and atomic `unit:`/`status:` values from the skill vocabulary
- [ ] Existing target notes were verified at their actual vault paths; nonexistent targets were marked as proposed
- [ ] Disputed claims were marked as disputed or needs-human unless the source itself resolves them
- [ ] Final analysis metadata matches the artifact state; no final handoff is left `in-progress`
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

- `references/inbox-analysis-pass.md`: analysis-agent prompt, constraints, CriticMarkup rules, and handoff artifact.
- `references/inbox-incorporation-pass.md`: incorporation-agent prompt, validation rules, durable-note editing contract, and retirement criteria.
- `references/mathematical-unit-library.md`: canonical mathematical unit and callout vocabulary.
- `references/original-draft.md`: original long-form draft. Treat it as background material, not the primary execution policy.
