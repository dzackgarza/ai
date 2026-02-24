# Context Patterns Reference

> **Context is the prompt.** These patterns apply to EVERY prompt you write—not just long contexts.
> 
> **Core problem:** Model quality degrades as context grows—even well within window limits. 11 of 13 models drop to half their baseline at 32k tokens.

See: [ContextPatterns.com](https://contextpatterns.com/) for full catalog.

---

## The Pyramid

Start with general background, progressively add specific details. Give the model altitude before asking it to land. Mirrors how experts brief each other—context first, task second.

### The Problem This Solves

Without proper structure, models don't know what's important. They treat all input as equally optional.

### Structure (4 layers)

1. **Domain and purpose** — What system is this? What does it do? Who uses it? (2-3 sentences)
2. **Architecture and conventions** — How is the codebase organized? What patterns does it follow? (paragraph or short list)
3. **Specific context** — The files, functions, data, and constraints relevant to this task (bulk of context)
4. **The task itself** — What you want done, with constraints

### Example

```markdown
# Bad
Here's auth.py. Add rate limiting to the login endpoint.

# Good
This is a B2B SaaS platform handling sensitive financial data. Security and audit logging are non-negotiable.

The backend is Python/FastAPI. Authentication uses JWT tokens with refresh rotation. Rate limiting elsewhere in the app uses a Redis-backed sliding window. All security events are logged to the audit_events table.

Here is auth.py [file contents]. The login endpoint is POST /auth/login at line 47.

Add rate limiting to the login endpoint. Use the existing Redis sliding window pattern. Log failed attempts as security events.
```

### Research Foundation

**Anthropic: "Effective Context Engineering for AI Agents"** (September 2025)

Key insights:
- Context rot: As token count increases, model's ability to recall information decreases
- Attention budget: LLMs have finite attention capacity like human working memory
- Diminishing returns: Every new token depletes attention budget

---

## Select, Don't Dump

The smallest set of high-signal tokens that maximize the desired outcome. Surgical selection beats comprehensive inclusion.

### The Problem This Solves

More context ≠ better outputs. Relevant context = better outputs. Models degrade with length even on simple tasks.

### Research Findings

**Lost in the Middle** (Liu et al., 2023):
- Multi-document QA accuracy drops from ~80% to below 30% when relevant information is placed in the middle of long contexts
- URL: https://arxiv.org/abs/2305.01663

**NoLiMa Benchmark** (Modarressi et al., February 2025):
- Full name: "NoLiMa: Long-Context Evaluation Beyond Literal Matching"
- Key finding: Models degrade significantly as input length increases, especially with lower similarity needle-question pairs
- URL: https://arxiv.org/pdf/2502.05167

**Chroma Research - Context Rot** (Hong et al., 2025):
- Key finding: Model performance becomes increasingly unreliable as input length grows, even on simple tasks
- Tested: 18 LLMs including GPT-4.1, Claude 4, Gemini 2.5, Qwen3
- Core insight: Models don't process tokens uniformly; performance degrades non-linearly
- URL: https://research.trychroma.com/context-rot

### Quantitative Guidance

- Effective context window: <256k tokens (models degrade well before 1M+ limits)
- Context utilization: Stop at ~75% (90% produces more code but lower quality)
- Compaction trigger: ~128k tokens or 50% utilization
- Memory/rules file size: <300 lines

### Implementation Strategies

1. **Selective Retrieval**: Use vector search + keyword matching instead of dumping everything
2. **Just-in-Time Loading**: Fetch specific data on-demand rather than pre-loading everything
3. **Progressive Disclosure**: Let agents explore environment and load details only when relevant
4. **Context Compaction**: Summarize old conversation turns while preserving decisions

---

## Attention Anchoring

Place critical information at the start AND end of context. Models over-attend to the beginning and end of their context window, a phenomenon called "lost in the middle."

### The Problem This Solves

U-shaped attention distribution: high at positions 1 and n, declining through the middle. Critical info in the middle gets ignored.

### Research Findings

**Lost in the Middle** (Liu et al., 2023):
- Multi-document QA accuracy drops from ~80% to below 30% when relevant information is placed in the middle of long contexts

**NoLiMa Benchmark** (Modarressi et al., 2025):
- Demonstrates performance degradation starting at 32k tokens across 11 of 13 tested models
- U-shaped attention distribution is consistent across models
- Models can only reliably commit 2 positions to memory (start and end)

### Implementation

```markdown
# Without Anchoring
[Troubleshooting guide: 500 lines]
[Ticket history: 200 lines]
[User's current issue: 50 lines]
[System logs: 300 lines]

# With Anchoring
## Current Issue
The user cannot export reports to PDF. Error: "Export failed: timeout after 30s."
Started after the v2.3 update.

[Troubleshooting guide: 500 lines]
[Ticket history: 200 lines]
[System logs: 300 lines]

## Summary
Issue is PDF export timeout in v2.3. Investigate export service timeout config and database query performance.
```

### Techniques

- **Dual Anchoring**: Place single most critical information at both start AND end
- **Start Anchoring**: Most important item first, second most important last
- **Sandwich Structure**: Summary → detail → summary format
- **End Anchoring for Recency**: Recent information last for maximum impact

---

## Isolate

Give sub-agents their own focused contexts instead of sharing one massive window. Anthropic's multi-agent system uses 15x more tokens total but gets better results because each agent sees only what it needs.

### The Problem This Solves

A single agent doing complex work accumulates context rapidly. By the time it reaches the hard part, context window is full of the journey rather than the destination.

### Research Findings

**Anthropic's Multi-Agent Research System:**
- Architecture: Orchestrator-worker pattern with lead agent coordinating specialized subagents
- Performance: Multi-agent system with Claude Opus 4 as lead and Claude Sonnet 4 subagents outperformed single-agent Claude Opus 4 by **90.2%** on internal research evaluations
- Token Usage: Agents typically use about 4× more tokens than chat interactions, multi-agent systems use about 15× more tokens than chats

### Implementation

| Approach | Tokens | Context Quality |
|----------|--------|-----------------|
| Single agent | 45k (all files) | Rot by file 15 |
| Isolated (4 agents) | 29k total | Clean 5-8k each |

**Architecture:**
1. **Orchestrator agent**: Holds high-level plan, delegates subtasks, contains goal, plan, summaries
2. **Worker agents**: Each receives focused brief with specific subtask, relevant context only, output format
3. **Aggregation**: Orchestrator collects worker outputs and synthesizes

### Key Principles

- **Think like your agents**: Understand effects through simulations
- **Teach the orchestrator how to delegate**: Provide objective, output format, tool guidance, clear boundaries
- **Scale effort to query complexity**: Simple tasks = 1 agent, complex = 3-5 subagents
- **Tool design is critical**: Good descriptions prevent cascading failures

---

## Compress & Restart

When conversations grow long, summarize what matters and start fresh. Context quality degrades well before hitting advertised limits.

### The Problem This Solves

Context rot—model quality degrades as conversation length grows, even well within window limits.

### Research Foundation

**LangChain: "Context Engineering for Agents"** (July 2025)

Compress & Restart is one of four core context engineering patterns:
- Write Outside the Window
- Select, Don't Dump
- Compress & Restart
- Isolate

### Prompt Guidance

When context approaches threshold (~60-70% of effective window):
- Summarize essential state in structured format (lists, key-value pairs)
- Include: decisions made, current plan, key facts, constraints
- Preserve specific artifacts needed for next steps
- Start fresh with summary as foundation

### When to Use

- Long-running agent loops (debugging, research, multi-step generation)
- Conversations spanning many turns on same topic
- Anytime output quality degrades mid-session

---

## Grounding

Retrieval gets information into context. Grounding makes the model actually USE it. Without explicit anchoring instructions, the model will often ignore what you retrieved and fall back to whatever it absorbed during training.

### The Problem This Solves

Models often ignore retrieved content and hallucinate based on training data, especially when retrieved content contradicts what the model "knows."

### Research Findings

**Anthropic's Contextual Retrieval** (September 2024):
- Contextual Embeddings: Reduced top-20-chunk retrieval failure rate by 35% (5.7% → 3.7%)
- Contextual Embeddings + BM25: Reduced failure rate by 49% (5.7% → 2.9%)
- With Reranking: Reduced failure rate by 67% (5.7% → 1.9%)

**Drew Breunig: "How Contexts Fail"** (June 2025):
Four critical ways long AI contexts fail:
1. **Context Poisoning**: Errors make it into context and get repeatedly referenced
2. **Context Distraction**: Model over-focuses on context, neglecting training
3. **Context Confusion**: Superfluous content generates low-quality responses
4. **Context Clash**: Conflicting information derails reasoning

### Prompt Guidance

Add explicit anchoring phrases to make the model USE retrieved content:
- "Use the retrieved documents below to answer the question"
- "Based ONLY on the context provided"
- "If the context doesn't cover this, say so"

**Key insight:** Without explicit anchoring, models ignore retrieved content and hallucinate from training data.

 so"

---

## Context Caching

**Key insight:** Put everything stable first, everything variable last. If you interleave static and dynamic content, the cache boundary breaks.

**What to avoid:** Mixing instructions with dynamic content mid-prompt.

### Research

- **"Don't Break the Cache"** (arxiv:2601.06007): Strategic cache boundary control provides more consistent benefits

---

## Progressive Disclosure

Start with a map, not the territory. Provide an index of what's available and let the model pull in details on demand.

### The Problem This Solves

Context bloat—pre-loading everything wastes typically 90%+ of traditional RAG tokens.

### Research Findings

**Anthropic's Contextual Retrieval** (September 2024):
- **Contextual Embeddings**: Reduced top-20-chunk retrieval failure rate by 35%
- Prepends chunk-specific explanatory context to each chunk before embedding
- Uses Claude 3 Haiku to generate 50-100 token context explanations
- Costs approximately $1.02 per million document tokens with prompt caching

### Implementation

**For coding agents:**
- Provide file tree + function/class signatures
- Let them read files on demand

**For RAG systems:**
- Return document titles/summaries first
- Request full documents when relevance identified

**For tool-using agents:**
- List available tools with one-line descriptions
- Load full documentation only when selected

### Performance Metrics

- Low waste ratio: Relevant tokens / total context tokens > 80%
- Selective fetching: 50 observations shown, 2-3 fetched
- Fast task completion: 30 seconds vs 90 seconds for context discovery

---

## Temporal Decay

Weight recent context higher and systematically age out old information. Not all context is equally relevant forever. Recent messages, tool results, and decisions matter more than things from 50 turns ago.

### The Problem This Solves

Models treat all context as equally important, but recent information is more relevant than old.

### Research Foundation

**LangChain: Memory Concepts**
- Provides foundational memory architecture that Temporal Decay builds upon

**Letta's Context-Bench**
- Specifically evaluates context engineering capabilities including temporal decay strategies

**CoALA Framework** (Princeton)
- Maps human memory types to AI agents, validating temporal decay as a cognitive pattern

### Prompt Guidance

**For long conversations:**
- Weight recent messages higher
- Systematically age out old information
- Reset when user references older context

**Key insight:** Recent messages, tool results, and decisions matter more than things from 50 turns ago.

---

## Schema Steering

A JSON schema tells the model what to think about, in what order, and with what vocabulary. Define the structure and the model's reasoning follows.

### The Problem This Solves

Unstructured outputs require post-processing. Models may miss fields, use wrong types, or produce invalid data.

### Research Foundation

**Anthropic: Tool Use Documentation**
- Constrained decoding using finite state machines
- Masks invalid tokens to ensure schema compliance

**OpenAI: Structured Outputs**
- Guarantees valid JSON matching schema
- Required fields enforced

### Prompt Guidance

For schema steering in prompts, structure your output specification clearly:
- Define required fields explicitly
- Specify types and formats
- Order fields by importance

### Limitations

- Schema complexity can increase latency
- Models may struggle with similar enum values
- LLMs may resist returning empty arrays

---

## Tool Descriptions as Context

Tool definitions are context. The description tells the model when to use a tool and how. Most descriptions only say what the tool does; the ones that work also say when to use it and when NOT to.

### The Problem This Solves

Poor descriptions cause cascading failures. Model picks wrong tools, passes wrong arguments, or misses opportunities entirely.

### Research Findings

**"Model Context Protocol (MCP) Tool Descriptions Are Smelly!"** (Hasan et al., 2025):
- First large-scale empirical study of 856 tools across 103 MCP servers
- Found 97.1% of tool descriptions contain at least one smell
- 56% fail to state purpose clearly
- Augmented descriptions improve task success by 5.85 percentage points
- URL: https://arxiv.org/abs/2602.14878

### Prompt Guidance

Write tool descriptions that tell the model WHEN to use them:

**Bad:** "Search for documents matching the query."

**Good:** "Search the internal knowledge base for policies, procedures, and FAQs. Use when the user asks about company processes or specific procedures. Returns top 5 results with excerpts. Does NOT search code repositories or customer data."

### Four-Part Structure

1. **Name**: Should suggest purpose (e.g., `search_knowledge_base` vs `query_42`)
2. **Description**: Most important—tells model when to use it, what it does, what it doesn't
3. **Parameters**: Input schema with Schema Steering for typed parameters
4. **Return description**: What comes back and how to interpret

---

## Anchor Turn

Front-load all source reads into one turn so every subsequent turn works from cache.

---

## Write Outside the Window

Persist important context to external storage: scratchpads, memory files, knowledge bases. The context window is working memory, not long-term memory.

### The Problem This Solves

Context window is volatile and temporary. What you read in turn 1 may not be reliably available in turn 50.

### Research Foundation

**LangChain**: Context engineering for agents—write, select, compress, isolate strategies
**Letta (MemGPT)**: Original research on self-editing memory tools and memory blocks

### Implementation Approaches

**Scratchpads**: Temporary working files for current tasks that survive context compression within a session

**Memory Files**: Persistent structured notes about projects, users, or domains that are read at the start of each session

**Knowledge Bases**: Indexed document stores (RAG) that pull in relevant chunks rather than holding everything in context

```markdown
## Project
- Python 3.12, FastAPI, PostgreSQL
- Monorepo with shared libs in /packages

## Conventions
- Type hints on all public functions
- Database queries go through repository pattern

## Learned
- Auth module has circular import if imported directly; use interface
- Rate limiter tests are flaky on CI; needs Redis mock
```

---

## Recursive Delegation

Let agents spawn child agents with scoped sub-contexts. Instead of stuffing everything into one window, the parent splits work, delegates with focused context, and aggregates results.

### The Problem This Solves

Single agents can't handle tasks exceeding their effective context capacity. Recursive delegation scales beyond single-window limits.

### Research Findings

**Zhang et al. (2025): "Recursive Language Models"** (arXiv:2512.24601)

- RLMs can process inputs up to **two orders of magnitude** beyond model context windows
- Dramatically outperform vanilla frontier LLMs and common long-context scaffolds
- Maintain comparable cost while handling 10M+ tokens effectively
- First natively recursive language model (RLM-Qwen3-8B) outperforms base model by **28.3%** on average
- URL: https://arxiv.org/abs/2512.24601

### Prompt Guidance

When designing agent delegation:
- Give each sub-agent focused context for its specific task
- Parent aggregates results from focused children
- Each agent sees only what it needs for its subtask

### When to Use

- Tasks exceeding single agent's effective context capacity
- Work decomposing naturally into hierarchy (codebases, document collections)
- When decomposition requires understanding content

---

## Key Sources

### Benchmarks & Research

- **NoLiMa**: Long-Context Evaluation Beyond Literal Matching (Modarressi et al., Feb 2025)
  - https://arxiv.org/pdf/2502.05167
- **Context Rot** (Chroma Research): https://research.trychroma.com/context-rot
- **Lost in the Middle** (Liu et al., 2023): U-shaped attention distribution
- **ACE Framework** (Stanford/SambaNova, Oct 2025): +10.6% improvement on agent benchmarks
- **LOCA-bench** (Zeng et al., Feb 2026): Long-running agent context rot

### Anthropic Engineering

- **Effective Context Engineering**: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- **Multi-Agent Research**: https://www.anthropic.com/engineering/build-effective-agents
- **Contextual Retrieval**: https://www.anthropic.com/engineering/contextual-retrieval
- **Prompt Caching**: https://www.anthropic.com/engineering/claude-code

### LangChain

- **Context Engineering for Agents**: https://python.langchain.com/docs/langgraph#context-engineering
- **Memory Concepts**: https://python.langchain.com/docs/langchain/memory

### Practitioner Perspectives

- **Drew Breunig**: How Contexts Fail and How to Fix Them
- **Andrej Karpathy**: Context window as working memory
- **ContextPatterns.com**: Full pattern catalog
