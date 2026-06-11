# /// script
# requires-python = ">=3.11"
# ///
"""
Post validated review findings to a PR as one review with resolvable threads.

Runner-side automation: consumes the validated artifact and the PR diff,
never involves the reviewer agent. One review per run: a top-level body
(summary + metadata) plus one inline, individually-resolvable comment per
finding. Findings are deduplicated against threads already on the PR via a
fingerprint marker (same components as the SARIF reviewFindingKey:
category | path — see report-to-sarif.py; agent-chosen labels are excluded
because they are free text reinvented each run).

Anchor classification (computed from the diff before posting, no fallbacks):
- a finding line visible in the diff       -> line-anchored thread
- file in diff, lines outside its hunks    -> thread on the file's first
                                              visible line (body carries the
                                              real range)
- file not in the diff                     -> listed in the top-level body
                                              only (already tracked in code
                                              scanning)

Thread bodies are diagnosis-only: no remediation is rendered or expected.
"""

import argparse
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys

FINGERPRINT_MARKER = "ai-review-fingerprint:"
REVIEW_LABELS = {"general": "General Review", "slop": "Slop Review"}

THREADS_QUERY = """
query($owner: String!, $name: String!, $number: Int!, $cursor: String) {
  repository(owner: $owner, name: $name) {
    pullRequest(number: $number) {
      reviewThreads(first: 100, after: $cursor) {
        pageInfo { hasNextPage endCursor }
        nodes { comments(first: 1) { nodes { body } } }
      }
    }
  }
}
"""


def _fail(msg: str) -> None:
    print(f"FATAL: {msg}", file=sys.stderr)
    sys.exit(1)


def _gh_json(args: list[str], body: dict | None = None) -> dict | list:
    result = subprocess.run(
        ["gh", *args],
        capture_output=True,
        text=True,
        input=json.dumps(body) if body is not None else None,
    )
    if result.returncode != 0:
        _fail(f"gh {' '.join(args[:3])} failed: {result.stderr.strip()}")
    return json.loads(result.stdout)


def _fingerprint(category: str, path: str) -> str:
    raw = "|".join([category, path])
    return hashlib.sha256(raw.encode()).hexdigest()


