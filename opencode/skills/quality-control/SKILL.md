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

### Auto-Fix Enforcement: Always Apply All Available Fixes

**Rule:** Agents MUST always apply all available auto-fixes when running any default recipe (`just test`, `just test-ci`). This is not optional, not a "best effort," and not conditional on whether failures are expected. Fixes run first, checks run second.

#### What happens when you run `just test`

The `test` recipe runs `_normalize` before any checks. This applies every auto-fix the toolchain supports:

**Python stack (`~/ai/quality-control/justfile`):**
| Tool | Flag | Fixes |
| --- | --- | --- |
| `ruff check` | `--fix` | Lint errors (E, F, I, UP) — unused imports, import sorting, pyupgrade patterns |
| `ruff format` | (implicit) | PEP 8 style formatting |
| `semgrep` | `--autofix` | Security and quality pattern fixes |
| `grain` | `--fix` | Unused code removal |

**TypeScript stack (`~/ai/quality-control/justfile-bun`):**
| Tool | Flag | Fixes |
| --- | --- | --- |
| `biome check` | `--write --unsafe` | Formatter, linter, import sorting — safe and unsafe fixes |
| `eslint` | `--fix` | Lint rule auto-fixes |
| `semgrep` | `--autofix` | Security and quality pattern fixes |

#### What agents MUST do

1. **Run `just test` (not individual checks).** The full stack with auto-fix is the only valid workflow. Do not run `ruff` or `biome` or `eslint` in isolation — the recipe handles all of them in the right order with the right flags.

2. **Never skip the auto-fix step.** If `just test` passes without changes, fine. If it applies fixes, those fixes are part of the intended output — they are not noise. Commit them.

3. **If a tool has an auto-fix flag that is not wired into the recipe, wire it in.** Do not apply it manually and leave the recipe stale. The justfile is the single source of truth. Add the flag and document it in this table.

