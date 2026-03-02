#!/usr/bin/env python3
import json
import glob
import os
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

# Glob and merge providers - fails immediately if no files found or invalid JSON
provider_files = glob.glob(os.path.join(providers_dir, "*.json"))
if not provider_files:
    raise RuntimeError(f"No provider JSON files found in {providers_dir}")

for provider_file in provider_files:
    provider_name = os.path.splitext(os.path.basename(provider_file))[0]
    with open(provider_file, "r") as f:
        config["provider"][provider_name] = json.load(f)

# Glob and merge agents - fails immediately if no files found or invalid JSON
agent_files = glob.glob(os.path.join(agents_dir, "*.json"))
if not agent_files:
    raise RuntimeError(f"No agent JSON files found in {agents_dir}")

for agent_file in agent_files:
    agent_name = os.path.splitext(os.path.basename(agent_file))[0]
    with open(agent_file, "r") as f:
        config["agent"][agent_name] = json.load(f)

# Glob and merge subagents - fails immediately if no files found or invalid JSON
subagent_files = glob.glob(os.path.join(subagents_dir, "*.json"))
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

# The schema relies on an external models.dev schema for the 'Model' type,
# which restricts the 'model' fields to a hardcoded remote enum.
# We must fetch that external schema, inject the highly specific custom
# Claude proxy models provided by the opencode-antigravity-auth plugin
# into its enum list, and inline it so jsonschema can validate our config.
if "properties" in schema and "model" in schema["properties"]:
    model_ref = schema["properties"]["model"].get("$ref", "")
    if model_ref.startswith("http"):
        # Download the external model schema
        model_schema_url = model_ref.split("#")[0]
        req_model = urllib.request.Request(
            model_schema_url, headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req_model, timeout=10) as response:
            model_schema = json.loads(response.read().decode())

        # Inject the custom models provided by the opencode-antigravity-auth plugin
        # that the public models.dev schema cannot know about.
        claude_proxy_models = [
            "google/gemini-claude-sonnet-4-6",
            "google/gemini-claude-opus-4-6-thinking",
        ]

        # Safely extend the enum if it exists
        if (
            "$defs" in model_schema
            and "Model" in model_schema["$defs"]
            and "enum" in model_schema["$defs"]["Model"]
        ):
            model_schema["$defs"]["Model"]["enum"].extend(claude_proxy_models)

            # Inline the $defs into our main schema and point the ref locally
            schema["$defs"] = schema.get("$defs", {})
            schema["$defs"]["Model"] = model_schema["$defs"]["Model"]
            schema["properties"]["model"]["$ref"] = "#/$defs/Model"

            # Also fix agent model ref
            if "patternProperties" in schema and "^.*$" in schema["patternProperties"]:
                agent_props = schema["patternProperties"]["^.*$"].get("properties", {})
                if "model" in agent_props:
                    agent_props["model"]["$ref"] = "#/$defs/Model"

# Validates config strictly and raises jsonschema.exceptions.ValidationError immediately if invalid
jsonschema.validate(instance=config, schema=schema)

# Write output - fails immediately on permission/IO errors
with open(output_path, "w") as f:
    json.dump(config, f, indent=2)
    f.write("\n")

print(f"Successfully rebuilt and validated config at {output_path}")
