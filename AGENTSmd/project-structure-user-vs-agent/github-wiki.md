---
order: 8
title: GitHub Wiki
---

When exploring a GitHub-backed repository, check whether the repository has a wiki before
treating repo-local docs as the complete durable context.
Determine the GitHub `<owner>/<repo>` from the remote, then check both the repository
setting and the initialized wiki repo:

```bash
gh repo view <owner>/<repo> --json hasWikiEnabled --jq '.hasWikiEnabled'
git ls-remote git@github.com:<owner>/<repo>.wiki.git HEAD
```

`hasWikiEnabled=true` means the wiki feature is enabled.
A successful `.wiki.git` ref check means wiki pages exist.
`Repository not found` from the `.wiki.git` probe usually means the wiki has not been
initialized with a page; it is not a surprising infrastructure failure.

Use the wiki for durable, long-horizon project knowledge: philosophy, requirements,
architectural decisions, feature doctrine, roadmaps, and design rationale that should
outlive a branch or session.
Do not use the wiki as a scratchpad, transcript, session log, task checklist, or live
implementation plan.

Plans belong in `agent-memory` plan records when the state must survive context windows
inside the project.
When a plan needs a public GitHub execution surface, load `git-guidelines` and use the
GitHub issue/PR workflow guidance to turn it into milestones, issues, sub-issues, and
draft PRs.
Wiki pages may link to those canonical planning artifacts, but they do not replace them.
