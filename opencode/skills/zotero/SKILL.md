---
name: zotero
description: Manage [[zotero/SKILL|Zotero]] reference libraries via the Web API. Search, list, add items by DOI/ISBN/PMID (with duplicate detection), delete/trash items, update metadata and tags, export in BibTeX/RIS/CSL-JSON, batch-add from files, check PDF attachments, cross-reference citations, find missing DOIs via CrossRef, and fetch open-access PDFs. Supports --json output for scripting. Use when the user asks about academic references, citation management, literature libraries, PDFs for papers, bibliography export, or [[zotero/SKILL|Zotero]] specifically.
metadata: {"clawdbot":{"emoji":"📚","requires":{"env":["ZOTERO_API_KEY","ZOTERO_USER_ID"]},"primaryEnv":"ZOTERO_API_KEY"}}
---
# [[zotero/SKILL|Zotero]] Skill

Interact with [[zotero/SKILL|Zotero]] personal or group libraries via the REST API v3.

## Setup

Requires two environment variables:

```
ZOTERO_API_KEY   — Create at https://www.zotero.org/settings/keys/new
ZOTERO_USER_ID   — Found on the same page (numeric, not username)
```

For group libraries, set `ZOTERO_GROUP_ID` instead of `ZOTERO_USER_ID`.

Optional env var for CrossRef/Unpaywall polite pool (improves DOI lookup success rate):

```
CROSSREF_EMAIL   — Your email (optional; uses fallback if unset)
```

If credentials are missing, tell the user what’s needed and link them to the key
creation page.

## CLI Script

All operations use `scripts/zotero.py` (Python 3, zero external dependencies).

```bash
python3 scripts/zotero.py <command> [options]
```

### Commands

| Command | Description | Example |
| --- | --- | --- |
| `items` | List top-level items | `zotero.py items --limit 50` |
| `search` | Search by query | `zotero.py search "cognitive load"` |
| `get` | Full item details + attachments | `zotero.py get ITEMKEY` |
| `collections` | List all collections | `zotero.py collections` |
| `tags` | List all tags | `zotero.py tags` |
| `children` | List attachments/notes for item | `zotero.py children ITEMKEY` |
| `add-doi` | Add item by DOI (dedup enabled) | `zotero.py add-doi 10.1234/example` |
| `add-isbn` | Add item by ISBN (dedup enabled) | `zotero.py add-isbn 978-0-123456-78-9` |
| `add-pmid` | Add item by PubMed ID | `zotero.py add-pmid 12345678` |
| `delete` | Move items to trash (recoverable by default) | `zotero.py delete KEY1 KEY2 --yes` |
| `update` | Modify item metadata/tags | `zotero.py update KEY --add-tags "new"` |
| `export` | Export as BibTeX/RIS/CSL-JSON | `zotero.py export --format bibtex` |
| `batch-add` | Add multiple items from file | `zotero.py batch-add dois.txt --type doi` |
| `check-pdfs` | Report which items have/lack PDFs | `zotero.py check-pdfs` |
| `crossref` | Match citations vs library | `zotero.py crossref bibliography.txt` |
| `find-dois` | Find & add missing DOIs via CrossRef | `zotero.py find-dois --limit 10` |
| `fetch-pdfs` | Fetch open-access PDFs for items | `zotero.py fetch-pdfs --dry-run` |

### Global Flags

- `--json` — JSON output instead of human-readable (works with items, search, get)

### Common Options

- `--limit N` — Max items to return (default 25)

- `--sort FIELD` — Sort by dateModified, title, creator, date

- `--direction asc|desc` — Sort direction

- `--collection KEY` — Filter by or add to collection

- `--type TYPE` — Filter by item type (journalArticle, book, conferencePaper, etc.)

- `--tags "tag1,tag2"` — Add tags when creating items

- `--force` — Skip duplicate detection on add commands

## Workflows

### Audit Attachment Completeness

When answering whether [[zotero/SKILL|Zotero]] items have PDFs, markdown extractions, or other
attachments, define the item universe before counting.

- Do not treat a collection query as a library-wide result unless the user
  explicitly scoped the question to that collection.
- If the user says "all [[zotero/SKILL|Zotero]] items", "the library", or points at an item visible
  in the [[zotero/SKILL|Zotero]] UI, query all top-level parent items, then inspect each parent's
  children for attachment content types.
- Use pagination for both parent item queries and attachment queries. A single
  `limit=500` or collection response is not evidence of full coverage.
- Count markdown extraction coverage parent-by-parent: parent item has at least
  one PDF child and at least one child attachment with
  `data.contentType == "text/markdown"`.
- If any item is cited as a counterexample, query that exact title/key and its
  children before making or defending an aggregate claim.
- Report the exact scope used in the conclusion, e.g. "collection X" versus "all
  parent items with PDF children in the library".

Use this method for library-wide markdown coverage against the workstation-local
[[zotero/SKILL|Zotero]] API:

