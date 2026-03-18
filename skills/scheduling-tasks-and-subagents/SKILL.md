---
name: scheduling-tasks-and-subagents
description: Use when asked to schedule recurring tasks, set up one-off delayed commands, or wake agent sessions on a timer.
---

# Scheduling Tasks and Subagents

Schedule persistent recurring tasks via systemd, run one-off delayed commands, and set up agent session wakeup patterns.

## task-sched (Recurring Tasks)

`task-sched` manages persistent systemd timer units. All tasks survive reboots.

### Invocation

```bash
uvx git+https://github.com/dzackgarza/task-sched <command> [options]
```

### Add a Task

```bash
uvx git+https://github.com/dzackgarza/task-sched add \
  --command "echo 'heartbeat'" \
  --schedule "hourly"
```

**Flags:**

| Flag            | Short | Description                          |
| --------------- | ----- | ------------------------------------ |
| `--command`     | `-c`  | Shell command to execute (required)  |
| `--schedule`    | `-s`  | Cron expression or preset (required) |
| `--working-dir` | `-d`  | Working directory                    |
| `--description` |       | Human-readable description           |
| `--on-complete` |       | Callback command on completion       |

**Schedule presets:**

| Preset     | Cron        |
| ---------- | ----------- |
| `minutely` | `* * * * *` |
| `hourly`   | `0 * * * *` |
| `daily`    | `0 0 * * *` |
| `weekly`   | `0 0 * * 0` |

Arbitrary 5-field cron expressions are also accepted.

### List Tasks

```bash
uvx git+https://github.com/dzackgarza/task-sched list
uvx git+https://github.com/dzackgarza/task-sched list --json
```

### Edit a Task

```bash
uvx git+https://github.com/dzackgarza/task-sched edit tsk_abc123 --schedule "daily"
uvx git+https://github.com/dzackgarza/task-sched edit tsk_abc123 --command "new-command"
```

### Run a Task Immediately

```bash
uvx git+https://github.com/dzackgarza/task-sched run tsk_abc123
```

### View Task Logs

```bash
uvx git+https://github.com/dzackgarza/task-sched log tsk_abc123
uvx git+https://github.com/dzackgarza/task-sched log tsk_abc123 --lines 50
```

### Remove a Task

```bash
uvx git+https://github.com/dzackgarza/task-sched remove tsk_abc123
uvx git+https://github.com/dzackgarza/task-sched remove tsk_abc123 --force
```

### Task IDs

All task IDs follow the format `tsk_<8 hex chars>` (e.g., `tsk_a1b2c3d4`). IDs are auto-generated on creation.

## at (One-Off Tasks)

For single-run delayed commands, use `at`:

```bash
# Run a command in 30 minutes
echo "echo 'done'" | at now + 30 minutes

# Run at a specific time
echo "echo 'backup'" | at 2pm tomorrow
```

## Agent Session Wakeup

After responding to a user, agent actions halt until the next prompt. To resume work on multi-step tasks, schedule a wakeup:

```bash
# Wake your own session in 1 minute
echo "npx --yes --package=git+https://github.com/dzackgarza/opencode-manager.git opx chat --session ses_XXXXXXXX --prompt 'continue the task'" | at now + 1 minute
```

Replace `ses_XXXXXXXX` with your actual session ID (from the introspection tool).

### Waking via Recurring Task

For longer polling cycles, use `task-sched`:

```bash
uvx git+https://github.com/dzackgarza/task-sched add \
  --command "npx --yes --package=git+https://github.com/dzackgarza/opencode-manager.git opx chat --session ses_XXX --prompt 'check status and continue'" \
  --schedule "hourly"
```

Remove the task when done:

```bash
uvx git+https://github.com/dzackgarza/task-sched remove tsk_XXXXXX
```

## Patterns

### Poll External Process

Schedule a check that wakes the agent to verify progress:

```bash
uvx git+https://github.com/dzackgarza/task-sched add \
  --command "opx chat --session ses_XXX --prompt 'check if build finished'" \
  --schedule "*/5 * * * *"
```

### Periodic Maintenance

```bash
uvx git+https://github.com/dzackgarza/task-sched add \
  --command "cd /path/to/repo && git fetch --prune" \
  --schedule "hourly" \
  --description "Prune stale remote branches"
```

### Callback on Completion

Use `--on-complete` to chain tasks:

```bash
uvx git+https://github.com/dzackgarza/task-sched add \
  --command "cd /project && uv run pytest" \
  --schedule "daily" \
  --on-complete "echo 'tests ran' >> /var/log/test-results.log"
```
