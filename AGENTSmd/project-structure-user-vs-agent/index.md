---
order: 120
title: 'Project Structure: User vs. Agent'
---

Every project has two audiences: the user, and agents working on the user’s behalf.

**What the user sees** is the project: source code, public interfaces, user-facing config, and a top-level `justfile` that exposes real workflows (`build`, `test`, `serve`).

**What agents need** is guardrails: process documentation, QC scripts, hooks, anti-gaming measures, slop checks, and diagnostic surfaces. These exist to constrain agent behavior, not to serve the user’s workflow.

These two surfaces must be kept separate. Agent-facing artifacts belong in `.agents/`. The user should never need to see or interact with them.
