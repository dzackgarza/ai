---
name: plan
description: "Plan mode: write markdown plan to .hermes/plans/, no exec."
license: MIT
metadata:
  hermes:
    tags: [planning, plan-mode, implementation, workflow]
    related_skills: [creating-implementation-plans, subagent-driven-development]
---
# Plan Mode

Use this skill when the user wants a plan instead of execution.

## Core behavior

For this turn, you are planning only.

- Do not implement code.

- Do not edit project files except the requested plan artifact.

- Do not run mutating terminal commands, commit, push, or perform external actions.

- You may inspect the repo or other context with read-only commands/tools when needed.

- Your deliverable is a durable plan artifact, not a chat-only outline.

## Storage

When `agent-memory` is available, file plans as project memories with type `plan`.
Use the `agent-memory` skill for the exact command surface.

If the runtime or user explicitly requires a repo-local markdown plan, save it under:

- `.hermes/plans/YYYY-MM-DD_HHMMSS-<slug>.md`

If `agent-memory` is required by the active instruction set but unavailable, report the
blocker instead of creating an untracked substitute.

## Output requirements

Write a markdown plan that is concrete and actionable.

Include, when relevant:

- Goal

- Current context / assumptions

- Proposed approach

- Step-by-step plan

- Files likely to change

- Tests / validation

- Risks, tradeoffs, and open questions

If the task is code-related, include exact file paths, likely test targets, and
verification steps.

## Transformation-Ready Plans

When a plan may become a GitHub epic, issue tree, PR body, multi-agent tracking surface,
or handoff artifact, write it so conversion is a projection, not another planning pass.

Interactive planning may stay exploratory while the user and agent converge on the
right decomposition. Do not force the first draft into GitHub mechanics. Once the user
finalizes the plan, the next durable tracking surface for nontrivial implementation work
is a GitHub epic issue with linked child issues, using native sub-issues when the active
GitHub surface supports them. A draft PR comes after that and
links its top-level checklist nodes to the relevant issues.

The plan must fix the semantic target before implementation or publication:

- State the externally meaningful milestone, included scope, explicit exclusions,
  preserved behavior, and observable completion condition.

- Define stable vocabulary and expand private referents. A future reader should not need
  transcript context, test mnemonics, issue numbers, file names, or agent scratchpads to
  know what the plan means.

- Represent real dependency structure: stacked foundations, parallel workstreams, and
  integration obligations. Do not flatten dependency order into a status checklist.

- Attach each task to an externally meaningful obligation with acceptance criteria and
  proof burden. Commands, commits, test IDs, green checks, artifact names, and labels are
  evidence or automation, not substitutes for the obligation.

- Separate internal execution material from the public plan. Classifications, local TODOs,
  debugging notes, current machine state, and review policy copies belong in the surface
  that owns them, not in the plan as progress.

- Mark which finalized milestones or workstreams should become GitHub issues. If the plan
  cannot be externalized as an epic plus issue tree without inventing scope, acceptance,
  dependencies, or proof burdens, keep planning instead of opening a PR.

If fragmented repository notes, subplans, scratchpads, or transcripts are the source
material, consolidate propositions by semantic role before writing the plan. Preserve
valid meaning, dependencies, obligations, and proof burdens; do not inherit wording,
checkmarks, duplicate status, or local identifiers as public truth.

If any milestone, scope boundary, dependency, acceptance criterion, proof burden, or
issue hierarchy must be invented during conversion, stop and report that the plan is not
ready to externalize.

## Interaction style

- If the request is clear enough, write the plan directly.

- If no explicit instruction accompanies `/plan`, infer the task from the current
  conversation context.

- If it is genuinely underspecified, ask a brief clarifying question instead of
  guessing.

- After saving the plan, reply briefly with the saved memory key or path.

## Plan Review Surface

When the user asks to read, inspect, annotate, or give feedback on a plan, generate the
review surface on demand:

- render the entire plan as one self-contained HTML page
- serve it from an ephemeral local server
- include inline annotation controls and a global Post button
- save the annotation payload to a file
- read that payload back before revising or acting

The review page is not a standing service.
Create it only for the requested plan-review turn.
