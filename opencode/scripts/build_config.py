#!/usr/bin/env python3
"""Build and validate opencode.json from the canonical source files."""

from __future__ import annotations

import argparse
import glob
import json
import logging
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent / "permissions"))
import jsonschema
from rich.console import Console
from rich.logging import RichHandler
from src.agent_markdown import get_prompt

_console = Console(stderr=True)
_handler = RichHandler(
    console=_console, markup=True, show_path=False, rich_tracebacks=True
)
_handler.setFormatter(logging.Formatter("%(message)s"))
logger = logging.getLogger("opencode.config.build")
if not logger.handlers:
    logger.addHandler(_handler)
logger.setLevel(logging.INFO)
logger.propagate = False

BASE_DIR = Path(os.path.expanduser("~/.config/opencode"))
SKELETON_PATH = BASE_DIR / "configs" / "config_skeleton.json"
PROVIDERS_DIR = BASE_DIR / "configs" / "providers"
OUTPUT_PATH = BASE_DIR / "opencode.json"
MODELS_DEV_API = "https://models.dev/api.json"
OPENROUTER_CHAT_COMPLETIONS_API = "https://openrouter.ai/api/v1/chat/completions"
SCHEMA_USER_AGENT = "opencode-config-builder/1.0"
IGNORED_PROVIDERS = {"qwen-code"}
# Providers whose live catalog is a large multi-modal reseller marketplace
# (TTS/image/video/etc.) rather than a curated text-model list: only the
# "did our chosen models rot" half of the live check is meaningful for them.
# Flagging every uncurated model as "unaccounted" would produce hundreds of
# unactionable findings and teach people to ignore --strict failures.
NARROW_ALLOWLIST_PROVIDERS = {"vectorengine"}
# models.dev's own provider registry (not just its per-provider model lists)
# publishes the real api base URL and auth env var name for providers we
# don't self-host connection details for locally. That structural metadata
# (which provider, which base URL) changes far less often than the model
# list itself, so it's a reasonable source for *where to check live* even
# though the model list it reports can lag. Some of models.dev's declared
# env var names don't match this repo's .envrc naming; known aliases here.
KNOWN_ENV_ALIASES = {
    "OLLAMA_API_KEY": "OLLAMA_CLOUD_API_KEY",
}
GOOGLE_GENERATIVE_LANGUAGE_API = "https://generativelanguage.googleapis.com/v1beta/models"


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r") as handle:
        return json.load(handle)


def _write_json(path: Path, data: dict[str, Any]) -> None:
    with path.open("w") as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")


def _resolve_prompt_slugs(value: Any) -> Any:
    if isinstance(value, dict):
        resolved: dict[str, Any] = {}
        for key, item in value.items():
            if key == "prompt_slug":
                resolved["prompt"] = get_prompt(str(item)).text
                continue
            resolved[key] = _resolve_prompt_slugs(item)
        return resolved
    if isinstance(value, list):
        return [_resolve_prompt_slugs(item) for item in value]
    return value


def _fetch_json(url: str, timeout: int = 30) -> dict[str, Any]:
    request = urllib.request.Request(url, headers={"User-Agent": SCHEMA_USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode())


def _post_json(
    url: str,
    data: dict[str, Any],
    headers: dict[str, str],
    timeout: int = 30,
) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        data=json.dumps(data).encode(),
        headers={"User-Agent": SCHEMA_USER_AGENT, **headers},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode())


def _extract_error_message(body: str) -> str:
    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        return body[:500]

    error = payload.get("error")
    if not isinstance(error, dict):
        return body[:500]
    message = error.get("message")
    if isinstance(message, str):
        return message
    return body[:500]


def load_config_sources() -> dict[str, Any]:
    config = _read_json(SKELETON_PATH)
    config.pop("permission", None)
    config["provider"] = {}
    provider_files = sorted(glob.glob(str(PROVIDERS_DIR / "*.json")))
    if not provider_files:
        raise RuntimeError(f"No provider JSON files found in {PROVIDERS_DIR}")

    for provider_file in provider_files:
        provider_path = Path(provider_file)
        provider_name = provider_path.stem
        config["provider"][provider_name] = _read_json(provider_path)

    config = _resolve_prompt_slugs(config)

    if config.get("agent") == {}:
        del config["agent"]
    return config


