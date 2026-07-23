# Required Outputs and Completion Checklist

## Required Outputs

For inbox analysis passes, the annotated source is the output.
Do not write a handoff, progress report, completion report, annotation count,
preservation receipt, validation preface, or routing summary into the annotated source
or a separate workflow artifact.
The continuation surface is the source body plus passage-local CriticMarkup.

For this artifact rule, an unresolved semantic blocker is any remaining source passage
whose mathematical contribution has not yet been locally routed, rejected, or marked
with a precise unresolved status in the annotated artifact.
Intentionally leaving source passages untouched is allowed.
Any structured section covered only by an umbrella duplicate, superseded,
already-covered, or preserve-source-visible comment is still unresolved, even when every
internal claim would route to the same note.
A syntax/anchor audit is only markup hygiene; it never cancels unhandled mathematical
source content.

For incorporation or durable-note editing work, report only unresolved review surfaces:

When reporting work, include:

- **Completed**: notes updated and what source-backed content changed.

- **Created**: new notes and why they deserved separate existence.

- **Review needed**: exact ambiguities, inferred steps, OCR/vision uncertainty, or
  high-risk items.

- **Not done / deferred**: what stayed source-visible and why.

- **Checks**: unresolved links, orphans/dead ends when relevant, and git diff/checkpoint
  status.

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

- [ ] Each processed inbox source has a compact synthesis of its final mathematical
  contribution

- [ ] Existing notes searched before new notes were created

- [ ] Routing was organized around mathematical objects, claims, and proof obligations,
  not source files or headings

- [ ] True claims, false framings, conjectures, open questions, proof obligations, dead
  ends, and reviewer-objection material were separated

- [ ] No annotation pass is treated as incorporation-ready when it only contains
  metadata, candidate targets, high-level section buckets, hashes, generic “accepted
  target” comments, or a ledger without synthesis

- [ ] Analysis-pass output preserves the full source body with passage-local
  CriticMarkup; any separate synthesis or ledger is excluded from the annotated source

- [ ] Source text was not reflowed, normalized, heading-rewritten, or otherwise cleaned
  up outside explicit CriticMarkup insertions

- [ ] Text/markdown annotated artifacts began as a literal source copy, not as
  regenerated model prose

- [ ] Analysis artifacts are grounded in the raw source and durable vault notes, not
  patterned on prior processed copies unless comparative review was explicitly requested

- [ ] CriticMarkup comments use exact syntax and atomic `unit:`/`status:` values from
  the skill vocabulary

- [ ] CriticMarkup comments include explicit labeled `action:` and `reason:` fields

- [ ] No source-level, whole-file, or `locator: entire source` comment was added

- [ ] No structured turn was covered by a single duplicate/superseded/already-covered
  comment

- [ ] Existing target notes were verified at their actual vault paths; nonexistent
  targets were marked as proposed

- [ ] Every anchored wikilink in CriticMarkup points to an existing heading/block in the
  named target; unverified anchors are omitted or explicitly marked proposed

- [ ] No CriticMarkup uses shorthand targets such as “same note”, “above note”, or “this
  note”; every route repeats the actual target note or section

- [ ] Disputed claims were marked as disputed or needs-human unless the source itself
  resolves them

- [ ] No handoff, progress summary, routing ledger, or completion/status claim was
  appended to the annotated source

- [ ] Analysis-pass agents annotated suggestions only and did not edit durable notes

- [ ] Incorporation-pass agents verified annotations against the full source before
  editing durable notes

- [ ] New notes have stable referents and real retrieval value

- [ ] No new note merely mirrors or launders a raw source artifact

- [ ] No empty or fake cards were created

- [ ] Any CriticMarkup on processed markdown sources is passage-local and tied to exact
  routed or rejected spans

- [ ] No generic explanatory filler replaced source-rich detail

- [ ] Formulas, hypotheses, and notation were not silently changed

- [ ] Images/PDFs/diagrams retain original provenance

- [ ] No figure was treated as redundant just because prose exists nearby

- [ ] High-risk items have explicit review packets

- [ ] No permanent note or MOC accidentally routes readers into raw inbox material

- [ ] No inbox source was renamed, moved, or deleted for graph hygiene alone

- [ ] Annotated sources live in `INBOX/.annotated/` until incorporation

- [ ] Incorporated sources live in `INBOX/.incorporated/` with original basenames intact
  and remain reviewable

- [ ] Any inbox deletion has explicit human approval

- [ ] MOCs were updated only when they improve navigation

- [ ] Bulk or destructive operations were checkpointed, scoped, and reviewed

