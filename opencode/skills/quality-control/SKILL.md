---
name: quality-control
description: Use when implementing, understanding, or delegating to the global quality control system in ~/ai/quality-control. Also use when setting up new projects with CI/CD, or when a local justfile needs to reference global QC recipes.
---
# Quality Control System

Before configuring, running, or modifying Quality Control checks, consult the central policy index:
[policy-index](file:///home/dzack/ai/opencode/skills/policy-index/SKILL.md)


The global quality control system at `~/ai/quality-control` provides centralized
linting, typechecking, formatting, complexity analysis, and code quality enforcement for
all projects. It is the single source of truth for QC workflows.

## Authority Hierarchy

When skill policies conflict, the following authority order determines which rule
prevails. A domain skill may narrow these policies for its domain but may not weaken
them.

| Rank | Skill | Owns |
| --- | --- | --- |
| **1** | `quality-control` | Generic QC invocation, public recipes, tool pins, and configs. No local reimplementation. |
| **2** | `test-guidelines` | Testing epistemology: what constitutes a proof, no mocks, no exceptions, no masking. |
| **3** | `tool-provisioning-and-environment-hygiene` | How tools run: ephemeral by default, uv-only Python, no pipx/pip/global npm. |
| **4** | `known-solution-first` | External tool/compiler/API uncertainty: public contracts before local probing. |
| **5** | `reality-grounded-debugging` | Diagnostic command discipline: stderr preservation, surface classification before mutation. |
| **6** | `writing-scripts-and-cli-interfaces` | CLI design patterns, project-owned dependency decisions, standalone script templates. |
| **7** | Domain skills | May narrow higher-ranked policies within their domain but may not weaken them. |

**Policy narrowing rule:** A domain skill may impose stricter requirements than a
higher-ranked skill (e.g., `test-guidelines` may add prohibitions beyond
`quality-control`'s defaults). It may not relax them (e.g., no skill may permit mocks
or pytest-mock).

**When a lower-ranked skill contradicts a higher-ranked skill, the higher-ranked skill
wins.** If `test-driven-development` says "mocks if unavoidable" and `test-guidelines`
says "no mocks, no exceptions," `test-guidelines` wins. If `clean-code` says "start with
try/catch" and `python-patterns` says "fail fast, no speculative try/catch,"
`python-patterns` (as a domain skill narrowing tool-provisioning's fail-loud doctrine)
wins.

The hierarchy is designed so that no skill below rank 3 can re-introduce mock seams,
local QC reimplementation, or global tool installation.

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

### Bridge-Burning Policies

Adhering to the [Bridge-Burning Policies](file:///home/dzack/ai/opencode/skills/anti-slop/SKILL.md#bridge-burning-policies) is a non-negotiable constraint for all development. These rules eliminate common agent validation-evasion pathways (such as runtime defaults, fallbacks, mocks, and diagnostic smoke tests in proof paths). 

Any exception to these rules must strictly follow the **Policy Exception Protocol** defined in [anti-slop/SKILL.md](file:///home/dzack/ai/opencode/skills/anti-slop/SKILL.md#policy-exception-protocol).

> [!IMPORTANT]
> **Bridge-Burning Red Flags:** If a construct would let an agent preserve the appearance of correctness while weakening the obligation, treat it as a red flag even if the code currently works. For a comprehensive catalog of code signatures, keywords, and patterns to look for, see the [Bridge-Burning Red Flags Reference Catalog](file:///home/dzack/ai/opencode/skills/reviewing-llm-code/references/bridge-burning-red-flags.md).



## Purpose

1. **Enshrine workflows** — Every workflow lives in the justfile.
   No ad-hoc scripts, no “I’ll just run this command directly”.
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

## Extending for Repo-Specific Testing

The global QC stack covers cross-project baselines: lint, typecheck, coverage,
complexity, copy-paste, and slop detection.
Individual projects may extend these with **domain-specific semantic tests** that
target their unique correctness requirements and the failure modes LLMs
systematically produce.

**Before adding any local QC extension, classify the check per the QC Extension
Gate below.** Extensions are only permitted for project-owned semantic tests.
Generic, reusable, or tool-configuration steps must be promoted to global QC —
they do not belong in local recipes or dev dependencies.

### QC Ownership

**Global QC owns:**
- generic linting, formatting, typechecking
- coverage machinery and thresholds
- bypass detection
- complexity checks, copy-paste detection, dead-code detection
- slop detectors and anti-pattern detectors
- tool versions and pins (ruff, mypy, biome, eslint, etc.)
- generic tool config files
- generic runner strategy (how tests execute, what gates compose)

**The project owns:**
- runtime dependencies
- build dependencies truly required by the project
- domain tests proving repository-owned behavior
- fixtures and real data needed by those tests
- minimal private adapters that connect project-specific tests to the global gate

**The project does not own:**
- its own generic lint/type/format/coverage stack
- duplicate tool pins
- local replacements for global QC
- public `lint`, `typecheck`, `coverage`, `check`, or similar QC recipes
- local scripts that should be global QC detectors
- generic QC tool installs in dev dependencies

### QC Extension Gate

Before adding any project-local QC recipe, script, tool config, or dev
dependency, classify the check:

1. **Does it verify this repository's domain semantics using project-owned
   fixtures/data?**
   - If yes: it may be local, private, and composed into `test`.
   - If no: continue.

2. **Could the same check apply to another repository?**
   - If yes: it belongs in `~/ai/quality-control`, not this repo.

3. **Does it encode a known LLM failure mode or anti-slop detector?**
   - If yes: promote it to global QC.

4. **Does it require a generic tool version, config file, ignore rule, or
   invocation pattern?**
   - If yes: global QC owns the tool/config/invocation.
     Do not pin it locally.

5. **Is it just a narrower way to run lint/typecheck/format/test/coverage?**
   - Reject it. Use the global recipe.

Local QC extensions are allowed only for project-owned semantic tests.
Reusable QC practices must be promoted upward.

### Promotion Pathway

When an agent wants to add a local QC step, it must classify it per the
Extension Gate above. Additionally:

- If the step catches a recurring LLM failure mode, it belongs in global QC.
- If the step appears useful in more than one repo, promote it to global QC.
- If unsure, do not add local QC silently; report the classification and ask
  for QC-owner direction.

Any change that adds project-local QC must report one of:

- "This is domain-specific and should remain local because ___."
- "This is reusable and was promoted to global QC in ___."
- "This appears reusable but was not promoted because ___; QC-owner follow-up
  is required."

### Mutation Testing

Mutation testing verifies that tests actually catch defects by introducing
controlled code mutations (flipping conditionals, swapping operators, deleting
statements) and asserting the test suite fails on each mutant.
A surviving mutant means tests are insufficient — the code might be buggy but
the tests are too weak to notice.

**Tools by language:**
- Python: `mutmut`, `mutpy`
- TypeScript/JavaScript: `stryker`
- Rust: `cargo-mutants`
- Java/Kotlin: `pitest`
- Go: `go-mutesting`

**Target:** Core logic modules — business rules, data transformations, public
APIs. Do not waste mutations on trivial getters/setters or framework glue.

### Property-Based Testing

Property-based testing asserts invariants over random inputs instead of
hard-coding examples.
This catches edge cases, off-by-one errors, type-incorrect assumptions, and
"works on my examples" reasoning — all common LLM failure modes.

**Tools by language:**
- Python: `hypothesis`, `crosshair` (symbolic/contract-based PBT)
- TypeScript/JavaScript: `fast-check`
- Rust: `proptest`, `quickcheck`
- Java/Kotlin: `jqwik`, `quickcheck`
- Go: `gopter`, `rapid`
- C++: `RapidCheck`

**Target:** Parsing, serialization, indexing, boundary computations, and any
function processing unbounded or untrusted input.

**Adversarial seeding:** Seed generators with values known to trigger LLM slop
— empty collections, sentinel values, mixed encodings, deeply nested
structures, extreme numeric ranges, overlapping intervals.

### Adversarial Design Against LLM Failure Modes

Tests must be explicitly designed to detect what LLMs systematically get wrong.
The following modalities are hard to game without actual correctness:

- **Gaming modalities:** LLMs learn to produce synthetic success signals —
  tests that pass trivially, coverage that exercises only happy paths,
  assertions that check tautologies. Mutation testing and property-based
  testing are the primary countermeasures because they cannot be satisfied by
  mimicking test structure.
- **Slop patterns:** Redundant assertions, tautological checks (e.g., `assert x
  is not None` without asserting actual values), testing only constructors or
  trivial getters, mocking external dependencies to avoid real integration
  testing, bypass comments (`# pragma: no cover`, `# type: ignore`).
- **Failure modes:** Off-by-one errors, swapped arguments, silent truncation,
  broken error handling (`except: pass`), assumptions about input shape,
  mixing mutability and immutability, ignoring return values.

### Structural Validation and Contract Enforcement

Projects must enforce data contracts at every boundary — API ingress, storage
serialization, inter-service communication, and configuration loading.
LLMs systematically produce type-incorrect or shape-incorrect data handling;
structural validation catches these at runtime or compile time without brittle
regex heuristics.

**Python:**
- `pydantic` — runtime data validation with type coercion, JSON schema export,
  and strict mode. Enforced via mypy's pydantic plugin.
- `msgspec` — fast serialization with schema enforcement.
- `dataclasses` with `@dataclass(slots=True, frozen=True)` — structural
  invariants where pydantic is overkill.

**TypeScript/JavaScript:**
- `zod`, `io-ts`, `valibot` — runtime schema validation at API and storage
  boundaries.
- TypeScript interfaces and types with `strict: true` in tsconfig — compile-time
  structural enforcement.

**Rust:**
- `serde` with `#[derive(Deserialize, Serialize)]` — compile-time contract
  enforcement for serialization boundaries.

**Go:**
- Struct tags with `go-playground/validator` — runtime boundary enforcement.

**Integration:**
QC does not enforce specific libraries via fragile grep patterns. Instead,
projects add targeted recipes that use the actual tooling:

- `_validate-models` — runs pydantic or zod validation on known model files
- `_schema-roundtrip` — property tests asserting serialize → deserialize →
  identity for all boundary types
- `_strict-compile` — tsc or mypy with strictest-available config

### How to Extend (Domain-Specific Only, After Gate Classification)

Project justfiles must NOT modify the global QC recipes.
Instead, wrap the global `test` and add project-specific (domain-owned) steps:

```justfile
# my-project/justfile
test:
  @just -f ~/ai/quality-control/justfile test
  @just _mutation-test
  @just _property-test
  @just _validate-models

_mutation-test:
  uv run mutmut run --paths-to-mutate src/my_project/

_property-test:
  uv run pytest tests/property/ -x -q

_validate-models:
  uv run python -m pydantic src/my_project/models/

test-ci: test
  @just -f ~/ai/quality-control/justfile test-ci
```

This preserves "delegate, never reimplement" while letting projects layer on
the adversarial depth their domain requires.

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
| `grain.toml` | Grain | Unused code and low-quality pattern detection |
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

## When QC Fails

When any QC check — build, typecheck, lint, format, complexity, or test — fails with
an opaque error or repeated failed attempt, load `reality-grounded-debugging` before
mutating the failing pipeline. It provides:

- Command-output discipline (preserve stdout, stderr, exit code)
- Surface classification (fixture, boundary log, intermediate dump, schema dump, diagnostic
  recipe, subprocess capture)
- A synthesis gate (raw observation, smallest reproducer, missing surface, verification path)

The failure indicates a missing debugging surface, not just a code defect to patch.
