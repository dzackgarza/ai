---
name: git-guidelines
description: Use when performing any git operation — staging, committing, branching, pushing, or deleting files. Required before any file edit to follow the checkpoint workflow, safe deletion rules, and commit format.
---

# Git Guidelines

## The Edit Workflow (Mandatory)

**Read → Checkpoint → Edit → Verify**

1. **Read** the file
2. **Checkpoint** — `git add <files>` (or commit) the *current* state before touching anything
3. **Edit** the file
4. **Verify** — run `git diff` immediately after to confirm what changed

This applies to **every edit** — one-liners, multi-file changes, everything. No exceptions.

## Red Flags — Stop and Checkpoint First

You are about to violate the workflow if:
- You are writing an Edit/Write tool call and haven't staged first
- You are "just fixing a typo" (still requires checkpoint)
- You plan to diff "at the end" instead of after each file
- You are bundling edits across files into one checkpoint

Each file gets its own checkpoint. Bundling is not cleaner history — it's missing safety.

## Safe Deletion

| DO | DON'T |
|----|-------|
| `trash <file>` | `rm <file>` |
| `gio trash <file>` | `rm -rf <dir>` |

`rm` is irreversible. Before deleting: "Can this be recovered if I'm wrong?"

## Commit Messages

```bash
git commit -m "$(cat <<'EOF'
Short imperative summary (under 70 chars)

Optional body explaining why, not what.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"
```

- Imperative mood: "Add X", "Fix Y", "Remove Z"
- Focus on *why*, not *what*
- Always include `Co-Authored-By`

## Staging Discipline

```bash
# ✅ Specific files
git add src/opencode_parser/errors.py tests/test_triage.py

# ❌ May include .env, credentials, binaries
git add -A
git add .
```

## Hard Constraints

| Rule | Forbidden command |
|------|-------------------|
| Never skip hooks | `--no-verify` |
| Never bypass signing | `--no-gpg-sign` |
| Never amend published commits | `--amend` on pushed commits |
| Never force push main/master | `git push --force origin main` |
| Never use interactive flags | `git rebase -i`, `git add -i` |
| Never `--no-edit` with rebase | not a valid rebase flag |

## When to Commit vs. When Not To

**DO** checkpoint with `git add` before every edit.

**DO NOT** create a commit unless the user explicitly asks. Checkpointing and committing are separate acts.

**NEVER** commit files that may contain secrets: `.env`, `credentials.json`, keys.

## What Goes in the Commit Message

Commit messages are the canonical record of completed work. Write them accordingly:

- **Body**: explain *why* decisions were made, what tradeoffs were accepted
- **Details of what changed**: belong here, not in repo docs or memory
- Repo artifacts track *current state + future work*, never completed work history
- Learned lessons and corrected workflows belong in **memory**, not the commit body

**See: `agent-memory`** for the full decision test (memory vs git vs repo artifacts).

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "The edit is tiny, no checkpoint needed" | Size is irrelevant. Checkpoint first. |
| "I'll diff at the end when everything is done" | You verify each file immediately after editing it. |
| "Bundling files makes history cleaner" | Each file needs its own safety net. Checkpoint each one. |
| "git add -A is faster" | Faster is not safer. Stage specific files. |
| "I already know what I changed" | Diff anyway. Surprises exist. |
