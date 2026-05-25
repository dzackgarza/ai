# OpenCode Slash Command Design

Slash commands should collect reliable context and present it in a shape the
agent can reason from. They should not try to replace the agent's analysis with
a brittle scripted judgment.

## Design Rules

- Automate simple, deterministic collection: repository shape, docs present,
  language/tool markers, git state, test entry points, and obvious dependency
  manifests.
- Leave synthesis to the agent. Commands should surface evidence and point to
  next reads; they should not claim architectural conclusions from shallow
  signals.
- Start broad, then narrow. A command that begins with `tree`-level orientation
  prevents path-guessing and keyword sampling.
- Fail fast when required tools or directories are missing. Do not silently
  downgrade to a partial report that looks complete.
- Print transparent command output and file paths. The agent must be able to
  audit where each fact came from.
- Keep project-type detection modest. Use detected markers to decide which
  context to show, not to force a fully automated playbook.
- Avoid hard-coded runtime targets. Commands should work from the current
  repository context and use injected OpenCode/session context instead of
  recreating it.

## Good Command Shape

A useful command gives the agent:

- broad file structure,
- nearby docs and agent instructions,
- available recipes and test entry points,
- dependency/config surfaces,
- git dirt and recent activity,
- concise prompts for what to inspect next.

The command is successful when it makes the first real read better targeted; it
is not successful merely because it prints a large report.
