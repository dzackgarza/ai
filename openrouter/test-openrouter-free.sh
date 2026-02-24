#!/bin/bash
# OpenRouter Free Models Test Harness
# Tests all free models with resume capability
# Results saved to test-openrouter-results.md

RESULTS_FILE="/home/dzack/test-openrouter-results.md"
PROGRESS_FILE="/home/dzack/.test-openrouter-progress"
TIMEOUT_SEC=30

# Free models list
MODELS=(
"openrouter/allenai/molmo-2-8b:free"
"openrouter/arcee-ai/trinity-large-preview:free"
"openrouter/arcee-ai/trinity-mini:free"
"openrouter/cognitivecomputations/dolphin-mistral-24b-venice-edition:free"
"openrouter/deepseek/deepseek-r1-0528-qwen3-8b:free"
"openrouter/deepseek/deepseek-r1-0528:free"
"openrouter/deepseek/deepseek-r1:free"
"openrouter/deepseek/deepseek-v3-base:free"
"openrouter/google/gemini-2.0-flash-exp:free"
"openrouter/google/gemma-3-12b-it:free"
"openrouter/google/gemma-3-27b-it:free"
"openrouter/google/gemma-3-4b-it:free"
"openrouter/google/gemma-3n-e2b-it:free"
"openrouter/google/gemma-3n-e4b-it:free"
"openrouter/kwaipilot/kat-coder-pro:free"
"openrouter/liquid/lfm-2.5-1.2b-instruct:free"
"openrouter/liquid/lfm-2.5-1.2b-thinking:free"
"openrouter/meta-llama/llama-3.1-405b-instruct:free"
"openrouter/meta-llama/llama-3.2-3b-instruct:free"
"openrouter/meta-llama/llama-3.3-70b-instruct:free"
"openrouter/meta-llama/llama-4-scout:free"
"openrouter/microsoft/mai-ds-r1:free"
"openrouter/mistralai/devstral-2512:free"
"openrouter/mistralai/devstral-small-2505:free"
"openrouter/mistralai/mistral-7b-instruct:free"
"openrouter/mistralai/mistral-nemo:free"
"openrouter/mistralai/mistral-small-3.2-24b-instruct:free"
"openrouter/moonshotai/kimi-dev-72b:free"
"openrouter/moonshotai/kimi-k2:free"
"openrouter/nousresearch/hermes-3-llama-3.1-405b:free"
"openrouter/nvidia/nemotron-3-nano-30b-a3b:free"
"openrouter/nvidia/nemotron-nano-12b-v2-vl:free"
"openrouter/nvidia/nemotron-nano-9b-v2:free"
"openrouter/openai/gpt-oss-120b:free"
"openrouter/openai/gpt-oss-20b:free"
"openrouter/qwen/qwen-2.5-vl-7b-instruct:free"
"openrouter/qwen/qwen2.5-vl-32b-instruct:free"
"openrouter/qwen/qwen2.5-vl-72b-instruct:free"
"openrouter/qwen/qwen3-14b:free"
"openrouter/qwen/qwen3-235b-a22b-07-25:free"
"openrouter/qwen/qwen3-235b-a22b:free"
"openrouter/qwen/qwen3-30b-a3b:free"
"openrouter/qwen/qwen3-32b:free"
"openrouter/qwen/qwen3-4b:free"
"openrouter/qwen/qwen3-8b:free"
"openrouter/qwen/qwen3-coder:free"
"openrouter/qwen/qwen3-next-80b-a3b-instruct:free"
"openrouter/qwen/qwq-32b:free"
"openrouter/sarvamai/sarvam-m:free"
"openrouter/stepfun/step-3.5-flash:free"
"openrouter/thudm/glm-z1-32b:free"
"openrouter/tngtech/deepseek-r1t2-chimera:free"
"openrouter/tngtech/tng-r1t-chimera:free"
"openrouter/z-ai/glm-4.5-air:free"
)

# Initialize results file header
init_results() {
    cat > "$RESULTS_FILE" << 'EOF'
# OpenRouter Free Models Test Results

**Test Date:** $(date '+%Y-%m-%d %H:%M:%S')  
**Timeout:** 30 seconds  
**Command:** `opencode run --attach http://localhost:4096 --agent=minimal --thinking --print-logs "Say hello and exit"`

---

## Summary

| Status | Count |
|--------|-------|
| ✅ Working | 0 |
| ⚠️ Timeout | 0 |
| ❌ Error | 0 |
| ⏭️ Skipped | 0 |
| **Total** | TOTAL |

---

## Results

EOF
    sed -i "s/\$(date '+%Y-%m-%d %H:%M:%S')/$(date '+%Y-%m-%d %H:%M:%S')/" "$RESULTS_FILE"
}

