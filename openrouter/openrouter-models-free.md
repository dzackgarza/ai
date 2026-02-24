# OpenRouter Models - Free Tier Checklist

**Generated:** 2026-02-23  
**Source:** `opencode models` from opencode configuration  
**Tested:** 2026-02-23

---

## Summary

| Category | Count |
|----------|-------|
| **Free Models** | 54 |
| **Tested** | 54 |
| **✅ Working** | 52 |
| **⚠️ Timeout** | 2 |
| **❌ Failed** | 0 |

---

## Test Results

### ✅ Working Models (52)

All of these responded with "hello" within 30 seconds:

#### A
- [x] `openrouter/arcee-ai/trinity-large-preview:free`

#### C
- [x] `openrouter/cognitivecomputations/dolphin-mistral-24b-venice-edition:free`

#### D
- [x] `openrouter/deepseek/deepseek-r1-0528-qwen3-8b:free`
- [x] `openrouter/deepseek/deepseek-r1-0528:free`
- [x] `openrouter/deepseek/deepseek-r1:free`
- [x] `openrouter/deepseek/deepseek-v3-base:free`

#### G
- [x] `openrouter/google/gemini-2.0-flash-exp:free`
- [x] `openrouter/google/gemma-3-12b-it:free`
- [x] `openrouter/google/gemma-3-27b-it:free`
- [x] `openrouter/google/gemma-3-4b-it:free`
- [x] `openrouter/google/gemma-3n-e2b-it:free`
- [x] `openrouter/google/gemma-3n-e4b-it:free`

#### K
- [x] `openrouter/kwaipilot/kat-coder-pro:free`

#### L
- [x] `openrouter/liquid/lfm-2.5-1.2b-instruct:free`
- [x] `openrouter/liquid/lfm-2.5-1.2b-thinking:free`

#### M
- [x] `openrouter/meta-llama/llama-3.1-405b-instruct:free`
- [x] `openrouter/meta-llama/llama-3.2-3b-instruct:free`
- [x] `openrouter/meta-llama/llama-3.3-70b-instruct:free`
- [x] `openrouter/meta-llama/llama-4-scout:free`
- [x] `openrouter/microsoft/mai-ds-r1:free`
- [x] `openrouter/mistralai/devstral-2512:free`
- [x] `openrouter/mistralai/devstral-small-2505:free`
- [x] `openrouter/mistralai/mistral-7b-instruct:free`
- [x] `openrouter/mistralai/mistral-nemo:free`
- [x] `openrouter/mistralai/mistral-small-3.2-24b-instruct:free`
- [x] `openrouter/moonshotai/kimi-dev-72b:free`
- [x] `openrouter/moonshotai/kimi-k2:free`

#### N
- [x] `openrouter/nousresearch/hermes-3-llama-3.1-405b:free`
- [x] `openrouter/nvidia/nemotron-3-nano-30b-a3b:free`
- [x] `openrouter/nvidia/nemotron-nano-12b-v2-vl:free`
- [x] `openrouter/nvidia/nemotron-nano-9b-v2:free`

#### O
- [x] `openrouter/openai/gpt-oss-120b:free`
- [x] `openrouter/openai/gpt-oss-20b:free`

#### Q
- [x] `openrouter/qwen/qwen-2.5-vl-7b-instruct:free`
- [x] `openrouter/qwen/qwen2.5-vl-32b-instruct:free`
- [x] `openrouter/qwen/qwen2.5-vl-72b-instruct:free`
- [x] `openrouter/qwen/qwen3-14b:free`
- [x] `openrouter/qwen/qwen3-235b-a22b-07-25:free`
- [x] `openrouter/qwen/qwen3-235b-a22b:free`
- [x] `openrouter/qwen/qwen3-30b-a3b:free`
- [x] `openrouter/qwen/qwen3-32b:free`
- [x] `openrouter/qwen/qwen3-4b:free`
- [x] `openrouter/qwen/qwen3-8b:free`
- [x] `openrouter/qwen/qwen3-coder:free`
- [x] `openrouter/qwen/qwen3-next-80b-a3b-instruct:free`
- [x] `openrouter/qwen/qwq-32b:free`

#### S
- [x] `openrouter/sarvamai/sarvam-m:free`
- [x] `openrouter/stepfun/step-3.5-flash:free`

#### T
- [x] `openrouter/thudm/glm-z1-32b:free`
- [x] `openrouter/tngtech/deepseek-r1t2-chimera:free`
- [x] `openrouter/tngtech/tng-r1t-chimera:free`

#### Z
- [x] `openrouter/z-ai/glm-4.5-air:free`

---

### ⚠️ Timeout (2)

These models did not respond within 30 seconds:

- [ ] `openrouter/allenai/molmo-2-8b:free` — TIMEOUT
- [ ] `openrouter/arcee-ai/trinity-mini:free` — TIMEOUT

---

### ❌ Failed (0)

No errors.

---

## Notes

- **Test command:** `opencode run --attach http://localhost:4096 --thinking --print-logs "Say hello and exit."`
- **Timeout:** 30 seconds per model
- Free models are identified by the `:free` suffix
- Model availability on OpenRouter can change — verify with `opencode models --refresh`
- Free tier models may have rate limits or reduced capabilities
- Some models may not support tool use on free tier
- Full test results: `~/test-openrouter-results-summary.md`
