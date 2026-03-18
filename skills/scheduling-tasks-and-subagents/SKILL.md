---
name: scheduling-tasks-and-subagents
description: Use when scheduling recurring tasks, one-off delayed commands, or waking agent sessions after a delay.
---

# Scheduling Tasks and Subagents

Schedule work to run later — either once (`at`) or on a repeating schedule (`task-sched`). Use this to wake yourself up after delays, poll external processes, or run periodic maintenance.

## Decision: Which Tool?

| Need                          | Tool         | Reason                                           |
| ----------------------------- | ------------ | ------------------------------------------------ |
| Run once, at a specific time  | `at`         | Simple, no persistence needed                    |
| Run repeatedly, forever       | `task-sched` | Creates systemd timer units that survive reboots |
| Chain: run B after A finishes | `task-sched` | `--on-complete` callback                         |
| "Wake me in 10 minutes"       | `at`         | One-shot self-wakeup                             |
| Poll external process hourly  | `task-sched` | Recurring check without manual setup             |

## Agent Session Wakeup Pattern

Agents stop after responding. To continue multi-step work:

```bash
# Schedule a message to yourself via 'at'
echo "opx chat --session ses_XXX --prompt 'continue task'" | at now + 10 minutes
```

Get your session ID from the introspection tool.

## Recurring Tasks (task-sched)

`task-sched` wraps systemd. Tasks get IDs like `tsk_a1b2c3d4`.

### Typical Flow

1. **Add** with command and schedule (preset like `hourly` or 5-field cron)
2. **List** to confirm and get the task ID
3. **Log** if it fails unexpectedly
4. **Remove** when no longer needed

### Test Commands Before Scheduling

Scheduled tasks run in a minimal environment. Always test first:

```bash
# Test your command in a clean shell before scheduling
env -i HOME=$HOME PATH=$PATH bash -c "your-command-here"
```

**Common failures:**

- **Missing `.envrc`**: If you set `--working-dir` to something other than your project root (e.g., `/tmp`), direnv won't source `.envrc` — and you won't have paths to tools like `npm` (via nvm) or `python` (via pyenv)
- **Missing shell init files**: `.bashrc`, `.zshrc` are not loaded in the minimal execution environment

**Fix with direnv:**

Always ensure your command runs in a context where `.envrc` is loaded. Options:

```bash
# Option 1: Set working-dir to a directory with .envrc
uvx git+https://github.com/dzackgarza/task-sched add \
  --command "npm run build" \
  --working-dir /home/dzack/my-project  # Contains .envrc with PATH setup

# Option 2: Explicitly eval direnv before the command
uvx git+https://github.com/dzackgarza/task-sched add \
  --command 'eval "$(direnv export bash)" && npm run build' \
  --working-dir /home/dzack/my-project

# Option 3: Use 'direnv exec' to run in a specific directory's env
uvx git+https://github.com/dzackgarza/task-sched add \
  --command 'direnv exec /home/dzack/my-project npm run build'
```

**Never manually construct paths to nvm/pyenv binaries** — this breaks when versions change.

### Anti-Stall Heartbeat (Periodic Self-Wakeup)

Agents can get stuck waiting indefinitely for user input or external events. Schedule a periodic heartbeat to guarantee regular wakeups:

```bash
# Wake yourself every 30 minutes to check for progress
task_id=$(uvx git+https://github.com/dzackgarza/task-sched add \
  --command "opx chat --session ses_XXX --prompt 'heartbeat: check if work is blocked and continue'" \
  --schedule "*/30 * * * *" \
  --description "Agent heartbeat for session ses_XXX")

# Store task_id somewhere to remove it later
```

**Pattern**: The heartbeat prompt should check:

- Are you waiting for something that already arrived?
- Is an external process you launched actually done?
- Has a long-running operation silently completed?

Remove when the session's work is truly complete.

### Polling External Processes

Wake yourself periodically to check if something finished:

```bash
uvx git+https://github.com/dzackgarza/task-sched add \
  --command "opx chat --session ses_XXX --prompt 'check if build finished'" \
  --schedule "*/15 * * * *"
```

**Critical**: Remove polling tasks when the work completes to avoid orphaned wakeups.

### Chaining with Completion Callbacks

Run a follow-up action after the main task finishes:

```bash
uvx git+https://github.com/dzackgarza/task-sched add \
  --command "cd /project && uv run pytest" \
  --schedule "daily" \
  --on-complete "opx chat --session ses_XXX --prompt 'test run finished'"
```

## Common Pitfalls

- **Orphaned wakeups**: Always remove polling tasks when the tracked work completes
- **Working directory**: Complex commands may need `--working-dir` or a wrapper script
- **Logs**: Check `task-sched log tsk_XXX` before assuming silent failure

## Reference

Full CLI syntax available via `--help`. Key commands:

- `uvx git+https://github.com/dzackgarza/task-sched add --help`
- `uvx git+https://github.com/dzackgarza/task-sched list`
- `uvx git+https://github.com/dzackgarza/task-sched log tsk_XXX`
- `man at`
