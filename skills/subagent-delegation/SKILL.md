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
- **Spawned**: Time of agent creation.
- **Expected**: Estimated runtime (if relevant to operation).
- **Status**: 🏃 Running, ✅ Complete, ❌ Blocked.

### Heartbeat Checks (Stall Prevention)
Periodically audit active sessions:
1. Run `sessions_list --activeMinutes 120`.
2. Compare output to tracking file.
3. **Investigate any missing or stalled agents**.
4. Log completions and lessons learned to `LEARNINGS.md`.

### Ralph Mode (Continuous Execution)
For complex tasks where first attempts often fail:
1. **Debug & Understand**: Don't repeat identical errors.
2. **Research**: Find how others solved similar blocks.
3. **Iterate**: Perform N attempts until user stories are satisfied.

---

## 2. Delegation Workflow

### Core Principle: Fresh Context Per Task
Always dispatch a fresh subagent per task + two-stage review (spec then quality) = high quality, fast iteration.

### Forced Two-Stage Review Cycle
Never accept implementation without independent verification:
1. **Spec Compliance**: Dispatch reviewer to confirm code matches the design (no gaps, no extras).
2. **Code Quality**: Dispatch **Code Quality** subagent to verify standards.
3. **CRITICAL**: Never start code quality review before spec compliance is ✅.
4. **Fix Loop**: If review fails, the original subagent (or a fix subagent) iterates until ✅.
5. **Final Review**: Dispatch final code-reviewer for the entire implementation after all tasks are done.

### Parallelism Strategy
- **Early turn (Explore)**: 3+ parallel calls/agents.
- **Middle turn (Build)**: 1-2 targets.
- **Late turn (Verify)**: Single call.

### Parallel Dispatch Strategy (Concurrency)
When facing multiple independent tasks or failures (e.g., different test files, different subsystems without shared state):
1. **Identify Independent Domains**: Group tasks by what is broken/needed. (e.g., File A tests vs File B tests).
2. **Dispatch in Parallel**: Send one focused agent per independent problem domain concurrently.
3. **Agent Prompt Structure**:
   - **Focused**: One clear problem domain.
   - **Self-contained**: Provide all context needed (e.g., specific error messages).
   - **Constraints**: "Fix tests only" or "Do not change unrelated files".
4. **When NOT to use Parallel Dispatch**:
   - Failures are related (fixing one might fix others).
   - Agents would interfere with each other (editing the same shared state/files).
   - Exploratory debugging (you don't know what's broken yet).

---

## 3. Red Flags - STOP and Redirect
- **NEVER:**
  - Start implementation on main/master without explicit user consent.
  - Skip reviews (spec compliance OR code quality).
  - Proceed with unfixed issues.
  - Dispatch multiple implementation subagents in parallel (conflicts).
  - Make subagent read plan file (provide full text instead).
  - Skip scene-setting context.
  - Ignore subagent questions.
  - Accept "close enough" on spec compliance.
  - Skip review loops.
  - Let implementer self-review replace actual review.
  - Move to next task while either review has open issues.
  - Dispatch implementation subagent without first populating **TodoWrite**.
  - Trust agent success reports without fresh verification evidence.

---
*Unified framework combining Operational Management and Delegation Logic.*

## 4. Integration

**Required workflow skills:**
- **using-git-worktrees** - REQUIRED: Set up isolated workspace.
- **Test Guidelines standards** - REQUIRED: All subagents follow high-quality testing guidelines.
- **prompt-engineering** - REQUIRED: Use for all subagent prompt engineering.
