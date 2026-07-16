---
name: notebooklm
description: Use when creating or managing Google NotebookLM notebooks from the terminal, adding URL/text/Drive/YouTube/local-file sources, querying a NotebookLM notebook, checking NotebookLM CLI authentication, or diagnosing NotebookLM CLI login/CDP failures.
---
# NotebookLM

Use the current unified NotebookLM CLI through `uvx`; do not rely on a globally installed
binary or the deprecated `notebooklm-cli` package.

## Core Policy

- Run NotebookLM commands as `uvx --from notebooklm-mcp-cli nlm ...`.
- Prefer noun-first commands: `notebook create`, `source add`, `notebook query`.
- Treat NotebookLM operations as external state changes. Create notebooks, add sources,
  rename notebooks, sync sources, or generate artifacts only when the user asked for that
  external change.
- Never delete NotebookLM notebooks or sources without explicit confirmation naming the
  object to delete. Deletion is permanent.
- Use `--json` when output will be parsed or passed to another command.
- Capture notebook IDs and source IDs from create/add/list output; titles are not stable
  implementation handles.

## Authentication

Start with a live auth check when the task depends on NotebookLM access:

```bash
uvx --from notebooklm-mcp-cli nlm login --check
```

If credentials are stale, use the current package login:

```bash
uvx --from notebooklm-mcp-cli nlm login
```

Use profiles only when the user names an account/profile. Do not silently switch profiles
to make a command pass.

## Standard Workflow

Create a notebook:

```bash
uvx --from notebooklm-mcp-cli nlm notebook create "Title"
```

List notebooks and capture an ID:

```bash
uvx --from notebooklm-mcp-cli nlm notebook list --json
```

Add sources. Use `--wait` when the next step queries the source content:

```bash
uvx --from notebooklm-mcp-cli nlm source add <notebook-id> --url "https://example.com" --wait --json
uvx --from notebooklm-mcp-cli nlm source add <notebook-id> --file /path/to/document.pdf --wait --json
uvx --from notebooklm-mcp-cli nlm source add <notebook-id> --text "source text" --title "Source title" --wait --json
uvx --from notebooklm-mcp-cli nlm source add <notebook-id> --drive <drive-id> --type pdf --wait --json
```

Query a notebook non-interactively:

```bash
uvx --from notebooklm-mcp-cli nlm notebook query <notebook-id> "question" --json
```

Use `--conversation-id <id>` for follow-up questions only when continuing the same
NotebookLM chat context is intended. Use `--source-ids <id1,id2>` when the answer must be
restricted to specific sources.

## Environment Traps

- `notebooklm-cli` is the old/deprecated package in this environment. It can expose an
  `nlm` command, but it lacks the current login and source-upload behavior. Use
  `notebooklm-mcp-cli`.
- `--remote-allow-origins` is a Chromium launch flag, not an `nlm` option. If a login
  traceback says Chrome rejected the WebSocket connection and mentions that flag, do not
  pass it to `nlm`.
- A CDP 403 during login usually means another Chrome/Chromium process already owns the
  debug port without the required origin allowance. Retry with the current CLI first; if
  the profile is confused, use `nlm login --clear` only after explaining that it clears the
  localized NotebookLM browser profile for that CLI.
- Do not use `nlm chat start` in agent automation. It opens an interactive REPL. Use
  `nlm notebook query` for one-shot and scriptable questions.
- After adding sources and before querying them, wait for processing with `--wait`; a
  successful add command without `--wait` is not evidence that NotebookLM has indexed the
  source.

## Validation Checklist

- [ ] `uvx --from notebooklm-mcp-cli nlm --version` resolves.
- [ ] `uvx --from notebooklm-mcp-cli nlm login --check` succeeds before stateful work.
- [ ] Notebook/source IDs were captured from live CLI output, not guessed from titles.
- [ ] Source adds that feed immediate queries used `--wait`.
- [ ] Queries use `notebook query`, not the interactive chat REPL.
- [ ] Any delete command has explicit user confirmation for the exact notebook/source.
