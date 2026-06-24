# Externalization: Source Plans, Issue Trees, and PRs

> Load this at any tier when a plan will become a GitHub epic, issue tree, PR body,
> multi-agent tracker, or handoff. Externalization is orthogonal to the plan tier.

## Transformation-Ready Source Plans

When a plan may become a GitHub epic, issue tree, PR body, multi-agent tracker, or
handoff, write it so conversion is a lossless projection without semantic invention.

Start from user stories and user-observable outcomes, and derive milestones,
dependencies, and acceptance criteria from those stories. A projection may add execution
metadata: owner, branch, status, blocker, commit, run, artifact, review link, and GitHub
formatting. It must not add, delete, demote, or reinterpret the milestone, scope,
baseline, vocabulary, execution graph, obligations, tasks, handoffs, integration duties,
proof burdens, or review prerequisites.

Before conversion, the plan must fix:

- externally meaningful milestone, finite scope, exclusions, preserved behavior, and
  observable completion state;
- stable vocabulary and complete referents. A future reader should not need transcript
  context, test mnemonics, issue numbers, file names, or agent scratchpads to know what
  the plan means;
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
checkmarks; re-evaluate old local status against current acceptance criteria, and count
repeated claims once.

Stop and repair the source plan when conversion would require inventing scope, user
behavior, acceptance criteria, proof burdens, dependency order, ownership, unresolved
architecture decisions, or a reconciliation choice among contradictory source claims.

## Plan to Issue Tree to PR

Interactive planning is allowed to be a roadmap while the decomposition is still being
discovered. The issue hierarchy is created after the user finalizes the plan, not before
the plan has a stable semantic shape.

For nontrivial implementation work, use this externalization sequence:

1. Create or update the vault-owned `agent-memory` plan record.
2. Finalize the plan with the user.
3. Create or update a parent GitHub issue that acts as the epic.
4. Create or attach child issues for the top-level milestones, foundations, workstreams,
   or independently reviewable obligations. Use native sub-issues when the active GitHub
   surface supports them; otherwise link the child issues from the epic body as a task
   list.
5. Verify the issue tree preserves the finalized plan's scope, dependencies,
   acceptance criteria, and proof burdens.
6. Draft implementation PRs from that issue tree. Each top-level PR checklist item must
   link to the relevant issue unless the PR is genuinely trivial.

The issue tree becomes the external tracking source. Local plan files and scratchpads may
explain how the tree was derived, but they must not remain the authoritative tracker once
GitHub issues exist.

Do not use issue creation as a substitute for planning. If the issue tree cannot be
created without adding new scope, choosing between unresolved alternatives, or weakening a
proof burden, return to planning.
