---
name: chrome-devtools-mcp
description: Use when debugging, inspecting, or automating a Chrome/Chromium browser from the terminal with ChromeDevTools chrome-devtools-mcp, especially when the user asks for npx usage, browser snapshots, screenshots, Lighthouse audits, page navigation, or agent-generated browser scripts. Prefer this skill over global install advice whenever the task can run through ephemeral npx.
---
# Chrome DevTools MCP CLI

Use the ChromeDevTools `chrome-devtools-mcp` package as an ephemeral CLI dependency.
Do not install it globally unless the user explicitly asks for a persistent command.

Primary command shape:

```bash
npx -y --package chrome-devtools-mcp@latest chrome-devtools <tool> [arguments] [flags]
```

The package exposes two binaries. `chrome-devtools-mcp` starts the MCP server.
`chrome-devtools` is the generated terminal CLI for browser actions. With `npx`, call
the non-default `chrome-devtools` binary through `--package`.

## First Checks

Verify Node is compatible before debugging package failures:

```bash
node --version
```

The upstream package currently requires Node `^20.19.0 || ^22.12.0 || >=23`.

Check the CLI without making it a project dependency:

```bash
npx -y --package chrome-devtools-mcp@latest chrome-devtools status
```

If the command starts a browser daemon, stop it when the task is done:

```bash
npx -y --package chrome-devtools-mcp@latest chrome-devtools stop
```

## Working Pattern

For repeated commands in one shell, define a short-lived shell function:

```bash
cdt() {
  npx -y --package chrome-devtools-mcp@latest chrome-devtools "$@"
}

cdt status
cdt list_pages --output-format=json
```

Use JSON output for agent scripts and parsing:

```bash
npx -y --package chrome-devtools-mcp@latest chrome-devtools list_pages --output-format=json
```

## Browser Lifecycle

The CLI talks to a background `chrome-devtools-mcp` daemon.
The first browser tool call can start the daemon and browser automatically.
Subsequent commands reuse the same background browser state.

Manage the daemon explicitly when state matters:

```bash
npx -y --package chrome-devtools-mcp@latest chrome-devtools status
npx -y --package chrome-devtools-mcp@latest chrome-devtools start --headless
npx -y --package chrome-devtools-mcp@latest chrome-devtools stop
```

`start` forwards supported server arguments to the MCP server. Confirm current support
from the package before relying on a flag:

```bash
npx -y --package chrome-devtools-mcp@latest chrome-devtools start --help
```

Headless mode is enabled by default. Browser isolation is enabled by default unless a
`--userDataDir` is provided.

## Common Commands

Open and navigate pages:

```bash
npx -y --package chrome-devtools-mcp@latest chrome-devtools new_page "https://example.com"
npx -y --package chrome-devtools-mcp@latest chrome-devtools navigate_page "https://web.dev" --type url
```

Capture page state:

```bash
npx -y --package chrome-devtools-mcp@latest chrome-devtools list_pages --output-format=json
npx -y --package chrome-devtools-mcp@latest chrome-devtools take_snapshot --output-format=json
npx -y --package chrome-devtools-mcp@latest chrome-devtools take_screenshot --filePath screenshot.png
```

Interact with elements using UIDs from a snapshot:

```bash
npx -y --package chrome-devtools-mcp@latest chrome-devtools click "element-uid-123"
npx -y --package chrome-devtools-mcp@latest chrome-devtools fill "input-uid-456" "search query"
```

Run Lighthouse when a browser-side performance/accessibility check is required:

```bash
npx -y --package chrome-devtools-mcp@latest chrome-devtools lighthouse_audit --mode snapshot --output-format=json
```

## Limits

The terminal CLI exposes generated commands for MCP tools that fit the CLI argument
model. Tools that require unsupported extra server categories are not available through
the CLI. Upstream also excludes some generated commands, including `wait_for` and
`fill_form`.

When a CLI command is missing, use the MCP server through a configured MCP client or
check the upstream tool reference before inventing a local wrapper.

## Troubleshooting

If the CLI hangs or cannot connect, stop the daemon and retry the smallest command:

```bash
npx -y --package chrome-devtools-mcp@latest chrome-devtools stop
npx -y --package chrome-devtools-mcp@latest chrome-devtools status
```

For verbose logs, export `DEBUG` in the shell instead of setting it inline:

```bash
export DEBUG='*'
npx -y --package chrome-devtools-mcp@latest chrome-devtools list_pages
unset DEBUG
```

Do not hide stderr while diagnosing CLI, browser, or package failures. Preserve the
command, stdout, stderr, exit code, Node version, and whether a daemon was already
running.

## Sources

- CLI contract: https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/cli.md
- Package bins and Node engine: https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/package.json
