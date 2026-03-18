---
name: read-arxiv-paper
description: Use when asked to read an arxiv paper given an arxiv URL
---

You will be given a URL of an arxiv paper, for example:

https://www.arxiv.org/abs/2601.07372

### Part 1: Normalize the URL

The goal is to fetch the TeX Source of the paper (not the PDF!). Transform the URL to use `/src/`:

https://www.arxiv.org/src/2601.07372

### Part 2: Download the paper source

Fetch the URL to a local `.tar.gz` file at `~/.cache/arxiv/{arxiv_id}.tar.gz`.

If the file already exists, skip the download.

### Part 3: Unpack the file

Unpack the contents into `~/.cache/arxiv/{arxiv_id}/` directory.

### Part 4: Locate the entrypoint

Every LaTeX source usually has an entrypoint such as `main.tex`. Find it by looking for `\documentclass` or `\begin{document}`.

### Part 5: Read the paper

Read the entrypoint and recurse through all relevant source files (`\input`, `\include`) to read the full paper.

### Part 6: Summarize and store via Serena

Once you've read the paper, produce a structured markdown summary covering:

- **Title and authors**
- **Core contribution / thesis**
- **Key methods and techniques**
- **Main results and findings**
- **Potential applications and relevance** to the current project

Store the summary using Serena's `write_memory` tool. Use a descriptive memory name like `paper_{tag}` where `{tag}` is a short slug derived from the paper's topic (e.g. `paper_conditional_memory`, `paper_lattice_embeddings`). First use `list_memories` to check the name doesn't collide with an existing memory.

This makes the summary available in future conversations via Serena's `read_memory` tool without any manual file management.
