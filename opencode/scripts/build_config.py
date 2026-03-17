#!/usr/bin/env python3
"""Build and validate opencode.json from the canonical source files."""

from __future__ import annotations

import glob
import json
import logging
import os
from pathlib import Path
import urllib.request
from typing import Any

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "permissions"))
from src.agent_markdown import get_prompt
import jsonschema
from rich.console import Console
from rich.logging import RichHandler


_console = Console(stderr=True)
_handler = RichHandler(console=_console, markup=True, show_path=False, rich_tracebacks=True)
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
SCHEMA_USER_AGENT = "opencode-config-builder/1.0"
IGNORED_PROVIDERS = {"qwen-code"}


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


def load_config_sources() -> dict[str, Any]:
    config = _read_json(SKELETON_PATH)
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

    model_ref = (((schema.get("properties") or {}).get("model") or {}).get("$ref") or "")
    if model_ref.startswith("http"):
        model_schema_url = model_ref.split("#")[0]
        model_schema = _fetch_json(model_schema_url, timeout=10)
        custom_models = [
            "google/gemini-claude-sonnet-4-6",
            "google/gemini-claude-opus-4-6-thinking",
        ]
        model_def = (((model_schema.get("$defs") or {}).get("Model")) or {})
        if "enum" in model_def:
            model_def["enum"].extend(custom_models)
            schema.setdefault("$defs", {})
            schema["$defs"]["Model"] = model_def
            schema["properties"]["model"]["$ref"] = "#/$defs/Model"
            agent_props = (((schema.get("properties") or {}).get("agent") or {}).get("properties") or {})
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


def get_models_dev_provider_models(models_dev_data: dict[str, Any], provider_id: str) -> set[str] | None:
    provider = models_dev_data.get(provider_id)
    if not provider:
        return None
    return set((provider.get("models") or {}).keys())


def show_provider_partition_diff(
    config: dict[str, Any],
    models_dev_data: dict[str, Any],
    provider_id: str,
) -> set[str]:
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
            f"Provider '{provider_id}' has models in both whitelist and blacklist: {overlap}"
        )

    if provider_id == "ollama-cloud":
        whitelist = {model.replace(":cloud", "") for model in whitelist}
        blacklist = {model.replace(":cloud", "") for model in blacklist}

    local_models = whitelist | blacklist
    models_dev_models = get_models_dev_provider_models(models_dev_data, provider_id)
    if models_dev_models is None:
        logger.info("[dim]%s: not in models.dev[/dim]", provider_id, extra={"markup": True})
        return whitelist

    in_local_not_dev = sorted(local_models - models_dev_models)
    in_dev_not_local = sorted(models_dev_models - local_models)
    if in_local_not_dev or in_dev_not_local:
        logger.warning(
            "[yellow]%s differs from models.dev (local_only=%d, upstream_only=%d)[/yellow]",
            provider_id,
            len(in_local_not_dev),
            len(in_dev_not_local),
            extra={"markup": True},
        )
    else:
        logger.info(
            "[green]Validated %s against models.dev[/green] (whitelist=%d blacklist=%d)",
            provider_id,
            len(whitelist),
            len(blacklist),
            extra={"markup": True},
        )
    return whitelist


def validate_provider_partitions(config: dict[str, Any]) -> None:
    models_dev_data = fetch_models_dev_api()
    for provider_id in sorted((config.get("provider") or {}).keys()):
        if provider_id in IGNORED_PROVIDERS:
            logger.warning(
                "[yellow]Skipping provider validation for %s (not in models.dev yet)[/yellow]",
                provider_id,
                extra={"markup": True},
            )
            continue
        show_provider_partition_diff(config, models_dev_data, provider_id)


def build_config() -> Path:
    config = load_config_sources()
    schema = fetch_config_schema(config)
    remove_model_enum(schema)
    validate_config_schema(config, schema)
    _write_json(OUTPUT_PATH, config)
    logger.info("[green]Validated and wrote %s[/green]", OUTPUT_PATH, extra={"markup": True})
    validate_provider_partitions(config)
    return OUTPUT_PATH


def main() -> None:
    build_config()


if __name__ == "__main__":
    main()
