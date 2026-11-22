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
| 100 | the newest Anthropic frontier model and the newest OpenAI frontier model, at maximum reasoning effort | on 2026-11-21: Claude Fable 5.2 (max) and GPT-6.2 Astra (max) |
| 50 | the newest DeepSeek model | on 2026-11-21: DeepSeek V4.1 Flash (1017) |

The anchors move. When Anthropic or OpenAI releases a new frontier model,
or DeepSeek releases a new model, the anchor changes to that model, and
every score is computed again from step 3 below. Scores are relative:
when the frontier improves, the same open model gets a lower score.

### The common scale

Different benchmarks rank models differently, and vendors report numbers
from their own harnesses. So every score starts from one independent board
that runs all models in one harness and covers both agentic and general
work: the **Artificial Analysis (AA) Intelligence Index**.

- Version used on 2026-11-21: **v4.3.2**, frozen 2026-10-27, 657 model
  configurations. Third-party mirror with the full table:
  <https://www.benchleader.com/benchmarks/aa_intelligence_index>. The
  current version is v5.0.1
  (<https://www.benchleader.com/benchmarks/aa_intelligence_index_v5>).
- v4.3.2 is used because the 50 anchor (DeepSeek V4.1 Flash) has a v4.3.2
  row and no visible v5.0.1 row. Values from two AA versions are never
  mixed in one formula: v5.0.1 is harder on open models (Kimi K3.1 Pro is
  55.1 on v4.3.2 and 46.5 on v5.0.1).
- Use the anchor model's highest configuration (for example `(max)`)
  when the board lists several.

### Steps to score a model

1. **Find the anchor values on the chosen AA version.**
   - `A50` = the AA value of the 50 anchor. On v4.3.2: DeepSeek V4.1
     Flash 1017 (max) = 45.1.
   - `A100` = the AA value of the 100 anchor. If the frontier model has
     no row on that version, convert it through a model that has rows on
     both versions. On 2026-11-21: Fable 5.2 (max) is 64.6 on v5.0.1 only.
     Opus 5.5 (max) is 59.1 on v5.0.1 and 57.6 on v4.3.2. So Fable 5.2 on
     v4.3.2 ≈ 64.6 × 57.6 / 59.1 ≈ 63. Record the conversion in the anchor
     row of the table.
2. **Compute the slope.** `k = 50 / (A100 − A50)`. On 2026-11-21:
   50 / (63 − 45.1) ≈ 2.79.
3. **Map each model that has a row on the same AA version.**
   `score = 50 + k × (AA − A50)`, rounded to an integer, and at least 0.
   The same line continues below the 50 anchor; do not compress the low
   end. One AA point is about 3 score points, so small AA gaps become
   large score gaps. Use the configuration the provider serves; if that is
   unknown, use the highest configuration.
4. **Bound a model that the visible table does not list.** If the board
   shows only the top rows (the mirror shows 60), a model that is missing
   scores below the last visible value. On 2026-11-21 that value was 41.8,
   which maps to 41. Choose a value below that bound from the evidence in
   step 5, and write "below 41.8 on AA v4.3.2" in the evidence cell.
5. **Use other evidence when there is no AA row.** Use the strongest
   evidence that exists, in this order, and name it in the evidence cell:
   1. An AA value on another AA version, converted as in step 1. If only
      a whole-number AA article value exists (for example "AA 30" in an
      AA article), use it with that version noted.
   2. The model's predecessor on the AA board, adjusted for the version
      step. For example, Ling 3.2 Flash uses Ling 3.1 Flash (43.9 → 47)
      and gets 48.
   3. Independent boards: Vals.ai (Vals Index, Terminal-Bench 2.1),
      Terminal-Bench 4.0, SWE-bench Pro. Compare with a model that has
      both that board's value and a score here. For example, Terminal-
      Bench 4.0: Sonnet 5.5 = 64.14.
   4. Vendor-reported benchmarks. These count for the least. When an
      independent result exists, it wins: Reflection reports Terminal-
      Bench 2.1 80.1 for Beam, but AA measured 30, so Beam is 10.
   5. Release facts: tier inside a series (Pro > base > Flash), generation,
      and whether the published checkpoint is a base model. A base
      checkpoint without instruction tuning (ERNIE 5.5 Flash on
      2026-11-21) gets a low score.
6. **Stealth and unknown models.** A model with no public identity and no
   benchmarks (OpenCode Zen and Kilo stealth models such as Big Pickle,
   Iceman, Tidepool Alpha, Glyph Cluster) gets the placeholder **40**, and
   its evidence cell says "stealth placeholder". When the vendor is named,
   or a benchmark appears, score it with steps 3 to 5.
7. **Routers.** A router that picks a different model per call (for
   example `openrouter/free`) gets about the score of the typical model it
   routes to, and its evidence cell says so.
8. **One score per model.** The same model on several providers has one
   row, and the row lists every provider id that serves it.

### Rounding and noise

Round each score to an integer. A gap of 3 points or less between two
models is noise; do not rank on it. A 10-point gap is a difference that
shows on most tasks.

### Display names

Each whitelisted model's display name in its provider fragment is
`[<score>] <Model>`, for example `"name": "[75] Kimi K3.1 Pro"` in `models`
of `nvidia.json`. The OpenCode model picker shows this name. When you
change a score, edit the `name` of that model in every provider fragment
in its row, with `jq`. Then rebuild the config and run `opencode reload`.

### When to update

- A model joins a whitelist: add or extend its row before an agent uses
  it.
- A model leaves every whitelist: delete its row. If it leaves one
  provider, delete only that provider id from its row.
- An anchor changes, or AA publishes a new version that contains the 50
  anchor: compute every score again from step 1, and change the snapshot
  date.
- New evidence appears for a model scored by steps 4 to 6: score it
  again.

Snapshot: 2026-11-21.

## Scores

| Score | Model | Provider ids | Evidence |
| ---: | --- | --- | --- |
| 100 | Frontier Anthropic and OpenAI | not whitelisted | anchor: Fable 5.2 (AA v5.0.1 64.6), GPT-6.2 Astra (62.1), maximum effort |
| 75 | Kimi K3.1 Pro | `nvidia/moonshotai/kimi-k3.1-pro`, `ollama-cloud/kimi-k3.1-pro`, `openmathos/moonshotai/kimi-k3.1-pro` | AA v4.3.2 55.1 (map: 78); AA v5.0.1 46.5, with the anchor below 36.6 (map: at least 68). NVIDIA serves it slowly |
| 53 | MiMo V2.6 Pro | `ollama-cloud/mimo-v2.6-pro` | AA v4.3.2 46.3 |
| 50 | DeepSeek V4.1 Flash | `ollama-cloud/deepseek-v4.1-flash`, `opencode/deepseek-v4.1-flash-free`, `openmathos/deepseek/deepseek-v4.1-flash`, `tokenharbor/deepseek-v4.1-flash:free` | anchor: AA v4.3.2 45.1 |
| 49 | GLM 5.3 | `ollama-cloud/glm-5.3`, `openmathos/z-ai/glm-5.3` | AA v4.3.2 44.8 |
| 48 | Ling 3.2 Flash | `openrouter/inclusionai/ling-3.2-flash:free` | predecessor Ling 3.1 Flash: AA v4.3.2 43.9 (map: 47) |
| 46 | Step 5 Preview | `nvidia/stepfun-ai/step-5-preview` | AA v4.3.2 43.7 |
| 45 | LongCat 2.5 | `opencode/longcat-2.5-free` | no AA row. Vendor: Terminal-Bench 4.0 38.5 (Sonnet 5.5: 64.14), Terminal-Bench 2.1 88.4, DeepSWE 64.6. Predecessor LongCat 2.0: AA 33 |
| 43 | MiniMax M3.1 Flash | `nvidia/minimaxai/minimax-m3.1-flash`, `ollama-cloud/minimax-m3.1-flash` | AA v4.3.2 42.7 |
| 41 | GLM 5.3 Flash | `nvidia/z-ai/glm-5.3-flash`, `ollama-cloud/glm-5.3-flash`, `openmathos/z-ai/glm-5.3-flash` | AA v4.3.2 41.8 |
| 40 | Hunyuan HY4 | `ollama-cloud/hy4` | no AA v4.3.2 row. AA v5.0.1 35, bridged to v4.3.2 through Kimi K3.1 Pro (55.1/46.5) gives 41.5; Vals Index 59.4% (#4). Full tier of the series whose Flash tier scores 30 |
| 40 | DeepSeek V4 Pro (0813) | `ollama-cloud/deepseek-v4-pro:0813` | not in the top 60 of AA v4.3.2 (below 41.8); an older generation than the anchor |
| 40 | Big Pickle | `opencode/big-pickle` | stealth placeholder; the compaction agent uses it |
| 40 | Glyph Cluster | `kilo/stealth/glyph-cluster` | stealth placeholder |
| 40 | Iceman | `opencode/iceman-free` | stealth placeholder |
| 40 | Tidepool Alpha | `opencode/tidepool-alpha-free` | stealth placeholder |
| 38 | MiniMax M3 | `ollama-cloud/minimax-m3` | below 41.8 on AA v4.3.2; predecessor of M3.1 Flash (43) |
| 38 | MiMo V2.6 Flash | `ollama-cloud/mimo-v2.6-flash`, `opencode/mimo-v2.6-flash-free`, `tokenharbor/mimo-v2.6-flash:free` | below 41.8 on AA v4.3.2; Flash tier of MiMo V2.6 Pro (53) |
| 35 | Mistral Large 4 | `nvidia/mistralai/mistral-large-4-1t-a52b`, `ollama-cloud/mistral-large-4`, `openmathos/mistralai/mistral-large-4-0` | below 41.8 on AA v4.3.2 |
| 35 | Particle 1 | `openrouter/particle-ai/particle-1:free` | no AA row. LLM Stats lists GPQA 90.4, MMLU 86.1, without a source |
| 33 | Muse Spark Open | `ollama-cloud/muse-spark-open`, `openmathos/meta/muse-spark-open` | AA v4.3 39 |
| 30 | Hunyuan HY4 Flash | `opencode/hy4-flash-free` | no AA row. Vals Index 50.78 (rank 33 of 39). Vendor: Terminal-Bench 4.0 19.2 |
| 30 | OpenRouter Free router | `openrouter/openrouter/free` | routes to a different free model per call |
| 25 | MiMo V2.5 | `tokenharbor/mimo-v2.5:free` | previous generation of MiMo V2.6 |
| 20 | ERNIE 5.5 Flash Preview | `openrouter/baidu/ernie-5.5-flash-preview:free` | no benchmarks found; the only published ERNIE 5.5 Flash checkpoint is a base model |
| 11 | Inkling 2 Small | `ollama-cloud/inkling-2-small`, `openmathos/thinkingmachines/inkling-2-small` | AA 31; Terminal-Bench 4.0 12.63 (Sonnet 5.5: 64.14) |
| 10 | Beam | `ollama-cloud/beam`, `opencode/beam-free`, `kilo/reflection/beam-free` | AA v4.3 30 (map: 8); AA hallucination rate 47%. Vendor claims (Terminal-Bench 2.1 80.1, SWE-bench Pro 66.1) are not confirmed |
