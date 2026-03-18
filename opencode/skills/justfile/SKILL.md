---
name: justfile
description: Use when working with just command runner, defining recipes, or managing project automation tasks
---

# Justfile

## What justfiles are — and are not

`just` is a **command runner**, not a build system. A justfile is the single canonical place for all repo-specific automation: build steps, test runners, install procedures, code generation, deployment, environment setup. The goal is **one place to look, one command to run** — no scattered shell scripts, no ad-hoc one-liners in CI configs, no "how do I run the tests again?" questions.

**Justfiles are not Makefiles.** Critical differences:

- No dependency tracking, no file targets, no implicit rules
- No tab-indentation requirement (uses any consistent indentation)
- Recipes are not shell scripts run in a single process unless you add a shebang — without one, each line is a separate shell invocation
- Variables use `{{ }}` syntax, not `$( )` or `$(VAR)`
- `just` parses the entire recipe body before execution — this matters for embedded code (see below)

**The anti-pattern to avoid:** creating `scripts/do-thing.sh`, `scripts/setup.py`, `scripts/update-config.js` etc. alongside a justfile. Recipes can directly contain any language via shebangs. Scripts proliferate when this isn't known; they fragment automation, lose discoverability, and accumulate without ownership.

---

## Core rule: just parses recipe bodies before execution

`just` parses ALL recipe content for its own syntax (variables like `{{ foo }}`, expressions, etc.) **before** handing anything to a shell. This means:

- Python code like `Path.home()` or `obj.attr` will cause a parse error — `just` sees `.` as a token
- Heredocs inside non-shebang recipes are NOT a solution: just still parses the heredoc content
- **The correct solution for any multi-line or embedded-language code is a shebang recipe**

When just sees `#!/usr/bin/env X` as the first line of a recipe body, it writes the entire body to a temp file and executes it with interpreter `X`. The body is NOT parsed for just syntax first.

---

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

**Key property:** When the recipe body starts with `#!`, just writes the entire body verbatim to a temp file and executes it. No just-syntax parsing occurs on the body. This means any language, any syntax, including constructs that would otherwise conflict with just's parser.

---

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

---

## Multi-line constructs require shebangs

Without a shebang, each recipe line is a separate shell invocation — variables don't persist, control flow doesn't work:

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

---

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

`{{justfile_directory()}}` — directory containing the justfile (stable, use instead of `$PWD`)
`{{justfile()}}` — absolute path to the justfile itself

---

## @ prefix — silence echo

By default just prints each command before running it. `@` suppresses this:

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

**Note:** `@` has no meaning inside shebang recipes — the whole body is a script, echoing is the shell's concern.

---

## Sharing state between recipes

Each recipe runs in a fresh environment. To share state:

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

---

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

---

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

---

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
