---
name: creating-implementation-plans
description: Use when creating implementation plans that will pass review and execute cleanly. Covers self-contained living-document plans, plan structure, task decomposition, milestones, verification design, and quality gates.
---
# Creating Implementation Plans

> [!IMPORTANT]
> All implementation plans created under this skill must adhere to the [Bridge-Burning Policies](file:///home/dzack/ai/opencode/skills/policy-index/SKILL.md#policy-registry) in `policy-index/SKILL.md`. These are non-negotiable hard constraints that eliminate runtime defaults, fallbacks, mocks, optional critical dependencies, and other agent validation-evasion pathways. Plans must specify how these constraints are enforced for the target code.

A plan is good when it can be executed by someone who wasn’t in the design conversation,
produces verifiable results, and doesn’t require mid-execution course corrections.

A plan is not a to-do list.
It is a **constrained execution specification** that makes success, failure, order, and
validation explicit.

## Self-Containment and Living Documents

Write every plan so a contributor with no prior context — only the current working tree
and this one plan file — can implement it end to end. A plan must be restartable from
itself alone: if every other note vanished, the plan still carries everything needed to
finish.

- Embed required knowledge in the plan, in your own words. Do not link to external blogs
  or docs, and do not write "as defined previously" or "see the architecture doc."
  Repeat any assumption you rely on, even at the cost of redundancy.

- Define every term of art in plain language at first use, or do not use it. When you
  name a non-obvious concept ("daemon", "middleware", "adapter"), state immediately how
  it manifests here — which files or commands embody it.

- If the plan builds on a prior plan checked into the repo, incorporate it by reference
  to its repository-relative path. If that prior plan is not checked in, copy the
  relevant context into this plan.

- Do not outsource key decisions to the reader. When ambiguity exists, resolve it in the
  plan and explain why you chose that path, rather than leaving the implementer to guess.

A plan is a living document, not a frozen spec. Revise it as work proceeds, as
discoveries occur, and as decisions are finalized; every revision must remain
self-contained. At each stopping point, update the plan to state the progress made and
the next steps — split a partly done task into a "done" part and a "remaining" part
rather than leaving its status ambiguous. Record not just what changed but why: it must
always be unambiguous why any change to the plan was made. After revising, append a short
note at the end of the plan stating what changed and the reason.

To hold this discipline, every plan carries four standing sections that are updated
throughout execution, not written once: `Progress`, `Surprises & Discoveries`,
`Decision Log`, and `Outcomes & Retrospective`. Their formats are defined under
[Living-Document Sections](#living-document-sections-required) below.

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

* * *

## Planning Workflow

1. **Clarify Requirements**: Identify scope boundaries, constraints, priorities, edge
   cases, and success criteria.
   (Ask targeted questions early).

2. **Thorough Research**: Investigate codebase, patterns, and dependencies *before*
   drafting tasks.

3. **Draft Phased Plan**: Create atomic tasks, group into logical sprints.

4. **Subagent Review**: Launch a subagent to review the plan for gaps and logic.

5. **Finalize**: Save to `.hermes/plans/`.

* * *

## Core Principles

### 1. Problem-first, not action-first

Begin by identifying:

- The current failure or gap

- The intended target state

- The reason the current state is unacceptable

A plan starting with implementation steps without defining the defect is structurally
weak.

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

State what counts as canonical source material.
Rebuilds must proceed from canonical source, not damaged derivatives.

### 5. Ordering must reflect real dependencies

Order by actual enabling conditions, not convenience.
Distinguish:

- Prerequisites

- Blocking dependencies

- Independent tasks

- Downstream integration work

A plan is defective if later steps assume artifacts earlier steps don’t guarantee.

### 6. Every task must have a completion test

Each task must specify:

- What artifact or state changes

- What condition constitutes completion

- How completion is checked

“Implemented” is not a completion test.

### 7. Validation must be externalized

Validate through observable checks: tests, linters, typecheckers, smoke commands (must not be proof-free smoke tests, see Policy 5), proof
obligations, file inventories, diff checks, reproducible outputs, schema validation,
link/build checks.

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

Steps should also be safely repeatable: write them so running the plan again causes no
damage or drift. If a step can fail halfway, state how to retry or recover; for a
destructive or migrating step, spell out the backup or safe fallback first.

### 10. Scope must be complete and explicitly bounded

Identify full target set AND exclusions.
Silent omissions produce false completion.

### 11. Interfaces matter more than internals

For multi-repo/tool/phase work, specify:

- What is canonical

- What is wrapper or adapter only

- What invokes what

- What form contracts take

- What runtime or transport is authoritative

### 12. Verification must happen at the level of use

Validate the system as it will actually be used: CLI invocation, import path, rendered
document, search result, proof compilation, published artifact, or file layout.

### 13. Purpose and observable behavior come first

Open the plan by explaining, in a few sentences, why the work matters from a user's
perspective: what someone can do after the change that they could not before, and how to
see it working. Phrase acceptance as behavior a human can verify ("after starting the
server, GET /health returns 200 with body OK"), not internal attributes ("added a
HealthCheck struct"). The plan must produce demonstrably working behavior, not code that
satisfies the letter of a definition while doing nothing meaningful. For a purely
internal change, show impact another way: a test that fails before and passes after, plus
a scenario that exercises the new behavior.

### 14. Record evidence that proves success

When steps produce terminal output, short diffs, or logs that demonstrate the change
works, capture concise excerpts in the plan. Prefer file-scoped diffs or small snippets a
reader can recreate by following the steps over large pasted blobs. Evidence is what
lets a later reader distinguish real success from a green checkmark.

* * *

## Plan Structure (Required)

### 1. Overview

Brief summary of the task and high-level approach.

### 2. Prerequisites

Any dependencies, requirements, tools, libraries, or access needed *before* the plan can
start.

### 3. Sprints / Phases

Group tasks into logical sprints that build on one another.

- Each sprint must result in a **demoable, runnable, and testable** increment

- Each sprint must have a clear demo/verification checklist

Phase boundaries should represent real stabilization points: recovered source, working
standalone artifact, published interface, rewired dependents, final verification.

### 4. Tasks (Decomposed and Actionable)

Task decomposition rule: **Atomic and Committable** (small, independent).

Each task must answer these five questions:

1. **Where** is the change made?
   (Location: specific file(s)/components)

2. **What** exactly is being changed?
   (Description)

3. **What must already be true** before this can start?
   (Dependencies)

4. **What observable condition** marks it done?
   (Acceptance criteria)

5. **What command, check, or inspection** verifies that?
   (Validation method)

Per-task complexity estimates are optional.
Useful only if they influence ordering, staffing, or risk.

### 5. Testing Strategy

How the overall implementation is proven correct, beyond individual task tests (e.g.,
integration tests, end-to-end flows).

### 6. Potential Risks & Rollback Plan

- **Risks**: Things that could go wrong

- **Mitigation**: Strategies to handle risks

- **Rollback**: How to undo changes if implementation fails

* * *

## Milestones

Milestones tell the story of the work; the `Progress` checklist tracks granular steps.
Both must exist and they are distinct. Introduce each milestone with a short paragraph
giving its scope, what will exist at the end that did not before, the commands to run,
and the acceptance you expect to observe — goal, work, result, proof. Each milestone must
be independently verifiable and must move the overall goal forward incrementally. Do not
abbreviate a milestone for brevity; detail omitted here becomes a gap for the next
contributor.

### Prototyping milestones

When requirements carry significant unknowns, include an explicit prototyping milestone
that builds a proof of concept or toy implementation to test feasibility before
committing to a full build. Read the source of any library you depend on — find or
acquire it — rather than guessing at its behavior. Keep prototypes additive and testable,
label their scope as prototyping, describe how to run and observe them, and state the
criteria for promoting the prototype to real work or discarding it. When several new
libraries or feature areas are involved, prototype each in isolation (a "spike") to prove
it works on its own before integrating them.

### Parallel implementations during migration

Parallel implementations are acceptable when they reduce risk: keep an adapter alongside
an older path during a migration so tests keep passing, then retire the old path once the
new one is proven. Prefer additive changes first, then subtractions that keep tests
green. Describe how to validate both paths and how to remove one safely with the suite
still passing.

* * *

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

For each nontrivial task: location, description, dependencies, acceptance criteria,
validation method

### G. System-Level Validation

- End-to-end checks

- Integration checks

- Representative real-use smoke tests (must be real, proof-bearing boundary tests or diagnostic commands, not proof-free smoke tests per Policy 5)

### H. Risk Handling

- Main risks

- Mitigation strategy

- Rollback/fallback path

### I. Stop Rules

Explicit conditions under which work must pause, revert, or require approval

* * *

## Quality Gates

Before a plan is “done,” check against these criteria:

### Completeness

- [ ] Goal is specific and measurable

- [ ] Non-goals are stated

- [ ] Edge cases and failure modes are addressed

- [ ] Dependencies between tasks are explicit

- [ ] At least one verification per task

### Actionability

- [ ] Every task names specific files

- [ ] No tasks say “investigate” or “figure out” without bounded scope

- [ ] A developer unfamiliar with the project could start implementing without asking
  questions

- [ ] Task order is causally possible (no circular dependencies)

- [ ] Each task answers the 5 questions (where, what, prerequisites, done condition,
  verification)

### Design Sensibility

- [ ] Complexity is proportionate to the problem

- [ ] No new abstractions without a concrete, current consumer

- [ ] Proposes mature libraries over custom solutions where they exist

- [ ] Design patterns match problem scale (no FactoryFactoryFactory)

### Test Quality

- [ ] Tests prove behavior, not implementation structure

- [ ] Assertions are substantive (`result.status == "approved"`, not
  `result is not None`)

- [ ] Tests cover real user paths, not just easy-to-test paths

- [ ] Error-path tests use errors that actually occur in production

* * *

## What a Good Plan Avoids

A plan is structurally weak if it contains:

- Implementation steps without defined target architecture

- Implicit scope with unstated omissions

- “Refactor” or “clean up” tasks without completion tests

- Validation by subjective review alone

- Downstream rewiring before upstream publication/stability

- Continued work on top of known damaged state

- Placeholders treated as acceptable intermediate shipped logic

- Local-only assumptions in workflow meant to validate remote or published use

- No rollback path for destructive or wide-impact work

- No stop rule preventing propagation of invalid assumptions

* * *

## Common Plan Failures (Anti-patterns)

| Anti-pattern | What goes wrong | Fix |
| --- | --- | --- |
| “Investigate X” | Unbounded, unverifiable | “Read `X.ts` and document the 3 entry points” |
| “Make it work” | No implementation path | “Add `validateInput()` at line 47 in `handler.ts`” |
| Task depends on later task | Causal impossibility | Reorder or split the dependency |
| Tests only check “not null” | Passes on any non-empty garbage | “Assert `result.token` is 32-char hex string” |
| No Rollback Plan | Destructive actions risk system state | “Define revert migration for schema changes” |

* * *

## Domain-Specific Extensions

### Software / Infrastructure

Additional requirements:

- Runtime/stack constraints

- Contract/interface specification

- Lint/type/test gates

- Installability or deployability validation

- Integration tests against real entrypoints

- Migration order for producers before consumers

Useful validations: CLI `--help`, real install, import smoke tests (must be real boundary tests/diagnostic commands, not proof-free smoke tests per Policy 5), schema validation,
CI reproduction, end-to-end command execution.

### Documentation / Knowledge Base / Writing

Additional requirements:

- Source-of-truth identification

- Intended audience and output format

- Structural completeness criteria

- Citation or reference policy

- Terminology consistency constraints

- Build/render/link validation if published

Useful validations: Style/lint/build passes, link checks, section coverage checklist,
factual/source cross-checks, render preview review.

### Mathematics / Research

Additional requirements:

- Exact problem statement

- Current known hypotheses and definitions

- What counts as a result: proof, counterexample, computation, literature inventory, or
  conjectural outline

- Dependency graph of lemmas/subproblems

- Criteria for a subclaim being established

- Explicit distinction between verified results and speculative directions

Useful validations: Formal proof check, symbolic/algebraic verification, numerical
sanity checks, citation to exact sources, consistency with hypotheses, reproducible
computation logs.

**Note:** “Investigate X” is not a task.
Decompose into concrete outputs: search for exact statements, compute invariant under
given hypotheses, test candidate lemma on model examples, or compare two formulations
under explicit assumptions.

### File Reorganization / Migration / Archival

Additional requirements:

- Canonical location rules

- Naming conventions

- Move/rename map

- Invariants that must survive reorganization

- Compatibility or redirect strategy for consumers

- Inventory before and after

Useful validations: Manifest diff, path resolution checks, broken-link/import checks,
duplicate detection, checksum or content equivalence checks.

* * *

## Planning Heuristics for LLM Agents

1. **Separate diagnosis from implementation** — If current state may be wrong, first
   inventory and contain.
   Don’t plan forward migration as though current artifacts are trustworthy.

2. **Prefer objective gates over narrative assurances** — Whenever possible, attach
   commands, proofs, checks, manifests, or explicit comparisons.

3. **Validate the true deployment/use mode early** — If final system is consumed
   remotely, published, rendered, compiled, or invoked through wrappers, validate that
   mode before large downstream work.

4. **Preserve canonical behavior before translating** — When porting systems, define
   source semantics first and preserve through substantive behavioral tests.

5. **Re-scope explicitly when targets changed** — If prior work dropped targets, added
   extras, or changed approved architecture, plan must re-state scope before more
   implementation.

6. **Make hidden assumptions visible** — Any assumption whose failure would invalidate
   later work belongs in prerequisites, dependencies, or stop rules.

7. **Use phases to control propagation** — Phase boundaries should represent real
   stabilization points.

8. **Require use-level acceptance, not merely internal correctness** — A component is
   complete when intended consumers can use it successfully under required constraints.

* * *

## Compact Plan Template

```md
# <Plan Title>

## Purpose / Big Picture

- What the user can do after this change that they could not before:
- How to see it working (observable behavior):

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

## Execution Progress

### Prerequisites

- [ ] <!-- status: pending --> Access requirements met
- [ ] <!-- status: pending --> Environment configured
- [ ] <!-- status: pending --> External dependencies resolved

### Phase 0: Containment / Recovery

- [ ] <!-- status: pending --> Task 0.1: [description]
- [ ] <!-- status: pending --> Task 0.2: [description]

### Phase 1: Core Implementation

- [ ] <!-- status: pending --> Task 1.1: [description]
- [ ] <!-- status: pending --> Task 1.2: [description]

### Phase N: Integration / Verification

- [ ] <!-- status: pending --> Task N.1: [description]
- [ ] <!-- status: pending --> Task N.2: [description]

### System-Level Validation

- [ ] <!-- status: pending --> End-to-end checks pass
- [ ] <!-- status: pending --> Real-use smoke checks pass

### Quality Gates

- [ ] <!-- status: pending --> Completeness verified
- [ ] <!-- status: pending --> Actionability verified
- [ ] <!-- status: pending --> Design sensibility verified
- [ ] <!-- status: pending --> Test quality verified

## Surprises & Discoveries

- Observation:
  Evidence:

## Decision Log

- Decision:
  Rationale:
  Date/Author:

## Outcomes & Retrospective

- Achieved:
- Remaining:
- Lessons:

## Revision Notes

- <date>: <what changed in this plan and why>
```

* * *

## Final Standard

A plan is **good** if it is:

- **Executable**: Each step names concrete action on concrete target

- **Ordered**: Dependencies and phase boundaries prevent invalid sequencing

- **Falsifiable**: Each task has observable acceptance criteria and validation

- **Stoppable**: Explicit gates prevent drift, compounding errors, and fake completion

Anything less is usually not a plan but a wish list.

* * *

## Living-Document Sections (Required)

Every plan carries these four sections and keeps them current as work proceeds. They are
how the plan stays restartable from itself: progress, what was learned, what was decided
and why, and how the result compared to the goal.

### Progress

A checklist of granular steps; see the format under
[Progress Tracking](#progress-tracking-execution-checklist) below. Every stopping point
is recorded here, even when that means splitting a partly done task into "done" and
"remaining." Stamp entries with timestamps (for example `(2025-10-01 13:00Z)`) so the
rate of progress is visible.

### Surprises & Discoveries

Unexpected behavior, bugs, performance tradeoffs, or insights found during
implementation, each with concise evidence — test output is ideal.

    - Observation: the optimizer reorders the two passes.
      Evidence: bench shows 1.4x when pass B runs before pass A.

### Decision Log

Every decision made while working the plan, with its rationale, so the reasoning survives
for the next contributor. If you change course mid-implementation, record why here and
reflect the consequence in `Progress`.

    - Decision: use library X for date handling.
      Rationale: timezone correctness; avoids a hand-rolled parser.
      Date/Author: 2025-10-01 / Z.G.

### Outcomes & Retrospective

At each major milestone and at completion, summarize what was achieved, what remains, and
lessons learned, measured against the original purpose.

* * *

## Progress Tracking: Execution Checklist

Every plan must include a task checklist at the end to track progress.

**Status notation:**

- `[ ]` = Incomplete

- `[x]` = Complete

- `[/]` = Blocked (explain reason)

- `[-]` = Skipped (explain reason)

**Format:**

```md
## Execution Progress

### Prerequisites

- [ ] Access requirements met
- [ ] Environment configured
- [ ] External dependencies resolved

### Phase 0: Containment / Recovery

- [ ] Task 0.1: [description]
- [/] Task 0.2: [description] — blocked: waiting for dependency X

### Phase 1: Core Implementation

- [x] Task 1.1: [description]
- [-] Task 1.2: [description] — skipped: no longer needed after refactor

### Phase N: Integration / Verification

- [ ] Task N.1: [description]
- [ ] Task N.2: [description]

### System-Level Validation

- [ ] End-to-end checks pass
- [ ] Real-use smoke checks pass

### Quality Gates

- [ ] Completeness verified
- [ ] Actionability verified
- [ ] Design sensibility verified
- [ ] Test quality verified
```

**Usage:** Check off items as they complete.
Use `[/]` for blocked (add reason) and `[-]` for skipped (add reason).
Stamp entries with a timestamp (for example `(2025-10-01 13:00Z)`) so progress rate is
visible. Reference this checklist in responses to indicate current progress.
