# Plugin Utilities Consolidation Plan

## Problem

LLM calling, provider dispatch, structured output, API key management, prompt templates,
and classification rubrics are currently scattered across Python scripts and TypeScript
plugins with no shared canonical implementation:

**Python (`scripts/run_agent.py`)**

- `litellm`-based provider registry with models.dev validation
- Jinja2 template parsing and rendering
- Provider slug convention: `provider_name/model_id` (e.g. `groq/llama-3.3-70b`)
- No structured output, no retries, plain text completion only

**TypeScript (`dev/prompt-router/index.ts`, `tests/classifier/run.ts`)**

- `@instructor-ai/instructor` + raw `openai` SDK for structured output
- Provider dispatch duplicated inline — both files call `endpointFor()` then rebuild
  `new OpenAI + Instructor` independently
- `ClassificationSchema` (zod) defined twice; `classify()` logic defined twice
- `CLASSIFIER_MODELS` list and fallback loop exist only in `prompt-router/index.ts`
- Retry logic (`max_retries: 3`) hardcoded at each call site

**Templates and rubrics**

- `tests/classifier/playbook.md` — classifier system prompt (9,920 bytes)
- `tiers/*.md` — per-tier injection text (6 files)
- `tests/classifier/cases.yaml` — 30+ labeled test cases
- All loaded via `Bun.file()` relative paths inside the plugin — not importable
  from anywhere else, not callable from Python

**Installed Python packages** (confirmed): `litellm 1.82`, `pydantic 2.12`,
`openai 2.24`, `groq 1.0`, `jinja2 3.1`. `pydantic-ai` is **not** installed.

---

## Architecture

### Single source of truth: `scripts/llm.py`

A standalone Python module (not a CLI) that:

1. Owns the **provider registry** — one table of providers with env var, litellm prefix,
   baseURL, drop_params, and models.dev slug. This is the only place provider metadata lives.
2. Exposes **`call_llm()`** — takes model slug, messages, optional zod-equivalent pydantic
   schema, temperature, max_tokens. Handles retries internally. Returns structured output
   or plain text.
3. Exposes **`call_with_fallback()`** — takes an ordered list of model slugs and tries
   each in sequence. First success wins.
4. Owns **structured output** via `instructor` (already installed as a litellm dep) or
   via litellm's native `response_format` — to be determined by compatibility testing.
5. Is called from TypeScript plugins via **subprocess** (`Bun.spawn` / `child_process`)
   with JSON-encoded input on stdin and JSON-encoded output on stdout. No HTTP server
   needed; subprocess is simpler and avoids port management.

> **Why not pydantic-ai?** It is not installed, and installing it pulls in a large
> dependency tree. `litellm` + `instructor` (already present transitively via litellm)
> or litellm's built-in `response_format` achieves the same goal. If pydantic-ai is
> installed separately later, `llm.py` can adopt it internally without changing the
> TS→Python calling contract.

### Template and rubric registry: `scripts/templates/`

All prompt templates, system prompts, and rubrics live here as flat files:

- `scripts/templates/classifier/playbook.md` — canonical classifier system prompt
- `scripts/templates/classifier/cases.yaml` — canonical test cases
- `scripts/templates/tiers/A.md`, `B.md`, `C.md`, `knowledge.md`, `model-self.md`, `S.md`

The plugin reads these via `llm.py` (which knows the canonical path), not via
`Bun.file(new URL(...))`. This decouples the template content from the plugin's
install location.

### TypeScript calling convention

Plugins call `llm.py` via a thin TS wrapper `utilities/shared/llm.ts` that:

- Spawns `python3 scripts/llm.py` with JSON on stdin
- Returns a typed Promise wrapping the JSON response
- Handles spawn errors and non-zero exits

This means all retry logic, fallback ordering, provider resolution, and structured output
enforcement happen in Python. TypeScript plugins are just callers.

### Provider registry parity

The TS `utilities/shared/providers.ts` (used for `endpointFor()`) is **kept** for cases
where a TS plugin needs to construct its own OpenAI client directly (e.g. streaming,
non-classification calls). But `providers.ts` is updated to match `llm.py`'s registry
exactly — same slugs, same env vars, same baseURLs — and `llm.py` is the canonical
source; `providers.ts` is generated or manually kept in sync.

---

## Completed

- **Python environment**: `pyproject.toml` at repo root, `.venv` via `uv sync`,
  `.envrc` activating the venv, `justfile` updated to use `.venv/bin/python`.
  `pydantic-ai`, `litellm`, `rich`, `jinja2`, `pyyaml`, `httpx`, `jsonschema` all
  installed and importable.

