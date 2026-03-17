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

    HAS_TYPER = True
except ImportError as e:
    HAS_TYPER = False
    print(
        f"Warning: typer not installed ({e}). Install with: pip install typer rich",
        file=sys.stderr,
    )


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


def get_pr_reviews(repo: str, pr_num: int) -> list[dict]:
    """Get all reviews for a PR."""
    output = run_gh(
        ["pr", "view", str(pr_num), "--repo", repo, "--json", "reviews,comments"]
    )
    data = json.loads(output)
    reviews = data.get("reviews", [])
    comments = data.get("comments", [])
    return reviews, comments


def extract_qodo_issues(comments: list[dict]) -> list[dict]:
    """Extract Qodo issues from comments."""
    issues = []
    for comment in comments:
        if comment.get("author", {}).get("login") != "qodo-code-review":
            continue

        body = comment.get("body", "")
        is_minimized = comment.get("isMinimized", False)

        # Skip if minimized (resolved)
        if is_minimized:
            continue

        # Extract bug count
        bug_match = re.search(r"🐞 Bugs \((\d+)\)", body)
        if not bug_match:
            continue

        # Find the "File Changes" section boundary - issues come after this
        file_changes_idx = body.find("### File Changes")
        if file_changes_idx == -1:
            file_changes_idx = body.find("## File Changes")

        # Get only the review section (before file changes)
        review_section = body[:file_changes_idx] if file_changes_idx > 0 else body

        # Extract individual issues from review section only
        # Format: <summary>  NUM.  <s>ISSUE_TITLE</s> ☑ <code>🐞 Bug</code>
        # Or: <summary>  NUM.  ISSUE_TITLE <code>🐞 Bug</code>

        # First find all issue summaries in review section
        issue_pattern = r"<summary>\s*(\d+)\.\s*(.*?)(?:\s*<code>|$)"

        for match in re.finditer(issue_pattern, review_section):
            issue_num = match.group(1)
            issue_content = match.group(2).strip()

            # Only include if it's a bug issue (has 🐞 Bug after it in the original body)
            # Look ahead in the original body from this match position
            look_ahead_start = match.start()
            look_ahead_end = min(look_ahead_start + 200, len(body))
            lookahead_section = body[look_ahead_start:look_ahead_end]

            if "🐞 Bug" not in lookahead_section and "🐞 Bugs" not in lookahead_section:
                continue

            # Check if this issue is resolved (has <s> tags or ☑)
            is_resolved = bool(re.search(r"<s>", issue_content)) or bool(
                re.search(r"☑", issue_content)
            )

            # Extract clean title - remove <s> tags
            issue_title = re.sub(r"<s>([^<]*)</s>", r"\1", issue_content).strip()

            # Extract description - find Description section between this issue and next
            # Each issue is in a <details> block, find content between Description and </details>
            issue_start = match.start()

            # Find the next issue's <summary> position after this one
            next_issue_pattern = r"<summary>\s*(\d+)\.\s*"
            next_matches = list(
                re.finditer(next_issue_pattern, review_section[issue_start:])
            )

            if len(next_matches) > 1:
                # There's another issue after this one
                next_issue_start = issue_start + next_matches[1].start()
                issue_section = review_section[issue_start:next_issue_start]
            else:
                # This is the last issue
                issue_section = review_section[issue_start:]

            # Extract description from this issue section - look for Description block
            # Format: <summary>Description</summary><pre>...description...</pre>
            # or: <summary>Description</summary><br/><pre>...description...</pre>
            desc_pattern = r"<summary>Description</summary>(.*?)(?=<hr/>|</details>)"
            desc_match = re.search(desc_pattern, issue_section, re.DOTALL)

            issue_description = ""
            if desc_match:
                issue_description = desc_match.group(1)
                # Remove <pre> tags and content
                issue_description = re.sub(
                    r"<pre>(.*?)</pre>", r"\1", issue_description, flags=re.DOTALL
                )
                issue_description = re.sub(r"<br\s*/?>", " ", issue_description)
                issue_description = re.sub(r"<b>|</b>|<i>|</i>", "", issue_description)
                # Remove leading > and extra whitespace
                lines = issue_description.split("\n")
                cleaned_lines = []
                for line in lines:
                    line = re.sub(r"^>\s*", "", line)
                    line = line.strip()
                    if line:
                        cleaned_lines.append(line)
                issue_description = " ".join(cleaned_lines)
                # Clean up HTML entities
                issue_description = issue_description.replace("&#x27;", "'")
                issue_description = issue_description.replace("&quot;", '"')
                issue_description = issue_description.replace("&gt;", ">")
                issue_description = issue_description.replace("&lt;", "<")
                issue_description = issue_description.replace("&amp;", "&")
                # Remove multiple spaces
                issue_description = re.sub(r"\s+", " ", issue_description)

            issues.append(
                {
                    "number": issue_num,
                    "title": issue_title,
                    "description": issue_description,
                    "resolved": is_resolved,
                    "minimized": is_minimized,
                }
            )

    return issues


def extract_gemini_issues(reviews: list[dict], comments: list[dict]) -> list[dict]:
    """Extract Gemini Code Assist issues."""
    issues = []

    for review in reviews:
        if review.get("author", {}).get("login") != "gemini-code-assist":
            continue

        state = review.get("state", "")
        # COMMENTED means not resolved
        if state == "COMMENTED":
            issues.append({"type": "review", "state": state, "resolved": False})

    return issues


