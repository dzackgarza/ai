# Mathematics Paper Retrieval

## Purpose

Find mathematics papers, resolve reliable metadata, store PDFs in the canonical library,
and route extraction through the PDF workflow.

## Source Strategy

- Use `arxiv` for preprints, arXiv IDs, TeX/PDF links, and fast abstract lookup.

- Use this `literature-review` skill for Semantic Scholar, OpenAlex, Crossref, and
  PubMed metadata searches.

- Use Semantic Scholar/OpenAlex for citation counts, references, and related paper
  discovery.

- Use Crossref for DOI normalization and journal metadata.

- Use Zotero skills for local library identity, attachments, and duplicate detection.

## Workflow

1. Search multiple metadata sources and deduplicate by DOI, arXiv ID, or exact
   title/author/year match.

2. Resolve the paper identity before downloading: DOI, arXiv ID, Zotero key, venue,
   year, and author list.

3. Store PDFs under `~/pdfs` in a library-like subfolder tree.

4. Route text/OCR extraction through `~/pdf-extraction` and its justfile recipes; do not
   put extraction artifacts in source repositories.

5. When reading the paper, use `reading-pdfs` or the PDF extraction endpoint rather than
   ad hoc PDF parsing.

## Responsibility Split

Paper retrieval responsibilities are separate:

- search: `literature-review` and `arxiv`,

- download/storage: Zotero plus `~/pdfs`,

- extraction: `~/pdf-extraction`,

- reading/synthesis: `reading-pdfs`, `read-arxiv-paper`, and
  `research-synthesis-workflow`.

Only add a new MCP surface if a current design proves it adds capability beyond these
existing endpoints.
