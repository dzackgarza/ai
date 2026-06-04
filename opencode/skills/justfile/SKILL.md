---
name: justfile
description: Use when working with just command runner, defining recipes, or managing project automation tasks
---

# Justfile

## Interface Design — What Belongs in a Justfile

### The universal convention: all workflows through just

`just` is the project-management API for every repository on this system. A user should be
able to clone any project, run `just`, and see the same set of familiar recipes —
regardless of language, framework, or build tooling. `just run` always starts the app.
`just test` always runs the test suite. `just build` always produces the artifact.

There are no exceptions. A Rust project does not route `cargo run` directly as the user
interface. A Node project does not expose `npm run dev` as the canonical entry point.
These are underlying implementations. The user never needs to know them. They run `just
run`. The justfile calls `cargo` or `npm` internally.

Routing workflows directly through language-specific build tools — `cargo run`, `npm run
build`, `python -m pytest`, `make` — spreads sources of truth across disparate tooling and
forces the user to do archaeology before interacting with the project. The justfile
centralizes the project interface into one place, one command.

### The recipe list is the project's architecture

Every recipe in `just --list` communicates to every future reader: **"this is a distinct, independently useful operation."** If a recipe is not independently useful, exposing it is architectural debt — it pollutes the surface, signals wrong ownership, and normalizes accretion by one-shot prompts.

A recipe should be public only if:

- A human would independently run it (`just build`, `just test`, `just deploy`)
- It is a necessary composition of private steps that must be documented (e.g., `just release` which builds, tags, publishes)
- It is genuinely user-facing for the project's audience (e.g., `just serve` for a static site owner)

A recipe should **not** be public if:

- It is only called as a dependency of another recipe (make it `[private]`)
- It exists because one-shot agents stacked it onto the file without removing or refactoring the recipe it duplicates
- It does one thing that is a sub-step of a well-known operation (e.g., `assemble` when `build` exists, `sync` when `deploy` exists)
- It is a one-time setup step presented as a permanent recipe (`setup-hooks`, `init-config` — these belong in documentation, not in `--list`)
- It wraps a single CLI command with no composition, configuration, or cross-platform abstraction — the CLI command itself is the interface

### Public vs private discipline

Use the `[private]` attribute for any recipe that is an implementation detail:

```just
[private]
_generate-manifest:
    node scripts/generate-manifest.cjs

[private]
_assemble-assets:
    rsync -a dist/ {{output_dir}}/assets/

build: _generate-manifest _assemble-assets
    @echo "Built to {{output_dir}}"
```

The rule of thumb: **if a recipe name has to be explained to understand when to run it, it probably shouldn't be public.** `just build` is self-explanatory.
`just assemble`, `just sync`, `just check-hygiene`, `just generate-macros` all require the reader to understand the pipeline's internals — they are internal steps masquerading as entry points.

### The fossil record problem

Agents asked "add a `build` recipe" add `build`. Agents asked "add a way to sync to a server" add `sync`. Agents asked "add a hygiene checker" add `check-hygiene`. Each request produces a new recipe.
No agent ever asks "does this conflict with the existing surface?"
or "should this be folded into an existing recipe?"

The result is a justfile whose public surface is the complete history of one-shot prompts rather than a designed interface.
The fix is not to avoid adding recipes — it's to **stop and read the existing surface** before adding another one.
If the new behavior is a sub-step of an existing recipe, it should be `[private]` or inlined.

### Single `test` recipe, always

There should be exactly **one** public test recipe.
All sub-tasks — unit tests, integration tests, visual regression, snapshot generation, linting, type-checking, hygiene checks — are `[private]` recipes that `test` composes.

```just
[private]
_typecheck:
    npx tsc --noEmit

[private]
_unit:
    npx vitest --run

[private]
_integration:
    npx playwright test

[private]
_snapshots:
    npx playwright test --update-snapshots

test: _typecheck _unit _integration _snapshots
    @echo "All gates passed"
```

Never expose `test-unit`, `test-integration`, `test-visual-regression`, `update-snapshots`, `check-hygiene`, or any other test sub-step as a public recipe.
If a developer needs to run a subset locally, they run the CLI tool directly (`npx vitest --run tests/unit`) — the justfile is not a test-discovery interface.

