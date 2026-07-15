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

Use the loop owned by the active harness:

- **Claude Code:** use its native Channels capability to deliver a verified GitHub event
  into the active Claude Code session. Keep that session and its Channel listener running;
  confirm an actual delivery reaches the session before relying on it.
- **Codex:** wait 60–120 seconds after requesting review or CI, then re-check the PR through
  GitHub. Use `gh pr checks` and the repository’s review-feedback scan; repeat the
  wait-and-check loop while the review is pending. Codex must not claim it is listening
  for a callback.
- **Other harnesses:** use their documented native event mechanism when one exists.
  Otherwise, re-check GitHub explicitly.

GitHub remains the PR’s source of truth. Every returned event or re-check begins with the
current reviews, comments, checks, and commits before triage.
