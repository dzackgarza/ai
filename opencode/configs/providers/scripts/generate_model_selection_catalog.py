#!/usr/bin/env python3
"""Build the model-selection JSON catalog from the YAML source."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert provider-models.yaml into provider-models.json."
    )
    default_dir = (
        Path(__file__).resolve().parents[2]
        / ".."
        / "skills"
        / "model-selection"
    ).resolve()
    parser.add_argument(
        "--input",
        type=Path,
        default=default_dir / "provider-models.yaml",
        help="Path to the YAML provider-model catalog.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=default_dir / "provider-models.json",
        help="Path to write the JSON provider-model catalog.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data = yaml.safe_load(args.input.read_text())
    assert isinstance(data, dict), f"expected YAML mapping in {args.input}"

    data["version"] = 1
    providers = data.get("providers")
    assert isinstance(providers, dict), "provider catalog must contain providers mapping"

    for provider_data in providers.values():
        assert isinstance(provider_data, dict), "provider entries must be mappings"
        models = provider_data.get("models")
        if models is None:
            provider_data["models"] = []
            continue
        assert isinstance(models, list), "provider models must be lists"
        for model in models:
            assert isinstance(model, dict), "model entries must be mappings"
            if "name" in model and "description" not in model:
                model["description"] = model["name"]

    args.output.write_text(json.dumps(data, indent=2) + "\n")


if __name__ == "__main__":
    main()
