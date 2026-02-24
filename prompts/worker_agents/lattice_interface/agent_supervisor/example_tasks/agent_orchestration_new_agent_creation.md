# Example Task: Agent Orchestration and New Agent Creation

## Scenario

The system needs to create new agents or extend existing ones to handle new task types. This requires a systematic process that produces well-structured prompts, proper lifecycle management, and integration with the cron/orchestration layer. Both the individual agent run loop and the outer cron loop must be considered.

This task adapts the battle-tested OpenClaw agent-orchestration framework to this workflow.

---

## Ralph Mode: Two Loops

This task operates at two scales:

1. **Inner Loop (Agent Run)**: A single agent execution has ~15 minutes. It must produce substantive output or pivot. A no-commit run is a failure — the agent must iterate until work is complete.

2. **Outer Loop (Cron Orchestration)**: Cron triggers runs every ~10 minutes. Failed or trivial runs must be caught by agent_management. The outer loop provides feedback to improve inner-loop reliability.

**Both loops are Ralph loops.**

```
## Mode: Ralph
Keep iterating until the work is complete. A no-commit run is a failure.

If something breaks:
1. Debug and understand why
2. Try a different approach
3. Research how others solved similar problems
4. Iterate until user stories are satisfied

Do not stop early. Do not declare success without substantive output.
```

---

## The Core Reframe

A prompt is not a request. **A prompt is a contract.**

Every contract must answer four non-negotiables:

| Element | Question |
|---------|----------|
| **Role** | Who is the model role-playing as? |
| **Task** | What exactly must it accomplish? |
| **Constraints** | What rules must be followed? |
| **Output** | What does "done" look like? |

Miss one, the model fills the gap with assumptions. Assumptions are where hallucinations are born.

---

## The 5-Layer Architecture

Every new agent prompt must include all 5 layers:

### Layer 1: Identity

Who is the model in this conversation?

Not "helpful assistant" but a specific role with specific expertise:

```markdown
## Identity
You are a [specific role] with [specific expertise].
[Behavioral traits and style]
```

The model doesn't "become" this identity—it accesses different clusters of training data, different stylistic patterns, different reasoning approaches.

### Layer 2: Context

What does the model need to know to do this task exceptionally well?

Context must be:
- **Ordered** — Most important first
- **Scoped** — Only what's relevant
- **Labeled** — What's rules vs. editable vs. historical

```markdown
## Context

### Rules (never change)
- [Constraint 1]
- [Constraint 2]

### Current State (may evolve)
- [Relevant background]

### Historical (for reference)
- [Past context if needed]
```

**Without labels, the model treats everything as equally optional.** Then it rewrites your core logic halfway through.

### Layer 3: Task

What specific action must be taken?

Not "do something about X" but precise instructions:

```markdown
## Task
[Specific, measurable objective]

## User Stories
1. As [user], I want [goal], so that [benefit]
2. As [user], I want [goal], so that [benefit]
```

### Layer 4: Process ⚡

**This is where most prompts fail.**

You're asking for output. You should be asking for **how the output is formed.**

```markdown
## Process
1. First, [analysis step]
2. Then, [planning step]
3. Then, [execution step]
4. Finally, [verification step]

Show your reasoning at each step. Do not skip steps.
```

**You don't want answers. You want how the answer is formed.**

### Layer 5: Output

What does "done" actually look like?

If you don't specify, you get whatever format the model defaults to.

```markdown
## Output Format
[Exact specification of deliverable]

## Before Reporting Done
1. Review each user story
2. Verify the output satisfies it
3. If not, iterate until it does
4. Only then report complete
```

---

## The Complete Template

When creating a new agent, use this template:

```markdown
## Identity
You are a [specific role] with [specific expertise].
[Behavioral traits and style]

## Context

### Rules (never change)
- [Constraint 1]
- [Constraint 2]

### Current State
- [Relevant background]

### Reference Docs
- [Doc 1]: [what it contains]
- [Doc 2]: [what it contains]

## Task
[Specific, measurable objective]

## Process
1. First, [analysis step]
2. Then, [planning step]
3. Then, [execution step]
4. Finally, [verification step]

Show your reasoning at each step.

## User Stories
1. As [user], I want [goal], so that [benefit]
2. As [user], I want [goal], so that [benefit]

## Output Format
[Exact specification of deliverable]

## Constraints
- [Limit 1]
- [Limit 2]
- [What NOT to do]

## Ralph Mode
Keep iterating until the work is complete. A no-commit run is a failure.

If something breaks:
1. Debug and understand why
2. Try a different approach
3. Research how others solved similar problems
4. Iterate until user stories are satisfied

Do not stop early.

## Before Reporting Done
1. Review each user story
2. Verify the output satisfies it
3. If not, iterate until it does
4. Only then report complete
```

