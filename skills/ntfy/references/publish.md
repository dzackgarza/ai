# Publishing (HTTP + CLI)

Canonical docs: `https://docs.ntfy.sh/publish/`

## Core Endpoints

- `POST|PUT /<topic>`: publish a message.
- `POST|PUT /<topic>/<sequence_id>`: publish/update an existing notification sequence.
- `POST /` with JSON body: publish as JSON (`topic` field required).
- `GET /<topic>/publish` (aliases: `/send`, `/trigger`): webhook-style publishing.
- `PUT /<topic>/<sequence_id>/clear` (alias: `/read`): clear notification.
- `DELETE /<topic>/<sequence_id>`: delete notification.

## Minimum Working Calls

### HTTP

```bash
curl -sS -d "Backup successful" https://ntfy.sh/mytopic
curl -sS -T ./report.txt -H "Filename: report.txt" https://ntfy.sh/mytopic
curl -sS https://ntfy.sh/mytopic/trigger
```

### ntfy CLI

```bash
ntfy publish mytopic "Backup successful"
ntfy pub --file ./report.txt mytopic
ntfy trigger mytopic
```

## Publish Parameters (Headers / Query Params)

Headers are case-insensitive. Query parameters must be lowercase.

| Canonical | Common aliases | Purpose |
|---|---|---|
| `X-Message` | `Message`, `m` | Message body |
| `X-Title` | `Title`, `t` | Notification title |
| `X-Sequence-ID` | `Sequence-ID`, `SID` | Sequence for update/clear/delete |
| `X-Priority` | `Priority`, `prio`, `p` | Priority (1-5 or name) |
| `X-Tags` | `Tags`, `Tag`, `ta` | Comma-separated tags/emojis |
| `X-Delay` | `Delay`, `At`, `In` variants | Scheduled delivery time |
| `X-Actions` | `Actions`, `Action` | Action buttons |
| `X-Click` | `Click` | URL/app URI on click |
| `X-Attach` | `Attach`, `a` | External attachment URL |
| `X-Markdown` | `Markdown`, `md` | Enable markdown rendering |
| `X-Icon` | `Icon` | External icon URL |
| `X-Filename` | `Filename`, `file`, `f` | Attachment filename override |
| `X-Email` | `Email`, `mail`, etc. | Forward notification via email |
| `X-Call` | `Call` | Trigger phone call (where supported) |
| `X-Cache` | `Cache` | `no` disables server caching for this message |
| `X-Firebase` | `Firebase` | `no` disables Firebase forwarding |
| `X-UnifiedPush` | `UnifiedPush`, `up` | UnifiedPush behavior |
| `Authorization` | n/a | Basic/Bearer auth |
| `Content-Type` | n/a | `text/markdown` enables markdown |

## Priority Mapping

- `5` / `max` / `urgent`
- `4` / `high`
- `3` / `default`
- `2` / `low`
- `1` / `min`

Example:

```bash
curl -sS -H "Priority: high" -d "Disk space low" https://ntfy.sh/alerts
```

## Common Features

### Title, tags, markdown, click URL, icon

```bash
curl -sS \
  -H "Title: Build failed" \
  -H "Tags: warning,build" \
  -H "Markdown: yes" \
  -H "Click: https://ci.example.com/runs/123" \
  -H "Icon: https://example.com/icons/ci.png" \
  -d "**main** failed at test stage" \
  https://ntfy.sh/ci-alerts
```

### Attachments

- Local file upload: `PUT` body + `Filename` header.
- External URL: `Attach: https://...`.

```bash
curl -sS -T ./incident.png -H "Filename: incident.png" https://ntfy.sh/alerts
curl -sS -H "Attach: https://example.com/incident.png" https://ntfy.sh/alerts
```

### Action buttons

- Up to 3 actions.
- Action types: `view`, `broadcast` (Android), `http`, `copy`.

Header format:

```text
action=<type>, label=<label>, ... ; action=<type>, label=<label>, ...
```

Short format examples:

- `view, Open dashboard, https://status.example.com, clear=true`
- `http, Retry, https://api.example.com/retry, method=POST, clear=true`
- `copy, Copy ID, 12345, clear=true`

### Scheduled delivery

Use `Delay`/`At`/`In` aliases with:
- Unix timestamp
- duration (`30m`, `2h`, `1 day`)
- natural language (`10am`, `tomorrow`, `Tuesday`)

Docs state current limits are typically:
- minimum delay: 10 seconds
- maximum delay: 3 days

```bash
curl -sS -H "In: 30m" -d "Reminder" https://ntfy.sh/reminders
curl -sS -H "At: tomorrow, 10am" -d "Daily check" https://ntfy.sh/reminders
```

#### Update/cancel scheduled messages

- Re-publish same sequence to replace scheduled message.
- Cancel by deleting sequence:

```bash
curl -sS -X DELETE https://ntfy.sh/mytopic/reminder-seq
```

## Publish as JSON

POST to root URL, not topic URL.

```bash
curl -sS https://ntfy.sh \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "mytopic",
    "message": "Disk space low",
    "title": "Low disk",
    "tags": ["warning","disk"],
    "priority": 4,
    "click": "https://status.example.com",
    "actions": [{"action":"view","label":"Open","url":"https://status.example.com"}]
  }'
```

Key JSON fields:
- Required: `topic`
- Common: `message`, `title`, `tags`, `priority`, `actions`, `click`
- Also supported: `attach`, `filename`, `markdown`, `icon`, `delay`, `email`, `call`, `sequence_id`

## Update, Clear, Delete Existing Notifications

### Update

- Use same sequence ID either in URL path or `X-Sequence-ID`.

```bash
curl -sS -d "Download started" https://ntfy.sh/files/job-123
curl -sS -d "Download 50%" https://ntfy.sh/files/job-123
curl -sS -H "X-Sequence-ID: job-123" -d "Download complete" https://ntfy.sh/files
```

### Clear (mark as read/dismiss)

```bash
curl -sS -X PUT https://ntfy.sh/files/job-123/clear
```

### Delete

```bash
curl -sS -X DELETE https://ntfy.sh/files/job-123
```

## Authentication Modes

### Basic auth with user/password

```bash
curl -sS -u user:pass -d "Secret message" https://ntfy.sh/private-topic
```

### Bearer token

```bash
curl -sS -H "Authorization: Bearer tk_xxx" -d "Secret message" https://ntfy.sh/private-topic
```

### Basic with empty user + token as password

```bash
curl -sS -u :tk_xxx -d "Secret message" https://ntfy.sh/private-topic
```

### `auth` query parameter

Use raw base64 of the full `Authorization` header value (without trailing `=`).

## Service Limits You Must Account For

From docs (defaults plus ntfy.sh notes):

- Message length: 4096 bytes (larger content treated as attachment).
- Request burst: 60 per visitor, refilling at 1 request / 5s.
- Daily messages: on `ntfy.sh`, 250/day (default behavior can be request-limit derived).
- Email: burst 16 then 1/hour; on `ntfy.sh`, daily email limit is 5.
- Subscriptions: 30 concurrent per visitor by default.
- Attachments (default server): 15 MB/file, 100 MB/visitor, 5 GB total cache.
- Attachments (`ntfy.sh`): 2 MB/file, 20 MB/visitor total.
- Attachment bandwidth: default 500 MB/day per visitor; `ntfy.sh` 200 MB/day.

Design automation to surface non-2xx status immediately (especially `429`).

## Related Docs

- `https://docs.ntfy.sh/publish/`
- `https://docs.ntfy.sh/publish/template-functions/`
- `https://docs.ntfy.sh/emojis/`