def fetch_config_schema(config: dict[str, Any]) -> dict[str, Any]:
    schema_url = config["$schema"]
    schema = _fetch_json(schema_url, timeout=10)

    model_ref = ((schema.get("properties") or {}).get("model") or {}).get("$ref") or ""
    if model_ref.startswith("http"):
        model_schema_url = model_ref.split("#")[0]
        model_schema = _fetch_json(model_schema_url, timeout=10)
        custom_models = [
            "google/gemini-claude-sonnet-4-6",
            "google/gemini-claude-opus-4-6-thinking",
        ]
        model_def = ((model_schema.get("$defs") or {}).get("Model")) or {}
        if "enum" in model_def:
            model_def["enum"].extend(custom_models)
            schema.setdefault("$defs", {})
            schema["$defs"]["Model"] = model_def
            schema["properties"]["model"]["$ref"] = "#/$defs/Model"
            agent_props = ((schema.get("properties") or {}).get("agent") or {}).get(
                "properties"
            ) or {}
            for agent_config in agent_props.values():
                model_prop = ((agent_config.get("properties") or {}).get("model")) or {}
                if "$ref" in model_prop:
                    model_prop["$ref"] = "#/$defs/Model"
    return schema


def remove_model_enum(schema_obj: Any) -> None:
    """Recursively remove model enum constraints from schema."""
    if isinstance(schema_obj, dict):
        model_def = ((schema_obj.get("$defs") or {}).get("Model")) or {}
        if "enum" in model_def:
            del model_def["enum"]
        for key, value in list(schema_obj.items()):
            if key == "$ref" and isinstance(value, str) and "model-schema" in value:
                schema_obj["$ref"] = "#/$defs/Model"
                schema_obj.setdefault("$defs", {})
                schema_obj["$defs"].setdefault("Model", {"type": "string"})
            else:
                remove_model_enum(value)
    elif isinstance(schema_obj, list):
        for item in schema_obj:
            remove_model_enum(item)


def validate_config_schema(config: dict[str, Any], schema: dict[str, Any]) -> None:
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(instance=config, schema=schema)


def fetch_models_dev_api() -> dict[str, Any]:
    try:
        return _fetch_json(MODELS_DEV_API)
    except Exception as exc:
        raise RuntimeError(f"Failed to fetch models.dev API: {exc}") from exc


def fetch_openrouter_api() -> dict[str, Any]:
    """Fetch live model list from OpenRouter API."""
    try:
        return _fetch_json("https://openrouter.ai/api/v1/models")
    except Exception as exc:
        raise RuntimeError(f"Failed to fetch OpenRouter API: {exc}") from exc


def check_openrouter_model_invocation(model_id: str) -> str | None:
    """Return a call-time error for unusable OpenRouter models."""
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        return "OPENROUTER_API_KEY is not set"

    payload = {
        "model": model_id,
        "messages": [{"role": "user", "content": "Reply with exactly OK."}],
        "max_tokens": 1,
        "temperature": 0,
    }
    try:
        _post_json(
            OPENROUTER_CHAT_COMPLETIONS_API,
            payload,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
        )
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode(errors="replace")
        return f"HTTP {exc.code}: {_extract_error_message(error_body)}"
    except Exception as exc:
        return f"{type(exc).__name__}: {exc}"
    return None


def is_openrouter_free(model: dict[str, Any]) -> bool:
    """Check if an OpenRouter model is free (cost == 0 or :free suffix)."""
    model_id = model.get("id", "")
    if model_id.endswith(":free"):
        return True
    pricing = model.get("pricing", {})
    prompt_cost = float(pricing.get("prompt", 0) or 0)
    completion_cost = float(pricing.get("completion", 0) or 0)
    if prompt_cost == 0 and completion_cost == 0:
        return True
    return False


def get_models_dev_provider_models(
    models_dev_data: dict[str, Any], provider_id: str
) -> set[str] | None:
    provider = models_dev_data.get(provider_id)
    if not provider:
        return None
    return set((provider.get("models") or {}).keys())


def get_models_dev_provider_meta(
    models_dev_data: dict[str, Any], provider_id: str
) -> dict[str, Any] | None:
    """Return models.dev's structural metadata (api base URL, npm package,
    auth env var names) for a provider, distinct from its model list."""
    provider = models_dev_data.get(provider_id)
    if not provider:
        return None
    return {
        "npm": provider.get("npm"),
        "api": provider.get("api"),
        "env": provider.get("env") or [],
    }


