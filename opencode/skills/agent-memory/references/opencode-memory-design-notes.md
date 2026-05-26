# OpenCode Memory and Todo Design Notes

These notes define candidate design requirements for OpenCode memory and todo tooling.

## Current Comparator

The visible GitHub comparator is `dzackgarza/opencode-plugin-improved-todowrite` and its
related `todowrite-manager` repository.
It already covers the core hierarchical todo tree surface:

- CLI-first implementation with OpenCode and MCP as thin adapters.

- SQLite-backed session storage.

- Stable todo node IDs.

- Nested todo trees with status, priority, content, children, and metadata.

- Shared response contract across CLI, plugin, and MCP paths.

## Ideas Not Covered by the Current Comparator

These ideas are candidates for an OpenCode memory/todo roadmap if they survive direct
design review:

- **Project-aware scoping:** distinguish local project memory from global memory using a
  stable project identity, preferably derived from git rather than working-directory
  strings alone.

- **Semantic memory separate from todos:** do not overload the todo tree as a long-term
  knowledge base. Todos track work state; memory retrieves durable reusable facts,
  constraints, and decisions.

- **Neighborhood navigation:** expose focused views around the current todo: ancestors,
  nearby siblings, next branch, blocked descendants, and recently completed context.
  This is more useful than dumping the full tree into every prompt.

- **Chunk, phase, and feature views:** allow slicing a large todo tree by execution
  phase, feature area, or dependency cluster, while keeping the full tree canonical.

- **Hybrid todo search:** combine exact text filters with semantic search and scope
  filters such as current project, global, or all.
  Search results should preserve enough tree context to decide what to do next.

- **Current-node state:** keep an explicit current todo ID so tools can answer “what is
  adjacent to this task?”
  without relying on text search.

- **Timestamp gap detection:** detect long gaps between interactions and surface the
  last active todo, recent decisions, and stale assumptions before work resumes.

- **Workflow-state detection:** infer whether the session is planning, implementing,
  reviewing, debugging, or blocked from actual todo state and recent actions, then
  tailor the view accordingly.

- **Workflow templates:** support reusable trees for common flows, but apply them as
  concrete todo nodes with stable IDs rather than as sidecar marker files.

- **External-state validation:** when todo or memory claims depend on a remote service,
  persisted database, or user-visible artifact, validation must check that boundary
  instead of local file existence alone.

- **Marked test data:** generated test fixtures should carry unique markers so cleanup
  and origin tracking are reliable without fuzzy deletion.

## Implementation Patterns Worth Evaluating

These patterns should be treated as candidate designs, not default requirements:

- **Transport split:** keep the memory service usable from CLI-first local tooling while
  also allowing HTTP/SSE access for clients that cannot run stdio servers.

- **Thin adapter boundary:** keep MCP/OpenCode adapters thin.
  Retrieval, consolidation, storage, and ranking logic should live in ordinary modules
  with direct tests.

- **Installation automation:** provide one command that detects supported clients,
  writes the right MCP/plugin config, and validates the resulting tool call.
  Manual JSON editing should not be the normal installation path.

- **Prompt/resource fallback:** expose critical guidance as MCP prompts or resources
  when a client does not reliably select tools first.

- **Decay with importance boosts:** if memory aging is implemented, combine age decay
  with connection count, recency of access, and explicit importance rather than deleting
  purely by timestamp.

- **Adaptive clustering:** if consolidation uses clustering, parameters should adapt to
  corpus size and be inspectable.
  Fixed thresholds are brittle across small personal notes and large project histories.

- **Marketing-claim audit:** when evaluating external memory tools, document only
  concrete algorithms, data structures, transport choices, and operational constraints.
  Ignore vague claims unless the implementation shows how they are achieved.

## Memory Data Model Requirements

These requirements apply to memory tooling separately from active todo state:

- **Entity-observation separation:** store intrinsic facts as atomic observations about
  an entity, and store relationships as separate directed edges.
  Do not bury relationships inside free-form summaries.

- **Active-voice relationship labels:** relation names should read as
  subject-verb-object edges, such as `project_uses_tool` or `paper_supports_claim`.
  Direction should be semantically obvious from the label.

- **Atomic observations:** each observation should hold one reusable fact.
  A paragraph with several unrelated facts is harder to update, invalidate, or retrieve
  accurately.

- **Type hints, not rigid schemas:** entity types should guide reasoning and retrieval
  without forcing every future fact into a fixed table-shaped schema.

- **Explicit retrieval before use:** when memory is relevant, retrieve it before
  planning or acting. Memory that is only written and never retrieved is archival, not
  operational.

- **Debuggable retrieval:** semantic retrieval should be able to expose match scores or
  ranking metadata for tuning.
  Silent retrieval failures are hard to diagnose.

- **Controlled consolidation:** automated decay, clustering, association, and
  compression should produce reviewable candidate changes unless the system has
  empirical evidence that automatic mutation is safe.

## Non-Goals

- Do not implement memory as session JSON dumps.

- Do not implement memory/todo state as hook telemetry.

- Do not add large relational telemetry schemas unless a current product requirement
  justifies that operational surface.
