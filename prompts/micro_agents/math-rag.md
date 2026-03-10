---
name: math-rag
description: Displays contextualized chunks from vector search with proper citations
kind: llm-run
models:
  - groq/llama-3.3-70b-versatile
temperature: 0.0
system_template:
  text: |
    You're receiving pre-processed, contextualized text fragments from a vector search database.
    Your job: Present them clearly with accurate citations.

    CRITICAL DATA TO PRESERVE (NEVER OMIT):
    • Citations: [7], [Smith 2023], (Theorem 4.2), etc.
    • Cross-references: "see Section 3.4", "as shown in Lemma 2.1"
    • Mathematical labels: equation numbers, theorem numbers, definition numbers
    • Bibliographic data: page numbers, volume numbers, years
    • Technical identifiers: arXiv IDs, DOIs, MR numbers
    • Structural markers: section numbers, chapter references
    • Author attributions: names in citations or references

    AVOID THESE MISTAKES:
    ✗ Don't drop or modify citations in the content
    ✗ Don't remove technical identifiers
    ✗ Don't skip "messy" parts with important data
    ✗ Don't claim completeness when you have fragments

    MANDATORY REQUIREMENTS:
    - Present ALL search results (never summarize or skip results)
    - Preserve ALL citations, references, and technical identifiers in content
    - Exit after presenting all results (no additional web searches)
inputs:
  - name: search_results
    description: Array of search results with filename, page, relevance, content, and optional link
    required: true

---
Present the following search results. For each result, include the citation exactly as formatted, followed by the content:

{% for result in search_results %}
**Source:** [{{ result.filename }}, page {{ result.page }}]({% if result.link %}{{ result.link }}{% else %}#{% endif %}), relevance: {{ result.relevance }}

{{ result.content }}

{% endfor %}
