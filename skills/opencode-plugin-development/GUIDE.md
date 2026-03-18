<!-- AGENTS.md-OTP: X7K9-MNPR-QW42 -->

# OpenCode Plugin Development

This is the shared development guide for repos under `/home/dzack/opencode-plugins`.

- `GUIDE.md` tells you how to start and work.
- `AUDIT.md` tells you how to evaluate completed work.
- If guidance applies to every repo, keep it in this skill or in `AUDIT.md`. Package-local
  docs should describe package-specific behavior only.

## Navigation

- Use this file for setup, repo-local workflow rules, proof design, and implementation
  conventions.
- Use `AUDIT.md` for the post-hoc compliance rubric before pushing or opening a PR.
- Use `opencode-cli/SKILL.md` for the global OpenCode config model, basic CLI commands,
  and manager command syntax.
- Use `opencode-cli/PLUGINS.md` when you need event, hook, or plugin SDK reference
  details.
- Use `opencode-cli/async-injection.md` when you need callback, background task, or
  delayed-delivery patterns.

## Orientation

- Each subdirectory is its own repo/package.
- The top-level `/home/dzack/opencode-plugins` repo stores shared policy/docs. Use it for
  shared guidance only; do package work in the relevant package repo.
- `~/ai/opencode/plugins/` is a separate workspace. Do not change it from here unless the task is explicitly about that workspace.
- Many paths on this system are symlinks. Check file type before assuming two paths are different files.
- Document env vars in a tracked local `.envrc` and in the package README. Tracked `.envrc`
  files should use `source_up` and `dotenv_if_exists .env` and must never contain live
  secrets.

## Shared Policy Surface

- Shared policy lives only in top-level `AGENTS.md` and `REPO_AUDIT.md`, both sourced
  from this skill.
- Package-local docs stay package-specific. Do not restate shared policy unless the
  package has a real exception.
- Do not create top-level `GAPS.md`, `PLAN.md`, `TODO.md`, `DEBUGGING.md`, or shadow
  audit docs.

## Before Editing

- Work in the relevant repo. Use the top-level repo only for shared policy/docs.
- Checkpoint before every edit with `git add <file>` or a commit.
- Use the repo's lowercase `justfile`. Do not run test, typecheck, build, or publish commands directly if a `just` recipe exists.
- Run `direnv allow` when the repo has a local `.envrc`.
- Read the repo's `README.md` and local docs before changing behavior.
- Do not use destructive git commands such as `git checkout`, `git restore`, `git reset --hard`, or `git stash` in noisy repos.
- Keep one source of truth for repeated constants, config values, and shared policy text.

## Research and Tooling

- Use official docs first. For libraries/frameworks/APIs, use Context7 before guessing from CLI flags or source alone.
- Use `gh` for GitHub work, not github.com.
- Use `probe` for repo discovery and structural search.
- Load config-editing guidance before touching JSON or YAML.
- Use `command opencode` only when bypassing a shell alias matters.
- If a narrow search misses, broaden immediately before concluding anything is absent.

## CLI-First Architecture

- The default architecture for plugin repos is: independent core logic, standalone Typer CLI, thin OpenCode adapter, then optional thin MCP adapter.
- Put storage, parsing, validation, network access, provider integration, and reporting into code that can run without OpenCode loaded.
- Limit plugin code to the parts that truly require OpenCode internals: session wiring, permission prompts, event publication, metadata/title updates, and hook-specific message mutation.
- A plugin tool should call the canonical CLI or its shared library entrypoint. It must not carry a second implementation of the same behavior.
- Hook-only plugins still need an independent CLI for the underlying operation. For example: classify, render, index, match, schedule, dispatch, or doctor.
- In plugin repos, the primary user-facing CLI should be written with Typer and structured around commands and subcommands with progressive-disclosure help.
- CLI help must be useful on its own: `--help` works, `no_args_is_help` is enabled where appropriate, subcommands expose focused help, and setup requirements appear before internal details.
- Package the CLI so it is runnable with `uvx` or `npx` when practical. If a repo cannot yet support one of those paths, treat that as an explicit migration gap, not an implicit exception.
- When config, credentials, databases, or local services are required, assume standard global env/config sources such as `~/.envrc` or the provider's normal credential files. Fail fast with clear setup messages that name the missing prerequisite and how to supply it.
- README and package docs should present the standalone CLI first. OpenCode plugin registration, hook wiring, and MCP registration come after the independent command surface.
- Keep one canonical request/response contract across the CLI, plugin wrapper, and MCP wrapper whenever possible.

