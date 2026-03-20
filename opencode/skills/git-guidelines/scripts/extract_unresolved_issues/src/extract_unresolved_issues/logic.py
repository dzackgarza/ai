import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, cast
from urllib.parse import urlparse

from pydantic import validate_call

from extract_unresolved_issues.models import (
    Comment,
    PRRef,
    ResolveInput,
    SummarizeInput,
    UnresolvedIssue,
)


@validate_call
def run_gh(args: list[str]) -> str:
    """Run a gh command and return output."""
    result = subprocess.run(["gh"] + args, capture_output=True, text=True, check=True)
    return result.stdout


@validate_call
def get_open_prs() -> list[PRRef]:
    """Get all open PRs by the user using gh api."""
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
    prs: list[PRRef] = []
    for line in output.strip().split("\n"):
        if line.strip():
            try:
                pr_data = cast(dict[str, Any], json.loads(line))
                repo_url = cast(str, pr_data.get("repository_url", ""))
                repo_name = repo_url.replace("https://api.github.com/repos/", "")
                if repo_name:
                    prs.append(
                        PRRef(
                            repo=repo_name,
                            number=int(pr_data.get("number") or 0),
                            url=cast(str | None, pr_data.get("url")),
                            title=cast(str | None, pr_data.get("title")),
                        )
                    )
            except json.JSONDecodeError:
                pass
    return prs


@validate_call
def parse_pr_url(pr_url: str) -> PRRef:
    if "#" in pr_url:
        repo_part, pr_num_str = pr_url.rsplit("#", 1)
        try:
            pr_num = int(pr_num_str)
        except ValueError:
            raise ValueError(f"Invalid PR number: {pr_num_str}")
        return PRRef(repo=repo_part, number=pr_num)
    elif "/pull/" in pr_url:
        parsed = urlparse(pr_url)
        path_parts = parsed.path.strip("/").split("/")
        if len(path_parts) >= 4 and path_parts[2] == "pull":
            repo = f"{path_parts[0]}/{path_parts[1]}"
            try:
                pr_num = int(path_parts[3])
            except (ValueError, IndexError):
                raise ValueError(f"Invalid PR URL: {pr_url}")
            return PRRef(repo=repo, number=pr_num)
        else:
            raise ValueError(f"Invalid PR URL format: {pr_url}")
    else:
        raise ValueError(f"Invalid format: {pr_url}. Use owner/repo#123 or a full URL")


@validate_call
def get_pr_reviews(repo: str, pr_num: int) -> tuple[list[Comment], list[Comment]]:
    """Get all reviews and comments for a PR using the API."""
    comments: list[Comment] = []
    try:
        owner, name = repo.split("/")
        query = (
            """query { repository(owner: "%s", name: "%s") { pullRequest(number: %s) { reviewThreads(first: 100) { nodes { id isResolved comments(first: 10) { nodes { id databaseId body author { login } } } } } } } }"""
            % (owner, name, pr_num)
        )

        output = run_gh(["api", "graphql", "--field", "query=" + query])
        data = cast(dict[str, Any], json.loads(output))
        threads_obj = cast(
            list[dict[str, Any]],
            data.get("data", {})
            .get("repository", {})
            .get("pullRequest", {})
            .get("reviewThreads", {})
            .get("nodes", []),
        )

        for thread in threads_obj:
            is_resolved = cast(bool, thread.get("isResolved", False))
            thread_comments = cast(
                list[dict[str, Any]], thread.get("comments", {}).get("nodes", [])
            )
            for comment in thread_comments:
                author_login = cast(dict[str, str], comment.get("author") or {})
                author = (
                    author_login.get("login", "unknown") if author_login else "unknown"
                )
                comments.append(
                    Comment(
                        id=int(comment.get("databaseId", 0)),
                        body=str(comment.get("body", "")),
                        author=author,
                        is_resolved=is_resolved,
                        type="comment",
                    )
                )
    except Exception as e:
        print(f"GraphQL fetch failed: {e}, falling back to REST", file=sys.stderr)
        try:
            output = run_gh(["api", f"repos/{repo}/pulls/{pr_num}/comments"])
            raw_comments = cast(list[dict[str, Any]], json.loads(output))
            for c in raw_comments:
                comments.append(
                    Comment(
                        id=int(c.get("id", 0)),
                        body=str(c.get("body", "")),
                        author=str(c.get("user", {}).get("login", "unknown")),
                        is_resolved=False,
                        created_at=str(c.get("created_at", "")),
                        type="comment",
                    )
                )
        except subprocess.CalledProcessError:
            pass

    reviews: list[Comment] = []
    try:
        output = run_gh(
            ["pr", "view", str(pr_num), "--repo", repo, "--json", "reviews"]
        )
        data = cast(dict[str, Any], json.loads(output))
        raw_reviews = cast(list[dict[str, Any]], data.get("reviews", []))
        for r in raw_reviews:
            reviews.append(
                Comment(
                    id=0,
                    body=str(r.get("body", "")),
                    author=str(r.get("author", {}).get("login", "unknown")),
                    is_resolved=False,
                    created_at=str(r.get("submittedAt", "")),
                    type="review",
                )
            )
    except subprocess.CalledProcessError:
        pass

    return reviews, comments


