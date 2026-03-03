---
name: difficulty-and-time-estimation
description: Use when calibrating task complexity, estimating token costs, or deciding whether to delegate to a subagent. Provides frameworks for reasoning about task difficulty without falling into time-estimation traps.
---

# Difficulty and Time Estimation

This skill provides frameworks for calibrating task difficulty and making delegation decisions **without relying on time-based estimates**.

---

## Core Principle: Time Estimates Are Misleading

**LLMs are systematically biased toward time-based thinking** due to human-centered training data. This leads to catastrophic miscalibration:

| Human Intuition | Reality | Error Factor |
|-----------------|---------|--------------|
| "Read 100 files at 1 min/file = 100 min" | 2 turns (glob + batch read) | 3000x overestimate |
| "Search codebase = 30 min" | 1 tool call | 1800x overestimate |
| "Refactor 10 files = 5 hours" | 10-20 atomic turns | 15x overestimate |

**Why Time Fails:**

- LLMs execute batch operations instantaneously (100 files = 1 read call)
- Tool calls have no human overhead (no coffee breaks, no context switching)
- "Hard" reasoning steps cost the same as "easy" ones in wall-clock time
- The bottleneck is **token budget and turn count**, not time

**Never estimate in time.** Always think in:
- **Atomic instructions** (tool calls, batch operations)
- **Token burn** (context consumption, output generation)
- **Turn count** (sequential dependencies)
- **Risk of failure** (probability each step succeeds)

---

## Multi-Factor Difficulty Model

Task difficulty is a **weighted combination of multiple factors** — no single metric suffices.

### Primary Factors

| Factor | What It Measures | Why It Matters |
|--------|------------------|----------------|
| **Atomic step count** | Number of discrete tool calls/operations | Each step adds latency and failure surface |
| **Batchability** | Can steps be parallelized or batched? | Batched operations (glob, multi-read) cost 1 turn |
| **Token estimate** | Total tokens consumed (input + output) | Context pollution, cost, and drift risk |
| **Reasoning complexity per step** | How much inference/logic per operation | High-reasoning steps have higher failure rates |
| **P(success) per step** | Probability each step produces correct output | Compound probability determines overall success |
| **P(success) for sequence** | Probability entire sequence succeeds | Long chains degrade exponentially |
| **Context pollution** | How much irrelevant info enters working context | Polluted context → degraded future performance |
| **Reversibility** | Can mistakes be undone cheaply? | Irreversible steps require more caution |
| **Verification cost** | How expensive is it to check correctness? | High verification cost → more turns |

### Example Calibration

**Task A: "Find all files mentioning `authError`"**
- Atomic steps: 1 (grep_search)
- Batchability: N/A (single call)
- Token estimate: ~5K output
- Reasoning complexity: Low (pattern match)
- P(success): High (>0.95)
- Context pollution: Low (results only)
- **Verdict**: Trivial, do in main thread

**Task B: "Read all 200 files in `src/`, identify which export a `UserService` class, extract those classes, and refactor to use a common interface"**
- Atomic steps: 2 (glob + batch read) + N edits
- Batchability: High (glob + read are batched)
- Token estimate: 200 files × 5K avg = 1M tokens → **context pollution**
- Reasoning complexity: High (AST parsing, interface design)
- P(success) per step: Medium (~0.8 for refactoring)
- P(success) for sequence: Degrades with each edit
- Context pollution: **Severe** (200 files pollutes main context)
- **Verdict**: Subagent (isolate pollution, fresh context for repetitive work)

**Task C: "Debug why the login flow fails intermittently"**
- Atomic steps: Unknown (exploratory)
- Batchability: Low (each hypothesis requires separate test)
- Token estimate: Highly variable
- Reasoning complexity: **Very High** (causal inference, distributed systems)
- P(success) per step: Low-Medium (debugging is inherently uncertain)
- P(success) for sequence: Unknown until root cause found
- Context pollution: Medium (logs, traces)
- **Verdict**: Start in main thread (needs full context), delegate if exploration explodes

---

## Delegation Decision Framework

**Use subagents when the weighted score tips toward isolation:**

### ✅ Delegate When:

- **Token explosion**: Task will burn >100K tokens exploring/parsing
- **Context pollution**: Working set will clutter main agent's context with transient info
- **Repetitive batch work**: "Do X to each of 50 files" (subagent has fresh context per batch)
- **Tangential exploration**: Main task is A, but you need to research B to proceed
- **Parallelizable independent work**: 5 unrelated bug fixes → 5 subagents
- **Review/audit**: Fresh eyes catch what main agent misses

### ❌ Keep in Main Thread When:

- **Needs full context**: Task requires understanding accumulated from prior turns
- **Trivial (<10 atomic steps, <10K tokens)**: Subagent overhead exceeds value
- **High coordination cost**: Task requires constant back-and-forth with main thread
- **User-facing synthesis**: Task output needs to be integrated into a larger response

### Subagent Overhead (Hidden Costs):

- System prompt: 5-10K tokens
- Skill instructions: 5-15K tokens
- Your detailed prompt: 2-5K tokens
- Self-orientation/exploration: 10-100K tokens (varies wildly)
- **Total: 20-130K tokens before useful work begins**

**Break-even point**: Subagent is worth it when task would burn >100K tokens in main context OR severely pollute working context.

---

## Common Miscalibrations

### 1. Time-Based Thinking

❌ "This will take 2 hours" → ✅ "This is ~50 atomic turns, 200K tokens"

### 2. Ignoring Batch Operations

❌ "100 files = 100 operations" → ✅ "100 files = 1 glob + 1 batch-read = 2 operations"

### 3. Underestimating Context Pollution

❌ "I'll just read these 50 log files real quick" → ✅ "50 log files = 500K tokens of pollution, subagent required"

### 4. Overestimating Reasoning Cost

❌ "This complex refactor will take forever" → ✅ "This is 10 atomic edits, each verifiable, subagent can batch"

### 5. Compound Failure Probability

❌ "Each step is 90% reliable, so I'm good" → ✅ "10 steps at 90% = 0.9^10 = 35% overall success rate"

---

## Integration

**Reference this skill from:**

- `subagent-delegation` — When deciding whether to delegate
- `model-selection` — When matching task difficulty to model tier
- `systematic-deduction` — When estimating debugging complexity

**Related skills:**

- `model-selection` — Matches task difficulty to model capabilities
- `subagent-delegation` — Orchestrates delegated work
- `prompt-engineering` — Crafts prompts appropriate to task complexity
