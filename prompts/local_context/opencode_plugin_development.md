<!-- AGENTS.md-OTP: X7K9-MNPR-QW42 -->

# OpenCode Plugin Development

*IMPORTANT*: do not hide env vars in the code base without clearly documenting them in a local .envrc and in the README for your repo. Moreover, ensure all envrcs use `source_up` so they properly inherit ~/.envrc (e.g. for global API keys; but if a local repo truly relies on a global env var, it should still document it in the local envrc.

## 1. Repo Facts

- Each subdirectory is its own package/repo. The top-level `/home/dzack/opencode-plugins`
  directory is **not** a git repo.
- `~/ai/opencode/plugins/` is a separate workspace. Do not touch it from here.
- Register plugins in OpenCode via the `plugin` array using an npm package, an explicit
  git alias like `package-name@git+https://github.com/owner/repo`, or a
  `file:///abs/path/to/src/index.ts` entry.
- For git-backed plugin installs, the alias before `@` must match the package `name`
  from the plugin repo's `package.json`.
- Bun caches installed npm plugins under `~/.cache/opencode/node_modules/`.

**Generated config rule:**

- Never edit `~/ai/opencode/opencode.json` directly.
- Source of truth: `~/ai/opencode/configs/config_skeleton.json`
- Rebuild from `~/ai/opencode/` with `just rebuild`
- Do not run `just rebuild` while inside an active OpenCode session; it restarts
  `opencode-serve` and kills the session.

## 2. Pre-Push Quality Checklist

Before pushing any plugin repo to GitHub, verify the following:

### Tests
- All tests are **substantive**—no content-free checks like `is not None` or `len(x) > 0`
- Tests prove correctness via invariants, identities, and nontrivial witnesses
- **NO MOCKS**—test against real OpenCode instances, agents, and models; no `unittest.mock`,
  `monkeypatch`, stubs, fakes, or simulated environments
- **NO WORKAROUNDS**—if OpenCode, agents, or models are unavailable, the test fails
- **Tests as external probes**—prefer real OpenCode instances or manually driven multi-turn
  sessions; internal consistency is not proof of real functionality (type system already
  guarantees internals). Exception: strict unit tests for complex nondeterministic
  functionality (e.g., micro agent evaluations with external LLM services)
- All tests pass: run `just test` or equivalent

### Repository Hygiene
- **Self-contained**: No references to paths outside the repo (no `/home/dzack/...`, no `~/ai/...`)
- No development debris: remove `.serena/`, `__pycache__/`, `.tmp*/`, debug logs, scratch files
- No personal information: no local paths, usernames, or system-specific details in code or docs

### Configuration Management
- All environment variables centralized in `.envrc`
- No secrets in code—`.envrc` contains only dummy defaults or commented placeholders
- Tweakable options sourced from `.envrc` or YAML config, not hardcoded
- One source of truth: constants defined once and imported, not duplicated

### Code Quality
- No "graceful" fallbacks or legacy compatibility layers—current working state only
- No comments discussing past state or refactoring history (that's what git is for)
- Proper semantic versioning (X.Y.Z) with `just bump` recipe for minor version increments

### Documentation
- README follows concise writing principles—purely informational, not marketing
- Clear onboarding process encoded in `justfile` (e.g., `just setup`, `just dev`)
- Direct usage without installation: provide `uvx`/`npx` commands that work from repo URL
- Explicit config snippets showing required setup

## 3. Config Loading

Precedence order, lowest → highest:

1. Remote config (`.well-known/opencode`)
2. Global config (`~/.config/opencode/opencode.json`)
3. `OPENCODE_CONFIG`
4. Project config (`./opencode.json`)
5. `.opencode/` directories
6. `OPENCODE_CONFIG_CONTENT`

Merge rules:

- `plugin` and `instructions` arrays concatenate, then dedupe
- Project config can add plugins/instructions but cannot remove global ones
- Objects deep-merge; later configs win on conflicts

Local testing:

- Each plugin may provide `.config/opencode.json` and a matching `.envrc`
- Prefer `direnv allow` inside the plugin directory
- Fallback: `OPENCODE_CONFIG=/abs/path/to/.config/opencode.json`
- Run from `$HOME` only when you explicitly want pure global config
- Correction: `OPENCODE_CONFIG` and `OPENCODE_CONFIG_CONTENT` do **not** isolate a
  repo from user-global OpenCode config. They add higher-precedence layers, but global
  config and `~/.opencode` discovery still apply and plugin arrays still concatenate.
- For a repo-only custom-port `opencode serve` harness, isolate config discovery
  explicitly:
  - set `XDG_CONFIG_HOME` to an empty temp dir to suppress `~/.config/opencode`
  - set `OPENCODE_TEST_HOME` to an empty temp dir to suppress `~/.opencode`
  - do **not** change `XDG_DATA_HOME` unless you also provide auth state there, because
    auth is read from XDG data storage
- An isolated test must not rely on user-global agents, prompts, plugins, or other
  config-defined surfaces. Define required agents locally or use built-ins that are
  present under the isolated runtime.

Monorepo local config pattern:

- Plugin repos that run OpenCode directly keep `.config/opencode.json`
- MCP-capable repos also keep `.config/opencode.mcp.json` for wrapper-only tests
- Matching `.envrc` files export `OPENCODE_CONFIG="$PWD/.config/opencode.json"`
- Some `.envrc` files also export verification passphrases used by live tests
- Current local test configs use `model: "github-copilot/gpt-4.1"`
- `plugin` points either at the package root (`file:///.../plugin/`) or at
  `src/index.ts`, depending on how the plugin is loaded
- `permission` should explicitly allow the plugin tools under test; when you need to
  force a shadow tool path, deny the built-in names and allow the plugin replacements
- `mcp-shim` and `zotero` are exceptions here: they do not follow the direct-plugin
  `.config/opencode.json` pattern

## 4. Running OpenCode

- Always use `/home/dzack/.opencode/bin/opencode` for smoke tests, agent/model
  discovery, and config sanity checks
- Never use the `opencode` alias for tests; it attaches to the server
- The standalone binary rereads config every invocation; “stale config” is not a valid
  explanation
- Do not use the shared/systemd `opencode serve` instance for repo-local tests
- A repo-local `opencode serve --hostname 127.0.0.1 --port <custom>` started inside the
  plugin's `direnv` is a valid `opencode-manager` target when the workflow depends on
  local config or env
- A custom-port repo-local server is **not** isolated just because `direnv` exported
  `OPENCODE_CONFIG`. If the test must exclude global user plugins/config, launch it
  with isolated `XDG_CONFIG_HOME` and `OPENCODE_TEST_HOME`
- `--attach` + `--agent` is broken; use standalone runs only
- Do **not** use the interactive CLI/TUI as your workflow harness for plugin tests
- Do **not** scrape ANSI/TUI/stdout from interactive OpenCode sessions as evidence
- Mandatory test harness for real workflows: `opencode-manager`
  - `opx` for run/resume/debug flows
  - `opx-session` for create/prompt/messages/abort/revert/permission orchestration
- Mandatory readable transcript renderer: `opx-session transcript`
  - `npx --yes --package=/home/dzack/opencode-plugins/opencode-manager opx-session transcript`
- The CLI is an entrypoint, not an orchestration layer. Multi-turn, async, and
  post-idle behavior must be driven through `opx` / `opx-session`, with evidence taken
  from session data, transcripts, debug traces, or external side effects
- The `echo` / `printf` stdin trick is a compatibility escape hatch only. If you must
  use it to start a real interactive session, discard the TUI output and inspect the
  resulting session through `opencode-manager` or transcript artifacts instead

Agent/model discovery:

- List available agents with `opencode agent list`
- For permissive test runs, prefer `--agent "Unrestricted Test"`
- If a run fails with provider/model errors, or produces no output when the prompt should
  be straightforward, check `opencode models` before debugging anything else

Service commands, only when changing deployed config outside an active session:

```bash
systemctl --user status opencode-serve
systemctl --user restart opencode-serve
```

## 5. Plugin Conventions

Standard package layout:

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

Required conventions:

- `src/index.ts` exports a named plugin factory ending in `Plugin`
- `package.json` provides at least `test` and `typecheck`
- `tsconfig.json` stays strict and includes Bun types when needed
- `.config/opencode.json` is the canonical local verification config
- Edit existing packages instead of inventing parallel scaffolds

Runtime rules:

- `tool.execute()` should return a string unless the upstream contract explicitly requires
  another shape
- `$` is unavailable inside `tool.execute()`; capture it at plugin init
- BunShell has no heredocs; use `printf` for multi-line content
- Tool descriptions say **when to use the tool**, not how it works
- Start tool descriptions with `Use when...`
- Do not expose internal paths, return shapes, or implementation details in tool
  descriptions

If a plugin tool shadows a built-in name:

- The plugin tool wins
- Schema changes are allowed
- Lifecycle behavior is not optional: preserve the upstream session wiring, event flow,
  and TUI contracts unless you have confirmed a parity limit

## 6. MCP Wrapper Conventions

When a plugin needs an MCP wrapper, use this layout:

```text
plugin-name/
└── mcp-server/
    ├── server.py
    ├── pyproject.toml
    ├── README.md
    └── tests/
```

Rules:

- Use `uv` for Python dependency management
- Reuse [`mcp-shim/run-tool.ts`](/home/dzack/opencode-plugins/mcp-shim/run-tool.ts)
  instead of re-implementing plugin logic in Python
- Keep FastMCP descriptions short, agent-oriented, and `Use when...` driven
- Prefer plain argument types with defaults over unnecessary `Optional[...]` schema
  complexity
- If the wrapper needs persisted state outside OpenCode, pass an explicit stable grouping
  key such as `project_dir`; do not assume a real OpenCode `sessionID` exists
- Remote-style install docs should use
  `uvx --from git+https://github.com/dzack/opencode-plugins#subdirectory=<plugin>/mcp-server`

## 7. Hooks and SDK Essentials

Hooks worth reaching for in this repo:

| Hook | Use |
|------|-----|
| `event` | Catch-all event stream and side effects |
| `tool.execute.before` | Rewrite/block tool args before execution |
| `tool.execute.after` | Adjust output, metadata, or titles after execution |
| `shell.env` | Inject environment variables into shell commands |
| `experimental.chat.messages.transform` | Rewrite/inject chat messages |
| `experimental.chat.system.transform` | Rewrite system prompt |
| `experimental.session.compacting` | Add persistent context before compaction |
| `tool.definition` | Adjust model-visible tool descriptions/schema |

Key runtime facts:

- `ToolContext` gives you `sessionID`, `messageID`, `agent`, `directory`, `worktree`,
  `abort`, and `metadata()`
- The real session id is `event.properties.sessionID`, not `event.properties.info.id`
- `session.idle` fires after every response; if you re-prompt, expect another idle
- Reasoning streams through `message.part.updated` plus `message.part.delta`, same as text
- Never `console.log()` inside a plugin; use `client.app.log(...)`

SDK calls used most often:

```typescript
await client.session.prompt({ path: { id: sessionID }, body: { noReply: false, parts } });
await client.session.promptAsync({ path: { id: sessionID }, body: { noReply: false, parts } });
await client.session.abort({ path: { id: sessionID } });
const { data: messages } = await client.session.messages({ path: { id: sessionID } });
```

## 8. Observed Repo Traps

These belong here because they were learned the hard way and are easy to rediscover
badly.

- The root directory is not a git repo; only the package subdirectories are
- Full built-in todo sidebar/store parity is impossible from a plugin alone with the
  current SDK because there is no generic todo write endpoint or event bus
- Tool-part parity can still be approximated by returning the upstream JSON string and
  mutating title/metadata in `tool.execute.after`
- A plugin tool literally named `websearch` is currently suppressed from the
  agent-visible tool list in this OpenCode build; use an alias if you need a proofable
  surface and track the upstream behavior separately

## 9. Shadowing Built-ins

Before replacing a built-in tool:

1. Read the official docs: `https://opencode.ai/docs/`
2. Ask DeepWiki over `anomalyco/opencode`
3. Read the upstream source with `gh`
4. Search upstream issues if the behavior is still unclear

For the built-in `task` tool, the authoritative source is:

```bash
gh api repos/anomalyco/opencode/contents/packages/opencode/src/tool/task.ts \
  | python3 -c "import json,sys,base64; print(base64.b64decode(json.load(sys.stdin)['content']).decode())"
```

If your replacement skips lifecycle hooks or event publication, you will get stale TUI
tiles and detached session hierarchies.

## 10. Testing Rules

Core rule: five real tests beat a hundred internal consistency tests.

**NEVER use mocks or simulations.** All tests must run against real OpenCode instances,
agents, and models. If OpenCode is unavailable, the test fails—do not work around this
with mocks, stubs, or synthetic environments.

Development order:

1. Prove behavior once by hand with a real `opx` / `opx-session` workflow
2. Stabilize the prompt until it is deterministic
3. Enshrine it in automated tests

For MCP frontends, verify three layers:

1. Shared logic/unit tests
2. FastMCP harness, usually `uv run pytest`
3. At least one live invocation, e.g. `uv run fastmcp call ... --json`

Additional testing rules:

- Prefer proofs that require actual tool execution: passphrases, timestamps, UUIDs,
  stable synthetic ids
- All multi-turn, async, resume, callback, and post-idle tests must be orchestrated via
  `opencode-manager`, not the rendered CLI
- **NO MOCKS**—test against real behavior only; no `unittest.mock`, `monkeypatch`,
  stubs, fakes, or simulated environments
- **NO WORKAROUNDS** for missing OpenCode, agents, or models—if unavailable, test fails
- **Tests as external probes**—prefer real OpenCode instances or manually driven
  multi-turn sessions; internal consistency is not proof of real functionality (type
  system already guarantees internals). Exception: strict unit tests for complex
  nondeterministic functionality (e.g., micro agent evaluations with external LLM services)
- Logs are hearsay; raw tool output beats log lines
- Rendered CLI/TUI output is not valid proof for tool execution, callback delivery, or
  transcript contents
- If stdout is ambiguous, do not guess. Read session messages, transcripts, event traces,
  or external side effects instead
- Sessions are scoped to their working directory

### Nondeterministic Agent Debugging Checklist

Before concluding anything about tool visibility, tool use, or model obedience:

- Freeze the exact apparatus: save the plugin code, config source, agent, model, prompt,
  working directory, and output mode. Change one variable at a time.
- Keep the full evidence stream. Do not reason from filtered `jq` output, assistant-only
  excerpts, or paraphrased summaries if the question is whether a tool actually ran.
- Prove one layer at a time:
  - Can the model see the tool? Ask for the exact description without calling it.
  - Can the model call the tool? Use a prompt that requires the tool with an argument
    shape only the target tool accepts.
  - Can you prove execution? Use a unique passphrase in raw tool output; when dispatch
    matters, prefer a raw `tool_use` event or an external side effect.
  - Can you prove the model saw the result? Require `ONLY` the passphrase in the next
    reply.
  - Can you prove the model did not fabricate? Compare assistant text with full stdout
    and, when needed, raw events.
- Use the evidence hierarchy:
  - Invalid for proof: rendered terminal/TUI output, ANSI streams, scraped CLI text
  - Weak: assistant final text
  - Better: exported transcript or `opx-session messages --json`
  - Strong: raw `tool_use` / session trace data such as `opx debug trace`
  - Strongest: raw `tool_use` plus an external side effect such as a marker file, UUID,
    timestamp, or other artifact the model cannot fake
- Treat negative results correctly:
  - Missing passphrase in assistant text does not prove the tool was unavailable
  - Missing tool banners in one renderer does not prove the tool was not called
  - Filtered or truncated output is not a valid basis for proving non-execution
  - Lack of evidence is not evidence of non-execution
- Stop on ambiguity:
  - If built-in and custom schemas overlap, redesign the probe
  - If the prompt can be satisfied from prior knowledge, redesign the probe
  - If success or failure depends on trusting the assistant to report honestly,
    redesign the probe
- Only after the minimal control passes should you move outward: standalone tool,
  shadowed name, local config, `file://` load, `git+` load, then the real plugin.

### Known Working Controls

Use these controls before blaming OpenCode internals, the generic plugin bridge, or the
model provider:

Detailed evidence, command patterns, and postmortems live in these memories:

- `plugin-debugging/file-url-plugin-deduplication-by-basename`
- `plugin-debugging/public-git-plus-plugin-proof`
- `plugin-debugging/assistant-text-is-not-tool-availability-evidence`

- Global plugin directory autoload works. `~/ai/opencode/plugins/local-tools.ts`
  currently contributes tools such as `introspection`, `list_sessions`,
  `read_transcript`, and `sleep`. If those appear in `tool.registry`, the autoload path
  and general plugin loader are working.
- `file://` plugin loading works with non-colliding basenames. The active controls are
  `file:///home/dzack/ai/opencode/tools/canonical-plugin-probes/canonical-smoke-fileproof.ts`
  and
  `file:///home/dzack/ai/opencode/tools/canonical-plugin-probes/canonical-shadowing-fileproof.ts`.
  They expose `mytool_fileproof_20260310` and `webfetch_fileproof_20260310`.
- The `file://` smoke control proves exact execution. `mytool_fileproof_20260310`
  returns the fixed token `PASS_MYTOOL_FILEPROOF_20260310`. If a raw `tool_use` event
  shows that output, `file://` inclusion and custom tool execution are both working.
- The `file://` URL-shaped control proves the bridge can surface another custom tool with
  a `url` argument. `webfetch_fileproof_20260310` returns
  `EXEC_WEBFETCH_FILEPROOF_20260310 <url>`. If this control works while your own
  `file://` plugin does not, focus on your plugin's basename, exports, tool ids, or
  permissions.
- Public `git+https` plugin loading works. The current control is
  `@dzackgarza/opencode-postgres-memory-plugin@git+https://github.com/dzackgarza/opencode-postgres-memory-plugin`,
  which exposes `query_memories`.
- `git+https` loading and tool exposure are separate from tool-body correctness. The
  `query_memories` control has been observed in `tool.registry` and in raw `tool_use`
  events, so the public `git+https` path is proven even when the tool body later fails
  inside its own Postgres runtime.
- For `file://` plugins, deduplication happens by filename stem before load. If a
  `file://` plugin shares a basename with an autoloaded file under
  `~/ai/opencode/plugins/`, the `file://` copy can disappear before loading. Use unique
  basenames and unique tool ids when proving load mechanics.
- Tool availability and tool execution are different questions. `service=tool.registry
  status=started <tool-id>` proves the model was offered the tool. A raw `tool_use`
  event proves the tool actually ran. Assistant text alone proves neither.
- If these controls pass, stop debugging OpenCode's general plugin bridge. Debug the
  local plugin instead: package alias vs `package.json` name, exported plugin function,
  tool ids, permissions, runtime dependencies, or the tool body itself.

## 11. Passphrase Method

Use this when you must prove that a tool path really executed.

Hard restrictions:

- Never place the passphrase in any prompt, system message, tool description, child-task
  prompt, or other model-visible text
- The only valid proof is the model relaying a token it could only have seen from tool
  output

Method:

1. Add a temporary verification seam gated by env/config
2. Emit a hidden passphrase in raw tool output
3. Run a bounded control prompt first
4. Run the experimental prompt and require `ONLY` the passphrase in the reply
5. For read-after-write tests, split the proof into two turns on the same session so the
   read path must execute

Reject any design where success could be explained by:

- the model repeating a token it already saw
- schema or description leakage
- another tool producing the same token
- a parent agent paraphrasing instead of quoting raw output
- logs or exports being inspected instead of making the agent relay the token

## 12. Test Commands

Manager-first commands:

```bash
MANAGER="npx --yes --package=git+ssh://git@github.com/dzackgarza/opencode-manager.git"
TRANSCRIPT="npx --yes --package=/home/dzack/opencode-plugins/opencode-manager opx-session transcript"

# One-shot workflow probe
$MANAGER opx run --agent Minimal --prompt "Your prompt."

# Resume a known session
$MANAGER opx resume --session ses_123 --prompt "Follow-up prompt."

# Create a session explicitly
$MANAGER opx-session create --title "plugin-test"

# Send a prompt without waiting for a reply
$MANAGER opx-session prompt ses_123 "Your prompt." --no-reply

# Read messages/transcript evidence from the real session
$MANAGER opx-session messages ses_123 --json
$MANAGER opx debug trace --session ses_123 --verbose
$TRANSCRIPT ses_123
```

Binary-only commands:

```bash
# List available agents
/home/dzack/.opencode/bin/opencode agent list

# Check available models/providers
/home/dzack/.opencode/bin/opencode models

# Pure global config
cd ~
timeout 15 /home/dzack/.opencode/bin/opencode run --agent Minimal "Your prompt."

# Local plugin config
cd /path/to/plugin
direnv allow
timeout 15 /home/dzack/.opencode/bin/opencode run --agent "Unrestricted Test" "Your prompt."

# Fallback without direnv
OPENCODE_CONFIG=/abs/path/to/.config/opencode.json \
timeout 15 /home/dzack/.opencode/bin/opencode run --agent "Unrestricted Test" "Your prompt."
```

Rules:

- `opencode-manager` is the required orchestration harness for real workflow tests
- No `--attach`
- No shared/systemd `opencode serve`
- A repo-local custom-port `opencode serve` is allowed when `opencode-manager` needs a
  server with the repo-local config/env
- No background jobs with `&`
- `timeout 15` is the default; MCP warmup is not the bottleneck
- Use `Unrestricted Test` when the test needs permissive edit/bash/tool access without
  fighting agent-level restrictions
- If the binary reports provider/model failures, run `opencode models` before blaming the
  plugin or MCP layer

Read-after-write persistence:

```bash
$MANAGER opx-session messages <session-id> --json
$MANAGER opx resume --session <session-id> --prompt "Follow-up prompt."
```

Async / post-idle pattern:

```bash
TMPDIR_ROOT="$(mktemp -d)"
mkdir -p "$TMPDIR_ROOT/config" "$TMPDIR_ROOT/home"

# Start a repo-local server when the workflow depends on local config/env
XDG_CONFIG_HOME="$TMPDIR_ROOT/config" \
OPENCODE_TEST_HOME="$TMPDIR_ROOT/home" \
direnv exec /path/to/plugin \
  /home/dzack/.opencode/bin/opencode serve --hostname 127.0.0.1 --port 4198

# Start the workflow without blocking on the model reply
OPENCODE_BASE_URL=http://127.0.0.1:4198 \
  $MANAGER opx-session prompt <session-id> "your prompt" --no-reply

# Poll or inspect the real session instead of scraping the TUI
OPENCODE_BASE_URL=http://127.0.0.1:4198 $MANAGER opx-session messages <session-id> --json
OPENCODE_BASE_URL=http://127.0.0.1:4198 $MANAGER opx debug trace --session <session-id> --verbose
OPENCODE_BASE_URL=http://127.0.0.1:4198 $TRANSCRIPT <session-id>
```

## 13. Workflow Conventions

### Information Architecture

| Location | Purpose |
|----------|---------|
| **GitHub Issues** | Observed bugs, failures, missing features—concrete problems only |
| **Local docs** (README, AGENTS.md) | Current state and high-level future directions |
| **Serena memories** | Local dev guidance, environment quirks, cross-session context |
| **Commit messages** | Changelogs, what changed and why |

**Rule**: Docs describe what *is* and what *will be*, never what *was*. No local issue tracking files like `GAPS.md`, `PLAN.md`, or `TODO.md`.

### Issue Workflow

- Apply git and issue workflow inside the relevant package repo. The top-level
  `/home/dzack/opencode-plugins` directory is coordination space, not a git repo.
- Log every observed non-trivial error as a **GitHub Issue** in the affected repo immediately.
- **All issues must be labeled immediately upon creation.**
- An issue is an observed bug, failure, missing proof, or other concrete problem that
  you cannot fix trivially in the current task or that is outside the current task.
- Do not file speculative concerns, defensive hedging, imagined fallbacks, or
  preemptive robustness work as bugs. Those are feature requests or design ideas.
- If you track those at all, **mandatory label** and describe them as `enhancement` or
  `documentation` rather than bugs.
- Close an issue only after a specific pushed commit fixes it or makes it irrelevant.
  The closing comment must say where the fix lives and how it resolves the issue.
- Before starting issue work in a package repo, make sure the current `main` work is
  committed and pushed.
- Create a dedicated branch with a git worktree for the issue. Do not pile new issue
  work onto a dirty `main`.
- Implement the fix or proof on that branch and push the branch.
- Open or update the PR with `gh`, then add a `@codex review` comment.
- Sleep up to 5 minutes waiting for Codex and Qodo Merge reviews.
- Triage every relevant review thread. Reviewers may over-suggest defensive,
  enterprise-style hedging that is inappropriate for a small plugin repo. Keep the
  scope pragmatic.
- Leave a comment on each relevant thread explaining the resolution decision. If you
  changed code, cite the commit or follow-up edit. If you rejected the suggestion,
  say why.
- After substantive updates, wait for fresh reviews and repeat until all relevant
  discussions are resolved.
- Stop once the branch, PR, and review threads are ready. Wait for the user to merge.
- Do not maintain local `GAPS.md`, `PLAN.md`, or `MCP-WRAPPERS-PLAN.md`
- Use Serena memory for durable architecture decisions and constraints, not work logs
- The git commit is the record of completed work; chat should only surface blockers, gaps,
  decisions needing review, and next actions
- “Done” means a real instance proved the behavior, not that the code looked plausible

## 14. Useful Patterns

Background task pattern:

- Return immediately from the tool
- Run the long work asynchronously
- Inject completion or failure back into the session with `client.session.promptAsync`

Reasoning interception pattern:

- Track reasoning part ids on `message.part.updated`
- Accumulate reasoning text from `message.part.delta`
- Abort and re-prompt when a known bad pattern appears
- Clean up per-session state on `session.deleted`

## 15. Researching Upstream

Read local type definitions first when you need signatures:

```bash
cat node_modules/@opencode-ai/plugin/dist/index.d.ts
cat node_modules/@opencode-ai/sdk/dist/gen/types.gen.d.ts
```

Then use this order:

1. DeepWiki over `anomalyco/opencode`
2. `gh` for specific files
3. A local clone for broad inspection

Authoritative upstream files:

- `packages/plugin/src/index.ts` — hook interfaces
- `packages/sdk/js/src/gen/types.gen.ts` — event union types
- `packages/opencode/src/session/message-v2.ts` — message part types
