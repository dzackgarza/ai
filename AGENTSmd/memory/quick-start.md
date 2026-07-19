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
- failure-context-loss
- failure-proxy-evidence
- failure-state-misplacement
- retest-model-self-evaluation
- source-observed-model-failure
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

Store significant experiences whose sequence, consequences, causal cues, or uncertainty
would be lost if compressed into a rule; stable operational knowledge; environment quirks;
cross-session context; technical findings; decisions and rationale; contemporaneous
reflections; and later reinterpretations. Distinguish what happened, what seemed causally
important, and what might help in the future. Proposed interventions are fallible products
of memory, not memory's definition.

Do not store git-history duplicates, live status mirrors, contentless work summaries, or
live TODOs. Those belong in git or GitHub issues. Preserve chronology when the order of
events is itself evidence.
