---
name: codex
description: "Delegate coding to OpenAI Codex CLI (features, PRs)."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Coding-Agent, Codex, OpenAI, Code-Review, Refactoring]
    related_skills: [[[claude-code/SKILL|claude-code]], [[hermes-agent/SKILL|hermes-agent]]]
---
# Codex CLI

Delegate coding tasks to [Codex](https://github.com/openai/codex) via the Hermes
terminal. Codex is OpenAI’s autonomous coding agent CLI.

## When to use

- Building features

- Refactoring

- PR reviews

- Batch issue fixing

Requires the codex CLI and a git repository.

## Prerequisites

- Codex installed: `npm install -g @openai/codex`

- OpenAI auth configured: either `OPENAI_API_KEY` or Codex OAuth credentials from the
  Codex CLI login flow

- **Must run inside a git repository** — Codex refuses to run outside one

- Use `pty=true` in terminal calls — Codex is an interactive terminal app

For Hermes itself, `model.provider: openai-codex` uses Hermes-managed Codex OAuth from
`~/.hermes/auth.json` after `hermes auth add openai-codex`. For the standalone Codex
CLI, a valid CLI OAuth session may live under `~/.codex/auth.json`; do not treat a
missing `OPENAI_API_KEY` alone as proof that Codex auth is missing.

## One-Shot Tasks

```
terminal(command="codex exec 'Add dark mode toggle to settings'", workdir="~/project", pty=true)
```

For scratch work (Codex needs a git repo):
```
terminal(command="cd $(mktemp -d) && git init && codex exec 'Build a snake game in Python'", pty=true)
```

## Background Mode (Long Tasks)

```
# Start in background with PTY
terminal(command="codex exec --full-auto 'Refactor the auth module'", workdir="~/project", background=true, pty=true)
# Returns session_id

# Monitor progress
process(action="poll", session_id="<id>")
process(action="log", session_id="<id>")

# Send input if Codex asks a question
process(action="submit", session_id="<id>", data="yes")

# Kill if needed
process(action="kill", session_id="<id>")
```

## Key Flags

| Flag | Effect |
| --- | --- |
| `exec "prompt"` | One-shot execution, exits when done |
| `--full-auto` | Sandboxed but auto-approves file changes in workspace |
| `--yolo` | No sandbox, no approvals (fastest, most dangerous) |

## PR Reviews

Clone to a temp directory for safe review:

```
terminal(command="REVIEW=$(mktemp -d) && git clone https://github.com/user/repo.git $REVIEW && cd $REVIEW && gh pr checkout 42 && codex review --base origin/main", pty=true)
```

### PR Feedback Loop (2026-07-13)

As of 2026-07-13, Codex has no native inbound session-wakeup capability. Do not use `at`
or `task-sched` expecting either to resume a Codex session.

For a short known wait, sleep 60–120 seconds and re-check the PR through GitHub with `gh
pr checks` and the repository’s review-feedback scan.

For a longer external wait, use a one-off script in a PTY: have it check the PR at a
reasonable interval, exit immediately when new relevant information arrives, and set a
finite long-horizon timeout. Codex can go idle while its PTY process runs and resumes when
that process exits. This is a task-local substitute for a scheduled wakeup, not a
persistent timer: terminate it when the PR loop ends, and do not claim Codex is listening
for a callback.

## Parallel Issue Fixing with Worktrees

```
# Create worktrees
terminal(command="git worktree add -b fix/issue-78 /tmp/issue-78 main", workdir="~/project")
terminal(command="git worktree add -b fix/issue-99 /tmp/issue-99 main", workdir="~/project")

# Launch Codex in each
terminal(command="codex --yolo exec 'Fix issue #78: <description>. Commit when done.'", workdir="/tmp/issue-78", background=true, pty=true)
terminal(command="codex --yolo exec 'Fix issue #99: <description>. Commit when done.'", workdir="/tmp/issue-99", background=true, pty=true)

# Monitor
process(action="list")

# After completion, push and create PRs
terminal(command="cd /tmp/issue-78 && git push -u origin fix/issue-78")
terminal(command="gh pr create --repo user/repo --head fix/issue-78 --title 'fix: ...' --body '...'")

# Cleanup
terminal(command="git worktree remove /tmp/issue-78", workdir="~/project")
```

## Batch PR Reviews

```
# Fetch all PR refs
terminal(command="git fetch origin '+refs/pull/*/head:refs/remotes/origin/pr/*'", workdir="~/project")

# Review multiple PRs in parallel
terminal(command="codex exec 'Review PR #86. git diff origin/main...origin/pr/86'", workdir="~/project", background=true, pty=true)
terminal(command="codex exec 'Review PR #87. git diff origin/main...origin/pr/87'", workdir="~/project", background=true, pty=true)

# Post results
terminal(command="gh pr comment 86 --body '<review>'", workdir="~/project")
```

## Rules

1. **Always use `pty=true`** — Codex is an interactive terminal app and hangs without a
   PTY

2. **Git repo required** — Codex won’t run outside a git directory.
   Use `mktemp -d && git init` for scratch

3. **Use `exec` for one-shots** — `codex exec "prompt"` runs and exits cleanly

4. **`--full-auto` for building** — auto-approves changes within the sandbox

5. **Background for long tasks** — use `background=true` and monitor with `process` tool

6. **Don’t interfere** — monitor with `poll`/`log`, be patient with long-running tasks

7. **Parallel is fine** — run multiple Codex processes at once for batch work
