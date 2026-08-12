---
order: 20
tags:
- source-system-contract
- source-observed-model-failure
- function-define
- function-procedure
- function-route
- failure-process-overproduction
- retest-model-reasoning
- retest-model-alignment
- retest-model-tool-use
- retest-policy-change
- retest-toolchain-change
title: Skill Routing Matrix
---

| Situation | Load |
| --- | --- |
| Code/tests/QC with a bridge-burning policy concern | `policy-index`, then only the narrower policy skills it routes to |
| Seeing defaults/fallbacks/mocks/skips/smoke/quarantine/deletion | `anti-slop`, `reviewing-llm-code/references/bridge-burning-red-flags.md`, `fixing-slop` |
| Fixing a slop finding | `fixing-slop` before editing |
| Reviewing LLM/agent output | `reviewing-subagent-work`, `reviewing-llm-code`, `anti-slop` |
| Acting on PR review feedback | `pr-feedback-triage`, `git-guidelines`, `test-guidelines` |
| Substantive repository work that depends on shared project state, or requested normalization of missing project surfaces | `project-initialization`, then only the owners it routes to |
| Behavioral regression or uncertain implementation failure | `reality-grounded-debugging`, `systematic-debugging`; add `known-solution-first` for external tools/errors |
| Negative findings or partial source reads | `epistemic-integrity`; add `reading-transcripts` for conversation logs |
| Plans or plan feedback that must survive the turn | `plan`, `agent-memory`; add `response-preparation` only for a substantive report |
| Roadmap, PRD, cross-agent, review-track, or proof-bearing work requiring public coordination | `project-initialization`, `plan`, `agent-memory`, `git-guidelines`; add downstream execution skills only when their phase begins |
| Using Jules for review | `jules`, `jules/references/anti-slop-report-review.md`; do not use Jules for immediate remediation |
