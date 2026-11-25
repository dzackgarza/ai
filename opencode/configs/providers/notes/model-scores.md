# Whitelisted Model Scores

These scores rank every whitelisted model by general reasoning and task
performance on one 0–100 scale. Use them to choose a model for an agent and
to order fallbacks.

## Methodology

### What a score measures

A score is the model's general reasoning and task performance, as one
number from 0 to 100. It covers the whole range of OpenCode agent work:
agentic operation in a terminal, coding, mathematics, research, reading
papers, and file and issue work. It does not include speed, price, context
length, or rate limits. A slow model (for example on NVIDIA NIM) keeps its
score.

### The anchors

Two fixed points define the scale. The user set both.

| Score | Anchor | Meaning |
| ---: | --- | --- |
| 100 | the newest Anthropic frontier model and the newest OpenAI frontier model, at maximum reasoning effort | on 2026-11-25: Claude Fable 5.2 (max) and GPT-6.2 Astra (max) |
| 50 | the newest DeepSeek model | on 2026-11-25: DeepSeek V4.1 Flash 1017 (max) |

The anchors move. When Anthropic or OpenAI releases a new frontier model,
or DeepSeek releases a new model, the anchor changes to that model, and
every score is computed again. Scores are relative: when the frontier
improves, the same open model gets a lower score.

### The common scale

Different benchmarks rank models differently, and vendors report numbers
from their own harnesses. So every score starts from one independent board
that runs all models in one harness and covers both agentic and general
work: the **Artificial Analysis (AA) Intelligence Index**, current
version.

- Version used on 2026-11-25: **v5.0.1**. Third-party mirror:
  <https://www.benchleader.com/benchmarks/aa_intelligence_index_v5>.
  The previous version v4.3.2 is at
  <https://www.benchleader.com/benchmarks/aa_intelligence_index>.
- The mirror page shows only the top rows, but its HTML carries every row
  in an embedded JSON payload. Each row has `name`, `effort`, and `value`.
  Read the payload, not the rendered table. On 2026-11-25 the payload had
  155 configurations for v5.0.1 and 632 for v4.3.2.
- Both anchors have v5.0.1 rows, so no anchor needs a conversion.

### Steps to score a model

1. **Read the anchor values.** `A50` = the 50 anchor on v5.0.1. `A100` =
   the mean of the two 100 anchors on v5.0.1. On 2026-11-25:
   `A50` = 32.40, `A100` = (64.77 + 62.19) / 2 = 63.48.
2. **Compute the slope.** `k = 50 / (A100 − A50)`. On 2026-11-25: 1.609.
3. **Map each model with a v5.0.1 row.**
   `score = 50 + k × (AA − A50)`, rounded to an integer, and at least 0.
   The same line continues below the 50 anchor. Use the configuration the
   provider serves; if that is unknown, use the highest configuration.
4. **Bridge a model with only a v4.3.2 row.** Fit a least-squares line
   `v5 = a × v4 + b` over every configuration that has rows on both
   versions, and map the bridged value with step 3. On 2026-11-25:
   `v5 = 1.132 × v4 − 12.63`, over 105 configurations. Do not use a ratio
   through one model: v5.0.1 compresses open models more than frontier
   models, and a single ratio carries that model's own error.
5. **Use other evidence when there is no AA row.** Use the strongest
   evidence that exists, in this order, and name it in the evidence cell:
   1. The model's predecessor or sibling tier on the AA board. A newer
      generation scores at least its predecessor unless independent
      evidence says otherwise. A Flash tier sits below its full tier by
      about the gap measured in other series on the same board (GLM 5.3 →
      Flash: 6; MiMo V2.6 Pro → Flash: 5).
   2. Independent boards: Vals.ai (Vals Index, Terminal-Bench 2.1),
      Terminal-Bench 4.0, SWE-bench Pro. Compare with models that have
      both that board's value and a score here.
   3. Vendor-reported benchmarks. These count for the least. When an
      independent result exists, it wins: Reflection reports
      Terminal-Bench 2.1 80.1 for Beam, but AA measured 17.66 on v5.0.1.
   4. OpenRouter usage, for models served there. See **OpenRouter usage
      signals** below.
   5. Release facts: tier inside a series, generation, and whether the
      published checkpoint is a base model.
6. **Stealth and unknown models.** A model with no public identity and no
   sourced benchmarks gets the placeholder **40**, and its evidence cell
   says "placeholder". When the vendor is named, or a benchmark appears,
   score it with steps 3 to 5.
7. **Routers.** A router that picks a different model per call (for
   example `openrouter/free`) gets about the score of the typical model it
   routes to, and its evidence cell says so.
8. **One score per model.** The same model on several providers has one
   row, and the row lists every provider id that serves it.

