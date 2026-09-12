# Free Vision Models via OpenRouter — Live Catalogue and Vetting

Source: `https://openrouter.ai/api/v1/models` (live, 2026-09-12) filtered to `pricing.prompt=0` and `pricing.completion=0` or `id` ends `:free`, cross-checked against `https://openrouter.ai/collections/free-models`. Local catalogue is `opencode/configs/providers/openrouter.json` (`whitelist` + `blacklist` must cover every live free model; validator in `opencode/scripts/build_config.py:validate_openrouter` enforces this). Vetting history lives in `opencode/configs/providers/notes/openrouter-model-vetting.md`.

* * *

## Summary

Live free models: 18 (22 priced $0 minus 4 BYOK `is_byok:true` which require Google AI Studio key and are not free without BYOK).
Free vision-capable (accepts `image` or `video` input, per `architecture.input_modalities`, non-BYOK): 7.
Whitelisted total: 5 (only `openrouter/free` advertises image input, but it is a router, not a model; no vision model is whitelisted).
Blacklisted vision: 7 (including 1 safety classifier).

`thinkingmachines/inkling:free` and `thinkingmachines/inkling-small:free` are **not vision models**. They are general multimodal MoE that accept image/audio but are gated `HTTP 403 is only available on agentic harnesses`. The 403 was from probing outside a harness, not from vision handling. They are documented in `openrouter-model-vetting.md` as harness-gated, not here.

* * *

## Free Vision Models (live 2026-09-12)

| Model | Input → Output | Context | Pricing | Catalogue | Vetting reason |
| --- | --- | --- | --- | --- | --- |
| `dots-studio/dots-3-note-preview:free` | text+image → text | 512K | $0 | blacklist | 280B/16B MoE, chat pass, `tools` returns 400 `bad request` — denies tool use, useful pure-text/vision via `opencode run` without tools only |
| `inclusionai/ling-3.0-flash-vl:free` | text+image+video → text | 262K | $0 | blacklist | 124B/5.5B MoE vision-Ling, chat + `tools=[search_files]` → well-formed `{"query":"auth"}`, tool-capable but domain vision-specialized, pending general agentic vetting |
| `nex-agi/nex-n2.5-mini:free` | text+image → text | 262K | $0 | blacklist | Qwen3.5 MoE 256 experts vision agentic coder, chat pass, tool call needs `reasoning.effort=none/low`, default high flaky — pending pinned-effort vetting |
| `nex-agi/nex-n2.5-pro:free` | text+image → text | 262K | $0 | blacklist | 512 experts vision agentic coder, same flaky-default concern |
| `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free` | text+image+audio+video → text | 256K | $0 | blacklist | 30B/3B multimodal omni perception sub-agent (Conv3D video, EVS), vision+audio+video, blacklisted as specialty omni, not general chat |
| `nvidia/nemotron-3.5-content-safety:free` | text+image → text | 256K | $0 | blacklist | Safety classifier, vision input but not generative |
| `openrouter/free` | text+image → text | varies | $0 | whitelist | Not a model, router that selects among free models, advertises image input |

Non-vision live free models (11) for completeness: `cohere/north-mini-code:free`, `inclusionai/ling-3.0-flash-fin:free`, `inclusionai/ling-3.0-flash-sante:free`, `liquid/lfm-2.5-2.6b:free`, `nvidia/nemotron-3-super-120b-a12b:free`, `nvidia/nemotron-3-ultra-550b-a55b:free`, `nvidia/nemotron-3.5-lightning:free`, `poolside/laguna-s-2.1:free`, `poolside/laguna-xs-2.1:free`, `thinkingmachines/inkling:free`, `thinkingmachines/inkling-small:free` — last two are harness-gated general models, not vision, documented in vetting notes.

* * *

## Vetting Decisions (how to read the table)

- **Parameter rule (<35B)**: `lfm-2.5-2.6b`, `nemotron-3.5-lightning` (30B) are <35B class and systematically blacklisted for agentic loops unless exceptional tuning is proven. No exception proven here. (`gemma-4-26b` is BYOK, not free, and not in this table.)
- **Tool-use gate**: `dots-studio` denies `tools` array with 400; `nemotron-nano-omni` and `content-safety` are specialty models, not general text+vision chat. They fail the agentic tool-call bar and belong to the "Useful but Non-Agentic" or specialty rosters. (`lyria` is BYOK audio-output, not free.)
- **Domain-specialized vision**: `ling-3.0-flash-vl` passes chat + tool call but is vision-enriched Ling specialized for video perception; `nex-n2.5` pair are vision agentic coders but need reasoning-effort pinning. Both are blacklisted pending broader harness-level vetting with image payloads, not because they are incapable.
- **Harness-gated (not vision)**: `thinkingmachines/inkling` pair are general multimodal MoE, not vision models. The 403 `is only available on agentic harnesses` was from probing outside a harness. They could be whitelisted when called via a harness, but this repo keeps them blacklisted until a harness probe passes. They are not listed in the vision table.
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
