---
name: jules-delegation
description: Delegate coding tasks to Google's Jules AI agent on GitHub repositories. Use when you need to offload implementation work, bug fixes, tests, or refactoring to an AI agent that operates on a GitHub repo.
---

# Jules Delegation

Use Jules to delegate coding tasks to Google's AI agent on GitHub.

## IMPORTANT CAVEATS

**Jules is a weak agent with significant failure modes.** All work must be heavily validated, gated, and reviewed before approval. Treat Jules adversarially when reviewing its output.

### Common Failure Patterns

- **Hollow PRs**: Minimal or trivial changes that don't actually solve the problem
- **High LOC for simple features**: Unnecessarily verbose implementations
- **Rushing to fix**: No research into root causes, just monkey-patches
- **Poor integration**: Doesn't properly integrate with existing code patterns
- **Testing theater**: Tests that pass but don't verify meaningful behavior
- **Obfuscation**: Complex code that hides lack of substance
- **Reward hacking**: Finds the minimal path to "done" without real value
- **Early termination**: Stops before significant work is complete
- **Goal substitution**: Completes a different task than requested

### Validation Requirements

- **ALWAYS** load and apply the `test-guidelines` skill when reviewing Jules output
- Check that tests actually verify correctness, not just coverage
- Verify the implementation addresses the actual root cause
- Ensure integration with existing code patterns
- Look for shortcuts, workarounds, and incomplete solutions
- Reprompt Jules to continue when gaps are found

### Automated Review Limitations

If a PR is created, automated reviews will catch technical flaws but typically assume the code is morally "right." They will NOT detect:

- Hollow implementations
- Short-circuited work
- Reward hacking
- Goal substitution
- Incomplete solutions

### When to Use Jules

Jules has a restricted Linux environment with no access to online docs or external references. Context engineering in the prompt is essential.

**Best for:**

- Straightforward tasks where the desired solution is already known
- Work where research has already been done
- Purely internal code changes (no external dependencies)
- First 50%+ of a larger task (expect ~90% completion, rarely 100%)
- Long-running autonomous work

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

**Use Jules when:**

- Validation takes less work than doing it yourself
- Unlikely to introduce regressions not caught by existing tests
- Low babysitting expected (few prompt corrections needed)

**External Review Required:**

No Jules PR should be accepted without deep review by external auditors. Automated reviews are insufficient.

## Setup

**Must be in the desired git repo directory:**

```bash
# Verify you're in the right repo
pwd
git remote -v | grep <owner/repo>

# Verify installation
which jules

# Check auth
jules remote list --repo
# If not authenticated: jules login

# Verify repo is connected
jules remote list --repo | grep <owner/repo>
```

## Quick Start

```bash
# Create task (auto-detects repo from git remote)
cd ~/path/to/repo
jules new "Fix the auth bug"

# Or specify repo explicitly
jules new --repo owner/repo "Add unit tests"
```

## Context Injection

Enrich prompts with current context:

```bash
BRANCH=$(git branch --show-current)
RECENT_FILES=$(git diff --name-only HEAD~3 | head -10 | tr '\n' ', ')
STAGED=$(git diff --cached --name-only | tr '\n' ', ')

jules new --repo owner/repo "Fix bug. Branch: $BRANCH, recent files: $RECENT_FILES"
```

## Common Patterns

### Add Tests

```bash
FILES=$(git diff --name-only HEAD~3 | grep -E '\.(js|ts|py|go|java)$' | head -5 | tr '\n' ', ')
jules new --repo owner/repo "Add unit tests for: $FILES"
```

### Fix Lint Errors

```bash
jules new --repo owner/repo "Fix all linting errors in the codebase"
```

### Review PR

```bash
PR_NUM=123
PR_INFO=$(gh pr view $PR_NUM --json title,body,files --jq '"\(.title)\n\(.body)\nFiles: \(.files[].path)"')
jules new --repo owner/repo "Review PR: $PR_INFO"
```

## Workflow

1. **Create**: `jules new "Task description"`
2. **Monitor**: Check status at https://jules.google.com/session/{id}
3. **Pull**: `jules remote pull --session {id}`
4. **Validate**: Apply test-guidelines, review adversarially
5. **Apply**: `jules remote pull --session {id} --apply`
6. **Reprompt**: If gaps found, reprompt Jules to continue

## Git Integration

After Jules completes and you've validated the work:

```bash
SESSION_ID=""
git checkout -b "jules/$SESSION_ID"
jules remote pull --session "$SESSION_ID" --apply
git add -A
git commit -m "feat: description"
git push -u origin "jules/$SESSION_ID"
gh pr create --title "Description" --body "Jules session: $SESSION_ID"
```

## Session States

| Status               | Action            |
| -------------------- | ----------------- |
| Planning/In Progress | Wait              |
| Awaiting User        | Respond at web UI |
| Completed            | Pull & validate   |
| Failed               | Check web UI      |

## Notes

- No CLI reply → use web UI for questions
- No CLI cancel → use web UI
- GitHub only (no GitLab/Bitbucket)
- Jules reads repo's AGENTS.md for context
- ALWAYS validate before applying changes
