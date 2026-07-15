---
name: git-operational-policy
description: Use before Git or GitHub work for staging, commit, deletion-safety, checkpoint, and push invariants.
---
# Git Operational Policy

This is the cross-cutting safety baseline for every route selected by [[git-guidelines/SKILL|the Git router]].
It owns checkpointing, staging, commit, deletion-safety, and push invariants.
Authentication, repositories, issues, pull requests, review, and returned feedback belong to their routed leaves.

## The Edit Workflow (Mandatory)

**Read → Checkpoint Commit → Edit → Verify → Commit**

1. **Read** the file

2. **Checkpoint commit** the current target-file state before touching it.
   If the target file is clean, `HEAD` is the checkpoint.
   If the target file already has uncommitted changes, commit those changes first or stop
   and ask how to proceed.
   Staging is not a checkpoint.

3. **Edit** the file

4. **Verify** — run `git diff` immediately after to confirm what changed

5. **Commit** every coherent substantive change before switching tasks, reporting
   completion, starting a risky follow-up edit, or leaving work to another session.
   Do not leave real work only in the index or working tree.

This applies to **every edit** — one-liners, multi-file changes, everything.
No exceptions.

## Red Flags — Stop and Checkpoint First

You are about to violate the workflow if:

- You are writing an Edit/Write tool call and the target file has uncommitted changes
  that are not already committed as the pre-edit checkpoint

- You are “just fixing a typo” (still requires checkpoint)

- You plan to diff “at the end” instead of after each file

- You plan to commit “later” after accumulating multiple independent changes

- You are bundling unrelated edits across files into one checkpoint

Each coherent change gets its own checkpoint commit.
Bundling unrelated work is not cleaner history — it is missing provenance.

## Safe Deletion

| DO | DON’T |
| --- | --- |
| `trash <file>` | `rm <file>` |
| `gio trash <file>` | `rm -rf <dir>` |

`rm` is irreversible.
Before deleting: “Can this be recovered if I’m wrong?”

## Destructive Git Operations

Never run `git checkout`, `git reset`, `git revert`, `git restore`, `git stash`, or any
other history/state operation that discards or hides work unless the user literally and
precisely requested that operation.

If you need to recover an old state:

- inspect the old content with read-only commands such as `git show`
- apply forward edits that restore the desired content
- commit the restoration as new history

Do not dump an old git version over a file as a shortcut.
The audit trail must show the original state, the mistaken edit, and the forward-facing
repair.

If a safety policy blocks a destructive operation, stop.
Do not work around the block or pivot to a different state-manipulation command.

## Commit Messages

Commit messages are the canonical record of completed work.
The body is mandatory for any nontrivial change.
Write it for a reader who has the diff but not the context — they can see *what*
changed, so tell them *why*, *how you decided*, and *what to expect*.

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

- **Imperative mood** in summary: “Add X”, “Fix Y”, “Remove Z”

- **Body is mandatory** for multi-file changes, refactors, and any change where
  rationale is not obvious from the diff.

- **Why before what.** The diff shows what changed.
  The message explains why.

- **Decisions section**: capture tradeoffs, rejected alternatives, and constraints that
  shaped the approach.
  A future reader should understand not just what you chose but what you ruled out.

- **Expected outcome**: state the observable result.
  “Tests pass”, “Endpoint returns 200”, “File reduced from 315 to 174 lines.”

- **Always include `Co-Authored-By`.** Use your actual model name and identity.

### Commit Type Prefixes

| Prefix | Use |
| --- | --- |
| `feat` | New capability |
| `fix` | Bug fix |
| `refactor` | Restructure without behavior change |
| `docs` | Documentation only |
| `test` | Test additions or fixes |
| `chore` | Build, tooling, dependency changes |
| `checkpoint` | Pre-edit safety snapshot |

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

Staging prepares a commit.
It is not itself a checkpoint or audit trail.

```bash
# ✅ Specific files
git add src/opencode_parser/errors.py tests/test_triage.py

# ❌ May include .env, credentials, binaries
git add -A
git add .
```

## Hard Constraints

| Rule | Forbidden command |
| --- | --- |
| Never skip hooks | `--no-verify` |
| Never bypass signing | `--no-gpg-sign` |
| Never amend published commits | `--amend` on pushed commits |
| Never force push main/master | `git push --force origin main` |
| Never use interactive flags | `git rebase -i`, `git add -i` |
| Never `--no-edit` with rebase | not a valid rebase flag |

## Commit Cadence

**DO** commit proactively.
User requests to commit or push are a lower bound, not permission gates.
If you changed tracked files in a way that advances, preserves, repairs, or tests the
task, commit it.

Commit immediately after:

- a source fix, test, spec row, mapping row, or other substantive artifact is verified;

- a red test is created for a reported bug;

- a green fix makes a committed red test pass;

- a workflow or policy contradiction is corrected;

- a long-running or multi-step task reaches a coherent review point;

- the user asks whether work was committed, asks for a handoff, or asks to stop.

Do not wait for explicit user approval to commit ordinary task progress.
Do not let hours of work accumulate only in the index or working tree.

**DO NOT** commit:

- read-only investigation;

- secrets or credential material;

- unrelated dirty files you did not touch;

- changes you do not understand well enough to describe in the commit body.

**NEVER** commit files that may contain secrets: `.env`, `credentials.json`, keys.

## Push Cadence

Push after committing when the user asked for pushed work, when the task depends on
GitHub-visible auditability, before claiming completion, and before any handoff after
substantive work.
If push fails, report the exact failure instead of treating a local commit as remotely
auditable.

## Commit Messages vs Memory vs Repo Artifacts

| Information | Where it goes |
| --- | --- |
| What changed, why, tradeoffs, decisions | Commit message body |
| Learned lessons, corrected workflows, calibration | Memory files |
| Current state, outstanding gaps, future work | Repo artifacts (e.g. LEDGER.md) |

Completed work history belongs in commits, never in repo docs.
**See: [[agent-memory/SKILL|agent-memory]]** for the full decision test.

## Returned PR feedback

Returned review feedback is owned by [[pr-feedback-triage/SKILL|pr-feedback-triage]].
Load that skill before using GitHub mechanics; it owns collection, policy-routed disposition, first-principles remediation, thread-local replies, resolution, and convergence.
This operational leaf supplies only staging, commit, push, authentication, and API mechanics.
Do not restate the feedback state machine here, create a top-level disposition ledger, or create a tracked review-log file.

## Issue work

Route issue creation, triage, governance, and writing rules to [[git-guidelines/github-issues/SKILL|GitHub issues]].
This operational baseline does not duplicate that procedure.

## Common Rationalizations

| Excuse | Reality |
| --- | --- |
| “The edit is tiny, no checkpoint needed” | Size is irrelevant. Checkpoint first. |
| “I’ll diff at the end when everything is done” | You verify each file immediately after editing it. |
| “Bundling files makes history cleaner” | Each file needs its own safety net. Checkpoint each one. |
| “git add -A is faster” | Faster is not safer. Stage specific files. |
| “I already know what I changed” | Diff anyway. Surprises exist. |
