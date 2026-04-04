# Next-Steps-Hook Plugin Verification

## Goal

Fix and verify the next-steps-hook plugin behavior: ensure it fires once (not
duplicated), injects correctly, and skips for subagent sessions.

## Completed Work (Commits)

- `b7423e2` — Removed duplicate export from local-tools.ts
- `98681e4` — Added subagent skip (parentID check)
- `5347427` — Added "not completed:" trigger
- `59111b2` — Added "next actions:" alias
- `392286f` — Grammar fix
- `38cc603` — Plugin Placement Rule documentation

## Outstanding Tasks

### 1. Restart OpenCode Server

Plugin changes require server restart to apply.

### 2. Verification Tests

Use repo-local `opencode serve` + `ocm` for controlled tests:
- **Baseline**: One-shot prompt "Reply with only the word 'ready'."
- **Trigger tests**: Sessions ending with trigger phrases ("Acknowledged.", "Not
  completed:")
- **Subagent test**: Confirm plugin skips when parentID is set

### 3. Audit local-tools.ts

Check for other duplicate plugin exports (file was deleted, but verify).

## Subagent Hook Investigation (b1)

- `tool.execute.after` fires when any tool completes, including `task`
- `event` hook + `session.idle` + `parentID` filter also works
- Default task behavior is blocking (sync)
