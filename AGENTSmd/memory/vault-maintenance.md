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
- retest-model-memory
- retest-model-alignment
- retest-model-tool-use
- retest-policy-change
- retest-toolchain-change
- retest-environment-change
title: Vault Status and Maintenance
---

Before real work on any project — including spikes and small or throwaway projects —
the agent-memory vault must be initialized for that project. There is no size threshold
below which a project skips having a vault-side project folder; a spike still captures
plans and decisions, and those need somewhere durable to live. If the current project
has no `.agent-memory.toml` binding or no vault-side project directory, initialize it
per `agent-memory` before proceeding.

As part of establishing a project, run the agent-memory doctor check:
`uvx --python 3.14 --from git+https://github.com/dzackgarza/agent-memory agent-memory doctor`.
If doctor reports issues, do not hand-patch them inline in the middle of the user's task.
Dispatch a subagent to run the **vault-maintenance workflow** (load `agent-memory`), then
continue the user's work once the vault is healthy.

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
