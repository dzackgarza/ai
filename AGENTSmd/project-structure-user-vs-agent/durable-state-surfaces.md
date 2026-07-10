---
order: 7
tags:
- purpose-context
- purpose-preference
- purpose-policy
- purpose-procedure
- purpose-reference
- purpose-remediation
- stability-model-contingent
- stability-policy-contingent
- stability-tool-contingent
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

All nontrivial work must route through the GitHub execution model before implementation
or public handoff. Nontrivial work includes roadmap, PRD, feature, cross-agent,
long-running, review-track, or proof-bearing work. The route is:

1. Use `project-initialization` to inspect existing wiki, issue tree, milestones, PRs,
   draft PRs, and memory binding.
2. Use `plan` and `agent-memory` while the plan is private or converging.
3. Before implementation, use `plan/references/externalization.md` and `git-guidelines`
   to place the work in the GitHub issue tree, select or create the GitHub Milestone
   scope, and create the PR claim map when a branch claims work.
4. Use `implement_plan` or `subagent-driven-development` only after the issue tree,
   milestone scope, and PR claim set are known, unless the user explicitly requested a
   diagnosis-only or audit-only pass.

Trivial direct commits are allowed only when the outcome, scope, proof, and rollback are
obvious from the diff itself and no public coordination surface is needed.

Mixed-state repos must be migrated into this model before feature work. Classify each
local note, plan, TODO, scratchpad, wiki page, issue, PR, and memory record by durable
owner. Preserve durable narrative in the wiki, private restart state in `agent-memory`,
and active execution state in GitHub issues, milestones, and PRs. Replace duplicate local
status with links to the canonical surface. Delete only scratch this agent created and
can prove has no continuing coordination value; unknown-origin artifacts require an
explicit user decision.

Do not keep the same durable fact authoritative in more than one place.
When a repo is mixed, classify each local note, plan, TODO, scratchpad, and process doc by
its durable owner, then migrate or link it instead of letting local residue accumulate.

Small observed errors or inefficiencies in repos this system owns should become either an
immediate fix or a GitHub issue on the owning repo.
Do not let repeated surprises, user corrections, tool friction, false greens, or app
paper cuts remain only in chat, local notes, or memory.
