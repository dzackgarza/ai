---
name: zotero
description: Search, read, add, and manage items in the local Zotero library.
---

# [[zotero/SKILL|Zotero]] Skill

Interact with the **live Zotero library on this workstation** through the running Zotero
desktop's own local API. There is no exported mirror, shard store, or proof ledger —
live Zotero is the only source of truth.

## Transport (the only sanctioned surface)

- **Read base:** `http://127.0.0.1:23119/api/users/0/...`
- **Write:** `POST http://127.0.0.1:23119/write` (local write-API addon)
- **File attach:** `POST http://127.0.0.1:23119/attach`
- **Health probe:** `GET http://127.0.0.1:23119/version`

Precondition: the Zotero desktop app is running with the local write-API addon loaded.
Verify with `zotero.health()` — the returned `capabilities` list names every write op
the addon currently exposes. If the desktop is down or the addon is not loaded, that is
the blocker to report — not a missing env var, not a missing server, not a missing key.

## NOT used (do not confuse with the above)

- **Cloud Web API** (`api.zotero.org`, `ZOTERO_API_KEY`, `ZOTERO_USER_ID`) — not used
  here. A dead or unset cloud key is never a blocker on this workstation.
- **Standalone translation server** (`:1969`) — not used here. A dead `:1969` is never a
  blocker.
- Any external read-only proxy to the cloud library is stale; route everything through
  the running desktop's local API instead.

If a guide, script, or memory record tells you to set `ZOTERO_API_KEY` /
`ZOTERO_USER_ID` or to call `api.zotero.org` for this library, that source is out of date.

## The I/O boundary: `lib/zotero.py`

The canonical client on this workstation lives in the `zotero-library` repo at
`lib/zotero.py`. Every read and every write in that repo goes through this module —
so the same client the loop writes through is the client tests read through, and no
second source of truth can drift from live state.

Payload shapes are the ones the live API actually accepts, not guessed:
`import_by_identifier`, `update_item_fields`, `trash_item`, `merge_items`,
`add_item_tags` / `remove_item_tags`, `attach_file`, `run_javascript`.

A non-2xx HTTP status or a `success != true` body is a **hard error**. There is no retry,
no fallback, no silent success.

### Public surface (read)

| Function | Returns | Notes |
| --- | --- | --- |
| `health()` | `{version, healthy, capabilities}` | Probe the write-API addon; raises if down. **Call first.** |
| `get_item(key)` | full item envelope `{key, data, meta, links, ...}` | |
| `get_data(key)` | just the `data` object | shape canonical/stamp/identity consume |
| `get_children(key)` | ALL child items, paginated | a heavily annotated item can exceed one page; truncation silently misreports "no extraction child" |
| `iter_top(page=100)` | all top-level items, paginated | |
| `biblio(items)` | items excluding attachment/note/annotation | |
| `biblio_top()` | top-level bibliographic items only | |
| `collections()` | all collections, paginated | |
| `collection_top(key, page=100)` | top-level items in a collection, paginated | |
| `saved_search_keys(name)` | item keys matching a live saved search | executes Zotero's OWN search engine via `run_javascript`; read-only, never edits the search |
| `duplicate_sets()` | Zotero's OWN duplicate sets | leverages `Zotero.Duplicates` rather than reimplementing matching |

### Public surface (write — every one is a `POST /write`)

| Function | Payload | Notes |
| --- | --- | --- |
| `import_by_identifier(identifier)` | `{identifier}` | the only provenance-bearing ingestion surface; callers MUST inspect `details.item_count` (a multi-volume identifier can create several items) and `item_key` before trusting the result |
| `update_item_fields(key, fields)` | `{item_key, fields:{...}}` | |
| `set_extra(key, extra)` | via `update_item_fields` | writes the `extra` field |
| `trash_item(key)` | `{item_key}` | recoverable |
| `merge_items(source, target)` | `{source_key, target_key}` | **target survives as master**; children move to target; redirect relation established by the API |
| `add_item_tags(key, tags)` | `{item_key, tags:[...]}` | |
| `remove_item_tags(key, tags)` | `{item_key, tags:[...]}` | |
| `attach_file(key, file_path, title)` | `POST /attach` | file must be under `/tmp` or `/var/tmp` |
| `run_javascript(code)` | `{operation:"run_javascript", code}` | run JS inside Zotero; for when no named op fits |

## Identity rule

When reporting an item to the user, include its **Zotero key + Better BibTeX citation
key + creator/author + title** whenever Zotero has those fields. A bare Zotero key is
only an implementation handle, not a useful item identity.

## Saved searches own publication status

