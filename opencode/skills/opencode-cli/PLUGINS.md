# OpenCode Plugins

Quick reference for creating and using OpenCode plugins with concrete examples.

For global CLI rules and manager command forms, read `SKILL.md` first. For plugin proof
rules and audit criteria, switch to `../opencode-plugin-development/GUIDE.md` and
`../opencode-plugin-development/AUDIT.md`.

---

## Plugin Locations

| Type    | Path                          |
| ------- | ----------------------------- |
| Project | `.opencode/plugins/`          |
| Global  | `~/.config/opencode/plugins/` |

**Local plugins are loaded AUTOMATICALLY** — simply place `.ts` files in these directories. **No registration in config is required.**

**Always use TypeScript (`.ts`).** OpenCode runs plugins via Bun, which executes TypeScript natively — no compilation step, no build tooling. `.js` works but offers no benefit.

**npm packages** require registration in `opencode.json`:

```json
{
  "plugin": ["my-plugin", "@org/scoped-plugin"]
}
```

---

## Plugin Structure

```js
// .opencode/plugins/my-plugin.js
export const MyPlugin = async ({ project, client, $, directory, worktree }) => {
  return {
    // Hook implementations
  };
};
```

**Context object:**

- `project` - Current project info
- `directory` - Current working directory
- `worktree` - Git worktree path
- `client` - OpenCode SDK client
- `$` - Bun shell API

---

## Compilation and Testing

### Compiling Plugins

Always compile before testing to catch type errors early:

```bash
cd ~/.config/opencode/plugins
bun build --compile my-plugin.ts
```

This bundles dependencies and catches TypeScript errors.

### Testing with One-Shots

Use `command opencode run` only for true one-shot probes where stdout is the product and
the session does not need to continue after idle:

```bash
cd ~/.config/opencode
command opencode run "Use my_tool to do something"
```

For multi-turn, async, resume, callback, or post-idle behavior, use `opencode-manager`
as the workflow harness and inspect the session directly:

```bash

# When the workflow depends on repo-local config/env, start a dedicated server there first
direnv exec /path/to/plugin \
  command opencode serve --hostname 127.0.0.1 --port 4198

# One-shot sanity check
OPENCODE_BASE_URL=http://127.0.0.1:4198 \
  npx --yes --package=git+https://github.com/dzackgarza/opencode-manager.git opx one-shot --agent Minimal --prompt "Use my_tool to do something"

# Proof-oriented session orchestration
OPENCODE_BASE_URL=http://127.0.0.1:4198 npx --yes --package=git+https://github.com/dzackgarza/opencode-manager.git opx begin-session "Trigger async behavior" --agent Minimal --json
OPENCODE_BASE_URL=http://127.0.0.1:4198 npx --yes --package=git+https://github.com/dzackgarza/opencode-manager.git opx chat --session ses_abc123 --prompt "Follow-up prompt"
OPENCODE_BASE_URL=http://127.0.0.1:4198 npx --yes --package=git+https://github.com/dzackgarza/opencode-manager.git opx debug trace --session ses_abc123 --verbose
OPENCODE_BASE_URL=http://127.0.0.1:4198 npx --yes --package=git+https://github.com/dzackgarza/opencode-manager.git opx transcript --session ses_abc123 --json
OPENCODE_BASE_URL=http://127.0.0.1:4198 $MANAGER opx delete --session ses_abc123
```

The rendered CLI/TUI is not valid evidence. Use debug traces, transcripts, or external
side effects.

**Two-phase debugging workflow:**

1. `command opencode run "prompt"` — fast one-shot sanity check
2. `opx begin-session` / `opx chat` / `opx transcript` — real workflow proof with session artifacts

### Common Pitfalls

**BunShell (`$`) context:**

The `$` shell from `PluginInput` is NOT available in `ToolContext`. Capture it at plugin initialization:

```ts
// CORRECT: Capture $ from plugin context
export const MyPlugin: Plugin = async (ctx) => {
  const shell = ctx.$;  // Capture here

  return {
    tool: {
      mytool: tool({
        args: { ... },
        async execute(args, context) {
          await shell`command`;  // Use captured shell
        },
      }),
    },
  };
};

// WRONG: Try to get $ from execute context
async execute(args, context) {
  const shell = context.$;  // undefined! Doesn't exist in ToolContext
}
```

**ToolContext available properties:**

