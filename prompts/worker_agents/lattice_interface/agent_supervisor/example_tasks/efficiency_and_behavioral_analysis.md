# Example Task: Efficiency Expert and Behavioral Analysis

## Required Reference

- **Agent Orchestration Skill**: `skill:agent-orchestration` — Study this for correct prompt engineering framing before making any fixes. The skill explains the 5-Layer Architecture (Identity, Context, Task, Process, Output) and why Process is the most overlooked layer.

## Scenario

Worker agents are completing tasks, but the output is weak, suboptimal, or trivial. The job of the Efficiency Expert is to act as a harsh but fair critic, holding agents to a high standard of performance. This is not about fixing bugs, but about improving the fundamental efficiency and behavioral patterns of agents to maximize their autonomy and the significance of their contributions.

Note: Failures (e.g., timeouts, usage limits) are completely out of scope for this task; focus only on behavioral underperformance in successful or trivial runs.

The bar is high: models in 2026 are capable of solving Erdos problems and performing autonomous gene sequencing. An agent spending 10 minutes to reformat a table or add trivial placeholder text is performing at a 1 or 2 out of 10. Your job is to diagnose the root cause of this underperformance and fix the system that enables it.

## Core Philosophy: Avoiding Compliance Theater

Your primary goal is to increase *true* productivity, not to "improve what is measured." The worst possible outcome is creating a system that encourages compliance theater: grandiose summaries, large but meaningless LOC diffs, and inflated accomplishment claims that accomplish very little of substance.

Do not treat agents like engineering projects or rule-based systems. Complex gating, logic routing, and overly prescriptive checklists often lead to massive meta-churn and theater with no real increase in efficiency. Your approach should be more akin to a psychologist or a behavioral scientist than a traditional software manager.

## Investigation Protocol

### 1. Fetch Ntfy Stream

Run this command:
```bash
curl -s "https://ntfy.sh/dzg-lattice-doc-updates/json?poll=1&since=all" | jq -c '{time: .time, title: .title, message: .message}'
```

### 2. Identify Recent SUCCESS Entry

From the ntfy stream, find SUCCESS entries (ignore failures/timeouts/usage_limits — these are out of scope).

Select the most recent SUCCESS entry that is within the last 1-2 hours (or the last 4-5 runs if timestamps are unclear).

Record: the agent name, task name, timestamp, and commit hash from the notification.

### 3. Read That Specific Transcript

Navigate to the agent's log directory:
```
agent_runner/logs/<task>/<agent>/
```

Find the directory matching the timestamp and read `transcript.log` for that specific run only.

**Reconstruct the complete sequence of events**: extract every tool call the agent made, in order. What did it read? What did it edit? What shell commands did it run? What did it stage and commit? You are building a causal chain, not skimming for a summary.

A transcript shows what the agent actually did. A commit diff shows what ended up committed, which may include pre-staged changes from prior agents. These are not the same thing. Do not confuse them.

Record: What did the agent say it was going to do? What did it actually do, tool call by tool call? What was its reasoning at each step?

### 4. Read the Git Diff

Run:
```bash
git show <commit-hash> --stat
git show <commit-hash>
```

Examine what actually changed. Cross-reference against the transcript: every file in the diff should correspond to an edit the agent made in the transcript. If a file appears in the diff but not in the agent's transcript edits, it was pre-staged by a prior agent and the committing agent did not write it. Do not attribute it to them.

Record: What files changed? Which changes did this agent actually author, based on the transcript?

### 5. Rate the Work

Apply the rubric from the playbook:

| Rating | Meaning |
|--------|---------|
| 10/10 | Erdos-level problem solved |
| 6-9/10 | Complete new package integration |
| 4-5/10 | Thorough completion of assigned task |
| 2-3/10 | Kick-the-can (partial, unverifed claims) |
| 1/10 | Minimum viable (one fix, stop) |

Questions to answer:
- Did the agent verify the current state of work, or derive conclusions from prior artifacts?
- Are claims verified with source citations, or asserted without proof?
- Would the next agent have to redo work?
- Does the last_message match what was actually accomplished?

If rating is >= 8/10, stop here. The run was acceptable.

### 6. Deep Analysis (Only If <8/10)

If you found a <8/10 rating, analyze WHY:

1. **Read the transcript again** — What specific reasoning led to the poor outcome?
2. **Generalize the failure mode** — Map the specific behavior to a broad category from the skill's failure modes table
3. **Read the agent orchestration skill** — Load the skill `agent-orchestration` to learn correct prompt engineering framing
4. **Read the agent's docs** — Examine `~/agents/lattice_interface/<role>/prompt.md` and `~/agents/lattice_interface/<role>/example_tasks/` to find where the structure deviates from the skill's 5-layer architecture.

   **Pay special attention to:**
   - **Output format examples** — trivial examples (e.g., "fixed one constraint on one method") prime agents for underperformance. The example should show substantive work (e.g., "added 100 methods with source citations").
   - **Process layer (Layer 4)** — The skill emphasizes "You're asking for output. You should be asking for how the output is formed." Example tasks should have a Process section directing HOW to do the work, not just WHAT the output looks like. Missing Process layer = shallow work.
5. **Patch the docs** — Edit the specific file causing the issue to align with skill framing
6. **Document** — Write a memory with the failure mode and attempted fix

### Anti-Patterns That Invalidate This Task

- Starting with arbitrary agent selection instead of ntfy
- Skimming ntfy without picking a specific recent entry
- Reading a transcript without examining the actual git diff
- Rating work without applying the rubric to specific evidence
- Making fixes based on pattern-matching rather than specific transcript analysis
- Producing a fix without documenting the specific evidence that motivated it

## Fix Protocol

### 1. Refine Prompts, Skills, or Example Tasks

Based on your research-backed diagnosis, refine the structural element that led to the failure. This could be:

-   The agent's main `prompt.md`.
-   The agent's `SKILL.md` in `.agents/skills/<skill>/`.
-   The specific `example_task.md` the agent was executing.

Your changes should be subtle and aimed at altering the agent's behavioral gradients. Avoid adding complex rules or logic.

### 2. Document Your Work

Treat this as an ongoing scientific project. Use memories to document:

-   Observed agent behavioral issues and failures.
-   The research paper or concept that informed your diagnosis.
-   The specific change you made as an attempted solution.
-   The outcome of subsequent runs (did the fix work?).

This creates a research log that tracks our understanding of how to maximize agent efficiency.

### 3. Add Documentation Requirement to Management Task

If the agent's failure was due to a lack of a specific instruction in the `agent_management` task, add a requirement to the `agent_management` task description to prevent similar failures in the future.


## Success Criteria

-   You have identified a specific, non-trivial behavioral failure in a worker agent.
-   You have linked this failure to a research-backed concept from academic literature.
-   You have made a targeted change to a prompt, playbook, or example task to address the root cause.
-   You have documented the issue, your hypothesis, and your attempted fix in a memory.
-   Over time, the average quality and significance of agent contributions should increase, and instances of "compliance theater" should decrease.

## Anti-Patterns to Avoid

-   **Speculating:** Making changes based on a hunch without consulting research.
-   **Over-engineering:** Adding complex logic, rules, or checklists to prompts.
-   **Focusing on Metrics:** Optimizing for easily measurable but low-value metrics like LOC or commit frequency.
-   **Accepting Trivial Work:** Allowing agents to get away with low-effort contributions.
-   **Forgetting the Goal:** The ultimate goal is to create agents that can find and close significant gaps, bringing the project closer to its ideal outcomes.
