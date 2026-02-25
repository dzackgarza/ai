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
Every spawned agent MUST be tracked in `notes/areas/active-agents.md` with:
- **Label**: Unique ID for the session.
- **Task**: Actionable goal.
- **Expected**: Estimated runtime (if relevant to operation).
- **Status**: 🏃 Running, ✅ Complete, ❌ Blocked.

### Heartbeat Checks (Stall Prevention)
Periodically audit active sessions:
1. Run `sessions_list --activeMinutes 120`.
2. Compare output to tracking file.
3. Log completions and lessons learned to `LEARNINGS.md`.

### Ralph Mode (Building for Failure)
For complex tasks where first attempts often fail:
1. **Debug & Understand**: Don't repeat identical errors.
2. **Research**: Find how others solved similar blocks.
3. **Attempt Limit**: You have [N] attempts before escalation.

---

## 2. Delegation Workflow

### Core Principle: Context Isolation
Always dispatch a fresh subagent per task to prevent context switch fatigue and token pollution.

### Two-Stage Review Cycle
Never accept implementation without independent verification:
1. **Spec Compliance**: Dispatch reviewer to confirm code matches the design (no gaps, no extras).
2. **Code Quality**: Dispatch **Code Quality** subagent to verify standards.
3. **Fix Loop**: If review fails, the original subagent (or a fix subagent) iterates until ✅.

### Parallelism Strategy
- **Early turn (Explore)**: 2-3 parallel calls/agents.
- **Middle turn (Build)**: 1-2 targets.
- **Late turn (Verify)**: Single call.

---

## 3. Red Flags - STOP and Redirect
- **Satisfaction before Evidence**: Never say "Great!" or "Done!" before seeing fresh verification output.
- **Proceeding with Issues**: Never move to the next task if the current one has open review feedback.
- **Trusting Success Reports**: Always verify subagent success by checking the actual repository state/diff.
- **Losing the Plan**: Ensure every subagent task is grounded in the overarching implementation plan.

---
*Unified framework combining Operational Management and Delegation Logic.*