# Update summary counts
update_summary() {
    local working=$(grep -c '^\[✅\]' "$RESULTS_FILE" 2>/dev/null || echo 0)
    local timeout=$(grep -c '^\[⚠️\]' "$RESULTS_FILE" 2>/dev/null || echo 0)
    local error=$(grep -c '^\[❌\]' "$RESULTS_FILE" 2>/dev/null || echo 0)
    local skipped=$(grep -c '^\[⏭️\]' "$RESULTS_FILE" 2>/dev/null || echo 0)
    local total=${#MODELS[@]}
    
    sed -i "s/| ✅ Working | [0-9]* |/| ✅ Working | $working |/" "$RESULTS_FILE"
    sed -i "s/| ⚠️ Timeout | [0-9]* |/| ⚠️ Timeout | $timeout |/" "$RESULTS_FILE"
    sed -i "s/| ❌ Error | [0-9]* |/| ❌ Error | $error |/" "$RESULTS_FILE"
    sed -i "s/| ⏭️ Skipped | [0-9]* |/| ⏭️ Skipped | $skipped |/" "$RESULTS_FILE"
    sed -i "s/| \*\*Total\*\* | [0-9]* |/| **Total** | $total |/" "$RESULTS_FILE"
}

# Test single model
test_model() {
    local model=$1
    local output
    local exit_code
    
    echo ""
    echo "========================================"
    echo "Testing: $model"
    echo "========================================"
    
    output=$(timeout $TIMEOUT_SEC opencode run \
        --attach http://localhost:4096 \
        --thinking \
        --print-logs \
        "Say hello and exit." 2>&1)
    
    exit_code=$?
    
    # Determine status
    local status_icon
    local status_text
    
    if [ $exit_code -eq 124 ]; then
        status_icon="⚠️"
        status_text="TIMEOUT"
    elif [ $exit_code -eq 0 ]; then
        # Check if output contains actual response
        if echo "$output" | grep -qi "hello"; then
            status_icon="✅"
            status_text="WORKING"
        else
            status_icon="❌"
            status_text="ERROR (no response)"
        fi
    else
        status_icon="❌"
        status_text="ERROR (exit $exit_code)"
    fi
    
    # Append to results
    echo "" >> "$RESULTS_FILE"
    echo "### $model" >> "$RESULTS_FILE"
    echo "" >> "$RESULTS_FILE"
    echo "**Status:** $status_icon $status_text" >> "$RESULTS_FILE"
    echo "" >> "$RESULTS_FILE"
    echo "<details>" >> "$RESULTS_FILE"
    echo "<summary>View Output</summary>" >> "$RESULTS_FILE"
    echo "" >> "$RESULTS_FILE"
    echo '```' >> "$RESULTS_FILE"
    echo "$output" | head -500 >> "$RESULTS_FILE"  # Limit output in results
    if [ ${#output} -gt 500 ]; then
        echo "... (truncated)" >> "$RESULTS_FILE"
    fi
    echo '```' >> "$RESULTS_FILE"
    echo "" >> "$RESULTS_FILE"
    echo "</details>" >> "$RESULTS_FILE"
    
    update_summary
    
    echo "Result: $status_text"
    return $exit_code
}

# Main
echo "OpenRouter Free Models Test Harness"
echo "===================================="
echo "Total models: ${#MODELS[@]}"
echo "Timeout: ${TIMEOUT_SEC}s"
echo "Results: $RESULTS_FILE"
echo ""

# Check for resume
START_INDEX=0
if [ -f "$PROGRESS_FILE" ]; then
    LAST_MODEL=$(cat "$PROGRESS_FILE")
    for i in "${!MODELS[@]}"; do
        if [ "${MODELS[$i]}" == "$LAST_MODEL" ]; then
            START_INDEX=$((i + 1))
            echo "Resuming from index $START_INDEX (${MODELS[$START_INDEX]})"
            break
        fi
    done
fi

# Initialize results if starting fresh
if [ $START_INDEX -eq 0 ]; then
    init_results
fi

# Test each model
for i in "${!MODELS[@]}"; do
    if [ $i -lt $START_INDEX ]; then
        continue
    fi
    
    model="${MODELS[$i]}"
    test_model "$model"
    
    # Save progress
    echo "$model" > "$PROGRESS_FILE"
    
    echo ""
    echo "Progress: $((i + 1))/${#MODELS[@]}"
    echo "Press Ctrl+C to pause (progress saved)"
    echo ""
    
    # Small delay between tests
    sleep 1
done

# Cleanup
rm -f "$PROGRESS_FILE"
echo ""
echo "========================================"
echo "All tests completed!"
echo "Results saved to: $RESULTS_FILE"
echo "========================================"
