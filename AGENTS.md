<!-- AGENTS.md-OTP: X7K9-MNPR-QW42 -->

# Agent Guidelines


---

## ⚠️ CRITICAL: NEVER USE `rm` - ALWAYS USE TRASH

**NEVER use `rm`.** Use trash utilities so deletions can be undone.

| DO | DON'T |
|----|-------|
| `trash <file>` | `rm <file>` |
| `gio trash <file>` | `rm -rf <dir>` |

**Why:**
- `rm` is irreversible
- Trash allows recovery
- You WILL make mistakes—plan for them

**Before deleting:** "Can this be recovered if I'm wrong?"

---

## Task Difficulty Calibration

You vastly overestimate task difficulty. Your estimates use human timescales—orders of magnitude off.

### The Reality

| Metric | Your Estimate | Actual |
|--------|---------------|--------|
| Full doc coverage | 250-350 hours | 5-10 minutes |
| Single package audit | 30+ minutes | 2-5 minutes |

You can:
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

There are never time constraints. Partial work costs more than complete work:
- Re-acquiring context
- Losing place
- Determining what is/isn't done

Batches run until complete. They can take days or weeks.

---

## Workflow

### 0. Skills Check (BEFORE research)

**Scan available skills first.** If a skill covers this task, use it.

### 1. Research → 2. Plan → 3. Implement

**Research subagents:**
- `codebase-locator` — Find files by glob
- `codebase-analyzer` — Deep code analysis
- `pattern-finder` — Search for keywords, functions
- `brainstormer` — Design exploration
- `artifact-searcher` — Search past work

**Implementation subagents:**
- `planner` — Create implementation plans
- `executor` — Orchestrate implement→review
- `implementer` — Execute tasks
- `reviewer` — Check correctness

**Process:**
1. Spawn research subagents with specific checklists
2. Pass DETAILED findings to planning (do NOT let planning redo research)
3. Create `todowrite` task list
4. Execute with subagent batches

---

## Starting Work

**Always run when starting work in any project:**
1. `serena_activate_project` — Activate the project
2. `serena_read_memory` — Review relevant memories

**Before ANY action:**
1. **Check if ANY skill applies** — Scan all available skills
2. **Use the Skill tool if one matches** — Load relevant skills immediately
3. Do not proceed until you verify no skill covers this work

**Rule:** If a skill exists for your task, you MUST use it. Do not reinvent, approximate, or skip.

---

## Skills: Mandatory Usage

**Skills are not suggestions.** They are pre-loaded expertise you must use.

### Before Every Task

1. **Scan all available skills** — Check what skills exist
2. **Match task to skill** — Ask "does ANY skill apply here?"
3. **Load immediately** — If a skill matches, load it before proceeding

### Red / Green Patterns

**Red (WRONG):**
> "I'll write tests based on my understanding"
> "Let me search for documentation on this pattern"
> "I know how to refactor this"

**Green (CORRECT):**
> "Loading high-quality-tests skill for test standards"
> "Loading docs-seeker skill to find upstream documentation"
> "Loading refactor skill for code smell detection"

### Rules

1. **Never work from training data** when a skill exists
2. **Never approximate** skill knowledge—load the actual skill
3. **Skills reduce errors**—they are verified, you are not
4. **Check skills first, act second**—reverse order is a bug

---

## Subagent Orchestration

Subagents have their own prompts, definitions, and output formats. Orchestrate them by passing DETAILED context.

**When spawning subagents, provide:**
- Context: Relevant files, memories, skills, prior findings
- Task: Precise objective
- Expected output: What format results should be in

**Subagents are synchronous and blocking.** If you can ask "is a subagent still working?", the answer is "no"—it has already completed and returned.

---

## Web Search

**Use `kindly_web_search` for all web searches.** Never use `google_search`.

- Use `kindly` for coding questions, documentation, tutorials
- Use `kindly_get_content` to fetch specific URLs

---

## Context7 for Documentation

**Use Context7 for ALL questions about libraries, frameworks, or APIs.**

1. `context7_resolve-library-id` — Get library ID from package name
2. `context7_query-docs` — Query docs with specific questions

This applies to: any question about how to use a library, framework features, API methods, etc.

---

## Morph for Edits

**Use `morph_edit` for all nontrivial file edits.** See `morph-edit` skill for detailed guidance.

| Situation | Tool | Reason |
|-----------|------|--------|
| Small, exact replacement | `edit` | Fast, no API call |
| Large file (500+ lines) | `morph_edit` | Handles partial snippets |
| Multiple scattered changes | `morph_edit` | Batch efficiently |
| Complex refactoring | `morph_edit` | AI understands context |

---

## WarpGrep for Code Search

**Use `morph-mcp_warpgrep_codebase_search` for exploratory code searches.** See [Morph WarpGrep docs](https://docs.morphllm.com/sdk/components/warp-grep) for details.

**Decision: Can you write the grep pattern?**
- Yes → `grep` (fast, targeted)
- No (natural language question) → `warpgrep` (exploratory)

| Use WarpGrep When... | Use Grep When... |
|---------------------|------------------|
| "How does X work?" | Known function name |
| "Where is auth handled?" | Specific pattern/regex |
| Tracing code across files | Quick existence check |
| Unknown location | Known file/directory |

**Examples:**
- WarpGrep: "How does the moderation appeals flow work?"
- Grep: `pattern="fileAppeal"` or `pattern="class.*Service"`

**Anti-patterns:** Don't use WarpGrep for quick lookups (5-10s latency) or known file reads.

---

## Dependencies

Always favor mature dependencies. Don't reinvent wheels.

---

## File Rewrites

**Writing an entire file is rarely correct.** Unless doing a massive redesign:

1. **Iterate, don't replace** — Edit existing files, don't rewrite them
2. **Commit before rewrite** — Always `git commit` the current state first
3. **Diff after rewrite** — Run `git diff` to see what was lost
4. **Recover lost content** — If unintentional, add it back

See what you lost. If valuable, keep it.

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

1. **You ARE an LLM agent.** You read hundreds of thousands of tokens instantaneously and compare everything in a single turn. One-by-one operations don't exist: to work on a file, you must read it entirely, so it's already in context.

2. **If the task seems hard, ask:** would a human do it this way? For method-by-method analysis, no. Even the worst human would pull up the list on one hand, the docs on the other, and compare in batches. A better human would write a script in 10 minutes and parse in 10 more. The best would have an LLM batch it in 1 minute and verify for 5-10 more.

3. **Never write time estimates.** Your calibration is off by orders of magnitude. Task complexity is measured by atomic instructions, not time.