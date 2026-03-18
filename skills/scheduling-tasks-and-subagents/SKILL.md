---
name: scheduling-tasks-and-subagents
description: Use when asked to schedule recurring tasks, set up one-off delayed commands, or wake agent sessions on a timer.
---

# Scheduling Tasks and Subagents

Schedule persistent recurring tasks via systemd, run one-off delayed commands, and set up agent session wakeup patterns.

## When to Use

**Use `task-sched`** (persistent, survives reboots):

- Recurring work (hourly, daily, weekly)
- Polling external processes
- Periodic maintenance scripts
- Chaining tasks with completion callbacks

**Use `at`** (one-off, runs once):

- Delayed execution ("in 30 minutes")
- Wake agent session after a wait
- Single scheduled maintenance

## Task-Sched Workflow

`task-sched` creates systemd timer units. Tasks are identified as `tsk_<8hex>`.

### 1. Define the Command

The command runs in a minimal shell. For complex logic, wrap in a script:

```bash
uvx git+https://github.com/dzackgarza/task-sched add \
  --command "cd /repo && ./scripts/backup.sh" \
  --schedule "daily"
```

### 2. Choose Schedule

**Presets**: `minutely`, `hourly`, `daily`, `weekly` — or any valid 5-field cron.

### 3. Optional Fields

- `--working-dir`: Set working directory
- `--description`: Human-readable label
- `--on-complete`: Callback after the task finishes

### 4. Manage

```bash
# List and identify your task ID
uvx git+https://github.com/dzackgarza/task-sched list

# Check logs if something fails
uvx git+https://github.com/dzackgarza/task-sched log tsk_abc123

# Run immediately (for testing)
uvx git+https://github.com/dzackgarza/task-sched run tsk_abc123

# Remove when done
uvx git+https://github.com/dzackgarza/task-sched remove tsk_abc123
```

## Agent Session Wakeup

Agents halt after responding until a new prompt arrives. To continue multi-step work, schedule a wakeup:

### Quick Wakeup (at)

```bash
echo "opx chat --session ses_XXX --prompt 'continue'" | at now + 10 minutes
```

### Polling Wakeup (task-sched)

For long-running external processes:

```bash
uvx git+https://github.com/dzackgarza/task-sched add \
  --command "opx chat --session ses_XXX --prompt 'check status and continue'" \
  --schedule "*/15 * * * *"
```

**Important**: Remove polling tasks when the work completes to avoid orphaned wakeups.

## Patterns

### Poll External Process

Wake agent to check if a build/deployment finished:

```bash
uvx git+https://github.com/dzackgarza/task-sched add \
  --command "opx chat --session ses_XXX --prompt 'check if build finished'" \
  --schedule "*/5 * * * *"
```

### Chain Tasks

Run a follow-up after the main task completes:

```bash
uvx git+https://github.com/dzackgarza/task-sched add \
  --command "cd /project && uv run pytest" \
  --schedule "daily" \
  --on-complete "opx chat --session ses_XXX --prompt 'tests finished'"
```

## Reference

For full command syntax, run:

```bash
uvx git+https://github.com/dzackgarza/task-sched --help
uvx git+https://github.com/dzackgarza/task-sched add --help
man at
```
