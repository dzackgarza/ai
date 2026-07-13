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

An external callback is PR monitoring only when it reaches the intended active work owner.
Do not infer that from `hermes webhook list`.

`hermes webhook subscribe` creates a Hermes gateway route that starts a new Hermes agent
run. It neither creates the GitHub subscription nor wakes a Codex, Claude Code, OpenCode,
or Kilo session. Use `webhook-subscriptions` only when the required response belongs to
Hermes.

For another harness, use its actual inbound-session capability. Claude Code Channels can
deliver an external event to a running Claude Code session after its channel server and
public ingress are configured. Codex CLI has no supported inbound channel for arbitrary
external events; its hooks observe Codex lifecycle events and cannot make a Codex session
listen for GitHub callbacks. Do not route Codex through Claude Code merely to obtain this
capability: that wakes Claude Code, not the Codex session.

Report callback-based PR monitoring only after boundary proof:

1. A repository webhook or installed GitHub App is subscribed to the required events.
2. GitHub can reach the public HTTPS delivery endpoint; a bare `localhost` route is not
   sufficient.
3. A real GitHub delivery passes authentication and reaches the target listener.
4. The target harness receives the event in the intended session, or a named replacement
   run starts, and that behavior is observed.

Until this proof exists, do not say that feedback will arrive, that the agent is listening,
or that a PR loop will resume automatically. End the current run normally and leave the
PR's GitHub state as the source of truth for a later explicit check.
