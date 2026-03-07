"""
Provider registry — single source of truth for all LLM providers.

Supported providers (user-facing slugs):
    groq/          → Groq (live /v1/models, chat models only)
    openrouter/    → OpenRouter (live /v1/models, :free-tier models only)
    nvidia/        → NVIDIA NIM (live /v1/models, vendor-prefixed IDs)
    mistral/       → Mistral (live /v1/models, completion_chat capable only)
    cloudflare/    → Cloudflare Workers AI (live models/search API, Text Generation only)
    ollama-cloud/  → Ollama Cloud (live /v1/models)
    ollama/        → Local Ollama (http://localhost:11434/v1, :cloud suffix only)

NOT supported:
    replicate/     → Replicate does NOT offer an OpenAI-compatible chat completions
                     endpoint. Its API uses predictions/{owner}/{name} format.
                     Removed from the registry. Use openrouter or nvidia for hosted
                     models with OpenAI-compat.

output_mode controls how pydantic-ai requests structured output:
    "tool"      — OpenAI tool-calling
    "prompted"  — JSON instruction injected into system prompt (safe universal fallback)

All unknown providers and models are hard errors — no silent fallbacks.

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


logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Provider config models
# ---------------------------------------------------------------------------


class ProviderConfig(BaseModel):
    env_var: Optional[str]  # None = no auth required (local ollama)
    base_url: str
    output_mode: str = "prompted"  # "tool" | "prompted"
    drop_params: bool = False  # litellm compat, kept for reference

    @property
    def effective_base_url(self) -> str:
        """Base URL to pass to pydantic-ai. Override in subclasses for dynamic URLs."""
        return self.base_url

    def get_models(self) -> list[str]:
        """Return available model IDs for this provider. Empty = no list available."""
        return []


class GroqProviderConfig(ProviderConfig):
    """Groq: fetches live model list from /v1/models.

    Filters out non-chat models (whisper, guard, orpheus, safeguard) by name.
    Groq rejects tool-calling for structured output, so output_mode='prompted'.
    """

    env_var: Optional[str] = "GROQ_API_KEY"
    base_url: str = "https://api.groq.com/openai/v1"
    output_mode: str = "prompted"

    _EXCLUDE = ("whisper", "guard", "orpheus", "safeguard")

    def get_models(self) -> list[str]:
        key = os.environ.get(self.env_var or "", "")
        if not key:
            logger.warning("%s not set, skipping Groq model fetch", self.env_var)
            return []
        try:
            resp = httpx.get(
                f"{self.base_url}/models",
                headers={"Authorization": f"Bearer {key}"},
                timeout=8.0,
            )
            resp.raise_for_status()
            data = resp.json()
            models = [
                m["id"]
                for m in data.get("data", [])
                if not any(excl in m["id"].lower() for excl in self._EXCLUDE)
            ]
            logger.debug("Groq: %d chat models", len(models))
            return models
        except httpx.HTTPStatusError as exc:
            logger.error(
                "Groq /v1/models %d: %s",
                exc.response.status_code,
                exc.response.text[:200],
            )
            return []
        except Exception as exc:
            logger.error("Failed to fetch Groq models: %s", exc)
            return []


class OpenRouterProviderConfig(ProviderConfig):
    """OpenRouter: fetches live :free models from /v1/models."""

    env_var: Optional[str] = "OPENROUTER_API_KEY"
    base_url: str = "https://openrouter.ai/api/v1"
    output_mode: str = "prompted"

    def get_models(self) -> list[str]:
        key = os.environ.get(self.env_var or "", "")
        if not key:
            logger.warning("%s not set, skipping OpenRouter model fetch", self.env_var)
            return []
        try:
            resp = httpx.get(
                f"{self.base_url}/models",
                headers={"Authorization": f"Bearer {key}"},
                timeout=10.0,
            )
            resp.raise_for_status()
            data = resp.json()
            free = [m["id"] for m in data.get("data", []) if ":free" in m["id"]]
            logger.debug("OpenRouter: %d free models", len(free))
            return free
        except httpx.HTTPStatusError as exc:
            logger.error(
                "OpenRouter /v1/models %d: %s",
                exc.response.status_code,
                exc.response.text[:200],
            )
            return []
        except Exception as exc:
            logger.error("Failed to fetch OpenRouter models: %s", exc)
            return []


class NvidiaProviderConfig(ProviderConfig):
    """NVIDIA NIM: fetches live model list from NIM /v1/models endpoint.

    models.dev 'nvidia' slug returns Pro-tier IDs that 404 on free accounts.
    The live NIM API returns the 187 free-accessible models with vendor-prefixed
    IDs (e.g. 'meta/llama-3.3-70b-instruct', 'deepseek-ai/deepseek-v3.2').
    These IDs must be passed verbatim to the NIM completions endpoint.
    """

    env_var: Optional[str] = "NVIDIA_NIM_API_KEY"
    base_url: str = "https://integrate.api.nvidia.com/v1"
    output_mode: str = "prompted"

    def get_models(self) -> list[str]:
        api_key = os.environ.get(self.env_var or "", "")
        if not api_key:
            logger.warning("%s not set, skipping NIM model fetch", self.env_var)
            return []
        try:
            resp = httpx.get(
                f"{self.base_url}/models",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=8.0,
            )
            resp.raise_for_status()
            data = resp.json()
            models = [m["id"] for m in data.get("data", [])]
            logger.debug("NIM: fetched %d models", len(models))
            return models
        except httpx.HTTPStatusError as exc:
            logger.error(
                "NIM /v1/models %d: %s",
                exc.response.status_code,
                exc.response.text[:200],
            )
            return []
        except httpx.TimeoutException:
            logger.error("NIM /v1/models request timed out")
            return []
        except Exception as exc:
            logger.error("Failed to fetch NIM models: %s", exc)
            return []


class CloudflareProviderConfig(ProviderConfig):
    """Cloudflare Workers AI.

    OpenAI-compatible endpoint requires the account ID in the URL:
        https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/ai/v1

    Both CLOUDFLARE_API_KEY and CLOUDFLARE_ACCOUNT_ID must be set.
    """

    env_var: Optional[str] = "CLOUDFLARE_API_KEY"
    account_id_env_var: str = "CLOUDFLARE_ACCOUNT_ID"
    base_url: str = "https://api.cloudflare.com/client/v4/accounts"  # placeholder
    output_mode: str = "prompted"
    drop_params: bool = True

    @property
    def effective_base_url(self) -> str:
        account_id = os.environ.get(self.account_id_env_var, "")
        if not account_id:
            raise ValueError(
                f"{self.account_id_env_var} not set (required for Cloudflare Workers AI)"
            )
        return f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/v1"

    def get_models(self) -> list[str]:
        account_id = os.environ.get(self.account_id_env_var, "")
        api_key = os.environ.get(self.env_var or "", "")
        if not api_key or not account_id:
            logger.warning(
                "%s or %s not set, skipping Cloudflare model fetch",
                self.env_var,
                self.account_id_env_var,
            )
            return []
        try:
            models: list[str] = []
            page = 1
            while True:
                resp = httpx.get(
                    f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/models/search",
                    params={"per_page": 100, "page": page},
                    headers={"Authorization": f"Bearer {api_key}"},
                    timeout=10.0,
                )
                resp.raise_for_status()
                data = resp.json()
                batch = data.get("result", [])
                models.extend(
                    m["name"]
                    for m in batch
                    if m.get("task", {}).get("name") == "Text Generation"
                )
                info = data.get("result_info", {})
                if len(models) >= info.get("total_count", 0) or not batch:
                    break
                page += 1
            logger.debug("Cloudflare: %d Text Generation models", len(models))
            return models
        except httpx.HTTPStatusError as exc:
            logger.error(
                "Cloudflare models %d: %s",
                exc.response.status_code,
                exc.response.text[:200],
            )
            return []
        except Exception as exc:
            logger.error("Failed to fetch Cloudflare models: %s", exc)
            return []


class MistralProviderConfig(ProviderConfig):
    """Mistral: fetches live model list from /v1/models, filtered to chat-capable models.

    Uses capabilities.completion_chat == True to exclude embed/OCR/moderation/audio models.
    """

    env_var: Optional[str] = "MISTRAL_API_KEY"
    base_url: str = "https://api.mistral.ai/v1"
    output_mode: str = "tool"

    def get_models(self) -> list[str]:
        key = os.environ.get(self.env_var or "", "")
        if not key:
            logger.warning("%s not set, skipping Mistral model fetch", self.env_var)
            return []
        try:
            resp = httpx.get(
                f"{self.base_url}/models",
                headers={"Authorization": f"Bearer {key}"},
                timeout=8.0,
            )
            resp.raise_for_status()
            data = resp.json()
            models = [
                m["id"]
                for m in data.get("data", [])
                if m.get("capabilities", {}).get("completion_chat")
            ]
            logger.debug("Mistral: %d chat models", len(models))
            return models
        except httpx.HTTPStatusError as exc:
            logger.error(
                "Mistral /v1/models %d: %s",
                exc.response.status_code,
                exc.response.text[:200],
            )
            return []
        except Exception as exc:
            logger.error("Failed to fetch Mistral models: %s", exc)
            return []


class OllamaCloudProviderConfig(ProviderConfig):
    """Ollama Cloud (https://ollama.com/v1).

    Fetches live model list from the OpenAI-compat /v1/models endpoint.
    """

    env_var: Optional[str] = "OLLAMA_API_KEY"
    base_url: str = "https://ollama.com/v1"
    output_mode: str = "prompted"

    def get_models(self) -> list[str]:
        key = os.environ.get(self.env_var or "", "")
        if not key:
            logger.warning(
                "%s not set, skipping Ollama Cloud model fetch", self.env_var
            )
            return []
        try:
            resp = httpx.get(
                f"{self.base_url}/models",
                headers={"Authorization": f"Bearer {key}"},
                timeout=8.0,
            )
            resp.raise_for_status()
            data = resp.json()
            models = [m["id"] for m in data.get("data", [])]
            logger.debug("Ollama Cloud: %d models", len(models))
            return models
        except httpx.HTTPStatusError as exc:
            logger.error(
                "Ollama Cloud /v1/models %d: %s",
                exc.response.status_code,
                exc.response.text[:200],
            )
            return []
        except Exception as exc:
            logger.error("Failed to fetch Ollama Cloud models: %s", exc)
            return []


class OllamaLocalProviderConfig(ProviderConfig):
    """Local Ollama (http://localhost:11434/v1).

    Only returns models with the ':cloud' suffix from the local /api/tags endpoint.
    Bare local models (e.g. 'qwen3:4b') are excluded to prevent accidental
    CPU-intensive inference.
    """

    env_var: Optional[str] = None  # no auth required
    base_url: str = "http://localhost:11434/v1"
    output_mode: str = "prompted"

    def get_models(self) -> list[str]:
        try:
            resp = httpx.get("http://localhost:11434/api/tags", timeout=3.0)
            resp.raise_for_status()
            data = resp.json()
            all_names = [m["name"] for m in data.get("models", [])]
            cloud = [n for n in all_names if n.endswith(":cloud")]
            logger.debug(
                "Local ollama: %d :cloud models (of %d total)",
                len(cloud),
                len(all_names),
            )
            return cloud
        except httpx.ConnectError:
            logger.debug("Local ollama not running (connection refused)")
            return []
        except Exception as exc:
            logger.error("Failed to fetch local ollama models: %s", exc)
            return []


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

PROVIDERS: dict[str, ProviderConfig] = {
    "groq": GroqProviderConfig(),
    "openrouter": OpenRouterProviderConfig(),
    "nvidia": NvidiaProviderConfig(),
    "mistral": MistralProviderConfig(),
    "cloudflare": CloudflareProviderConfig(),
    "ollama-cloud": OllamaCloudProviderConfig(),
    "ollama": OllamaLocalProviderConfig(),
}

# ---------------------------------------------------------------------------
# Resolution helpers
# ---------------------------------------------------------------------------


def resolve(slug: str) -> tuple[ProviderConfig, str]:
    """Split 'groq/llama-3.3-70b' → (ProviderConfig, 'llama-3.3-70b').

    Provider prefix is the first path segment. Unknown prefixes are a hard error.
    """
    if "/" not in slug:
        raise ValueError(
            f"Invalid model format {slug!r}. Expected provider/model "
            f"(known providers: {', '.join(PROVIDERS)})"
        )
    prefix, model_id = slug.split("/", 1)
    if prefix not in PROVIDERS:
        raise ValueError(
            f"Unknown provider {prefix!r}. Supported: {', '.join(PROVIDERS)}"
        )
    return PROVIDERS[prefix], model_id


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
    OpenRouterProvider for openrouter/ slugs. Falls back to generic OpenAIProvider
    for all others.
    """
    key = api_key(cfg)
    profile = OpenAIModelProfile(
        default_structured_output_mode=cfg.output_mode,  # type: ignore[arg-type]
    )
    if slug.startswith("groq/"):
        return GroqModel(model_id, provider=GroqProvider(api_key=key))
    if slug.startswith("openrouter/"):
        provider = OpenRouterProvider(api_key=key)
        return OpenAIChatModel(model_id, provider=provider, profile=profile)
    # All others: OpenAIProvider with provider-specific base URL
    provider = OpenAIProvider(base_url=cfg.effective_base_url, api_key=key)
    return OpenAIChatModel(model_id, provider=provider, profile=profile)


def list_models(provider: str | None = None) -> list[str]:
    """Return all available model slugs, optionally filtered to one provider.

    Each slug is in 'provider/model' form. Raises ValueError for unknown provider.
    """
    if provider is not None:
        cfg = PROVIDERS.get(provider)
        if cfg is None:
            raise ValueError(f"Unknown provider {provider!r}. Known: {list(PROVIDERS)}")
        return [f"{provider}/{m}" for m in cfg.get_models()]
    return [f"{name}/{m}" for name, cfg in PROVIDERS.items() for m in cfg.get_models()]


def validate(slug: str) -> None:
    """Validate a model slug: provider registered, API key(s) set, model known.

    Raises ValueError with a descriptive message on any failure.
    Skips model-list validation only when the provider returns no list.
    """
    cfg, model_id = resolve(slug)  # raises on unknown provider
    prefix = slug.split("/", 1)[0]

    # API key check
    key = api_key(cfg)
    if not key and cfg.env_var is not None:
        raise ValueError(f"{cfg.env_var} not set (required for {slug})")

    # Cloudflare also needs account ID
    if isinstance(cfg, CloudflareProviderConfig):
        if not os.environ.get(cfg.account_id_env_var):
            raise ValueError(
                f"{cfg.account_id_env_var} not set (required for cloudflare/)"
            )

    available = cfg.get_models()
    if not available:
        logger.warning(
            "Skipping model validation for %s (no model list available)", prefix
        )
        return

    if model_id not in available:
        sample = available[:20]
        lines = "\n  ".join(f"{prefix}/{m}" for m in sample)
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
