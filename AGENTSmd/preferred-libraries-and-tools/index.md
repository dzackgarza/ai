---
order: 110
title: Preferred Libraries and Tools
---

- `agent-memory` for managing memories and agent-facing documentation (see the Memory section)

- `gh` for all Github operations (alternative to webfetching)

  - Never use backticks in text pushed through gh (or any other CLI tools), since this induces shell escaping.

- `tree`, `exa` for exploration

- `ctags` for code navigation — use `just -f ~/opencode-plugins/justfile -C ~/your/working/directory ctags`

- `opencode` for most agent and LLM-related tasks.

  - Use `command opencode` instead of `opencode` to use the CLI instead of the background server.

- `gemini`, `codex`, `claude`, `qwen`, `jules` for one-off agentic work, when usage is available.

  - These are paid models, ask before using.

- semtools `search` for semantically searching expository text,

  - `npx -y -p @llamaindex/semtools search "spectral sequence" ~/notes/Obsidian/Unsorted/*.md`

- PDF extraction: **LOAD `reading-pdfs` skill.** Use justfile recipes in `~/pdf-extraction`, not ad hoc installs.

  - Never: `pdftotext`, `pymupdf`, etc.
    Extremely low quality.
    Prefer e.g. `mineru`

- `open-issues` to list all outstanding open issues across synced plugin trackers.

- `probe` and `ast-grep` for semantic searching — **always** `npx -y @probelabs/probe`. **LOAD `probe` skill.**

- `jq` and `yq` for manipulating JSON and YAML

- `uv` for all python-related projects. See `self-contained-python-scripts` under
  `tool-provisioning-and-environment-hygiene` for the mandatory policy on agent-authored
  Python scripts with dependencies.

- `bun` and typescript for all JS-related development

- `svelte`, `vite`, `tailwind` etc for all HTML-related development

- `pandoc` for document construction and conversions

- `flowmark` for markdown formatting (semantic line breaks, pandoc-structural awareness).
  Run via just recipe: `just ~/.pandoc/justfile format-markdown <file> [files...]`

- `ctx7` for doc lookup.

  - Search for library and get ID: ` npx ctx7 library react "hooks"`

  - Fetch docs for specific library ID: `npx ctx7 docs /facebook/react "useEffect"`

- `deepwiki` for speeding up doc exploration, locating relevant code quicker

  - `uvx mcp2cli --mcp https://mcp.deepwiki.com/mcp read-wiki-structure --repo-name facebook/react`

  - `uvx mcp2cli --mcp https://mcp.deepwiki.com/mcp ask-question --repo-name facebook/react --question "How does useEffect work?"`

- `mcp2cli` — CLI bridge for any MCP server.
  Use `--toon` for token-efficient output (40-60% token savings).

  - List tools (ALWAYS use --toon for LLM consumption) `uvx mcp2cli --mcp https://mcp.deepwiki.com/mcp --list --toon`

  - E.g. `uvx mcp2cli --mcp-stdio "npx @modelcontextprotocol/server-filesystem /tmp" --list --toon`
