# Hermes Cron — Process-Bound Persistence Model

Cron jobs are persisted in SQLite (survive restarts), but the scheduler only ticks while
a Hermes process is alive.
This is the single most common misconception about Hermes cron, because “cron” implies a
system-level service.

## Three runtime scenarios

| Setup | Scheduler lives? |
| --- | --- |
| Interactive `hermes` (CLI) | Only while the session is open. Dies on `/quit`. |
| `hermes gateway run` (foreground) | Yes, while that terminal is open. |
| `hermes gateway install` (systemd) | Yes, 24/7 background daemon. |

There is no standalone scheduler daemon.
If the user expects cron to keep running after they close the terminal, they need
`hermes gateway install && hermes gateway start`.

## Example: user pushback

User: “If I close the app, none of those scheduled tasks run?”
Agent: “Correct. The scheduler lives in the Hermes process.
Gateway mode (`hermes gateway install` → systemd) keeps it alive as a background
service. CLI-only mode has no persistence.”

## Script-only (no_agent=True) mode

Good for zero-LLM-cost watchdogs.
The script lives in `~/.hermes/scripts/<name>.py` (or `.sh`). When creating:

- Set `no_agent=true` so the script runs directly

- The script’s stdout is delivered to the user (verbatim, wrapped in cron framing
  headers)

- The script can write side-effect files (like appending to a report) — that’s its main
  job

- `workdir` sets CWD before the script runs; useful for git-aware or project-scoped
  scripts

## Agent-driven vs Script-only (no_agent) cron jobs

A cron job can run in two modes, chosen by the `no_agent` field:

| Mode | no_agent | What runs | Best for |
| --- | --- | --- | --- |
| **Script-only** | `true` | A Python/bash script in `~/.hermes/scripts/` | Watchdogs, mechanical checks, zero-LLM-cost tasks. Script output is delivered verbatim. |
| **Agent-driven** | `false` (default) | A full agent session with the given `prompt` | Tasks requiring reasoning, reading, analysis, judgment. The agent loads context, reads files, and writes a report. |

**Crucial distinction:** Script-only is for *mechanical* tasks (check if a file exists,
count lines, run a command).
Agent-driven is for *tasks that need intelligence* (read plans, understand what
happened, write an insightful report).
Do NOT reach for script-only when the user wants analysis — they will call it out.

### Writing effective agent-driven cron prompts

A good prompt for a recurring status-check cron job:

1. **Direct the agent to READ actual content** — planning docs, git log, output files,
   error sidecars. Not “count the files” but “read what’s happening.”

2. **Specify what constitutes insight** — “what’s being extracted right now,” "what
   kinds of errors are appearing," “are there any anomalies.”
   Not “report the counts of X, Y, Z.”

3. **Ask for specific, named items** — “which book is currently extracting,” "what error
   patterns emerged in recent reviews," “which books finished since last report.”
   Names, not numbers.

4. **Push the agent to think** — “are there any problems or blockers?
   what should happen next?”
   Force reasoning, not templating.

5. **Domain-aware framing** — indicate what the “semantically meaningful work” is in
   this project. For a PDF extraction project, the meaningful work is *mathematical OCR
   quality* and *specific book progress*, not file counts.

### Anti-patterns (from real user pushback)

**Anti-pattern 1: Static file-counter for an analysis task.** A Python script that
counts `.md` files and runs `git status` and formats them as a report is not a status
check — it’s a dashboard.
The user will say “this was a task that needed intelligence” and you will have to delete
it and start over.

**Anti-pattern 2: Shallow analysis prompt.** Listing “what the agent should check” as
bullet points of things to count or run (`git status`, `ls`, count files, read queue
depth) produces a report with the same numbers the static script would have produced,
just wrapped in prose.
The user will say “you wildly misinterpreted what constitutes a good report — file/line
counts are not meaningful.”

**Anti-pattern 3: no_agent=True for reasoning tasks.** If the task involves
understanding what’s happening, assessing quality, or writing narrative analysis, never
use no_agent=True. The script has no LLM and cannot reason.
Reserve script-only for genuinely mechanical checks (is the server up, is disk full, has
a file been modified).

### What a good status report looks like

A status report on a complex project should answer the questions a domain-aware
colleague would ask:

- “What extraction work happened since yesterday?”
  (specific book names, whether it finished or failed)

- “What review/correction work was done?”
  (which books, what stage)

- “What error patterns are emerging?”
  (e.g., “binomial-for-fraction across many sections in Apostol — MinerU can’t handle
  displayed fractions”)

