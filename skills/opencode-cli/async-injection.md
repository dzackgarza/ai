# OpenCode: Async Injection & Background Tasks

Reference for firing background work from plugins and injecting results back into sessions — from tools or event handlers. Researched from SDK types and working plugin examples.

---

## Key APIs

### `client.session.prompt()` vs `client.session.promptAsync()`

| API | Returns | Behavior |
|-----|---------|----------|
| `prompt()` | `{ info: AssistantMessage, parts: Part[] }` | Blocks until the model responds |
| `promptAsync()` | `204 void` | Returns immediately; server queues the prompt |

Use `promptAsync()` for all background work. `prompt()` blocks — calling it from a background task that outlives the agent's turn will hang indefinitely.

Both accept the same body, including `noReply`:

| `noReply` | Effect |
|-----------|--------|
| `false` (default) | Injects message AND triggers a new model response |
| `true` | Injects silently — context only, no response |

### `client.session.abort()`

Cancels in-progress generation. Sets session to `idle`. Does NOT destroy session history. Use when you need to interrupt mid-stream before injecting (see CoT interceptor pattern in PLUGINS.md).

### `client.session.status()`

Returns `{ [sessionID: string]: SessionStatus }` where `SessionStatus` is:

```typescript
{ type: "idle" } | { type: "busy" } | { type: "retry"; attempt: number; message: string; next: number }
```

Use for polling. Prefer the `session.idle` event for reactive patterns.

---

## `ToolContext.sessionID`

`sessionID` is available directly inside `tool.execute()` via the context argument:

```typescript
async execute(args, context) {
  const { sessionID } = context; // Always present — no need to track separately
}
```

Full `ToolContext` shape:

```typescript
type ToolContext = {
  sessionID: string;
  messageID: string;
  agent: string;
  directory: string;
  worktree: string;
  abort: AbortSignal;
  metadata(input: { title?: string; metadata?: { [key: string]: any } }): void;
  ask(input: AskInput): Promise<void>;
};
```

---

## Background Task Pattern (from a Tool)

Fire a task from a tool call without blocking. Inject the result when done.

```typescript
export const MyPlugin: Plugin = async ({ client }) => {
  return {
    tool: {
      my_async_tool: tool({
        description: "Use when ... (triggering condition, not what it does)",
        args: { seconds: tool.schema.number() },
        async execute(args, context) {
          const { sessionID } = context;

          // Fire and forget — do NOT await
          runBackground(sessionID, args.seconds, client).catch(async (err) => {
            // Best-effort error injection
            await client.session.promptAsync({
              path: { id: sessionID },
              body: {
                noReply: false,
                parts: [{ type: "text", text: `[task failed] ${err?.message}` }],
              },
            }).catch(() => {}); // Swallow — session may be gone
          });

          return `Task started. Result will be injected on completion.`;
        },
      }),
    },
  };
};

async function runBackground(sessionID: string, seconds: number, client: any) {
  await new Promise((resolve) => setTimeout(resolve, seconds * 1000));

  await client.session.promptAsync({
    path: { id: sessionID },
    body: {
      noReply: false, // Inject result AND trigger a new model response
      parts: [{ type: "text", text: `[task complete] ${new Date().toISOString()}` }],
    },
  });
}
```

### Mid-turn vs Idle

`promptAsync()` returns 204 immediately regardless of session state. If the session is currently busy (agent mid-turn), the server queues the prompt and processes it when the session becomes idle — the agent is not interrupted. If idle, the prompt fires immediately.

> **Open question:** mid-turn queueing behavior is inferred from the API design
> (`promptAsync` vs `prompt`) and consistent with observed behavior, but not confirmed
> from server source. Verify it with a kept session plus `opx-session messages` or
> `opx debug trace`, not with rendered CLI output.

---

## Testing

Background work requires a session harness that can outlive the first idle and expose the
real session artifacts. Do not use rendered CLI/TUI output as evidence.

```bash
MANAGER="npx --yes --package=git+ssh://git@github.com/dzackgarza/opencode-manager.git"
TRANSCRIPT="npx --yes --package=/home/dzack/opencode-plugins/opencode-manager opx-session transcript"

# Start a repo-local server first when the workflow depends on local config/env
direnv exec /path/to/plugin \
  /home/dzack/.opencode/bin/opencode serve --hostname 127.0.0.1 --port 4198

# Simplest path: keep the session and linger past the first idle
OPENCODE_BASE_URL=http://127.0.0.1:4198 $MANAGER opx run \
  --agent Minimal \
  --prompt "Trigger the async workflow here" \
  --linger 10 \
  --keep

# Full control: create and drive the session explicitly
OPENCODE_BASE_URL=http://127.0.0.1:4198 $MANAGER opx-session create --title "async-test"
OPENCODE_BASE_URL=http://127.0.0.1:4198 $MANAGER opx-session prompt ses_abc123 "Trigger the async workflow here" --no-reply

# Inspect the real session instead of scraping terminal output
OPENCODE_BASE_URL=http://127.0.0.1:4198 $MANAGER opx-session messages ses_abc123 --json
OPENCODE_BASE_URL=http://127.0.0.1:4198 $MANAGER opx debug trace --session ses_abc123 --verbose
OPENCODE_BASE_URL=http://127.0.0.1:4198 $TRANSCRIPT ses_abc123
```

Use `opx-session messages --json` or `opx debug trace` when you need raw evidence for
callback delivery, a resumed turn, or an assistant error.

---

## Sources

| File | What it confirms |
|------|-----------------|
| `node_modules/@opencode-ai/plugin/dist/tool.d.ts` | `ToolContext` shape including `sessionID`, `messageID`, `abort` |
| `node_modules/@opencode-ai/sdk/dist/gen/sdk.gen.d.ts` | `prompt()`, `promptAsync()`, `abort()`, `status()` method signatures |
| `node_modules/@opencode-ai/sdk/dist/gen/types.gen.d.ts` | `SessionPromptData`, `SessionPromptAsyncData`, `SessionStatus`, `noReply` |
| `plugins/async-command.ts` | Working implementation of background tool with result injection |
| `plugins/stop-hooks.ts` | Idle-only injection via `session.idle` event |
| `plugins/cot-trivial-test.ts` | Mid-stream abort + re-prompt via `message.part.delta` |