def resolve_first_env(env_names: list[str]) -> str | None:
    for name in env_names:
        value = os.environ.get(name) or os.environ.get(
            KNOWN_ENV_ALIASES.get(name, "")
        )
        if value:
            return value
    return None


def fetch_google_models(api_key: str) -> list[str]:
    """Fetch the live model list from the Google Generative Language API."""
    request = urllib.request.Request(
        f"{GOOGLE_GENERATIVE_LANGUAGE_API}?key={api_key}&pageSize=200",
        headers={"User-Agent": SCHEMA_USER_AGENT},
    )
    with urllib.request.urlopen(request, timeout=15) as response:
        payload = json.loads(response.read().decode())
    return [
        str(m["name"]).removeprefix("models/")
        for m in payload.get("models", [])
        if m.get("name")
    ]


def resolve_env_template(value: Any) -> str | None:
    """Resolve a "{env:VAR}" placeholder to its environment value, if present."""
    if not isinstance(value, str):
        return None
    if value.startswith("{env:") and value.endswith("}"):
        return os.environ.get(value[len("{env:") : -1])
    return value


def fetch_openai_compatible_models(base_url: str, api_key: str | None) -> list[dict[str, Any]]:
    """Fetch the live model list from an OpenAI-compatible `/models` endpoint."""
    headers = {"User-Agent": SCHEMA_USER_AGENT}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    url = base_url.rstrip("/") + "/models"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=15) as response:
        payload = json.loads(response.read().decode())
    return payload.get("data", [])


def _diff_live_ids(
    provider_id: str, live_ids: set[str], whitelist: set[str], blacklist: set[str]
) -> list[str]:
    """Shared whitelist/blacklist-vs-live-catalog diff, used by every live
    provider check regardless of API shape."""
    issues: list[str] = []
    known = whitelist | blacklist

    missing_whitelist = sorted(whitelist - live_ids)
    if missing_whitelist:
        message = (
            f"{provider_id}: {len(missing_whitelist)} whitelisted model(s) "
            f"missing from the live catalog (rotated/dead): {missing_whitelist}"
        )
        issues.append(message)
        logger.warning("[yellow]%s[/yellow]", message, extra={"markup": True})

    unaccounted: list[str] = []
    if provider_id in NARROW_ALLOWLIST_PROVIDERS:
        logger.info(
            "[dim]%s: narrow-allowlist provider, skipping unaccounted-model "
            "check (%d live models not curated)[/dim]",
            provider_id,
            len(live_ids - known),
            extra={"markup": True},
        )
    elif not whitelist:
        # Empty whitelist means default-allow (e.g. anthropic.json is
        # blacklist-only): every non-blacklisted live model is expected and
        # not drift, so there's nothing to triage here.
        logger.info(
            "[dim]%s: default-allow (blacklist-only), skipping "
            "unaccounted-model check[/dim]",
            provider_id,
            extra={"markup": True},
        )
    else:
        unaccounted = sorted(live_ids - known)
        if unaccounted:
            message = (
                f"{provider_id}: {len(unaccounted)} live model(s) absent from "
                f"both whitelist and blacklist (unclassified/new): {unaccounted}"
            )
            issues.append(message)
            logger.warning("[yellow]%s[/yellow]", message, extra={"markup": True})

    if not missing_whitelist and not unaccounted:
        logger.info(
            "[green]Validated %s against its live catalog[/green] "
            "(whitelist=%d blacklist=%d live=%d)",
            provider_id,
            len(whitelist),
            len(blacklist),
            len(live_ids),
            extra={"markup": True},
        )
    return issues


