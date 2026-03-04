#!/usr/bin/env python3
import json
import os
import glob
import subprocess
import urllib.request
import jsonschema

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

# Inject the highly specific custom Claude proxy models
if "properties" in schema and "model" in schema["properties"]:
    model_ref = schema["properties"]["model"].get("$ref", "")
    if model_ref.startswith("http"):
        model_schema_url = model_ref.split("#")[0]
        req_model = urllib.request.Request(
            model_schema_url, headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req_model, timeout=10) as response:
            model_schema = json.loads(response.read().decode())

        claude_proxy_models = [
            "google/gemini-claude-sonnet-4-6",
            "google/gemini-claude-opus-4-6-thinking",
        ]

        if (
            "$defs" in model_schema
            and "Model" in model_schema["$defs"]
            and "enum" in model_schema["$defs"]["Model"]
        ):
            model_schema["$defs"]["Model"]["enum"].extend(claude_proxy_models)
            schema["$defs"] = schema.get("$defs", {})
            schema["$defs"]["Model"] = model_schema["$defs"]["Model"]
            schema["properties"]["model"]["$ref"] = "#/$defs/Model"

            if "patternProperties" in schema and "^.*$" in schema["patternProperties"]:
                agent_props = schema["patternProperties"]["^.*$"].get("properties", {})
                if "model" in agent_props:
                    agent_props["model"]["$ref"] = "#/$defs/Model"

# Validates config strictly
jsonschema.validate(instance=config, schema=schema)

# Write output keeping the dictionary insertion order (which preserves the primary->subagent sorting)
with open(output_path, "w") as f:
    json.dump(config, f, indent=2)
    f.write("\n")

print(f"Successfully rebuilt and validated config at {output_path}")

# Restart opencode-serve user service to pick up config changes
subprocess.run(
    ["systemctl", "--user", "restart", "opencode-serve"],
    check=True
)
print("Restarted opencode-serve user service")

# Refresh models to pick up any provider changes
subprocess.run(
    ["opencode", "models", "--refresh"],
    check=True
)
print("Refreshed opencode models")


def list_runtime_provider_models(provider_id):
    output = subprocess.check_output(["opencode", "models", provider_id], text=True)
    prefix = f"{provider_id}/"
    return {
        line.strip()[len(prefix):]
        for line in output.splitlines()
        if line.strip().startswith(prefix)
    }


def list_upstream_provider_models(provider_id):
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


def assert_provider_partition_matches_upstream(provider_id):
    provider_cfg = config.get("provider", {}).get(provider_id)
    if provider_cfg is None:
        raise RuntimeError(
            f"Provider '{provider_id}' must be explicitly shadowed in config/provider "
            "for whitelist/blacklist partitioning."
        )

    model_overrides = set((provider_cfg.get("models") or {}).keys())
    blacklist = set(provider_cfg.get("blacklist") or [])
    overlap = sorted(model_overrides & blacklist)
    if overlap:
        raise RuntimeError(
            f"Provider '{provider_id}' has models present in both allowlist "
            f"and blacklist: {overlap}"
        )

    covered = model_overrides | blacklist
    upstream = list_upstream_provider_models(provider_id)

    missing = sorted(upstream - covered)
    blacklist_extra = sorted(blacklist - upstream)
    if missing or blacklist_extra:
        raise RuntimeError(
            f"Provider '{provider_id}' partition mismatch. "
            f"missing_from_partition={missing} "
            f"blacklist_not_in_upstream={blacklist_extra}"
        )

    manual_additions = sorted(model_overrides - upstream)
    if manual_additions:
        print(
            f"Provider '{provider_id}' manual allowlist additions not in "
            f"upstream: {manual_additions}"
        )

    print(
        f"Verified provider '{provider_id}' partition against upstream: "
        f"upstream={len(upstream)} allow={len(model_overrides)} "
        f"deny={len(blacklist)}"
    )
    return model_overrides


def assert_runtime_whitelist_applied(provider_id, expected_models):
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
# 1) Partition against upstream models catalog.
# 2) Validate runtime list reflects whitelist after blacklist filtering.
nvidia_whitelist = assert_provider_partition_matches_upstream("nvidia")
assert_runtime_whitelist_applied("nvidia", nvidia_whitelist)
