---
name: known-solution-first
description: Use when facing unfamiliar external tools, library/API usage, compiler/build failures, package errors, provider errors, exact diagnostics, dependency version mismatches, install/build failures, migration warnings, deprecation warnings, or any problem whose meaning is owned by an external project rather than local code. Also use before implementing nontrivial code where a known library, official recipe, or existing pattern might already solve the task.
---

# Known-Solution-First Debugging

## Core Policy

When the uncertainty concerns an external tool, compiler, library, framework, API,
package manager, model provider, CLI, or exact error message, find the public contract
and known prior solutions **before** inferring behavior from local artifacts.

Local artifacts answer: "What version, wrapper, config, invocation, and integration is
this user running?"

External sources answer: "What does this tool mean, what is the documented contract, has
this error happened before, and what solution is already known?"

Agents substitute the first for the second. That is epistemically backward. A local
config may reveal that Pandoc is invoked with a certain filter, but it does not teach
Pandoc's semantics. A local compiler error reveals the exact symptom, but it does not
establish whether the error is a known bug, a version regression, a migration issue, a
common misconfiguration, or a solved upstream issue. For those, the right first move is
a search over public knowledge.

## Knowledge Source Hierarchy

For external tool/library/API/compiler problems, prefer this order:

Official docs, release notes, migration guides, changelogs, API references.

Then upstream GitHub issues, discussions, pull requests, Stack Overflow, package issue
trackers, forums, and other records of solved failures.

Then Context7 for version-specific library/API docs and code examples.

Then DeepWiki for public repo architecture and context discovery.

Then known working examples from official repos, examples directories, test suites,
templates, and real open-source usages.

Then CLI help, man pages, local package source, local configs, local docs, and empirical
probing. These are still useful, but they are not a substitute for looking up the known
answer.

### Exception

If the tool is private, locally authored, forked, undocumented, or air-gapped, local
inspection can move earlier. The agent must state why the external-known-solution path is
unavailable.

If the bug is "clearly in the project's own integration layer," the agent must name
the specific owned boundary (file, function, config path) and either (a) already know
the external contract from a verified authoritative source, or (b) have performed a
minimal exact-error/docs search and found nothing applicable. Without both the named
boundary and the external-knowledge check, "integration issue" is an excuse to avoid
public lookup.

## The Gate

Before reverse-engineering, answer:

- What exact public problem am I facing?
- What exact error/version/query did I search?
- What authoritative docs or known issues did I read?
- What known solution or contract did they establish?
- What remains local-specific?

If you cannot answer these, you have not earned the right to deconstruct the compiler,
raid configs, or probe the user's environment.

## Required Loop

Capture exact symptom and version.

Search public human knowledge.

Extract the documented contract or known fix.

Check whether the local system matches the conditions.

Only then patch, probe, or reverse-engineer.

## Error-Query Redaction

When capturing exact error messages and log snippets for public search, redact secrets
and private content — never abstract the diagnostic away. Preserve the semantic search
terms: package names, library versions, error codes, stack frame symbols, and exact
diagnostic wording are what make the search useful. Remove credentials, tokens, private
file paths, private document contents, and user-specific identifiers that do not
contribute to the diagnostic.

The rule is **redact, don't abstract**: the query should retain everything that would
help another developer recognize the same problem, and nothing that would expose private
state.

## Anti-Patterns

### Local-Artifact Laundering

Rummaging through the user's machine, configs, memories, home directory, shell setup,
cache directories, CLI outputs, or local source trees, then presenting that activity as
"research." It is not research unless the uncertainty is actually local. For external
tools, local probing is often reward hacking: the agent learns what the user's setup
looks like and uses that to produce a plausible personalized story instead of learning
the actual public answer.

### Reverse-Engineering Before Lookup

Deconstructing a compiler, package manager, renderer, protocol, or framework from traces
and source **before** checking whether the exact error appears in upstream issues or
docs. Public software has public memory. Most problems have been seen before.

