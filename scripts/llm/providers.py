"""
Provider registry — single source of truth for all LLM providers.

Merges the provider tables from scripts/run_micro_agent.py (models.dev-backed, 7 providers)
and opencode/scripts/llm.py (pydantic-ai native, 4 providers) into one canonical dict.

Slug convention (used everywhere: Python, TypeScript, justfile):
    groq/          → Groq
    openrouter/    → OpenRouter  (no prefix also accepted for backward compat)
    nvidia/        → NVIDIA NIM
    mistral/       → Mistral
    replicate/     → Replicate
    cloudflare/    → Cloudflare Workers AI
    ollama/        → Local Ollama  (no auth)
    ollama-cloud/  → Ollama Cloud

output_mode controls how pydantic-ai requests structured output:
    "tool"      — OpenAI tool-calling (not supported by all providers)
    "prompted"  — JSON instruction injected into system prompt (universal fallback)

CLI:
    python -m scripts.llm.providers              # list all providers
    python -m scripts.llm.providers <provider>   # list models for provider
"""

from __future__ import annotations

import httpx
import logging
import os
from typing import Optional

from pydantic import BaseModel
from pydantic_ai.models.groq import GroqModel
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.profiles.openai import OpenAIModelProfile
from pydantic_ai.providers.groq import GroqProvider
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.providers.openrouter import OpenRouterProvider

from scripts.llm.models_dev import fetcher as _models_dev

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Provider config models
# ---------------------------------------------------------------------------


class ProviderConfig(BaseModel):
    env_var: Optional[str]  # None = no auth required (ollama)
    base_url: str
    output_mode: str = "prompted"  # "tool" | "prompted"
    litellm_prefix: str = ""  # for plain-text litellm calls in run_micro_agent.py
    models_dev_slug: Optional[str] = None  # if set, get_models() queries models.dev
    drop_params: bool = False  # litellm: drop unsupported params

    def get_models(self) -> list[str]:
        """Return available model IDs for this provider."""
        if self.models_dev_slug:
            return _models_dev.get_models(self.models_dev_slug)
        return []


class ReplicateProviderConfig(ProviderConfig):
    """Replicate: fetches models from Replicate REST API, not models.dev."""

    env_var: Optional[str] = "REPLICATE_API_TOKEN"
    base_url: str = ""
    litellm_prefix: str = "replicate"

    def get_models(self) -> list[str]:
        env_var = self.env_var or "REPLICATE_API_TOKEN"
        api_key = os.environ.get(env_var, "")
        if not api_key:
            logger.warning("REPLICATE_API_TOKEN not set, skipping model fetch")
            return []
        try:
            resp = httpx.get(
                "https://api.replicate.com/v1/models",
                headers={"Authorization": f"Token {api_key}"},
                timeout=5.0,
            )
            resp.raise_for_status()
            data = resp.json()
            models = [f"{r['owner']}/{r['name']}" for r in data.get("results", [])]
            logger.info("Fetched %d models from Replicate API", len(models))
            return models
        except httpx.HTTPStatusError as exc:
            logger.error(
                "Replicate API %d: %s",
                exc.response.status_code,
                exc.response.text[:200],
            )
            return []
        except httpx.TimeoutException:
            logger.error("Replicate API request timed out")
            return []
        except Exception as exc:
            logger.error("Failed to fetch Replicate models: %s", exc)
            return []


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

PROVIDERS: dict[str, ProviderConfig] = {
    "groq": ProviderConfig(
        env_var="GROQ_API_KEY",
        base_url="https://api.groq.com/openai/v1",
        output_mode="prompted",  # groq rejects tool-calling for structured output
        litellm_prefix="groq",
        models_dev_slug="groq",
    ),
    "openrouter": ProviderConfig(
        env_var="OPENROUTER_API_KEY",
        base_url="https://openrouter.ai/api/v1",
        output_mode="prompted",  # provider mix; prompted is universally safe
        litellm_prefix="openrouter",
        models_dev_slug="openrouter",
    ),
    "nvidia": ProviderConfig(
        env_var="NVIDIA_API_KEY",
        base_url="https://integrate.api.nvidia.com/v1",
        output_mode="prompted",  # mistral models on NIM reject tool-calling
        litellm_prefix="nvidia_nim",
        models_dev_slug="nvidia",
    ),
    "mistral": ProviderConfig(
        env_var="MISTRAL_API_KEY",
        base_url="https://api.mistral.ai/v1",
        output_mode="tool",
        litellm_prefix="mistral",
        models_dev_slug="mistral",
    ),
    "replicate": ReplicateProviderConfig(),
    "cloudflare": ProviderConfig(
        env_var="CLOUDFLARE_API_KEY",
        base_url="https://api.cloudflare.com/client/v4/ai",
        output_mode="prompted",
        litellm_prefix="cloudflare",
        models_dev_slug="cloudflare-workers-ai",
        drop_params=True,
    ),
    "ollama": ProviderConfig(
        env_var=None,
        base_url="http://localhost:11434/v1",
        output_mode="prompted",
        litellm_prefix="ollama",
    ),
    "ollama-cloud": ProviderConfig(
        env_var="OLLAMA_API_KEY",
        base_url="https://ollama.com",
        output_mode="prompted",
        litellm_prefix="ollama",
        models_dev_slug="ollama-cloud",
    ),
}


