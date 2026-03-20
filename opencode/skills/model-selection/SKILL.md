---
name: model-selection
description: Use when selecting models for tasks — matches task complexity to model tier (S/A/B/C with +/− variants) based on APEX Testing ELO scores (real-world agentic coding benchmark).
---

# Model Selection

## Model Tier System (APEX Testing)

From [APEX Testing](https://www.apex-testing.org/) — an agentic coding benchmark that measures real-world task completion, not benchmark performance on pre-solved GitHub issues. Uses ELO ratings from actual coding tasks performed by the models.

**Why APEX over SWE-bench:** SWE-bench rates Gemini Flash 3 nearly as high as Opus 4.6 (75.8% vs 75.6%). APEX shows the actual gap: Opus 4.6 at 1878 ELO vs Gemini far lower. SWE-bench tests on issues that have already been solved — APEX tests actual agentic capability.

**Last Checked:** 2026-03-01

| Tier   | APEX ELO  | Description                   |
| ------ | --------- | ----------------------------- |
| **S+** | ≥1870     | Elite frontier coders         |
| **S**  | 1800–1870 | Strong frontier coders        |
| **A+** | 1750–1800 | Excellent alternatives        |
| **A**  | 1700–1750 | Solid performers              |
| **A−** | 1650–1700 | Good for targeted tasks       |
| **B+** | 1600–1650 | Lightweight/constrained infra |
| **B**  | 1500–1600 | Code completion only          |
| **C**  | <1500     | Minimal agentic capability    |

---

### S+ Tier (≥1870)

| Model             | APEX ELO |
| ----------------- | -------- |
| Claude Opus 4.6   | 1878     |
| Claude Sonnet 4.6 | 1874     |
| GPT 5.2           | 1829     |
| Claude Opus 4.5   | 1815     |
| GPT 5.3 Codex     | 1812     |

**Turn capacity:** 300-500+ turns

---

### S Tier (1800–1870)

| Model                | APEX ELO |
| -------------------- | -------- |
| Claude 4.5 Sonnet    | ~1800    |
| GPT 5.1 Codex        | ~1790    |
| Gemini 3 Pro Preview | ~1780    |
| Claude 4 Opus        | ~1770    |
| DeepSeek V3.2        | ~1760    |
| Qwen3 Coder 480B     | ~1750    |

**Turn capacity:** 200-400 turns

---

### A+ Tier (1750–1800)

| Model                        | APEX ELO |
| ---------------------------- | -------- |
| Gemini 3 Flash (high reason) | ~1745    |
| MiniMax M2.1                 | ~1740    |
| GPT-5.1                      | ~1735    |
| Kimi K2.5                    | ~1720    |
| GLM 5                        | ~1710    |

**Turn capacity:** 100-200 turns

---

### A Tier (1700–1750)

| Model           | APEX ELO |
| --------------- | -------- |
| Claude 4 Haiku  | ~1700    |
| Gemini 2.5 Pro  | ~1695    |
| DeepSeek V3.1   | ~1680    |
| Mistral Large 3 | ~1670    |
| Qwen3.5 400B    | ~1660    |

**Turn capacity:** 50-150 turns

---

### A− Tier (1650–1700)

| Model            | APEX ELO |
| ---------------- | -------- |
| Gemini 2.5 Flash | ~1650    |
| Llama 4 Maverick | ~1640    |
| Nemotron Ultra   | ~1630    |
| GPT-4.1          | ~1620    |

**Turn capacity:** 30-80 turns

---

### B+ Tier (1600–1650)

| Model         | APEX ELO |
| ------------- | -------- |
| Devstral 2    | ~1600    |
| Gemma 3       | ~1590    |
| Mixtral 8x22B | ~1580    |
| Llama 3.3 70B | ~1570    |

**Turn capacity:** 30-50 turns

---

### B Tier (1500–1600)

| Model             | APEX ELO |
| ----------------- | -------- |
| Qwen2.5 Coder 32B | ~1550    |
| R1 Distill        | ~1530    |
| Phi 4             | ~1510    |
| Gemma 2 27B       | ~1500    |

**Turn capacity:** 20-40 turns

---

### C Tier (<1500)

| Model            | APEX ELO |
| ---------------- | -------- |
| Gemini 2.0 Flash | ~1450    |
| Llama 4 Scout    | ~1400    |
| Phi 3.5          | ~1350    |
| Qwen2.5 7B       | ~1300    |

**Turn capacity:** 10-20 turns

---

## Key Differences from SWE-bench

| Aspect            | SWE-bench                            | APEX Testing                       |
| ----------------- | ------------------------------------ | ---------------------------------- |
| **What it tests** | Pre-solved GitHub issues             | Real agentic task completion       |
| **Problem**       | Models see solutions during training | Tests actual working capability    |
| **Example**       | Gemini Flash 3: 75.8%                | Gemini Flash 3: far below Opus 4.6 |
| **Realism**       | Artificial                           | Reflects real user experience      |

---

## Usage Guidelines

- **S+ tier:** Complex refactors, multi-file architectural changes, debugging across subsystems
- **S tier:** Significant features, complex bug fixes, substantial code generation
- **A+ tier:** Targeted features, moderate refactoring, well-scoped tasks
- **A tier:** Bug fixes, code reviews, smaller features
- **A−/B+ tier:** Simple code generation, documentation, smaller tasks
- **B/C tier:** Code completion, simple scripts only

---

## Summarization Model Guidance

When the task is summarization (papers, long markdown, search snippets, technical reports), prioritize:

- **Context window headroom:** target at least 2x expected prompt size
- **Stability under load:** prefer models with fewer transient 429s in your provider
- **Output consistency:** prefer models that return direct `content` (not reasoning-only partials)
- **Cost tier constraints:** if free-tier only, pin a concrete free model and live-ping it before use

Recommended process:

1. List candidate models for your provider/tier.
2. Filter by context limit and pricing constraints.
3. Live-ping each candidate with a trivial prompt.
4. Run a small summarization smoke test.
5. Run one realistic long-context test.
6. Pin the winner in config (avoid router aliases for repeatable behavior).

---

## Provider Model Inventory Script

Use `~/ai/opencode/skills/model-selection/scripts/fetch_provider_models.py` when you need a current provider-by-provider model inventory (cross-referenced with `models.dev`) from keys present in `~/.envrc`.
For invocation and options, use the script help: `python3 ~/ai/opencode/skills/model-selection/scripts/fetch_provider_models.py --help`.

---

## Local Models

When considering local/deployed models (Ollama, llama.cpp, etc.), use **[llmfit](https://github.com/sweepai/llmfit)** to check compatibility and feasibility before committing to a model. `llmfit` benchmarks models against your hardware and estimates:

- **Throughput** (tokens/second)
- **Memory requirements**
- **Time to first token** latency
- **Whether the model can run at all** on your setup

Don't guess — run `llmfit` to verify a local model will actually work for agentic tasks.

---

## Related Skills

- **creating-subagents** — When to create subagents; subagent descriptions are agent-facing delegation instructions (Use when/Pass/Ask format)
- **prompt-engineering** — Writing effective prompts
- **subagent-delegation** — Managing subagent lifecycle and review cycles
- **test-guidelines** — Writing tests that verify model output
