---
name: ocr-and-documents
description: "Extract text from PDFs/scans — redirects to Mistral OCR, not pymupdf."
version: 3.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [PDF, Documents, Research, Arxiv, Text-Extraction, OCR]
    related_skills: [reading-pdfs, powerpoint]
---

# PDF & Document Extraction

**The entire point of this skill is to redirect agents away from low-quality PDF
extraction tools (pymupdf, marker-pdf, docling, pymupdf4llm) and toward high-quality
solutions.**

**Do not** reach for pymupdf, marker-pdf, or any ad-hoc PDF library unless explicitly
directed to. These produce poor results on complex documents, equations, tables, and
scanned pages. The system has better options.

* * *

## Tool Selection (in order of preference)

| Priority | Tool | When to use |
| --- | --- | --- |
| **1** | **Mistral OCR** (via `reading-pdfs` skill) | **Default** for any PDF — API-based, handles tables, math, scanned docs, multi-column. Check `reading-pdfs` skill. |
| **2** | **Managed recipes** (`~/pdf-extraction` justfile) | When Mistral API is unavailable. Uses Docling / MinerU with managed environments. |
| **3** | **pymupdf** | **Only** for trivial text-only PDFs when neither Mistral API nor the extraction recipes work. Minimal quality. |
| **4** | **marker-pdf** | **Do not use.** ~3-5GB install for results that are still worse than Mistral OCR. |

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

### 2. Fallback: managed local extraction

If Mistral OCR is unavailable (no API key, offline), use the recipes in
`~/pdf-extraction`:

```bash
just -f ~/pdf-extraction/justfile -d ~/pdf-extraction docling document.pdf
just -f ~/pdf-extraction/justfile -d ~/pdf-extraction mineru document.pdf
```

These manage their own environments via `uv sync`. Do not create a separate venv or
install dependencies manually.

### 3. Last resort: pymupdf (text-only PDFs only)

For simple text-based PDFs when neither API nor recipes are available:

```bash
uvx --from pymupdf python3 -c "
import pymupdf
doc = pymupdf.open('document.pdf')
for page in doc:
    print(page.get_text())
"
```

pymupdf will **not** handle: scanned pages, equations, complex tables, reading order,
headers/footers removal. If the document needs any of these, do not use pymupdf.

* * *

## What to Avoid

- **pymupdf4llm** — installs pymupdf + pymupdf4llm but quality is still far below Mistral
  OCR. Do not reach for it.

- **marker-pdf** — downloads ~2.5GB of PyTorch models and still produces worse results
  than Mistral OCR. Not worth the disk space or time.

- **Ad-hoc OCR scripts** — do not write your own tesseract/pytesseract pipeline or use
  `pdf2image` + `pytesseract`. Delegate to the managed recipes or Mistral OCR.

- **Docling standalone** — use through `~/pdf-extraction` justfile, not installed ad-hoc.

* * *

## Non-PDF Documents

| Format | Tool | Notes |
| --- | --- | --- |
| DOCX | `python-docx` via PEP 723 script | Parses actual structure — far better than OCR |
| PPTX | `python-pptx` via `powerpoint` skill | Full slide/notes support |
| HTML | `web_extract` or `python-html2text` | Prefer URL extraction |
