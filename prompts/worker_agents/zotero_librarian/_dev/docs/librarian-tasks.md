# Librarian Agent - Quality Checks

Each task maps to tools in `src/zotero_librarian/__init__.py`.

---

## 1. Can I find this?

- Item has a title (not empty, not "Untitled")
- Item has at least one author/creator
- Item has a year
- Item is in at least one collection
- Item has at least one tag or subject

**Tools:** `items_without_field()`, `items_not_in_collection()`, `items_without_tags()`

---

## 2. Is it complete?

**Journal article:** has journal name, volume, pages  
**Book:** has publisher, place  
**Book chapter:** has book title, page range  
**Thesis:** has university  
**Everything:** has DOI or other identifier if one exists

**Tools:** `items_missing_required_fields()`

---

## 3. Is the PDF there?

- Item has a PDF attached
- PDF file is not corrupted/empty
- PDF actually matches the item (not a different paper)

**Tools:** `items_without_pdf()`, `items_without_attachments()`, `attachment_info()`

---

## 4. Are there duplicates?

- Same DOI appears twice
- Same title + author + year appears twice
- Preprint and final version both exist

**Tools:** `duplicate_dois()`, `duplicate_titles()`, `find_duplicates_by_field()`

---

## 5. Is anything broken?

- DOI actually resolves (not a typo)
- URL links work
- No placeholder text like "[No title]" or "TBD"

**Tools:** `validate_doi()`, `validate_isbn()`, `validate_issn()`, `items_with_invalid_doi()`, `items_with_invalid_isbn()`, `items_with_invalid_issn()`, `items_with_broken_urls()`, `items_with_placeholder_titles()`

---

## 6. Does it belong somewhere?

- Item is filed in a collection (not floating in "Unfiled Items")
- Collection names make sense (not "stuff", "temp", "new folder")

**Tools:** `items_not_in_collection()`, `empty_collections()`, `single_item_collections()`, `get_collections()`

---

## 7. Are names consistent?

- Author names use same format throughout
- Journal names consistent (not "Nature" vs "Nature (London)" vs "NATURE")
- Tags use same spelling (not "machine-learning" vs "machine_learning")

**Tools:** `creator_name_variations()`, `journal_name_variations()`, `similar_tags()`, `all_tags()`

---

## 8. Is the information correct?

- DOI resolves to the actual paper
- Author list is complete
- Journal name is the real journal
- Item type is correct (preprint vs journal article vs thesis)

**Tools:** `validate_doi()`, `preprints_without_doi()`

---

## 9. Is there a text version? (nice-to-have)

- PDF has an attached markdown or text extract
- Notes contain transcribed key passages

**Tools:** `items_with_notes()`, `get_notes()`

---

## 10. More completeness checks

- Abstract field has the actual abstract
- Enough fields for BibTeX export
- PDF unavailable items tagged (e.g., "paywalled")
- Item type tagged clearly

**Tools:** `items_without_abstract()`, `all_tags()`, `items_by_tag()`

---

## 11. Citation metadata

- "Cites" list attached
- "Cited by" list attached
- Citations use canonical IDs (DOI, BibTeX key)

**Tools:** `get_citations()`, `items_without_cites()`, `items_without_cited_by()`

---

That's it. Everything else is nice-to-have.
