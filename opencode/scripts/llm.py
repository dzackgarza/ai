#!/usr/bin/env python3
"""
Canonical LLM call module for the OpenCode workspace.

All LLM calls — from plugins, scripts, and test harnesses — go through here.
This is the single source of truth for:
  - Provider registry (env vars, base URLs, slug conventions)
  - Structured output via pydantic-ai (with automatic retries on parse failure)
  - Ordered model fallback (try each model in sequence; first success wins)
  - Schema registry (add a BaseModel subclass + name entry to use from TS)

CLI (for TypeScript subprocess callers):
  stdin:  JSON { "models": [...], "messages": [...], "schema": "Name",
                 "temperature": 0.0, "max_tokens": 500 }
  stdout: JSON { "ok": true, "result": {...} }
       or JSON { "ok": false, "error": "..." }

Direct Python usage:
  import asyncio
  from scripts.llm import call_llm, call_with_fallback, Classification
  result = asyncio.run(call_with_fallback(
      ["groq/llama-3.3-70b-versatile"],
      [{"role": "user", "content": "..."}],
      schema=Classification,
  ))
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import sys
from typing import Any, TypeVar

from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.profiles.openai import OpenAIModelProfile
from pydantic_ai.providers.openai import OpenAIProvider

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Provider registry — single source of truth
#
# Slug convention (matches utilities/shared/providers.ts):
#   groq/     → Groq
#   nvidia/   → NVIDIA NIM
#   ollama/   → local Ollama
#   (none)    → OpenRouter (default)
#
# output_mode controls how pydantic-ai requests structured output:
#   "tool"      → OpenAI tool-calling (default; not supported by all providers)
#   "prompted"  → JSON instruction in system prompt (universal fallback)
# ---------------------------------------------------------------------------


class ProviderConfig(BaseModel):
    env_var: str | None  # None = no auth required (ollama)
    base_url: str
    output_mode: str = "tool"  # "tool" | "prompted"


PROVIDERS: dict[str, ProviderConfig] = {
    "groq": ProviderConfig(
        env_var="GROQ_API_KEY",
        base_url="https://api.groq.com/openai/v1",
        output_mode="prompted",  # groq rejects tool-calling for structured output
    ),
    "nvidia": ProviderConfig(
        env_var="NVIDIA_API_KEY",
        base_url="https://integrate.api.nvidia.com/v1",
        output_mode="prompted",  # mistral models on NIM reject tool-calling
    ),
    "ollama": ProviderConfig(
        env_var=None,
        base_url="http://localhost:11434/v1",
        output_mode="prompted",
    ),
    "openrouter": ProviderConfig(
        env_var="OPENROUTER_API_KEY",
        base_url="https://openrouter.ai/api/v1",
        output_mode="prompted",  # provider mix; prompted is universally safe
    ),
}


def _resolve(slug: str) -> tuple[ProviderConfig, str]:
    """Split 'groq/llama-3.3-70b' → (ProviderConfig, 'llama-3.3-70b').
    Slugs with no registered prefix route to OpenRouter unchanged."""
    for prefix, cfg in PROVIDERS.items():
        if prefix == "openrouter":
            continue
        if slug.startswith(f"{prefix}/"):
            return cfg, slug[len(prefix) + 1 :]
    return PROVIDERS["openrouter"], slug


def _api_key(cfg: ProviderConfig) -> str:
    if cfg.env_var is None:
        return "ollama"
    return os.environ.get(cfg.env_var, "")


def _make_model(cfg: ProviderConfig, model_id: str) -> OpenAIChatModel:
    """Build an OpenAIChatModel with the correct output mode for the provider."""
    provider = OpenAIProvider(base_url=cfg.base_url, api_key=_api_key(cfg))
    profile = OpenAIModelProfile(
        default_structured_output_mode=cfg.output_mode,  # type: ignore[arg-type]
    )
    return OpenAIChatModel(model_id, provider=provider, profile=profile)


# ---------------------------------------------------------------------------
# Schema registry
#
# Register pydantic BaseModel subclasses by name for use from TS callers.
# ---------------------------------------------------------------------------


class Classification(BaseModel):
    """Tier classification for a user prompt."""

    tier: str  # "model-self" | "knowledge" | "C" | "B" | "A" | "S"
    reasoning: str


SCHEMAS: dict[str, type[BaseModel]] = {
    "Classification": Classification,
}

OutputT = TypeVar("OutputT", bound=BaseModel)

# ---------------------------------------------------------------------------
# Core call
# ---------------------------------------------------------------------------


async def call_llm(
    model_slug: str,
    messages: list[dict[str, str]],
    schema: type[OutputT] | None = None,
    temperature: float = 0.0,
    max_tokens: int = 500,
    retries: int = 3,
) -> OutputT | str:
    """Call one model. Returns a pydantic model instance or plain string.

    Raises on API error or schema parse failure after retries.
    """
    cfg, model_id = _resolve(model_slug)
    api_key = _api_key(cfg)
    if not api_key and cfg.env_var is not None:
        raise ValueError(f"{cfg.env_var} not set (required for {model_slug})")

    model = _make_model(cfg, model_id)
    output_type: Any = schema if schema is not None else str

    # Extract system prompt; concatenate remaining messages into prompt string
    system: str | None = None
    user_parts: list[str] = []
    for msg in messages:
        if msg.get("role") == "system":
            system = msg["content"]
        elif msg.get("content"):
            user_parts.append(msg["content"])
    prompt = "\n\n".join(user_parts)

    agent: Agent[None, Any] = Agent(
        model,
        output_type=output_type,
        system_prompt=system or "",
        retries=retries,
    )

    result = await agent.run(prompt)
    return result.output


async def call_with_fallback(
    model_slugs: list[str],
    messages: list[dict[str, str]],
    schema: type[OutputT] | None = None,
    temperature: float = 0.0,
    max_tokens: int = 500,
    retries: int = 3,
) -> OutputT | str:
    """Try each model in order; return first success. Raises if all fail."""
    last_exc: Exception | None = None
    for slug in model_slugs:
        cfg, _ = _resolve(slug)
        if _api_key(cfg) == "" and cfg.env_var is not None:
            logger.debug("Skipping %s: %s not set", slug, cfg.env_var)
            continue
        try:
            return await call_llm(
                slug,
                messages,
                schema=schema,
                temperature=temperature,
                max_tokens=max_tokens,
                retries=retries,
            )
        except Exception as exc:
            logger.warning("Model %s failed: %s", slug, exc)
            last_exc = exc
    raise RuntimeError(f"All models failed. Last error: {last_exc}") from last_exc


# ---------------------------------------------------------------------------
# CLI entry point — called via subprocess from TypeScript
# ---------------------------------------------------------------------------


async def _cli_main() -> None:
    raw = sys.stdin.read()
    try:
        req = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(json.dumps({"ok": False, "error": f"Invalid JSON input: {exc}"}))
        sys.exit(1)

    models: list[str] = req.get("models", [])
    messages: list[dict[str, str]] = req.get("messages", [])
    schema_name: str | None = req.get("schema")
    temperature: float = req.get("temperature", 0.0)
    max_tokens: int = req.get("max_tokens", 500)
    retries: int = req.get("retries", 3)

    if not models:
        print(json.dumps({"ok": False, "error": "No models specified"}))
        sys.exit(1)

    schema: type[BaseModel] | None = None
    if schema_name:
        schema = SCHEMAS.get(schema_name)
        if schema is None:
            known = list(SCHEMAS)
            print(
                json.dumps(
                    {
                        "ok": False,
                        "error": f"Unknown schema: {schema_name!r}. Known: {known}",
                    }
                )
            )
            sys.exit(1)

    try:
        result = await call_with_fallback(
            models,
            messages,
            schema=schema,
            temperature=temperature,
            max_tokens=max_tokens,
            retries=retries,
        )
        if isinstance(result, BaseModel):
            print(json.dumps({"ok": True, "result": result.model_dump()}))
        else:
            print(json.dumps({"ok": True, "result": result}))
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}))
        sys.exit(1)


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")
    asyncio.run(_cli_main())
