# Inbox Analysis Pass

Use this reference when the task is to semantically parse a long-form mathematical inbox source and prepare incorporation suggestions. This pass is analysis only. Do not edit durable notes, MOCs, or paper files.

## Role

The analysis agent reads one inbox source deeply, researches the current vault for integration targets, and writes passage-local CriticMarkup suggestions into an annotated copy of the source.

The output is an annotated source in `INBOX/.annotated/` with the original basename preserved. The source remains a source artifact; the annotated copy is not a durable note.

This pass is allowed to fail. If you cannot reconstruct the mathematical story of the source and explain what should change in the vault, mark the source blocked and explain the blocker. Do not emit a plausible-looking annotated file whose only real content is metadata, target lists, hashes, or a few broad comments.

Solution-shaped filler is harmful. A bad analysis pass can mislead the incorporation agent and bury the raw source under false confidence.

## Directory Contract

- Input path: `INBOX/<original basename>`
- Output path: `INBOX/.annotated/<original basename>`
- Do not write to `INBOX/.incorporated/`.
- Do not create or edit permanent notes.
- Do not delete, rename, retitle, or normalize the raw source for graph hygiene.
- The annotated artifact is a full annotated copy of the source body, not a separate memo, digest, or selected-excerpt report. Add metadata, local CriticMarkup, and a handoff, but do not replace the source with a synthesized ledger.
- For text or markdown sources, create the annotated artifact by copying the raw source body first and then inserting CriticMarkup and handoff material into that copy. Do not ask the model to rewrite or regenerate the source body from memory.
- A complete rewrite is invalid even when it is semantically faithful. The analysis pass preserves provenance by editing a source copy, not by producing a new document that restates the source.
- Ground the analysis in the raw source and durable vault notes. Do not imitate prior processed copies or use them as format examples.

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

Use `analysis_status: in-progress` while reading if the artifact is still being developed. Do not use metadata to replace source text. Metadata tracks lifecycle and provenance; it does not summarize the mathematical payload.

Before final handoff, set `analysis_status` accurately:

- `complete`: the whole source was synthesized and routing targets were checked;
- `needs-human`: the source was read, but one or more mathematical or routing decisions remain disputed;
- `blocked`: the source could not be processed without more information or a stronger pass.

Do not leave `analysis_status: in-progress` on an artifact presented as final.

## Required Reading Posture

Read the source end-to-end before writing incorporation suggestions. The first deliverable is understanding, not markup.

Create the processed artifact early and use it as the working surface for understanding the source. Start with provenance and an `analysis_status: in-progress` header, then revise the artifact as the mathematical story becomes clear. Do not keep all analysis private until the end; if interrupted, the file should show what has actually been understood and what remains unresolved.

Preserve the source text in the working artifact literally. The only routine body changes are inserted CriticMarkup comments, inserted additions/deletions/substitutions when explicitly proposing durable text, and appended handoff material. Do not reflow paragraphs, normalize Unicode, change quote characters, convert source frontmatter into headings, duplicate heading markers, rewrite citation formatting, or otherwise "clean up" the source body while annotating. A compact synthesis and routing ledger may be added for handoff, but selected representative passages are not a substitute for inline annotation of the source. If the requested output directory is nonstandard, keep the same artifact semantics there: full source body plus annotations.

If you cannot insert annotations without regenerating or reformatting the source body, mark the pass `blocked`. A malformed but literal source copy is easier for a human to audit than a polished reconstruction that changes source text.

For chatlogs, transcripts, and iterative notes, reconstruct the whole mathematical conversation:

- What mathematical objects, claims, constructions, proof ideas, examples, computations, objections, and dead ends appear?
- Which statements survive the whole source as true, proved, usable, conjectural, open, false, superseded, or merely rhetoric?
- What changed from the beginning of the source to the end?
- Which false starts or incorrect framings are still useful as warnings, reviewer objections, or proof-gap remarks?
- What would be lost if the raw source disappeared after incorporation?

Only after answering those questions should you annotate. CriticMarkup is the visible trace of the synthesis; it is not a substitute for synthesis.

Use two passes when the source is long:

- **Story pass:** read through the whole source and write a compact narrative of the final mathematical state, including false starts and status changes.
- **Routing pass:** search the vault and attach CriticMarkup near the passages that actually support each durable update, rejection, warning, or blocker.

The story pass can be partial or in-progress. The routing pass cannot be marked complete until the whole source has been reconciled.

Process source-local passages after the whole-source read:

- Give stable locators to meaningful turns, sections, paragraph clusters, figures, tables, displayed formulas, and formal statements.
- Route mathematical insights, not headings. A heading can help locate content, but it is not a unit of meaning.
- Preserve the role of discarded material. A false theorem-shaped claim may become a warning remark, a rejected route, or an objection-resolution note, not simply disappear.
- Keep repeated or near-duplicate passages only when they add a new status change, new evidence, or a useful formulation.
- Treat disputes as first-class content. If the user challenges a claim and a later assistant defends it, do not automatically choose either side. Mark the issue as `needs-human` or preserve it as an objection-resolution thread unless the source itself settles it.
- Do not make a giant exhaustive table to prove you read the source. Include enough local annotations and a short synthesis handoff that an incorporation agent can update the vault intelligently.

## Quality Gate

Before marking `analysis_status: complete`, inspect your own annotated source as if another agent produced it.

The pass is not complete if any of these are true:

