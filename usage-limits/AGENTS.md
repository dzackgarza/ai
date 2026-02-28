# Usage Limits — Agent Guide

Four scripts report quota across Claude, Codex, Amp, and Antigravity in a uniform table:

```
| Identifier              | XX% | ████████░░░░ | in 4h 12m |
```

## File Structure

| File | Purpose |
|------|---------|
| `usage_base.py` | `UsageProvider` ABC — orchestration, anchoring, notifications |
| `usage_table.py` | `UsageRow` (Pydantic) + `UsageTable` (Rich renderer) |
| `claude_usage.py` | Claude Code provider |
| `codex_usage.py` | Codex CLI provider |
| `amp_usage.py` | Amp provider (credit replenishment model) |
| `antigravity_usage.py` | Antigravity provider (per-model quotas) |

---

## Notification Logic

`UsageProvider.should_notify()` fires when any row is exhausted (≥ 100%). It schedules the notification for the **latest** `reset_at` among all exhausted rows — the true blocking constraint.

`UsageProvider._handle_notifications()` calls `should_notify()`, deduplicates via ntfy scheduled-message lookup, then fires `_schedule_notification()`.

### Standard truth table (Claude, Codex, Antigravity)

| 5h     | 7d     | Notify? | Target     |
|--------|--------|---------|------------|
| < 100  | < 100  | No      | —          |
| 100    | < 100  | Yes     | 5h reset   |
| 100    | 100    | Yes     | later of the two |
| < 100  | 100    | Yes     | 7d reset   |

### Amp (override)

Amp overrides `_handle_notifications()` entirely. It has no exhaustion concept.

| Credits     | Action |
|-------------|--------|
| Full (0% used) | Notify immediately |
| Not full    | Schedule for exact hour credits reach $10 |

Deduplication key: `amp-topup-{unix_timestamp_of_topup_time}`

---

## Anchoring Logic

Anchoring runs a minimal CLI command to start a usage window before it lapses. The base implementation runs `anchor_command()` and re-fetches after anchoring.

`run()` skips anchoring when `anchor_command()` returns `None` or `--no-anchor` is set.

### Default rule (Claude, Codex) — `UsageProvider.should_anchor()`

Anchor when any row has `reset_at = None` (window never started) **and** no row is exhausted.

| 5h              | 7d              | Anchor? | Reason                    |
|-----------------|-----------------|---------|---------------------------|
| 0% (no reset)   | 0% (no reset)   | Yes     | Both idle                 |
| 0% (no reset)   | 0 < x < 100     | Yes     | 7d active, 5h idle        |
| 0% (no reset)   | 100%            | No      | 7d exhausted — wasted     |
| 0 < x < 100     | 0% (no reset)   | Yes     | 5h active, 7d never started |
| 0 < x < 100     | 0 < x < 100     | No      | Both active               |
| 0 < x < 100     | 100%            | No      | 7d exhausted — wasted     |
| 100%            | any             | No      | 5h exhausted — wasted     |

### Antigravity override — `AntigravityProvider.should_anchor()`

Anchor when **all** models are at exactly 0% usage (fresh quota just became available). Antigravity's own cron scheduler handles the actual wakeup trigger; this Python script only detects the condition and notifies.

| All models at 0% | Anchor? |
|------------------|---------|
| Yes              | Yes     |
| No               | No      |

### Amp

No anchoring. Credits replenish continuously; there is no idle window to start. `anchor_command()` returns `None`.

---

## Adding a New Provider

### 1. Implement `UsageProvider`

Create `{name}_usage.py`. Implement two abstract methods and set four class attributes:

```python
import argparse
from typing import Any

from usage_base import UsageProvider
from usage_table import UsageRow


class MyProvider(UsageProvider):
    name = "MyTool"           # Display name in table header and notifications
    state_dir = "mytool_usage"  # Directory name under ~/.local/state/
    ntfy_topic = "usage-updates"   # Optional; this is the default
    ntfy_server = "http://localhost"  # Optional; this is the default

    def fetch_raw(self) -> Any:
        """Fetch raw data from API or CLI. Exit with sys.exit(1) on auth failure."""
        ...

    def to_rows(self, raw: Any) -> list[UsageRow]:
        """Convert raw data to UsageRow list. One row per quota window or model."""
        return [
            UsageRow(
                identifier="MyTool (5h)",   # Shown in the Identifier column
                pct_used=42.0,              # 0.0–100.0
                reset_at=some_datetime_utc, # datetime | None; None = not applicable
            ),
        ]


def main() -> None:
    parser = argparse.ArgumentParser(description="MyTool usage limits checker")
    parser.add_argument("--json", "-j", action="store_true")
    parser.add_argument("--no-notify", action="store_true")
    parser.add_argument("--no-anchor", action="store_true")  # omit if no anchoring
    args = parser.parse_args()
    MyProvider().run(args)


if __name__ == "__main__":
    main()
```

### 2. Choose identifier format

| Provider type | Identifier pattern | Example |
|---|---|---|
| Single window | `"Name"` | `"Amp"` |
| Multiple windows | `"Name (window)"` | `"Claude (5h)"`, `"Claude (7d)"` |
| Per-model | `"Provider: Model"` | `"Antigravity: Gemini 2.5 Flash"` |

### 3. Override anchoring (if needed)

If the default idle-window rule does not apply, override `should_anchor()` and `anchor_command()`:

```python
def anchor_command(self) -> list[str]:
    return ["mytool", "--flag", "Say hello and do nothing else"]

def should_anchor(self, rows: list[UsageRow]) -> bool:
    # Custom logic — e.g., anchor only when 5h window is idle
    return any(r.identifier.endswith("(5h)") and r.reset_at is None for r in rows)
```

Return `None` from `anchor_command()` (the default) to disable anchoring entirely.

### 4. Override notifications (if needed)

Override `_handle_notifications(rows)` only when the standard exhaustion-based logic does not fit — as Amp does for its fill-based model. The standard logic handles all exhaustion/deduplication patterns correctly for window-based quotas.

---

## Testing a New Provider

Run these checks in order. Fix each failure before continuing.

### Import and instantiation
```bash
python -c "from mytool_usage import MyProvider; p = MyProvider(); print('OK')"
```

### Table renders without errors
```bash
python mytool_usage.py --no-notify --no-anchor
```
Check: header panel shows, all rows display `| Identifier | XX% | bar | time |`, no wrapping or truncation in the Identifier or Pct columns.

### JSON output
```bash
python mytool_usage.py --json | python -m json.tool > /dev/null && echo "valid JSON"
```

### Logic unit checks

```python
python -c "
from mytool_usage import MyProvider
from usage_table import UsageRow
from datetime import datetime, timezone, timedelta

p = MyProvider()
now = datetime.now(timezone.utc)

idle     = [UsageRow(identifier='X (5h)', pct_used=0.0)]
active   = [UsageRow(identifier='X (5h)', pct_used=50.0, reset_at=now + timedelta(hours=2))]
dead     = [UsageRow(identifier='X (5h)', pct_used=100.0, reset_at=now + timedelta(hours=1))]

# Anchor
print('anchor idle:',     p.should_anchor(idle))    # True for window-based
print('anchor active:',   p.should_anchor(active))  # False
print('anchor exhausted:', p.should_anchor(dead))   # False

# Notify
print('notify idle:',     p.should_notify(idle))    # (False, None)
print('notify active:',   p.should_notify(active))  # (False, None)
print('notify exhausted:', p.should_notify(dead))   # (True, datetime)
"
```

### ABC enforcement

```python
python -c "
from usage_base import UsageProvider
class Incomplete(UsageProvider):
    name = 'x'
    state_dir = 'x'
try:
    Incomplete()
    print('FAIL — should have raised TypeError')
except TypeError:
    print('OK — abstract methods enforced')
"
```

---

## `UsageRow` Reference

```python
UsageRow(
    identifier: str,          # Required. Label shown in table.
    pct_used: float,          # Required. 0.0–100.0.
    reset_at: datetime | None # Optional. UTC datetime of limit reset. None = N/A.
)
```

Computed fields (read-only, derived automatically):

| Field | Type | Value |
|-------|------|-------|
| `is_exhausted` | `bool` | `True` when `pct_used >= 100.0` |
| `time_until_reset` | `str` | `"in 4h 12m"`, `"in 2d 3h"`, `"now"`, or `""` if `reset_at` is `None` |
