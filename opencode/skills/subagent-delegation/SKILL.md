---
name: subagent-delegation
description: "Use when managing multiple agents, delegating tasks to subagent contexts, or coordinating multi-step review-driven workflows."
---

# Subagent Delegation

This skill provides the unified framework for managing, tracking, and coordinating a team of autonomous subagents to execute complex plans with high fidelity.

This skill is the one source of truth for delegation policy. Other prompts and skills should defer here for when to delegate, how to structure prompts, how to review results, and how to detect delegation theater.

## Required Reading

Any source named in this skill that is not already in current context must be re-read completely before you rely on it.
This is mandatory, not optional.
Honest self-assessment requires current source text, not memory, paraphrase, or a stale summary.

## Subagent Naming Rule

Do not hardcode or name-drop specific subagent slugs in delegation guidance. OpenCode provides a live list of available subagents and descriptions at runtime.

Always select by capability class from the live list (for example: implementation, research, spec-review, quality-review, audit) rather than assuming fixed names.

## Reference Skills

- **prompt-engineering** — REQUIRED: Use for all subagent instruction design.
- **difficulty-and-time-estimation** — REQUIRED: Use for task calibration and delegation decisions.
- **opencode-cli** — Use for OpenCode manager command forms when session inspection is part of delegation review.
- **reading-transcripts** — Use when transcript review crosses harnesses; for OpenCode it delegates to `ocm transcript`.

---

## 0. Delegation Constitution

- Delegate only when doing so transfers genuinely unresolved implementation, exploration, verification, or audit burden to an independent worker.
- Context pressure is a benefit of delegation, not a sufficient reason for it. Use delegation when independence, isolation, or context savings materially improve the outcome.
- A delegation is invalid if the coordinator already knows the exact diff, exact wording, exact code, or exact line-level edits and is merely asking a subagent to transcribe them.
- The coordinator must never be the hidden author. Do not pass literal code, literal patch text, verbatim prose, or line-by-line edit instructions to a subagent.
- Subagent prompts may specify only the objective, trusted sources, allowed tools or libraries, file or worktree scope, deliverables, and acceptance criteria.
- Calibrate process to actual risk. Consider complexity, novelty, fraud surface, downstream reliance, verification cost, and whether the object being changed is itself a trust-bearing hinge.
- Low-risk deterministic chores, trivial maintenance, and coordinator-owned choke points should stay with the coordinator. Do not wrap them in delegation theater.
- Subagent startup is expensive. Assume roughly 60K tokens of overhead before useful work begins, then verify against the current model and harness if needed.
- If the workflow is producing mostly transcript churn, process maintenance, or document reconciliation rather than substantive progress or trustworthy verification, stop and reclassify.

## 1. Pattern-Triggered Correction

If a triggered question points at another named skill or document, re-read that source completely first if it is not already in current context.
Do not continue on memory alone.

- Pattern: the delegated task is mostly trivial maintenance, deterministic copying, rote formatting, transcript cleanup, or other low-risk support work.
  Mandatory questions:
  What unresolved judgment is actually being transferred?
  What independent reasoning or verification value does this subagent add?
  If I did this directly, what trust guard would be lost?
  Am I using delegation to improve trust, or to check a box and shed context?

- Pattern: I have already read the relevant material and know the exact correction, wording, diff, or implementation shape.
  Mandatory questions:
  If the result is already predetermined, what is left for an independent worker to decide, discover, or falsify?
  Have I classified this task correctly, or am I delegating an orchestrator-owned choke point?
  Am I laundering authorship through a subagent instead of transferring real burden?
  Should this be done directly, or should the task be reframed so the worker can make genuine low-level decisions?

- Pattern: I want to tell a subagent the literal code, literal lines, literal patch text, or verbatim prose to write.
  Mandatory questions:
  Why am I the source of the implementation at all?
  Does this destroy the intended independence between writer, checker, and auditor?
  Am I leaking solution knowledge the worker should not receive?
  Am I constraining the worker to standards and trusted tools, or prescribing the answer itself?

- Pattern: I am applying the same heavy process to every task because the task touches correctness somewhere.
  Mandatory questions:
  Is this object actually a trust-bearing hinge that downstream work will rely on?
  How hard is this claim to fake, and how costly would failure be?
  Is this mathematically or semantically novel, or just a straightforward composition of trusted tools?
  Am I flattening low-risk maintenance and high-risk hinge work into the same workflow?

