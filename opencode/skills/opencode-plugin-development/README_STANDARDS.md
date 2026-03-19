# README Standards

Conventions and drift analysis extracted from all first-party READMEs in this repo. Use as the reference when writing or auditing plugin READMEs.

---

## Project-Wide Standards

These apply to every package in this repo, regardless of type. READMEs must reflect and document compliance with them.

### Architecture: CLI-first, thin tool and MCP layers

Every plugin must be structured in three layers, implemented in order:

```
CLI  →  Tool layer  →  MCP layer
```

- **CLI** — the core logic lives in a standalone CLI binary (or set of subcommands) that can be invoked directly from the shell, tested without an agent, and called from scripts. This is the source of truth for behavior.
- **Tool layer** — a thin OpenCode plugin that shells into the CLI. It handles schema, argument validation, and surfacing results to the agent. It contains no business logic.
- **MCP layer** — a thin FastMCP wrapper (Python) exposed as an `mcp` subcommand of the core CLI. It must not duplicate logic — it simply launches the FastMCP server.

**Consolidation Rule**: The repository must be a single Python package with a root-level `pyproject.toml`. The MCP server is not a separate project; it is a feature of the primary CLI.

The MCP layer must never re-implement what the CLI does. If the CLI changes behavior, the MCP layer inherits it automatically because it delegates to the same binary.

READMEs must reflect this layering. The `## Install` section documents the tool layer; `### MCP Installation` documents the MCP layer. The `## Dependencies` section must list the CLI binary as an external runtime dependency if it ships separately.

### justfile — standardized recipes

Every package must have a `justfile` with at minimum these recipes:

| Recipe | Purpose |
|--------|---------|
| `just install` | Install all dependencies (npm/uv/etc.) |
| `just typecheck` | Run the type checker only |
| `just test` | Run the test suite only |
| `just check` | Run `typecheck` + `test` together |

Additional recipes as needed (e.g. `just mcp-test`, `just reddit-live-verify`), but the four above are the canonical surface. All CI, documentation, and agent instructions route through `just` — never raw `bun test`, `bunx tsc`, `uv run pytest`, etc.

READMEs must only reference `just` recipes in the `## Checks` section. Direct invocation of the underlying tools is never documented.

### Environment / direnv split

Every package uses a three-layer isolation hierarchy:

| File | Purpose | Tracked in git |
|------|---------|----------------|
| **`.envrc`** | Declares env vars; calls `source_up`; **forces isolation** | **Yes** |
| **`.env`** | Secrets and machine-local overrides only | **No** |
| **`~/.envrc`** | Global secrets (API keys, credentials) | **No** |

**Rules:**
- **Inherit via `source_up`**: The local `.envrc` must start with `source_up` to pull in global secrets from `~/.envrc`.
- **Forced OpenCode Isolation**: The local `.envrc` **must** export `OPENCODE_CONFIG="$PWD/.config/opencode.json"`.
- **XDG Isolation**: The local `.envrc` **must** override `XDG` variables to a local path (e.g., `$PWD/.xdg-home`) to prevent state leakage (configs, cache, data) between projects.
    ```bash
    export XDG_CONFIG_HOME="$PWD/.xdg-home"
    export XDG_DATA_HOME="$PWD/.xdg-home"
    export XDG_CACHE_HOME="$PWD/.xdg-home"
    ```
- **Local Overrides**: Use `dotenv_if_exists .env` in the `.envrc` for machine-local secrets not in `~/.envrc`.
- **No Secrets in Git**: Never store live secrets in the tracked `.envrc`.
- **No Inline Env**: Never set env vars inline in shell commands (`SECRET=x some_command`).
- **Activation**: `direnv allow .` must be the first step in every `## Install` section and every `## Checks` section.

READMEs must document all env vars a package reads in the `## Environment Variables` table — including those that come from parent `.envrc` files.

---

---

## Semantic Standards

### Intended audience

Every plugin README serves three readers simultaneously. Write for all three without conflating them:

| Reader | Needs |
|--------|-------|
| **Agent** | Tool names, schemas, output contracts, side effects, verification methodology. Reads at runtime. |
| **Developer (user)** | Install steps, configuration, dependency chain, what must be on `PATH`. |
| **Developer (contributor)** | How to run checks, targeted test invocations, what the justfile exposes. |

