<!-- AGENTS.md-OTP: X7K9-MNPR-QW42 -->

# Agent Guidelines

NEVER EDIT opencode.json directly! Read the justfile!

## OpenCode Workspace

`~/ai/opencode` is the live OpenCode config directory, symlinked into
`~/.config/opencode`. Keep runtime-discovered paths stable. Reorganize inside
the owning subtrees instead of adding new root clutter.

### Source Of Truth

- Managed markdown-agent generation: `../justfile` `build-agents`
- Config assembly: `scripts/build_config.py`
- Canonical prompt templating: `llm-templating-engine` (installed in `.venv` via `pyproject.toml`)
- Canonical template-driven LLM execution: `llm-run` (installed in `.venv` via `pyproject.toml` and exposed locally through `just run-microagent`)
- Provider configs: `configs/providers/*.json`
- Managed agent prompt slugs: resolved through the `ai-prompts` dependency
- Generated OpenCode markdown agents: `agents/*.md`
- Plugin code: `plugins/`
- Plugin-local runtime config: `configs/local-plugins.json`

### Stable Paths

- `configs/`
- `docs/`
- `plugins/`
- `opencode.json`
- `configs/local-plugins.json`

### Canonical Pathways

- `just build-agents`
- `just build-config`
- `just build`
- `just providers-validate`
- `just check-plugins`
- `just opencode-harness run --help`

### Layout

- `configs/providers/`: provider source files, notes, and maintenance scripts
- `agents/`: generated OpenCode markdown agents consumed at runtime
- `ai-prompts`: canonical prompt library, resolved by slug through `pyproject.toml`
- `plugins/`: runtime-loaded plugins and plugin-owned utilities
- `plugins/utilities/harness/`: compatibility wrapper/docs for the extracted session automation CLI
- `scripts/`: repo-wide maintenance entrypoints
- `docs/`: policy and organization docs

### Prompt Templating

- All prompt rendering is centralized in `llm-templating-engine`. Do not reimplement prompt parsing, frontmatter handling, Jinja rendering, or include semantics inside repo-local helper code, plugins, or ad hoc scripts.
- `ai-prompts` is the canonical prompt source. Callers in this repo resolve prompt slugs through the dependency instead of reading workspace-local prompt files.
- Prompt templates are markdown files with YAML frontmatter. The templating engine preserves frontmatter; runner-reserved execution fields such as `kind`, `models`, `system_template`, `temperature`, `max_tokens`, `retries`, `output_schema`, and `response_template` belong to `llm-runner`.
- Jinja `{% include %}` and `{% import %}` are supported through the canonical `llm-templating-engine` environment. Included prompt templates contribute only their markdown body. Child frontmatter is ignored by design.
- If a new use case needs different prompt composition or LLM execution semantics, extend `llm-templating-engine` or `llm-runner` rather than adding a repo-local second path. Verify there are no regressions for both template-defined runs (`llm-run` or `just run-microagent`) and managed agent generation (`just build-agents`).

### Build Behavior

- `just build-agents` is the canonical full build for managed agents. It:
  1. Fetches published `ai-prompts` prompt slugs via `uvx`
  2. Pipes each markdown prompt through `opencode-permission-policy-compiler`
  3. Writes the resulting OpenCode agent markdown into `agents/*.md`
- `just build-config` rebuilds `opencode.json` through `scripts/build_config.py` while ignoring any skeleton-level `permission` block, then applies the global permission baseline via `opencode-permission-policy-compiler set-global-policy global`
- The permission-policy definition lives in `configs/opencode-permission-policy-compiler/config.toml`, and `just install` symlinks that repo directory into the XDG config location consumed by `opencode-permission-policy-compiler`.
- `just build` runs the full repo-level flow (`check-plugins`, `build-config`, `build-agents`, `build-agents-md`)
- The builder also counts tokens for fully rendered prompts and warns when any generated agent exceeds the configured threshold (`OPENCODE_AGENT_TOKEN_WARNING_THRESHOLD`, default `5000`).

### Permission Ownership

- This repo does not own a local permission compiler implementation.
- The global permission-policy definition lives in `configs/opencode-permission-policy-compiler/config.toml`.
- Managed agent permission overlays are compiled by the external `opencode-permission-policy-compiler`.
- `just install` symlinks that repo policy directory into `~/.config/opencode-permission-policy-compiler` for the external compiler.
- Use `/*` suffixes for `external_directory` permission paths. The current OpenCode runtime asks for approvals using derived directory globs like `/path/to/dir/*`, so bare directory entries do not match those prompts.

---

## Epistemic Integrity

Absence of evidence is not evidence of absence. Do not extrapolate failures to find or know to assertions of impossibility or non-existence. E.g. integers exist, but you will never find them by throwing darts at the real line.


**When reporting that something was _not_ found, use this format:**

