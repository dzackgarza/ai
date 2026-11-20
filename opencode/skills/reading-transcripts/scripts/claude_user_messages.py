"""Print the messages that the human user typed in a Claude Code session, with timestamps.

A Claude Code JSONL stores tool results, system reminders, compaction summaries,
subagent hand-backs and scheduled prompts under the same `user` role as the text
that the person typed. This script keeps only the typed text:

- events whose `origin.kind` is `human`;
- messages sent while a turn was running, which the harness wraps in the text
  "The user sent a new message while you were working:".

A wrapped message has no timestamp of its own, so it is printed with the
timestamp of the nearest earlier event. Each message is printed once.
The JSONL line number in each header locates the message for a context read.

A typed message can survive only inside an `api-request-blob` event, where no
field separates it from a scheduled prompt. `--unclassified` also prints the
first 300 characters of each remaining plain user text that does not start with
a known machine prefix, so that a reader can judge those by hand.
"""

import argparse
import json
import re
import sys
from pathlib import Path

MIDTURN_OPEN = "The user sent a new message while you were working:"
MIDTURN_CLOSE = "This is how Claude Code surfaces messages"
MACHINE_PREFIXES = (
    "<system-reminder",
    "<command-",
    "<local-command",
    "<bash-",
    "<task-notification",
    "Tool loaded",
    "[Request interrupted",
    "Another Claude session sent a message",
    "This session is being continued from a previous conversation",
    "Base directory for this skill:",
)


def user_texts(event: dict) -> list[str]:
    message = event.get("message")
    if not isinstance(message, dict) or message.get("role") != "user":
        return []
    content = message.get("content", "")
    if isinstance(content, str):
        return [content]
    return [
        block.get("text", "")
        for block in content
        if isinstance(block, dict) and block.get("type") == "text"
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("jsonl", type=Path, help="Claude Code session file")
    parser.add_argument(
        "--unclassified",
        action="store_true",
        help="also print the head of plain user texts with no human marker",
    )
    args = parser.parse_args()

    last_timestamp = "unknown"
    seen: set[str] = set()
    with args.jsonl.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                # The last line of a session that is still running can be partial.
                print(f"[line {line_number}: not valid JSON, skipped]", file=sys.stderr)
                continue
            if event.get("timestamp"):
                last_timestamp = event["timestamp"]
            origin = event.get("origin")
            typed = isinstance(origin, dict) and origin.get("kind") == "human"
            for text in user_texts(event):
                if MIDTURN_OPEN in text:
                    body = text.split(MIDTURN_OPEN, 1)[1].split(MIDTURN_CLOSE, 1)[0]
                    kind = "mid-turn"
                elif typed:
                    body, kind = text, "typed"
                elif (
                    args.unclassified
                    and not event.get("isMeta")
                    and not event.get("isCompactSummary")
                    and not text.lstrip().startswith(MACHINE_PREFIXES)
                ):
                    body, kind = text.strip()[:300], "unclassified"
                else:
                    continue
                key = re.sub(r"\s+", " ", body.strip())[:300]
                if not key or key in seen:
                    continue
                seen.add(key)
                print(f"\n===== line {line_number} | {last_timestamp} | {kind}")
                print(body.strip())


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        sys.exit(0)
