# Externalization: Issue Trees, Milestones, Wiki Projections, and PR Claims

> Load this at any tier when a plan may become a GitHub issue tree, GitHub
> milestone, wiki roadmap/projection, draft PR, multi-agent tracker, or handoff.
> Externalization is orthogonal to plan tier.

## Core Model

Externalized project planning is one tree, not parallel artifacts:

```text
planning tree node -> GitHub issue
parent/child edge  -> GitHub sub-issue relation
sibling order      -> GitHub sub-issue order, or a wiki roadmap list only when needed
blocker edge       -> GitHub issue dependency
delivery bucket    -> GitHub Milestone assigned to the relevant issues and PRs
implementation     -> PR linked to the issue set it claims to satisfy
readable map       -> wiki projection generated or refreshed from GitHub state
```

Use ordinary semantic node names: roadmap, roadmap item, phase, feature, story,
proof obligation, implementation task. Do not introduce fake node labels such as
ROOT, epic, milestone issue, or custom status layers unless the repository already
uses them. GitHub issues store nodes; sub-issues store tree edges.

Every issue should be story-shaped at its own altitude. A roadmap issue may state
a broad user story. A feature issue states a narrower user story. An
implementation issue may state a developer, operator, reviewer, or system story.
The common requirement is that each node says what condition must become true and
why it matters.

Proof obligations normally belong inside the story/feature issue body as the
definition of done for that node. Split a proof obligation into a child issue only
when it is large enough to track, review, or implement independently. Tests,
checks, review, screenshots, logs, and artifacts are evidence for obligations; they
are not the obligations themselves.

PRs are not tree leaves. A PR is an implementation transaction against a selected
issue set. It may claim one issue, several sibling issues, a vertical slice, or an
entire subtree. The PR body must state its claim scope, linked issues, milestone,
implementation plan, evidence, and any partial/non-claims.

GitHub Milestones are delivery/progress buckets, not the tree. Shape the issue
tree so milestone-sized work is usually a coherent subtree. Create the GitHub
Milestone object for that delivery slice, describe its issue-tree scope, assign it
to descendant issues that count toward delivery, and assign it to PRs linked to
those issues. If a PR spans multiple milestones, split it or attach it only to the
broader milestone/release and say why.

The wiki is a readable roadmap and projection surface. It may hold durable
narrative context and generated tree/status views, but it must not own live issue,
PR, or completion state. A wiki may own the ordered top-level roadmap list only if
GitHub's issue/sub-issue ordering cannot represent that order cleanly; all
decomposition and execution state still belongs to issues, milestones, and PRs.

## Source Plan Requirements

Before creating GitHub objects, the source plan must fix:

- the roadmap or product story and the ordered top-level branches;
- which existing roadmap node, issue subtree, or milestone the work belongs under;
- the story-shaped issue nodes to create or update;
- proof obligations and acceptance criteria for each semantic node;
- which proof obligations remain embedded in an issue body and which deserve child
  issues;
- dependency edges that are blockers, distinct from traversal order;
- the GitHub Milestone objects needed up front, with scope expressed as a subtree
  root or explicitly enumerated issue set;
- the PR claim set: the issues or subtree this PR intends to close, partially
  advance, or only reference;
- explicit non-goals and deferred work.

Do not let test IDs, commands, filenames, commits, labels, green checks, issue
numbers, or artifact names stand in for obligations. They are evidence pointers
only when attached to a declared criterion.

If source material is scattered across plans, scratchpads, transcripts, comments,
or run notes, normalize propositions by semantic role before publishing anything:

- roadmap/story intent, scope, non-goals, and acceptance criteria;
- proof obligations and evidence expectations;
- tree edges, sibling order, dependencies, and milestone scope;
- implementation claims and PR closure/ref relationships;
- current execution state that must be verified current before use;
- residue: obsolete alternatives, raw commands, duplicated reminders, private
  reasoning, and status claims with no continuing coordination value.

When sources disagree, do not use latest-file-wins, most-detailed-text-wins, or
most-confident-language-wins. Resolve the contradiction in the source plan before
externalizing it.

