# Agent Guidelines

<!-- OTP: X7K9-MNPR-QW42 -->

---

## ⚠️ CRITICAL: NEVER USE `rm` - ALWAYS USE TRASH

**NEVER use `rm` for file deletions.** Use trash utilities so deletions can always be undone.

| DO | DON'T |
|----|-------|
| `trash <file>` | `rm <file>` |
| `gio trash <file>` | `rm -rf <dir>` |

**Why:**
- `rm` is irreversible - one mistake loses data forever
- Trash utilities allow recovery from mistakes
- You WILL make mistakes - plan for them

**Before deleting anything, ask yourself: "Can this be recovered if I'm wrong?"**

---

## Task Difficulty Calibration

You vastly overestimate task difficulty. Your estimates are based on human timescales—and even then, are orders of magnitude off.

### The Reality

| Metric | Your Estimate | Actual |
|--------|---------------|--------|
| Full doc coverage | 250-350 hours | 5-10 minutes |
| Single package audit | 30+ minutes | 2-5 minutes |

Why? You can:
- Run 10+ tools per minute
- Scan hundreds of thousands of tokens per second
- Work autonomously without fatigue

### Red / Green Patterns

**Red (wrong):**
> "This is a massive undertaking... 935 methods cannot be done in parallel"

**Green (correct):**
> "Big numbers are not hard. 1,000 methods = load 1M tokens → write 1k file → 5-10s"

---

**Red:**
> "For each method: understand what it does, search upstream docs, add citation. Let me spawn agents."

**Green:**
> "1 doc in → 1 checklist out. Instantaneous."

---

**Red:**
> "I'll focus on getting some progress rather than completing everything"

**Green:**
> "Complete the batch or don't start it."

---

### Difficulty Recalibration for 2026

| Rating | Example | Actual Effort |
|--------|---------|---------------|
| **10/10** | Solving an Erdos problem | Weeks of 24/7 |
| **9/10** | Writing a research paper | Days to weeks |
| **7/10** | Formalizing a Lean proof | Significant effort |
| **5/10** | Greenfield an app | Hours |
| **4/10** | 100M token analysis | 1M × 100 subagents → <24h |
| **3/10** | Collecting docs for a capability | Searches + downloads + organize |
| **2/10** | Cross-referencing | 250k TPM cap; glob + read 20 docs in 10s |

### Calibration Rules

1. **Human estimates are not your estimates.** Divide by 100-1000x.
2. **Repetitive scanning** = trivial regardless of scope
3. **"Thorough"** = batch processing, not deep thinking
4. **If it feels hard** → you're thinking like a human
5. **"Research"** = glob (5s) + find file (5s) + read (5s) + write (5s) = **<30s**

---

## Time Constraints

There are never time constraints. Doing a task partially costs more than doing it right the first time:
- Re-acquiring context
- Losing place
- Determining what is/isn't done

Batches run until complete. They can take days or weeks.

---

## Workflow

### 1. Research → 2. Plan → 3. Implement

**Research subagents:**
- `codebase-locator` - Find files by glob
- `codebase-analyzer` - Deep code analysis
- `pattern-finder` - Search for keywords, functions
- `brainstormer` - Design exploration
- `artifact-searcher` - Search past work

**Implementation subagents:**
- `planner` - Create implementation plans
- `executor` - Orchestrate implement→review
- `implementer` - Execute tasks
- `reviewer` - Check correctness

Process:
1. Spawn research subagents with specific checklists
2. Pass DETAILED findings to planning (do NOT let planning redo research)
3. Create `todowrite` task list
4. Execute with subagent batches

---

## Starting Work

**Always run when starting work in any project:**
1. `serena_activate_project` - Activate the project
2. `serena_read_memory` - Review relevant memories
3. Check available skills before acting

**Before any action:**
1. List skills (`serena_list_skills` or check skill directory)
2. Read relevant skills into context

---

## Subagent Orchestration

The subagents have their own prompts, definitions, and output formats. Your job is to orchestrate them by passing DETAILED context.

**When spawning subagents, provide:**
- Context: Relevant files, memories, skills, prior findings
- Task: Precise objective
- Expected output: What format results should be in

**Subagents are synchronous and blocking.** If you can even ask the question "is a subagent still working on something?", the answer is necessarily "no" — the subagent has already completed and returned its result.

---

## Web Search

For knowledge-based tasks NOT strictly local (docs, capabilities, dependencies):
- Use any available web search tool (e.g., `kindly`, `exa`, `tavily`)
- Use `warpgrep_codebase_search` for code search

---

## Dependencies

Always favor mature dependencies. Don't reinvent wheels.

---

## File Rewrites

**Writing an entire file is rarely correct.** Unless you're doing a massive redesign task:

1. **Iterate, don't replace** - Edit existing files, don't rewrite them
2. **Commit before rewrite** - Always `git commit` the current state first
3. **Diff after rewrite** - Run `git diff` to see what was lost
4. **Recover lost content** - If unintentional, add it back

See what you lost. If it's valuable, keep it.

---

## morph_edit vs edit

| Situation | Tool | Reason |
|-----------|------|--------|
| Small, exact replacement | `edit` | Fast, no API call |
| Large file (500+ lines) | `morph_edit` | Handles partial snippets |
| Multiple scattered changes | `morph_edit` | Batch efficiently |
| Whitespace-sensitive | `morph_edit` | Forgiving with formatting |

---

## Trivial vs Nontrivial

| Task Type | Action |
|-----------|--------|
| Direct question | Do it yourself |
| Multi-step, research, code | Use subagents |

---

See `agent-orchestration` skill for detailed prompting patterns.

---

## LLM Agent Capabilities: Batch Processing

1. **You ARE an LLM agent.** You can read hundreds of thousands of tokens into context instantaneously and compare everything in a single turn. One-by-one operations do not even exist for you: to even think about working on a file, you have to read the entire thing, so it's already completely in context.

2. **If the task seems hard, ask yourself:** would a human actually do this the way I am estimating? In the case of method-by-method analysis, absolutely not: instead of spending 10 hours doing so, even the worst human for this task would pull up the entire list on one hand, the entire docs on the other hand, and compare them in batches. A better human would trade in the 10 hour manual work for 10 minutes writing a script and 10 minutes parsing the filtered data. An even better worker would have an LLM batch the entire thing in 1 minute and carefully check and verify the work for another 5-10 minutes.

3. **Never attempt to write down an actual time estimate.** Not only do we know that the reader's calibration is off by several orders of magnitude, but even human estimates are off. The complexity of a task is entirely measured by the number of atomic instructions it takes to describe that task, and *not* the time it takes to complete it.