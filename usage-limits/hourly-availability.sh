#!/usr/bin/env bash
# Hourly availability check - posts to ntfy

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NTFY_TOPIC="${NTFY_TOPIC:-usage-updates}"
NTFY_SERVER="${NTFY_SERVER:-http://localhost}"

cd "$SCRIPT_DIR"

# Source envrc for OLLAMA_SESSION_COOKIE
set -a && . ~/.envrc && set +a

# Helper function to format availability with time
format_availability() {
    local json="$1"
    local name=$(echo "$json" | jq -r '.name')
    local available=$(echo "$json" | jq -r '.available_now')
    local when=$(echo "$json" | jq -r '.available_when // "now"')
    
    if [ "$available" = "true" ]; then
        echo "✓ $name"
    else
        # Convert ISO datetime to relative time
        if [ "$when" != "null" ] && [ "$when" != "now" ]; then
            local when_human=$(date -d "$when" "+%a %H:%M" 2>/dev/null || echo "$when")
            echo "✗ $name (until $when_human)"
        else
            echo "✗ $name"
        fi
    fi
}

# Build message
MESSAGE="Availability Check - $(date '+%Y-%m-%d %H:%M')"$'\n'$'\n'

MESSAGE+="Claude: "
CLAUDE_JSON=$(python claude_usage.py -a | jq '.[0]')
MESSAGE+="$(format_availability "$CLAUDE_JSON")"
MESSAGE+=$'\n'

MESSAGE+="Codex: "
CODEX_JSON=$(python codex_usage.py -a | jq '.[0]')
MESSAGE+="$(format_availability "$CODEX_JSON")"
MESSAGE+=$'\n'

MESSAGE+="Ollama: "
OLLAMA_JSON=$(python ollama_usage.py -a | jq '.[0]')
MESSAGE+="$(format_availability "$OLLAMA_JSON")"
MESSAGE+=$'\n'

MESSAGE+="Antigravity:"$'\n'
while IFS= read -r item; do
    MESSAGE+="  $(format_availability "$item")"$'\n'
done < <(python antigravity_usage.py -a | jq -c '.[]')

# Post to ntfy
curl -s -X POST "$NTFY_SERVER/$NTFY_TOPIC" \
    -H "Title: Hourly Availability Check" \
    -H "Priority: 3" \
    -H "Tags: white_check_mark,clock" \
    -d "$MESSAGE" > /dev/null

echo "Posted availability update to ntfy"
