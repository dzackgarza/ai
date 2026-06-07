---
name: bespoke-software-policy
description: |
  Load as a mandatory filter before ANY code review or sweep analysis.
  Applies the project's bespoke-software rules to every finding before reporting.
---

# Bespoke Software Policy

This repository targets the owner's actual machines with enforced conventions.
It is NOT distributed, multi-platform, or multi-user. Apply these rules to
EVERY finding before reporting.

## In Scope (Valid Findings)

Report these if they cause observable harm:

- **Actual bugs** — wrong behavior, crashes, data corruption
- **Build/test failures** — commands that don't run or produce wrong output
- **Config that breaks a concrete workflow** — a change that prevents the owner
  from doing their work (not "might break on another machine")
- **Architectural decay that causes real friction** — not speculation about
  future pain, but changes the owner has actually complained about

## Out of Scope (Suppress Immediately)

The following are NEVER valid findings in bespoke software.
If a finding matches any of these, suppress it without reporting:

### Portability
- Hardcoded `/home/dzack/` paths or any absolute local paths. Directory
  structure is enforced across the owner's machines. These are intentional.
- Machine-specific config files (`.serena_config.yml`, local editor configs,
  personal tool configs). They are machine-specific by design.
- Non-portable conventions, shell aliases, or tool choices. Portability
  across machines is not a goal.
- Version ranges that look "too narrow." The convention is latest unless
  pinning is strictly required. `requires-python = ">=3.14"` is correct.

### Enterprise Patterns
- Missing multi-platform support, scaling features, containerization,
  horizontal scaling, or cloud-native patterns.
- Missing security hardening, RBAC, audit logging, or compliance features.
- Missing CI/CD for multiple architectures or operating systems.

### Backward Compatibility
- Breaking changes. There are no legacy consumers. Every change is breaking
  by default. Do not report interface changes, removals, or renames as
  compatibility defects.
- Deprecation warnings from updating to latest libraries. The fix is to
  adapt to the new API, not to pin the old version.

### Meta / Infrastructure
- The agent's own configuration (AGENTS.md, .agents/, skills/, prompts/).
  If it had a concrete defect, the user would see task failures.
- CI pipeline files (.github/workflows/, quality-control/). The mechanism
  is not the target.
- Stale backup files, temporary markers, throwaway comments. Housekeeping
  is Tier 2 at most and only reported when no significant issues exist.

### Speculative / Unverifiable Claims
- "This might cause issues in the future" without a specific observable
  mechanism. Every finding must identify a concrete defect that exists NOW.
- "Context dilution" or "cognitive overload" for the agent's own prompt
  length. The agent cannot test this claim.
- "A future contributor might be confused" — there are no future unknown
  contributors. The only audience is the owner.

## Verification Rule

For every potential finding, ask: "Does this cause a concrete problem for
the owner RIGHT NOW on their actual machine?" If no, suppress it.

For every proposed remedy, ask: "Does this make the software work better
for the owner on their actual machine?" If the remedy only helps an
imagined future scenario, reject it.
