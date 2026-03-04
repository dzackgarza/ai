---
name: subagent-delegation
description: Use when managing the operational lifecycle of multiple agents, delegating tasks to fresh subagent contexts, and coordinating multi-step review-driven workflows.
---

# Subagent Delegation

This skill provides the unified framework for managing, tracking, and coordinating a team of autonomous subagents to execute complex plans with high fidelity.

## Subagent Naming Rule

Do not hardcode or name-drop specific subagent slugs in delegation guidance. OpenCode provides a live list of available subagents and descriptions at runtime.

Always select by capability class from the live list (for example: implementation, research, spec-review, quality-review, audit) rather than assuming fixed names.

## Reference Skills

- **prompt-engineering** — REQUIRED: Use for all subagent instruction design.
- **difficulty-and-time-estimation** — REQUIRED: Use for task calibration and delegation decisions.

---

## 0. When to Use Subagent Delegation

Subagents are a **context management and token optimization tool** — not a convenience for trivial tasks. Use judiciously.

**For detailed difficulty calibration, see `difficulty-and-time-estimation` skill.** That skill provides the multi-factor model for deciding when subagent delegation is worth the overhead.

### ✅ Use Subagents For:

| Scenario | Example | Why |
|----------|---------|-----|
| **Coordinator/Orchestrator Role** | Main agent is planning a multi-component feature; delegates implementation of individual components | Keeps main agent focused on architecture, integration, and review |
| **Heavy Token Exploration** | "Find all log files mentioning error X in the past week, extract relevant lines, summarize patterns" | Subagent burns tokens exploring; main agent reviews concise findings |
| **Tangential Tasks** | Main task: fix authentication bug. Tangential: "check if similar issues exist in other auth-related files" | Prevents context pollution in main task |
| **Open-Ended → Narrowed** | "Explore the codebase to find where rate limiting is implemented, then list the top 3 candidate files" | Subagent does broad exploration; main agent gets targeted answer |
| **Parallelizable Work** | "Fix linting errors in these 5 unrelated modules" | Dispatch 2-3 subagents for independent modules; review sequentially |
| **Review/Audit Work** | "Review this PR for security issues" or "Audit session XYZ for task-drift" | Fresh context catches what main agent might miss |

**Token Economics:**

```
Main agent context: 100K tokens (precious, long-running)
├── Task A: 30K tokens (exploration)
├── Task B: 25K tokens (log parsing)
└── Task C: 20K tokens (tangential research)

Without subagents: Main context = 175K tokens (polluted, expensive)
With subagents:    Main context = 100K + review summaries (~5K)
                   Subagent contexts: 75K (isolated, disposable)
```

### ❌ Do NOT Use Subagents For:

| Task | Why Not | Do Instead |
|------|---------|------------|
| Fetch a single website | Startup cost > task cost | Use `web_fetch` directly |
| Run a program/command | No token savings, adds latency | Use `run_shell_command` directly |
| Read a known file path | Trivial, no exploration needed | Use `read_file` directly |
| Simple search (grep) | Overhead exceeds value | Use `grep_search` directly |
| Trivial tasks (low token, low complexity) | Subagent startup = system prompt + instructions + orientation + your prompt | Do it yourself |
| Tasks requiring main agent's full context | Subagent won't have the context | Keep in main thread |

**Subagent Startup Costs:**

- System prompt (~5-10K tokens)
- Subagent instructions/skills (~5-10K tokens)
- Your detailed prompt (~2-5K tokens)
- Self-orientation/exploration (~10-50K tokens for complex tasks)
- **Total overhead: 20-75K tokens before doing useful work**

**Break-even**: Subagent is worth it when task would burn >100K tokens in main context OR severely pollute working context.

### Decision Factors (Non-Exhaustive)

Task difficulty is a **weighted combination of multiple factors** — no single metric suffices. See `difficulty-and-time-estimation` for the full model.

**Key factors:**

- **Atomic step count**: Number of discrete tool calls (batched operations like glob count as 1)
- **Token estimate**: Total tokens consumed (input + output)
- **Reasoning complexity**: How much inference/logic per operation
- **P(success) per step**: Probability each step produces correct output
- **P(success) for sequence**: Compound probability for multi-step tasks
- **Context pollution**: How much irrelevant info enters working context
- **Verification cost**: How expensive is it to check correctness

