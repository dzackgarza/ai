# Free Vision Models via OpenRouter — Live Catalogue and Vetting

Source: `https://openrouter.ai/api/v1/models` (live, 2026-09-12) filtered to `pricing.prompt=0` and `pricing.completion=0` or `id` ends `:free`, cross-checked against `https://openrouter.ai/collections/free-models`. Local catalogue is `opencode/configs/providers/openrouter.json` (`whitelist` + `blacklist` must cover every live free model; validator in `opencode/scripts/build_config.py:validate_openrouter` enforces this). Vetting history lives in `opencode/configs/providers/notes/openrouter-model-vetting.md`.

* * *

## Summary

Live free models: 22.
Free vision-capable (accepts `image` or `video` input): 13.
Whitelisted total: 5 (only `openrouter/free` is vision-capable among whitelisted, but it is a router, not a model).
Blacklisted vision: 12 (including 2 audio-vision, 1 safety classifier, 2 harness-gated).

The `thinkingmachines` pair is gated `HTTP 403 is only available on agentic harnesses`. Raw `curl` probes correctly 403. They *could* be whitelisted when called through an agentic harness (OpenCode is listed at https://openrouter.ai/apps), but this repo keeps them blacklisted until a harness-header probe passes. See vetting notes. They remain listed here as free vision models with their gate documented.

* * *

## Free Vision Models (live 2026-09-12)

| Model | Input → Output | Context | Pricing | Catalogue | Vetting reason |
| --- | --- | --- | --- | --- | --- |
| `dots-studio/dots-3-note-preview:free` | text+image → text | 512K | $0 | blacklist | 280B/16B MoE, chat pass, `tools` returns 400 `bad request` — denies tool use, useful pure-text/vision via `opencode run` without tools only |
| `google/gemma-4-26b-a4b-it:free` | text+image+video → text | 1M? | $0 | blacklist | 26B-A4B, <35B class, vision, not vetted for agentic loops |
| `google/gemma-4-31b-it:free` | text+image+video → text | 1M? | $0 | blacklist | 31B, live but 400 on every chat, dead endpoint shape |
| `google/lyria-3-clip-preview` | text+image → text+audio | 32K? | $0 | blacklist | Audio generation (Lyria), not text agentic, vision input but audio output |
| `google/lyria-3-pro-preview` | text+image → text+audio | 32K? | $0 | blacklist | Same as clip |
| `inclusionai/ling-3.0-flash-vl:free` | text+image+video → text | 262K | $0 | blacklist | 124B/5.5B MoE vision-Ling, chat + `tools=[search_files]` → well-formed `{"query":"auth"}`, tool-capable but domain vision-specialized, pending general agentic vetting |
| `nex-agi/nex-n2.5-mini:free` | text+image → text | 262K | $0 | blacklist | Qwen3.5 MoE 256 experts vision agentic coder, chat pass, tool call needs `reasoning.effort=none/low`, default high flaky — pending pinned-effort vetting |
| `nex-agi/nex-n2.5-pro:free` | text+image → text | 262K | $0 | blacklist | 512 experts vision agentic coder, same flaky-default concern |
| `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free` | text+image+audio+video → text | 256K | $0 | blacklist | 30B/3B multimodal omni perception sub-agent (Conv3D video, EVS), vision+audio+video, blacklisted as specialty omni, not general chat |
| `nvidia/nemotron-3.5-content-safety:free` | text+image → text | 256K | $0 | blacklist | Safety classifier, vision input but not generative |
| `openrouter/free` | text+image → text | varies | $0 | whitelist | Not a model, router that selects among free models, advertises image input |
| `thinkingmachines/inkling:free` | text+image+audio → text | 1.05M | $0 | blacklist | 975B/41B MoE vision+audio, 1.05M context, harness-gated (raw 403), blacklisted for raw API; could be whitelisted via harness, pending harness probe — see vetting notes |
| `thinkingmachines/inkling-small:free` | text+image+audio → text | 1.05M | $0 | blacklist | 276B/12B small sibling, same gate and triage |

Non-vision live free models (9) for completeness: `cohere/north-mini-code:free`, `inclusionai/ling-3.0-flash-fin:free`, `inclusionai/ling-3.0-flash-sante:free`, `liquid/lfm-2.5-2.6b:free`, `nvidia/nemotron-3-super-120b-a12b:free`, `nvidia/nemotron-3-ultra-550b-a55b:free`, `nvidia/nemotron-3.5-lightning:free`, `poolside/laguna-s-2.1:free`, `poolside/laguna-xs-2.1:free`.

* * *

## Vetting Decisions (how to read the table)

- **Parameter rule (<35B)**: `gemma-4-26b`, `lfm-2.5-2.6b`, `nemotron-3.5-lightning` (30B) are <35B class and systematically blacklisted for agentic loops unless exceptional tuning is proven. No exception proven here.
- **Tool-use gate**: `dots-studio` denies `tools` array with 400; `lyria` is audio-output; `nemotron-nano-omni` and `content-safety` are specialty models, not general text+vision chat. They fail the agentic tool-call bar and belong to the "Useful but Non-Agentic" or specialty rosters.
- **Domain-specialized vision**: `ling-3.0-flash-vl` passes chat + tool call but is vision-enriched Ling specialized for video perception; `nex-n2.5` pair are vision agentic coders but need reasoning-effort pinning. Both are blacklisted pending broader harness-level vetting with image payloads, not because they are incapable.
- **Harness-gated vision**: `inkling` pair are open-weight multimodal MoE from Thinking Machines Lab. The 403 is not an expiry; it is the free-tier harness gate. When the request originates from a listed agentic harness (OpenCode is at https://openrouter.ai/apps) the gate *could* clear, so they are whitelist-*able* in principle. This repo keeps them blacklisted until a harness-header probe is recorded. Raw `validate_openrouter` shows 403 — that is expected for raw probes.
- **Router**: `openrouter/free` is not a model; it is a free-tier router. Whitelisted because it is the simplest entry point for free inference.

* * *

## How to Verify

```bash
# Live free count and vision filter
python3 /tmp/vision_probe.py  # or: curl -s https://openrouter.ai/api/v1/models | jq

# Local catalogue invariant
cd opencode && uv run --python .venv/bin/python scripts/build_config.py --validate-only --strict --provider openrouter

# Vision file is the repo root record; vetting history is the notes file
cat FREE_VISION_MODELS.md
cat opencode/configs/providers/notes/openrouter-model-vetting.md
```

## When to Update

- Free tier rotates frequently. Re-run the live fetch and the validator. Any `unaccounted` free model must be triaged into `whitelist` or `blacklist` with a probe record (chat + `tools=[search_files]` payload) and a note in `openrouter-model-vetting.md`.
- For vision models, add a row here with modalities, context, and vetting outcome. If a model is harness-gated, note the gate and the harness header required.
- If a vision model is promoted to whitelist, test it with an image payload through the harness (`opencode run -m openrouter/<id>` with image) and record the JSON tool-call validity.

* * *

## Sources

- OpenRouter free collection: https://openrouter.ai/collections/free-models (ranked 2026-09)
- OpenRouter full catalogue: https://openrouter.ai/api/v1/models
- This repo's validator: `opencode/scripts/build_config.py:validate_openrouter`, `is_openrouter_free`, `_is_upstream_rate_limit`
- Vetting notes: `opencode/configs/providers/notes/openrouter-model-vetting.md` (sweeps 2026-08-12, 2026-08-21, 2026-09-12)
