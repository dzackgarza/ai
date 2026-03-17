#!/usr/bin/env python3
"""
Extract unresolved PR review issues from GitHub.

Finds all open PRs by the authenticated user, checks Qodo/Gemini/Codex reviews,
and identifies issues that are NOT resolved (not struck through, not minimized).

Usage:
    python scripts/extract_unresolved_issues.py [--output FILE]

    # Summarize PR comments
    python scripts/extract_unresolved_issues.py summarize owner/repo#123
"""

import argparse
import json
import subprocess
import sys
import re
from datetime import datetime
from pathlib import Path

try:
    import typer
    import rich
except ImportError:
    print(
        "Error: typer and rich are required. Install with: pip install typer rich",
        file=sys.stderr,
    )
    sys.exit(1)


def run_gh(args: list[str]) -> str:
    """Run a gh command and return output."""
    result = subprocess.run(["gh"] + args, capture_output=True, text=True, check=True)
    return result.stdout


def get_open_prs() -> list[dict]:
    """Get all open PRs by the user using gh api."""
    # Use gh api to search for PRs
    query = "is:pr author:@me is:open sort:created"
    output = run_gh(
        [
            "api",
            "search/issues",
            "-q",
            ".items[] | {number: .number, repository_url: .repository_url, url: .html_url, title: .title}",
            "--method",
            "GET",
            "-F",
            f"q={query}",
            "-F",
            "per_page=50",
        ]
    )
    # Parse each line as JSON
    prs = []
    for line in output.strip().split("\n"):
        if line.strip():
            try:
                pr = json.loads(line)
                # Extract repo name from URL
                repo_url = pr.get("repository_url", "")
                repo_name = repo_url.replace("https://api.github.com/repos/", "")
                if repo_name:
                    pr["repositoryName"] = repo_name
                    prs.append(pr)
            except json.JSONDecodeError:
                pass
    return prs


def get_pr_reviews(repo: str, pr_num: int) -> tuple[list[dict], list[dict]]:
    """Get all reviews and comments for a PR using the API (more complete than pr view)."""
    # Fetch unresolved threads via GraphQL (this is the source of truth for resolved threads)
    try:
        owner, name = repo.split("/")
        query = (
            """query { repository(owner: "%s", name: "%s") { pullRequest(number: %s) { reviewThreads(first: 100) { nodes { id isResolved comments(first: 10) { nodes { id databaseId body author { login } } } } } } } }"""
            % (owner, name, pr_num)
        )

        output = run_gh(["api", "graphql", "--field", "query=" + query])
        data = json.loads(output)
        threads = (
            data.get("data", {})
            .get("repository", {})
            .get("pullRequest", {})
            .get("reviewThreads", {})
            .get("nodes", [])
        )

        # Build comments list with resolved status
        comments = []
        for thread in threads:
            is_resolved = thread.get("isResolved", False)
            for comment in thread.get("comments", {}).get("nodes", []):
                comments.append(
                    {
                        "id": comment.get("databaseId"),
                        "body": comment.get("body", ""),
                        "user": {
                            "login": comment.get("author", {}).get("login", "unknown")
                        },
                        "isResolved": is_resolved,
                    }
                )
    except Exception as e:
        print(f"GraphQL fetch failed: {e}, falling back to REST", file=sys.stderr)
        # Fallback to REST API
        try:
            output = run_gh(["api", f"repos/{repo}/pulls/{pr_num}/comments"])
            comments = json.loads(output)
        except subprocess.CalledProcessError:
            comments = []

    # Fetch reviews
    try:
        output = run_gh(
            ["pr", "view", str(pr_num), "--repo", repo, "--json", "reviews"]
        )
        data = json.loads(output)
        reviews = data.get("reviews", [])
    except subprocess.CalledProcessError:
        reviews = []

    return reviews, comments


def extract_all_unresolved_comments(comments: list[dict]) -> list[dict]:
    """
    Extract ALL unresolved comments - simple mechanism:
    A comment is unresolved if the review thread is not resolved (isResolved != true).
    """
    issues = []

    for comment in comments:
        # Check if thread is resolved
        is_resolved = comment.get("isResolved", False)
        if is_resolved:
            continue  # Skip resolved conversations

        author = comment.get("user", {}).get("login", "unknown")
        body = comment.get("body", "")

        issues.append(
            {
                "author": author,
                "body": body,
            }
        )

    return issues


