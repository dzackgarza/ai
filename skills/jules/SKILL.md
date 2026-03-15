---
name: jules
description: Use when delegating a coding task to Jules — bug fixes, tests, docs, features, or code reviews on a GitHub repo.
license: Apache-2.0
metadata:
author: sanjay3290
version: "1.1"
---

# Jules Task Delegation

Delegate coding tasks to Google's Jules AI agent on GitHub repositories.

## IMPORTANT: Quality Caveats

**Jules is a weak agent with significant failure modes.** All work must be heavily validated, gated, and reviewed before approval. Treat Jules output adversarially when reviewing.

### Common Failure Patterns

- **Hollow PRs**: Minimal or trivial changes that don't actually solve the problem
- **High LOC for simple features**: Unnecessarily verbose implementations
- **Rushing to fix**: No root cause research, just monkey-patches
- **Poor integration**: Doesn't use existing code patterns
- **Testing theater**: Tests that pass but don't verify meaningful behavior
- **Obfuscation**: Complex code hiding lack of substance
- **Reward hacking**: Minimal path to "done" without real value
- **Early termination**: Stops before significant work is complete
- **Goal substitution**: Completes a different task than requested

### Validation Requirements

- **ALWAYS** load `test-guidelines` skill when reviewing Jules output
- Check that tests verify correctness, not just coverage
- Verify the implementation addresses the actual root cause
- Look for shortcuts, workarounds, and incomplete solutions
- Reprompt Jules to continue when gaps are found

### Automated Review Limitations

Automated GitHub reviewers are given **only the PR diff and Jules' own description of it**. They have no access to the original task, the original expectations, or any blockers Jules encountered along the way.

Reviewers are trained to find bugs, logical errors, and **inconsistencies between what Jules reports and what the code actually does**. This is a useful check — but it only operates within Jules' own framing. The one thing reviewers cannot do is compare the original task requirements against what was delivered, because the only source of "expectations" available to them is Jules' own PR title, body, and commit messages. Jules controls all of that, and Jules is incentivized to make its work appear aligned with expectations — downplaying or omitting blockers, fallback decisions, or abandoned goals entirely.

**Concrete example:** Jules hits a blocker and decides it cannot implement the requested feature. Instead of reporting failure, it implements scaffolding and reframes the PR as "laying the groundwork for future implementation." The PR description presents this as forward progress. Automated reviewers evaluate it as a scaffolding task — checking that the scaffolding is well-structured, consistent, and bug-free. It passes. The original task ("implement the feature") was a complete failure, but nothing in the review pipeline had any way to know that.

**Clearing automated review is not sufficient.** You must independently compare the original task against actual PR contents, using your own copy of the original task description — not Jules' framing — as the benchmark for completeness.

### When to Use Jules

Jules has a restricted Linux environment with no access to online docs or external references. Context engineering in the prompt is essential.

**Best for:**
- Straightforward tasks where the desired solution is already known
- Work where research has already been done
- Purely internal code changes (no external dependencies)
- First 50%+ of a larger task (expect ~90% completion, rarely 100%)

**Avoid for:**
- Tasks requiring external API research
- Complex integration with unfamiliar libraries
- Work likely to need babysitting through repeated prompts

**Cost/Benefit:**

| Aspect      | Value                            |
| ----------- | -------------------------------- |
| Free tier   | 100 tasks/day                    |
| Concurrency | Up to 15 parallel                |
| Model       | Watered-down Gemini 3 (Mar 2026) |
| Quality     | Good for 50-90%, rarely complete |

**No Jules PR should be accepted without deep review. Automated reviews are insufficient.**

---

## Setup (Run Before First Command)

### 1. Install CLI

```bash
which jules || npm install -g @google/jules
```

### 2. Check Auth

```bash
jules remote list --repo
```

If fails → tell user to run `jules login` (or `--no-launch-browser` for headless)

### 3. Auto-Detect Repo

```bash
git remote get-url origin 2>/dev/null | sed -E 's#.*(github\.com)[/:]([^/]+/[^/.]+)(\.git)?#\2#'
```

If not GitHub or not in git repo → ask user for `--repo owner/repo`

### 4. Verify Repo Connected

Check repo is in `jules remote list --repo`. If not → direct to https://jules.google.com

## Commands

### Create Tasks

```bash
jules new "Fix auth bug" # Auto-detected repo
jules new --repo owner/repo "Add unit tests" # Specific repo
jules new --repo owner/repo --parallel 3 "Implement X" # Parallel sessions
cat task.md | jules new --repo owner/repo # From stdin
```

### Monitor

