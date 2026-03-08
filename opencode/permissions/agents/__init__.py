from __future__ import annotations

"""Canonical registry of all managed agents."""

import importlib
import os
import pkgutil
import sys

_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, _root)

from src.base import Agent

AGENTS: list[Agent] = []

_here = os.path.dirname(__file__)
for _info in pkgutil.iter_modules([os.path.join(_here, "primary")]):
    _mod = importlib.import_module(f"agents.primary.{_info.name}")
    if hasattr(_mod, "AGENT"):
        AGENTS.append(_mod.AGENT)

for _info in pkgutil.walk_packages(
    [os.path.join(_here, "subagents")],
    prefix="agents.subagents.",
):
    _mod = importlib.import_module(_info.name)
    if hasattr(_mod, "AGENT"):
        AGENTS.append(_mod.AGENT)
