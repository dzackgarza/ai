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
- **Pagination limit:** `httpie` queries are strictly limited to 100 results per request. You must loop using `&start=N` to fetch all data. Do NOT use the `zotero` python skill for local cache reads, as that script is hardcoded to the official authenticated web API.
- **Read-Only:** You cannot attach new files or modify metadata via this local API.

## Core Workflows

Do not attempt to write Python wrappers. Use these exact `httpie` and `jq` pipelines.

### 0. Basic Item Retrieval

```bash
# Get top-level items (excludes raw attachments/notes)
uvx --from httpie http GET "https://zotero.dzackgarza.com/api/users/1049732/items/top?limit=25"

# Get a specific item by its key
uvx --from httpie http GET "https://zotero.dzackgarza.com/api/users/1049732/items/<ITEM_KEY>"

# Get all items (including child attachments)
uvx --from httpie http GET "https://zotero.dzackgarza.com/api/users/1049732/items?limit=25"

# Get children of a specific item (attachments, notes)
uvx --from httpie http GET "https://zotero.dzackgarza.com/api/users/1049732/items/<ITEM_KEY>/children"
```

### 1. Reading Papers and Finding File Locations

The Zotero database stores files locally. You can find the exact path to a PDF or Markdown file by inspecting its `enclosure` link.

```bash
# Find the local filepath of an attachment (e.g. a PDF)
uvx --from httpie http GET "https://zotero.dzackgarza.com/api/users/1049732/items/<ATTACHMENT_KEY>" | \
  jq -r '.links.enclosure.href' | sed 's|file://||'
```

_Result:_ `/home/dzack/Zotero/storage/<ATTACHMENT_KEY>/<filename>.pdf`

Once you have the path, use the **`marker`** skill or native file reading tools to read the paper's contents.

### 2. Searching and Filtering (Fulltext vs Metadata)

Zotero supports powerful search via the `q` parameter.

- **Metadata only (Default):** `q=<term>` searches only titles, creators, and years.
- **Fulltext Search:** Append `&qmode=everything` to search the full text of indexed PDFs and all metadata fields (like abstracts).

```bash
# Fulltext search across all items and PDFs
uvx --from httpie http GET "https://zotero.dzackgarza.com/api/users/1049732/items?q=quantum&qmode=everything&limit=5" | jq -r '.[].data.title'
```

### 3. Finding Items Without Attachments (Needs PDF)

Items missing PDFs have no child items. You can find them by checking `.meta.numChildren`.

```bash
# Find top-level items that have NO attachments
uvx --from httpie http GET "https://zotero.dzackgarza.com/api/users/1049732/items/top?limit=100" | \
  jq -r '.[] | select(.meta.numChildren == 0) | .key'
```

### 4. Extracting Core Metadata & BibTeX Keys

When inspecting library contents, extract just the necessary fields. BetterBibTeX keys are usually stored in the `extra` field.

```bash
# Extract Key, Title, First Author, Year, and BibTeX Key
uvx --from httpie http GET "https://zotero.dzackgarza.com/api/users/1049732/items/top?limit=5" | \
  jq -r '.[] | [
    .key,
    .data.title,
    (.data.creators[0].lastName // "No Author"),
    (.data.date | substring(0;4)),
    (.data.extra | capture("Citation Key: (?<key>[^\\n]+)") | .key // "No Key")
  ] | @tsv'
```

### 5. Finding Specific File Types (Markdown, PDFs)

PDFs and Markdown notes are stored as child items (`itemType=attachment`). There is NO server-side filter for `contentType`, so you must filter with `jq`.

```bash
# Find recent Markdown file attachments
uvx --from httpie http GET "https://zotero.dzackgarza.com/api/users/1049732/items?itemType=attachment&limit=100" | \
  jq -r '.[] | select(.data.contentType == "text/markdown") | .key'

# Get ALL child attachments (PDFs/Markdown) for a specific parent item
uvx --from httpie http GET "https://zotero.dzackgarza.com/api/users/1049732/items/<PARENT_KEY>/children" | \
  jq -r '.[] | [.data.contentType, .links.enclosure.href] | @tsv'
```

### 6. Finding Collections

To list all collections and their IDs:

```bash
uvx --from httpie http GET "https://zotero.dzackgarza.com/api/users/1049732/collections?limit=50" | \
  jq -r '.[] | [.key, .data.name, .meta.numItems] | @tsv'
```

### 7. Fetching All PDFs (Pagination Loop)

Because of the 100-item limit, you must loop over `start=N` to fetch all attachments.

```bash
# Find ALL PDF attachments across the library (paginated loop)
total=$(uvx --from httpie http --headers GET "https://zotero.dzackgarza.com/api/users/1049732/items?itemType=attachment" | awk -F': ' 'tolower($1) == "total-results" {print $2}' | tr -d '\r')
for ((i=0; i<total; i+=100)); do
  uvx --from httpie http GET "https://zotero.dzackgarza.com/api/users/1049732/items?itemType=attachment&limit=100&start=$i" | \
    jq -r '.[] | select(.data.contentType == "application/pdf") | .key'
done
```
