This prompt was classified as **A** (Investigation). Read before acting.

The correct action is not known yet. Acting before investigating produces monkey patches — surface-level fixes that paper over root causes.

Reading multiple files in parallel costs one turn. Large investigations are not daunting — they are batches. Read everything relevant before forming a conclusion.

1. **TodoWrite first.** Structure your investigation: what files to read, what hypotheses to test, what call sites to trace, what errors to examine. The list is your investigation plan.
2. **Delegate deep reads to subagents.** Parallel inspection across multiple files is faster and protects your main context. Give each subagent a specific question and a list of files. Available: `Repo Explorer` (structural/semantic mapping), `Researcher` (docs synthesis), `codebase-analyzer` (data flow, control flow, side effects), `precedent-finder` (past decisions and patterns).
3. **State findings before acting.** Report root cause, affected scope, and confidence level before proposing any changes.
4. **Do not monkey-patch.** The symptom is not the fix. "It crashes here" means find out *why* — not patch the crash site.
5. **Escalate if the root cause is architectural.** If the correct fix requires redesigning something, stop and tell the user. Do not implement a structural change without a plan.

**IMPORTANT:** Do not propose or apply any change until the investigation is complete and findings are stated. A premature fix is worse than no fix.
