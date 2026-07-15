---
name: git-operational-policy
description: Use when performing any git or GitHub operation — staging, committing,
  branching, pushing, PRs, code review, issues, auth, repo management, or deleting
  files. Consolidated entry point for all git skills.
---
# Git Guidelines

## Structure

This skill is the consolidated entry point for all git and GitHub operations.
Reference docs within this skill:

- `auth.md` — GitHub authentication (tokens, SSH, gh CLI, API access)
- `pr-workflow.md` — branch, commit, push, CI monitoring, merge lifecycle
- `code-review.md` — performing code reviews on local changes and PRs
- `creating-prs.md` — PR worker guide (contracts, review readiness, feedback handling)
- `reviewing-prs.md` — field guide for reviewing AI-assisted code
- `issues.md` — issue management (view, create, manage, triage)
- `repo-management.md` — clone, create, fork, settings, releases, workflows
- `scripts/extract_unresolved_issues/` — PR review scanning tool (see PR Review Workflow below)

The former separate skills [[git-guidelines/github-auth/SKILL|github-auth]], [[git-guidelines/github-pr-workflow/SKILL|github-pr-workflow]], [[git-guidelines/github-code-review/SKILL|github-code-review]],
[[git-guidelines/github-issues/SKILL|github-issues]], and [[git-guidelines/github-repo-management/SKILL|github-repo-management]] have been consolidated here.
Each old location remains as a redirect stub.

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

## Issue Workflow

### Owned Repo Improvement Loop

For repos owned by this system, observed defects should not remain as chat residue or
private notes.
If an app, tool, plugin, QC gate, or agent workflow has a small observed error,
inefficiency, false green, confusing edge case, or recurring paper cut, do one of these
before handoff:

- fix it in the current coherent work unit and commit the fix;
- file a GitHub issue on the owning repo with evidence and concrete expected behavior;
- if ownership or scope is ambiguous, ask the user where to file it.

Do not file speculative bugs. Do not create issues for vague dissatisfaction without an
observed example. Do not bury observed owned-repo defects only in memory; memory can note
the durable lesson, but the actionable project gap belongs on GitHub.

### Filing Issues

**All issues must be labeled immediately upon creation.**

Use
`gh issue create --repo <owner>/<repo> --title "..." --body-file issue.md --label "<label>"`

For roadmap, feature, PRD, or cross-agent planning issues, first load
`plan/references/externalization.md`. Create story-shaped issue nodes, use native
sub-issues for parent/child tree edges, use dependencies only for blockers, assign the
GitHub Milestone that owns the delivery slice, and avoid turning a wiki page or issue body
into a second live tracker.

**Mandatory Issue Rules:**

1. **Deep description**: Explain exactly what is happening or missing.

2. **Proof**: Include relevant logs, outputs, error traces, or code snippets that PROVE
   the issue exists. Provide as many clear examples as possible.

3. **Concrete Expectations**: Describe new designs, specs, and expected behavior.
   Include TDD-style pseudocode showing what the expected new behavior looks like.
   Do not list “benefits”.

4. **Informative Only**: Use plain, technical language.
   No marketing or selling language.

5. **No Implementation Code**: Do NOT attempt to write the actual code to fix the
   problem in the issue body.
   The person filing the issue does NOT decide HOW to fix it; they provide data to more
   specialized design and triage agents.

6. **No Plans**: Do not include a step-by-step “plan” to fix the issue.
   That is a separate task.
   High-level suggestions for phases are permitted.

7. **No Time Estimates**: NEVER include time estimates.

**Minimal Issue Template:**

Create a local `.md` file for the body and pass it to `gh issue create --body-file`:

```markdown
# Description

<Deep description of the problem or feature>

# Evidence

<Logs, outputs, or code proving the issue exists. Clear examples.>

# Expected Behavior

<Concrete expectations. TDD-style pseudocode.>

# Suggested Phases (Optional)

<High-level suggestions for phases, but no detailed implementation plan.>
```

### Available Labels

- `bug`: Observed bugs, failures, or incorrect behavior.

- `enhancement`: Feature requests, improvements, or design ideas.

- `documentation`: Improvements or additions to documentation.

**Mandatory**: If an observed owned-repo defect, inefficiency, false green, or recurring
paper cut cannot be fixed in the current coherent work unit, log it as an issue on the
owning repo.
Do not file speculative concerns; frame observed improvement ideas as `enhancement` when
they are not bugs.

## Common Rationalizations

| Excuse | Reality |
| --- | --- |
| “The edit is tiny, no checkpoint needed” | Size is irrelevant. Checkpoint first. |
| “I’ll diff at the end when everything is done” | You verify each file immediately after editing it. |
| “Bundling files makes history cleaner” | Each file needs its own safety net. Checkpoint each one. |
| “git add -A is faster” | Faster is not safer. Stage specific files. |
| “I already know what I changed” | Diff anyway. Surprises exist. |
