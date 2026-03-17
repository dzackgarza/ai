# Unresolved PR Review Issues

**Generated:** 2026-03-16

This document tracks open PRs with unresolved review issues. Issues are considered resolved only when:

- The review comment has been marked as **resolved** in GitHub (clicked checkmark), OR
- The concern is **struck through** in the PR (~~text~~)

---

## opencode-plugin-improved-webtools

### PR #39 — fix: use actual row count when reported total results is 0

| Issue                                                                                                           | Reporter | Status          |
| --------------------------------------------------------------------------------------------------------------- | -------- | --------------- |
| Offset inflates total — `Math.max(reportedTotal, offset + results.length)` inflates totals when window is empty | Qodo     | 🔴 NOT RESOLVED |

**Details:** When `results.length === 0`, total becomes `Math.max(reportedTotal, offset)` which incorrectly raises totals based on the requested offset.

---

### PR #36 — fix: sanitize credential paths from yt-dlp stderr before logging

| Issue                                                                                                                               | Reporter | Status          |
| ----------------------------------------------------------------------------------------------------------------------------------- | -------- | --------------- |
| Punctuation bypasses redaction — regex requires whitespace/EOL, paths followed by punctuation (e.g. `auth.json.`) won't be redacted | Qodo     | 🔴 NOT RESOLVED |
| Test leaks env var — `process.env.YTDLP_COOKIES_FILE` is set but never restored, causing order-dependent tests                      | Qodo     | 🔴 NOT RESOLVED |
| Test depends on mktemp — test depends on system utilities (`mktemp`, `rm`) making it non-portable                                   | Qodo     | 🔴 NOT RESOLVED |

---

## opencode-manager

### PR #10 — fix: boolean flags no longer consume the following positional argument

| Issue                                                                                                                                            | Reporter | Status          |
| ------------------------------------------------------------------------------------------------------------------------------------------------ | -------- | --------------- |
| CamelCase booleans still swallow — `--noReply`, `--teeTemp` still go through "read next arg as value" logic and consume required positional args | Qodo     | 🔴 NOT RESOLVED |

---

## zotero-local-write-api

### PR #6 — fix: remove tag from all items before deleting from library

| Issue                                                                                                                                                      | Reporter | Status          |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | --------------- |
| Partial tag delete state — mid-loop `saveTx()` failure or `removeFromLibrary()` failure can leave library in partially-updated state while returning error | Qodo     | 🔴 NOT RESOLVED |

---

## opencode-zotero-plugin

### PR #38 — feat: implement analysis.toc-note command for LLM-generated structured notes

| Issue                                                                                                                                                                                                                       | Reporter           | Status                             |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ | ---------------------------------- |
| Critical: node_modules committed — entire `node_modules` directory added to repository, bloats repo and complicates reviews. Also: discrepancy between PR title (new feature) and actual changes (only vendor dependencies) | Gemini Code Assist | 🔴 NOT RESOLVED (state: COMMENTED) |

---

## Resolved / No Issues

The following PRs have either no unresolved issues or issues were properly addressed:

| Repo                              | PR  | Status                                  |
| --------------------------------- | --- | --------------------------------------- |
| opencode-plugin-improved-webtools | #37 | ✅ Issues addressed in f33d24c, 2df1283 |
| opencode-plugin-improved-webtools | #38 | ✅ Qodo: "Great, no issues found!"      |
| opencode-plugin-improved-webtools | #40 | ✅ Clean                                |
| opencode-manager                  | #11 | ✅ Fixed in 51dc292                     |
| opencode-zotero-plugin            | #37 | ✅ Clean                                |
| zotero-local-write-api            | #7  | ✅ Clean                                |
| usage-limits                      | #4  | ✅ Clean                                |

---

## Additional PRs with Unresolved Issues (Found on deeper check)

### opencode-plugin-improved-webtools PR #33 — CLI-first migration

