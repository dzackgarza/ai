# Inbox Analysis Pass

Use this reference when the task is to semantically parse a long-form mathematical inbox
source and prepare incorporation suggestions.
This pass is analysis only.
Do not edit durable notes, MOCs, or paper files.

## Role

The analysis agent reads one inbox source deeply, researches the current vault for
integration targets, and writes passage-local CriticMarkup suggestions into an annotated
copy of the source.

The output is an annotated source in `INBOX/.annotated/` with the original basename
preserved. The source remains a source artifact; the annotated copy is not a durable
note.

This pass is allowed to leave unfinished source-local work visible.
If you cannot reconstruct the mathematical story of the source and explain what should
change in the vault, record the unresolved issue beside the relevant passage and leave
the source for another direct pass.
Do not emit a plausible-looking annotated file whose only real content is metadata,
target lists, hashes, or a few broad comments.

Solution-shaped filler is harmful.
A bad analysis pass can mislead the incorporation agent and bury the raw source under
false confidence.

## Directory Contract

- Input path: `INBOX/<original basename>`

- Output path: `INBOX/.annotated/<original basename>`

- Do not write to `INBOX/.incorporated/`.

- Do not create or edit permanent notes.

- Do not delete, rename, retitle, or normalize the raw source for graph hygiene.

- During analysis, research durable vault notes only.
  Do not read, list, cite, or expand existing lifecycle artifacts in
  `INBOX/.annotated/`, `INBOX/.processed/`, `INBOX/.incorporated/`, or scratch
  directories as target evidence or format examples.
  If directory discovery reveals one of these paths, skip it without opening it.

- Treat existing lifecycle artifacts as quarantined evidence.
  They may contain prior slop, stale routing, or false status claims.
  Never open an existing `.annotated` copy to understand the raw source, copy its style,
  or decide whether the redo is needed.

- To create the annotated path, create the stage directory directly if needed and copy
  the raw source to the intended output path.
  Do not inspect the stage directory first to see what is there.
  If the exact output path already exists and the user asked for a redo from raw,
  overwrite it mechanically from the raw source before any semantic research.
  If overwrite authority is absent, report a blocker instead of reading the old output.
  If the task is explicitly to continue or refine an existing annotated artifact, read
  the raw source and then read the annotated artifact as the current work surface;
  assess every existing annotation as a proposal, not evidence.

- The annotated artifact is a full annotated copy of the source body, not a separate
  memo, digest, routing ledger, progress summary, or selected-excerpt report.
  Add local CriticMarkup without replacing the source with a synthesized ledger.

- For text or markdown sources, create the annotated artifact by copying the raw source
  body first and then inserting CriticMarkup into that copy.
  Do not ask the model to rewrite or regenerate the source body from memory.

- A complete rewrite is invalid even when it is semantically faithful.
  The analysis pass preserves provenance by editing a source copy, not by producing a
  new document that restates the source.

- Ground the analysis in the raw source and durable vault notes.
  Do not imitate prior processed copies or use them as format examples.

If the vault uses a different inbox root, map these stage names onto the existing root
without changing their meaning: raw, annotated, incorporated.

## Source Metadata

Adding flat YAML metadata to a markdown source is allowed when it preserves the source
body exactly. Use sidecar metadata for non-markdown sources.

Frontmatter metadata is optional.
Do not let metadata editing delay or damage semantic annotation.
If frontmatter editing becomes ambiguous or starts to disturb the copied source, stop
editing the frontmatter and continue semantic annotation.

Recommended flat fields:

```yaml
source_id: SRC-YYYY-MM-DD-shortslug
source_kind: chat | note | pdf | image | transcript | mixed | other
inbox_stage: annotated
original_path: INBOX/example.md
annotated_path: INBOX/.annotated/example.md
source_hash: sha256:...
delete_eligible: false
```

Do not add work-status metadata such as `analysis_status`, `analysis_scope`,
`candidate_targets`, or `blocked_targets`. They encourage receipt-checking and become
stale or confabulated quickly.
Metadata tracks lifecycle and provenance only; it does not summarize the mathematical
payload.

## Required Reading Posture

Read the source end-to-end before writing incorporation suggestions.
The first deliverable is understanding, not markup.

