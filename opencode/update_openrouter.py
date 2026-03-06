#!/usr/bin/env python3

import json

# Models to remove from config (not in models.dev)
models_to_remove = {"aurora-alpha", "sherlock-dash-alpha", "sherlock-think-alpha"}

# Models to add from models.dev (free models not in config)
models_to_add = {
    "arcee-ai/trinity-large-preview:free",
    "nvidia/nemotron-3-nano-30b-a3b:free", 
    "openai/gpt-5.3-codex",
    "openai/gpt-5.4",
    "openai/gpt-5.4-pro"
}

# Load current openrouter config
with open("/home/dzack/.config/opencode/configs/providers/openrouter.json", "r") as f:
    config = json.load(f)

# Remove models not in models.dev
if "models" in config:
    new_models = {}
    for model_id, model_info in config["models"].items():
        if model_id not in models_to_remove:
            new_models[model_id] = model_info
    config["models"] = new_models

# Add models from models.dev (free models)
if "models" in config:
    for model_id in models_to_add:
        if model_id not in config["models"]:
            config["models"][model_id] = {
                "name": model_id.split("/")[-1].replace(":free", "").replace("-", " ").title()
            }

# Write updated config
with open("/home/dzack/.config/opencode/configs/providers/openrouter.json", "w") as f:
    json.dump(config, f, indent=2)

print(f"✓ Updated openrouter.json:")
print(f"  - Removed {len(models_to_remove)} models not in models.dev")
print(f"  - Added {len(models_to_add)} free models from models.dev")
print(f"  - Total models: {len(config['models'])}")