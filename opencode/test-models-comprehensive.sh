#!/bin/bash
# Comprehensive tool calling test for ALL models in the skill

PROMPT="Fetch the UUID from https://httpbin.org/uuid and return ONLY the UUID value. You must actually curl the URL."

# Get expected UUID
EXPECTED=$(curl -s https://httpbin.org/uuid | grep -o '[0-9a-f-]\{36\}')
echo "Expected UUID: $EXPECTED"
echo ""

# ALL models from the skill
MODELS=(
    # SOTA models
    "google/antigravity-claude-opus-4-6-thinking"
    "google/antigravity-claude-sonnet-4-6"
    "google/antigravity-gemini-3-flash"
    "google/antigravity-gemini-3-pro"
    "google/antigravity-gemini-3.1-pro"
    "openai/codex-mini-latest"
    "opencode/big-pickle"
    "opencode/glm-5-free"
    "opencode/gpt-5-nano"
    "opencode/minimax-m2.5-free"
    "ollama/minimax-m2.5:cloud"
    
    # OpenRouter top tier
    "openrouter/stepfun/step-3.5-flash:free"
    "openrouter/arcee-ai/trinity-large-preview:free"
    "openrouter/nvidia/nemotron-3-nano-30b-a3b:free"
    "openrouter/deepseek/deepseek-r1:free"
    "openrouter/meta-llama/llama-3.1-405b-instruct:free"
    "openrouter/arcee-ai/trinity-mini:free"
    
    # OpenRouter mid tier
    "openrouter/qwen/qwen3-32b:free"
    "openrouter/mistralai/mistral-small-3.2-24b-instruct:free"
    "openrouter/mistralai/devstral-2512:free"
    "openrouter/moonshotai/kimi-k2:free"
    "openrouter/meta-llama/llama-3.3-70b-instruct:free"
    "openrouter/minimax/minimax-m2.5"
    "openrouter/qwen/qwq-32b:free"
    
    # OpenRouter lightweight
    "openrouter/google/gemma-3-12b-it:free"
    "openrouter/mistralai/mistral-7b-instruct:free"
    "openrouter/nvidia/nemotron-nano-9b-v2:free"
    "openrouter/qwen/qwen3-8b:free"
    "openrouter/x-ai/grok-3-mini"
)

RESULTS_FILE="tool_test_all_models_$(date +%Y%m%d_%H%M%S).csv"
echo "Model,Result,Response" > "$RESULTS_FILE"

PASS=0
FAIL=0
TIMEOUT=0
ERROR=0

for MODEL in "${MODELS[@]}"; do
    echo -n "$MODEL: "
    
    OUTPUT=$(timeout 45s opencode run -m "$MODEL" "$PROMPT" 2>&1) || true
    
    if echo "$OUTPUT" | grep -q "$EXPECTED"; then
        echo "✓ PASS"
        echo "\"$MODEL\",PASS,\"Tool calling works\"" >> "$RESULTS_FILE"
        ((PASS++))
    elif echo "$OUTPUT" | grep -qi "timeout\|timed out"; then
        echo "⏱ TIMEOUT"
        echo "\"$MODEL\",TIMEOUT,\"Hung or too slow\"" >> "$RESULTS_FILE"
        ((TIMEOUT++))
    elif echo "$OUTPUT" | grep -qi "error\|failed\|not found\|provider"; then
        echo "✗ ERROR"
        echo "\"$MODEL\",ERROR,\"$(echo "$OUTPUT" | head -1 | tr '"' "'" | cut -c1-100)\"" >> "$RESULTS_FILE"
        ((ERROR++))
    else
        echo "✗ HALLUCINATED"
        echo "\"$MODEL\",HALLUCINATED,\"Did not fetch UUID\"" >> "$RESULTS_FILE"
        ((FAIL++))
    fi
done

echo ""
echo "=== SUMMARY ==="
echo "PASS: $PASS"
echo "HALLUCINATED: $FAIL"
echo "TIMEOUT: $TIMEOUT"
echo "ERROR: $ERROR"
echo ""
echo "Results saved to: $RESULTS_FILE"