The requirement to produce a full-site snapshot gallery on every test run is not a separate recipe — it's a `[private]` dependency of `test`. Snapshot updates are part of the test gate; they are not a distinct user-facing operation.
If snapshots must be rebaselined, that's `npx playwright test --update-snapshots` at the CLI, not `just update-snapshots`.

**CI uses the same `test` recipe.** CI never gets its own recipe.
If CI needs different behavior, the CI config passes arguments to `just test` or sets environment variables.
A separate `test-ci` or `test-staging` recipe is always a sign that the developer and CI gates have diverged — which means CI verifies something different from what developers run, which means CI failures are surprises.

### One entry point per concern

Beyond `test`, a project might expose one or two other entry points:

```
just build     # compile + assemble (configurable output)
just test      # full QC gate (typecheck, unit, integration, snapshots)
just serve     # dev preview server
```

Everything else — `assemble`, `sync`, `check-hygiene`, `generate-macros`, `preview`, `preview-open`, `test-release`, `test-staging`, `update-snapshots` — is an internal step of one of these three, or belongs in a CLI.

### Progressive disclosure via CLI, not recipe proliferation

When a project has many granular operations, the justfile should expose a thin layer over a proper CLI tool, not expose each operation as a recipe:

```just
# Thin justfile over a CLI
default:
    @opx --help

build:
    @opx build

test:
    @opx test

serve:
    @opx serve
```

The CLI (`opx` or `npx <project>` or `uvx <project>`) owns the granular subcommands: `opx assemble`, `opx sync`, `opx check-hygiene`, `opx preview`, `opx preview-open`, `opx generate-macros`, `opx list-posts`. These are discoverable through `--help` and grouped by concern.
They don't pollute `just --list` because they are not the project's entry points.

This follows the `writing-scripts-and-cli-interfaces` skill: a CLI provides progressive disclosure, named subcommands, typed arguments, and help text.
A justfile provides compositions of those subcommands with project-local defaults.
The justfile is the **surface**; the CLI is the **depth**.

### Audience awareness

Group recipes by who runs them:

