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


def load_skills(skills_dir: pathlib.Path) -> str:
    """Load and concatenate all shared and mode-specific skill guides."""
    _shared = skills_dir / "_shared"
    guides = []

    for fname in ["common.md", "source-coverage.md", "decay-risks.md"]:
        path = _shared / fname
        if path.exists():
            guides.append(path.read_text())

    for guide_dir, fname in [
        ("brooks-review", "pr-review-guide.md"),
        ("brooks-sweep", "sweep-guide.md"),
    ]:
        path = skills_dir / guide_dir / fname
        if path.exists():
            guides.append(path.read_text())

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

    # Assemble the prompt
    system = load_skills(skills_dir)
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
