#!/usr/bin/env python3
"""Extract or refresh active Qwen access token from local Chromium storage."""

from __future__ import annotations

import argparse
import base64
import glob
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

JWT_RE = re.compile(rb"eyJ[a-zA-Z0-9_-]{10,}\.eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}")


def b64_decode(s: str) -> bytes:
    s += "=" * (-len(s) % 4)
    return base64.urlsafe_b64decode(s)


def find_browser_tokens() -> list[tuple[int, str]]:
    candidate_paths = (
        glob.glob(os.path.expanduser("~/.config/chromium/Default/Local Storage/leveldb/*.ldb"))
        + glob.glob(os.path.expanduser("~/.config/chromium/Default/Local Storage/leveldb/*.log"))
        + glob.glob(os.path.expanduser("~/.config/google-chrome/Default/Local Storage/leveldb/*.ldb"))
        + glob.glob(os.path.expanduser("~/.config/google-chrome/Default/Local Storage/leveldb/*.log"))
    )

    tokens: list[tuple[int, str]] = []
    seen: set[str] = set()

    for path in candidate_paths:
        try:
            with open(path, "rb") as fp:
                data = fp.read()
                if b"chat.qwen.ai" not in data:
                    continue
                for match in JWT_RE.finditer(data):
                    t = match.group(0).decode("ascii", errors="ignore")
                    if t in seen:
                        continue
                    seen.add(t)
                    parts = t.split(".")
                    if len(parts) == 3:
                        try:
                            payload = json.loads(b64_decode(parts[1]))
                            exp = int(payload.get("exp", 0))
                            tokens.append((exp, t))
                        except Exception:
                            pass
        except Exception:
            pass

    tokens.sort(key=lambda x: x[0], reverse=True)
    return tokens


def validate_or_refresh(token: str) -> str:
    url = f"https://qwen.aikit.club/v1/refresh?token={token}"
    req = urllib.request.Request(url, headers={"User-Agent": "opencode-qwen/1.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode())
        refreshed = data.get("access_token")
        if refreshed:
            return refreshed
    return token


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract active Qwen web session token.")
    parser.add_argument("--refresh", action="store_true", help="Refresh token against upstream endpoint")
    parser.add_argument("--quiet", action="store_true", help="Print only token string")
    args = parser.parse_args()

    tokens = find_browser_tokens()
    if not tokens:
        print("No Qwen session tokens found in local browser storage.", file=sys.stderr)
        return 1

    best_exp, best_token = tokens[0]
    if args.refresh:
        try:
            best_token = validate_or_refresh(best_token)
        except Exception as exc:
            if not args.quiet:
                print(f"Warning: token refresh failed ({exc}), using extracted token.", file=sys.stderr)

    if args.quiet:
        print(best_token)
    else:
        print(f"Active Qwen token (expires timestamp {best_exp}):")
        print(best_token)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
