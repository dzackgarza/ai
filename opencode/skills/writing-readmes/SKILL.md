---
name: writing-readmes
description: Use when writing, reviewing, or improving a README file, especially when deciding what a repository entry point must tell consumers before they install, evaluate, or use it.
---

# Writing READMEs

Use this skill as the README-specific layer on top of `writing-documentation`.

The documentation skill owns the general workflow, style rules, and OSOT
policy. This skill owns the README acceptance contract: a README must let a
new consumer understand why the repo exists, decide whether it applies, install
it, run a first useful example, verify the result, and find deeper docs.

## Required Sequence

- Load `writing-documentation` first.
- Load `writing-documentation/reference/doc-types.md` and use its README
  section as the canonical structural source.
- Load `writing-documentation/reference/strunk-white-principles.md` for prose
  quality.
- Inspect the repository's public surfaces before rewriting: package metadata,
  CLI help, examples, docs, justfile or task runner, configuration schema, and
  existing README.
- Rewrite only after identifying the consumer path and the canonical sources
  that should be linked rather than duplicated.

## README Purpose

A README is the repository entry point for consumers and cloners.

It must answer:

- What is this repository?
- Why does it exist?
- Who should use it?
- What problem does it solve?
- What public interface does the user interact with?
- What prerequisites, credentials, permissions, or services are required?
- How does a user install it?
- How does a user run the smallest useful example?
- What output or behavior proves the example worked?
- What are the important limits, risks, unsupported cases, or maturity notes?
- Where should the reader go for reference, guides, architecture, operations,
  contributing, changelog, or support?

If a README cannot answer these, it has not done its job.

## Structure

Use the README section in `reference/doc-types.md` as the source of truth.
Adapt the order to the project, but preserve the reader path:

- Identify the project.
- Explain the concrete problem and audience.
- State status or maturity when it affects adoption.
- Show installation with prerequisites.
- Show quick start with expected output.
- Explain the main public capabilities when they are not obvious from the quick
  start.
- State configuration, credentials, permissions, persistence, network behavior,
  and data boundaries when relevant.
- State limits and unsupported cases.
- Link to canonical docs for details.
- State the license when applicable.

No section is mandatory by name.
Every required reader question must still be answered somewhere.

## OSOT For READMEs

Do not duplicate maintained reference material, but do not hide the first
usable path behind a link.

Include:

- the primary install command;
- the minimum viable command, import, API call, or workflow;
- required prerequisites and credentials;
- expected output or verification;
- one representative configuration example if configuration is required for
  first use;
- links to canonical references after the reader has enough context to choose
  them.

Link instead of copying:

- exhaustive CLI flag tables;
- complete API references;
- full configuration schemas;
- changelogs and release history;
- contributor workflows;
- architecture internals not required for first use;
- generated docs or help output.

Bad OSOT: "See docs" with no install or usage path.
Good OSOT: one runnable path in the README, then links to full references.

## What To Remove

Delete content that does not help a consumer decide, install, use, verify, or
understand boundaries:

- generic claims true of any project;
- marketing adjectives without evidence;
- popularity claims unless adoption itself changes the user's decision;
- badge walls and vanity badges;
- contributor process details better owned by `CONTRIBUTING.md`;
- full API or CLI references already generated elsewhere;
- internal function names, private modules, pipeline labels, or state paths the
  consumer never touches;
- development backstory unless it changes trust, status, or adoption risk;
- feature lists that do not explain the user-visible behavior.

Do not delete public names users must type: package names, commands, import
paths, public modules, public configuration keys, endpoint paths, file formats,
and documented state locations are consumer-facing facts.

## Evidence Rules

Every important claim needs evidence available to the reader.

- Performance claims need benchmark name, baseline, conditions, and result.
- Compatibility claims need versions or platforms.
- Security or privacy claims need the concrete mechanism or boundary.
- Production-readiness claims need the operational facts that make them true.
- "Works with X" needs setup or a link to setup.
- "Similar to X" is allowed only when it clarifies fit and states the
  difference.

If the evidence would be too long for the README, state the bounded result and
link to the canonical evidence.

## Surprises To Surface

State these before or near first use when they apply:

- required accounts, keys, tokens, or paid APIs;
- network calls and external services;
- local files, browser cookies, databases, caches, or credentials read;
- persistent state, generated files, and cache invalidation behavior;
- telemetry, analytics, or logging;
- destructive operations or writes outside the repository;
- unsupported platforms, data types, scale limits, or known failure modes;
- experimental, archived, internal-only, or unmaintained status.

## README Review Gate

Reject or rewrite a README when:

- it lacks installation or first-use instructions for a usable project;
- the quick start has no expected output or verification;
- it says what the project is but not why it exists;
- it describes internals before the consumer problem and public interface;
- it links to other docs instead of providing the entry path;
- it duplicates full reference material that has a canonical source;
- it hides credentials, network behavior, state, privacy, or destructive
  behavior;
- it uses arbitrary line limits to remove required facts;
- it has a "features" list where the reader still cannot tell what to do.

## Validation Checklist

- [ ] `writing-documentation` was loaded and followed.
- [ ] `reference/doc-types.md` supplied the README structure.
- [ ] The README states the concrete problem and audience.
- [ ] The README explains why the repo exists.
- [ ] Installation includes prerequisites and verification.
- [ ] Quick start is runnable and includes expected output or observable
      behavior.
- [ ] Required public names are present.
- [ ] Credentials, permissions, network behavior, persistence, and data
      boundaries are disclosed when relevant.
- [ ] Limits, unsupported cases, and maturity are stated when they affect use.
- [ ] Canonical references are linked instead of duplicated.
- [ ] No arbitrary length rule removed information required by the consumer.