def parse_diff(text: str) -> dict[str, set[int]]:
    """Map each file in the diff to its commentable RIGHT-side line numbers.

    Commentable lines are those visible in the unified diff on the new side:
    added lines and context lines within hunks. Deleted files have no new
    side and are omitted.
    """
    files: dict[str, set[int]] = {}
    current: str | None = None
    new_line: int | None = None
    for line in text.splitlines():
        if line.startswith("+++ "):
            target = line[4:].split("\t")[0]
            if target == "/dev/null":
                current = None
            else:
                current = target[2:] if target.startswith("b/") else target
                files.setdefault(current, set())
            new_line = None
        elif line.startswith("@@"):
            m = re.match(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", line)
            if not m:
                _fail(f"unparseable hunk header: {line}")
            new_line = int(m.group(1))
        elif current is not None and new_line is not None:
            if line.startswith("+"):
                files[current].add(new_line)
                new_line += 1
            elif line.startswith("-") or line.startswith("\\"):
                pass
            elif line.startswith(" ") or line == "":
                files[current].add(new_line)
                new_line += 1
            else:
                # diff --git / index / similarity headers end the hunk body
                new_line = None
    return files


def existing_fingerprints(repo: str, pr_number: int) -> set[str]:
    """Fingerprints already present in any review thread on the PR.

    Resolved threads count: a resolved thread is a disposition, equivalent
    to a dismissed alert — the finding is not re-posted.
    """
    owner, name = repo.split("/")
    found: set[str] = set()
    cursor: str | None = None
    while True:
        args = [
            "api", "graphql",
            "-f", f"query={THREADS_QUERY}",
            "-F", f"owner={owner}",
            "-F", f"name={name}",
            "-F", f"number={pr_number}",
        ]
        if cursor:
            args.extend(["-F", f"cursor={cursor}"])
        data = _gh_json(args)
        threads = data["data"]["repository"]["pullRequest"]["reviewThreads"]
        for node in threads["nodes"]:
            for comment in node["comments"]["nodes"]:
                for m in re.finditer(
                    re.escape(FINGERPRINT_MARKER) + r"\s*([0-9a-f]{64})",
                    comment["body"],
                ):
                    found.add(m.group(1))
        if not threads["pageInfo"]["hasNextPage"]:
            break
        cursor = threads["pageInfo"]["endCursor"]
    return found


def pick_anchor(finding: dict, commentable: dict[str, set[int]]) -> int | None:
    """Best RIGHT-side anchor line for a finding, or None if file is off-diff."""
    loc = finding["location"]
    lines = commentable.get(str(loc["path"]))
    if not lines:
        return None
    for ln in range(loc["start_line"], loc["end_line"] + 1):
        if ln in lines:
            return ln
    return min(lines)


def render_thread_body(finding: dict, review_label: str, fp: str) -> str:
    loc = finding["location"]
    lines = [
        f"### [{review_label}][{finding['tier']}] {finding['label']}",
        f"<!-- {FINGERPRINT_MARKER} {fp} -->",
        "",
        f"**Location:** `{loc['path']}:{loc['start_line']}-{loc['end_line']}`",
        f"**Violated invariant:** {finding['violated_invariant']}",
        f"**Proof:** `{finding['proof_command']}`",
    ]
    for key, title in [
        ("symptom", "Symptom"),
        ("source", "Source"),
        ("consequence", "Consequence"),
        ("pattern", "Pattern"),
        ("why_it_matters", "Why this matters"),
    ]:
        if finding.get(key):
            lines.append(f"**{title}:** {finding[key]}")
    ev_parts = [
        f"`{e['path']}:{e['lines'][0]}-{e['lines'][1]}` ({e['kind']})"
        for e in finding["evidence"]
    ]
    lines.append(f"**Evidence:** {', '.join(ev_parts)}")
    return "\n".join(lines)


def render_review_body(
    review_label: str,
    findings: list[dict],
    posted: int,
    skipped: int,
    off_diff: list[dict],
) -> str:
    run_url = (
        f"{os.environ['GITHUB_SERVER_URL']}/{os.environ['GITHUB_REPOSITORY']}"
        f"/actions/runs/{os.environ['GITHUB_RUN_ID']}"
    )
    tier1 = sum(1 for f in findings if f["tier"] == "tier1")
    tier2 = sum(1 for f in findings if f["tier"] == "tier2")
    lines = [
        f"## {review_label} — automated PR review",
        "",
        f"Run: {run_url}",
        f"Findings: {len(findings)} (tier1 {tier1}, tier2 {tier2}) | "
        f"threads posted: {posted} | duplicates skipped: {skipped} | "
        f"off-diff (tracker only): {len(off_diff)}",
    ]
    if off_diff:
        lines.extend(
            [
                "",
                "### Off-diff findings (tracked in code scanning, no thread)",
                "",
            ]
        )
        for f in off_diff:
            loc = f["location"]
            lines.append(
                f"- `{loc['path']}:{loc['start_line']}-{loc['end_line']}` — "
                f"[{f['tier']}] {f['label']}: {f['violated_invariant']}"
            )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Post validated findings as resolvable PR review threads"
    )
    parser.add_argument("--artifact", required=True, type=pathlib.Path)
    parser.add_argument("--diff", required=True, type=pathlib.Path)
    parser.add_argument("--repo", required=True, help="owner/repo")
    parser.add_argument("--pr-number", required=True, type=int)
    args = parser.parse_args()

    artifact = json.loads(args.artifact.read_text())
    report_type = artifact["report_type"]
    review_label = REVIEW_LABELS[report_type]
    findings = artifact["findings"]

    commentable = parse_diff(args.diff.read_text())
    seen = existing_fingerprints(args.repo, args.pr_number)

    comments: list[dict] = []
    off_diff: list[dict] = []
    skipped = 0
    for finding in findings:
        loc = finding["location"]
        fp = _fingerprint(finding["category"], str(loc["path"]))
        if fp in seen:
            skipped += 1
            continue
        seen.add(fp)
        anchor = pick_anchor(finding, commentable)
        if anchor is None:
            off_diff.append(finding)
            continue
        comments.append(
            {
                "path": str(loc["path"]),
                "line": anchor,
                "side": "RIGHT",
                "body": render_thread_body(finding, review_label, fp),
            }
        )

    if not comments and not off_diff:
        print(
            f"All {len(findings)} finding(s) already have threads on "
            f"PR #{args.pr_number}; nothing to post."
        )
        return

    payload = {
        "event": "COMMENT",
        "body": render_review_body(
            review_label, findings, len(comments), skipped, off_diff
        ),
        "comments": comments,
    }
    _gh_json(
        [
            "api",
            "--method", "POST",
            f"repos/{args.repo}/pulls/{args.pr_number}/reviews",
            "--input", "-",
        ],
        body=payload,
    )
    print(
        f"Posted review to PR #{args.pr_number}: {len(comments)} thread(s), "
        f"{skipped} duplicate(s) skipped, {len(off_diff)} off-diff."
    )


if __name__ == "__main__":
    main()
