# Status

Updated: `2026-03-11T07:42:06Z` (UTC)

- Global OpenCode startup was re-verified from the rebuilt `~/ai` config. In `/tmp/opencode-status-refresh.log` there are no `Failed to resolve latest version` warnings, no `plugin_init_warmup` warning, no `when.match is not a function` error, and no duplicate-skill warning. `invalid` is still present and is an expected built-in tool.
- `opencode-time-travel-plugin` is fixed and pinned in `opencode/configs/config_skeleton.json` at `fbd33f84d611afb98bc8fb49409aeb8d531b24ea`.
- `opencode-plugin-improved-task` is fixed for the pointless startup warmup warning, its repo-local `.config/opencode.json` now points at the checkout, and the global config is pinned at `e4355344fbe5f0590ed13424918d730d04a56aec`.
- All git-backed OpenCode plugins in `opencode/configs/config_skeleton.json` are commit-pinned.
- The external plugin packages that were still on `@latest` are now version-pinned: `opencode-anthropic-auth@0.0.13`, `opencode-qwencode-auth@1.3.0`, `opencode-openai-codex-auth@4.4.0`, `cc-safety-net@0.7.1`, `@azumag/opencode-rate-limit-fallback@1.70.0`, `@ramtinj95/opencode-tokenscope@1.5.2`, `opencode-pty@0.2.3`.
- Remaining substantive issue: the shadowed `task` tool in `opencode-plugin-improved-task` still fails the interactive async resume proof. The plugin dispatches both async calls, including `resumed=true`, but the parent session can exit before the later completion is consumed. Tracking issue: https://github.com/dzackgarza/opencode-plugin-improved-task/issues/4
