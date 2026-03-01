#!/usr/bin/env python3
"""Antigravity usage limits checker — wraps the antigravity-usage CLI."""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from typing import Any

from usage_base import UsageProvider
from usage_table import UsageRow, ModelAvailability


class AntigravityProvider(UsageProvider):
    """Antigravity usage checker.

    Wraps `antigravity-usage quota --all-models --refresh --json` (global install).
    Per-model quota is tracked individually; each model gets its own table row.

    Anchoring is handled entirely by the antigravity-usage npm package (wakeup cron).
    This script detects fresh quota and sends notifications.
    """

    name = "Antigravity"
    state_dir = "antigravity_usage"
    ntfy_topic = "usage-updates"
    ntfy_server = "http://localhost"

    def provider_name(self) -> str:
        return "Antigravity"

    def fetch_raw(self) -> dict:
        """Run antigravity-usage CLI and return parsed JSON."""
        cmd = ["antigravity-usage", "quota", "--all-models", "--refresh", "--json"]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                if "not logged in" in result.stderr.lower():
                    print("Error: Not logged in. Run: antigravity-usage login", file=sys.stderr)
                else:
                    print(f"Error: {result.stderr}", file=sys.stderr)
                sys.exit(1)
            return json.loads(result.stdout)
        except FileNotFoundError:
            print("Error: antigravity-usage not found. Run: npm install -g antigravity-usage", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON output: {e}", file=sys.stderr)
            sys.exit(1)
        except subprocess.TimeoutExpired:
            print("Error: Command timed out", file=sys.stderr)
            sys.exit(1)

    def to_rows(self, raw: Any) -> list[UsageRow]:
        """Convert per-model quota data to UsageRow list.
        
        Note: 
        - remainingPercentage: float 0.0-1.0 (1.0 = 100% remaining = 0% used)
        - remainingPercentage: null/missing means N/A = 0% remaining (100% used/exhausted)
        """
        rows = []

        for model in raw.get("models", []):
            label = model.get("label", model.get("modelId", ""))
            is_exhausted = model.get("isExhausted", False)
            remaining_pct = model.get("remainingPercentage")
            reset_time = model.get("resetTime")

            if is_exhausted:
                pct_used = 100.0
            elif remaining_pct is None:
                # N/A = no remaining quota = 100% used
                pct_used = 100.0
            else:
                # remaining_pct is 0.0-1.0, convert to pct_used 0-100
                pct_used = (1.0 - remaining_pct) * 100.0

            reset_at = None
            if reset_time:
                try:
                    reset_at = datetime.fromisoformat(
                        reset_time.replace("Z", "+00:00")
                    ).astimezone(timezone.utc)
                except ValueError:
                    pass

            rows.append(UsageRow(
                identifier=f"Antigravity: {label}",
                pct_used=pct_used,
                reset_at=reset_at,
            ))

        return rows

    def availability(self, rows: list[UsageRow]) -> list[ModelAvailability]:
        """Get availability grouped by model family bucket.

        Antigravity models are grouped into 4 buckets based on reset times:
        1. Flash (All): Gemini 3 Flash, 2.5 Flash, 2.5 Flash Thinking (~3h)
        2. Pro (2.5): Gemini 2.5 Pro (~5h)
        3. Pro (3): Gemini 3 Pro High/Low, 3.1 Pro High/Low (~1d 10h)
        4. Claude (All): Claude Opus 4.6, Sonnet 4.6, GPT-OSS 120B (~12h)

        Returns one ModelAvailability per bucket, sampling any model in bucket.
        """
        # Define bucket groupings by model keywords
        buckets = [
            ("Flash (All)", ["flash"], []),
            ("Pro (2.5)", ["2.5 pro"], []),
            ("Pro (3)", ["3 pro", "3.1 pro"], []),
            ("Claude (All)", ["claude", "gpt-oss"], []),
        ]
        
        # Assign each row to a bucket
        for row in rows:
            label_lower = row.identifier.lower()
            for bucket_name, keywords, models in buckets:
                if any(kw in label_lower for kw in keywords):
                    models.append(row)
                    break
        
        # Build availability from one sample per bucket
        result = []
        for bucket_name, _, models in buckets:
            if not models:
                continue
            
            # Sample first model in bucket
            sample = models[0]
            # available_now = has meaningful quota (< 99% used)
            # 99%+ is effectively exhausted for practical purposes
            available_now = sample.pct_used < 99.0
            available_when = None if available_now else sample.reset_at
            
            result.append(ModelAvailability(
                name=f"Antigravity: {bucket_name}",
                available_now=available_now,
                available_when=available_when,
            ))
        
        return result

    def should_anchor(self, rows: list[UsageRow]) -> bool:
        """Antigravity anchoring handled by the npm package — no action needed."""
        return False

    def notify_always(self, rows: list[UsageRow]) -> None:
        """Fire when all models are at < 1% — background wakeup already triggered."""
        if rows and all(r.pct_used < 1.0 for r in rows):
            self.send_ntfy(
                "Antigravity Quota Fresh",
                "All models at <1% — quota freshly available.",
                tags="white_check_mark,rocket",
            )

    # _handle_notifications() not overridden — base class schedules notifications
    # for the latest exhausted reset_at, which covers per-model quota exhaustion.


def main() -> None:
    parser = argparse.ArgumentParser(description="Antigravity usage limits checker")
    parser.add_argument("--json", "-j", action="store_true", help="JSON output")
    parser.add_argument("--no-notify", action="store_true", help="Suppress all notifications (testing)")
    parser.add_argument("--availability", "-a", action="store_true", help="Output availability data as JSON")
    args = parser.parse_args()

    AntigravityProvider().run(args)


if __name__ == "__main__":
    main()
