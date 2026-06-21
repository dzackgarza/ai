---
order: 20
title: Skill Routing Matrix
---

| Situation | Load |
| --- | --- |
| Writing or reviewing code/tests/QC | `policy-index`, `anti-slop`, `bespoke-software-policy`, `reviewing-llm-code/references/bridge-burning-red-flags.md`, `test-guidelines` |
| Seeing defaults/fallbacks/mocks/skips/smoke/quarantine/deletion | `anti-slop`, `reviewing-llm-code/references/bridge-burning-red-flags.md`, `fixing-slop` |
| Fixing a slop finding | `fixing-slop` before editing |
| Reviewing LLM/agent output | `reviewing-subagent-work`, `reviewing-llm-code`, `anti-slop` |
| Acting on PR review feedback | `pr-feedback-triage`, `git-guidelines`, `test-guidelines` |
| Debugging failures | `reality-grounded-debugging`, `systematic-debugging`; add `known-solution-first` for external tools/errors |
| Negative findings or partial source reads | `epistemic-integrity`; add `reading-transcripts` for conversation logs |
| Plans or plan feedback | `plan`, `agent-memory`; add `response-preparation` for the report |
| Using Jules for review | `jules`, `jules/references/anti-slop-report-review.md`; do not use Jules for immediate remediation |
