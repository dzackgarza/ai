<!-- AGENTS.md-OTP: X7K9-MNPR-QW42 -->

# OpenCode Plugin Development

## 1. Repo Facts

- Each subdirectory is its own package/repo. The top-level `/home/dzack/opencode-plugins`
  directory is **not** a git repo.
- `~/ai/opencode/plugins/` is a separate workspace. Do not touch it from here.
- Register plugins in OpenCode via the `plugin` array using either an npm package or a
  `file:///abs/path/to/src/index.ts` entry.
- Bun caches installed npm plugins under `~/.cache/opencode/node_modules/`.

**Generated config rule:**

- Never edit `~/ai/opencode/opencode.json` directly.
- Source of truth: `~/ai/opencode/configs/config_skeleton.json`
- Rebuild from `~/ai/opencode/` with `just rebuild`
- Do not run `just rebuild` while inside an active OpenCode session; it restarts
  `opencode-serve` and kills the session.

## 2. Config Loading

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

## 3. Running OpenCode

- Always use `/home/dzack/.opencode/bin/opencode` for testing
- Never use the `opencode` alias for tests; it attaches to the server
- The standalone binary rereads config every invocation; “stale config” is not a valid
  explanation
- Do not use `opencode serve` or the systemd service for tests
- `--attach` + `--agent` is broken; use standalone runs only

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

## 4. Plugin Conventions

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

## 5. MCP Wrapper Conventions

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

## 6. Hooks and SDK Essentials

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

## 7. Observed Repo Traps

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

## 8. Shadowing Built-ins

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

## 9. Testing Rules

Core rule: five real tests beat a hundred internal consistency tests.

Development order:

1. Prove behavior once by hand with a real `opencode run`
2. Stabilize the prompt until it is deterministic
3. Enshrine it in automated tests

For MCP frontends, verify three layers:

1. Shared logic/unit tests
2. FastMCP harness, usually `uv run pytest`
3. At least one live invocation, e.g. `uv run fastmcp call ... --json`

Additional testing rules:

- Prefer proofs that require actual tool execution: passphrases, timestamps, UUIDs,
  stable synthetic ids
- No mocks as the primary proof of behavior
- Logs are hearsay; raw tool output beats log lines
- If stdout is ambiguous because tool banners or assistant formatting got mixed in, parse
  the transcript instead of guessing
- Sessions are scoped to their working directory

## 10. Passphrase Method

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

## 11. Test Commands

Always use the binary, not the alias:

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

- No `--attach`
- No `opencode serve`
- No background jobs with `&`
- `timeout 15` is the default; MCP warmup is not the bottleneck
- Use `Unrestricted Test` when the test needs permissive edit/bash/tool access without
  fighting agent-level restrictions
- If the binary reports provider/model failures, run `opencode models` before blaming the
  plugin or MCP layer

Read-after-write persistence:

```bash
/home/dzack/.opencode/bin/opencode session list
timeout 15 /home/dzack/.opencode/bin/opencode run --agent Minimal -s <session-id> "Follow-up prompt."
```

Async pattern:

```bash
mkdir -p /tmp/plugin-test
(cd /tmp/plugin-test && timeout 90 sh -c 'echo "your prompt" | /home/dzack/.opencode/bin/opencode') >/dev/null 2>&1
(cd /tmp/plugin-test && /home/dzack/.opencode/bin/opencode session list)
python ~/.agents/skills/reading-transcripts/scripts/parse_transcript.py --harness opencode <session-id>
```

## 12. Workflow Conventions

- Track bugs, feature requests, open questions, known limitations, and roadmap items in
  GitHub issues
- Do not maintain local `GAPS.md`, `PLAN.md`, or `MCP-WRAPPERS-PLAN.md`
- Use Serena memory for durable architecture decisions and constraints, not work logs
- The git commit is the record of completed work; chat should only surface blockers, gaps,
  decisions needing review, and next actions
- “Done” means a real instance proved the behavior, not that the code looked plausible

## 13. Useful Patterns

Background task pattern:

- Return immediately from the tool
- Run the long work asynchronously
- Inject completion or failure back into the session with `client.session.promptAsync`

Reasoning interception pattern:

- Track reasoning part ids on `message.part.updated`
- Accumulate reasoning text from `message.part.delta`
- Abort and re-prompt when a known bad pattern appears
- Clean up per-session state on `session.deleted`

## 14. Researching Upstream

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
