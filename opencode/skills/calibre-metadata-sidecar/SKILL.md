---
name: calibre-metadata-sidecar
description: Use when creating compact metadata proof sidecars for Calibre book PDFs, resolving ISBN/DOI/title-author metadata, or preparing a Calibre book for possible Zotero import without generating evidence sprawl.
---

# Calibre Metadata Sidecar

Create one compact metadata proof sidecar for one Calibre book PDF. This skill is for
books already living in a Calibre-style library path, not for attaching artifacts to
Zotero.

## Artifact Model

Hard cap for one book:

- the original Calibre PDF;
- one compact JSON proof sidecar beside the PDF or in the book's `auto/` directory;
- a Zotero item only if a later workflow explicitly imports it.

Do not create screenshots, source-cache files, extracted HTML pages, prose reports,
checklists, agent transcripts, or multiple evidence files. If the metadata cannot be
proven inside one compact sidecar, write a `needs_review` sidecar instead of adding
more artifacts.

## Output Name

Prefer a deterministic sidecar name derived from the PDF stem:

```text
{Book Stem}_zotero-proof.json
```

If the Calibre book already has an `auto/` directory for extraction artifacts, place
the proof sidecar there. Otherwise place it beside the source PDF unless a repo-local
workflow says otherwise.

## Core Policy

- The sidecar proves identity; it does not collect research notes.
- Visible PDF identifiers and canonical records are the authority.
- Do not approve from filename, Calibre folder name, or plausible title/author match
  alone.
- Do not import into Zotero as part of this skill unless the user explicitly asked for
  import after approval.
- Do not include unverified Zotero fields just because they are plausible.
- Do not add field-level proof unless a field comes from somewhere other than the exact
  identifier record.

## Metadata Lanes

### Exact-ID Approval

Approve when:

- the PDF front matter visibly contains a valid ISBN or DOI;
- the identifier resolves to a canonical library, publisher, DOI, or equivalent record;
- the canonical title and creator agree with the PDF title/copyright pages;
- publisher/date/edition/format do not visibly conflict;
- the Zotero candidate is copied from the canonical record with only mechanical
  normalization.

Write one `approved` sidecar.

### Exact-ID Conflict

Write `needs_review` when the identifier resolves but there is a concrete ambiguity:

- multiple ISBNs with unclear set/volume/format meaning;
- title, creator, edition, publisher, or date conflict;
- DOI resolves to a chapter or article rather than the book;
- canonical record describes another format or edition.

Record only the conflict needed for human review.

### No Exact ID

If no usable ISBN/DOI is visible, search by title and creator. Require stronger
corroboration than a filename match. If the match is not clean, write
`needs_review`.

## Sidecar Shape

Keep the JSON compact:

```json
{
  "schema": "zotero-proof.v1",
  "status": "approved",
  "pdf_sha256": "...",
  "calibre": {
    "pdf_path": "/path/to/book.pdf",
    "book_dir": "/path/to/Book (123)"
  },
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

Do not include agent reasoning, confidence scores, long summaries, source snapshots,
or screenshots.

## Field Overrides

Use `field_overrides` only when a field is not supported by the canonical identifier
record, for example a translator visible on the PDF title page but absent from the
ISBN record. If there is no override, do not write field-level proof.

## Final Check

Before stopping:

- validate the JSON parses;
- confirm the sidecar names the exact source PDF path and hash;
- confirm `status` is either `approved` or `needs_review`;
- confirm no auxiliary evidence artifacts were created.
