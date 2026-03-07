---
name: reading-pdfs
description: Use when reading a PDF — converts to markdown via Mistral OCR with local caching.
metadata:
  author: dzack
  version: "0.1.0"
---

# Reading PDFs with Mistral OCR

## Overview

Use Mistral OCR API as the first attempt for converting PDFs to markdown. It has some amount of free usage on the free tier.

**Important:** Before extracting any PDF, check if it already exists in the local collection at `~/pdfs/`.

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

**Always save the original PDF alongside the extracted markdown.** Name them `paper.pdf` and `paper.md` for arXiv papers.

For arXiv papers:

- Download URL: `https://arxiv.org/pdf/{arxiv_id}.pdf`
- Store as: `~/pdfs/arxiv/{arxiv_id}/paper.md`

## Workflow

1. **Check if already extracted** - Look for `~/pdfs/arxiv/{arxiv_key}/paper.md`
2. **If not exists** - Download PDF, extract with OCR, save to appropriate location
3. **Return the markdown content**

## Using Mistral OCR

### Installation

```bash
pip install mistralai
```

### Basic OCR Extraction

```python
import os
from mistralai import Mistral

# Use environment variable - never hardcode API keys
api_key = os.environ.get("MISTRAL_API_KEY")
client = Mistral(api_key=api_key)

# Upload PDF
with open("/path/to/file.pdf", "rb") as f:
    uploaded = client.files.upload(
        file={"file_name": "file.pdf", "content": f.read()},
        purpose="ocr"
    )

# Get signed URL
signed_url = client.files.get_signed_url(file_id=uploaded.id, expiry=1)

# Process with OCR
response = client.ocr.process(
    document={"document_url": signed_url.url},
    model="mistral-ocr-latest"
)

# Extract markdown
markdown = "\n\n".join(page.markdown for page in response.pages)
```

### Utility Function

```python
def extract_pdf_to_markdown(pdf_path: str) -> str:
    """Extract PDF to markdown using Mistral OCR."""
    import os
    from mistralai import Mistral

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

    # Extract to markdown
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

## Notes

- The OCR handles complex documents including tables, math equations, and multi-column layouts
- Free tier has some OCR usage included (check dashboard for limits)
- The API returns `pages_processed` in usage info
- For very large documents, consider processing in batches
