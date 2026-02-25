---
name: subagent-delegation
description: Use when managing the operational lifecycle of multiple agents, delegating tasks to fresh subagent contexts, and coordinating multi-step review-driven workflows.
---

# Subagent Delegation

This skill provides the unified framework for managing, tracking, and coordinating a team of autonomous subagents to execute complex plans with high fidelity.

## Reference Skills
- **prompt-engineering** — REQUIRED: Use for all subagent instruction design.

---

## 1. Operational Lifecycle

### Agent Tracking (No Orphans)
Every spawned agent MUST be tracked to maintain visibility and prevent context pollution. Maintain `notes/areas/active-agents.md` with:
- **Label**: Unique identifier for the agent.
- **Task**: Short description of the objective.
- **Status**: Running, Completed, or Blocked.

### Heartbeat Checks
Periodically audit active sessions to catch stalled or crashed agents:
1. Run `sessions_list --activeMinutes 120`.
2. Compare to tracking file.
3. Resolve missing or stalled sessions.

### Ralph Mode (Resilience)
For complex builds where first attempts may fail:
1. **Debug & Understand** before retry.
2. **Try New Approach** rather than repeating errors.
3. **Research** alternatives if stuck.

---

## 2. Delegation Workflow

### Core Principle: Fresh Context Per Task
Always dispatch a fresh subagent per task to prevent context switch fatigue and token pollution.

### The Two-Stage Review Process
Never accept implementation without a two-stage quality gate:
1. **Spec Compliance Review**: Verify implementation matches the requirements exactly (no under/over-building).
2. **Code Quality Review**: Verify code meets the "Code Quality" agent standards (cleanliness, patterns).

### Coordination Strategy
- **Exploration (Early)**: High parallelism (3+ agents) for broad research.
- **Execution (Middle)**: Target focus (1-2 agents) for implementation.
- **Convergence (Late)**: Single-agent verification and integration.

---

## 3. Red Flags - STOP and Redirect
- **Satisfaction before Evidence**: Never say "Great!" or "Done!" before seeing fresh verification output.
- **Proceeding with Issues**: Never move to the next task if the current one has open review feedback.
- **Trusting Success Reports**: Always verify subagent success by checking the actual repository state/diff.
- **Losing the Plan**: Ensure every subagent task is grounded in the overarching implementation plan.

---
*Unified framework combining Operational Management and Delegation Logic.*
