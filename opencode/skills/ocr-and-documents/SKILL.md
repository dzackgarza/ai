---
name: ocr-and-documents
description: "Extract text from PDFs/scans — redirects to high-quality extraction (Mistral OCR, marker-pdf), away from pymupdf garbage."
version: 3.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [PDF, Documents, Research, Arxiv, Text-Extraction, OCR]
    related_skills: [reading-pdfs, powerpoint]
---

# PDF & Document Extraction

**The purpose of this skill is to redirect agents away from pymupdf and similar
low-quality PDF tools, toward tools that actually handle mathematics, equations, tables,
and scanned documents correctly.**

This is a mathematical research system. Correct equation extraction is the primary
requirement. "Lightweight" tools that produce garbage on math are not acceptable.

* * *

## Tool Selection (in order of preference)

| Priority | Tool | When to use |
| --- | --- | --- |
| **1** | **Mistral OCR** (via `reading-pdfs` skill) | **Default** — API-based, handles tables, math, scanned docs, multi-column. Check `reading-pdfs` skill. |
| **2** | **marker-pdf** | High-quality local fallback when Mistral API is unavailable. Handles math, equations, OCR, complex layouts. ~5GB install (negligible for a research system). |
| **3** | **Managed recipes** (`~/pdf-extraction` justfile) | Docling / MinerU with managed environments. When neither Mistral API nor marker-pdf are suitable. |
| **4** | **pymupdf** | **Garbage on math.** Only for trivial text-only PDFs where nothing else is available and equations are not needed. |

* * *

## Workflow

### 1. Try Mistral OCR first

Load the `reading-pdfs` skill and follow its extraction workflow. This uses the Mistral
API with local caching under `~/pdfs/`.

```bash
# After loading the reading-pdfs skill, run the PEP 723 script:
uv run scripts/extract_ocr.py document.pdf
```

Mistral OCR handles: text, tables, equations, scanned documents, multi-column layouts,
code blocks.

### 2. Fallback: marker-pdf

When Mistral OCR is unavailable (no API key, offline), use marker-pdf for high-quality
local extraction:

```bash
# Single file
uvx marker_single document.pdf --output_dir ./output

# Batch
uvx marker /path/to/folder --workers 4
```

**Why marker-pdf over pymupdf:** marker-pdf handles equations, LaTeX, scanned pages,
complex tables, reading order. pymupdf produces garbage on all of these. The ~5GB
install is a one-time cost for correct extraction, which is the only acceptable outcome
for research documents.

### 3. Fallback: managed local recipes

Use the managed recipes in `~/pdf-extraction` for docling/mineru extraction:

```bash
just -f ~/pdf-extraction/justfile -d ~/pdf-extraction docling document.pdf
just -f ~/pdf-extraction/justfile -d ~/pdf-extraction mineru document.pdf
```

These manage their own environments via `uv sync`. Do not create a separate venv or
install dependencies manually.

### 4. Last resort: pymupdf (text-only PDFs only)

Only when the document is purely text (no equations, no tables, no scanned pages) and
none of the above options are available:

```bash
uvx --from pymupdf python3 -c "
import pymupdf
doc = pymupdf.open('document.pdf')
for page in doc:
    print(page.get_text())
"
```

pymupdf will **not** handle: scanned pages, equations, complex tables, reading order,
headers/footers removal. **For mathematical papers, pymupdf is useless** — it cannot
extract equations or LaTeX.

* * *

## What to Avoid

- **pymupdf4llm** — a wrapper around pymupdf. Same garbage on math.

- **pymupdf for anything non-trivial** — produces unusable output on equations, tables,
  scanned documents.

- **Ad-hoc OCR pipelines** — do not build your own tesseract/pytesseract/pdf2image
  pipeline. Use marker-pdf or the managed recipes instead.

- **Installing extraction tools manually** — always use `uvx` for one-shot tools or the
  `~/pdf-extraction` justfile for managed extraction. No `pip install marker-pdf` or
  `pip install pymupdf`.

* * *

## Non-PDF Documents

| Format | Tool | Notes |
| --- | --- | --- |
| DOCX | `python-docx` via PEP 723 script | Parses actual structure — far better than OCR |
| PPTX | `python-pptx` via `powerpoint` skill | Full slide/notes support |
| HTML | `web_extract` or `python-html2text` | Prefer URL extraction |
