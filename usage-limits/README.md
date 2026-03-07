# Usage Limits Checkers

Four harnesses, unified interface. All auto-detect auth, all support JSON output.

## ⚠️ Obtaining Usage Data

**None of this information is publicly documented.** Each provider required reverse-engineering:

| Provider | How Auth Was Found |
|----------|-------------------|
| **Claude** | Inspected `~/.claude/.credentials.json` discovered by CLI; OAuth endpoint found via network tab + GitHub issues |
| **Codex** | Located `~/.codex/auth.json` via filesystem search; WHAM API endpoint discovered in browser DevTools Network tab |
| **Amp** | `amp usage` CLI command discovered via `amp --help`; output parsed with regex |
| **Antigravity** | Global npm package `antigravity-usage` found via community Discord; `--json` flag discovered via source inspection |
| **Ollama** | Session cookie extracted from browser DevTools → Application → Cookies; HTML scraping from `/settings` page |
| **OpenRouter** | Free tier request count not exposed via API — no tracking available |
| **Qwen** | OpenAI logging feature discovered via CLI docs; request count from local log files in `~/qwen-logs/` |

**OpenRouter does not expose free tier request counts** — the API only tracks credits. The 50 requests/day free tier limit cannot be queried programmatically.

**To add a new provider, expect to:**

1. Search GitHub issues, Reddit, Discord for existing community discoveries
2. Inspect browser DevTools (Network tab, Application storage)
3. Search filesystem for credential files (`~/.config/`, `~/.local/`, `~/.*`)
4. Reverse-engineer CLI commands (`strace`, `--verbose` flags)
5. Read package source code (npm, pip) when available

There is no official documentation. Everything here was discovered through community effort.

## Claude Code

```bash
python claude_usage.py           # Rich summary (auto-anchor + auto-notify)
python claude_usage.py --json    # JSON output
python claude_usage.py --no-notify   # Disable auto-notification
python claude_usage.py --no-anchor   # Disable auto-anchoring
```

- **Auth:** `~/.claude/.credentials.json`
- **Anchor:** `claude --setting-sources "" "Say hello"`
- **State:** `~/.local/state/claude_usage/`
- **Windows:** 5-hour session, 7-day weekly

## Codex

```bash
python codex_usage.py            # Rich summary (auto-anchor + auto-notify)
python codex_usage.py --json     # JSON output
python codex_usage.py --no-notify    # Disable auto-notification
python codex_usage.py --no-anchor    # Disable auto-anchoring
```

- **Auth:** `~/.codex/auth.json`
- **Anchor:** `codex exec -c project_doc_max_bytes=0 "Say hello"`
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

## Antigravity

```bash
python antigravity_usage.py      # Rich summary (auto-notify)
python antigravity_usage.py --json  # JSON output
python antigravity_usage.py --no-notify  # Disable auto-notification
```

- **Auth:** `npx antigravity-usage login` (one-time Google OAuth)
- **Data source:** Wraps `antigravity-usage` CLI
- **Windows:** Aggregated 5h/7d from per-model quotas
- **Notifications:** Fresh window + exhausted quota (same as Claude/Codex)
- **Note:** Requires Node.js for `npx`. Works without Antigravity desktop app.

## OpenRouter

> **Not yet implemented.** `fetch_raw()` raises `NotImplementedError`. A request-counting mechanism is needed that does not depend on third-party observability tooling.

```bash
python openrouter_usage.py         # Rich summary (not yet functional)
python openrouter_usage.py --json  # JSON output
python openrouter_usage.py --no-notify  # Disable auto-notification
```

- **Limits:** 50 req/day if credits never purchased; 1000 req/day if credits were ever purchased. Resets at UTC midnight.
- **Known constraint:** OpenRouter API only exposes credit balance, not request counts. The daily free-tier count cannot be queried directly.

## Qwen Code

```bash
python qwen_usage.py             # Rich summary
python qwen_usage.py --json      # JSON output
python qwen_usage.py --no-notify # Disable auto-notification
```

- **Auth:** Auto-detected from Qwen CLI session
- **Data source:** Local OpenAI logging files in `~/qwen-logs/`
- **Setup:** Enable logging in `~/.qwen/settings.json`:
  ```json
  {
    "model": {
      "enableOpenAILogging": true,
      "openAILoggingDir": "~/qwen-logs"
    }
  }
  ```
- **Limits:** 1000 requests/day (free tier), resets at UTC midnight
- **How it works:** Counts log files created by Qwen CLI's OpenAI logging feature

## Decision Logic (Centralized)

### Fresh Window Notifications

All three harnesses notify immediately when a fresh 5-hour window is available:

| Harness | Trigger | Notification |
|---------|---------|--------------|
| Claude | 5h at 0% + anchored | "Window open - fresh 5h available" |
| Codex | 5h at 0% (no reset) | "Window open - fresh 5h available" |
| Amp | 0% used (full) | "Credits full - optimal time to run" |

### Anchor Logic (Claude + Codex)

Both Claude and Codex anchor idle windows by running a minimal CLI command:

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
# All auto-notify + auto-anchor by default; use --no-* to disable

just usage              # All providers
just usage --json       # All providers in JSON

just usage-claude       # Claude (auto-anchor + auto-notify)
just usage-claude --no-notify  # Disable notifications
just usage-claude --no-anchor  # Disable anchoring

just usage-codex        # Codex (auto-anchor + auto-notify)
just usage-codex --no-notify  # Disable notifications
just usage-codex --no-anchor  # Disable anchoring

just usage-amp          # Amp (auto-notify)
just usage-amp --no-notify    # Disable notifications

just usage-antigravity  # Antigravity (auto-notify)
just usage-antigravity --no-notify  # Disable notifications

just usage-openrouter   # OpenRouter (auto-notify) — not yet functional
just usage-openrouter --no-notify  # Disable notifications

just usage-ollama       # Ollama (auto-notify)
just usage-ollama --no-notify  # Disable notifications

just usage-qwen         # Qwen (auto-notify)
just usage-qwen --no-notify  # Disable notifications
```

Recipes are in `~/ai/justfile`.
