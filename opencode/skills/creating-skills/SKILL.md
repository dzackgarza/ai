---
name: creating-skills
description: Use when creating new skills, editing existing skills, or verifying skills work before deployment. Skill content should encode behavior and constraints, not reference material.
---

# Creating Skills

A skill encodes **behavioral policy**, not reference documentation. It tells agents **how to work**, **what to check**, and **what to avoid** -- it does not replace the docs.

## Core Principles

### Conciseness: The Context Window Is a Public Good

Your skill shares the context window with the system prompt, conversation history, other skills' metadata, and the user's request. Only add context Claude doesn't already have.

Challenge each piece of content:
- "Does Claude really need this explanation?"
- "Can I assume Claude knows this?"
- "Does this paragraph justify its token cost?"

### Degrees of Freedom

Match specificity to the task's fragility:

- **High freedom** (text instructions): Multiple approaches valid, context-dependent decisions
- **Medium freedom** (pseudocode/parameterized scripts): Preferred pattern exists, some variation acceptable
- **Low freedom** (exact scripts, no params): Fragile operations, consistency critical, specific sequence required

Think of it as: narrow bridge with cliffs (low freedom) vs open field with no hazards (high freedom).

### Behavioral Policy Over Reference

Skills tell agents what to do, not what things are. If the agent can fetch it with `--help`, docs, schema inspection, or file search -- exclude it.

## What Skills Should Be