## OpenCode Config and Registration

- Never edit `~/ai/opencode/opencode.json` directly. The source of truth is
  `~/ai/opencode/configs/config_skeleton.json`; rebuild from `~/ai/opencode/` with
  `just rebuild`.
- Do not run `just rebuild` while inside an active OpenCode session; it restarts the
  managed server and kills that session.
- Register plugins in OpenCode via the `plugin` array using an npm package, a
  `name@git+https://...` alias, or a `file:///abs/path/to/src/index.ts` entry.
- For git-backed plugin installs, the alias before `@` must match the package `name`
  from `package.json`.
- Bun caches installed npm plugins under `~/.cache/opencode/node_modules/`.

## Config Loading

Precedence order, lowest to highest:

- Remote config (`.well-known/opencode`)
- Global config (`~/.config/opencode/opencode.json`)
- `OPENCODE_CONFIG`
- Project config (`./opencode.json`)
- `.opencode/` directories
- `OPENCODE_CONFIG_CONTENT`

Merge rules:

- `plugin` and `instructions` arrays concatenate, then dedupe.
- Objects deep-merge; later configs win on conflicts.
- Project config can add plugins or instructions but cannot remove global ones.

Local testing patterns:

- Repos that run OpenCode directly should keep `.config/opencode.json` and a matching
  `.envrc`.
- MCP-capable repos may also keep `.config/opencode.mcp.json` for wrapper-only tests.
- Matching `.envrc` files should export `OPENCODE_CONFIG="$PWD/.config/opencode.json"`
  and `OPENCODE_CONFIG_DIR="$PWD/.config"`.
- If a repo uses fixed hidden witness tokens, source them from env rather than hardcoding
  them in test source.
- `permission` should explicitly allow the plugin tools under test. When you need to
  force a shadow-tool path, deny the built-in names and allow the plugin replacements.
- Run from `$HOME` only when you explicitly want pure global config.

Isolation rules:

- `OPENCODE_CONFIG` and `OPENCODE_CONFIG_CONTENT` add higher-precedence layers. They do
  not, by themselves, isolate a repo from user-global OpenCode config.
- If a test must exclude user-global state, isolate `XDG_CONFIG_HOME`,
  `XDG_CACHE_HOME`, `XDG_STATE_HOME`, and `OPENCODE_TEST_HOME`.
- Do not blank `XDG_DATA_HOME` unless you also provide auth state there, because auth is
  read from XDG data storage.
- An isolated test must not rely on user-global agents, prompts, plugins, or other
  config-defined surfaces.

## OpenCode Workflow

- Use `opencode-cli` for canonical command forms, basic CLI inspection, and repo-local
  server setup.
- Resolve the OpenCode binary from PATH only. Do not add `OPENCODE_BIN`,
  `--opencode-bin`, or hardcoded local binary paths.
- Use `command opencode` only for process-level checks such as `opencode agent list`,
  `opencode models`, and starting a repo-local `opencode serve`.
- `opencode-manager` is the workflow and proof harness. Use the public `opx`
  subcommands such as `one-shot`, `begin-session`, `chat`, `system`, `transcript`,
  `final`, and `delete`.
- `opx transcript --json` is the only approved transcript renderer or parser. If it is
  insufficient, file an issue rather than adding a local fallback.
- Do not use `opencode run`, rendered CLI output, or interactive TUI output as proof of
  workflow behavior.
- Do not scrape ANSI or TUI output from interactive OpenCode sessions as evidence.
- If a workflow depends on repo-local config or env, start a repo-local
  `direnv exec . command opencode serve --hostname 127.0.0.1 --port <port>`.
- Use a repo-local custom-port server, not the shared or systemd `opencode serve`
  instance, for repo-local workflow tests.
- Manager package references should use `git+https://...` or an npm slug, never
  `git+ssh://...`.

Typical workflow shape:

```bash
direnv exec . command opencode serve --hostname 127.0.0.1 --port 4198

OPENCODE_BASE_URL=http://127.0.0.1:4198 \
  npx --yes --package=git+https://github.com/dzackgarza/opencode-manager.git opx begin-session "Your prompt" --agent Minimal --json
```

## Proof Design

