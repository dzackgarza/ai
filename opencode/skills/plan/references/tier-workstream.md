# Workstream / Organizational Tier

> Load this after routing to the workstream tier in `../SKILL.md`. The universal skeleton
> and policies there still apply; this file supplies the workstream body and quality bar.

A workstream plan takes real requirements, gathered feedback, or a heterogeneous item set
and coalesces it into typed workstreams. Its value is organization: turning a pile into a
few named streams with shared shape and shared acceptance so execution is parallelizable
and nothing is reinvented on fresh context. It defers per-item judgment to execution.

## When this tier applies

- You hold concrete feedback, a review queue, or a large heterogeneous item set.
- The hard part is intelligent judgment per item, not unknown mechanism.
- Resolving every item now would be doing the executor's research inside the plan.

## The core move: coalesce into typed workstreams

Group the items into a few typed workstreams. Each workstream names:

- the item set and its count ("15 items");
- the shared remediation shape ("book sections to migrate to an ambient book with a real
  Zotero book-section sub-item");
- shared acceptance — what proves any item in the stream is done;
- the criteria and tie-breakers the executor applies (see below);
- where the executor records work so passes accumulate — a freeform prose ledger.

Coalescing is not classifying. Grouping into typed workstreams is the correct move.
Encoding the per-item interpretive decision into a classifier, schema, or state machine so
the agent never has to read the item again is banned. Coalesce to the workstream; leave
item-level judgment to execution.

## Body section (replaces the universal work-decomposition slot)

```markdown
## Workstreams
### <Workstream name> (<count> items)
- Items / how to enumerate:
- Shared remediation shape:
- Criteria and tie-breakers:
- Shared acceptance:
- Executor ledger:
- Parent outcome served:
```

## Feedback must drive the plan

A workstream plan built from gathered feedback must force the executor to consult that
feedback. If the plan could be executed end to end without ever reading the feedback, it
has failed at this tier — that is the worst-of-both-worlds outcome where 100 items of
detailed review produce a plan generic enough to ignore them. Quote or reference the actual
dispositions; do not summarize them into generic verbs.

## Criteria elicitation is the deliverable

For judgment-heavy work the planning act is eliciting and freezing the user's domain
criteria up front: per-type "good enough" rules, preferences, and tie-breakers (for
example: prefer DOI over ISBN; one ISBN per book, latest edition; lecture notes need a live
URL). A plan that invents these licenses fresh subagents to reinvent requirements mid-task.
If the criteria are not known, the blocking next step is asking the user, not building
machinery to paper over the gap.

## Implementation is often an intelligent pass

When the hard part is judgment, the implementation is usually an agent pass with a loose,
open-ended prompt and a freeform prose ledger, not deterministic control flow. Plan toward
that: state the problem, the criteria, and the output shape, then let the agent reason. Do
not cage judgment inside rules, scoring tables, exact-match pipelines, certificates, or
schemas. The durable artifact is corrected state plus a prose note explaining what was
tried and what remains, so the next agent continues instead of restarting.

## Tasks at this tier

A workstream is not a task list. Where a task field would normally name a file and a diff,
name the endpoint and observable result instead; the exactness lives in shared acceptance
and the executor's per-item proof. Per-item routing decisions are made during execution and
recorded in the ledger, not pre-decided here.