def validate_openai_compatible_provider(
    provider_id: str,
    provider_cfg: dict[str, Any],
    base_url_override: str | None = None,
    api_key_override: str | None = None,
) -> list[str]:
    """Validate a directly-queryable OpenAI-compatible provider against its own
    live `/models` endpoint, rather than the third-party models.dev mirror.

    This is the authoritative check for providers like NVIDIA NIM or
    VectorEngine that models.dev may track late or not at all: it catches both
    whitelisted models that have rotated off the live catalog and new live
    models that have not yet been triaged into the whitelist or blacklist.

    base_url_override/api_key_override let callers supply connection details
    for providers that don't self-declare options.baseURL locally (e.g.
    ollama-cloud, which relies on opencode's own built-in provider registry)
    but whose base URL and auth env var are known from models.dev's provider
    metadata.
    """
    issues: list[str] = []
    options = provider_cfg.get("options") or {}
    base_url = base_url_override or options.get("baseURL")
    if not base_url:
        return issues

    api_key = api_key_override
    if api_key is None and "apiKey" in options:
        api_key = resolve_env_template(options["apiKey"])
        if not api_key:
            logger.warning(
                "[yellow]%s: apiKey env var unset, skipping live validation[/yellow]",
                provider_id,
                extra={"markup": True},
            )
            return issues

    try:
        live_models = fetch_openai_compatible_models(base_url, api_key)
    except Exception as exc:  # noqa: BLE001 - live endpoints fail in many ways
        logger.warning(
            "[yellow]%s: live model list unreachable (%s), skipping live "
            "validation[/yellow]",
            provider_id,
            exc,
            extra={"markup": True},
        )
        return issues

    live_ids = {str(model.get("id", "")) for model in live_models if model.get("id")}
    whitelist = set((provider_cfg.get("models") or {}).keys())
    blacklist = set(provider_cfg.get("blacklist") or [])
    return _diff_live_ids(provider_id, live_ids, whitelist, blacklist)


def validate_google_provider(
    provider_id: str, provider_cfg: dict[str, Any], api_key: str
) -> list[str]:
    """Validate the Google provider against the live Generative Language API
    (different auth/response shape than the OpenAI-compatible providers)."""
    try:
        live_ids = set(fetch_google_models(api_key))
    except Exception as exc:  # noqa: BLE001 - live endpoints fail in many ways
        logger.warning(
            "[yellow]%s: live model list unreachable (%s), skipping live "
            "validation[/yellow]",
            provider_id,
            exc,
            extra={"markup": True},
        )
        return []

    whitelist = set((provider_cfg.get("models") or {}).keys())
    blacklist = set(provider_cfg.get("blacklist") or [])
    return _diff_live_ids(provider_id, live_ids, whitelist, blacklist)


def show_provider_partition_diff(
    config: dict[str, Any],
    models_dev_data: dict[str, Any],
    provider_id: str,
) -> tuple[set[str], list[str]]:
    provider_cfg = (config.get("provider") or {}).get(provider_id)
    if provider_cfg is None:
        raise RuntimeError(
            f"Provider '{provider_id}' must be explicitly shadowed in config/provider "
            "for whitelist/blacklist partitioning."
        )

    whitelist = set((provider_cfg.get("models") or {}).keys())
    blacklist = set(provider_cfg.get("blacklist") or [])
    overlap = sorted(whitelist & blacklist)
    if overlap:
        raise RuntimeError(
            f"Provider '{provider_id}' has models in both whitelist and blacklist: "
            f"{overlap}"
        )

    if provider_id == "ollama-cloud":
        whitelist = {model.replace(":cloud", "") for model in whitelist}
        blacklist = {model.replace(":cloud", "") for model in blacklist}

    models_dev_models = get_models_dev_provider_models(models_dev_data, provider_id)
    if models_dev_models is None:
        logger.info(
            "[dim]%s: not in models.dev[/dim]", provider_id, extra={"markup": True}
        )
        return whitelist, []

    # Stale blacklist entries (no longer resolving in models.dev at all) are
    # dead weight, not drift: the model is already rejected either way, so
    # there's nothing to act on. Only whitelist entries going dead, or new
    # live models needing triage, are real issues -- the same rule
    # _diff_live_ids already applies to every live-endpoint-checked provider.
    issues = _diff_live_ids(provider_id, models_dev_models, whitelist, blacklist)
    return whitelist, issues


