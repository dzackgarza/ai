---
name: plan
description: "Plan mode: write markdown plan to .hermes/plans/, no exec."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [planning, plan-mode, implementation, workflow]
    related_skills: [writing-plans, subagent-driven-development]
---

# Plan Mode

Use this skill when the user wants a plan instead of execution.

## Core behavior

For this turn, you are planning only.

- Do not implement code.

- Do not edit project files except the plan markdown file.

- For repository implementation plans, branch and draft-PR setup are part of recording the plan, not implementation.
  You may create the dedicated branch, commit the plan artifact, push the branch, and open or update the draft PR. Do not change source, tests, docs unrelated to the plan, or implementation files.

- You may inspect the repo or other context with read-only commands/tools when needed.

- Your deliverable is a markdown plan saved inside the active workspace under `.hermes/plans/`.

- For repository implementation plans, the draft PR body is the canonical tracker and must contain the same nested task tree before implementation starts.

## Output requirements

Write a markdown plan that is concrete and actionable.

Include, when relevant:

- Goal

- Current context / assumptions

- Proposed approach

- Step-by-step plan

- Files likely to change

- Tests / validation

- Risks, tradeoffs, and open questions

If the task is code-related, include exact file paths, likely test targets, and verification steps.

For repository implementation work, also include:

- Dedicated branch name
- Draft PR URL
- Whether the plan's task tree has been copied to the PR body
- A blocking preflight item if branch or PR creation could not be completed

Use one nested task tree:

```md
- [ ] <Milestone or goal>
  - [ ] <Workstream or phase>
    - [ ] <Task>
      - [ ] <Subtask or proof obligation>
```

Do not split checkboxes into "completed," "outstanding," "bookkeeping," or provenance sections.
Checked means complete, and every checked line must include same-line proof such as `Proof commit: <sha>`. Blocked work stays unchecked with `Blocked: <reason>`.

## Save location

Save the plan with `write_file` under:

- `.hermes/plans/YYYY-MM-DD_HHMMSS-<slug>.md`

Treat that as relative to the active working directory / backend workspace.
Hermes file tools are backend-aware, so using this relative path keeps the plan with the workspace on local, docker, ssh, modal, and daytona backends.

If the runtime provides a specific target path, use that exact path.
If not, create a sensible timestamped filename yourself under `.hermes/plans/`.

For repository implementation plans, commit the plan file on the dedicated branch and pre-record the plan tree in the draft PR body.
If the environment prevents branch or PR creation, the saved plan must start with a blocking preflight section and must say implementation cannot start until the branch is pushed and the draft PR contains the task tree.

## Interaction style

- If the request is clear enough, write the plan directly.

- If no explicit instruction accompanies `/plan`, infer the task from the current conversation context.

- If it is genuinely underspecified, ask a brief clarifying question instead of guessing.

- After saving the plan, reply briefly with what you planned and the saved path.
