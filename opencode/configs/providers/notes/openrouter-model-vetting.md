# OpenRouter Model Selection & Vetting Process

When configuring OpenCode to use free models via OpenRouter, we follow a strict selection and vetting process. Agentic workflows (tool calling, json formatting, negative constraints) require high parameter capability, instruction tuning, and specific API support.

This document serves as the historical record of which models have been tested, approved, or blacklisted, and why.

---

## ✅ The "Approved for Subagents" Roster

These models have passed strict testing. They successfully handle standard text generation AND they correctly output syntactically valid JSON tool calls matching the OpenCode schemas.

- `openrouter/arcee-ai/trinity-large-preview:free`
- `openrouter/google/gemma-3-27b-it:free` (Passes schema validation, though may struggle with complex reasoning chains compared to larger models)
- `openrouter/nvidia/nemotron-3-nano-30b-a3b:free` (Surprisingly capable: handles optional boolean parameters and schema typing perfectly despite its 30B size)
- `openrouter/openai/gpt-oss-120b:free`
- `openrouter/qwen/qwen3-coder:free`
- `openrouter/qwen/qwen3-next-80b-a3b-instruct:free`
- `openrouter/stepfun/step-3.5-flash:free`
- `openrouter/z-ai/glm-4.5-air:free`

---

## 🟡 The "Useful but Non-Agentic" Roster

These models are active on the free tier but **failed** strict tool-calling validation. They should NOT be assigned to subagents (like `Reviewer: Code` or `Writer: General Code`) because they will output broken JSON or hallucinate tool syntax.

However, they are valuable for **pure text tasks** (summarization, document classification, translation, transcript compression) if invoked directly via `opencode run` without tool permissions.

**Failed Tool/JSON Formatting (Output strings instead of booleans, broke JSON syntax):**

- `meta-llama/llama-3.3-70b-instruct:free` (Failed strict boolean JSON typing test)
- `nvidia/nemotron-nano-9b-v2:free` (Output invalid JSON arguments)
- `nvidia/nemotron-nano-12b-v2-vl:free` (Output invalid JSON arguments)

**API Explicitly Denies Tool Use:**

- `cognitivecomputations/dolphin-mistral-24b-venice-edition:free`
- `liquid/lfm-2.5-1.2b-thinking:free`

---

## ❌ The Blacklist

Models are systematically blacklisted based on the following criteria:

1.  **Redundant variants**: Variants that have clearly superior (free) variants available (e.g. Trinity Mini vs Trinity Large).
2.  **Size Constraints (<= 20B heuristic)**: Models too small for complex agentic workflows; prone to infinite loops and instruction drift.
3.  **Non-free**: Every model provided by OpenRouter that does not explicitly end in `:free` is blanket-blacklisted to prevent accidental token charges during autonomous subagent loops.
4.  **Specialized models**: Models with "Uncensored", "Roleplay" (RP), or other non-technical tunings that diverge from technical accuracy.
5.  **Small Context (<= 64k)**: Insufficient for 10-20 turns of interactive work or large file context.
6.  **"Braindead" models**: Models known to simply fail nontrivial work (e.g. Gemini 2.0 series, GPT-OSS 20B).

### 1. Superior Variants / Size / "Braindead"
- `arcee-ai/trinity-mini:free` (Redundant; `trinity-large` is vastly superior)
- `openai/gpt-oss-20b:free` (Too small / braindead for nontrivial tasks)
- `google/gemini-2.0-flash-exp:free` (Known "braindead" series)
- `google/gemini-2.0-flash:free`
- `google/gemini-2.0-flash-lite:free`
- `google/gemini-2.0-pro:free`

### 2. General Parameter Constraints (<= 35B)
Small models fall into infinite tool loops, ignore negative constraints (e.g. "Do not use bash"), and suffer rapid context degradation.

- `allenai/molmo-2-8b:free`
- `deepseek/deepseek-r1-0528-qwen3-8b:free`
- `google/gemma-3-12b-it:free`
- `google/gemma-3-4b-it:free`
- `google/gemma-3n-e2b-it:free`
- `google/gemma-3n-e4b-it:free`
- `liquid/lfm-2.5-1.2b-instruct:free`
- `meta-llama/llama-3.2-3b-instruct:free`
- `mistralai/mistral-7b-instruct:free`
- `mistralai/mistral-small-3.2-24b-instruct:free`
- `qwen/qwen-2.5-vl-7b-instruct:free`
- `qwen/qwen2.5-vl-32b-instruct:free`
- `qwen/qwen3-14b:free`
- `qwen/qwen3-4b:free`
- `qwen/qwen3-8b:free`
- `qwen/qwq-32b:free`

### 3. Dead Endpoints (404 No Endpoints)
These models are technically documented as "free" but return a hard 404 from the OpenRouter API.

- `deepseek/deepseek-r1-0528:free`
- `deepseek/deepseek-r1:free`
- `deepseek/deepseek-v3-base:free`
- `meta-llama/llama-3.1-405b-instruct:free`
- `meta-llama/llama-4-scout:free`
- `microsoft/mai-ds-r1:free`
- `mistralai/devstral-small-2505:free`
- `mistralai/mistral-nemo:free`
- `moonshotai/kimi-dev-72b:free`
- `moonshotai/kimi-k2:free`
- `qwen/qwen2.5-vl-72b-instruct:free`
- `qwen/qwen3-235b-a22b-07-25:free`
- `qwen/qwen3-235b-a22b:free`
- `sarvamai/sarvam-m:free`
- `tngtech/deepseek-r1t2-chimera:free`
- `tngtech/tng-r1t-chimera:free`
- `qwen/qwen3-30b-a3b:free`
- `qwen/qwen3-32b:free`
- `thudm/glm-z1-32b:free`

### 4. Expired Free Periods
These models return explicit HTTP 400 API errors stating "The free period has ended. To continue using this model, please migrate to the paid slug."

- `kwaipilot/kat-coder-pro:free`
- `mistralai/devstral-2512:free`

---

_Note: OpenRouter's free tier rotates frequently. To validate a new free model, run it through `test_models2.py` which forces a strict JSON schema validation for tool-calling capabilities._