@validate_call
def get_pr_check_runs(repo: str, head_sha: str) -> list[CheckRun]:
    """Get all check runs and their annotations for a PR's HEAD commit."""
    check_runs: list[CheckRun] = []
    try:
        output = run_gh(["api", f"repos/{repo}/commits/{head_sha}/check-runs"])
        data = cast(dict[str, Any], json.loads(output))
        runs = cast(list[dict[str, Any]], data.get("check_runs", []))

        for run in runs:
            check_run = CheckRun(
                id=int(run.get("id", 0)),
                name=str(run.get("name", "Unknown")),
                status=str(run.get("status", "unknown")),
                conclusion=str(run.get("conclusion"))
                if run.get("conclusion")
                else None,
                details_url=str(run.get("details_url"))
                if run.get("details_url")
                else None,
            )

            # Only fetch annotations if the check failed or requires action
            if check_run.conclusion in ("failure", "action_required", "neutral"):
                try:
                    ann_output = run_gh(
                        ["api", f"repos/{repo}/check-runs/{check_run.id}/annotations"]
                    )
                    ann_data = cast(list[dict[str, Any]], json.loads(ann_output))
                    for ann in ann_data:
                        check_run.annotations.append(
                            CheckRunAnnotation(
                                path=str(ann.get("path", "")),
                                start_line=int(ann.get("start_line", 0)),
                                annotation_level=str(
                                    ann.get("annotation_level", "warning")
                                ),
                                message=str(ann.get("message", "")),
                                title=str(ann.get("title"))
                                if ann.get("title")
                                else None,
                                blob_href=str(ann.get("blob_href"))
                                if ann.get("blob_href")
                                else None,
                            )
                        )
                except subprocess.CalledProcessError:
                    pass

            check_runs.append(check_run)

    except subprocess.CalledProcessError as e:
        print(f"Failed to fetch check runs: {e}", file=sys.stderr)

    return check_runs


@validate_call
def extract_all_unresolved_comments(comments: list[Comment]) -> list[UnresolvedIssue]:
    """Extract ALL unresolved comments (not resolved)."""
    issues: list[UnresolvedIssue] = []
    for comment in comments:
        if comment.is_resolved:
            continue
        issues.append(UnresolvedIssue(author=comment.author, body=comment.body))
    return issues


