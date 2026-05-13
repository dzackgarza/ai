# Planning Card Framework

This directory is the reusable source for filesystem-backed planning cards. Reference it when a project needs a tracker-backed planning hierarchy. Project-local planning instructions should point here and record only local choices: schema installation method, card root, current feature IDs, generated artifact paths, and hook commands.

## Contents

- Card Definition
- Schema Source
- No Fallbacks
- Hierarchy
- Decision Cards
- Layer Gate Discipline
- Required Planning Pipeline
- Filesystem Layout
- Frontmatter Links
- Metadata Field Scope
- No Static Metadata Rollups
- Specification Cards
- Plan Cards
- Phase Cards
- Task Cards
- Generated Tags
- Progressive Disclosure
- Link Discipline
- Recipe Workflow
- Git Hooks

## Card Definition

A card is any tracked file: a markdown file with YAML frontmatter whose `trackerStatus.type` selects a tracker schema. In this framework, feature, spec, plan, phase, and task files are all cards.

Do not treat "card" as a UI-only object. If a file is tracked by the schema system, it is a card and must obey the same frontmatter, containment, dependency, and validation rules.

## Schema Source

Project-local tracker schemas live at the project root under `.nimbalyst/trackers/`, symlinked to `~/ai/planning/schemas/`. The canonical schemas live under `~/ai/planning/schemas/`. Schema edits go there with a git commit on that repo. Projects symlink and consume these schemas — local forks are never correct. If a schema is too restrictive, the fix is to add the field to the canonical schema, not to fork or relax the local copy.

Install those files as symlinks into a project `.nimbalyst/trackers/` directory before creating cards. Use schemas as the source of truth for allowed fields, required fields, status values, display roles, and table columns.

- `schemas/feature.yaml`
- `schemas/spec.yaml`
- `schemas/plan.yaml`
- `schemas/phase.yaml`
- `schemas/task.yaml`
- `schemas/decision.yaml`

Install, copy, or symlink those files into a project `.nimbalyst/trackers/` directory before creating cards. Use schemas as the source of truth for allowed fields, required fields, status values, display roles, and table columns.

If a project symlinks schemas from this directory, edit the canonical schema here under `schemas/`. Do not replace a project symlink with a divergent local copy. The only path for schema changes is editing the canonical source.

## No Fallbacks

Planning data must be actually correct. The workflow must fail instead of guessing, skipping, or rendering partial state.

Hard failures:

- A markdown file under the card target tree has no YAML frontmatter.
- A card is missing `id` or `trackerStatus.type`.
- A card `id` does not match its filename stem.
- A card references an unknown ID in `parents`, `dependsOn`, `plans`, `phases`, or `tasks`.
- A card uses a tracker type without a schema.
- A card appears in a filesystem location that contradicts the hierarchy.
- A DAG node has an unknown type or cannot be placed in the planning hierarchy.

Do not add fallback groups, inferred types, placeholder nodes, best-effort renders, or warning-only validation paths. Stop and fix the data.

## Hierarchy

Preserve this containment tree:

```text
feature
├── spec
└── plan
    └── phase
        └── task
```

Responsibilities:

- Feature cards define the feature boundary, user outcome, scope, non-goals, major contracts, and links to child specs and plans.
- Spec cards define durable requirements and acceptance criteria. Specs describe observable behavior, public contracts, inputs, outputs, workflows, state transitions, recovery behavior, endpoints, commands, and verification obligations. Specs are implementation-agnostic: they must remain true if every current plan and phase is scrapped.
- Plan cards design the phase breakdown that will satisfy the feature and specs. Plans define each phase's purpose, concrete accomplishment target, success/failure boundary, sequencing, audit requirements, and expected drill-down shape.
- Phase cards turn a plan's phase definition into local milestones and atomic task cards.
- Task cards define executable work.

Do not place plans above other plans to simulate feature hierarchy. A feature owns specs and plans. A plan owns phases. A phase owns tasks.

Plan-level task directories are forbidden. A path such as
`plans/features/FEATURE-ID/plans/PLAN-ID/tasks/TASK-ID.md` is not a shortcut or a
temporary staging area; it means the phase gate was skipped. Do not create or continue
from that path. Create or repair the phase card first, then place tasks under the
phase's `tasks/` directory.