- `directory` - Current project directory
- `worktree` - Git worktree root
- `sessionID`, `messageID`, `agent`
- `abort` - AbortSignal
- `metadata()` - Set title/metadata

**Shell escaping:** BunShell doesn't support heredocs. Use `printf` with proper escaping:

```ts
const escaped = args.content.replace(/'/g, "'\"'\"'");
await shell`printf '%s' '${escaped}' > ${filepath}`;
```

---

## Events Reference

### Session Events

- `session.created`, `session.compacted`, `session.deleted`
- `session.idle` - **Equivalent to Claude Code's "Stop" hook** — fires after AI finishes responding
- `session.error`, `session.updated`, `session.diff`, `session.status`
- `experimental.session.compacting` - Fires before compaction; modify `output.context` (append) or `output.prompt` (replace entirely)

**Note:** `session.idle` is the key event for stop hooks. In a typical one-shot, it fires once per AI response — so a stop hook that injects a follow-up prompt will trigger a second `session.idle`.

### Tool Events

These use a **different handler signature** than `event` — they receive `(input, output)` directly, not `{ event }`:

- `tool.execute.before` - Intercept tool call before execution; can modify `output.args` or throw to block
- `tool.execute.after` - Inspect result after execution

### Message Events

- `message.part.delta` - **High-frequency streaming event** (~100× per response); fires as tokens stream in
- `message.part.updated` - Fires when a part is finalized (much less frequent than delta)
- `message.updated`, `message.removed`, `message.part.removed`

**Observed frequencies (one-shot, single response):** `message.part.delta` × 102, `message.part.updated` × 14, `message.updated` × 12. Do not use `delta` for post-response logic — use `session.idle` instead.

**Note:** `message.part.updated` contains text in `event.properties.part.text` (NOT `event.message`).

**`message.part.delta` payload shape:**

```ts
{
  type: "message.part.delta",
  properties: {
    sessionID: string,
    messageID: string,
    partID: string,   // links back to the Part being streamed
    field: string,    // which field is being updated (e.g. "text")
    delta: string,    // the incremental content appended
  }
}
```

**Part types available in the SDK** (`type` field on a Part):
`text` | `reasoning` | `tool` | `file` | `subtask` | `agent` | `stepStart` | `stepFinish` | `snapshot` | `patch` | `retry` | `compaction`

`reasoning` parts carry chain-of-thought content from thinking models. They stream exactly like `text` parts: created empty via `message.part.updated`, then filled token-by-token via `message.part.delta` with `field: "text"`.

### Intercepting CoT / Mid-Stream Intervention

The `event` hook receives `message.part.delta` events in real-time, including `reasoning` parts — so a plugin can observe CoT as it streams. However, **the `event` hook is read-only**: there is no way to modify or suppress a delta.

There are two ways to stop in-progress generation, and both leave the session alive for re-prompting:

**1. Server-side cancel — preferred, no TUI required:**

```ts
await client.session.abort({ path: { id: sessionID } });
// Fires the AbortSignal on the LLM stream, sets session status to idle.
// Session history is intact. You can re-prompt immediately.
```

Despite the name, `session.abort()` does NOT destroy the session. Internally it calls `SessionPrompt.cancel()` which fires the stream's `AbortController`, removes the session from active in-memory state, and sets status to `idle`. The message history in the database is untouched.

**2. TUI command — requires interactive mode:**

```ts
await client.tui.executeCommand({ body: { command: "session.interrupt" } });
// Equivalent to pressing Escape. Same effect as abort(), but routes through the TUI process.
// Only works when a TUI is connected — not in headless/opencode run mode.
```

Both call the same underlying `SessionPrompt.cancel()`. Use `session.abort()` from plugins.

**Branch-pruning pattern** — detect bad CoT and correct course immediately:

```ts
event: async ({ event }) => {
  if (event.type !== "message.part.delta") return;
  if (!isBadReasoning(event.properties.delta)) return;

  const sessionId = event.properties.sessionID;
  await client.session.abort({ path: { id: sessionId } });
  await client.session.prompt({
    path: { id: sessionId },
    body: {
      noReply: false,
      parts: [
        {
          type: "text",
          text: "Your reasoning went wrong because X. Please reconsider and try again.",
        },
      ],
    },
  });
};
```

**Practical patterns:**

