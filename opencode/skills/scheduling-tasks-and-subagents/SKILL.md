---
name: scheduling-tasks-and-subagents
description: Use when creating an independently useful recurring task or a delayed command with a verified delivery target.
---
# Scheduling Tasks and Subagents

`task-sched` creates persistent systemd scheduled commands. Use it only when the command
should keep running independently of the agent session.

A scheduled command is not a timer that wakes the agent which created it. It runs its own
command and writes its own result. It wakes an agent only when that command explicitly
uses a configured, live harness ingress and a real delivery to that ingress has been
verified. Scheduler logs and `--on-complete` do not return results to the originating
session.

## Decision: Which Tool?

| Need | Use | Why |
| --- | --- | --- |
| Active session; wait 1–2 minutes, then act | Normal shell command with `sleep` | The session owns the wait; no persistent state |
| Codex waits for an external PR/CI event | The Codex PTY-loop pattern | Read the [[codex/SKILL|codex]] skill; it exits a one-off PTY process when new information arrives |
| Claude Code receives an external PR/CI event | Claude Code Channels | Read the [[claude-code/SKILL|claude-code]] skill; Channels provide native delivery into an active session |
| One independent command at a later time | `at` | Use only when its command has an independent result or verified delivery target |
| Recurring work that should outlive this session | `task-sched` | Creates a persistent systemd timer with its own lifecycle |

Do not use `at` or `task-sched` for an active PR loop, a short delay, or generic “wake
me later” behavior. Use the owning harness’s mechanism instead.

## Persistent Tasks (`task-sched`)

`task-sched` is appropriate for independently useful recurring work: for example, a
periodic maintenance command, report, backup, or health check. Before adding one, name:

1. the task’s durable owner and purpose;
2. why it remains useful after the current session ends;
3. its schedule and expected effect; and
4. the explicit removal or replacement condition.

Test the command first. Then add it, record its task ID, inspect `task-sched list`, and
use `task-sched log <task-id>` when it fails. Remove it when its stated lifecycle ends.

Scheduled commands run with a minimal environment. Use `--working-dir` when the command
needs a project directory. Use `direnv exec` only when that command actually requires the
project environment; do not add it to unrelated commands such as `gh pr view`.

### Completion Callbacks

`--on-complete` runs a command after *each* scheduled invocation completes. It is not a
session-wakeup feature by itself. A callback may notify a harness only when it targets that
harness’s configured ingress and a delivery has been proven; otherwise its output is just
another scheduled-process result.

## Harness Routes

- For an active Codex wait or PR loop, read [[codex/SKILL|codex]].
- For an active Claude Code wait or PR loop, read [[claude-code/SKILL|claude-code]].
- Do not infer a generic delivery path from another harness, a session ID, scheduler logs,
  or the existence of a timer.

## Reference

- `uvx --from git+https://github.com/dzackgarza/task-sched task-sched add --help`
- `uvx --from git+https://github.com/dzackgarza/task-sched task-sched list`
- `uvx --from git+https://github.com/dzackgarza/task-sched task-sched log <task-id>`
- `man at`
