---
name: opencode-plugin-development
description: Use when developing OpenCode plugins with hooks, custom tools, and event handling.
---

# OpenCode Plugin Development

Develop TypeScript plugins that extend OpenCode agent behavior with hooks, custom tools, and event handling.

## Quick Start

1. Create a single TypeScript file in `~/ai/opencode/plugin/`. Do not include a `package.json` file.
2. Export a named plugin function
3. Restart OpenCode

```ts
import type { Plugin } from "@opencode-ai/plugin";

export const MyPlugin: Plugin = async ({ client }) => {
  console.log("Plugin loaded!");

  return {
    // hooks go here
  };
};
```

## Plugin Location: Local vs External

**Local plugins** (inline TypeScript, <200LOC):

- Location: `~/ai/opencode/plugin/` (global, NOT project-local `.opencode/`)
- No `package.json` needed
- Restart OpenCode to reload

**External plugins** (refactored, >200LOC):

- Always in their own git repo under `/home/dzack/opencode-plugins/`
- NEVER use `file://` directives — always use `git+https://`
- NEVER pin to a specific branch or commit — always use default branch
- The `git+https://` URL without a ref pulls the default branch automatically

```json
// In opencode.json — use default branch, never specific commit/branch
{
  "plugins": [
    "git+https://github.com/dzackgarza/opencode-plugins.git/my-plugin"
  ]
}
```

**Why:** Local plugins in project directories get lost or shadowed. External plugins with `file://` directives couple to local paths. Git-sourced plugins with pinned commits become stale. Using default-branch `git+https://` ensures live latest version is always correct.

**CRITICAL**: The plugin function receives a **context object**, not individual parameters.

```ts
// ✅ CORRECT - destructure what you need
export const MyPlugin: Plugin = async ({ client, project, $, directory }) => {
  await client.session.prompt({ ... })
}

// ❌ WRONG - treating context as client
export const MyPlugin: Plugin = async (client) => {
  await client.session.prompt({ ... })  // FAILS: context.session.prompt doesn't exist
}
```

### Context Object Properties

| Property    | Type       | Description                  |
| ----------- | ---------- | ---------------------------- |
| `client`    | SDK Client | OpenCode SDK for API calls   |
| `project`   | Project    | Current project info         |
| `directory` | string     | Current working directory    |
| `worktree`  | string     | Git worktree path            |
| `$`         | Shell      | Bun's shell API for commands |

## Available Hooks

### Event Hook

Subscribe to system events:

```ts
event: async ({ event }) => {
  if (event.type === "session.created") {
    // New session started
  }
  if (event.type === "session.idle") {
    // Agent finished responding
  }
  if (event.type === "message.updated") {
    // Message added/changed
  }
};
```

**Event Types:**

- `session.created`, `session.deleted`, `session.idle`, `session.error`, `session.compacted`
- `message.updated`, `message.removed`, `message.part.updated`
- `tool.execute.before`, `tool.execute.after`
- `file.edited`, `file.watcher.updated`
- `permission.updated`, `permission.replied`

### Stop Hook

Intercept agent stop attempts:

```ts
stop: async (input) => {
  const sessionId = input.sessionID || input.session_id;

  if (!workComplete) {
    await client.session.prompt({
      path: { id: sessionId },
      body: {
        parts: [{ type: "text", text: "Please complete X before stopping." }],
      },
    });
  }
};
```

### Tool Execution Hooks

Intercept tool calls before/after execution:

```ts
"tool.execute.before": async (input, output) => {
  // Block dangerous commands
  if (input.tool === "bash" && output.args.command.includes("rm -rf")) {
    throw new Error("Dangerous command blocked")
  }
}

"tool.execute.after": async (input) => {
  // React to completed tool calls
  if (input.tool === "edit") {
    console.log(`File edited: ${input.args.filePath}`)
  }
}
```

### System Prompt Transform

Inject context into the system prompt:

```ts
"experimental.chat.system.transform": async (input, output) => {
  output.system.push(`<custom-context>
    Important project rules go here.
  </custom-context>`)
}
```

### Compaction Hook

Preserve state when sessions are compacted:

```ts
"experimental.session.compacting": async (input, output) => {
  output.context.push(`<preserved-state>
    Task progress: 75%
    Files modified: src/main.ts
  </preserved-state>`)
}
```

### Custom Tools

Add tools the agent can use:

```ts
import { tool } from "@opencode-ai/plugin";

return {
  tool: {
    myTool: tool({
      description: "Does something useful",
      args: {
        input: tool.schema.string(),
        count: tool.schema.number().optional(),
      },
      async execute(args, ctx) {
        return `Processed: ${args.input}`;
      },
    }),
  },
};
```

