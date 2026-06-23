---
name: creating-implementation-plans
description: Use when creating, writing, reviewing, or revising implementation plans, source plans, externalization-ready plans, or durable execution specs; use before multi-step work, delegation, plan review, or plan-to-issue-tree-to-PR conversion.
---
# Creating Implementation Plans

> [!IMPORTANT]
> Plans created under this skill must respect the Bridge-Burning Policies in
> `policy-index`. Do not plan fallbacks, mocks, optional critical dependencies,
> runtime defaults, proof-free smoke checks, or other validation-evasion paths unless a
> narrower loaded policy explicitly permits them.

This is the canonical planning skill. Use this skill for implementation plans, source
plans, delegation handoffs, plan-review revisions, and plans that may become GitHub
epics, issue trees, or PR tracking surfaces.

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

## Plan Fit Gate

Use planning to preserve intent, state, coordination, and proof. Do not use planning as a
substitute for available object-level work.

If concrete feedback already names actions, sources, examples, user stories, or cases,
first ask whether representative instances can be resolved directly with existing repo
surfaces. Write a new plan, schema, router, taxonomy, script, or gate only when it
controls a real risk, preserves restartable state, coordinates multiple actors, or
captures repetition already observed in direct work.

For heterogeneous queues, size is not semantic homogeneity. Do not batch interpretive
decisions behind classifiers, ledgers, schemas, or automation merely because there are
many items. Automate navigation, retrieval, bookkeeping, and repeated mechanical
transforms; preserve item-level judgment for interpretation, source selection, and
mutation decisions.

Formalize successful behavior after representative traces exist. A plan may require
several direct case resolutions before it can honestly define stable categories, proof
burdens, or reusable workflow machinery.

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

When a plan may become a GitHub epic, issue tree, PR body, multi-agent tracker, or
handoff, write it so conversion is a lossless projection without semantic invention.

A projection may add execution metadata: owner, branch, status, blocker, commit, run,
artifact, review link, and GitHub formatting. It must not add, delete, demote, or
reinterpret the milestone, scope, baseline, vocabulary, execution graph, obligations,
tasks, handoffs, integration duties, proof burdens, or review prerequisites.

Before conversion, the plan must fix:

- externally meaningful milestone, finite scope, exclusions, preserved behavior, and
  observable completion state;
- stable vocabulary and complete referents;
- stacked foundations, parallel lanes, handoff contracts, and integration obligations;
- every obligation's actor, trigger or context, intended result, acceptance criteria,
  proof burden, dependencies, and supplied artifacts;
- which finalized milestones, workstreams, or obligations should become issues linked
  under the epic, using native sub-issues only when supported;
- proof design before implementation assessment.

Do not let test IDs, commands, filenames, commits, labels, green checks, or artifact names
stand in for obligations. They are evidence or automation only when attached to a declared
criterion.

If source material is scattered across plans, scratchpads, transcripts, comments, or run
notes, consolidate propositions by semantic role before writing the public plan. Preserve
valid meaning, dependencies, obligations, and proof burdens. Do not inherit wording,
checkboxes, duplicate status, or private identifiers as public truth.

Classify each proposition before consolidation:

- governing intent: milestone, scope, behavior, constraints, or acceptance criteria;
- work decomposition: substantive transformations, dependencies, lanes, handoffs, or
  integration work;
- scratchpad observation: symptom, command result, hypothesis, local TODO, or provisional
  idea;
- current execution state: ownership, branch, blocker, or completion claim that must be
  verified current before use;
- evidence material: output, screenshot, artifact, log, CI run, or report that must map
  to a named criterion;
- policy or automation: global review, proof, environment, or enforcement behavior that
  belongs in skills, CI, rulesets, or repository settings;
- residue: obsolete alternatives, raw commands, duplicated reminders, private reasoning,
  and notes with no continuing coordination or evidentiary value.

When sources disagree, do not use latest-file-wins, most-detailed-text-wins, or
most-confident-language-wins. Identify the conflicting propositions, distinguish intended
behavior from implementation state and hypothesis, resolve the contradiction in the
source plan, and publish only the coherent current obligation.

Normalize propositions, not prose blocks. Split paragraphs that mix obligations,
hypotheses, commands, and status claims. Expand internal referents, keep internal IDs only
as aliases, and convert micro-actions into their substantive parent. Do not inherit
checkmarks; re-evaluate old local status against current acceptance criteria, and count repeated claims once.

Stop and repair the source plan when conversion would require inventing scope, user
behavior, acceptance criteria, proof burdens, dependency order, ownership, unresolved
architecture decisions, or a reconciliation choice among contradictory source claims.

## Plan to Issue Tree to PR

Interactive planning is allowed to be a roadmap while the decomposition is still being
discovered. The issue hierarchy is created after the user finalizes the plan, not before
the plan has a stable semantic shape.

For nontrivial implementation work, use this externalization sequence:

1. Finalize the plan with the user.
2. Create or update a parent GitHub issue that acts as the epic.
3. Create or attach child issues for the top-level milestones, foundations, workstreams,
   or independently reviewable obligations. Use native sub-issues when the active GitHub
   surface supports them; otherwise link the child issues from the epic body as a task
   list.
4. Verify the issue tree preserves the finalized plan's scope, dependencies,
   acceptance criteria, and proof burdens.
5. Draft implementation PRs from that issue tree. Each top-level PR checklist item must
   link to the relevant issue unless the PR is genuinely trivial.

The issue tree becomes the external tracking source. Local plan files and scratchpads may
explain how the tree was derived, but they must not remain the authoritative tracker once
GitHub issues exist.

Do not use issue creation as a substitute for planning. If the issue tree cannot be
created without adding new scope, choosing between unresolved alternatives, or weakening a
proof burden, return to planning.

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
- **Externalization readiness:** if the plan will be projected into a GitHub issue tree
  and PR, no semantic invention is needed.
- **Projection integrity:** translation causes no semantic loss, invention, demotion, or
  proxy promotion; stacked, parallel, handoff, and integration structure stays explicit.
- **Evidence discrimination:** proof design distinguishes provenance, execution,
  attainment, and adequacy; evidence applies to the current revision and named criteria.
- **Closure:** every scope item maps to an obligation, every obligation maps to tasks and
  proof burdens, every task has one primary parent, and no repeated internal mention earns
  duplicate progress.

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
| Inherited checkmark | Old local status is treated as current public truth | Re-evaluate against current acceptance criteria and evidence |
| Duplicate corroboration | One claim repeated in several artifacts becomes several progress signals | Collapse repeats into one claim and require independent evidence |
| Evidence dumping | Commits, runs, logs, or artifacts are listed without a criterion | Map each witness to the obligation and false positive it rejects |
| Chat-only plan | Work cannot survive context rollover | Save a durable plan artifact through the active plan/memory workflow |
| Frozen plan | Discoveries and decisions leave the artifact stale | Update progress, discoveries, decisions, and revision notes |
| Implementation-defined success | Code determines its own acceptance after the fact | Lock acceptance and proof before implementation |

## Related Skills

- `plan`: storage and review-surface workflow when the user explicitly asks for a plan.
- `subagent-driven-development`: executes approved plans task by task.
- `test-driven-development` and `test-guidelines`: proof design for code changes.
- `git-guidelines`: checkpoint, commit, PR, and review workflow.