def summarize_pr_comments(pr_url: str, output_file: str = None) -> str:
    """Generate a token-friendly summary of all PR comments."""
    # Parse PR URL or owner/repo#num
    if "#" in pr_url:
        repo_part, pr_num = pr_url.rsplit("#", 1)
        try:
            pr_num = int(pr_num)
        except ValueError:
            print(f"Invalid PR number: {pr_num}", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"Invalid format: {pr_url}. Use owner/repo#123", file=sys.stderr)
        sys.exit(1)

    # Fetch PR details and comments
    try:
        output = run_gh(
            [
                "pr",
                "view",
                str(pr_num),
                "--repo",
                repo_part,
                "--json",
                "title,url,number,body,state",
            ]
        )
        pr_data = json.loads(output)
    except subprocess.CalledProcessError:
        print(f"PR not found: {repo_part}#{pr_num}", file=sys.stderr)
        sys.exit(1)

    # Fetch ALL comments using API (pr view --json comments misses some)
    try:
        output = run_gh(["api", f"repos/{repo_part}/pulls/{pr_num}/comments"])
        comments = json.loads(output)
    except subprocess.CalledProcessError:
        comments = []

    # Also fetch reviews (they have different authors than comments)
    try:
        output = run_gh(
            ["pr", "view", str(pr_num), "--repo", repo_part, "--json", "reviews"]
        )
        reviews_data = json.loads(output)
        reviews = reviews_data.get("reviews", [])
    except subprocess.CalledProcessError:
        reviews = []

    lines = [
        f"# PR #{pr_data['number']}: {pr_data['title']}",
        f"[{pr_data['url']}]({pr_data['url']})",
        f"**State:** {pr_data.get('state', 'unknown')}",
        "",
        "---",
        "",
    ]

    # Group comments and reviews by author
    authors: dict = {}

    # Process comments (from API - use 'user' and 'created_at')
    for comment in comments:
        author = comment.get("user", {}).get("login", "unknown")
        if author not in authors:
            authors[author] = []

        # Get FULL raw body - no truncation
        body = comment.get("body", "")

        authors[author].append(
            {
                "body": body,
                "created_at": comment.get("created_at", ""),
                "type": "comment",
            }
        )

    # Process reviews (treat as comments)
    for review in reviews:
        author = review.get("user", {}).get("login", "unknown")
        if author not in authors:
            authors[author] = []

        body = review.get("body", "")

        authors[author].append(
            {
                "body": body,
                "created_at": review.get("submitted_at", ""),
                "type": "review",
            }
        )

    # Output all comments and reviews in order - no grouping
    for comment in comments:
        author = comment.get("user", {}).get("login", "unknown")
        date = (
            comment.get("created_at", "")[:10]
            if comment.get("created_at")
            else "unknown"
        )
        lines.append(f"## {author} ({date})")
        lines.append("")
        lines.append(comment.get("body", ""))
        lines.append("")
        lines.append("---")
        lines.append("")

    for review in reviews:
        author = review.get("user", {}).get("login", "unknown")
        date = (
            review.get("submitted_at", "")[:10]
            if review.get("submitted_at")
            else "unknown"
        )
        lines.append(f"## {author} ({date})")
        lines.append("")
        lines.append(review.get("body", ""))
        lines.append("")
        lines.append("---")
        lines.append("")

    result = "\n".join(lines)

    if output_file:
        Path(output_file).write_text(result)
        print(f"Wrote to {output_file}", file=sys.stderr)

    return result


def extract_bot_summary(body: str, bot: str) -> str:
    """Extract key information from bot comments for token efficiency."""
    if bot == "qodo-code-review":
        # Extract issue counts and titles
        bugs = re.findall(r"(\d+)\.\s+(.+?)(?:\s+<code>|$)", body, re.DOTALL)
        if bugs:
            lines = ["**Issues:**"]
            for num, title in bugs[:5]:  # Max 5 issues
                title = re.sub(r"<[^>]+>", "", title).strip()[:100]
                lines.append(f"- {num}. {title}")
            return "\n".join(lines)

    elif bot == "kilo-code-bot":
        # Extract issue table
        issues = re.findall(r"\|(.+?)\|(.+?)\|(.+?)\|", body)
        if issues:
            lines = ["**Issues:**"]
            for file_path, line, issue in issues[:5]:
                if "." in file_path.strip():
                    issue = issue.strip()[:80]
                    lines.append(f"- {file_path.strip()}:{line.strip()} - {issue}")
            return "\n".join(lines)

    elif bot == "gemini-code-assist":
        # Extract changelog
        changelog = re.search(
            r"<details>.*?<summary><b>Changelog</b></summary>(.*?)</details>",
            body,
            re.DOTALL,
        )
        if changelog:
            return changelog.group(1)[:500]

    # Default: first 500 chars
    return body[:500]