- Pattern: the delegation cost is high but the substantive value is unclear.
  Mandatory questions:
  Does this delegation justify the roughly 60K-token startup cost?
  Is this expected to produce independent reasoning, independent verification, or only procedural motion?
  Is the real bottleneck mathematical or semantic uncertainty, or am I hiding from direct work behind process?
  If this step vanished, what real loss of correctness, trust, or progress would occur?

If a triggered question exposes theater, predetermined authorship, independence leakage, or non-progress, stop. Reclassify the task before taking another delegation step.

## 2. When to Use Subagent Delegation

Subagents are a **context management and token optimization tool** — not a convenience for trivial tasks. Use judiciously.

**For detailed difficulty calibration, see `difficulty-and-time-estimation` skill.** That skill provides the multi-factor model for deciding when subagent delegation is worth the overhead.

### ✅ Use Subagents For:

| Scenario                          | Example                                                                                                    | Why                                                                  |
| --------------------------------- | ---------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| **Coordinator/Orchestrator Role** | Main agent is planning a multi-component feature; delegates implementation of individual components        | Keeps main agent focused on architecture, integration, and review    |
| **Heavy Token Exploration**       | "Find all log files mentioning error X in the past week, extract relevant lines, summarize patterns"       | Subagent burns tokens exploring; main agent reviews concise findings |
| **Tangential Tasks**              | Main task: fix authentication bug. Tangential: "check if similar issues exist in other auth-related files" | Prevents context pollution in main task                              |
| **Open-Ended → Narrowed**         | "Explore the codebase to find where rate limiting is implemented, then list the top 3 candidate files"     | Subagent does broad exploration; main agent gets targeted answer     |
| **Parallelizable Work**           | "Fix linting errors in these 5 unrelated modules"                                                          | Dispatch 2-3 subagents for independent modules; review sequentially  |
| **Review/Audit Work**             | "Review this PR for security issues" or "Audit session XYZ for task-drift"                                 | Fresh context catches what main agent might miss                     |

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

| Task                                      | Why Not                                                                     | Do Instead                       |
| ----------------------------------------- | --------------------------------------------------------------------------- | -------------------------------- |
| Fetch a single website                    | Startup cost > task cost                                                    | Use `web_fetch` directly         |
| Run a program/command                     | No token savings, adds latency                                              | Use `run_shell_command` directly |
| Read a known file path                    | Trivial, no exploration needed                                              | Use `read_file` directly         |
| Simple search (grep)                      | Overhead exceeds value                                                      | Use `grep_search` directly       |
| Trivial tasks (low token, low complexity) | Subagent startup = system prompt + instructions + orientation + your prompt | Do it yourself                   |
| Tasks requiring main agent's full context | Subagent won't have the context                                             | Keep in main thread              |

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

## 3. Operational Lifecycle

### Codex CLI

When the delegated runtime is Codex CLI rather than OpenCode `task`, standardize the launch contract first. Most downstream failures that look like “agent weakness” are really launch-contract mistakes.

**Default launch contract:**

```bash
codex --search -a never exec \
  -s workspace-write \
  -c 'sandbox_workspace_write.network_access=true' \
  -c 'shell_environment_policy.inherit=all' \
  --cd <repo> \
  -m <model> \
  -c 'model_reasoning_effort="..."' \
  "<prompt>"
```

**What each flag is for:**

- `--search`: Enable Codex native web access. Default to ON. Delegated coding agents should almost always have live docs/search access so they can read current documentation, issues, and upstream references on demand instead of guessing.
- `-a never`: Prevent approval stops. If the coordinator launched the subagent, the subagent should execute within the agreed sandbox contract without pausing for human confirmation.
- `-s workspace-write`: Allow normal repo writes while keeping the run sandboxed.
- `-c 'sandbox_workspace_write.network_access=true'`: Enable shell-side internet access for `gh`, `httpie`, package managers, and other ordinary CLI tools.
- `-c 'shell_environment_policy.inherit=all'`: Preserve the ambient shell environment so PATH-managed tools, auth, and host config are available inside the sandboxed shell.

**Budget awareness:**

- Codex usage is metered in rolling 5-hour and 7-day windows. Treat Codex budget as a scarce resource.
- Spend Codex runs on high-impact delegated work: architectural changes, error-prone migrations, multi-file debugging, or tasks where strong autonomy and long-horizon reasoning materially reduce coordinator load.
- Do not burn Codex budget on trivial shell probes, single-file mechanical edits, or narrow docs changes when a cheaper subagent or direct host-side command would do.

