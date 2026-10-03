# OpenRouter Model Selection & Vetting Process

When configuring OpenCode to use free models via OpenRouter, we follow a strict
selection and vetting process.
Agentic workflows (tool calling, json formatting, negative constraints) require high
parameter capability, instruction tuning, and specific API support.

This document serves as the historical record of which models have been tested,
approved, or blacklisted, and why.

* * *

## ✅ The “Approved for Subagents” Roster

These models have passed strict testing.
They successfully handle standard text generation AND they correctly output
syntactically valid JSON tool calls matching the OpenCode schemas.

- `openrouter/arcee-ai/trinity-large-preview:free`

- `openrouter/arcee-ai/trinity-mini:free`

- `openrouter/meta-llama/llama-3.3-70b-instruct:free` *(rotated off the free
  tier 2026-08; paid base model still listed — removed from whitelist)*

- `openrouter/minimax/minimax-m2.5:free`

- `openrouter/mistralai/mistral-small-3.1-24b-instruct`

- `openrouter/mistralai/mistral-small-3.2-24b-instruct`

- `openrouter/openai/gpt-oss-120b:free` *(rotated off the free tier 2026-08;
  paid base model still listed — removed from whitelist)*

- `openrouter/openrouter/elephant-alpha`

- `openrouter/openrouter/free`

- `openrouter/openrouter/owl-alpha`

- `openrouter/poolside/laguna-xs.2:free` *(dead 2026-08; succeeded by the
  laguna 2.1 line below)*

- `openrouter/poolside/laguna-s-2.1:free` *(provisional 2026-08: successor of
  the approved laguna line; passed a live chat call, strict tool-call vetting
  still pending)*

- `openrouter/poolside/laguna-xs-2.1:free` *(provisional 2026-08: successor of
  the approved laguna line; passed a live chat call, strict tool-call vetting
  still pending)*

- `openrouter/z-ai/glm-4.5-air:free`

* * *

## 🟡 The “Useful but Non-Agentic” Roster

These models are active on the free tier but **failed** strict tool-calling validation.
They should NOT be assigned to subagents (like `Reviewer: Code` or
`Writer: General Code`) because they will output broken JSON or hallucinate tool syntax.

However, they are valuable for **pure text tasks** (summarization, document
classification, translation, transcript compression) if invoked directly via
`opencode run` without tool permissions.

**Failed Tool/JSON Formatting (Output strings instead of booleans, broke JSON syntax):**

- `nvidia/nemotron-nano-9b-v2:free` (Output invalid JSON arguments)

- `nvidia/nemotron-nano-12b-v2-vl:free` (Output invalid JSON arguments)

**API Explicitly Denies Tool Use:**

- `cognitivecomputations/dolphin-mistral-24b-venice-edition:free`

- `liquid/lfm-2.5-1.2b-thinking:free`

* * *

## ❌ The Blacklist

### 1. Parameter Constraints (<35B)

Models below ~35B are systematically blacklisted unless they have proven exceptional
tuning.
Small models fall into infinite tool loops, ignore negative constraints (e.g. “Do
not use bash”), and suffer rapid context degradation.

- `allenai/molmo-2-8b:free`

- `deepseek/deepseek-r1-0528-qwen3-8b:free`

- `google/gemma-3-12b-it:free`

- `google/gemma-3-4b-it:free`

- `google/gemma-3n-e2b-it:free`

- `google/gemma-3n-e4b-it:free`

- `liquid/lfm-2.5-1.2b-instruct:free`

- `meta-llama/llama-3.2-3b-instruct:free`

- `mistralai/mistral-7b-instruct:free`

- `google/gemma-3-27b-it:free` (Moved to free tier but failed validation) - removed
  2026-05-09

- `qwen/qwen-2.5-vl-7b-instruct:free`

- `qwen/qwen2.5-vl-32b-instruct:free`

- `qwen/qwen3-14b:free`

- `qwen/qwen3-4b:free`

- `qwen/qwen3-8b:free`

- `qwen/qwq-32b:free`

### 2. Dead Endpoints (404 No Endpoints)

These models are technically documented as “free” somewhere on OpenRouter or third-party
lists, but pinging the API returns a hard 404. OpenRouter has likely rotated them out.

- `deepseek/deepseek-r1-0528:free`

- `deepseek/deepseek-r1:free`

- `deepseek/deepseek-v3-base:free`

- `google/gemini-2.0-flash-exp:free`

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

### 3. Expired Free Periods

These models return explicit HTTP 400 API errors stating “The free period has ended.
To continue using this model, please migrate to the paid slug.”

- `kwaipilot/kat-coder-pro:free`

- `mistralai/devstral-2512:free`

### 4. Paid / Premium Models (All)

Every other model provided by OpenRouter that does not explicitly end in `:free` is
blanket-blacklisted to prevent accidental token charges during autonomous subagent
loops. This includes all standard Claude, OpenAI, and Gemini premium endpoints available
via OpenRouter.

* * *

*Note: OpenRouter’s free tier rotates frequently.
To validate a new free model, run it through `test_models2.py` which forces a strict
JSON schema validation for tool-calling capabilities.*

* * *

## 2026-08-12 Catalog Sweep

Whitelist removals (rotated/dead upstream): `meta-llama/llama-3.3-70b-instruct:free`,
`openai/gpt-oss-120b:free`, `qwen/qwen3-coder:free`, `poolside/laguna-m.1:free`,
`poolside/laguna-xs.2:free`.

Moved whitelist → blacklist: `google/gemma-4-31b-it:free` (live but every chat
call returns HTTP 400 "Provider returned error").

