#!/usr/bin/env python3
"""Inject external_directory whitelist from config_skeleton.json into primary agent frontmatter.

Primary agents need external_directory: {*: ask, <known paths>: allow} so that:
  - Novel paths prompt the user (ask)
  - All skeleton-defined paths are silently allowed (last-match wins, specifics come after wildcard)

Subagents inherit the skeleton's default-deny and are not touched here.

Run via: just build-config  (called as _build-opencode-inject-agent-ext-dirs)
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

BASE = Path(__file__).parent.parent  # opencode/

PRIMARY_AGENTS = ["interactive.md", "general-primary.md", "build.md", "plan.md"]


def build_agent_ext_dir(skeleton_ext_dir: dict[str, str]) -> dict[str, str]:
    """Return external_directory block for primary agents.

    Wildcard comes first so that specific paths (appended after) win via
    last-match-wins semantics in opencode's permission evaluator.
    """
    return {"*": "ask"} | {k: v for k, v in skeleton_ext_dir.items() if k != "*"}


def inject(path: Path, agent_ext_dir: dict[str, str]) -> None:
    content = path.read_text()
    m = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not m:
        print(f"WARNING: no YAML frontmatter found in {path.name}, skipping")
        return
    fm: dict = yaml.safe_load(m.group(1)) or {}
    body = content[m.end():]
    fm.setdefault("permission", {})["external_directory"] = agent_ext_dir
    dumped = yaml.dump(fm, default_flow_style=False, allow_unicode=True, sort_keys=False)
    path.write_text(f"---\n{dumped}---\n{body}")
    print(f"  → {path.name}")


def main() -> None:
    skeleton = json.loads((BASE / "configs" / "config_skeleton.json").read_text())
    agent_ext_dir = build_agent_ext_dir(skeleton["permission"]["external_directory"])
    for name in PRIMARY_AGENTS:
        inject(BASE / "agents" / name, agent_ext_dir)


if __name__ == "__main__":
    main()
