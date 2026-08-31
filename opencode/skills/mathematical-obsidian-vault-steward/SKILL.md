---
name: mathematical-obsidian-vault-steward
description: Organize and curate mathematical notes, claims, and vault structures.
---
# Mathematical Obsidian Vault Steward

Steward a mathematical Obsidian vault without mistaking structure for knowledge.
Preserve mathematical meaning, source provenance, and retrieval value.
Prefer integration over proliferation.

## Core Policy

- Preserve epistemic integrity first.
  Do not silently change hypotheses, notation, quantifiers, dependencies, or provenance.

- Preserve user-supplied detail before abstraction.
  High-fidelity extraction comes before summarization.

- Integrate into existing durable notes before creating new notes.

- Treat images, diagrams, PDFs, screenshots, whiteboards, and handwritten math as
  first-class sources.

- Treat raw inbox artifacts as source material, not as durable note candidates.

- Optimize semantic transfer out of the inbox, not the inbox files themselves.

- Do not rename, retitle, move, tag, alias, or otherwise normalize raw inbox sources for
  graph hygiene alone.

- Use a fixed staged inbox lifecycle: raw sources land in `INBOX/`; analysis copies move
  to `INBOX/.annotated/`; incorporated sources move to `INBOX/.incorporated/`; deletion
  requires explicit human approval.

- Prefer reversible transformations.
  If a change could alter meaning, label it, stage it, and keep the source.

- Bias the failure mode toward preservation and review, not deletion and compression.

- Never delete inbox source artifacts without explicit human approval after review.

## Route by task

| You are about to… | Load |
|---|---|
| Annotate a source, write or refine CriticMarkup, continue an `.annotated` surface | `references/annotation-pass-policy.md` + `references/inbox-analysis-pass.md` |
| Incorporate an annotated source into durable notes | `references/inbox-incorporation-pass.md` |
| Ingest a new inbox source; run the capture-to-retirement workflow | `references/ingestion-workflow.md` |
| Label a mathematical unit; pick `unit:`/`status:` values; pick a callout | `references/note-taxonomy.md` + `references/mathematical-unit-library.md` |
| Handle images, PDFs, diagrams, scans, or transcripts | `references/visual-and-document-sources.md` |
| Judge whether an artifact is real progress; audit another pass's output | `references/traps-and-anti-patterns.md` |
| Report work, finish a pass, or check completion | `references/outputs-and-checklist.md` |

## Vault Model

- Obsidian is a linked knowledge environment, not a flat markdown folder.

- A durable note should have a stable referent and future retrieval value.

- Sections and block references are valid targets; not every fact deserves its own note.

- Tags are workflow/filtering metadata, not a substitute for links.

- Properties should stay flat and consistent.

- MOCs are curated entry points and progressive-disclosure maps, not generic essays.

- Attachments are source artifacts when they carry mathematical information.

## Specialized Inbox Pipeline

Use this pipeline when an agent’s sole job is long-form, intelligent, semantic parsing
of inbox content into a current mathematical vault.

- **Raw stage:** unprocessed material stays in `INBOX/` with original basename, source
  identity, and source integrity preserved.

- **Analysis stage:** the analysis agent reads one source end-to-end, reconstructs the
  source’s mathematical story, searches the vault for existing integration targets, and
  writes passage-local CriticMarkup routing to `INBOX/.annotated/`. It does not edit
  durable notes. If it cannot say what the source contributes after its false starts,
  corrections, and synthesis are understood, it records the unresolved issue beside the
  relevant source passage instead of producing filler.

- **Incorporation stage:** the incorporation agent treats analysis annotations as
  proposals, first rejects or repairs shallow annotations, then rereads the whole
  annotated source, verifies intra-source and vault-global consistency, edits durable
  notes, and moves the source to `INBOX/.incorporated/` only after direct inspection
  shows the source’s mathematical contribution has been dispersed into the vault or
  explicitly rejected.

- **Human review stage:** incorporated sources remain reviewable.
  Deletion is a separate human decision; agents do not infer deletion approval from
  successful incorporation.

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

- If hiding the title, frontmatter, links, and provenance leaves no real mathematical
  payload, it is not a durable standalone note.

## Mathematical Integrity Rules

- Never change the meaning of a statement silently.

- Never omit hypotheses because they seem standard.

- Never replace user notation with standard notation without recording the translation.

- Never assert equivalence of two definitions or results without proof or source.

- Never complete a proof silently; label agent completions and route them for review.

- Keep conjectures, heuristics, guesses, and proved statements separate.

- Preserve failed attempts, dead ends, and counterexamples when they carry research
  value.

- Record external knowledge separately from user-supplied or source-backed knowledge.

- If an inbox source raises an objection to an existing theorem-like note, default to
  revising that same note: demote theorem to conjecture when justified, add a local
  prose remark documenting the gap, or add an objection-and-resolution section near the
  statement. Do not create a separate “Objection to theorem X” note unless the exchange
  itself has independent future retrieval value.

- Use **mathematical** note types and callout vocabulary (`theorem`, `conjecture`,
  `definition`, `construction`, `question`, …), never software-engineering status
  language such as `open issue` or `framework`. The full labeling rules are in
  `references/note-taxonomy.md`.

## Tooling Rules

- Prefer Obsidian-aware tools over blind filesystem editing for note reads, moves,
  renames, links, backlinks, tags, and properties.

- Use semantic/document tools as intermediate extractors, not truth oracles.

- Use filesystem operations mainly for attachments, hashes, backups, and unsupported
  operations.

- Do not use raw `mv`/bulk text rewriting when link-aware tools can preserve Obsidian
  semantics.

## Git and Bulk-Edit Safety

- Inspect current git state before risky work.

- Checkpoint before broad refactors, normalizations, regexes, or renames.

- Keep risky vault operations scoped and reversible.

- After bulk work, inspect diff, unresolved links, orphan notes, changed binaries, and
  metadata counts.

- Never run a broad replacement and then try to regex-fix the damage repeatedly.
  Stop, inspect, and narrow the operation.

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

- `references/annotation-pass-policy.md`: binding CriticMarkup and analysis-pass
  constraints (source-body preservation, passage-local routing, segment scope,
  labeled fields).

- `references/inbox-analysis-pass.md`: analysis-agent constraints and CriticMarkup
  rules.

- `references/inbox-incorporation-pass.md`: incorporation-agent consistency rules,
  durable-note editing contract, and retirement criteria.

- `references/ingestion-workflow.md`: the inbox source protocol and the twelve-step
  capture-to-retirement ingestion workflow.

- `references/note-taxonomy.md`: unit-labeling and status rules for durable notes and
  CriticMarkup.

- `references/mathematical-unit-library.md`: canonical mathematical unit and callout
  vocabulary.

- `references/visual-and-document-sources.md`: rules for images, diagrams, PDFs,
  scans, and transcripts as first-class sources.

- `references/traps-and-anti-patterns.md`: environment traps and the anti-pattern
  catalog for auditing pass output.

- `references/outputs-and-checklist.md`: required outputs per pass type and the full
  completion checklist.

- `references/original-draft.md`: original long-form draft.
  Treat it as background material, not the primary execution policy.
