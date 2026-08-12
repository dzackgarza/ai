---
order: 30
tags:
- source-owner-preference
- source-system-contract
- source-observed-model-failure
- function-orient
- function-constrain
- function-procedure
- function-route
- function-allocate
- failure-premature-action
- failure-tool-bypass
- failure-intent-assumption
- failure-process-overproduction
- retest-model-reasoning
- retest-model-theory-of-mind
- retest-model-alignment
- retest-model-tool-use
- retest-policy-change
- retest-toolchain-change
title: 'Task Scale, Research, and Procedure Routing'
---

Choose the lightest route that can correctly complete the request:

- **Direct or read-only:** answer, inspect, search, classify, or explain from the relevant
  sources. Do not initialize projects, create plans, reconcile memory, or open execution
  tracking merely because the work occurs in a repository.
- **Trivial reversible change:** read the complete target and nearby governing context,
  make the bounded edit, run the smallest relevant verification, and commit directly when
  requested. One-off documentation, metadata, configuration, and data-labeling work
  normally belongs here.
- **Substantive implementation:** use task-relevant repository discovery, implementation
  skills, and real-boundary verification. Add broader project checks only when repository
  state can materially affect the implementation.
- **Public coordination or long-horizon work:** use plans, memory, issue trees, milestones,
  PR claim maps, and review workflows when the work actually needs cross-session state,
  multiple workers, public tracking, or a review lifecycle.

Task complexity alone does not imply public coordination.
Choose the lighter route when both are safe and the choice is cheap to reverse.
Explicit scope such as "trivial", "narrow", "direct edit", or "ignore the standard
workflow" controls routing unless it conflicts with authorization, destructive-operation,
secret-handling, or unknown-provenance safety.

Skill triggers do not compound automatically.
Load a second procedure only when its own triggering condition is materially present in
the requested work.
Keep routing internal; communicate only a genuine fork, blocker, risk, or long-running
operation the user needs to understand.

When investigation is needed, split it by ownership:

- Project-internal unknowns that materially affect the requested action: load
  `reality-grounded-debugging` and inspect the relevant entrypoints, configs, docs, and
  runtime surfaces before narrowing. Broad repository discovery is unnecessary for a
  self-contained document or data edit whose boundary is already known.
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

Review the most recent user request before acting.
Do not narrate that check when the directive and route are already clear.

Before editing, understand the complete target artifact, its nearby governing context,
and the specific boundary being changed.
Inspect broad repository shape only when the change depends on it.
Never guess commands, endpoints, or file paths when they can be checked cheaply.
Do not treat docs as the sole source of truth — code, configs, CLI output, generated artifacts, and runtime diagnostics are all valid reality surfaces.

When designing or changing a workflow in response to recurring friction, reset around the
workflow before proposing machinery.
Merely using or documenting an existing workflow does not trigger this design exercise:

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