def extract_kilo_code_bot_issues(comments: list[dict]) -> list[dict]:
    """Extract issues from kilo-code-bot comments."""
    issues = []

    for comment in comments:
        if comment.get("author", {}).get("login") != "kilo-code-bot":
            continue

        body = comment.get("body", "")

        # Check if minimized
        if comment.get("isMinimized", False):
            continue

        # Look for issue table after "Issue Details" section
        # Format:
        # | File | Line | Issue |
        # |------|------|-------|
        # | README.md | 35 | ... |
        # Only match rows where File contains a path-like pattern (has . or /)
        table_pattern = r"\|\s*(\S+)\s*\|\s*(\d+)\s*\|\s*(.+?)\s*\|"
        for match in re.finditer(table_pattern, body):
            file_path = match.group(1)
            line_num = match.group(2)
            issue_desc = match.group(3).strip()

            # Skip non-file rows (severity table, headers)
            # File paths typically have extension or contain /
            if "." not in file_path and "/" not in file_path:
                continue

            # Skip if issue description is empty or just contains markers
            if not issue_desc or len(issue_desc) < 5:
                continue

            # Issues are unresolved unless marked resolved
            issues.append(
                {
                    "title": issue_desc,
                    "file": file_path,
                    "line": line_num,
                    "resolved": False,
                    "source": "kilo-code-bot",
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
    """Generate markdown report."""
    lines = [
        "# Unresolved PR Review Issues",
        "",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "This document tracks open PRs with unresolved review issues. Issues are considered resolved only when:",
        "",
        "- The review comment has been marked as **resolved** in GitHub (clicked checkmark), OR",
        "- The concern is **struck through** in the PR (~~text~~)",
        "",
        "---",
        "",
    ]

    unresolved_count = 0
    resolved_count = 0

    for pr in prs:
        repo = pr["repositoryName"]
        pr_num = pr["number"]
        title = pr["title"]
        url = pr["url"]

        key = f"{repo}#{pr_num}"
        issues = all_issues.get(key, [])

        if not issues:
            continue

        pr_unresolved = [
            i
            for i in issues
            if not i.get("resolved", False)
            and "COMMENTED state" not in i.get("title", "")
        ]
        pr_resolved = [i for i in issues if i.get("resolved", False)]

        # Skip PRs with no issues at all (only bot reviews that aren't issues)
        if not pr_unresolved and not [
            i
            for i in issues
            if i.get("title") != "Review in COMMENTED state (not resolved)"
        ]:
            continue

        unresolved_count += len(pr_unresolved)
        resolved_count += len(pr_resolved)

        lines.append(f"## {repo}")
        lines.append("")
        lines.append(f"### PR #{pr_num} — {title}")
        lines.append(f"[Link]({url})")
        lines.append("")

        if pr_unresolved:
            lines.append("| Issue | Status |")
            lines.append("|-------|--------|")
            for issue in pr_unresolved:
                title = issue["title"]
                desc = issue.get("description", "")
                # Truncate description if too long
                if desc and len(desc) > 200:
                    desc = desc[:200] + "..."
                if desc:
                    lines.append(f"| **{title}**  \n_{desc}_ | 🔴 NOT RESOLVED |")
                else:
                    lines.append(f"| {title} | 🔴 NOT RESOLVED |")
            lines.append("")

        if pr_resolved:
            lines.append("| ~~Resolved~~ | Status |")
            lines.append("| ---- | ---- |")
            for issue in pr_resolved:
                lines.append(f"| ~~{issue['title']}~~ | ✅ RESOLVED |")
            lines.append("")

    # Summary
    lines.extend(
        [
            "---",
            "",
            "## Summary",
            "",
            "| Status | Count |",
            "|--------|-------|",
            f"| 🔴 NOT RESOLVED | {unresolved_count} |",
            f"| ✅ RESOLVED | {resolved_count} |",
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
            from urllib.parse import urlparse

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

        issues = []

        # Qodo issues from comments
        qodo_issues = extract_qodo_issues(comments)
        issues.extend(qodo_issues)

        # Gemini issues
        gemini_issues = extract_gemini_issues(reviews, comments)
        for gi in gemini_issues:
            issues.append(
                {
                    "title": "Review in COMMENTED state (not resolved)",
                    "resolved": False,
                    "source": "gemini",
                }
            )

        # kilo-code-bot issues
        kilo_issues = extract_kilo_code_bot_issues(comments)
        issues.extend(kilo_issues)

        if issues:
            all_issues[key] = issues

    markdown = generate_markdown(prs, all_issues)

    if args.output:
        Path(args.output).write_text(markdown)
        print(f"Wrote to {args.output}", file=sys.stderr)
    else:
        print(markdown)


# Typer CLI
if HAS_TYPER:
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
            issues = []

            qodo_issues = extract_qodo_issues(comments)
            issues.extend(qodo_issues)

            gemini_issues = extract_gemini_issues(reviews, comments)
            for gi in gemini_issues:
                issues.append(
                    {
                        "title": "Review in COMMENTED state (not resolved)",
                        "resolved": False,
                        "source": "gemini",
                    }
                )

            kilo_issues = extract_kilo_code_bot_issues(comments)
            issues.extend(kilo_issues)

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


if __name__ == "__main__":
    if HAS_TYPER:
        # Run typer which handles subcommands
        app()
    else:
        main()