```
- Searched: [specific sources, URLs, docs, commands run]
- Found: [what was or was not found]
- Conclusion: [labeled as inference — "I believe", "based on limited evidence"]
- Confidence: [High / Medium / Low]
- Gaps: [what remains unsearched]
```

When the search space is small and an epistemic conclusion is necessary, just be exhaustive and broad. 15 greps for specific (guessed) keywords can be less efficient than a simple 'ls' or 'tree'. use this as an aphorism for repeated depth-focused searches compared to fewer breadth-focused searches.

Omitting any field is a rule violation.

| Wrong                           | Correct                                                 |
| ------------------------------- | ------------------------------------------------------- |
| "There's no endpoint for X"     | "I found no documented endpoint for X in [sources]"     |
| "X doesn't exist"               | "I found no evidence of X in [sources]"                 |
| "This feature is not supported" | "I found no documentation of this feature in [sources]" |

**Self-check before every response containing a negative finding:**

1. Did I search, or am I assuming?
2. Did I report what I searched, or claim universal knowledge?
3. Did I label my conclusion as inference?
4. Did I fill in all five fields above?

Never skip from "I found nothing" to "nothing exists."

---

## Tools

**Web search & browsing:**

1. **Search** → use tavily (`tavily_search` or `tavily_research`)
2. **Read pages** → use `read-and-fetch-webpages` skill (gh for GitHub, curl+w3m for others)

**Always use `gh` for GitHub issues/PRs** - never browse github.com directly.

**Context7:** Use for ALL library/framework/API questions. `context7_resolve-library-id` → `context7_query-docs`.

**Edits:**

Use `edit` for all code edits.

**Search:**

| Question              | Tool       |
| --------------------- | ---------- |
| Text/grep pattern?    | `grep`     |
| AST pattern matching? | `ast-grep` |

Grep examples: `pattern="fileAppeal"`, `pattern="class.*Service"`.

**ast-grep:** Use for structural code patterns (function definitions, class hierarchies, import statements, etc.).

---

## Research Before Action

When there's a question of how anything works:

1. **First** → online docs (Context7 for libraries/frameworks/APIs)
2. **Then** → readmes, playbooks, examples, web docs, man pages
3. **Last resort** → CLI args, testing commands, endpoint guesswork

**Never touch a CLI, API, or SDK without thoroughly reading all available docs first.**

---

## Engineering Rules

- **Favor mature dependencies.** Do not reinvent wheels.
- **Iterate, don't replace.** Edit existing files. Writing an entire file is rarely correct. Run `git diff` after rewrites — see what you lost. If valuable, restore it.

---

## Memory

Memories store durable, reusable agent context not captured in repository files.

**Store:** Stable operational guidance, environment quirks, cross-session execution context.

**Do not store:** Audit trails, decision logs, changelogs, work summaries. Those belong in git.

---

## Chat Responses After Completing Work

Do not summarize what was done. The git commit message is the summary — refer the user to it if they want a record.

**Chat output after a task should contain only:**

- Items NOT completed and why
- Gaps or open questions identified during the work
- Errors or surprises that were skipped and need revisiting
- Decisions made during the process that may need user review
- Next actions, if any

If none of the above apply, a one-line confirmation is sufficient. A changelog in chat is noise.

## Lattices

Note that `lattice` does NOT mean lattices related to cryptography in any meaningful sense.
A lattice, by definition, is a free $R$-module of finite rank with a (usually nondegenerate) symmetric bilinear form.
This may be definite or indefinite, and is NOT assumed to be positive-definite, embedding in a particular vector space, to have a "basis", to be unimodular, etc.

---

## Anchor: Epistemic Integrity (Restated)

When you find no evidence of something, you MUST use the five-field format from the Epistemic Integrity section above. Every negative finding requires: Searched, Found, Conclusion (labeled as inference), Confidence, Gaps. No exceptions.

---

## Config File Handling

- **Use `jq` for JSON and `yq` for YAML** when reading or querying config files. Never manually parse with grep/head/tail.

- **Never edit JSON or YAML files directly** with edit/patch tools. Instead, use this pattern:
  1. Read the file into a Python script
  2. Parse as JSON/YAML
  3. Modify the object in memory
  4. Dump back as pretty-printed JSON/YAML

  This prevents indentation issues and syntax errors entirely.

---

## Git Workflow

All work is done in **noisy git repos** with uncommitted changes from others.

- **Never use `git stash`, `git checkout`, or `git restore`.** These operations are destructive and conflict with checkpoint-based workflow.
- **Always use `git add` and `git commit`** to create checkpoints of your specific changes.
- Commits are **save-states**, not atomic units of work. It's fine if your commit includes others' uncommitted changes — the point is to checkpoint *your* work.
- If you need to see what changed, use `git diff`. If you need to verify what's staged, use `git diff --cached`.

---

## Orientation

- **Use basic orientation tools** like `ls`, `exa`, and `tree` when starting work.
- **Read all READMEs and AGENTS.md files** encountered.
