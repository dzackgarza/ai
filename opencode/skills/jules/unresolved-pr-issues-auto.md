# Unresolved PR Review Issues

**Generated:** 2026-03-16 13:52

This document tracks open PRs with unresolved review issues. Issues are considered resolved only when:

- The review comment has been marked as **resolved** in GitHub (clicked checkmark), OR
- The concern is **struck through** in the PR (~~text~~)

---

## dzackgarza/opencode-plugin-improved-webtools

### PR #39 — fix: use actual row count when reported total results is 0
[Link](https://github.com/dzackgarza/opencode-plugin-improved-webtools/pull/39)

| Issue | Status |
|-------|--------|
| **Offset inflates total**  
_formatResults now sets total = Math.max(reportedTotal, offset + results.length), which makes total equal to offset when results.length === 0; this misreports totals for out-of-range offsets (e.g., sho..._ | 🔴 NOT RESOLVED |

## dzackgarza/opencode-plugin-improved-webtools

### PR #37 — feat: add pre-flight dependency checks at plugin startup
[Link](https://github.com/dzackgarza/opencode-plugin-improved-webtools/pull/37)

| Issue | Status |
|-------|--------|
| **Websearch blocked by w3m**  
_ImprovedWebSearchPlugin throws at initialization if w3m is missing, which prevents *both* webfetch and websearch from registering even though websearch executes without w3m. This makes websearch unusa..._ | 🔴 NOT RESOLVED |
| **Wrong yt-dlp preflight**  
_The YouTube handler’s checkDependencies rejects execution unless yt-dlp exists in PATH, but the actual handler invokes yt-dlp via uvx --from yt-dlp[...] yt-dlp, so a valid uvx-based setup will be fals..._ | 🔴 NOT RESOLVED |
| **Depends on external which**  
_checkDependency() shells out to the which command, so environments without which will fail all dependency checks and can get misleading “missing dependency” errors (including the startup w3m check). T..._ | 🔴 NOT RESOLVED |

## dzackgarza/opencode-plugin-improved-webtools

### PR #36 — fix: sanitize credential paths from yt-dlp stderr before logging
[Link](https://github.com/dzackgarza/opencode-plugin-improved-webtools/pull/36)

| Issue | Status |
|-------|--------|
| **Punctuation bypasses redaction**  
_sanitizeStderr only matches sensitive paths when followed by whitespace or end-of-string, so paths followed by punctuation (e.g. a trailing '.') or wrapped in quotes/parentheses won't be redacted and ..._ | 🔴 NOT RESOLVED |
| **Test leaks env var**  
_The unit test sets process.env.YTDLP_COOKIES_FILE and never restores it, which can alter subsequent tests because youtube command building conditionally adds --cookies based on that env var._ | 🔴 NOT RESOLVED |
| **Test depends on mktemp**  
_The unit test exercises fetchYoutubeTranscriptMarkdown, which unconditionally shells out to mktemp and rm -rf via Bun.$, making the test dependent on system utilities/filesystem rather than only valid..._ | 🔴 NOT RESOLVED |

## dzackgarza/opencode-manager

### PR #11 — fix: switch sendPrompt from response.json() to SSE stream reader
[Link](https://github.com/dzackgarza/opencode-manager/pull/11)

| Issue | Status |
|-------|--------|
| **Tool-call reply returned**  
_sendPrompt treats any message.updated with role === "assistant" as the final answer, so it can return an intermediate assistant message whose finish is "tool-calls" (requires continuation) instead of ..._ | 🔴 NOT RESOLVED |
| **Strict SSE data parsing**  
_sendPrompt only recognizes lines starting with "data: " and does not implement SSE event framing, so valid SSE payloads like data: (no space) or multi-line data: frames can be skipped, leaving finalMe..._ | 🔴 NOT RESOLVED |

## dzackgarza/opencode-manager

### PR #10 — fix: boolean flags no longer consume the following positional argument
[Link](https://github.com/dzackgarza/opencode-manager/pull/10)

| Issue | Status |
|-------|--------|
| **CamelCase booleans still swallow**  
_main() treats only dashed boolean flags as immediate booleans; camelCase aliases (e.g. --noReply, --teeTemp) still fall through to the “take next token as value” path and can consume the next position..._ | 🔴 NOT RESOLVED |

## dzackgarza/zotero-local-write-api

### PR #6 — fix: remove tag from all items before deleting from library
[Link](https://github.com/dzackgarza/zotero-local-write-api/pull/6)

| Issue | Status |
|-------|--------|
| **Partial tag delete state**  
_handleDeleteTag removes and saves tags item-by-item and only afterwards calls Zotero.Tags.removeFromLibrary, so any mid-loop saveTx() failure or a removeFromLibrary() failure can leave the library in ..._ | 🔴 NOT RESOLVED |

## dzackgarza/usage-limits

### PR #4 — refactor: migrate OTLP sink to centralized otlp-collector dependency
[Link](https://github.com/dzackgarza/usage-limits/pull/4)

| Issue | Status |
|-------|--------|
| **Removed serve still invoked**  
_The PR deletes the Typer serve command, but the new just serve recipe and the new systemd unit still run usage-limits serve, which will fail at runtime with an unknown-command error._ | 🔴 NOT RESOLVED |
| **install-service greps wrong source**  
_just install-service greps OPENROUTER_SINK_TOKEN from the .envrc file (where it’s commented out) instead of extracting from .env or the environment, so the command will fail under set -e or generate a..._ | 🔴 NOT RESOLVED |
| **OpenRouter notify always fires**  
_OpenRouterProvider.fetch_raw() returns count=0 unconditionally, so pct_used stays 0 and notify_always() sends a “Daily Reset” notification on every run when --notify is enabled._ | 🔴 NOT RESOLVED |
| **OpenRouter limit message incorrect**  
_OpenRouter computes the daily limit as 50 or 1000 depending on is_free_tier, but the “Daily Reset” notification always reports 1000 requests available, misleading users on the 50/day tier._ | 🔴 NOT RESOLVED |

## dzackgarza/opencode-plugin-improved-webtools

### PR #33 — CLI-first migration for improved-webtools
[Link](https://github.com/dzackgarza/opencode-plugin-improved-webtools/pull/33)

| Issue | Status |
|-------|--------|
| **Bridge timeout mismatch**  
_run_bridge() kills the Bun bridge after 60s, but the TypeScript webfetch pipeline explicitly allows longer steps (e.g., Wikipedia conversion up to 120s), so the CLI/MCP can time out mid-operation. Thi..._ | 🔴 NOT RESOLVED |
| **Fetch/search status misleading**  
_The Bun bridge hardcodes status: "ok" for fetch and search, even when operations return clear setup/validation failure messages (missing SEARXNG_INSTANCE_URL, missing curl/w3m/uvx, etc.). As a result,..._ | 🔴 NOT RESOLVED |

## dzackgarza/opencode-time-travel-plugin

### PR #5 — feat: migrate time-travel plugin to cli-first architecture
[Link](https://github.com/dzackgarza/opencode-time-travel-plugin/pull/5)

| Issue | Status |
|-------|--------|
| **Weekday cron parsing broken**  
_parse_cron_expression() rewrites the entire weekday field via .replace("7","0"), corrupting valid expressions containing the digit 7 (for example */7 becomes */0 and raises). This makes some recurring..._ | 🔴 NOT RESOLVED |
| **Blocking dispatch polling**  
_The plugin’s poller calls dispatchDueReminders() on an interval, which executes the CLI via spawnSync with no timeout; this blocks the event loop and can hang the OpenCode process if the CLI stalls. A..._ | 🔴 NOT RESOLVED |
| **Cancel not-found throws**  
_The CLI cancel command exits with code 1 when a reminder is missing, and the plugin calls it via runTimeTravelCli() which throws on any non-zero exit status. This turns a normal “not found” cancellati..._ | 🔴 NOT RESOLVED |
| **Non-portable PATH check**  
_commandOnPath() hardcodes PATH splitting on :, so CLI detection fails on platforms using different delimiters (e.g., Windows uses ;). It also checks only for file existence (not executability), which ..._ | 🔴 NOT RESOLVED |

## dzackgarza/opencode-zotero-plugin

### PR #36 — feat: migrate zotero plugin to cli-first architecture
[Link](https://github.com/dzackgarza/opencode-zotero-plugin/pull/36)

| Issue | Status |
|-------|--------|
| **Dispatcher imports missing symbols**  
_zotero_librarian._dispatch imports batch_delete_items, delete_*, and delete_item symbols that are not defined in the referenced modules, causing an ImportError during import and preventing zotero-lib ..._ | 🔴 NOT RESOLVED |
| **PyYAML removed but required**  
_python/pyproject.toml no longer declares PyYAML, but zotero_librarian.settings imports yaml and is loaded at import time by connector.py, so a clean install will fail to import the package._ | 🔴 NOT RESOLVED |
| **Trash tool name mismatch**  
_The dispatcher registry now exposes delete_item/delete_items, but the OpenCode plugin still calls trash_item/trash_items, so zotero_trash_items requests will fail with an unknown-tool error._ | 🔴 NOT RESOLVED |

| ~~Resolved~~ | Status |
| ---- | ---- |
| ~~Unsupported extractor default ☑~~ | ✅ RESOLVED |

## dzackgarza/opencode-plugin-improved-webtools

### PR #29 — feat: arxiv local library + audit fixes
[Link](https://github.com/dzackgarza/opencode-plugin-improved-webtools/pull/29)

| Issue | Status |
|-------|--------|
| **Missing opencode-manager in tests**  
_The integration test shells out to npx --package=<repo>/../opencode-manager opx ..., but this repo neither contains that sibling path nor declares it as an npm dependency, so the integration test will..._ | 🔴 NOT RESOLVED |
| **GitHub file path not encoded**  
_The GitHub handler decodes URL path segments and then interpolates the decoded filePath into a `gh api ...contents/<filePath>?ref=... string, so filenames containing reserved characters like ?` or # c..._ | 🔴 NOT RESOLVED |
| **Unpinned bunx git shim**  
_The MCP server executes bunx --package=git+https://... opencode-mcp-shim on every tool call with a 30s timeout, which runs mutable remote code (supply-chain risk) and can fail in offline/cold-cache sc..._ | 🔴 NOT RESOLVED |

## dzackgarza/opencode-zotero-plugin

### PR #27 — feat: implement issues + audit fixes
[Link](https://github.com/dzackgarza/opencode-zotero-plugin/pull/27)

| Issue | Status |
|-------|--------|
| **Trash tool permission denied**  
_.config/opencode.json still allows zotero_delete_items, but the TypeScript plugin exports zotero_trash_items, so OpenCode will deny the trash tool for both default and plugin-proof agent permissions._ | 🔴 NOT RESOLVED |
| **Npm publish missing python**  
_package.json restricts published files to src/ only, but src/index.ts executes Python from a sibling python/ directory (cwd: ../python), so installed consumers will fail because that directory is not ..._ | 🔴 NOT RESOLVED |
| **Attach-bytes memory blowup**  
_The new attach-bytes fallback base64-encodes source_file.read_bytes() into JSON, which loads the entire file into memory and can exhaust memory or severely degrade performance on large PDFs._ | 🔴 NOT RESOLVED |
| **Config resource hard-required**  
_settings.py unconditionally reads config.yaml as a package resource, so environments where that resource isn’t shipped (or is mispackaged) will crash during import instead of producing a structured co..._ | 🔴 NOT RESOLVED |

## dzackgarza/opencode-time-travel-plugin

### PR #3 — feat: systemd-backed reminders + audit fixes
[Link](https://github.com/dzackgarza/opencode-time-travel-plugin/pull/3)

| Issue | Status |
|-------|--------|
| **Recurring install not rolled back**  
_When scheduling a recurring reminder, errors from ensureRecurringDispatcherInstalled() only trigger deletion of the reminder JSON, leaving any already-written unit files/timers behind. This can result..._ | 🔴 NOT RESOLVED |
| **ExecStart breaks on spaces**  
_The recurring dispatcher unit file embeds home and dispatchScript into ExecStart= without quoting/escaping, so paths containing spaces can break systemd argument parsing and prevent the dispatcher fro..._ | 🔴 NOT RESOLVED |

| ~~Resolved~~ | Status |
| ---- | ---- |
| ~~Corrupt reminder crashes plugin ☑~~ | ✅ RESOLVED |
| ~~Shell command persistence risk ☑~~ | ✅ RESOLVED |
| ~~Integration tests assume nc/systemd ☑~~ | ✅ RESOLVED |

---

## Summary

| Status | Count |
|--------|-------|
| 🔴 NOT RESOLVED | 33 |
| ✅ RESOLVED | 4 |
