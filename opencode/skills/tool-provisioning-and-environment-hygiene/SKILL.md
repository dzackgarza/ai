---
name: tool-provisioning-and-environment-hygiene
description: Cross-cutting policy for tool installation. Covers when to use uvx/npx/bunx vs uv add/npm install vs uv tool install/pipx vs OS package managers. Bans pip install --break-system-packages, system Python mutation, and installed-tool-first selection.
---
# Tool Provisioning and Environment Hygiene

## Core Policy

Use the right provisioning mechanism for the intended lifetime:

| Scope | Mechanism | Example |
| --- | --- | --- |
| One-off CLI invocation | Ephemeral runner | `uvx`, `npx -y`, `bunx` |
| Project dependency | Project package manager | `uv add`, `npm install --save-dev`, `bun add --dev` |
| Persistent user tool | Isolated tool manager | `uv tool install`, `pipx install` |
| OS-level package | OS package manager | `apt install`, only when authorized |

Do not mix tiers. If a tool is needed once, use an ephemeral runner. If a tool is a
project dependency, declare it in the project manifest. If a tool is a persistent user
tool, install it with an isolated tool manager. Only reach for the OS package manager
when the task requires it and the user has authorized that scope or the repo explicitly
documents it.

## Prohibitions

- Never use `pip install --break-system-packages`.
- Never install into system Python.
- Never install globally (`npm install -g`, `cargo install`, `go install`) just to avoid
  using an ephemeral runner or declaring a project dependency.
- Never decide against a better dependency because it is not currently installed.
  Local availability is an applicability check, not a selection strategy.
- Never write fallback code, stubs, soft degradation, or reimplementation when a missing
  dependency would solve the task. Declare and provision it instead.

## If a Dependency Is Missing

Stop. Do not write fallback code. Do not substitute a worse tool. Do not skip the
dependency and reimplement it. Declare the dependency through the correct mechanism and
provision it. Only ask the user if credentials, sudo, licensing, or network blocks the
provisioning.

## Stderr Discipline

Commands that are diagnostic (investigation, install, build, discovery, extraction,
verification) must preserve stdout, stderr, and exit code. Never suppress stderr on
diagnostic commands.

If output suppression is intentional in a non-diagnostic context (cleanup recipes,
`curl -s` for API responses consumed by `jq`, known-safe fallbacks in auth detection),
the suppression must be named as such and must not appear in examples for
investigation, install, build, discovery, extraction, or verification.

## Home-Directory Mutation

Do not write to or probe `~` unless the task has a concrete, bounded reason. Skill
examples that normalize home-directory paths or file-based operations must state the
bounded permission: the user explicitly asked to perform this action, these are the
allowed target paths, and this does not authorize general home-directory inspection or
global tool installation.

## Cross-References

Required when any skill provides tool-installation instructions:

- `known-solution-first` — external-tool uncertainty must start with public contracts,
  docs, and known solutions before CLI probing or local artifact inspection.

- `reality-grounded-debugging` — command-output discipline, stderr preservation,
  surface-classification matrix.

- `python-patterns` — uv-only, `uv run` metadata blocks for standalone scripts.

Load alongside any skill that provides `pip install`, `npm install`, or tool-install
examples to check compliance.
