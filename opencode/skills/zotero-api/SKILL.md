---
name: zotero-api
description: Use when you need to query Zotero data, find references, export citations, search for papers, or fetch PDFs using the local Zotero Web API cache.
---
# Zotero API (Local Cache)

## Environment Traps

- **Local Proxy:** This machine runs a local cache of the Zotero v3 API at
  `https://zotero.dzackgarza.com`.

- **Target User:** The primary library is `users/1049732`.

- **Auth:** No API keys are required.
  The proxy is read-only.

- **Base URL:** `https://zotero.dzackgarza.com/api/users/1049732`

- **Missing Features:** The local proxy does NOT support translation endpoints
  (`format=bibtex` or `include=citation`). It returns empty data for these.

- **Pagination limit:** `curl` queries are strictly limited to 100 results per request.
  You must loop using `&start=N` to fetch all data.
  Do NOT use the [[zotero/SKILL|zotero]] python skill for local cache reads, as that script is
  hardcoded to the official authenticated web API.

- **Read-Only:** You cannot attach new files or modify metadata via this local API.

## Core Workflows

Do not attempt to write Python wrappers.
Use these exact `curl` and `jq` pipelines.

### Local Better BibTeX and Fulltext Attachments

For workflows that need to attach existing extraction output back to Zotero, use
Zotero’s local client APIs, not the read-only cache:

- Better BibTeX JSON-RPC and local Zotero endpoints run at `http://localhost:23119` when
  Zotero is open and local API permissions are enabled.

- The relevant write path is the local `fulltext-attach` endpoint.

- This is separate from `https://zotero.dzackgarza.com`, which is read-only and cannot
  attach files.

Before using the local write path, verify Zotero is running, Better BibTeX is enabled,
and the item key or Better BibTeX citation key resolves to the intended attachment.
Do not upload extraction artifacts based only on normalized titles or years.

### Local Better BibTeX and Fulltext Attachments

For workflows that need to attach existing extraction output back to Zotero, use
Zotero's local client APIs, not the read-only cache:

- Better BibTeX JSON-RPC and local Zotero endpoints run at
  `http://localhost:23119` when Zotero is open and local API permissions are
  enabled.
- The relevant write path is the local `fulltext-attach` endpoint.
- This is separate from `https://zotero.dzackgarza.com`, which is read-only and
  cannot attach files.

Before using the local write path, verify Zotero is running, Better BibTeX is
enabled, and the item key or Better BibTeX citation key resolves to the intended
attachment. Do not upload extraction artifacts based only on normalized titles
or years.

### 0. Basic Item Retrieval

```bash
# Get top-level items (excludes raw attachments/notes)
curl -s "https://zotero.dzackgarza.com/api/users/1049732/items/top?limit=25"

# Get a specific item by its key
curl -s "https://zotero.dzackgarza.com/api/users/1049732/items/<ITEM_KEY>"

# Get all items (including child attachments)
curl -s "https://zotero.dzackgarza.com/api/users/1049732/items?limit=25"

# Get children of a specific item (attachments, notes)
curl -s "https://zotero.dzackgarza.com/api/users/1049732/items/<ITEM_KEY>/children"
```

### 1. Reading Papers and Finding File Locations

The Zotero database stores files locally.
You can find the exact path to a PDF or Markdown file by inspecting its `enclosure`
link.

```bash
# Find the local filepath of an attachment (e.g. a PDF)
curl -s "https://zotero.dzackgarza.com/api/users/1049732/items/<ATTACHMENT_KEY>" | \
  jq -r '.links.enclosure.href' | sed 's|file://||'
```

*Result:* `/home/dzack/Zotero/storage/<ATTACHMENT_KEY>/<filename>.pdf`

Once you have the path, use the **`marker`** skill or native file reading tools to read
the paper’s contents.

### 2. Searching and Filtering (Fulltext vs Metadata)

Zotero supports powerful search via the `q` parameter.

- **Metadata only (Default):** `q=<term>` searches only titles, creators, and years.

- **Fulltext Search:** Append `&qmode=everything` to search the full text of indexed
  PDFs and all metadata fields (like abstracts).

```bash
# Fulltext search across all items and PDFs
curl -s "https://zotero.dzackgarza.com/api/users/1049732/items?q=quantum&qmode=everything&limit=5" | jq -r '.[].data.title'
```

### 3. Finding Items Without Attachments (Needs PDF)

Items missing PDFs have no child items.
You can find them by checking `.meta.numChildren`.

```bash
# Find top-level items that have NO attachments
curl -s "https://zotero.dzackgarza.com/api/users/1049732/items/top?limit=100" | \
  jq -r '.[] | select(.meta.numChildren == 0) | .key'
```

### 4. Extracting Core Metadata & BibTeX Keys

When inspecting library contents, extract just the necessary fields.
BetterBibTeX keys are usually stored in the `extra` field.

```bash
# Extract Key, Title, First Author, Year, and BibTeX Key
curl -s "https://zotero.dzackgarza.com/api/users/1049732/items/top?limit=5" | \
  jq -r '.[] | [
    .key,
    .data.title,
    (.data.creators[0].lastName // "No Author"),
    (.data.date | substring(0;4)),
    (.data.extra | capture("Citation Key: (?<key>[^\\n]+)") | .key // "No Key")
  ] | @tsv'
```

### 5. Finding Specific File Types (Markdown, PDFs)

PDFs and Markdown notes are stored as child items (`itemType=attachment`). There is NO
server-side filter for `contentType`, so you must filter with `jq`.

```bash
# Find recent Markdown file attachments
curl -s "https://zotero.dzackgarza.com/api/users/1049732/items?itemType=attachment&limit=100" | \
  jq -r '.[] | select(.data.contentType == "text/markdown") | .key'

# Get ALL child attachments (PDFs/Markdown) for a specific parent item
curl -s "https://zotero.dzackgarza.com/api/users/1049732/items/<PARENT_KEY>/children" | \
  jq -r '.[] | [.data.contentType, .links.enclosure.href] | @tsv'
```

### 6. Finding Collections

To list all collections and their IDs:

```bash
curl -s "https://zotero.dzackgarza.com/api/users/1049732/collections?limit=50" | \
  jq -r '.[] | [.key, .data.name, .meta.numItems] | @tsv'
```

### 7. Fetching All PDFs (Pagination Loop)

Because of the 100-item limit, you must loop over `start=N` to fetch all attachments.

```bash
# Find ALL PDF attachments across the library (paginated loop)
total=$(curl -sI "https://zotero.dzackgarza.com/api/users/1049732/items?itemType=attachment" | grep -i 'total-results' | awk '{print $2}' | tr -d '\r')
for ((i=0; i<total; i+=100)); do
  curl -s "https://zotero.dzackgarza.com/api/users/1049732/items?itemType=attachment&limit=100&start=$i" | \
    jq -r '.[] | select(.data.contentType == "application/pdf") | .key'
done
```
