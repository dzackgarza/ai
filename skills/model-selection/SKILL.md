---
name: model-selection
description: Use when selecting models for tasks — matches task complexity to model tier (S/A/B/C with +/− variants) based on SWE-bench scores from vava-nessa/free-coding-models.
---

# Model Selection

## Model Tier System (SWE-bench Verified)

From [`vava-nessa/free-coding-models`](https://github.com/vava-nessa/free-coding-models) — 134 models ranked by SWE-bench Verified scores (industry-standard benchmark for real GitHub issue resolution).

| Tier | SWE-bench Score | Description |
|------|-----------------|-------------|
| **S+** | ≥70% | Elite frontier coders |
| **S** | 60–70% | Elite frontier coders |
| **A+** | 50–60% | Great alternatives |
| **A** | 40–50% | Great alternatives |
| **A−** | 35–40% | Solid performers |
| **B+** | 30–35% | Solid performers |
| **B** | 20–30% | Lightweight/older models |
| **C** | <20% | Lightweight/older models |

---

### S+ Tier (≥70%)

| Model | SWE-bench |
|-------|-----------|
| GLM 5 | 77.8% |
| Kimi K2.5 | 76.8% |
| Step 3.5 Flash | 74.4% |
| MiniMax M2.1 | 74.0% |
| GLM 4.7 | 73.8% |
| DeepSeek V3.2 | 73.1% |
| Devstral 2 | 72.2% |
| Kimi K2 Thinking | 71.3% |
| Qwen3 Coder 480B | 70.6% |
| Qwen3 235B | 70.0% |

**Turn capacity:** 300-500+ turns

---

### S Tier (60–70%)

| Model | SWE-bench |
|-------|-----------|
| MiniMax M2 | 69.4% |
| DeepSeek V3.1 Terminus | 68.4% |
| Qwen3.5 400B | 68.0% |
| Qwen3 80B Thinking | 68.0% |
| Kimi K2 Instruct | 65.8% |
| Qwen3 80B Instruct | 65.0% |
| Llama 4 Maverick | 62.0% |
| DeepSeek V3.1 | 62.0% |
| GPT OSS 120B | 60.0% |

**Turn capacity:** 200-400 turns

---

### A+ Tier (50–60%)

**Turn capacity:** 100-200 turns

---

### A Tier (40–50%)

| Model | SWE-bench |
|-------|-----------|
| Qwen2.5 Coder 32B | 46.0% |

**Turn capacity:** 50-150 turns

---

### A− Tier (35–40%)

**Turn capacity:** 30-80 turns

---

### B+ Tier (30–35%)

**Turn capacity:** 30-50 turns

---

### B Tier (20–30%)

**Turn capacity:** 20-40 turns

---

### B− Tier (<20%, high end)

**Turn capacity:** 10-25 turns

---

### C Tier (<20%)

**Turn capacity:** 10-20 turns

---

### C− Tier

**Turn capacity:** 5-10 turns

---

## Related Skills

- **creating-subagents** — When to create subagents; subagent descriptions are agent-facing delegation instructions (Use when/Pass/Ask format)
- **prompt-engineering** — Writing effective prompts
- **subagent-delegation** — Managing subagent lifecycle and review cycles
- **test-guidelines** — Writing tests that verify model output

## Cross-References

| Skill | Application to Model Selection |
|-------|-------------------------------|
| `creating-subagents` | Match subagent tasks to model tiers; B/C-tier requires verification |
| `prompt-engineering` | Adapt prompt complexity to model tier |
| `subagent-delegation` | Review loops, checkpointing for B/C-tier output |
| `test-guidelines` | Verify B/C-tier output rigorously |
