---
name: creating-implementation-plans
description: Use when creating implementation plans that will pass review and execute cleanly. Covers plan structure, task decomposition, verification design, and quality gates.
---

# Creating Implementation Plans

A plan is good when it can be executed by someone who wasn't in the design conversation, produces verifiable results, and doesn't require mid-execution course corrections.

A plan is not a to-do list. It is a **constrained execution specification** that makes success, failure, order, and validation explicit.

## Purpose: What Every Plan Must Answer

Before implementation begins, a plan must let an agent answer:

1. What problem is being solved?
2. What state is considered correct at the end?
3. What must not be changed?
4. What must be true before work can proceed?
5. In what order must work occur?
6. How is each step verified objectively?
7. What conditions force a stop, rollback, or re-scope?

If a plan does not answer those questions, it is **underspecified**.

---

## Planning Workflow

1. **Clarify Requirements**: Identify scope boundaries, constraints, priorities, edge cases, and success criteria. (Ask targeted questions early).
2. **Thorough Research**: Investigate codebase, patterns, and dependencies _before_ drafting tasks.
3. **Draft Phased Plan**: Create atomic tasks, group into logical sprints.
4. **Subagent Review**: Launch a subagent to review the plan for gaps and logic.
5. **Finalize**: Save to `.serena/plans/`.

---

## Core Principles

### 1. Problem-first, not action-first

Begin by identifying:

- The current failure or gap
- The intended target state
- The reason the current state is unacceptable

A plan starting with implementation steps without defining the defect is structurally weak.

### 2. Constraints must be explicit

Name non-negotiable constraints early:

- Required stack or methodology
- Forbidden architectures or approaches
- Interface or compatibility requirements
- Repository, environment, or publication constraints
- Quality gates mandatory before continuation

### 3. Recovery precedes forward progress

If current state is damaged or corrupted, separate:

- Containment
- Recovery
- Resumed implementation

Do not continue feature work on top of uncontained failure state.

### 4. Canonical sources must be identified

State what counts as canonical source material. Rebuilds must proceed from canonical source, not damaged derivatives.

### 5. Ordering must reflect real dependencies

Order by actual enabling conditions, not convenience. Distinguish:

- Prerequisites
- Blocking dependencies
- Independent tasks
- Downstream integration work

A plan is defective if later steps assume artifacts earlier steps don't guarantee.

### 6. Every task must have a completion test

Each task must specify:

- What artifact or state changes
- What condition constitutes completion
- How completion is checked

"Implemented" is not a completion test.

### 7. Validation must be externalized

Validate through observable checks: tests, linters, typecheckers, smoke commands, proof obligations, file inventories, diff checks, reproducible outputs, schema validation, link/build checks.

### 8. Stop rules must exist

State when implementation cannot continue:

- Do not proceed until remote install works
- Do not continue until canonical sources are recovered
- Do not resume until approval is obtained
- Do not migrate downstream consumers until upstream interfaces are stable

### 9. Rollback or fallback must be available

For risky work, define:

- Rollback point
- Fallback artifact or commit
- What is preserved during rollback
- Conditions triggering rollback

### 10. Scope must be complete and explicitly bounded

Identify full target set AND exclusions. Silent omissions produce false completion.

### 11. Interfaces matter more than internals

For multi-repo/tool/phase work, specify:

- What is canonical
- What is wrapper or adapter only
- What invokes what
- What form contracts take
- What runtime or transport is authoritative

### 12. Verification must happen at the level of use

Validate the system as it will actually be used: CLI invocation, import path, rendered document, search result, proof compilation, published artifact, or file layout.

---

## Plan Structure (Required)

### 1. Overview

Brief summary of the task and high-level approach.

### 2. Prerequisites

Any dependencies, requirements, tools, libraries, or access needed _before_ the plan can start.

### 3. Sprints / Phases

Group tasks into logical sprints that build on one another.

- Each sprint must result in a **demoable, runnable, and testable** increment
- Each sprint must have a clear demo/verification checklist

Phase boundaries should represent real stabilization points: recovered source, working standalone artifact, published interface, rewired dependents, final verification.

### 4. Tasks (Decomposed and Actionable)

Task decomposition rule: **Atomic and Committable** (small, independent).

Each task must answer these five questions:

1. **Where** is the change made? (Location: specific file(s)/components)
2. **What** exactly is being changed? (Description)
3. **What must already be true** before this can start? (Dependencies)
4. **What observable condition** marks it done? (Acceptance criteria)
5. **What command, check, or inspection** verifies that? (Validation method)

Per-task complexity estimates are optional. Useful only if they influence ordering, staffing, or risk.

### 5. Testing Strategy

How the overall implementation is proven correct, beyond individual task tests (e.g., integration tests, end-to-end flows).

### 6. Potential Risks & Rollback Plan

- **Risks**: Things that could go wrong
- **Mitigation**: Strategies to handle risks
- **Rollback**: How to undo changes if implementation fails

---

## Minimal Required Fields for Any Plan

A plan is minimally acceptable only if it includes:

### A. Goal and Defect Statement

- Current state/problem
- Target state
- Why the gap matters

### B. Constraints

- Required architecture, method, or output form
- Explicit prohibitions
- Approval gates if applicable

### C. Preconditions / Prerequisites

- Access requirements
- Environment/tooling assumptions
- External dependencies

### D. Scope

- Full set of targets
- Explicit exclusions or archival decisions

### E. Phased Structure

- Ordered phases or milestones
- Clear boundary between recovery, implementation, integration, and verification

### F. Task Specification

For each nontrivial task: location, description, dependencies, acceptance criteria, validation method

