# Commit checkpoint directive

Read this at every commit.

Remove all code comments from each changed file before committing. Keep design rationale in the specification.

- Autoformatter output is canonical. Re-stage and commit formatter rewrites.
- Commit everything this session produced. No undecided untracked files.
- A checkpoint may be red when it marks a step toward a fix.
- A deliberately failing red proof goes through `ai-review-ci red-commit --issue <issue> -m "<message>"` rather than `--no-verify`.
- The commit message body carries the reasoning: what changed and why, what was ruled out, what evidence settled it.
