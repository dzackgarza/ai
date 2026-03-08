---
name: justfile
description: Use when working with just command runner, defining recipes, or managing project automation tasks
---

# Justfile

## Multi-Line Constructs

**Problem:** Recipes without shebang are parsed line-by-line. Extra leading whitespace causes parse errors.

**Solution:** Use shebang for multi-line constructs.

```just
# ❌ Fails - extra whitespace
conditional:
  if true; then
    echo 'True!'
  fi

# ✅ Works - shebang
conditional:
  #!/usr/bin/env sh
  if true; then
    echo 'True!'
  fi
```

**Alternatives:**

```just
# Single line
if true; then echo 'True!'; fi

# Backslash continuation
if true; then \
  echo 'True!'; \
fi
```

**Applies to:** if/for/while statements, any multi-line shell logic

## Setting Variables in Recipes

**Problem:** Recipe lines run in separate shell instances. Shell variables don't persist between lines.

```just
# ❌ Doesn't work - can't set just variables in recipe
foo:
  x := "hello"
  echo {{x}}

# ❌ Doesn't work - new shell each line
foo:
  y=bye
  echo $y

# ✅ Works - single shell instance with shebang
foo:
  #!/usr/bin/env bash
  set -euxo pipefail
  x=hello
  echo $x

# ✅ Works - chain with &&
foo:
  x=hello && echo $x
```

**Rule:** Use shebang recipes for shell variables that span multiple lines.
