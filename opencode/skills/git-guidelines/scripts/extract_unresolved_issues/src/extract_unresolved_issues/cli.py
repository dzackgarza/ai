import sys
from pathlib import Path

from cyclopts import App

from extract_unresolved_issues.logic import (
    extract_issues_for_prs,
    get_open_prs,
    parse_pr_url,
    resolve_comment,
    summarize_pr_comments,
)
from extract_unresolved_issues.models import (
    ResolveInput,
    SummarizeInput,
)

app = App()


@app.command
def summarize(
    pr_url: str,
    output_file: Path | None = None,
) -> None:
    """Summarize all PR comments (token-friendly).

    Args:
        pr_url: PR URL or owner/repo#num (e.g., https://github.com/owner/repo/pull/123 or owner/repo#123)
        output_file: File to write the output to. If not provided, prints to stdout.
    """
    inp = SummarizeInput(pr_url=pr_url, output_file=output_file)
    try:
        result = summarize_pr_comments(inp)
        if not output_file:
            try:
                from rich.console import Console
                from rich.markdown import Markdown

                console = Console()
                console.print(Markdown(result))
            except ImportError:
                print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


@app.command
def issues(
    pr_url: str,
    output_file: Path | None = None,
) -> None:
    """Extract unresolved issues from a PR.

    Args:
        pr_url: PR URL or owner/repo#num (e.g., https://github.com/owner/repo/pull/123 or owner/repo#123)
        output_file: File to write the output to. If not provided, prints to stdout.
    """
    try:
        pr_ref = parse_pr_url(pr_url)
        markdown = extract_issues_for_prs([pr_ref], output_file=output_file)
        if not output_file:
            print(markdown)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


@app.command(name="list")
def list_issues(
    repo: str | None = None,
    output_file: Path | None = None,
) -> None:
    """List unresolved issues across all open PRs.

    Args:
        repo: Filter by repository (owner/repo)
        output_file: File to write the output to. If not provided, prints to stdout.
    """
    print("Fetching open PRs...", file=sys.stderr)
    try:
        prs = get_open_prs()
        if repo:
            prs = [p for p in prs if p.repo == repo]

        print(f"Found {len(prs)} open PRs", file=sys.stderr)

        markdown = extract_issues_for_prs(prs, output_file=output_file)
        if not output_file:
            print(markdown)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


@app.command
def resolve(
    comment_id: str,
    justification: str,
    repo: str | None = None,
) -> None:
    """Resolve a PR comment with a required justification.

    Args:
        comment_id: ID of the comment to resolve
        justification: Justification string, must include commit hash or issue ref
        repo: Repository (owner/repo). If omitted, inferred from current dir.
    """
    inp = ResolveInput(comment_id=comment_id, justification=justification, repo=repo)
    try:
        resolve_comment(inp)
        print(f"✅ Resolved comment {comment_id}")
        print(f"   Justification: {justification}")
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
