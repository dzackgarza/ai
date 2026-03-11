# Status

Updated: `2026-03-11T08:09:02Z` (UTC)

- Global OpenCode startup was re-verified from the rebuilt `~/ai` config. In `/tmp/opencode-status-refresh.log` there are no `Failed to resolve latest version` warnings, no `plugin_init_warmup` warning, no `when.match is not a function` error, and no duplicate-skill warning. `invalid` is still present and is an expected built-in tool.
- `opencode-time-travel-plugin` is fixed and pinned in `opencode/configs/config_skeleton.json` at `fbd33f84d611afb98bc8fb49409aeb8d531b24ea`.
- `opencode-plugin-improved-task` is fixed for the pointless startup warmup warning, its repo-local `.config/opencode.json` now points at the checkout, and the global config is pinned at `e4355344fbe5f0590ed13424918d730d04a56aec`.
- All git-backed OpenCode plugins in `opencode/configs/config_skeleton.json` are commit-pinned.
- The external plugin packages that were still on `@latest` are now version-pinned: `opencode-anthropic-auth@0.0.13`, `opencode-qwencode-auth@1.3.0`, `opencode-openai-codex-auth@4.4.0`, `cc-safety-net@0.7.1`, `@azumag/opencode-rate-limit-fallback@1.70.0`, `@ramtinj95/opencode-tokenscope@1.5.2`, `opencode-pty@0.2.3`.
- The previously filed `task` async-resume issue was closed because it was based on flawed TUI-scraping and non-equivalent probes, not session-level evidence. There is no remaining confirmed plugin-runtime bug from that line of investigation.
