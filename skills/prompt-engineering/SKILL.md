---
name: prompt-engineering
description: Use when writing or refactoring system prompts, subagent instructions, or task definitions to ensure rigorous, tool-centric agent behavior.
---

# Prompt Engineering

A prompt is not a request. **A prompt is a contract.** This skill defines the standards for engineering robust agent instructions.

## Foundational Principles

-   **Audience is the Agent**: Prompts are instructions **for the agent**, not documentation for users. After writing, review the prompt to ensure it speaks directly to the agent and avoids meta-commentary.
-   **Combat Knowledge Staleness**: Your innate knowledge of prompting is several generations behind the state-of-the-art. You **MUST** research current best practices and user sentiment weekly to stay updated.
-   **Iterate, Never Rewrite**: Prompts are self-documenting, version-controlled artifacts.
    -   **Always** make incremental changes and track them with `git diff`.
    -   **Never** rewrite a prompt wholesale. Edits should be atomic.
    -   **Verify** that rewrites do not lose semantic content, unless the change is intentional.
-   **Avoid Greenfield Prompts**: Never create a prompt from innate knowledge or training data. This knowledge is almost certainly outdated. Always start from a user draft or find vetted prompts online as a base.
-   **Maintain Organization**:
    -   Ensure prompts are well-organized and not "monkey-patched."
    -   Before adding new instructions, check if the guidance already exists. Repetition is acceptable only for critical emphasis, not from oversight.
-   **Workflow**:
    -   **Always** edit existing files; do not create new ones for iterative changes.
    -   **Always** get explicit permission for major refactors or rewrites.

## Reference Files

| Subdoc | When to Read |
|--------|-------------|
| `reference/context-patterns.md` | Always—for structuring ANY prompt's context (Pyramid, Select Don't Dump, Attention Anchoring, Grounding, etc.) |
| `reference/research-findings.md` | When writing agent prompts, need research-backed techniques (rule-based prompting, parallel tool calling), or want to optimize tool use |

### Templates

| Template | When to Use |
|----------|-------------|
| `templates/builder-agent.md` | When prompting an agent to implement code/features |
| `templates/research-agent.md` | When prompting an agent to research/gather information |
| `templates/review-agent.md` | When prompting an agent to review code/specs |

## 1. The 5-Layer Architecture

Effective prompts must follow this structure to ground the model in reality:

| Layer | Component | Focus |
| :--- | :--- | :--- |
| **Layer 1** | **Identity** | Specific role and behavioral contract (Architect, Builder, etc.). |
| **Layer 2** | **Context** | Ordered, scoped, and labeled information (Rules, State, History). |
| **Layer 3** | **Task** | Precise, measurable, and actionable objective. |
| **Layer 4** | **Process** | **Reasoning-first & Action-first**. How the output is formed. |
| **Layer 5** | **Output** | Exact specification of the deliverable (JSON, Markdown, file format). |

## 2. Operating Rules (Hard Constraints)

Behavioral rules outperform identity-based prompts. Place these in the first 100 tokens.

1. **Action-First** — Execute tool calls BEFORE any explanation.
2. **Exact Schema** — Parameter names must match tool definitions exactly.
3. **Exploration Parallelism** — Make 2-3 parallel tool calls (read/grep/glob) when gathering context.
4. **No Guessing** — If a file path or API is unknown, use search tools rather than assuming.

## 3. The Process Layer (Directing Reasoning)

Don't just ask for output; direct the reasoning cycle:
- **Analyze**: Read context and identify core invariants/constraints.
- **Reason**: List possible approaches and justify the selection.
- **Plan**: Create atomic, verifiable steps.
- **Execute**: Perform work using the correct tools.
- **Verify**: Audit output against task requirements.

## 4. Constraint-Based Instruction

Vagueness is failure. Use "MUST," "ALWAYS," and "NEVER" to define strict boundaries.
- **DRY Principle**: NEVER restate or duplicate guidance found in referenced skills. Use `**REQUIRED BACKGROUND:** Reference [skill-name]` instead.

## 5. Reference Skills Pattern

Every agent prompt MUST include a Reference Skills section to anchor the agent to version-controlled standards:

```markdown
## Reference Skills
- **clean-code** — Code quality standards.
- **high-quality-tests** — Testing standards.
- **systematic-debugging** — Bug investigation methodology.
```

## Anti-Patterns
- **Narrative Prompts**: Writing "I would like you to..." instead of hard rules.
- **Generic Roles**: Using "helpful assistant" instead of a specific behavioral contract.
- **Duplicated Logic**: Copying skill content into a prompt (stale guidance risk).

---
*Derived from Hal Stack orchestration principles.*