Decision cards are top-level auxiliary feature cards, not a layer inside plans, phases, or tasks. Use them only when work cannot continue because a real decision cannot be resolved unambiguously from approved feature/spec/plan cards, repo conventions, or existing contracts.

## Decision Cards

Do not leave durable "needs decision", "open decision", "decide later", "TBD", or "choose an approach" language in feature, spec, plan, phase, or task bodies. That language is an ephemeral drafting smell. Correct it immediately:

- If the answer follows unambiguously from approved cards, repo rules, or existing implementation contracts, resolve it in the card body and remove the decision language.
- If the answer does not follow unambiguously and blocks work, create a `decision` card.
- Link blocked work to the decision card with `dependsOn`.
- Mark blocked work `blocked` when execution cannot continue until the decision resolves.
- When the decision is decided, update the dependent card body with the chosen contract and unblock only the cards whose dependencies are satisfied.

Decision cards should contain the decision question, the known constraints, the viable options, and the chosen option when decided. They must not become implementation plans or task lists.

Place decision cards in the feature's top-level `decisions/` directory:

```text
plans/features/FEATURE-ID/decisions/DECISION-ID.md
```

Decision cards are parented to the feature. Plans, phases, and tasks that cannot proceed without the decision link to the decision card with `dependsOn` and use `status: blocked` while blocked.

## Layer Gate Discipline

Work one layer at a time. Do not leapfrog from feature definition into plans, phases, or tasks. Do not write tasks while writing a feature. Do not write tasks while writing a plan.

Required gates:

- Feature and spec gate: write the feature card and its spec cards first, as durable artifacts. Get approval for what the feature is, why it should exist, what behavior it must provide, and what evidence proves it works before planning implementation.
- Plan gate: after the feature and specs are approved, create the plan card or fleet of sibling plan cards. Plans break the approved feature into phases and encode what each phase must accomplish before task authoring begins.
- Phase drafting gate: after the plan is approved, create phase cards under each plan. Phases break the plan into ordered local milestones, but they are not approved for execution until their task cards are written and unambiguous.
- Task gate: after the phase breakdown is accepted, create task cards under each phase. Tasks are executable contracts for implementation agents.

The point of the feature/spec gate is to decide `what`, `why`, and `should we` before deciding `how`. Implementation work is often straightforward once the right problem is specified. Skipping the feature/spec gate risks implementing an inferred solution to the wrong problem.

Approval is layer-local. A feature approval authorizes planning; it does not authorize tasks. A plan approval authorizes phase design; it does not authorize task execution. A phase approval requires its tasks to be fully specified and free of unresolved operational decisions.

Useful granularity model:

- A feature can correspond to a git branch.
- A plan can correspond to a major milestone on that branch.
- A phase can correspond to a smaller milestone inside the plan.
- A task can correspond to one nontrivial but atomic unit of work, usually a commit or small collection of commits, often performed in a worktree.

## Required Planning Pipeline

Build the hierarchy top-down:

- First, develop the feature card and spec cards in isolation from implementation plans. Define the user outcome, scope, non-goals, contracts, requirements, acceptance criteria, public surfaces, expected outputs, workflows, and verification obligations. Stop for approval before planning implementation.
- Then, break the approved feature into high-level plans and create the plan cards. Plans may depend on one another, but they remain siblings under the feature unless a different feature boundary is required. Each plan must design its phases before phase cards are created. Stop for approval before creating phases.
- Then, break each approved plan into draft phases and create phase cards. Phases own local milestones and sequencing inside the plan. Stop for review of the phase breakdown before creating tasks.
- Then, break accepted draft phases into task cards. Tasks are executable units with concrete verification. A phase is approved for execution only after its child tasks are fully specified and free of unresolved operational decisions.

Before writing any task card, name the owning feature, plan, and phase, and confirm the
phase card exists. If no phase owner exists, the next action is phase repair, not task
creation. A plan-level `tasks/` directory is evidence of a process failure and must not
receive additional cards.

Do not create task cards first and backfill the feature. Do not let an implementation plan define the feature boundary. If a plan starts defining the feature, move that material into the feature card or spec cards.

## Filesystem Layout

Mirror containment in the filesystem. A feature owns a directory containing its feature card plus `specs/`, `decisions/`, and `plans/` subdirectories.

Use this layout:

