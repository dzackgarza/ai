# /// script
# requires-python = ">=3.11"
# dependencies = ["cyclopts"]
# ///
"""
Reconcile a freshly-rendered review comment against prior bot comments on the PR.

Computes stable finding IDs from artifact fields, classifies each finding as
new/repeated/changed/disappeared, and rewrites the PR comment with lineage
annotations and hidden metadata for future reconciliation.

Usage:
  uv run reconcile-review-comment.py --artifact .review-report-artifact.json \
      --comment .review-report-comment.md --pr-number 6

Expects GH_TOKEN env var for gh CLI auth.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from cyclopts import App

app = App(
    name="reconcile-review-comment",
    help="Reconcile review comment with prior PR bot comments.",
)

HIDDEN_META_RE = re.compile(
    r"<!-- review-report:v1\n(.*?)-->", re.DOTALL | re.MULTILINE
)


def _compute_finding_id(
    finding: dict,
    report_type: str,
    repo_sha: str,
) -> str:
    """Stable hash-based finding identifier."""
    loc = finding.get("location", {})
    key = hashlib.sha256(
        "|".join(
            [
                report_type,
                repo_sha,
                str(loc.get("path", "")),
                str(loc.get("start_line", "")),
                str(loc.get("end_line", "")),
                (finding.get("violated_invariant", "") or "").strip().lower(),
                (finding.get("proof_command", "") or "").strip().lower(),
            ]
        ).encode()
    ).hexdigest()[:12]
    return f"ID-{key}"


def _fetch_prior_comments(pr_number: int, repo: str) -> list[dict]:
    """Fetch all comments on the PR via gh API."""
    result = subprocess.run(
        [
            "gh",
            "api",
            f"repos/{repo}/issues/{pr_number}/comments",
            "--paginate",
            "--jq",
            ".[] | {body: .body, id: .id, created_at: .created_at}",
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode != 0:
        print(f"Warning: gh API failed: {result.stderr.strip()}", file=sys.stderr)
        return []

    comments = []
    for line in result.stdout.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        try:
            comments.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return comments


def _extract_metadata(comment_body: str) -> dict | None:
    """Parse hidden metadata block from a prior comment."""
    m = HIDDEN_META_RE.search(comment_body)
    if not m:
        return None

    meta = {}
    for line in m.group(1).strip().split("\n"):
        line = line.strip()
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        meta[key.strip()] = value.strip()

    finding_ids_str = meta.get("finding_ids", "")
    if finding_ids_str:
        ids = {}
        for entry in finding_ids_str.split(","):
            entry = entry.strip()
            if ":" in entry:
                fid, status = entry.split(":", 1)
                ids[fid.strip()] = status.strip()
        meta["finding_ids"] = ids
    else:
        meta["finding_ids"] = {}

    return meta


def _classify_findings(
    current_ids: dict[str, dict],
    prior_metadata_list: list[dict],
) -> dict[str, str]:
    """Classify each finding ID: new, repeated, changed, disappeared."""
    prior_by_run = [meta.get("finding_ids", {}) for meta in prior_metadata_list]
    latest_prior_ids = set(prior_by_run[0].keys()) if prior_by_run else set()
    all_prior_ids = set()
    for m in prior_by_run:
        all_prior_ids.update(m.keys())

    current_id_set = set(current_ids.keys())
    classifications = {}

    for fid in current_id_set:
        if fid in latest_prior_ids:
            classifications[fid] = "repeated"
        elif fid in all_prior_ids:
            classifications[fid] = "changed"
        else:
            classifications[fid] = "new"

    for fid in latest_prior_ids:
        if fid not in current_id_set:
            classifications[fid] = "disappeared"

    return classifications


def _rewrite_comment(
    fresh_comment: str,
    artifact: dict,
    classifications: dict[str, str],
) -> str:
    """Inject finding IDs and lineage annotations into the rendered comment."""
    report_type = artifact.get("report_type", "unknown")
    repo_sha = artifact.get("repo_sha", "unknown")
    findings = artifact.get("findings", [])

    finding_id_map = {}
    for f in findings:
        fid = _compute_finding_id(f, report_type, repo_sha)
        f["_finding_id"] = fid
        finding_id_map[fid] = f

    finding_ids_str = ",".join(
        f"{fid}:{classifications.get(fid, 'new')}" for fid in finding_id_map
    )
    meta_block = (
        "<!-- review-report:v1\n"
        f"report_type={report_type}\n"
        f"repo_sha={repo_sha}\n"
        f"finding_ids={finding_ids_str}\n"
        "-->\n"
    )

    lineage_lines = ["", "## Finding Lineage", ""]
    status_counts: dict[str, int] = {}
    for fid, status in classifications.items():
        status_counts[status] = status_counts.get(status, 0) + 1

    parts = []
    for s in ["new", "repeated", "changed", "disappeared"]:
        cnt = status_counts.get(s, 0)
        if cnt > 0:
            parts.append(f"{cnt} {s}")
    if parts:
        lineage_lines.append(" | ".join(parts) + "")
    lineage_lines.append("")

    lines = fresh_comment.split("\n")
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        finding_match = re.match(r"^(### Finding \d+: .+?)\s*(\(.*?\))?\s*$", line)
        if finding_match:
            finding_num_str = line.split(":")[0].replace("### Finding ", "").strip()
            try:
                finding_num = int(finding_num_str) - 1
                if 0 <= finding_num < len(findings):
                    f = findings[finding_num]
                    fid = f.get("_finding_id", "?")
                    status = classifications.get(fid, "?")
                    status_prefix = {
                        "new": "New",
                        "repeated": "Repeated",
                        "changed": "Changed",
                        "disappeared": "Disappeared",
                    }.get(status, "?")
                    new_lines.append(f"{line.strip()} [{fid}]")
                    new_lines.append("")
                    new_lines.append(f"**Status:** {status_prefix}")
                    new_lines.append("")
                    i += 1
                    continue
            except (ValueError, IndexError):
                pass

        new_lines.append(line)
        i += 1

    result = meta_block + "\n".join(new_lines)

    summary_end = result.find("## Checked Surfaces")
    if summary_end > 0:
        result = result[:summary_end] + "\n".join(lineage_lines) + result[summary_end:]
    else:
        result += "\n".join(lineage_lines)

    return result


@app.command
def reconcile(
    artifact: Path,
    comment: Path,
    pr_number: int,
    repo: str = "dzackgarza/ai",
):
    """Reconcile a freshly-rendered review comment against prior PR comments.

    Args:
        artifact: Path to the validated artifact JSON (.review-report-artifact.json)
        comment: Path to the rendered comment markdown (.review-report-comment.md)
        pr_number: GitHub PR number to check for prior comments.
        repo: GitHub owner/name (default dzackgarza/ai). Set in CI via github.repository.
    """
    if not artifact.is_file():
        print(f"Error: artifact not found: {artifact}", file=sys.stderr)
        sys.exit(1)
    if not comment.is_file():
        print(f"Error: comment not found: {comment}", file=sys.stderr)
        sys.exit(1)
    if not os.environ.get("GH_TOKEN"):
        print("Error: GH_TOKEN env var required", file=sys.stderr)
        sys.exit(1)

    with open(artifact) as f:
        artifact_data = json.load(f)
    with open(comment) as f:
        fresh_comment = f.read()

    report_type = artifact_data.get("report_type", "unknown")
    repo_sha = artifact_data.get("repo_sha", "")

    prior_comments = _fetch_prior_comments(pr_number, repo)

    prior_metadata_list = []
    for pc in prior_comments:
        meta = _extract_metadata(pc.get("body", ""))
        if meta:
            prior_metadata_list.append(meta)

    current_ids = {}
    for f in artifact_data.get("findings", []):
        fid = _compute_finding_id(f, report_type, repo_sha)
        current_ids[fid] = f

    classifications = _classify_findings(current_ids, prior_metadata_list)

    updated_comment = _rewrite_comment(
        fresh_comment,
        artifact_data,
        classifications,
    )

    with open(comment, "w") as f:
        f.write(updated_comment)

    new_count = sum(1 for s in classifications.values() if s == "new")
    repeated_count = sum(1 for s in classifications.values() if s == "repeated")
    changed_count = sum(1 for s in classifications.values() if s == "changed")
    disappeared_count = sum(1 for s in classifications.values() if s == "disappeared")

    parts = []
    if new_count:
        parts.append(f"{new_count} new")
    if repeated_count:
        parts.append(f"{repeated_count} repeated")
    if changed_count:
        parts.append(f"{changed_count} changed")
    if disappeared_count:
        parts.append(f"{disappeared_count} disappeared")
    print(f"findings: {', '.join(parts)}" if parts else "no findings")
    print(f"comment reconciled: {comment}")


if __name__ == "__main__":
    app()
