# /// script
# requires-python = ">=3.11"
# ///
"""
Post validated review findings as individual GitHub PR review threads.

Reads a validated GeneralReport/SlopReport artifact JSON and posts each
finding as a separate PR review comment (thread) via the GitHub REST API.

Usage:
  uv run quality-control/ci/post-validated-findings-as-review-threads.py \
    --artifact .review-report-artifact.json \
    --pr-number 123 \
    --repo owner/repo \
    [--dry-run]
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


def _fail(msg: str) -> None:
    print(f"FATAL: {msg}", file=sys.stderr)
    sys.exit(1)


def _check_gh(dry_run: bool) -> None:
    """Verify gh CLI and GH_TOKEN are available (skipped in dry-run)."""
    if dry_run:
        return
    if "GH_TOKEN" not in os.environ:
        _fail("GH_TOKEN environment variable is required")
    result = subprocess.run(
        ["gh", "--version"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        _fail("gh CLI is not available")


def _get_pr_head_sha(repo: str, pr_number: int) -> str:
    """Get the PR head commit SHA via gh API."""
    result = subprocess.run(
        ["gh", "api", f"repos/{repo}/pulls/{pr_number}", "--jq", ".head.sha"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        _fail(f"Failed to get PR head SHA: {result.stderr.strip()}")
    sha = result.stdout.strip()
    if not sha or len(sha) != 40:
        _fail(f"Invalid PR head SHA: {sha}")
    return sha


def _read_artifact(path: Path) -> dict:
    """Read and validate the artifact JSON."""
    if not path.is_file():
        _fail(f"Artifact not found: {path}")
    with open(path) as f:
        data = json.load(f)
    if "findings" not in data:
        _fail(f"Artifact {path} has no 'findings' key")
    if not isinstance(data["findings"], list):
        _fail(f"Artifact {path} 'findings' is not a list")
    return data


def _get_finding_body(path: Path, index: int) -> str:
    """Get rendered finding body via check-report.py finding-body subcommand."""
    checker = Path(__file__).resolve().parent.parent / "check-report.py"
    result = subprocess.run(
        ["uv", "run", str(checker), "finding-body", str(path), "--index", str(index)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        _fail(
            f"check-report.py finding-body failed for index {index}: "
            f"{result.stderr.strip()}"
        )
    return result.stdout.strip()


def _post_review_comment(
    repo: str,
    pr_number: int,
    commit_sha: str,
    path: str,
    line: int,
    body: str,
    dry_run: bool,
) -> dict | None:
    """Post a single PR review comment via gh API.

    Returns the API response dict on success, None on failure.
    On dry_run, prints what would be posted and returns a placeholder.
    """
    payload = {
        "body": body,
        "commit_id": commit_sha,
        "path": path,
        "line": line,
        "side": "RIGHT",
    }

    if dry_run:
        print(f"  [DRY RUN] Would post review comment on {path}:{line}")
        return {"html_url": f"<dry-run: {path}:{line}>"}

    # Write payload to a temp file to avoid shell escaping issues
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(payload, f)
        tmp_path = f.name

    try:
        result = subprocess.run(
            [
                "gh",
                "api",
                f"repos/{repo}/pulls/{pr_number}/comments",
                "--method",
                "POST",
                "--input",
                tmp_path,
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            stderr = result.stderr.strip()
            print(
                f"  WARNING: Failed to post comment on {path}:{line}: {stderr}",
                file=sys.stderr,
            )
            return None
        return json.loads(result.stdout)
    finally:
        os.unlink(tmp_path)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Post validated review findings as GitHub PR review threads"
    )
    parser.add_argument(
        "--artifact",
        required=True,
        type=Path,
        help="Path to validated artifact JSON",
    )
    parser.add_argument(
        "--pr-number",
        required=True,
        type=int,
        help="Pull request number",
    )
    parser.add_argument(
        "--repo",
        required=True,
        help="Repository in owner/repo format",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be posted without making API calls",
    )
    args = parser.parse_args()

    _check_gh(dry_run=args.dry_run)

    artifact = _read_artifact(args.artifact)
    findings = artifact["findings"]

    if not findings:
        print("No findings to post.")
        sys.exit(0)

    head_sha = (
        artifact.get("repo_sha", "dry-run-sha")
        if args.dry_run
        else _get_pr_head_sha(args.repo, args.pr_number)
    )

    posted: list[dict] = []
    unthreadable: list[dict] = []

    for i, finding in enumerate(findings):
        loc = finding.get("location", {})
        loc_path = loc.get("path", "")
        start_line = loc.get("start_line", 0)

        if not loc_path or not start_line:
            unthreadable.append(finding)
            continue

        body = _get_finding_body(args.artifact, i)

        print(
            f"Posting finding {i}: {finding.get('label', '?')} on {loc_path}:{start_line}"
        )

        response = _post_review_comment(
            repo=args.repo,
            pr_number=args.pr_number,
            commit_sha=head_sha,
            path=loc_path,
            line=start_line,
            body=body,
            dry_run=args.dry_run,
        )

        if response is None:
            unthreadable.append(finding)
        else:
            posted.append(
                {
                    "index": i,
                    "label": finding.get("label", ""),
                    "path": loc_path,
                    "line": start_line,
                    "url": response.get("html_url", ""),
                    "id": response.get("id", 0),
                }
            )

    # Summary
    print()
    print("=" * 60)
    print(f"Threads posted: {len(posted)}")
    print(f"Unthreadable:   {len(unthreadable)}")
    print()

    if posted:
        print("Posted threads:")
        for p in posted:
            print(f"  {p['url']} -- {p['label']} on {p['path']}:{p['line']}")

    if unthreadable:
        print("Unthreadable findings (not posted as review threads):")
        for f in unthreadable:
            loc = f.get("location", {})
            print(
                f"  {f.get('label', '?')} at "
                f"{loc.get('path', '?')}:{loc.get('start_line', '?')}"
            )

    # Write summary artifact for downstream use
    summary = {
        "repo": args.repo,
        "pr_number": args.pr_number,
        "commit_sha": head_sha,
        "posted": posted,
        "unthreadable_count": len(unthreadable),
        "unthreadable_labels": [f.get("label", "") for f in unthreadable],
    }
    summary_path = Path(".review-thread-summary.json")
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nSummary written to {summary_path}")

    if not posted and findings:
        print(
            "FATAL: No findings could be posted as review threads. "
            "This may indicate an authentication or API issue (GH_TOKEN, rate limits, permissions).",
            file=sys.stderr,
        )
        sys.exit(1)

    if unthreadable:
        print(
            "WARNING: Some findings could not be posted as review threads. "
            "They are listed above.  The gardener agent should process them.",
            file=sys.stderr,
        )

    sys.exit(0)


if __name__ == "__main__":
    main()