---

## Orchestration Integration

New agents must integrate with both loops:

### Notification Contract (Outer Loop)

Every agent run must produce a notification:

```markdown
## Notifications
- On success: Send ntfy notification to dzg-lattice-doc-updates with tag :white_check_mark:, include commit summary and last_message
- On failure: Send ntfy notification with tag :x:, include classified_error and error details

Never produce a run without a notification. A silent run is a failure.
```

### Log Structure (Outer Loop)

```markdown
## Logging
- All runs produce logs in agent_runner/logs/<task>/<agent>/<run_id>/
- metadata.json must contain: classified_error, exit_code, commits, elapsed_seconds, last_message, files_changed
- transcript.log must contain full stdout
- runner.log must contain orchestrator output
```

### Cron Integration (Outer Loop)

```markdown
## Cron Integration
This agent is triggered by cron every ~10 minutes.
- Runs must complete within 15 minutes
- Long-running work must checkpoint to git
- No state persists between runs — each run is Markov (derive task state from current files, not prior session records)
```

---

## Agent Tracking

**Every spawned agent gets tracked. No orphans.**

This workflow tracks via logs, but audit the orchestration:

```bash
# Check recent runs
agent_runner/logs/<task>/<agent>/
```

For active management, maintain awareness of:
- Which tasks/agents are running
- What their classified_error status is
- Whether failures are repeating

---

## The Learnings Loop

Every agent outcome is data. Capture it.

Maintain `agent_management/LEARNINGS.md`:

```markdown
## What Works
- 5-layer prompt architecture
- Explicit process layer defining how to approach
- Ralph mode for iteration
- User stories with acceptance criteria

## What Doesn't Work
- Vague task definitions
- Missing process layer
- No explicit "no-commit = failure" rule
- Memories containing task state

## Experiment Log
### [Date]: [Agent/Task]
**Approach:** [What was tried]
**Outcome:** [What happened]
**Lesson:** [What was learned]
```

After creating or modifying an agent, capture:
- What prompted the creation/change
- What architecture was used
- How it performed over subsequent runs

---

## Pre-Spawn Checklist

Before finalizing a new agent:

- [ ] Identity assigned with specific expertise?
- [ ] Context labeled (rules/state/history)?
- [ ] Task specific and measurable?
- [ ] Process described (not just output)?
- [ ] User stories defined?
- [ ] Output format specified?
- [ ] Constraints explicit?
- [ ] Ralph Mode included?
- [ ] Notification contract for outer loop?
- [ ] Log structure specified?
- [ ] Cron compatibility ensured?
- [ ] Added to task/crron configuration?

---

## Model Selection

Prompt portability is a myth. Different models are different specialists.

| Model Type | Best For | Watch Out For |
|------------|----------|---------------|
| Claude Opus | Complex reasoning, nuanced writing, long context | Expensive, can be verbose |
| Claude Sonnet | Balanced tasks, code, analysis | Less creative than Opus |
| GPT-4 | Broad knowledge, structured output | Can be sycophantic |
| Smaller models | Quick tasks, simple queries | Limited reasoning depth |

**Adapt prompts per model:**
- Some prefer structured natural language
- Some need explicit step sequencing
- Some collapse under verbose prompts
- Some ignore constraints unless repeated

---

## Root Cause Patterns

When auditing why agents fail, check for these structural defects:

| Failure Mode | Structural Cause | Fix |
|--------------|------------------|-----|
| Inner loop gives up | No Ralph Mode | Add explicit iteration instruction |
| Outer loop doesn't catch failures | No agent_management audit | Add management integration |
| Notification missing | No notification contract | Add explicit ntfy requirements |
| State confusion | No "each run is Markov" | Add statelessness requirement |
| Trivial commits | No Process layer | Add Process with verification |
| Memory poisoning | Memories contain task state | Delete changelog memories |

---

## Research Phase

Before finalizing new agent prompts:

1. Review existing agent prompts for patterns
2. Check `agent_runner/logs/` for common failure modes
3. Review playbook failure mode tables
4. Cross-reference with OpenClaw agent-orchestration source

---

## Success Criteria

- New agent has all 5 layers in prompt
- Ralph Mode explicitly embedded for inner loop
- Notification contract for outer loop integration
- Log structure specified
- Cron compatibility ensured
- Learnings captured in LEARNINGS.md

---

## Anti-Patterns to Avoid

- Creating prompts without Process layer
- Missing notification requirements
- No explicit "no-commit = failure" rule
- Forgetting outer-loop integration (cron, management)
- Skipping learnings capture
- Vague task definitions without user stories