1. Fetch all items with pagination from `http://127.0.0.1:23119/api/users/0/items`.
2. Keep only top-level parent items: `data.itemType != "attachment"`.
3. For each parent key, fetch all children with pagination from
   `/api/users/0/items/{KEY}/children`.
4. Count a parent as needing extraction when it has at least one child attachment
   with `data.contentType == "application/pdf"` and no child attachment with
   `data.contentType == "text/markdown"`.
5. For a named counterexample, search the exact title with `/items?q=...`, inspect
   each matching parent and its children, and check whether the parent belongs to
   the collection being discussed before using it to confirm or refute the aggregate
   result.

The observed failure mode: querying only
`/collections/JEJSXB2N/items?limit=500` produced 433/433 markdown coverage for that
collection, but a full-library parent/child walk found 465 parent items with PDF
children and 26 of those had no markdown child. The counterexample title
`Introduction to the Minimal Model Problem` had a PDF-only parent outside
`JEJSXB2N`, so the collection-scoped result was not a library-wide result.

### Add a paper by DOI

```bash
python3 zotero.py add-doi "10.1093/jamia/ocaa037" --tags "review"
# Warns if already in library. Use --force to override.
```

Duplicate detection: translates DOI to metadata, searches library by first author,
compares DOI fields.

### Bulk add from a file

```bash
# One identifier per line, # for comments
python3 zotero.py batch-add dois.txt --type doi --tags "imported"
```

Skips duplicates. Reports summary: added/skipped/failed.

### Export bibliography

```bash
python3 zotero.py export --format bibtex --output refs.bib
python3 zotero.py export --format csljson --collection COLLKEY
```

### Update tags/metadata

```bash
python3 zotero.py update ITEMKEY --add-tags "important" --remove-tags "unread"
python3 zotero.py update ITEMKEY --title "Corrected Title" --date "2024"
python3 zotero.py update ITEMKEY --doi "10.1234/example"
python3 zotero.py update ITEMKEY --url "https://example.com/paper"
python3 zotero.py update ITEMKEY --add-collection COLLKEY
```

### Delete items

```bash
python3 zotero.py delete KEY1 KEY2 --yes           # Trash (recoverable, default)
python3 zotero.py delete KEY1 --permanent --yes    # Permanent delete
```

### Cross-reference citations

```bash
python3 zotero.py crossref my-paper.txt
```

Extracts `Author (Year)` patterns from text and matches against library.

### Find missing DOIs

```bash
# Dry run (default) — show matches without writing anything
python3 zotero.py find-dois --limit 20

# Actually write DOIs to Zotero
python3 zotero.py find-dois --apply

# Filter by collection
python3 zotero.py find-dois --collection COLLKEY --apply
```

Scans journalArticle and conferencePaper items missing DOIs, queries CrossRef, and
matches by title similarity (>85%), exact year, and first author last name.
Dry run by default — use `--apply` to write.
Only patches the DOI field; never touches other metadata.
1s delay between CrossRef requests (polite pool with mailto).

### Fetch open-access PDFs

```bash
# Dry run — show which PDFs are available and from where
python3 zotero.py fetch-pdfs --dry-run --limit 10

# Fetch and attach as linked URLs (no storage quota used)
python3 zotero.py fetch-pdfs --limit 20

# Also save PDFs locally
python3 zotero.py fetch-pdfs --download-dir ./pdfs

# Upload to Zotero storage instead of linked URL
python3 zotero.py fetch-pdfs --upload --limit 10

# Only try specific sources
python3 zotero.py fetch-pdfs --sources unpaywall,semanticscholar
```

Tries three legal OA sources in order: Unpaywall → Semantic Scholar → DOI content
negotiation. By default creates linked URL attachments (no [[zotero/SKILL|Zotero]] storage quota needed).
Use `--upload` for full S3 upload to [[zotero/SKILL|Zotero]] storage.
Use `--download-dir` to also save PDFs locally.

**Sources:** `unpaywall`, `semanticscholar`, `doi` (default: all three)

**Rate limits:** 1s between Unpaywall/Semantic Scholar requests, 2s between DOI
requests.

### Scripting with JSON

```bash
python3 zotero.py --json items --limit 100 | jq '.items[].DOI'
python3 zotero.py --json get ITEMKEY | jq '.title'
```

## Notes

- Zero dependencies — Python 3 stdlib only (urllib, json, argparse)

- Write operations require an API key with write permissions

- If [[zotero/SKILL|Zotero]] translation server is down (503), DOI lookups fall back to CrossRef

- **Input validation:** DOIs must be `10.xxxx/...` format.
  Item keys are 8-char alphanumeric (e.g., `VNPN6FHT`). ISBNs must be valid checksums.

- `check-pdfs` fetches all items; for large libraries (500+), this may be slow

- `fetch-pdfs` also processes all items — use `--collection` to scope for large
  libraries

- Rate limits are generous; batch-add includes 1s delay between items

- For common errors and troubleshooting, see
  [references/troubleshooting.md](references/troubleshooting.md)