## Session State Management

Track state across a session using Maps keyed by session ID:

```ts
interface SessionState {
  filesModified: string[];
  commitMade: boolean;
}

const sessions = new Map<string, SessionState>();

function getState(sessionId: string): SessionState {
  let state = sessions.get(sessionId);
  if (!state) {
    state = { filesModified: [], commitMade: false };
    sessions.set(sessionId, state);
  }
  return state;
}

export const MyPlugin: Plugin = async ({ client }) => {
  return {
    event: async ({ event }) => {
      const sessionId = (event as any).session_id || (event as any).sessionID;

      if (event.type === "session.created" && sessionId) {
        sessions.set(sessionId, { filesModified: [], commitMade: false });
      }

      if (event.type === "session.deleted" && sessionId) {
        sessions.delete(sessionId);
      }
    },

    "tool.execute.after": async (input) => {
      const state = getState(input.sessionID);

      if (input.tool === "edit" || input.tool === "write") {
        state.filesModified.push(input.args.filePath as string);
      }

      if (
        input.tool === "bash" &&
        /git commit/.test(input.args.command as string)
      ) {
        state.commitMade = true;
      }
    },

    stop: async (input) => {
      const sessionId = (input as any).sessionID || (input as any).session_id;
      const state = getState(sessionId);

      if (state.filesModified.length > 0 && !state.commitMade) {
        await client.session.prompt({
          path: { id: sessionId },
          body: {
            parts: [{ type: "text", text: "You have uncommitted changes!" }],
          },
        });
      }
    },
  };
};
```

## Common Patterns

### Detect User-Provided Images

```ts
event: async ({ event }) => {
  if (event.type === "message.updated") {
    const message = (event as any).properties?.message;
    if (message?.role === "user") {
      const content = JSON.stringify(message.content || "");
      if (
        content.includes("image/") ||
        /\.(png|jpg|jpeg|gif|webp)/i.test(content)
      ) {
        // User provided an image
      }
    }
  }
};
```

### Track File Modifications

```ts
"tool.execute.after": async (input) => {
  if (input.tool === "edit" || input.tool === "write") {
    const filePath = input.args.filePath as string
    // Track the modification
  }
}
```

### Enforce Verification Before Commit

```ts
"tool.execute.before": async (input, output) => {
  if (input.tool === "bash" && /git commit/.test(output.args.command as string)) {
    if (!state.testsRan) {
      throw new Error("Run tests before committing!")
    }
  }
}
```

## Using External Dependencies

To use external npm packages in your single-file plugin, add the dependency to `opencode/package.json` in the root repository. OpenCode will resolve and make these available to your plugin at runtime.

## Running Shell Commands

Use Bun's shell API via `$`:

```ts
export const MyPlugin: Plugin = async ({ $ }) => {
  return {
    "tool.execute.after": async (input) => {
      if (input.tool === "edit" && input.args.filePath.endsWith(".rs")) {
        // Run cargo fmt after Rust file edits
        const result = await $`cargo fmt --check`.quiet();
        if (result.exitCode !== 0) {
          console.log("Formatting issues detected");
        }
      }
    },
  };
};
```

## Logging

Use structured logging instead of console.log:

```ts
await client.app.log({
  service: "my-plugin",
  level: "info", // debug, info, warn, error
  message: "Something happened",
  extra: { key: "value" },
});
```

## Plugin Load Order

1. Global config (`~/.config/opencode/opencode.json`)
2. Project config (`./opencode.json`)
3. Plugin directory (`~/ai/opencode/plugin/` - which is symlinked to `~/.config/opencode/plugin/`. Always use the `~/ai/` path for version control.)

All hooks from all plugins run in sequence.

## Debugging Tips

1. **Plugin not loading?** Check for TypeScript errors — syntax errors prevent loading
2. **Hooks not firing?** Verify the hook name matches exactly (case-sensitive)
3. **State not persisting?** Use session-keyed Maps, not global variables
4. **client.session.prompt failing?** Check your destructuring: `async ({ client })` not `async (client)`

## Key Runtime Facts

- `ToolContext` exposes `sessionID`, `messageID`, `agent`, `directory`, `worktree`, `abort`, and `metadata()`
- The real session id is `event.properties.sessionID`, not `event.properties.info.id`
- `session.idle` fires after every response. If you re-prompt, expect another idle
- Reasoning streams through `message.part.updated` plus `message.part.delta`, same as text
- Never `console.log()` inside a plugin. Use `client.app.log(...)`

## References

- See `GUIDE.md` for repo workflow rules and proof design
- See `AUDIT.md` for compliance checklist before PR
- See `references/README_STANDARDS.md` for documentation templates
