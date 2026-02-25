---
name: agent-orchestration
description: Use when managing the operational lifecycle of multiple agents, tracking their status, heartbeats, and handling multi-step coordination.
---

# Agent Orchestration 🦞

**By Hal Labs** — Part of the Hal Stack

This skill provides the operational framework for managing and coordinating multiple autonomous agents.

## Reference Skills

**REQUIRED BACKGROUND:** For instructions on how to write or engineering prompts for agents, use:
- **prompt-engineering** — Unified standards for prompt-writing (5-layer architecture, rules, parallelism).

---

## 1. Agent Tracking (No Orphans)

Every spawned agent must be tracked to maintain visibility and prevent context pollution.

Maintain `notes/areas/active-agents.md`:

```markdown
## Currently Running

| Label | Task | Spawned | Expected | Status |
|-------|------|---------|----------|--------|
| research-x | Competitor analysis | 9:00 AM | 15m | 🏃 Running |

## Completed Today

| Label | Task | Runtime | Result |
|-------|------|---------|--------|
| builder-v2 | Dashboard update | 8m | ✅ Complete |
```

## 2. The Heartbeat Check

Periodically audit active sessions to catch stalled or crashed agents:
1. Run `sessions_list --activeMinutes 120`.
2. Compare output to the tracking file.
3. Investigate any missing or stalled agents.
4. Log completions to `LEARNINGS.md`.

## 3. Ralph Mode (Continuous Execution)

For complex tasks where first attempts often fail, use Ralph Mode:
1. **Debug and understand** the failure first.
2. **Try a different approach** rather than repeating the same error.
3. **Research** how others solved similar problems if stuck.
4. **Iterate** until user stories are satisfied.

You have [N] attempts before escalation is required.

## 4. Coordination Strategy

- **Early Phase**: High parallelism (3+ agents) for broad exploration.
- **Middle Phase**: Narrower focus (1-2 agents) for implementation.
- **Late Phase**: Single-agent convergence for verification.

---
*Part of the Hal Stack 🦞*