`Published`, `Unpublished`, and `Publication status unknown` are live Zotero saved
searches — the trustable live views. Treat saved searches as **read-only implementation
scaffolding**: do not create, delete, rename, edit criteria for, or otherwise modify
them or the `_status-rule:*` helper searches. Start triage from
`Publication status unknown`; correct an item if the evidence supports a Zotero write,
or append a blocker note to the item's ledger, then move on.

## Audit Attachment Completeness

When answering whether Zotero items have PDFs, markdown extractions, or other
attachments, define the item universe before counting.

- Do not treat a collection query as a library-wide result unless the user explicitly
  scoped the question to that collection.
- For "all Zotero items" or "the library": query all top-level parent items
  (`iter_top()`), then inspect each parent's children (`get_children(key)`) for
  attachment content types.
- Count markdown extraction coverage parent-by-parent: parent has at least one PDF
  child and at least one child attachment with `data.contentType == "text/markdown"`.
- If any item is cited as a counterexample, fetch that exact key and its children
  before making or defending an aggregate claim.
- Report the exact scope used in the conclusion, e.g. "collection X" versus "all
  parent items with PDF children in the library".

The observed failure mode: a single `limit=500` collection response is not evidence of
full coverage. A full-library parent/child walk can find parents with PDF children and
no markdown child that a collection-scoped query missed entirely.

## `pdf:extraction-skip`

Live Zotero tag. Removes an item from extraction candidates. Use for reference corpora
or other PDFs that should remain attached but should not get Mistral/MinerU extraction
artifacts. Candidate reports and the automated loop must ignore PDF-bearing items with
this tag.

## Workflows

### Health check first

```python
from lib.zotero import health
h = health()
# h["version"], h["healthy"], h["capabilities"]
```

If `health()` raises, the desktop or addon is down. Report that blocker — do not
attempt cloud fallback, do not set env vars.

### Add a paper by identifier (DOI / ISBN / PMID / arXiv)

```python
from lib.zotero import import_by_identifier
r = import_by_identifier("10.1093/jamia/ocaa037")
# INSPECT r["details"]["item_count"] and r["item_key"] — a multi-volume
# identifier can create several items.
```

This is the only provenance-bearing ingestion surface. Deduplicate against existing
items first (`duplicate_sets()` or a title/identifier search), then import.

### Update metadata / tags

```python
from lib.zotero import update_item_fields, add_item_tags, remove_item_tags, set_extra
update_item_fields("ABCD1234", {"title": "Corrected Title", "date": "2024"})
add_item_tags("ABCD1234", ["review"])
set_extra("ABCD1234", "Citation Key: milneSG3\n...")
```

### Merge duplicates (target survives)

```python
from lib.zotero import merge_items
merge_items(source_key="AAAA1111", target_key="BBBB2222")  # BBBB2222 survives
```

Used to collapse a malformed original onto a fresh add-by-identifier item so the
survivor carries canonical provenance.

### Attach a file (PDF / markdown extraction)

```python
from lib.zotero import attach_file
attach_file("ABCD1234", "/tmp/paper.md", "Extracted markdown")
# file_path MUST be under /tmp or /var/tmp
```

### Trash

```python
from lib.zotero import trash_item
trash_item("ABCD1234")  # recoverable
```

### Resolve a saved search's live membership

```python
from lib.zotero import saved_search_keys
keys = saved_search_keys("Publication status unknown")
```

Executes Zotero's OWN saved-search engine via `run_javascript`, so it always reflects
the exact live membership the user sees in the UI. Read-only — never edits the search.

## When no named operation fits: `run_javascript`

For ad-hoc work inside Zotero (resolving saved searches, running `Zotero.Duplicates`,
inspecting live state), `run_javascript(code)` runs JS inside Zotero and returns its
result. Prefer a named op when one exists; reach for `run_javascript` only when the
named surface does not cover the need.

## Anti-patterns

| Pattern | Why bad | Do instead |
| --- | --- | --- |
| Set `ZOTERO_API_KEY` / `ZOTERO_USER_ID` for this library | cloud Web API is not used here | call the running desktop's local API |
| Call `api.zotero.org` | cloud is not the transport here | `http://127.0.0.1:23119/api/users/0/...` |
| Fall back to translation server `:1969` | not used here; a dead `:1969` is never a blocker | use `import_by_identifier` on the local addon |
| Treat a collection `limit=500` as library-wide | silent coverage gaps | full parent/child walk with `iter_top()` + `get_children()` |
| Trust a stale report/cache over live state | live Zotero is the only source of truth | reread through `lib/zotero.py` |
| Report items by bare Zotero key | not a useful identity | key + Better BibTeX citekey + creator + title |
| Modify or rename `Published` / `Unpublished` / `Publication status unknown` saved searches | read-only scaffolding | start triage from them, never edit them |
| Retry / fallback / silent success on non-2xx | a hard error in `lib/zotero.py` | surface the error, do not mask it |

