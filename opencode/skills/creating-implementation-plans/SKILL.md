---
name: creating-implementation-plans
description: Use when creating, writing, reviewing, or revising implementation plans, source plans, PR-ready plans, or durable execution specs; use before multi-step work, delegation, plan review, or plan-to-PR conversion.
---
# Creating Implementation Plans

> [!IMPORTANT]
> Plans created under this skill must respect the Bridge-Burning Policies in
> `policy-index`. Do not plan fallbacks, mocks, optional critical dependencies,
> runtime defaults, proof-free smoke checks, or other validation-evasion paths unless a
> narrower loaded policy explicitly permits them.

This is the canonical planning skill. Use this skill for implementation plans, source plans, delegation handoffs,
plan-review revisions, and plans that may become PR tracking surfaces.

A plan is not a todo list or chat outline. It is a constrained execution specification
that fixes success, failure, order, ownership, and proof before implementation begins.

## Core Policy

Write plans so a contributor with only the current working tree and the plan can execute
or review the work without private context.

A valid plan must:

- explain the user-visible or repository-visible result being delivered;
- state the current defect, gap, or need and why it matters;
- define scope, exclusions, preserved behavior, and non-negotiable constraints;
- identify canonical source material and required repo/runtime evidence;
- order work by real dependencies rather than convenient checklist order;
- attach every substantive task to an obligation, acceptance criterion, and proof burden;
- name exact files, commands, expected observations, and stop conditions;
- stay current as execution proceeds.

If a plan leaves the implementer to decide the milestone, scope, dependency graph,
acceptance criteria, or proof burden, the plan is not ready.

## Required Discovery

Before drafting tasks:

- load repo instructions and task-relevant skills;
- inspect the repo shape, existing plans, tests, just recipes, configs, and nearby
  implementation patterns;
- identify canonical source files and damaged derivatives;
- confirm whether the work is recovery, implementation, migration, documentation, or
  review-track preparation;
- ask only questions that block a concrete plan decision.

Do not start from expected filenames, remembered commands, or generic templates when the
repo can show the real surface.

## Plan Structure

Use this structure unless the user or repo supplies a stricter one:

```markdown
# <Plan Title>

## Purpose / Observable Result
- What someone can do or verify after this work:
- Why the current state is insufficient:
- Observable completion condition:

## Scope
- Included:
- Excluded:
- Preserved behavior:
- Constraints and prohibitions:

## Sources and Current State
- Canonical sources:
- Relevant existing behavior:
- Known damaged or superseded artifacts:
- Assumptions already verified:
- Unknowns that still block planning:

## Execution Graph
- Stacked prerequisites:
- Parallel workstreams:
- Integration points:
- Handoff contracts:

## Milestones
### <Milestone name>
- Result:
- Dependencies:
- Acceptance:
- Verification:
- Stop conditions:

## Task Plan
### <Task name>
- Obligation served:
- Files:
- Preconditions:
- Change:
- Acceptance criteria:
- Proof / verification:
- Commit boundary:

## System-Level Validation
- Real boundary checks:
- Regression checks:
- Review or artifact checks:

## Risks / Recovery / Stop Rules
- Risks:
- Recovery path:
- Stop and ask when:

## Progress
- [ ] <granular task> -- evidence required:

## Surprises & Discoveries
- Observation:
  Evidence:
  Consequence for the plan:

## Decision Log
- Decision:
  Rationale:
  Date/author:

## Outcomes & Retrospective
- Achieved:
- Remaining:
- Lessons:

## Revision Notes
- <date>: <what changed in this plan and why>
```

## Task Quality

Every nontrivial task must answer:

- **Where:** exact file, module, command, route, artifact, or external surface.
- **What:** the concrete state change, not a vague action verb.
- **Why:** the obligation or milestone it serves.
- **Before:** dependencies and inputs that must already exist.
- **Done:** observable acceptance criteria.
- **Proof:** command, test, artifact, diff, or inspection that would fail if the work were
  wrong.
- **Commit:** the smallest coherent checkpoint boundary.

For code tasks, include the TDD or reproducer sequence when applicable: write or identify
the failing proof, confirm it fails for the intended reason, implement narrowly, rerun the
same proof, then run the relevant system gate.

Tasks should be assignment-sized: small enough for a focused implementation pass, but not
so small that they track typing, file touching, classification, or environment trivia.

## Language and Referents

Treat "neural-ese" as a planning defect, not a style preference. A plan item fails
when it uses deictic language without a stable antecedent, invented shorthand, vague
jargon, aphoristic status language, or authority priming that gestures at seriousness
without naming the behavior, decision, surface, and evidence.

Bad plan language usually makes a task sound inspectable while hiding what a reviewer
would judge. "Update proof obligations" is not a task; "define the proof obligation that
PDF export from the app menu produces the expected Beamer artifact, then prove it through
the repo E2E recipe" is a task. "Classify this as env-blocked" is not a task unless it
is nested under the substantive obligation and names the concrete blocker, owner,
evidence, and unblock condition.

