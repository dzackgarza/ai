# Durable State Surfaces

Every project should converge toward one organized state model:

- The `agent-memory` vault holds reusable decisions, corrections, traps, advice and project context.
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

Select the work unit in the GitHub issue tree with itree. Use Spec Kit to write and
revise its requirements, plan and tasks from the start. The issue body and comments
carry current state and evidence. Use the project constitution for priorities.
When transferring an existing plan, match it to the owning issue first. Preserve
open obligations, acceptance criteria, order, dependencies and evidence.

Direct commits are appropriate when the requested outcome has a bounded owner, can be
verified locally, and needs no public coordination surface. This includes trivial edits
and can include substantive but self-contained maintenance.

Correct planning instructions that send work outside the issue workflow at their source. Classify each
local note, plan, TODO, scratchpad, wiki page, issue, PR, and memory record by durable
owner. Preserve durable narrative in the wiki, reusable lessons in `agent-memory`,
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