def get_pr_details(repo: str, pr_num: int) -> tuple[list[dict], list[dict]]:
    """Get detailed review info for a PR."""
    try:
        reviews, comments = get_pr_reviews(repo, pr_num)
        return reviews, comments
    except subprocess.CalledProcessError as e:
        print(f"Error fetching PR {repo}#{pr_num}: {e}", file=sys.stderr)
        return [], []


def generate_markdown(prs: list[dict], all_issues: dict) -> str:
    """Generate markdown report - just show author + full body for each unresolved comment."""
    lines = [
        "# Unresolved PR Review Issues",
        "",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "A comment is unresolved if the 'Resolve Conversation' button was never clicked.",
        "",
        "---",
        "",
    ]

    unresolved_count = 0

    for pr in prs:
        repo = pr["repositoryName"]
        pr_num = pr["number"]
        title = pr["title"]
        url = pr["url"]

        key = f"{repo}#{pr_num}"
        issues = all_issues.get(key, [])

        if not issues:
            continue

        unresolved_count += len(issues)

        lines.append(f"## {repo}")
        lines.append("")
        lines.append(f"### PR #{pr_num} — {title}")
        lines.append(f"[Link]({url})")
        lines.append("")

        # Show each unresolved comment with author and full body
        for i, issue in enumerate(issues, 1):
            author = issue.get("author", "unknown")
            body = issue.get("body", "")
            lines.append(f"### {i}. {author}")
            lines.append("")
            lines.append(body)
            lines.append("")
            lines.append("---")
            lines.append("")

    # Summary
    lines.extend(
        [
            "## Summary",
            "",
            f"🔴 **NOT RESOLVED:** {unresolved_count}",
            "",
        ]
    )

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Extract unresolved PR review issues")
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    parser.add_argument(
        "--repo",
        "-r",
        help="Filter by repository (e.g., dzackgarza/opencode-plugin-improved-webtools)",
    )
    parser.add_argument(
        "--pr",
        "-p",
        type=int,
        help="Filter by PR number (requires --repo)",
    )
    parser.add_argument(
        "pr_url",
        nargs="?",
        help="PR URL or owner/repo#num (e.g., https://github.com/owner/repo/pull/123 or owner/repo#123)",
    )
    args = parser.parse_args()

    # Handle PR URL argument
    if args.pr_url:
        # Parse PR URL or owner/repo#num
        pr_url = args.pr_url
        if "#" in pr_url:
            # owner/repo#123
            repo_part, pr_num = pr_url.rsplit("#", 1)
            try:
                pr_num = int(pr_num)
            except ValueError:
                print(f"Invalid PR number: {pr_num}", file=sys.stderr)
                sys.exit(1)
            # Fetch PR details to get title
            try:
                output = run_gh(
                    [
                        "pr",
                        "view",
                        str(pr_num),
                        "--repo",
                        repo_part,
                        "--json",
                        "title,url,number",
                    ]
                )
                pr_data = json.loads(output)
                prs = [
                    {
                        "repositoryName": repo_part,
                        "number": pr_data["number"],
                        "title": pr_data["title"],
                        "url": pr_data["url"],
                    }
                ]
            except subprocess.CalledProcessError:
                print(f"PR not found: {repo_part}#{pr_num}", file=sys.stderr)
                sys.exit(1)
        elif "/pull/" in pr_url:
            # Full URL - https://github.com/owner/repo/pull/123
            parsed = urlparse(pr_url)
            path_parts = parsed.path.strip("/").split("/")
            if len(path_parts) >= 4 and path_parts[2] == "pull":
                repo = f"{path_parts[0]}/{path_parts[1]}"
                try:
                    pr_num = int(path_parts[3])
                except (ValueError, IndexError):
                    print(f"Invalid PR URL: {pr_url}", file=sys.stderr)
                    sys.exit(1)
                # Fetch PR details to get title
                try:
                    output = run_gh(
                        [
                            "pr",
                            "view",
                            str(pr_num),
                            "--repo",
                            repo,
                            "--json",
                            "title,url,number",
                        ]
                    )
                    pr_data = json.loads(output)
                    prs = [
                        {
                            "repositoryName": repo,
                            "number": pr_data["number"],
                            "title": pr_data["title"],
                            "url": pr_data["url"],
                        }
                    ]
                except subprocess.CalledProcessError:
                    print(f"PR not found: {repo}#{pr_num}", file=sys.stderr)
                    sys.exit(1)
            else:
                print(f"Invalid PR URL format: {pr_url}", file=sys.stderr)
                sys.exit(1)
    else:
        print("Fetching open PRs...", file=sys.stderr)
        prs = get_open_prs()

        if args.repo:
            prs = [p for p in prs if p["repositoryName"] == args.repo]

        if args.pr:
            if not args.repo:
                print("--pr requires --repo", file=sys.stderr)
                sys.exit(1)
            prs = [p for p in prs if p["number"] == args.pr]

    print(f"Found {len(prs)} open PRs", file=sys.stderr)

    all_issues = {}

    for pr in prs:
        repo = pr["repositoryName"]
        pr_num = pr["number"]
        key = f"{repo}#{pr_num}"

        print(f"Checking {key}...", file=sys.stderr)

        reviews, comments = get_pr_details(repo, pr_num)

        # Extract ALL unresolved comments (simple: not minimized = unresolved)
        issues = extract_all_unresolved_comments(comments)

        if issues:
            all_issues[key] = issues

    markdown = generate_markdown(prs, all_issues)

    if args.output:
        Path(args.output).write_text(markdown)
        print(f"Wrote to {args.output}", file=sys.stderr)
    else:
        print(markdown)


