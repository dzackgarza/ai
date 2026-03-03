#!/usr/bin/env python3
"""
OpenRouter API Ping Tester

This script tests a list of OpenRouter models to determine if their
endpoints are alive (HTTP 200), rate-limited, permanently dead (HTTP 404),
or if their free promotional periods have expired.

Usage:
  python3 ping_openrouter_models.py
"""

import os
import requests
import json
import time

api_key = os.environ.get("OPENROUTER_API_KEY")
if not api_key:
    print("No OPENROUTER_API_KEY found in environment variables.")
    exit(1)

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://opencode.ai",
    "X-Title": "OpenCode Test",
}


def check_endpoint(model_name):
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
        if "error" in data:
            err_msg = data["error"].get("message", "")
            if "No endpoints found" in err_msg:
                print("❌ 404 No Endpoints")
                return False
            elif (
                "rate-limited" in err_msg
                or "temporarily rate-limited" in err_msg
                or "Provider returned error" in err_msg
            ):
                print(f"⚠️ Rate Limited/Provider Error (but likely active): {err_msg}")
                return True
            else:
                print(f"❌ Error: {err_msg}")
                return False
        else:
            print("✅ Active")
            return True

    except Exception as e:
        print(f"❌ Network/Timeout: {e}")
        return False


if __name__ == "__main__":
    with open(
        "/home/dzack/.config/opencode/configs/providers/openrouter.json", "r"
    ) as f:
        config = json.load(f)

    # Test all models currently configured as available
    active_models = list(config.get("models", {}).keys())

    print(f"Testing {len(active_models)} models for endpoint availability...\n")

    for model in active_models:
        check_endpoint(model)
        time.sleep(1)  # Be gentle with rate limits
