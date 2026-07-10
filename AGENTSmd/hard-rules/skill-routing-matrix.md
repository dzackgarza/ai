---
order: 20
tags:
- source-system-contract
- function-define
- function-procedure
- function-route
- retest-model-tool-use
- retest-policy-change
- retest-toolchain-change
title: Skill Routing Matrix
---

| Situation | Load |
| --- | --- |
| Writing or reviewing code/tests/QC | `policy-index`, `anti-slop`, `bespoke-software-policy`, `reviewing-llm-code/references/bridge-burning-red-flags.md`, `test-guidelines` |
| Seeing defaults/fallbacks/mocks/skips/smoke/quarantine/deletion | `anti-slop`, `reviewing-llm-code/references/bridge-burning-red-flags.md`, `fixing-slop` |
| Fixing a slop finding | `fixing-slop` before editing |
| Reviewing LLM/agent output | `reviewing-subagent-work`, `reviewing-llm-code`, `anti-slop` |
| Acting on PR review feedback | `pr-feedback-triage`, `git-guidelines`, `test-guidelines` |
| Starting work in a repository, cloning/switching projects, or seeing missing `.agents`, memory, justfile, QC, hooks, or CI surfaces | `project-initialization`, then `git-guidelines`, `agent-memory`, `justfile`, or `tool-provisioning-and-environment-hygiene` as routed by the skill |
| Debugging failures | `reality-grounded-debugging`, `systematic-debugging`; add `known-solution-first` for external tools/errors |
| Negative findings or partial source reads | `epistemic-integrity`; add `reading-transcripts` for conversation logs |
| Plans or plan feedback | `plan`, `agent-memory`; add `response-preparation` for the report |
| Nontrivial roadmap, PRD, feature, cross-agent, review-track, or proof-bearing work | `project-initialization`, `plan`, `agent-memory`, `git-guidelines`; add `proof-obligation-workflow` when stories/proof burdens are in scope and `implement_plan` or `subagent-driven-development` before execution |
| Using Jules for review | `jules`, `jules/references/anti-slop-report-review.md`; do not use Jules for immediate remediation |
