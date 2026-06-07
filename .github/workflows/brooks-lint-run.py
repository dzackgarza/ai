# /// script
# requires-python = ">=3.11"
# ///
"""
Brooks-Lint runner: assembles skills + template + diff, runs opencode.

The agent MUST submit its report by calling:
  just -f .agents/justfile post-brooks-review <tmp-json> <pr-number>

That recipe validates the report. If valid, it writes .brooks-report-artifact.json.
If invalid, it exits non-zero and the agent retries.

This script loops until .brooks-report-artifact.json appears (agent succeeded)
or max retries exhausted.

Usage:
  python3 brooks-lint-run.py [--mode review] [--skills-dir SKILLS]
    [--base-ref REF] [--template TEMPLATE] [--pr-number N]
"""

import argparse
import os
import pathlib
import subprocess
import sys
import time

IGNORE_DIRS = frozenset(
    {
        ".git",
        "node_modules",
        ".venv",
        "__pycache__",
        "dist",
        "build",
        ".next",
        "coverage",
    }
)

ARTIFACT_PATH = pathlib.Path(".brooks-report-artifact.json")
CHECKER_PATH = pathlib.Path(".agents/scripts/check-brooks-report.py")
MAX_ATTEMPTS = 5
OPENCODE_TIMEOUT = 600


def collect_repo_docs(repo_root: pathlib.Path) -> str:
    """Find all README.md and AGENTS.md files. Inject as context so the model
    cannot skip reading project documentation before making findings."""
    sections = []
    for pattern in ("*README.md", "*AGENTS.md", "*AGENTS*.md"):
        for p in repo_root.rglob(pattern):
            rel = p.relative_to(repo_root)
            if any(part in IGNORE_DIRS for part in p.parts):
                continue
            if not p.is_file():
                continue
            if p.stat().st_size > 500_000:
                continue
            sections.append(f"### Repo doc: {rel}\n\n{p.read_text()}")
    if not sections:
        return ""
    return "## Repo Documentation\n\n" + "\n\n---\n\n".join(sections)


def load_skills(skills_dir: pathlib.Path, slop_mode: bool = False) -> str:
    """Load and concatenate all shared and mode-specific skill guides."""
    _shared = skills_dir / "_shared"
    guides = []

    for fname in ["common.md", "source-coverage.md", "decay-risks.md"]:
        path = _shared / fname
        if path.exists():
            guides.append(path.read_text())

    ci_protocol = pathlib.Path("opencode/skills/_shared/ci-sweep-protocol.md").resolve()
    guides.append(ci_protocol.read_text())

    skills_repo = pathlib.Path("opencode/skills").resolve()
    for skill_name in [
        "policy-index",
        "bespoke-software-policy",
        "anti-slop",
        "reviewing-llm-code",
        "fixing-slop",
        "test-guidelines",
        "tool-provisioning-and-environment-hygiene",
    ]:
        path = skills_repo / skill_name / "SKILL.md"
        guides.append(path.read_text())

    if slop_mode:
        for ref_dir in [
            skills_repo / "reviewing-llm-code" / "references",
            skills_repo / "anti-slop" / "references",
        ]:
            for ref_file in sorted(ref_dir.iterdir()):
                if ref_file.suffix == ".md":
                    guides.append(ref_file.read_text())
    else:
        ref_path = (
            skills_repo
            / "reviewing-llm-code"
            / "references"
            / "bridge-burning-red-flags.md"
        )
        guides.append(ref_path.read_text())

    for guide_dir, fname in [
        ("brooks-review", "pr-review-guide.md"),
    ]:
        path = skills_dir / guide_dir / fname
        if path.exists():
            guides.append(path.read_text())

    repo_docs = collect_repo_docs(pathlib.Path.cwd())
    if repo_docs:
        guides.append(repo_docs)

    return "\n\n---\n\n".join(guides)