- **`scripts/llm.py`** (Task 1): Full provider registry, `call_llm()`,
  `call_with_fallback()`, schema registry (`Classification`), `load_template()`,
  stdin/stdout CLI. Uses native `GroqModel`/`GroqProvider` to avoid OpenAI SDK
  `service_tier` validation issues on Groq responses. `OpenRouterProvider` used
  for openrouter slugs. Generic `OpenAIProvider` for nvidia/ollama.

- **`scripts/templates/`** (Task 2): All prompt templates and rubrics moved here.
  - `classifier/playbook.md` — canonical classifier system prompt
  - `classifier/cases.yaml` — labeled test cases
  - `tiers/{A,B,C,knowledge,model-self,S}.md` — per-tier injection text

- **`utilities/shared/llm.ts`** (Task 3): Thin Bun subprocess wrapper. Spawns
  `scripts/llm.py`, serialises JSON request on stdin, returns parsed response.
  Exports `callLLM<T>()` and `loadTemplate()`. Path resolution is relative to the
  file's own location — no hardcoded absolute paths.

- **`dev/prompt-router/index.ts`** (Task 4): Removed `@instructor-ai/instructor`,
  `openai`, `zod`, and inline provider logic. Now imports `callLLM`/`loadTemplate`
  from `utilities/shared/llm`. `CLASSIFIER_MODELS` is now a plain `string[]`.
  Tier instructions and system prompt loaded via `loadTemplate()`.

- **`tests/classifier/run.ts`** (Task 5): Removed `@instructor-ai/instructor`,
  `openai`, `zod`, `endpointFor`, and inline `classify()` loop. Now uses `callLLM`
  and `loadTemplate`. `--mode` flag removed (mode is now handled by `llm.py` per
  provider). Template files loaded from canonical `scripts/templates/` via Python.

- **`scripts/test_llm_compat.py`** (Task 7): Smoke test — calls each provider with
  a fixed prompt, verifies `Classification` parses correctly. Live results:
  groq ✓, nvidia ✓, openrouter ✓, ollama ✗ (llama3.2 not installed locally).

---

## Tasks (ordered)

### Task 0 — Prerequisites ✓

- `pydantic-ai` installed in `.venv` — confirmed importable.
- Verify litellm structured output (`response_format`) works on groq/nvidia before
  committing to it vs. pydantic-ai's native model calling.

### Task 1 — `scripts/llm.py` — core module ✓

**File**: `scripts/llm.py`

Key elements:

```python
# Provider registry — single source of truth
PROVIDERS: dict[str, ProviderConfig] = {
    "groq": ProviderConfig(env_var="GROQ_API_KEY", litellm_prefix="groq", ...),
    "nvidia": ProviderConfig(env_var="NVIDIA_API_KEY", litellm_prefix="nvidia_nim",
                             base_url="https://integrate.api.nvidia.com/v1", ...),
    "openrouter": ProviderConfig(env_var="OPENROUTER_API_KEY", litellm_prefix="openrouter", ...),
    "ollama": ProviderConfig(env_var=None, litellm_prefix="ollama",
                             base_url="http://localhost:11434", ...),
}

# Structured output schema (pydantic BaseModel subclass)
# call_llm() accepts schema: type[BaseModel] | None
# If schema given: uses litellm response_format or instructor for structured output
# If no schema: plain text completion

def call_llm(
    model: str,              # "groq/llama-3.3-70b-versatile"
    messages: list[dict],
    schema: type[BaseModel] | None = None,
    temperature: float = 0.0,
    max_tokens: int = 500,
    max_retries: int = 3,
) -> BaseModel | str: ...

def call_with_fallback(
    models: list[str],       # tried in order; first success wins
    messages: list[dict],
    schema: type[BaseModel] | None = None,
    **kwargs,
) -> BaseModel | str: ...
```

**CLI interface** (for subprocess calling from TS):

```
stdin:  JSON { models, messages, schema_name, temperature, max_tokens }
stdout: JSON { ok: true, result: {...} } | { ok: false, error: "..." }
```

Schema registry maps `schema_name` strings to pydantic `BaseModel` subclasses defined
in the module. Adding a new schema = adding a class + registering its name.

### Task 2 — Template registry: `scripts/templates/` ✓

Move (not copy) template files from their current plugin-local locations:

