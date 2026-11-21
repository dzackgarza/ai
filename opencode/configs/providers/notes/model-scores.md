# Whitelisted Model Scores

These scores rank every whitelisted model by general reasoning and task
performance on one 0–100 scale. Use them to choose a model for an agent and
to order fallbacks.

## Scale

- **Anchors:** the current frontier models of Anthropic and OpenAI, at
  maximum effort, are 100. On 2026-11-21 these are Claude Fable 5.2 and
  GPT-6.2 Astra. DeepSeek V4.1 Flash, the newest DeepSeek model, is
  exactly 50. When a new frontier model is released, it becomes the 100
  anchor, and the other scores go down.
- **Primary evidence:** the Artificial Analysis (AA) Intelligence Index
  v4.3.2 (frozen 2026-10-27,
  [table](https://www.benchleader.com/benchmarks/aa_intelligence_index)).
  AA runs every model in one harness, and the index covers both agentic
  operation and general reasoning. On it, DeepSeek V4.1 Flash 1017 (max)
  is 45.1. The frontier is about 63: Fable 5.2 is only on v5.0.1 (64.6),
  and Opus 5.5 (max) scores 59.1 on v5.0.1 and 57.6 on v4.3.2, so Fable
  5.2 converts to about 63 on v4.3.2.
- **Map:** score = 50 + 2.79 × (AA − 45.1), rounded, at least 0. The map is
  linear through the two anchors, and a model below the anchor continues
  on the same line. One AA point is about 3 score points.
- **Other evidence:** when a model has no v4.3.2 row, its score comes from
  the evidence in its row. A vendor-reported benchmark counts for less than
  an AA result. For example, Reflection reports 80.1 on Terminal-Bench 2.1
  for Beam, but AA measured Beam at 30.
- **No evidence:** stealth models have no public identity or benchmarks.
  Their score is 40, a placeholder, until a live trial or a published
  identity gives evidence.
- **Noise:** a gap of 3 points or less is noise. A 10-point gap is a
  difference you see on most tasks.
- **Snapshot:** 2026-11-21. Score each new whitelisted model before an
  agent uses it. When a model leaves the whitelist, delete its row.

The same model can be served by more than one provider. It has one score.

Each whitelisted model's display name in its provider fragment is
`[<score>] <Model>`, with the score and model name from this table, for
example `"name": "[75] Kimi K3.1 Pro"` in `models` of `nvidia.json`. The
OpenCode model picker shows this name. When a score or a whitelist changes,
change the table and the fragment `name` together.

## Scores

| Score | Model | Provider ids | Evidence |
| ---: | --- | --- | --- |
| 100 | Frontier Anthropic and OpenAI | not whitelisted | anchor: Fable 5.2 (AA v5.0.1 64.6), GPT-6.2 Astra (62.1), maximum effort |
| 75 | Kimi K3.1 Pro | `nvidia/moonshotai/kimi-k3.1-pro`, `ollama-cloud/kimi-k3.1-pro` | AA v4.3.2 55.1 (map: 78); AA v5.0.1 46.5, with the anchor below 36.6 (map: at least 68). NVIDIA serves it slowly |
| 53 | MiMo V2.6 Pro | `ollama-cloud/mimo-v2.6-pro` | AA v4.3.2 46.3 |
| 50 | DeepSeek V4.1 Flash | `ollama-cloud/deepseek-v4.1-flash`, `opencode/deepseek-v4.1-flash-free`, `tokenharbor/deepseek-v4.1-flash:free` | anchor: AA v4.3.2 45.1 |
| 49 | GLM 5.3 | `ollama-cloud/glm-5.3` | AA v4.3.2 44.8 |
| 48 | Ling 3.2 Flash | `openrouter/inclusionai/ling-3.2-flash:free` | predecessor Ling 3.1 Flash: AA v4.3.2 43.9 (map: 47) |
| 46 | Step 5 Preview | `nvidia/stepfun-ai/step-5-preview` | AA v4.3.2 43.7 |
| 45 | LongCat 2.5 | `opencode/longcat-2.5-free` | no AA row. Vendor: Terminal-Bench 4.0 38.5 (Sonnet 5.5: 64.14), Terminal-Bench 2.1 88.4, DeepSWE 64.6. Predecessor LongCat 2.0: AA 33 |
| 43 | MiniMax M3.1 Flash | `nvidia/minimaxai/minimax-m3.1-flash`, `ollama-cloud/minimax-m3.1-flash` | AA v4.3.2 42.7 |
| 41 | GLM 5.3 Flash | `nvidia/z-ai/glm-5.3-flash`, `ollama-cloud/glm-5.3-flash` | AA v4.3.2 41.8 |
| 40 | DeepSeek V4 Pro (0813) | `ollama-cloud/deepseek-v4-pro:0813` | not in the top 60 of AA v4.3.2 (below 41.8); an older generation than the anchor |
| 40 | Big Pickle | `opencode/big-pickle` | stealth placeholder; the compaction agent uses it |
| 40 | Glyph Cluster | `kilo/stealth/glyph-cluster` | stealth placeholder |
| 40 | Iceman | `opencode/iceman-free` | stealth placeholder |
| 40 | Tidepool Alpha | `opencode/tidepool-alpha-free` | stealth placeholder |
| 38 | MiniMax M3 | `ollama-cloud/minimax-m3` | below 41.8 on AA v4.3.2; predecessor of M3.1 Flash (43) |
| 38 | MiMo V2.6 Flash | `ollama-cloud/mimo-v2.6-flash`, `opencode/mimo-v2.6-flash-free`, `tokenharbor/mimo-v2.6-flash:free` | below 41.8 on AA v4.3.2; Flash tier of MiMo V2.6 Pro (53) |
| 35 | Mistral Large 4 | `nvidia/mistralai/mistral-large-4-1t-a52b`, `ollama-cloud/mistral-large-4` | below 41.8 on AA v4.3.2 |
| 35 | Particle 1 | `openrouter/particle-ai/particle-1:free` | no AA row. LLM Stats lists GPQA 90.4, MMLU 86.1, without a source |
| 33 | Muse Spark Open | `ollama-cloud/muse-spark-open` | AA v4.3 39 |
| 30 | Hunyuan HY4 Flash | `opencode/hy4-flash-free` | no AA row. Vals Index 50.78 (rank 33 of 39). Vendor: Terminal-Bench 4.0 19.2 |
| 30 | OpenRouter Free router | `openrouter/openrouter/free` | routes to a different free model per call |
| 25 | MiMo V2.5 | `tokenharbor/mimo-v2.5:free` | previous generation of MiMo V2.6 |
| 20 | ERNIE 5.5 Flash Preview | `openrouter/baidu/ernie-5.5-flash-preview:free` | no benchmarks found; the only published ERNIE 5.5 Flash checkpoint is a base model |
| 11 | Inkling 2 Small | `ollama-cloud/inkling-2-small` | AA 31; Terminal-Bench 4.0 12.63 (Sonnet 5.5: 64.14) |
| 10 | Beam | `ollama-cloud/beam`, `opencode/beam-free`, `kilo/reflection/beam-free` | AA v4.3 30 (map: 8); AA hallucination rate 47%. Vendor claims (Terminal-Bench 2.1 80.1, SWE-bench Pro 66.1) are not confirmed |