Create the annotated artifact early and use it as the working surface for understanding
the source.
Add provenance metadata only when it is a safe targeted edit, then revise the
artifact as the mathematical story becomes clear.
Do not keep all analysis private until the end; if interrupted, the file should show
what has actually been understood and what remains unresolved through local
CriticMarkup.

Preserve the source text in the working artifact literally.
The only routine body changes are inserted CriticMarkup comments and inserted
additions/deletions/substitutions when explicitly proposing durable text.
Do not reflow paragraphs, normalize Unicode, change quote characters, convert source
frontmatter into headings, duplicate heading markers, rewrite citation formatting, or
otherwise “clean up” the source body while annotating.
Do not append a synthesis, routing ledger, progress summary, or handoff to compensate
for missing inline analysis.
If the requested output directory is nonstandard, keep the same artifact semantics
there: full source body plus annotations.

After inserting CriticMarkup, do not clean blank lines, spacing, escaping, or markdown
layout merely for neatness.
Cosmetic cleanup is a common path to source-body damage.
If you notice a harmless extra blank line, leave it.
If you introduce a literal artifact such as a stray replacement token, remove only that
exact token and then stop editing nearby source text.

Prefer exact local replacement of the adjacent source line or paragraph over line-number
range edits. Exact replacement means literal matching against a source block just read
from the current artifact.
Do not use regex mode, wildcard spans such as `.*`, anchors, capture groups, or
replacement backreferences to insert CriticMarkup.
If adding a comment requires line arithmetic, regex surgery, regenerating source lines,
or replacing a broad block copied from model memory, leave the passage unresolved.
A missing annotation is safer than duplicated or mutated source text.

If you cannot insert annotations without regenerating or reformatting the source body,
leave local evidence of the blocker if possible and do not manufacture a polished
reconstruction.
A malformed but literal source copy is easier for a human to audit than a
polished reconstruction that changes source text.

When inserting multiple comments into a copied source, first draft the full set of
comments with stable surrounding passages.
Then use targeted literal replacements around exact passages.
Do not insert top-down from absolute line numbers and then chase shifted line numbers.

Do not batch several insertions into the same local region in one tool step.
Use one literal exact block replacement, reread the local region, then decide whether
the next replacement is safe.

For any exact block replacement, paste the existing source lines from the current
artifact exactly as read.
Do not retype source prose from memory.
After the edit, inspect the artifact diff before calling the segment source-faithful.
Any changed source line outside CriticMarkup insertion/removal, including quote marks,
dashes, Unicode, formula text, citation escaping, or punctuation, is source-body damage;
repair that line before proceeding.

This is not a coverage exercise.
If high-fidelity local routing of the whole source is too large to finish cleanly,
complete one coherent source segment well and leave the remaining source without fake
broad catch-all comments.
A later agent must assess the artifact directly; fake completeness is worse than partial
useful analysis.

When the current artifact contains many umbrella comments or broad placeholders, choose
one coherent segment and improve only that segment.
Do not build a whole-file cleanup plan.
Do not start editing a second segment until the first segment has been inspected after
edits and remains source-faithful.
A clean one-section improvement plus explicit remaining blockers is a valid continuation
state.

When you intentionally leave substantive passages or internal sections untouched, those
source locators are unresolved semantic blockers.
It is acceptable for the annotated artifact to be partial, but it is not acceptable to
answer as though no semantic blockers remain.
A syntax, field-value, or anchor audit is only markup hygiene; it never cancels
unhandled mathematical source content.

Do not use source/reference-list lines as insertion anchors for long mathematical
answers. Anchor comments near the mathematical heading, paragraph, or list item being
classified. If the only reliable anchor you have is a repeated source citation such as
`> [3] ...`, stop and choose a more local passage or use line insertion after inspecting
the current file.

If any long claim-list or proof-sketch turn is covered only by a compact turn-level
`duplicate`, `superseded`, `already covered`, or `preserve-source-visible` comment, the
artifact still needs further local analysis.
A later pass should remove, replace, or refine that broad comment beside the internal
units.
Leaving work for a later pass means leaving the unhandled source passage without a
synthetic coverage comment, not adding a placeholder.
Do not say “fully mapped”, “no blockers”, “no durable note edits required”, or “ready to
retire” while such broad coverage remains.

For chatlogs, transcripts, and iterative notes, reconstruct the whole mathematical
conversation:

- What mathematical objects, claims, constructions, proof ideas, examples, computations,
  objections, and dead ends appear?

