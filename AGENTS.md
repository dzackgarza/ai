<!-- AGENTS.md-OTP: X7K9-MNPR-QW42 -->

# Agent Guidelines

Note: there are many symlinks on this system, check the file type if you find confusing duplication. Reusable agent-facing prompts now live in the `ai-prompts` repo and are consumed by slug; `~/ai/prompts` is reserved for `local_context` overlays and repo-specific guidance.

## Hard Rules

1. **Checkpoint before every edit.** `git commit` (or `git add`) the current state BEFORE editing. Verify with `git diff` after.
2. **Load applicable skills before acting.** Scan all available skills. If one applies, load it. Do not proceed until verified.
3. **Run at project start:** `serena_activate_project`, then `serena_read_memory`.
4. **Never write time estimates.** Your calibration is off by orders of magnitude.
5. **OSOT: One Source of Truth.** Any constant, hard-coded, or re-used data should be defined in one canonical place and referenced elsewhere. This includes documentation: never attempt restate a fact when you can point to the canonical source.
6. **Tests are meant to prove correctness**. Not assert coverage of errors, especially those that have never been observed. Error-path work is useless, proof-of-correctness work is essential. And mocks are not going to help you prove anything. Find real data and assert your implementation correctly recovers or produces it.
7. **Never bury the lede**: do not produce volumes of text when there are critical issues, or bury failures in paragraphs or summaries of success. Focus on critical, oustanding issues, and clearly delineate and highlight them.
8. **Never work around failures and hide them**. User requests are highly specific and can not be substituted with semantically similar or inferred different requests. If you attempt a task and are met with failure, never work around it if it means changing the entire task to something the user didn't ask for. If failures fundamentally block the request as stated, stop and report this to the user instead of attempting to work around it, pivot to another problem or task, etc.
9. **Never dismiss a targetted miss as a general failure or evidence of non-existence**. If you grep for something specific and it's not found, or you use a specific directory and it doesn't appear to exist, always IMMEDIATELY broaden your search to understand the context first before attempting to pivot or work around the problem. Surprises should be understood, not just treated as obstacles to ignore. Files get moved, functions get renamed/moved, typos are made. Always broaden.
10. **Never insert trivial section counters in markdown**. This becomes immediately stale as soon as a new section is added, and creates MORE work as more complexity is added. Similarly, do not number lists, subsections, etc manually, ever.
11. **Never plow through important blockers**. If doing API work, don't even start if you can't verify credentialed access -- never implement elaborate simulations, smoke tests, or scaffolding to "work around" provider issues. Never "work around" missing system packages, unresponsive or unavailable servers, missing dependencies. Immediately stop to fix the gap, and if it can not be fixed by you (e.g. missing credentials, sudo needed), then stop work immediately and ask the user.

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

Never skip from "I found nothing" to "nothing exists."

---

## Tools

**Web search & browsing:**

1. **Search** → use tavily (`tavily_search` or `tavily_research`) or the custom websearch/webfetch tools from improved-webtools (no rate limits, automated parsing)
2. **Read pages** → use `read-and-fetch-webpages` skill (gh for GitHub, curl+w3m for others)

**Always use `gh` for GitHub issues/PRs** — never browse github.com directly.
Never use backticks in text pushed through gh (or any other CLI tools), since this induces shell escaping.

**Context7 (CLI):** Use for ALL library/framework/API questions. No MCP server—uses on-demand CLI calls.

```bash
# Resolve library name to ID
npx ctx7 library <name> "<query>"
# Example: npx ctx7 library react "hooks"

# Fetch documentation for a library ID
npx ctx7 docs <libraryId> "<query>"
# Example: npx ctx7 docs /facebook/react "useEffect"
```

Get API key at `context7.com/dashboard` for higher rate limits.

**DeepWiki (via mcp2cli):** Query GitHub repository documentation. No MCP server config needed—uses on-demand CLI calls. See "Custom CLI Tools" section for full docs.

**Config files (JSON/YAML):** LOAD `config-file-editing` skill before any edit.

For AST pattern matching use `ast-grep` skill; for semantic/structural discovery use `probe` skill (`npx -y @probelabs/probe`).

**Never:** touch a config without reading docs first.

**NEVER `git checkout`, `git restore`, or revert files you did not modify.** These are others' committed work. Touch only the files you changed; verify with `git diff`.

---

## Research Before Action

When there's a question of how anything works:

1. **First** → online docs (Context7 CLI: `npx ctx7 library <name> "<query>"` or `npx ctx7 docs <libraryId> "<query>"`; DeepWiki via mcp2cli — see "Custom CLI Tools" section)
2. **Then** → readmes, playbooks, examples, web docs, man pages
3. **Last resort** → CLI args, testing commands, endpoint guesswork

**Never touch a CLI, API, or SDK without thoroughly reading all available docs first.**

---

## Engineering Rules

- **Favor mature dependencies.** Do not reinvent wheels.
- **Iterate, don't replace.** Writing an entire file is rarely correct. Run `git diff` after rewrites — see what you lost. If valuable, restore it.

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

- **Before editing any JSON or YAML file: LOAD `config-file-editing` skill.** Never raw-edit config files.

---

## Git Workflow

All work is in **noisy repos** with others' uncommitted changes. **Never use `git stash`, `git checkout`, or `git restore`** — destructive in this context. Use `git add`/`git commit` for checkpoints. **For any git operation: LOAD `git-guidelines` skill.**

---

## Orientation

- **Use basic orientation tools** like `ls`, `exa`, and `tree` when starting work.
- **Read all READMEs and AGENTS.md files** encountered.

**When corrected:** LOAD `handling-corrections` skill before responding. Do not thrash, pivot, or act until you understand the scope.

---

## Opencode

