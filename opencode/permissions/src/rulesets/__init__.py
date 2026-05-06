"""rulesets — abstract named permission rule combinations.

Each module exports a single class with a ``layers()`` classmethod.
Add a new ruleset by creating a new file here.
"""
import importlib
import pkgutil
import os

_here = os.path.dirname(__file__)

RULESET_REGISTRY: dict[str, type] = {}
for _, _name, _ in pkgutil.iter_modules([_here]):
    _mod = importlib.import_module(f"src.rulesets.{_name}")
    for _attr in vars(_mod).values():
        if isinstance(_attr, type) and hasattr(_attr, "layers") and _attr.__module__ == _mod.__name__:
            RULESET_REGISTRY[_name] = _attr
            break
