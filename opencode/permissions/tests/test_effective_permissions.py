from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def test_main_show_effective_runs_for_minimal_agent() -> None:
    result = subprocess.run(
        [sys.executable, "main.py", "--show-effective", "Minimal"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr or result.stdout
    assert "Effective permissions" in result.stdout
    assert "Minimal" in result.stdout


@pytest.mark.parametrize(
    ("value", "pattern", "expected"),
    [
        ("ls", "ls *", True),
        ("ls -la", "ls *", True),
        ("lstmeval", "ls *", False),
        ("file1.txt", "file?.txt", True),
        ("file12.txt", "file?.txt", False),
        ("foo+bar", "foo+bar", True),
        ("C:\\Windows\\System32\\drivers", "C:/Windows/System32/*", True),
    ],
)
def test_wildcard_match_tracks_upstream_opencode_cases(
    value: str,
    pattern: str,
    expected: bool,
) -> None:
    from src.display import wildcard_match

    assert wildcard_match(value, pattern) is expected
