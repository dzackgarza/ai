---
name: creating-skills
description: Use when creating new skills, editing existing skills, or verifying skills work before deployment. Skill content should encode behavior and constraints, not reference material.
---

# Creating Skills

A skill encodes **behavioral policy**, not reference documentation. It tells agents **how to work**, **what to check**, and **what to avoid**—it does not replace the docs.

## What Skills Should Be

### 1. Behavioral Policy

Rules that change how agents work:

- Inspect before editing
- Verify assumptions against source
- Prefer existing patterns over invention
- Never claim success without running checks
- Do not broaden scope unless required

### 2. Decision Procedures

Compact instructions for recurring choices:

- How to choose between grep, AST tools, tests, and docs
- When to read config vs infer defaults
- When to use a subagent
- When to patch vs rewrite
- When to stop and report a blocker

### 3. Environment-Specific Traps

Facts not obvious and costly to rediscover:

- Wrapper command hides real executable
- Config loader merges files in nonstandard order
- Codegen step overwrites edits
- Test harness must run from specific directory
- CLI flag is misleading or broken

### 4. High-Value Invariants

Project constraints in working memory:

- Additive-only edits
- Do not edit generated files
- Preserve public API
- Update docs and tests together
- Output must include checklist

### 5. Workflow Recipes

Operational playbooks:

- How to prepare reproducible bug report
- How to do safe refactor in this repo
- How to validate migration
- How to audit generated stubs one file at a time

## What Skills Should NOT Be

### 1. Pasted Manuals

Do not dump:

- Full CLI references
- Exhaustive flag lists
- Full config schemas
- Environment variable catalogs
- Install instructions
- Model catalogs

### 2. Marketing Pages

Do not include:

- Feature overviews
- Ecosystem summaries
- Product positioning
- Persuasive explanations

### 3. Substitutes for Discovery

Do not encode material agent can obtain via:

- `--help`
- Reading repo docs
- Schema inspection
- File search
- Command experimentation

### 4. Stale Caches

Avoid storing:

- Exact version-specific flags
- Current recommended models
- Provider availability
- Changing URLs
- Transient project status

### 5. Broad Tutorials

Skills are operational memory, not onboarding guides.

## Practical Test: Should This Be in a Skill?

Before adding content, ask:

1. **Can the agent fetch this directly in under a few commands?** If yes, exclude it.
2. **Is this primarily reference, or does it alter behavior?** If reference only, exclude it.
3. **Is this likely to go stale?** If yes, prefer live lookup.
4. **Would omission cause a recurring execution failure?** If no, exclude it.
5. **Is this a local trap, invariant, or workflow rule?** If yes, include it.
6. **Does this reduce ambiguity at action time?** If yes, include it.

## What NOT to Waste Tokens On

- Installation instructions
- Basic command usage examples
- Full subcommand enumerations
- Repeated flag tables
- Full config key listings
- Environment variable lists
- Provider/model catalogs
- Long permission tables
- Standard MCP boilerplate
- Generic "what is X" explanations
- Broad feature summaries
- Lengthy examples of obvious syntax

## What IS Worth Spending Tokens On

- Required validation sequence
- Mandatory output structure
- Anti-scope-drift constraints
- Common failure patterns
- Local conventions differing from upstream docs
- Forbidden shortcuts
- Evidence required before marking done
- Exact review checklist
- Escalation conditions
- When not to trust automation
- Task-specific decomposition rules

## Skill Location

**All skills must be stored in `~/ai/opencode/skills/`**

Do NOT create skills in other locations. This directory is the canonical source and is symlinked into harness-specific directories.

## Directory Structure

```
~/ai/opencode/skills/
skill-name/
├── SKILL.md (required)
├── scripts/ (optional: executable helpers)
├── references/ (optional: JIT-loaded docs)
└── assets/ (optional: output resources)
```

## SKILL.md Structure

**Frontmatter (YAML) requirements:**

```yaml
---
name: skill-name
description: Use when [specific triggering conditions and symptoms]
---
```

- Only `name` and `description` fields allowed
- `name`: lowercase letters, numbers, hyphens only (no spaces, underscores, special chars)
- `description`: Must start with "Use when...", max 1024 characters total
- NEVER summarize workflow in description
- Description is the ONLY trigger mechanism—include specific symptoms, errors, situations

**Validate YAML before committing:**

```bash
# Check for syntax errors
python3 -c "import yaml; yaml.safe_load(open('SKILL.md'))"

# Or use yq
yq '.' SKILL.md > /dev/null && echo "YAML valid"
```

**Body template:**

```markdown
# Skill Name

Brief overview (1-2 sentences).

## Core Policy

- Rule 1
- Rule 2
- Rule 3

## Decision Procedures

When to do X vs Y:

- Condition A → do X
- Condition B → do Y

## Environment Traps

- Trap 1: [description] → [mitigation]
- Trap 2: [description] → [mitigation]

## Required Outputs

- Output 1: [format/requirements]
- Output 2: [format/requirements]

## Validation Checklist

- [ ] Check 1
- [ ] Check 2
- [ ] Check 3

## Anti-Patterns

| Pattern     | Why Bad     | Do Instead      |
| ----------- | ----------- | --------------- |
| Bad pattern | Explanation | Better approach |
```

**Body rules:**

- Encode behavior, not reference
- Keep under 500 lines
- Use cross-references: `[See FORMS.md](FORMS.md)`
- Avoid deeply nested references

**REQUIRED: Load these skills before writing:**

- **writing-for-agent-audiences** — How to write effective agent-facing documentation
- **writing-clearly-and-concisely** — Concise prose techniques

## Testing Skills

Test-Driven Development for skills:

1. **RED**: Run scenario WITHOUT skill → document failures
2. **GREEN**: Write minimal skill addressing failures → verify compliance
3. **REFACTOR**: Close loopholes → re-test until bulletproof

**Test with pressure scenarios:**

- Time pressure
- Sunk cost
- Authority pressure
- Exhaustion

Success: Agent follows rule under maximum pressure.

## Skill Creation Checklist

- [ ] Content encodes behavior, not reference
- [ ] No duplication of discoverable material (`--help`, docs, schema)
- [ ] No volatile details (version-specific flags, current models)
- [ ] No marketing or persuasive filler
- [ ] Description: "Use when..." + triggers only
- [ ] Under 500 lines
- [ ] YAML frontmatter valid (tested with `python3 -c` or `yq`)
- [ ] Tested with pressure scenarios
- [ ] Addresses specific failure modes observed
- [ ] Cross-references other skills where needed
- [ ] Includes validation checklist for outputs

## One-Sentence Rule

A skill tells the agent **how to work**, **what to check**, and **what to avoid**; it does not try to replace the docs.
