# Environment Traps and Anti-Patterns

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

- A trailing comment after an answer’s references list is not passage-local analysis of
  the answer’s mathematical claims.

- An honest partial artifact with one source segment analyzed well is better than a fake
  incorporation-ready artifact with broad comments over the hard parts.

- “No blockers” is false when broad comments still hide unexpanded claim-list turns.

- A solution-shaped annotated file can be worse than an unprocessed source if it hides
  missing analysis.

- A polished-looking ledger can still be slop if it does not explain the source’s final
  mathematical contribution.

- A selected-excerpt report is not an annotated source; it may hide the exact passages
  the incorporation agent needs to audit.

- A rewrapped or normalized source body is not source preservation; it can destroy
  locators and make human audit harder.

- A model-regenerated transcript is not a source copy, even when it contains all the
  same ideas.

- A whole-file Write path is a red flag for analysis-pass work.
  Prefer constrained agents and targeted edits into a literal source copy.

- An annotated artifact patterned on previous processed outputs is not independent
  evidence of source understanding.
  Analysis agents must work from the raw source and the durable vault unless comparative
  review is the explicit task.

- A wikilink to a plausible title is not a checked target.
  Verify the actual existing note path or mark it as proposed.

- A wikilink with a plausible heading is not a checked section.
  Verify every `#Heading` or block anchor against the target note’s displayed heading
  text, never a slugified guess, and never write ambiguous references such as “same
  note#Heading”.

- A disputed source claim is not automatically a proof obligation.
  Preserve the dispute unless the source resolves it.

- Renaming a source file is not provenance preservation.

- A note can be nonempty and still be fake if it contains only scaffolding.

- Images, diagrams, and scanned math often carry information that prose extraction
  misses.

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
| Bucketed duplicate dismissal | Marks a long claim inventory or proof-obligation list as “already covered” without unit-level actions | Route or reject the internal mathematical units at their own subsection or paragraph-cluster boundaries |
| Repetition shortcut | Marks a repeated or condensed claim-list turn as duplicate because another turn was annotated | Check the repeated turn for differences and annotate its internal sections, or mark it `needs-human` locally |
| End-of-answer routing | Places the only comment after a long answer’s references/source list | Attach comments beside the internal mathematical sections they classify |
| Completion pressure | Compresses hard sections to make the artifact look done | Finish one coherent segment well and leave unresolved passages for a fresh direct pass |
| Handoff laundering | Adds a progress summary, routing ledger, or completion claim that later agents may trust instead of reading the source | Put material facts only in passage-local CriticMarkup beside the source text that supports them |
| Premature retirement | Says “fully mapped”, “no blockers”, or “ready to retire” while broad annotations remain | Keep the source in `.annotated` until a fresh direct pass finds no further local semantic work |
| Opaque processing | Advances a source lifecycle without showing which exact passages were routed, imported, rejected, or blocked | Mark local routing and non-import decisions beside the relevant source passages |
| Reward-hacked cleanup | Renames or deletes sources after creating fake notes that preserve little content | Preserve the source and prove semantic transfer item by item before any human-approved deletion |
| Silent semantic drift | “Cleans up” notation or wording and changes meaning | Preserve notation or record the translation explicitly |
| Software-status leakage | Uses labels like “open issue” or “framework” instead of mathematical types | Normalize to conjecture, question, construction, remark, theorem, etc. |
| Dirty-source deletion | Deletes images/PDFs/chats after extraction | Keep originals until audit and retirement criteria pass |
| Tool-blind editing | Breaks links/properties with plain file edits | Prefer [[obsidian/SKILL|Obsidian]]-aware tools and controlled scripts |
| Regex cascade corruption | Uses repeated broad regexes to fix earlier broad regexes | Revert, inspect, narrow scope, and re-run safely |

