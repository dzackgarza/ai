# /// script
# requires-python = ">=3.11"
# ///
"""
Review report validator: validates candidate JSON artifacts against
a review-type-specific schema loaded from reviews/<report_type>/schema.json.

Type-agnostic — the schema defines which fields are required per finding,
which markers must appear in the human-readable report, and which content
patterns to reject.
"""

import json
import pathlib
import re
import subprocess
import sys
from pathlib import Path

HERE = pathlib.Path(__file__).parent.resolve()
REVIEWS_DIR = HERE / "reviews"

# Infrastructure paths that are forbidden as findings
INFRA_PREFIXES = [
    ".github/",
    ".agents/",
    "quality-control/",
    "opencode/skills/",
]

REQUIRED_TOP_LEVEL_KEYS = [
    "schema_version",
    "repo_sha",
    "review_scope",
    "findings",
    "checked_surfaces",
    "score",
    "report",
    "report_type",
]


def is_infra_path(path_str: str) -> bool:
    path_str = path_str.lstrip("./")
    for prefix in INFRA_PREFIXES:
        if path_str.startswith(prefix):
            return True
    return False


def check_file_exists_in_git(path: str, repo_sha: str) -> bool:
    """Check if a file exists in the given git commit."""
    result = subprocess.run(
        ["git", "cat-file", "-e", f"{repo_sha}:{path}"],
        capture_output=True,
    )
    # git cat-file -e exits 0 (exists), 1 (not found), or 128+ (real error)
    if result.returncode >= 2:
        raise RuntimeError(
            f"git cat-file -e {repo_sha}:{path} failed: "
            f"{result.stderr.decode().strip()}"
        )
    return result.returncode == 0


def load_schema(report_type: str) -> dict:
    schema_path = REVIEWS_DIR / report_type / "schema.json"
    if not schema_path.is_file():
        raise RuntimeError(
            f"Unknown review type '{report_type}': no schema at {schema_path}"
        )
    with open(schema_path) as f:
        return json.load(f)


def validate_finding(finding: dict, idx: int, repo_sha: str, schema: dict) -> list[str]:
    violations = []
    required_fields = schema.get("finding_required_fields", [])

    for field in required_fields:
        if field not in finding:
            violations.append(f"Finding #{idx} missing field: {field}")

    if violations:
        return violations

    tier = finding.get("tier")
    if tier not in ["tier1", "tier2"]:
        violations.append(f"Finding #{idx} has invalid tier: {tier}")

    forbidden_categories = schema.get("forbidden_categories", [])
    category = str(finding.get("category", "")).lower()
    for forbidden in forbidden_categories:
        if forbidden in category:
            violations.append(f"Finding #{idx} has forbidden category: {category}")

    location = finding.get("location", {})
    path = location.get("path", "")
    if not path:
        violations.append(f"Finding #{idx} location missing path")
    else:
        if is_infra_path(path):
            violations.append(
                f"Finding #{idx} on {path} is forbidden: no meta/infrastructure findings allowed"
            )
        if not check_file_exists_in_git(path, repo_sha):
            violations.append(
                f"Finding #{idx} cites non-existent path in commit {repo_sha}: {path}"
            )

    evidence = finding.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        violations.append(
            f"Finding #{idx} missing evidence of inspection (e.g. file-read evidence)"
        )

    return violations


def validate_report_content(report: str, schema: dict) -> list[str]:
    """Validate that the human-readable report field contains the required markers."""
    violations = []
    report_min_length = schema.get("report_min_length", 200)

    if not report or len(report.strip()) < report_min_length:
        violations.append(
            "The 'report' field is too short or empty. Provide full substantive analysis."
        )
        return violations

    markers = schema.get("report_required_markers", [])
    for marker in markers:
        if not re.search(marker, report, re.IGNORECASE):
            violations.append(
                f"Mandatory marker '{marker.replace(r'\\s+', ' ')}' not found in report field. "
                "You must provide detailed analysis for at least one finding."
            )

    reject_patterns = schema.get("report_reject_patterns", [])
    for pattern in reject_patterns:
        if re.search(pattern, report, re.IGNORECASE):
            violations.append(
                f"Finding rejected: report contains prohibited pattern '{pattern}'. "
                "Remove this content from the report."
            )

    return violations


def collect_violations(data: dict) -> list[str]:
    violations: list[str] = []

    if not isinstance(data, dict):
        return ["Root must be a JSON object"]

    for key in REQUIRED_TOP_LEVEL_KEYS:
        if key not in data:
            violations.append(f"Missing required field: {key}")

    if violations:
        return violations

    repo_sha = data.get("repo_sha", "")
    report_type = data.get("report_type", "")
    findings = data.get("findings", [])
    report_text = data.get("report", "")

    if not isinstance(findings, list):
        violations.append("findings must be a list")
    else:
        has_tier1 = any(
            f.get("tier") == "tier1" for f in findings if isinstance(f, dict)
        )
        has_tier2 = any(
            f.get("tier") == "tier2" for f in findings if isinstance(f, dict)
        )

        if has_tier1 and has_tier2:
            violations.append(
                "Tier 2 findings are not allowed if any Tier 1 findings exist. "
                "Clean the significant issues first."
            )

    try:
        schema = load_schema(report_type)
    except RuntimeError as e:
        violations.append(str(e))
        return violations

    if isinstance(findings, list):
        for idx, finding in enumerate(findings):
            violations.extend(validate_finding(finding, idx, repo_sha, schema))

    violations.extend(validate_report_content(report_text, schema))

    if not findings and len(data.get("checked_surfaces", [])) == 0:
        violations.append(
            "Report has zero findings AND zero checked surfaces. "
            "Provide evidence of actual repository scanning."
        )

    return violations


def main() -> None:
    if len(sys.argv) < 2:
        print(f"Usage: uv run {sys.argv[0]} <result.json>")
        sys.exit(1)

    result_path = Path(sys.argv[1])
    if not result_path.is_file():
        print(f"Error: file not found: {result_path}", file=sys.stderr)
        sys.exit(1)

    with open(result_path) as f:
        data = json.load(f)

    violations = collect_violations(data)

    if not violations:
        print("Report validation PASSED")
        sys.exit(0)

    print(f"Report validation FAILED ({len(violations)} violation(s)):")
    for v in violations:
        print(f"  - {v}")

    print("\nERROR: Your report failed validation.")
    sys.exit(1)


if __name__ == "__main__":
    main()
