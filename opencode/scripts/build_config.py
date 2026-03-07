#!/usr/bin/env python3
import json
import os
import glob
import subprocess
import urllib.request
import jsonschema
from rich import print
from rich.console import Console
from rich.theme import Theme

console = Console(
    theme=Theme(
        {
            "info": "cyan",
            "warning": "yellow",
            "error": "bold red",
            "success": "green",
        }
    )
)

base_dir = os.path.expanduser("~/.config/opencode")
skeleton_path = os.path.join(base_dir, "configs", "config_skeleton.json")
providers_dir = os.path.join(base_dir, "configs", "providers")
agents_dir = os.path.join(base_dir, "configs", "agents")
subagents_dir = os.path.join(base_dir, "configs", "subagents")
output_path = os.path.join(base_dir, "opencode.json")

# Load skeleton - fails immediately (FileNotFoundError/JSONDecodeError) if missing/invalid
with open(skeleton_path, "r") as f:
    config = json.load(f)

config["provider"] = {}
config["agent"] = {}

# Glob and merge providers
provider_files = sorted(glob.glob(os.path.join(providers_dir, "*.json")))
if not provider_files:
    raise RuntimeError(f"No provider JSON files found in {providers_dir}")

for provider_file in provider_files:
    provider_name = os.path.splitext(os.path.basename(provider_file))[0]
    with open(provider_file, "r") as f:
        config["provider"][provider_name] = json.load(f)

# Glob and merge primary agents (Alphabetical)
agent_files = sorted(glob.glob(os.path.join(agents_dir, "*.json")))
if not agent_files:
    raise RuntimeError(f"No agent JSON files found in {agents_dir}")

for agent_file in agent_files:
    agent_name = os.path.splitext(os.path.basename(agent_file))[0]
    with open(agent_file, "r") as f:
        config["agent"][agent_name] = json.load(f)

# Glob and merge subagents (Alphabetical, appended AFTER primary agents)
subagent_files = sorted(glob.glob(os.path.join(subagents_dir, "*.json")))
if not subagent_files:
    raise RuntimeError(f"No subagent JSON files found in {subagents_dir}")

for subagent_file in subagent_files:
    subagent_name = os.path.splitext(os.path.basename(subagent_file))[0]
    with open(subagent_file, "r") as f:
        config["agent"][subagent_name] = json.load(f)

# Fetch config schema
schema_url = config["$schema"]
req = urllib.request.Request(schema_url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=10) as response:
    schema = json.loads(response.read().decode())

# Inject the highly specific custom Claude proxy models and cursor-acp models
if "properties" in schema and "model" in schema["properties"]:
    model_ref = schema["properties"]["model"].get("$ref", "")
    if model_ref.startswith("http"):
        model_schema_url = model_ref.split("#")[0]
        req_model = urllib.request.Request(
            model_schema_url, headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req_model, timeout=10) as response:
            model_schema = json.loads(response.read().decode())

        custom_models = [
            "google/gemini-claude-sonnet-4-6",
            "google/gemini-claude-opus-4-6-thinking",
            "cursor-acp/auto",
        ]

        if (
            "$defs" in model_schema
            and "Model" in model_schema["$defs"]
            and "enum" in model_schema["$defs"]["Model"]
        ):
            model_schema["$defs"]["Model"]["enum"].extend(custom_models)
            schema["$defs"] = schema.get("$defs", {})
            schema["$defs"]["Model"] = model_schema["$defs"]["Model"]
            schema["properties"]["model"]["$ref"] = "#/$defs/Model"

            # Also update agent.*.model fields to use local $defs
            if "properties" in schema and "agent" in schema["properties"]:
                agent_props = schema["properties"]["agent"].get("properties", {})
                for agent_name in agent_props:
                    agent_config = agent_props[agent_name]
                    if (
                        "properties" in agent_config
                        and "model" in agent_config["properties"]
                    ):
                        agent_config["properties"]["model"]["$ref"] = "#/$defs/Model"


