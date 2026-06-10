# /// script
# requires-python = ">=3.11"
# ///
"""
Post validated review findings as a single GitHub PR review.

Reads a validated GeneralReport/SlopReport artifact JSON and submits
one PR review with each finding as an inline review comment.

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


def _build_review_body(artifact: dict) -> str:
    """Build a short review body header from the artifact."""
    findings = artifact.get("findings", [])
    total = len(findings)
    tier1 = sum(1 for f in findings if f.get("tier") == "tier1")
    tier2 = sum(1 for f in findings if f.get("tier") == "tier2")
    report_type = artifact.get("report_type", "review")
    sha = artifact.get("repo_sha", "unknown")

    header = f"{report_type.capitalize()} review run\n\n"
    header += f"Commit: `{sha}`\n"
    header += f"Findings: {total}\n"
    header += f"Tier 1: {tier1}\n"
    header += f"Tier 2: {tier2}"
    return header


def _post_review(
    repo: str,
    pr_number: int,
    commit_sha: str,
    body: str,
    comments: list[dict],
    dry_run: bool,
) -> dict:
    """Submit one PR review with inline comments via gh API.

    Returns the API response dict.
    On dry_run, prints the payload and returns a placeholder.
    """
    payload = {
        "commit_id": commit_sha,
        "body": body,
        "event": "COMMENT",
        "comments": comments,
    }

    if dry_run:
        print(json.dumps(payload, indent=2))
        return {
            "id": 0,
            "html_url": "<dry-run>",
        }

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(payload, f)
        tmp_path = f.name

    try:
        result = subprocess.run(
            [
                "gh",
                "api",
                f"repos/{repo}/pulls/{pr_number}/reviews",
                "--method",
                "POST",
                "--input",
                tmp_path,
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            _fail(f"Failed to post review: {result.stderr.strip()}")
        return json.loads(result.stdout)
    finally:
        os.unlink(tmp_path)


def _fetch_review_comments(repo: str, pr_number: int, review_id: int) -> list[dict]:
    """Fetch inline comments for a submitted review."""
    result = subprocess.run(
        [
            "gh",
            "api",
            f"repos/{repo}/pulls/{pr_number}/reviews/{review_id}/comments",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(
            f"  WARNING: Failed to fetch review comments: {result.stderr.strip()}",
            file=sys.stderr,
        )
        return []
    return json.loads(result.stdout)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Post validated review findings as a single GitHub PR review"
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

    comments: list[dict] = []
    unthreadable_indices: list[int] = []

    for i, finding in enumerate(findings):
        loc = finding.get("location", {})
        loc_path = loc.get("path", "")
        start_line = loc.get("start_line", 0)
        end_line = loc.get("end_line", start_line)

        if not loc_path or not start_line:
            unthreadable_indices.append(i)
            continue

        comment: dict = {
            "path": loc_path,
            "body": _get_finding_body(args.artifact, i),
            "side": "RIGHT",
        }

        if end_line > start_line:
            comment["start_line"] = start_line
            comment["start_side"] = "RIGHT"
            comment["line"] = end_line
        else:
            comment["line"] = start_line

        comments.append(comment)

        print(
            f"Queued finding {i}: {finding.get('label', '?')} on {loc_path}:{start_line}"
        )

    review_body = _build_review_body(artifact)

    print(f"\nSubmitting review with {len(comments)} inline comments...")

    response = _post_review(
        repo=args.repo,
        pr_number=args.pr_number,
        commit_sha=head_sha,
        body=review_body,
        comments=comments,
        dry_run=args.dry_run,
    )

    review_id = response.get("id")
    review_url = response.get("html_url")

    # Fetch inline comment IDs for the summary
    posted_comments: list[dict] = []
    if not args.dry_run and review_id:
        inline_comments = _fetch_review_comments(args.repo, args.pr_number, review_id)
        for idx, ic in enumerate(inline_comments):
            if idx < len(comments):
                posted_comments.append(
                    {
                        "index": idx,
                        "path": ic.get("path", ""),
                        "line": ic.get("line", 0),
                        "url": ic.get("html_url", ""),
                        "id": ic.get("id", 0),
                    }
                )

    # Summary
    print()
    print("=" * 60)
    print(f"Review submitted: {review_url or '<dry-run>'}")
    print(f"Review ID:       {review_id or 0}")
    print(f"Findings posted: {len(comments)}")
    print(f"Unthreadable:    {len(unthreadable_indices)}")
    print()

    if unthreadable_indices:
        print("Unthreadable findings (not posted as review comments):")
        for i in unthreadable_indices:
            f = findings[i]
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
        "review_id": review_id,
        "review_url": review_url,
        "finding_count": len(findings),
        "posted_count": len(comments),
        "unthreadable_count": len(unthreadable_indices),
        "comments": posted_comments if posted_comments else None,
    }
    summary_path = Path(".review-thread-summary.json")
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nSummary written to {summary_path}")

    if not comments and findings:
        print(
            "FATAL: No findings could be posted as review comments. "
            "This may indicate an authentication or API issue (GH_TOKEN, rate limits, permissions).",
            file=sys.stderr,
        )
        sys.exit(1)

    if unthreadable_indices:
        print(
            "WARNING: Some findings could not be posted as review comments. "
            "They are listed above.",
            file=sys.stderr,
        )

    sys.exit(0)


if __name__ == "__main__":
    main()
