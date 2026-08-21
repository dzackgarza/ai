# The .agents Directory

Every project root contains a `.agents/` directory. This is the canonical location for
agent-facing project artifacts that are not durable memory or durable documentation:

- **`justfile`** — Agent-facing recipes for QC, debugging, and guardrail enforcement. All recipes are `[private]`.
- **Scripts** — Hygiene checks, anti-gaming measures, slop detection, hook scripts. Scripts that encode reusable diagnostic surfaces live here, referenced by the private justfile.

Durable operational knowledge, corrections, decisions, and planning state are managed
through `agent-memory` and bound by `.agent-memory.toml`; they are not maintained as loose
markdown under `.agents/`.
Durable project narrative and readable roadmap/proof projections belong on the wiki.
Active user stories, roadmap nodes, feature contracts, proof burdens, and handoffs belong
in the GitHub issue tree, GitHub Milestones, and PR claim maps.
If a local `.agents/` note starts carrying durable guidance, migrate it to the vault,
wiki, or GitHub issue/PR surface that owns it, then remove or replace the local note with
a pointer.

Nothing in `.agents/` is user-facing. The top-level `justfile` may route through agent
recipes to enforce mandatory measures, but those recipes are `[private]` and invisible to
`just --list`.

## .agents/justfile

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
