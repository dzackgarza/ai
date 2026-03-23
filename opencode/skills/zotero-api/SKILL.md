---
name: zotero-api
description: Use when you need to interact directly with the Zotero Web API v3, particularly the local instance at zotero.dzackgarza.com.
---

# Zotero API Guidelines

This skill covers direct interaction with the Zotero Web API v3.

## Local Instance Access

On authenticated machines (including this one), you have access to a LOCAL Zotero API instance at:
`https://zotero.dzackgarza.com`

This fronts a local cache, NOT the public web API, which means it is extremely fast and does not require API keys for read access.
The primary user ID is `1049732`.

Base URL for all queries: `https://zotero.dzackgarza.com/api/users/1049732`

## Common Operations

Always use standard tools like `curl` or `httpx` to query these endpoints. The API returns JSON by default.

### Getting Items

To retrieve top-level items (excluding attachments and notes):

```bash
curl -s "https://zotero.dzackgarza.com/api/users/1049732/items/top"
```

To retrieve all items (including child attachments like PDFs):

```bash
curl -s "https://zotero.dzackgarza.com/api/users/1049732/items"
```

To get a specific item by its key:

```bash
curl -s "https://zotero.dzackgarza.com/api/users/1049732/items/<itemKey>"
```

### Searching

You can search items by appending the `q` parameter (which searches titles and individual creator fields by default).
Only search metadata is currently available, not full text.

```bash
# Search for items containing "cognitive"
curl -s "https://zotero.dzackgarza.com/api/users/1049732/items?q=cognitive"
```

### Finding Items with Attached PDFs

In the Zotero API, PDFs are "child items" (attachments) that belong to a parent item. To find items with PDFs, you can filter by `itemType`:

```bash
# Find PDF attachments
curl -s "https://zotero.dzackgarza.com/api/users/1049732/items?itemType=attachment&q=pdf"
```

Alternatively, to find the children (e.g. PDFs) of a specific item key:

```bash
curl -s "https://zotero.dzackgarza.com/api/users/1049732/items/<itemKey>/children"
```

### Extracting Metadata (Titles, Authors, Years)

Zotero API returns item data under the `data` key in the JSON response.
You can use `jq` to parse out specific fields:

```bash
# Extract title, first creator, and date
curl -s "https://zotero.dzackgarza.com/api/users/1049732/items/top?limit=5" | jq -r '.[] | .data.title + " | " + .data.creators[0].lastName + " | " + .data.date'
```

### Export Formats (BibTeX, JSON, etc)

Zotero can format citations directly if you specify export formats (like BibTeX) via `format`.
Available export formats: `bibtex`, `biblatex`, `csljson`, `ris`, etc.

```bash
# Get BibTeX for a specific item
curl -s "https://zotero.dzackgarza.com/api/users/1049732/items/<itemKey>?format=bibtex"
```

If you just want a formatted citation string according to a specific style:

```bash
curl -s "https://zotero.dzackgarza.com/api/users/1049732/items/<itemKey>?include=citation&style=apa"
```

## Pagination & Limits

- By default, the API returns 25 results.
- Use `limit` (max 100) and `start` for pagination.
- Sort with `sort` (e.g. `dateAdded`, `dateModified`, `title`, `creator`, `date`) and `direction` (`asc`, `desc`).

```bash
# Get the 100 most recently added items
curl -s "https://zotero.dzackgarza.com/api/users/1049732/items?limit=100&sort=dateAdded&direction=desc"
```

## API Versioning

The current API version is v3. You can request it explicitly by appending `v=3` to your query string, though the local instance handles default routing.
