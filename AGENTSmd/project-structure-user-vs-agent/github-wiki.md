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
Every GitHub-backed project should have a wiki.
If the wiki feature is disabled, ask the user or repository owner to enable it.
If the wiki is enabled but `.wiki.git` does not exist yet, tell the user that GitHub may
require them to click into the Wiki tab and create the first page before agents can
clone or update it.

Use the wiki for durable, long-horizon project knowledge: philosophy, requirements,
architectural decisions, feature doctrine, roadmaps, feature lists, user stories, and
design rationale that should outlive a branch or session.
Do not use the wiki as a scratchpad, transcript, session log, task checklist, or live
implementation plan.

A repo wiki should be user-story-first.
Its primary project-management content is an extensive, explicit set of user stories:
who the user is, what they are trying to accomplish, what workflow they perform, what
state they observe, and what outcome proves the story is satisfied.
Do not invent thin stories from implementation details.
When stories are missing, vague, or conflicting, prompt the user for the product and
workflow facts needed to write them.

Proof burdens belong in the wiki when they describe durable obligations, especially
user-observable and end-to-end behavior.
Ground proof burdens in user stories and real workflows before translating them into
tests, CI gates, or manual verification procedures.
A proof burden should name the story it protects, the boundary it must exercise, the
observable evidence required, and the current implementation or test artifact when one
exists.

Roadmaps and feature lists also belong in the wiki, but they should not flatten the
project into status rows.
Roadmaps should link features to user stories, proof burdens, decisions, issues,
milestones, and draft PRs.
Feature pages should describe the user-facing contract, ownership boundary, expected
proof, and related work rather than only listing implementation tasks.

Organize the wiki as a cross-referenced project knowledge graph, not a flat list of
files.
Maintain a Home page or map page that links the main story, feature, roadmap, proof,
and decision pages.
Use stable page names, backlinks, and local indexes so an agent can start from any one
page and find the related user stories, feature contracts, proof burdens, and execution
artifacts.

Plans belong in `agent-memory` plan records when the state must survive context windows
inside the project.
When a plan needs a public GitHub execution surface, load `git-guidelines` and use the
GitHub issue/PR workflow guidance to turn it into milestones, issues, sub-issues, and
draft PRs.
Wiki pages may link to those canonical planning artifacts, but they do not replace them.
