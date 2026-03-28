---
name: quality-control
description: Use when implementing, understanding, or delegating to the global quality control system in ~/ai/quality-control. Also use when setting up new projects with CI/CD, or when a local justfile needs to reference global QC recipes.
---
# Quality Control System

The global quality control system at `~/ai/quality-control` provides centralized
linting, typechecking, formatting, complexity analysis, and code quality enforcement for
all projects. It is the single source of truth for QC workflows.

## High-Level Policies

### Minimal Public API

**Only two public recipes exist:** `test` and `test-ci`. Everything else is private
(prefixed with `_`). This prevents cherry-picking — agents cannot run just `lint` or
just `typecheck` in isolation to bypass the full stack.

### Auto-Fix Before Check

The `test` recipe runs `_normalize` first, which executes:
- `ruff check --fix .` — auto-fix lint errors
- `ruff format .` — auto-format code

Only after normalization does the full QC stack run.
This ensures code is in a consistent state before any assertions.

### Full Stack, No Exceptions

`just test` runs the complete QC pipeline.
There is no separate `just lint` or `just typecheck` for agents to use.
Running only typecheck is insufficient — the full stack must pass.

### No-Bypass Policy

Bypass comments are explicitly blocked in staged files:
- `# pragma: no cover` — Python coverage bypass
- `// istanbul ignore` — JS coverage bypass
- `# noqa` — Python lint bypass
- `# type: ignore` — Python type bypass
- `@ts-ignore` — TS type bypass
- `@ts-expect-error` without comment — TS expect-error without justification
- `// eslint-disable` — ESLint bypass

**Rule:** Fix the underlying issue, never hide it with a bypass comment.
If you find yourself needing a bypass, escalate to the user for QC agent review/approval
instead.

## Purpose

1. **Enshrine workflows** — Every workflow lives in the justfile.
   No ad-hoc scripts, no "I'll just run this command directly".
   Justfile is the single source of truth for project operations.

2. **Fix opinionated workflows** — Agents cannot cherry-pick checks.
   For example, `just typecheck` does NOT assert code quality — the `test` recipe runs
   the full QC stack. Running only typecheck is insufficient.

3. **Abstract complexity** — Env management, sandbox setup, tool installation, common
   tasks — all hidden in private recipes.
   Users run workflows, not infrastructure.

## Two Justfiles

### Python: `justfile`

Location: `~/ai/quality-control/justfile`

Used for: Pure Python projects, Python CLI tools, Python packages.

Recipes:
- `just test` — Local quality checks: normalization, bypass detection, coverage,
  diff-cover, vulture, deptry, semgrep, jscpd, lizard, import-linter, codeql,
  ai-slop-detector
- `just test-ci` — **superset of test**, adds live/isolated checks (coverage thresholds,
  diff-cover against base branch, integration tests)

### TypeScript: `justfile-bun`

Location: `~/ai/quality-control/justfile-bun`

Used for: TypeScript projects, Bun-based packages, Node.js CLIs.

Recipes:
- `just test` — Local quality checks: bypass detection, coverage, diff-cover, knip,
  biome, ast-grep, eslint, tsc, semgrep, jscpd, lizard, codeql, lint-staged
- `just test-ci` — **superset of test**, adds live/isolated checks (coverage thresholds,
  diff-cover against base branch, integration tests)

## Usage in Local Projects

**Never reimplement QC locally.** Local justfiles must delegate to the global justfile:

```justfile
# my-project/justfile
test:
  @just -f ~/ai/quality-control/justfile test

test-ci:
  @just -f ~/ai/quality-control/justfile test-ci
```

Or for TypeScript/Bun projects:

```justfile
# my-project/justfile
test:
  @just -f ~/ai/quality-control/justfile-bun test

test-ci:
  @just -f ~/ai/quality-control/justfile-bun test-ci
```

## Hooks

Pre-commit and pre-push hooks block on `just test`. Copy/symlink into `.git/hooks/`:

```bash
ln -s ~/ai/quality-control/pre-commit.hook .git/hooks/pre-commit
ln -s ~/ai/quality-control/pre-push.hook .git/hooks/pre-push
```

## Global Configs

The QC system uses these configs (all stored in `~/ai/quality-control/`):

| Config | Tool | Purpose |
| --- | --- | --- |
| `ruff-global.toml` | Ruff | Python linting (E, F, I, UP), Python 3.14, strict |
| `mypy-global.ini` | Mypy | Python type checking, strict mode |
| `pytest-local.ini` | pytest | Python test configuration |
| `pyproject.toml` | Various | Python project metadata |
| `biome.json` | Biome | TypeScript/JS formatting and linting |
| `eslint.config.js` | ESLint | TypeScript/JS linting |
| `knip.json` | Knip | TypeScript/JS dead code detection |
| `semgrep.yml` | Semgrep | Custom security and quality rules |
| `.jscpd.json` | jscpd | Copy-paste detection |
| `sgconfig.yml` | ast-grep | Custom AST-based rules |
| `.lintstagedrc.json` | lint-staged | Pre-commit hook staged file processing |
| `.slopconfig.yaml` | ai-slop-detector | AI-generated code detection |
| `.coveragerc` | coverage.py | Coverage configuration |
| `ast-grep/rules/` | ast-grep | Custom rule definitions |

## Workflows

### Local Development

```bash
just test       # Run all local QC checks
just test-ci    # Run all checks including CI-specific ones
```

### CI Pipeline

Projects should run `just test-ci` in CI to match local + CI checks.

## Key Principle

**Delegate, never reimplement.** Local projects use global QC infrastructure.
The QC agent owns rule changes, not individual projects.
