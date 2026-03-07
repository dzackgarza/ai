# OpenCode Plugins

Global plugins loaded from `~/.config/opencode/plugins/`.

## Structure

- Root `*.ts`: active runtime-loaded plugins and tool surfaces.
- `examples/`: in-development or reference plugins that are **not** auto-loaded while they stay under `examples/`.
- `tests/unit/`: unit tests for the active runtime-loaded plugins.
- `utilities/harness/`: session automation CLI.
- `utilities/scripts/`: helper scripts that support plugin-adjacent workflows.

## Active Runtime Plugins

These files live at the plugin root because OpenCode auto-loads top-level plugin modules:

| File | Purpose |
|------|---------|
| `async-command.ts` | Background callback tool |
| `git-add.ts` | Staging helper tool |
| `git-commit.ts` | Commit helper tool |
| `introspection.ts` | Session metadata tool |
| `list-sessions.ts` | Session listing tool |
| `plan_exit.ts` | Plan handoff tool |
| `read-transcript.ts` | Transcript export tool |
| `sleep.ts` | Time-based callback tools |
| `write_plan.ts` | Plan persistence tool |
| `plugins_config.ts` | Reads local plugin toggle state |

## Example Plugin Surfaces

- `examples/command-interceptor/`: example interceptor plus its unit test.
- `examples/prompt-router/`: prompt-router plugin in development, grouped with:
  - `tiers/` behavioral instruction files
  - `tests/classifier/` classifier harness and scored runs
  - `tests/behavior/` end-to-end behavior harness and captured results
  - `tests/prompt-router.test.ts` prompt-matching unit test
- `examples/context-injector.ts`, `examples/cot-trivial-test.ts`, and the JS examples remain as standalone reference plugins.
- `examples/retired/` contains examples intentionally kept out of the active surface.

## Recipes

```bash
just check
just test
just classifier
just behavior A
just baseline A
just callback-integration
just session list
```

Recipe intent:

- `just test` runs live unit tests plus example tests that still belong to current example plugins.
- `just classifier`, `just classifier-model`, `just classifier-mdjson`, `just behavior`, and `just baseline` are all scoped to `examples/prompt-router/`.
- `just session ...` delegates to `utilities/harness/`.

## Layout

```text
plugins/
├── *.ts                          # Active auto-loaded plugins
├── examples/                     # In-development and reference plugins
│   ├── command-interceptor/
│   ├── prompt-router/
│   │   ├── index.ts
│   │   ├── tiers/
│   │   └── tests/
│   └── retired/
├── tests/
│   └── unit/                     # Active-plugin unit tests
└── utilities/
    ├── harness/                  # Session automation CLI
    └── scripts/                  # Helper scripts
```

## Local Config

Plugin toggle state lives at `~/ai/opencode/configs/local-plugins.json`.
