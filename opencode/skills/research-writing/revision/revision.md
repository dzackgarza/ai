---
name: scholarly-paper-revision
description: "Use when revising an existing scholarly manuscript or integrating research sources into its LaTeX project."
---
# Scholarly Manuscript Revision

## Scope and source

Read the root document, affected includes, and adjacent argument before editing.
Establish the audience, requested change, document class, bibliography, macro files,
and build command from the project. Ask only for information these sources cannot
settle. Keep the existing genre, organization, voice, notation, and claims except
where the requested revision requires a change. Creation templates and proof-format
defaults do not authorize restructuring an existing manuscript.

Match the revision to the request. A local correction stays local. Do not impose a
survey format, graduate tutorial, length target, section scheme, title formula,
summary box, or additional deliverable. Improve teaching through explanations the
intended reader needs, rather than through a prescribed teaching format.

## Argument and evidence

Check grammar, order of explanation, and notation together with the argument.
Introduce unfamiliar objects and necessary hypotheses before use. For claims within
scope, check the derivation, domain of validity, dimensions or units where relevant,
and supporting citation. Retain qualifications and distinctions during compression.
Repair established gaps within the authorized scope; otherwise identify the passage,
the missing justification, and a possible correction with its remaining uncertainty.
Use examples or expanded derivations when they resolve a real reader difficulty.

When integrating supplied material:

- Separate research evidence from macro definitions and examples of typography or style.
- Read the relevant source text and appendices. Match each imported assertion to its
  page, theorem, assumptions, and bibliography entry; translate notation explicitly.
- Retain attribution and conflicting conclusions. Identify which claims are cited
  results, worked illustrations, or contributions of the manuscript.
- State which necessary sources could not be accessed. An abstract or secondary
  summary does not establish review of a proof in the full paper.
- Use actual supplied or verified results. Substantial new experiments require
  authorization; plausible numerical outcomes cannot fill missing evidence.

For a substantive exposition review, trace whether the reader can reach each result
from the preceding definitions and hypotheses. Check whether examples illustrate the
stated scope and whether transitions express actual mathematical dependencies.
An independent review is optional when available and authorized, not a requirement
for a small edit. Keep unresolved mathematical issues distinct from prose judgments.

## Editorial pass

Apply [[writing/clarity/clarity|clarity]] and
[[llm-failure-modes/scholarly-prose|scholarly prose patterns]]. Use the catalog's
passage-level evidence rule: a stylistic cue alone does not justify an edit.
Preserve exact terminology, useful contrast, and distinctive authorial rhythm.

## LaTeX preservation and verification

Keep the project's existing macro environment. Use its definitions and supplied
macros; add local definitions for local needs. Resolve a local name collision locally
instead of changing shared macros. A preferred macro bundle is a possible starting
point for a new standalone document, not a dependency to inject into an existing one.

Follow [[mathematics/writing/latex-compile-qa/latex-compile-qa|LaTeX compile and QA]]
with the actual project root and configured engine. Inspect the log and affected PDF
pages, including changed equations, references, and page breaks. Rebuild after the
last source edit. A successful build establishes typesetting, not mathematical truth.
Build helpers must preserve the project's conventions; page bounds require an actual
task constraint. Deliver the requested source and output, with verification and any
material unresolved limits stated accurately.