```text
plans/features/FEATURE-ID/
├── FEATURE-ID.md
├── specs/
│   └── SPEC-ID.md
├── decisions/
│   └── DECISION-ID.md
└── plans/
    ├── PLAN-ID/
    │   ├── PLAN-ID.md
    │   ├── PHASE-ID/
    │   │   ├── PHASE-ID.md
    │   │   └── tasks/
    │   │       └── TASK-ID.md
    │   └── ...
    └── PLAN-ID/
        └── PLAN-ID.md
```

Keep card IDs stable when moving files. Paths may change to reflect hierarchy; wikilinks should continue to target IDs.

## Frontmatter Links

Encode containment and execution ordering separately:

- `parents` encodes containment.
- `dependsOn` encodes dependency ordering or blocking relationships.
- Feature cards list child plans in `plans`.
- Plan cards list child phases in `phases` when useful.
- Phase cards list child tasks in `tasks` when useful.
- `tags` are generated from containment; do not maintain them manually.

Containment requirements:

- Feature cards have no required parent.
- Spec cards must have a feature parent in `parents`.
- Plan cards must have a feature parent in `parents`.
- Phase cards must have their owning plan in `parents`.
- Task cards must have their owning phase in `parents`.
- Decision cards must have the feature in `parents`.

Do not use `dependsOn` to mean "is contained by." Do not rely on body text as the only place where hierarchy is recorded.

## Metadata Field Scope

Frontmatter is metadata, not the document body. Metadata fields should be short, plain values that index, filter, and summarize the card. Use a few paragraphs at most for text fields such as `description`. For array fields such as `successCriteria`, each entry should be at most a couple of paragraphs and should remain plain prose.

Put richer material in the body: complex explanations, full acceptance criteria, gates, checklists with substructure, tables, diagrams, examples, transcripts, command output, design arguments, and any markdown that needs headings or internal organization.

Task cards may set `complexity` as a numeric score from `0` to `100`. Use it as a rough execution-complexity signal for scheduling and delegation; do not replace the body context, acceptance criteria, or dependency fields with the score.

## No Static Metadata Rollups

Do not track child-card metadata manually inside parent card bodies. Each card owns its own metadata in frontmatter: `status`, `parents`, `dependsOn`, `tags`, and tracker-specific fields. Parent cards may link to child cards and explain why those children exist, but they must not copy child status, completion percentage, review state, owner, priority, or other mutable tracker metadata into body text.

Forbidden patterns:

- A phase table that lists child tasks and manually writes each task's current status.
- A plan summary that says a phase is `in-progress` because it copied the phase card's status.
- A feature body that maintains counts such as "7 tasks complete, 3 needs-review".
- Any prose that must be updated only because a linked card changed metadata.

Allowed patterns:

- A phase card lists its task cards and explains the purpose of each task.
- A plan card explains confusing dependency order, sequencing constraints, or milestone intent.
- A card records acceptance criteria, design nuance, activity logs, review comments, or durable decisions.
- Generated views, kanban boards, DAGs, or short scripts aggregate child status dynamically from frontmatter.

Static metadata rollups make ordinary local changes nonlocal: changing one task from `in-progress` to `needs-review` would require searching and editing every parent or sibling body that copied the old status. That creates large, opaque diffs and defeats the fixed hierarchy. Query the cards instead.

## Specification Cards

A spec elaborates what it means for the feature to work correctly. It is not a plan summary, phase index, or task checklist.

Include concrete, durable requirements:

- Accepted input forms, command invocations, endpoint methods, request shapes, and file layouts that are part of the public contract.
- Expected outputs, status codes, stdout or JSON shapes, persisted records, UI-visible behavior, and side effects.
- State transitions, recovery behavior, concurrency behavior, compatibility requirements, and failure semantics when they are part of the feature.
- Verification obligations stated as observable checks: a named E2E scenario, fixture shape, invariant, or command that proves the contract.

Exclude implementation-contingent structure:

- Phase names, phase order, task IDs, and plan sequencing.
- "Current implementation" details that could change without changing user-visible behavior.
- Claims that a spec requirement is satisfied because a phase exists.

Specs may mention likely implementation surfaces when those surfaces are part of the required behavior. For example, "POST `/api/submit` accepts `{ plan, origin }` and returns 202 before any waiter resolves" is a spec requirement if that endpoint is the feature contract. "Phase 2 implements submit/wait after Phase 1" is plan content.

