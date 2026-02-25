# OpenRouter Models - Free Tier Checklist

**Generated:** 2026-02-25  
**Source:** OpenRouter API (`https://openrouter.ai/api/v1/models`)  
**Updated:** 2026-02-25

---

## Summary

| Category | Count |
|----------|-------|
| **Free Models (in API)** | 25 |
| **Supports Tools** | 14 |
| **Excluded (No Tool Support)** | 11 |

---

## Supports Tools (14 models) ✅

Models kept for OpenCode config (all are `:free` and API-reported tool-capable):

- [ ] `openrouter/arcee-ai/trinity-mini:free` — 131,072 ctx, 131,072 output
- [ ] `openrouter/google/gemma-3-27b-it:free` — 131,072 ctx, 8,192 output
- [ ] `openrouter/meta-llama/llama-3.3-70b-instruct:free` — 128,000 ctx, 128,000 output
- [ ] `openrouter/mistralai/mistral-small-3.1-24b-instruct:free` — 128,000 ctx, 4,096 output
- [ ] `openrouter/nvidia/nemotron-3-nano-30b-a3b:free` — 256,000 ctx, 256,000 output
- [ ] `openrouter/nvidia/nemotron-nano-12b-v2-vl:free` — 128,000 ctx, 128,000 output
- [ ] `openrouter/nvidia/nemotron-nano-9b-v2:free` — 128,000 ctx, 128,000 output
- [ ] `openrouter/openai/gpt-oss-120b:free` — 131,072 ctx, 131,072 output
- [ ] `openrouter/openai/gpt-oss-20b:free` — 131,072 ctx, 131,072 output
- [ ] `openrouter/qwen/qwen3-4b:free` — 40,960 ctx, 40,960 output
- [ ] `openrouter/qwen/qwen3-coder:free` — 262,000 ctx, 262,000 output
- [ ] `openrouter/qwen/qwen3-next-80b-a3b-instruct:free` — 262,144 ctx, 262,144 output
- [ ] `openrouter/upstage/solar-pro-3:free` — 128,000 ctx, 4,096 output
- [ ] `openrouter/z-ai/glm-4.5-air:free` — 131,072 ctx, 96,000 output

---

## Repro Command

```bash
curl -s "https://openrouter.ai/api/v1/models" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for m in sorted(data['data'], key=lambda x: x['id']):
    if not m['id'].endswith(':free'):
        continue
    params = {p.lower() for p in m.get('supported_parameters', [])}
    if {'tools', 'tool_choice'}.issubset(params):
        print(m['id'])
"
```
