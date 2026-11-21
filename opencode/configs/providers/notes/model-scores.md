# Whitelisted Model Scores

These scores rank every whitelisted model by general reasoning and task
performance on one 0–100 scale. They are judgment scores, not benchmark
results. Use them to choose a model for an agent and to order fallbacks.

- **Anchors:** the current frontier models of Anthropic and OpenAI, at
  maximum effort, are 100. On 2026-11-21 these are the newest Claude Fable
  and the newest OpenAI Astra. DeepSeek V4.1 Flash, the newest DeepSeek
  model, is exactly 50. When a new frontier model is released, it becomes
  the 100 anchor, and the other scores go down.
- **Scale:** the scale is linear between the two anchors. A 10-point gap is a difference you see on most tasks. A gap of
  3 points or less is noise.
- **Basis:** benchmark impressions from the 2026-11 provider review (Vals.ai
  Terminal-Bench 2.1, Terminal-Bench 4.0, SWE-bench Pro, GPQA, HLE), model
  generation and size, and vendor tier (Pro > base > Flash).
- **Stealth models:** these have no public benchmarks. Their scores are
  guesses. The table marks them with "stealth".
- **Snapshot:** 2026-11-21. Score each new whitelisted model against the
  anchor before an agent uses it. When a model leaves the whitelist, delete
  its row.

The same model can be served by more than one provider. It has one score.

| Score | Model | Provider ids | Note |
| ---: | --- | --- | --- |
| 100 | Frontier Anthropic and OpenAI | not whitelisted | anchor: newest Fable and newest Astra, maximum effort |
| 62 | Kimi K3.1 Pro | `nvidia/moonshotai/kimi-k3.1-pro`, `ollama-cloud/kimi-k3.1-pro` | strongest reasoning here; NVIDIA serves it slowly |
| 58 | Kimi K3 | `ollama-cloud/kimi-k3` | |
| 57 | GLM 5.3 | `ollama-cloud/glm-5.3` | strong agentic operation |
| 54 | DeepSeek V4 Pro (0813) | `ollama-cloud/deepseek-v4-pro:0813` | older generation, Pro tier |
| 53 | MiMo V2.6 Pro | `ollama-cloud/mimo-v2.6-pro` | |
| 52 | MiniMax M3 | `ollama-cloud/minimax-m3` | |
| 50 | DeepSeek V4.1 Flash | `ollama-cloud/deepseek-v4.1-flash`, `opencode/deepseek-v4.1-flash-free`, `tokenharbor/deepseek-v4.1-flash:free` | anchor |
| 49 | Step 5 Preview | `nvidia/stepfun-ai/step-5-preview` | preview release |
| 48 | MiniMax M3.1 Flash | `nvidia/minimaxai/minimax-m3.1-flash`, `ollama-cloud/minimax-m3.1-flash` | |
| 48 | Mistral Large 4 | `nvidia/mistralai/mistral-large-4-1t-a52b`, `ollama-cloud/mistral-large-4` | good general knowledge, weaker agentic operation |
| 47 | Kimi K2.7 Code | `ollama-cloud/kimi-k2.7-code` | coding specialist, older generation |
| 47 | LongCat 2.5 | `opencode/longcat-2.5-free` | |
| 46 | GLM 5.3 Flash | `nvidia/z-ai/glm-5.3-flash`, `ollama-cloud/glm-5.3-flash` | |
| 46 | MiMo V2.6 Flash | `ollama-cloud/mimo-v2.6-flash`, `opencode/mimo-v2.6-flash-free`, `tokenharbor/mimo-v2.6-flash:free` | |
| 45 | DeepSeek V4 Flash | `tokenharbor/deepseek-v4-flash:free` | superseded by V4.1 Flash |
| 45 | Beam | `ollama-cloud/beam`, `opencode/beam-free`, `kilo/reflection/beam-free` | thin evidence |
| 45 | Big Pickle | `opencode/big-pickle` | stealth; the compaction agent uses it |
| 44 | Glyph Cluster | `kilo/stealth/glyph-cluster` | stealth |
| 44 | Iceman | `opencode/iceman-free` | stealth |
| 43 | Tidepool Alpha | `opencode/tidepool-alpha-free` | stealth |
| 42 | Muse Spark Open | `ollama-cloud/muse-spark-open` | inconclusive benchmarks |
| 42 | Hunyuan HY4 Flash | `opencode/hy4-flash-free` | thin evidence |
| 42 | ERNIE 5.5 Flash Preview | `openrouter/baidu/ernie-5.5-flash-preview:free` | thin evidence |
| 40 | Ling 3.2 Flash | `openrouter/inclusionai/ling-3.2-flash:free` | thin evidence |
| 40 | MiMo V2.5 | `tokenharbor/mimo-v2.5:free` | previous generation |
| 40 | OpenRouter Free router | `openrouter/openrouter/free` | the routed model, so the quality, changes per call |
| 25 | Inkling 2 Small | `ollama-cloud/inkling-2-small` | Terminal-Bench 4.0: 12.63 (Sonnet 5.5: 64.14) |
| 30 | Particle 1 | `openrouter/particle-ai/particle-1:free` | thin evidence |