Most READMEs currently collapse the agent reader into the developer reader and omit the contributor surface entirely. The Checks section serves contributor needs; the Tools/Agent Surface section serves agent needs; the Install + Environment Variables sections serve developer needs.

### The existence question

Every README must answer, in the opening description or a dedicated section: **why does this tool exist at all?** Not what it does mechanically — what gap in the existing tool landscape required it to be built.

The answer must be specific and technical, not motivational. Examples of what this looks like:

> `websearch` wraps a local SearXNG instance. It exists because agents cannot scrape Google, and delegating web search to provider APIs requires per-service API keys and exposes queries to third parties. SearXNG aggregates multiple engines without keys.

> `webfetch` exists because most webfetch implementations either summarize content (causing agents to extrapolate from partial data) or return raw HTML with display-level markup that pollutes context windows. This tool routes by domain — stripping markup for general pages, piping academic URLs through a local PDF/source archive, transcribing YouTube via Whisper — so agents receive the actual content, not a rendering artifact.

> `reminder-injection` exists because agents do not reliably recall which skills are available without explicit enumeration. Injecting semantically matched skill summaries into each user message surfaces the relevant ones without requiring the agent to remember to ask.

The opening sentence of a README is not a summary of the implementation. It is the answer to "why should this exist in the world?" If that question can't be answered clearly, the README isn't done.

### Precision: surface the invisible

Agents rely on READMEs to know what to expect. When behavior is invisible — things that happen inside the plugin, outside the agent's direct observation — the README must make it visible. Self-reporting from an agent about unexpected behavior is notoriously unreliable. The README is the ground truth.

Document exactly:
- What the tool description looks like at runtime (if it is dynamic — e.g., subagent list appended at startup — say so and show the structure)
- What gets injected into the session by hook plugins (show the literal shape of the injected text, not just "injects skill summaries")
- What side effects occur on every call (files written, git commits made, external processes spawned)
- What happens on failure (is the error surfaced in the tool output? does the plugin swallow it? does it propagate to the session?)
- Exact defaults for every env var, not "configurable" or "optional"

Vague gestures at behavior force agents to experiment and self-report. That is not acceptable for tooling that is supposed to be reliable.

**Do not document:**
- Internal build processes, CI pipelines, or release automation (semantic-release, GitHub Actions workflows, automated test runs on push)
- Internal quality metrics (test counts, coverage percentages, "zero-knowledge UUID proof" — these are testing infrastructure, not behavioral contract)
- Internal testing methodology (passphrase-based liveness proofs are a CI concern, not a README concern)

### Tone: declarative, not instructional

Prose descriptions must be **declarative** — stating what a tool or plugin does, not teaching the reader how to think about it.

```
✓  "This plugin stores a hierarchical todo tree for each session."
✗  "Use this plugin to store todos for complex work."

✓  "Writes a Markdown transcript file to the session state directory on each completed task call."
✗  "The plugin will write a file that you can use to review what happened."
```

Imperative mood appears only inside code blocks and numbered install steps, never in prose descriptions of behavior.

Do not use motivational or marketing framing ("powerful", "flexible", "easy to use"). Do not present features as achievements ("supports X", "includes Y"). State the behavior and let the reader evaluate it. A feature list is a capability spec, not a promotional section.

The README is for technical readers. It does not need to sell the tool, explain why someone might want it generally, or walk through introductory concepts. It answers: what does this do, exactly, and what must be true for it to do that?

### Plain-text readability

READMEs are consumed in many non-browser contexts: agent reads, `cat`, grep, search indexers, LLM context windows, CLI pagers. Any content that only works in a rendered GitHub browser view fails these contexts.

Images, demo GIFs, and screenshot tables are not primary content. If a section conveys nothing when images do not render, it is not documentation — it is decoration. Do not use images as the primary vehicle for explaining behavior. State the behavior in text.

This includes demo tables (a two-column grid of screenshots renders as an empty table in text), video links ("Watch Demo"), and badge-heavy headers. These may coexist with real content but must never substitute for it.

### No ephemeral external links

Do not link to tweets, social media posts, or "New:" callouts pointing to external announcements. These rot on the timescale of months. If something is worth communicating, state it in the README directly. If it is not worth stating in the README, it does not belong there.

