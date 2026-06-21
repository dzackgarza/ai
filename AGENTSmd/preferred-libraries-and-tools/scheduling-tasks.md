---
order: 20
title: Scheduling Tasks
---

Use `task-sched` to schedule persistent systemd tasks.
For help, run `uvx git+https://github.com/dzackgarza/task-sched --help`.

```bash
# Add a recurring task
uvx git+https://github.com/dzackgarza/task-sched add --command "echo 'heartbeat'" --schedule "hourly"

# List scheduled tasks
uvx git+https://github.com/dzackgarza/task-sched list
```

For one-off tasks, use `at`:

```bash
echo "opx chat --session ses_xxx --prompt 'continue work'" | at now + 30 minutes
```