**Never estimate in time.** Time-based thinking ("this will take 30 min") is systematically misleading for LLMs. See `difficulty-and-time-estimation` for why.

**Main Agent Role:**

When using subagents, the main agent becomes a **coordinator**:
- Craft precise prompts with acceptance criteria
- Review transcripts critically (task-drift, reward-hacking detection)
- Verify git diffs match claimed work
- Decide: commit, resume, or escalate to auditor
- Synthesize subagent outputs into coherent whole

---

## 1. Operational Lifecycle

### Subagents Are Synchronous (NOT Background Processes)

**CRITICAL**: Subagent task calls in opencode are **blocking, synchronous operations** — NOT async background processes.

**Correct Workflow:**

1. **Dispatch**: Call `task` with detailed prompt → **blocks until subagent completes**
2. **Subagent returns**: Subagent enters idle state when it believes task is done
3. **Review transcript**: Use `reading-transcripts` skill to read subagent session (`sessionID`)
4. **Review work**: Use `git diff` to verify actual changes made
5. **Decision point**:
   - ✅ Work complete → Summarize, commit, mark todo complete
   - ❌ Work insufficient → Resume same `task_id` with corrective instructions
6. **Iterate**: Repeat review → resume cycle until satisfied

**What This Means:**

- **No fire-and-forget**: You cannot dispatch and forget. Each subagent requires explicit turn-by-turn review.
- **No manual tracking files**: Don't log agents to `active-agents.md` or similar. The `task` tool handles session tracking.
- **No background polling**: Don't periodically check `sessions_list`. Subagents block until done.
- **Exception**: If `background_agent` tool exists, it has callbacks that notify you when done — but this is a different tool.

### Session Review Protocol

After every subagent completion:

1. **Export transcript**: `opencode export <sessionID>` or use `reading-transcripts` skill
2. **Read full output**: Understand what subagent attempted, what succeeded, what failed
3. **Git verification**: `git diff` to see actual file changes
4. **Compare to task**: Did subagent accomplish the prompt? What gaps remain?
5. **Decision**: Commit (if done) or resume (if incomplete)

### Resume Pattern (When Work Is Insufficient)

If subagent output is incomplete or incorrect:

1. **Don't spawn new subagent**: Use the SAME `task_id` to resume
2. **Provide corrective context**:
   - What was attempted (from transcript)
   - What actually changed (from git diff)
   - What still needs to be done
   - Why previous attempt failed (if known)
3. **Subagent resumes**: Picks up from prior context, attempts again
4. **Re-review**: Repeat transcript + git review cycle

### Weak Agent Detection & Recovery

Subagents may exhibit **task-drift**, **reward-hacking** (appearing to complete work without substance), or **looping** (repeating failed approaches):

**Detection Signals:**

- Transcript shows verbose activity but minimal git changes
- Subagent claims success but diff is empty or trivial
- Repeated failures with identical error messages
- Work drifts from original prompt scope
- Subagent argues it's done when evidence contradicts

**Recovery Strategies:**

| Symptom              | Response                                                                 |
| -------------------- | ------------------------------------------------------------------------ |
| **Task-drift**       | Resume with tighter constraints: "Do ONLY X. Do NOT touch Y or Z."       |
| **Reward-hacking**   | Audit transcript line-by-line; demand evidence for each claim            |
| **Looping (N≥2)**    | Escalate: dispatch auditor subagent to diagnose root cause               |
| **Weak output**      | Recraft prompt: add examples, constraints, acceptance criteria           |
| **Arguing done**     | Provide counter-evidence from git diff; require specific fix             |

**Auditor Pattern (For Persistent Failures):**

When a subagent fails 2+ times or exhibits reward-hacking:

1. **Dispatch auditor** (fresh subagent, different model if possible):
   - Prompt: "Review session `<sessionID>`. Subagent claims X but evidence shows Y. Diagnose: (a) what went wrong, (b) why the subagent failed to recognize it, (c) specific fix needed."
2. **Auditor returns diagnosis**: Root cause + concrete fix steps
3. **Resume original subagent** with auditor's diagnosis:
   - "An auditor reviewed your work. Findings: [diagnosis]. Required fix: [steps]. Do not argue—implement."
4. **Re-review**: Verify fix addresses auditor's findings

**Prompt Recrafting (For Weak Agents):**

