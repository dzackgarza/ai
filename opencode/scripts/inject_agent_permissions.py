#!/usr/bin/env python3
"""Inject permissions into agent frontmatter based on agent mode.

Primary agents (mode: primary):
  - external_directory: {*: ask, <skeleton-defined paths>: allow}
    Novel paths prompt the user; known paths are silently allowed.
    Wildcard comes first so that specific allows (appended after) win via
    last-match-wins semantics in opencode's permission evaluator.

Subagents (mode: subagent):
  - task: deny  (subagents must not spawn further tasks)

Agents with a wildcard-deny permission block ('*': deny) are skipped — they
already cover everything and injecting into them would be redundant.

Run via: just build-config  (called as _build-opencode-inject-agent-ext-dirs)
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

BASE = Path(__file__).parent.parent  # opencode/
AGENTS_DIR = BASE / "agents"


def _parse_agent(path: Path) -> tuple[dict, str] | None:
    """Return (frontmatter_dict, body) or None if no frontmatter."""
    content = path.read_text()
    m = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not m:
        print(f"WARNING: no YAML frontmatter in {path.name}, skipping")
        return None
    fm = yaml.safe_load(m.group(1)) or {}
    return fm, content[m.end():]


def _write_agent(path: Path, fm: dict, body: str) -> None:
    dumped = yaml.dump(fm, default_flow_style=False, allow_unicode=True, sort_keys=False)
    path.write_text(f"---\n{dumped}---\n{body}")
    print(f"  → {path.name}")


def _has_wildcard_deny(fm: dict) -> bool:
    perm = fm.get("permission") or {}
    return perm.get("*") == "deny"


def inject_primary(path: Path, agent_ext_dir: dict[str, str]) -> None:
    parsed = _parse_agent(path)
    if parsed is None:
        return
    fm, body = parsed
    if _has_wildcard_deny(fm):
        return
    fm.setdefault("permission", {})["external_directory"] = agent_ext_dir
    _write_agent(path, fm, body)


def inject_subagent(path: Path) -> None:
    parsed = _parse_agent(path)
    if parsed is None:
        return
    fm, body = parsed
    if _has_wildcard_deny(fm):
        return
    fm.setdefault("permission", {})["task"] = "deny"
    _write_agent(path, fm, body)


def build_agent_ext_dir(skeleton_ext_dir: dict[str, str]) -> dict[str, str]:
    return {"*": "ask"} | {k: v for k, v in skeleton_ext_dir.items() if k != "*"}


def main() -> None:
    skeleton = json.loads((BASE / "configs" / "config_skeleton.json").read_text())
    agent_ext_dir = build_agent_ext_dir(skeleton["permission"]["external_directory"])

    for agent_path in sorted(AGENTS_DIR.glob("*.md")):
        parsed = _parse_agent(agent_path)
        if parsed is None:
            continue
        fm, _ = parsed
        mode = fm.get("mode")
        if mode == "primary":
            inject_primary(agent_path, agent_ext_dir)
        elif mode == "subagent":
            inject_subagent(agent_path)


if __name__ == "__main__":
    main()
