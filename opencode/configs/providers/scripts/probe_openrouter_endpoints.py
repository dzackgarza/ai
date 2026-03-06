#!/usr/bin/env python3
"""Ping configured OpenRouter models for endpoint viability."""

from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parents[3]
OPENROUTER_CONFIG = ROOT / "configs" / "providers" / "openrouter.json"
API_KEY = os.environ.get("OPENROUTER_API_KEY")


def build_headers() -> dict[str, str]:
    if not API_KEY:
        raise SystemExit("No OPENROUTER_API_KEY found in environment variables.")
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://opencode.ai",
        "X-Title": "OpenCode Probe",
    }


def check_endpoint(model_name: str, headers: dict[str, str]) -> bool:
    print(f"Checking {model_name}...", end=" ", flush=True)
    payload = {
        "model": model_name,
        "messages": [{"role": "user", "content": "ping"}],
        "max_tokens": 5,
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=10,
        )
        data = response.json()
        if "error" not in data:
            print("ACTIVE")
            return True

        err_msg = data["error"].get("message", "")
        if "No endpoints found" in err_msg:
            print("NO ENDPOINTS")
            return False
        if "rate-limited" in err_msg or "Provider returned error" in err_msg:
            print(f"RATE LIMITED OR PROVIDER ERROR: {err_msg}")
            return True

        print(f"ERROR: {err_msg}")
        return False
    except Exception as exc:
        print(f"NETWORK OR TIMEOUT: {exc}")
        return False


def load_models() -> list[str]:
    with OPENROUTER_CONFIG.open() as handle:
        config = json.load(handle)
    return list((config.get("models") or {}).keys())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("models", nargs="*", help="Optional subset of model IDs to probe")
    parser.add_argument("--delay", type=float, default=1.0, help="Seconds between probes")
    args = parser.parse_args()

    configured_models = load_models()
    models = args.models or configured_models
    print(f"Testing {len(models)} OpenRouter models for endpoint availability.\n")

    headers = build_headers()
    for index, model in enumerate(models):
        check_endpoint(model, headers)
        if index < len(models) - 1:
            time.sleep(args.delay)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
