---
order: 10
title: Chat Responses After Completing Work
---

Never summarize what was done.
The git commit message is the summary — refer the user to it if they want a record.
When finishing a task, review the entire chat history, identify the most recent user directive/task request as well as the overall task, and if that communicated requirement has not been met, continue.

**Your chat output should contain only the following, when applicable:**

- Gaps or questions identified during the most recent task.

- Errors or surprises that were skipped and need revisiting

- Nontrivial decisions made that have not been documented or explicitly discussed with a user

- Items NOT completed from the overall task, due to branching, tangents, goal substitution or relaxation, or divergence of work with literal content of user’s requests.

- Next actions, if any

**Chat output should never contain:**

- Changelogs (should be in git history)

- Summaries (unless explicitly requested)

- Implications of completion or finalization when there are open tasks in the chat history.

- Speculation not tied to specific evidence or investigations

Touch only the files you intended to change; verify with `git diff` before responding.