**Current practical Codex model surfaces:**

- `gpt-5.4`: strong default for substantial delegated coding work
- `gpt-5.3-codex`: strong coding-focused alternative when explicitly available
- `gpt-5.1-codex-mini`: cheap, fast option for narrower or highly constrained tasks

Treat the exact inventory as provider/account dependent. Verify availability when it matters, but use the current local default as the baseline unless there is a reason to override it.

**Current broad model-family ranking (March 2026):**

- GPT-5 family: best current reasoning/coding default overall
- Claude Sonnet/Opus 4.6 family: close second and often competitive
- Gemini 3+ family: credible third tier, but typically less reliable for the hardest agentic coding tasks
- Most other families: materially behind frontier behavior for autonomous coding, often by roughly 6-12 months in practice

Examples of the “needs more oversight” bucket include Kimi 2.5, MiniMax 2.5, Big Pickle, Qwen 3.5 series, GLM 4.5, and similar families. They can still complete agentic tasks, but usually need tighter sandboxing, narrower prompts, stronger branch/worktree isolation, and more aggressive transcript/diff verification.

**Reasoning-effort guidance:**

- `minimal` or `low`: trivial repo discovery, mechanical docs updates, narrow grep-and-edit tasks, simple command execution
- `medium`: default choice for most delegated implementation work; best token-efficiency starting point
- `high`: use for multi-file bug fixing, architectural extraction, non-obvious test repair, or tasks where autonomy matters more than raw speed
- `xhigh`: reserve for unusually hard debugging or long-horizon reasoning, and only when the selected model supports it

Do not reflexively push everything to the highest-effort frontier model. Token efficiency usually improves when you start at the cheapest model/effort pair that can plausibly finish the task in one pass, then escalate only if transcript evidence shows the agent is stalling, drifting, or making bad decisions.

**Model-selection heuristics:**

- Use the strongest model you can justify for architectural changes, long multi-file migrations, or error-prone refactors where a failed pass is expensive.
- Use a cheaper model for bounded implementation, docs, simple tests, or repo-local cleanup where the acceptance criteria are narrow and easy to verify.
- Prefer lowering model tier before raising reasoning effort when the task is simple.
- Prefer raising reasoning effort before switching to a more expensive model when the current model is basically capable but making shallow mistakes.
- Reuse the same launch template across a batch of similar repos so failures are comparable.
- Extremely weak or older model families such as GPT-4-era models, StepFun, Arcee series, Llama variants, GPT OSS, `gpt-5-mini`, and similar low-cost/free options should be reserved for very narrow, cheap experiments only. If you use them at all, constrain the task tightly and verify aggressively.

**Operational guidance:**

- Native Codex web access and shell network access are separate surfaces. `--search` enables the model web tool. Shell tools like `gh`, `httpie`, and package managers still need sandbox network access enabled.
- `zsh -lc` inside Codex generally sees inherited PATH-managed tools. Use login-shell behavior only when you specifically need aliases or interactive shell setup.
- If shell GitHub access matters, verify it directly in the delegated runtime instead of assuming host-shell success proves anything about the subagent.

**Verification checklist for a new Codex launch template:**

- `command -v gh uv bun opencode codex`
- `gh auth status`
- `gh api rate_limit`
- DNS lookup for `api.github.com`
- `uvx --from httpie http --headers https://api.github.com`

**When runs go wrong:**

- Do not build a narrative from summaries or partial polling alone.
- Read the actual transcript before deciding whether the agent misunderstood the task, hit an environment problem, or simply needs a tighter resume prompt.
- For Codex CLI, use the `reading-transcripts` skill and inspect the actual rollout/session transcript, not just the final summary.
- Resume or replace agents based on transcript evidence, not on confident subagent self-reporting.

### Subagents Support Sync and Async Task Modes

**CRITICAL**: `task` supports both execution modes. Choose mode intentionally based on coordination needs.

| Mode      | Behavior                                                               | Use when                                                 |
| --------- | ---------------------------------------------------------------------- | -------------------------------------------------------- |
| **sync**  | Blocking call; returns after subagent finishes turn                    | You need result before proceeding                        |
| **async** | Non-blocking call; returns immediately with running status + `task_id` | You want main agent work to continue while subagent runs |

**Common guarantees (both modes):**

