---
name: ntfy
description: Use when sending, receiving, and automating ntfy notifications via HTTP or ntfy CLI, including auth, scheduling, attachments, actions, and stream or poll subscriptions
---

# ntfy

Operational skill for using ntfy from scripts, cron jobs, CI, and CLI workflows.
Source of truth: `https://docs.ntfy.sh/`.

## Scope

This skill is for normal ntfy usage:
- publish notifications (HTTP and CLI)
- subscribe/consume notifications (streaming and polling)
- authenticate to protected topics
- use advanced delivery features (actions, scheduling, attachments)

Do not default to incident forensics. Only do troubleshooting analysis when explicitly requested.

## Load Order

1. `references/publish.md` for sending notifications.
2. `references/subscribe.md` for reading notifications.

## Quick Start

### Publish a basic message

```bash
curl -sS -d "Backup completed" https://ntfy.sh/<topic>
```

### Publish with title, priority, and tags

```bash
curl -sS \
  -H "Title: Backup status" \
  -H "Priority: high" \
  -H "Tags: white_check_mark,backup" \
  -d "Nightly backup completed" \
  https://ntfy.sh/<topic>
```

### Stream messages as JSON

```bash
curl -sS -N https://ntfy.sh/<topic>/json
```

### Poll recent messages and exit

```bash
curl -sS "https://ntfy.sh/<topic>/json?poll=1&since=1h"
```

## Project Defaults (`lattice_interface`)

- Topic: `dzg-lattice-doc-updates`
- Query helper: `just ntfy-last-hour`

Equivalent API query:

```bash
curl -sS "https://ntfy.sh/dzg-lattice-doc-updates/json?poll=1&since=1h"
```

## Automation Rules

- Always capture HTTP status and response body when publishing from automation.
- Treat non-2xx responses as hard failures.
- Keep topic names explicit and consistent; topic mismatch is the most common operator error.
- Do not include secrets in message text, title, tags, click URLs, or action payloads.
