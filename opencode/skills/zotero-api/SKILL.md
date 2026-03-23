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
- **Missing Features:** The local proxy does NOT support translation endpoints (`format=bibtex` or `include=citation`). It returns empty data for these.
- **Pagination limit:** `curl` queries are strictly limited to 100 results per request. You must loop using `&start=N` to fetch all data. Do NOT use the `zotero` python skill for local cache reads, as that script is hardcoded to the official authenticated web API.

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

PDFs are stored as child items (`itemType=attachment`). There is NO server-side filter for `contentType`.

```bash
# Get children (e.g. PDFs) for a specific item key
curl -s "https://zotero.dzackgarza.com/api/users/1049732/items/<ITEM_KEY>/children" | \
  jq -r '.[] | select(.data.contentType == "application/pdf") | .data.url'

# Find ALL PDF attachments across the library (paginated loop)
total=$(curl -sI "https://zotero.dzackgarza.com/api/users/1049732/items?itemType=attachment" | grep -i 'total-results' | awk '{print $2}' | tr -d '\r')
for ((i=0; i<total; i+=100)); do
  curl -s "https://zotero.dzackgarza.com/api/users/1049732/items?itemType=attachment&limit=100&start=$i" | \
    jq -r '.[] | select(.data.contentType == "application/pdf") | .key'
done
```