- Which statements survive the whole source as true, proved, usable, conjectural, open,
  false, superseded, or merely rhetoric?

- What changed from the beginning of the source to the end?

- Which false starts or incorrect framings are still useful as warnings, reviewer
  objections, or proof-gap remarks?

- What would be lost if the raw source disappeared after incorporation?

Only after answering those questions should you annotate.
CriticMarkup is the visible trace of the synthesis; it is not a substitute for
synthesis.

Use two passes when the source is long:

- **Story pass:** read through the whole source and build the final mathematical state,
  including false starts and status changes.
  Any narrative needed for later use belongs in local CriticMarkup beside the passages
  that support it.

- **Routing pass:** search the vault and attach CriticMarkup near the passages that
  actually support each durable update, rejection, warning, or blocker.

The story pass can be partial.
The routing pass is not incorporation-ready until the whole source has been reconciled
through passage-local annotations.

Process source-local passages after the whole-source read:

- Give stable locators to meaningful turns, sections, paragraph clusters, figures,
  tables, displayed formulas, and formal statements.

- Route mathematical insights, not headings.
  A heading can help locate content, but it is not a unit of meaning.

- Treat claim inventories, proof-sketch reconstructions, and “remaining things to prove”
  lists as mathematical source content.
  They need passage-local routing, rejection, or explicit duplicate/no-import comments
  just as much as earlier conversational turns.

- Every substantive section or turn must have either a nearby route comment or a nearby
  reason it should not be imported.
  It is not enough for a later summary or status note to say that a long section was
  “already covered.”

- A structured claim inventory or proof-obligation list is not one remark.
  Annotate it at the subsection, paragraph-cluster, or mathematical-unit level.
  A single comment after a multi-page list saying “duplicate”, “already covered”, or “no
  new claims” is invalid.

- If a claim inventory or proof-obligation list is divided by Roman numerals, numbered
  headings, bold item labels, or other visible internal sections, put CriticMarkup
  beside those internal sections.
  Do not wait until the references/source list or the end of the answer to attach one
  global routing comment.

- Do not annotate a structured claim-list turn as a whole merely because an earlier or
  later turn has similar section-level coverage.
  Repeated, condensed, or expanded versions still need their internal sections checked
  for differences.

- For any turn or section that contains multiple numbered items, Roman-numeral sections,
  bold item labels, or theorem-like claims, the minimum acceptable local work is one
  CriticMarkup comment per internal item being handled.
  There is no exception for `duplicate`, `superseded`, `preserve-source-visible`, or
  `already covered`.

- If you cannot handle every internal item in that structured turn, choose one coherent
  subset and annotate that subset deeply.
  Leave the rest untouched for a later direct pass; do not add a turn-level placeholder.
  “Untouched” means no synthetic umbrella comment.

- Do not invent a same-target exception.
  A visible claim list remains structured even when all of its internal claims point to
  the same durable note.
  If splitting every item would be low value, handle the useful subset locally and leave
  the rest without an umbrella comment.

- A references/source list at the end of an answer is not the passage being routed.
  It is usually the worst place for the only comment on a long mathematical answer,
  because it separates the routing decision from the claims.

- A single block comment may cover only an unstructured paragraph cluster with one
  mathematical payload.
  It may not cover a list, Roman-numeral section, numbered section, or run of
  bold-labeled items. If a list mixes constructions, conjectures, questions, proof
  obligations, rejected claims, or different canonical vault notes, split the annotation
  by unit.

- When the source has Roman-numeral sections, one section is the maximum normal segment.
  After a coherent improvement inside one such section, do not edit adjacent sections or
  the rest of the turn.
  Similar defects elsewhere should remain visible as future continuation state.

- `status: duplicate` and `action: preserve-source-visible` do not relax the
  internal-item rule. A duplicate comment with one route may cover only the source item
  it is attached to. If the reason says the passage restates content from several durable
  notes, or if the section mixes branch-curve geometry with KSBA stability, cusps with
  semifans, comparison with IAS, or arithmetic setup with lattice identity, split the
  source passage into smaller comments beside its internal headings, bold labels, or
  paragraphs.

- “Already present in the vault” is a routing conclusion, not a reason to stop analysis.
  For each already-present unit, say whether the incorporation agent should merge
  wording, add a caveat, reject as duplicate, demote/promote a statement, or leave
  source-visible with no durable edit.

