---
order: 7
tags:
- source-owner-context
- source-owner-preference
- source-system-contract
- source-observed-model-failure
- function-orient
- function-define
- function-constrain
- function-procedure
- function-route
- function-allocate
- function-evaluate
- failure-state-misplacement
- failure-destructive-state-change
- failure-context-loss
- failure-process-overproduction
- retest-model-reasoning
- retest-model-alignment
- retest-model-memory
- retest-policy-change
- retest-toolchain-change
title: Durable State Surfaces
---

Every project should converge toward one organized state model:

- `agent-memory` central vault: private or converging plans, phase state, queues,
  residue ledgers, durable corrections, reusable decisions, traps, advice, and project
  context.
- GitHub issue tree, GitHub Milestones, and PR claim maps: public execution state for
  nontrivial work, active user stories, roadmap nodes, feature contracts, proof burdens,
  long-running handoffs, accepted work contracts, and auditable progress.
- GitHub wiki: durable long-horizon project knowledge, feature doctrine, requirements,
  architecture decisions, design rationale, user-story narrative, and readable roadmap or
  proof projections. It is not the live execution tracker.
- `.agents/`: private agent automation, guardrail recipes, diagnostics, hook helpers,
  and scripts. It is not a durable documentation or planning store.
- Repo-local scratch files: temporary work surfaces for in-the-weeds investigation only.
  "Scratch" means artifacts this agent created for the current task. Before handoff,
  delete or promote only that owned scratch. Pre-existing, concurrent, or provenance-unknown
  files are not scratch; preserve them and report any conflict.

Work that requires public coordination or handoff must route through the GitHub execution
model. This includes roadmap or PRD execution, multi-agent or long-running handoffs,
review-track work, and proof-bearing work whose claims need public tracking.
Implementation complexity by itself does not create that requirement. The route is:

1. Use `project-initialization` to inspect existing wiki, issue tree, milestones, PRs,
   draft PRs, and memory binding.
2. Use `plan` and `agent-memory` while the plan is private or converging.
3. Before implementation, use `plan/references/externalization.md` and `git-guidelines`
   to place the work in the GitHub issue tree, select or create the GitHub Milestone
   scope, and create the PR claim map when a branch claims work.
4. Use `implement_plan` or `subagent-driven-development` only after the issue tree,
   milestone scope, and PR claim set are known, unless the user explicitly requested a
   diagnosis-only or audit-only pass.

Direct commits are appropriate when the requested outcome has a bounded owner, can be
verified locally, and needs no public coordination surface. This includes trivial edits
and can include substantive but self-contained maintenance.

Mixed-state repositories must be migrated only when the mixed state overlaps the requested
work or prevents a safe handoff. Do not turn unrelated normalization into a prerequisite
for a bounded task. When migration is in scope, classify each
local note, plan, TODO, scratchpad, wiki page, issue, PR, and memory record by durable
owner. Preserve durable narrative in the wiki, private restart state in `agent-memory`,
and active execution state in GitHub issues, milestones, and PRs. Replace duplicate local
status with links to the canonical surface. Delete only scratch this agent created and
can prove has no continuing coordination value; unknown-origin artifacts require an
explicit user decision.

Do not keep the same durable fact authoritative in more than one place.
When a repo is mixed, classify each local note, plan, TODO, scratchpad, and process doc by
its durable owner, then migrate or link it instead of letting local residue accumulate.

Small observed errors or inefficiencies should become an immediate fix or GitHub issue
when they belong to the current coherent work unit or the user requested tracking.
Do not interrupt a bounded task to create unrelated administrative work; report a real
blocking defect instead.
