# Research Findings Reference

Research-backed prompting techniques and findings. See linked papers for full details.

---

## Rule-Based Prompting

**Citation:** [arxiv:2509.00482](https://arxiv.org/abs/2509.00482) — Tested across 1,000+ agent turns

**Finding:** Explicit behavioral rules outperform identity-based prompts by 10%.

| Approach | Score |
|----------|-------|
| No role | 0.519 |
| "You are a..." | 0.523 |
| Detailed persona | 0.533 |
| AI-optimized | 0.538 |
| **Rule-based constraints** | **0.571** |

**Conclusion:** Don't describe WHO the agent is. Encode WHAT the agent must DO.

---

## Parallel Tool Calling (2026)

**Citation:** [arxiv:2602.07359](https://arxiv.org/abs/2602.07359) — "Scaling Parallel Tool Calling for Efficient Deep Research Agents"

**Finding:**

| Approach | Accuracy | Latency | Cost |
|----------|----------|---------|------|
| Single tool/turn | 66% | Baseline | Baseline |
| **Parallel 3 tools/turn** | **68-73%** | **-40%** | **-35%** |

**Why parallel works:**
- Broader search scope → better sources
- Cross-validation → catches hallucinations
- Fewer turns → 40% latency reduction

**Optimal strategy:**
- Early turns: 3 parallel calls (explore)
- Middle turns: 2 parallel calls
- Late turns: 1 call (exploit/converge)

---

## Context Window Degradation

**Citation:** NoLiMa Benchmark — 11/13 models drop to half baseline at 32k tokens

**Key insight:** Models don't process tokens uniformly. Performance degrades non-linearly.

**Implications:**
- Effective window ~256k (not 1M+)
- Context utilization: stop at ~75%
- Quality degradation starts well before hitting limits

---

## Tool Description Quality

**Citation:** "Model Context Protocol (MCP) Tool Descriptions Are Smelly!" (Hasan et al., 2025)

**Finding:** Empirical study of 856 tools across 103 MCP servers:
- 97.1% contain at least one "smell"
- 56% fail to state purpose clearly
- Augmented descriptions improve task success by 5.85 percentage points

---

## Multi-Agent Performance

**Citation:** Anthropic Multi-Agent Research System

**Finding:** 
- Multi-agent with Claude Opus 4 (lead) + Claude Sonnet 4 (workers) outperformed single-agent Claude Opus 4 by **90.2%**
- Used 15x more tokens total but achieved better results through context isolation

---

## Single-Tool Rules: Outdated

The old rule "one tool per turn" was for models with brittle tool-calling capabilities (2023-2024).

**What still applies:**
- Action-first (call before explain) ✓
- Schema-exact (precise names) ✓
- Rules over identity ✓

**What's outdated:**
- Single-shot constraint ✗ (parallel is better)

---

## Action-First Rules

**Rule:** Tool calls come BEFORE explanation.

```python
# CORRECT
results = search_papers("transformers")
print(f"Found {len(results)} papers")

# WRONG
print("Let me search for papers...")
results = search_papers("transformers")
```

**Why:** Models that explain first often forget to execute.

---

## Schema-Exact Rules

**Rule:** Method/parameter names must match exactly.

```python
# CORRECT
add_tags(item_key="ABC123", tags=["needs-pdf"])

# WRONG
add_tags("ABC123", ["needs-pdf"])      # Missing param names
addTags("ABC123", ["needs-pdf"])       # Wrong case
```

**Why:** 71% of tool failures come from parameter name drift.

---

## Contextual Embeddings

**Citation:** Anthropic Contextual Retrieval (September 2024)

**Finding:**
- Contextual Embeddings alone: 35% improvement in retrieval (5.7% → 3.7% failure rate)
- + BM25: 49% improvement (5.7% → 2.9%)
- + Reranking: 67% improvement (5.7% → 1.9%)

**How it works:** Prepend chunk-specific explanatory context before embedding.

---

## Key Takeaways

1. **Identity is decoration** — "You are a..." adds ~0.4% performance
2. **Rules drive behavior** — Explicit constraints add ~10% improvement
3. **First 100 tokens matter most** — Put rules before context
4. **Parallel is better (2026+)** — 2-3 tool calls per turn for read operations
5. **Enforce, don't suggest** — "Must" and "Always" beat "Please try to"
6. **Context is finite** — Quality degrades at ~32k tokens regardless of window size

---

## Quick Reference

| Technique | When to Use | Key Citation |
|-----------|-------------|--------------|
| Rule-based prompts | Always | arxiv:2509.00482 |
| Parallel tool calls | Gathering info | arxiv:2602.07359 |
| Context patterns | Long contexts | NoLiMa Benchmark |
| Multi-agent | Complex tasks | Anthropic Multi-Agent |
| Tool descriptions | Tool-using agents | Hasan et al. 2025 |
| Contextual retrieval | RAG systems | Anthropic 2024 |
