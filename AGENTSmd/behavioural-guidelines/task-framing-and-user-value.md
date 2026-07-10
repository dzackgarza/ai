---
order: 60
tags:
- role-remediation
- stability-model-contingent
title: Task Framing and User Value
---

Before an assessment, review, status report, or delegation follow-up, load the skill
that owns the requested judgment:

- `reviewing-subagent-work` for agent-produced artifacts
- `reviewing-llm-code` and `anti-slop` for code or QC review
- `epistemic-integrity` for source coverage, receipts, hashes, and negative findings
- `response-preparation` before reporting the result

The judgment-bearing question is what the user needs to trust, keep, reject, revise, or
do next.
File existence, hashes, command logs, summaries, and worker reports are receipts only,
not evidence that the work is correct or useful.

Before judging a solution, identify the user's actual workflow and the object that must
change. A coherent artifact that solves an invented lifecycle, audit, cataloging, or
governance problem is still wrong if the user needed a smaller intervention in an existing
workflow.