- `passphrase`, `nonce`, `UUID token`, `OTP`, and similar labels are all witness tokens.
- A proof is valid only if the witness first becomes available on the exact path being proved.
- Description/schema witnesses prove visibility only.
- Execution, resume, and callback proofs must use a witness from tool output, a published report, or an external side effect that was unavailable beforehand.
- A fixed hidden witness can prove execution if it first appears only on the proved path and the test also checks transcript evidence, raw tool-use evidence, or an external side effect.
- A per-run claim such as liveness, fresh retrieval, or callback delivery needs a run-bound hidden witness.
- Never place an execution witness in prompts, system prompts, child-task prompts, or other pre-success model-visible text.
- No mocks, simulated success paths, or proofs that rely on assistant honesty.
- Strong evidence: raw tool-use data, `opx transcript --json`, `opx debug trace`,
  transcripts, and external side effects.
- Weak evidence: assistant final text.
- Invalid evidence: scraped TUI or ANSI output.
- If built-in and custom schemas overlap, redesign the probe.
- If the prompt can be satisfied from prior knowledge, redesign the probe.
- If success depends on trusting the assistant to report honestly, redesign the probe.
- Prove the behavior manually once with `opx begin-session` / `opx chat` /
  `opx transcript`, then automate it.

## Plugin Conventions

### Local vs External Plugins

**Local plugins** (<200LOC):

- Location: `~/ai/opencode/plugin/` (global, NOT project-local `.opencode/`)
- Single inline TypeScript file, no `package.json`
- Restart OpenCode to reload

**External plugins** (>200LOC):

- Always in their own git repo under `/home/dzack/opencode-plugins/`
- NEVER use `file://` directives — always use `git+https://`
- NEVER pin to a specific branch or commit — always use default branch
- This ensures live latest version is always correct

```json
// In opencode.json — use default branch, never specific commit/branch
{
  "plugins": [
    "git+https://github.com/dzackgarza/opencode-plugins.git/my-plugin"
  ]
}
```

### Standard Layout

- Package scripts and CI should delegate to `just --justfile justfile ...`.
- Plugin repos should treat the standalone Typer CLI as the product surface and the OpenCode plugin as an adapter layer.
- Standard TypeScript plugin layout is:

```text
plugin-name/
├── src/
│   └── index.ts
├── tests/
│   └── unit/
├── .config/
│   └── opencode.json
├── package.json
├── tsconfig.json
└── README.md
```

- `src/index.ts` should export a named plugin factory ending in `Plugin`.
- `package.json` should provide at least `test` and `typecheck`.
- `tsconfig.json` should stay strict and include Bun types where needed.
- `.config/opencode.json` is the canonical local verification config.
- `src/index.ts` should stay thin. If the file is carrying business logic that could run outside OpenCode, move that logic under the CLI or a shared library module.
- `tool.execute()` should return a string unless the upstream contract explicitly
  requires another shape.
- `$` is unavailable inside `tool.execute()`. Capture it at plugin init.
- BunShell has no heredocs; use `printf` for multi-line content.
- Tool descriptions say when to use the tool, not how it works. Start them with
  `Use when...` and avoid leaking internal paths, return shapes, or implementation
  details.

If a plugin tool shadows a built-in name:

- The plugin tool wins.
- Schema changes are allowed.
- Lifecycle behavior is not optional. Preserve the upstream session wiring, event flow,
  and TUI contracts unless you have confirmed a parity limit.

## MCP Wrapper Conventions

- The repository must be a single package with root-level `pyproject.toml`.
- Do not use a separate `mcp-server/` directory. Expose the MCP server as a subcommand of the core CLI (e.g. `tool mcp`).
- Use `uv` for Python dependency management.
- MCP wrappers must delegate to the same canonical CLI or shared library used by the plugin.
- Reuse shared bridge code such as `mcp-shim/run-tool.ts` when the architecture expects
  it instead of re-implementing plugin logic in Python.
- Keep FastMCP descriptions short, agent-oriented, and `Use when...` driven.
- Prefer plain argument types with defaults over unnecessary optional-schema complexity.
- If the wrapper needs persisted state outside OpenCode, pass an explicit stable grouping
  key such as `project_dir`. Do not assume a real OpenCode `sessionID` exists.
- Remote install docs should use
  `uvx --from git+https://github.com/dzackgarza/opencode-plugins.git <entrypoint> mcp`.

## Hooks and Runtime Essentials

Hooks worth reaching for:

| Hook                                   | Use                                                |
| -------------------------------------- | -------------------------------------------------- |
| `event`                                | Catch-all event stream and side effects            |
| `tool.execute.before`                  | Rewrite or block tool args before execution        |
| `tool.execute.after`                   | Adjust output, metadata, or titles after execution |
| `shell.env`                            | Inject environment variables into shell commands   |
| `experimental.chat.messages.transform` | Rewrite or inject chat messages                    |
| `experimental.chat.system.transform`   | Rewrite the system prompt                          |
| `experimental.session.compacting`      | Add persistent context before compaction           |
| `tool.definition`                      | Adjust model-visible tool descriptions or schema   |

