---
order: 10
tags:
- source-owner-preference
- source-system-contract
- function-define
- function-constrain
- function-procedure
- function-route
- function-allocate
- retest-model-memory
- retest-policy-change
- retest-toolchain-change
- retest-environment-change
title: Quick Start
---

Load `agent-memory` for the exact command surface.

Use the GitHub `uvx` runner by default:

```bash
uvx --python 3.14 --from git+https://github.com/dzackgarza/agent-memory agent-memory --help
```

Use it for memory search, retrieval, project binding, doctor checks, adding typed
project/global memories, and creating or updating `plan` records. Use a bare
`agent-memory` command only after verified setup has placed it on `PATH`.
Prefer `inspect` and `search` before broad filesystem scans of memory vaults.

Store stable operational guidance, environment quirks, cross-session execution context,
technical findings, durable corrections, durable decisions, and all plan state that must
survive a context window.
Do not store changelogs or audit trails; those belong in git. Do not store live TODOs;
those belong in GitHub issues when they outlive the immediate task.
