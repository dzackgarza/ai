---
name: model-selection
description: Use when selecting models for tasks — matches task complexity to model tier (S/A/B/C with +/− variants) based on SWE-bench scores from vava-nessa/free-coding-models.
---

# Model Selection

## Model Tier System (SWE-bench Verified)

From [`vava-nessa/free-coding-models`](https://github.com/vava-nessa/free-coding-models) and the official [SWE-bench Leaderboard](https://www.swebench.com/). Models are ranked by SWE-bench Verified scores (industry-standard benchmark for real GitHub issue resolution).

**Last Checked:** 2026-02-26

| Tier   | SWE-bench Score | Description              |
| ------ | --------------- | ------------------------ |
| **S+** | ≥70%            | Elite frontier coders    |
| **S**  | 60–70%          | Elite frontier coders    |
| **A+** | 50–60%          | Great alternatives       |
| **A**  | 40–50%          | Great alternatives       |
| **A−** | 35–40%          | Solid performers         |
| **B+** | 30–35%          | Solid performers         |
| **B**  | 20–30%          | Lightweight/older models |
| **C**  | <20%            | Lightweight/older models |

---

### S+ Tier (≥70%)

| Model                                 | SWE-bench |
| ------------------------------------- | --------- |
| GLM 5                                 | 77.8%     |
| Claude 4.5 Opus (high reasoning)      | 76.8%     |
| Kimi K2.5                             | 76.8%     |
| Gemini 3 Flash (high reasoning)       | 75.8%     |
| MiniMax M2.5 (high reasoning)         | 75.8%     |
| Claude Opus 4.6                       | 75.6%     |
| Step 3.5 Flash                        | 74.4%     |
| Claude 4.5 Opus medium (20251101)     | 74.4%     |
| Gemini 3 Pro Preview (2025-11-18)     | 74.2%     |
| MiniMax M2.1                          | 74.0%     |
| GLM 4.7                               | 73.8%     |
| DeepSeek V3.2                         | 73.1%     |
| GLM-5 (high reasoning)                | 72.8%     |
| GPT-5-2 (high reasoning)              | 72.8%     |
| GPT 5.2 Codex                         | 72.8%     |
| Devstral 2                            | 72.2%     |
| GPT-5.2 (2025-12-11) (high reasoning) | 71.8%     |
| Claude 4.5 Sonnet (high reasoning)    | 71.4%     |
| Kimi K2 Thinking                      | 71.3%     |
| Kimi K2.5 (high reasoning)            | 70.8%     |
| Claude 4.5 Sonnet (20250929)          | 70.6%     |
| Qwen3 Coder 480B                      | 70.6%     |
| DeepSeek V3.2 (high reasoning)        | 70.0%     |
| Qwen3 235B                            | 70.0%     |

**Turn capacity:** 300-500+ turns

---

### S Tier (60–70%)

| Model                                   | SWE-bench |
| --------------------------------------- | --------- |
| MiniMax M2                              | 69.4%     |
| GPT-5.2 (2025-12-11)                    | 69.0%     |
| DeepSeek V3.1 Terminus                  | 68.4%     |
| Qwen3 80B Thinking                      | 68.0%     |
| Qwen3.5 400B                            | 68.0%     |
| Claude 4 Opus (20250514)                | 67.6%     |
| Claude 4.5 Haiku (high reasoning)       | 66.6%     |
| GPT-5.1-codex (medium reasoning)        | 66.0%     |
| GPT-5.1 (2025-11-13) (medium reasoning) | 66.0%     |
| Kimi K2 Instruct                        | 65.8%     |
| Qwen3 80B Instruct                      | 65.0%     |
| GPT-5 (2025-08-07) (medium reasoning)   | 65.0%     |
| Claude 4 Sonnet (20250514)              | 64.93%    |
| Kimi K2 Thinking                        | 63.4%     |
| DeepSeek V3.1                           | 62.0%     |
| Llama 4 Maverick                        | 62.0%     |
| Minimax M2                              | 61.0%     |
| GPT OSS 120B                            | 60.0%     |
| DeepSeek V3.2 Reasoner                  | 60.0%     |

**Turn capacity:** 200-400 turns

---

### A+ Tier (50–60%)

| Model                                      | SWE-bench |
| ------------------------------------------ | --------- |
| GPT-5 mini (2025-08-07) (medium reasoning) | 59.8%     |
| o3 (2025-04-16)                            | 58.4%     |
| Mistral Large 675B                         | 58.0%     |
| Devstral small (2512)                      | 56.4%     |
| GPT-5 Mini                                 | 56.2%     |
| Nemotron Ultra 253B                        | 56.0%     |
| Qwen3-Coder 480B/A35B Instruct             | 55.4%     |
| GLM-4.6 (T=1)                              | 55.4%     |
| GLM-4.5 (2025-08-22)                       | 54.2%     |
| Devstral (2512)                            | 53.8%     |
| Gemini 2.5 Pro (2025-05-06)                | 53.6%     |
| Claude 3.7 Sonnet (20250219)               | 52.8%     |
| Colosseum 355B                             | 52.0%     |
| QwQ 32B                                    | 50.0%     |

**Turn capacity:** 100-200 turns

---

### A Tier (40–50%)

| Model                | SWE-bench |
| -------------------- | --------- |
| Nemotron Super 49B   | 49.0%     |
| Mistral Medium 3     | 48.0%     |
| Qwen2.5 Coder 32B    | 46.0%     |
| Magistral Small      | 45.0%     |
| o4-mini (2025-04-16) | 45.0%     |
| Llama 4 Scout        | 44.0%     |
| Llama 3.1 405B       | 44.0%     |
| Kimi K2 Instruct     | 43.8%     |
| Nemotron Nano 30B    | 43.0%     |
| R1 Distill 32B       | 43.9%     |
| GPT OSS 20B          | 42.0%     |

**Turn capacity:** 50-150 turns

---

### A− Tier (35–40%)

| Model                | SWE-bench |
| -------------------- | --------- |
| GPT-4.1 (2025-04-14) | 39.58%    |
| Llama 3.3 70B        | 39.5%     |
| Seed OSS 36B         | 38.0%     |
| R1 Distill 14B       | 37.7%     |
| Stockmark 100B       | 36.0%     |

**Turn capacity:** 30-80 turns

---

### B+ Tier (30–35%)

| Model                                      | SWE-bench |
| ------------------------------------------ | --------- |
| GPT-5 nano (2025-08-07) (medium reasoning) | 34.8%     |
| Ministral 14B                              | 34.0%     |
| Mixtral 8x22B                              | 32.0%     |
| Granite 34B Code                           | 30.0%     |

**Turn capacity:** 30-50 turns

---

### B Tier (20–30%)

| Model                         | SWE-bench |
| ----------------------------- | --------- |
| Gemini 2.5 Flash (2025-04-17) | 28.73%    |
| R1 Distill 8B                 | 28.2%     |
| gpt-oss-120b                  | 26.0%     |
| GPT-4.1-mini (2025-04-14)     | 23.94%    |
| R1 Distill 7B                 | 22.6%     |
| GPT-4o (2024-11-20)           | 21.62%    |
| Llama 4 Maverick Instruct     | 21.04%    |

**Turn capacity:** 20-40 turns

---

### C Tier (<20%)

| Model                      | SWE-bench |
| -------------------------- | --------- |
| Gemma 2 9B                 | 18.0%     |
| Phi 4 Mini                 | 14.0%     |
| Gemini 2.0 flash           | 13.52%    |
| Phi 3.5 Mini               | 12.0%     |
| Llama 4 Scout Instruct     | 9.06%     |
| Qwen2.5-Coder 32B Instruct | 9.0%      |

**Turn capacity:** 10-20 turns

---

## Related Skills

- **creating-subagents** — When to create subagents; subagent descriptions are agent-facing delegation instructions (Use when/Pass/Ask format)
- **prompt-engineering** — Writing effective prompts
- **subagent-delegation** — Managing subagent lifecycle and review cycles
- **test-guidelines** — Writing tests that verify model output