If useful, add a non-normative `Verification Coverage` section that links to tests or proof artifacts. Do not make the spec's meaning depend on a plan, phase, or task that could be replaced.

Good spec pattern:

```markdown
## Submit And Wait Contract

When a client submits plan text `P` with origin `claude-hook`, the daemon stores one pending review record, returns JSON containing the review ID, and keeps the wait request blocked until the review receives an approve, deny, cancel, or reset verdict.

## Acceptance Criteria

- `POST /api/submit` with `{ "plan": P, "origin": "claude-hook" }` returns `202` and a stable review ID.
- `GET /api/state` includes exactly one pending review with that ID before verdict resolution.
- `plannotator wait --json <id>` emits a JSON object with the final verdict and exits with the documented status code.
- Restarting the daemon before verdict resolution preserves the pending review and lets `wait` complete after the verdict.

## Verification Coverage

- A built-artifact E2E scenario submits a real plan, waits through the CLI, resolves it through the daemon API, and checks the JSON output and exit code.
```

Bad spec pattern:

```markdown
## Submit And Wait Contract

Phase 2 implements submit/wait. Phase 3 adds the E2E spec. Phase 4 verifies it.
```

That ordering belongs in a plan. The spec should state the externally observable contract and the evidence required to prove it.

## Plan Cards

A plan takes an approved feature and its specs and designs a feature-level roadmap. It answers:

> What must become true, in what order, for this feature branch to reach a releasable state?

A plan must be concrete enough that each phase can later be expanded into task cards, but abstract enough that it does not pre-implement the feature inside the plan. It defines milestone-scale units of work, not atomic work items.

Plan cards must define:

- The repository state that counts as feature completion for this plan.
- Explicit non-goals that keep adjacent work out of the branch.
- Planning assumptions that affect scope, sequencing, or validation.
- The phase list and dependency order.
- Each phase's concrete outcome, stated as a property of the repository after the phase closes.
- Each phase's scope boundary: what belongs in the phase and what is deferred.
- Each phase's 4-10 milestone-level todo clusters, using verbs, artifacts, and observable effects without function-level micromanagement.
- Each phase's dependencies, ordering constraints, and downstream blockers.
- Each phase's validation expectations: the kinds of tests, audits, or proof evidence that close the milestone.
- Each phase's risks and linked blocking decision cards when a decision affects sequencing, scope, or correctness.

Plan cards may mention representative task shapes when that clarifies the phase design. They must not author task cards, assign subagents, enumerate every task acceptance check, name implementation functions, or copy task metadata. The phase file turns the approved phase definition into atomic task cards.

Plan-level todo clusters must pass this test:

> A later phase-planning pass can expand this item into multiple task cards without reinterpreting the feature.

Examples:

- Too vague: "Make state handling robust."
- Plan-level: "Define the allowed daemon state transitions, illegal transition responses, and recovery behavior consumed by CLI and HTTP callers."
- Phase-level: "Add integration coverage for submit-while-active returning collision guidance."
- Task-level: "In `03-state-machine.spec.ts`, assert raw `POST /api/submit` during active review returns HTTP 409 and mentions the force-clear command."

Recommended phase granularity:

- A phase should usually correspond to a reviewable milestone on the feature branch.
- A phase is too large if it contains unrelated architectural decisions, unrelated test surfaces, or cannot be reviewed as a coherent milestone.
- A phase is too small if it is one implementation task, one file edit, one test case, or one local cleanup.
- Common phase boundaries include surface reduction, contract definition, implementation integration, persistence or lifecycle orchestration, user-facing or agent-facing workflow, and verification hardening.

The following baseline is suggested, not mandatory. Preserve the project schema and hierarchy first; adapt headings when a project needs different names, but keep the semantic content. Do not duplicate frontmatter-derived facts in the body. For example, do not add a body section that merely restates the parent feature, parent spec, parent plan, status, tags, or child-link fields already encoded in YAML.