# Validates config strictly
# Note: We remove model enum validation since custom models (cursor-acp, etc.) aren't in upstream schemas
# Opencode validates models at runtime against its actual provider registry
def remove_model_enum(schema_obj):
    """Recursively remove model enum constraints from schema."""
    if isinstance(schema_obj, dict):
        if "$defs" in schema_obj and "Model" in schema_obj["$defs"]:
            if "enum" in schema_obj["$defs"]["Model"]:
                del schema_obj["$defs"]["Model"]["enum"]
        # Also handle external $ref to model schemas
        for key, value in list(schema_obj.items()):
            if key == "$ref" and isinstance(value, str) and "model-schema" in value:
                # Replace external model ref with local unconstrained version
                schema_obj["$ref"] = "#/$defs/Model"
                if "$defs" not in schema_obj:
                    schema_obj["$defs"] = {}
                if "Model" not in schema_obj["$defs"]:
                    schema_obj["$defs"]["Model"] = {"type": "string"}
            else:
                remove_model_enum(value)
    elif isinstance(schema_obj, list):
        for item in schema_obj:
            remove_model_enum(item)


remove_model_enum(schema)
jsonschema.validate(instance=config, schema=schema)

# Write output keeping the dictionary insertion order (which preserves the primary->subagent sorting)
with open(output_path, "w") as f:
    json.dump(config, f, indent=2)
    f.write("\n")

print(f"Successfully rebuilt and validated config at {output_path}")

# Restart opencode-serve user service to pick up config changes
subprocess.run(["systemctl", "--user", "restart", "opencode-serve"], check=True)
print("Restarted opencode-serve user service")

# Refresh models to pick up any provider changes
subprocess.run(["opencode", "models", "--refresh"], check=True)
print("Refreshed opencode models")


def list_runtime_provider_models(provider_id: str) -> set[str]:
    """Query runtime provider models, cached after first call."""
    global _runtime_models_cache
    if _runtime_models_cache is None:
        output = subprocess.check_output(["opencode", "models"], text=True)
        _runtime_models_cache = {}
        current_provider = None
        for line in output.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            if "/" in stripped and not stripped.startswith(" "):
                current_provider = stripped.rstrip("/")
                _runtime_models_cache[current_provider] = []
            elif current_provider and stripped.startswith("  "):
                model_name = stripped.lstrip()
                if model_name:
                    _runtime_models_cache[current_provider].append(model_name)

    return set(_runtime_models_cache.get(provider_id, []))


_runtime_models_cache: dict[str, list[str]] | None = None