This includes marketing-style "New:" callouts in the body of the README. News belongs in a CHANGELOG, not in the documentation.

### Theory of mind: write for the reader's mental model, not the author's

Every sentence in a README must be there because a reader — who knows nothing about the internals — would need it to understand the tool. Not because the author knows it, finds it interesting, or wants to establish credibility.

The test for every paragraph: what specific question does this resolve for a reader who has read everything above it? If the answer is unclear, the paragraph does not belong, or it belongs earlier.

The most common failure is writing from the author's vantage point: the author already has the mental model, so they add claims and details that only make sense if you already have that model. A reader encountering "end-to-end encrypted short link service" has no frame of reference for what is being encrypted, what the link links to, who operates the service, or why any of this is relevant — because the architecture was never established.

**Establish the mental model before adding detail.** The sequence must be:

1. What processes exist, where they run, and who operates them
2. What the information flow between them is
3. Behavioral claims and contracts, now that the reader can evaluate them
4. Configuration, now that the reader knows what they are configuring

Detail presented before the mental model is established is noise. The reader cannot evaluate it, file it, or act on it.

**Every feature must answer its prerequisite questions first.** For any non-trivial feature, ask: what does the reader need to understand before this feature makes sense? Document those prerequisites first. For a sharing feature: How does a collaborator receive the content? Do they need an account? Do they connect to your machine directly or through a relay? How does their feedback return to you? What is the information passing model? These are not details — they are the feature. If they are not answered, the feature is not documented.

### Name every component that appears in a claim

Before making any behavioral or trust claim, the README must have established exactly what entity the claim applies to. "The server", "the backend", "the service" are undefined until the architecture has been described — and in tools that run a local process, "the server" is the user's own machine, which makes security claims about it nonsensical.

If a tool has both a local component and a remote component, name them distinctly and consistently throughout. A claim like "the server cannot read your data" requires the reader to already know which server is meant, where it runs, and who operates it. Without that, the claim is not just vague — it may actively contradict the evident architecture.

Before writing any claim about a component, ask: has this component been named and its trust boundary defined? If not, define it first.

### Contracts, not trust signals

Security, privacy, and reliability claims must be stated as what the reader can rely on (the contract), not as how they are achieved (the implementation).

```
✓  "The server cannot read plan content — only ciphertext is stored."
✗  "End-to-end encryption using AES-256-GCM. Zero-knowledge storage."
```

The mechanism is an internal detail. The guarantee is the contract. State the guarantee; omit the mechanism unless it is directly relevant to how the reader configures or uses the tool.

### What to surface: behavioral contracts, not implementation

A README documents the **external contract** of a package — what it exposes, what it returns, what side effects it has, and what it requires. It does not document how those things are implemented internally.

**Always document:**
- Tool names and parameter schemas (every field, type, required/optional)
- Output contract — exact structure of what the tool returns (section names, YAML keys, field names)
- Side effects — files written, external services called, state mutated
- What the plugin owns vs. what the host (OpenCode) owns (acceptance boundaries)
- What the proof/verification methodology can and cannot prove
- Every env var the package reads, including those with defaults

**Do not document in the README:**
- Internal architecture or implementation details (those belong in AGENTS.md or code comments)
- Why the implementation was designed a particular way (belongs in commit messages or ADRs)
- Tutorial-style "How It Works" walkthroughs — if a developer needs to understand internals, they read the code
- Step-by-step conceptual explanations of standard patterns (e.g. explaining what a passphrase is)
- Anything about the build system, CI, release process, or internal test infrastructure
- Qualitative claims about internal quality ("robust", "reliable", "production-ready")

The test: if removing a paragraph would leave the behavioral contract fully specified, remove it.

### Output contract documentation

For every tool that returns structured output, the README must document the return structure explicitly — not just "returns a report" but the actual section names, YAML keys, and field names a caller can rely on.

