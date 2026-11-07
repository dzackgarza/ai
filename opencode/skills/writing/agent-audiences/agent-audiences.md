---
name: writing-for-agent-audiences
description: Use when creating, editing, reviewing, or evaluating any prose consumed by AI agents. Mandatory for every edit to a SKILL.md or linked skill resource, and for prompts, instructions, system prompts, subagent tasks, or other agent-facing documentation.
---
# Writing Documentation for LLMs

## Policy index

Cite the policy ID with the affected passage. IDs remain stable when sections move.
The linked section owns the rule; examples illustrate its application.

| Policy ID | Rule |
| --- | --- |
| `AGENT001` | [Assume reasoning capacity; verify applied understanding](#assume-reasoning-capacity-verify-applied-understanding) |
| `AGENT002` | [Meta-Commentary and Framing](#meta-commentary-and-framing) |
| `AGENT003` | [Theory-of-Mind Gap: Don’t Write Instructions the Agent Can’t Act On](#theory-of-mind-gap-dont-write-instructions-the-agent-cant-act-on) |
| `AGENT004` | [Test across models](#test-across-models) |
| `AGENT005` | [Distill Evaluations Into Task Rules](#distill-evaluations-into-task-rules) |
| `AGENT006` | [Mine Correction Sequences for Reset Gates](#mine-correction-sequences-for-reset-gates) |
| `AGENT007` | [Organize like a table of contents](#organize-like-a-table-of-contents) |
| `AGENT008` | [Table of contents for long files](#table-of-contents-for-long-files) |
| `AGENT009` | [Consistent terminology](#consistent-terminology) |
| `AGENT010` | [Descriptions: what + when](#descriptions-what--when) |
| `AGENT011` | [Examples over explanations](#examples-over-explanations) |
| `AGENT012` | [Workflows with clear steps](#workflows-with-clear-steps) |
| `AGENT013` | [Feedback loops for critical tasks](#feedback-loops-for-critical-tasks) |
| `AGENT014` | [Conditional workflows](#conditional-workflows) |
| `AGENT015` | [Verifiable intermediate outputs](#verifiable-intermediate-outputs) |
| `AGENT016` | [Avoid time-sensitive information](#avoid-time-sensitive-information) |
| `AGENT017` | [Too many options](#too-many-options) |
| `AGENT018` | [Deeply nested references](#deeply-nested-references) |
| `AGENT019` | [Vague trigger terms](#vague-trigger-terms) |
| `AGENT020` | [Windows-style paths](#windows-style-paths) |
| `AGENT021` | [Create evaluations first](#create-evaluations-first) |
| `AGENT022` | [Separate Worker Concerns from Orchestrator Concerns](#separate-worker-concerns-from-orchestrator-concerns) |
| `AGENT023` | [Develop iteratively with Claude](#develop-iteratively-with-claude) |

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

### Assume reasoning capacity; verify applied understanding

**Policy ID: `AGENT001`**

The LLM can reason, but a correct explanation does not establish that it will apply
the distinction while working. Teach a distinction when observed work shows that it
was lost, even if the agent can repeat the corresponding principle on request.
Use a worked example, vary its presentation, introduce a nearby wrong case, and ask
for transfer to another domain. Keep familiar background facts concise.
Challenge every piece:

- “Which observed reasoning error or missing fact does this explanation address?”

- “What different action should follow when the relevant condition occurs?”

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

**Policy ID: `AGENT002`**

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

Skill-authoring guidance is explicitly meta. Preserve load-bearing audience psychology
when compressing it would recreate a subjective escape hatch. A slogan such as “use
objective triggers” is not a substitute for the causal model that makes the rule usable.

### Theory-of-Mind Gap: Don’t Write Instructions the Agent Can’t Act On

**Policy ID: `AGENT003`**

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
> That is checklist theater.

This fails because: the agent cannot recognize “checklist theater” in itself.
The warning is addressed to a capacity the agent lacks.
The agent will either ignore the warning or, worse, treat it as another box to check —
producing checklist-theater about not-doing-checklist-theater.

**Good (structural constraint the agent CAN follow):**

> This is a single-gate test, not a sequential checklist.
> If ANY signal matches, STOP immediately — do not continue evaluating remaining
> signals. One match is total.
> Do not narrate your evaluation of each signal.

This specifies an observable action without asking for a judgment about motives.
It still depends on the agent recognizing the signal and following the instruction.
It does not make the failure structurally impossible.

**Object-level worker skills:** do not rely on explaining a failure to the affected
worker; make the failure structurally impossible.

**Skill-writing and behavioral-control skills:** teach why the worker cannot safely
interpret the gate, then remove that faculty's jurisdiction. Read
[[writing/agent-audiences/references/behavioral-control-design|Behavioral Control Design for Self-Exonerating Agents]] before writing downstream behavioral controls.

**The principle:** teach the missing distinction, then bind it to an observable
decision in the normal workflow. In a teaching or failure-analysis skill, explain the
reasoning mechanism through concrete examples. In the operative task instructions,
state when to compare source and artifact, what evidence can falsify the proposal,
and which dependent action must wait if that comparison fails.

Neither an explanation nor a required output format proves that the check happened.
Verify that the evidence actually changes the decision. The
[coverage and semantic drift lesson](../llm-failure-modes/coverage-and-semantic-drift.md)
demonstrates this combination of teaching, acceptance rules, and bounded repair.

### Test across models

**Policy ID: `AGENT004`**

Effectiveness varies by model.
Skills that work for Claude Opus may need more detail for Claude Haiku.

### Distill Evaluations Into Task Rules

**Policy ID: `AGENT005`**

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

Generalization is not genericization. In authoring, review, and orchestration skills,
preserve causal models and analogies that explain why an apparently reasonable rule is
gameable. Endpoint wording without that explanation cannot guide the next design.

### Mine Correction Sequences for Reset Gates

**Policy ID: `AGENT006`**

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

In behavioral and authoring skills, preserve the theory of mind behind the gate. The
writer must understand how targets rebase history, exonerate their current selves, and
convert contradictions into small procedural omissions.

* * *

## Structure & Progressive Disclosure

### Organize like a table of contents

**Policy ID: `AGENT007`**

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

**Policy ID: `AGENT008`**

For any file over 100 lines, include a TOC at the top so LLM sees full scope:

```markdown
## Contents

- Authentication and setup
- Core methods (create, read, update, delete)
- Advanced features
- Error handling patterns
```

### Consistent terminology

**Policy ID: `AGENT009`**

Choose one term per concept and use it throughout:

- Always “API endpoint” (not “URL”, “route”, “path”)

- Always “field” (not “box”, “element”, “control”)

- Always “extract” (not “pull”, “get”, “retrieve”)

* * *

## Content Patterns

### Descriptions: what + when

**Policy ID: `AGENT010`**

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

**Policy ID: `AGENT011`**

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

**Policy ID: `AGENT012`**

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

**Policy ID: `AGENT013`**

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

**Policy ID: `AGENT014`**

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

**Policy ID: `AGENT015`**

For complex tasks, create verifiable intermediate formats:

```markdown
## Batch update workflow

1. Create plan file (JSON format)
2. **Validate plan**: Run `validate_plan.py`
3. If validation passes, execute
4. Verify output matches plan
```

### Avoid time-sensitive information

**Policy ID: `AGENT016`**

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

**Policy ID: `AGENT017`**

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

**Policy ID: `AGENT018`**

Keep references one level deep.
Nested chains (file A → file B → file C) cause partial reads and missed context.

### Vague trigger terms

**Policy ID: `AGENT019`**

Be specific in descriptions for discovery:

**Vague**: `Helps with data`

**Specific**:
`Analyze Excel spreadsheets, generate pivot tables, create charts. Use when working with Excel files, spreadsheets, or .xlsx files.`

### Windows-style paths

**Policy ID: `AGENT020`**

Always use forward slashes (Unix style):

- ✓ Good: `scripts/helper.py`

- ✗ Wrong: `scripts\helper.py`

* * *

## Testing & Iteration

### Create evaluations first

**Policy ID: `AGENT021`**

Before writing extensive documentation:

1. Identify gaps with LLM working without docs

2. Create 3+ representative test cases

3. Establish baseline performance

4. Convert observed failures into object-level rules or examples

5. Test and iterate based on results

Evaluation notes are for the skill author.
A worker-facing skill should receive the distilled invariant, not the test transcript or
the evaluator’s diagnosis.

When baseline and guided workers both solve isolated examples, report no demonstrated
improvement. Such a result can expose a gap between explaining a principle and applying
it during execution. Include task-shaped cases where the worker must notice the
condition without a prompt naming the failure. Sustained-use claims require observed
source selection, implementation, reuse, or closure decisions over time. Passing a
short exercise or strengthening instruction wording cannot establish those claims.

### Separate Worker Concerns from Orchestrator Concerns

**Policy ID: `AGENT022`**

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

**Policy ID: `AGENT023`**

1. Complete a task with Claude without docs

2. Identify the reusable pattern

3. Ask Claude to create docs capturing that pattern

4. Remove unnecessary background; preserve lessons tied to observed execution failures

5. Test docs with a fresh instance on similar tasks

6. Iterate based on observations

## Related Skills

- → [[creating-skills/SKILL|creating-skills]] — REQUIRED: Load alongside when writing or editing `SKILL.md`
  files. Covers what belongs in a skill, description writing guidelines.

  Covers progress logs, self-correcting state machines.


  Covers concrete examples, variable placeholders, priming context.

* * *

## Key Takeaway

Effective LLM documentation assumes reasoning capacity, teaches distinctions through
examples, places checks at the decisions they govern, and supports progressive discovery.
Test with target models and iterate based on real usage patterns.
