#!/bin/bash
# Test script for OpenRouter free models
# Usage: ./test-openrouter-model.sh <model-name>

MODEL=$1

if [ -z "$MODEL" ]; then
    echo "Usage: $0 <model-name>"
    echo "Example: $0 openrouter/meta-llama/llama-3.3-70b-instruct:free"
    exit 1
fi

echo "========================================"
echo "Testing: $MODEL"
echo "========================================"
echo ""

# Run with 30s timeout, thinking, print-logs, attach to background server
# Using --agent=minimal to avoid any agent-specific prompts
timeout 30s opencode run \
    --attach http://localhost:4096 \
    --agent=minimal \
    --thinking \
    --print-logs \
    "Say hello and exit. Do not perform any other actions." 2>&1

EXIT_CODE=$?
echo ""
echo "========================================"
echo "Exit code: $EXIT_CODE"
echo "========================================"

if [ $EXIT_CODE -eq 124 ]; then
    echo "RESULT: TIMEOUT (30s exceeded)"
elif [ $EXIT_CODE -eq 0 ]; then
    echo "RESULT: SUCCESS"
else
    echo "RESULT: ERROR (exit code $EXIT_CODE)"
fi

exit $EXIT_CODE
