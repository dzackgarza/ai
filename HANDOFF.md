# Restore OpenCode startup

## Task

Restore interactive OpenCode startup and model selection on this host, with the
configured plugin functions available.

## Completion condition

| Requirement | Acceptance | Status |
| --- | --- | --- |
| Startup | A fresh normal launch reaches the input prompt | Unverified after repair |
| Model selection | The normal configuration returns HTTP 200 from `/api/model` | Blocked by package installation |
| Plugins | Configured plugin functions load with the selected OpenCode API | Version choice pending |
| Existing sessions | Preserve session data and existing worker processes | Required throughout |

The installed OpenCode is 2.0.31. A private 2.1.4 probe also returns HTTP 503,
`Location plugins did not finish activating`. The background server holds npm
installation locks for TokenScope and cc-safety-net. The staging directories are
empty. The server log also reports `LockTimeoutError` for TokenScope.

A separate configuration copy with the package plugin list empty returns the model
list successfully. This is diagnostic evidence, not the intended final setup.
Installing the configured packages with Bun succeeds. Their installed entrypoints
show that TokenScope 1.8.1, Ensemble 0.13.3, and context-mode 1.0.169 use the older
plugin API. TokenScope's upstream V2 support request remains open.

## Next work

1. Resolve the pending choice: use OpenCode 1.x with the existing plugin API, or
   retain OpenCode 2.x and update the plugin setup. The user has not selected either
   route. TokenScope needs a V2 implementation if V2 is retained.
2. Repair package installation through a verified install path. Recheck live lock
   ownership before changing runtime state. Do not delete locks held by a live
   process. The OpenCode CLI skill requires approval before resetting the user
   service.
3. Verify a fresh normal launch, model selection, and plugin functions. Record the
   chosen setup in the owning config sources and rebuild the generated config.

The existing global config is assembled from `opencode/configs/config_skeleton.json`
and provider fragments. `opencode/cli.json` separately loads
`oc-codex-multi-auth`; its initial package preparation stalled, then completed.

Use the log at `~/.local/share/opencode/log/opencode.log` to verify current state.
Do not reuse `OPENCODE_CONFIG_CONTENT` probes: `opencode debug config` on this
installation does not include that variable. An isolated `XDG_CONFIG_HOME` did
select the diagnostic configuration.

Upstream evidence:

- [Unbounded V2 npm installation](https://github.com/anomalyco/opencode/issues/41934)
- [Cold-cache Arborist hang](https://github.com/anomalyco/opencode/issues/31463)
- [TokenScope V2 support](https://github.com/ramtinj95/opencode-tokenscope/issues/52)
