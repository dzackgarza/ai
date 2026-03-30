---
name: ntfy
description: "Use when sending, receiving, or automating ntfy notifications via HTTP or CLI."
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
echo "Backup completed" | uvx --from httpie http POST https://ntfy.sh/<topic>
```

### Publish with title, priority, and tags

```bash
echo "Nightly backup completed" | uvx --from httpie http POST https://ntfy.sh/<topic> \
  "Title:Backup status" \
  "Priority:high" \
  "Tags:white_check_mark,backup"
```

### Stream messages as JSON

```bash
uvx --from httpie http --stream GET https://ntfy.sh/<topic>/json
```

### Poll recent messages and exit

```bash
uvx --from httpie http GET "https://ntfy.sh/<topic>/json?poll=1&since=1h"
```

## Project Defaults (`lattice_interface`)

- Topic: `dzg-lattice-doc-updates`
- Query helper: `just ntfy-last-hour`

Equivalent API query:

```bash
uvx --from httpie http GET "https://ntfy.sh/dzg-lattice-doc-updates/json?poll=1&since=1h"
```

## Automation Rules

- Always capture HTTP status and response body when publishing from automation.
- Treat non-2xx responses as hard failures.
- Keep topic names explicit and consistent; topic mismatch is the most common operator error.
- Do not include secrets in message text, title, tags, click URLs, or action payloads.