- a reader could have written the annotations after skimming headings rather than understanding the mathematical development;
- the handoff does not say what the source contributes mathematically after false starts and later corrections are reconciled;
- true claims, false framings, conjectures, open questions, proof obligations, and dead ends are not distinguished;
- comments say only `accepted target`, `route to`, `merge into`, or similarly vague phrases;
- comments identify a note but not the mathematical payload, proposed vault action, status, and source-grounded reason;
- comments use shorthand targets such as "same note", "above note", or "this note" instead of naming the actual target note or section;
- the source is treated as a list of independent snippets when its value is the narrative of correction, refinement, or synthesis;
- a disputed item is promoted to a proof obligation without acknowledging the dispute and whether the source resolves it;
- a disputed item is marked `needs-human` locally but then reappears in the handoff as an ordinary open proof obligation or conjecture;
- any target path points to a folder where the note does not actually exist;
- any `#Heading` or block anchor in a target link was not checked against the current target note;
- final metadata says `in-progress` while the handoff claims the pass is complete;
- the output is a synthetic analysis memo, selected-excerpt report, or routing ledger rather than a full annotated copy of the source;
- the source body has been normalized, rewrapped, reformatted, or otherwise rewritten outside local CriticMarkup insertions and appended handoff material;
- the artifact was produced by a whole-file write/regeneration path rather than by copying the source and applying targeted insertions;
- the artifact is patterned on previous processed copies rather than grounded in the raw source and durable vault notes;
- the handoff is doing all of the analytic work that should be visible beside the source passages;
- the output mostly proves that files exist, hashes were computed, metadata was added, or target notes were listed;
- duplicate or near-duplicate sources have not been cross-compared for substantive differences.

When the pass fails this gate, set `analysis_status: blocked` or `needs-human`, leave the raw source unincorporated, and state exactly what remains unread, unclassified, or unresolved.

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

Vault research must be visible in the annotation or handoff. Prefer a target section or heading, not just a note title. If the right target does not exist, say which nearby notes were checked and why the proposed new note passes the stable referent test.

Organize routing around mathematical objects and claims, not source order alone. A long chat may contribute one coherent update spread across many turns; route that update once, with locators for the important turns.

Target paths must be real. Before finalizing a wikilink or path, verify whether the target note already exists and use its actual vault location. If no matching note exists, label the target as proposed and state which existing notes were checked.

Anchors must be real too. Before finalizing `[[Target#Heading]]` or a block reference, inspect the current target note's headings or blocks and verify the exact anchor exists. Use the displayed heading text, not a slugified or URL-style version. If the target note exists but the right heading does not, either route to the note without an anchor, propose the heading explicitly, or mark the route `needs-human`; do not invent an anchor.

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

- target note and section, or a specific proposed new-note title with a stable-referent reason;
- mathematical role from `mathematical-unit-library.md` when a formal unit is being incorporated;
- action: add, merge, demote, promote, split, reject, preserve-source-visible, or needs-human;
- proof/status: proved, source-backed, conjectural, unproved, open, proof-sketch, contradicted, superseded, duplicate, rejected, disputed, needs-human, blocked, external, or source-uncertain;
- reason grounded in the source;
- source-local locator when the surrounding passage is not enough.

Repeat the actual target in each comment. Do not write "same note", "above note", "this note", or similar shorthand, because comments may be read out of order by the incorporation agent.

Use exact CriticMarkup syntax. A comment starts with `{>>` and ends with `<<}`. Do not escape the closing marker, and do not end comments with `\}` or `}` alone.

Keep status fields atomic. Do not write prose statuses such as `proven? no`, `accepted`, `preserved with reservation`, or `proved-in-source`; instead choose the nearest status from the list and put nuance in the reason. Slash-separated values such as `disputed/needs-human` are invalid. If a disputed passage needs human judgment, choose `needs-human` as the status and say in the reason that the passage is disputed; if the task is only to preserve the disagreement, choose `disputed`.

Keep mathematical unit fields atomic too. Do not write `fact/conjecture`, `construction/question`, `remark/question`, or similar hybrid labels. Split the route into separate comments, or choose the primary unit and put the nuance in the reason.

After the semantic pass is done, do a narrow markup hygiene pass: every `{>>` comment must close with `<<}`, no comment may close with `>>}` or `\}`, every `status:` value must come from the allowed list above, and every `unit:` value must come from `mathematical-unit-library.md`. This check does not prove quality; it only prevents malformed annotations from blocking incorporation.

Bad comment:

```markdown
{>> route: accepted target [[Cusp data for polarized Coble moduli]] <<}
```

Good comment:

```markdown
{>> route: merge into [[Cusp data for polarized Coble moduli#Reduction to Sterk]]; unit: computation; status: unproved; reason: this passage says cusp counts require explicit orbit enumeration and rejects discriminant-form shortcuts; locator: section 2, incidence proof paragraph <<}
```

## Handoff Output

At the end of the annotated source, add a concise handoff section only if the source format allows it without corrupting the source. The handoff is an index of local annotations, not a substitute for them.

Include:

- source ID;
- a compact mathematical synthesis of the whole source: what survived, what failed, what remains open, and what the source contributes to the paper/vault;
- candidate target notes and the existing headings or neighborhoods inspected;
- routing decisions grouped by mathematical object or claim, with source locators for the passages that matter;
- high-risk suggestions;
- superseded suggestions and the later source location that superseded them;
- suggested new notes, if any, with the stable referent test;
- explicit blockers for the incorporation agent.

If the synthesis is shallow, generic, or could have been written without reading the whole source, the pass is not complete. Mark it blocked instead of hiding the gap.

Do not claim incorporation happened. The incorporation agent decides what to edit.