- Repeated, condensed, or superseded passages still need real vault routes.
  Do not write `route: superseded by Turn N`, `route: see expanded annotation`,
  `route: line ...`, or similar.
  Repeat the durable target path and use `status: superseded` with
  `action: preserve-source-visible` when the incorporation agent should not import the
  repeated wording.

- Preserve the role of discarded material.
  A false theorem-shaped claim may become a warning remark, a rejected route, or an
  objection-resolution note, not simply disappear.

- Keep repeated or near-duplicate passages only when they add a new status change, new
  evidence, or a useful formulation.

- Treat disputes as first-class content.
  If the user challenges a claim and a later assistant defends it, do not automatically
  choose either side. Mark the issue as `needs-human` or preserve it as an
  objection-resolution thread unless the source itself settles it.

- If a disputed source claim already appears in a durable note, route the dispute to
  that note with a local caveat, demotion, or `needs-human` proposal.
  Do not only preserve the dispute in the source artifact.

- Do not claim “no new durable claims” or “all content is already covered” unless every
  major claim, proof obligation, construction, objection, and rejection in the source
  has been checked against named durable note sections and annotated locally with its
  target and action.

- Do not make a giant exhaustive table to prove you read the source.
  Include enough local annotations that an incorporation agent can update the vault
  intelligently after reading the source itself.

## Quality Gate

Before treating an annotated source as ready for incorporation, inspect the artifact
directly as if another agent produced it.

The artifact is not incorporation-ready if any of these are true:

- a reader could have written the annotations after skimming headings rather than
  understanding the mathematical development;

- the local annotations do not show what the source contributes mathematically after
  false starts and later corrections are reconciled;

- true claims, false framings, conjectures, open questions, proof obligations, and dead
  ends are not distinguished;

- hard sections were compressed because local routing would take longer;

- any text claims no blockers or readiness to retire while any long claim-list turn is
  only broadly annotated;

- a claim-inventory, proof-sketch reconstruction, or “remaining proof obligations”
  section has no local annotations and is only summarized elsewhere;

- a structured turn has one comment covering multiple internal items instead of one
  comment per handled item;

- a structured claim-list or proof-sketch turn is covered by one umbrella
  `status: superseded`, `status: duplicate`, `already covered`, or
  `preserve-source-visible` comment;

- a source-level, whole-file, or `locator: entire source` comment appears instead of
  passage-local routing;

- a broad `unit: remark` comment collapses theorem-like claims, constructions,
  questions, computations, or proof obligations that need separate mathematical status;

- comments say only `accepted target`, `route to`, `merge into`, or similarly vague
  phrases;

- comments omit a literal `action:` field or a literal `reason:` field;

- comments use non-action verbs such as `cross-check`, `review`, or `check against`
  where an incorporation agent needs an action: `add`, `merge`, `demote`, `promote`,
  `split`, `reject`, `preserve-source-visible`, or `needs-human`;

- comments identify a note but not the mathematical payload, proposed vault action,
  status, and source-grounded reason;

- comments collapse several claim-list subsections or proof obligations into one
  bucket-level note-title map without section-level actions;

- the only comment on a long mathematical answer appears after its references/source
  list instead of beside the internal claim sections;

- comments use shorthand targets such as “same note”, “above note”, or “this note”
  instead of naming the actual target note or section;

- comments use title-only wikilinks when an existing target note path is known;

- the source is treated as a list of independent snippets when its value is the
  narrative of correction, refinement, or synthesis;

- a disputed item is promoted to a proof obligation without acknowledging the dispute
  and whether the source resolves it;

- a disputed item is marked `needs-human` locally but later text treats it as an
  ordinary open proof obligation or conjecture;

- a disputed item already appears in a durable note but the annotation does not name
  that note and propose a local caveat, demotion, rejection, objection-resolution
  remark, or `needs-human` review;

- any target path points to a folder where the note does not actually exist;

- any `#Heading` or block anchor in a target link was not checked against the current
  target note;

- the output is a synthetic analysis memo, selected-excerpt report, or routing ledger
  rather than a full annotated copy of the source;

- the source body has been normalized, rewrapped, reformatted, or otherwise rewritten
  outside local CriticMarkup insertions;

- the artifact was produced by a whole-file write/regeneration path rather than by
  copying the source and applying targeted insertions;

