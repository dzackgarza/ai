---
order: 10
title: Quick Start
---

Load `agent-memory` for the exact command surface.

Use the GitHub `uvx` runner by default:

```bash
uvx --python 3.14 --from git+https://github.com/dzackgarza/agent-memory agent-memory --help
```

Use it for memory search, retrieval, project binding, doctor checks, and adding typed
project/global memories. Use a bare `agent-memory` command only after verified setup has
placed it on `PATH`.
Prefer `inspect` and `search` before broad filesystem scans of memory vaults.

Store stable operational guidance, environment quirks, cross-session execution context,
technical findings, and durable decisions.
Do not store changelogs or audit trails; those belong in git.
