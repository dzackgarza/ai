---
order: 30
title: 'Critical Directive: Research Before Action, Always'
---

**Split by ownership.** For project-internal unknowns, the rule below ("tree first")
applies — expose the local directory structure and configs before narrowing.

For external tools, compilers, libraries, APIs, package managers, providers, or exact
error messages, the first pass is different. Load `known-solution-first` and search
public contracts (docs, release notes, issues, known fixes) before inspecting local
integration. Local artifacts answer "what is on this machine." External sources answer
"what does the tool mean, what is the documented contract, and has this error been
solved upstream."

START EVERY LOCAL EXPLORATION BY USING A `tree` COMMAND.
Do NOT spike with greps, guess file paths or directories, or run narrow searches --
start broad and THEN narrow. But for tool/API/compiler unknowns, reach for web search,
Context7, DeepWiki, and upstream docs before local probing. See `known-solution-first`.

**BEFORE TAKING ANY ACTION**: review the most immediately recent user requests, and verbally confirm whether or not the actions you are planning actually align with the directive.
User directives are highly specific, not suggestions.
Verbally confirm what the user's stated directive was, your planned action, and why the goal you're pursuing is the exact goal the user stated.

Inspect the repo's declared entrypoints, docs, configs, and runtime surfaces before diving into targeted source edits. Valid discovery paths include:

- `tree`, `find`, `ls` — expose actual directory structure first
- `just --list`, `package.json#scripts`, `Makefile`, CLI `--help` — learn available commands
- Config files (pyproject.toml, .envrc, tsconfig.json, Cargo.toml, etc.) — understand project conventions
- README, AGENTS.md, architectural docs — read for intent
- GitHub issues, web search, Context7/DeepWiki, existing skills, `known-solution-first` skill
- Source code itself (via `tree`, `probe extract`, Serena, glob, read) when docs are stale or incomplete

Never make an edit without first understanding the repo's shape and the specific boundary you are about to change.
Never guess commands, endpoints, or file paths without running them first.
Do not treat docs as the sole source of truth — code, configs, CLI output, generated artifacts, and runtime diagnostics are all valid reality surfaces.
