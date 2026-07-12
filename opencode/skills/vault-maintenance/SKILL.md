---
name: vault-maintenance
description: Use when an agent-memory command has a commit or validation failure, the vault is malformed, or the user explicitly requests vault recovery. Do not trigger on unrelated dirty paths.
---

# Vault Maintenance

Use this workflow only after:

- an `agent-memory` command reports a commit failure;
- `agent-memory doctor` or `agent-memory plan validate` reports a vault problem; or
- the user explicitly requests vault repair.

## Dispatch

Do not merely report or ignore a recovery trigger: dispatch one dedicated vault-maintenance subagent. It owns inspection, repair, validation, commit, and push of the affected vault paths. Continue unrelated parent work instead of treating that recovery as a blocker.

A dirty vault worktree alone is not a recovery condition. Normal `agent-memory` CRUD is path-scoped: preserve unrelated changes and continue normal memory work.

During actual recovery, read the relevant reference workflow:

- [Check Vault State](references/check-vault-state.md)
- [Repair Vault Errors](references/repair-vault-errors.md)
- [Commit Vault Work](references/commit-vault-work.md)

## Recovery Disposition

The delegated subagent must leave the observed failure as one of:

- a validated, pushed vault commit;
- a corrected, validated, pushed vault commit after repair; or
- an escalated exact-path conflict after identifying the competing authored changes.

Do not stash, discard, reset, or silently ignore changes involved in the actual failure. Do not treat unrelated dirty paths as a blocker.