@validate_call
def summarize_pr_comments(inp: SummarizeInput) -> str:
    """Generate a token-friendly summary of all PR comments."""
    pr_ref = parse_pr_url(inp.pr_url)

    try:
        output = run_gh(
            [
                "pr",
                "view",
                str(pr_ref.number),
                "--repo",
                pr_ref.repo,
                "--json",
                "title,url,number,body,state,headRefOid",
            ]
        )
        pr_data = cast(dict[str, Any], json.loads(output))
    except subprocess.CalledProcessError:
        raise ValueError(f"PR not found: {pr_ref.repo}#{pr_ref.number}")

    comments_raw: list[dict[str, Any]] = []
    try:
        output = run_gh(["api", f"repos/{pr_ref.repo}/pulls/{pr_ref.number}/comments"])
        comments_raw = cast(list[dict[str, Any]], json.loads(output))
    except subprocess.CalledProcessError:
        pass

    reviews_raw: list[dict[str, Any]] = []
    try:
        output = run_gh(
            [
                "pr",
                "view",
                str(pr_ref.number),
                "--repo",
                pr_ref.repo,
                "--json",
                "reviews",
            ]
        )
        reviews_data = cast(dict[str, Any], json.loads(output))
        reviews_raw = cast(list[dict[str, Any]], reviews_data.get("reviews", []))
    except subprocess.CalledProcessError:
        pass

    head_sha = str(pr_data.get("headRefOid", ""))
    check_runs = get_pr_check_runs(pr_ref.repo, head_sha) if head_sha else []

    lines = [
        f"# PR #{pr_data.get('number', pr_ref.number)}: {pr_data.get('title', 'Unknown')}",
        f"[{pr_data.get('url', '')}]({pr_data.get('url', '')})",
        f"**State:** {pr_data.get('state', 'unknown')}",
        "",
        "---",
        "",
    ]

    if check_runs:
        lines.append("## Automated Checks")
        lines.append("")
        for run in check_runs:
            status_icon = (
                "❌"
                if run.conclusion in ("failure", "action_required")
                else "✅"
                if run.conclusion == "success"
                else "⚠️"
            )
            lines.append(f"### {status_icon} {run.name}")
            if run.details_url:
                lines.append(f"[Details]({run.details_url})")

            if run.annotations:
                lines.append("")
                for ann in run.annotations:
                    lines.append(
                        f"- **{ann.path}:{ann.start_line}** ({ann.annotation_level})"
                    )
                    lines.append(f"  {ann.message}")
            lines.append("")
        lines.append("---")
        lines.append("")

    for c in comments_raw:
        author = str(c.get("user", {}).get("login", "unknown"))
        date = str(c.get("created_at", ""))[:10] if c.get("created_at") else "unknown"
        lines.append(f"## {author} ({date})")
        lines.append("")
        lines.append(str(c.get("body", "")))
        lines.append("")
        lines.append("---")
        lines.append("")

    for r in reviews_raw:
        author = str(r.get("author", {}).get("login", "unknown"))
        date = str(r.get("submittedAt", ""))[:10] if r.get("submittedAt") else "unknown"
        lines.append(f"## {author} ({date})")
        lines.append("")
        lines.append(str(r.get("body", "")))
        lines.append("")
        lines.append("---")
        lines.append("")

    result = "\n".join(lines)
    if inp.output_file:
        inp.output_file.write_text(result)
        print(f"Wrote to {inp.output_file}", file=sys.stderr)

    return result


@validate_call
def generate_markdown(
    prs: list[PRRef], all_issues: dict[str, list[UnresolvedIssue]]
) -> str:
    """Generate markdown report for unresolved issues."""
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
        key = f"{pr.repo}#{pr.number}"
        issues = all_issues.get(key, [])
        if not issues:
            continue

        unresolved_count += len(issues)

        lines.append(f"## {pr.repo}")
        lines.append("")
        lines.append(f"### PR #{pr.number} — {pr.title or 'Unknown'}")
        lines.append(f"[Link]({pr.url or ''})")
        lines.append("")

        for i, issue in enumerate(issues, 1):
            lines.append(f"### {i}. {issue.author}")
            lines.append("")
            lines.append(issue.body)
            lines.append("")
            lines.append("---")
            lines.append("")

    lines.extend(
        [
            "## Summary",
            "",
            f"🔴 **NOT RESOLVED:** {unresolved_count}",
            "",
        ]
    )

    return "\n".join(lines)