```markdown
---
id: PLAN-FEATURE-ID
trackerStatus:
  type: plan
parents:
- '[[FEATURE-ID]]'
dependsOn: []
phases:
- '[[PHASE-CONTRACTS]]'
- '[[PHASE-IMPLEMENTATION]]'
title: Feature implementation roadmap
status: needs-review
description: Roadmap for taking FEATURE-ID from approved feature/spec contracts to releasable implementation.
successCriteria:
- The approved phases satisfy the feature and spec contracts.
- Each phase has explicit validation expectations and downstream blockers.
---

## Goal

The daemon refactor is releasable when the built CLI and daemon satisfy the approved local-daemon contract from clean state, including lifecycle, singleton review state, submit/wait/clear, wrapper behavior, recovery, packaging, and E2E certification.

## Phase Overview

| Phase | Outcome | Blocks |
|-------|---------|--------|
| [[PHASE-CONTRACTS]] | Every user-visible daemon behavior has an approved observable contract. | [[PHASE-IMPLEMENTATION]], [[PHASE-CERTIFICATION]] |
| [[PHASE-IMPLEMENTATION]] | All CLI, daemon, and wrapper surfaces route through the accepted contracts. | [[PHASE-CERTIFICATION]] |

## [[PHASE-CONTRACTS]] - Semantic Contracts

### Outcome

Every downstream task can cite an accepted daemon contract instead of inferring behavior.

### Scope

In scope:
- State transitions, illegal-state responses, exit codes, recovery commands, concurrency rules, and persisted state semantics.

Out of scope:
- Implementation rewrites, browser polish, and packaging changes except where needed to make contracts observable.

### Todo Clusters

- Inventory all user-visible daemon behaviors that downstream tests would otherwise infer.
- Define legal and illegal state transitions with observable inputs, outputs, and persistence effects.
- Define recovery behavior for crashes, stale state, fixed ports, and interrupted clients.
- Review every contract against the feature and spec before implementation tasks depend on it.

### Dependencies

Depends on:
- Approved feature and spec cards.

Blocks:
- Implementation and E2E certification phases that encode these contracts.

### Validation Expectations

- Contract review proves no downstream test relies on unresolved decision language.
- Coverage planning maps each contract to at least one later proof surface.

### Risks / Blocking Decisions

- If cancellation and stale verdict handling are unresolved, create feature-level decision cards and block this phase until they are decided.
```

Bad plan pattern:

```markdown
## Task List

- [[TASK-1]] status: in-progress
- [[TASK-2]] status: needs-review
- [[TASK-3]] status: done
```

That is a metadata rollup and task index, not a plan. A plan defines why phases exist, what each phase must make true, why the order is correct, what each phase excludes, and what evidence closes each milestone. Phase cards define the task inventory.

A reviewer must be able to answer these questions without opening future phase files:

- What are the milestone-sized phases?
- What concrete repository state does each phase produce?
- Why are the phases ordered this way?
- What is explicitly excluded from each phase?
- What kind of evidence closes each phase?
- Which parts still require design decisions during phase planning?
- Can each phase be expanded into task cards without inventing missing feature intent?

## Phase Cards

A phase takes one approved plan milestone and turns it into executable task-card design. It answers:

> What exact tasks must agents execute to make this phase true?

Phase cards must define:

- The phase outcome inherited from the plan, refined only where needed for execution.
- The local scope and non-scope for this phase.
- The task inventory or planned task inventory, with each task's purpose but not mutable task metadata.
- Ordering constraints between tasks inside the phase.
- Operational decisions made during phase planning, so task cards do not decide behavior on the fly.
- Phase-level acceptance gates that prove the milestone, usually by aggregating task proof artifacts and targeted integration checks.
- Audit checks for ambiguous language, weak tests, missing fixtures, unsafe file scope, or dependency mistakes.

Phase cards may link to child tasks and explain why each exists. They must not manually track task status, completion percentage, owner, or review state. Query those from task frontmatter or generated views.

The following baseline is suggested, not mandatory. Do not add body sections that restate parent plan, status, tags, or task-list metadata already encoded in frontmatter.

