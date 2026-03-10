# Usage Limits Extraction Plan

## Goal

Extract `usage_limits` into its own public Python repo so that:

- `uvx usage-limits ...` is the canonical operational interface
- Python callers can import a stable library API
- new providers are added as uniform provider submodules instead of ad hoc standalone scripts
- downstream tools consume one JSON contract regardless of provider

The extraction target should be the packaged implementation in `scripts/usage_limits`, not the legacy top-level `usage-limits/` tree.

## Current State

### Live sources

- `scripts/usage_limits/`
  - already packaged with `pyproject.toml`
  - already has `src/usage_limits/`
  - already has provider modules for `claude`, `codex`, `amp`, `openrouter`, `qwen`, `ollama`
  - already has shared base/table abstractions and test coverage
- `usage-limits/`
  - older parallel implementation
  - still contains the fuller operational docs
  - still contains `antigravity_usage.py`, which has not yet been ported into the packaged project
  - is still the path used by `home-justfile`

### Architectural problems

- There are two implementations of the same concept in one repo.
- The packaged version is the right shape for extraction, but it is still feature-incomplete relative to the legacy tree.
- The public CLI is fragmented into provider-specific entrypoints such as `usage-claude`, not a single canonical machine-consumable CLI.
- The JSON surface is provider-local and command-local, not a single documented contract for downstream consumers.
- Provider extensibility exists only by editing the package directly. There is no registry or plugin discovery boundary yet.

## Target Repo

Repo name: `usage-limits`

The extracted repo should be a standalone Python project with this shape:

```text
usage-limits/
├── README.md
├── pyproject.toml
├── src/
│   └── usage_limits/
│       ├── __init__.py
│       ├── base.py
│       ├── cli.py
│       ├── contracts.py
│       ├── registry.py
│       ├── rendering.py
│       ├── providers/
│       │   ├── __init__.py
│       │   ├── amp.py
│       │   ├── antigravity.py
│       │   ├── claude.py
│       │   ├── codex.py
│       │   ├── ollama.py
│       │   ├── openrouter.py
│       │   └── qwen.py
│       └── py.typed
└── tests/
```

## Design Direction

### Canonical public surfaces

There should be one primary CLI:

- `usage-limits providers list`
- `usage-limits collect --provider claude --json`
- `usage-limits collect --all --json`
- `usage-limits availability --provider claude --json`
- `usage-limits availability --all --json`
- `usage-limits table --provider claude`
- `usage-limits table --all`

Provider-specific aliases such as `usage-claude` can exist as thin compatibility entrypoints, but they should be secondary.

There should also be one canonical Python surface:

```python
from usage_limits import collect_provider, collect_all, list_providers
```

### Uniform JSON contract

Downstream programs need one stable JSON schema independent of provider.

Recommended top-level payload for `collect --json`:

```json
{
  "version": "1",
  "captured_at": "2026-03-10T12:00:00Z",
  "providers": [
    {
      "provider": "claude",
      "display_name": "Claude Code",
      "status": "ok",
      "rows": [
        {
          "identifier": "Claude (5h)",
          "pct_used": 42.0,
          "reset_at": "2026-03-10T15:30:00Z",
          "is_exhausted": false,
          "time_until_reset": "in 3h 30m"
        }
      ],
      "availability": [
        {
          "name": "Claude",
          "available_now": true,
          "available_when": null
        }
      ],
      "metadata": {},
      "errors": []
    }
  ]
}
```

Recommended payload for a provider failure:

```json
{
  "provider": "openrouter",
  "display_name": "OpenRouter",
  "status": "error",
  "rows": [],
  "availability": [],
  "metadata": {},
  "errors": [
    {
      "type": "not_implemented",
      "message": "Request counting is not yet implemented."
    }
  ]
}
```

This contract lets other tools consume:

- current exhaustion state
- next-available times
- provider-specific notes or metadata
- partial success across multiple providers

without scraping Rich output or provider-specific JSON.

### Provider extensibility

Use provider submodules plus a registry boundary.

Core pattern:

- `UsageProvider` remains the strategy interface
- `registry.py` maps provider slugs to provider classes
- `providers/__init__.py` exposes first-party providers
- future external providers are discovered through Python entry points, not git submodules

Recommended entry point group:

- `usage_limits.providers`

That allows a future external package such as `usage-limits-perplexity` to register itself without editing core.

