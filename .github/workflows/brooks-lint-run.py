# /// script
# requires-python = ">=3.11"
# ///
"""
Brooks-Lint runner: assembles skills + template + diff, runs opencode.

Usage:
  python3 brooks-lint-run.py [--mode review] [--skills-dir SKILLS] [--base-ref REF]
"""

import argparse
import json
import os
import pathlib
import subprocess
import sys

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


def collect_repo_docs(repo_root: pathlib.Path) -> str:
    """Find all README.md and AGENTS.md files. Inject as context so the model
    cannot skip reading project documentation before making findings."""
    sections = []
    for pattern in ("*README.md", "*AGENTS.md", "*AGENTS*.md"):
        for p in repo_root.rglob(pattern):
            rel = p.relative_to(repo_root)
            if any(part in IGNORE_DIRS for part in p.parts):
                continue
            if p.stat().st_size > 500_000:
                continue  # skip huge files
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

    # Load CI exploration protocol from the project's own repo (not the brooks-lint checkout).
    # This is project-owned code, not an external skill guide.
    ci_protocol = pathlib.Path("opencode/skills/_shared/ci-sweep-protocol.md").resolve()
    guides.append(ci_protocol.read_text())  # no guard — fail loudly if missing

    # Force-inject skill SKILL.md files. The template previously asked the agent to
    # load these via skill() — but agents routinely skip or fail at that. Loading them
    # here guarantees the content is in context regardless of agent compliance.
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
        guides.append(path.read_text())  # no guard — fail loudly if missing

    # In slop mode, load ALL reference files from reviewing-llm-code and anti-slop.
    # The main SKILL.md files are already loaded above; the references add detection
    # pattern depth across bridge-burning violations, runtime control-flow, case
    # studies, code patterns, test patterns, text patterns, UX antipatterns, etc.
    if slop_mode:
        for ref_dir in [
            skills_repo / "reviewing-llm-code" / "references",
            skills_repo / "anti-slop" / "references",
        ]:
            for ref_file in sorted(ref_dir.iterdir()):
                if ref_file.suffix == ".md":
                    guides.append(ref_file.read_text())
    else:
        # Non-slop mode: only load the core bridge-burning red-flag reference.
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

    # Inject project documentation (README.md, AGENTS.md) as part of system context.
    # Not a separate prompt layer — the template is the single source of instructions.
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


def substitute_diff(template: str, diff: str) -> str:
    """Replace {{DIFF}} in template. Empty diff -> no-diff message."""
    placeholder = "{{DIFF}}"
    if placeholder not in template:
        return template
    if not diff.strip():
        return template.replace(
            placeholder, "*No diff \u2014 full codebase scan only.*"
        )
    return template.replace(placeholder, diff)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run brooks-lint review via opencode")
    parser.add_argument(
        "--mode", default="review", help="Review mode (review, audit, etc.)"
    )
    parser.add_argument(
        "--skills-dir",
        default=".brooks-lint/skills",
        help="Path to brooks-lint skills directory",
    )
    parser.add_argument(
        "--base-ref", default=None, help="Git base ref for diff (e.g., main)"
    )
    parser.add_argument(
        "--template",
        default=".github/workflows/brooks-review-template.md",
        help="Path to prompt template",
    )
    args = parser.parse_args()

    skills_dir = pathlib.Path(args.skills_dir)
    template_path = pathlib.Path(args.template)

    if not skills_dir.is_dir():
        print(
            json.dumps(
                {
                    "error": f"Skills directory not found: {skills_dir}",
                    "mode": args.mode,
                }
            )
        )
        sys.exit(1)
    if not template_path.is_file():
        print(
            json.dumps(
                {"error": f"Template not found: {template_path}", "mode": args.mode}
            )
        )
        sys.exit(1)

    # Assemble the prompt: system (skills + project docs) + body (template + diff).
    # The template is the single source of prompt instructions — no injected layers.
    system = load_skills(skills_dir, slop_mode=(args.mode == "slop"))
    diff = get_diff(args.base_ref)
    template = template_path.read_text()
    body = substitute_diff(template, diff)
    prompt = f"{system}\n\n{body}"

    # Run opencode
    try:
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
            capture_output=True,
            text=True,
            check=False,
            timeout=300,
            env={**os.environ, "OPENCODE_PURE": "1"},
        )
        output = result.stdout.strip()
        score_str = None
        import re

        m = re.search(r"Health\s+Score[:\s]+(\d+)", output, re.IGNORECASE)
        if m:
            score_str = m.group(1)
        score = int(score_str) if score_str else None
        print(json.dumps({"report": output, "score": score, "mode": args.mode}))
    except subprocess.TimeoutExpired:
        print(json.dumps({"error": "opencode run timed out", "mode": args.mode}))
        sys.exit(1)
    except FileNotFoundError:
        print(json.dumps({"error": "opencode not found in PATH", "mode": args.mode}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e), "mode": args.mode}))
        sys.exit(1)


if __name__ == "__main__":
    main()
