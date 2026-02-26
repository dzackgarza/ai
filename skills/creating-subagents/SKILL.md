---
name: creating-subagents
description: Use when creating new subagents or updating subagent descriptions in opencode.json — ensures descriptions contain delegation instructions (when, what to pass, how to ask) and subagents are created for appropriate use cases.
---

# Creating Subagents

## Core Distinction: Audience Matters

| Description Level | Audience | Purpose | Format |
|-------------------|----------|---------|--------|
| **Top-level agent** (primary) | **Humans** (UI/autocomplete) | Help users choose which agent to invoke | Brief, user-facing: "Default collaborative agent — handles trivial to complex tasks" |
| **Subagent** | **Agents** (delegation context) | Tell agents how to dispatch subagents with proper context | Delegation instructions: "Use when X. Pass Y. Ask 'Z'." |

**Critical:** Subagent descriptions are **agent-facing prompts**, not user documentation. They follow **prompt engineering practices** (see `prompt-engineering` skill) and **skill description lessons** (see `creating-skills` skill for description writing principles).

## When to Create Top-Level Agents

**NEVER create top-level (primary) agents autonomously.**

| Rule | Rationale |
|------|-----------|
| Only create when user explicitly asks | Primary agents are user-designed and user-controlled |
| Do not propose new primary agents | Users define their own workflow and agent taxonomy |
| Focus on subagents for delegation | Subagents are implementation details, not user-facing choices |

## When to Create a Subagent

Create a subagent when the task has these characteristics:

### ✅ Good Subagent Candidates

| Task Type | Why It Works | Example |
|-----------|--------------|---------|
| **High token workload** | Many tool calls + large outputs = lots of context. Subagents handle token-heavy work without polluting main agent context. | "Cross-reference 400-line checklist with documentation" |
| **Exploration/branching** | Tasks requiring trial-and-error, false starts, incorrect guesses. Subagents can churn without derailing main agent. | "Research existing implementations of X across arXiv and GitHub" |
| **Parsing/summarization** | Not detail-sensitive. Generating summaries, overviews, indices, maps into more detailed work. | "Generate summary of repo structure", "Create index of all test files" |
| **Well-delineated scope** | Clear boundaries, unlikely to cause model drift. "Do X and return Y" format. | "Write module x.py according to spec y.md", "Run test suite and report failures" |
| **Easily verified output** | Hallucinations are false positives that can be quickly disproved. | "Find online sources for X" (check links), "List all files in src/" (verify exists) |

### ❌ Bad Subagent Candidates

