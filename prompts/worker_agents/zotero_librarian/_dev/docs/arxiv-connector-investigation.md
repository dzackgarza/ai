# Investigate Zotero Connectors for arXiv Import

## Goal
Understand how Zotero Connectors parse arXiv pages and populate metadata automatically, then implement the same functionality in zotero_librarian.

## Tasks
- [x] Fetch Zotero Connectors repo structure → Verified: Found arXiv.org translator (1100 lines)
- [x] Extract arXiv translator source code → Verified: Complete translator saved to arXiv.org.js
- [x] Identify API endpoints used → Verified: arXiv Atom API + DOI content negotiation
- [x] Document metadata field mappings → Verified: Complete field mapping documented
- [x] Create implementation summary → Verified: Flow documentation complete
- [x] Implement `import_arxiv_paper()` → Creates Zotero item from arXiv ID
- [x] Implement `import_arxiv_papers()` → Batch import multiple papers

## Done When
- [x] Complete understanding of how connectors fetch and parse arXiv metadata
- [x] Documented API usage patterns for importing items
- [x] Can implement similar functionality in zotero_librarian
- [x] Functions exported and documented in README

## Key Findings

### Architecture
The Zotero Connector does NOT need the actual web page DOM. It:
1. Extracts arXiv ID from URL via regex
2. Calls arXiv Atom API: `https://export.arxiv.org/api/query?id_list={ID}`
3. Parses Atom XML response
4. Maps fields using `arXivCategories` lookup table
5. Creates Zotero item via `newItem.complete()`

### What We Implemented

#### Core Functions
- `import_arxiv_paper(zot, paper_id, collection_key=None)` - Import single paper
- `import_arxiv_papers(zot, paper_ids, collection_key=None)` - Batch import

#### Features (matching official translator)
- Fetches metadata from arXiv API
- Creates preprint item type
- Maps all fields: title, authors, abstract, date, URL, DOI
- Formats categories as human-readable tags (e.g., "math.AG" → "Mathematics - Algebraic Geometry")
- Attaches PDF automatically
- Supports adding to collection

#### Category Formatting
- `format_arxiv_category("math.AG")` → "Mathematics - Algebraic Geometry"
- `format_arxiv_categories(["math.AG", "cs.LG"])` → ["Mathematics - Algebraic Geometry", "Computer Science - Machine Learning"]

### Usage Example
```python
from zotero_librarian import get_zotero, import_arxiv_paper

zot = get_zotero()
result = import_arxiv_paper(zot, "2301.12345")
if result["success"]:
    print(f"Created item {result['key']}")
```

### Files Created/Modified
- `arXiv.org.js` - Complete official translator source (reference)
- `src/zotero_librarian/arxiv_tools.py` - Added import functions + category mappings
- `src/zotero_librarian/__init__.py` - Exported new functions
- `README.md` - Added documentation and examples
