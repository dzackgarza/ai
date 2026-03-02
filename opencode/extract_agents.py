#!/usr/bin/env python3
import json
import os

base_dir = os.path.expanduser("~/.config/opencode")
input_file = os.path.join(base_dir, "opencode.json")

with open(input_file, "r") as f:
    config = json.load(f)

agents = config.get("agent", {})

for name, data in agents.items():
    if data.get("mode") == "subagent":
        out_dir = os.path.join(base_dir, "configs", "subagents")
    else:
        out_dir = os.path.join(base_dir, "configs", "agents")

    out_file = os.path.join(out_dir, f"{name}.json")
    with open(out_file, "w") as f:
        json.dump(data, f, indent=2)

print("Extraction complete.")