- the artifact is patterned on previous processed copies rather than grounded in the raw
  source and durable vault notes;

- any appended summary, routing ledger, progress note, or handoff is doing analytic work
  that should be visible beside the source passages;

- the output mostly proves that files exist, hashes were computed, metadata was added,
  or target notes were listed;

- any text says “no new notes”, “no new claims”, or “already covered” without mapping
  the source’s major mathematical units to existing note sections and explicit actions
  or rejections;

- any final answer says no semantic blockers remain while substantive source sections
  are intentionally untouched, broadly dismissed, or not yet locally routed;

- a duplicate or preserve-source-visible comment uses one route while its reason names
  mathematical payloads that belong in multiple durable notes;

- a comment calls a visible claim-list section homogeneous instead of routing its
  internal items, especially branch-curve geometry plus KSBA stability, cusp data plus
  semifan proof obligations, comparison claims plus IAS construction, or arithmetic
  setup plus lattice identity;

- a long claim inventory or proof-obligation list receives only one trailing
  `unit: remark` comment when its internal items have different mathematical units or
  statuses;

- an annotation points to another annotation, such as “see Segment C”, instead of
  repeating the actual target path, action, and reason;

- a `route:` field points to a source turn, source line, other annotation, or “expanded
  annotation” instead of a durable vault target;

- duplicate or near-duplicate sources have not been cross-compared for substantive
  differences.

When the artifact fails this gate, keep the source out of `.incorporated/` and make the
missing semantic work visible at the relevant source passages.
Do not replace that missing work with status metadata or a summary.

## Vault Research Protocol

For each extracted unit, search for existing integration targets before suggesting a new
note.

Search at least:

- exact names and title variants;

- notation variants and formulas;

- theorem, lemma, proposition, conjecture, and construction names;

- aliases and nearby MOCs;

- backlinks and the local neighborhood of candidate target notes;

- paper-section maps, outline notes, and project meta notes when present;

- source IDs or provenance packets already mentioned in the vault.

Exclude inbox lifecycle folders from target research.
`INBOX/.annotated/`, `INBOX/.processed/`, `INBOX/.incorporated/`, and scratch output
folders are source workflow surfaces, not durable note targets.
If search or directory discovery returns these paths, ignore them without reading their
contents.

Route content to the mathematical object it modifies.
If a source raises concerns about an existing theorem, suggest updating that theorem’s
note. Do not suggest a new “Objection to theorem X” note unless the objection-resolution
exchange is itself reusable enough to justify a separate linked note.

Vault research must be visible in passage-local annotations.
Prefer a target section or heading, not just a note title.
If the right target does not exist, say in the local annotation which nearby notes were
checked and why the proposed new note passes the stable referent test.

Organize routing around mathematical objects and claims, not source order alone.
A long chat may contribute one coherent update spread across many turns; route that
update once, with locators for the important turns.

Target paths must be real.
Before finalizing a wikilink or path, verify whether the target note already exists and
use its actual vault location.
If an existing note is found, write the vault-relative path in the wikilink, e.g.
`[[03_Compactifications/Cusp data for polarized Coble moduli#Reduction to Sterk]]`, not
a title-only link. If no matching note exists, label the target as proposed and state
which existing notes were checked.

Anchors must be real too.
Before finalizing `[[Target#Heading]]` or a block reference, inspect the current target
note’s headings or blocks and verify the exact anchor exists.
Use the displayed heading text, not a slugified or URL-style version.
If the target note exists but the right heading does not, either route to the note
without an anchor, propose the heading explicitly, or mark the route `needs-human`; do
not invent an anchor.

## Mathematical Units

Use the canonical vocabulary in `mathematical-unit-library.md`.

Important routing defaults:

- Reclassify each source item from its mathematical role.
  Never inherit a previous `unit:` label just because you are splitting or refining an
  existing comment.

- Theorems, lemmas, propositions, and corollaries require exact hypotheses and proof
  status.

- Unproved theorem-shaped claims are conjectures.

- Open criteria or unresolved decisions are questions or problems.

- Established rules, criteria, implications, equivalences, and if-and-only-if statements
  that are not main theorems are propositions; unresolved ones are conjectures or
  questions.

