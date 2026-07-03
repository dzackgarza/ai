#!/usr/bin/env python3
"""Probe Cloudflare Workers AI through the OpenAI-compatible chat endpoint."""

from __future__ import annotations

import argparse
import json
import os
import urllib.request


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Send one chat-completion probe to Cloudflare Workers AI."
    )
    parser.add_argument("model", help="Cloudflare model id, for example @cf/zai-org/glm-5.2")
    parser.add_argument("--prompt", default="Hello", help="Probe prompt text.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    account_id = os.environ["CLOUDFLARE_ACCOUNT_ID"]
    api_key = os.environ["CLOUDFLARE_API_KEY"]
    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/v1/chat/completions"
    body = json.dumps(
        {"model": args.model, "messages": [{"role": "user", "content": args.prompt}]}
    ).encode()
    request = urllib.request.Request(
        url,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(request) as response:
        payload = json.loads(response.read().decode())

    print(payload["choices"][0]["message"]["content"])


if __name__ == "__main__":
    main()
