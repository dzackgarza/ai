---
name: zotero-pdf-extraction-attachments
description: Use when auditing, extracting, attaching, or verifying PDF-to-markdown/MinerU artifacts for Zotero items, especially when checking whether PDFs have markdown children or attaching existing extraction output back to Zotero.
---

# Zotero PDF Extraction Attachments

Use this skill for Zotero items whose PDF attachments need markdown extraction
artifacts, or whose existing extraction artifacts need to be attached back to Zotero.

## Core Policy

- Define the item universe before counting or claiming coverage.
- Treat Zotero parent items, PDF attachments, and markdown extraction attachments as
  distinct records. Never count attachment totals as parent-item completion.
- Do not treat a collection query as library-wide evidence unless the user explicitly
  named that collection.
- Use the running Zotero local API/client for attachment evidence and writes. The
  read-only cache/proxy can help inspect metadata, but it cannot prove writes or attach
  files.
- Do not infer a Zotero parent from normalized titles, years, or filenames alone. Use
  exact item keys, child attachment keys, or a verified Better BibTeX key.
- Do not download or re-extract a PDF until you have checked whether Zotero already has
  a local PDF child and whether a markdown child already exists.

## Coverage Audit

For library-wide markdown extraction coverage:

- Fetch all items with pagination from the local Zotero API, not just one collection.
- Keep only parent items: `data.itemType != "attachment"`.
- For each parent key, fetch children with pagination from `/items/{KEY}/children`.
- Count a parent as needing extraction only when it has at least one PDF child
  (`data.contentType == "application/pdf"`) and no markdown extraction child
  (`data.contentType == "text/markdown"`).
- Report the exact scope: all PDF-bearing parents in the library, a named collection,
  or a named item search.

Observed failure to avoid: querying only `JEJSXB2N` showed complete markdown coverage
for that collection, while a full-library parent/child walk found PDF-bearing parents
outside the collection with no markdown child.

## Counterexample Handling

If the user names an item they can see in Zotero:

- Search the exact title or key.
- Inspect every matching parent item.
- Fetch each matching parent's children.
- Check collection membership before using that item to confirm or refute a
  collection-scoped claim.
- If the named item has a PDF child and no markdown child, the global claim is false
  unless the previous claim was explicitly scoped away from that item.

## Extraction Workflow

When a Zotero parent has a PDF child but no markdown child:

- Resolve the PDF attachment's local file path from the child attachment record.
- Use the managed PDF extraction workflow for the repository or system; do not create
  ad hoc extraction scripts when a maintained recipe exists.
- Preserve extraction artifacts outside source repos unless the repo explicitly owns
  those artifacts.
- Keep the original PDF and extracted markdown/JSON relationship auditable: parent key,
  PDF attachment key, source file path, extraction command/recipe, output path, and
  verification evidence.

## Attachment Workflow

Before attaching extracted markdown or MinerU JSON back to Zotero:

- Verify Zotero is running and the local attachment/write API is reachable.
- Verify the parent item key resolves to the intended Zotero item.
- Verify the extraction file exists and is non-empty.
- Stage files only through the supported local-client attachment path; do not write
  directly into Zotero storage or mutate Zotero SQLite.
- After every attach or relink, re-query the parent item's children and verify the new
  child attachment content type, title, and attachment key.

## Completion Evidence

Do not claim an item is extracted or attached from filenames, queue entries, command
success, or aggregate attachment counts. A Zotero PDF item is markdown-extracted only
when its parent item has:

- at least one PDF child attachment;
- at least one `text/markdown` child attachment;
- child records verified through the local Zotero API after any write.

For full MinerU completion, require the project-specific JSON sidecar standard in
addition to markdown; do not silently upgrade "has markdown" into "fully extracted".
