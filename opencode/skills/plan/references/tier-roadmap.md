# Roadmap / Strategic Tier

> Load this after routing to the roadmap tier in `../SKILL.md`. The universal skeleton and
> policies there still apply; this file supplies the roadmap body and quality bar.

A roadmap plan gives constraining direction without doing the implementer's work. It fixes
phases, invariants, user stories, and outcomes, and names which phases are complex enough
to spawn their own child plan. It carries no task-level detail and never prescribes a diff.

## When this tier applies

- The work spans multiple phases, milestones, or workstreams.
- You are setting direction that others — agents or child plans — will execute under.
- The decomposition is still being discovered and must stay a roadmap until it is stable.

## Body section (replaces the universal work-decomposition slot)

The universal skeleton already carries the `Execution Graph`. Add Milestones as the
work decomposition:

```markdown
## Milestones
### <Milestone name>
- Result:
- Dependencies:
- Acceptance:
- Verification:
- Stop conditions:
- Spawns child plan: <yes + intended child plan key, or no>
```

## Milestones

Milestones describe delivered capability or restored correctness. The progress checklist
tracks granular execution. Keep them separate.

A milestone must state:

- the result that will exist at the end;
- what it blocks or depends on;
- which work can happen in parallel;
- how integration is verified;
- what observable evidence proves it is complete.

Use a prototyping milestone when requirements depend on unknown library, runtime, UI, API,
or proof behavior. A prototype must be additive, bounded, and tied to a promotion or
discard decision.

Use parallel workstreams only when their interfaces are explicit. State what each stream
produces, consumes, and must preserve for integration (record this in the skeleton's
Execution Graph).

## User stories first

Derive milestones, dependencies, and acceptance criteria from user stories and
user-observable outcomes, not from implementation guesses. Do not invent thin stories from
implementation details. When stories are missing, vague, or conflicting, prompt the user
for the product and workflow facts needed to write them before drafting milestones.

## Invariants

State invariants as properties that must always hold, phrased to constrain outcomes without
dictating implementation — for example: "every cited item is canonical-backed, carries a
prose provenance note, or is explicitly on the review list." An invariant a wrong
implementation could still satisfy is decoration, not direction; cut it or sharpen it.

## Spawning child plans

Mark each milestone or phase too complex to expand inline as one that must spawn its own
child plan at a closer-to-implementation tier. Do not expand it here. Record the intended
child plan key so the tree link exists before the child is written. The roadmap stays the
parent the child points back to.

## Altitude check (roadmap-specific)

At this altitude the failure is vagueness that constrains nothing. Before saving, confirm
every milestone and invariant rules something out: a competent but adversarial implementer
reading only this plan could not satisfy it while building the wrong thing. If they could,
the milestone is aspirational framing — sharpen the observable boundary.
