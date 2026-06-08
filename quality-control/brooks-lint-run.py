# /// script
# requires-python = ">=3.11"
# ///
"""
Brooks-Lint runner: manages the agent loop, harvesting, and validation.

The agent acts as a candidate generator. The harness finalizes the artifact.
"""

import argparse
import os
import pathlib
import subprocess
import sys
import time
import shutil
import re
import json

IGNORE_DIRS = {
    ".git", "node_modules", ".venv", "__pycache__", "dist", "build", ".next", "coverage"
}

ARTIFACT_PATH = pathlib.Path(".brooks-report-artifact.json")
MARKDOWN_PATH = pathlib.Path(".brooks-report-artifact.md")
SCORE_PATH = pathlib.Path(".brooks-report-score.txt")
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
            if not p.is_file() or p.stat().st_size > 500_000:
                continue
            sections.append(f"### Repo doc: {rel}\n\n{p.read_text()}")
    return "## Repo Documentation\n\n" + "\n\n---\n\n".join(sections) if sections else ""

def load_skills(skills_dir: pathlib.Path, slop_mode: bool = False) -> str:
    skills_repo = pathlib.Path("opencode/skills").resolve()
    guides = []
    for fname in ["common.md", "source-coverage.md", "decay-risks.md"]:
        p = skills_dir / "_shared" / fname
        if p.exists(): guides.append(p.read_text())

    ci_protocol = pathlib.Path("opencode/skills/_shared/ci-sweep-protocol.md").resolve()
    if ci_protocol.exists(): guides.append(ci_protocol.read_text())

    for skill_name in ["policy-index", "bespoke-software-policy", "anti-slop", "reviewing-llm-code", "fixing-slop", "test-guidelines", "tool-provisioning-and-environment-hygiene"]:
        p = skills_repo / skill_name / "SKILL.md"
        if p.exists(): guides.append(p.read_text())

    ref_file = "bridge-burning-red-flags.md"
    if slop_mode:
        for ref_dir in [skills_repo / "reviewing-llm-code" / "references", skills_repo / "anti-slop" / "references"]:
            if ref_dir.exists():
                for f in sorted(ref_dir.iterdir()):
                    if f.suffix == ".md": guides.append(f.read_text())
    else:
        p = skills_repo / "reviewing-llm-code" / "references" / ref_file
        if p.exists(): guides.append(p.read_text())

    p = skills_dir / "brooks-review" / "pr-review-guide.md"
    if p.exists(): guides.append(p.read_text())

    repo_docs = collect_repo_docs(pathlib.Path.cwd())
    if repo_docs: guides.append(repo_docs)
    return "\n\n---\n\n".join(guides)

def substitute(template: str, **kwargs: str) -> str:
    for k, v in kwargs.items(): template = template.replace(f"{{{{{k}}}}}", v)
    return template

def validate_candidate(candidate_path: pathlib.Path, repo_sha: str) -> tuple[bool, str]:
    print(f"--- Validating candidate {candidate_path} ---", file=sys.stderr)
    result = subprocess.run([sys.executable, str(CHECKER_PATH), str(candidate_path)], capture_output=True, text=True, check=False)
    if result.returncode != 0:
        msg = result.stdout.strip() + "\n" + result.stderr.strip()
        print(f"--- Artifact validation FAILED ---\n{msg}", file=sys.stderr)
        return False, msg
    return True, ""

