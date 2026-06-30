---
order: 30
title: 'Critical Directive: Research Before Action, Always'
---

Split by ownership before investigating.

- Project-internal unknowns: load `reality-grounded-debugging`, start with `tree`, and
  inspect declared entrypoints, configs, docs, and runtime surfaces before narrowing.
- External tools, compilers, libraries, APIs, package managers, providers, exact errors,
  and dependency choices: load `known-solution-first` before local probing.
- Project automation and validation commands: load `justfile` and use declared recipes
  when they exist.
- Semantic code work after broad discovery: route to explicit CLI tools by operation.

CLI routing for code navigation and edits:

- Name/text discovery: use `rg` and `fd`.
- Semantic narrowing after broad discovery: use `probe`.
- Structural search or syntax-aware rewrites: use `ast-grep`.
- Workspace symbols, references, definitions, and rename through a known-good language
  server: use `lsp-cli`.
- Language-specific semantic rename: use `gorename` for Go, `clang-rename` for C/C++,
  `ts-morph` for TypeScript/JavaScript, `rope` for Python, and OpenRewrite for Java/JVM.
- Repeatable JavaScript/TypeScript codemods: use `jscodeshift`.
- If the language server, project registration, or symbol index is not already working,
  do not spend task budget repairing it unless the user asked for that setup; use the
  explicit CLI route above or ordinary file edits instead.

**BEFORE TAKING ANY ACTION**: review the most immediately recent user requests, and verbally confirm whether or not the actions you are planning actually align with the directive.
User directives are highly specific, not suggestions.
Verbally confirm what the user's stated directive was, your planned action, and why the goal you're pursuing is the exact goal the user stated.

Never make an edit without first understanding the repo's shape and the specific boundary you are about to change.
Never guess commands, endpoints, or file paths without running them first.
Do not treat docs as the sole source of truth — code, configs, CLI output, generated artifacts, and runtime diagnostics are all valid reality surfaces.

When a request names an existing workflow or recurring friction, reset around the workflow
before proposing machinery:

- State the user gesture, the object being acted on, the existing substrate, and the
  smallest boundary that can intercept or observe it.
- Separate capture-time facts from later enrichment, review, cataloging, or citation work.
- Name the owner system before and after each handoff.
- Keep technical proof attributes out of user-facing identity or organization unless the
  workflow actually needs a content-addressed store.
- Prefer native substrate: browser or extension hooks before helper apps, identifier lookup
  before manual metadata, collection or membership state before new statuses, and
  artifact-native metadata before external sidecars.
- Do not add logs, queues, lifecycle states, managers, or sidecars until the native owner,
  available facts, and required state transition are known.
