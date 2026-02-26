# OpenCode Plugins

Quick reference for creating and using OpenCode plugins with concrete examples.

---

## Plugin Locations

| Type    | Path                          |
| ------- | ----------------------------- |
| Project | `.opencode/plugins/`          |
| Global  | `~/.config/opencode/plugins/` |

**npm packages** are specified in `opencode.json`:

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

## Events Reference

### Session Events

- `session.created`, `session.deleted`, `session.compacted`
- `session.idle`, `session.error`, `session.updated`, `session.diff`, `session.status`

### Tool Events

- `tool.execute.before` - Modify tool input/output before execution
- `tool.execute.after` - Inspect tool results after execution

### Session Events

- `session.created`, `session.compacted`, `session.deleted`
- `session.idle` - **Equivalent to Claude Code's "Stop" hook** - fires after AI finishes responding
- `session.error`, `session.updated`, `session.diff`, `session.status`

**Note:** `session.idle` is the key event for implementing Claude Code-style hooks that inject context after a response.

### Message Events

- `message.updated`, `message.removed`, `message.part.updated`, `message.part.removed`

**Note:** `message.part.updated` contains text in `event.properties.part.text` (NOT `event.message`).

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
2. Inspect the last message for patterns
3. If pattern found, inject context with `noReply: true` to trigger new response

```ts
// .opencode/plugins/otp-hook.js
export const OtpHook = async ({ client }) => {
  let lastOtp = null;

  return {
    event: async ({ event }) => {
      // session.idle fires after AI response is complete
      if (event.type !== "session.idle") return;

      const sessionId = event.properties?.info?.id;
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

        // Inject secret message - triggers new AI response!
        await client.session.prompt({
          path: { id: sessionId },
          body: {
            noReply: true,
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

### SDK Reference

Full SDK docs: https://opencode.ai/docs/sdk/

| Method                                           | Description                                |
| ------------------------------------------------ | ------------------------------------------ |
| `client.session.prompt({ noReply: true })`       | Inject context without triggering response |
| `client.session.messages({ path: { id } })`      | Get session messages                       |
| `client.session.command({ path: { id }, body })` | Send command to session                    |

---

## TypeScript Support

```ts
import type { Plugin } from "@opencode-ai/plugin";

export const MyPlugin: Plugin = async (ctx) => {
  // Full type safety
};
```

---

## External Dependencies

Add `package.json` to `.opencode/` for external npm packages:

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

## Full Docs

→ https://opencode.ai/docs/plugins/
