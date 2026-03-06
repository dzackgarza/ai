---
name: semantic-search
description: Run semantic search and ask questions over existing text/markdown collections with SemTools.
metadata:
  author: dzack
  version: "0.1.0"
---

# Semantic Search with SemTools

## Overview

Use this workflow for fast document QA on text-based data:

1. Ensure inputs are already text/markdown
2. `search` relevant chunks
3. `ask` only on narrowed context

This avoids token-limit failures from sending entire corpora to `ask`.

For PDF extraction/caching, use the `reading-pdfs` skill first.

This skill assumes `ask` already has a working model in `~/.semtools_config.json`.

## Environment

- `ask` uses OpenAI-compatible config in `~/.semtools_config.json`

Do not hardcode keys in scripts. Use environment variables.

## Use Current Config (Default Path)

Use the currently selected `ask` config exactly as-is.

1. Validate `ask` is live.
2. Run `search` to narrow context.
3. Pipe narrowed text to `ask`.

Quick live check:

```bash
printf 'test' | ask "Reply with OK"
```

## Search Usage

Use semantic search on text-based files:

```bash
search "Higgs boson" ~/pdfs/arxiv/0704.0001/*.md --max-distance 0.8 --n-lines 5
```

Observed behavior in this environment: stdin mode may be more reliable than file-arg mode.

Recommended:

```bash
cat ~/pdfs/arxiv/0704.0001/paper.md | search "Higgs boson" --max-distance 0.8 --n-lines 5
```

## Ask Usage

Ask over small content:

```bash
printf 'Lattice theory and integer programming are related.' | ask "Summarize in one sentence."
```

Ask over one markdown paper:

```bash
cat ~/pdfs/arxiv/0704.0001/paper.md | ask "In 3 bullet points, what are the main findings?"
```

## Context-Sizing Guidance

- Full single-paper context worked in testing.
- Oversized multi-paper or repeated input can exceed context/token limits.
- Prefer `search -> ask` pipelines for large collections.

Pattern (recommended for large files):

```bash
cat FILE.md | search "your question keywords" --max-distance 0.7 --n-lines 6 | ask "Answer precisely with citations from snippets."
```

Multi-file pattern:

```bash
cat ~/pdfs/arxiv/*/paper.md | search "your topic" --max-distance 0.7 --n-lines 6 | ask "Summarize themes and cite snippet evidence."
```

## Quick Health Checks

Check search:

```bash
cat ~/pdfs/arxiv/0704.0001/paper.md | search "LHC" --max-distance 0.8 --n-lines 3
```

Check ask:

```bash
printf 'test' | ask "Reply with OK"
```

## Troubleshooting (Footnote)

Only when the current config fails (rate limits, empty content, context failures):

1. Reduce context via `search` before `ask`.
2. Re-run live check.
3. If still failing, use `model-selection` to choose and validate another model.
