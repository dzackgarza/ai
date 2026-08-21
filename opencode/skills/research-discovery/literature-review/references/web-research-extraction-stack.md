# Web Research Extraction Stack

## Purpose

Support high-rate, low-cost web-informed research when built-in search/fetch tools are
insufficient.
The desired output format is clean Markdown or structured JSON suitable for
LLM ingestion and citation checking.

## Candidate Stack

- **Crawl4AI**: primary self-hostable crawler/scraper for Markdown/JSON extraction,
  selectors, metadata, links, and dynamic content through browser automation.

- **ScrapeGraphAI**: optional semantic extraction layer when raw page content needs
  schema-guided structuring or summarization.

- **Firecrawl**: fallback for deep crawling, dynamic JavaScript-heavy pages, or batch
  extraction where its API/self-hosted mode is appropriate.

## Current Routing

Use current web/search tools first.
Reach for this stack only when the task requires repeated crawling, structured
extraction, or self-hosted high-volume collection.
If implemented, it should become a current skill or MCP entry with fresh documentation
checks and current upstream validation.

## Output Contract

- Preserve source URLs and retrieval dates.

- Keep extracted text separate from synthesis.

- Emit Markdown or JSON, not agent prose.

- Do not hide failed fetches behind partial summaries.

- For research claims, pass results through `research-synthesis-workflow` before
  drafting conclusions.
