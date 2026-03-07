# Classifier test harness

Evaluates every model in `CLASSIFIER_MODELS` against a labeled 12-case suite.
Records per-run YAML logs and cumulative accuracy in `scores.yaml`.

## Usage

```bash
cd plugins/examples/prompt-router/tests/classifier

# Default model (groq/llama-3.3-70b-versatile):
bun run run.ts

# Specific model:
bun run run.ts groq/moonshotai/kimi-k2-instruct

# MD_JSON mode (prompt-based JSON, no response_format header):
bun run run.ts nvidia/mistralai/mistral-large-3-675b-instruct-2512 --mode MD_JSON
```

Output: `runs/<model-slug>/<timestamp>.yaml`. Cumulative scores: `scores.yaml`.

## How it works

1. Reads `playbook.md` (constitutional classifier system prompt) and `cases.yaml`.
2. Calls the model for each case; compares returned tier to expected tier.
3. Updates `scores.yaml` with cumulative accuracy.
4. Uses `@instructor-ai/instructor` with Zod schema + `max_retries: 3` — invalid
   JSON is retried automatically, eliminating parse errors from results.
5. 10s delay between calls to stay within Groq's 6 RPM free-tier cap.

## Model compatibility

### Confirmed accurate (12/12)

| Model | Mode | Latency | Notes |
|-------|------|---------|-------|
| `groq/llama-3.3-70b-versatile` | JSON | 138–400ms | Primary — fast LPU, generous free tier |
| `groq/moonshotai/kimi-k2-instruct` | JSON | 151–1165ms | Reliable fallback |
| `nvidia/mistralai/mistral-large-3-675b-instruct-2512` | MD_JSON | 890–1688ms | Requires MD_JSON; 400 on json_object probe |
| `nvidia/mistralai/mistral-small-3.1-24b-instruct-2503` | JSON | 995–1630ms | Accurate, slower |

### Confirmed accurate (11/12)

| Model | Mode | Notes |
|-------|------|-------|
| `nvidia/meta/llama-3.3-70b-instruct` | JSON | NVIDIA NIM |
| `groq/meta-llama/llama-4-maverick-17b-128e-instruct` | JSON | Superseded by kimi-k2 |

### Last-resort only

| Model | Constraint |
|-------|-----------|
| `arcee-ai/trinity-large-preview:free` (OpenRouter) | **50 req/day account-wide cap** |

### Rejected — do not use

| Model | Reason |
|-------|--------|
| `stepfun/step-3.5-flash:free`, `z-ai/glm-4.5-air:free` | Thinking models — content empty at `max_tokens=200` |
| `nvidia/nvidia/llama-3.1-nemotron-ultra-253b-v1` | Thinking model — JSON truncated (Unexpected EOF) |
| `groq/qwen/qwen3-32b` | Thinking model — outputs `<think>` blocks |
| `nvidia/google/gemma-3-27b-it` | Strict role alternation incompatible with instructor |

## Rate limit notes

**Groq free tier:** ~100k tokens/day. Constitutional playbook is ~2,300 tokens/call.
Max safe runs/day: ~43. Hit the TPD limit → switch to NVIDIA NIM for batch runs.

**OpenRouter free tier:** 50 requests/day account-wide (resets midnight UTC). Reserve for spot-checks only.

**NVIDIA NIM:** No daily cap. Prefer for batch runs when Groq TPD is exhausted.

## MD_JSON mode

Some models return HTTP 400 on `response_format: json_object` (e.g., Mistral Large
on NVIDIA NIM — Mistral tokenizer not supported for guidance backend).

Pass `--mode MD_JSON` to use prompt-based JSON instead. Works for Mistral Large
(12/12 at `max_tokens=400`).

**Rule:** HTTP 400/404 on json_object probe ≠ model is unusable. Always try `--mode MD_JSON`.