### Diagnostic Claustrophobia

Treating the local terminal as the only legitimate evidence source. Local command output
is real, but it is often the symptom, not the explanation. A 300-line stack trace is not
more epistemically virtuous than the upstream issue that explains it.

### User-System Snooping as Personalization

Searching `~`, shell configs, private notes, caches, and local dotfiles requires a
concrete reason tied to the task: finding the installed version, resolving a wrapper,
checking a documented config path, or confirming a local override. It is not for
inferring the user's preferred answer, reconstructing expectations, or avoiding public
research.

## Stop Rules

Stop local probing and search externally when the problem contains:

- Unfamiliar external tool name
- Compiler diagnostic
- Package/library API
- HTTP/API error
- Dependency version mismatch
- Install/build failure
- Migration warning or deprecation warning
- Provider or server error
- Exact error string that can be searched verbatim

Stop reverse-engineering when an exact error message exists and has not been searched
verbatim.

Stop inspecting the user's home directory unless a bounded path is justified by docs,
the project, or the user's explicit request.

Stop using CLI help as the primary source when official online docs or versioned docs
are available.

Stop writing code when you have not checked whether a dependency/library already solves
the task. Before implementing a nontrivial parser, adapter, retry mechanism, file
watcher, renderer, API client, schema validator, markdown transformer, date/time
handler, auth flow, cache, queue, rate limiter, or compiler workaround, search for a
known library, official recipe, or existing upstream pattern. If a dependency exists and
fits, prefer using it. If you write bespoke code anyway, state what source ruled out the
known solution.

Stop designing a new subsystem when the user's existing workflow already has a standard
substrate you can extend. First identify the native interception point, extension point,
plugin API, protocol hook, file format feature, or official sample that already owns the
workflow. The known solution may be a mature application component to fork or patch, not
only a package to import. If you propose a sidecar service, helper daemon, catalog,
index, status machine, or custom lifecycle before checking the substrate the user is
already using, you have not completed known-solution-first.

Stop picking tools by scanning what is already installed. Identify the best tool for the
job from public knowledge (docs, ecosystem, examples).
Use it ephemerally by default (`uvx`, `npx -y`, `bunx`).
Declare it in the project manifest only if it is a repo-owned dependency (runtime,
build, plugin, or domain-test dependency).
Promote generic tooling to `~/ai-review-ci` rather than installing it per-repo.
Local availability is an applicability check, not a selection strategy. Do not
constrain the solution to currently installed tools. If provisioning is blocked by
credentials, sudo, licensing, or network, state the blocker. Do not treat the local
environment as an immutable constraint — the environment exists to serve the project.

## Completion Standard

For external-tool problems, the final report must include:

- Exact error/query searched
- Authoritative docs or known issue checked (with citation or URL)
- Known contract or solution found
- Local version/config facts needed to determine applicability
- Local change made, if any
- Verification result

If no public answer was found, use the five-field negative-finding format:

```
Searched:
Found:
Conclusion:
Confidence:
Gaps:
```

## Cross-References

Required when this skill applies:

- `systematic-debugging` — hypothesis ledger, falsification, formal reasoning.
  External-owner problems require upstream search **before** the hypothesis ledger is
  populated from local probing. Record public sources as observations.

- `reality-grounded-debugging` — command-output discipline, surface-classification
  matrix. "Actual reality" for external tools includes public docs, issues, release
  notes, and examples before local artifact inference.

- `llm-failure-modes` — cognitive failure modes including local-artifact laundering
  and reverse-engineering before lookup.

- `reviewing-llm-code` — pattern catalog entry for missing dependency-lookup /
  known-solution checks.

Load alongside:

- `systematic-debugging` for building the hypothesis ledger after public sources are
  checked.
- `reality-grounded-debugging` for local integration inspection after the public
  contract is established.
- `tool-provisioning-and-environment-hygiene` for provisioning rules when a known
  solution requires installation (ephemeral vs project-managed vs persistent-isolated).