**LOAD `opencode-cli` skill** before any opencode work. Never restart or blame stale cache. Use `command opencode` not the bare alias.

---

## Waking Your Own Session

After responding to a user, your actions halt immediately until you receive a new prompt. This halts continuous or long-term work — you cannot make progress on a task that requires multiple steps if no new message arrives.

**To resume work later**, use the `at` scheduler to wake your own session:

```bash
# Get current session ID via introspection tool, then schedule a chat message:
echo "npx --yes --package=git+https://github.com/dzackgarza/opencode-manager.git opx chat --session ses_XXXXXXXX --prompt 'continue the task'" | at now + 1 minute
```

This sends a new prompt to your session at a fixed time, effectively waking you up to continue work.

**When to use:**

- Multi-step tasks where you need to pause and resume later
- Waiting for external processes or scheduled events
- Long-running work that should continue after a delay

## Scheduling Tasks

Use `task-sched` to schedule persistent systemd tasks:

```bash
# Add a recurring task
task-sched add --command "opx chat --session ses_xxx --prompt 'your message'" --schedule "hourly"

# List scheduled tasks
task-sched list

# Remove a task
task-sched remove tsk_xxxxx

# Run now (manual trigger)
task-sched run tsk_xxxxx
```

For one-off tasks, use `at`:

```bash
echo "opx chat --session ses_xxx --prompt 'continue work'" | at now + 30 minutes
```

Presets: `minutely`, `hourly`, `daily`, `weekly`, or cron expressions like `0 9 * * *`.

---

## Conventions for this system

- Never store or use local secrets or inline them into any shell commands. They must be stored in ~/.envrc, trusted with `direnv allow`, and all projects should have a .envrc file that either sources ~/.envrc directly or uses the `source_up` directive.
  - Project-local envrc files should be tracked via git, and thus never store true secrets, only env vars. If a project truly needs a local secret (rare), then it should be in a gitignore .env file and the envrc file should source it.
- All projects must have centralized recipes in a justfile and be run with `just`. Always look for one and use its recipes, never bypass them.
  - In particular, all tests, type-checking, builds, publishing, etc must be routed through `just`, never run such processes or commands "manually".
- Dependencies between projects should be routed through github and use uvx/npx calls when possible, or explicitly declared as dependencies. Do not tie across file system boundaries unless absolutely necessary.
  - **Never** set env vars inline in shell commands (e.g., `MYSECRET=123 some_command`) — these are visible in the process list. Use env files or exports instead.

## Custom CLI Tools

- **Context7 (`ctx7`)** — Library/framework documentation lookup (replaces Context7 MCP server)

  ```bash
  # Search for library and get ID
  npx ctx7 library <name> "<query>"
  # Example: npx ctx7 library react "hooks"

  # Fetch docs for specific library ID
  npx ctx7 docs <libraryId> "<query>"
  # Example: npx ctx7 docs /facebook/react "useEffect"

  # Setup (OAuth + API key)
  npx ctx7 setup
  ```

  API key: `context7.com/dashboard` | Store in `~/.envrc` as `CONTEXT7_API_KEY`

- **mcp2cli** — CLI bridge for any MCP server. Use `--toon` for token-efficient output (40-60% savings on arrays).

  ```bash
  # List tools (ALWAYS use --toon for LLM consumption)
  uvx mcp2cli --mcp https://mcp.deepwiki.com/mcp --list --toon

  # Search tools
  uvx mcp2cli --mcp https://mcp.deepwiki.com/mcp --search "question" --toon

  # DeepWiki examples
  uvx mcp2cli --mcp https://mcp.deepwiki.com/mcp read-wiki-structure --repo-name facebook/react
  uvx mcp2cli --mcp https://mcp.deepwiki.com/mcp ask-question --repo-name facebook/react --question "How does useEffect work?"

  # Other MCP servers
  uvx mcp2cli --mcp-stdio "npx @modelcontextprotocol/server-filesystem /tmp" --list --toon

  # OpenAPI specs
  uvx mcp2cli --spec https://petstore3.swagger.io/api/v3/openapi.json --list --toon
  ```

- `semtools` for semantically searching expository text, e.g. `npx -y -p @llamaindex/semtools search "spectral sequence" ~/notes/Obsidian/Unsorted/*.md`
- PDF extraction: **LOAD `reading-pdfs` skill.** Use justfile recipes in `~/pdf-extraction`, not ad hoc installs.
- `open-issues` to list all outstanding open issues across synced plugin trackers. File issues on dzackgarza repos immediately when encountered. Do not file "bugs" for errors that have never actually been observed.
- For nontrivial features: work in a worktree with a branch → PR → `@codex review` → wait 3–5 min → **LOAD `git-guidelines` skill** to scan all comment surfaces correctly.
- `probe` for semantic searching — **always** `npx -y @probelabs/probe`. **LOAD `probe` skill.**

## Live User Feedback with Plannotator

Use these tools to present changes to users for real-time feedback:

- **`submit_plan`** — Present an implementation plan to the user for review, annotation, and approval before implementation.
- **`plannotator_annotate`** — Present any markdown document to the user for live annotation and corrections. Use after heavy document rewrites or additions.
- **`plannotator_review`** — Present git diff changes to the user for line-level code review.

**When to use:**

- After making significant git changes and before pushing/releasing
- After heavy document rewrites or additions
- Any time you want the user to review and annotate specific content in real-time

---

## Libraries

- `uv` for all python-related projects
- `bun` and typescript for all JS-related development
- `svelte`, `vite`, `tailwind` etc for all HTML-related development
- `pandoc` for document construction and conversions
- `docling` or `mineru` for PDF conversion (never: pdftotext, pymupdf, etc)

## PDF Storage

- PDF storage is managed in `~/pdf-extraction` with justfile recipes for extraction and conversion.