### G. System-Level Validation

- End-to-end checks
- Integration checks
- Representative real-use smoke tests

### H. Risk Handling

- Main risks
- Mitigation strategy
- Rollback/fallback path

### I. Stop Rules

Explicit conditions under which work must pause, revert, or require approval

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
- [ ] Each task answers the 5 questions (where, what, prerequisites, done condition, verification)

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

## What a Good Plan Avoids

A plan is structurally weak if it contains:

- Implementation steps without defined target architecture
- Implicit scope with unstated omissions
- "Refactor" or "clean up" tasks without completion tests
- Validation by subjective review alone
- Downstream rewiring before upstream publication/stability
- Continued work on top of known damaged state
- Placeholders treated as acceptable intermediate shipped logic
- Local-only assumptions in workflow meant to validate remote or published use
- No rollback path for destructive or wide-impact work
- No stop rule preventing propagation of invalid assumptions

---

## Common Plan Failures (Anti-patterns)

| Anti-pattern                | What goes wrong                       | Fix                                                |
| --------------------------- | ------------------------------------- | -------------------------------------------------- |
| "Investigate X"             | Unbounded, unverifiable               | "Read `X.ts` and document the 3 entry points"      |
| "Make it work"              | No implementation path                | "Add `validateInput()` at line 47 in `handler.ts`" |
| Task depends on later task  | Causal impossibility                  | Reorder or split the dependency                    |
| Tests only check "not null" | Passes on any non-empty garbage       | "Assert `result.token` is 32-char hex string"      |
| No Rollback Plan            | Destructive actions risk system state | "Define revert migration for schema changes"       |

---

## Domain-Specific Extensions

### Software / Infrastructure

Additional requirements:

- Runtime/stack constraints
- Contract/interface specification
- Lint/type/test gates
- Installability or deployability validation
- Integration tests against real entrypoints
- Migration order for producers before consumers

Useful validations: CLI `--help`, real install, import smoke tests, schema validation, CI reproduction, end-to-end command execution.

### Documentation / Knowledge Base / Writing

Additional requirements:

- Source-of-truth identification
- Intended audience and output format
- Structural completeness criteria
- Citation or reference policy
- Terminology consistency constraints
- Build/render/link validation if published

Useful validations: Style/lint/build passes, link checks, section coverage checklist, factual/source cross-checks, render preview review.

### Mathematics / Research

Additional requirements:

- Exact problem statement
- Current known hypotheses and definitions
- What counts as a result: proof, counterexample, computation, literature inventory, or conjectural outline
- Dependency graph of lemmas/subproblems
- Criteria for a subclaim being established
- Explicit distinction between verified results and speculative directions

Useful validations: Formal proof check, symbolic/algebraic verification, numerical sanity checks, citation to exact sources, consistency with hypotheses, reproducible computation logs.

**Note:** "Investigate X" is not a task. Decompose into concrete outputs: search for exact statements, compute invariant under given hypotheses, test candidate lemma on model examples, or compare two formulations under explicit assumptions.

### File Reorganization / Migration / Archival

Additional requirements:

- Canonical location rules
- Naming conventions
- Move/rename map
- Invariants that must survive reorganization
- Compatibility or redirect strategy for consumers
- Inventory before and after

Useful validations: Manifest diff, path resolution checks, broken-link/import checks, duplicate detection, checksum or content equivalence checks.

---

## Planning Heuristics for LLM Agents

1. **Separate diagnosis from implementation** — If current state may be wrong, first inventory and contain. Don't plan forward migration as though current artifacts are trustworthy.

2. **Prefer objective gates over narrative assurances** — Whenever possible, attach commands, proofs, checks, manifests, or explicit comparisons.

3. **Validate the true deployment/use mode early** — If final system is consumed remotely, published, rendered, compiled, or invoked through wrappers, validate that mode before large downstream work.

4. **Preserve canonical behavior before translating** — When porting systems, define source semantics first and preserve through tests or golden outputs.

5. **Re-scope explicitly when targets changed** — If prior work dropped targets, added extras, or changed approved architecture, plan must re-state scope before more implementation.

6. **Make hidden assumptions visible** — Any assumption whose failure would invalidate later work belongs in prerequisites, dependencies, or stop rules.

7. **Use phases to control propagation** — Phase boundaries should represent real stabilization points.

8. **Require use-level acceptance, not merely internal correctness** — A component is complete when intended consumers can use it successfully under required constraints.

---

## Compact Plan Template

```md
# <Plan Title>

## Goal

- Current defect/state:
- Target state:
- Why this matters:

## Constraints

- Required:
- Forbidden:
- Approval gates:

## Prerequisites

- Access:
- Tools/environment:
- External dependencies:

## Scope

- Included targets:
- Excluded/deprecated targets:

## Phases

### Phase 0: Containment / Recovery

Goal:
Tasks:

- Location:
- Description:
- Dependencies:
- Acceptance criteria:
- Validation:

### Phase 1: Core implementation

...

### Phase N: Integration / Verification

...

## System-Level Validation

- End-to-end checks:
- Real-use smoke checks:

## Risks / Rollback

- Risks:
- Mitigations:
- Rollback path:

## Stop Rules

- Do not proceed if:
```

---

## Final Standard

A plan is **good** if it is:

- **Executable**: Each step names concrete action on concrete target
- **Ordered**: Dependencies and phase boundaries prevent invalid sequencing
- **Falsifiable**: Each task has observable acceptance criteria and validation
- **Stoppable**: Explicit gates prevent drift, compounding errors, and fake completion

Anything less is usually not a plan but a wish list.
