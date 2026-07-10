---
order: 25
tags:
- source-owner-context
- source-system-contract
- source-observed-model-failure
- function-orient
- function-define
- function-constrain
- function-procedure
- function-route
- function-allocate
- failure-state-misplacement
- failure-context-loss
- failure-tool-bypass
- failure-process-overproduction
- retest-model-memory
- retest-model-alignment
- retest-model-tool-use
- retest-policy-change
- retest-toolchain-change
- retest-environment-change
title: Vault Status and Maintenance
---

Initialize and validate the project vault when the task will use durable project memory,
cross-session plans, long-running queues, or project initialization.
A direct answer, bounded edit, data-labeling task, one-off configuration change, or
throwaway spike does not require a project vault merely because it occurs in a repository.

When establishing or using project memory, run the agent-memory doctor check:
`uvx --python 3.14 --from git+https://github.com/dzackgarza/agent-memory agent-memory doctor`.
If doctor reports issues that block the requested memory operation, run the
**vault-maintenance workflow** with `agent-memory` or report the blocker.
Vault defects unrelated to the requested object do not block direct work.

The vault-maintenance workflow includes reconciling harness plan captures into real
agent-memory plans:

- Sort Codex and Claude plan captures (native harness plan/ExecPlan artifacts) into
  proper `plan`-type agent-memory records under their owning project, so plan state
  lives in the central vault rather than as loose harness residue.
- For an **orphaned** plan capture with no clearly associated project, resolve the
  project it belongs to and initialize agent-memory at that project's repository so a
  vault-side project folder exists to hold the plan. Do not drop, merge, or force an
  orphaned plan into an unrelated project to make it fit; give it a real home. If no
  owning project can be determined at all, surface the orphan rather than silently
  discarding it.

Load `agent-memory` for the exact command surface and record shape.
