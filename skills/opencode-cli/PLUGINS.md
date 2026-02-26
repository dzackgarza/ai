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
