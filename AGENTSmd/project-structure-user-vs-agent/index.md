---
order: 120
tags:
- purpose-context
- purpose-preference
- purpose-policy
- purpose-reference
- purpose-remediation
- stability-model-independent
- stability-model-contingent
- stability-policy-contingent
- stability-tool-contingent
title: 'Project Structure: User vs. Agent'
---

Every project has two audiences: the user, and agents working on the user’s behalf.

**What the user sees** is the project: source code, public interfaces, user-facing config, and a top-level `justfile` that exposes real workflows (`build`, `test`, `serve`).

**What agents need** is guardrails: process documentation, QC scripts, hooks, anti-gaming measures, slop checks, and diagnostic surfaces. These exist to constrain agent behavior, not to serve the user’s workflow.

These two surfaces must be kept separate. Agent-facing automation belongs in `.agents/`.
Durable agent knowledge and plans belong in the central `agent-memory` vault; durable
project doctrine belongs on the wiki; public execution state belongs in the GitHub issue
tree, GitHub Milestones, and PR claim maps. The user should never need to inspect
`.agents/` to understand the project.
