#!/usr/bin/env python3
"""Add the Cloudflare Workers AI provider to the local Hermes config."""

from __future__ import annotations

import os
from pathlib import Path

import yaml


def main() -> None:
    account_id = os.environ["CLOUDFLARE_ACCOUNT_ID"]
    config_path = Path.home() / ".hermes" / "config.yaml"
    config = yaml.safe_load(config_path.read_text())
    assert isinstance(config, dict), f"expected mapping in {config_path}"

    providers = config.setdefault("custom_providers", [])
    assert isinstance(providers, list), "custom_providers must be a list"
    if any(provider.get("name") == "cloudflare" for provider in providers):
        print("Cloudflare already in custom_providers.")
        return

    providers.append(
        {
            "name": "cloudflare",
            "display_name": "Cloudflare Workers AI",
            "base_url": f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/v1",
            "env_vars": ["CLOUDFLARE_API_KEY"],
        }
    )

    config_path.write_text(yaml.safe_dump(config, sort_keys=False))
    print("Added cloudflare to custom_providers.")


if __name__ == "__main__":
    main()
