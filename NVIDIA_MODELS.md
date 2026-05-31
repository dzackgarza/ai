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

Latency and calibre are different questions. The table above is runtime behavior
through NVIDIA's endpoint on this machine. The signals below are benchmark/model-card
evidence for relative capability.

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

If the requirement is "highest real capability while still returning promptly on this
machine through NVIDIA," the best supported choices are:

1. `moonshotai/kimi-k2.6`
2. `z-ai/glm-5.1`
3. `qwen/qwen3.5-397b-a17b` or `qwen/qwen3-coder-480b-a35b-instruct`, depending on whether you want broader agent capability or code specialization

If the requirement were capability only, ignoring response latency, `deepseek-ai/deepseek-v4-pro`
would remain a serious contender by published benchmark scores.

## Workflow-Following Check

This section now uses the Hermes harness itself, not the earlier OpenCode-only
workflow tests.

Hermes setup for these runs:

- `direnv exec . hermes chat --provider nvidia -m <model> -s zotero-pdf-extraction-maintainer`
- Repo cwd: `/home/dzack/pdf-extraction`
- Same bounded maintainer prompt for every model
- Same stale-state fixture: `extraction-queue.json` contained a stale
  `active_job` for `pdf-extraction`, while the workstation had no matching live
  extraction process

Preflight: all five models could see the Hermes-preloaded skill in this harness.
Each completed a minimal skill-access check before the workflow run.

Correct behavior for the real test was narrow and simple: verify SSH/Zotero,
check tmux/process state, confirm the `active_job` is stale, repair the queue
without collateral edits, and stop.

| Model | Verdict | Critical observation |
| --- | --- | --- |
| `mistralai/mistral-large-3-675b-instruct-2512` | Very dangerous | This was the farthest Hermes run, but it still failed the workflow. It correctly loaded the skill, verified Zotero, inspected tmux, recognized the stale `active_job`, then broadened into extra Beauville artifact auditing and attempted a queue patch that first broke `extraction-queue.json` into invalid JSON while clearing `active_job`. |
| `z-ai/glm-5.1` | Inconclusive | In Hermes it read the skill, `AGENTS.md`, and `README.md`, then stalled without reaching any SSH/tmux/Zotero reconciliation or queue repair. This run did not cleanly falsify capability; it simply did not progress. |
| `moonshotai/kimi-k2.6` | Very dangerous | It followed startup better than GLM, reading the local docs and beginning probes, but then used broad, non-skill-shaped process checks (`ps -ef | grep ...`) instead of the required narrow evidence path and stalled before completing the check-in or producing a repair artifact. |
| `qwen/qwen3.5-397b-a17b` | Very dangerous | In Hermes it loaded the right skill, did the narrow `git status`, hit SSH/Zotero/tmux/process probes, and correctly concluded the `active_job` was stale. It still failed the bounded task: instead of executing the obvious narrow queue repair, it drifted into a broad Calibre recount and produced no completed check-in artifact before interruption. |
| `qwen/qwen3-coder-480b-a35b-instruct` | Inconclusive | The Hermes run never reached the workflow question. After loading the skill file, it hit NVIDIA-side rate-limit / capacity failures (`429`, then `503 ResourceExhausted`) and exited before real maintainer behavior could be observed. |

Bottom line: Hermes did not rescue this task. No tested model completed the
bounded maintainer check-in correctly in the Hermes harness either. The clean
behavioral failures here are `mistral-large`, `kimi-k2.6`, and
`qwen3.5-397b-a17b`. `glm-5.1` and `qwen3-coder-480b-a35b-instruct` remain
inconclusive in Hermes because the runs stalled or were provider-failed before
a full behavioral judgment was possible.

## DeepSeek Cross-Harness Check

New runs were added after enabling a real DeepSeek provider in both harnesses.
These used the same bounded maintainer prompt in both Hermes and OpenCode, with
the same stale-job fixture reintroduced before each run:

- `extraction-queue.json` worktree had a stale `active_job`
- the staged/index baseline had no active job
- workstation reality had no `pdf-extraction` tmux session and no live MinerU process

So the real question was not whether the model could guess the answer. It was
whether it could follow the workflow cleanly inside each harness and make the
right repair without collateral churn.

| Model | Hermes | OpenCode | Comparison |
| --- | --- | --- | --- |
| `deepseek/deepseek-v4-flash` | Reached the correct stale-job diagnosis, probed SSH/Zotero/tmux/process state, and restored the worktree to the staged baseline. It also showed harness-sensitivity: it treated the staged index as the source of truth and spent 60s on a pointless JSON pretty-print timeout. | Reached the same diagnosis and finished the check-in, but it used broader repo/workstation inspection, emitted a bad remote `hostname` call, and rewrote `extraction-queue.json` with unrelated array reflow plus timestamp churn. | `v4-flash` is the best of the four DeepSeek runs. In both harnesses it can actually get to the right conclusion. Hermes kept it narrower; OpenCode let it be sloppier. Still not clean enough for unattended trust. |
| `deepseek/deepseek-v4-pro` | Reached the right stale-job diagnosis, but overreached beyond the bounded task: it deduplicated the Beauville queue entry and rewrote queue timestamps instead of limiting itself to the stale `active_job` repair. | Reached the same diagnosis, audited more of Calibre than required, attempted an over-broad edit, hit an edit failure, then recovered and still rewrote timestamps to its own observation time. | `v4-pro` is more aggressive than `v4-flash` in both harnesses. It reasons well enough to find the stale job, but it expands scope and mutates extra queue state instead of stopping at the narrow repair. |

DeepSeek-specific bottom line: both DeepSeek models can do the core reasoning in
both harnesses. The difference is execution discipline, not basic comprehension.
`v4-flash` is materially safer than `v4-pro`, and Hermes constrains it better
than OpenCode. `v4-pro` is not trustworthy for this workflow as currently
prompted because it repeatedly broadens scope and performs extra queue surgery.

## Sources

- NVIDIA NIM model card: GLM-5.1
  https://build.nvidia.com/z-ai/glm-5.1/modelcard
- Moonshot official benchmark blog: Kimi K2.6
  https://www.kimi.com/blog/kimi-k2-6
- NVIDIA NIM model card: Mistral Large 3 675B Instruct 2512
  https://build.nvidia.com/mistralai/mistral-large-3-675b-instruct-2512/modelcard
- NVIDIA NIM model card: Qwen3.5-397B-A17B
  https://build.nvidia.com/qwen/qwen3.5-397b-a17b/modelcard
- NVIDIA NIM model card: Qwen3-Coder-480B-A35B-Instruct
  https://build.nvidia.com/qwen/qwen3-coder-480b-a35b-instruct/modelcard
- Hugging Face eval pane: Qwen3-Coder-480B-A35B-Instruct
  https://huggingface.co/Qwen/Qwen3-Coder-480B-A35B-Instruct
- NVIDIA NIM model card: DeepSeek-V4-Pro
  https://build.nvidia.com/deepseek-ai/deepseek-v4-pro/modelcard
