# Agentic Delivery Doctrine

This repository is the configuration, prompt, and skill hub for an agentic development system. Its doctrine is not to add process for its own sake. Its doctrine is to make agent work public, convergent, and proof-bearing enough that agents can execute most of the loop without hidden local state or human rescue.

## Canonical State

GitHub PRs, issues, milestones, and review threads are the public execution graph. Local plans, transcripts, scratch files, and memory records are support surfaces, not the authoritative project state.

Rules:

- Put plans, contracts, residue ledgers, review dispositions, and completion evidence on the GitHub surface when they govern project work.
- Use local memory for reusable operational guidance and resumption context, not as a private substitute for issue or PR state.
- A checked item in a PR body needs evidence that another agent can inspect, such as a commit, a CI run, a review-thread disposition, or a linked issue.
- Do not close work by producing an artifact that only changes representation. The substantive user boundary remains the acceptance condition.

## Proof Boundary

Green checks are not enough unless the proof path crosses the boundary the user actually depends on.

Rules:

- Prefer user-observable proof over implementation-internal proof: app boot, rendered page, CLI command, live add-on/API state, generated config, branch protection, or deployed/staged behavior.
- Treat tests that mock the owned boundary as unit coverage only. They cannot prove startup, network integration, browser behavior, native wrapper behavior, or live data correctness.
- When a failure reaches the user boundary after a green suite, treat that as a system failure in the proof design, not as an isolated implementation mistake.
- Convert every false-green class into a rule, fixture, gate, or skill update.

The `zotero-gui` PR #7 startup failure is the standing calibration case: review volume, test volume, and large PR bodies did not matter because the proof chain missed the actual app-start boundary.

## Process Allocation

Use the smallest workflow that preserves fail-loud correctness at the relevant risk boundary.

Rules:

- Low-risk single-surface changes can use narrow inspection and focused proof.
- Medium-risk feature work needs user-story proof before helper-level proof can be treated as sufficient.
- High-risk changes to app startup, persistence, external APIs, GitHub state, branch protection, review gates, memory migration, or shared QC require explicit public tracking and boundary proof.
- Do not expand bounded tasks into broad cleanup. Do not shrink substantive goals into administrative completion.

## Review Convergence

Review must block unsafe work, but it must also converge.

Rules:

- Findings need stable identity, provenance, and state. Reposting the same catalog across pushes is review churn, not diligence.
- Every review thread needs a visible disposition: accepted with commit evidence, rejected with reason, or split into a tracked issue.
- Do not let agents self-resolve review feedback through agreement language, bulk dismissal, hidden owner approval claims, or local-only notes.
- Reviewer prompts and triage skills should be calibrated against accepted and rejected ground-truth cases, not assumed to improve because wording changed.

## Known Surfaces First

Owned code and doctrine should shrink bespoke glue unless the project owns a real domain obligation.

Rules:

- Prefer standard parsers, typed models, schema validators, mature libraries, official CLIs, and framework-native surfaces over hand-rolled parsing or ad hoc dictionaries.
- If a custom parser, schema, adapter, or merge helper remains, name the domain obligation it owns and the proof that keeps it honest.
- Use CLI-first product surfaces for tools. OpenCode, MCP, and other adapters should be thin wrappers around a standalone operational CLI when possible.
- Do not make local filesystem coupling the integration model between projects. Route dependencies through GitHub, package managers, `uvx`, or `npx -y` unless the repo explicitly owns the local boundary.

## Durable Learning

Agent behavior improves through observed failures converted into executable doctrine.

Rules:

- Convert recurring failures into object-level rules, fixtures, gates, or skill edits.
- Evaluate prompt and skill changes where ground truth exists. A stronger-sounding instruction is not evidence that agent behavior changed.
- Distinguish doctrine from history. Commit messages record completed work; issues track gaps; memory records reusable operational guidance; wiki pages record stable doctrine.
- Keep doctrine specific enough to execute: trigger, required action, proof boundary, and stop condition.

## Research And Data Artifacts

Research notes, metadata pipelines, and source-derived records follow the same proof doctrine as code.

Rules:

- Give every research artifact an owner, path, source relation, and proof burden. A folder of residue is not a project surface.
- Distinguish source-authority material from derived notes, generated cards, normalized metadata, and dashboards.
- For mathematical or document repositories, compileability, rendered output, searchable text, and source linkage are boundary proofs, not cleanup polish.
- Treat external metadata and document matching as adversarial identity work. A normalized record proves only its relation to the pinned source snapshot; a separate identity check must catch wrong-source matches.
- Use `needs_review` for wrong-identity or insufficient-identity cases instead of falsely verifying a plausible record.

## Long-Running Work

Long-running agent work is acceptable only when bounded, resumable, and externally tracked.

Rules:

- External-source cascades need per-source timeouts, per-item and per-batch budgets, explicit disabled/quota-dead states, and a real `needs_review` disposition.
- `needs_review` is valid only after the intended search space has been exhausted or a documented blocker prevents safe completion.
- Progress state for long loops belongs in GitHub issues or typed project memory, not in chat-only status.
- Restarting a long loop must resume from explicit queue state and blocker buckets, not from reconstructed vibes.

## Documentation Shape

Write agent-facing doctrine as constraints agents can execute.

Rules:

- Prefer direct rules over meta-commentary about agent psychology.
- Preserve concrete commands, paths, evidence requirements, state machines, and prohibitions when migrating doctrine.
- Use progressive disclosure: overview pages route to focused pages; focused pages carry the operational detail.
- If a doctrine edit moves knowledge from one surface to another, compare the destination against the source before retiring or relying on the old surface.