### OpenRouter usage signals

OpenRouter pages embed their data as JSON in the HTML. Read the payload,
not the rendered page:

- `https://openrouter.ai/<author>/<model>/apps`: the top 5 apps for the
  model, each with `total_tokens` and `categories` (for example
  `cli-agent`, `ide-extension`, `personal-agent`).
- `https://openrouter.ai/apps/<slug>`: the top 10 models in one app, as
  `ListItem` entries in order.

What the signals can show:

- **The model works in agent loops.** Sustained traffic from agentic
  coding apps (Hermes Agent, Claude Code, pi, OpenClaw, DeepSeek Harness)
  shows that the served model follows instructions and calls tools. This
  can refute a low score that rests on a release fact. ERNIE 5.5 Flash
  Preview carries about 470B tokens through agent apps other than Kilo
  Code, so the served model is not the base checkpoint.
- **A coarse ordering in one app.** Compare models inside the same agent
  app, not across apps. Use tokens from apps that do not promote the
  model.

What the signals cannot show:

- **A fine ranking.** Volume follows price, free availability, app
  defaults, and age more than quality. On 2026-11-25, Ling 3.1 Flash (46)
  had 18B tokens in Hermes Agent while MiMo V2.6 Flash (41) had 349B.
- **Promoted models.** An app that features a free model sends it most
  of its traffic. Kilo Code sent ERNIE 5.5 Flash Preview 3.9T of its
  4.4T tokens and ranks it above DeepSeek V4.1 Flash 1017.
- **Roleplay traffic.** Tokens from roleplay and companion apps
  (SillyTavern, Janitor AI, ISEKAI ZERO, Hello Minds) say nothing about
  agent work. Ignore them.

The `/rankings` page has daily rows with `total_tool_calls` and
`requests_with_tool_call_errors`, but on 2026-11-25 it held only the top
20 models and the tool fields were 0.

### Generations inside one vendor

The board does not order models by tier name. An older Pro can score
below a newer Flash: DeepSeek V4 Pro (max) is 23.06 on v5.0.1 and
DeepSeek V4.1 Flash 1017 (max) is 32.40. Generation dominates tier when
the board says so. Do not move a score to make tier names look ordered.

### Rounding and noise

Round each score to an integer. A gap of 3 points or less between two
models is noise; do not rank on it. A 10-point gap is a difference that
shows on most tasks.

### Display names

Each whitelisted model's display name in its provider fragment is
`[<score>] <Model>`, for example `"name": "[73] Kimi K3.1 Pro"` in `models`
of `nvidia.json`. The OpenCode model picker shows this name. When you
change a score, edit the `name` of that model in every provider fragment
in its row, with `jq`. Then rebuild the config and run `opencode reload`.

### When to update

- A model joins a whitelist: add or extend its row before an agent uses
  it.
- A model leaves every whitelist: delete its row. If it leaves one
  provider, delete only that provider id from its row.
- An anchor changes, or AA publishes a new version: compute every score
  again from step 1, and change the snapshot date.
- New evidence appears for a model scored by steps 5 to 7: score it
  again.

Snapshot: 2026-11-25.

## Scores

