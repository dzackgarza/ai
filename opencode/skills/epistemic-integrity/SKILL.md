---
name: epistemic-integrity
description: Use when reporting negative findings, analyzing documents/transcripts/logs, summarizing source material, or reasoning from partial search/read evidence.
---
# Epistemic Integrity

## Core Policy

Absence of evidence is not evidence of absence.
Report the evidence boundary before stating the conclusion.

Use this skill whenever the task depends on:

- a failed search, missing result, or "not found" claim
- a summary or characterization of a document, transcript, log, codebase, or other
  non-homogeneous text
- partial reads caused by pagination, truncation, sampling, `head`, `tail`, line
  limits, search hits, snippets, or tool output caps
- deciding whether the inspected material is enough to support a whole-document,
  whole-repo, or whole-system claim

## Negative Findings

Every negative finding must use this five-field format:

```text
- Searched: [specific sources, URLs, docs, commands run]
- Found: [what was or was not found]
- Conclusion: [labeled as inference: "I believe", "based on limited evidence", etc.]
- Confidence: [High / Medium / Low]
- Gaps: [what remains unknown, unresolved, or uninspected]
```

Do not collapse "I did not find X" into "X does not exist."

Correct shape:

```text
- Searched: repo tree, README.md, docs/, `rg "webhook" src tests`
- Found: no documented webhook endpoint or route handler in inspected files
- Conclusion: based on this repository evidence, I found no documented webhook surface
- Confidence: Medium
- Gaps: generated routes and external deployment config were not inspected
```

## Coverage Before Claims

Natural language, code, logs, and transcripts are structured sequences, not
well-mixed samples.
A slice can be internally coherent and still be misleading about the whole.

If you have not read the relevant material end-to-end, you may report only what the
inspected section literally says, labeled with its range or search basis.
You may not characterize the whole artifact.

Allowed:

```text
Lines 1-300 of the 11,000-line transcript describe the setup phase.
I have not inspected the later turns, so this does not support a whole-session summary.
```

Not allowed:

```text
The transcript is about setup.
```

## Partial-Read Disclosure

When analysis is based on partial material, include:

- total known size, if available
- exact portion inspected: line ranges, sections, files, search query, command, or tool
  cap
- whether the claim is local to the inspected material or intended as a whole-artifact
  claim
- the unread or uninspected gaps that could change the conclusion

Do not use filenames, titles, metadata, file size, the user's description, or a worker's
summary as evidence for content.
Those are pointers to inspect, not the inspected source.

## Search Shape

When the search space is small and the conclusion matters, inspect it broadly instead
of stacking narrow guessed searches.
One `tree`, manifest read, or full directory inventory is stronger than many targeted
misses for expected names.

After a targeted miss, broaden before concluding:

- inspect the containing tree or index
- read manifests, route tables, docs, or generated file lists
- search for semantic neighbors and alternative names
- state the remaining blind spots

## Transcript and Agent-Output Work

For prior conversations and subagent work, load `reading-transcripts` for the parser and
location rules.
Treat summaries, task cards, hashes, and file existence as receipts, not semantic proof.

If the user asks for a review or assessment, inspect the artifact against the source
material and the user's purpose.
Do not call byte-level or checklist validation a review unless the requested judgment
was mechanical.

## Completion Gate

Before reporting, check:

- Did every negative finding use the five-field format?
- Are all whole-artifact claims backed by complete coverage?
- Are partial-read claims explicitly scoped to the inspected material?
- Did a targeted miss broaden to structural inspection before becoming a conclusion?
- Are metadata, filenames, summaries, and receipts treated only as pointers?