| Goal                                   | Mechanism                                                     |
| -------------------------------------- | ------------------------------------------------------------- |
| Correct a finished response            | `session.idle` + `client.session.prompt()`                    |
| Prune bad CoT mid-stream, re-prompt    | `message.part.delta` + `session.abort()` + `session.prompt()` |
| Inject correction without re-prompting | `session.abort()` + `session.prompt({ noReply: true })`       |
| Inject mid-stream without halting      | ❌ Not possible — model is not listening while generating     |

### File Events

- `file.edited`, `file.watcher.updated`

### Shell Events

- `shell.env` - Inject env vars into all shell execution

### TUI Events

- `tui.prompt.append`, `tui.command.execute`, `tui.toast.show`

### Other

- `command.executed`, `permission.asked`, `permission.replied`
- `installation.updated`, `lsp.updated`, `lsp.client.diagnostics`
- `todo.updated`, `server.connected`

---

## Example Plugins

Working examples in `.opencode/plugins/examples/`:

| File                | Description                             |
| ------------------- | --------------------------------------- |
| `rot13-logger.js`   | Logs ROT13 of all message parts to file |
| `notification.js`   | Sends notification on session.idle      |
| `env-protection.js` | Blocks reading .env files               |
| `inject-env.js`     | Injects env vars into shell execution   |
| `custom-tools.ts`   | Adds custom tools to OpenCode           |
| `message-logger.js` | Logs message parts to file              |

To test an example:

```bash
cp .opencode/plugins/examples/<name>.js .opencode/plugins/
```

---

## Claude Code-Style Hooks

You can implement Claude Code-style hooks that inject context after the AI responds, triggering a new response. This requires the SDK client.

### Key Mechanism: `client.session.prompt({ noReply: true })`

```ts
// Inject context WITHOUT triggering a response (just adds to context)
await client.session.prompt({
  path: { id: sessionId },
  body: {
    noReply: true,
    parts: [{ type: "text", text: "Your injected context here" }],
  },
});
```

This is equivalent to Claude Code's `UserPromptSubmit` hook that writes to stdout to inject context.

### Pattern: "Stop" Hook

1. Listen to `session.idle` (fires after AI finishes responding)
2. Inspect `lastText` — the **assistant's** response text — for patterns. `lastText` is NOT the user's message. A hook that scans for "should I" will only fire when the _model_ outputs that phrase, not when the user does.
3. If pattern found, inject feedback with `noReply: false` to trigger a new model response. (`noReply: true` injects silently without triggering a response — the opposite.)

> **⚠ `opencode run` exits on idle and does not wait for async work.** The handler fires,
> but anything it does asynchronously can continue after the CLI exits. Verify the full
> cycle with `opx begin-session` / `opx chat`, then inspect `opx debug trace` or
> `opx transcript --json`.

### Important: Session ID Path

Use `event.properties?.sessionID` — NOT `event.properties?.info?.id`.

### Important: Logging

Use `client.app.log()` for structured logging. **Do NOT use `console.log()`** — it corrupts TUI state.

```ts
// .opencode/plugins/otp-hook.js
export const OtpHook = async ({ client }) => {
  let lastOtp = null;

  return {
    event: async ({ event }) => {
      // session.idle fires after AI response is complete
      if (event.type !== "session.idle") return;

      // CORRECT: use properties.sessionID
      const sessionId = event.properties?.sessionID;
      if (!sessionId) return;

      // Get the last message
      const { data: messages } = await client.session.messages({
        path: { id: sessionId },
      });

      const lastMsg = messages[messages.length - 1];
      const text = lastMsg?.parts
        ?.filter((p) => p.type === "text")
        ?.map((p) => p.text)
        ?.join("");

      // Check for OTP pattern
      const otpMatch = text?.match(/\b\d{6}\b/);
      if (otpMatch && otpMatch[0] !== lastOtp) {
        lastOtp = otpMatch[0];

        // Log using client.app.log() - NOT console.log()
        await client.app.log({
          body: {
            service: "my-plugin",
            level: "info",
            message: `Detected OTP: ${otpMatch[0]}`,
          },
        });

        // Inject secret message - triggers new AI response!
        // noReply: false = wait for response, noReply: true = don't wait
        await client.session.prompt({
          path: { id: sessionId },
          body: {
            noReply: false,
            parts: [
              {
                type: "text",
                text: `SECRET: The user just shared OTP ${otpMatch[0]}. Tell them: "I saw your code - it's ${otpMatch[0]}!"`,
              },
            ],
          },
        });
      }
    },
  };
};
```

