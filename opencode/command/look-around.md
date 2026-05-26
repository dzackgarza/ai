---
description: Orient to the current repository before acting
---
The user’s directive is to look around the current repository before narrowing or
editing. Start broad, then report the project shape and the next targeted reads.

Run only lightweight orientation commands.
Prefer:

```bash
pwd
tree -a -L 3 -I '.git|node_modules|__pycache__|*.pyc|.venv|dist|build'
git status --short
test -f AGENTS.md && sed -n '1,220p' AGENTS.md
test -f README.md && sed -n '1,220p' README.md
test -f justfile && just --list
```

Then print:

- repository purpose inferred from docs,

- important subtrees,

- current git state relevant to safe edits,

- canonical commands or recipes found,

- targeted files to read next.

Do not run dependency installs, test suites, servers, or cleanup commands from this
command.
