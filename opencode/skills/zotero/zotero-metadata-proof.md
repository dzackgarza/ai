---
name: zotero-metadata-proof
description: Use when identifying [[zotero/SKILL|Zotero]] metadata for a PDF, deciding whether to import a PDF as a [[zotero/SKILL|Zotero]] item, resolving ISBN/DOI/title-author metadata, or producing proof that a PDF corresponds to a [[zotero/SKILL|Zotero]] candidate record.
---

# [[zotero/SKILL|Zotero]] Metadata Proof

Use this skill to identify [[zotero/SKILL|Zotero]] metadata for a PDF under a strict artifact budget.
The output is not a research dossier; it is one compact proof capsule that supports
or rejects one [[zotero/SKILL|Zotero]] metadata candidate.

## Artifact Model

Hard cap for one PDF:

- the original PDF;
- the [[zotero/SKILL|Zotero]] item, only after approval/import;
- one compact proof capsule, preferably `book.zotero-proof.json` or a
  [[zotero/SKILL|Zotero]]-attached note/file.

Do not create per-source snapshots, screenshots, source-cache files, prose reports,
checklists, agent transcripts, or review memos. If the match cannot be proven within
one compact capsule, write `needs_review` in that capsule instead of generating more
evidence artifacts.

## Core Principle

Produce one minimal, auditable claim:

> This PDF corresponds to this [[zotero/SKILL|Zotero]] metadata, with enough provenance for a human or
> script to re-check it.

The agent is not the authority. Visible PDF identifiers and canonical records are the
authority. Confidence scores, summaries, and plausible bibliographic guesses are not
proof.

## Fast Path: Exact Identifier

For normal ISBN/DOI-resolvable books:

- Extract visible ISBNs or DOIs from the PDF front matter.
- Validate the identifier mechanically.
- Resolve the exact identifier through a canonical source.
- Compare the resolved title, creator, publisher, date, edition, and format against
  the PDF title/copyright pages.
- Build the [[zotero/SKILL|Zotero]] candidate from the canonical record with only mechanical
  normalization.
- If there are no conflicts, write one approved proof capsule and import only if
  import was requested or approved.

One exact ISBN/DOI record plus matching PDF front matter is usually sufficient. Require
a second source only when front matter is missing, the canonical source is weak, or
there is a concrete conflict.

## Lanes

### Lane 1: Exact-ID Approval

Approve when:

- the PDF visibly contains a valid ISBN or DOI;
- the identifier resolves to a canonical record;
- the canonical title and creator match the PDF;
- the [[zotero/SKILL|Zotero]] candidate is copied from that record;
- there are no obvious conflicts such as wrong edition, wrong volume, set ISBN versus
  volume ISBN, chapter DOI versus book DOI, or editor/author mismatch.

Output one approved proof capsule.

### Lane 2: Exact-ID With Conflict

Use when the identifier resolves but something is off. Examples:

- the PDF lists multiple ISBNs and the correct one is ambiguous;
- the resolved record title differs from the title page;
- the record describes a set, ebook, hardcover, paperback, chapter, or different
  edition;
- the record says editor where the PDF title page supports author, or the reverse.

Output one proof capsule with `status: "needs_review"` and a short `conflicts` array.
Do not create auxiliary evidence.

### Lane 3: No Exact ID

If there is no usable ISBN/DOI, search by title and creator. Require stronger
corroboration. If the match is not clean, write `needs_review`. Do not respond to
uncertainty by collecting more files.

## Proof Capsule Shape

For a clean ISBN/DOI case, keep the capsule small:

```json
{
  "schema": "zotero-proof.v1",
  "status": "approved",
  "pdf_sha256": "...",
  "zotero": {
    "itemType": "book",
    "title": "The Example Book",
    "creators": [
      {
        "creatorType": "author",
        "firstName": "Jane",
        "lastName": "Example"
      }
    ],
    "publisher": "Example Press",
    "date": "2021",
    "ISBN": "9781234567897"
  },
  "identity_proof": {
    "method": "visible_isbn_exact_match",
    "pdf_evidence": {
      "pages": [2, 4],
      "visible_isbn": "9781234567897",
      "visible_title": "The Example Book",
      "visible_creators": ["Jane Example"]
    },
    "canonical_record": {
      "source_type": "library_or_publisher_record",
      "lookup": "isbn:9781234567897",
      "url": "https://...",
      "retrieved_at": "2026-05-25T00:00:00Z",
      "record_id": "...",
      "returned_fields": {
        "title": "The Example Book",
        "creators": ["Jane Example"],
        "publisher": "Example Press",
        "date": "2021",
        "isbn": "9781234567897"
      }
    }
  },
  "review": {
    "verdict": "approved",
    "conflicts": [],
    "dropped_fields": []
  }
}
```

Do not include agent reasoning, long summaries, generated bibliographic explanations,
screenshots, confidence scores, or unverified fields.

## Field Overrides

Use identity-level proof first. Do not write verbose per-field proof when the exact
identifier record supports the whole [[zotero/SKILL|Zotero]] candidate and matches the PDF.

Use `field_overrides` only when a [[zotero/SKILL|Zotero]] field comes from a different source than the
canonical identifier record, for example:

```json
"field_overrides": {
  "translator": {
    "value": "John Translator",
    "source": "PDF title page, page 3",
    "reason": "Canonical ISBN record omitted translator"
  }
}
```

No override, no field-level paperwork.

## Review Gate

The adversarial reviewer is a gate, not a document generator. It may only:

- approve;
- downgrade to `needs_review`;
- remove unsupported fields.

The review section is exception-only:

```json
"review": {
  "verdict": "needs_review",
  "conflicts": [
    {
      "problem": "Same title and author appear in two editions; PDF copyright page is missing."
    }
  ],
  "dropped_fields": ["date", "edition"]
}
```

Do not record a checklist of attacks attempted.

## One-Book Workflow

For one PDF:

- compute the PDF hash;
- inspect front matter for title, creators, publisher, date, edition, visible ISBNs,
  and visible DOIs;
- if an ISBN/DOI is present, validate and resolve that exact identifier;
- compare the canonical record against the PDF front matter;
- if clean, build the [[zotero/SKILL|Zotero]] candidate and write one approved proof capsule;
- if conflicted, write one `needs_review` proof capsule;
- if no exact ID exists, search by title and creator and apply the same capsule-only
  approval or `needs_review` rule.

For simple ISBN/DOI metadata, the workflow should not generate four artifacts. For
difficult books, it still should not generate four artifacts. If one proof capsule is
not enough to make the result auditable, the item is not approved automatically.
