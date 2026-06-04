---
name: ocr-and-documents
description: "Extract text from PDFs/scans (pymupdf, marker-pdf)."
version: 2.3.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [PDF, Documents, Research, Arxiv, Text-Extraction, OCR]
    related_skills: [powerpoint]
---
# PDF & Document Extraction

For DOCX: use `python-docx` (parses actual document structure, far better than OCR). For
PPTX: see the `powerpoint` skill (uses `python-pptx` with full slide/notes support).
This skill covers **PDFs and scanned documents**.

## Step 1: Remote URL Available?

If the document has a URL, **always try `web_extract` first**:

```
web_extract(urls=["https://arxiv.org/pdf/2402.03300"])
web_extract(urls=["https://example.com/report.pdf"])
```

This handles PDF-to-markdown conversion via Firecrawl with no local dependencies.

Only use local extraction when: the file is local, web_extract fails, or you need batch
processing.

## Step 2: Choose Local Extractor

| Feature | pymupdf (~25MB) | marker-pdf (~3-5GB) |
| --- | --- | --- |
| **Text-based PDF** | ✅ | ✅ |
| **Scanned PDF (OCR)** | ❌ | ✅ (90+ languages) |
| **Tables** | ✅ (basic) | ✅ (high accuracy) |
| **Equations / LaTeX** | ❌ | ✅ |
| **Code blocks** | ❌ | ✅ |
| **Forms** | ❌ | ✅ |
| **Headers/footers removal** | ❌ | ✅ |
| **Reading order detection** | ❌ | ✅ |
| **Images extraction** | ✅ (embedded) | ✅ (with context) |
| **Images → text (OCR)** | ❌ | ✅ |
| **EPUB** | ✅ | ✅ |
| **Markdown output** | ✅ (via pymupdf4llm) | ✅ (native, higher quality) |
| **Install size** | ~25MB | ~3-5GB (PyTorch + models) |
| **Speed** | Instant | ~1-14s/page (CPU), ~0.2s/page (GPU) |

**Decision**: Use pymupdf unless you need OCR, equations, forms, or complex layout
analysis.

If the user needs marker capabilities but the system lacks ~5GB free disk:
> "This document needs OCR/advanced extraction (marker-pdf), which requires ~5GB for
> PyTorch and models. Your system has [X]GB free.
> Options: free up space, provide a URL so I can use web_extract, or I can try pymupdf
> which works for text-based PDFs but not scanned documents or equations."

* * *

## pymupdf (lightweight)

Run via `uvx` — no local install needed:

```bash
uvx pymupdf4llm --help
```

**Via helper script**:
```bash
uv run python scripts/extract_pymupdf.py document.pdf              # Plain text
uv run python scripts/extract_pymupdf.py document.pdf --markdown   # Markdown
uv run python scripts/extract_pymupdf.py document.pdf --tables     # Tables
uv run python scripts/extract_pymupdf.py document.pdf --images out/  # Extract images
uv run python scripts/extract_pymupdf.py document.pdf --metadata   # Title, author, pages
uv run python scripts/extract_pymupdf.py document.pdf --pages 0-4   # Specific pages
```

**Inline (uses uvx with pymupdf for one-shot invocation)**:
```bash
uvx --from pymupdf python3 -c "
import pymupdf
doc = pymupdf.open('document.pdf')
for page in doc:
    print(page.get_text())
"
```

* * *

## marker-pdf (high-quality OCR)

```bash
# Check disk space first
uv run python scripts/extract_marker.py --check
```

**Via helper script**:
```bash
uv run python scripts/extract_marker.py document.pdf                # Markdown
uv run python scripts/extract_marker.py document.pdf --json         # JSON with metadata
uv run python scripts/extract_marker.py document.pdf --output_dir out/  # Save images
uv run python scripts/extract_marker.py scanned.pdf                 # Scanned PDF (OCR)
uv run python scripts/extract_marker.py document.pdf --use_llm      # LLM-boosted accuracy
```

**CLI**:
```bash
uvx marker_single document.pdf --output_dir ./output
uvx marker /path/to/folder --workers 4    # Batch
```

* * *

## Arxiv Papers

```
# Abstract only (fast)
web_extract(urls=["https://arxiv.org/abs/2402.03300"])

# Full paper
web_extract(urls=["https://arxiv.org/pdf/2402.03300"])

# Search
web_search(query="arxiv GRPO reinforcement learning 2026")
```

## Split, Merge & Search

pymupdf handles these natively.
The snippets below are excerpts showing the logic; to run them, use `uvx --from pymupdf python3 -c "..."` for one-liners or a PEP 723 script for reusable tools.

```python
# Excerpt: Split — extract pages 1-5 to a new PDF
import pymupdf
doc = pymupdf.open("report.pdf")
new = pymupdf.open()
for i in range(5):
    new.insert_pdf(doc, from_page=i, to_page=i)
new.save("pages_1-5.pdf")
```

```python
# Excerpt: Merge multiple PDFs
import pymupdf
result = pymupdf.open()
for path in ["a.pdf", "b.pdf", "c.pdf"]:
    result.insert_pdf(pymupdf.open(path))
result.save("merged.pdf")
```

```python
# Excerpt: Search for text across all pages
import pymupdf
doc = pymupdf.open("report.pdf")
for i, page in enumerate(doc):
    results = page.search_for("revenue")
    if results:
        print(f"Page {i+1}: {len(results)} match(es)")
        print(page.get_text("text"))
```

No extra dependencies needed — pymupdf covers split, merge, search, and text extraction
in one package.

* * *

## Notes

- `web_extract` is always first choice for URLs

- pymupdf is the safe default — instant, no models, works everywhere

- marker-pdf is for OCR, scanned docs, equations, complex layouts — install only when
  needed

- Both helper scripts accept `--help` for full usage

- marker-pdf downloads ~2.5GB of models to `~/.cache/huggingface/` on first use

- For Word docs: use a PEP 723 inline script with `python-docx` (better than OCR — parses actual structure). `uvx python-docx` will not work because `python-docx` is a library, not a CLI tool. Use `uv run --with python-docx python -c "..."` for one-liners or a PEP 723 script for anything reusable.

- For PowerPoint: see the `powerpoint` skill (uses python-pptx)
