---
name: organizing-pdfs
description: 'Use when organizing a directory of PDFs against [[zotero/SKILL|Zotero]] or another reference
  library: bucketing local PDFs, finding DOI/ISBN/source provenance, creating [[zotero/SKILL|Zotero]]
  items, attaching PDFs, trashing verified redundant local copies, and leaving a final contents ledger.
  Trigger on requests to sort PDFs, clean a downloads PDF folder, compare PDFs to [[zotero/SKILL|Zotero]],
  import PDFs into [[zotero/SKILL|Zotero]], or decide what remaining PDFs are.'
---

# Organizing PDFs

Use this skill for cleanup runs where a directory contains loose PDFs that need to be
identified, matched to [[zotero/SKILL|Zotero]], imported, attached, and then removed from the local
staging folder when [[zotero/SKILL|Zotero]] has become the authority.

This is a semantic workflow. Filenames, hashes, and search hits are leads, not proof.

## Load These Skills

- [[reading-pdfs/SKILL|reading-pdfs]] before extracting or inspecting PDF contents.
- [[zotero/SKILL|zotero]] or [[zotero-api/SKILL|zotero-api]] before reading or writing [[zotero/SKILL|Zotero]] state.
- [[zotero-pdf-extraction-attachments/SKILL|zotero-pdf-extraction-attachments]] when verifying [[zotero/SKILL|Zotero]] parent/child attachment state.
- [[epistemic-integrity/SKILL|epistemic-integrity]] before reporting missing sources, no-identifier findings, or any
  conclusion based on partial PDF reads.
- [[git-guidelines/SKILL|git-guidelines]] before deleting or trashing local files; use recoverable trash.
- [[response-preparation/SKILL|response-preparation]] before final reports.

## Core Rule

Once a live [[zotero/SKILL|Zotero]] parent item and matching PDF attachment are verified, the local
download-folder copy is redundant. Move the local copy to recoverable trash unless the
user explicitly says to keep it.

Verification means a live [[zotero/SKILL|Zotero]] API reread after the write, not a script's intended
state, a filename match, or a stale report.

## Workflow

1. Inventory the local directory.
   - List all PDFs recursively.
   - Record page counts with `pdfinfo`.
   - Extract the first few pages with `pdftotext`.
   - For OCR-poor or image-only files, render and inspect first-page thumbnails.
   - Keep generated working files clearly named so they can be cleaned later.

2. Manually pre-bucket by intelligent inspection.
   - Likely library works: books, papers, theses, arXiv/preprint items, published notes.
   - Likely non-library material: random lecture notes, local notes, homeworks, exams,
     syllabi, handwritten notes, article snippets, personal drafts.
   - Middle ground: ambiguous titled notes, theses, proceedings chapters, course notes
     with authors and stable source pages.

3. Match against [[zotero/SKILL|Zotero]] semantically.
   - Do not expect local attachment filenames to match [[zotero/SKILL|Zotero]] filenames.
   - Use title page, author, date, DOI/ISBN/arXiv, source URL, and content identity.
   - Byte identity is useful but not required; a source may prepend front matter while
     the underlying work is the same.
   - For edge cases, inspect the PDF and the [[zotero/SKILL|Zotero]] item/children before deciding.

4. Bucket results.
   - In [[zotero/SKILL|Zotero]] with PDF already.
   - In [[zotero/SKILL|Zotero]] but missing PDF.
   - Not in [[zotero/SKILL|Zotero]].
   - Keep buckets current with the live filesystem and live [[zotero/SKILL|Zotero]] state. Recompute or
     verify before using an old report.

5. Trash verified duplicates.
   - For items already in [[zotero/SKILL|Zotero]] with a semantically matching PDF child, move the local
     PDF to recoverable trash.
   - Use `gio trash` or the local equivalent, never irreversible `rm`.
   - Write a small trash log when many files are moved.

6. Find identifiers only where plausible.
   - Look for DOI, ISBN, [[research-discovery/arxiv/SKILL|arXiv]] ID, MR/Zbl, or repository handles for real works.
   - Do not waste identifier-search time on obvious handwritten notes, homework,
     private drafts, exams, or local handouts.
   - For negative findings, state what was searched and what remains unknown.

7. Import identifier-backed works.
   - Prefer [[zotero/SKILL|Zotero]]'s add-by-identifier/import-by-identifier surface.
   - Deduplicate against existing [[zotero/SKILL|Zotero]] items before importing.
   - Attach the local PDF to the chosen or created parent.
   - Reread the parent and children through the live [[zotero/SKILL|Zotero]] API.
   - After verified attachment, trash the local PDF.

8. Find source/provenance for no-identifier works.
   - Accept direct PDFs, author pages, repository records, [[research-discovery/arxiv/SKILL|arXiv]] records, DOI landing
     pages, institutional repository pages, or strong bibliographic pages.
   - Correct wrong provenance immediately; do not let a plausible source for a different
     work drive [[zotero/SKILL|Zotero]] metadata.
   - For accepted no-identifier items, create a [[zotero/SKILL|Zotero]] parent with appropriate type,
     creators, date, URL, and provenance in `Extra`.
   - Apply the library's accepted-provenance tag only when there is inspected evidence
     and the local policy permits it.
   - Attach, reread, verify, then trash the local PDF.

9. Leave a final contents ledger.
   - After imports and trashing, write one Markdown file in the directory describing
     each remaining PDF.
   - Include path, page count, and a short practical identification note.
   - State the coverage basis: page counts, early text extraction, visual checks for
     image-only files, not full-document summaries unless actually read.

10. Clean intermediate artifacts.
    - Keep the final ledger.
    - Trash stale bucket reports, identifier work JSON, source work JSON, and attach/trash
      logs once their purpose is finished and no longer needed.
    - Preserve unrelated non-PDF files unless their provenance is known and the user
      asked to remove them.

## Decision Boundaries

- Do not report "not in [[zotero/SKILL|Zotero]]" from filename search alone.
- Do not create a [[zotero/SKILL|Zotero]] item from a guessed title when the PDF's title page or source
  indicates a different work.
- Do not stop after attaching if the cleanup objective implies removing redundant local
  staging copies.
- Do not trash personal/local material merely because it is not a [[zotero/SKILL|Zotero]] work.
- Do not keep stale generated reports that contradict the current directory state.

## Final Report

Report only what the user cannot see from the filesystem:

- the final ledger path, if created;
- any unresolved ambiguous items;
- any items intentionally kept because they are personal/local or not library material;
- any [[zotero/SKILL|Zotero]] lint warnings or metadata gaps that remain after writes.

Avoid restating every item unless the user asked for a full report.
