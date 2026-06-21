---
order: 50
title: Engineering Rules
---

- **Favor mature dependencies.** Outsource common patterns to minimize owned surface.

- **Iterate, don’t replace.** Writing an entire file is almost NEVER correct, unless greenfielding a new file.

- **Use PTYs for long-running commands.** NEVER wrap ordinary shell commands in short `timeout` calls unless the task specifically asks for a timeout or the command itself requires one.
  Run long-running work in an async PTY/session and poll it until it exits.
  If a timeout is genuinely required, it should usually be measured in minutes, not seconds.
  No research or engineering task is so time sensitive that impatience is worth corrupting the result: premature timeouts more than double the work by forcing agents to discover the artificial failure, reconcile partial state, and rerun the same command correctly.

- Run `git diff` after rewrites — see what you lost semantically.
  If valuable or unintentional, restore it carefully before moving forward.

- **Auto-formatting is intentional QC.** All edits are automatically formatted by tooling (e.g., flowmark, prettier, ruff, etc.). This is NOT noise — it improves code and writing quality over time.
  Do NOT omit auto-formatting changes from git commits.
  Do NOT attempt to manipulate git to "only" commit your intended change and ignore formatting.
  Do NOT attempt to undo auto-formatting, ever.
  It is a feature, not a side effect.

- After any knowledge-transfer edit, immediately perform an explicit semantic comparison between the new destination doc(s) and the old source material.
  Knowledge transfer includes moving instructions into skills, consolidating docs, retiring docs after migration, rewriting prompts, or replacing local procedures with global guidance.
  Check for lost endpoints, commands, hostnames, paths, credential models, state machines, evidence requirements, examples, warnings, and operational constraints.
  Any watering-down, vague summarization, generic regression-to-the-mean wording, missing concrete procedure, or weakened prohibition is a defect.
  Rectify it immediately before deleting, retiring, or relying on the old source.
