---
name: ssh-workstation-and-tmux
description: "Use when working with remote SSH workstations and managing long-running jobs via named tmux sessions."
---
# SSH Workstation & Named Tmux Sessions

Pattern for long-running remote work: SSH into a workstation, use named tmux sessions to
keep jobs alive across disconnects.

## Connection

```
ssh dzack@ssh-work.dzackgarza.com
```

The connection goes through a Cloudflare Tunnel (handled by `~/.ssh/config` —
`ProxyCommand cloudflared access ssh`), but that's irrelevant to *using* it.
Just `ssh` and it works.

## Pattern: Named Tmux Sessions

Start a long job in a named tmux session so it survives disconnects and can be checked
later.

```
# Start
tmux new-session -d -s <session-name>
tmux send-keys -t <session-name> '<long-running-command>' Enter

# Monitor
tmux capture-pane -pt <session-name>

# Re-attach
tmux attach -t <session-name>
```

The project standardizes on session name `pdf-extraction`, but the pattern is general —
pick a descriptive name per task.

## Key Remote Paths

- `~/pdf-inputs/` — incoming work queue (PDFs to process)
- `~/pdf-outputs/` — completed extraction artifacts
- `~/pdf-extraction/` — project checkout with MinerU venv at `~/.venv/bin/mineru`

## Machine Specs

4-core CPU, 32 GB RAM, Arch Linux.
No GPU. Throughput ~3-4 pages/min for MinerU.

## Cron heartbeat pattern

Long-running autonomous OpenCode sessions on the workstation are kept alive by a local
Hermes cron job that pings them every 15 minutes (`no_agent=True`, just a `uvx`
command). The ping tells the agent to continue work, re-read plans, and keep processing.
This replaces the old system-crontab approach.
