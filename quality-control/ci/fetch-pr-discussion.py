# /// script
# requires-python = ">=3.11"
# ///
"""
Fetch and dump the full PR discussion state as markdown context for the gardener agent.

Outputs a structured markdown document covering:
- PR metadata (title, body, head SHA, state)
- Issue comments (top-level PR comments)
- Review comments (threaded comments on code)
- Recent commits
- Existing review thread index comment (if present)

Usage:
  uv run quality-control/ci/fetch-pr-discussion.py \
    --pr-number 123 \
    --repo owner/repo
"""

import argparse
import json
import subprocess
import sys


def _fail(msg: str) -> None:
    print(f"FATAL: {msg}", file=sys.stderr)
    sys.exit(1)


def _gh_api(path: str, jq_filter: str | None = None) -> str | bytes:
    """Call gh api and return stdout. Decodes JSON unless jq_filter is set."""
    cmd = ["gh", "api", path]
    if jq_filter:
        cmd.extend(["--jq", jq_filter])
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        _fail(f"gh api {path} failed: {result.stderr.strip()}")
    return result.stdout


def _gh_api_json(path: str) -> list | dict:
    """Call gh api and parse JSON response."""
    raw = _gh_api(path)
    return json.loads(raw)


def _fmt_comment(c: dict) -> str:
    """Format a single comment for the context dump."""
    user = c.get("user", {}).get("login", "unknown")
    created = c.get("created_at", "?")[:10]
    body = c.get("body", "") or ""
    # Truncate very long bodies to keep context manageable
    if len(body) > 2000:
        body = body[:2000] + "\n\n[... truncated ...]"
    return f"- **{user}** ({created}):\n{body}\n"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch and dump PR discussion state for the gardener agent"
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

    lines: list[str] = []

    # ── PR metadata ──────────────────────────────────────────────────
    lines.append("# PR Discussion State")
    lines.append("")
    pr_data = _gh_api_json(f"repos/{repo}/pulls/{pr}")
    lines.append(f"**PR:** [{repo}#{pr}](https://github.com/{repo}/pull/{pr})")
    lines.append(f"**Title:** {pr_data.get('title', '?')}")
    lines.append(f"**State:** {pr_data.get('state', '?')}")
    lines.append(f"**Head SHA:** {pr_data.get('head', {}).get('sha', '?')}")
    lines.append(f"**Base:** {pr_data.get('base', {}).get('ref', '?')}")
    lines.append("")
    pr_body = (pr_data.get("body") or "").strip()
    if pr_body:
        lines.append("## PR Description")
        lines.append("")
        lines.append(pr_body)
        lines.append("")

    # ── Issue (top-level) comments ──────────────────────────────────
    lines.append("## Issue Comments (top-level PR comments)")
    lines.append("")
    issue_comments = _gh_api_json(f"repos/{repo}/issues/{pr}/comments")
    if issue_comments:
        lines.append(f"_{len(issue_comments)} comments_\n")
        for c in issue_comments:
            lines.append(_fmt_comment(c))
    else:
        lines.append("_None._")
    lines.append("")

    # ── Review comments (threads on code) ───────────────────────────
    lines.append("## Review Comments (threads on diff)")
    lines.append("")
    review_comments = _gh_api_json(f"repos/{repo}/pulls/{pr}/comments")
    if review_comments:
        lines.append(f"_{len(review_comments)} comments_\n")
        # Group by pull_request_review_id for threading
        from collections import defaultdict

        threads: dict[int | None, list[dict]] = defaultdict(list)
        for rc in review_comments:
            threads[rc.get("pull_request_review_id")].append(rc)

        for review_id, comments in threads.items():
            first = comments[0]
            path = first.get("path", "?")
            line = first.get("line", "?")
            lines.append(
                f"### Thread (review {review_id or 'orphan'}) on `{path}:{line}`"
            )
            lines.append("")
            for rc in comments:
                user = rc.get("user", {}).get("login", "unknown")
                created = rc.get("created_at", "?")[:10]
                body = (rc.get("body") or "").strip()
                lines.append(f"- **{user}** ({created}):")
                if body:
                    if len(body) > 1000:
                        body = body[:1000] + "\n  [... truncated]"
                    for line_text in body.split("\n"):
                        lines.append(f"  {line_text}")
                else:
                    lines.append("  _(empty)_")
            lines.append("")
    else:
        lines.append("_None._")
    lines.append("")

    # ── Recent commits ──────────────────────────────────────────────
    lines.append("## Recent Commits")
    lines.append("")
    commits = _gh_api_json(f"repos/{repo}/pulls/{pr}/commits")
    if commits:
        lines.append(f"_{len(commits)} commits_\n")
        for c in commits[-10:]:  # last 10 max
            sha = c.get("sha", "?")[:8]
            msg = (c.get("commit", {}).get("message", "") or "").split("\n")[0]
            author = c.get("commit", {}).get("author", {}).get("name", "?")
            lines.append(f"- `{sha}` {author}: {msg}")
    else:
        lines.append("_None._")
    lines.append("")

    # ── Index comment detection ─────────────────────────────────────
    lines.append("## Index Comment")
    lines.append("")
    index_comment_id = None
    for c in issue_comments:
        body = c.get("body", "") or ""
        if "<!-- review-thread-index -->" in body:
            index_comment_id = c.get("id")
            lines.append(
                f"Index comment found: ID {index_comment_id} "
                f"by @{c.get('user', {}).get('login', '?')} "
                f"({c.get('created_at', '?')[:10]})"
            )
            break
    if index_comment_id is None:
        lines.append("_No index comment found._")
    lines.append("")

    # ── Gardener instructions ───────────────────────────────────────
    lines.append("## Gardener Actions")
    lines.append("")
    lines.append(
        "Based on the above PR state, perform the following actions as needed:"
    )
    lines.append("")
    lines.append("### Allowed")
    lines.append(
        "- Create missing review threads for actionable issues found in top-level comments"
    )
    lines.append(
        "- Reply to an existing thread with links to duplicate reports or added evidence"
    )
    lines.append(
        "- Fold external bot comments into existing threads by replying with a cross-link"
    )
    lines.append(
        "- Create threads for external bot findings that are actionable and anchorable"
    )
    lines.append(
        "- Update one top-level Review thread index comment (marked with `<!-- review-thread-index -->`)"
    )
    lines.append("- Optionally reopen or flag threads that violate stated guidelines")
    lines.append("")
    lines.append("### Forbidden")
    lines.append("- Delete old comments or erase evidence")
    lines.append("- Rewrite historical discussion")
    lines.append("- Decide PR acceptance or add approval/rejection labels")
    lines.append("- Claim uncertain semantic grouping is certain")
    lines.append("")
    lines.append("### Safety rule")
    lines.append(
        "If uncertain, append information somewhere auditable instead of deleting "
        "or suppressing it."
    )
    lines.append("")
    lines.append("### Index comment format")
    lines.append(
        "When updating the index comment, use the following structure. "
        "Regenerate it from the full thread set each time."
    )
    lines.append("")
    lines.append("```markdown")
    lines.append("<!-- review-thread-index -->")
    lines.append("## Review thread index")
    lines.append("")
    lines.append("### Unresolved")
    lines.append("")
    lines.append("1. <finding label>  ")
    lines.append("   Thread: <review-thread-link>  ")
    lines.append("   Sources: <source list>  ")
    lines.append("   Notes: <optional notes>")
    lines.append("")
    lines.append("### Resolved")
    lines.append("")
    lines.append("3. <finding label>  ")
    lines.append("   Thread: <review-thread-link>  ")
    lines.append("   Fix/disposition: <commit or reply link>")
    lines.append("")
    lines.append("### Folded external/top-level comments")
    lines.append("")
    lines.append("- External bot comment <link> → thread <link>")
    lines.append("")
    lines.append("### Unthreadable / needs triage")
    lines.append("")
    lines.append("- Repository-wide issue with no stable changed-file anchor")
    lines.append("```")
    lines.append("")
    lines.append("### GitHub API for actions")
    lines.append("")
    lines.append("Use `gh api` for all GitHub operations.  GH_TOKEN is available.")
    lines.append("")
    lines.append("**Post a review comment (line-level):**")
    lines.append("```")
    lines.append("gh api repos/{owner}/{repo}/pulls/{num}/comments --method POST \\")
    lines.append("  --input - <<'EOF'")
    lines.append('{"body":"...","commit_id":"<sha>","path":"<file>","line":<n>}')
    lines.append("EOF")
    lines.append("```")
    lines.append("")
    lines.append("**Post a reply to an existing review comment:**")
    lines.append("```")
    lines.append(
        "gh api repos/{owner}/{repo}/pulls/{num}/comments/{comment_id}/replies "
        "--method POST \\"
    )
    lines.append('  --field body="..."')
    lines.append("```")
    lines.append("")
    lines.append("**Update an issue comment (for index):**")
    lines.append("```")
    lines.append(
        "gh api repos/{owner}/{repo}/issues/comments/{comment_id} --method PATCH \\"
    )
    lines.append('  --field body="..."')
    lines.append("```")
    lines.append("")
    lines.append("**Create a new issue comment (for index):**")
    lines.append("```")
    lines.append("gh api repos/{owner}/{repo}/issues/{num}/comments --method POST \\")
    lines.append('  --field body="..."')
    lines.append("```")

    output = "\n".join(lines)
    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Discussion state written to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