def validate_justification(justification: str) -> bool:
    """
    Validate that justification contains a commit link or issue reference.

    Valid patterns:
    - Commit SHA (short or full): abc123, abc123def...
    - Commit reference: commit abc123, /commit/abc123
    - Commit URL: https://github.com/owner/repo/commit/abc123
    - Issue reference: #123, issue #123
    - Issue URL: https://github.com/owner/repo/issues/123
    """
    # Check for commit references
    # Pattern:
    # - /commit/ in URL
    # - word "commit" followed by SHA (6-40 chars)
    # - standalone 6-40 char hex string
    has_commit_ref = bool(
        re.search(r"/commit/[a-fA-F0-9]{6,40}", justification)
        or re.search(r"\bcommit\s+[a-fA-F0-9]{6,40}\b", justification, re.IGNORECASE)
        or re.search(r"\b[0-9a-fA-F]{6,40}\b", justification)  # bare SHA
    )

    # Check for issue references
    # Pattern: #123, issue #123, or full issue URL
    has_issue_ref = bool(
        re.search(r"#\d+", justification)  # #123
        or re.search(r"issues/\d+", justification)  # issues/123
        or re.search(r"\bissue\s+#?\d+", justification, re.IGNORECASE)  # issue #123
    )

    return has_commit_ref or has_issue_ref