@validate_call
def extract_issues_for_prs(prs: list[PRRef], output_file: Path | None = None) -> str:
    all_issues: dict[str, list[UnresolvedIssue]] = {}
    for pr in prs:
        key = f"{pr.repo}#{pr.number}"
        print(f"Checking {key}...", file=sys.stderr)

        try:
            output = run_gh(
                [
                    "pr",
                    "view",
                    str(pr.number),
                    "--repo",
                    pr.repo,
                    "--json",
                    "title,url,number",
                ]
            )
            pr_data = cast(dict[str, Any], json.loads(output))
            pr.title = cast(str, pr_data.get("title"))
            pr.url = cast(str, pr_data.get("url"))
        except subprocess.CalledProcessError:
            print(f"Failed to load PR metadata for {key}", file=sys.stderr)

        reviews, comments = get_pr_reviews(pr.repo, pr.number)
        issues = extract_all_unresolved_comments(comments)
        if issues:
            all_issues[key] = issues

    markdown = generate_markdown(prs, all_issues)
    if output_file:
        output_file.write_text(markdown)
        print(f"Wrote to {output_file}", file=sys.stderr)
    return markdown


@validate_call
def validate_justification(justification: str) -> bool:
    has_commit_ref = bool(
        re.search(r"/commit/[a-fA-F0-9]{6,40}", justification)
        or re.search(r"\bcommit\s+[a-fA-F0-9]{6,40}\b", justification, re.IGNORECASE)
        or re.search(r"\b[0-9a-fA-F]{6,40}\b", justification)
    )
    has_issue_ref = bool(
        re.search(r"#\d+", justification)
        or re.search(r"issues/\d+", justification)
        or re.search(r"\bissue\s+#?\d+", justification, re.IGNORECASE)
    )
    return has_commit_ref or has_issue_ref


@validate_call
def resolve_comment(inp: ResolveInput) -> dict[str, Any]:
    """Resolve a PR comment by minimizing the conversation."""
    if not validate_justification(inp.justification):
        raise ValueError(
            "Justification must include a commit reference (e.g., commit abc123 or /commit/) "
            "or an issue reference (e.g., #123 or issues/123)"
        )

    repo = inp.repo
    if not repo:
        try:
            result = run_gh(
                [
                    "repo",
                    "view",
                    "--json",
                    "nameWithOwner",
                    "-q",
                    ".nameWithOwner",
                ]
            )
            repo = result.strip()
        except subprocess.CalledProcessError:
            raise ValueError("Could not determine repository. Please specify --repo.")

    try:
        comment_result = run_gh(
            [
                "api",
                f"repos/{repo}/pulls/comments/{inp.comment_id}",
                "-q",
                ".pull_request_url",
            ]
        )
        pull_url = comment_result.strip()
        pull_number = pull_url.split("/")[-1]
        owner, name = repo.split("/")

        threads_query = (
            """query { repository(owner: "%s", name: "%s") { pullRequest(number: %s) { reviewThreads(first: 100) { nodes { id isResolved comments(first: 10) { nodes { id databaseId } } } } } } }"""
            % (owner, name, pull_number)
        )

        threads_result = run_gh(["api", "graphql", "--field", "query=" + threads_query])
        threads_data = cast(dict[str, Any], json.loads(threads_result))

        try:
            threads = cast(
                list[dict[str, Any]],
                threads_data.get("data", {})
                .get("repository", {})
                .get("pullRequest", {})
                .get("reviewThreads", {})
                .get("nodes", []),
            )
        except AttributeError:
            threads = []

        thread_id = None
        for thread in threads:
            thread_comments = cast(
                list[dict[str, Any]], thread.get("comments", {}).get("nodes", [])
            )
            for comment in thread_comments:
                if comment.get("databaseId") == int(inp.comment_id):
                    thread_id = str(thread.get("id"))
                    break
            if thread_id:
                break

        if not thread_id:
            raise ValueError(
                f"Could not find review thread for comment {inp.comment_id}"
            )

        resolve_query = (
            """mutation { resolveReviewThread(input: {threadId: "%s"}) { thread { isResolved } } }"""
            % thread_id
        )

        resolve_result = run_gh(["api", "graphql", "--field", "query=" + resolve_query])
        resolve_data = cast(dict[str, Any], json.loads(resolve_result))
        if resolve_data.get("errors"):
            raise ValueError(f"GraphQL error: {resolve_data['errors']}")

        return {
            "success": True,
            "comment_id": inp.comment_id,
            "thread_id": thread_id,
            "justification": inp.justification,
        }

    except subprocess.CalledProcessError as e:
        raise ValueError(f"Failed to resolve comment: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse GraphQL response: {e}")
