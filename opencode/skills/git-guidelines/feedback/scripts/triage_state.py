#!/usr/bin/env python3
"""Structured, idempotent state for PR review-feedback triage.

Collects ALL review threads on a PR (paginated, no 100-cap), keys each finding by
a STABLE identity that survives line shifts and cross-run re-emission, records any
existing disposition stamps, and emits:

  - a machine state file (.pr/triage_state.json), keyed by stable id;
  - the human ledger (.pr/REVIEW_DISPOSITIONS.md) the skill prescribes;
  - a worklist on stdout: NEW | RE-RAISED | OPEN-PENDING | CLOSED per finding;
  - a convergence verdict (the loop terminates when NEW == 0 and OPEN-PENDING == 0).

Idempotent: re-running reconciles against existing state and existing thread
stamps. It never re-litigates a finding already dispositioned under the same
stable id, so a usage-limit death mid-round resumes cleanly.

Why a stable id, not (path:line): a commit shifts line numbers and the reviewer
re-posts the same finding as a new thread/comment id each push. Matching on
(path:line) or comment id therefore loses the thread or re-litigates it. The
ai-review-fingerprint (when present) is the reviewer's own stable id; otherwise a
content hash of (path + normalized finding title) is used.

Usage:
  triage_state.py [--repo owner/name] [--pr N] [--json] [--no-write]
Defaults: --repo and --pr are derived from the current branch's PR when omitted.
Requires: gh (authenticated). Standard library only.
"""
from __future__ import annotations
import argparse, hashlib, json, re, subprocess, sys
from pathlib import Path

FINGERPRINT_RE = re.compile(r"ai-review-fingerprint:\s*([0-9a-f]{8,})")
# Stamp markers written by the disposition/remediation/verification steps.
DISPOSITION_RE = re.compile(r"Disposition \(independent disposition subagent\):\s*(.+)", re.I)
VERIFICATION_RE = re.compile(r"Verification \(orchestrator-stamped\)", re.I)
COMMIT_RE = re.compile(r"\bCommit:\s*([0-9a-f]{7,40})", re.I)
VERDICT_RE = re.compile(r"\b(Accepted(?:\s+as\s+written|\s+with\s+modified\s+remediation)?|Rejected|Outdated|Duplicate|Investigate)\b", re.I)


def gh_graphql(query: str, **variables) -> dict:
    # gh casts -F values (int/bool/null) but passes -f values as strings; typed
    # GraphQL vars like $pr:Int! must go through -F or the call is rejected.
    args = ["gh", "api", "graphql", "-f", f"query={query}"]
    for key, val in variables.items():
        flag = "-F" if isinstance(val, int) and not isinstance(val, bool) else "-f"
        args += [flag, f"{key}={val}"]
    out = subprocess.run(args, capture_output=True, text=True)
    if out.returncode != 0:
        sys.exit(f"gh graphql failed: {out.stderr.strip()[:400]}")
    return json.loads(out.stdout)


def resolve_target(repo: str | None, pr: int | None) -> tuple[str, int]:
    if not repo:
        r = subprocess.run(["gh", "repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"],
                           capture_output=True, text=True)
        repo = r.stdout.strip()
    if not pr:
        r = subprocess.run(["gh", "pr", "view", "--json", "number", "-q", ".number"],
                           capture_output=True, text=True)
        if r.returncode != 0 or not r.stdout.strip():
            sys.exit("No PR for the current branch; pass --pr N.")
        pr = int(r.stdout.strip())
    if not repo or "/" not in repo:
        sys.exit("Could not resolve --repo owner/name.")
    return repo, int(pr)


def fetch_threads(repo: str, pr: int) -> list[dict]:
    owner, name = repo.split("/", 1)
    query = (
        "query($owner:String!,$name:String!,$pr:Int!,$cursor:String){"
        " repository(owner:$owner,name:$name){ pullRequest(number:$pr){"
        "  reviewThreads(first:100, after:$cursor){ pageInfo{hasNextPage endCursor}"
        "   nodes{ id isResolved isOutdated path line"
        "    comments(first:30){ nodes{ databaseId author{login} body createdAt }}}}}}}"
    )
    threads, cursor = [], None
    while True:
        data = gh_graphql(query, owner=owner, name=name, pr=int(pr), **({"cursor": cursor} if cursor else {}))
        conn = data["data"]["repository"]["pullRequest"]["reviewThreads"]
        threads += conn["nodes"]
        if conn["pageInfo"]["hasNextPage"]:
            cursor = conn["pageInfo"]["endCursor"]
        else:
            return threads


def normalized_title(body: str) -> str:
    """First meaningful line, stripped of tier/badge/markup, lowercased."""
    for raw in body.splitlines():
        line = re.sub(r"<!--.*?-->", "", raw)
        line = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", line)  # badge images
        line = re.sub(r"[#>*`\[\]]", "", line)
        line = re.sub(r"\[(General|Slop) Review\]\[tier\d\]", "", line, flags=re.I)
        line = re.sub(r"ai-review/\w+\s*/", "", line)
        line = line.strip()
        if len(line) >= 8:
            return line.lower()[:160]
    return body.strip().lower()[:160]


def stable_key(thread: dict) -> str:
    first = thread["comments"]["nodes"][0]["body"] if thread["comments"]["nodes"] else ""
    m = FINGERPRINT_RE.search(first)
    if m:
        return f"fp:{m.group(1)}"
    digest = hashlib.sha1(f"{thread['path']}|{normalized_title(first)}".encode()).hexdigest()[:16]
    return f"ct:{digest}"


