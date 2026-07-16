#!/usr/bin/env python3
"""Print OpenRouter pricing records for selected model-id fragments."""

from __future__ import annotations

import argparse
import json
import urllib.request


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inspect OpenRouter pricing for model-id fragments."
    )
    parser.add_argument("fragments", nargs="+", help="Model id substrings to match.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    request = urllib.request.Request("https://openrouter.ai/api/v1/models")
    with urllib.request.urlopen(request) as response:
        payload = json.loads(response.read().decode())

    for model in payload["data"]:
        model_id = model["id"]
        if any(fragment in model_id for fragment in args.fragments):
            print(model_id, model.get("pricing"))


if __name__ == "__main__":
    main()
