# scripts/llm/ — Canonical LLM Package

## Problem

LLM calling logic is split across two files in two different locations, neither of which
is the correct canonical home:

- `scripts/run_agent.py` (repo root `~/ai/scripts/`) — the actual entry point used in
  README and justfile. Has: full provider registry (7 providers), models.dev API
  integration, ReplicateProvider, Jinja2 template runner, argparse CLI. Missing:
  structured output, fallback, TS bridge.

- `opencode/scripts/llm.py` (wrong subtree) — created in a previous session with the
  right ideas but in the wrong place. Has: pydantic-ai structured output, fallback,
  TS subprocess bridge, schema registry, `load_template()`. Missing: models.dev
  discovery, Replicate, mistral, cloudflare providers.

Neither file imports from the other. `run_agent.py` was never refactored (Task 6 was
incorrectly closed as N/A because the agent searched the wrong directory).

## Approach

Merge both into a single **`scripts/llm/`** package at the repo root (`~/ai/scripts/llm/`).
`run_agent.py` becomes a thin wrapper over this package — its CLI surface and README
entry point stay exactly as-is. The TS bridge (`opencode/scripts/llm.py` acting as
subprocess target) becomes `scripts/llm/bridge.py` with a `__main__` entry.

### Why a package not a single file?

The two files together are ~680 lines covering distinct concerns. A package allows:

- Each module independently importable and testable
- Each module independently runnable as a CLI (`python -m scripts.llm.bridge`, etc.)
- Clean separation: providers / call logic / schemas / templates / CLI bridge

## Layout

```
scripts/
  llm/
    __init__.py        — public API: call_llm, call_with_fallback, load_template, SCHEMAS
    providers.py       — PROVIDERS registry + _resolve() + _api_key() + _make_model()
                         Merged from both files. All 8+ providers. models.dev-aware.
    models_dev.py      — ModelsDevFetcher (lifted from run_agent.py unchanged)
    call.py            — call_llm(), call_with_fallback() using pydantic-ai
                         CLI: python -m scripts.llm.call <model> <prompt>
    schemas.py         — pydantic BaseModel subclasses (Classification, etc.)
                         SCHEMAS registry dict
    templates.py       — load_template(), Jinja2 render_template()
                         Searches scripts/templates/ relative to package root
                         CLI: python -m scripts.llm.templates <name> [--var k=v ...]
    bridge.py          — stdin/stdout JSON dispatcher for TS subprocess callers
                         CLI: python -m scripts.llm.bridge (reads JSON from stdin)
  run_agent.py         — thin wrapper: parse_template() + build_variables() + main()
                         delegates get_completion() → call.call_llm()
                         delegates template rendering → templates.render_template()
                         delegates provider init/validation → providers module
  templates/           — canonical template files (moved from opencode/scripts/templates/)
    classifier/
      playbook.md
      cases.yaml
    tiers/
      A.md  B.md  C.md  knowledge.md  model-self.md  S.md

opencode/scripts/
  llm.py               — DELETED (replaced by scripts/llm/)
  test_llm_compat.py   — updated: import from scripts.llm instead
  templates/           — DELETED (moved to scripts/templates/)
```

## Provider Registry (merged)

From `run_agent.py` (via models.dev): groq, openrouter, mistral, replicate, cloudflare-workers-ai, ollama-cloud, nvidia  
From `llm.py` (hardcoded): groq, nvidia, ollama (local), openrouter

Merged result — `providers.py`:

- groq, openrouter, mistral, nvidia: ModelsDevProvider (env var + models.dev slug)
- replicate: ReplicateProvider (Replicate API)
- cloudflare-workers-ai: ModelsDevProvider (drop_params=True)
- ollama: local Ollama (no auth, base_url http://localhost:11434/v1)
- ollama-cloud: ModelsDevProvider (Ollama cloud API)

Each entry also carries `base_url` and `output_mode` ("tool" | "prompted") for
pydantic-ai model construction. `_make_model()` stays in providers.py and is called
by call.py.

## TS Bridge Contract (unchanged)

`bridge.py` keeps the same stdin/stdout JSON protocol already consumed by
`opencode/plugins/utilities/shared/llm.ts`. Only the path to invoke changes:

Before: `python opencode/scripts/llm.py`  
After: `python -m scripts.llm.bridge` (or `python scripts/llm/bridge.py`)

`llm.ts` path resolution updated accordingly.

## Jinja2 / YAML frontmatter (run_agent.py surface)

`run_agent.py`'s `parse_template()`, `build_variables()`, and `main()` stay in
`run_agent.py`. The Jinja2 render and `get_completion()` calls are delegated to
`scripts.llm.templates` and `scripts.llm.call` respectively.

`templates.py` also exposes a CLI:

```
python -m scripts.llm.templates classifier/playbook --var tier=A
```

This makes template rendering available to both Python scripts and TS subprocess callers.

## PYTHONPATH

The `scripts/llm/` package is at `~/ai/scripts/llm/`. To import it as `scripts.llm`,
callers must have `~/ai` on PYTHONPATH, or use `python -m scripts.llm.bridge` run from
`~/ai`. The `opencode/justfile` already uses `.venv/bin/python` — adding a
`PYTHONPATH = repo_root` variable there is sufficient. The root `justfile` already has
`repo := ...` defined.

## Trade-offs

- **pydantic-ai over litellm** for structured output: pydantic-ai's native provider
  classes avoid schema mismatches (e.g. Groq `service_tier`). litellm is still used
  for plain-text calls in run_agent.py (no behavior change there).
- **No HTTP server**: subprocess/stdin-stdout is sufficient and avoids port management.
- **models.dev stays async-lazy**: ModelsDevFetcher fetches only when `get_models()` is
  called, same as today. Not called during structured output path (pydantic-ai).

## Tasks

1. Checkpoint current state
2. Create `scripts/llm/` package: providers.py, models_dev.py, call.py, schemas.py, templates.py, bridge.py, **init**.py
3. Move `opencode/scripts/templates/` → `scripts/templates/`
4. Thin-wrap `scripts/run_agent.py` to delegate to package
5. Delete `opencode/scripts/llm.py` (replaced)
6. Update `opencode/scripts/test_llm_compat.py` imports
7. Update `opencode/plugins/utilities/shared/llm.ts` path
8. Update `opencode/justfile` PYTHONPATH if needed
9. Smoke-test: `python scripts/run_agent.py --help` and `python -m scripts.llm.bridge`
