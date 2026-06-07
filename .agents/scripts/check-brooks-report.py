#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
"""
Validate a brooks-lint / slop review report against template-driven output format.

Asserts positively that the report conforms to the required structure:
   1. At least one valid finding label
   2. At least one file:line reference (evidence of source examination)
   3. A Health Score mention
   4. Not trivially short
   5. All Mermaid diagrams pass syntax validation (via maid)

Usage:
    uv run .agents/scripts/check-brooks-report.py <result.json>
    uv run .agents/scripts/check-brooks-report.py <result.json> --verbose
"""

import json
import re
import subprocess
import sys
from pathlib import Path

# Finding labels across all templates: brooks-lint and slop
FINDING_LABEL = re.compile(r"\[(PR BLOCKER|SHOULD FILE ISSUE|NOTE|SLOP|SLOP SUSPECT)\]")

# File-path-with-line evidence: something like "path/to/file.py:42"
FILE_PATH = re.compile(r"[a-zA-Z0-9_\-./]+\.\w+:\d+")

# Health Score mention
HEALTH_SCORE = re.compile(r"Health\s+Score", re.IGNORECASE)

MIN_CHARS = 200

# Mermaid block delimiter
MERMAID_BLOCK = re.compile(r"```mermaid\n(.+?)\n```", re.DOTALL)


def _validate_mermaid(block: str) -> list[str]:
    """Validate a single Mermaid diagram via maid. Returns errors, empty = pass."""
    try:
        result = subprocess.run(
            ["npx", "@probelabs/maid", "--format", "json", "-"],
            input=block,
            capture_output=True,
            text=True,
            timeout=30,
        )
        parsed = json.loads(result.stdout)
        if not parsed.get("valid", False):
            return [parsed.get("error", "unknown error")]
        return []
    except subprocess.TimeoutExpired:
        return ["maid timed out"]
    except (json.JSONDecodeError, FileNotFoundError, OSError) as e:
        return [f"maid invocation failed: {e}"]


def collect_violations(report: str) -> list[str]:
    """Return a list of human-readable violation strings. Empty list = pass."""
    violations: list[str] = []

    stripped = report.strip()
    if not stripped:
        violations.append("Report is empty")
        return violations

    if len(stripped) < MIN_CHARS:
        violations.append(
            f"Report is too short ({len(stripped)} chars, minimum {MIN_CHARS})"
        )

    if not FINDING_LABEL.search(stripped):
        violations.append(
            "No finding label found — expected at least one of "
            "[PR BLOCKER], [SHOULD FILE ISSUE], [NOTE], [SLOP], [SLOP SUSPECT]"
        )

    if not HEALTH_SCORE.search(stripped):
        violations.append("No Health Score mention found")

    if not FILE_PATH.search(stripped):
        violations.append(
            "No file:line reference found (e.g. path/to/file.py:42) — "
            "evidence of actual source examination is required"
        )

    # Validate Mermaid diagrams
    for idx, match in enumerate(MERMAID_BLOCK.finditer(stripped), start=1):
        errors = _validate_mermaid(match.group(1))
        if errors:
            violations.append(
                f"Mermaid diagram #{idx} has syntax errors: {'; '.join(errors)}"
            )

    return violations


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: uv run .agents/scripts/check-brooks-report.py <result.json>")
        sys.exit(1)

    verbose = "--verbose" in sys.argv
    result_path = Path(sys.argv[1])

    if not result_path.exists():
        print(f"Result file not found: {result_path}")
        sys.exit(1)

    with open(result_path) as f:
        data = json.load(f)

    report = data.get("report", "")
    score = data.get("score")

    if verbose:
        print(f"Score: {score}")
        print(f"Report length: {len(report)} chars")
        print()

    violations = collect_violations(report)

    if not violations:
        if verbose:
            print("Report validation PASSED")
        sys.exit(0)

    print(f"Report validation FAILED ({len(violations)} violation(s)):")
    print()
    for v in violations:
        print(f"  - {v}")
    print()
    print("The report was NOT posted. Fix the agent output and re-run.")
    sys.exit(1)


if __name__ == "__main__":
    main()
