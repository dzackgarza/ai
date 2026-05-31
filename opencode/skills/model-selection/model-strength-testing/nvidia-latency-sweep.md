# NVIDIA Model Shortlist

Direct API latency sweep against `https://integrate.api.nvidia.com/v1/chat/completions`
using `NVIDIA_API_KEY` from the environment.

Prompt shapes:

- `small`: `Reply with OK and nothing else.`

- `large`: real harness-shaped prompt built from
  `/home/dzack/pdf-extraction/.opencode/agents/zotero-steward.md` plus
  `/home/dzack/pdf-extraction/.agents/skills/zotero-pdf-extraction-maintainer/SKILL.md`
  and a final `reply with OK` instruction.

Prompt sizes:

- `small`: 31 chars

- `large`: 1,829 system chars + 31,631 user chars

Timeout policy:

- Each request was allowed a full 90s response window.

- Single sample per model/prompt pair.

## Shortlist

These 15 were tested after discarding obvious non-contenders: embeddings, rerankers,
vision/image/audio models, safety/guard models, tiny models, and stale utility models.

- `deepseek-ai/deepseek-r1-0528`

- `deepseek-ai/deepseek-v3.2`

- `deepseek-ai/deepseek-v4-flash`

- `deepseek-ai/deepseek-v4-pro`

- `meta/llama-3.1-405b-instruct`

- `minimaxai/minimax-m2.5`

- `minimaxai/minimax-m2.7`

- `mistralai/devstral-2-123b-instruct-2512`

- `mistralai/mistral-large-3-675b-instruct-2512`

- `moonshotai/kimi-k2.6`

- `nvidia/nemotron-4-340b-instruct`

- `qwen/qwen3-coder-480b-a35b-instruct`

- `qwen/qwen3-next-80b-a3b-thinking`

- `qwen/qwen3.5-397b-a17b`

- `z-ai/glm-5.1`

## Results

| Model | Small | Large | Status |
| --- | ---: | ---: | --- |
| `mistralai/mistral-large-3-675b-instruct-2512` | 0.621s | 0.923s | Fast and usable |
| `z-ai/glm-5.1` | 1.765s | 1.868s | Fast and usable |
| `moonshotai/kimi-k2.6` | 1.088s | 2.794s | Fast and usable |
| `qwen/qwen3.5-397b-a17b` | 37.323s | 8.599s | Usable, but erratic |
| `qwen/qwen3-coder-480b-a35b-instruct` | 9.833s | 10.181s | Usable, slower |
| `deepseek-ai/deepseek-v4-flash` | 90.222s timeout | 90.231s timeout | Too slow / hangs |
| `deepseek-ai/deepseek-v4-pro` | 90.164s timeout | 90.263s timeout | Too slow / hangs |
| `minimaxai/minimax-m2.7` | 90.202s timeout | 90.256s timeout | Too slow / hangs |
| `deepseek-ai/deepseek-r1-0528` | 0.156s 404 | 0.287s 404 | Listed, but unavailable |
| `deepseek-ai/deepseek-v3.2` | 0.242s 404 | 0.169s 404 | Listed, but unavailable |
| `meta/llama-3.1-405b-instruct` | 0.105s 404 | 0.129s 404 | Listed, but unavailable |
| `mistralai/devstral-2-123b-instruct-2512` | 0.108s 404 | 0.123s 404 | Listed, but unavailable |
| `nvidia/nemotron-4-340b-instruct` | 0.151s 404 | 0.143s 404 | Listed, but backend missing |
| `minimaxai/minimax-m2.5` | 0.143s 410 | 0.158s 410 | End-of-life |
| `qwen/qwen3-next-80b-a3b-thinking` | 0.132s 410 | 0.250s 410 | End-of-life |

## Recommendation

Best operational choices from this sweep:

1. `mistralai/mistral-large-3-675b-instruct-2512`

2. `z-ai/glm-5.1`

3. `moonshotai/kimi-k2.6`

If code-specialization matters more than raw latency:

1. `qwen/qwen3-coder-480b-a35b-instruct`

Not recommended for these cron jobs right now:

- `deepseek-ai/deepseek-v4-flash`

- `deepseek-ai/deepseek-v4-pro`

Reason:

- Both exceeded the 90s window even on the minimal prompt in this direct API test.

## Capability Signals

Latency and calibre are different questions.
The table above is runtime behavior through NVIDIA’s endpoint on this machine.
The signals below are benchmark/model-card evidence for relative capability.

| Model | Public capability signals | Read |
| --- | --- | --- |
| `z-ai/glm-5.1` | SWE-Bench Pro 58.4, Terminal-Bench 2.0 63.5, AIME 2026 95.3, GPQA-Diamond 86.2, HLE w/ tools 52.3, MCP-Atlas 71.8 | Strong all-around agent/coding model with good local latency |
| `moonshotai/kimi-k2.6` | Terminal-Bench 2.0 66.7, SWE-Bench Pro 58.6, SWE-Bench Verified 80.2, GPQA-Diamond 90.5, HLE w/ tools 54.0, BrowseComp 83.2 | Strongest combined public agent/coding numbers among the locally fast models here |
| `mistralai/mistral-large-3-675b-instruct-2512` | MMMLU 85.46, GPQA-Diamond 43.94, AMC 52.0, LiveCodeBench 34.41, General Prompts Surge 55 | Very fast in this sweep, but the public coding/agentic evidence is weaker than GLM/Kimi |
| `qwen/qwen3.5-397b-a17b` | MMLU-Pro 87.8, SuperGPQA 70.4, TAU2-Bench 86.7, MCP-Mark 46.1, SWE-Bench Verified 76.4, Terminal Bench 2 52.5 | High-capability multimodal agent model, but slower and more erratic locally |
| `qwen/qwen3-coder-480b-a35b-instruct` | Officially positioned as open-SOTA / Claude-Sonnet-comparable for agentic coding; HF eval pane currently shows SWE-Bench Pro 38.7 and TerminalBench 23.9 | Coding-specialized, but the directly visible public numbers are mixed |
| `deepseek-ai/deepseek-v4-pro` | GPQA Diamond 90.1, LiveCodeBench 93.5, Terminal Bench 2.0 67.9, SWE Verified 80.6, SWE Pro 55.4, HLE w/ tools 48.2 | Very strong on paper, but unusable here within a 90s response window |
| `deepseek-ai/deepseek-v4-flash` | GPQA Diamond 88.1, LiveCodeBench 91.6, Terminal Bench 2.0 56.9, SWE Verified 79.0, SWE Pro 52.6, HLE w/ tools 45.1 | Also strong on paper, also too slow here |

## Takeaway

If the requirement is “highest real capability while still returning promptly on this
machine through NVIDIA,” the best supported choices are:

1. `moonshotai/kimi-k2.6`

2. `z-ai/glm-5.1`

3. `qwen/qwen3.5-397b-a17b` or `qwen/qwen3-coder-480b-a35b-instruct`, depending on
   whether you want broader agent capability or code specialization

If the requirement were capability only, ignoring response latency,
`deepseek-ai/deepseek-v4-pro` would remain a serious contender by published benchmark
scores.
