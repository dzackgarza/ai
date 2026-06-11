# /// script
# requires-python = ">=3.11"
# ///
"""
Review harness: assembles the reviewer prompt and loops opencode until a
validated report artifact exists.

Prompt assembly order: reviewer context (existing tracked findings), scope
instructions (repo-wide sweep or PR diff), manifest documents (skills and
guides, statically declared per review type), repo docs, task template.

The agent writes a candidate report to a fixed path, then calls
submit-candidate (no arguments) to validate and submit. submit-candidate
copies the validated report to .review-report-artifact.json. This harness
only checks for that artifact's existence after each opencode invocation;
on timeout or a missing artifact it continues the session with
`opencode run -c`.
"""

import argparse
import os
import pathlib
import subprocess
import sys
import time

IGNORE_DIRS = {
    ".git",
    "node_modules",
    ".venv",
    "__pycache__",
    "dist",
    "build",
    ".next",
    "coverage",
}

ARTIFACT_PATH = pathlib.Path(".review-report-artifact.json")
MAX_ATTEMPTS = 5
OPENCODE_TIMEOUT = 600


def collect_repo_docs(repo_root: pathlib.Path) -> str:
    sections = []
    for pattern in ("*README.md", "*AGENTS.md", "*AGENTS*.md"):
        for p in repo_root.rglob(pattern):
            rel = p.relative_to(repo_root)
            if any(part in IGNORE_DIRS for part in p.parts):
                continue
            if not p.is_file() or p.stat().st_size > 500_000:
                continue
            sections.append(f"### Repo doc: {rel}\n\n{p.read_text()}")
    return (
        "## Repo Documentation\n\n" + "\n\n---\n\n".join(sections) if sections else ""
    )


def load_manifest(manifest_path: pathlib.Path) -> str:
    """Inline every document listed in the manifest, in order.

    One repo-relative path per line. A directory entry inlines all of its
    top-level *.md files, sorted by name. Missing entries are fatal.
    """
    sections = []
    for raw in manifest_path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        p = pathlib.Path(line)
        if p.is_dir():
            files = sorted(p.glob("*.md"))
            if not files:
                print(f"FATAL: manifest dir has no .md files: {p}", file=sys.stderr)
                sys.exit(1)
            sections.extend(f.read_text() for f in files)
        elif p.is_file():
            sections.append(p.read_text())
        else:
            print(f"FATAL: manifest entry not found: {p}", file=sys.stderr)
            sys.exit(1)
    if not sections:
        print(f"FATAL: manifest is empty: {manifest_path}", file=sys.stderr)
        sys.exit(1)
    return "\n\n---\n\n".join(sections)


SUBMITTED_CANDIDATE = "submitted.json"


def run_opencode(task_path: pathlib.Path, *, continue_session: bool) -> int:
    cmd = ["opencode", "run"]
    if continue_session:
        cmd.append("-c")

    env = {
        **os.environ,
        "OPENCODE_PURE": "1",
        "RUNNER_TEMP": str(task_path.parent.parent),
    }
    with open(task_path) as f:
        res = subprocess.run(
            cmd,
            stdin=f,
            capture_output=True,
            text=True,
            check=False,
            timeout=OPENCODE_TIMEOUT,
            env=env,
        )

    sys.stdout.write(res.stdout)
    sys.stderr.write(res.stderr)
    return res.returncode


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--template", required=True)
    parser.add_argument("--scope", required=True, help="Path to scope instructions md")
    parser.add_argument("--manifest", required=True, help="Path to prompt manifest")
    parser.add_argument(
        "--reviewer-context",
        required=True,
        help="Path to reviewer context file (existing tracked findings)",
    )
    args = parser.parse_args()

    template_path = pathlib.Path(args.template)
    scope_path = pathlib.Path(args.scope)
    manifest_path = pathlib.Path(args.manifest)
    ctx_path = pathlib.Path(args.reviewer_context)
    for p in (template_path, scope_path, manifest_path, ctx_path):
        if not p.is_file():
            print(f"FATAL: required input not found: {p}", file=sys.stderr)
            sys.exit(1)

    run_dir = pathlib.Path(".agents/review-runner").resolve()
    candidates_dir = run_dir / "candidates"
    candidates_dir.mkdir(parents=True, exist_ok=True)
    task_path = run_dir / "task.md"

    body = template_path.read_text()
    sections = [
        ctx_path.read_text(),
        scope_path.read_text(),
        load_manifest(manifest_path),
    ]
    repo_docs = collect_repo_docs(pathlib.Path.cwd())
    if repo_docs:
        sections.append(repo_docs)
    sections.append(body)
    initial_prompt = "\n\n".join(sections)

    submitted_path = candidates_dir / SUBMITTED_CANDIDATE

    for attempt in range(1, MAX_ATTEMPTS + 1):
        if attempt > 1:
            time.sleep(5)
            prompt = (
                f"The previous invocation in this opencode session ended without "
                f"a valid report at {ARTIFACT_PATH}. Continue the existing session. "
                f"Write the report to {submitted_path}, then run "
                f"submit-candidate with no arguments."
            )
        else:
            prompt = initial_prompt

        task_path.write_text(prompt)
        print(f"--- opencode run attempt {attempt}/{MAX_ATTEMPTS} ---", file=sys.stderr)
        # Clear any prior files to prevent stale submissions
        submitted_path.unlink(missing_ok=True)
        ARTIFACT_PATH.unlink(missing_ok=True)
        try:
            run_opencode(task_path, continue_session=(attempt > 1))
        except subprocess.TimeoutExpired:
            print("--- opencode timed out ---", file=sys.stderr)
        except FileNotFoundError:
            print(
                "FATAL: 'opencode' executable not found in PATH. "
                "This is a non-transient failure — exiting immediately.",
                file=sys.stderr,
            )
            sys.exit(1)

        if ARTIFACT_PATH.exists():
            print("--- Report artifact submitted ---", file=sys.stderr)
            sys.exit(0)

    print(f"FATAL: No report artifact after {MAX_ATTEMPTS} attempts", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
