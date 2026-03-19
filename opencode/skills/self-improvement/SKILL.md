---
name: self-improvement
description: Build production systems with AI by writing less code, not more. Use deterministic tooling, deliberate context engineering, and architectural priming.
---

# Production AI Engineering

I've created secure, reliable production applications by writing less code, not more.

## Here's what actually works

Use deterministic code everywhere. Only use AI where AI is needed, but have the LLM write the deterministic code for you.

LLMs are best at deduction, NOT induction. Don't wait for the model to infer codebase context, instead force-load modular summaries into context as memory files or via other mechanisms. These memory files serve as high-level natural language-driven summaries of your codebase.

Prime attention toward YOUR architecture. Do NOT rely on the LLM to make assumptions of what it's been trained on. When you force-inject context that never falls out, every attention head is predisposed toward your patterns, your constraints, your existing abstractions.

LLMs are best at deduction, NOT induction. (Yes it's that important!) If you rely on the LLM to fall back to its training for your code, you get the average of all code... sloppy. So, when creating memory, you SHOULD clearly define architecture constraints, design patterns, data flow, frameworks, libraries, dependencies, state management, etc. Again, have the LLM write this for you. Force-load it so it cannot fall out of context!

Use ctags to reduce hallucination and code duplication. It's fast, free magic. Use hooks to automatically inject a filtered markdown view of files/classes/methods/functions into a memory file. Run the script on every Pre/PostToolUse to prime the agent's attention towards existing code as it works.

Don't use monoliths. If you must, you've got to leverage memory files religiously. They are your lifeline. In small codebases, this isn't too difficult to manage. For large ones, you MUST be more verbose and modular in your memory files. You'll have to intentionally load/unload when needed.

Contract-driven development eliminates most issues with AI-based coding. Protobufs, Connect RPC, Pydantic, ZeroMQ, etc., anything strongly typed fundamentally works better. Define a contract, let deterministic codegen handle expansion. These contracts not only allow you to programmatically generate and lint your code, but they are also the compressed semantic description of your codebase… in other words, they become your modular memory files.

Deterministic tooling and formal validation is the whole game. Code generation from schemas. Programmatic contract testing. Limit the amount of context the agent needs to work by moving the reasoning process earlier in the stack. Let it focus on architectural choices and threat modelling instead of debugging code for hours.

Skills replace MCPs. MCPs are bulky, token intensive, and wasteful. Before LLMs, entire production workflows and "intelligent orchestration" was done via well-written bash scripts & CLI tools. You don't need more abstraction, you need less. Skills should teach the model how to use tools, frameworks, libraries etc. Anytime you've got a repetition, automate it with a script and give it to the model.

Separate planning from execution. I use planning mode frequently. For complex plans requiring exhaustive reasoning, I use a UserPromptSubmit hook that spawns a headless agent to logically decompose my prompt into atomic actions, then present this atomized plan to the primary agent. This atomizer agent shares the same memory files, so its plans are entirely context-aware. The primary agent no longer wastes tokens interpreting your request, instead it deliberately spends reasoning tokens on solving the problem. This is a process I call semantic outsourcing.

**tl;dr:** Deliberate context engineering is the only way to leverage AI to build production systems that scale. Shift-left reasoning as early as possible in the stack. Use deterministic code everywhere. Only use AI where AI is needed, but have the LLM write that deterministic code for you.

All of the abstraction you'd ever need is in the very terminal your agent codes in.