```
dev/prompt-router/tests/classifier/playbook.md
  → scripts/templates/classifier/playbook.md

dev/prompt-router/tests/classifier/cases.yaml
  → scripts/templates/classifier/cases.yaml

dev/prompt-router/tiers/{A,B,C,knowledge,model-self,S}.md
  → scripts/templates/tiers/{A,B,C,knowledge,model-self,S}.md
```

`llm.py` resolves template paths relative to its own `__file__` — no hardcoded paths.

The plugin (`prompt-router/index.ts`) currently loads `tiers/*.md` and `playbook.md`
via `Bun.file(new URL(...))`. After this task it calls `llm.py` with `schema_name:
"Classification"` and `template: "classifier/playbook"` instead, removing all file I/O
from the plugin.

### Task 3 — `utilities/shared/llm.ts` — TS subprocess wrapper ✓

```typescript
// utilities/shared/llm.ts
export interface LLMRequest {
  models: string[];            // ordered fallback list
  messages: { role: string; content: string }[];
  schema_name?: string;        // registered schema in llm.py
  temperature?: number;
  max_tokens?: number;
}

export interface LLMResponse<T = unknown> {
  ok: true;
  result: T;
} | {
  ok: false;
  error: string;
}

export async function callLLM<T = string>(req: LLMRequest): Promise<T>
```

Spawns `python3 <abs-path-to-scripts/llm.py>` with `req` on stdin. Returns parsed
result or throws on `ok: false`. Path to `llm.py` is resolved relative to this file's
location — no hardcoded absolute paths.

### Task 4 — Refactor `prompt-router/index.ts` ✓

Replace the inline `new OpenAI + Instructor + create()` classification loop with:

```typescript
import { callLLM } from "../../utilities/shared/llm";
// ...
const result = await callLLM<{ tier: Tier; reasoning: string }>({
  models: CLASSIFIER_MODELS,
  messages: [...],
  schema_name: "Classification",
  temperature: 0,
  max_tokens: 200,
});
```

`CLASSIFIER_MODELS` becomes a plain `string[]` (no more `ModelConfig` with `mode` and
`maxTokens` — those are now `llm.py`'s concern per provider).

Tier instructions are no longer loaded from `Bun.file()` — they are returned by
`llm.py` via a `get_template("tiers/A")` call, or the plugin fetches them once at
startup via a separate `callLLM` request with `action: "load_template"`.

### Task 5 — Refactor `tests/classifier/run.ts` ✓

Replace the inline classify function with a call to `callLLM()`. The test harness
becomes:

```
for each case → callLLM({ models: [model], schema_name: "Classification", ... })
```

The `ClassificationSchema` zod definition in `run.ts` is deleted; ground truth is the
pydantic schema in `llm.py`.

### Task 6 — Update `scripts/run_agent.py`

`run_agent.py` already has a solid provider registry and template system. Refactor it
to import from `llm.py` instead of reimplementing provider dispatch. The CLI interface
stays the same; only the internals change to use `call_llm()`.

### Task 7 — Compatibility smoke tests ✓

Script: `scripts/test_llm_compat.py`

For each provider with a set API key:

- Call `call_llm()` with `schema_name: "Classification"` on a fixed test prompt
- Verify response parses as `Classification`
- Record pass/fail per model

This replaces the need to run the full classifier evaluation harness to verify a new
model works. Run it after any change to `llm.py`.

### Task 8 — Update `utilities/shared/providers.ts`

Ensure the TS provider table matches `llm.py`'s PROVIDERS registry:

- Same slugs (groq/, nvidia/, ollama/, no-prefix = openrouter)
- Same env var names
- Same baseURLs

Add a comment noting `llm.py` is the canonical source.

---

## Out of scope (for now)

- Installing pydantic-ai (evaluate after litellm structured output compatibility is confirmed)
- Migrating run_agent.py's Jinja2 template system to the new templates/ directory
  (run_agent.py templates are user-facing agent templates, not classification rubrics)
- HTTP server or RPC layer between Python and TypeScript (subprocess is sufficient)
- Harness decomposition (session-harness.ts splitting) — separate concern, separate plan

---

## Order

```
0 (prereqs) → 1 (llm.py) → 2 (templates/) → 3 (llm.ts) → 4 (prompt-router refactor)
                                                          → 5 (classifier test refactor)
                          → 6 (run_agent.py update)
1 → 7 (smoke tests, can run in parallel with 3–5)
1 → 8 (providers.ts sync, can happen any time after 1)
```

Tasks 4 and 5 are blocked on 3. Task 6 is blocked on 1. Task 7 is independent of 3–6.