Example from improved-task (correct):
```
Successful sync completion returns a markdown report with YAML front matter:
- `session_id`
- `tokens_used`
...
The report body is organized into these sections:
- `## Agent's Last Message`
- `## Turn-by-Turn Summary`
- `## Completion Review`
```

This level of specificity is what distinguishes a contract from a description.

### Side effects and acceptance boundaries

Every plugin must explicitly state:
- What it writes (files, database rows, git commits)
- What external services it calls beyond the configured OpenCode server
- What it is responsible for vs. what the host system (OpenCode, the shell) owns

Example from improved-task (correct):
```
Actual TUI rendering remains a manual acceptance boundary. The plugin owns the
shadowing and session/report contract; OpenCode owns how that contract is rendered
in the interface.
```

This tells the agent reader precisely what to test and what to accept as given.

### Hook plugins vs. tool plugins

Plugins that use `chat.message` hooks instead of exposing named tools must use `## Agent Surface` (not `## Tools`) and document the processing pipeline — what the hook reads, what it does, and what it injects — in behavioral terms.

The processing pipeline for a hook is its contract. Document it step by step (scan → embed → inject) because an agent reader needs to understand what will happen to their messages, even though no tool call is involved.

### Storage and artifact plugins

For plugins whose primary output is a persistent artifact (files, database records), the README must document the artifact format as part of the contract:
- File format / schema
- Directory structure and naming conventions
- How to inspect or search the artifacts directly (outside the plugin)

This is appropriate because the artifacts are part of the user-visible contract, not an implementation detail. See postgres-memory-plugin for the correct pattern.

### What does not belong

| Content | Where it belongs instead |
|---------|--------------------------|
| "How It Works" internals | AGENTS.md or code comments |
| Implementation rationale ("we chose X because Y") | Commit message, ADR |
| Version history, changelogs | CHANGELOG.md |
| Release process mechanics | CHANGELOG.md or a separate RELEASING.md |
| CI pipeline details (semantic-release, automated publishing) | CI config files |
| Internal test infrastructure (passphrase proofs, liveness checks) | Test files and AGENTS.md |
| Build system details beyond `just check` | justfile |
| Active worktree paths, session IDs | WORKTREES.md or session notes |
| License (unless actively enforced) | `package.json` / `pyproject.toml` `license` field only |
| Conventional commits guide | Link to spec, not reproduced inline |
| Feature counts, test pass counts, coverage metrics | Nowhere — not relevant to readers |

### Platform target

All tooling targets Linux/Unix only. Do not document macOS or Windows alternatives, workarounds, or caveats. Do not add `brew install` steps, Windows path syntax, or platform-conditional instructions. If a tool does not work on a given platform, that platform is out of scope, not a gap to document.

### Configuration, not installation

Plugins and MCP servers are **configured**, not installed. The host harness (OpenCode, the MCP client) resolves and loads them from the configuration entry — there is no separate install step for the end user.

READMEs must never instruct users to:
- `npm install` a plugin
- `clone` the repository to use it
- Run any setup command before adding the config entry

The correct framing is "add this to your configuration":

```
✓  "Add to your OpenCode configuration:"
✗  "Install the plugin:"
✗  "Clone the repo and run just install"
```

The `## Install` section heading (and its content) applies only to **contributors** setting up a local development environment. For end users, the section is `## Configuration` — showing the JSON snippet they drop into their config file, and nothing else.

This distinction must be clear in the README structure. If the README has both audiences, separate them explicitly:

```markdown
## Configuration

Add to your OpenCode config:

```json
{ "plugin": ["@dzackgarza/..."] }
```

## Development Setup

For contributors working on the plugin locally:

```bash
direnv allow .
just install
```
```

The `just install` / `direnv allow` steps never appear in the user-facing configuration section.

### No-install usage and drop-in agent commands

Prefer `uvx` and `npx` for immediate, dependency-free usage. The goal is that an agent or developer can drop a single command into an AGENTS.md file or shell and have the tool work with no prior setup:

```bash
uvx --from git+https://github.com/dzackgarza/<repo> <entrypoint> --help
npx --yes --package=git+https://github.com/dzackgarza/<repo> <entrypoint> --help
```

The README must include the canonical no-install invocation for every tool that supports it. This is the primary install surface for agents. The `just install` path is for contributors and local development, not the first-class usage pattern.

### Direct CLI bypass

If a plugin or MCP server wraps an underlying CLI tool, the README must document how to call the CLI directly, bypassing the plugin entirely. This serves two purposes:
- Agents can use the tool without OpenCode running
- Developers can debug the CLI layer in isolation from the plugin layer

