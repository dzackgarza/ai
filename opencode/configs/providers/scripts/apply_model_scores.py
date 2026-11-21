#!/usr/bin/env python3
"""Set each whitelisted model's display name to "[score] Model".

The score and model name come from the table in notes/model-scores.md. Each
provider id in a row's backticks names one whitelisted model. The script
fails if a whitelisted model has no row, or if a row names a provider id
that is not whitelisted, so the table and the fragments cannot drift.

Usage: python3 scripts/apply_model_scores.py   (from configs/providers)
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROW = re.compile(r"^\| (\d+) \| ([^|]+?) \| ([^|]+) \|")


def scored_names() -> dict[str, str]:
    names: dict[str, str] = {}
    for line in (ROOT / "notes" / "model-scores.md").read_text().splitlines():
        match = ROW.match(line)
        if not match:
            continue
        for provider_model in re.findall(r"`([^`]+)`", match.group(3)):
            names[provider_model] = f"[{match.group(1)}] {match.group(2)}"
    return names


def main() -> None:
    names = scored_names()
    for path in sorted(ROOT.glob("*.json")):
        cfg = json.loads(path.read_text())
        models = cfg.get("models") or {}
        whitelist = cfg.get("whitelist") or list(models)
        if not whitelist:
            continue
        for model_id in whitelist:
            key = f"{path.stem}/{model_id}"
            if key not in names:
                raise SystemExit(f"no score row for {key}")
            models.setdefault(model_id, {})["name"] = names.pop(key)
        cfg["models"] = models
        path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")
    if names:
        raise SystemExit(f"score rows name non-whitelisted ids: {sorted(names)}")


if __name__ == "__main__":
    main()
