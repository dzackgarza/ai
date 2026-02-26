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

### File Events

- `file.edited`, `file.watcher.updated`

### Message Events

- `message.updated`, `message.removed`, `message.part.updated`, `message.part.removed`

### Shell Events

- `shell.env` - Inject env vars into all shell execution

### TUI Events

- `tui.prompt.append`, `tui.command.execute`, `tui.toast.show`

### Other

- `command.executed`, `permission.asked`, `permission.replied`
- `installation.updated`, `lsp.updated`, `lsp.client.diagnostics`
- `todo.updated`, `server.connected`

---

## Concrete Examples

### 1. Send Notifications (session.idle)

```js
// .opencode/plugins/notification.js
export const NotificationPlugin = async ({ $, directory }) => {
  return {
    event: async ({ event }) => {
      if (event.type === "session.idle") {
        await $`osascript -e 'display notification "Session completed!" with title "opencode"'`;
      }
    },
  };
};
```

### 2. Block .env Access (tool.execute.before)

```js
// .opencode/plugins/env-protection.js
export const EnvProtection = async () => {
  return {
    "tool.execute.before": async (input, output) => {
      if (input.tool === "read" && output.args.filePath?.includes(".env")) {
        throw new Error("Do not read .env files");
      }
    },
  };
};
```

### 3. Inject Environment Variables (shell.env)

```js
// .opencode/plugins/inject-env.js
export const InjectEnvPlugin = async () => {
  return {
    "shell.env": async (input, output) => {
      output.env.MY_API_KEY = "secret";
      output.env.PROJECT_ROOT = input.cwd;
    },
  };
};
```

### 4. Custom Tools

```ts
// .opencode/plugins/custom-tools.ts
import { type Plugin, tool } from "@opencode-ai/plugin";

export const CustomToolsPlugin: Plugin = async (ctx) => {
  return {
    tool: {
      mytool: tool({
        description: "This is a custom tool",
        args: {
          foo: tool.schema.string(),
        },
        async execute(args, context) {
          const { directory, worktree } = context;
          return `Hello ${args.foo} from ${directory}`;
        },
      }),
    },
  };
};
```

### 5. Logging

```js
// .opencode/plugins/my-plugin.js
export const MyPlugin = async ({ client }) => {
  await client.app.log({
    body: {
      service: "my-plugin",
      level: "info",
      message: "Plugin initialized",
      extra: { foo: "bar" },
    },
  });
  // Levels: debug, info, warn, error
};
```

### 6. Compaction Hooks (modify context)

```ts
// .opencode/plugins/compaction.ts
import type { Plugin } from "@opencode-ai/plugin";

export const CompactionPlugin: Plugin = async (ctx) => {
  return {
    "experimental.session.compacting": async (input, output) => {
      // Inject additional context
      output.context.push(`
        ## Custom Context
        - Current task status
        - Important decisions made
        - Files being actively worked on
      `);
    },
  };
};
```

### 7. Compaction Hooks (replace prompt)

```ts
// .opencode/plugins/custom-compaction.ts
import type { Plugin } from "@opencode-ai/plugin";

export const CustomCompactionPlugin: Plugin = async (ctx) => {
  return {
    "experimental.session.compacting": async (input, output) => {
      // Replace entire prompt
      output.prompt = `You are generating a continuation prompt...
Summarize:
1. Current task and status
2. Files being modified
3. Blockers or dependencies
4. Next steps`;
    },
  };
};
```

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