The bypass invocation must appear in the README as a concrete command, not a pointer to another README or "see the CLI docs." It is part of the behavioral contract.

### Progressive disclosure via Typer subcommands

CLI interfaces must use [Typer](https://typer.tiangolo.com/) with subcommands, structured for progressive discovery:

- `--help` at the top level lists available subcommands with one-line descriptions
- Each subcommand has its own `--help` with full parameter docs
- Agents discover functionality incrementally through help text, minimizing token usage
- Do not expose every option at the top level; bury deviation-from-happy-path options in subcommands

READMEs must not reproduce the full `--help` output. Instead, document the intended workflows (the happy path) and name the subcommands an agent would use for off-path operations. The help text is the spec for parameters; the README is the spec for when to use each subcommand and why.

### Opinionated workflows, not fine-grained control

The public interface exposes opinionated workflows with sane defaults. It does not expose every internal knob. Agents should not need to think about implementation details to accomplish the common case.

Structure:
- **Top-level subcommands** — happy-path workflows. Minimal flags. The agent calls these and gets a result.
- **Deep subcommands** (e.g. `debug`, `advanced`, `inspect`) — deviation paths for when the happy path fails or an operator needs visibility into internals. These exist but are not the default discovery surface.

The README documents the top-level workflows in full. Deep subcommands are acknowledged ("see `<tool> debug --help` for low-level diagnostics") but not enumerated, to avoid agents being distracted by internals when the happy path works.

### Licensing

Every README must include a `## License` section at the bottom. All packages in this repo are MIT:

```markdown
## License

MIT
```

Do not link to a LICENSE file. Do not reproduce the full license text. The one-liner is sufficient and consistent across all packages.

### GitHub repository descriptions

Every repository must have a GitHub description set — the one-line summary that appears on the repo page and in search results. This is not in the README but is documented here as a standard because it must be kept in sync with the README's one-line description.

The GitHub description must be:
- The same sentence as the one-line description under the H1 in the README
- No longer than ~120 characters
- No trailing period

When updating a README's one-line description, update the GitHub repo description to match.

---

## Canonical Section Order

```
<ko-fi badge>
# <short-name>
<one-line description + existence justification>

## Configuration
  ### MCP Configuration   (if applicable)
## Tools   OR   ## Agent Surface   (if no tool names exposed)
  ### `tool_name`
    #### Input
    #### Example Input
## Environment Variables
## Dependencies
## Development Setup   (contributors only)
## Checks             (contributors only)
## License
```

Optional sections (append after Checks if needed):
- `## Release Process`
- `## Breaking Changes`
- Deprecation notice — goes before H1 if applicable (see below)

---

## Rules

### Ko-fi badge

Always line 1, before everything else:

```markdown
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/I2I57UKJ8)
```

No blank line between badge and H1.

**Currently missing from:** improved-webtools (main), improved-webtools/mcp-server, zotero-plugin, task-sched.

### H1 title

Use the short kebab-case name — not the full package name, not title case, not backtick-quoted:

```markdown
# improved-task       ✓
# opencode-plugin-prompt-transformer   ✗  (full package name)
# Improved Web Tools                   ✗  (title case)
# `opencode-plugin-mcp-shim`           ✗  (backtick in H1)
```

### One-line description

Immediately after H1. State what it shadows or exposes in one sentence. No blank line between H1 and description.

### Section headings — use these exact names

| Concept | Correct heading |
|---------|----------------|
| Config snippet for end users | `## Configuration` |
| Local dev setup for contributors | `## Development Setup` |
| Tool listing (tools exposed to agent) | `## Tools` |
| Hook-only plugins (no tool names) | `## Agent Surface` |
| Internal-only packages | `## Public Interface` |
| Runtime dependencies | `## Dependencies` |
| Runtime environment knobs | `## Environment Variables` |
| How to run checks | `## Checks` |

Do not use: `## Install`, `## Installation`, `## Tool Names`, `## Requirements`, `## Development`, `## Validation`.

`## Configuration` is for end users (the config JSON snippet). `## Development Setup` is for contributors (`direnv allow`, `just install`). Never merge them into a single `## Install` section.

### Install section

```markdown
## Install

```bash
cd ./<short-name>
direnv allow .
just install
```

Register in OpenCode:

```json
{
  "plugin": [
    "@dzackgarza/<package-name>@git+https://github.com/dzackgarza/opencode-plugins#subdirectory=<dir>"
  ]
}
```
```

Always include `direnv allow .`. Do not omit it.

If the plugin also ships an MCP wrapper, add a `### MCP Installation` subsection:

```markdown
### MCP Configuration

Add to any MCP client config:

```json
{
  "mcpServers": {
    "<slug>": {
      "command": "uvx",
      "args": [
        "--from", "git+https://github.com/dzackgarza/opencode-plugins.git",
        "<entrypoint>",
        "mcp"
      ]
    }
  }
}
```
```

### Tool parameter tables

Use a markdown table with exactly these columns:

```markdown
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string` | Yes | ... |
| `mode` | `"sync" \| "async"` | No | ... |
```

Do not use prose bullet lists (`- \`url\`: (string) ...`) or plaintext code blocks for parameter docs.

