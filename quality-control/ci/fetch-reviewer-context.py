# /// script
# requires-python = ">=3.11"
# ///
"""
Generate a compact reviewer context file from a PR's current thread set and index.

This context is given to review agents before they run, to prevent re-raising
existing issues without new evidence.

Usage:
  uv run quality-control/ci/fetch-reviewer-context.py \
    --pr-number 123 \
    --repo owner/repo \
    --output .reviewer-context.md

The output is a markdown file with unresolved/resolved threads and known
duplicate clusters.  Pass it to the review agent as instructions:

  "Do not intentionally re-raise these issues unless you have new evidence,
  the problem reappears in a materially different form, or the previous
  resolution is directly contradicted by the current code."
"""

import argparse
import json
import subprocess
import sys


def _fail(msg: str) -> None:
    print(f"FATAL: {msg}", file=sys.stderr)
    sys.exit(1)


def _gh_api_json(path: str) -> list | dict:
    result = subprocess.run(
        ["gh", "api", path],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        _fail(f"gh api {path} failed: {result.stderr.strip()}")
    return json.loads(result.stdout)


def _extract_threads_from_index(body: str) -> tuple[list[str], list[str]]:
    """Parse the index comment structure to extract thread references."""
    unresolved: list[str] = []
    resolved: list[str] = []
    current_section: str | None = None
    for line in body.split("\n"):
        stripped = line.strip()
        if stripped.startswith("### Unresolved"):
            current_section = "unresolved"
        elif stripped.startswith("### Resolved"):
            current_section = "resolved"
        elif stripped.startswith("### "):
            current_section = None
        elif (
            current_section and "." in stripped and stripped.split(".", 1)[0].isdigit()
        ):
            target = unresolved if current_section == "unresolved" else resolved
            target.append(stripped)
    return unresolved, resolved


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate reviewer context from PR thread state"
    )
    parser.add_argument("--pr-number", required=True, type=int)
    parser.add_argument("--repo", required=True)
    parser.add_argument(
        "--output",
        default=None,
        help="Output file path (default: stdout)",
    )
    args = parser.parse_args()

    repo = args.repo
    pr = args.pr_number

    # Fetch issue comments to find the index
    issue_comments = _gh_api_json(f"repos/{repo}/issues/{pr}/comments")

    # Find the index comment
    index_body = None
    index_url = None
    for c in issue_comments:
        body = c.get("body", "") or ""
        if "<!-- review-thread-index -->" in body:
            index_body = body
            index_url = c.get("html_url", "")
            break

    lines: list[str] = []
    lines.append("## Existing review issues on this PR")
    lines.append("")

    if index_body:
        unresolved, resolved = _extract_threads_from_index(index_body)
        if unresolved:
            lines.append("### Unresolved")
            for item in unresolved:
                lines.append(f"- {item}")
            lines.append("")
        if resolved:
            lines.append("### Resolved")
            for item in resolved:
                lines.append(f"- {item}")
            lines.append("")
        lines.append(f"Full index: {index_url}")
    else:
        lines.append("_No review thread index found yet._")
        lines.append("")

    # Always include the instruction
    lines.append("### Instructions")
    lines.append("")
    lines.append(
        "Do not intentionally re-raise these issues unless you have new "
        "evidence, the problem reappears in a materially different form, "
        "or the previous resolution is directly contradicted by the "
        "current code."
    )
    lines.append("")

    output = "\n".join(lines)
    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Reviewer context written to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