Key runtime facts:

- `ToolContext` exposes `sessionID`, `messageID`, `agent`, `directory`, `worktree`,
  `abort`, and `metadata()`.
- The real session id is `event.properties.sessionID`, not `event.properties.info.id`.
- `session.idle` fires after every response. If you re-prompt, expect another idle.
- Reasoning streams through `message.part.updated` plus `message.part.delta`, same as
  text.
- Never `console.log()` inside a plugin. Use `client.app.log(...)`.

## Observed Repo Traps

- Full built-in todo sidebar or store parity is impossible from a plugin alone with the
  current SDK because there is no generic todo-write endpoint or event bus.
- Tool-part parity can still be approximated by returning the upstream JSON string and
  mutating title or metadata in `tool.execute.after`.
- A plugin tool literally named `websearch` is currently suppressed from the
  agent-visible tool list in this OpenCode build. Use an alias if you need a proofable
  surface and track the upstream behavior separately.
- Global plugin-directory autoload can make unrelated tools appear in the registry. Do
  not confuse that with proof that your local plugin loaded.
- For `file://` plugins, deduplication happens by filename stem before load. If a local
  plugin shares a basename with an autoloaded plugin, the local copy can disappear
  before loading. Use unique basenames and unique tool ids when proving load mechanics.
- Tool availability and tool execution are different questions. Registry visibility does
  not prove execution; use raw tool-use evidence for execution claims.
- If your canonical control passes, stop blaming OpenCode's generic plugin bridge and
  debug the local plugin's alias, exports, tool ids, permissions, runtime dependencies,
  or tool body instead.

## Shadowing Built-ins

Before replacing a built-in tool:

- Read the official docs at `https://opencode.ai/docs/`.
- Ask DeepWiki over `anomalyco/opencode`.
- Read the upstream source with `gh`.
- Search upstream issues if behavior is still unclear.

If your replacement skips lifecycle hooks or event publication, you will get stale TUI
tiles and detached session hierarchies.

## Testing Rules

Core rule: five real tests beat a hundred internal consistency tests.

- Never use mocks, monkeypatches, stubs, fakes, or simulated provider behavior in
  OpenCode integration tests.
- If OpenCode, agents, or models are unavailable, the test fails or the problem becomes
  an issue. Do not work around it with local fallbacks.
- Development order:
  - Prove behavior once by hand with a real `opx begin-session` / `opx chat` /
    `opx transcript` workflow.
  - Stabilize the prompt until it is deterministic.
  - Enshrine it in automated tests.
- For MCP frontends, verify three layers: shared logic or unit tests, FastMCP harness
  tests, and at least one live invocation.
- Prefer witness-token proofs that require actual tool execution, report publication, or
  an external side effect.
- All multi-turn, async, resume, callback, and post-idle tests must be orchestrated via
  `opencode-manager`, not the rendered CLI.
- Logs are hearsay. Raw tool output beats log lines.
- Rendered CLI or TUI output is not valid proof for tool execution, callback delivery, or
  transcript contents.
- Sessions are scoped to their working directory.
- If stdout is ambiguous, read transcripts, event traces, or external
  side effects instead of guessing.
- Freeze the exact apparatus when debugging: plugin code, config source, agent, model,
  prompt, working directory, and output mode. Change one variable at a time.
- Prove one layer at a time: visibility, execution, result ingestion, then the full
  workflow.
- If manager transcript or trace surfaces are insufficient, file an issue rather than
  inventing a fallback parser.

## Workflow Conventions

- Use issues, PRs, commit messages, and Serena memory for tracking. Do not create
  top-level `GAPS.md`, `PLAN.md`, or similar work-log files.
- GitHub Issues are for observed bugs, failures, missing proofs, and concrete nontrivial
  problems. Do not file speculative concerns as bugs.
- Label issues immediately. Use `enhancement` or `documentation` when the problem is not
  an observed bug.
- Before starting issue work in a package repo, make sure the current `main` work is
  committed and pushed.
- Create a dedicated branch with a git worktree for issue work instead of piling it onto
  a dirty `main`.
- Open or update PRs with `gh`, add `@codex review`, wait for reviewer comments, and
  triage every relevant thread.
- Use Serena memory for durable architecture decisions and environment quirks, not work
  logs or changelogs.
