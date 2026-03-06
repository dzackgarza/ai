#!/usr/bin/env python3
"""Run a strict OpenRouter tool-calling probe against configured models."""

from __future__ import annotations

import argparse
import json
import os
import sys
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
        "X-Title": "OpenCode Tool Probe",
    }


def evaluate_model(model_name: str, headers: dict[str, str]) -> bool:
    print(f"\nTesting tool calling: {model_name}")
    payload = {
        "model": model_name,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a subagent. You must call a tool to answer the user. "
                    "Do not explain anything. Just output the tool call in JSON format."
                ),
            },
            {
                "role": "user",
                "content": 'Find all the files in the "src" directory that contain the word "auth".',
            },
        ],
        "tools": [
            {
                "type": "function",
                "function": {
                    "name": "search_files",
                    "description": "Searches files for a pattern",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "pattern": {"type": "string"},
                            "directory": {"type": "string"},
                            "case_sensitive": {"type": "boolean"},
                        },
                        "required": ["pattern", "directory"],
                    },
                },
            }
        ],
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=25,
        )
        data = response.json()
        if "error" in data:
            print(f"API ERROR: {data['error'].get('message', '')}")
            return False

        message = data["choices"][0]["message"]
        tool_calls = message.get("tool_calls") or []
        if not tool_calls:
            print(f"FAILED: no native tool call. Output snippet: {str(message.get('content'))[:100]}")
            return False

        args = tool_calls[0]["function"]["arguments"]
        try:
            parsed = json.loads(args)
        except json.JSONDecodeError:
            print("FAILED: tool call arguments were not valid JSON.")
            return False

        if isinstance(parsed.get("case_sensitive"), bool):
            print("PASSED: native tool call with correct boolean typing.")
            return True
        if "case_sensitive" in parsed:
            print("FAILED: native tool call used a string instead of a boolean.")
            return False

        print("PASSED: native tool call omitted the optional boolean cleanly.")
        return True
    except Exception as exc:
        print(f"NETWORK OR TIMEOUT ERROR: {exc}")
        return False


def load_models() -> list[str]:
    with OPENROUTER_CONFIG.open() as handle:
        config = json.load(handle)
    return list((config.get("models") or {}).keys())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("models", nargs="*", help="Optional subset of model IDs to probe")
    parser.add_argument("--delay", type=float, default=2.0, help="Seconds between probes")
    args = parser.parse_args()

    models = args.models or load_models()
    print(f"Running tool-calling probe on {len(models)} models...")

    headers = build_headers()
    failures = 0
    for index, model in enumerate(models):
        if not evaluate_model(model, headers):
            failures += 1
        if index < len(models) - 1:
            time.sleep(args.delay)

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
