#!/usr/bin/env python3
"""Inspect a single provider entry from models.dev."""

from __future__ import annotations

import argparse
import json
import urllib.request


def fetch_models_dev_api() -> dict:
    url = "https://models.dev/api.json"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "opencode-provider-debug/1.0"},
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("provider", nargs="?", default="opencode")
    args = parser.parse_args()

    api_data = fetch_models_dev_api()
    provider_data = api_data.get(args.provider)

    if provider_data:
        models = provider_data.get("models") or {}
        print(f"models.dev shows {args.provider} with {len(models)} models:\n")
        for model_id, model_info in models.items():
            print(f"  {model_id} - {model_info['name']}")
        return 0

    print(f"{args.provider} not found in models.dev\n")
    similar = [name for name in api_data if args.provider.split("-")[0] in name]
    if similar:
        print(f"Similar provider names: {', '.join(similar)}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
