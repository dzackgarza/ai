#!/bin/bash
# Wrapper to send command output to Jules feedback
# Usage: ./jules-feedback.sh SESSION_ID "command to run"

SESSION_ID="$1"
shift
CMD="$*"

# Run the command and capture output
OUTPUT=$(eval "$CMD")

# Send to Jules
cd /home/dzack/opencode-plugins/improved-jules-cli
source .venv/bin/activate
source ~/.envrc
python -m improved_jules_cli feedback "$SESSION_ID" "$OUTPUT"
