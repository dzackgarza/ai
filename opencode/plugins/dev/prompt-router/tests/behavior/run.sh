#!/usr/bin/env bash
# Behavioral test runner for the prompt-router plugin.
#
# Usage:
#   ./run.sh <tier>                              # routing run (injection ON)
#   PROMPT_ROUTER_ENABLED=false ./run.sh <tier>  # baseline (classify-only)
#
# Tiers: model-self, knowledge, C, B, A, S
#
# PROMPT_ROUTER_ENABLED env var controls runtime behavior:
#   true  → force enable (inject instruction)
#   false → force disable (classify and log, but do NOT inject)
#   unset → default behavior
#
# Timeouts include 30s MCP warmup buffer. Use `opencode serve &` before
# batch runs to amortize warmup cost across sessions.
#
# Output:
#   results/<tier>/<timestamp>.yaml  — result + observed_behaviors scaffold

set -euo pipefail

TIER="${1:-}"
if [[ -z "$TIER" ]]; then
  echo "Usage: $0 <tier>" >&2
  echo "Valid tiers: model-self, knowledge, C, B, A, S" >&2
  exit 1
fi

# Timeouts include 30s MCP warmup buffer on top of expected model time
case "$TIER" in
  model-self)
    PROMPT="Describe every tool you have access to."
    TIMEOUT=90
    ;;
  knowledge)
    PROMPT="What is the latest stable release of Node.js, and does it support the Web Crypto API natively without any flags?"
    TIMEOUT=150
    ;;
  C)
    PROMPT="In \`lib/arguments/parser.js\` line 22, rename the parameter \`args\` to \`argumentList\` and update its one usage on the same line."
    TIMEOUT=120
    ;;
  B)
    PROMPT="Add a JSDoc comment to every exported function in \`lib/arguments/specific.js\`."
    TIMEOUT=240
    ;;
  A)
    PROMPT="The test \`should handle empty input\` in \`test/arguments/parser.test.js\` is failing. Figure out why and fix it."
    TIMEOUT=360
    ;;
  S)
    PROMPT="Design a plugin for tracking token usage per session."
    TIMEOUT=150
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

LOG_SNAPSHOT="/tmp/pr-log-before-$TIMESTAMP.txt"
[[ -f /var/sandbox/.prompt-router.log ]] && cp /var/sandbox/.prompt-router.log "$LOG_SNAPSHOT"

echo "=== Behavioral Test Run ==="
echo "Tier:      $TIER"
echo "Mode:      ${PROMPT_ROUTER_ENABLED:-'(default)'}"
echo "Timeout:   ${TIMEOUT}s"
echo "Prompt:    $PROMPT"
echo ""

cd /var/sandbox/execa

# Exit code 124 = timeout (ok — model may still have completed).
timeout "$TIMEOUT" opencode run "$PROMPT" 2>/dev/null || true

# Extract new log entry written during this run
CLASSIFICATION_JSON=""
if [[ -f /var/sandbox/.prompt-router.log ]]; then
  if [[ -f "$LOG_SNAPSHOT" ]]; then
    CLASSIFICATION_JSON=$(diff "$LOG_SNAPSHOT" /var/sandbox/.prompt-router.log | grep '^>' | sed 's/^> //' | tail -1 || true)
  else
    CLASSIFICATION_JSON=$(tail -1 /var/sandbox/.prompt-router.log)
  fi
fi

TIER_CLASSIFIED=$(echo "$CLASSIFICATION_JSON" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('tier','unknown'))" 2>/dev/null || echo "unknown")
REASONING=$(echo "$CLASSIFICATION_JSON" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('reasoning',''))" 2>/dev/null || echo "")

TIER="$TIER" \
TIER_CLASSIFIED="$TIER_CLASSIFIED" \
TIMESTAMP="$TIMESTAMP" \
PROMPT="$PROMPT" \
REASONING="$REASONING" \
RESULT_FILE="$RESULT_FILE" \
python3 - <<'PYEOF'
import yaml, os

result = {
    'tier_expected': os.environ['TIER'],
    'tier_classified': os.environ['TIER_CLASSIFIED'],
    'timestamp': os.environ['TIMESTAMP'],
    'prompt': os.environ['PROMPT'],
    'reasoning': os.environ['REASONING'],
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

result_file = os.environ['RESULT_FILE']
with open(result_file, 'w') as f:
    yaml.dump(result, f, default_flow_style=False, allow_unicode=True)
print(f"Result:    {result_file}")
PYEOF

echo ""
echo "Classification: tier_classified=$TIER_CLASSIFIED"
echo "Fill in observed_behaviors in: $RESULT_FILE"