- “Any problems?” (SSH dropped, OOM, stalled extraction, mismatch between extracted and
  reviewed)

- “What should happen next?”
  (this book is ready for review, queue needs replenishment)

## Heartbeat/Pacer pattern (pinging a persistent autonomous agent)

A common pattern: a long-running autonomous agent session manages complex work
(extraction pipeline, research, etc.), and a cron job exists solely to **poke it
periodically** with a reminder to keep working.
The cron is not the worker — it’s a pacemaker.

**Architecture:**

- There is a persistent agent session (OpenCode, Hermes, or other) that runs
  autonomously using `sleep` to continue working over hours/days

- A cron job fires every N minutes and sends a heartbeat message: “continue your work,
  update your worklog, keep going”

- The cron job does NOT do the work itself — it just prods the existing session

**When this makes sense:**

- The autonomous session has accumulated context over many turns (knowledge of what’s
  been done, what’s next, SSH state, etc.)

- The work involves long-running operations (SSH extraction) where each cron run would
  be too short to make progress

- The cron provides a safety net: if the agent stalls (API error, sleep expired without
  resuming), the next heartbeat will nudge it

**Implementing in Hermes cron:**

Option A — Prompt-based (simplest, no extra files):
```
schedule="*/5 * * * *"
prompt="Run: /path/to/cron-opencode-chat <session_id> 'continue working...'"
```
The agent does one LLM call per tick — reports success or flags failure.

Option B — Script-based with general-purpose helper (zero LLM overhead):
```
schedule="*/5 * * * *"
no_agent=true
script="<general-purpose-helper>.sh"
```
The helper takes a session ID and prompt as arguments.
This avoids coupling the cron job to a specific hardcoded script.

**Anti-pattern: dedicated hardcoded script.** Creating a one-off `.sh` file that
hardcodes the session ID and prompt is overfit coupling.
If the session ID or prompt changes, you have to edit a file that the user may not know
about. The command should either live in the cron job definition itself (prompt-based),
or use a general-purpose helper that takes arguments (script-based).

**Anti-pattern: wrapper chain.** If you DO write a script, make it the actual command —
not a wrapper around a wrapper.
Example of wrong: `pdf-heartbeat.sh` calls `cron-opencode-chat` (itself a helper script)
which sources envrc and runs `uvx`. The right approach: the script IS the uvx command
directly, with env sourcing inline.
Each layer of indirection is a point of coupling and confusion.

```
# BAD — wrapper around a wrapper
#!/bin/bash
source .envrc
exec cron-opencode-chat $SESSION "$PROMPT"

# GOOD — the actual command
#!/bin/bash
source ~/.envrc
exec timeout 30 uvx git+https://github.com/...git chat <session> "<prompt>"
```

If the user objects to scripting entirely, the prompt-based approach (Option A above)
avoids file coupling at the cost of a small LLM call per tick.
Accept the tradeoff — don’t force a script file where the user doesn’t want one.

**Migration from system crontab:** System cron entries often require wrapper scripts
because crontab has poor variable-expansion and quoting.
Hermes cron does not have these limitations — commands can be inlined directly in the
prompt field or passed as arguments to a general-purpose helper.
When migrating a system crontab entry to Hermes cron, prefer inlining over recreating
the wrapper.

## Observability / run history

- `cronjob(action='list')` shows `last_run_at`, `last_status`
  (success/failed/interrupted), `last_delivery_error` for each job.

- `hermes cron status` shows scheduler daemon status and PID.

- Agent-driven cron runs create sessions in the session store.
  Find them via `hermes sessions list` or `session_search`.

- Gateway and scheduler logs live in `~/.hermes/logs/agent.log` and
  `~/.hermes/logs/gateway.log`.

- There is no dedicated “cron run history viewer” — session search and log grep are the
  tools.

## Delivery behavior

- Omit `deliver` to auto-detect current chat (origin).
  For no_agent scripts, this means the script’s stdout is delivered to the chat that
  created the cron job.
  For agent-driven jobs, the agent’s output is delivered.

- `deliver='local'` means no delivery at all — the job runs silently, output is only in
  logs.

- **Heartbeat/pacer jobs should use `deliver='local'`.** These jobs exist only to prod
  an autonomous session — the user doesn’t need to see “heartbeat sent” every 5 minutes.
  If the heartbeat fails, the `last_status` field on the job will show it.
  Only deliver output if the job produces information the user should read (status
  reports, alerts, etc.).
