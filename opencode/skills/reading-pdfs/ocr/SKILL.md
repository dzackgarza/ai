---
name: pdf-ocr-reading
description: Use when reading a PDF — converts to markdown via Mistral OCR with local
  caching.
metadata:
  author: dzack
  version: 0.1.0
---
# Reading PDFs with Mistral OCR

## Overview

Use Mistral OCR API as the first attempt for converting PDFs to markdown.
It has some amount of free usage on the free tier.

**Important:** Before extracting any PDF, check if it already exists in the local
collection at `~/pdfs/`.

## PDF Storage Structure

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

**Always save the original PDF alongside the extracted markdown.** Name them `paper.pdf`
and `paper.md` for [[research-discovery/search/SKILL|arXiv]] papers.

For [[research-discovery/search/SKILL|arXiv]] papers:

- Download URL: `https://arxiv.org/pdf/{arxiv_id}.pdf`

- Store as: `~/pdfs/arxiv/{arxiv_id}/paper.md`

## Workflow

1. **Check if already extracted** - Look for `~/pdfs/arxiv/{arxiv_key}/paper.md`

2. **If not exists** - Download PDF, extract with OCR, save to appropriate location

3. **Return the markdown content**

## Using Mistral OCR

### Basic OCR Extraction (PEP 723 Script)

Save the following as a standalone script and run with `uv run`:

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

### Utility Function (Excerpt)

**Excerpt only — do not save/run directly.**
This snippet shows the logic. To run it, embed in a PEP 723 script (see the full
script template above) or include in an existing uv-managed project with `mistralai`
declared as a dependency.

```python
import os
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
```

### Downloading and Extracting an ArXiv Paper

```python
import os
import urllib.request

def get_arxiv_paper(arxiv_id: str, base_dir: str = os.path.expanduser("~/pdfs/arxiv")) -> str:
    """
    Download arXiv paper and extract to markdown if not already cached.

    Args:
        arxiv_id: e.g., "0704.0001"
        base_dir: Base directory for PDF storage

    Returns:
        Path to extracted markdown file
    """
    # Check if already extracted
    paper_dir = os.path.join(base_dir, arxiv_id)
    paper_md = os.path.join(paper_dir, "paper.md")

    if os.path.exists(paper_md):
        with open(paper_md, "r") as f:
            return f.read()

    # Create directory
    os.makedirs(paper_dir, exist_ok=True)

    # Download PDF
    pdf_path = os.path.join(paper_dir, "paper.pdf")
    if not os.path.exists(pdf_path):
        url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
        urllib.request.urlretrieve(url, pdf_path)

    # Extract to markdown using the script above
    # Save as scripts/extract_ocr.py with PEP 723 metadata, then:
    # uv run scripts/extract_ocr.py {pdf_path}
    markdown = extract_pdf_to_markdown(pdf_path)

    # Save markdown
    with open(paper_md, "w") as f:
        f.write(markdown)

    return markdown
```

## Example Usage

```python
# Get a paper (downloads and caches if not exists)
paper = get_arxiv_paper("0704.0001")
print(paper[:1000])  # First 1000 chars
```

## Local Extraction ([[justfile/SKILL|justfile]] recipes)

For extracting PDFs locally without the Mistral API, use the managed recipes in
`~/pdf-extraction`. These handle environment setup automatically via `uv sync`.

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
rendered PDFs or Markdown.
The recipe should own that mode; do not run private one-off extraction scripts.
After extraction, verify the expected output files and keep the run log with the
artifacts.

## [[zotero/SKILL|Zotero]] and MinerU Artifacts

MinerU markdown/JSON are external research artifacts, not repository source.
Preserve that separation:

- Original PDFs belong under `~/pdfs` or [[zotero/SKILL|Zotero]] storage, not in agent/code repos.

- Extraction artifacts belong under `~/pdf-extraction` outputs or the relevant [[zotero/SKILL|Zotero]]
  attachment path, not in Git LFS.

- When [[zotero/SKILL|Zotero]] already has a PDF, prefer resolving the local attachment path via the
  [[zotero-api/SKILL|zotero-api]] skill before downloading a duplicate.

- When attaching existing MinerU output back to [[zotero/SKILL|Zotero]], verify against the running
  [[zotero/SKILL|Zotero]] local API and Better BibTeX key; do not infer matches from filenames alone.

When only structured extraction data is needed, prefer a recipe that emits the
minimal MinerU JSON artifacts (`middle.json` and `content_list.json`) without
generating extra rendered PDFs or Markdown. The recipe should own that mode;
do not run private one-off extraction scripts. After extraction, verify the
expected output files and keep the run log with the artifacts.

## [[zotero/SKILL|Zotero]] and MinerU Artifacts

MinerU markdown/JSON are external research artifacts, not repository source.
Preserve that separation:

- Original PDFs belong under `~/pdfs` or [[zotero/SKILL|Zotero]] storage, not in agent/code repos.
- Extraction artifacts belong under `~/pdf-extraction` outputs or the relevant
  [[zotero/SKILL|Zotero]] attachment path, not in Git LFS.
- When [[zotero/SKILL|Zotero]] already has a PDF, prefer resolving the local attachment path via
  the [[zotero-api/SKILL|zotero-api]] skill before downloading a duplicate.
- When attaching existing MinerU output back to [[zotero/SKILL|Zotero]], verify against the
  running [[zotero/SKILL|Zotero]] local API and Better BibTeX key; do not infer matches from
  filenames alone.

## Notes

- The OCR handles complex documents including tables, math equations, and multi-column
  layouts

- Free tier has some OCR usage included (check dashboard for limits)

- The API returns `pages_processed` in usage info

- For very large documents, consider processing in batches
