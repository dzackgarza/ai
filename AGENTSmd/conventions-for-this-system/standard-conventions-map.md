---
title: Standard Conventions Map
order: 90
tags:
- source-system-contract
- source-owner-preference
- function-constrain
- function-route
- function-allocate
- function-procedure
- retest-toolchain-change
---

Problem → canonical system convention. Follow these by default; deviate only
with explicit user approval.

| Problem | Convention |
|---------|-----------|
| Bespoke config format choice | **TOML.** All bespoke project configs are TOML, parsed with a real TOML parser — never hand-rolled INI/regex parsing, never JSON/YAML for new bespoke configs. Use Python's `tomllib` (read) or `tomli-w`/`tomlkit` (write). |
| Config file location | **XDG-compliant paths.** Configs live under `~/.config/<app>/`, not as sidecar files attached to repos (which are just clutter). |
| Task runner | **justfile** ([[justfile]] skill). Never Makefiles, `npm run`, `bun run`, or other ad-hoc runners unless absolutely required by an external constraint — and even then minimize their use so as not to confuse the single-runner convention. |
| Interactive wizards / prompts | **gum.** Any interactive CLI prompt, confirmation, selection, spinner, or wizard — use `gum`. |
| Search / filtering UX | **fzf.** Fuzzy search and interactive filtering of any list. |
| User-facing desktop menus | **dmenu / rofi.** Launchers, quick-select menus, and desktop-issued prompts. |
| Desktop widgets | **ags.** Bars, panels, system tray, and persistent desktop widgets. |
| JS-based projects | **bun.** Runtime and package execution for any JavaScript/TypeScript project. |
| JS dependency management | **pnpm.** Never `npm`. Install deps and run scripts via `pnpm`. |
| Nontrivial CLIs | **Python** ([[writing-scripts-and-cli-interfaces]] skill). Build command-line tools in Python, not shell, once the task outgrows a one-liner. |
| Memory | **agent-memory** ([[agent-memory]] skill). Durable knowledge, plans, and project state live in the central vault. |
| Plans | **agent-memory** ([[agent-memory]] skill). Always file plans as `plan` records with agent-memory, never as loose repo-local markdown. |
| System-wide search | **locate** (or `kpsewhich` for TeX), not `rg ~`-style filesystem crawls. Use the right index for the domain. |
| Mathematical calculations | **Prefer symbolic and semantic.** `sage`, `sympy`, GAP, Julia, Macaulay2, Singular — not naive float arithmetic. |
| Web UIs | **Vite + Svelte/React + Tailwind.** Never hand-roll HTML or CSS; use the framework's component and styling system. |
| Desktop UIs | **Tauri** ([[developing-linux-guis]] skill). Never Qt, Electron, or other heavy GUI frameworks. |
| Markdown parsing | **Pandoc CLI or package, use the AST.** Always semantic parsing, never regex. Embedded Pandoc + custom filters highly preferable to hand-rolled scraping solutions. |
| LaTeX parsing | **Pandoc AST, plastex.** Semantic parsing, never regex-based extraction. |
| Linters / type-checkers / autoformatters | **Always integrated in upstream QC.** Use locally and then push upstream. Prefer always-on, opinionated autoformatters and always use autofix flags. |
| Autoformatting markdown | **Flowmark fork.** Use the flowmark fork for semantic markdown autoformatting. |
| PDF parsing | **reading-pdfs** ([[reading-pdfs]] skill). Use Mistral OCR API as primary extraction; MinerU for local structured extraction. Never hand-rolled PDF scraping. |
| Finding papers | **Local Zotero search first** ([[zotero]] skill), which has markdown extractions — cite by BibTeX key. arxiv ([[arxiv]] skill) second, cite by URL. |
| APIs | **OpenAPI spec.** Always describe APIs with an OpenAPI specification. |
| Greenfield is never greenfield | **Find 3–5 strong, vetted reference implementations first** ([[known-solution-first]] skill). Borrow liberally — not as dependencies, but as a way to understand patterns in code that has already solved the problems. Never implement from scratch without first finding prior art. |