| Score | Model | Provider ids | Evidence |
| ---: | --- | --- | --- |
| 100 | Frontier Anthropic and OpenAI | not whitelisted | anchor: Fable 5.2 (max) 64.77, GPT-6.2 Astra (max) 62.19 |
| 73 | Kimi K3.1 Pro | `nvidia/moonshotai/kimi-k3.1-pro`, `ollama-cloud/kimi-k3.1-pro`, `openmathos/moonshotai/kimi-k3.1-pro` | AA v5.0.1 46.55. NVIDIA serves it slowly |
| 53 | Hunyuan HY4 | `ollama-cloud/hy4` | AA v5.0.1 34.57 |
| 50 | DeepSeek V4.1 Flash | `ollama-cloud/deepseek-v4.1-flash`, `opencode/deepseek-v4.1-flash-free`, `openmathos/deepseek/deepseek-v4.1-flash`, `tokenharbor/deepseek-v4.1-flash:free` | anchor: AA v5.0.1 32.40 (1017, max) |
| 49 | GLM 5.3 | `ollama-cloud/glm-5.3`, `openmathos/z-ai/glm-5.3` | AA v5.0.1 31.55 (max) |
| 47 | Inkling 2 Small | `ollama-cloud/inkling-2-small`, `openmathos/thinkingmachines/inkling-2-small` | AA v5.0.1 30.68 |
| 47 | Ling 3.2 Flash | `openrouter/inclusionai/ling-3.2-flash:free` | no AA row. Predecessor Ling 3.1 Flash: AA v5.0.1 29.65 (map: 46) |
| 46 | MiMo V2.6 Pro | `ollama-cloud/mimo-v2.6-pro` | AA v5.0.1 29.94 |
| 45 | MiniMax M3.1 Flash | `nvidia/minimaxai/minimax-m3.1-flash`, `ollama-cloud/minimax-m3.1-flash` | AA v5.0.1 29.06 |
| 44 | Step 5 Preview | `nvidia/stepfun-ai/step-5-preview` | AA v5.0.1 28.52 |
| 44 | Hunyuan HY4 Flash | `opencode/hy4-flash-free` | no AA row. Flash tier of Hunyuan HY4 (53), less the Flash gap of other series; Vals Index 50.78 against HY4 59.4 |
| 43 | GLM 5.3 Flash | `nvidia/z-ai/glm-5.3-flash`, `ollama-cloud/glm-5.3-flash`, `openmathos/z-ai/glm-5.3-flash` | AA v5.0.1 27.74 (max) |
| 42 | Particle 1 | `openrouter/particle-ai/particle-1:free` | no AA row. OpenRouter: 96B tokens, 75% from agentic coding apps (Kilo Code, DeepSeek Harness, Hermes Agent, pi, Claude Code); #7 in Kilo Code. Usage like Ling 3.1/3.2 Flash (46–47) in the same apps. LLM Stats lists GPQA 90.4 and MMLU 86.1 without a source |
| 41 | MiMo V2.6 Flash | `ollama-cloud/mimo-v2.6-flash`, `opencode/mimo-v2.6-flash-free`, `tokenharbor/mimo-v2.6-flash:free` | AA v5.0.1 26.83 |
| 40 | Mistral Large 4 | `nvidia/mistralai/mistral-large-4-1t-a52b`, `ollama-cloud/mistral-large-4`, `openmathos/mistralai/mistral-large-4-0` | AA v5.0.1 26.12 (high) |
| 40 | Big Pickle | `opencode/big-pickle` | placeholder (stealth); the compaction agent uses it |
| 40 | Glyph Cluster | `kilo/stealth/glyph-cluster` | placeholder (stealth) |
| 40 | Iceman | `opencode/iceman-free` | placeholder (stealth) |
| 40 | Tidepool Alpha | `opencode/tidepool-alpha-free` | placeholder (stealth) |
| 38 | Muse Spark Open | `ollama-cloud/muse-spark-open`, `openmathos/meta/muse-spark-open` | AA v5.0.1 24.88 (xhigh) |
| 35 | DeepSeek V4 Pro (0813) | `ollama-cloud/deepseek-v4-pro:0813` | AA v5.0.1 23.06 (DeepSeek V4 Pro, max). Older generation than the anchor |
| 35 | LongCat 2.5 | `opencode/longcat-2.5-free` | no AA row. Predecessor LongCat 2.0: AA v4.3.2 19.11, bridged 9.0 (map: 12). Vendor: Terminal-Bench 4.0 38.5 (Sonnet 5.5: 64.14). One generation step on this board has added up to about 38 points (DeepSeek V4 Flash 0420 → V4.1 Flash 1017) |
| 35 | ERNIE 5.5 Flash Preview | `openrouter/baidu/ernie-5.5-flash-preview:free` | no AA row. OpenRouter: 4.4T tokens, 95% from agentic coding apps; about 470B outside Kilo Code, which promotes it (Hermes Agent 186B against MiMo V2.6 Flash 349B and Ling 3.2 Flash 24B). The served model works in agent loops, so it is not the base checkpoint. Predecessor ERNIE 5.0 (thinking): AA v4.3.2 14.26, bridged 3.5 (map: 4) |
| 29 | MiniMax M3 | `ollama-cloud/minimax-m3` | AA v5.0.1 19.05 |
| 26 | Beam | `ollama-cloud/beam`, `opencode/beam-free`, `kilo/reflection/beam-free` | AA v5.0.1 17.66. Vendor claims (Terminal-Bench 2.1 80.1, SWE-bench Pro 66.1) are not confirmed |
| 21 | OpenRouter Free router | `openrouter/openrouter/free` | picks at random from the 11 OpenRouter free models. Mean of their scores: Ling 3.2 Flash 47, Particle 1 42, Flint 40 (placeholder), ERNIE 5.5 Flash Preview 35; on AA v5.0.1 Nemotron 3.5 Super VL 20, Nemotron 3 Ultra 17, LFM3 1.7B 8, Nemotron 3.5 Lightning 7, Gemma 4 31B 5; bridged from v4.3.2 Gemma 4 26B A4B 8, Nemotron 3 Nano Omni 0 |
| 17 | MiMo V2.5 | `tokenharbor/mimo-v2.5:free` | AA v4.3.2 21.82, bridged 12.1 |