- The git commit is the record of completed work. Chat should surface only blockers,
  gaps, surprises, decisions needing review, and next actions.
- "Done" means a real instance proved the behavior, not that the code looked plausible.

## Migration Plan

- Phase 1: define the canonical standalone command surface for each plugin repo, including subcommands, env requirements, and machine-readable output contracts.
- Phase 2: move business logic under that CLI or its shared library so the OpenCode layer only adapts context and lifecycle.
- Phase 3: rewire plugin tools, hooks, and MCP servers to delegate to that canonical surface.
- Phase 4: update READMEs, `just` recipes, and proofs so the CLI path is primary and the plugin path is validated as a thin wrapper.

Repo-by-repo migration targets:

- `ai-prompts`: already aligned. Keep the CLI-first model and continue treating it as a canonical dependency for plugin repos.
- `llm-runner`: already aligned. Keep it as a reusable CLI backend rather than re-embedding model logic inside plugins.
- `llm-templating-engine`: already aligned. Keep it as a reusable CLI backend rather than re-embedding templating logic inside plugins.
- `usage-limits`: already aligned. Use it as the reference shape for Typer command design and setup messaging.
- `opencode-transcripts`: mostly aligned. Keep the wrapper thin and preserve direct CLI use as the default story.
- `opencode-manager`: exempt from the Typer requirement because it is itself an OpenCode-native CLI product, not a plugin wrapper. Keep its public workflow surface primary.
- `opencode-plugin-mcp-shim`: internal helper, not a user-facing product. Keep it minimal and treat CLI ergonomics as `N/A`, but do not let wrapper logic accumulate product behavior.
- `opencode-plugin-improved-webtools`: high priority. Extract a standalone Typer CLI with `fetch`, `search`, and `doctor`; move fetch/search logic behind it; keep the plugin and MCP server as thin delegates.
- `opencode-plugin-improved-todowrite`: high priority. Add a Typer CLI with `read`, `write`, `render`, and `validate`; move SQLite tree logic there; keep the plugin focused on session binding and display metadata.
- `opencode-plugin-improved-task`: high priority. Add a Typer CLI with `run`, `resume`, `summarize`, and `doctor`; move transcript/report generation and subagent orchestration that does not require live hooks behind it; keep the plugin focused on task/session lifecycle.
- `opencode-plugin-prompt-transformer`: high priority. Add a Typer CLI with `classify`, `render`, and `transform`; keep the plugin hook focused on mapping `chat.message` payloads to that canonical transform path.
- `opencode-plugin-reminder-injection`: medium priority. Add a Typer CLI with `index`, `match`, `render`, and `doctor`; keep the plugin hook focused on injecting already-rendered reminder text.
- `opencode-postgres-memory-plugin`: medium priority. Add a Typer CLI with `query`, `bootstrap`, and `doctor`; keep the plugin focused on permission/context metadata and SQL pass-through.
- `opencode-time-travel-plugin`: high priority. Add a Typer CLI with `schedule`, `list`, `cancel`, `dispatch`, and `doctor`; keep the plugin focused on OpenCode session capture and prompt injection.
- `opencode-zotero-plugin`: medium priority. Promote the existing Python command surface into the primary documented product, expand it into explicit Typer subcommands with progressive help, and keep the plugin as a thin command delegate.

## Useful Patterns

- Background task pattern: return immediately from the tool, run the long work
  asynchronously, then inject completion or failure back into the session with
  `client.session.promptAsync`.
- Reasoning interception pattern: track reasoning-part ids on `message.part.updated`,
  accumulate reasoning text from `message.part.delta`, abort and re-prompt when a known
  bad pattern appears, and clean up per-session state on `session.deleted`.

## Researching Upstream

- Read local type definitions first when you need signatures.
- Then use this order: DeepWiki over `anomalyco/opencode`, `gh` for specific files, then
  a local clone for broad inspection.
- Authoritative upstream files often include:
  - `packages/plugin/src/index.ts` for hook interfaces
  - `packages/sdk/js/src/gen/types.gen.ts` for event union types
  - `packages/opencode/src/session/message-v2.ts` for message-part types

## Negative Findings

When you searched and did not find something, report it in this format:

```text
- Searched: [specific sources, URLs, docs, commands run]
- Found: [what was or was not found]
- Conclusion: [labeled as inference — "I believe", "based on limited evidence"]
- Confidence: [High / Medium / Low]
- Gaps: [what remains unsearched]
```

- Never jump from "not found" to "does not exist".