def get_diff(base_ref: str | None) -> str:
    """Get the PR diff against base_ref, falling back to HEAD~1."""
    if base_ref:
        try:
            result = subprocess.run(
                ["git", "diff", f"origin/{base_ref}...HEAD"],
                capture_output=True,
                text=True,
                check=False,
                timeout=30,
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout
        except Exception:
            pass

    try:
        result = subprocess.run(
            ["git", "diff", "HEAD~1"],
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
        )
        if result.returncode == 0:
            return result.stdout or ""
    except Exception:
        pass

    return ""


def substitute(template: str, **kwargs: str) -> str:
    """Replace {{KEY}} placeholders, leaving unknown placeholders intact."""
    for key, value in kwargs.items():
        template = template.replace("{{" + key + "}}", value)
    return template


def validate_artifact() -> bool:
    """Re-validate artifact in case agent bypassed the just recipe.
    Returns True only if the checker script passes."""
    if not ARTIFACT_PATH.exists():
        return False
    result = subprocess.run(
        [str(CHECKER_PATH), str(ARTIFACT_PATH)],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        print(
            "--- Artifact re-validation FAILED (agent may have bypassed recipe) ---",
            file=sys.stderr,
            flush=True,
        )
        for line in (result.stdout or "").strip().splitlines():
            print(f"  checker: {line}", file=sys.stderr)
        for line in (result.stderr or "").strip().splitlines():
            print(f"  checker err: {line}", file=sys.stderr)
    return result.returncode == 0


def run_opencode(prompt: str) -> int:
    """Run opencode with prompt on stdin. Output flows to parent's stdout/stderr."""
    result = subprocess.run(
        [
            "opencode",
            "run",
            "--model",
            "opencode/deepseek-v4-flash-free",
            "--dangerously-skip-permissions",
            "--file",
            "/dev/stdin",
        ],
        input=prompt,
        text=True,
        check=False,
        timeout=OPENCODE_TIMEOUT,
        env={**os.environ, "OPENCODE_PURE": "1"},
    )
    return result.returncode


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run brooks-lint review via opencode (loops until artifact created)"
    )
    parser.add_argument("--mode", default="review")
    parser.add_argument(
        "--skills-dir",
        default="opencode/skills",
        help="Path to skills directory",
    )
    parser.add_argument("--base-ref", default=None, help="Git base ref for diff")
    parser.add_argument(
        "--template",
        default=".github/workflows/brooks-review-template.md",
    )
    parser.add_argument(
        "--pr-number",
        default=None,
        help="PR number for the agent to use when calling the recipe",
    )
    args = parser.parse_args()

    skills_dir = pathlib.Path(args.skills_dir)
    template_path = pathlib.Path(args.template)

    if not skills_dir.is_dir():
        print(f"FATAL: Skills directory not found: {skills_dir}", file=sys.stderr)
        sys.exit(1)
    if not template_path.is_file():
        print(f"FATAL: Template not found: {template_path}", file=sys.stderr)
        sys.exit(1)

    # Assemble the prompt
    system = load_skills(skills_dir, slop_mode=(args.mode == "slop"))
    diff = get_diff(args.base_ref)
    template = template_path.read_text()
    body = substitute(template, DIFF=diff, PR_NUMBER=args.pr_number or "0")
    prompt = f"{system}\n\n{body}"

    # Loop: run opencode until artifact appears or max attempts exhausted
    for attempt in range(1, MAX_ATTEMPTS + 1):
        if attempt > 1:
            time.sleep(5)

        print(
            f"--- opencode run attempt {attempt}/{MAX_ATTEMPTS} ---",
            file=sys.stderr,
            flush=True,
        )

        try:
            run_opencode(prompt)
        except subprocess.TimeoutExpired:
            print(
                f"--- opencode timed out after {OPENCODE_TIMEOUT}s ---",
                file=sys.stderr,
                flush=True,
            )
        except FileNotFoundError:
            print("FATAL: opencode not found in PATH", file=sys.stderr)
            sys.exit(1)

        if ARTIFACT_PATH.exists():
            if validate_artifact():
                print(
                    f"--- Report artifact validated ({ARTIFACT_PATH.stat().st_size} bytes) ---",
                    file=sys.stderr,
                    flush=True,
                )
                sys.exit(0)
            else:
                # Agent bypassed the recipe — delete and retry
                ARTIFACT_PATH.unlink()
                print(
                    "--- Invalid artifact removed, retrying ---",
                    file=sys.stderr,
                    flush=True,
                )
                continue

        print(
            "--- No artifact found. Agent did not submit a valid report ---",
            file=sys.stderr,
            flush=True,
        )

    print(
        f"FATAL: No report artifact after {MAX_ATTEMPTS} opencode attempts",
        file=sys.stderr,
    )
    sys.exit(1)


if __name__ == "__main__":
    main()
