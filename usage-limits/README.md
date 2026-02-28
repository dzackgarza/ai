# Usage Limits Checkers

Three harnesses, unified interface. All auto-detect auth, all support JSON output.

## Claude Code

```bash
python claude_usage.py           # Rich summary (auto-anchor + auto-notify)
python claude_usage.py --json    # JSON output
python claude_usage.py --no-notify   # Disable auto-notification
python claude_usage.py --no-anchor   # Disable auto-anchoring
```

- **Auth:** `~/.claude/.credentials.json`
- **State:** `~/.local/state/claude_usage/`
- **Windows:** 5-hour session, 7-day weekly

## Codex

```bash
python codex_usage.py            # Rich summary (auto-notify)
python codex_usage.py --json     # JSON output
python codex_usage.py --no-notify    # Disable auto-notification
```

- **Auth:** `~/.codex/auth.json`
- **State:** `~/.local/state/codex_usage/`
- **Windows:** 5-hour session, 7-day weekly

## Amp

```bash
python amp_usage.py              # Rich summary (auto-notify)
python amp_usage.py --json       # JSON output
python amp_usage.py --no-notify  # Disable auto-notification
```

- **Auth:** `~/.local/share/amp/secrets.json` (via `amp usage` CLI)
- **Windows:** Continuous replenishment ($0.42/hr to $10 max)
- **Notifications:** 
  - **Immediate** when credits are full (optimal time to run tasks)
  - **Scheduled** for exact top-up hour when not full

## Decision Logic (Centralized)

### Fresh Window Notifications

All three harnesses notify immediately when a fresh 5-hour window is available:

| Harness | Trigger | Notification |
|---------|---------|--------------|
| Claude | 5h at 0% + anchored | "Window open - fresh 5h available" |
| Codex | 5h at 0% (no reset) | "Window open - fresh 5h available" |
| Amp | 0% used (full) | "Credits full - optimal time to run" |

### Anchor Logic (Claude only)

Claude anchors idle windows by running a minimal command:

| 5h    | 7d    | Anchor? | Reason                          |
|-------|-------|---------|---------------------------------|
| 0     | 0     | ✅      | Both idle                       |
| 0     | 0<x   | ✅      | 7d active, 5h idle              |
| 0     | 100   | ❌      | 7d exhausted — wasted           |
| 0<x   | 0     | ✅      | 5h active, 7d never started     |
| 0<x   | 0<x   | ❌      | Both active                     |
| 0<x   | 100   | ❌      | 7d exhausted — wasted           |
| 100   | 0     | ❌      | 5h exhausted — wasted           |
| 100   | 0<x   | ❌      | 5h exhausted — wasted           |
| 100   | 100   | ❌      | Both exhausted — wasted         |

### Notify Logic (All)

Notify if ANY window exhausted (≥100%), scheduling for the **latest** reset:

| 5h    | 7d    | Notify? | Target     |
|-------|-------|---------|------------|
| 100   | 0     | ✅      | 5h         |
| 100   | 0<x   | ✅      | 5h         |
| 100   | 100   | ✅      | max(5h,7d) |
| 0<x   | 100   | ✅      | 7d         |
| 0     | 100   | ✅      | 7d         |

### Amp Top-Up Notifications

Amp replenishes continuously. `--notify` schedules for the exact hour when credits will be full.

## Justfile

```bash
# All auto-notify by default; use --no-notify to disable

just usage              # Claude (auto-anchor + auto-notify)
just usage --no-notify  # Disable notifications
just usage --json       # JSON output

just codex-usage        # Codex (auto-notify)
just codex-usage --no-notify  # Disable notifications
just codex-usage --json # JSON output

just amp-usage          # Amp (auto-notify)
just amp-usage --no-notify    # Disable notifications
just amp-usage --json   # JSON output
```
