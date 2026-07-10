---
order: 110
tags:
- purpose-preference
- purpose-policy
- purpose-procedure
- purpose-reference
- stability-policy-contingent
- stability-tool-contingent
- stability-environment-contingent
title: Preferred Libraries and Tools
---

Prefer tool-routing skills over memorized commands:

- Memory and agent-facing documentation: `agent-memory`
- GitHub, `gh`, commits, PRs, issues, deletion: `git-guidelines`
- Project automation and command discovery: `justfile`
- Local structure and debugging surfaces: `reality-grounded-debugging`
- External docs, Context7, DeepWiki, package/API/compiler/provider errors:
  `known-solution-first`
- Name/text discovery: `rg` and `fd`
- Semantic narrowing after broad discovery: `probe`
- Structural search and syntax-aware rewrites: `ast-grep`
- Workspace symbols/references/rename when the language server is known-good: `lsp-cli`
- Language-specific semantic rename: `gorename`, `clang-rename`, `ts-morph`, `rope`,
  or OpenRewrite
- Repeatable JavaScript/TypeScript codemods: `jscodeshift`
- JSON/YAML edits: `config-file-editing`
- Python scripts, `uv`, missing dependencies, install choices:
  `tool-provisioning-and-environment-hygiene`
- PDFs: `reading-pdfs`
- Markdown formatting and prose rewrites: `writing-clearly-and-concisely`,
  `writing-for-agent-audiences`, and the project `justfile`
- Frontend and GUI work: `design`, `responsive-design`, `developing-linux-guis`,
  `visual-regression-testing`
- Mathematical research tooling: `lattices`, `sagemath`, `lean4`, `arxiv`,
  `literature-review`
- Scheduled tasks or reminders: `scheduling-tasks-and-subagents`
- Delegated paid-model work: ask before using `gemini`, `codex`, `claude`, `qwen`, or
  `jules`; load the matching delegation skill first

When pushing text through `gh` or shell commands, avoid backticks in user-supplied
message bodies because they trigger shell escaping hazards.
