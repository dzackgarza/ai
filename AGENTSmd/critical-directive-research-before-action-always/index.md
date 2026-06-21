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
- Semantic code search after broad discovery: load `probe` or `ast-grep`.

**BEFORE TAKING ANY ACTION**: review the most immediately recent user requests, and verbally confirm whether or not the actions you are planning actually align with the directive.
User directives are highly specific, not suggestions.
Verbally confirm what the user's stated directive was, your planned action, and why the goal you're pursuing is the exact goal the user stated.

Never make an edit without first understanding the repo's shape and the specific boundary you are about to change.
Never guess commands, endpoints, or file paths without running them first.
Do not treat docs as the sole source of truth — code, configs, CLI output, generated artifacts, and runtime diagnostics are all valid reality surfaces.