# ---------------------------------------------------------------------------
# Resolution helpers
# ---------------------------------------------------------------------------


def resolve(slug: str) -> tuple[ProviderConfig, str]:
    """Split 'groq/llama-3.3-70b' → (ProviderConfig, 'llama-3.3-70b').

    Slugs with no registered prefix route to OpenRouter unchanged.
    Accepts 'openrouter/...' prefix as well as bare slugs for backward compat.
    """
    for prefix, cfg in PROVIDERS.items():
        if prefix == "openrouter":
            continue
        if slug.startswith(f"{prefix}/"):
            return cfg, slug[len(prefix) + 1 :]
    # bare slug or openrouter/... prefix → OpenRouter
    if slug.startswith("openrouter/"):
        return PROVIDERS["openrouter"], slug[len("openrouter/") :]
    return PROVIDERS["openrouter"], slug


def api_key(cfg: ProviderConfig) -> str:
    if cfg.env_var is None:
        return "ollama"
    return os.environ.get(cfg.env_var) or ""


def make_model(
    cfg: ProviderConfig, model_id: str, slug: str
) -> GroqModel | OpenAIChatModel:
    """Build the pydantic-ai model object for a provider+model.

    Uses native GroqModel for groq/ slugs to avoid OpenAI SDK response-validation
    issues (e.g. service_tier literal mismatch on Groq responses). Uses native
    OpenRouterProvider for openrouter slugs. Falls back to generic OpenAIProvider
    for all others (nvidia, ollama, mistral, etc.).
    """
    key = api_key(cfg)
    profile = OpenAIModelProfile(
        default_structured_output_mode=cfg.output_mode,  # type: ignore[arg-type]
    )
    if slug.startswith("groq/"):
        return GroqModel(model_id, provider=GroqProvider(api_key=key))
    if cfg.base_url == "https://openrouter.ai/api/v1" or slug.startswith("openrouter/"):
        provider = OpenRouterProvider(api_key=key)
        return OpenAIChatModel(model_id, provider=provider, profile=profile)
    provider = OpenAIProvider(base_url=cfg.base_url, api_key=key)
    return OpenAIChatModel(model_id, provider=provider, profile=profile)


def list_models(provider: str | None = None) -> list[str]:
    """Return all available model slugs, optionally filtered to one provider.

    Each slug is in 'provider/model' form. Providers with no model list
    (e.g. bare ollama) return an empty contribution.
    """
    if provider is not None:
        cfg = PROVIDERS.get(provider)
        if cfg is None:
            raise ValueError(f"Unknown provider {provider!r}. Known: {list(PROVIDERS)}")
        return [f"{provider}/{m}" for m in cfg.get_models()]
    return [f"{name}/{m}" for name, cfg in PROVIDERS.items() for m in cfg.get_models()]


def validate(slug: str) -> None:
    """Validate a model slug: provider registered, API key set, model known.

    Raises ValueError with a descriptive message on failure.
    Skips model list validation if the provider has no list.
    """
    if "/" not in slug:
        raise ValueError(f"Invalid model format {slug!r}. Expected: provider/model")
    provider_prefix = slug.split("/", 1)[0]
    if provider_prefix not in PROVIDERS:
        raise ValueError(
            f"Unsupported provider {provider_prefix!r}. "
            f"Supported: {', '.join(PROVIDERS)}"
        )
    cfg = PROVIDERS[provider_prefix]
    key = api_key(cfg)
    if not key and cfg.env_var is not None:
        raise ValueError(f"{cfg.env_var} not set (required for {slug})")
    available = cfg.get_models()
    if not available:
        logger.warning(
            "Skipping model validation for %s (no model list available)",
            provider_prefix,
        )
        return
    model_id = slug.split("/", 1)[1]
    if model_id not in available:
        sample = available[:20]
        lines = "\n  ".join(f"{provider_prefix}/{m}" for m in sample)
        extra = f"\n  ... and {len(available) - 20} more" if len(available) > 20 else ""
        raise ValueError(f"Model {slug!r} not found. Available:\n  {lines}{extra}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 1:
        for slug in list_models():
            print(slug)
    elif len(sys.argv) == 2:
        try:
            for slug in list_models(sys.argv[1]):
                print(slug)
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            sys.exit(1)
    else:
        print("Usage: python -m scripts.llm.providers [<provider>]", file=sys.stderr)
        sys.exit(1)
