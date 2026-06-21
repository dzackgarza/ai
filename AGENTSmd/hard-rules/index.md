---
order: 70
title: Hard Rules
---

Use `tree` to understand your surroundings (for local project structure).
Do not just use ls, grep/rg/ag/etc, which only show narrow slices.
For tool/API/compiler unknowns, use `known-solution-first` instead — the first pass is
web search, Context7, DeepWiki, and upstream docs, not local `tree`.
Never implement fallback behaviour, soft defaults, “graceful” error handling, or fail-open conditions. Every error path must fail loudly. Silence is a bug.
No legacy flags. No deprecated symbols. No “backwards-compatible” shims. Breaking changes are fine — we are in development.
When revising feature A to work more like feature B, clean up the codebase as if feature A had never existed: delete the old implementation, its tests, its types, its exports, its config entries. Do not wrap it in a `deprecated` annotation, do not gate it behind a feature flag, do not preserve it as a fallback path, do not add a compatibility adapter. The old thing is gone. The new thing replaces it entirely.
Agents have an asymmetric risk model (see `llm-failure-modes/coding-failures.md` #20): they treat adding code as safe and deleting code as dangerous, even when tests prove the replacement is correct. This compulsion produces codebase bloat — every refactor becomes additive (+2 files, +492 lines of legacy wiring) instead of net-negative. Resist it. When tests exist that cover the replacement, deletion is safe. Delete.
A second-pass cleanup in clean context is a proven mitigation: after implementing a change, explicitly re-read the diff in a fresh context and strip every fallback, legacy branch, and defensive guard that the tests do not require. The first pass implements; the second pass deletes everything the first pass was too cautious to remove.
When reviewing code (your own or others'), explicitly check for: guards against impossible conditions (the invariant already holds upstream), over-engineered abstractions unnecessary for the codebase's current state, backwards-compatibility shims preserving code that no consumer requires, and any fallback branch that exists "just in case" rather than because a test proves it's needed. Make a plan to remove these, making the code more concise, easier to reason about, and cleaner.
Stating the deployment context matters: this is dev/test mode on a single-user system, not production. Code bloat from defensive fallbacks is the primary risk, not missing edge-case handling. Agents that aren't told this explicitly will default to preserving fallbacks — the asymmetric risk model (#20) overrides standing rules unless the context is made explicit in the prompt.
This system is pre-launch. There are no existing users. There is no one depending on any interface, any API, any data format, any config key. Backwards compatibility is not merely unnecessary — it is a fiction. There is nothing to be compatible *with*. Every "in case a consumer requires this" guard is guarding against a consumer that does not exist. An API key will not grow legs and walk out of the .env. A save format has no players whose saves would break. Delete the old code. Delete the old docs. Technical debt is the enemy; unused code is its raw material.
Agents treat their own just-generated mistakes as having the same preservation weight as mature, deployed code — building backwards compatibility to an incorrect function they wrote five minutes ago, as if it had a large customer base depending on it. Code the agent itself produced has zero deployment history and zero users. It is not legacy. It is not mature. It is not a constraint. It is a draft. If it was wrong, replace it entirely — do not wrap it in a fallback, do not annotate it as deprecated, do not wire a compatibility shim to it.
The named rationalizations to reject: "for compatibility with legacy code," "normalize function for existing call pattern," "in case the API is unavailable," "to gracefully handle missing dependencies." These are all inventions — there is no legacy code (this system is pre-launch), no existing call patterns (the agent just wrote them), no unavailable APIs (the network is available). There are no optional missing dependencies. If a tool or dependency is needed, provision it through the approved runner/global-QC/uv pathway and fail loudly if that pathway is blocked. Do not `try import`. Do not conditionally import. Do not catch `ImportError` and substitute a stub. If a dependency is needed, declare it and fail if absent. Do not bloat function signatures with optional arguments for hypothetical callers that do not exist — every parameter should be required by an actual call site in the codebase right now.

All software written here is bespoke, for one user, on one system, tightly integrated with the tools on this system. It is not distributed, not multi-platform, not designed to scale, not built for unknown audiences. There is no “legacy user” — the only user is the owner, immediately after the task is done, expecting the old functionality to have vanished as if it never existed. Every change is a breaking change by default.
Do not attempt multi-platform support, horizontal scaling, or imagined security hardening. These are enterprise patterns — they do not belong in bespoke software. The correct behavior is: work on happy paths, fail loudly and immediately outside of them. Do not prototype edge cases; prototype permutations of happy paths instead. Block non-happy branching and edge behaviours with sharp assertions, not soft guards. Put the user experience on guardrails that don’t accept veering.
Complete opinionated config only. No runtime defaults. The app may ship with a generated/starter config populated with values. Runtime code must validate that config and fail if required values are missing. No env-var switching, no feature-flag toggling, no runtime mode selection. The software runs one way, on this system, with these dependencies. If something needs to change, change the config, commit it, and move on — do not parameterize against imagined future variation.
Do not aim for “legacy” compatibility, preservation of historical artifacts, or interop with old versions.
Do not write code that gracefully accepts malformed inputs or data, or makes “best effort” attempts.
Instead: understand explicit data shapes, assert correctness, fail loudly.
Force data to be fixed and fit explicit schemas.
Enumerate accepted types. Interfaces must loudly reject malformed data — silence is a bug.
Short-circuit paths with optional data to quickly normalize and assert existence.
Eliminate weakly typed signatures: optional, “Any”, “unknown”, by understanding the exact data you are working with and enforcing it.
If you don’t know what the data looks like, do not write code for it.

**Never suppress stderr to construct a synthetic fallback result.**
`cmd 2>/dev/null || echo "guess"` — silences the diagnostic that would tell you what actually happened, then substitutes your own guess. Every failure mode now produces the same indistinguishable string.

**Checkpoint before every edit.** `git commit` (or `git add`) the current state BEFORE editing.
Verify with `git diff` after.

**Self-contained Python scripts (mandatory).**
Any agent-authored Python script that imports third-party (non-stdlib) packages must
declare dependencies as PEP 723 inline script metadata and run through `uv`. No
separate install step. No implicit environment assumption. No `pip install` prelude.
The full policy (hierarchy, forbidden pathways, canonical template, review rule) is in
`tool-provisioning-and-environment-hygiene` under "Self-Contained Python Scripts with uv".
