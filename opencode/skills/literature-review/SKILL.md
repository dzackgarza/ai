---
name: literature-review
version: 1.2.0
description: Use when finding academic papers on a topic, looking up specific DOIs, or drafting literature review sections with citations.
---
# Literature Review

Help write academic literature reviews using a multi-engine search integration (S2, OA,
CR, PM).

## Capabilities

- **Multi-Source Search**: Find relevant academic papers using Semantic Scholar (S2),
  OpenAlex (OA), Crossref (CR), and PubMed (PM).

- **Mathematics Paper Discovery**: For mathematics, combine general metadata sources
  with [[arxiv/SKILL|arXiv]], zbMATH/OpenAlex/Semantic Scholar, DOI lookup, [[zotero/SKILL|Zotero]], and the local PDF
  workflow.

- **Web Research Extraction**: For high-rate web-informed research, prefer a
  self-hostable extraction stack only when the built-in web/search tools are
  insufficient; see `references/web-research-extraction-stack.md`.

- **Full Abstracts**: All sources now return complete abstracts (PubMed uses `efetch`
  for full XML records).

- **DOI Extraction**: DOIs are extracted from all sources for cross-referencing and
  deduplication.

- **Automatic Deduplication**: When searching multiple sources (`--source all` or
  `--source both`), results are automatically deduplicated by DOI.

- **Polite Access**: Automatic email identification for OpenAlex/Crossref “Polite Pool”
  (via `USER_EMAIL` env var).

- **Abstract Reconstruction**: Reconstructs abstracts from OpenAlex inverted index
  format.

- **Synthesis**: Group papers by theme and draft review sections based on metadata.

## Environment Variables

| Variable | Purpose | Default |
| --- | --- | --- |
| `USER_EMAIL` | Email for polite API access | `anonymous@example.org` |
| `CLAWDBOT_EMAIL` | Fallback if USER_EMAIL not set | — |
| `SEMANTIC_SCHOLAR_API_KEY` | Optional S2 API key for higher rate limits | — |
| `OPENALEX_API_KEY` | Optional OpenAlex API key | — |

## Workflows

### 1. Broad Search (All Bases)

Get a comprehensive overview from all major academic databases.
Results are automatically deduplicated by DOI.

```bash
python3 scripts/lit_search.py search "impact of glycyrrhiza on bifidobacterium" --limit 5 --source all
```

### 2. Targeted Search

- **OpenAlex** (`oa`): Fast and comprehensive, good abstracts.

- **Semantic Scholar** (`s2`): High-quality citation data and TL;DRs.

- **Crossref** (`cr`): Precise DOI-based metadata (no abstracts).

- **PubMed** (`pm`): Gold standard for biomedical research, full abstracts and PMIDs.

```bash
python3 scripts/lit_search.py search "prebiotic effects of liquorice" --source pm
```

### 3. Comparing Sources

Search both S2 and OA simultaneously to ensure nothing is missed.
Deduplicated by default.

```bash
python3 scripts/lit_search.py search "Bifidobacterium infantis growth" --source both
```

### 4. Getting Full Details (S2)

Retrieve detailed metadata including TL;DR summaries.

```bash
python3 scripts/lit_search.py details "DOI:10.1016/j.foodchem.2023.136000"
```

### 5. Writing the Review

1. **Extract**: Pull key findings from the abstracts found.

2. **Organize**: Group findings into a logical structure (e.g., chronological or
   thematic).

3. **Draft**: Use the “Think step-by-step” approach to synthesize multiple sources into
   a coherent narrative.

### 6. Mathematics Paper Retrieval

For mathematics literature work, use `references/math-paper-retrieval.md` as the
workflow:

- search metadata with this skill and [[arxiv/SKILL|arxiv]],

- resolve DOI/arXiv/Zotero identity before downloading,

- store PDFs through `~/pdfs` and extract through `~/pdf-extraction`,

- use [[reading-pdfs/SKILL|reading-pdfs]] for local paper reading.

## Output Format

Each result includes:

- `id`: Source-specific identifier (PMID for PubMed, OpenAlex ID, S2 paper ID, DOI for
  Crossref)

- `doi`: DOI when available (used for deduplication)

- `title`: Paper title

- `year`: Publication year

- `authors`: List of author names

- `abstract`: Full abstract text (when available)

- `venue`: Journal or conference name

- `citationCount`: Citation count (S2, OA)

- `source`: Which database the result came from

## Tips for Success

- **Citations**: Always cross-reference the DOI or PMID for accuracy in bibliography.

- **Filtering**: Focus on papers with higher `citationCount` or recent years for a more
  modern review.

- **PubMed for Medicine**: Use `--source pm` for the most reliable biomedical
  literature.

- **Deduplication**: Multi-source searches automatically remove duplicates; use single
  sources if you need raw counts.

## References

- `references/math-paper-retrieval.md` — canonical mathematics paper retrieval workflow.

- `references/web-research-extraction-stack.md` — high-volume web extraction stack
  notes.
