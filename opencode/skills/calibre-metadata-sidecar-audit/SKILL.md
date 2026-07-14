---
name: calibre-metadata-sidecar-audit
description: Use when adversarially reviewing Calibre metadata proof sidecars, downgrading unsupported [[zotero/SKILL|Zotero]] metadata claims, checking ISBN/DOI identity proof, or deciding whether a sidecar should remain approved or become needs_review.
---

# Calibre Metadata Sidecar Audit

Audit an existing Calibre metadata proof sidecar as a gate. The audit does not create
research dossiers and does not produce a separate memo.

## Core Policy

- The sidecar is the only audit artifact. Update its `review` object only when the
  audit changes the verdict, conflicts, or dropped fields.
- Do not create screenshots, cached source records, extracted pages, transcripts,
  prose reports, or checklists.
- Do not approve from the agent's confidence, Calibre filename, folder name, or a
  plausible metadata match.
- Do not expand uncertainty into more paperwork. If the sidecar is not enough to prove
  the metadata under the artifact budget, downgrade to `needs_review`.

## Audit Powers

The auditor may only:

- leave `approved` unchanged when the identity proof is clean;
- downgrade to `needs_review`;
- remove unsupported [[zotero/SKILL|Zotero]] fields by adding them to `review.dropped_fields`;
- record short concrete conflicts in `review.conflicts`.

The auditor must not import into [[zotero/SKILL|Zotero]], attach files, rewrite the whole metadata
candidate for style, or add explanatory essays.

## Required Checks

Inspect only what is needed to test the proof:

- Does the `pdf_sha256` match the current PDF?
- Does the PDF evidence cite visible front-matter pages, ISBNs/DOIs, title, and
  creators accurately enough to re-check?
- Is the ISBN/DOI mechanically valid?
- Does the canonical record lookup match the exact identifier claimed?
- Do canonical title and creator agree with the PDF?
- Are edition, volume, set ISBN, format, publisher, date, and editor/author roles free
  of visible conflict?
- Are all [[zotero/SKILL|Zotero]] fields either supported by the canonical record or listed in
  `field_overrides` with concise PDF evidence?

Do not record this checklist in the sidecar. It is the audit procedure, not output.

## Conflict Handling

When the proof is not clean, set:

```json
"review": {
  "verdict": "needs_review",
  "conflicts": [
    {
      "problem": "PDF lists both set ISBN and volume ISBN; sidecar uses the set ISBN but the canonical record does not identify this volume."
    }
  ],
  "dropped_fields": []
}
```

Keep conflicts short and exception-only. Do not list every attack attempted.

## Dropped Fields

If the identity proof supports the item but not a specific [[zotero/SKILL|Zotero]] field, do not reject
the whole sidecar automatically. Remove or mark the unsupported field:

```json
"review": {
  "verdict": "approved",
  "conflicts": [],
  "dropped_fields": ["edition"]
}
```

Use `needs_review` instead when the unsupported field affects identity: wrong edition,
wrong volume, wrong work, wrong creator role, or chapter/article versus book.

## Approval Standard

Keep or set `approved` only when:

- the PDF hash and path identify the audited PDF;
- the visible PDF identifier resolves to the canonical record cited;
- the canonical record supports the [[zotero/SKILL|Zotero]] candidate;
- PDF front matter does not contradict the candidate;
- unsupported non-identity fields are dropped rather than silently retained.

## Final Check

Before stopping:

- validate the sidecar JSON parses;
- verify the final `review.verdict` is `approved` or `needs_review`;
- ensure the audit produced no auxiliary artifacts;
- report only the final verdict and any changed conflicts/dropped fields.
