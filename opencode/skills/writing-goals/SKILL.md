---
name: writing-goals
description: "Use when writing a goal, outline, plan, handoff, or task order for an autonomous agent."
---
# Goals, outlines and plans

In practice an autonomous goal outranks the repo's rules, because the worker rereads its
goal and acts on it session after session. So the goal text itself has to carry the
project's priorities. This governs every goal, outline, plan, handoff, and task order an
agent writes.

## Making a goal

- Start from my own statement of the task. Put that first, in my terms.
- One task, with the scope I named. Roadmaps, inventories, later phases stay in their
  owning issue; the goal doesn't talk about them.
- An outline written to answer a question is not a goal. It becomes one only if I issue it
  as one.
- Before writing, read my messages on the project, the governing docs, the owning issues,
  and the current source.
- Find the work by subtraction: required capabilities minus what's actually in the source
  at a named revision. An earlier handoff, report, or checked-off task is a *claim*. It
  doesn't establish status.
- Include the step that connects the parts to the public entry point. Parts that exist but
  aren't hooked up are not the finished capability.
- State the completion condition as behaviours of the software: each required item, its
  acceptance condition, and its status in the source.
- Keep the layers between my words and the work thin. Every generated outline, spec, and
  task list is one more place where a priority can be invented out of nothing. Write only
  the layers the worker actually needs.

## What a goal prioritizes

The order comes from the required functionality that's still missing.

- Order work by missing required functionality. Each early item changes what the software
  can do. Among those, order by real input dependencies: a later item consumes what an
  earlier one produces.
- User-facing work changes a behaviour of the software, including code not yet wired to an
  entry point. Repo-internal work only demonstrates self-consistency and could wait forever
  with no change in behaviour: evidence records, revision pins, receipts, repeated audits,
  demos of functionality that already exists.
- CI state, timeouts, memory limits, benchmarks, and failed expensive runs do not set the
  order. They're evidence for whichever item owns them.
- Performance comes *last*. It starts only once all required functionality exists. A
  functional item can use whatever time and memory it needs. Fix slowness earlier only if a
  small required example of the chosen capability can't finish at all.
- Add no priority that I or the owning issue didn't state. Read the repo's priority rules
  before writing the order.

## What a goal must agree with

- My messages. They're the source of truth for intent. If an agent-written doc disagrees
  with them, fix the doc. Don't present the conflict to me as a decision.
- The repo's constitution, `AGENTS.md`, and work-priority rules, including its separation
  of roles. A rule in a governing doc stands on its own; it doesn't need a matching quote
  from me.
- The owning issue, for the required items and their acceptance conditions.
- The current source, for what's there and what's missing.

A number, budget, workload, trial, or phase gate that shows up only in agent-written text is
a *proposal*. It doesn't enter a goal as a requirement until it traces back to a message of
mine or a governing doc.

## Checking a goal

You check it by reading the goal against its sources. That's a judgment about meaning. A
script, checklist, or receipt only tests form -- perfectly well-formed text can still direct
zero useful work. Answer these for every item, and rewrite the goal when an answer fails:

- Which of my messages or which governing doc requires this item?
- Is it inside the scope I named?
- Is it missing from the source at the named revision?
- Once it's done, does the software behave differently? If not, it's repo-internal and does
  not go ahead of functional items.
- Does each stated prerequisite supply an input this item actually consumes? A prerequisite
  that only supplies evidence is not a dependency.

Then read the whole goal as a worker who has nothing else:

- Does the first action change what the software can do?
- Could a worker satisfy every line and add no required capability? If yes, the goal is wrong.
- Is it still the task I stated -- not narrower, not wider?

The output of an issue selector like `itree next` is just one more claim. Check it the same
way when a session resumes.

(N.B.: ` uvx --from git+https://github.com/dzackgarza/itree itree`)

## Goal text must not contain

- A priority, budget, threshold, or workload with no source in my messages or the governing
  docs. Performance is the repeat offender.
- CI state, a timeout, a memory limit, a benchmark, or a failed expensive run as the reason
  for an item or its position.
- Progress measured in commits, comments, receipts, reading counts, closed tasks, green
  checks, or any other change of state.
- Evidence records, revision pins, exports, inventories, audits, reviews, or frozen trials
  ahead of functional items, or gating them.
- A demo, notebook, or showcase listed as functionality.
- Polish, cleanup, or docs ahead of unfinished functionality.
- An adapter, bridge, or shim that keeps an old interface alive instead of updating its
  consumers.
- Work that belongs to another role, or to a phase outside the named scope.
- Narrowing: a specimen, first witness, fragment, or toy example standing in for the
  required capability.
- Inflation: a capability or prerequisite that neither the requirement nor a real
  dependency calls for.
- A status claim copied from an earlier doc and not read from the source.
- Chores as obligations: commits, pushes, worker status, gates run.
- An instruction to stop, report, or ask when the next step is clear, or a decision for me
  that fails the three checks in Essential rules.
- A task number or internal label with no statement of the behaviour it stands for.
