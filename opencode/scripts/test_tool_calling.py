#!/usr/bin/env python3
"""
OpenRouter Strict Agentic Tool-Calling Validation

This script puts models through a rigorous agentic simulation.
It tests whether a model can:
1. Output a native JSON tool call (not raw text wrapped in markdown).
2. Correctly infer parameter types (e.g. booleans vs strings).
3. Handle optional parameters without hallucinating schema violations.

Usage:
  python3 test_tool_calling.py [model_slug]
"""

import os
import requests
import json
import time
import sys

api_key = os.environ.get("OPENROUTER_API_KEY")
if not api_key:
    print("No OPENROUTER_API_KEY found in environment variables.")
    sys.exit(1)

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://opencode.ai",
    "X-Title": "OpenCode Test",
}


def evaluate_model(model_name):
    print(f"\n--- Testing Tool Calling: {model_name} ---")
    payload = {
        "model": model_name,
        "messages": [
            {
                "role": "system",
                "content": "You are a subagent. You must call a tool to answer the user. Do not explain anything. Just output the tool call in JSON format.",
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
            print(f"⚠️ API Error: {data['error'].get('message', '')}")
            return False

        message = data["choices"][0]["message"]
        has_tool_call = "tool_calls" in message and len(message["tool_calls"]) > 0
        content = message.get("content")

        if has_tool_call:
            args = message["tool_calls"][0]["function"]["arguments"]
            try:
                parsed = json.loads(args)
                if isinstance(parsed.get("case_sensitive"), bool):
                    print(
                        "✅ PASSED: Correct native tool call and typed boolean correctly."
                    )
                    return True
                elif "case_sensitive" in parsed:
                    print("❌ FAILED: Native tool call, but typed boolean as string.")
                    return False
                else:
                    print(
                        "✅ PASSED: Correct native tool call (omitted optional param)."
                    )
                    return True
            except json.JSONDecodeError:
                print("❌ FAILED: Native tool call, but arguments are not valid JSON.")
                return False
        else:
            print("❌ FAILED: Did not output a native tool call.")
            print("Output snippet: ", str(content)[:100])
            return False

    except Exception as e:
        print(f"⚠️ Network/Timeout Error: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1:
        evaluate_model(sys.argv[1])
    else:
        with open(
            "/home/dzack/.config/opencode/configs/providers/openrouter.json", "r"
        ) as f:
            config = json.load(f)

        models_to_test = list(config.get("models", {}).keys())
        print(f"Running TOOL-CALLING test on {len(models_to_test)} models...")

        for model in models_to_test:
            evaluate_model(model)
            time.sleep(2)
