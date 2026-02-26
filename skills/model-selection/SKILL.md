---
name: model-selection
description: Use when selecting models for tasks — matches task complexity to model tier (S/A/B/C with +/− variants) based on SWE-bench scores from vava-nessa/free-coding-models.
---

# Model Selection

## Model Tier System (SWE-bench Verified)

From [`vava-nessa/free-coding-models`](https://github.com/vava-nessa/free-coding-models) — 134 models ranked by SWE-bench Verified scores (industry-standard benchmark for real GitHub issue resolution).

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

| Model            | SWE-bench |
| ---------------- | --------- |
| GLM 5            | 77.8%     |
| Kimi K2.5        | 76.8%     |
| Step 3.5 Flash   | 74.4%     |
| MiniMax M2.1     | 74.0%     |
| GLM 4.7          | 73.8%     |
| DeepSeek V3.2    | 73.1%     |
| Devstral 2       | 72.2%     |
| Kimi K2 Thinking | 71.3%     |
| Qwen3 Coder 480B | 70.6%     |
| Qwen3 235B       | 70.0%     |

**Turn capacity:** 300-500+ turns

---

### S Tier (60–70%)

| Model                  | SWE-bench |
| ---------------------- | --------- |
| MiniMax M2             | 69.4%     |
| DeepSeek V3.1 Terminus | 68.4%     |
| Qwen3 80B Thinking     | 68.0%     |
| Qwen3.5 400B           | 68.0%     |
| Kimi K2 Instruct       | 65.8%     |
| Qwen3 80B Instruct     | 65.0%     |
| DeepSeek V3.1          | 62.0%     |
| Llama 4 Maverick       | 62.0%     |
| GPT OSS 120B           | 60.0%     |

**Turn capacity:** 200-400 turns

---

### A+ Tier (50–60%)

| Model               | SWE-bench |
| ------------------- | --------- |
| Mistral Large 675B  | 58.0%     |
| Nemotron Ultra 253B | 56.0%     |
| Colosseum 355B      | 52.0%     |
| QwQ 32B             | 50.0%     |

**Turn capacity:** 100-200 turns

---

### A Tier (40–50%)

| Model              | SWE-bench |
| ------------------ | --------- |
| Nemotron Super 49B | 49.0%     |
| Mistral Medium 3   | 48.0%     |
| Qwen2.5 Coder 32B  | 46.0%     |
| Magistral Small    | 45.0%     |
| Llama 4 Scout      | 44.0%     |
| Llama 3.1 405B     | 44.0%     |
| Nemotron Nano 30B  | 43.0%     |
| R1 Distill 32B     | 43.9%     |
| GPT OSS 20B        | 42.0%     |

**Turn capacity:** 50-150 turns

---

### A− Tier (35–40%)

| Model          | SWE-bench |
| -------------- | --------- |
| Llama 3.3 70B  | 39.5%     |
| Seed OSS 36B   | 38.0%     |
| R1 Distill 14B | 37.7%     |
| Stockmark 100B | 36.0%     |

**Turn capacity:** 30-80 turns

---

### B+ Tier (30–35%)

| Model            | SWE-bench |
| ---------------- | --------- |
| Ministral 14B    | 34.0%     |
| Mixtral 8x22B    | 32.0%     |
| Granite 34B Code | 30.0%     |

**Turn capacity:** 30-50 turns

---

### B Tier (20–30%)

| Model         | SWE-bench |
| ------------- | --------- |
| R1 Distill 8B | 28.2%     |
| R1 Distill 7B | 22.6%     |

**Turn capacity:** 20-40 turns

---

### C Tier (<20%)

| Model        | SWE-bench |
| ------------ | --------- |
| Gemma 2 9B   | 18.0%     |
| Phi 4 Mini   | 14.0%     |
| Phi 3.5 Mini | 12.0%     |

**Turn capacity:** 10-20 turns

---

## Related Skills

- **creating-subagents** — When to create subagents; subagent descriptions are agent-facing delegation instructions (Use when/Pass/Ask format)
- **prompt-engineering** — Writing effective prompts
- **subagent-delegation** — Managing subagent lifecycle and review cycles
- **test-guidelines** — Writing tests that verify model output
