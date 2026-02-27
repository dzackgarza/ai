# Zotero Librarian - Suggested Commands

## Installation

```bash
pip install zotero-librarian
```

With arXiv tools:
```bash
pip install zotero-librarian[arxiv]
```

## Testing

```bash
pytest
```

Run specific test files:
```bash
pytest test_tools.py
pytest test_arxiv_tools.py
```

## Basic Usage

Initialize the Zotero client:
```python
from zotero_librarian import get_zotero

zot = get_zotero()
```

## Common Examples

### Find items without PDFs and tag them
```python
from zotero_librarian import get_zotero, items_without_pdf, batch_add_tags

zot = get_zotero()
no_pdf = items_without_pdf(zot)
batch_add_tags(zot, no_pdf[:10], ["needs-pdf"])
```

### Import by DOI
```python
from zotero_librarian import get_zotero, import_by_doi

zot = get_zotero()
item = import_by_doi(zot, "10.1038/nature12373")
```

### Find duplicates
```python
from zotero_librarian import get_zotero, duplicate_dois

zot = get_zotero()
dups = duplicate_dois(zot)
for doi, items in dups.items():
    if len(items) > 1:
        print(f"Duplicate: {doi}")
```

### Export library
```python
from zotero_librarian import get_zotero, export_to_json, export_to_bibtex

zot = get_zotero()
export_to_json(zot, "backup.json")
export_to_bibtex(zot, "library.bib")
```

### Library statistics
```python
from zotero_librarian import get_zotero, library_summary, items_per_type

zot = get_zotero()
print(library_summary(zot))
print(items_per_type(zot))
```

### arXiv tools
```python
from zotero_librarian import search_arxiv_papers, download_arxiv_paper

papers = search_arxiv_papers("derived categories", max_results=10, categories=["math.AG"])
if papers:
    download_arxiv_paper(papers[0]["id"])
```

## Key Functions

- Read: `all_items()`, `search_by_title()`, `items_without_pdf()`
- Write: `batch_add_tags()`, `add_item_to_collection()`, `delete_item()`
- Import: `import_by_doi()`, `import_by_isbn()`, `import_arxiv_paper()`
- Export: `export_to_json()`, `export_to_bibtex()`
- Stats: `library_summary()`, `items_per_type()`, `tag_cloud()`