Tooling and environment steps belong in the proof path, not as standalone progress,
unless the shared artifact or external precondition is itself reviewer-relevant. "Ensure
Playwright is installed" is normally subsumed by the proof task that uses Playwright; the
plan item is the boundary behavior being proven and the admissible evidence for it.

## Milestones and Execution Graph

Milestones describe delivered capability or restored correctness. The progress checklist
tracks granular execution. Keep them separate.

A milestone must state:

- the result that will exist at the end;
- what it blocks or depends on;
- which work can happen in parallel;
- how integration is verified;
- what observable evidence proves it is complete.

Use a prototyping milestone when requirements depend on unknown library, runtime, UI,
API, or proof behavior. A prototype must be additive, bounded, and tied to a promotion or
discard decision.

Use parallel workstreams only when their interfaces are explicit. State what each stream
produces, consumes, and must preserve for integration.

## Transformation-Ready Source Plans

When a plan may become a PR body, issue contract, multi-agent tracker, or handoff, write
it so conversion is a lossless projection without semantic invention.

Before conversion, the plan must fix:

- externally meaningful milestone, finite scope, exclusions, preserved behavior, and
  observable completion state;
- stable vocabulary and complete referents;
- stacked foundations, parallel lanes, handoff contracts, and integration obligations;
- every obligation's actor, trigger or context, intended result, acceptance criteria,
  proof burden, dependencies, and supplied artifacts;
- proof design before implementation assessment.

Do not let test IDs, commands, filenames, commits, labels, green checks, or artifact names
stand in for obligations. They are evidence or automation only when attached to a declared
criterion.

If source material is scattered across plans, scratchpads, transcripts, comments, or run
notes, consolidate propositions by semantic role before writing the public plan. Preserve
valid meaning, dependencies, obligations, and proof burdens. Do not inherit wording,
checkboxes, duplicate status, or private identifiers as public truth.

Stop and repair the source plan when conversion would require inventing scope, user
behavior, acceptance criteria, proof burdens, dependency order, ownership, or unresolved
architecture decisions.

## Living-Document Discipline

A plan remains authoritative only while it is current.

Update the plan at every stopping point:

- mark completed tasks only when their acceptance and proof are satisfied;
- split partly done work into completed and remaining parts;
- record blockers with the evidence or missing input;
- add discoveries that change the plan;
- log decisions and their rationale;
- append a revision note explaining what changed and why.

Do not use progress edits to launder incomplete work. Administrative updates, labels,
comments, and green checks are not completion unless they satisfy the declared obligation.

## Quality Gates

Before saving or handing off a plan, verify:

- **Completeness:** goal, scope, exclusions, preserved behavior, dependencies, risks, and
  stop rules are explicit.
- **Actionability:** tasks name exact files or surfaces, preconditions, changes,
  acceptance, proof, and commit boundaries.
- **Design sense:** the approach follows repo patterns, removes avoidable duplication,
  and does not introduce fallback or compatibility shims as a substitute for correctness.
- **Proof quality:** validation happens at the real use boundary and would fail on a
  plausible broken implementation.
- **Restartability:** another agent can resume from the plan alone.
- **PR readiness:** if the plan will be projected into a PR, no semantic invention is
  needed.

## Anti-Patterns

| Pattern | Failure | Required correction |
| --- | --- | --- |
| "Make tests pass" | Derived status replaces intended behavior | State the behavior and attach tests as evidence |
| Test ID as task | Private shorthand hides the obligation | Define the user/system outcome, then cite the test |
| File-touch checklist | Activity is counted as progress | Tie each edit to an obligation and acceptance criterion |
| Vague action verbs | `update`, `reconcile`, or `clean up` can mean anything | State concrete before/after behavior |
| Neural-ese | Deictic wording, invented jargon, status language, or authority priming hides the referent | Rewrite into exact behavior, decision, surface, and evidence |
| Tool step as task | Environment trivia becomes visible progress | Nest setup under the boundary proof it enables |
| Classification as task | Labels such as `env-blocked` replace the real obstacle | Record blocker evidence and unblock condition under the substantive task |
| Chat-only plan | Work cannot survive context rollover | Save a durable plan artifact through the active plan/memory workflow |
| Frozen plan | Discoveries and decisions leave the artifact stale | Update progress, discoveries, decisions, and revision notes |
| Implementation-defined success | Code determines its own acceptance after the fact | Lock acceptance and proof before implementation |

## Related Skills

- `plan`: storage and review-surface workflow when the user explicitly asks for a plan.
- `subagent-driven-development`: executes approved plans task by task.
- `test-driven-development` and `test-guidelines`: proof design for code changes.
- `git-guidelines`: checkpoint, commit, PR, and review workflow.