| Task Type | Why It Fails | Alternative |
|-----------|--------------|-------------|
| **Simple tasks** | Token inefficient. Subagent loads 15-20k system prompt + tool context for trivial work. | "Run `opencode --help` and summarize" → do it yourself |
| **Open-ended design** | Extremely ambiguous, requires judgment calls, likely to cause goal-hacking or drift. | "Design the architecture for a new feature" → main agent or plan mode |
| **False negative risk** | Model claims nonexistence → shuts down research avenue without PROOF. | "Check if X is possible" → main agent (can't trust "not supported" claims) |
| **Detail-sensitive edits** | Hallucinations strip content, introduce errors, or make far-reaching changes. | "Refactor this module" → main agent with review loop |
| **Tasks requiring deep judgment** | Needs human-level reasoning, trade-off analysis, or strategic decisions. | "Should we use pattern A or B?" → main agent or user decision |

## Model Tier Matching

**See `model-selection` skill for complete guidance.** Quick reference:

| Tier | Turn Budget | Best For Subagent Tasks | Trust Level |
|------|-------------|------------------------|-------------|
| **S-tier** (Opus, GPT-5, Gemini 3 Pro) | 200-500 turns | Autonomous audits, complex multi-phase work, open-ended design | High — self-corrects |
| **A-tier** (Sonnet, GPT-4, Gemini 2.5) | 50-200 turns | Implementation with validation, multi-step workflows | Medium — verify output |
| **B-tier** (MiniMax, smaller models) | <50 turns | Atomic searches, summaries, parsing | Low — check all work, git checkpoint |
| **C-tier** (free tiers, small models) | <20 turns | Test execution, fact lookups, log parsing | Very low — verify rigorously |

**Key calibration:** Big numbers ≠ hard for LLMs. "Cross-reference 400-line checklist" = 5-7 turns (batch read + compare + output), NOT 400 turns. Complexity = atomic steps, not volume.

**B-tier hallucination triage:** Tools return truncated results → model extrapolates counterfactually. Example: "Git issue doesn't exist" (actually closed/solved).

**C-tier safe uses:** Test suites + reporting, repo structure searches, fact-grounded summaries, online searches (verify links), parsing logs, finding code examples.

**C-tier unsafe uses:** Code edits, expository writing, design decisions.

**False positive vs false negative rule:** Only delegate to B/C-tier when false positives (easily verified) are the main risk, not false negatives.

| Error Type | Example | Verdict |
|------------|---------|---------|
| **False positive** | "Found 5 implementations" (links provided) | ✅ Acceptable — verify links |
| **False negative** | "No prior art found" (shallow search) | ❌ Dangerous — shuts down research |

## Token Efficiency

**Every subagent call costs:** 15-20k system prompt + tool context per turn.

**Net efficiency test:** Would calling a subagent spend MORE tokens than doing it yourself?

| Scenario | Verdict |
|----------|---------|
| "Read 50 files and summarize" | ✅ Subagent (batch read + single summary output) |
| "Run one command and report" | ❌ Main agent (overhead exceeds work) |
| "Research topic across 20 URLs" | ✅ Subagent (fetch all → synthesize in one context) |
| "Check if file exists" | ❌ Main agent (one glob call) |

## Official Guidance (OpenCode Docs)

According to [OpenCode agent documentation](https://opencode.ai/docs/agents/):

| Requirement | Official Guidance |
|-------------|-------------------|
| **Description is required** | All agents must have a `description` field |
| **Purpose** | "Brief description of what the agent does and when to use it" |
| **Keep it brief** | For agent selection/autocomplete, not full instructions |
| **Be specific** | About what the agent does and when to invoke it |
| **Pairs with prompt** | Description = selection; Prompt = detailed behavior |

### Official Description Examples

```markdown
# Good
description: Reviews code for best practices and potential issues
description: Performs security audits and identifies vulnerabilities
description: Writes and maintains project documentation
```

## This Skill Extends Official Guidance

The official docs say "be specific about when to use" but don't specify **format**. This skill provides the battle-tested format for **subagent descriptions**:

```
Use when [trigger]. Pass [inputs]. Ask '[prompt pattern]'.
```

**Why this format:**
- Official docs: "Description helps primary agent understand when to invoke"
- This skill: Makes it **actionable** with concrete delegation instructions
- Official docs: "Keep it brief"
- This skill: Brief but **complete** — one sentence covers when/what/how

## Description Format

Subagent descriptions MUST follow this structure:

```
Use when [trigger scenario]. Pass [required inputs]. Ask '[example prompt pattern]'.
```

| Component | Purpose | Example |
|-----------|---------|---------|
| **Use when** | Trigger scenario — when should an agent dispatch this subagent? | "Use when finding existing patterns and past decisions" |
| **Pass** | Required inputs — what files, context, or data to provide | "Pass the topic or problem being solved" |
| **Ask** | Prompt patterns — example delegation prompts with `[placeholders]` | "Ask 'Search for precedent on [topic]' or 'How have we handled [similar problem] before?'" |

## Process

### 1. Determine If Subagent Is Appropriate

Before creating a subagent, ask:

- [ ] Is this a high-token workload (many tool calls, large outputs)?
- [ ] Does it involve exploration/trial-and-error?
- [ ] Is the output easily verified?
- [ ] Is the scope well-delineated (not open-ended design)?
- [ ] Would doing it yourself be token-inefficient?
- [ ] What model tier will handle this? (Match task complexity to tier)

**If NO to most questions:** Do not create a subagent. Handle in main agent.

### 2. Read the Subagent Prompt

Read the subagent's prompt file (`prompts/subagents/*.md` or `prompts/worker_agents/**/subagents/**/*.md`).

Extract:
- **Role**: What does this subagent do?
- **Inputs**: What does it need to operate?
- **Prompt patterns**: What are example delegation prompts?
- **Constraints**: File restrictions, report-only modes, tool limitations?

### 3. Write the Description

Follow the format:

```
Use when [what the prompt says it does]. Pass [what the prompt expects as input]. Ask '[example prompts from the prompt file]'.
```

### 4. Add Required Fields

Every subagent needs:

```json
{
  "agent-name": {
    "description": "Use when X. Pass Y. Ask 'Z'.",
    "mode": "subagent",
    "model": "provider/model-name",
    "permission": {
      "task": "deny"
    },
    "prompt": "{file:/path/to/prompt.md}"
  }
}
```

### 5. Validate

Check that the description:
- ✅ Starts with "Use when"
- ✅ Includes "Pass" (inputs)
- ✅ Includes "Ask" with quoted prompt patterns
- ✅ Uses `[placeholders]` for variable parts
- ✅ Mentions any constraints (e.g., "writes to src/ only", "REPORT-ONLY")
- ✅ Matches model tier to task complexity

## Red Flags

**NEVER:**
- Create primary agents without explicit user request
- Write skill-style descriptions for subagents ("Use when X — does Y")
- Omit prompt patterns or input requirements
- Write user-facing descriptions for subagents
- Include "you" or "your" (descriptions are read by agents about other agents)
- Delegate false-negative-prone tasks to B/C-tier models
- Use subagents for simple tasks (token inefficient)
- Trust C-tier models for code edits or design decisions

**ALWAYS:**
- Include concrete prompt examples in quotes
- Use `[placeholders]` for variable parts
- Mention file/directory constraints if applicable
- Note if the subagent is "REPORT-ONLY" (doesn't edit files)
- Match task complexity to model tier
- Verify subagent output for B/C-tier models
- Git checkpoint before and after subagent work

## Related Skills

- **prompt-engineering** — REQUIRED: Writing effective prompts. Subagent descriptions ARE prompts that prime delegating agents. Apply principles: be concrete, provide examples, use placeholders for variables.
- **creating-skills** — REQUIRED: Skill description writing lessons. The "Use when" trigger pattern comes from skill description best practices. Adapt TDD approach: watch agents fail to delegate properly, write descriptions that prevent those failures.
- **model-selection** — REQUIRED: Selecting appropriate models for subagent tasks. Match task complexity to model tier (S/A/B/C), understand difficulty calibration, and optimize for token efficiency.
- **subagent-delegation** — Operational lifecycle and review cycles for subagents.

## Cross-References

| Skill | What It Teaches | Application to Subagent Descriptions |
|-------|-----------------|-------------------------------------|
| `prompt-engineering` | Concrete examples, variable placeholders, priming context | Description format with "Ask '[pattern]'" and `[placeholders]` |
| `creating-skills` | Description writing for tool selection | "Use when" trigger pattern, scenario-based framing |
| `creating-skills/anthropic-best-practices` | Description field guidelines | Keep descriptions concise but expository (1024 char max) |
| `model-selection` | Model tier capabilities, difficulty calibration, task-to-tier matching | Match task complexity to S/A/B/C-tier models |
| `subagent-delegation` | Review loops, checkpointing | Verify B/C-tier output, git checkpoint atomic work |
