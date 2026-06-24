---
name: writing-documentation
description: Use when writing, reviewing, or improving technical documentation, including READMEs, guides, API docs, architecture docs, runbooks, tutorials, and CLI docs.
---

# Writing Documentation

Write documentation that lets its intended reader decide, install, use, verify,
debug, or extend the thing being documented.

This skill is the source of truth for general documentation workflow and quality
criteria. Use narrower skills, such as `writing-readmes`, only for
type-specific gates.

## Required References

Load references only as needed for the current documentation type:

- Always load `reference/strunk-white-principles.md` before writing,
  reviewing, or rewriting documentation.
- Load `reference/doc-types.md` before choosing structure, reviewing
  structure, or working on README, API, tutorial, guide, architecture, CLI, or
  operations docs.
- Load `reference/examples.md` when improving existing prose or when the task
  needs before/after patterns.

## Core Policy

- Start from the reader's task, not from the repository's internal structure.
- Preserve every fact the reader needs to succeed.
  Concision never justifies deleting prerequisites, commands, expected output,
  limits, risks, or decision context.
- Prefer canonical sources over duplication.
  Link to API reference, CLI help, schemas, changelogs, or design docs when
  those are the maintained source.
- Do not replace necessary facts with vague pointers.
  A pointer to another document is valid only after the current document gives
  enough information for its own purpose.
- Write facts, commands, examples, constraints, and boundaries.
  Delete slogans, mood-setting, and claims that cannot be verified from the
  repository or a cited source.
- Keep agent-control material out of user-facing docs.
  Prompts, correction history, private status systems, review gates, live planning
  state, and supervision doctrine belong in agent-owned or planning surfaces, not
  consumer documentation.

## Documentation Workflow

Before writing or rewriting:

- Identify the document type from `reference/doc-types.md`.
- State the target reader.
- State the reader task the document must enable.
- Establish external reality before adopting project vocabulary: artifact type, real
  reader, smallest complete use case, useful payload, and current implementation
  boundary.
- Inspect the current document, nearby docs, and canonical sources for the
  facts the reader needs.
- Decide which facts belong in the current document and which belong in linked
  canonical sources.

When drafting:

- Lead with the reader's first decision or first action.
- Use executable examples and complete commands.
- Include expected output when the reader needs verification.
- State prerequisites before commands that depend on them.
- Use the public interface: package names, CLI commands, public modules,
  public configuration keys, request shapes, and documented file locations.
- Move implementation internals to architecture or contributor docs unless a
  consumer must interact with them.

When reviewing:

- Check whether the document achieves its reader task.
- Check whether examples still run or are sourced from a maintained test,
  example, or help output.
- Check whether links point to canonical sources.
- Check whether any fact is duplicated in a way likely to drift.
- Check whether any essential fact was removed for brevity.
- Check whether the document asks the reader to enter a private ontology before it
  names the ordinary thing, task, input, output, and evidence.

## Concision Rule

Omit needless words, not needed information.

Delete:

- sentences true of any project;
- promotional adjectives without measurements or evidence;
- contributor or release process details from consumer docs;
- repeated facts already maintained in a canonical source;
- backstory that does not change installation, use, evaluation, or operation.

Keep or add:

- the reason the project exists, stated as a concrete problem;
- installation and verification commands;
- minimal working examples;
- expected output or observable success criteria;
- prerequisites, credentials, permissions, and network behavior;
- data, security, caching, persistence, and privacy boundaries;
- status, maturity, limits, and cases where the tool should not be used;
- links to deeper docs when the reader has enough context to choose them.

## One Source Of Truth

Documentation should point at canonical sources instead of cloning them.

Use this rule:

- If the reader needs one command to begin, include the command.
- If the reader needs a complete option reference, link to `--help`, API docs,
  schema docs, or generated reference.
- If the reader needs one configuration example, include the example.
- If the reader needs every configuration key, link to the schema or reference.
- If the reader needs project history, link to changelog or releases.
- If the reader needs contributor process, link to `CONTRIBUTING.md` or the
  developer guide.

Do not use OSOT as an excuse to omit the minimum usable path.

## Type Routing

- README: project entry point for evaluation, installation, first use, and
  links to deeper docs. Also load `writing-readmes`.
- API reference: public signatures, parameters, return values, errors, and
  examples.
- CLI documentation: commands, arguments, options, examples, configuration,
  and exit behavior.
- Tutorial or guide: task-oriented path with verification at meaningful
  checkpoints.
- Architecture documentation: system structure, data flow, decisions,
  tradeoffs, and consequences.
- Runbook or operations guide: deployment, credentials, state, monitoring,
  recovery, and failure modes.

## Validation Checklist

- [ ] The target reader and reader task are clear.
- [ ] The document type matches `reference/doc-types.md`.
- [ ] Required prerequisites are stated before use.
- [ ] Commands and examples are complete enough to run.
- [ ] Expected output or verification is present where needed.
- [ ] Necessary limits, risks, and unsupported cases are stated.
- [ ] Public names and interfaces are documented where consumers need them.
- [ ] Implementation internals are omitted unless consumers must interact with
      them.
- [ ] Canonical sources are linked instead of duplicated.
- [ ] Brevity did not remove information required for the reader task.
- [ ] Prose follows `reference/strunk-white-principles.md`.

## Anti-Patterns

| Pattern | Why it fails | Do instead |
| --- | --- | --- |
| Compressing to an arbitrary line count | Hides required installation, usage, or boundary facts | Keep the shortest document that satisfies the reader task |
| Linking to docs before answering the entry question | Forces readers to search before knowing whether they care | Give enough context, then link |
| Copying generated reference material | Drifts from CLI help, schemas, or API docs | Include one working path and link to the canonical reference |
| Writing from internal architecture outward | Makes newcomers decode implementation names | Start with the public problem and interface |
| Replacing facts with adjectives | Produces claims the reader cannot verify | State behavior, measurements, examples, and limits |
| Publishing agent meta-work as product docs | Makes prompts, correction history, or review doctrine look like user-facing architecture | Move private process material to the agent-owned surface and keep docs task-facing |
| Explaining why a bad doc pattern is bad inside the doc | Substitutes disclosure for remediation and fossilizes the correction | Remove the bad pattern; link to the correct canonical surface only when the reader needs it |
| Treating names as evidence | Gives invented components authority before locating code, data, or workflows | Verify named things against implementation, payload, examples, or external sources |
