---
name: pdf-ocr-reading
description: Use when reading a loose / non-library PDF — converts to markdown via
  MinerU (primary) or Mistral OCR (fallback) with local caching. The parent
  reading-pdfs skill checks Zotero first; this leaf runs only after the PDF is
  confirmed not in the library. For any Zotero library item, use the zotero skill's
  extraction loop instead.
metadata:
  author: dzack
  version: 0.2.1
---
# Reading PDFs with OCR

## Precondition: Zotero check already done

The [[reading-pdfs/SKILL|reading-pdfs]] parent runs the Zotero check as step 1. This
leaf is reached only when the PDF is confirmed **not** in the library. If you arrived
here without doing that check, go back to the parent and do it first — running ad-hoc
OCR against a library item bypasses the loop's attach order and completion criterion,
and the loop then re-enters the item forever.

## Provider order

1. **MinerU precise API** — primary. Returns `full.md`, `content_list.json`, and middle
   JSON (`middle.json` or `layout.json` middle-result spelling). Preferred for math,
   tables, and multi-column layouts.
2. **Mistral OCR** — fallback. Uploads the PDF through the files API and OCRs the signed
   URL, so large PDFs do not go through a base64 request body. Use when MinerU is
   unavailable, rejects the PDF (e.g. >200 pages in one shot), or returns unusable
   artifacts.

Provider credentials (`MINERU_API_TOKEN`, `MISTRAL_API_KEY`) live in the machine
environment. Do not put API keys in commands, docs, or committed files.

## Local extraction recipes (`~/pdf-extraction`)

For non-library PDFs, prefer the managed recipes in `~/pdf-extraction` over hand-rolled
scripts. They handle environment setup automatically via `uv sync`.

```bash
# From any directory
just -f ~/pdf-extraction/justfile -d ~/pdf-extraction <recipe>
```

| Recipe | Purpose |
| --- | --- |
| `sample-pdf` | Regenerate the smoke-test PDF |
| `docling` | Extract with Docling |
| `mineru` | Extract with MinerU |
| `smoke` | Run both extraction checks |

Outputs appear under `~/pdf-extraction/artifacts/` and `~/pdf-extraction/outputs/`.

**Do not** create a separate venv or install ad hoc — let the recipes manage the
environment.

When only structured extraction data is needed, prefer a recipe that emits the minimal
MinerU JSON artifacts (`middle.json` and `content_list.json`) without generating extra
rendered PDFs or Markdown. The recipe should own that mode; do not run private one-off
extraction scripts. After extraction, verify the expected output files and keep the run
log with the artifacts.

## PDF storage layout (non-library)

```
~/pdfs/
├── arxiv/
│   └── {arxiv_key}/
│       ├── paper.pdf        # Original PDF
│       └── paper.md         # Extracted markdown
├── other/
    └── {filename}/
        ├── content.pdf
        └── content.md
```

Always save the original PDF alongside the extracted markdown. For
[[research-discovery/search/search|arXiv]] papers, name them `paper.pdf` and `paper.md`,
download from `https://arxiv.org/pdf/{arxiv_id}.pdf`, and store as
`~/pdfs/arxiv/{arxiv_id}/paper.md`.

## Mistral OCR fallback (PEP 723 script)

Use only when MinerU is unavailable or rejects the PDF. Save as a standalone script and
run with `uv run`:

```python
# /// script
# requires-python = ">=3.11"
# dependencies = ["mistralai<2"]
# ///

import os
import sys
from mistralai import Mistral


def extract_pdf_to_markdown(pdf_path: str) -> str:
    """Extract PDF to markdown using Mistral OCR."""
    api_key = os.environ.get("MISTRAL_API_KEY")
    client = Mistral(api_key=api_key)

    with open(pdf_path, "rb") as f:
        uploaded = client.files.upload(
            file={"file_name": os.path.basename(pdf_path), "content": f.read()},
            purpose="ocr"
        )

    signed_url = client.files.get_signed_url(file_id=uploaded.id, expiry=1)

    response = client.ocr.process(
        document={"document_url": signed_url.url},
        model="mistral-ocr-latest"
    )

    return "\n\n".join(page.markdown for page in response.pages)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: uv run extract_ocr.py <pdf_path>", file=sys.stderr)
        sys.exit(1)
    markdown = extract_pdf_to_markdown(sys.argv[1])
    print(markdown)
```

## MinerU and Zotero artifacts — separation of concerns

MinerU markdown/JSON are external research artifacts, not repository source. Preserve
that separation:

- Original PDFs belong under `~/pdfs` or [[zotero/SKILL|Zotero]] storage, not in
  agent/code repos.
- Extraction artifacts belong under `~/pdf-extraction` outputs or the relevant
  [[zotero/SKILL|Zotero]] attachment path, not in Git LFS.
- When [[zotero/SKILL|Zotero]] already has a PDF, resolve the local attachment path via
  the [[zotero/SKILL|zotero]] skill (running desktop local API) before downloading a
  duplicate.
- When attaching existing MinerU output back to a [[zotero/SKILL|Zotero]] library item,
  use the zotero skill's `just attach-extraction` — do not infer matches from filenames
  alone, and do not bypass the loop's attach order.

## Notes

- MinerU handles complex documents including tables, math equations, and multi-column
  layouts better than Mistral; that is why it is primary.
- For very large documents (>200 pages), MinerU's precise API rejects one-shot calls;
  chunk into ≤200-page pieces, or fall back to Mistral.
- Free tiers have usage limits — check the provider dashboard.
- For very large documents, consider processing in batches.