def validate_openrouter(config: dict[str, Any]) -> list[str]:
    """Validate OpenRouter provider against its live model list.

    Checks (each runs independently so one finding cannot hide another):
    1. Whitelisted models missing from the live OpenRouter model list
    2. Whitelisted models that are live but no longer free
    3. Free-suffix whitelist entries whose paid base model still exists
    4. Whitelisted models that fail a minimal chat completion call
    5. Free models present in the blacklist
    6. Free models live but absent from both whitelist and blacklist (new drift)

    Returns the list of issue messages found; callers decide whether to treat
    them as fatal.
    """
    issues: list[str] = []
    provider_cfg = (config.get("provider") or {}).get("openrouter")
    if provider_cfg is None:
        message = "OpenRouter provider not found in config"
        issues.append(message)
        logger.warning("[yellow]%s[/yellow]", message, extra={"markup": True})
        return issues

    whitelist = set((provider_cfg.get("models") or {}).keys())
    blacklist_raw = provider_cfg.get("blacklist", [])
    blacklist = set(blacklist_raw) if isinstance(blacklist_raw, list) else set()

    openrouter_data = fetch_openrouter_api()
    live_models = openrouter_data.get("data", [])
    live_by_id = {str(model.get("id", "")): model for model in live_models}
    live_ids = set(live_by_id)
    missing_whitelist = sorted(whitelist - live_ids)
    if missing_whitelist:
        message = (
            f"OpenRouter: {len(missing_whitelist)} whitelisted model(s) missing "
            f"from the live model list: {missing_whitelist[:15]}"
        )
        issues.append(message)
        logger.warning("[yellow]%s[/yellow]", message, extra={"markup": True})
    else:
        logger.info(
            "[green]OpenRouter: All whitelisted models are present in the live "
            "model list[/green]",
            extra={"markup": True},
        )

    paid_whitelist = sorted(
        model_id
        for model_id in whitelist & live_ids
        if not is_openrouter_free(live_by_id[model_id])
    )
    if paid_whitelist:
        message = (
            f"OpenRouter: {len(paid_whitelist)} whitelisted model(s) are priced "
            f"above zero: {paid_whitelist[:15]}"
        )
        issues.append(message)
        logger.warning("[yellow]%s[/yellow]", message, extra={"markup": True})
    else:
        logger.info(
            "[green]OpenRouter: All live whitelisted models are priced at zero[/green]",
            extra={"markup": True},
        )

    missing_free_with_paid_base = sorted(
        model_id
        for model_id in missing_whitelist
        if model_id.endswith(":free")
        and model_id.removesuffix(":free") in live_ids
        and not is_openrouter_free(live_by_id[model_id.removesuffix(":free")])
    )
    if missing_free_with_paid_base:
        message = (
            f"OpenRouter: {len(missing_free_with_paid_base)} missing whitelisted "
            f"free model(s) have paid base models still listed: "
            f"{missing_free_with_paid_base[:15]}"
        )
        issues.append(message)
        logger.warning("[yellow]%s[/yellow]", message, extra={"markup": True})

    invocation_failures = {
        model_id: error
        for model_id in sorted(whitelist)
        if (error := check_openrouter_model_invocation(model_id)) is not None
    }
    if invocation_failures:
        message = (
            f"OpenRouter: {len(invocation_failures)} whitelisted model(s) failed "
            f"a minimal chat completion call: {list(invocation_failures.items())[:10]}"
        )
        issues.append(message)
        logger.warning("[yellow]%s[/yellow]", message, extra={"markup": True})
    else:
        logger.info(
            "[green]OpenRouter: All whitelisted models passed a minimal chat "
            "completion call[/green]",
            extra={"markup": True},
        )

    free_live_ids = {
        str(model.get("id", "")) for model in live_models if is_openrouter_free(model)
    }
    # Being free does not make blacklisting wrong: notes/openrouter-model-
    # vetting.md documents deliberate quality exclusions (failed tool-calling,
    # <35B parameter issues) among exactly these ids. This is expected state,
    # not drift, so it's informational only and does not fail --strict.
    blacklisted_free = sorted(free_live_ids & blacklist)
    if blacklisted_free:
        logger.info(
            "[dim]OpenRouter: %d free model(s) deliberately blacklisted: "
            "%s[/dim]",
            len(blacklisted_free),
            blacklisted_free[:25],
            extra={"markup": True},
        )
    else:
        logger.info(
            "[green]OpenRouter: No free models are present in the blacklist[/green]",
            extra={"markup": True},
        )

    unaccounted_free = sorted(free_live_ids - whitelist - blacklist)
    if unaccounted_free:
        message = (
            f"OpenRouter: {len(unaccounted_free)} free model(s) absent from both "
            f"whitelist and blacklist: {unaccounted_free}"
        )
        issues.append(message)
        logger.warning("[yellow]%s[/yellow]", message, extra={"markup": True})
    else:
        logger.info(
            "[green]OpenRouter: All live free models are accounted for[/green]",
            extra={"markup": True},
        )

    return issues