| Issue                                                                                                         | Reporter | Status          |
| ------------------------------------------------------------------------------------------------------------- | -------- | --------------- |
| Bridge timeout mismatch — CLI/MCP has hardcoded 60s timeout but TypeScript allows up to 120s (e.g. Wikipedia) | Qodo     | 🔴 NOT RESOLVED |
| Fetch/search status misleading — CLI status doesn't accurately reflect operation status                       | Qodo     | 🔴 NOT RESOLVED |

### opencode-time-travel-plugin PR #5 — migrate to cli-first architecture

| Issue                                                                                         | Reporter | Status          |
| --------------------------------------------------------------------------------------------- | -------- | --------------- |
| Weekday cron parsing broken — `.replace("7", "0")` corrupts valid expressions like `*/7`      | Qodo     | 🔴 NOT RESOLVED |
| Blocking dispatch polling — blocking while-loop in async context                              | Qodo     | 🔴 NOT RESOLVED |
| Cancel not-found throws — canceling non-existent schedule throws instead of graceful handling | Qodo     | 🔴 NOT RESOLVED |
| Non-portable PATH check — relies on PATH behavior that may vary                               | Qodo     | 🔴 NOT RESOLVED |

### opencode-zotero-plugin PR #36 — migrate to cli-first Typer architecture

| Issue                                                              | Reporter | Status          |
| ------------------------------------------------------------------ | -------- | --------------- |
| Dispatcher imports missing symbols — missing imports in dispatcher | Qodo     | 🔴 NOT RESOLVED |
| PyYAML removed but required — dependency removed but still needed  | Qodo     | 🔴 NOT RESOLVED |
| ~~Unsupported extractor default~~ — resolved (struck through)      | Qodo     | ✅ RESOLVED     |
| Trash tool name mismatch — tool name doesn't match expected format | Qodo     | 🔴 NOT RESOLVED |

### opencode-plugin-improved-webtools PR #29 — arxiv local library + audit fixes

| Issue                                                            | Reporter | Status          |
| ---------------------------------------------------------------- | -------- | --------------- |
| Missing opencode-manager in tests — test dependency not declared | Qodo     | 🔴 NOT RESOLVED |
| GitHub file path not encoded — paths not URL-encoded properly    | Qodo     | 🔴 NOT RESOLVED |
| Unpinned bunx git shim — security risk from unpinned dependency  | Qodo     | 🔴 NOT RESOLVED |

### opencode-zotero-plugin PR #27 — implement issues + audit fixes

| Issue                                                                                 | Reporter | Status          |
| ------------------------------------------------------------------------------------- | -------- | --------------- |
| Trash tool permission denied — permission error not handled gracefully                | Qodo     | 🔴 NOT RESOLVED |
| Npm publish missing python — CI publish step missing Python dependency                | Qodo     | 🔴 NOT RESOLVED |
| Attach-bytes memory blowup — loading entire file into memory causes performance issue | Qodo     | 🔴 NOT RESOLVED |
| Config resource hard-required — config file required but should be optional           | Qodo     | 🔴 NOT RESOLVED |

### opencode-time-travel-plugin PR #3 — systemd-backed reminders

| Issue                                                                        | Reporter | Status          |
| ---------------------------------------------------------------------------- | -------- | --------------- |
| ~~Corrupt reminder crashes plugin~~ — resolved                               | Qodo     | ✅ RESOLVED     |
| ~~Shell command persistence risk~~ — resolved                                | Qodo     | ✅ RESOLVED     |
| Recurring install not rolled back — failed install not cleaned up            | Qodo     | 🔴 NOT RESOLVED |
| ~~Integration tests assume nc/systemd~~ — resolved                           | Qodo     | ✅ RESOLVED     |
| ExecStart breaks on spaces — systemd service file fails with spaces in paths | Qodo     | 🔴 NOT RESOLVED |

---

_This document was not fully exhaustive on first pass. Older PRs need complete Qodo review body extraction._