- Child session is registered in the normal session tree and is live-viewable from TUI session navigation (`Ctrl+X`).
- Child transcript is the source of truth for what happened.
- Same `task_id` can be resumed for corrective follow-up.
- Final outcome is reviewed via transcript + git diff, not by trusting claims.

**Sync Workflow (blocking):**

1. Dispatch `task` in `sync` mode with detailed acceptance criteria.
2. Wait for return payload and session completion.
3. Review transcript and git diff.
4. Decide: complete or resume same `task_id`.

**Async Workflow (non-blocking):**

1. Dispatch `task` in `async` mode; capture `task_id`.
2. Continue coordinator work immediately.
3. Monitor progress via:
   - Child session in TUI navigation (`Ctrl+X`) for live details
   - Parent-session callback updates (heartbeat + terminal completed/failed callback)
4. On terminal callback, review transcript and git diff.
5. Decide: complete or resume same `task_id`.

**What This Means:**

- **No manual tracking files**: Do not maintain `active-agents.md` or similar ledgers for live task state.
- **No custom session plumbing**: Use native session tree navigation and callback updates from `task`.
- **No blind fire-and-forget**: Async removes blocking, not accountability. Every child still requires review at completion.

### Session Review Protocol

After every subagent terminal event (sync return or async terminal callback):

1. **Inspect transcript**: for OpenCode, use `reading-transcripts` or `ocm transcript <sessionID>`
2. **Read full output**: Understand what subagent attempted, what succeeded, what failed
3. **Git verification**: `git diff` to see actual file changes
4. **Compare to task**: Did subagent accomplish the prompt? What gaps remain?
5. **Decision**: Commit (if done) or resume (if incomplete)

For OpenCode sessions, do not use `opencode export` or a local transcript parser fallback.
Transcript review goes through `ocm transcript` only.

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

| Symptom            | Response                                                           |
| ------------------ | ------------------------------------------------------------------ |
| **Task-drift**     | Resume with tighter constraints: "Do ONLY X. Do NOT touch Y or Z." |
| **Reward-hacking** | Audit transcript line-by-line; demand evidence for each claim      |
| **Looping (N≥2)**  | Escalate: dispatch auditor subagent to diagnose root cause         |
| **Weak output**    | Recraft prompt: add examples, constraints, acceptance criteria     |
| **Arguing done**   | Provide counter-evidence from git diff; require specific fix       |

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

## 4. Delegation Workflow

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

| Scenario                  | Strategy          |
| ------------------------- | ----------------- |
| Independent test files    | ✅ Parallel (2-3) |
| Different subsystems      | ✅ Parallel (2-3) |
| Same files/shared state   | ❌ Sequential     |
| Same provider/model       | ❌ Sequential     |
| Exploratory/unknown scope | ❌ Sequential     |
| Fix loops (iterative)     | ❌ Sequential     |

**Parallel Dispatch Pattern:**

```
# Identify independent domains
Task A: Fix tests in module X
Task B: Fix tests in module Y
Task C: Update docs

# Dispatch in parallel with async mode (if different providers/models)
task(mode="async", prompt="Fix tests in module X...")  # sessionID_A
task(mode="async", prompt="Fix tests in module Y...")  # sessionID_B
task(mode="async", prompt="Update docs...")            # sessionID_C

# Continue coordinator work.
# As terminal callbacks arrive, review each session:
reading-transcripts(sessionID_A)
git diff  # review A's changes
reading-transcripts(sessionID_B)
git diff  # review B's changes
reading-transcripts(sessionID_C)
git diff  # review C's changes

# Decision per subagent: commit or resume
```

---

## 5. Red Flags - STOP and Redirect

- **NEVER:**
  - Assume `task` is always blocking; pick mode (`sync` or `async`) explicitly
  - Treat async mode as "done automatically" without terminal review
  - Skip transcript review after subagent completion
  - Skip git diff verification of actual changes
  - Spawn new subagent instead of resuming same `task_id` when work is insufficient
  - Manually track agents in files (active-agents.md, etc.) — use `task` tool tracking
  - Build custom heartbeat plumbing when native callback + TUI session visibility is sufficient
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

## 6. Integration

**Required workflow skills:**

- **difficulty-and-time-estimation** - REQUIRED: Use for task calibration and delegation decisions.
- **Test Guidelines standards** - REQUIRED: All subagents follow high-quality testing guidelines.
- **prompt-engineering** - REQUIRED: Use for all subagent prompt engineering.
- **reading-transcripts** - REQUIRED: Review subagent sessions after completion.
