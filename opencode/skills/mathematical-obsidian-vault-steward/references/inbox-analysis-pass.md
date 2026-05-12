# Inbox Analysis Pass

Use this reference when the task is to semantically parse a long-form mathematical inbox source and prepare incorporation suggestions. This pass is analysis only. Do not edit durable notes, MOCs, or paper files.

## Role

The analysis agent reads one inbox source deeply, researches the current vault for integration targets, and writes passage-local CriticMarkup suggestions into an annotated copy of the source.

The output is an annotated source in `INBOX/.annotated/` with the original basename preserved. The source remains a source artifact; the annotated copy is not a durable note.

## Directory Contract

- Input path: `INBOX/<original basename>`
- Output path: `INBOX/.annotated/<original basename>`
- Do not write to `INBOX/.incorporated/`.
- Do not create or edit permanent notes.
- Do not delete, rename, retitle, or normalize the raw source for graph hygiene.

If the vault uses a different inbox root, map these stage names onto the existing root without changing their meaning: raw, annotated, incorporated.

## Source Metadata

Adding flat YAML metadata to a markdown source is allowed when it preserves the source body exactly. Use sidecar metadata for non-markdown sources.

Recommended flat fields:

```yaml
source_id: SRC-YYYY-MM-DD-shortslug
source_kind: chat | note | pdf | image | transcript | mixed | other
inbox_stage: annotated
original_path: INBOX/example.md
annotated_path: INBOX/.annotated/example.md
source_hash: sha256:...
analysis_status: complete | blocked | needs-human
analysis_scope: full-source | partial-source
candidate_targets:
  - "[[Target note]]"
blocked_targets: []
delete_eligible: false
```

Do not use metadata to replace source text. Metadata tracks lifecycle and provenance; it does not summarize the mathematical payload.

## Required Source Pass

Read the source end-to-end before finalizing any routing suggestion.

Process section by section:

- Assign a stable source-local locator to every meaningful section, turn, page, heading, paragraph cluster, figure, table, or displayed formula.
- Extract semantically meaningful mathematical units before deciding note destinations.
- Track later corrections in the same source. A suggestion from an early section can be superseded by a later turn, resolution, or retraction.
- Keep discarded or superseded suggestions visible as analysis decisions, not as permanent-note edits.

For conversations and transcripts, every turn can change the status of earlier mathematical claims. Do not finalize a demotion, objection, or theorem update until the whole source has been checked for later resolution.

## Vault Research Protocol

For each extracted unit, search for existing integration targets before suggesting a new note.

Search at least:

- exact names and title variants;
- notation variants and formulas;
- theorem, lemma, proposition, conjecture, and construction names;
- aliases and nearby MOCs;
- backlinks and the local neighborhood of candidate target notes;
- paper-section maps, outline notes, and project meta notes when present;
- source IDs or provenance packets already mentioned in the vault.

Route content to the mathematical object it modifies. If a source raises concerns about an existing theorem, suggest updating that theorem's note. Do not suggest a new "Objection to theorem X" note unless the objection-resolution exchange is itself reusable enough to justify a separate linked note.

## Mathematical Units

Use the canonical vocabulary in `mathematical-unit-library.md`.

Important routing defaults:

- Theorems, lemmas, propositions, and corollaries require exact hypotheses and proof status.
- Unproved theorem-shaped claims are conjectures.
- Open criteria or unresolved decisions are questions or problems.
- Objects, recipes, divisor packages, and explicit constructions are constructions.
- Local concerns, caveats, failed proof attempts, and provenance notes are usually prose remarks near the target statement.
- A fact is a small source-backed assertion that does not warrant theorem-like status.

Use callout suggestions for formal mathematical units except remarks. Remarks should be suggested as ordinary prose under or near the affected statement.

## CriticMarkup Rules

Use CriticMarkup as passage-local editorial markup.

- Prefer comments: `{>> route: suggest adding this as a prose remark under [[Target note#Heading]] because ... <<}`
- Use additions only when suggesting exact text at the source passage: `{++ suggested durable text ++}`.
- Use deletions only for suggested removal from durable notes, not for deleting source text.
- Use substitutions for demotions or status changes: `{~~ theorem ~> conjecture ~~}{>> reason: no proof in source; later turn confirms gap <<}`.
- Keep comments beside the passage they evaluate.
- Do not place a global summary block at the top of the source.
- Do not turn CriticMarkup into a changelog.

Every routing comment should say:

- target note or section;
- mathematical unit type;
- action: add, merge, demote, promote, split, reject, preserve-source-visible, or needs-human;
- reason grounded in the source;
- source-local locator when the surrounding passage is not enough.

## Handoff Output

At the end of the annotated source, add a concise handoff section only if the source format allows it without corrupting the source. The handoff is an index of local annotations, not a substitute for them.

Include:

- source ID;
- analysis scope and whether every section was reviewed;
- candidate target notes;
- high-risk suggestions;
- superseded suggestions and the later source location that superseded them;
- suggested new notes, if any, with the stable referent test;
- explicit blockers for the incorporation agent.

Do not claim incorporation happened. The incorporation agent decides what to edit.
