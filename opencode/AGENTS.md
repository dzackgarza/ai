<!-- AGENTS.md-OTP: X7K9-MNPR-QW42 -->

# Agent Guidelines

## Hard Rules

1. **Checkpoint before every edit.** `git commit` (or `git add`) the current state BEFORE editing. Verify with `git diff` after.
2. **Load applicable skills before acting.** Scan all available skills. If one applies, load it. Do not proceed until verified.
3. **Run at project start:** `serena_activate_project`, then `serena_read_memory`.
4. **Never write time estimates.** Your calibration is off by orders of magnitude.
5. **OSOT: One Source of Truth.** Any constant, hard-coded, or re-used data should be defined in one canonical place and referenced elsewhere. This includes documentation: never attempt restate a fact when you can point to the canonical source.
6. **Tests are meant to prove correctness**. Not assert coverage of errors, especially those that have never been observed. Error-path work is useless, proof-of-correctness work is essential. And mocks are not going to help you prove anything. Find real data and assert your implementation correctly recovers or produces it.

---

## OpenCode Workspace

`~/ai/opencode` is the live OpenCode config directory, symlinked into
`~/.config/opencode`. Keep runtime-discovered paths stable. Reorganize inside
the owning subtrees instead of adding new root clutter.

### Source Of Truth

- Permissions and profile composition: `scripts/manage_permissions.py`
- Config assembly: `scripts/build_config.py`
- Permission policy: `docs/PERMISSION_SPEC.md`
- Provider configs: `configs/providers/*.json`
- Agent configs: `configs/agents/*.json`
- Subagent configs: `configs/subagents/*.json`
- Plugin code: `plugins/`
- Plugin-local runtime config: `configs/local-plugins.json`

### Stable Paths

- `configs/`
- `docs/`
- `plugins/`
- `opencode.json`
- `configs/local-plugins.json`

### Canonical Pathways

- `just permissions-apply`
- `just config-build`
- `just rebuild`
- `just providers-validate`
- `just plugins-check`
- `just harness run --help`

### Layout

- `configs/providers/`: provider source files, notes, and maintenance scripts
- `configs/agents/`: primary agent definitions
- `configs/subagents/`: live subagent definitions
- `plugins/`: runtime-loaded plugins and plugin-owned utilities
- `plugins/utilities/harness/`: session automation CLI
- `scripts/`: repo-wide maintenance entrypoints
- `docs/`: policy and organization docs

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
