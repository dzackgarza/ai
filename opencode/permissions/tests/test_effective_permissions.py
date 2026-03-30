from __future__ import annotations

import json
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


def test_write_global_policy_omits_top_level_allow_rules(tmp_path: Path) -> None:
    from main import write_global_policy_cmd

    config_path = tmp_path / "opencode.json"
    config_path.write_text('{"$schema":"https://example.test/schema","permission":{"question":"allow"}}\n')

    write_global_policy_cmd(config_path)

    payload = json.loads(config_path.read_text())
    permission = payload["permission"]

    assert "question" not in permission
    assert "webfetch" not in permission
    assert "bash" not in permission
    assert permission["external_directory"]["*"] == "ask"
    assert permission["external_directory"]["/tmp/*"] == "allow"


def test_unrestricted_test_agent_compiles_to_allow_every_known_tool() -> None:
    from agents.primary.unrestricted_test import AGENT
    from src.models import ALL_TOOLS

    compiled = AGENT.compile()

    for tool in ALL_TOOLS:
        if tool == "external_directory":
            assert compiled[tool] == {"*": "allow"}
            continue
        assert compiled[tool] == "allow"


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
