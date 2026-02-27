# Zotero Librarian

**Tools for managing your Zotero library.**

## Quick Start

```bash
# See what's available
just

# Library overview
just stats

# Find all quality issues
just quality
```

## Philosophy

These are **tools for intelligent agents**, not automation scripts.

### Design Principles

- **Readable** - Well-documented, self-contained Python
- **Adaptable** - Start here, modify for your needs
- **Non-destructive** - Find issues first, then decide what to fix
- **No Truncation** - Always return complete data. If a query returns 500 items, return all 500.

## Tools

### Library Overview

```bash
just stats        # Item counts, collections, attachments
just quality      # All quality issues at a glance
```

### Find Issues

```bash
just find-no-pdf         # Items without PDF attachments
just find-duplicates     # Duplicate titles
just find-similar-tags   # Similar tags (typos, variations)
```

### Browse

```bash
just list-collections    # All collections with counts
just list-tags           # All tags with frequency
```

### Fix Issues

```bash
just tag-needs-pdf    # Tag all items missing PDF
```

### Python

```bash
just shell    # Python REPL with library loaded
```

## Python API

```python
from agents import ZoteroAgent

lib = ZoteroAgent()

# Library overview
stats = lib.library_stats()
issues = lib.find_quality_issues()

# Find problems
no_pdf = lib.find_items_without_pdf()
duplicates = lib.find_duplicates_by_title()

# Fix issues (with judgment)
for item in no_pdf[:10]:  # First 10
    lib.add_tags(item["key"], ["needs-pdf"])
```

## Requirements

- Zotero 7+ running
- Local API enabled: **Edit → Settings → Advanced → "Allow other applications to communicate with Zotero"**

## Installation

```bash
just install    # Uses uv
```

## Project Structure

```
zotero_librarian/
├── agents.py            # Main tool - start here
├── README.md            # This file
├── justfile             # Quick commands
├── .venv/               # Python environment (use it)
├── _dev/                # Development (source, tests, docs)
└── zoter_librarian/     # Legacy nested project (ignored)
```

**For librarians:** Use `agents.py`, `just`, and `.venv/` at the top level.

**For developers:** See `_dev/` for source code and documentation.