This is the right extensibility model for `uvx`. Literal git submodules would be the wrong abstraction because they complicate installation, publication, and dependency resolution.

### Provider contract

The current base class is close, but the extracted repo should formalize a provider result model instead of having the CLI infer shape ad hoc.

Recommended direction:

- `ProviderSnapshot`
- `ProviderAvailability`
- `ProviderError`

Each provider should return a typed snapshot object, not raw dicts plus side-effect printing.

Provider responsibilities:

- authenticate or discover local auth state
- fetch raw usage data
- normalize into `UsageRow`
- produce availability information
- describe whether anchoring applies
- emit metadata that is useful but not table-shaped

Core responsibilities:

- CLI parsing
- registry lookup
- JSON serialization
- Rich rendering
- notification scheduling
- multi-provider orchestration

## Refactor Phases

### Phase 1: Choose the seed and freeze the legacy tree

- declare `scripts/usage_limits` the source of truth
- mark top-level `usage-limits/` as migration-only
- stop adding new features to the legacy tree

Exit criterion:

- all new work happens in the packaged project

### Phase 2: Reach feature parity inside the packaged project

- port `antigravity_usage.py` into `src/usage_limits/providers/antigravity.py`
- port any missing docs or operational notes that still exist only in `usage-limits/README.md` and `usage-limits/AGENTS.md`
- make `scripts/usage_limits/justfile` consistent with actual scripts and provider modules

Exit criterion:

- the packaged project fully replaces the top-level tree operationally

### Phase 3: Introduce registry and canonical contracts

- add `contracts.py` for typed JSON payloads
- add `registry.py` for provider registration and lookup
- add aggregate collection helpers for one or all providers
- move provider entrypoints to thin wrappers around the shared registry flow

Exit criterion:

- provider execution no longer lives in six separate hand-built CLIs

### Phase 4: Build the uniform CLI

- add `usage-limits` as the primary script
- support `providers list`, `collect`, `availability`, and `table`
- keep provider-specific aliases only as wrappers
- document `uvx --from git+https://github.com/... usage-limits collect --all --json`

Exit criterion:

- downstream users can stop shelling into individual provider scripts

### Phase 5: Split to a new repo

- create the new repo from the packaged project, not from `usage-limits/`
- preserve git history if practical
- add CI for `pytest`, `ruff`, and live-provider checks that are safe to run in CI or can be opt-in
- publish the repo publicly

Exit criterion:

- the project installs and runs independently of `~/ai`

### Phase 6: Migrate consumers

Current visible consumer:

- `home-justfile` still shells into top-level `usage-limits/*.py`

Migration target:

- `home-justfile` should call `uvx usage-limits collect --all --json` or `uvx usage-limits table --all`
- any future repo consumers should depend on the uniform JSON CLI or import the library directly

Exit criterion:

- no operational path depends on `~/ai/usage-limits`

### Phase 7: Remove the legacy tree from `~/ai`

- archive or delete top-level `usage-limits/`
- keep only a short pointer note if needed during transition

Exit criterion:

- there is only one implementation left in `~/ai`, or ideally none because the code has moved out

## CLI Recommendation

Use Typer for the primary CLI.

Reasons:

- consistent with the current Python CLI direction in this workspace
- good subcommand ergonomics
- straightforward JSON file/stdin options
- easy to expose a single canonical `usage-limits` command plus thin aliases

## Testing Strategy

### Contract tests

- JSON serialization for single-provider and multi-provider collection
- registry lookup and provider discovery
- provider error normalization

### Table/render tests

- keep the current `UsageTable` tests
- add tests for aggregate multi-provider display ordering

### Provider tests

- deterministic unit tests for provider normalization logic
- live tests only where real data can be queried reliably
- fixture-based tests for HTML/CLI parsing

### Consumer-proof tests

- one `uvx --from ... usage-limits collect --all --json` smoke test
- one import-level test for the public Python API

## Migration Rules

- do not carry forward the top-level legacy JSON or script names as if they were public contracts
- treat the extracted package as a new public API
- preserve only behavior that is genuinely worth keeping
- write docs against the new canonical CLI first

## Immediate Next Actions

- port `antigravity` into `scripts/usage_limits`
- add `contracts.py` and `registry.py`
- add the aggregate `usage-limits` CLI
- switch `home-justfile` to the packaged project instead of the legacy tree
- only then split the package into its own repo
