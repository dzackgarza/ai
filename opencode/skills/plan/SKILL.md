---
name: plan
description: "The canonical planning skill and plan mode: create, write, review, or revise durable implementation plans, source plans, and externalization-ready execution specs through agent-memory. When invoked as plan mode, plan only — no execution this turn."
license: MIT
metadata:
  hermes:
    tags: [planning, plan-mode, implementation, workflow]
    related_skills: [subagent-driven-development, requesting-code-review, test-driven-development, git-guidelines]
---
# Plan

> [!IMPORTANT]
> Plans created under this skill must respect the Bridge-Burning Policies in
> `policy-index`. Do not plan fallbacks, mocks, optional critical dependencies,
> runtime defaults, proof-free smoke checks, or other validation-evasion paths unless a
> narrower loaded policy explicitly permits them.

This is the canonical planning skill. Use it for implementation plans, source plans,
delegation handoffs, plan-review revisions, and plans that may become or fit into
GitHub issue trees, milestones, wiki projections, or PR claim maps. It is also the
plan-mode skill: when the user invokes `/plan` or asks for a plan instead of execution,
the **Plan Mode** contract below governs
the turn.

A plan is not a todo list or chat outline. It is a constrained execution specification
that fixes success, failure, order, ownership, and proof before implementation begins.

## Plan Mode (This-Turn Behavior)

When the user wants a plan instead of execution, for that turn you are planning only:

- Do not implement code.
- Do not edit project files except the requested plan artifact.
- Do not run mutating terminal commands, commit, push, or perform external actions.
- You may inspect the repo or other context with read-only commands/tools when needed.
- Your deliverable is a durable plan artifact, not a chat-only outline.

Never begin implementation from a plan until the user has approved it.

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
- make acceptance and proof exact enough to score a result — name the commands, expected
  observations, and stop conditions that would fail a wrong implementation — without
  prescribing the implementation diff (see Plan Tier and the Plan Tree);
- stay current as execution proceeds.

If a plan leaves the implementer to decide the milestone, scope, dependency graph,
acceptance criteria, or proof burden, the plan is not ready.

## Plan Tier and the Plan Tree

There is no single plan shape. A plan is a node in a tree of plans, and its tier sets how
tight it should be. Decide the tier first; do not slide into implementation research just
to produce the plan.

**Tiers (rough and flexible, not a rigid ladder):**

- **Roadmap / strategic.** Defines phases, invariants, user stories, and outcomes. Carries
  no task-level detail. Its job is to name the phases and mark which are complex enough to
  spawn their own child plan.
