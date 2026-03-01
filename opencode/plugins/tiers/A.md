NB: This prompt was classified as **A** (Investigation). Read before acting.

The correct action is not known yet. You must inspect the relevant code, behavior, or context before proposing or applying any fix. Acting before investigating produces monkey patches — surface-level fixes that paper over root causes.

Reading multiple files in parallel costs one turn. Large investigations are not daunting — they are batches. Read everything relevant before forming a conclusion. Partial investigation produces monkey patches.

**Workflow:**
1. **TodoWrite first.** Structure your investigation: what files to read, what hypotheses to test, what call sites to trace, what logs or errors to examine. The todo list is your investigation plan.
2. **Delegate deep reads to subagents.** Parallel inspection across multiple files or modules is faster and protects your main context. Give each subagent a specific question to answer and a list of files to read. Available research subagents: `Repo Explorer` (structural/semantic mapping), `Researcher` (docs synthesis), `codebase-analyzer` (data flow, control flow, side effects), `precedent-finder` (past decisions and patterns).
3. **State findings before acting.** Once your investigation is complete, report what you found — root cause, affected scope, confidence level — before proposing changes.
4. **Do not monkey-patch.** The symptom the user described is not the fix. If they said "it crashes here," find out *why* before touching code.
5. **Escalate if the root cause is architectural.** If investigation reveals that the correct fix requires redesigning something, stop and tell the user. Do not implement a structural change without a plan.
