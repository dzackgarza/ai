# /// script
# requires-python = ">=3.11"
# ///
"""
Brooks-Lint runner: assembles skills + template + diff, runs opencode.

The harness owns validation and finalization. The agent must save candidate JSON files to
$RUNNER_TEMP/brooks/candidates/. The harness validates them externally and atomically
writes the final .brooks-report-artifact.json.

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
import shutil

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
            if ref_dir.exists():
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
        if ref_path.exists():
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
    if base_ref:
        try:
            result = subprocess.run(
                ["git", "diff", f"origin/{base_ref}...HEAD"],
                capture_output=True,
                text=True,
                check=False
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except FileNotFoundError:
            pass
    try:
        result = subprocess.run(
            ["git", "diff", "HEAD~1...HEAD"],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except FileNotFoundError:
        pass
    return "No diff found."

def substitute(template: str, **kwargs: str) -> str:
    for k, v in kwargs.items():
        template = template.replace(f"{{{{{k}}}}}", v)
    return template

def validate_candidate(candidate_path: pathlib.Path) -> tuple[bool, str]:
    print(f"--- Validating candidate {candidate_path} ---", file=sys.stderr)
    result = subprocess.run(
        [sys.executable, str(CHECKER_PATH), str(candidate_path)],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        err_msg = result.stdout.strip() + "\n" + result.stderr.strip()
        print(f"--- Artifact validation FAILED ---", file=sys.stderr)
        for line in err_msg.splitlines():
            print(f"  checker: {line}", file=sys.stderr)
        return False, err_msg
    return True, ""

def run_opencode(task_path: pathlib.Path, candidates_dir: pathlib.Path, attempt: int) -> int:
    cmd = [
        "opencode",
        "run",
        "--model",
        "opencode/deepseek-v4-flash-free",
        "--file",
        str(task_path),
    ]
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=False,
        timeout=OPENCODE_TIMEOUT,
        env={**os.environ, "OPENCODE_PURE": "1"},
    )
    
    # Forward stdout/stderr for logs
    sys.stdout.write(result.stdout)
    sys.stderr.write(result.stderr)
    
    # Extract fenced JSON blocks from stdout
    import re
    blocks = re.findall(r"```json\n(.*?)\n```", result.stdout, re.DOTALL)
    for i, block in enumerate(blocks):
        cpath = candidates_dir / f"attempt-{attempt}-stdout-{i}.json"
        cpath.write_text(block.strip())
        
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

    runner_temp = os.environ.get("RUNNER_TEMP", "/tmp")
    brooks_dir = pathlib.Path(runner_temp) / "brooks"
    candidates_dir = brooks_dir / "candidates"
    candidates_dir.mkdir(parents=True, exist_ok=True)
    task_path = brooks_dir / "task.md"

    # Assemble the prompt
    system = load_skills(skills_dir, slop_mode=(args.mode == "slop"))
    diff = get_diff(args.base_ref)
    template = template_path.read_text()
    
    # We substitute into template
    body = substitute(template, DIFF=diff, PR_NUMBER=args.pr_number or "0", CANDIDATES_DIR=str(candidates_dir))
    current_prompt = f"{system}\n\n{body}"

    # Loop: run opencode until valid candidate appears or max attempts exhausted
    for attempt in range(1, MAX_ATTEMPTS + 1):
        if attempt > 1:
            time.sleep(5)

        task_path.write_text(current_prompt)

        print(f"--- opencode run attempt {attempt}/{MAX_ATTEMPTS} ---", file=sys.stderr)

        # Clear old candidates
        for c in candidates_dir.glob("*.json"):
            c.unlink()

        try:
            run_opencode(task_path, candidates_dir, attempt)
        except subprocess.TimeoutExpired:
            print(f"--- opencode timed out after {OPENCODE_TIMEOUT}s ---", file=sys.stderr)
        except FileNotFoundError:
            print("FATAL: opencode not found in PATH", file=sys.stderr)
            sys.exit(1)

        valid_candidate = None
        rejection_reasons = []

        # Find any JSON file in candidates_dir
        for cpath in candidates_dir.glob("*.json"):
            is_valid, err_msg = validate_candidate(cpath)
            if is_valid:
                valid_candidate = cpath
                break
            else:
                rejection_reasons.append((cpath.name, err_msg))
        
        if valid_candidate:
            print(f"--- Report artifact validated ---", file=sys.stderr)
            shutil.copy(str(valid_candidate), str(ARTIFACT_PATH))
            sys.exit(0)

        # Handle failure
        print("--- No valid candidate found. Agent did not submit a valid report ---", file=sys.stderr)
        if rejection_reasons:
            failures_text = "\n\n".join([f"Candidate {name} failed validation:\n{err}" for name, err in rejection_reasons])
            current_prompt += f"\n\n## Continuation Context (Attempt {attempt})\n\nYour prior candidate was rejected for:\n{failures_text}\n\nRepair only those defects. Reuse prior analysis where valid. Do not edit harness files. Do not delete candidate files. Write your fixed report to {candidates_dir}/attempt-{attempt+1}.json."
        else:
            current_prompt += f"\n\n## Continuation Context (Attempt {attempt})\n\nYou did not produce any candidate JSON files in {candidates_dir}. You must write your JSON output to a file in that directory."

    print(f"FATAL: No report artifact after {MAX_ATTEMPTS} opencode attempts", file=sys.stderr)
    sys.exit(1)

if __name__ == "__main__":
    main()