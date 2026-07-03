---
order: 50
title: Engineering Rules
---

- For external tools, dependencies, and known library surfaces, load
  `known-solution-first` before implementing bespoke logic.

- For owned code changes, load the policy skills named in the Bridge-Burning Policy
  Router before writing or reviewing code/tests/QC.

- For long-running commands, use PTYs/sessions and poll them.
  Do not create artificial short timeouts for ordinary engineering work.

- When you kick off a long-running background job — build, test suite, training run,
  batch, remote task, or dispatched agent — and will stop to wait for it, give the user
  an expected-completion ETA before you wait, grounded in the job's own reported
  duration, its historical runtime, or its observed progress rate. Do not go silent and
  leave the user blind to when the job should return. This concrete completion ETA for an
  already-running job is operational status, not a time estimate for proposed work, and is
  the explicit exception to the "never write time estimates" ban.

- For git checkpoints, diffs, commits, and recoverable deletion, load `git-guidelines`.

- For standalone Python scripts, dependency provisioning, missing tools, or install
  choices, load `tool-provisioning-and-environment-hygiene`.

- For markdown/prose rewrites, load `writing-for-agent-audiences` and
  `writing-clearly-and-concisely`.

- After any knowledge-transfer edit, perform an explicit semantic comparison between
  the new destination docs and the old source material.
  Knowledge transfer includes moving instructions into skills, consolidating docs, retiring docs after migration, rewriting prompts, or replacing local procedures with global guidance.
  Check for lost endpoints, commands, hostnames, paths, credential models, state machines, evidence requirements, examples, warnings, and operational constraints.
  Any watering-down, vague summarization, generic regression-to-the-mean wording, missing concrete procedure, or weakened prohibition is a defect.
  Rectify it immediately before deleting, retiring, or relying on the old source.
