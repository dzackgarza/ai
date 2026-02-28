#!/usr/bin/env python3
"""Test usage_table with exact antigravity data."""

import json
import subprocess
from datetime import datetime, timezone

from usage_table import UsageTable, ModelRow

# Get actual antigravity data
result = subprocess.run(
    ["npx", "antigravity-usage", "quota", "--all-models", "--refresh", "--json"],
    capture_output=True, text=True, timeout=30
)
data = json.loads(result.stdout)

# Convert to ModelRows (same logic as antigravity_usage.py)
rows = []
for model in data.get("models", []):
    label = model.get("label", "")
    is_exhausted = model.get("isExhausted", False)
    remaining_pct = model.get("remainingPercentage")
    reset_time = model.get("resetTime")
    
    if is_exhausted:
        pct_used = 100
    elif remaining_pct is not None:
        pct_used = 100 - remaining_pct
    else:
        pct_used = 0
    
    # Calculate time string (same format as antigravity)
    if reset_time:
        reset_dt = datetime.fromisoformat(reset_time.replace("Z", "+00:00"))
        delta = reset_dt - datetime.now(timezone.utc)
        if delta.total_seconds() <= 0:
            time_str = "now"
        else:
            total_hrs = int(delta.total_seconds() / 3600)
            mins = int((delta.total_seconds() % 3600) / 60)
            time_str = f"in {total_hrs}h {mins}m"
    else:
        time_str = ""
    
    # Group by family
    if "claude" in label.lower():
        family = "Claude"
    elif "gemini" in label.lower():
        family = "Gemini"
    else:
        family = "Other"
    
    rows.append(ModelRow(
        family=family,
        model=label,
        pct_used=pct_used,
        reset_time=time_str,
        is_exhausted=is_exhausted,
    ))

# Render with usage_table
print("=== usage_table output ===")
table = UsageTable()
table.render(rows, title=data.get("email", "Usage"))
