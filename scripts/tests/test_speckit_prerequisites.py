from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


CLI = Path(__file__).resolve().parents[1] / "speckit-prerequisites"


class SpecKitPrerequisitesTest(unittest.TestCase):
    def test_configured_hooks_on_cli_transitions(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            feature = root / "specs/001-example"
            feature.mkdir(parents=True)
            (root / ".specify").mkdir()
            templates = root / ".specify/templates"
            templates.mkdir()
            (templates / "tasks-template.md").write_text("# Tasks: [FEATURE NAME]\n")
            (root / ".specify/feature.json").write_text(
                json.dumps({"feature_directory": "specs/001-example"})
            )
            (root / ".specify/extensions.yml").write_text(
                """hooks:
  before_plan:
    - extension: frontier-simplify
      command: frontier-simplify
      optional: false
  after_tasks:
    - extension: frontier-simplify
      command: frontier-simplify
      optional: false
  before_implement:
    - extension: frontier-simplify
      command: speckit.delivery-review
      optional: false
  before_converge:
    - extension: frontier-simplify
      command: speckit.delivery-review
      optional: false
"""
            )
            for name in ("spec.md", "plan.md", "tasks.md"):
                (feature / name).write_text("# Example\n")

            def invoke(*args: str) -> subprocess.CompletedProcess[str]:
                return subprocess.run(
                    [str(CLI), "--json", *args],
                    cwd=root,
                    capture_output=True,
                    text=True,
                )

            legacy = invoke("--require-tasks")
            self.assertEqual(legacy.returncode, 0, legacy.stderr)
            self.assertEqual(json.loads(legacy.stdout)["FEATURE_DIR"], str(feature))
            self.assertIn("EXECUTE_COMMAND: speckit.delivery-review", legacy.stderr)
            for step, event, command in (
                ("plan", "before_plan", "frontier-simplify"),
                ("tasks", "after_tasks", "frontier-simplify"),
                ("implement", "before_implement", "speckit.delivery-review"),
                ("converge", "before_converge", "speckit.delivery-review"),
            ):
                result = invoke("--step", step)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(result.stdout)["FEATURE_DIR"], str(feature))
                self.assertIn(event, result.stderr)
                self.assertIn(f"EXECUTE_COMMAND: {command}", result.stderr)
            (feature / "tasks.md").unlink()
            rejected = invoke("--step", "implement")
            self.assertNotEqual(rejected.returncode, 0)
            self.assertIn("tasks.md not found", rejected.stderr)