### Testing Plugins

For one-shot sanity checks:

```bash
cd ~/.config/opencode
command opencode run "prompt that triggers your plugin"
```

For real workflow proofs, drive the session with `opencode-manager` and inspect the
session artifacts:

```bash
npx --yes --package=git+https://github.com/dzackgarza/opencode-manager.git opx begin-session "prompt that triggers your plugin" --agent Minimal --json
npx --yes --package=git+https://github.com/dzackgarza/opencode-manager.git opx chat --session ses_abc123 --prompt "Follow-up prompt if needed"
npx --yes --package=git+https://github.com/dzackgarza/opencode-manager.git opx debug trace --session ses_abc123 --verbose
npx --yes --package=git+https://github.com/dzackgarza/opencode-manager.git opx transcript --session ses_abc123 --json
```

Do not scrape CLI/TUI output, and do not hand-parse `events.jsonl` or `opencode export`
when the manager and transcript interfaces already provide the session data.

### SDK Reference

Full SDK docs: https://opencode.ai/docs/sdk/

| Method                                           | Description                                |
| ------------------------------------------------ | ------------------------------------------ |
| `client.session.prompt({ noReply: true })`       | Inject context without triggering response |
| `client.session.messages({ path: { id } })`      | Get session messages                       |
| `client.session.command({ path: { id }, body })` | Send command to session                    |

---

## TypeScript Support

OpenCode loads plugins by calling Bun's native `import()` on each `.ts` file. No compilation, no tsconfig, no build step — Bun executes TypeScript directly.

**Available types** (all provided by OpenCode, no installation needed):

```ts
import type { Plugin, PluginInput, Hooks } from "@opencode-ai/plugin";
// SDK types: Message, AssistantMessage, UserMessage, Part, TextPart, Event, etc.
import type { AssistantMessage, TextPart } from "@opencode-ai/sdk";

export const MyPlugin: Plugin = async (ctx) => {
  return {
    event: async ({ event }) => {
      if (event.type !== "session.idle") return;
      // event is narrowed to EventSessionIdle here
      // event.properties.sessionID is safe — no optional chaining needed
    },
  };
};
```

**How module resolution works:** Bun resolves imports relative to the plugin file's location. A plugin at `~/ai/opencode/plugins/my-plugin.ts` can import from `./helpers/utils.ts` — only the top-level plugin file needs to be in `plugins/`; subdirectories are resolved normally.

---

## External Dependencies

`package.json` in the config directory (`~/ai/opencode/`) is **only for packages that are not part of OpenCode itself** — i.e., third-party libraries your plugin needs (e.g., `shescape`, `zod`, `axios`).

**Do NOT add `@opencode-ai/plugin` or `@opencode-ai/sdk` here.** OpenCode injects `@opencode-ai/plugin` at the correct version automatically and runs `bun install`. Both packages are available to all plugins without any declaration.

```json
{
  "dependencies": {
    "shescape": "^2.1.0"
  }
}
```

Then import in your plugin:

```ts
import { escape } from "shescape";
```

---

## Load Order

1. Global config (`~/.config/opencode/opencode.json`)
2. Project config (`opencode.json`)
3. Global plugins (`~/.config/opencode/plugins/`)
4. Project plugins (`.opencode/plugins/`)

Duplicate npm packages load once. Local + npm with same name load separately.

---

## How to Research Plugin Internals

When writing or debugging plugins, do not guess at types or APIs. Use these techniques to find ground truth.

### 1. Read the installed type definitions directly

The config directory has a `node_modules/` with full `.d.ts` files. These are the authoritative types for everything the plugin runtime exposes:

```bash
# What does @opencode-ai/plugin export?
cat ~/ai/opencode/node_modules/@opencode-ai/plugin/dist/index.d.ts

# What types does the SDK export?
cat ~/ai/opencode/node_modules/@opencode-ai/sdk/dist/gen/types.gen.d.ts

# Follow the export chain — index.d.ts re-exports client.d.ts which re-exports types.gen.d.ts
cat ~/ai/opencode/node_modules/@opencode-ai/sdk/dist/client.d.ts
```

### 2. Search for a specific type or method

