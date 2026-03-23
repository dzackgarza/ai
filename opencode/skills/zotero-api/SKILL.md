---
name: zotero-api
description: Use when you need to query Zotero data, find references, export citations, search for papers, or fetch PDFs using the local Zotero Web API cache.
---

# Zotero API (Local Cache)

## Environment Traps

- **Local Proxy:** This machine runs a local cache of the Zotero v3 API at `https://zotero.dzackgarza.com`.
- **Target User:** The primary library is `users/1049732`.
- **Auth:** No API keys are required. The proxy is read-only.
- **Base URL:** `https://zotero.dzackgarza.com/api/users/1049732`

## Workflow Recipes

Do not attempt to write Python wrappers or learn the schema via exploration. Use these exact `curl` and `jq` pipelines to prevent context flooding.

### Extracting Core Metadata (Titles, Authors, Years)

When inspecting library contents, extract just the necessary fields.

```bash
curl -s "https://zotero.dzackgarza.com/api/users/1049732/items/top?limit=10" | \
  jq -r '.[] | [
    .key,
    .data.title,
    (.data.creators[0].lastName // "No Author"),
    (.data.date | substring(0;4))
  ] | @tsv'
```

### Searching and Filtering

To search the library (defaults to `titleCreatorYear`):

```bash
curl -s "https://zotero.dzackgarza.com/api/users/1049732/items?q=<SEARCH_TERM>&limit=5" | \
  jq -r '.[] | "\(.key) \(.data.title)"'
```

### Finding PDF Attachments

PDFs are stored as child items (`itemType=attachment`). To find a PDF for a specific item:

```bash
curl -s "https://zotero.dzackgarza.com/api/users/1049732/items/<ITEM_KEY>/children" | \
  jq -r '.[] | select(.data.contentType == "application/pdf") | .data.url'
```

### Formatting Citations & Exports

Do not manually parse fields to create citations. Use the API's native formatters (`format` or `include`).

```bash
# Export as BibTeX
curl -s "https://zotero.dzackgarza.com/api/users/1049732/items/<ITEM_KEY>?format=bibtex"

# Get a pre-formatted string (e.g. APA)
curl -s "https://zotero.dzackgarza.com/api/users/1049732/items/<ITEM_KEY>?include=citation&style=apa" | jq -r '.citation'
```
