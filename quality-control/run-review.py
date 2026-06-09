# /// script
# requires-python = ">=3.11"
# ///
"""
Review runner: manages the agent loop, harvesting, and finalization.

The agent writes a candidate report to a fixed path, then calls
quality-control/ci/submit-candidate (no arguments) to validate and submit.
The script copies the validated report to .review-report-artifact.json
on success. The harness only checks for existence of that artifact after
the opencode session ends — the script owns validation and submission.
On timeout or missing artifact, the harness re-prompts and loops.
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

HERE = pathlib.Path(__file__).parent.resolve()

ARTIFACT_PATH = pathlib.Path(".review-report-artifact.json")
COMMENT_PATH = pathlib.Path(".review-report-comment.md")
SCORE_PATH = pathlib.Path(".review-report-score.txt")
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


def load_skills(skills_dir: pathlib.Path, slop_mode: bool = False) -> str:
    skills_repo = pathlib.Path("opencode/skills").resolve()
    guides = []
    for fname in ["common.md", "source-coverage.md", "decay-risks.md"]:
        p = skills_dir / "_shared" / fname
        if p.exists():
            guides.append(p.read_text())

    ci_protocol = pathlib.Path("opencode/skills/_shared/ci-sweep-protocol.md").resolve()
    if ci_protocol.exists():
        guides.append(ci_protocol.read_text())

    for skill_name in [
        "policy-index",
        "bespoke-software-policy",
        "test-guidelines",
        "tool-provisioning-and-environment-hygiene",
    ]:
        p = skills_repo / skill_name / "SKILL.md"
        if p.exists():
            guides.append(p.read_text())

    if slop_mode:
        for skill_name in ["anti-slop", "reviewing-llm-code", "fixing-slop"]:
            p = skills_repo / skill_name / "SKILL.md"
            if p.exists():
                guides.append(p.read_text())
        for ref_dir in [
            skills_repo / "reviewing-llm-code" / "references",
            skills_repo / "anti-slop" / "references",
        ]:
            if ref_dir.exists():
                for f in sorted(ref_dir.iterdir()):
                    if f.suffix == ".md":
                        guides.append(f.read_text())

    p = skills_dir / "brooks-review" / "pr-review-guide.md"
    if p.exists():
        guides.append(p.read_text())

    repo_docs = collect_repo_docs(pathlib.Path.cwd())
    if repo_docs:
        guides.append(repo_docs)
    return "\n\n---\n\n".join(guides)


def substitute(template: str, **kwargs: str) -> str:
    for k, v in kwargs.items():
        template = template.replace(f"{{{{{k}}}}}", v)
    return template


SUBMITTED_CANDIDATE = "submitted.json"


def run_opencode(task_path: pathlib.Path) -> int:
    cmd = ["opencode", "run", "--model", "opencode/deepseek-v4-flash-free"]

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
    parser.add_argument("--mode", default="review")
    parser.add_argument("--skills-dir", default="opencode/skills")
    parser.add_argument("--base-ref")
    parser.add_argument(
        "--template",
        default=str(HERE / "reviews" / "general" / "template.md"),
    )
    parser.add_argument("--pr-number", default="0")
    parser.add_argument(
        "--reviewer-context",
        default=None,
        help="Path to reviewer context file (existing issues on this PR)",
    )
    args = parser.parse_args()

    skills_dir, template_path = (
        pathlib.Path(args.skills_dir),
        pathlib.Path(args.template),
    )
    if not skills_dir.is_dir() or not template_path.is_file():
        print("FATAL: Missing dependencies", file=sys.stderr)
        sys.exit(1)

    run_dir = pathlib.Path(".agents/review-runner").resolve()
    candidates_dir = run_dir / "candidates"
    candidates_dir.mkdir(parents=True, exist_ok=True)
    task_path = run_dir / "task.md"

    repo_sha = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()

    system = load_skills(skills_dir, slop_mode=(args.mode == "slop"))
    template = template_path.read_text()
    # Remove PR_NUMBER from the body entirely to de-anchor the agent
    body = substitute(template, REPO_SHA=repo_sha)

    # Prepend instruction to scan full repo (not just PR diff), but DO consider existing threads
    header = """
# INSTRUCTIONS: Repository-wide sweep, not PR-diff review

You are performing a FRESH, COMPREHENSIVE REPOSITORY AUDIT.
Scan the ENTIRE repository source tree — do NOT limit analysis to recent commits or diffs.
Analyze all files as if this were a day-zero audit of a new codebase.

HOWEVER: The context above lists existing review issues on this PR (from the thread index).
Do NOT re-raise these issues unless you have new evidence, the problem reappears in a
materially different form, or the previous resolution is directly contradicted by the
current code. The index is maintained by a separate gardener agent — respect it.
"""
    current_prompt = f"{header}\n\n{system}\n\n{body}"

    # Prepend reviewer context if provided (existing issues on this PR)
    if args.reviewer_context:
        ctx_path = pathlib.Path(args.reviewer_context)
        if not ctx_path.is_file():
            print(
                f"FATAL: --reviewer-context file not found: {ctx_path}", file=sys.stderr
            )
            sys.exit(1)
        ctx = ctx_path.read_text()
        current_prompt = f"{ctx}\n\n{current_prompt}"

    submitted_path = candidates_dir / SUBMITTED_CANDIDATE

    for attempt in range(1, MAX_ATTEMPTS + 1):
        if attempt > 1:
            time.sleep(5)
        task_path.write_text(current_prompt)
        print(f"--- opencode run attempt {attempt}/{MAX_ATTEMPTS} ---", file=sys.stderr)
        # Clear any prior files to prevent stale submissions
        submitted_path.unlink(missing_ok=True)
        ARTIFACT_PATH.unlink(missing_ok=True)
        try:
            run_opencode(task_path)
        except subprocess.TimeoutExpired:
            print("--- opencode timed out ---", file=sys.stderr)
        except FileNotFoundError:
            print(
                "FATAL: 'opencode' executable not found in PATH. "
                "This is a non-transient failure — exiting immediately.",
                file=sys.stderr,
            )
            sys.exit(1)
        except Exception as e:
            print(f"--- opencode error: {e} ---", file=sys.stderr)

        if ARTIFACT_PATH.exists():
            print("--- Report artifact submitted ---", file=sys.stderr)
            try:
                comment = COMMENT_PATH.read_text()
                # Extract score from rendered comment (machine-parseable anchor)
                import re

                m = re.search(r"\*\*Score: (\d+)/100\*\*", comment)
                score = m.group(1) if m else "0"
                SCORE_PATH.write_text(score)
            except Exception as e:
                print(f"Warning: Failed to read rendered comment: {e}", file=sys.stderr)
            sys.exit(0)

        current_prompt += (
            f"\n\n## Continuation Context (Attempt {attempt})\n\n"
            f"Your session ended without a valid report at {ARTIFACT_PATH}.\n"
            f"Run quality-control/ci/submit-candidate (no arguments) after writing your "
            f"report to {submitted_path}."
        )

    print(f"FATAL: No report artifact after {MAX_ATTEMPTS} attempts", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
