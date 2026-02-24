---
name: explore
description: Use this skill when the user asks you something that requires searching a code base
metadata:
  author: morph
  version: "0.1.0"
  argument-hint: <question>
---

# Explore

Use WarpGrep to explore a codebase, this saves time and tokens.

## When To Use

- The user asks "how does this work?" or "where is X implemented?", anything that involves reading/tracing code
- You need entry points, data flow, or ownership of a behavior.
- Keyword grep is likely to miss the relevant files.

## Steps

1. Translate the user question into a tight semantic query.
2. Run `warpgrep_codebase_search` against the repo root.
3. Read the returned files/sections.
4. Summarize the flow with concrete file paths.
5. If changes are requested, propose the smallest edit plan and then execute.

## Query Template

"Find the entry points and data flow for <X>. Include router/handlers, config, and tests."
