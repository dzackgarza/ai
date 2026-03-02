#!/usr/bin/env python3
import json
import os

base_dir = os.path.expanduser("~/.config/opencode")


def list_permissions():
    """Scan all agents and collect permission settings."""
    permissions_by_agent = {}

    # Check agents
    agents_dir = os.path.join(base_dir, "configs", "agents")
    for filename in os.listdir(agents_dir):
        if filename.endswith(".json"):
            agent_name = filename[:-5]
            with open(os.path.join(agents_dir, filename), "r") as f:
                data = json.load(f)
                if "permission" in data:
                    permissions_by_agent[agent_name] = data["permission"]

    # Check subagents
    subagents_dir = os.path.join(base_dir, "configs", "subagents")
    for filename in os.listdir(subagents_dir):
        if filename.endswith(".json"):
            agent_name = filename[:-5]
            with open(os.path.join(subagents_dir, filename), "r") as f:
                data = json.load(f)
                if "permission" in data:
                    permissions_by_agent[agent_name] = data["permission"]

    print("Agent Permissions Overview:")
    for agent, perms in permissions_by_agent.items():
        print(f"\n{agent}:")
        print(json.dumps(perms, indent=2))


if __name__ == "__main__":
    list_permissions()