def resolve_comment(comment_id: str, justification: str, repo: str = None) -> dict:
    """
    Resolve a PR comment by minimizing the conversation.

    Requires a justification that links to a commit or issue.
    """
    # Validate justification
    if not validate_justification(justification):
        raise ValueError(
            "Justification must include a commit reference (e.g., commit abc123 or /commit/) "
            "or an issue reference (e.g., #123 or issues/123)"
        )

    # Determine repo if not provided
    if not repo:
        # Try to get repo from current git remote
        try:
            result = subprocess.run(
                [
                    "gh",
                    "repo",
                    "view",
                    "--json",
                    "nameWithOwner",
                    "-q",
                    ".nameWithOwner",
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            repo = result.stdout.strip()
        except subprocess.CalledProcessError:
            raise ValueError("Could not determine repository. Please specify --repo.")

    # Resolve via GraphQL - get thread ID from comment, then resolve thread
    import json

    try:
        # Get pull number from comment
        comment_result = subprocess.run(
            [
                "gh",
                "api",
                f"repos/{repo}/pulls/comments/{comment_id}",
                "-q",
                ".pull_request_url",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        pull_url = comment_result.stdout.strip()
        pull_number = pull_url.split("/")[-1]
        owner, name = repo.split("/")

        # Get review threads and find the one containing our comment
        threads_query = (
            """query { repository(owner: "%s", name: "%s") { pullRequest(number: %s) { reviewThreads(first: 100) { nodes { id isResolved comments(first: 10) { nodes { id databaseId } } } } } } }"""
            % (owner, name, pull_number)
        )

        threads_result = subprocess.run(
            ["gh", "api", "graphql", "--field", "query=" + threads_query],
            capture_output=True,
            text=True,
            check=True,
        )

        if threads_result.returncode != 0:
            raise Exception(f"GraphQL query failed: {threads_result.stderr}")

        threads_data = json.loads(threads_result.stdout)
        threads = threads_data["data"]["repository"]["pullRequest"]["reviewThreads"][
            "nodes"
        ]

        # Find thread with our comment
        thread_id = None
        for thread in threads:
            for comment in thread["comments"]["nodes"]:
                if comment["databaseId"] == int(comment_id):
                    thread_id = thread["id"]
                    break
            if thread_id:
                break

        if not thread_id:
            raise Exception(f"Could not find review thread for comment {comment_id}")

        # Resolve the thread
        resolve_query = (
            """mutation { resolveReviewThread(input: {threadId: "%s"}) { thread { isResolved } } }"""
            % thread_id
        )

        resolve_result = subprocess.run(
            ["gh", "api", "graphql", "--field", "query=" + resolve_query],
            capture_output=True,
            text=True,
            check=True,
        )

        resolve_data = json.loads(resolve_result.stdout)
        if resolve_data.get("errors"):
            raise Exception(f"GraphQL error: {resolve_data['errors']}")

        return {
            "success": True,
            "comment_id": comment_id,
            "thread_id": thread_id,
            "justification": justification,
        }

    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to resolve comment: {e}")
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse GraphQL response: {e}")


# Typer CLI
app = typer.Typer(help="Extract PR review issues and summarize comments")


@app.command()
def summarize(
    pr_url: str,
    output_file: str = typer.Option(None, "-o", "--output", help="Output file"),
):
    """Summarize all PR comments (token-friendly)."""
    result = summarize_pr_comments(pr_url, output_file)
    if not output_file:
        # Render markdown nicely using rich
        try:
            from rich.console import Console
            from rich.markdown import Markdown

            console = Console()
            console.print(Markdown(result))
        except ImportError:
            # Fallback to plain text
            print(result)


@app.command()
def issues(
    pr_url: str,
    output_file: str = typer.Option(None, "-o", "--output", help="Output file"),
):
    """Extract unresolved issues from a PR."""
    # Parse PR URL
    if "#" in pr_url:
        repo_part, pr_num = pr_url.rsplit("#", 1)
        try:
            pr_num = int(pr_num)
        except ValueError:
            print(f"Invalid PR number: {pr_num}", file=sys.stderr)
            raise typer.Exit(1)

        # Fetch PR details
        try:
            output = run_gh(
                [
                    "pr",
                    "view",
                    str(pr_num),
                    "--repo",
                    repo_part,
                    "--json",
                    "title,url,number",
                ]
            )
            pr_data = json.loads(output)
            prs = [
                {
                    "repositoryName": repo_part,
                    "number": pr_data["number"],
                    "title": pr_data["title"],
                    "url": pr_data["url"],
                }
            ]
        except subprocess.CalledProcessError:
            print(f"PR not found: {repo_part}#{pr_num}", file=sys.stderr)
            raise typer.Exit(1)
    else:
        print("Error: Provide PR as owner/repo#123", file=sys.stderr)
        raise typer.Exit(1)

    # Get issues
    all_issues = {}
    for pr in prs:
        repo = pr["repositoryName"]
        pr_num = pr["number"]
        key = f"{repo}#{pr_num}"
        reviews, comments = get_pr_details(repo, pr_num)

        # Extract ALL unresolved comments (simple: not minimized = unresolved)
        issues = extract_all_unresolved_comments(comments)

        if issues:
            all_issues[key] = issues

    markdown = generate_markdown(prs, all_issues)

    if output_file:
        Path(output_file).write_text(markdown)
        print(f"Wrote to {output_file}", file=sys.stderr)
    else:
        print(markdown)


@app.command()
def list(
    repo: str = typer.Option(None, "-r", "--repo", help="Filter by repository"),
    output: str = typer.Option(None, "-o", "--output", help="Output file"),
):
    """List unresolved issues across all open PRs."""
    sys.argv = ["extract_unresolved_issues.py"]
    if repo:
        sys.argv.extend(["--repo", repo])
    if output:
        sys.argv.extend(["--output", output])
    main()


@app.command()
def resolve(
    comment_id: str = typer.Argument(..., help="Comment ID to resolve"),
    justification: str = typer.Argument(
        ..., help="Justification (must include commit or issue reference)"
    ),
    repo: str = typer.Option(None, "-r", "--repo", help="Repository (owner/repo)"),
):
    """Resolve a PR comment with a required justification."""
    try:
        result = resolve_comment(comment_id, justification, repo)
        print(f"✅ Resolved comment {comment_id}")
        print(f"   Justification: {justification}")
    except ValueError as e:
        print(f"❌ Validation error: {e}", file=sys.stderr)
        raise typer.Exit(1)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