- **Behavioral policy**: Rules that change how agents work (inspect before editing, verify assumptions, prefer existing patterns)
- **Decision procedures**: Compact instructions for recurring choices (when to grep vs AST tools, when to patch vs rewrite, when to stop and report a blocker)
- **Environment-specific traps**: Facts not obvious and costly to rediscover (wrapper hides real executable, codegen overwrites edits, test harness must run from specific directory)
- **High-value invariants**: Project constraints in working memory (additive-only edits, don't edit generated files, update docs and tests together)
- **Workflow recipes**: Operational playbooks (safe refactor, validate migration, audit generated stubs one file at a time)

## What Skills Should NOT Be

- **Pasted manuals**: CLI references, flag lists, config schemas, env var catalogs, install instructions
- **Marketing**: Feature overviews, ecosystem summaries, product positioning
- **Substitutes for discovery**: Material obtainable via `--help`, repo docs, schema inspection, file search
- **Stale caches**: Version-specific flags, current models, provider availability, changing URLs
- **Broad tutorials**: Skills are operational memory, not onboarding guides

## Practical Test

Before adding content, ask:

- **Can the agent fetch this in under a few commands?** If yes, exclude.
- **Is this primarily reference, or does it alter behavior?** If reference only, exclude.
- **Is this likely to go stale?** If yes, prefer live lookup.
- **Would omission cause a recurring execution failure?** If no, exclude.
- **Is this a local trap, invariant, or workflow rule?** If yes, include.
- **Does this reduce ambiguity at action time?** If yes, include.

## Skill Location and Directory Structure

**All skills must be stored in `~/ai/opencode/skills/`** -- the canonical source, symlinked into harness-specific directories.

```
skill-name/
├── SKILL.md              # Main instructions (required, under 500 lines)
├── references/           # JIT-loaded detailed docs (one level deep from SKILL.md)
├── scripts/              # Executable helpers (executed, not loaded into context)
└── assets/               # Output resources
```

## SKILL.md Structure

### Frontmatter

```yaml
---
name: skill-name
description: Use when [specific triggering conditions and symptoms]
---
```

- `name`: Max 64 chars, lowercase letters/numbers/hyphens only. No reserved words ("anthropic", "claude"). Prefer **gerund form** (`processing-pdfs`, `analyzing-spreadsheets`, `testing-code`).
- `description`: Max 1024 chars, non-empty. Must be **third person** (NOT "I can help you" or "You can use this"). Include both what the skill does AND when to use it, with specific triggers/symptoms.

**Validate frontmatter before committing:**

```bash
yq --front-matter=extract '.' SKILL.md > /dev/null && echo "YAML valid"
```

### Body Rules

- Encode behavior, not reference
- Under 500 lines
- Use cross-references for detail: `See [FORMS.md](references/forms.md)`
- Keep references **one level deep** from SKILL.md (never reference-from-reference)
- Include TOC at top of reference files over 100 lines
- Use consistent terminology throughout (pick one term, use it everywhere)
- No time-sensitive information (use "old patterns" sections with `<details>` if needed)
- Name reference files descriptively (`form_validation_rules.md`, not `doc2.md`)
- Always use forward slashes in file paths

### Body Template

```markdown
# Skill Name

Brief overview (1-2 sentences).

## Core Policy
- Rule 1
- Rule 2

## Decision Procedures
When to do X vs Y:
- Condition A -> do X
- Condition B -> do Y

## Environment Traps
- Trap 1: [description] -> [mitigation]

## Required Outputs
- Output 1: [format/requirements]

## Validation Checklist
- [ ] Check 1
- [ ] Check 2

## Anti-Patterns
| Pattern | Why Bad | Do Instead |
|---------|---------|------------|
| Bad pattern | Explanation | Better approach |
```

## Writing Effective Content

### Token Efficiency

**Worth spending tokens on:**
- Required validation sequences
- Mandatory output structure
- Anti-scope-drift constraints
- Common failure patterns and rationalization counters
- Local conventions differing from upstream docs
- Forbidden shortcuts
- Evidence required before marking done
- Escalation conditions
- Task-specific decomposition rules

**NOT worth spending tokens on:**
- Installation instructions or basic command usage
- Full subcommand/flag/config/env var enumerations
- Provider/model catalogs
- Generic "what is X" explanations
- Lengthy examples of obvious syntax
- Standard MCP boilerplate

### Common Authoring Patterns

**Template pattern:** Provide output templates. Match strictness to fragility -- strict for API responses/data formats, flexible for context-dependent analysis.

**Examples pattern:** Input/output pairs for style-dependent outputs (commit messages, reports, documentation). Examples communicate desired style more clearly than descriptions.

**Conditional workflow pattern:** Decision trees guiding through branching operations ("Creating new? -> follow creation workflow. Editing existing? -> follow editing workflow").

**Feedback loops:** Validate -> fix -> repeat cycles that catch errors early. Include validation scripts or checklists.

For detailed examples of each: See [references/anthropic-best-practices.md](references/anthropic-best-practices.md#common-patterns)

### Workflows

Break complex operations into sequential steps with copyable checklists:

```
Task Progress:
- [ ] Step 1: Analyze input
- [ ] Step 2: Create mapping
- [ ] Step 3: Validate mapping
- [ ] Step 4: Execute
- [ ] Step 5: Verify output
```

Clear steps prevent skipping critical validation. Push large workflows into separate files.

For detailed workflow examples: See [references/anthropic-best-practices.md](references/anthropic-best-practices.md#workflows-and-feedback-loops)

## Executable Code Guidelines

When skills include scripts:

- **Solve, don't punt:** Handle errors explicitly rather than letting scripts fail for Claude to debug
- **No magic numbers:** Document all constants with justification (Ousterhout's law)
- **Prefer pre-made scripts:** More reliable than generated code, save tokens, ensure consistency
- **Clarify execution intent:** "Run `script.py`" (execute) vs "See `script.py`" (read as reference)
- **Fully qualified MCP tool names:** `ServerName:tool_name` to avoid "tool not found" errors
- **List required packages explicitly:** Don't assume anything is installed
- **Verifiable intermediate outputs:** plan-validate-execute pattern for complex batch/destructive operations

For full executable code guidelines: See [references/anthropic-best-practices.md](references/anthropic-best-practices.md#advanced-skills-with-executable-code)

## Evaluation and Testing

### Evaluation-Driven Development

**Create evaluations BEFORE writing extensive documentation.** This ensures your skill solves real problems rather than documenting imagined ones.

- Run Claude on representative tasks without the skill -- document specific failures
- Create 3+ evaluation scenarios testing those gaps
- Write minimal skill addressing the failures
- Iterate: execute evaluations, compare against baseline, refine

### TDD for Skills (RED-GREEN-REFACTOR)

- **RED**: Run pressure scenarios WITHOUT skill -> document failures and rationalizations verbatim
- **GREEN**: Write minimal skill addressing specific baseline failures -> verify compliance
- **REFACTOR**: Close loopholes with explicit rationalization counters -> re-test until bulletproof

Success: agent follows rule under maximum pressure (3+ combined pressures: time + sunk cost + authority + exhaustion).

For full testing methodology: See [references/testing-skills.md](references/testing-skills.md)
For persuasion psychology behind skill language: See [references/persuasion-principles.md](references/persuasion-principles.md)

### Iterative Development with Claude A/B

- **Claude A** writes/refines the skill
- **Claude B** (fresh instance) tests it on real tasks
- Observe Claude B's behavior -> refine with Claude A -> repeat

Watch for: unexpected exploration paths, missed references, overreliance on certain sections, ignored bundled files. Iterate based on observations, not assumptions.

For full iterative process: See [references/anthropic-best-practices.md](references/anthropic-best-practices.md#develop-skills-iteratively-with-claude)

## Anti-Patterns

| Pattern | Why Bad | Do Instead |
|---------|---------|------------|
| Dumping full CLI reference | Wastes tokens on discoverable info | Link to `--help` or docs |
| Too many tool options | Confuses; agent can't choose | Provide one default + escape hatch |
| Windows-style paths | Breaks on Unix | Always use forward slashes |
| Deeply nested references | Claude partially reads nested files | Keep refs one level deep |
| Time-sensitive content | Goes stale silently | Use `<details>` "old patterns" sections |
| Inconsistent terminology | Confuses understanding | Pick one term per concept |
| Over-explaining to Claude | Wastes context on known concepts | Assume Claude is smart |
| Writing skill before testing | Addresses imagined failures | Always baseline test first (RED) |

## Skill Creation Checklist

### Content
- [ ] Encodes behavior, not reference
- [ ] No duplication of discoverable material (`--help`, docs, schema)
- [ ] No volatile details (version-specific flags, current models)
- [ ] No marketing or persuasive filler
- [ ] Consistent terminology throughout
- [ ] No time-sensitive information

### Structure
- [ ] Name: lowercase-hyphens, max 64 chars, gerund form preferred
- [ ] Description: third person, "Use when..." + triggers, max 1024 chars
- [ ] SKILL.md body under 500 lines
- [ ] YAML frontmatter validated
- [ ] File references one level deep
- [ ] Progressive disclosure for detailed content
- [ ] Reference files over 100 lines have TOC

### Code (if applicable)
- [ ] Scripts solve problems, don't punt
- [ ] No magic numbers (all values justified)
- [ ] Required packages listed explicitly
- [ ] MCP tool names fully qualified (`ServerName:tool_name`)
- [ ] Validation/verification steps for critical operations
- [ ] Feedback loops for quality-critical tasks

### Testing
- [ ] Baseline test without skill (RED phase)
- [ ] 3+ evaluation scenarios
- [ ] Tested with pressure scenarios (3+ combined pressures)
- [ ] Agent follows rules under maximum pressure
- [ ] Tested with all target models (Haiku/Sonnet/Opus)

## Required Skills Before Writing

Load these before writing skill content:
- **writing-for-agent-audiences** -- How to write effective agent-facing documentation
- **writing-clearly-and-concisely** -- Concise prose techniques

## References

- [Anthropic Official Best Practices](references/anthropic-best-practices.md) -- Full authoring guide with detailed examples and patterns
- [Testing Skills (TDD)](references/testing-skills.md) -- RED-GREEN-REFACTOR methodology for skill development
- [Persuasion Principles](references/persuasion-principles.md) -- Psychology of effective skill language
- [OpenAI YAML Fields](references/openai_yaml.md) -- openai.yaml config reference for cross-platform skills