- Target-note proof status overrides source labels.
  If the target note’s frontmatter, tags, type line, callout, or heading frames the item
  as a conjecture, proposed statement, open issue, or “why this is a conjecture”, use
  `conjecture` or `question`, not `proposition`, even if the source label says “Theorem
  Statement”.

- Target-note proof obligations also override source certainty.
  If the durable note says an item is a checklist entry, obligation to prove,
  verification still needing proof, migrated research claim, or awaiting corroboration,
  do not label the source assertion as `fact`. Use `question` with `status: open` for
  proof or verification obligations, or `conjecture` with `status: conjectural` for
  intended theorem-like claims.

- Do not let `duplicate` erase proof status.
  If a source item is already recorded in a target section that says it is pending
  verification, conjectural, disputed, or still needs proof, choose
  `status: conjectural`, `open`, `disputed`, or `needs-human` as appropriate and explain
  in `reason:` that the target already records it.

- Definitions of terminology, named lattices, groups, divisors, moduli spaces, notation,
  or standing identifications are definitions.

- Recipes, quotients, disjoint unions, normalizations, families, packages, models,
  procedures, construction steps, construction requirements, and explicit constructions
  are constructions.

- Local concerns, caveats, failed proof attempts, and provenance notes are usually prose
  remarks near the target statement.

- A fact is a small source-backed assertion about an already-defined object that does
  not warrant theorem-like status.
  Do not use `fact` for the act of defining or constructing a named object.

Use callout suggestions for formal mathematical units except remarks.
Remarks should be suggested as ordinary prose under or near the affected statement.
A unit is not `remark` merely because the durable edit will be ordinary prose.
Use `remark` only for contextual, caveat-like, historical, comparative, motivational, or
provenance content.

## CriticMarkup Rules

Use CriticMarkup as passage-local editorial markup.

- Prefer comments:
  `{>> route: suggest adding this as a prose remark under [[Target note#Heading]] because ... <<}`

- Use additions only when suggesting exact text at the source passage:
  `{++ suggested durable text ++}`.

- Use deletions only for suggested removal from durable notes, not for deleting source
  text.

- Use substitutions for demotions or status changes:
  `{~~ theorem ~> conjecture ~~}{>> reason: no proof in source; later turn confirms gap <<}`.

- Keep comments beside the passage they evaluate.

- Do not place a global summary block at the top of the source.

- Do not turn CriticMarkup into a changelog.

Every routing comment should say:

- target note path and section, or a specific proposed new-note title with a
  stable-referent reason;

- mathematical role from `mathematical-unit-library.md` when a formal unit is being
  incorporated;

- action: add, merge, demote, promote, split, reject, preserve-source-visible, or
  needs-human;

- proof/status: proved, source-backed, conjectural, unproved, open, proof-sketch,
  contradicted, superseded, duplicate, rejected, disputed, needs-human, blocked,
  external, or source-uncertain;

- reason grounded in the source;

- source-local locator when the surrounding passage is not enough.

Use explicit labeled fields, not free prose packed into `route:`. The normal shape is:

```markdown
{>> route: [[Target note#Heading]]; unit: question; status: open; action: merge; reason: this passage isolates the proof obligation not yet separated in the target note; locator: Turn 7 item 2 <<}
```

A comment without `action:` and `reason:` is malformed even if its prose implies an
action or reason.

`cross-check`, `review`, `compare`, and similar verbs are not CriticMarkup actions.
Use `needs-human` when a decision genuinely requires later review, or choose the
concrete edit/rejection action the incorporation agent should evaluate.

Repeat the actual target in each comment.
Do not write “same note”, “above note”, “this note”, or similar shorthand, because
comments may be read out of order by the incorporation agent.

Use exact CriticMarkup syntax.
A comment starts with `{>>` and ends with `<<}`. Do not escape the closing marker, and
do not end comments with `\}` or `}` alone.

Do not damage adjacent source punctuation while inserting comments.
If a paragraph ends in citations such as `[12][13]`, keep those characters exactly as
they appear in the raw source; put the comment on its own line before or after the
paragraph if inline insertion would require escaping brackets, moving punctuation, or
changing citation text.
Never convert source citations to `\[12\]` or similar cleanup artifacts.