```markdown
---
id: PHASE-CONTRACTS
trackerStatus:
  type: phase
parents:
- '[[PLAN-FEATURE-ID]]'
dependsOn: []
tasks:
- '[[TASK-CONTRACT-INVENTORY]]'
- '[[TASK-CONTRACT-REVIEW]]'
title: Semantic contracts
status: unstarted
description: Convert unresolved feature behavior into accepted observable contracts before implementation and E2E assertions depend on it.
successCriteria:
- Every downstream task can cite accepted contracts for the behavior it implements or verifies.
- No child task contains unresolved product, architecture, API, or acceptance decisions.
---

## Outcome

Every downstream implementation and proof task can cite an accepted contract instead of inferring daemon behavior.

## Scope

In scope:
- State transitions, illegal-state responses, exit codes, recovery commands, concurrency rules, and persisted state semantics.

Out of scope:
- Implementation rewrites, browser polish, packaging changes, and E2E suite completion except where needed to make contracts reviewable.

## Task Design

| Task | Purpose | Blocks |
|------|---------|--------|
| [[TASK-CONTRACT-INVENTORY]] | Inventory all user-visible behaviors that need contracts before implementation. | [[TASK-CONTRACT-REVIEW]] |
| [[TASK-CONTRACT-REVIEW]] | Review the contracts for observable inputs, outputs, state effects, and recovery behavior. | Implementation and E2E tasks |

## Ordering

- Inventory precedes review because review cannot close until every contract candidate is visible.
- Contract review blocks downstream implementation and E2E tasks that encode these behaviors.

## Acceptance Gates

- All child tasks are accepted.
- The phase audit finds no unresolved decision language in child tasks.
- Each accepted contract maps to a downstream implementation or proof surface.

## Risks / Blocking Decisions

- Cancellation and stale verdict handling may require splitting or adding tasks before this phase is approved.
```

## Task Cards

A task card is a recipe, prompt, and contract for a bounded unit of work. It must be specific enough that an implementation agent can execute it without deciding product behavior, architecture, scope, sequencing, or acceptance criteria on the fly.

Task cards must define:

- The exact objective and non-goals.
- The files, modules, or surfaces the task may change when that is known.
- The inputs, outputs, state changes, endpoints, CLI behavior, or UI behavior the task must produce.
- The verification command or proof artifact required for acceptance.
- Dependencies on other tasks, phases, specs, fixtures, or decisions.

Task cards must not contain unresolved decision language:

- Do not write "decide whether", "figure out", "choose an approach", "investigate and implement", "design as needed", or "handle appropriately" as task work.
- Do not leave API shape, storage shape, exit-code behavior, UI workflow, or test acceptance criteria for the implementation agent to invent.
- Do not approve a phase if any child task still requires operational decisions. Make the decisions during task authoring and encode them in the task card.

A task should be reasonably nontrivial but atomic for a 2026 coding agent. If it requires multiple independent design decisions, split it or return to the phase or plan layer. If it is a trivial mechanical edit, merge it into a neighboring task unless isolation improves verification.

The following baseline is suggested, not mandatory. Do not add body sections that restate parent phase, status, tags, or dependency metadata already encoded in frontmatter.

```markdown
---
id: TASK-CONTRACT-INVENTORY
trackerStatus:
  type: task
parents:
- '[[PHASE-CONTRACTS]]'
dependsOn: []
title: Inventory daemon behavior requiring contracts
status: unstarted
description: Identify every user-visible daemon behavior that downstream implementation or E2E tasks would otherwise infer.
successCriteria:
- The inventory covers CLI, HTTP, browser, wrapper, persistence, lifecycle, recovery, and concurrency behavior.
- Each inventory entry names the accepted source or marks the missing decision that must be resolved before task approval.
complexity: 35
---

## Objective

Produce the contract inventory required by [[PHASE-CONTRACTS]] so downstream tasks do not infer daemon behavior.

## Non-Goals

- Do not implement behavior.
- Do not write E2E tests.
- Do not change public contracts; record missing decisions for phase planning.

## Allowed Scope

- Planning cards and proof-design notes inside this phase.
- Existing docs or source may be read for evidence, but source edits are out of scope.

## Work Contract

- Inventory every CLI command, HTTP endpoint, browser action, wrapper behavior, persistence effect, lifecycle transition, recovery path, and concurrency case that downstream tasks must treat as public behavior.
- For each behavior, record accepted input forms, expected outputs, state effects, persistence effects, exit codes or status codes, and recovery behavior.
- Mark unresolved behavior as a phase decision to settle before approving child implementation or E2E tasks.

## Acceptance Checks

- The inventory has no "decide later", "handle appropriately", or equivalent unresolved operational language.
- Each behavior either cites an accepted contract or names the specific missing decision.
- Phase review can use the inventory to create or approve downstream task cards without inventing feature intent.

## Verification

- Run the planning validation recipe after editing cards.
- Include the exact command output or blocker in the task handoff.
```

