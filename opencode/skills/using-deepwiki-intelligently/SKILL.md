---
name: using-deepwiki-intelligently
description: Use when planning DeepWiki queries for codebase exploration or architecture understanding.
---

# Using DeepWiki Intelligently

DeepWiki is a **free intelligent LLM service with RAG over GitHub repos**. Treat it as an **intelligent data source for guidance**, not a dumb search engine or code aggregator.

## Core Policy

- **Use DeepWiki to GUIDE and NARROW your tasks**, not to offload your work
- **Trust but verify** all DeepWiki results — it suffers from standard LLM failure modes
- **Never treat DeepWiki as a file fetcher** — use `gh` or direct source reads for that
- **Always verify negative findings** — no RAG hits can cause confident false claims of non-existence

## What DeepWiki Is For

**Good queries** (guidance, exploration, narrowing):

- "How do plugins add system prompts to chat?"
- "What hooks are available for intercepting tool execution?"
- "How does session continuation work in this codebase?"
- "Where is the message transformation logic located?"

These queries use DeepWiki's RAG + LLM to **point you at relevant code**, not to reproduce it.

## What DeepWiki Is NOT For

**Bad queries** (dumb aggregation, file fetching):

- "Provide all of the source code for x.ts, y.ts, and z.ts"
- "List every function in the plugin system"
- "Show me the complete implementation of X"

**Why these are bad:**

1. **Actively worse than `gh`** — direct file fetch is faster and lossless
2. **Introduces "telephone" loss** — LLM summarization can drop critical details
3. **Risks hallucination** — model may invent or misquote code
4. **Wastes the RAG advantage** — you're using an intelligent guide as a dumb copier

## LLM Failure Modes to Watch For

| Failure Mode | Symptom | Mitigation |
|--------------|---------|------------|
| **No RAG hits** | Confidently claims "X doesn't exist" | Broaden search, verify in source |
| **Partial retrieval** | Misses relevant files, claims completeness | Cross-check with grep/glob |
| **Hallucinated paths** | Cites non-existent files or functions | Verify paths exist before trusting |
| **Outdated info** | References removed or renamed symbols | Check git history, verify current state |

## Decision Procedure

**Before querying DeepWiki:**

1. **What am I trying to learn?**
   - Structure/architecture/flow → DeepWiki is appropriate
   - Exact file contents → Use `gh`, `read_file`, or `glob` instead
   - Specific symbol location → Use `find_symbol` or grep first

2. **What will I do with the result?**
   - Guide my own investigation → DeepWiki
   - Copy-paste into code → Direct source read
   - Verify existence → Direct inspection

**After receiving DeepWiki results:**

1. **Verify all file paths exist** before acting on them
2. **Cross-check negative claims** ("X not found") with direct search
3. **Use results as starting points**, not final answers
4. **Read the actual source** DeepWiki points you to

## Required Verification Checklist

Before acting on DeepWiki output:

- [ ] File paths cited actually exist (verified via `glob` or `read_file`)
- [ ] Negative claims ("not found", "doesn't exist") cross-checked with direct search
- [ ] Symbol/function names verified in source
- [ ] Used DeepWiki to **guide** investigation, not replace it

## Anti-Patterns

| Pattern | Why Bad | Do Instead |
|---------|---------|------------|
| "Show me the full source of X" | Lossy, slow, hallucination risk | `read_file` or `gh view` |
| Accepting "not found" without verification | RAG gaps cause false negatives | Grep/glob to confirm |
| Using DeepWiki when you know the file path | Unnecessary indirection | Read the file directly |
| Treating DeepWiki as authoritative | It's an LLM with retrieval, not ground truth | Verify in source |

## When to Use DeepWiki

**Use DeepWiki when:**

- Exploring an unfamiliar codebase or subsystem
- You need to understand architecture or data flow
- You don't know which files to read yet
- You want a guided tour of a feature area

**Don't use DeepWiki when:**

- You know the exact file paths
- You need complete, verbatim code
- You're checking for existence of a specific symbol
- A direct `read_file`, `glob`, or `gh` call would work