4. **Never use bypass comments (`# noqa`, `@ts-ignore`, `# type: ignore`, etc.) as a substitute for letting auto-fix do its job.** The [No-Bypass Policy](#no-bypass-policy) is stricter than any individual tool's silence mechanism.

#### Why this rule exists

Without an explicit auto-fix requirement, agents routinely:
- Run checks without fixing, see failures, and reach for bypass comments instead of letting the tool fix itself
- Run `ruff check` without `--fix` (diagnostic only), then manually "fix" issues that `--fix` would have handled automatically
- Apply fixes manually to a subset of files while leaving the rest broken
- Skip auto-fix entirely and report "lint pass" when the actual fix step was never run

This is not a performance optimization. It is an epistemic integrity requirement: the state of the code after `just test` must be the state that was actually checked.

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

### Hard-Fail Doctrine: No Soft Skips

**Rule:** Every QC recipe MUST hard-fail (`exit 1`) when its prerequisites are absent.
There is no "Skipping: no X found; exit 0" path. QC failure is `exit 1` — always.

This covers all prerequisite types:

| Missing prerequisite | Example failure |
|---|---|
| No source files of the correct language | Python QC finds no `.py` files |
| No tests | `_pytest_with_coverage` finds no test files |
| No project config | `_deptry`/`_pytest_with_coverage` finds no `pyproject.toml` |
| No tool config | `_import-linter` finds no `.importlinter` or `[tool.import-linter]` |
| No tool installation | `_codeql` finds `codeql` CLI not on `PATH` |
| No coverage output | `_diff-cover` finds no `coverage.xml`/`lcov.info` from preceding step |

**Rationale:** QC is not optional, not best-effort, not advisory. If a prerequisite is
missing, the project is misconfigured — the correct response is a hard failure with a
clear error message telling the developer what to fix, not a silent green check.

#### Failure modes this policy exists to prevent

These are concrete misunderstandings that occurred during development and must not recur:

1. **"Missing source files are OK — the tool has nothing to scan, so skip silently."**
   Wrong. If the QC justfile for a language runs on a project and finds no source files
   of that language, that means either the project is using the wrong justfile (should
   map to a different language stack) or the project has no source code (not a real
   project). Both are configuration errors that must fail loudly.

2. **"Missing tool installations are OK — skip gracefully if the CLI is not on PATH."**
   Wrong. Every tool in the QC chain is mandatory. If CodeQL is not installed, QC must
   fail with an error telling the developer to install it. Silently skipping means the
   QC result is incomplete, which defeats the purpose of having a QC system.

3. **"Missing project config files are OK — skip the check that depends on them."**
   Wrong. If `pyproject.toml` is missing (or `tsconfig.json`, or `.importlinter`), the
   project is not properly configured. QC must fail, not amputate the check.

4. **"It's OK for a recipe to `exit 0` with a 'skipping' message."** Wrong. `exit 0` is
   a success signal. A check that did not run is not a success — it is a gap in the QC
   pipeline. The test runner and CI both interpret `exit 0` as "all good." Silent gaps
   produce false confidence.

**What a hard failure looks like:**

```
ERROR: vulture: no Python files found in a Python project.
```

Not:

```
Skipping vulture: no Python files found.
exit 0
```

The error message must name the tool, the missing prerequisite, and (when applicable)
the remediation (e.g., "Install CodeQL from https://github.com/github/codeql-cli").

### Language Isolation: One Language per Justfile

**Rule:** Each justfile owns exactly one language stack. No recipe in the Python justfile
may depend on JS/TS files existing. No recipe in the TS justfile may depend on Python
files existing.

| Justfile | Language | Validates presence of |
|---|---|---|
| `justfile` | Python | `.py` files, `pyproject.toml`, test files, Python tools on PATH |
| `justfile-bun` | TypeScript/JS | `.ts`/`.tsx`/`.js`/`.jsx`/`.mjs`/`.cjs` files, `tsconfig.json`, `package.json` |
| `justfile-sage` | SageMath | `.sage` files, `sage` binary |

#### Failure mode this policy exists to prevent

**"It doesn't matter which justfile a recipe lives in — recipes are just scripts."**
Wrong. A Python-justfile recipe that checks for `.ts` files will hard-fail on a pure
Python project (no `.ts` files exist), falsely indicating a QC failure. This is a
configuration error: the recipe belongs in the TS justfile, not the Python one.
Cross-contamination creates false negatives on correct projects and makes the QC
system impossible to reason about.

**Cross-contamination pattern (prohibited):**

```
# Python justfile — WRONG: contains JS/TS-specific recipes
_js-qc-files:          # does not belong here — hard-fails when no .ts files exist
_slop-scan:            # does not belong here — hard-fails on pure Python projects
```

**Correct separation:**

```
# Python justfile
test: _python-syntax _mypy _normalize ...   # Python tools only

# TS justfile
test: _normalize _knip _biome _slop-scan ...  # TS tools only
```

Running the wrong justfile for a project also fails — if Python QC runs on a project
with no Python files, every recipe that checks for `.py` files will exit 1. This is
correct: the developer is using the wrong justfile.

### No Optional Tools

#### Failure mode this policy exists to prevent

**"CodeQL is a security scanner — it's optional, not a core quality check."** Wrong.
Every tool in the global QC chain was deliberately included. Making any tool optional
creates a precedent for cherry-picking: "this project doesn't need deptry," "this
project doesn't need import-linter," "semgrep is overkill here." Over time, the full
stack degrades into whatever subset an agent subjectively decides is "appropriate."
The QC system is not negotiable per-project.

**Rule:** Every tool in the QC chain is mandatory. There is no "skip if not installed",
no `command -v tool || exit 0`, no graceful degradation.

| Tool | Behavior if missing | Before (wrong) | After (correct) |
|---|---|---|---|
| `codeql` | Hard fail | `exit 0` "Skipping CodeQL: CLI not installed" | `exit 1` "ERROR: Install CodeQL from ..." |
| `deptry` | Hard fail | `exit 0` "Skipping: no pyproject.toml" | `exit 1` "ERROR: no pyproject.toml found" |
| `import-linter` | Hard fail | `exit 0` "Skipping: no config" | `exit 1` "ERROR: no config found" |

If a tool cannot be installed or configured, QC is blocked until it is. This is by
design: QC must be complete to pass.

### Ephemeral Tools

#### Failure mode this policy exists to prevent

**"Tools need to be installed globally with `npm install -g` or `pip install` to be
available."** Wrong. Global installs pollute the system Python and node environments,
create version conflicts with project-local dependencies, and are invisible unless you
know to look. Every tool in the QC stack has a working ephemeral runner (`uvx`, `bun x`,
`npx -y`). If a tool cannot run ephemerally, it is the wrong tool — replace it, don't
install it globally.

**Rule:** All tools run via ephemeral runners (`uvx`, `bun x`, `npx -y`). No
permanent global or local installation of QC tools is permitted. See
`tool-provisioning-and-environment-hygiene` (rank 3 in the authority hierarchy).

| Correct | Incorrect |
|---|---|
| `uvx --from ruff ruff check --fix` | `pip install ruff && ruff check` |
| `bun x biome check` | `bun add --global @biomejs/biome && biome check` |
| `npx -y ast-grep scan` | `npm install -g @ast-grep/cli && ast-grep scan` |

**Sole exception:** ESLint flat config requires its plugins to be locally installed in
`~/ai/quality-control/node_modules/` because the flat config uses ES module imports
that resolve relative to the config file's directory. This exception is documented at
the recipe site in `_eslint-deps`. No other tool may use this exception.

### Bridge-Burning Policies

Adhering to the [Bridge-Burning Policies](file:///home/dzack/ai/opencode/skills/anti-slop/SKILL.md#bridge-burning-policies) is a non-negotiable constraint for all development. These rules eliminate common agent validation-evasion pathways (such as runtime defaults, fallbacks, mocks, and diagnostic smoke tests in proof paths). 

Any exception to these rules must strictly follow the **Policy Exception Protocol** defined in [anti-slop/SKILL.md](file:///home/dzack/ai/opencode/skills/anti-slop/SKILL.md#policy-exception-protocol).

> [!IMPORTANT]
> **Bridge-Burning Red Flags:** If a construct would let an agent preserve the appearance of correctness while weakening the obligation, treat it as a red flag even if the code currently works. For a comprehensive catalog of code signatures, keywords, and patterns to look for, see the [Bridge-Burning Red Flags Reference Catalog](file:///home/dzack/ai/opencode/skills/reviewing-llm-code/references/bridge-burning-red-flags.md) and the [Runtime Control-Flow Red Flags Catalog](file:///home/dzack/ai/opencode/skills/reviewing-llm-code/references/runtime-control-flow-red-flags.md).



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

## Assertion Policy vs QC Policy

Project tests must not enforce generic policy by inspecting code shape or asserting absence of banned constructs.

Global QC owns policy policing:
- mocks/fakes/stubs;
- type ignores and `as any`;
- runtime defaults/fallbacks;
- skip/xfail;
- source suppression;
- local QC surfaces;
- stderr suppression;
- exact-string assertion patterns where mechanically detectable.

Project tests own behavior proof:
- real boundary exercised;
- semantic output asserted;
- side effects verified;
- structured errors checked;
- independent oracles used.

Do not scatter policy-policing tests into projects. For the catalog of assertion constraints, see the central [Banned Test Shapes Catalog](file:///home/dzack/ai/opencode/skills/test-guidelines/references/banned-test-shapes.md).

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
