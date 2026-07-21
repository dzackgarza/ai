---
name: reading-pdfs
description: Use when a user needs to read, search, summarize, or extract information from a PDF. The first step is always to check whether the PDF belongs to a live Zotero library item; the answer routes the rest of the workflow.
---
# Reading PDFs

Start here for any PDF request. **Step 1 is always: is this PDF in Zotero?** Do not
skip it and do not assume the answer — run the check.

## Step 1 — Check Zotero first

The live Zotero library on this workstation is reached through the running Zotero
desktop's local API (`http://127.0.0.1:23119`). Every read and every write to the
library goes through the [[zotero/SKILL|zotero]] skill's `lib/zotero.py` client. Do
not call cloud APIs, the translation server, or any external proxy.

Probe health, then resolve the PDF against the library:

```python
from lib.zotero import health, iter_top, get_children

health()  # raises if the desktop/addon is down — that is the blocker to report
# Walk top-level items and their children to find a PDF child whose
# data.contentType == "application/pdf" and whose attachment path resolves to
# this PDF (or whose bytes match, if you have the file in hand).
```

For a paper you already have in hand (file path, title, DOI, or arXiv id), match it
against library items by identifier or title, then confirm the PDF child. The
[[zotero/SKILL|zotero]] skill owns the full surface; load it for the read + any
follow-up writes.

If the PDF is **already attached to a Zotero library item**, go to Step 2A.
If the PDF is **not** in the library, go to Step 2B.

## Step 2A — In Zotero: use the extraction loop

Do not run ad-hoc OCR against library items. The [[zotero/SKILL|zotero]] skill's
extraction loop owns provider order (MinerU primary, Mistral fallback, reversed for
>200pp), page-count routing, artifact staging (`/tmp/<KEY>_content_list.json`,
`/tmp/<KEY>_middle.json`, `/tmp/<KEY>_extracted.md`), attach order (JSON first,
markdown sentinel last), retries, and the blocker ledger.

```bash
just extraction-loop --search "Publication status unknown" --max-items 5
just extraction-candidates --checklist --limit 25
just attach-extraction ABCD1234 /tmp/ABCD1234_extracted.md
```

Completion = a live Zotero `*_extracted.md` child attachment for the item, not a
checked box or a successful provider call. If the item already has a `*_extracted.md`
child, read that — do not re-extract.

If the library item has no PDF yet, that is an **acquisition** problem owned by the
`zotero-library` repo's `PDF_ACQUISITION.md` (`just find-pdf`, `just check-lead`,
`work/<KEY>/pdf.md` ledger), not by this skill. Load the [[zotero/SKILL|zotero]] skill
and follow that ladder.

## Step 2B — Not in Zotero: ad-hoc extraction

For a loose / non-library PDF (e.g. under `~/pdfs/`), select one leaf procedure:

- [[reading-pdfs/ocr/SKILL|OCR reading]] — turn a loose PDF into cached Markdown with
  MinerU (primary) or Mistral OCR (fallback).
- [[reading-pdfs/extraction/SKILL|structured extraction]] — extract text, tables,
  figures, captions, or a higher-fidelity artifact for a paper or report.

Do not load both leaves unless the request requires both outputs. Read the selected
leaf before conversion or extraction.

## Why the check is mandatory

Skipping the check produces two real failure modes:

1. Re-extracting a library item ad-hoc, bypassing the loop's attach order and
   completion criterion — the item's extraction state in Zotero then disagrees with
   what the agent did, and the loop re-enters it forever.
2. Downloading or OCRing a duplicate of a PDF Zotero already has, wasting provider
   quota and storage.

The check is cheap (one local API walk) and the only authoritative routing signal.