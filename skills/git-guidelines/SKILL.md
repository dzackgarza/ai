---
name: git-guidelines
description: Use when performing any git operation — staging, committing, branching, pushing, or deleting files. Required before any file edit to follow the checkpoint workflow, safe deletion rules, and commit format.
---

# Git Guidelines

## The Edit Workflow (Mandatory)

**Read → Checkpoint → Edit → Verify**

1. **Read** the file
2. **Checkpoint** — `git add <files>` (or commit) the _current_ state before touching anything
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

| DO                 | DON'T          |
| ------------------ | -------------- |
| `trash <file>`     | `rm <file>`    |
| `gio trash <file>` | `rm -rf <dir>` |

`rm` is irreversible. Before deleting: "Can this be recovered if I'm wrong?"

## Commit Messages

Commit messages are the canonical record of completed work. The body is mandatory for any nontrivial change. Write it for a reader who has the diff but not the context — they can see _what_ changed, so tell them _why_, _how you decided_, and _what to expect_.

### Format

```bash
git commit -m "$(cat <<'EOF'
<type>: <imperative summary under 70 chars>

Why: <problem or need that prompted this change>

Changes:
- <concrete change 1 and its rationale>
- <concrete change 2 and its rationale>

Decisions:
- <tradeoff or alternative considered, and why this path was chosen>

Expected outcome: <what should be different now, how to verify>

Co-Authored-By: <Your Model Name> <noreply@google.com>
EOF
)"
```

### Rules

- **Imperative mood** in summary: "Add X", "Fix Y", "Remove Z"
- **Body is mandatory** for multi-file changes, refactors, and any change where rationale is not obvious from the diff.
- **Why before what.** The diff shows what changed. The message explains why.
- **Decisions section**: capture tradeoffs, rejected alternatives, and constraints that shaped the approach. A future reader should understand not just what you chose but what you ruled out.
- **Expected outcome**: state the observable result. "Tests pass", "Endpoint returns 200", "File reduced from 315 to 174 lines."
- **Always include `Co-Authored-By`.** Use your actual model name and identity.

### Commit Type Prefixes

| Prefix       | Use                                 |
| ------------ | ----------------------------------- |
| `feat`       | New capability                      |
| `fix`        | Bug fix                             |
| `refactor`   | Restructure without behavior change |
| `docs`       | Documentation only                  |
| `test`       | Test additions or fixes             |
| `chore`      | Build, tooling, dependency changes  |
| `checkpoint` | Pre-edit safety snapshot            |

### Red / Green Examples

**Red (insufficient):**

```
refactor: rewrite AGENTS.md
```

**Green (canonical record):**

```
refactor: rewrite AGENTS.md for concision and structural compliance

Why: Post-mortem showed epistemic humility rules were violated despite
38 lines of declarative guidance. Duplication across 3 sections diluted
attention budget. File had grown to 315 lines organically.

Changes:
- Epistemic integrity: declarative "NEVER" rules → mandatory five-field
  output format. The format makes step-skipping a structural violation.
- Attention anchoring: epistemic rules at positions 2 and 8 (start/end).
- Merged Role + Calibration, added task→operation mapping table.
- Removed 5 instances of duplicated content.

Decisions:
- Chose process constraint over reinforced declarative rules because
  the post-mortem proved declarative rules fail even with emphasis.
- Kept tool routing in global file (user preference) rather than
  moving to project-level files.

Expected outcome: 174 lines (down from 315). All semantic content
preserved. Epistemic violations should decrease due to required format.
```

## Staging Discipline

```bash
# ✅ Specific files
git add src/opencode_parser/errors.py tests/test_triage.py

# ❌ May include .env, credentials, binaries
git add -A
git add .
```

## Hard Constraints

| Rule                          | Forbidden command              |
| ----------------------------- | ------------------------------ |
| Never skip hooks              | `--no-verify`                  |
| Never bypass signing          | `--no-gpg-sign`                |
| Never amend published commits | `--amend` on pushed commits    |
| Never force push main/master  | `git push --force origin main` |
| Never use interactive flags   | `git rebase -i`, `git add -i`  |
| Never `--no-edit` with rebase | not a valid rebase flag        |

## When to Commit vs. When Not To

**DO** checkpoint with `git add` before every edit.

**DO NOT** create a commit unless the user explicitly asks. Checkpointing and committing are separate acts.

**NEVER** commit files that may contain secrets: `.env`, `credentials.json`, keys.

## Commit Messages vs Memory vs Repo Artifacts

| Information                                       | Where it goes                   |
| ------------------------------------------------- | ------------------------------- |
| What changed, why, tradeoffs, decisions           | Commit message body             |
| Learned lessons, corrected workflows, calibration | Memory files                    |
| Current state, outstanding gaps, future work      | Repo artifacts (e.g. LEDGER.md) |

Completed work history belongs in commits, never in repo docs. **See: `agent-memory`** for the full decision test.

## Common Rationalizations

| Excuse                                         | Reality                                                  |
| ---------------------------------------------- | -------------------------------------------------------- |
| "The edit is tiny, no checkpoint needed"       | Size is irrelevant. Checkpoint first.                    |
| "I'll diff at the end when everything is done" | You verify each file immediately after editing it.       |
| "Bundling files makes history cleaner"         | Each file needs its own safety net. Checkpoint each one. |
| "git add -A is faster"                         | Faster is not safer. Stage specific files.               |
| "I already know what I changed"                | Diff anyway. Surprises exist.                            |