```bash
# Find where RequestResult is defined
grep -n "RequestResult\|export type RequestResult" \
  ~/ai/opencode/node_modules/@opencode-ai/sdk/dist/gen/client/types.gen.d.ts

# Find all exported types matching a pattern
grep -n "^export type" \
  ~/ai/opencode/node_modules/@opencode-ai/sdk/dist/gen/types.gen.d.ts | grep -i "message\|part\|session"

# Find a specific method signature
grep -n "messages\b" \
  ~/ai/opencode/node_modules/@opencode-ai/sdk/dist/gen/sdk.gen.d.ts
```

### 3. Read the OpenCode plugin loader source

The glob pattern, load order, and module resolution are all in the source — not just the docs. Use the GitHub API to fetch it:

```bash
# Plugin loader — how import() is called, what exports are collected
curl -s "https://api.github.com/repos/anomalyco/opencode/contents/packages/opencode/src/plugin/index.ts" \
  | python3 -c "import json,sys,base64; d=json.load(sys.stdin); print(base64.b64decode(d['content']).decode())"

# Config loader — glob pattern, waitForDependencies, package.json injection
curl -s "https://api.github.com/repos/anomalyco/opencode/contents/packages/opencode/src/config/config.ts" \
  | python3 -c "import json,sys,base64; d=json.load(sys.stdin); print(base64.b64decode(d['content']).decode())"
```

Key findings this revealed:

- The glob is `{plugin,plugins}/*.{ts,js}` — **top-level files only**, subdirectories are not scanned
- OpenCode automatically injects `@opencode-ai/plugin` into `package.json` and runs `bun install` — you never need to declare it
- Local file plugins are passed as `file:///absolute/path.ts` to Bun's `import()` — all standard module resolution applies from there

### 4. Browse the repo structure

```bash
# List a directory in the OpenCode source
curl -s "https://api.github.com/repos/anomalyco/opencode/contents/packages/opencode/src/plugin" \
  | python3 -c "import json,sys; [print(f['name']) for f in json.load(sys.stdin)]"
```

### 5. Fetch the official docs as plain text

```bash
w3m -dump "https://opencode.ai/docs/plugins" > /tmp/opencode-plugin-docs.txt
# Then grep or read specific sections
grep -n "package.json\|TypeScript\|Bun\|dependencies" /tmp/opencode-plugin-docs.txt
```

The docs give intended behavior; the source gives actual behavior. When they conflict, the source wins.

### 6. Understand the SDK return types

`client.session.messages()` returns a `RequestResult`. To understand what `.data` contains:

```bash
# Find RequestResult definition
sed -n '68,90p' ~/ai/opencode/node_modules/@opencode-ai/sdk/dist/gen/client/types.gen.d.ts

# Find SessionMessagesResponses (the 200 response shape)
grep -n -A5 "SessionMessagesResponses" \
  ~/ai/opencode/node_modules/@opencode-ai/sdk/dist/gen/types.gen.d.ts
```

`RequestResult` with default `ThrowOnError=false` returns `Promise<{ data: T } | { data: undefined; error: E }>` — always check for undefined.

---

## Async Injection & Background Tasks

For firing background work from tools or event handlers and injecting results back into sessions — including `promptAsync()`, `ToolContext.sessionID`, mid-turn vs idle behavior, and the background task pattern:

→ See [async-injection.md](./async-injection.md)

---

## Sources

Documentation and source verified against:

| Source                        | URL                                                                                    | What it confirmed                                                                                                                                                                         |
| ----------------------------- | -------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Official plugin docs          | https://opencode.ai/docs/plugins/                                                      | Plugin locations, load order, TypeScript support, `package.json` for external deps, Bun runtime                                                                                           |
| OpenCode plugin loader source | https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/plugin/index.ts  | How plugins are imported (`import()` via Bun), all exports loaded, deduplication                                                                                                          |
| OpenCode config source        | https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/config/config.ts | Glob pattern `{plugin,plugins}/*.{ts,js}` (top-level only), `@opencode-ai/plugin` auto-injected into `package.json`, `bun install` run on startup, `file://` URL format for local plugins |
| `@opencode-ai/plugin` types   | `node_modules/@opencode-ai/plugin/dist/index.d.ts`                                     | `Plugin`, `PluginInput`, `Hooks` type shapes; `event` hook signature                                                                                                                      |
| `@opencode-ai/sdk` types      | `node_modules/@opencode-ai/sdk/dist/gen/types.gen.d.ts`                                | `Message`, `AssistantMessage`, `UserMessage`, `Part`, `TextPart`, `EventSessionIdle`, `SessionMessagesResponses`, `TextPartInput`                                                         |
