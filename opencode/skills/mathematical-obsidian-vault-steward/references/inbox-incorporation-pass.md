# Inbox Incorporation Pass

Use this reference when the task is to apply an annotated inbox source to durable
mathematical notes. This pass edits the vault, but only after validating the analysis
annotations against the whole source and the current vault.

## Role

The incorporation agent is not a stenographer for the analysis pass.
It treats every annotation as a proposal.
Its job is to decide which proposals globally make sense, update the canonical notes,
and preserve an audit trail that lets a human review the source later.

## Directory Contract

- Input path: `INBOX/.annotated/<original basename>`

- Output path after successful incorporation: `INBOX/.incorporated/<original basename>`

- Preserve the original basename.

- Do not delete incorporated sources.

- Leave sources needing more analysis in `.annotated` with local CriticMarkup explaining
  the unresolved passages.

If a vault has a different inbox root, preserve the raw, annotated, incorporated stages
without inventing a new lifecycle.

## Required Verification

Before editing durable notes:

- Run the analysis quality gate first.
  If the annotated source is mostly metadata, hashes, candidate target lists, broad
  section buckets, generic `accepted target` comments, or appended summary prose, stop
  before editing durable notes.

- Verify that the annotated source reconstructs the mathematical story of the full
  source: surviving claims, false framings, conjectures, open questions, proof
  obligations, dead ends, and the resulting vault-level update.

- If the artifact clearly has unfinished local analysis, incorporate only if the user
  explicitly asked for partial incorporation; otherwise leave it in `.annotated` for
  another analysis pass.

- Verify that claim inventories, proof-sketch reconstructions, and “remaining things to
  prove” sections have passage-local annotations or explicit no-import reasons at the
  subsection, paragraph-cluster, or mathematical-unit level.
  If those sections are only covered by appended summary prose, one trailing “duplicate”
  comment, or a bucket-level note-title map, the artifact is not incorporation-ready.

- If any text says “fully mapped”, “no blockers”, “no durable note edits required”, or
  “ready to retire” while long claim-list turns are covered only by broad comments,
  ignore that claim and treat the artifact as needing direct analysis.

- If the only comment on a long mathematical answer appears after its references/source
  list, treat that as missing passage-local analysis.
  The incorporation agent should block or repair the analysis before editing durable
  notes.

- Treat claims such as “no new durable claims”, “all content routes into existing
  notes”, or “already covered” as proposals to verify, not conclusions.
  For each major source unit, inspect the named durable note section that allegedly
  absorbs or rejects it.

- “Already covered” still needs an incorporation decision: merge wording, reject as
  duplicate, add caveat, demote/promote, preserve source-visible, or block for human
  review.

- Verify that routing decisions are grouped around mathematical objects and claims, not
  merely the order of headings in the source.

- Verify that each routing comment uses an actual incorporation action.
  Non-action routes such as `cross-check`, `review`, or `compare against` are blocked
  unless you can repair them by reading the whole source and target notes.

- Reject comments that refer to another comment such as “see Segment C” instead of
  restating the actual target, action, status, and reason.

- Verify that every existing target path actually exists in the vault.
  Correct plausible-but-wrong folder guesses before editing durable notes.

- Verify that disputed source claims remain marked as disputed or needs-human unless the
  source itself resolves them.

- If a disputed source claim already appears in a durable note, inspect that note before
  accepting a source-visible-only decision.
  The likely durable action is a local caveat, demotion, rejection, objection-resolution
  remark, or `needs-human` blocker near the affected statement.

- Do not infer analysis from file existence, CriticMarkup count, hash preservation,
  source metadata, or another agent’s claim that the pass was complete.

- Read the whole annotated source, not only the CriticMarkup.

- Check whether later source sections supersede earlier objections, corrections, or
  demotion suggestions.

- Verify each proposed target note still exists and still means what the annotation
  assumes.

- Inspect nearby headings, backlinks, aliases, and MOCs around every proposed target.

- Check whether multiple annotations conflict with each other.

- Check whether the same content has already been incorporated elsewhere.

If turn 1 says a theorem is wrong and turn 10 resolves the issue, do not demote the
theorem. Instead, consider whether the objection and resolution should become a prose
remark near the theorem or a linked objection-resolution note when the exchange has
future review value.

If the analysis pass is shallow but the user explicitly asks you to repair it, switch
roles and perform the missing whole-source synthesis before editing durable notes.
Otherwise, leave the source in `.annotated` with local CriticMarkup at the passages that
show why incorporation is not justified.

## Editing Rules

Edit the smallest durable surface that preserves meaning.

- Prefer updating an existing note or section over creating a new note.

- Put caveats, objections, and proof gaps near the affected theorem, lemma, conjecture,
  construction, or definition.

- Demote theorem-like statements to conjectures only when the full source and target
  note justify the status change.

- Promote conjectures only when a proof or authoritative source is actually present.

- Keep remarks as top-level prose, not remark callouts.

- Use callouts for formal mathematical units according to
  `mathematical-unit-library.md`.

- Preserve source notation unless the note already has a canonical notation.
  Record translations explicitly.

- Keep provenance compact but traceable: source ID, locator, and whether the text is
  source-backed, user-asserted, agent-inferred, or externally verified.

Never create a note whose only payload is that another note has a possible problem.
A separate objection-resolution note is justified only when the exchange is reusable,
historically important, or too large for the target note without harming readability.

## Incorporation Decisions

For each annotation, choose one decision:

- `accepted`: edited into a durable note;

- `accepted-with-rewrite`: incorporated after correcting target, type, or wording;

- `merged`: combined with an existing note section;

- `superseded`: later source material changed the right action;

- `rejected`: not incorporated because it is false, duplicate, unsupported, or
  graph-polluting;

- `blocked`: needs human or mathematical review before editing.

Record decisions passage-locally when practical.
Use CriticMarkup comments on the annotated source for decisions that differ from the
analysis proposal.

When rejecting or blocking shallow analysis, record the reason in terms of missing
semantic work, not process receipts.
Examples: “no synthesis of the conversation’s final mathematical state”, “source treated
as independent snippets instead of a correction arc”, “false start not routed as warning
or rejection”, or “target section not inspected”.

## Durable Note Shape

Use existing local conventions first.
When a vault needs default structure, use:

- flat YAML frontmatter;

- one primary mathematical type per note;

- Obsidian wikilinks to dependencies and nearby concepts;

- callouts for formal units except remarks;

- provenance section only when it carries source value, not as filler.

Do not create or preserve fake cards.
If hiding a note title, YAML, and links leaves no mathematical payload, merge the
content elsewhere.

## Lifecycle Completion

Move the annotated source to `INBOX/.incorporated/` only after:

- all annotations have an incorporation decision;

- accepted edits were made and checked against the source;

- rejected or blocked suggestions are marked;

- durable notes do not link readers into raw inbox paths unless explicitly intended;

- any source metadata remains lifecycle/provenance-only;

- deletion remains human-approved only.

Recommended flat metadata updates:

```yaml
inbox_stage: incorporated
incorporated_targets:
  - "[[Target note]]"
delete_eligible: false
```

For partial incorporation, keep the source in `.annotated` unless unresolved passages
are explicitly marked locally and the user asked to advance it.

## Required Checks

After editing:

- inspect the diff for unintended source loss, status changes, or unrelated note churn;

- search for broken links introduced by new wikilinks;

- verify any changed YAML remains valid if frontmatter was edited;

- verify source IDs and target paths are consistent;

- confirm no source artifact was deleted.

Report only unresolved blockers, review-needed decisions, skipped surprises, and next
actions.
