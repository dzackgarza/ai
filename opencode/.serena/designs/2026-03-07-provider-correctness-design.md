# Provider Correctness & All-7-Providers Smoke Test

## Problem

After the litellm→pydantic-ai migration, several providers are silently broken:

1. **groq**: hello_world.md uses `groq/meta-llama/llama-3.3-70b-versatile` — the `meta-llama/` vendor prefix is a Groq API convention, not a models.dev convention. models.dev groq slug returns bare IDs like `llama-3.3-70b-versatile`. The template must use the bare ID.

2. **nvidia**:
   - `env_var` is `NVIDIA_API_KEY` in current code but original used `NVIDIA_NIM_API_KEY` (both are set in env). Should canonicalize to `NVIDIA_NIM_API_KEY` to match original.
   - `get_models()` uses models.dev `nvidia` slug which returns IDs like `nvidia/llama-3.1-nemotron-70b-instruct`. These are NIM Pro-tier models that 404 on free accounts. NIM API (`/v1/models`) serves 187 models with vendor-prefixed IDs like `meta/llama-3.3-70b-instruct`. Must fetch live from NIM API.

3. **cloudflare**:
   - `base_url` is `https://api.cloudflare.com/client/v4/ai` — wrong. The OpenAI-compatible endpoint is `https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/ai/v1`.
   - Must read `CLOUDFLARE_ACCOUNT_ID` from env to construct the URL at runtime.
   - `get_models()` uses models.dev which returns text + embedding + image models. Need to filter to text/chat models only.

4. **ollama-cloud**:
   - `base_url` is `https://ollama.com` — missing `/v1` suffix. Should be `https://ollama.com/v1`.
   - Hit weekly rate limit in testing; functional once URL is fixed.

5. **ollama (local)**:
   - Current code has `env_var=None` and no `get_models()`. Local models include bare names like `qwen3:4b` AND cloud variants like `kimi-k2-thinking:cloud`. Only `:cloud` suffix variants should be returned by `get_models()` to avoid CPU-intensive local inference.
   - Fetch from `http://localhost:11434/api/tags`, filter to `name.endswith(':cloud')`.

6. **openrouter**:
   - `get_models()` uses models.dev openrouter slug → 189 models, all tiers. Must filter to `:free` suffix only (54 free models confirmed).

7. **replicate**: untested — structural code looks correct (live API fetch). No change needed pending smoke test.

8. **mistral**: working ✓ (confirmed)

9. **groq**: working ✓ once template is fixed to bare model ID

## Approach

All fixes are confined to:

- `scripts/llm/providers.py` — provider registry, URL construction, model list filtering
- `scripts/llm/templates.py` — inline dict schema support
- `scripts/llm/schemas.py` — inline dict → pydantic model generation
- `prompts/micro_agents/hello_world.md` — model slug fix

No changes to `call.py`, `__init__.py`, `run_micro_agent.py`, `models_dev.py`.

## Components

### NvidiaProviderConfig (new subclass)

```python
class NvidiaProviderConfig(ProviderConfig):
    def get_models(self) -> list[str]:
        # Fetch from https://integrate.api.nvidia.com/v1/models
        # Return id field directly (already vendor-prefixed)
```

### CloudflareProviderConfig (new subclass)

```python
class CloudflareProviderConfig(ProviderConfig):
    account_id_env_var: str = "CLOUDFLARE_ACCOUNT_ID"

    @property
    def resolved_base_url(self) -> str:
        account_id = os.environ.get(self.account_id_env_var, "")
        return f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/v1"

    def get_models(self) -> list[str]:
        # models.dev cloudflare-workers-ai, filter to chat models
        # Heuristic: exclude embedding, reranker, whisper, bge models
```

### OllamaLocalProviderConfig (new subclass)

```python
class OllamaLocalProviderConfig(ProviderConfig):
    def get_models(self) -> list[str]:
        # GET http://localhost:11434/api/tags
        # Return only names ending with ':cloud'
```

### OpenRouterProviderConfig (new subclass or override)

Override `get_models()` to filter models.dev results to `:free` suffix.

### Inline dict schema in YAML frontmatter

```yaml
schema:
  label: str
  score: float
  reasoning: str
```

`MicroAgent.schema_class()` detects `schema` value is a dict → calls `schemas.make_schema_from_dict(name, d)` → dynamically creates a pydantic BaseModel subclass.

## make_model() change for Cloudflare

`make_model()` must call `cfg.resolved_base_url` (not `cfg.base_url`) for `CloudflareProviderConfig`. Cleanest: add `effective_base_url` property to `ProviderConfig` that subclasses can override; default returns `self.base_url`.

## Trade-offs

- NIM live fetch vs models.dev: live is necessary because models.dev `nvidia` slug returns Pro-tier models only. Accept the extra HTTP call.
- CF account_id in URL: unavoidable — CF's OpenAI-compat endpoint requires it. No alternative.
- Ollama :cloud filter: avoids accidentally hammering local CPU. Explicit and safe.
- OpenRouter :free filter: matches stated intent (free-tier models only for this workspace).

## Tasks (ordered)

1. Checkpoint current state
2. Fix `hello_world.md` model slug
3. Add `NvidiaProviderConfig`, `CloudflareProviderConfig`, `OllamaLocalProviderConfig`, `OpenRouterProviderConfig` subclasses to `providers.py`
4. Update PROVIDERS registry entries to use new subclasses; fix `ollama-cloud` base_url; fix `nvidia` env_var
5. Add `effective_base_url` property; update `make_model()` to use it
6. Add `make_schema_from_dict()` to `schemas.py`; update `MicroAgent.schema_class()` to detect dict schema
7. Smoke test all 7 providers (groq, openrouter, nvidia, mistral, replicate, cloudflare, ollama-cloud) against hello_world
