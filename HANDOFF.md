# OpenCode plugin support

## Task

Keep OpenCode startup and model selection working on the current stable release.
The startup hang is resolved. Complete support for the configured plugins on the
current API.

## Completion condition

| Requirement | Acceptance | Verified status |
| --- | --- | --- |
| Release | Current stable executable and background service | 2.1.4 |
| Startup | Fresh launch reaches the input prompt with a selected model | Verified |
| Models | Normal background service returns its model list | Verified |
| PTY, Ensemble | Current server entrypoints activate | Active in `/api/plugin` |
| context-mode | Native V2 entrypoint activates and its tools and hooks work | Published 1.0.169 exports the older API; load fails visibly |

## Next work

1. Check context-mode's current upstream release and V2 support. The installed
   entrypoint is `node_modules/context-mode/build/adapters/opencode/plugin.js`.
   It exports `{ id, server }`; OpenCode requires `{ id, effect }` or `{ id, setup }`.
   A native port needs to preserve its tools, routing, and session hooks. Changing
   to MCP-only mode would lose automatic routing and hooks.
2. Validate the chosen native implementation through OpenCode's plugin inventory
   and actual tool and hook execution. This remaining work is separate from the
   resolved package-install startup hang.

Plugin dependencies are installed with `just install-plugins`. Configured local
entrypoint directories are owned by `opencode/configs/config_skeleton.json`.
Use `just build-config` and `opencode reload` to apply source changes. Config build
completes with provider-catalog warnings; those warnings need separate provider
maintenance and do not block startup.
