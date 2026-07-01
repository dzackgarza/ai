---
name: vault-maintenance
description: Use when an agent-memory vault has staged or unstaged changes, commit failures, validation failures, or suspected vault corruption.
---

# Vault Maintenance

The vault should be committed at all times.
Any staged or unstaged vault change outside the currently executing recovery is an ephemeral error state, not ordinary work to preserve on a long-lived branch.

Before normal `agent-memory add`, `update`, `delete`, `search`, or `plan` work resumes, read the relevant reference workflow:

- [Check Vault State](references/check-vault-state.md)
- [Repair Vault Errors](references/repair-vault-errors.md)
- [Commit Vault Work](references/commit-vault-work.md)

## Default Disposition

Uncommitted vault state must become one of:

- a validated vault commit;
- a corrected vault commit after repair;
- a surfaced blocker with the exact dirty paths and failed validation command.

Do not stash, discard, reset, or silently ignore vault changes.
Do not continue normal memory work while the vault is dirty unless the active operation itself is the recovery.
