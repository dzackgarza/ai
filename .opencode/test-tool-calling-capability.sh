#!/bin/bash
# Tool calling capability test for OpenCode models
# Tests if models can actually use curl to fetch dynamic content

set -e

# Test prompt - fetches UUID that changes every request
PROMPT="Fetch the current UUID from https://httpbin.org/uuid and repeat it back exactly. The UUID changes on every request, so you must actually curl the URL. Format your response as: UUID: <the-uuid>"

# Expected UUID (fetch before running model)
EXPECTED_UUID=$(curl -s https://httpbin.org/uuid | grep -o '[0-9a-f-]\{36\}')

echo "=== Tool Calling Capability Test ==="
echo "Expected UUID: $EXPECTED_UUID"
echo ""

# Models to test
MODELS=(
    # Top tier OpenRouter
    "openrouter/stepfun/step-3.5-flash:free"
    "openrouter/deepseek/deepseek-r1:free"
    "openrouter/meta-llama/llama-3.1-405b-instruct:free"
    # Mid tier OpenRouter
    "openrouter/qwen/qwen3-32b:free"
    "openrouter/mistralai/mistral-small-3.2-24b-instruct:free"
    # Lightweight OpenRouter
    "openrouter/qwen/qwen3-8b:free"
    # Recommended free
    "opencode/big-pickle"
    "opencode/glm-5-free"
    "openai/codex-mini-latest"
    "google/antigravity-claude-sonnet-4-6"
    "ollama/minimax-m2.5:cloud"
)

# Results file
RESULTS_FILE="tool_calling_test_results_$(date +%Y%m%d_%H%M%S).md"

echo "# Tool Calling Test Results" > "$RESULTS_FILE"
echo "**Date:** $(date)" >> "$RESULTS_FILE"
echo "**Test:** Fetch UUID from httpbin.org and repeat back" >> "$RESULTS_FILE"
echo "**Expected UUID:** \`$EXPECTED_UUID\`" >> "$RESULTS_FILE"
echo "" >> "$RESULTS_FILE"
echo "| Model | Result | Notes |" >> "$RESULTS_FILE"
echo "|-------|--------|-------|" >> "$RESULTS_FILE"

for MODEL in "${MODELS[@]}"; do
    echo -n "Testing $MODEL... "
    
    # Run with 30s timeout
    OUTPUT=$(timeout 30s opencode run -m "$MODEL" "$PROMPT" 2>&1) || true
    
    # Check if output contains the expected UUID
    if echo "$OUTPUT" | grep -q "$EXPECTED_UUID"; then
        echo "✓ PASS"
        echo "| \`$MODEL\` | ✓ PASS | Tool calling works |" >> "$RESULTS_FILE"
    else
        echo "✗ FAIL"
        # Determine failure type
        if echo "$OUTPUT" | grep -qi "timeout"; then
            echo "| \`$MODEL\` | ✗ TIMEOUT | Hung or slow |" >> "$RESULTS_FILE"
        elif echo "$OUTPUT" | grep -qi "error\|failed\|not found"; then
            echo "| \`$MODEL\` | ✗ ERROR | $(echo "$OUTPUT" | head -1 | cut -c1-50) |" >> "$RESULTS_FILE"
        else
            echo "| \`$MODEL\` | ✗ HALLUCINATED | Did not fetch UUID |" >> "$RESULTS_FILE"
        fi
    fi
done

echo ""
echo "=== Results saved to $RESULTS_FILE ==="
cat "$RESULTS_FILE"
