---
name: writing-for-agent-audiences
description: Use when writing or editing prose intended to be consumed by AI agents — prompts, instructions, SKILL.md bodies, system prompts, subagent task descriptions, or any agent-facing documentation.
---
# Writing Documentation for LLMs

> Guidance for creating effective documentation and instructions that LLMs can discover,
> understand, and use successfully.

## Contents

- [Core Principles](#core-principles)

- [Structure & Progressive Disclosure](#structure--progressive-disclosure)

- [Content Patterns](#content-patterns)

- [Anti-patterns](#anti-patterns)

- [Testing & Iteration](#testing--iteration)

* * *

## Core Principles

### Assume competence

The LLM is already very smart.
Only add information the LLM doesn’t have.
Challenge every piece:

- “Does the LLM really need this explanation?”

- “Can I assume the LLM knows this?”

- “Does this justify its token cost?”

**Verbose example** (~150 tokens):

```
PDF (Portable Document Format) files are a common file format that contains
text, images, and other content. To extract text from a PDF, you'll need to
use a library. There are many libraries available for PDF processing...
```

**Concise example** (~50 tokens):

```
Use pdfplumber for text extraction:
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

### Meta-Commentary and Framing

**Rule:** Meta-commentary belongs *only* in skills where the task is explicitly meta.
Otherwise, the skill should be purely prescriptive.

Most skills operate at the object level (e.g., extracting a PDF, writing a test,
compiling LaTeX). In these skills, do not explain the psychology of LLMs to an LLM.
State the rule directly.
Avoid meta-writing like “LLMs often struggle with …” or “This rule exists because models
tend to...”.

**Verbose/Meta example (Wrong for an object-level skill)**:

> LLMs often resort to simple fallbacks like pdftotext or pymupdf when dealing with
> PDFs. To catch this common failure mode, you must use MinerU.

**Concise/Prescriptive example (Correct for an object-level skill)**:

> Never use simple fallbacks like pdftotext or pymupdf.
> Use MinerU for PDF extraction.

**When Meta-Commentary is Appropriate:** If a skill is explicitly about agent behavior,
failure modes, or introspection (e.g., an [[llm-failure-modes/SKILL|llm-failure-modes]] skill or an
`agent-orchestration` skill), then discussing LLM behavior, tendencies, and failure
patterns is completely appropriate and necessary for the task context.

### Theory-of-Mind Gap: Don’t Write Instructions the Agent Can’t Act On

The most dangerous skill-writing mistake is writing instructions that assume the agent
has self-awareness about its own failure modes.
This creates a catch-22: the skill exists because the agent DOES NOT understand these
patterns, so instructions that assume it does are circular.
If the agent could recognize the failure mode in itself, it wouldn’t need the skill.

**The pattern to avoid:** meta-warnings about agent psychology that the agent cannot act
on because the very blindness the warning describes prevents it from recognizing when
it’s doing the thing.

**Bad (assumes self-awareness the agent doesn’t have):**

> Do not mechanically run through checklists without genuine consideration.
> That is checklist theater — the exact failure mode described in
> [[addressing-shallow-work/SKILL|addressing-shallow-work]].

This fails because: the agent cannot recognize “checklist theater” in itself.
The warning is addressed to a capacity the agent lacks.
The agent will either ignore the warning or, worse, treat it as another box to check —
producing checklist-theater about not-doing-checklist-theater.

**Good (structural constraint the agent CAN follow):**

> This is a single-gate test, not a sequential checklist.
> If ANY signal matches, STOP immediately — do not continue evaluating remaining
> signals. One match is total.
> Do not narrate your evaluation of each signal.

This works because: it describes an observable behavior (stop on first match) without
requiring self-awareness.
The agent can follow the instruction mechanically.
The structural constraint does the work that the meta-warning cannot.

**The principle:** when you know an agent has a failure mode, do not explain the failure
mode to the agent. Instead, write the instruction so that the failure mode is
structurally impossible.
The theory-of-mind gap is something to account for in how you write instructions, not
something to explain to the agent.

### Test across models

Effectiveness varies by model.
Skills that work for Claude Opus may need more detail for Claude Haiku.

### Distill Evaluations Into Task Rules

Use observed agent failures to improve instructions, but translate them into the
worker’s normal task language.

Include evaluation-derived guidance when it becomes an object-level rule:

```
After replacing a source block, inspect the diff and repair any non-CriticMarkup
source-line changes before continuing.
```

Do not include evaluator or harness trivia:

```
In trial 3, the agent changed a quote mark and then claimed the segment was
source-faithful.
```

The agent-facing rule should say what good work requires in production.
Keep run numbers, transcript postmortems, scoring rubrics, wrapper output formats, and
evaluator complaints out of object-level skills unless those mechanics are themselves
the task.

### Mine Correction Sequences for Reset Gates

A long correction sequence is stronger evidence than a single bad answer. Do not distill
it as "avoid X" for each corrected detail. First map the sequence:

- What did each correction force the agent to remove?
- Which assumption survived across multiple corrections?
- Where should the agent have abandoned the frame instead of locally patching it?

Write the resulting skill addition as a reset gate or decision rule. Good rules force an
observable action: restate the workflow gesture, identify the existing substrate, stop
after repeated mechanism-removal corrections, or ask for the missing workflow fact.

Do not paste the case study, quote the transcript, or preserve the domain topic unless
the skill is about that domain. The skill should receive the generalized operational
constraint that would have prevented the correction sequence.

* * *

## Structure & Progressive Disclosure

### Organize like a table of contents

Main file provides overview and points to detailed materials.
LLM reads additional files only when needed.

**Pattern**:

- Main file: high-level guide with references (< 500 lines)

- Reference files: one per domain or topic

- Keep references one level deep (avoid chains: A → B → C)

**Example structure**:

```
my-doc/
├── OVERVIEW.md           # High-level guide
├── reference/
│   ├── api.md           # Specific reference
│   ├── examples.md      # Usage examples
│   └── troubleshooting.md
└── scripts/
    └── helper.py        # Executable utilities
```

### Table of contents for long files

For any file over 100 lines, include a TOC at the top so LLM sees full scope:

```markdown
## Contents

- Authentication and setup
- Core methods (create, read, update, delete)
- Advanced features
- Error handling patterns
```

### Consistent terminology

Choose one term per concept and use it throughout:

- Always “API endpoint” (not “URL”, “route”, “path”)

- Always “field” (not “box”, “element”, “control”)

- Always “extract” (not “pull”, “get”, “retrieve”)

* * *

## Content Patterns

### Descriptions: what + when

Enable discovery with concrete descriptions:

1. **What it does**: The concrete capability

2. **When to use it**: Specific triggers and contexts

**Good example**:

```
Extract text and tables from PDF files, fill forms, merge documents.
Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

**Bad example**:

```
Helps with documents
```

### Examples over explanations

Show concrete input/output before abstract descriptions:

```markdown
## Generating commit messages

Follow these examples:

**Example 1:**
Input: Added user authentication with JWT tokens
Output:
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware
```

### Workflows with clear steps

Break complex operations into sequential steps:

```markdown
## Database migration workflow

Task Progress:

- [ ] Step 1: Create backup
- [ ] Step 2: Run migration script
- [ ] Step 3: Verify schema
- [ ] Step 4: Validate data integrity
```

### Feedback loops for critical tasks

Use validators for quality-critical work:

```markdown
## Document editing process

1. Make your edits
2. **Validate**: Run `validate.py`
3. If validation fails:
   - Review errors
   - Fix issues
   - Run validation again
4. **Only proceed when validation passes**
5. Finalize output
```

### Conditional workflows

Guide the LLM through decision points:

```markdown
## Modification workflow

1. Determine the modification type:
   - Creating new content? → Follow "Creation workflow"
   - Editing existing content? → Follow "Editing workflow"

2. Creation workflow:
   - Use library X
   - Build from scratch
   - Export format Y

3. Editing workflow:
   - Unpack existing file
   - Modify content
   - Repack when complete
```

### Verifiable intermediate outputs

For complex tasks, create verifiable intermediate formats:

```markdown
## Batch update workflow

1. Create plan file (JSON format)
2. **Validate plan**: Run `validate_plan.py`
3. If validation passes, execute
4. Verify output matches plan
```

### Avoid time-sensitive information

Use “old patterns” sections for deprecated approaches:

```markdown
## Current method

Use the v2 API endpoint: `api.example.com/v2/messages`

## Old patterns

<details>
<summary>Legacy v1 API (deprecated 2025-08)</summary>
The v1 API used: `api.example.com/v1/messages`
</details>
```

* * *

## Anti-patterns

### Too many options

Don’t present multiple approaches unless necessary.

**Bad**:

```
You can use pypdf, or pdfplumber, or PyMuPDF, or pdf2image, or...
```

**Good**:

```
Use pdfplumber for text extraction.

For scanned PDFs requiring OCR, use pdf2image with pytesseract.
```

### Deeply nested references

Keep references one level deep.
Nested chains (file A → file B → file C) cause partial reads and missed context.

### Vague trigger terms

Be specific in descriptions for discovery:

**Vague**: `Helps with data`

**Specific**:
`Analyze Excel spreadsheets, generate pivot tables, create charts. Use when working with Excel files, spreadsheets, or .xlsx files.`

### Windows-style paths

Always use forward slashes (Unix style):

- ✓ Good: `scripts/helper.py`

- ✗ Wrong: `scripts\helper.py`

* * *

## Testing & Iteration

### Create evaluations first

Before writing extensive documentation:

1. Identify gaps with LLM working without docs

2. Create 3+ representative test cases

3. Establish baseline performance

4. Convert observed failures into object-level rules or examples

5. Test and iterate based on results

Evaluation notes are for the skill author.
A worker-facing skill should receive the distilled invariant, not the test transcript or
the evaluator’s diagnosis.

### Separate Worker Concerns from Orchestrator Concerns

When writing agent-facing guidance, distinguish clearly:

**Worker-useful** (belongs in agent skill):

- What to read, what to preserve, what to annotate

- Artifact constraints: “Do not append status claims to the output”

- Decision criteria: “Block if you cannot produce holistic summary”

- Output requirements specific to the task domain

**Not worker-useful** (belongs in orchestrator notes):

- Execution mechanics: “In `opencode run --format json`…”

- Harness behavior: “every assistant text part is user-visible …”

- How results are consumed by later stages

- Wrapper trivia about how the tool runs

Wrong: Writing in a vault-analysis skill:
> In opencode run --format json, every assistant text part is user-visible output.

Right: Writing in a vault-analysis skill:
> Do not append handoffs or progress summaries to the annotated source.
> Later analysis should proceed from the source body and passage-local comments.

The first makes the worker think about execution plumbing.
The second constrains the artifact at the object level.

Rule: If your skill mentions the harness, runner, or execution wrapper, you are
contaminating worker guidance with orchestrator concerns.

### Develop iteratively with Claude

1. Complete a task with Claude without docs

2. Identify the reusable pattern

3. Ask Claude to create docs capturing that pattern

4. Review for conciseness (remove explanations Claude already knows)

5. Test docs with a fresh instance on similar tasks

6. Iterate based on observations

## Related Skills

- → [[creating-skills/SKILL|creating-skills]] — REQUIRED: Load alongside when writing or editing `SKILL.md`
  files. Covers what belongs in a skill, description writing guidelines.

- → [[looped-task-skill-author/SKILL|looped-task-skill-author]] — REQUIRED: Load alongside when the agent-facing prose
  supports repeated one-shot loops or long-horizon continuation.
  Covers progress logs, self-correcting state machines.

- → [[subagent-delegation/authoring/SKILL|creating-subagents]] — REQUIRED: Load alongside when writing subagent descriptions
  or agent definitions.

- → [[prompt-engineering/SKILL|prompt-engineering]] — Load alongside when writing broader prompt contracts and
  reference-skill sections.
  Covers concrete examples, variable placeholders, priming context.

* * *

## Key Takeaway

Effective LLM documentation assumes intelligence, uses examples over explanation,
organizes for progressive discovery, and validates critical workflows.
Test with target models and iterate based on real usage patterns.