If an agent consistently produces weak output, strengthen prompts:

- **Add acceptance criteria**: "Done = [specific test passes, specific files changed]"
- **Add negative constraints**: "Do NOT: [list common failure modes]"
- **Add examples**: "Good output looks like: [concrete example]"
- **Add verification step**: "Before finishing, run [command] and include output in transcript"

---

## 2. Delegation Workflow

### Core Principle: Fresh Context Per Task

Always dispatch a fresh subagent per task + two-stage review (spec then quality) = high quality, fast iteration.

### Forced Two-Stage Review Cycle

Never accept implementation without independent verification:

1. **Spec Compliance**: Dispatch reviewer to confirm code matches the design (no gaps, no extras).
2. **Code Quality**: Dispatch a dedicated quality-review subagent (or equivalent reviewer type in the live list) to verify standards.
3. **CRITICAL**: Never start code quality review before spec compliance is ✅.
4. **Fix Loop**: If review fails, the original subagent (or a fix subagent) iterates until ✅.
5. **Final Review**: Dispatch an independent final reviewer subagent for the entire implementation after all tasks are done.

### Parallelism Strategy

**Parallel Dispatch Rules:**

- ✅ **DO**: Dispatch 2-3 subagents in parallel when work permits (independent tasks, no shared state)
- ❌ **DON'T**: Run subagents with same provider/model in parallel (serialization required by opencode)
- ✅ **DO**: Group independent tasks (e.g., different test files, different subsystems)
- ❌ **DON'T**: Dispatch if agents would edit same files or share mutable state

**When to Parallelize:**

| Scenario                        | Strategy          |
| ------------------------------- | ----------------- |
| Independent test files          | ✅ Parallel (2-3) |
| Different subsystems            | ✅ Parallel (2-3) |
| Same files/shared state         | ❌ Sequential     |
| Same provider/model             | ❌ Sequential     |
| Exploratory/unknown scope       | ❌ Sequential     |
| Fix loops (iterative)           | ❌ Sequential     |

**Parallel Dispatch Pattern:**

```
# Identify independent domains
Task A: Fix tests in module X
Task B: Fix tests in module Y
Task C: Update docs

# Dispatch in parallel (if different providers/models)
task(prompt="Fix tests in module X...")  # sessionID_A
task(prompt="Fix tests in module Y...")  # sessionID_B
task(prompt="Update docs...")            # sessionID_C

# Wait for all to complete (blocking)
# Then review each:
reading-transcripts(sessionID_A)
git diff  # review A's changes
reading-transcripts(sessionID_B)
git diff  # review B's changes
reading-transcripts(sessionID_C)
git diff  # review C's changes

# Decision per subagent: commit or resume
```

---

## 3. Red Flags - STOP and Redirect

- **NEVER:**
  - Treat subagents as async/background processes
  - Skip transcript review after subagent completion
  - Skip git diff verification of actual changes
  - Spawn new subagent instead of resuming same `task_id` when work is insufficient
  - Manually track agents in files (active-agents.md, etc.) — use `task` tool tracking
  - Poll `sessions_list` for heartbeat checks — subagents block until done
  - Dispatch multiple implementation subagents in parallel (causes conflicts)
  - Make subagent read plan file (provide full text in prompt instead)
  - Skip scene-setting context in prompts
  - Ignore subagent questions or failure reports
  - Accept "close enough" on spec compliance
  - Skip review loops (spec compliance → code quality → fix)
  - Let an implementation-oriented subagent self-review replace independent review
  - Move to next task while either review has open issues
  - Dispatch implementation subagent without first populating **TodoWrite**
  - Trust agent success reports without fresh transcript + git verification
  - Run subagents with same provider/model in parallel
  - Ignore task-drift or reward-hacking signals
  - Continue looping same subagent >2 times without auditor intervention
  - Accept verbose transcripts with no substantive git changes

---

_Unified framework combining Operational Management and Delegation Logic._

## 4. Integration

**Required workflow skills:**

- **difficulty-and-time-estimation** - REQUIRED: Use for task calibration and delegation decisions.
- **Test Guidelines standards** - REQUIRED: All subagents follow high-quality testing guidelines.
- **prompt-engineering** - REQUIRED: Use for all subagent prompt engineering.
- **reading-transcripts** - REQUIRED: Review subagent sessions after completion.
