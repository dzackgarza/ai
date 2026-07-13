---
order: 30
tags:
- source-owner-preference
- source-system-contract
- function-constrain
- function-procedure
- function-route
- retest-model-tool-use
- retest-policy-change
- retest-toolchain-change
title: Monitoring PR Activity
---

A completed local CLI session is not a PR monitor. Do not say it is listening,
waiting for feedback, or will resume automatically.

GitHub remains the PR’s source of truth. When a task is explicitly resumed, inspect the
current reviews, comments, checks, and commits through the repository’s normal GitHub
surface before acting. A separate local service, event log, or another harness does not
supply a generic wake-up path for that session.
