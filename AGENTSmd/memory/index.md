---
order: 90
tags:
- source-owner-context
- source-owner-preference
- source-system-contract
- function-orient
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
title: Memory
---

Durable memory and project planning state are managed by `agent-memory`, invoked by default through `uvx --python 3.14 --from git+https://github.com/dzackgarza/agent-memory agent-memory`.
Memories are typed plain-Markdown files in a vault, addressed by key (e.g. `projects/<project-id>/decisions/parser-choice`), and split across two scopes:

- **global** — durable, cross-repo operational knowledge ("what this system is": environment conventions, machine stewardship, recurring workflows).
- **project** — knowledge bound to a single repository via `.agent-memory.toml`.

Memory **types** are `decision`, `trap`, `advice`, `context`, `reference`, and `plan`.
The types classify records; they do not define memory as a policy ledger. `reference` and
`context` may preserve significant experiences, their consequences, causal sequence,
contemporaneous reflections, later interpretations, uncertainty, and alternative
explanations. `advice` and `trap` hold proposed working guidance; they must not replace the
experience that grounds them when that experience remains valuable.
Use `plan` records for every plan, contract, phase state, queue, residue ledger, and
other planning state that must survive context windows.
Plans belong in the central vault through `agent-memory`, not as loose repo-local
Markdown.

**Store:** Significant experiences that would lose meaning if reduced to a rule; stable
operational knowledge; environment quirks; cross-session execution context; technical
findings; decisions and rationale; contemporaneous lessons; and later interpretations.
Separate observation, interpretation, and proposed intervention. A memory need not
instruct a future agent.

**Promote:** If a decision changes public project direction, user stories, proof burdens,
roadmaps, or cross-agent handoff state, update the owning GitHub issue, milestone, PR, or
wiki page as well as any needed memory.

**Do not store:** Git-history duplicates, live status mirrors, contentless work summaries,
or live TODO lists. Those belong in git or GitHub issues. Chronology is not itself an
audit trail: preserve sequence when it carries cause-and-effect, consequences, changing
interpretation, or details needed to recognize a related future incident.

**Setup:** use the `uvx` runner for normal invocation and project binding:
`uvx --python 3.14 --from git+https://github.com/dzackgarza/agent-memory agent-memory init project --vault <vault>`.
Use the checkout's `just setup` only when provisioning the global vault and persistent runtime dependencies.
Validate a repository's wiring with `uvx --python 3.14 --from git+https://github.com/dzackgarza/agent-memory agent-memory doctor`.
