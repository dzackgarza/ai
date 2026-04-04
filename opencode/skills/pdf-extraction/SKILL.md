---
name: pdf-extraction
description: Use when extracting text and formulas from mathematical PDFs using MinerU.
---

# PDF Extraction

**Repository:** `~/pdf-extraction`

## Canonical Sources

| Document | Purpose |
|----------|---------|
| [`README.md`](~/pdf-extraction/README.md) | Extraction methods, commands, output structure |
| [`AGENTS.md`](~/pdf-extraction/AGENTS.md) | Agent guidelines, debugging workflow |
| [`.envrc`](~/pdf-extraction/.envrc) | SSH server configuration and workflow |
| [`justfile`](~/pdf-extraction/justfile) | Available recipes |
| [`GAPS.md`](~/pdf-extraction/GAPS.md) | Extraction log and completed jobs |

## Workflow

1. **Read `README.md`** - Determine extraction method (local GPU, SSH, API, or Mistral OCR)
2. **Check `justfile`** - Available recipes for local extraction
3. **Read `.envrc`** - SSH workflow commands (if no local GPU)
4. **Consult `AGENTS.md`** - Debugging and quality guidelines

## Banned Extraction Methods

**NEVER use these tools for mathematical PDFs:**

- `pdftotext` / `poppler-utils`
- `pymupdf` / `fitz`
- `pdfplumber`
- `pdfminer` / `pdfminer.six`
- `PyPDF2` / `pypdf`
- `borb`
- `pdf2image` + OCR (Tesseract)
- `camelot` / `tabula-py` (table extractors)
- `grobid`
- `scienceparser`
- `CERMINE`
- `any2txt` / `textract`
- `pdf-extract` (Ruby gem)
- `pdfreader`
- `pikepdf` (low-level, not extraction)
- `hocr`-based workflows
- `ocrmypdf` (document OCR, not math)
- Google Cloud Vision OCR
- AWS Textract
- Azure Computer Vision OCR

**Why these are banned:**

These tools produce **low-quality, misleading extractions** that are **never suitable for mathematical content**:

- Formula corruption (LaTeX → garbled text)
- Lost structure (theorems, proofs, definitions merged)
- Wrong character encoding (Greek letters, operators)
- No layout awareness (multi-column disasters)
- Table destruction
- Reference/citation corruption

**NEVER use a "fallback" strategy.** If you cannot extract a PDF using an accepted method from this repo:

1. **Declare failure** - The PDF cannot be reliably extracted
2. **Report the blocker** - What prevented extraction
3. **DO NOT** attempt workarounds with banned tools
4. **DO NOT** substitute low-quality extraction for high-quality failure

Mathematical content is too sensitive to corruption. A failed extraction is preferable to misleading garbage.

## Rules

- **DO NOT** duplicate commands or workflows from the canonical sources
- **DO NOT** guess extraction parameters - read the docs
- **DO** cross-reference the appropriate document for the task at hand
- **NEVER** use banned tools as "fallbacks"