def disposition_of(thread: dict) -> dict | None:
    """Best-effort parse of any landed stamp on the thread (skip the finding itself)."""
    nodes = thread["comments"]["nodes"]
    for c in nodes[1:]:
        body = c["body"] or ""
        if DISPOSITION_RE.search(body) or VERDICT_RE.search(body.splitlines()[0] if body else ""):
            verdict = (VERDICT_RE.search(body) or [None, "unknown"])[1]
            return {
                "verdict": verdict.lower() if verdict else "unknown",
                "has_verification": bool(VERIFICATION_RE.search(body)),
                "commit": (COMMIT_RE.search(body).group(1) if COMMIT_RE.search(body) else None),
                "by": c["author"]["login"] if c["author"] else None,
            }
    return None


ACCEPT_VERDICTS = ("accepted", "accepted as written", "accepted with modified remediation", "investigate")


def classify(thread: dict, disp: dict | None) -> str:
    if thread["isResolved"]:
        return "CLOSED"
    if disp is None:
        return "NEW"  # open, no landed disposition -> needs a disposition this round
    if any(disp["verdict"].startswith(v) for v in ACCEPT_VERDICTS):
        # accepted/investigate but still open -> remediation/closure pending
        return "OPEN-PENDING"
    # open but stamped reject/outdated/duplicate that was never resolved -> resolve it
    return "OPEN-PENDING"


def build_ledger(records: list[dict]) -> str:
    acc = [r for r in records if r["state"] in ("OPEN-PENDING", "CLOSED") and r["disp"] and any(
        r["disp"]["verdict"].startswith(v) for v in ("accepted",))]
    rej = [r for r in records if r["disp"] and any(r["disp"]["verdict"].startswith(v) for v in ("rejected", "outdated", "duplicate"))]
    openn = [r for r in records if r["state"] in ("NEW", "OPEN-PENDING")]
    lines = ["# Review dispositions", "", "_Generated by triage_state.py; keyed by stable finding id (fingerprint or content hash)._", ""]
    lines += ["## Accepted and remediated", ""]
    for r in acc:
        lines += [f"### {r['path']}:{r['line']} ({r['key']})",
                  f"- Verdict: {r['disp']['verdict']}",
                  f"- Commit: {r['disp']['commit'] or '(none recorded)'}",
                  f"- Verification stamp present: {r['disp']['has_verification']}",
                  f"- Thread: {r['thread_id']}", ""]
    lines += ["## Rejected / Outdated / Duplicate", ""]
    for r in rej:
        lines += [f"### {r['path']}:{r['line']} ({r['key']})  — {r['disp']['verdict']}",
                  f"- Thread: {r['thread_id']}", ""]
    lines += ["## Still open", ""]
    for r in openn:
        lines += [f"### {r['path']}:{r['line']} ({r['key']})  — {r['state']}",
                  f"- Thread: {r['thread_id']}", ""]
    return "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description="Structured idempotent PR review-triage state.")
    ap.add_argument("--repo")
    ap.add_argument("--pr", type=int)
    ap.add_argument("--json", action="store_true", help="emit the worklist as JSON")
    ap.add_argument("--no-write", action="store_true", help="do not write .pr/ artifacts")
    args = ap.parse_args()

    repo, pr = resolve_target(args.repo, args.pr)
    threads = fetch_threads(repo, pr)

    records, seen = [], {}
    for t in threads:
        key = stable_key(t)
        disp = disposition_of(t)
        state = classify(t, disp)
        rec = {"key": key, "thread_id": t["id"], "path": t["path"], "line": t["line"],
               "resolved": t["isResolved"], "outdated": t["isOutdated"], "state": state, "disp": disp}
        records.append(rec)
        # A stable key seen with a prior landed disposition makes an open re-post a RE-RAISED, not NEW.
        if key in seen and state == "NEW" and seen[key].get("disp"):
            rec["state"] = "RE-RAISED"
        seen[key] = rec

    counts: dict[str, int] = {}
    for r in records:
        counts[r["state"]] = counts.get(r["state"], 0) + 1
    new = counts.get("NEW", 0)
    pending = counts.get("OPEN-PENDING", 0)
    converged = (new == 0 and pending == 0)

    if not args.no_write:
        out = Path(".pr"); out.mkdir(exist_ok=True)
        (out / "triage_state.json").write_text(json.dumps(
            {"repo": repo, "pr": pr, "counts": counts, "converged": converged, "records": records}, indent=1))
        (out / "REVIEW_DISPOSITIONS.md").write_text(build_ledger(records))

    if args.json:
        print(json.dumps({"counts": counts, "converged": converged,
                          "worklist": [r for r in records if r["state"] in ("NEW", "RE-RAISED", "OPEN-PENDING")]}, indent=1))
        return

    print(f"{repo} PR #{pr}: {len(records)} threads  " + "  ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    print(f"CONVERGED: {converged}  (terminate the loop only when NEW=0 and OPEN-PENDING=0)\n")
    for state in ("NEW", "OPEN-PENDING", "RE-RAISED"):
        rows = [r for r in records if r["state"] == state]
        if not rows:
            continue
        print(f"== {state} ({len(rows)}) ==")
        for r in rows:
            v = f" [{r['disp']['verdict']}]" if r["disp"] else ""
            print(f"  {r['path']}:{r['line']}  {r['key']}{v}  {r['thread_id'][-8:]}")
        print()


if __name__ == "__main__":
    main()