Nested types go in a sub-table immediately below the parent table, labeled with the type name in bold:

```markdown
**`TodoTreeNode`:**

| Field | Type | Description |
|-------|------|-------------|
```

Always follow the parameter table with an `#### Example Input` fenced JSON block.

### Environment variables table

Four columns, always in this order:

```markdown
| Name | Required | Default | Controls |
|------|----------|---------|---------|
| `VAR_NAME` | Yes | — | What it controls |
| `VAR_NAME` | No | `fallback` | What it controls |
```

- Use `—` (em dash) for no default.
- Every plugin with integration tests exposes a `<PLUGIN>_TEST_PASSPHRASE` variable (`Required: No`, `Default: —`).

Do not reduce to 2-column `Variable | Description` — the Required and Default columns carry meaning.

### Checks section

```markdown
## Checks

```bash
direnv allow .
just check
```

For targeted runs, use the canonical `justfile` entrypoints:

```bash
just typecheck
just test
just test-file tests/path/to/file.ts 'test name'
```

Do not run `bun test`, `bunx tsc`, or `uv run pytest` directly.
```

The warning against direct invocation must appear in every plugin. It is missing from most READMEs today.

### Deprecation notice

If a package is deprecated, use a GitHub-flavored callout placed **before the H1** (and before the Ko-fi badge if the package is fully retired):

```markdown
> [!WARNING]
> **Deprecated** — Replaced by:
>
> - One-off: `...`
> - Recurring: `...`
> - See [replacement-package](link)

# <short-name>
```

Only time-travel-plugin currently does this correctly.

### Root README

The root `README.md` is an index only. It must contain:
- Ko-fi badge
- H1 `# OpenCode Plugins`
- Bulleted plugin list with relative links to each plugin's README
- Brief description per plugin (one clause)

It must **not** contain:
- Active worktree paths
- Session IDs or Codex migration state
- Any ephemeral operational data

Operational state (worktrees, session IDs) belongs in session notes or a separate `WORKTREES.md`, not the index.

---

## Compliance Gaps (as of audit)

| Repo | Issues |
|------|--------|
| `zotero-plugin` | Nearly empty — missing Features, Tools, Environment Variables, Dependencies, Checks |
| `reminder-injection` | Missing Install, Checks, Dependencies sections |
| `task-sched` | Missing Features, Environment Variables; no Ko-fi badge |
| `improved-webtools` | Missing Ko-fi badge; uses bullet lists instead of tables for tool params; uses `## Installation`, `## Development` |
| `improved-webtools/mcp-server` | Missing Ko-fi badge; uses code-block format for tool params |
| `improved-todowrite/mcp-server` | Uses code-block format for tool params |
| `mcp-shim` | Uses `## Installation`, `## Requirements`, `## Validation` instead of canonical names; H1 uses backtick-quoted name |
| `prompt-transformer` | H1 uses full package name instead of short name |
| `reminder-injection` | H1 uses full package name; extra blank line after badge |
| `opencode-manager` | H1 uses backtick-quoted name |
| `time-travel-plugin` | Uses `## Usage` for install; bullet lists for tool params; H1 uses full package name |
| `postgres-memory-plugin` | `## Configuration` instead of `## Environment Variables`; dependency table uses non-standard columns |
| Root `README.md` | Contains worktree paths and Codex session IDs (ephemeral operational state) |
