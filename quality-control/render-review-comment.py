# /// script
# requires-python = ">=3.11"
# ///
"""
Render a validated review artifact (JSON) into a uniform PR comment (markdown).

Reads the artifact JSON from the first argument, produces a markdown comment
on stdout with a machine-parseable score anchor:

    **Score: 80/100**

The score is derived from findings:
  - Start at 100
  - Subtract 20 per Tier 1 finding
  - Subtract 5 per Tier 2 finding
  - Floor at 0
"""

import json
import pathlib
import sys


def compute_score(findings: list[dict]) -> int:
    tier1 = sum(1 for f in findings if f.get("tier") == "tier1")
    tier2 = sum(1 for f in findings if f.get("tier") == "tier2")
    raw = 100 - (tier1 * 20) - (tier2 * 5)
    return max(0, raw)


def render_evidence(evidence: list[dict]) -> str:
    lines = []
    for ev in evidence:
        p = ev.get("path", "?")
        lo, hi = (ev.get("lines") or ["?", "?"])[:2]
        lines.append(f"- `{p}:{lo}-{hi}` ({ev.get('kind', '?')})")
    return "\n".join(lines)


def render_checked_surfaces(surfaces: list[dict]) -> str:
    if not surfaces:
        return "_None._"
    rows = ["| Path | Reason | Lines | Result |", "|------|--------|-------|--------|"]
    for s in surfaces:
        lo, hi = (s.get("lines_read") or ["?", "?"])[:2]
        rows.append(
            f"| `{s['path']}` | {s.get('reason', '?')} | {lo}-{hi} | {s.get('result', '?')} |"
        )
    return "\n".join(rows)


def render_finding(n: int, f: dict) -> str:
    tier = f.get("tier", "?")
    label = f.get("label", "?")
    category = f.get("category", "?")
    loc = f.get("location", {})
    loc_path = loc.get("path", "?")
    start = loc.get("start_line", "?")
    end = loc.get("end_line", "?")
    violated = f.get("violated_invariant", "")
    proof = f.get("proof_command", "")

    lines = [
        f"### Finding {n}: {label} ({category}, {tier})",
        "",
        f"**Location:** `{loc_path}:{start}-{end}`",
    ]
    if violated:
        lines.append(f"**Violated invariant:** {violated}")
    if proof:
        lines.append(f"**Proof command:** `{proof}`")
    lines.append("")

    # General review fields
    if "symptom" in f:
        lines.append("| Field | Detail |")
        lines.append("|-------|--------|")
        for field in ["symptom", "source", "consequence", "remedy"]:
            lines.append(f"| **{field.capitalize()}** | {f.get(field, '')} |")
        lines.append("")

    # Slop review fields
    if "pattern" in f:
        slop_fields = [
            ("Pattern", "pattern"),
            ("Original task", "task_narrative"),
            ("Slop narrative", "slop_narrative"),
            ("Why this matters", "why_it_matters"),
            ("User surprise", "user_surprise"),
            ("Existential justification", "existential_justification"),
            ("Failure mode", "failure_mode"),
        ]
        lines.append("| Field | Detail |")
        lines.append("|-------|--------|")
        for label_k, key in slop_fields:
            lines.append(f"| **{label_k}** | {f.get(key, '')} |")
        lines.append("")

    evidence = f.get("evidence", [])
    if evidence:
        lines.append("**Evidence:**")
        lines.append(render_evidence(evidence))
        lines.append("")

    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    if len(sys.argv) < 2:
        print(f"Usage: uv run {sys.argv[0]} <artifact.json>", file=sys.stderr)
        sys.exit(1)

    artifact_path = pathlib.Path(sys.argv[1])
    if not artifact_path.is_file():
        print(f"Error: file not found: {artifact_path}", file=sys.stderr)
        sys.exit(1)

    with open(artifact_path) as f:
        data = json.load(f)

    report_type = data.get("report_type", "unknown")
    findings = data.get("findings", [])
    checked_surfaces = data.get("checked_surfaces", [])
    rejected_easy_wins = data.get("rejected_easy_wins", [])

    score = compute_score(findings)
    tier1_count = sum(1 for f in findings if f.get("tier") == "tier1")
    tier2_count = sum(1 for f in findings if f.get("tier") == "tier2")

    lines = [
        f"# Code Review: {report_type}",
        "",
        f"**Score: {score}/100**",
        "",
        "## Summary",
        "",
        f"- Tier 1 findings: {tier1_count}",
        f"- Tier 2 findings: {tier2_count}",
        f"- Score: {score}/100 (base 100, -20 per Tier 1, -5 per Tier 2, min 0)",
        "",
    ]

    if findings:
        lines.append("## Findings")
        lines.append("")
        for i, f in enumerate(findings, 1):
            lines.append(render_finding(i, f))

    lines.append("## Checked Surfaces")
    lines.append("")
    lines.append(render_checked_surfaces(checked_surfaces))
    lines.append("")

    if rejected_easy_wins:
        lines.append("## Rejected Easy Wins")
        lines.append("")
        for r in rejected_easy_wins:
            lines.append(f"- {r}")
        lines.append("")

    print("\n".join(lines))


if __name__ == "__main__":
    main()
