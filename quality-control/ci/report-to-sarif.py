# /// script
# requires-python = ">=3.11"
# ///
"""
Convert a validated review report artifact to SARIF 2.1.0 for upload
as GitHub code scanning alerts.

Usage:
  uv run quality-control/ci/report-to-sarif.py \
    --artifact .review-report-artifact.json \
    --output .review-report.sarif

The category is derived from the report_type field in the artifact:
  "general" -> "ai-general-review"
  "slop"    -> "ai-slop-review"

Each finding becomes one SARIF result.  The partialFingerprint is a
deterministic hash of (category, label, path) — stable across line shifts
so the same finding maps to the same code scanning alert across runs.
"""

import hashlib
import json
import sys
from pathlib import Path

SARIF_VERSION = "2.1.0"
SARIF_SCHEMA = (
    "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/"
    "master/Schemata/sarif-schema-2.1.0.json"
)

CATEGORY_PREFIX = "ai-review"


def _tool_name(report_type: str) -> str:
    return f"{CATEGORY_PREFIX}/{report_type}"


def _category(report_type: str) -> str:
    return report_type


def _tier_to_level(tier: str) -> str:
    return "error" if tier == "tier1" else "warning"


def _fingerprint(category: str, label: str, path: str) -> dict[str, str]:
    """Deterministic hash for alert identity.  Stable across line shifts.

    Components: category + label + path.
    No line numbers, no timestamps, no commit SHAs.
    """
    raw = "|".join([category, label, path])
    h = hashlib.sha256(raw.encode()).hexdigest()
    return {"reviewFindingKey": h}


def _build_artifact(artifact: dict, report_type: str) -> dict:
    findings: list[dict] = artifact.get("findings", [])
    run_sha = artifact.get("repo_sha", "?")

    # Rules — deduplicated by category
    seen_rules: dict[str, int] = {}
    rules: list[dict] = []
    results: list[dict] = []

    for finding in findings:
        category = finding.get("category", "?")
        label = finding.get("label", "?")
        tier = finding.get("tier", "tier2")
        violated = finding.get("violated_invariant", "")
        loc = finding.get("location", {})
        loc_path = loc.get("path", "?")
        start_line = loc.get("start_line", 1)
        end_line = loc.get("end_line", start_line)

        # Register rule if new
        if category not in seen_rules:
            rule_index = len(rules)
            seen_rules[category] = rule_index
            rules.append(
                {
                    "id": category,
                    "name": label,
                    "shortDescription": {"text": violated[:200] if violated else label},
                    "defaultConfiguration": {"level": _tier_to_level(tier)},
                }
            )
        else:
            rule_index = seen_rules[category]

        # Build location properties
        location_props: dict = {
            "uri": loc_path,
            "uriBaseId": "%ROOT%",
        }

        region: dict = {}
        if start_line:
            region["startLine"] = start_line
        if end_line and end_line != start_line:
            region["endLine"] = end_line

        result: dict = {
            "ruleId": category,
            "ruleIndex": rule_index,
            "level": _tier_to_level(tier),
            "message": {"text": violated},
            "locations": [
                {
                    "physicalLocation": {
                        "artifactLocation": location_props,
                        "region": region,
                    }
                }
            ],
            "partialFingerprints": _fingerprint(category, label, loc_path),
            "properties": {
                "label": label,
                "tier": tier,
                "category": category,
            },
        }

        # Include narrative fields if present (general review)
        if "symptom" in finding:
            result["properties"]["symptom"] = finding["symptom"]
        if "consequence" in finding:
            result["properties"]["consequence"] = finding["consequence"]
        if "remedy" in finding:
            result["properties"]["remedy"] = finding["remedy"]
        if "proof_command" in finding:
            result["properties"]["proof_command"] = finding["proof_command"]

        # Slop-specific fields
        if "pattern" in finding:
            result["properties"]["slop_pattern"] = finding["pattern"]
        if "why_it_matters" in finding:
            result["properties"]["why_it_matters"] = finding["why_it_matters"]

        results.append(result)

    return {
        "$schema": SARIF_SCHEMA,
        "version": SARIF_VERSION,
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": _tool_name(report_type),
                        "informationUri": "https://github.com/dzackgarza/ai",
                        "rules": rules,
                    }
                },
                "automationDetails": {
                    "id": _category(report_type),
                },
                "results": results,
                "originalUriBaseIds": {
                    "%ROOT%": {"uri": "file:///github/workspace/"},
                },
                "properties": {
                    "repo_sha": run_sha,
                    "report_type": report_type,
                },
            }
        ],
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="Convert review report artifact to SARIF 2.1.0"
    )
    parser.add_argument(
        "--artifact",
        required=True,
        type=Path,
        help="Path to validated .review-report-artifact.json",
    )
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Path to write .review-report.sarif",
    )
    args = parser.parse_args()

    if not args.artifact.is_file():
        print(f"FATAL: artifact not found: {args.artifact}", file=sys.stderr)
        sys.exit(1)

    with open(args.artifact) as f:
        artifact = json.load(f)

    report_type = artifact.get("report_type", "")
    if report_type not in ("general", "slop"):
        print(
            f"FATAL: unknown report_type '{report_type}' in artifact",
            file=sys.stderr,
        )
        sys.exit(1)

    sarif = _build_artifact(artifact, report_type)

    with open(args.output, "w") as f:
        json.dump(sarif, f, indent=2)

    n = len(sarif["runs"][0]["results"])
    print(f"SARIF written to {args.output} ({n} findings)")


if __name__ == "__main__":
    main()