def fetch_models_dev_api() -> dict:
    """Fetch canonical model data from models.dev API."""
    url = "https://models.dev/api.json"
    req = urllib.request.Request(
        url, headers={"User-Agent": "opencode-config-builder/1.0"}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        raise RuntimeError(f"Failed to fetch models.dev API: {e}")


# Cache for models.dev data
_models_dev_cache: dict | None = None


def get_models_dev_provider_models(provider_id: str) -> set[str] | None:
    """Get models for a provider from models.dev API (cached)."""
    global _models_dev_cache
    if _models_dev_cache is None:
        _models_dev_cache = fetch_models_dev_api()

    provider = _models_dev_cache.get(provider_id)
    if not provider:
        return None  # Provider not in models.dev
    return set((provider.get("models") or {}).keys())


def list_upstream_provider_models(provider_id: str) -> set[str]:
    cache_root = os.environ.get("XDG_CACHE_HOME", os.path.expanduser("~/.cache"))
    models_cache_path = os.path.join(cache_root, "opencode", "models.json")
    with open(models_cache_path, "r") as f:
        models_cache = json.load(f)

    provider = models_cache.get(provider_id)
    if not provider:
        raise RuntimeError(
            f"Provider '{provider_id}' not found in upstream models cache at "
            f"{models_cache_path}"
        )

    return set((provider.get("models") or {}).keys())


def list_cursor_acp_upstream_models() -> set[str]:
    """Query Cursor ACP API directly for available models."""
    try:
        with urllib.request.urlopen(
            "http://127.0.0.1:32124/v1/models", timeout=5
        ) as response:
            data = json.loads(response.read().decode())
            return {m["id"] for m in data.get("data", [])}
    except Exception as e:
        raise RuntimeError(f"Failed to query Cursor ACP API: {e}")


def assert_provider_partition_matches_models_dev(provider_id: str) -> set[str]:
    """Validate provider config against models.dev canonical source.

    Reports symmetric difference between:
    - Models in local config (whitelist ∪ blacklist)
    - Models in models.dev API

    With actionable guidance for resolving discrepancies.
    """
    provider_cfg = config.get("provider", {}).get(provider_id)
    if provider_cfg is None:
        raise RuntimeError(
            f"Provider '{provider_id}' must be explicitly shadowed in config/provider "
            "for whitelist/blacklist partitioning."
        )

    whitelist = set((provider_cfg.get("models") or {}).keys())
    blacklist = set(provider_cfg.get("blacklist") or [])

    # Check for overlap (hard error - config bug)
    overlap = sorted(whitelist & blacklist)
    if overlap:
        raise RuntimeError(
            f"[bold red] "
            f"Provider '{provider_id}' has models in both whitelist and blacklist: {overlap}"
        )

    # Special handling for ollama-cloud - strip ":cloud" suffix
    if provider_id == "ollama-cloud":
        whitelist = {model.replace(":cloud", "") for model in whitelist}
        blacklist = {model.replace(":cloud", "") for model in blacklist}

    local_models = whitelist | blacklist
    models_dev_models = get_models_dev_provider_models(provider_id)

    # Provider not in models.dev - skip validation but warn
    if models_dev_models is None:
        print(
            f"[bold yellow] "
            f"Provider '{provider_id}' not found in models.dev API, skipping validation"
        )
        return whitelist

    # Calculate symmetric difference
    in_local_not_dev = sorted(local_models - models_dev_models)
    in_dev_not_local = sorted(models_dev_models - local_models)

    has_discrepancies = bool(in_local_not_dev or in_dev_not_local)

    if has_discrepancies:
        print(
            f"\n[bold yellow]⚠ Provider '{provider_id}' model discrepancy detected:[/]\n"
        )

        if in_local_not_dev:
            print(
                f"  [cyan]Models in config but NOT in models.dev ({len(in_local_not_dev)}):[/]"
            )
            for model in in_local_not_dev[:10]:  # Limit output
                print(f"    [cyan]• {model}[/]")
            if len(in_local_not_dev) > 10:
                print(f"    [cyan]  ... and {len(in_local_not_dev) - 10} more[/]")
            print(
                f"\n  [blue]→ Action: Verify these models exist in 'opencode models {provider_id}' "
                f"and/or the provider's original API.[/]"
            )
            print("  [blue]  If confirmed, models.dev may be out of date.[/]\n")

        if in_dev_not_local:
            print(
                f"  [magenta]Models in models.dev but NOT in config ({len(in_dev_not_local)}):[/]"
            )
            for model in in_dev_not_local[:10]:  # Limit output
                print(f"    [magenta]• {model}[/]")
            if len(in_dev_not_local) > 10:
                print(f"    [magenta]  ... and {len(in_dev_not_local) - 10} more[/]")
            print(
                f"\n  [blue]→ Action: Check 'opencode models {provider_id}' for these models.[/]"
            )
            print(
                f"  [blue]  Add to whitelist (if free/usable) or blacklist in configs/providers/{provider_id}.json[/]\n"
            )

        # Show summary stats
        print(
            f"  [bold]Summary:[/] "
            f"local={len(local_models)} models.dev={len(models_dev_models)} "
            f"symmetric_diff={len(in_local_not_dev) + len(in_dev_not_local)}"
        )
    else:
        print(
            f"[green]✓[/] Provider '{provider_id}' validated: "
            f"models.dev={len(models_dev_models)} whitelist={len(whitelist)} blacklist={len(blacklist)}"
        )

    return whitelist


def assert_cursor_acp_blacklist_matches_api(provider_id: str) -> set[str]:
    """Guard for cursor-acp: verify blacklist covers all API models except whitelisted."""
    provider_cfg = config.get("provider", {}).get(provider_id)
    if provider_cfg is None:
        raise RuntimeError(
            f"Provider '{provider_id}' must be explicitly defined in config/provider"
        )

    model_overrides = set((provider_cfg.get("models") or {}).keys())
    blacklist = set(provider_cfg.get("blacklist") or [])

    # Check no overlap
    overlap = sorted(model_overrides & blacklist)
    if overlap:
        raise RuntimeError(
            f"Provider '{provider_id}' has models present in both allowlist "
            f"and blacklist: {overlap}"
        )

    # Query API directly for upstream models
    try:
        upstream = list_cursor_acp_upstream_models()
    except RuntimeError as e:
        print(
            f"Provider '{provider_id}' warning: API unavailable ({e}), skipping blacklist verification"
        )
        return model_overrides

    # All upstream models must be either whitelisted or blacklisted
    covered = model_overrides | blacklist
    missing = sorted(upstream - covered)
    blacklist_extra = sorted(blacklist - upstream)

    if missing:
        raise RuntimeError(
            f"Provider '{provider_id}' has models from API not covered by whitelist/blacklist: {missing}"
        )

    if blacklist_extra:
        print(
            f"Provider '{provider_id}' warning: blacklist contains models not in API: {blacklist_extra}"
        )

    manual_additions = sorted(model_overrides - upstream)
    if manual_additions:
        print(
            f"Provider '{provider_id}' manual allowlist additions not in API: {manual_additions}"
        )

    print(
        f"Verified provider '{provider_id}' against Cursor ACP API: "
        f"api={len(upstream)} allow={len(model_overrides)} deny={len(blacklist)}"
    )
    return model_overrides


def assert_runtime_whitelist_applied(
    provider_id: str, expected_models: set[str]
) -> None:
    listed = list_runtime_provider_models(provider_id)
    missing_from_runtime = sorted(expected_models - listed)
    unexpected_in_runtime = sorted(listed - expected_models)
    if missing_from_runtime or unexpected_in_runtime:
        raise RuntimeError(
            f"Provider '{provider_id}' runtime whitelist mismatch. "
            f"missing_from_runtime={missing_from_runtime} "
            f"unexpected_in_runtime={unexpected_in_runtime}"
        )

    print(
        f"Verified provider '{provider_id}' runtime whitelist: "
        f"runtime={len(listed)} expected={len(expected_models)}"
    )


# Guardrail order:
# 1) Validate against models.dev canonical source.
# 2) Validate runtime list reflects whitelist after blacklist filtering.
#
# Note: We validate ALL providers, not just nvidia and cursor-acp, since we want
# comprehensive coverage of all provider configs.

# Providers to ignore (not in models.dev yet)
ignored_providers = {"cursor-acp", "qwen-code"}

# Validate all providers against models.dev
providers_to_validate = []  # Empty = validate all providers in config

for provider_id in config.get("provider", {}).keys():
    # Skip ignored providers
    if provider_id in ignored_providers:
        print(
            f"[yellow][bold]⚠️  SKIPPING '{provider_id}' - not found in models.dev yet[/]"
        )
        continue

    # Skip validation for specific providers if needed
    if providers_to_validate and provider_id not in providers_to_validate:
        continue

    whitelist = assert_provider_partition_matches_models_dev(provider_id)
    # Still validate runtime whitelist application
    assert_runtime_whitelist_applied(provider_id, whitelist)
