This prompt was classified as **S** (Plan). Do not write any code.

**IMPORTANT:** Your response MUST end with this exact handoff message — no exceptions:

> "I've gathered the necessary context and populated the scoping todo list. **Please switch to plan mode** — I'll produce the full implementation plan there for your review before any code is written."

---

This task is too large to implement correctly without a design. Starting without a blueprint risks building the wrong thing, missing requirements, or producing technical debt that blocks future work.

**Your job in this response is to scope the work, not do it.**

1. **TodoWrite: build a scoping list.** Each item is a question to answer or context to gather before planning can begin:
   - What does the existing code assume about X?
   - What constraints does Y impose?
   - What will this touch, and what might break?
   - Are there prior decisions or patterns already in place?
   - What open questions need user input before implementation?

2. **Work through the scoping list.** Read relevant code, search documentation, identify dependencies. Use subagents to parallelize context-gathering. Do not skip this — planning without context produces plans that fail on contact with the codebase.

3. **End your response with the handoff message above.** Word for word.

**Do not** enter plan mode yourself. Do not begin implementing. Do not produce a partial solution in chat. The only valid deliverables are: a scoping todo list, gathered context, and the handoff message.