def validate_provider_partitions(
    config: dict[str, Any], only_provider: str | None = None
) -> list[str]:
    models_dev_data = fetch_models_dev_api()
    all_issues: list[str] = []
    provider_ids = sorted((config.get("provider") or {}).keys())
    if only_provider is not None:
        if only_provider not in provider_ids:
            raise RuntimeError(f"Unknown provider '{only_provider}'")
        provider_ids = [only_provider]

    for provider_id in provider_ids:
        provider_cfg = config["provider"][provider_id]
        if provider_id == "openrouter":
            # OpenRouter uses live API validation, not models.dev
            all_issues.extend(validate_openrouter(config))
            continue
        if provider_id in IGNORED_PROVIDERS:
            logger.warning(
                "[yellow]Skipping provider validation for %s "
                "(not in models.dev yet)[/yellow]",
                provider_id,
                extra={"markup": True},
            )
            continue
        if provider_cfg.get("npm") == "@ai-sdk/openai-compatible" and (
            provider_cfg.get("options") or {}
        ).get("baseURL"):
            # Directly-queryable providers (NVIDIA NIM, VectorEngine, ...) are
            # validated against their own live catalog, which is authoritative
            # over the third-party models.dev mirror.
            all_issues.extend(
                validate_openai_compatible_provider(provider_id, provider_cfg)
            )
            continue

        # Providers that don't self-declare options.baseURL locally (they
        # rely on opencode's own built-in provider registry) but whose real
        # base URL and auth env var are published in models.dev's provider
        # metadata (not its lagging model list). If we hold a working
        # credential, check live truth instead of the model-list mirror.
        meta = get_models_dev_provider_meta(models_dev_data, provider_id)
        if meta:
            api_key = resolve_first_env(meta.get("env") or [])
            if meta.get("npm") == "@ai-sdk/openai-compatible" and meta.get("api") and api_key:
                all_issues.extend(
                    validate_openai_compatible_provider(
                        provider_id,
                        provider_cfg,
                        base_url_override=meta["api"],
                        api_key_override=api_key,
                    )
                )
                continue
            if meta.get("npm") == "@ai-sdk/google" and api_key:
                all_issues.extend(
                    validate_google_provider(provider_id, provider_cfg, api_key)
                )
                continue
            logger.info(
                "[dim]%s: no credential for live validation (needs one of "
                "%s), falling back to models.dev model-list diff[/dim]",
                provider_id,
                meta.get("env"),
                extra={"markup": True},
            )

        _, issues = show_provider_partition_diff(config, models_dev_data, provider_id)
        all_issues.extend(issues)

    return all_issues


def build_config(
    strict: bool = False,
    validate_only: bool = False,
    only_provider: str | None = None,
) -> Path:
    config = load_config_sources()

    if not validate_only:
        schema = fetch_config_schema(config)
        remove_model_enum(schema)
        validate_config_schema(config, schema)
        _write_json(OUTPUT_PATH, config)
        logger.info(
            "[green]Validated and wrote %s[/green]",
            OUTPUT_PATH,
            extra={"markup": True},
        )

    issues = validate_provider_partitions(config, only_provider=only_provider)

    if issues:
        logger.warning(
            "[yellow]%d provider partition issue(s) found[/yellow]",
            len(issues),
            extra={"markup": True},
        )
        if strict:
            for issue in issues:
                logger.error("[red]- %s[/red]", issue, extra={"markup": True})
            raise SystemExit(1)

    return OUTPUT_PATH


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build opencode.json and validate provider model partitions."
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Skip schema fetch/write; only run provider partition validation.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero if any provider partition issue is found.",
    )
    parser.add_argument(
        "--provider",
        default=None,
        help="Restrict validation to a single provider id.",
    )
    args = parser.parse_args()
    build_config(
        strict=args.strict,
        validate_only=args.validate_only,
        only_provider=args.provider,
    )


if __name__ == "__main__":
    main()
