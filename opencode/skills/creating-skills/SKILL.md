---
name: creating-skills
description: Use when creating new skills, editing existing skills, or verifying skills work before deployment. Skill content should encode behavior and constraints, not reference material.
---
# Creating Skills

> [!IMPORTANT]
> All skills authored or modified under this skill must adhere to the [[policy-index/SKILL#policy-registry|Bridge-Burning Policies]] in `policy-index/SKILL.md`. Any skill that relates to writing, editing, refactoring, testing, or building code MUST include a prominent warning forcing agents to comply with these policies as non-negotiable hard constraints.

A skill encodes **behavioral policy**, not reference documentation.
It tells agents **how to work**, **what to check**, and **what to avoid**—it does not
replace the docs.

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

2. **Is this primarily reference, or does it alter behavior?** If reference only,
   exclude it.

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

- Generic “what is X” explanations

- Broad feature summaries

- Lengthy examples of obvious syntax

## What IS Worth Spending Tokens On

- Required validation sequence

- Mandatory output structure

- Anti-scope-drift constraints

- Common failure patterns

- Observed failures distilled into production rules

- Local conventions differing from upstream docs

- Forbidden shortcuts

- Evidence required before marking done

- Exact review checklist

- Escalation conditions

- When not to trust automation

- Task-specific decomposition rules

- **Bridge-Burning Policies**: When authoring coding, testing, or review skills, you must reference and respect the [[policy-index/SKILL#policy-registry|Bridge-Burning Policies]] defined in `policy-index/SKILL.md`.

## Skill Location

**All skills must be stored in `~/ai/opencode/skills/`**

Do NOT create skills in other locations.
This directory is the canonical source and is symlinked into harness-specific
directories.

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

- `name`: lowercase letters, numbers, hyphens only (no spaces, underscores, special
  chars)

- `description`: Must start with “Use when...”, max 1024 characters total

- NEVER summarize workflow in description

- Description is the ONLY trigger mechanism—include specific symptoms, errors,
  situations

**Validate YAML frontmatter before committing:**

Since `SKILL.md` is a Markdown file with a YAML header, you must extract only the
metadata block for validation:

```bash
# Use yq (mikefarah/yq, the Go version) — ensures correct yq is used
yq --front-matter=extract '.' SKILL.md > /dev/null 2>&1 && echo "YAML valid"
```

Note: `--front-matter=extract` only checks that the YAML block parses.
It will not reject files missing frontmatter entirely; pair with
`head -1 SKILL.md | grep -q '^---$'` if that matters.

**To query a specific frontmatter field:**

```bash
yq --front-matter=extract '.name' SKILL.md
```

**To modify a field in place (preserves markdown body):**

```bash
yq --front-matter=process -i '.name = "new-name"' SKILL.md
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

- Avoid deeply nested references

**REQUIRED: Load these skills before writing:**

- [[writing-for-agent-audiences/SKILL|writing-for-agent-audiences]] — How to write effective agent-facing documentation

- [[obra-the-elements-of-style/SKILL|writing-clearly-and-concisely]] — Concise prose techniques

- [[looped-task-skill-author/SKILL|looped-task-skill-author]] — Required for repeated one-shot loops, persistent state,
  or continuation workflows

- [[creating-subagents/SKILL|creating-subagents]] — Required when the skill interacts with subagent or
  runtime-agent definitions

- [[prompt-engineering/SKILL|prompt-engineering]] — Required for system prompts, agent definitions, or prompt
  contracts adjacent to the skill

## Testing Skills

Test-Driven Development for skills:

1. **RED**: Run scenario WITHOUT skill → document failures

2. **GREEN**: Write minimal skill addressing failures → verify compliance

3. **REFACTOR**: Close loopholes → re-test until bulletproof

Transcript observations are raw evidence for the skill author, not prose to paste into
the skill. Convert each useful observation into one of:

- an object-level invariant;

- a decision rule;

- a validation step;

- a concrete good/bad example.

Do not put run numbers, model names, wrapper output formats, transcript mechanics, or
evaluator complaints into an object-level skill unless those mechanics are themselves
the task. Prior failures belong in the skill only after they have been generalized into
normal task-facing behavior.

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

- [ ] Description: “Use when...” + triggers only

- [ ] Under 500 lines

- [ ] YAML frontmatter valid (tested with `yq --front-matter=extract`)

- [ ] Tested with pressure scenarios

- [ ] Addresses specific failure modes observed

- [ ] Cross-references other skills where needed, and explicitly references the [[policy-index/SKILL#policy-registry|Bridge-Burning Policies]] if the skill touches writing, editing, refactoring, building, or testing code

- [ ] Includes validation checklist for outputs

## One-Sentence Rule

A skill tells the agent **how to work**, **what to check**, and **what to avoid**; it
does not try to replace the docs.