## PDF extraction policy (for items in this library)

The live Zotero library is the source of truth for what counts as extracted — not a
checked box, not a script's intended state, not a stale report. The canonical loop
lives in the `zotero-library` repo (`EXTRACTION_LOOP.md`).

### Provider order

- **MinerU precise API is primary.** Its precise API returns the more valuable artifact
  set: `full.md`, `content_list.json`, and middle JSON (`middle.json` or MinerU's
  `layout.json` middle-result spelling).
- **Mistral OCR is fallback.** The Mistral path uploads the PDF through the files API
  and OCRs the signed URL, so large PDFs do not go through a base64 request body.
- **Order reverses for PDFs over 200 pages.** MinerU's precise API rejects those
  one-shot, so Mistral runs first and MinerU is chunked into ≤200-page pieces as the
  fallback.
- A provider failure on one item does **not** crash the run: the loop retries with
  bounded backoff (rate limits: 15/20/25s; network: 2/5/10s; empty extraction: 5/15s),
  then falls through to the next provider in order, then records the failure and skips
  to the next candidate.

### Sanctioned surface

```bash
just extraction-loop --search "Publication status unknown" --max-items 5
just extraction-candidates --checklist --limit 25
just attach-extraction ABCD1234 /tmp/ABCD1234_extracted.md
```

Do not run private extraction scripts against library items. Use the loop. The loop
owns provider order, page-count routing, artifact staging, attach order, retries, and
the blocker ledger.

### Artifact staging + attach order

1. MinerU stages `/tmp/<KEY>_content_list.json` and `/tmp/<KEY>_middle.json` first,
   then `/tmp/<KEY>_extracted.md`. Mistral fallback stages only
   `/tmp/<KEY>_extracted.md`.
2. Attach JSON artifacts first and the Markdown sentinel **last**. This keeps a partial
   MinerU attach retryable: an item does not leave the live candidate view until its
   Markdown child is attached.

### Completion criterion

An item is extracted when **live Zotero shows a `*_extracted.md` child attachment** for
it. A checked checklist box, a successful provider call, or a staged `/tmp` file is not
completion. Reread live Zotero to confirm.

### Opt-out tag: `pdf:extraction-skip`

Live Zotero tag. Removes an item from extraction candidates. Use for reference corpora
or other PDFs that should remain attached but should not get MinerU/Mistral extraction
artifacts. The loop and `extraction-candidates` must ignore PDF-bearing items with this
tag.

### Candidate selection

The loop selects the first top-level item with a PDF child, no `*_extracted.md` child,
and no `pdf:extraction-skip` tag. If an item has multiple PDF children, it uses the
bibliographic-looking PDF and rejects an ambiguous choice before calling a provider.

### Failure handling

If both providers are exhausted for an item, append a blocker entry to
`work/<KEY>/notes.md` (provider, PDF path, failure, next attempt) and skip to the next
candidate for the rest of this run — do not retry that item again or halt the loop.
Re-run the loop after fixing the blocker to pick the item back up.

### Credentials

`MISTRAL_API_KEY` and `MINERU_API_TOKEN` live in the machine environment managed
outside this repo. Do not put API keys in commands, docs, or committed files.

### Manual one-off

For a manual loop: `just extraction-candidates --checklist`, extract one PDF, stage
the Markdown under `/tmp` or `/var/tmp`, then
`just attach-extraction <KEY> /tmp/<KEY>_extracted.md`. Do not bypass the loop for
library items; it owns the trust model.

## Scope boundary

This skill covers **reading and mutating the live Zotero library on this workstation**
through the running desktop's local API, including the PDF extraction loop for library
items. It does not own: ad-hoc extraction of non-library PDFs (see
[[reading-pdfs/SKILL|reading-pdfs]]), or the citation-cleanup loop and its
policy rules (those live in the `zotero-library` repo's `AGENTS.md` and `policy/`).

The repo also owns a PDF **acquisition** ladder (trust-tiered cascade from arXiv →
OA → Numdam → libgen → Sci-Hub → fuzzy → human, with a `just check-lead` agreement gate
before any download and an append-only `work/<KEY>/pdf.md` ledger with a closed
outcome vocabulary). That lives in the `zotero-library` repo's `PDF_ACQUISITION.md`,
not in this skill.