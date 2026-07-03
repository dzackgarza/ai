---
order: 30
title: Operational Rules
---

Load applicable skills before acting.
If a listed skill applies, that skill owns the detailed procedure.

- Git, deletion, checkpoints, commits, and destructive-operation bans:
  `git-guidelines`
- Memories, durable guidance, project binding, and memory mutations: `agent-memory`
- Negative findings, targeted misses, partial reads, and "not found" claims:
  `epistemic-integrity`
- Tests, mocks, proof quality, and red/green obligations: `test-guidelines` plus
  `reality-grounded-debugging`
- Missing tools, dependencies, Python script dependencies, or install pathways:
  `tool-provisioning-and-environment-hygiene`
- External APIs, providers, compilers, packages, and exact diagnostics:
  `known-solution-first`
- Completion reports and concise user-facing status: `response-preparation`
- Corrections, critiques, remaining-work questions, and anti-laundering:
  `handling-corrections`
- Nontrivial roadmap, PRD, feature, cross-agent, review-track, or proof-bearing work:
  `project-initialization`, `plan`, `agent-memory`, and `git-guidelines`; add
  `proof-obligation-workflow`, `implement_plan`, or `subagent-driven-development` when
  their work starts

Never write or discuss time estimates for work you suggest. The sole exception is the
completion ETA for a long-running background job you have already started and are about to
wait on (see Engineering Rules).
Never insert manual section counters in Markdown.
Keep canonical facts in one source and route to it instead of restating dynamic
metadata.