New free models blacklisted per the <35B parameter rule:
`inclusionai/ling-3.0-tiny:free`, `liquid/lfm-2.5-2.6b:free`,
`nvidia/nemotron-3.5-lightning:free` (30B-A3B).

Provisional whitelist additions (laguna 2.1 line, chat-verified, tool-call
vetting pending): `poolside/laguna-s-2.1:free`, `poolside/laguna-xs-2.1:free`.

* * *

## 2026-08-21 Catalog Sweep

Whitelist addition: `stealth/ox-alpha` ("Ox Alpha", 1M context, multimodal,
zero-cost promotional window). Free but has no `:free` suffix, like the
already-approved `openrouter/elephant-alpha` and `openrouter/owl-alpha`
stealth entries. Re-check pricing when the promotional window closes;
rule 4 (blanket-blacklist anything not ending in `:free`) exists to stop
accidental token charges, and this entry is a deliberate exception to it.

New free models blacklisted after strict tool-call vetting:

- `dots-studio/dots-3-note-preview:free` — 280B total / 16B active MoE, so it
  clears the <35B bar, and a plain chat call returns text normally. Any request
  carrying a `tools` array returns HTTP 400 `{"code":400,"msg":"bad request"}`.
  The same payload against `nvidia/nemotron-3-ultra-550b-a55b:free` returns a
  well-formed `read_file` call, so the payload is sound and the model is the
  cause. Belongs to the "API Explicitly Denies Tool Use" roster; usable for
  pure text work through `opencode run` without tool permissions.

- `z-ai/glm-5.2:free` — every call over ~5 minutes of retries returned upstream
  429 `"z-ai/glm-5.2:free is temporarily rate-limited upstream"` from the shared
  Decart pool. Not a defect in the model: no successful chat call means it never
  reached even the provisional bar the laguna 2.1 line passed. Retry when the
  shared pool has capacity, or after adding a BYOK z.ai key.

Moved whitelist → blacklist: `nvidia/nemotron-3-super-120b-a12b:free` — still
listed in the catalog, but every call returns HTTP 404 "Provider returned
error". Paid base `nvidia/nemotron-3-super-120b-a12b` still resolves. Same
"Dead Endpoints" shape as the llama-3.3-70b and gpt-oss-120b free tiers. The
`:free` route on kilo is a separate gateway and still passes.

* * *

## 2026-09-12 Catalog Sweep

Whitelist removal: `stealth/ox-alpha` — no longer in the live catalog (HTTP 404 "Thank you for participating in the Stealth Ox Alpha testing period. This model was ZAI's GLM-5.3 Flash. Use it now: https://openrouter.ai/z-ai/glm-5.3-flash"). Promotional window closed. Paid base `z-ai/glm-5.3-flash` still listed separately.

New free models blacklisted (7 unaccounted free models flagged by `validate_openrouter`; all probed live at 2026-09-12 via `openrouter.ai/api/v1/chat/completions` with `OPENROUTER_API_KEY`):

- `inclusionai/ling-3.0-flash-fin:free` — 124B total / 5.1B active MoE, finance-specialized Ling 3.0 Flash variant. Chat probe succeeds (reasoning-only response for "Reply with exactly OK" is expected from this thinking model) and a `tools=[search_files]` probe returns a well-formed `{"query":"auth"}` tool call. Tool-capable but domain-specialized; not vetted for general agentic loops. Blacklisted pending broader evaluation; usable for pure-text finance tasks via `opencode run` without tools if needed.

- `inclusionai/ling-3.0-flash-sante:free` — 124B total / 5.1B active MoE, health/medicine-specialized Ling 3.0 Flash variant. Same probe results as fin: chat OK, tool call well-formed. Same triage.

- `inclusionai/ling-3.0-flash-vl:free` — 124B total / 5.5B active MoE, vision-enriched Ling 3.0 Flash variant (text+image+video->text). Same probe results as fin/sante: chat OK, tool call well-formed. Same triage.

- `nex-agi/nex-n2.5-mini:free` — Qwen3.5 MoE agentic coding model (256 experts, 40 layers, 2048 hidden). Chat probe succeeds ("OK"). Tool probe with default `reasoning.effort=high` intermittently returns no `tool_calls` (reasoning-only), but with `effort=none/low` returns a well-formed `search_files` call. Behavior depends on reasoning config, so the default agentic harness would see flaky tool use. Blacklisted pending a dedicated vetting run that pins reasoning effort and checks JSON schema validity across multiple prompts.

- `nex-agi/nex-n2.5-pro:free` — Larger sibling (512 experts, 60 layers, 4096 hidden, FP8 quantized). Same shape as mini: chat OK, tool call present with `effort=none/low` and usually with `high` (one high-effort probe succeeded). Same flaky-default concern; blacklisted pending the same dedicated vetting.

- `thinkingmachines/inkling-small:free` — 276B total / 12B active MoE (open-weight multimodal, 1.05M context). Gate-restricted: every raw chat probe returns HTTP 403 "is only available on agentic harnesses. Try plugging it into a coding agent or productivity app listed on https://openrouter.ai/apps". The 403 is from probing outside a harness, not from model capability. Not invocable via the raw API the validator uses, so it cannot pass the minimal raw check. Blacklisted for raw API; it could be whitelisted when called through a harness (OpenCode is listed at https://openrouter.ai/apps), but remains blacklisted until a harness probe passes. Not a vision model.

- `thinkingmachines/inkling:free` — 975B total / 41B active MoE flagship (1.05M context). Same HTTP 403 gate as the small variant. Same triage: blacklisted for raw API, harness-whitelistable in principle, pending harness validation. Not a vision model.

Validator clean after this sweep: no unaccounted free models; remaining whitelisted models pass live chat checks (one rate-limited upstream is informational only).

