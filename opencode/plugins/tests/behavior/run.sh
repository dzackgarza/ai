#!/usr/bin/env bash
# Behavioral test runner for the prompt-router plugin.
#
# Usage:
#   ./run.sh <tier>                          # routing run (injection ON)
#   PROMPT_ROUTER_ENABLED=false ./run.sh <tier>  # baseline (classify-only)
#
# Tiers: model-self, knowledge, C, B, A, S
#
# PROMPT_ROUTER_ENABLED env var overrides killswitches.ts at runtime:
#   true  → force enable (inject instruction)
#   false → force kill  (classify and log, but do NOT inject)
#   unset → use value in killswitches.ts
#
# Output: results/<tier>/<timestamp>.yaml

set -euo pipefail

TIER="${1:-}"
if [[ -z "$TIER" ]]; then
  echo "Usage: $0 <tier>" >&2
  echo "Valid tiers: model-self, knowledge, C, B, A, S" >&2
  exit 1
fi

case "$TIER" in
  model-self)
    PROMPT="Describe every tool you have access to."
    TIMEOUT=30
    ;;
  knowledge)
    PROMPT="What is the latest stable release of Node.js, and does it support the Web Crypto API natively without any flags?"
    TIMEOUT=90
    ;;
  C)
    PROMPT="In \`lib/arguments/parser.js\` line 22, rename the parameter \`args\` to \`argumentList\` and update its one usage on the same line."
    TIMEOUT=60
    ;;
  B)
    PROMPT="Add a JSDoc comment to every exported function in \`lib/arguments/specific.js\`."
    TIMEOUT=180
    ;;
  A)
    PROMPT="The test \`should handle empty input\` in \`test/arguments/parser.test.js\` is failing. Figure out why and fix it."
    TIMEOUT=300
    ;;
  S)
    PROMPT="Design a plugin for tracking token usage per session."
    TIMEOUT=90
    ;;
  *)
    echo "Unknown tier: $TIER" >&2
    exit 1
    ;;
esac

TIMESTAMP=$(date -u +"%Y-%m-%dT%H-%M-%SZ")
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESULTS_DIR="$SCRIPT_DIR/results/$TIER"
mkdir -p "$RESULTS_DIR"
RESULT_FILE="$RESULTS_DIR/$TIMESTAMP.yaml"
TRANSCRIPT_FILE="/tmp/opencode-transcript-$TIMESTAMP.txt"

LOG_SNAPSHOT="/tmp/pr-log-before-$TIMESTAMP.txt"
[[ -f /var/sandbox/.prompt-router.log ]] && cp /var/sandbox/.prompt-router.log "$LOG_SNAPSHOT"

echo "=== Behavioral Test Run ==="
echo "Tier:    $TIER"
echo "Timeout: ${TIMEOUT}s"
echo "Prompt:  $PROMPT"
echo ""

cd /var/sandbox
timeout "$TIMEOUT" opencode run --print-logs "$PROMPT" 2>&1 | tee "$TRANSCRIPT_FILE" || true

# Extract new log entry written during this run
CLASSIFICATION_JSON=""
if [[ -f /var/sandbox/.prompt-router.log ]]; then
  if [[ -f "$LOG_SNAPSHOT" ]]; then
    CLASSIFICATION_JSON=$(diff "$LOG_SNAPSHOT" /var/sandbox/.prompt-router.log | grep '^>' | sed 's/^> //' | tail -1)
  else
    CLASSIFICATION_JSON=$(tail -1 /var/sandbox/.prompt-router.log)
  fi
fi

TIER_CLASSIFIED=$(echo "$CLASSIFICATION_JSON" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('tier','unknown'))" 2>/dev/null || echo "unknown")
REASONING=$(echo "$CLASSIFICATION_JSON" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('reasoning',''))" 2>/dev/null || echo "")

python3 - <<PYEOF
import yaml

result = {
    'tier_expected': '$TIER',
    'tier_classified': '$TIER_CLASSIFIED',
    'timestamp': '$TIMESTAMP',
    'prompt': """$PROMPT""",
    'reasoning': """$REASONING""",
    'transcript_file': '$TRANSCRIPT_FILE',
    'observed_behaviors': {
        'todo_write_created': None,
        'files_read_before_edit': None,
        'web_search_made': None,
        'subagents_spawned': None,
        'code_written': None,
        'root_cause_stated': None,
        'plan_mode_handoff': None,
        'total_tool_calls': None,
        'notes': '',
    },
}

with open('$RESULT_FILE', 'w') as f:
    yaml.dump(result, f, default_flow_style=False, allow_unicode=True)
print(f"Result: $RESULT_FILE")
PYEOF

echo ""
echo "Classification: tier_classified=$TIER_CLASSIFIED"
echo "Fill in observed_behaviors in: $RESULT_FILE"