- **Workstream / organizational.** Takes real requirements, feedback, or a heterogeneous
  item set and coalesces it into *typed workstreams*: a count, a shared remediation shape,
  and shared acceptance ("15 items are book sections to migrate to an ambient book with a
  real Zotero book-section sub-item"). It defers per-item judgment to execution. Resolving
  every item's disposition inside the plan is doing the implementer's research, and a plan
  that never forces you to read the gathered feedback has failed at this tier.
- **Implementation-adjacent.** A scoring rubric for one coherent piece of work: endpoint,
  constraints, acceptance, proof. Loose on mechanism. Often a *leaf that is not written as
  an artifact at all* — when the parent constrains the endpoint enough, the implementer's
  own internal planning covers it, and a written leaf only steps on their toes while
  tracking nothing more auditable than the resulting commits.

**Calibration — rubric, not leash.** A plan is tight enough to (1) tell an implementer
roughly what the right endpoint is and (2) serve as a diagnostic rubric that could rank
several independent implementations of it — and loose enough that many implementations
satisfy it. Prescribing the exact line edits is an anti-pattern: strong implementers make
that micro-plan internally, and the diff is no more auditable than the commits and PRs.
Spend tightness on outcomes, criteria, and invariants, not on mechanism.

**The tree.** Every plan declares its parent plan key (or marks itself root / user-facing).
A high-tier plan marks each phase too complex to expand inline as one that must spawn its
own child plan. Store the whole tree as keyed `agent-memory` plan records so parent and
child links live in one place.

The tree exists to stop the most common drift: an agent descends into a sub-sub-plan and
loses the ambient, user-facing outcome entirely. The upward parent pointer keeps that
outcome one hop away at every depth. When you open or resume a child plan, restate the
parent outcome it serves before working.

**Routing gate (mandatory).** Do not draft a plan body until you have named the tier and
loaded its reference. The tier reference supplies the work-decomposition body, quality bar,
and tier-specific guidance; the universal skeleton and policies in this file apply to every
tier.

- roadmap / strategic → `references/tier-roadmap.md`
- workstream / organizational → `references/tier-workstream.md`
- implementation-adjacent → `references/tier-implementation.md`

Additionally load `references/externalization.md` whenever the plan will become or must
fit into a GitHub issue tree, GitHub milestone, wiki projection, draft PR, or multi-agent
tracker -- at any tier. Implementation-adjacent plans must decide their tree fit before
becoming local task lists or PR draft plans.

## Storage and Ownership Lifecycle

File every durable plan as a project-scoped `agent-memory` record with type `plan`.
Use the `agent-memory` skill for the exact command surface. If `agent-memory` is
unavailable, report the blocker instead of creating an untracked substitute.

A repo-local Markdown file may be a review/export artifact, but it is not the durable
source of truth unless it points back to the vault-owned plan key. If a runtime or user
explicitly requires a local Markdown export, first create or update the vault-owned plan
record, then write the local file as a non-authoritative compatibility copy that points
back to the memory key.

Keep a plan vault-owned while it is exploratory, single-agent, or still converging with
the user. Promote it to GitHub-owned execution state when any of these become true:

- the plan coordinates multiple agents, branches, repos, milestones, or handoffs;
- the plan defines public user stories, project direction, proof burdens, or roadmap
  commitments;
- work will span enough time that GitHub visibility is needed for auditability or
  resumption;
- the plan has been finalized by the user and is ready to become an issue tree,
  milestone, or draft PR contract;
- unresolved gaps, bugs, or follow-up obligations should be discoverable by future
  agents without reading vault internals.

Before promotion drives implementation, fill the externalization Plan Fit Gate: tree root,
parent issue or roadmap/wiki node, GitHub milestone, issue set or subtree claimed,
close/reference split, and claimed/non-claimed proof obligations.

After promotion, the GitHub issue tree, GitHub Milestones, and PR claim maps are the
execution tracker. Wiki pages are readable projections or durable narrative context, not
live status owners. Keep the vault plan as derivation context or a restart aid, but do not
let it diverge into a second private source of truth.

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

The detailed application of this gate to feedback-driven and judgment-heavy work —
coalescing into typed workstreams, criteria elicitation, and implementing through an
intelligent pass rather than deterministic machinery — lives in `references/tier-workstream.md`.

### Proportionality and Surface Placement

The Plan Fit Gate is where disproportionate machinery is cheapest to prevent. Agent
planning drifts toward inventing classification systems, governance, roles, and gates
before there is a demonstrated failure mode or an organization to need them. Apply three
checks before a plan proposes structure:

- **A control earns its place only against a demonstrated failure mode, and only as the
  simplest standard mechanism for it.** Prefer the machinery society has already
  internalized — databases, git, pull requests, issues, milestones, ordinary access
  control, citations, hashes — over a bespoke symbolic framework. Plan a custom gate,
  status system, taxonomy, or doctrine only when a standard tool demonstrably fails the
  specific risk. See `bespoke-software-policy` → **Proportionality: Earned vs. Manufactured
  Complexity**.
- **Do not plan institutions before they exist.** Roles, stewards, owners, councils,
  approval tiers, and separation-of-duty rules are not planning placeholders. Plan them
  when there are real actors to fill them and a real boundary they enforce, not as
  front-loaded structure.
- **Place state on the surface that owns it.** Ephemeral status, current-MVP plans,
  roadmaps, and work state belong in `agent-memory` plan records, GitHub issues,
  milestones, and PRs — never dumped into a README or user-facing doc, which would require
  constant babysitting and staleness review. The plan's own living state stays in the plan
  record, not in the product's documentation.

## Required Discovery

Before drafting tasks:

- load repo instructions and task-relevant skills;
- inspect the repo shape, existing plans, tests, just recipes, configs, and nearby
  implementation patterns;
- identify canonical source files and damaged derivatives;
- confirm whether the work is recovery, implementation, migration, documentation, or
  review-track preparation;
- if the work may touch public execution state, inspect the relevant GitHub issue tree,
  milestones, draft PRs, and wiki projection before naming local tasks;
- ask only questions that block a concrete plan decision. For judgment-heavy work the
  criteria are themselves a blocking decision: elicit the user's per-type standards,
  preferences, and tie-breakers before drafting, because a plan that invents them licenses
  fresh subagents to reinvent requirements mid-task.

Do not start from expected filenames, remembered commands, or generic templates when the
repo can show the real surface.

## Plan Structure

Every plan shares the skeleton below. Your tier reference (loaded at the routing gate)
supplies the work-decomposition body that fills the `<Work decomposition>` slot.

```markdown
# <Plan Title>

> Tier: <roadmap | workstream | implementation-adjacent>
> Parent plan: <agent-memory key, or "root / user-facing">
> Externalized fit: <private, or GitHub tree root + parent issue + milestone + PR claim set>

## Purpose / Observable Result
- What someone can do or verify after this work:
- Why the current state is insufficient:
- Observable completion condition:

## Scope
- Included:
- Excluded:
- Preserved behavior:
- Constraints and prohibitions:

## Invariants
- Properties that must hold throughout and after the work (constrain outcomes without
  dictating implementation):

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

## <Work decomposition — supplied by your tier reference>
- roadmap -> Milestones
- workstream -> Workstreams
- implementation-adjacent -> Task Plan + System-Level Validation

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

A roadmap plan fills the slot with Milestones; a workstream plan with typed Workstreams; an
implementation-adjacent plan with a Task Plan and System-Level Validation. Use only the
skeleton sections your tier needs.

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

The same defect has a high-altitude form: a Purpose, milestone, or invariant that sounds
weighty but rules nothing out ("build a robust system for X"). Judge every altitude by what
it constrains, not by how serious it sounds. A Purpose or milestone that no implementation
could violate is not direction; it is decoration.

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

- **Tier and tree placement:** the plan declares its tier and parent (or root), tightness
  matches the tier, and any phase too complex to expand inline is marked to spawn a child
  plan rather than being prescribed down to the diff.
- **Completeness:** goal, scope, exclusions, preserved behavior, dependencies, risks, and
  stop rules are explicit.
- **Actionability:** at the implementation-adjacent tier, tasks name exact files or
  surfaces, preconditions, changes, acceptance, proof, and commit boundaries; higher tiers
  name endpoints, workstreams, and acceptance instead of diffs.
- **Design sense:** the approach follows repo patterns, removes avoidable duplication,
  and does not introduce fallback or compatibility shims as a substitute for correctness.
- **Proof quality:** validation happens at the real use boundary and would fail on a
  plausible broken implementation.
- **Restartability:** another agent can resume from the plan alone.
- **Externalization readiness:** if the plan will be projected into or executed from a
  GitHub issue tree, milestone, wiki projection, or PR, the Plan Fit Gate is filled and
  no semantic invention is needed (see `references/externalization.md`).
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
| Premature institution | Plan invents roles, owners, gates, or doctrine before actors or a demonstrated failure exist | Plan controls only against a demonstrated failure mode, using the simplest standard mechanism |
| Status in the product | Plan routes ephemeral status, MVP state, or roadmap into a README or user-facing doc | Keep work state in the plan record, issues, and milestones; keep docs task-facing |
| Bespoke-over-standard | Plan designs a custom system where a database, git, PR review, or issues already fit | Justify any bespoke mechanism against the standard tool it replaces, or use the standard tool |
| Line-edit leash | Plan prescribes the exact diff or files to touch, doing the implementer's job and tracking nothing more auditable than the commits | Constrain the endpoint and acceptance as a rubric; leave the mechanism to the implementer |
| Feedback-blind plan | A plan so high-level it could run without ever consulting the gathered feedback, licensing reinvention on fresh context | Coalesce the actual feedback into typed workstreams with counts, shared shape, and shared acceptance |
| Orphan plan | Plan has no parent pointer, so a deep sub-plan loses the user-facing outcome | Declare the parent plan key or mark the plan root; restate the parent outcome on resume |
| Materialized leaf | Writing a leaf plan artifact the parent already constrains | Do not write it; let the implementer plan internally and score against the parent rubric |
| Deterministic cage | A judgment task is encoded into rules, scoring tables, exact-match pipelines, certificates, or schemas | Hand judgment to an intelligent agent pass with a loose prompt and a freeform ledger; freeze only the user's criteria |
| Aspirational framing | A Purpose, milestone, or invariant that sounds like a mission statement and rules nothing out | Judge every altitude by what it constrains; state the observable boundary, not the ambition |

## Interaction Style

- If the request is clear enough, write the plan directly.
- If no explicit instruction accompanies `/plan`, infer the task from the current
  conversation context.
- If it is genuinely underspecified, ask a brief clarifying question instead of guessing.
- After saving the plan, reply briefly with the saved memory key. Include a local export
  path only when one was explicitly created.

## Plan Review Surface

When the user asks to read, inspect, annotate, or give feedback on a plan, generate the
review surface on demand:

- Generate the plan review artifact in plain HTML as `<plan>.html` under `.lavish/` unless
  another location is requested.
- Launch and share it with `npx -y lavish-axi .lavish/<plan>.html` (or provided path).
- Read feedback with `npx -y lavish-axi poll .lavish/<plan>.html` before revising or acting.
- Save the annotation payload file returned by lavish and include it in handoff notes.

The review page is not a standing service. Create it only for the requested plan-review
turn.

## References

Load on demand after the routing gate:

- `references/tier-roadmap.md` — roadmap / strategic plans: phases, invariants, milestones,
  user stories, child-plan spawning.
- `references/tier-workstream.md` — workstream / organizational plans: coalescing gathered
  feedback or item sets into typed workstreams; criteria elicitation; intelligent-pass
  implementation.
- `references/tier-implementation.md` — implementation-adjacent plans: rubric calibration,
  task plan, task quality, system-level validation.
- `references/externalization.md` — converting any plan into a GitHub issue tree and PRs.

## Related Skills

- `subagent-driven-development`: executes approved plans task by task.
- `test-driven-development` and `test-guidelines`: proof design for code changes.
- `git-guidelines`: checkpoint, commit, PR, and review workflow.
- `agent-memory`: storage command surface for vault-owned plan records.
