---
description: Introduce yourself to a repo - tree, markdown files, and README
---

You are being introduced to a new repository. Here is an orientation:

**Directory structure (2 levels, gitignore-aware):**
!`tree -L 2 --gitignore`

**Markdown files:**
!`git ls-files '*.md' '*.mdx' 2>/dev/null || find . \( -name '*.md' -o -name '*.mdx' \) -not -path './.git/*'`

**README:**
!`[ -f README.md ] && cat README.md || echo "(no README.md in project root)"`

Based on the above, introduce yourself to this repository: summarize what it is, its structure, and any key entry points or documentation found.