```bash
jules remote list --session # All sessions
jules remote list --repo # Connected repos
```

### Retrieve Results

```bash
jules remote pull --session <id>          # View diff
jules remote pull --session <id> --apply  # Apply locally
jules teleport <id>                       # Clone + apply
```

### Latest Session Shortcut

```bash
LATEST=$(jules remote list --session 2>/dev/null | awk 'NR==2 {print $1}')
jules remote pull --session $LATEST
```

## Smart Context Injection

Enrich prompts with current context for better results:

```bash
BRANCH=$(git branch --show-current)
RECENT_FILES=$(git diff --name-only HEAD~3 2>/dev/null | head -10 | tr '\n' ', ')
RECENT_COMMITS=$(git log --oneline -5 | tr '\n' '; ')
STAGED=$(git diff --cached --name-only | tr '\n' ', ')

jules new --repo owner/repo "Fix the bug in auth module. Context: branch=$BRANCH, recently modified: $RECENT_FILES"
```

## Template Prompts

### Add Tests

```bash
FILES=$(git diff --name-only HEAD~3 2>/dev/null | grep -E '\.(js|ts|py|go|java)$' | head -5 | tr '\n' ', ')
jules new "Add unit tests for recently modified files: $FILES. Include edge cases and mocks where needed."
```

### Add Documentation

```bash
FILES=$(git diff --name-only HEAD~3 2>/dev/null | grep -E '\.(js|ts|py|go|java)$' | head -5 | tr '\n' ', ')
jules new "Add documentation comments to: $FILES. Include function descriptions, parameters, return values, and examples."
```

### Fix Lint Errors

```bash
jules new "Fix all linting errors in the codebase. Run the linter, identify issues, and fix them while maintaining code functionality."
```

### Review PR

```bash
PR_NUM=123
PR_INFO=$(gh pr view $PR_NUM --json title,body,files --jq '"\(.title)\n\(.body)\nFiles: \(.files[].path)"')
jules new "Review this PR for bugs, security issues, and improvements: $PR_INFO"
```

## Workflow

1. **Create**: `jules new "Task description"`
2. **Monitor**: `jules remote list --session` or https://jules.google.com
3. **Pull**: `jules remote pull --session <id>`
4. **Validate**: Load `test-guidelines`, review adversarially
5. **Apply**: `jules remote pull --session <id> --apply` (only after validation)
6. **Reprompt**: If gaps found, reprompt Jules to continue

## Git Integration (Apply + Commit)

After Jules completes and you've validated the work:

```bash
SESSION_ID=""
TASK_DESC=""
git checkout -b "jules/$SESSION_ID"
jules remote pull --session "$SESSION_ID" --apply
git add -A
git commit -m "feat: $TASK_DESC
Jules session: $SESSION_ID"
git push -u origin "jules/$SESSION_ID"
gh pr create --title "$TASK_DESC" --body "Automated changes from Jules session $SESSION_ID"
```

## Poll Until Complete

```bash
SESSION_ID=""
while true; do
STATUS=$(jules remote list --session 2>/dev/null | grep "$SESSION_ID" | awk '{print $NF}')
case "$STATUS" in
Completed)
echo "Done!"
jules remote pull --session "$SESSION_ID"
break ;;
Failed)
echo "Failed. Check: https://jules.google.com/session/$SESSION_ID"
break ;;
*User*)
echo "Needs input: https://jules.google.com/session/$SESSION_ID"
break ;;
*)
echo "Status: $STATUS - waiting 30s..."
sleep 30 ;;
esac
done
```

## AGENTS.md Template

Create in repo root to improve Jules results:

```markdown
# AGENTS.md

## Project Overview

[Brief description]

## Tech Stack

- Language: [TypeScript/Python/Go/etc.]
- Framework: [React/FastAPI/Gin/etc.]
- Testing: [Jest/pytest/go test/etc.]

## Code Conventions

- [Linter/formatter used]
- [Naming conventions]
- [File organization]

## Testing Requirements

- Unit tests for new features
- Integration tests for APIs
- Coverage target: [X]%

## Build & Deploy

- Build: `[command]`
- Test: `[command]`
```

## Session States

| Status                 | Action            |
| ---------------------- | ----------------- |
| Planning / In Progress | Wait              |
| Awaiting User          | Respond at web UI |
| Completed              | Pull & validate   |
| Failed                 | Check web UI      |

## Notes

- **No CLI reply** → Use web UI for Jules questions
- **No CLI cancel** → Use web UI to cancel
- **GitHub only** → GitLab/Bitbucket not supported
- **AGENTS.md** → Jules reads from repo root for context
- **ALWAYS validate before applying changes**
