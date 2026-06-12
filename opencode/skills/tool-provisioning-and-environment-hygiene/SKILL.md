---
name: tool-provisioning-and-environment-hygiene
description: Cross-cutting policy for tool installation. Covers when to use uvx/npx/bunx vs uv add/npm install vs uv tool install vs OS package managers. Bans pip install --break-system-packages, system Python mutation, pipx, and installed-tool-first selection.
---
# Tool Provisioning and Environment Hygiene

## Core Policy

Use the right provisioning mechanism for the intended lifetime:

| Scope | Mechanism | Example |
| --- | --- | --- |
| Generic tool / QC tool / inspection tool | Ephemeral runner, usually from global QC | `uvx`, `npx -y`, `bunx`; see `quality-control` |
| Python CLI one-off | Ephemeral runner | `uvx`, `uvx --from package` |
| Project dependency (repo-owned runtime/build/plugin/domain-test only) | Project package manager | `uv add`, `npm install --save-dev`, `bun add --dev` |
| Agent-authored Python script with deps | PEP 723 + `uv run` | See self-contained scripts policy below |
| Persistent Python user tool (exceptional) | Isolated tool manager | `uv tool install` only |
| OS-level package | OS package manager | `apt install`, only when authorized |

Do not mix tiers. If a tool is needed once, use an ephemeral runner. If a tool is a
project dependency, declare it in the project manifest. If a tool is a persistent user
tool, install it with an isolated tool manager. Only reach for the OS package manager
when the task requires it and the user has authorized that scope or the repo explicitly
documents it.

## Prohibitions

> [!IMPORTANT]
> All code produced under this skill must adhere to the [Bridge-Burning Policies](file:///home/dzack/ai/opencode/skills/anti-slop/SKILL.md#bridge-burning-policies) in `anti-slop/SKILL.md`. These are non-negotiable hard constraints that eliminate runtime defaults, fallbacks, mocks, optional critical dependencies, and other agent validation-evasion pathways.

- Never use `pip install --break-system-packages`.
- Never install into system Python.
- Never use `pipx`.
- Never use `pip` in any context.
- Never install globally (`npm install -g`, `cargo install`, `go install`) just to avoid
  using an ephemeral runner or declaring a project dependency.
- Never install generic QC tools (ruff, mypy, pytest, pytest-cov, coverage, basedpyright,
  etc.) as per-repo dev dependencies. These belong in global QC at `~/ai-review-ci`.
  Project dev dependencies are for repo-owned runtime/build/plugin/domain-test dependencies.
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

## Self-Contained Python Scripts with uv

### Core Rule

Any Python script created by an agent that imports non-stdlib packages must be
self-contained with PEP 723 inline script metadata and run through `uv`. No separate
install step. No implicit environment assumption. No `pip install` prelude.

### Canonical Template

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "httpx>=0.28",
#   "rich>=13",
# ]
# ///

import httpx
from rich.pretty import pprint

response = httpx.get("https://example.com")
response.raise_for_status()
pprint(response.text[:200])
```

Run as either:

```bash
uv run script.py
```

or, if executable:

```bash
chmod +x script.py
./script.py
```

### Accepted Hierarchy

| Scenario | Mechanism |
| --- | --- |
| Generic QC tool / inspection tool | Ephemeral runner, usually from global QC (`~/ai-review-ci`). See `quality-control`. |
| Python CLI tool | `uvx tool ...` |
| Python CLI where package name differs from command | `uvx --from package command ...` |
| One-shot Python snippet with dependencies | `uv run --with package python - <<'PY' ... PY` |
| Python script written to disk | PEP 723 inline metadata + `uv run` |
| Executable Python script | `#!/usr/bin/env -S uv run --script` + PEP 723 inline metadata |
| Existing uv project | `uv sync` + `uv run ...`; `uv add` only for repo-owned dependencies (runtime, build, domain-test). Generic QC tools go in global QC. |

`uv run --with ... script.py` is acceptable for a transient one-shot command written and
discarded in a single session. But if the script is written to disk, checked in, handed
to another agent, documented in a skill, or reused as a recipe, dependencies belong in
the script metadata. `uv run --with` must not become a hidden install surrogate
scattered across docs.

### Forbidden Pathways

```
No pip install.
No python -m pip install.
No pipx (already prohibited above).
No ad hoc venv.
No "install these requirements first" script prelude.
No assuming the current interpreter has the imports.
No checking what is installed and adapting downward.
```

### Hard Review Rule

Reject any agent-authored Python script that imports third-party packages but lacks
PEP 723 / uv inline script metadata, unless it is inside an existing uv-managed project
and intentionally uses that project environment.

This must be checked in every review pass — code review, PR review, gate review, or
spot-check of any agent-produced artifact.

### Related Skills

- `known-solution-first` — external-tool uncertainty: start with public contracts,
  docs, and known solutions before CLI probing or local artifact inspection.

- `reality-grounded-debugging` — command-output discipline, stderr preservation,
  surface-classification matrix.

- `python-patterns` — uv-only, PEP 723 inline metadata for standalone scripts.

- `writing-scripts-and-cli-interfaces` — standalone script template, Cyclopts/Pydantic.