Keep status fields atomic.
Do not write prose statuses such as `proven?
no`, `accepted`, `preserved with reservation`, `proved-in-source`, or `source-verified`;
instead choose the nearest status from the list and put nuance in the reason.
Use `source-backed`, not `source-verified`. Slash-separated values such as
`disputed/needs-human` are invalid.
If a disputed passage needs human judgment, choose `needs-human` as the status and say
in the reason that the passage is disputed; if the task is only to preserve the
disagreement, choose `disputed`.

Keep mathematical unit fields atomic too.
Do not write `fact/conjecture`, `construction/question`, `remark/question`, or similar
hybrid labels.
Split the route into separate comments, or choose the primary unit and put
the nuance in the reason.

Do not let `fact` become the safe default.
A line headed “Theorem Statement” is `theorem` only when proved and otherwise usually
`conjecture`; a line defining cusp pairs, admissibility, strata, lattices, groups,
divisors, or moduli spaces is usually `definition`; a line defining a trace rule,
quotient, normalization, family, model, construction step, or construction requirement
is usually `construction`. Use `fact` only for a small property of an already-defined
object. A line asserting a rule, criterion, implication, equivalence, or if-and-only-if
claim is usually `proposition` if established and `conjecture` or `question` if
unresolved or target-framed as proposed; it is not `remark` merely because it is
duplicate. Before leaving a handled segment, reread every CriticMarkup comment inside
that source segment, including comments that were already present before the current
edit. If the adjacent source label names a mathematical object, criterion, stratum,
quotient, model, family, normalization, rule, construction step, or construction
requirement, the comment probably needs `definition` or `construction`, not `fact`. If
the adjacent source sentence contains a rule, criterion, implication, equivalence, or
if-and-only-if claim, the comment probably needs `proposition`, `conjecture`, or
`question`, not `remark`. Repairing local misclassified `fact` or `remark` comments is
real analysis work; do not skip them to chase an untouched section.

CriticMarkup reasons are not a changelog.
Do not write that a comment was split from an umbrella, that an existing annotation was
refined, that a previous agent missed something, or that “this pass” did anything.
The durable comment should explain the source claim, the vault target, and the
incorporation action.

After the semantic pass is done, do a narrow markup hygiene pass: every `{>>` comment
must close with `<<}`, no comment may close with `>>}` or `\}`, every `status:` value
must come from the allowed list above, and every `unit:` value must come from
`mathematical-unit-library.md`. This check does not prove quality; it only prevents
malformed annotations from blocking incorporation.
Never treat this hygiene pass as evidence that the annotation is complete.

Also audit the route and status fields before leaving the artifact.
Any match for `route: superseded`, `route: see`, `line ~`, `expanded annotation`,
`status: source-verified`, or a title-only wikilink when the actual note path exists
should be fixed in the handled segment or left visible for a later direct pass.
If a reason says the payload is already covered in a named target section, the `route:`
link should include that verified `#Heading`. If the section was not verified or does
not exist, do not describe it as an existing target section.

Bad comment:

```markdown
{>> route: accepted target [[Cusp data for polarized Coble moduli]] <<}
```

Good comment:

```markdown
{>> route: merge into [[Cusp data for polarized Coble moduli#Reduction to Sterk]]; unit: computation; status: unproved; reason: this passage says cusp counts require explicit orbit enumeration and rejects discriminant-form shortcuts; locator: section 2, incidence proof paragraph <<}
```

## No Handoffs

Do not append a handoff, progress summary, routing ledger, completion note, next-steps
block, or source-level/global annotation to the annotated source.

Prior-agent prose about work status is not evidence.
It invites later agents to check receipts instead of reading the source, and it can
launder confabulated completion claims into the workflow.

If information matters, put it in CriticMarkup beside the source passage that supports
it:

- synthesis belongs near the turns or sections whose later resolution changes the
  mathematical state, not in an `entire source` comment;

- target research belongs in the route comment for the unit being routed;

- rejection and no-import reasons belong beside the rejected passage;

- supersession belongs beside both the superseded passage when practical and the later
  passage that changes the decision;

- human-review needs belong beside the exact disputed or uncertain mathematical content.

Each future agent must assess the source and annotations directly.
Lifecycle advancement happens only when a fresh direct pass finds no additional
source-local semantic work is needed.

If the synthesis is shallow, generic, or could have been written without reading the
whole source, the artifact is not incorporation-ready.
Make the gap visible beside the relevant passage instead of hiding it behind a status
claim.

Do not claim incorporation happened.
The incorporation agent decides what to edit.