def run_opencode(task_path: pathlib.Path, candidates_dir: pathlib.Path, attempt: int) -> int:
    cmd = ["opencode", "run", "--model", "opencode/deepseek-v4-flash-free"]
    env = {**os.environ, "OPENCODE_PURE": "1", "RUNNER_TEMP": str(task_path.parent.parent)}
    with open(task_path, 'r') as f:
        res = subprocess.run(
            cmd,
            stdin=f,
            capture_output=True,
            text=True,
            check=False,
            timeout=OPENCODE_TIMEOUT,
            env=env,
        )
    
    # Forward stdout/stderr for logs
    sys.stdout.write(res.stdout)
    sys.stderr.write(res.stderr)
    
    # Extract fenced JSON blocks from stdout
    import re
    blocks = re.findall(r"```json\n(.*?)\n```", res.stdout, re.DOTALL)
    for i, block in enumerate(blocks):
        cpath = candidates_dir / f"attempt-{attempt}-stdout-{i}.json"
        cpath.write_text(block.strip())
        
    return res.returncode

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="review")
    parser.add_argument("--skills-dir", default="opencode/skills")
    parser.add_argument("--base-ref")
    parser.add_argument("--template", default=".github/workflows/brooks-review-template.md")
    parser.add_argument("--pr-number", default="0")
    args = parser.parse_args()

    skills_dir, template_path = pathlib.Path(args.skills_dir), pathlib.Path(args.template)
    if not skills_dir.is_dir() or not template_path.is_file():
        print("FATAL: Missing dependencies", file=sys.stderr); sys.exit(1)

    brooks_dir = pathlib.Path(".agents/brooks").resolve()
    candidates_dir = brooks_dir / "candidates"
    candidates_dir.mkdir(parents=True, exist_ok=True)
    task_path = brooks_dir / "task.md"

    # Get current SHA
    try: repo_sha = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except: repo_sha = "HEAD"

    system = load_skills(skills_dir, slop_mode=(args.mode == "slop"))
    template = template_path.read_text()
    # Remove PR_NUMBER from the body entirely to de-anchor the agent
    body = substitute(template, CANDIDATES_DIR=str(candidates_dir), REPO_SHA=repo_sha)
    
    # Prepend strict instruction to IGNORE PR context
    header = """
# IMPORTANT: IGNORE ALL PULL REQUEST CONTEXT

You are NOT performing a PR review. You are performing a FRESH, COMPREHENSIVE REPOSITORY AUDIT.
Do NOT look at recent commits or diffs to guide your analysis.
Scan the ENTIRE repository source tree.
Analyze all files as if this were a day-zero audit of a new codebase.
"""
    current_prompt = f"{header}\n\n{system}\n\n{body}"

    for attempt in range(1, MAX_ATTEMPTS + 1):
        if attempt > 1: time.sleep(5)
        task_path.write_text(current_prompt)
        print(f"--- opencode run attempt {attempt}/{MAX_ATTEMPTS} ---", file=sys.stderr)
        for c in candidates_dir.glob("*.json"): c.unlink()
        try: run_opencode(task_path, candidates_dir, attempt)
        except subprocess.TimeoutExpired: print("--- opencode timed out ---", file=sys.stderr)
        except Exception as e: print(f"--- opencode error: {e} ---", file=sys.stderr)

        valid_candidate, rejection_reasons = None, []
        for cpath in candidates_dir.glob("*.json"):
            is_valid, err = validate_candidate(cpath, repo_sha)
            if is_valid: valid_candidate = cpath; break
            rejection_reasons.append((cpath.name, err))

        if valid_candidate:
            print("--- Report artifact validated ---", file=sys.stderr)
            shutil.copy(str(valid_candidate), str(ARTIFACT_PATH))
            
            # Extract markdown and score for CI
            try:
                with open(valid_candidate, 'r') as f:
                    data = json.load(f)
                MARKDOWN_PATH.write_text(str(data.get("report", "No report provided.")))
                SCORE_PATH.write_text(str(data.get("score", "0")))
            except Exception as e:
                print(f"Warning: Failed to extract markdown/score: {e}", file=sys.stderr)

            sys.exit(0)

        if rejection_reasons:
            rejections = "\n\n".join([f"Candidate {n} failed:\n{e}" for n, e in rejection_reasons])
            current_prompt += f"\n\n## Continuation Context (Attempt {attempt})\n\nYour prior candidate was rejected for:\n{rejections}\n\nRepair only those defects. Reuse prior analysis where valid. Write fixed JSON to {candidates_dir}/attempt-{attempt+1}.json."
        else:
            current_prompt += f"\n\n## Continuation Context (Attempt {attempt})\n\nYou did not produce any candidate JSON files in {candidates_dir} or in stdout fenced blocks."

    print(f"FATAL: No report artifact after {MAX_ATTEMPTS} attempts", file=sys.stderr)
    sys.exit(1)

if __name__ == "__main__": main()
