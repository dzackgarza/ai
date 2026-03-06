#!/usr/bin/env python3
"""Apply the current curated OpenRouter model adjustments."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OPENROUTER_CONFIG = ROOT / "configs" / "providers" / "openrouter.json"

MODELS_TO_REMOVE = {"aurora-alpha", "sherlock-dash-alpha", "sherlock-think-alpha"}
MODELS_TO_ADD = {
    "arcee-ai/trinity-large-preview:free",
    "nvidia/nemotron-3-nano-30b-a3b:free",
    "openai/gpt-5.3-codex",
    "openai/gpt-5.4",
    "openai/gpt-5.4-pro",
}


def display_name(model_id: str) -> str:
    return model_id.split("/")[-1].replace(":free", "").replace("-", " ").title()


def main() -> int:
    with OPENROUTER_CONFIG.open() as handle:
        config = json.load(handle)

    models = config.setdefault("models", {})
    config["models"] = {
        model_id: model_info
        for model_id, model_info in models.items()
        if model_id not in MODELS_TO_REMOVE
    }

    for model_id in MODELS_TO_ADD:
        config["models"].setdefault(model_id, {"name": display_name(model_id)})

    with OPENROUTER_CONFIG.open("w") as handle:
        json.dump(config, handle, indent=2)
        handle.write("\n")

    print("Updated openrouter.json:")
    print(f"  removed: {len(MODELS_TO_REMOVE)}")
    print(f"  ensured present: {len(MODELS_TO_ADD)}")
    print(f"  total models: {len(config['models'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
