---
order: 20
title: .agents/justfile
---

The agent-facing justfile holds recipes for:

- `[private]` hygiene checks (dead code, duplication, complexity, slop)
- `[private]` anti-gaming measures (bypass detection, checker integrity)
- `[private]` debug surfaces (isolated reproducers, artifact dumps, fixture runners)
- `[private]` hook scripts (pre-commit, pre-push)

The top-level `justfile` composes user-facing workflows from these private recipes where needed:

```justfile
# Top-level justfile — user-facing surface
build:
    @project-cli build

test:
    @project-cli test
    @just -f .agents/justfile _test-agent

serve:
    @project-cli serve
```

Agent-facing recipes are never exposed to the user. They exist to prevent agents from bypassing mandatory checks, hacking proof loops, or mutating global state without isolation.
