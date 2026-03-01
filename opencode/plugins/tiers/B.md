NB: This prompt was classified as **B** (Iteration). Apply the same operation across a set of targets.

You know what to do before opening the first file. Only the targets vary.

**Workflow:**
1. **TodoWrite first.** Enumerate every target item before starting. The list is your contract — it makes progress visible and prevents drift.
2. **Apply uniformly.** Run the same operation on each item. Do not make per-item judgment calls about *what* to do. If an item turns out to need different treatment, flag it and move on — do not silently handle it differently.
3. **Mark items complete as you go.**
4. **Delegate large sets.** If the set has more than ~10 items, dispatch the iteration to a subagent with an explicit checklist rather than processing sequentially in the main context. Provide the subagent with the full operation spec and the item list.

If at any point the task reveals that items require individual judgment (not just iteration), stop and escalate — this may be an A-tier task.
