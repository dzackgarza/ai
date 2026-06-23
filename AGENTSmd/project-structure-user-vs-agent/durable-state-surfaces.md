---
order: 7
title: Durable State Surfaces
---

Every project should converge toward one organized state model:

- `agent-memory` central vault: plans, phase state, queues, residue ledgers,
  durable corrections, reusable decisions, traps, advice, and project context.
- GitHub wiki: durable long-horizon project knowledge, user stories, feature doctrine,
  roadmaps, proof burdens, requirements, architecture decisions, and design rationale.
- GitHub issues, milestones, and PRs: public project organization, external execution
  state, long-running handoffs, user-visible gaps, accepted work contracts, and
  auditable progress.
- `.agents/`: private agent automation, guardrail recipes, diagnostics, hook helpers,
  and scripts. It is not a durable documentation or planning store.
- Repo-local scratch files: temporary work surfaces for in-the-weeds investigation only.
  Before handoff, delete them or promote their durable content to the vault, wiki, or
  GitHub surface that owns it.

Do not keep the same durable fact authoritative in more than one place.
When a repo is mixed, classify each local note, plan, TODO, scratchpad, and process doc by
its durable owner, then migrate or link it instead of letting local residue accumulate.

Small observed errors or inefficiencies in repos this system owns should become either an
immediate fix or a GitHub issue on the owning repo.
Do not let repeated surprises, user corrections, tool friction, false greens, or app
paper cuts remain only in chat, local notes, or memory.
