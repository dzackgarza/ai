# Subscribing (API + CLI)

Canonical docs:
- `https://docs.ntfy.sh/subscribe/api/`
- `https://docs.ntfy.sh/subscribe/cli/`

## API Endpoint Shapes

For topic `<topic>`:

- `GET /<topic>/json`: newline-delimited JSON stream.
- `GET /<topic>/sse`: server-sent events (great for browser/EventSource).
- `GET /<topic>/raw`: one line per message body.
- `GET /<topic>/ws`: WebSocket JSON stream.

## Minimum Working Calls

```bash
# JSON stream (long-lived)
curl -sS -N https://ntfy.sh/<topic>/json

# SSE stream
curl -sS -N https://ntfy.sh/<topic>/sse

# Raw stream
curl -sS -N https://ntfy.sh/<topic>/raw

# Poll and exit
curl -sS "https://ntfy.sh/<topic>/json?poll=1"
```

## Polling, Replay, and Filters

### Replay and poll

- `poll=1`: return available cached messages then close.
- `since=<value>`: replay from duration, Unix timestamp, message ID, `all`, or `latest`.
- `scheduled=1` (alias `sched=1`): include scheduled/delayed messages.

Examples:

```bash
curl -sS "https://ntfy.sh/mytopic/json?poll=1&since=10m"
curl -sS "https://ntfy.sh/mytopic/json?poll=1&since=latest"
curl -sS "https://ntfy.sh/mytopic/json?poll=1&sched=1"
```

### Filters

Available filters (case-insensitive):
- `id`
- `message`
- `title`
- `priority` (OR across listed priorities)
- `tags` (AND across listed tags)

Examples:

```bash
curl -sS "https://ntfy.sh/alerts/json?poll=1&priority=high,urgent"
curl -sS "https://ntfy.sh/alerts/json?poll=1&tags=error,zfs"
```

### Multi-topic subscribe

```bash
curl -sS -N https://ntfy.sh/topicA,topicB/json
```

## Subscription Parameters

| Parameter | Aliases | Meaning |
|---|---|---|
| `poll` | `X-Poll`, `po` | Return cached messages and close |
| `since` | `X-Since`, `si` | Replay from duration/timestamp/message ID |
| `scheduled` | `X-Scheduled`, `sched` | Include scheduled messages |
| `id` | `X-ID` | Exact message ID filter |
| `message` | `X-Message`, `m` | Exact message text filter |
| `title` | `X-Title`, `t` | Exact title filter |
| `priority` | `X-Priority`, `prio`, `p` | Priority filter |
| `tags` | `X-Tags`, `tag`, `ta` | Tag filter |

## Message JSON Model

The JSON/SSE payload includes these important fields:

- `id` (message identifier)
- `time` (Unix timestamp)
- `event` (`open`, `keepalive`, `message`, `message_delete`, `message_clear`, `poll_request`)
- `topic`
- Optional for `message` events: `message`, `title`, `tags`, `priority`, `click`, `actions`, `attachment`, `sequence_id`, `expires`

Typical consumer rule:
- Handle only `event == "message"` for business logic.
- Ignore or separately handle `open`/`keepalive`/`poll_request`.

## Authentication for Subscribe

Protected topics require auth, same as publishing:

```bash
curl -sS -u user:pass https://ntfy.sh/private/json
curl -sS -H "Authorization: Bearer tk_xxx" https://ntfy.sh/private/json
```

`auth` query parameter is also supported (base64-encoded authorization header value).

## ntfy CLI Subscription

## Stream JSON

```bash
ntfy subscribe <topic>
# alias: ntfy sub <topic>
```

## Run a command per message

```bash
ntfy sub <topic> 'notify-send "$m"'
ntfy sub <topic> '/path/to/script.sh'
```

Message fields are exposed as env vars:

- `NTFY_ID` (`$id`)
- `NTFY_TIME` (`$time`)
- `NTFY_TOPIC` (`$topic`)
- `NTFY_MESSAGE` (`$message`, `$m`)
- `NTFY_TITLE` (`$title`, `$t`)
- `NTFY_PRIORITY` (`$priority`, `$prio`, `$p`)
- `NTFY_TAGS` (`$tags`, `$tag`, `$ta`)
- `NTFY_RAW` (`$raw`)

## Subscribe to multiple topics from config

```bash
ntfy subscribe --from-config
```

Config location examples:
- Linux user: `~/.config/ntfy/client.yml`
- macOS user: `~/Library/Application Support/ntfy/client.yml`

Core config pattern:

```yaml
default-host: https://ntfy.sh
subscribe:
  - topic: alerts
    command: 'notify-send "Important" "$m"'
    if:
      priority: high,urgent
```

## Related Docs

- `https://docs.ntfy.sh/subscribe/api/`
- `https://docs.ntfy.sh/subscribe/cli/`
- `https://docs.ntfy.sh/subscribe/web/`
- `https://docs.ntfy.sh/subscribe/phone/`
