#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
"""
Validate a brooks-lint / slop review candidate report.

Asserts positively that the report conforms to the required structured JSON format
AND that the markdown 'report' field contains the mandatory Brooks-Lint markers.
"""

import json
import sys
import os
import subprocess
import re
from pathlib import Path

# Infrastructure paths that are forbidden as findings
INFRA_PREFIXES = [
    ".github/",
    ".agents/",
    "quality-control/",
    "opencode/",
    ".opencode/",
    ".serena/",
    ".claude/",
    ".git/",
    "nginx.conf",
    ".envrc",
    "justfile",
    "home-justfile",
    "pyproject.toml",
    "package.json",
    "package-lock.json",
    "uv.lock",
    ".gitignore",
]

FORBIDDEN_CATEGORIES = [
    "meta",
    "infrastructure",
    "ci-workflow",
    "agent-config",
    "harness",
    "environment",
]

# Mandatory markers for the markdown report field
MANDATORY_MARKERS = [
    r"Finding\s+\d+",
    r"Symptom:",
    r"Source:",
    r"Consequence:",
    r"Remedy:",
]

def is_infra_path(path_str: str) -> bool:
    path_str = path_str.lstrip("./")
    for prefix in INFRA_PREFIXES:
        if path_str.startswith(prefix):
            return True
    return False

def check_file_exists_in_git(path: str, repo_sha: str) -> bool:
    """Check if a file exists in the given git commit."""
    try:
        # We check current working directory (which should be the repo root)
        subprocess.run(
            ["git", "cat-file", "-e", f"{repo_sha}:{path}"],
            capture_output=True,
            check=True
        )
        return True
    except Exception:
        # Fallback to local check if git fails (e.g. shallow clone without that SHA)
        return Path(path).exists()

def validate_finding(finding: dict, idx: int, repo_sha: str, report_type: str) -> list[str]:
    violations = []
    
    if report_type == "slop":
        required_fields = ["tier", "label", "category", "location", "pattern", "task_narrative", "slop_narrative", "why_it_matters", "user_surprise", "existential_justification", "failure_mode", "evidence"]
    else:
        required_fields = ["tier", "label", "category", "location", "symptom", "source", "consequence", "remedy", "evidence"]

    for field in required_fields:
        if field not in finding:
            violations.append(f"Finding #{idx} missing field: {field}")
    
    if violations:
        return violations

    tier = finding.get("tier")
    if tier not in ["tier1", "tier2"]:
        violations.append(f"Finding #{idx} has invalid tier: {tier}")

    category = str(finding.get("category", "")).lower()
    for forbidden in FORBIDDEN_CATEGORIES:
        if forbidden in category:
            violations.append(f"Finding #{idx} has forbidden category: {category}")

    location = finding.get("location")
    if not isinstance(location, dict):
        violations.append(f"Finding #{idx} location must be a dict")
    else:
        path = location.get("path")
        if not path:
            violations.append(f"Finding #{idx} location missing path")
        else:
            if is_infra_path(path):
                violations.append(f"Finding #{idx} on {path} is forbidden: no meta/infrastructure findings allowed")
            if not check_file_exists_in_git(path, repo_sha):
                violations.append(f"Finding #{idx} cites non-existent path in commit {repo_sha}: {path}")

    evidence = finding.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        violations.append(f"Finding #{idx} missing evidence of inspection (e.g. file-read evidence)")

    return violations

def validate_report_content(report: str, report_type: str) -> list[str]:
    """Validate that the human-readable report field contains the required markers."""
    violations = []
    
    if not report or len(report.strip()) < 200:
        violations.append("The 'report' field is too short or empty. Provide full substantive analysis.")
        return violations

    if report_type == "slop":
        markers = [
            r"Finding\s+\d+",
            r"Pattern:",
            r"Concrete evidence:",
            r"Original requested task narrative:",
            r"Descent into slop narrative:",
            r"Why this matters:",
            r"User surprise analysis:",
            r"Existential justification:",
            r"Failure mode:"
        ]
    else:
        markers = [
            r"Finding\s+\d+",
            r"Symptom:",
            r"Source:",
            r"Consequence:",
            r"Remedy:",
        ]

    for marker in markers:
        if not re.search(marker, report, re.IGNORECASE):
            violations.append(f"Mandatory marker '{marker.replace(r'\\s+', ' ')}' not found in report field. You must provide detailed analysis for at least one finding.")
            
    # REJECT CARGO CULT -O FINDINGS
    if "-O" in report or "optimized mode" in report.lower():
        violations.append("Finding rejected: We do NOT care about Python's optimized mode (-O). It is a trivial concern and we never run Python that way. Remove this cargo-cult finding.")

    return violations

def collect_violations(data: dict) -> list[str]:
    violations: list[str] = []

    if not isinstance(data, dict):
        return ["Root must be a JSON object"]

    required_keys = ["schema_version", "repo_sha", "review_scope", "findings", "checked_surfaces", "score", "report", "report_type"]
    for key in required_keys:
        if key not in data:
            violations.append(f"Missing required field: {key}")

    if violations:
        return violations

    repo_sha = data["repo_sha"]
    findings = data["findings"]
    report_text = data.get("report", "")
    report_type = data.get("report_type", "brooks")
    
    if not isinstance(findings, list):
        violations.append("findings must be a list")
    else:
        has_tier1 = any(f.get("tier") == "tier1" for f in findings if isinstance(f, dict))
        has_tier2 = any(f.get("tier") == "tier2" for f in findings if isinstance(f, dict))
        
        if has_tier1 and has_tier2:
            violations.append("Tier 2 findings are not allowed if any Tier 1 findings exist. Clean the significant issues first.")

        for idx, finding in enumerate(findings):
            violations.extend(validate_finding(finding, idx, repo_sha, report_type))

    # SUBSTANTIVE CONTENT CHECK
    violations.extend(validate_report_content(report_text, report_type))

    if not findings and len(data.get("checked_surfaces", [])) == 0:
        violations.append("Report has zero findings AND zero checked surfaces. Provide evidence of actual repository scanning.")

    return violations

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: uv run check-brooks-report.py <result.json>")
        sys.exit(1)

    result_path = Path(sys.argv[1])
    if not result_path.exists():
        print(f"Result file not found: {result_path}")
        sys.exit(1)

    try:
        with open(result_path) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Report validation FAILED (Invalid JSON): {e}")
        sys.exit(1)

    violations = collect_violations(data)

    if not violations:
        print("Report validation PASSED")
        sys.exit(0)

    print(f"Report validation FAILED ({len(violations)} violation(s)):")
    for v in violations:
        print(f"  - {v}")
    
    print("\nERROR: Your report is hollow or missing mandatory Brooks-Lint template markers.")
    print("You must review the template provided in the task and return a fully compliant report")
    print("that includes 'Finding X', 'Symptom:', 'Source:', 'Consequence:', and 'Remedy:' sections.")
    
    sys.exit(1)

if __name__ == "__main__":
    main()
