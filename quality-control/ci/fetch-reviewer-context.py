# /// script
# requires-python = ">=3.11"
# ///
"""
Generate a compact reviewer context file from code scanning alert state.

This context is given to review agents before they run, to prevent re-raising
existing issues without new evidence.

Queries code scanning alerts for the relevant tool categories
(ai-general-review, ai-slop-review) and formats them by state
(open, dismissed, fixed).

Usage:
  uv run quality-control/ci/fetch-reviewer-context.py \
    --repo owner/repo \
    --categories ai-general-review,ai-slop-review \
    --output .reviewer-context.md

The output is a markdown file with open/dismissed/fixed findings grouped
by state.  Pass it to the review agent as instructions:

  "Do not intentionally re-raise these issues unless you have new evidence,
  the problem reappears in a materially different form, or the previous
  resolution is directly contradicted by the current code."
"""

import argparse
import json
import subprocess
import sys


def _fail(msg: str) -> None:
    print(f"FATAL: {msg}", file=sys.stderr)
    sys.exit(1)


def _gh_api_json(
    method: str, path: str, params: dict | None = None, body: dict | None = None
) -> list | dict:
    args = ["gh", "api", "--method", method, path]
    if params:
        for k, v in params.items():
            args.extend(["--field", f"{k}={v}"])
    if body:
        args.extend(["--input", "-"])

    result = subprocess.run(
        args,
        capture_output=True,
        text=True,
        input=json.dumps(body) if body else None,
    )
    if result.returncode != 0:
        _fail(f"gh api {method} {path} failed: {result.stderr.strip()}")
    return json.loads(result.stdout)


def _fetch_alerts(repo: str, tool_name: str | None = None) -> list[dict]:
    """Fetch code scanning alerts for a repo, optionally filtering by tool.

    Returns an empty list when no analysis exists (404), which is the
    expected state before the first SARIF upload.
    """
    params: dict = {"per_page": "100"}
    if tool_name:
        params["tool_name"] = tool_name

    path = f"repos/{repo}/code-scanning/alerts"
    args = ["gh", "api", "--method", "GET", path]
    for k, v in params.items():
        args.extend(["--field", f"{k}={v}"])

    result = subprocess.run(args, capture_output=True, text=True)

    if result.returncode == 0:
        return json.loads(result.stdout)

    # 404 "no analysis found" is the pre-upload state — not a real failure
    if "no analysis found" in result.stderr:
        return []

    _fail(f"gh api GET {path} failed: {result.stderr.strip()}")


def _alert_label(alert: dict) -> str:
    """Extract finding label from alert properties or rule description."""
    props = (
        alert.get("most_recent_instance", {}).get("location", {}).get("properties", {})
    )
    if props and props.get("label"):
        return props["label"]
    rule = alert.get("rule", {})
    return rule.get("name", rule.get("id", "?"))


def _alert_category(alert: dict) -> str:
    props = (
        alert.get("most_recent_instance", {}).get("location", {}).get("properties", {})
    )
    if props and props.get("category"):
        return props["category"]
    return alert.get("rule", {}).get("id", "?")


def _alert_location(alert: dict) -> str:
    loc = alert.get("most_recent_instance", {}).get("location", {})
    path = loc.get("physical_location", {}).get("artifact_location", {}).get("uri", "?")
    region = loc.get("physical_location", {}).get("region", {})
    line = region.get("startLine", "?")
    return f"{path}:{line}"


def _alert_url(alert: dict) -> str:
    return alert.get("html_url", alert.get("url", "?"))


def _format_alert(alert: dict) -> str:
    label = _alert_label(alert)
    loc = _alert_location(alert)
    url = _alert_url(alert)
    return f"- **{label}** at `{loc}`  \n  Alert: {url}"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate reviewer context from code scanning alerts"
    )
    parser.add_argument(
        "--repo",
        required=True,
        help="Repository in owner/repo format",
    )
    parser.add_argument(
        "--categories",
        default="ai-general-review,ai-slop-review",
        help="Comma-separated list of tool/category names to query",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output file path (default: stdout)",
    )
    args = parser.parse_args()

    repo = args.repo
    categories = [c.strip() for c in args.categories.split(",") if c.strip()]

    lines: list[str] = []
    lines.append("## Existing repo-wide review findings")
    lines.append("")
    lines.append(
        "Do not intentionally re-raise these issues unless you have new "
        "evidence, the problem reappears in a materially different form, "
        "or the previous resolution is directly contradicted by the "
        "current code."
    )
    lines.append("")

    for cat in categories:
        try:
            alerts = _fetch_alerts(repo, tool_name=cat)
        except Exception as e:
            lines.append(f"### {cat}")
            lines.append("")
            lines.append(f"_Error querying alerts: {e}_")
            lines.append("")
            continue

        if not alerts:
            lines.append(f"### {cat}")
            lines.append("")
            lines.append("_No existing findings._")
            lines.append("")
            continue

        open_alerts = [a for a in alerts if a.get("state") == "open"]
        dismissed_alerts = [a for a in alerts if a.get("state") == "dismissed"]
        fixed_alerts = [a for a in alerts if a.get("state") == "fixed"]

        lines.append(f"### {cat}")

        if open_alerts:
            lines.append("")
            lines.append("**Open / accepted findings:**")
            for a in open_alerts:
                lines.append(_format_alert(a))

        if dismissed_alerts:
            lines.append("")
            lines.append("**Dismissed / rejected findings:**")
            for a in dismissed_alerts:
                reason = a.get("dismissed_reason", "?")
                comment = a.get("dismissed_comment", "")
                extra = f" ({reason}: {comment})" if comment else f" ({reason})"
                lines.append(_format_alert(a) + extra)

        if fixed_alerts:
            lines.append("")
            lines.append("**Fixed findings:**")
            for a in fixed_alerts:
                lines.append(_format_alert(a))

        lines.append("")

    output = "\n".join(lines).strip() + "\n"

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Reviewer context written to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