## Generated Tags

Use `just derive-tags plans/features` to rewrite card tags from containment ancestry.

The recipe applies these rules:

- Each descendant of a feature gets the feature ID as a tag.
- Each descendant of a plan gets that plan ID as an additional tag.
- Each descendant of a phase gets that phase ID as an additional tag.
- A card does not tag itself with its own ID.
- Cards with no qualifying feature, plan, or phase ancestor have no `tags` field.

These tags exist for tracker and kanban views, grouping, filtering, and generated navigation. Agents should not use frontmatter `tags` as planning semantics. The hierarchy is encoded by `parents`, child-link fields, and the filesystem.

Do not hand-write topical tags such as `e2e`, `cli`, or `validation` in tracker frontmatter. Keep frontmatter tags structural and reproducible. If a card needs extra discoverability, add a body section such as `## Keywords` or `## Related Concepts` and write the terms there.

## Progressive Disclosure

Write each card for its own level. Higher-level cards may link deeply for navigation, but they must not restate or depend on lower-level execution structure for their meaning.

Use this rule:

- Feature cards may link to specs, plans, and major contracts.
- Spec cards own durable behavior and verification requirements. They may link to proof artifacts or tests, but the requirement itself must remain valid if the implementation plan changes.
- Spec requirements must remain independent of phase names, phase order, task layout, and current implementation sequencing.
- Plan cards own phase design: concrete outcome, scope boundary, milestone-level todo clusters, sequencing, validation expectations, risks, and drill-down shape.
- Phase cards own task grouping and local acceptance gates.
- Task cards own implementation details and verification commands.

Plans design phases; they do not replace the drill-down layer. If a plan starts listing task cards as the primary content, move that material into phase cards and restore the plan to milestone outcomes, boundaries, sequencing, and validation.

## Link Discipline

Prefer links that answer one of these questions:

- Which spec defines this required behavior?
- Which plan executes this feature work?
- Which phase owns this local milestone?
- Which task implements or verifies this slice?
- Which proof artifact verifies this contract?

Avoid links that make a card duplicate a lower-level table. Do not mirror a phase table in a spec. Do not make a spec depend on plan topology. Link to implementation artifacts only as current coverage, not as the source of truth.

## Recipe Workflow

Use the `planning/justfile` recipes from a project root or copy the justfile into the project.

Recipe dependency order is mandatory:

- `check-schema` runs `derive-tags` first.
- `dag` runs `check-schema` first.
- `validate` runs `dag`, which means validation rederives tags, checks schemas, and regenerates the DAG in order.

Common commands:

```bash
just --justfile ~/gitclones/ai/planning/justfile install-schemas .nimbalyst/trackers
just --justfile ~/gitclones/ai/planning/justfile derive-tags plans/features
just --justfile ~/gitclones/ai/planning/justfile check-schema plans/features .nimbalyst/trackers
just --justfile ~/gitclones/ai/planning/justfile dag plans/features plans/plan-dag.md .nimbalyst/trackers
just --justfile ~/gitclones/ai/planning/justfile validate plans/features .nimbalyst/trackers plans/plan-dag.md
```

After hierarchy or schema edits:

- Run `just validate plans/features .nimbalyst/trackers plans/plan-dag.md`.
- Run `git diff --check -- plans .nimbalyst/trackers`.
- Inspect the regenerated containment DAG and confirm each feature points to its specs and plans.

## Git Hooks

Install project git hooks that run the planning recipes after card updates. Hooks keep generated tags and DAG output fresh instead of relying on agents to remember the sequence.

Required hook behavior:

- Pre-commit hooks must run `just validate plans/features .nimbalyst/trackers plans/plan-dag.md` when planning cards or tracker schemas changed.
- Post-merge hooks must run the same validation after pulling or merging changes that affect planning cards or tracker schemas.
- Post-checkout hooks must run the same validation after switching branches when planning cards or tracker schemas changed.
- Hooks must fail on validation errors. Do not convert failures to warnings.

If a hook rewrites tags or `plans/plan-dag.md`, stage the generated changes deliberately before committing. Generated planning data must be current in git.