## Plan Fit Gate

Before drafting a plan body for work that may touch an existing GitHub tree, name
the intended fit:

```text
Tree root:
Parent issue or roadmap/wiki node:
GitHub milestone:
Issue set or subtree this work claims:
Issues this PR may close:
Issues this PR may only reference:
Proof obligations claimed:
Proof obligations explicitly not claimed:
```

If any field is unknown and the repository already has public planning state,
inspect the issue tree, milestones, draft PRs, and wiki projection before writing
the plan. If the repository lacks a usable tree, the plan's first job may be
intake/scaffolding, not implementation.

## Intake For New Trees

When scaffolding a project roadmap with the user, proceed top-down:

1. Extract the product-level story: what product, what pain, what desired workflow.
2. Collect concrete end-to-end stories from real usage sessions.
3. Cluster those stories into ordered roadmap branches.
4. Cut milestone-sized subtrees by asking what smallest coherent delivery is useful.
5. Drill into only the active or next milestone subtree.
6. Define feature/story nodes and proof obligations.
7. Split only the parts that need implementation tracking.
8. Create issues/sub-issues for the accepted tree.
9. Create GitHub Milestones for milestone subtrees.
10. Open draft PRs only when a claimable issue set exists.
11. Render or refresh the wiki projection from the resulting GitHub state.

Do not start by asking the user for issue titles, labels, implementation tasks, or
GitHub mechanics. Ask for stories, failure modes, safety boundaries, exclusions,
and what would make the first milestone useful.

## Externalization Sequence

For nontrivial implementation work:

1. Create or update the vault-owned `agent-memory` plan record while the plan is
   still private or converging.
2. Finalize the plan with the user.
3. Inspect the existing GitHub issue tree, milestones, draft PRs, and wiki
   projection.
4. Create or update story-shaped issues under the correct parent issue. Use native
   sub-issues for parent/child edges when available; otherwise keep explicit links
   in the parent issue until native sub-issues can be used.
5. Preserve sibling order through GitHub sub-issue order where available. Use
   dependencies only for blockers, not for ordinary roadmap order.
6. Create GitHub Milestone objects for milestone-sized subtrees before or while
   creating their descendant issues. Link each milestone to its scope root or
   issue-set definition.
7. Assign milestone membership to descendant issues that count toward delivery and
   to PRs linked to those issues. Do not rely on milestone names alone as scope.
8. Draft PRs from the selected issue set or subtree. The PR body stores the local
   implementation plan and claim scope.
9. Use closing keywords or Development links only for issues the PR fully satisfies
   on merge. Use `Refs` or prose for broader parents, deferred work, partial
   claims, or excluded scope.
10. Verify the issue tree, milestone assignments, PR body, and wiki projection
    preserve the finalized plan without semantic invention.

After externalization, GitHub issues, milestones, and PRs are the execution
tracker. The vault plan remains derivation context or restart aid; it must not
diverge into a private second tracker.

## Draft PR Body Requirements

A draft PR created from this workflow must state:

- Target issue set or subtree.
- GitHub milestone.
- Linked issues to close on merge.
- Broader parent issues only referenced.
- Proof obligations claimed, partially claimed, and not claimed.
- Local implementation plan.
- Evidence required for each claim.
- Explicit exclusions and split/follow-up conditions.

A PR may close a parent issue only when the PR explicitly claims the whole subtree
rooted there and the evidence supports that claim. Otherwise close only the issues
actually satisfied and reference the parent.

## Stop Rules

Stop and repair the source plan before externalizing when:

- the plan would create a second roadmap, milestone list, or current-traversal
  status surface instead of using the issue tree;
- proof obligations are treated as tests, check names, or generic acceptance prose;
- a GitHub Milestone has no explicit issue-tree scope;
- a PR claim set cannot be named before implementation starts;
- top-level order is represented only by title numbering when GitHub sub-issue
  order or a wiki roadmap list should own it;
- dependencies are being used to encode ordinary traversal order;
- the wiki would manually mirror live issue/PR status;
- issue creation would require inventing user stories, proof obligations, scope, or
  milestone cuts not present in the source plan.
