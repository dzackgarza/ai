---
name: zotero-api
description: Use when you need to query Zotero data, find references, export citations, search for papers, or fetch PDFs using the local Zotero Web API cache.
---

# Zotero Local API

This machine has a local, read-only cache of the Zotero v3 API at `https://zotero.dzackgarza.com`.
The primary user ID is `1049732`. No authentication or API keys are required.

Base URL: `https://zotero.dzackgarza.com/api/users/1049732`

## Query Patterns

Use `curl -s` and `jq` for all operations. Do not write python wrappers.

### 1. Basic Search and Retrieval

Append `?q=<term>` to search titles and creator fields. Use `items/top` to exclude raw attachment/note items.

```bash
# Get 10 recent top-level items
curl -s "https://zotero.dzackgarza.com/api/users/1049732/items/top?limit=10&sort=dateAdded&direction=desc" | jq '.'

# Search for "cognitive"
curl -s "https://zotero.dzackgarza.com/api/users/1049732/items?q=cognitive&limit=5" | jq '.'
```

### 2. Extracting Core Metadata

Extract exact fields without reading the full JSON payload.

```bash
# Extract title, authors, and year
curl -s "https://zotero.dzackgarza.com/api/users/1049732/items/top?limit=5" | \
  jq -r '.[] | [
    .key,
    .data.title,
    (.data.creators[0].lastName // "No Author"),
    (.data.date | substring(0;4))
  ] | @tsv'
```

### 3. Finding PDF Attachments

PDFs are "child items" in the Zotero data model.

```bash
# Find all PDF attachments across the library
curl -s "https://zotero.dzackgarza.com/api/users/1049732/items?itemType=attachment&q=pdf" | jq -r '.[].key'

# Get children (e.g. PDFs) for a specific item key
curl -s "https://zotero.dzackgarza.com/api/users/1049732/items/<ITEM_KEY>/children" | \
  jq -r '.[] | select(.data.itemType == "attachment") | .data.url'
```

### 4. Citation Export

Get pre-formatted citations or raw export formats by appending `format` or `include`.

```bash
# Export item as BibTeX
curl -s "https://zotero.dzackgarza.com/api/users/1049732/items/<ITEM_KEY>?format=bibtex"

# Get a pre-formatted APA citation string
curl -s "https://zotero.dzackgarza.com/api/users/1049732/items/<ITEM_KEY>?include=citation&style=apa" | jq -r '.citation'
```

## API Parameters

| Parameter   | Values                                                  | Description         |
| ----------- | ------------------------------------------------------- | ------------------- |
| `limit`     | `1`-`100` (default: 25)                                 | Results per request |
| `start`     | Integer                                                 | Pagination offset   |
| `sort`      | `dateAdded`, `dateModified`, `title`, `creator`, `date` | Sorting field       |
| `direction` | `asc`, `desc`                                           | Sorting direction   |
| `format`    | `json`, `bibtex`, `biblatex`, `csljson`, `ris`          | Output format       |
