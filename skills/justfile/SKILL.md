---
name: justfile
description: Use when working with just command runner, defining recipes, or managing project automation tasks
---

# Justfile

## Shebang Recipes

**What:** Recipes starting with `#!` are saved to a temp file and executed as scripts.

```just
# Bash with strict mode
deploy:
  #!/usr/bin/env bash
  set -euxo pipefail
  echo "Deploying..."

# Python
analyze:
  #!/usr/bin/env python3
  import sys
  print(f"Python {sys.version}")

# Split shebang arguments
debug:
  #!/usr/bin/env -S bash -x
  ls
```

## Multi-Line Constructs

**Problem:** Non-shebang recipes parsed line-by-line.

```just
# ❌ Fails - extra whitespace
conditional:
  if true; then
    echo 'True!'
  fi

# ✅ Works - use shebang
conditional:
  #!/usr/bin/env sh
  if true; then
    echo 'True!'
  fi
```

## Setting Variables in Recipes

**Problem:** Each recipe line runs in a new shell instance.

```just
# ✅ Shebang = single shell instance
foo:
  #!/usr/bin/env bash
  x=hello
  echo $x
```

## Sharing Environment Variables Between Recipes

**Problem:** Each recipe runs in a fresh shell.

**Solution:** Call binaries directly:

```just
venv:
  [ -d .venv ] || python3 -m venv .venv

run: venv
  .venv/bin/python3 main.py
```

## Command Evaluation (Backticks)

**Use:** Capture command output into variables.

```just
# Simple backtick
localhost := `dumpinterfaces | cut -d: -f2`

# Indented multi-line
stuff := ```
    echo foo
    echo bar
  ```
```

## Constants

**Built-in values:**

| Constant | Value | Use |
|----------|-------|-----|
| `PATH_SEP` | `/` or `\` | Path separator |
| `PATH_VAR_SEP` | `:` or `;` | PATH delimiter |
| `HEXLOWER` | `0123456789abcdef` | Hex digits |
| `HEXUPPER` | `0123456789ABCDEF` | Hex digits |

**ANSI escape sequences (quote them):**

```just
# Colors
RED, GREEN, BLUE, CYAN, MAGENTA, YELLOW, BLACK, WHITE
BG_RED, BG_GREEN, etc.

# Styles
BOLD, ITALIC, UNDERLINE, STRIKETHROUGH, INVERT, HIDE

# Reset
NORMAL  # Always reset after styling
CLEAR   # Clear screen
```

**Example:**

```just
@info:
  echo '{{GREEN}}✓{{NORMAL}} Build complete'

@error:
  echo '{{RED}}{{BOLD}}Error:{{NORMAL}} Something failed'
```

## Groups

**Organize recipes for `--list`:**

```just
[group('lint')]
js-lint:
  echo 'Linting...'

[group('lint')]
[group('rust')]
rust-lint:
  echo 'Linting Rust...'
```

```bash
just --list       # Grouped display
just --groups     # Show group names
```

## Python Recipes with uv

```just
set unstable
set script-interpreter := ['uv', 'run', '--script']

[script]
hello:
  print("Hello!")
```
