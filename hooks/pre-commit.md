# Commit checkpoint directive

Read this at every commit.

Remove all code comments from each changed file before committing. Keep design rationale in the specification.

- Autoformatter output is canonical. Re-stage and commit formatter rewrites.
- Commit everything this session produced. No undecided untracked files.
- A checkpoint may be red when it marks a step toward a fix.
- A deliberately failing red proof goes through `ai-review-ci red-commit --issue <issue> -m "<message>"` rather than `--no-verify`.
- A commit or push that changes only documentation (Markdown, Spec Kit files under `.specify/` and `.claude/skills/`) uses `--no-verify` when the repository's hook would run a build or a test suite. A change to code, configuration, lockfiles or CI keeps the hooks.
- The commit message body carries the reasoning: what changed and why, what was ruled out, what evidence settled it.