- **User** (runs the project's output): `build`, `serve`
- **Developer** (works on the project): `test`, `setup`, `clean`
- **CI** (automated pipelines): the same `test` recipe — CI should never have its own recipe that duplicates or narrows the developer's test path

Recipes that don't fit one of these three categories are suspect.
`update-snapshots` and `test-staging` are operations that should happen automatically (as part of the test gate) or on demand via a CLI subcommand, not as distinct recipes a user must know about.

### Agent-facing recipes (`.agents/justfile`)

Projects also need recipes that serve agents, not users or developers: QC guardrails, hygiene checks, debugging surfaces, anti-gaming measures, and hook scripts. These must never appear in `just --list` or the top-level justfile.

- Agent-facing recipes live in `.agents/justfile`, a separate file at the project root.
- **All agent-facing recipes are `[private]`**, invisible to `just --list`.
- The top-level `justfile` routes through agent recipes where mandatory enforcement is needed:
  ```justfile
  test:
      @project-cli test
      @just -f .agents/justfile _test-agent
  ```
- `.agents/justfile` recipes cover: hygiene checks (dead code, duplication, complexity, slop), anti-gaming measures, debug surfaces (isolated reproducers, artifact dumps, fixture runners), and hook scripts (pre-commit, pre-push).

This is documented in the `Project Structure: User vs. Agent` section of `AGENTS.md`.

Every just recipe that runs a diagnostic, build, or test command should preserve stdout, stderr, and exit code. If a recipe requires suppressing output (e.g. `>/dev/null` on pip install), make the suppression explicit and document what diagnostic channel is being dropped and why. Recipes that silence their own failures prevent agents from discovering missing debugging surfaces. See `reality-grounded-debugging` for command-output discipline and surface-upgrade requirements.

### Large justfiles are a smell

A justfile that grows beyond ~30 lines of recipe bodies is usually reinventing something that already exists:

- Reusable QC recipes (type-checking, linting, test-running, coverage) are in `~/ai/quality-control/`. Import them instead of rewriting them.
  See the `quality-control` skill.
- Repo-specific build logic belongs in the build tool's config (`vite.config.ts`, `pyproject.toml`, `Cargo.toml`), not in a justfile recipe.
- Granular utility subcommands belong in a proper CLI tool (see **Progressive disclosure via CLI** above), not as recipes.

A justfile that has recipes for type-checking, linting, individual test suites, code generation, asset compilation, snapshot management, and deployment — all with 5-10 line bodies — is a justfile that should be replaced by a thin wrapper over a CLI and global QC imports.
The justfile's job is **composition and defaults**, not implementation.

### Recipe naming as API design

- Verbs, not nouns: `build`, not `builder` or `build-process`
- Consistent tense: `build`, `test`, `deploy`, `serve` — imperative, present tense
- If a name requires a hyphen to be clear (`check-hygiene`, `generate-macros`, `test-release`), it is describing an implementation detail, not a user-facing operation.
  The user doesn't care about hygiene or macros or release variants — they care about `test`.

* * *

## What justfiles are — and are not

`just` is a **command runner**, not a build system.
A justfile is the single canonical place for all repo-specific automation: build steps, test runners, install procedures, code generation, deployment, environment setup.
The goal is **one place to look, one command to run** — no scattered shell scripts, no ad-hoc one-liners in CI configs, no “how do I run the tests again?”
questions.

**Justfiles are not Makefiles.** Critical differences:

- No dependency tracking, no file targets, no implicit rules

- No tab-indentation requirement (uses any consistent indentation)

- Recipes are not shell scripts run in a single process unless you add a shebang — without one, each line is a separate shell invocation

- Variables use `{{ }}` syntax, not `$( )` or `$(VAR)`

- `just` parses the entire recipe body before execution — this matters for embedded code (see below)

**The anti-pattern to avoid:** creating `scripts/do-thing.sh`, `scripts/setup.py`, `scripts/update-config.js` etc.
alongside a justfile.
Recipes can directly contain any language via shebangs.
Scripts proliferate when this isn’t known; they fragment automation, lose discoverability, and accumulate without ownership.

* * *

## Core rule: just parses recipe bodies before execution

`just` parses ALL recipe content for its own syntax (variables like `{{ foo }}`, expressions, etc.)
**before** handing anything to a shell.
This means:

- Python code like `Path.home()` or `obj.attr` will cause a parse error — `just` sees `.` as a token

- Heredocs inside non-shebang recipes are NOT a solution: just still parses the heredoc content

- **The correct solution for any multi-line or embedded-language code is a shebang recipe**

When just sees `#!/usr/bin/env X` as the first line of a recipe body, it writes the entire body to a temp file and executes it with interpreter `X`. The body is NOT parsed for just syntax first.

* * *

## Shebang recipes — the primary tool for non-trivial logic

```just
# Bash with strict mode
deploy:
  #!/usr/bin/env bash
  set -euxo pipefail
  echo "Deploying..."

# Python — recipe body IS Python, no heredoc, no subprocess
analyze:
  #!/usr/bin/env python3
  import sys
  from pathlib import Path
  print(f"Python {sys.version}")
  print(Path.home())  # ✅ works fine — just doesn't parse shebang recipe bodies

# Node
gen-config:
  #!/usr/bin/env node
  const fs = require('fs')
  fs.writeFileSync('config.json', JSON.stringify({version: 1}))
```

**Key property:** When the recipe body starts with `#!`, just writes the entire body verbatim to a temp file and executes it.
No just-syntax parsing occurs on the body.
This means any language, any syntax, including constructs that would otherwise conflict with just’s parser.

* * *

## Internal recipes — replacing external scripts

When a recipe needs both shell commands AND another language, **split into internal recipes** rather than reaching for a subprocess or external script file:

```just
# ✅ Correct: separate recipes, one calls the other
install:
  #!/usr/bin/env bash
  set -euo pipefail
  mkdir -p ~/.config/myapp
  ln -sf {{justfile_directory()}}/config ~/.config/myapp/config
  just _write-rc-vars   # call internal recipe

# Prefixing with _ is convention for internal/private recipes
_write-rc-vars:
  #!/usr/bin/env python3
  from pathlib import Path
  rc = Path.home() / '.bashrc'
  text = rc.read_text()
  if 'MY_APP_HOME' not in text:
      rc.write_text(text + '\nexport MY_APP_HOME=' + str(Path.home() / '.config/myapp') + '\n')
```

**Call pattern:** `just _recipe-name` or `just --justfile {{justfile()}} _recipe-name` when calling from within a shebang recipe (the `just` binary is on PATH).

Internal recipes:

- Are listed in `just --list` unless you use `[private]`

- Can be any language

- Are version-controlled alongside the justfile

- Replace the need for `scripts/` directories entirely

```just
# Hide from --list with [private]
[private]
_setup-db:
  #!/usr/bin/env python3
  import sqlite3
  # ...
```

* * *

## Multi-line constructs require shebangs

Without a shebang, each recipe line is a separate shell invocation — variables don’t persist, control flow doesn’t work:

```just
# ❌ Fails — 'fi' runs in a different shell from 'if'
conditional:
  if true; then
    echo 'True!'
  fi

# ✅ Works — shebang makes the whole body a single script
conditional:
  #!/usr/bin/env bash
  if true; then
    echo 'True!'
  fi
```

* * *

## Variables and parameters

```just
# Top-level variable
version := "1.0.0"

# With fallback from environment
repo := env_var_or_default("REPO", env_var("HOME") / "myproject")

# Recipe parameter with default
build target="debug":
  cargo build --{{target}}

# Variadic parameter
test *args:
  pytest {{args}}
```

`{{justfile_directory()}}` — directory containing the justfile (stable, use instead of `$PWD`) `{{justfile()}}` — absolute path to the justfile itself

* * *

## @ prefix — silence echo

By default just prints each command before running it.
`@` suppresses this:

```just
# Prints the command, then runs it
build:
  cargo build

# Silent — only output is the command's stdout/stderr
@build:
  cargo build

# Per-line silence in non-shebang recipes
setup:
  @echo "Setting up..."
  mkdir -p dist
```

**Note:** `@` has no meaning inside shebang recipes — the whole body is a script, echoing is the shell’s concern.

* * *

## Sharing state between recipes

Each recipe runs in a fresh environment.
To share state:

```just
# ✅ Use just variables (evaluated at parse time)
config_dir := env_var("HOME") / ".config/myapp"

install:
  mkdir -p {{config_dir}}

clean:
  rm -rf {{config_dir}}

# ✅ Use dependency recipes + direct binary paths
venv:
  [ -d .venv ] || python3 -m venv .venv

run: venv
  .venv/bin/python3 main.py
```

* * *

## Groups

```just
[group('test')]
test-unit:
  pytest tests/unit

[group('test')]
test-integration:
  pytest tests/integration

[group('build')]
build:
  cargo build
```

```bash
just --list       # grouped display
just --groups     # show group names only
```

* * *

## Python recipes with uv

`[script]` was stabilized in just 1.38.0. `set unstable` is no longer required.

```just
set script-interpreter := ['uv', 'run', '--script']

[script]
analyze:
  # /// script
  # requires-python = ">=3.11"
  # dependencies = ["requests"]
  # ///
  import requests
  print(requests.get("https://example.com").status_code)
```

This differs from a plain `#!/usr/bin/env python3` shebang recipe: `[script]` passes the recipe body through `uv run --script`, which reads the inline PEP 723 dependency block and installs deps into an isolated environment automatically.

* * *

## Common patterns

```just
# Default recipe shows help
default:
  @just --list

# Require a variable to be set
deploy:
  #!/usr/bin/env bash
  : ${DEPLOY_TARGET:?DEPLOY_TARGET must be set}
  echo "Deploying to $DEPLOY_TARGET"

# Confirm before destructive action
drop-db:
  #!/usr/bin/env bash
  read -p "Drop database? [y/N] " confirm
  [[ "$confirm" == "y" ]] || exit 1
  psql -c "DROP DATABASE myapp"
```
