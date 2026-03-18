---
name: creating-implementation-plans
description: Use when creating implementation plans that will pass review and execute cleanly. Covers plan structure, task decomposition, verification design, and quality gates.
---

# Creating Implementation Plans

A plan is good when it can be executed by someone who wasn't in the design conversation, produces verifiable results, and doesn't require mid-execution course corrections.

## Planning Workflow

1.  **Clarify Requirements**: Identify scope boundaries, constraints, priorities, edge cases, and success criteria. (Ask targeted questions early).
2.  **Thorough Research**: Investigate codebase, patterns, and dependencies _before_ drafting tasks.
3.  **Draft Phased Plan**: Create atomic tasks, group into logical sprints.
4.  **Subagent Review**: Launch a subagent to review the plan for gaps and logic.
5.  **Finalize**: Save to `.serena/plans/`.

---

## Plan Structure (Required)

Every plan must include these sections:

### 1. Overview

Brief summary of the task and the high-level approach.

### 2. Prerequisites

Any dependencies, requirements, tools, libraries, or access needed _before_ the plan can start.

### 3. Sprints / Phases

Group tasks into logical sprints that build on one another.

- Each sprint must result in a **demoable, runnable, and testable** increment.
- Each sprint must have a clear demo/verification checklist.

### 4. Tasks (Decomposed and Actionable)

Task decomposition rule: **Atomic and Committable** (small, independent).

Each task must specify:

- **Location**: Specific file(s)/components involved.
- **Description**: What needs to be done.
- **Perceived Complexity**: Score from **1-10**.
- **Dependencies**: Any preceding tasks.
- **Acceptance Criteria**: Specific, testable requirements.
- **Validation**: Test(s) or alternate validation method (command + expected result).

### 5. Testing Strategy

How the overall implementation is proven correct, beyond individual task tests (e.g., integration tests, end-to-end flows).

### 6. Potential Risks & Rollback Plan

- **Risks**: Things that could go wrong.
- **Mitigation**: Strategies to handle risks.
- **Rollback**: How to undo changes if the implementation fails.

---

## Quality Gates

Before a plan is "done," check against these criteria:

### Completeness

- [ ] Goal is specific and measurable
- [ ] Non-goals are stated
- [ ] Edge cases and failure modes are addressed
- [ ] Dependencies between tasks are explicit
- [ ] At least one verification per task

### Actionability

- [ ] Every task names specific files
- [ ] No tasks say "investigate" or "figure out" without bounded scope
- [ ] A developer unfamiliar with the project could start implementing without asking questions
- [ ] Task order is causally possible (no circular dependencies)

### Design Sensibility

- [ ] Complexity is proportionate to the problem
- [ ] No new abstractions without a concrete, current consumer
- [ ] Proposes mature libraries over custom solutions where they exist
- [ ] Design patterns match problem scale (no FactoryFactoryFactory)

### Test Quality

- [ ] Tests prove behavior, not implementation structure
- [ ] Assertions are substantive (`result.status == "approved"`, not `result is not None`)
- [ ] Tests cover real user paths, not just easy-to-test paths
- [ ] Error-path tests use errors that actually occur in production

---

## Common Plan Failures (Anti-patterns)

| Anti-pattern                | What goes wrong                       | Fix                                                |
| --------------------------- | ------------------------------------- | -------------------------------------------------- |
| "Investigate X"             | Unbounded, unverifiable               | "Read `X.ts` and document the 3 entry points"      |
| "Make it work"              | No implementation path                | "Add `validateInput()` at line 47 in `handler.ts`" |
| Task depends on later task  | Causal impossibility                  | Reorder or split the dependency                    |
| Tests only check "not null" | Passes on any non-empty garbage       | "Assert `result.token` is 32-char hex string"      |
| No Rollback Plan            | Destructive actions risk system state | "Define revert migration for schema changes"       |
