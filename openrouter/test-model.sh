#!/bin/bash
# Test single OpenRouter model interactively
# Usage: ./test-model.sh <model-name>

MODEL=$1
TIMEOUT_SEC=30

if [ -z "$MODEL" ]; then
    echo "Usage: $0 <model-name>"
    echo "Example: $0 openrouter/meta-llama/llama-3.3-70b-instruct:free"
    echo ""
    echo "Or run without arguments for interactive mode"
    exit 1
fi

echo "========================================"
echo "Testing: $MODEL"
echo "Timeout: ${TIMEOUT_SEC}s"
echo "========================================"
echo ""

OUTPUT=$(timeout $TIMEOUT_SEC opencode run \
    --attach http://localhost:4096 \
    --thinking \
    --print-logs \
    "Say hello and exit." 2>&1)

EXIT_CODE=$?

echo ""
echo "========================================"
echo "Exit code: $EXIT_CODE"
echo "========================================"

if [ $EXIT_CODE -eq 124 ]; then
    echo "RESULT: ⚠️ TIMEOUT"
elif [ $EXIT_CODE -eq 0 ]; then
    if echo "$OUTPUT" | grep -qi "hello"; then
        echo "RESULT: ✅ WORKING"
    else
        echo "RESULT: ❌ ERROR (no response)"
    fi
else
    echo "RESULT: ❌ ERROR (exit $EXIT_CODE)"
fi

echo ""
echo "=== Output (last 100 lines) ==="
echo "$OUTPUT" | tail -100
