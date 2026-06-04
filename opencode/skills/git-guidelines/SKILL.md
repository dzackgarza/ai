---
name: git-guidelines
description: 'Use when performing any git operation — staging, committing, branching, pushing, or deleting files.'
---
# Git Guidelines

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
**See: `agent-memory`** for the full decision test.

## PR Review Workflow

For nontrivial features: branch + PR → tag `@codex review` → wait 3–5 min for automated
reviewers (Codex, Qodo, etc.)
to post.

### Publish review guidance before submission

Before opening a PR, updating a PR for review, or tagging automated reviewers, ensure
the target repo’s local `AGENTS.md` contains the canonical review guidance from
`~/ai/PR_GUIDANCE.md`.

`~/ai/PR_GUIDANCE.md` is the source of truth.
The repo-local `AGENTS.md` copy is a required distribution copy because Codex and other
review agents read the target repo’s local guidance.
Do not replace it with a link, summary, or paraphrase.

Required handling:

- If the target repo has no local `AGENTS.md`, create one containing the canonical
  `# Review Guidelines` section from `~/ai/PR_GUIDANCE.md`.

- If local `AGENTS.md` already has a top-level `# Review Guidelines` section, replace
  that section with the current contents of `~/ai/PR_GUIDANCE.md`.

- If local `AGENTS.md` lacks that section, append the current contents of
  `~/ai/PR_GUIDANCE.md`.

- Do not create duplicate `# Review Guidelines` sections.

- Verify with `git diff` that the section is present, current, and the only local
  `AGENTS.md` change unless the user requested other edits.

If repo policy or permissions prevent updating local `AGENTS.md`, do not request review
yet. Report the blocker and the exact repo policy or permission issue.

### Review feedback is a judgment task

Review comments are not administrative obstacles to clear.
They are claims about the work that must be understood, accepted or rejected, and made
legible to the human maintainer.

Before resolving a thread, reporting a PR as clean, or moving to check polling, you must
be able to state:

> The reviewer is asking us to change or believe ___. The repo rule or project norm in
> tension is ___. The purpose of that rule is ___. My disposition is ___ because ___.
> The user can audit this in ___.

If you cannot fill those blanks with concrete evidence from the diff, source, repo
policy, or review text, you have not handled the feedback.
Read more, inspect the code, or stop and report the blocker.

Use Socratic pressure to test the disposition:

- What would be false or missing if I simply marked this resolved?

- What evidence would convince the user that I understood the suggestion?

- Which repo rule’s purpose would be harmed by literal compliance?

- Which repo rule’s purpose would be harmed by ignoring the suggestion?

- If I reject this advice, what concrete source or policy fact defeats it?

If any answer is scanner status, check status, process compliance, or a claim that a bot
will re-review later, stop.
That is not judgment.

### Split feedback from remediation

Every review item has two separable claims:

1. The feedback claim: what is allegedly wrong?
2. The suggested remediation: what change is being proposed?

Classify both. A true claim does not make the proposed fix acceptable.
A bad proposed fix does not make the underlying claim false.

Disposition options:
- Accepted as written
- Accepted with modified remediation
- Rejected
- Investigate before action

### Interpret policy by purpose

Repo rules exist to protect the work, not to excuse abandoning it.
When review feedback conflicts with a literal reading of repo guidance, do judicial
analysis:

- Identify the substantive concern raised by the reviewer.

- Identify the literal repo rule, hook, or policy that appears to block the fix.

- State the purpose of that rule.

- Decide which action best preserves that purpose and the project objective.

- Leave the reasoning in the thread response or commit message.

Some correct decisions may contradict a literal reading of a repo rule.
That is allowed only when the decision preserves the rule’s purpose, is source-backed,
and leaves a clear audit trail.
Never use this to bypass hard safety constraints such as secrets handling, destructive
git operations, or explicit user refusal.

### Thread responses are audit notes for users

A review reply is not a conversation with the bot.
Automated reviewers usually will not return to debate the point.
Write every reply for the human maintainer who needs to understand exactly why the
suggestion was accepted, modified, or rejected.

Each substantive reply must include:

- Disposition: accepted, accepted with modification, or rejected.

- Reason: the source evidence, repo policy, and tradeoff that determined the decision.

- Audit anchor: the commit, file, line, command output, or linked issue where the user
  can verify the disposition.

- Policy interpretation: when repo guidance is involved, explain how the action follows
  the spirit of the rule, not merely its literal text.

Visible thread reply must state:

- Claim disposition:
- Remediation disposition:
- Policy basis:
- Code/action taken or explicit non-change:
- Audit anchor:

A PR thread resolved by deletion must not say only “removed.” It must follow the deletion disposition format:

- Deleted artifact:
- Original burden:
- Burden disposition:
  - solved by:
  - invalidated by:
  - transferred to:
  - remains open in:
- Verification:

Do not write replies like “fixed”, “done”, “addressed”, “acknowledged”, or “will follow
up” unless the surrounding text contains the actual disposition and evidence.
Do not address the reviewer as if it is waiting to chat.

Never resolve a review thread without first posting a visible human-readable reply on
that thread. The resolve-tool justification is not an audit trail; it is hidden from the
user in the normal PR reading flow.
Resolving without a visible reply hides feedback and is banned, even if the code was
changed correctly.

### Banned PR-review behavior

- Treating `NOT RESOLVED: 0`, green checks, or a clean scanner as proof that review
  advice was understood.

- Treating a hook, policy, or tool rejection as a terminal reason to abandon
  source-backed feedback without interpreting the rule’s purpose.

- Resolving a review comment without a visible thread response that records the
  disposition, evidence, and policy reasoning.

- Resolving a thread before the code, commit message, or thread response shows the
  disposition and reasoning.

- Polling checks while any review, top-level comment, check annotation, or summary
  comment has not been substantively dispositioned.

- Reporting “remaining: none” when only inline threads were scanned.

- Laundering feedback through process language such as “scanner clean”, “thread
  resolved”, or “bot pending” instead of stating the judgment made.

### Scan ALL comment surfaces

`gh pr view` only returns issue-level comments, not inline review thread comments.
To properly parse and summarize all PR feedback, **use the bundled CLI tool**:

```bash
uv run -m extract_unresolved_issues --help
```

You can run it from anywhere in the codebase directly by providing the full path to the
module inside the git-guidelines skill:

```bash
uv run --directory ~/ai/opencode/skills/git-guidelines/scripts/extract_unresolved_issues -m extract_unresolved_issues summarize <owner>/<repo>#<N>
```

This tool automatically pulls:

- Top-level PR comments

- Inline code review threads

- Automated check-run errors (like Codacy static analysis)

Disposition every feedback item.
For accepted inline feedback, reply with the human-readable disposition and fix commit,
then resolve the thread using the tool’s `resolve` command:

```bash
uv run --directory ~/ai/opencode/skills/git-guidelines/scripts/extract_unresolved_issues -m extract_unresolved_issues resolve <COMMENT_ID> "Accepted in commit 1234abc. Reason: <why this satisfies the review concern and repo policy>."
```

**The script never produces stale output.** Automated bots (Codacy, Gemini,
kilo-code-bot) update their comments in place when new commits land.
Open review threads stay listed until the “Resolve Conversation” button is clicked.
Every item in the output requires disposition — fix it, reject it with evidence, or
report why it is blocked.
There is no such thing as an already-handled item that still appears.

**All checks, warnings, and notices must be resolved before the PR can be accepted.**
This includes low-severity notices from automated tools.
If a check is failing, the PR is blocked regardless of how many threads have been
resolved.

**After pushing a fix, loop until the check clears.** Codacy re-runs typically complete
within 1 minute. Poll with a 1–2 minute sleep between scans:

```bash
# Loop until all checks pass
while true; do
    gh pr checks <N> --repo <owner>/<repo>
    uv run --directory ~/ai/opencode/skills/git-guidelines/scripts/extract_unresolved_issues \
        -m extract_unresolved_issues issues <owner>/<repo>#<N>
    sleep 90
done
```

Stop only when `gh pr checks` shows all green and the `issues` command reports
`NOT RESOLVED: 0`.

### “Resolve” is overloaded — clear each surface separately

| Object | How to resolve |
| --- | --- |
| Inline review thread | Reply in thread + resolve via GraphQL |
| Top-level PR comment | Reply on comment surface (no resolution bit) |
| Review summary comment | Reply on PR comment surface |
| Linked GitHub issue | Update/comment/close the issue itself — PR-thread resolution does NOT close the issue |

### After replying or resolving

Rerun the full PR scan AND the relevant issue scan.
Bots can post follow-up comments after your reply.

```bash
gh issue view <N> --repo <owner>/<repo> --json state,title,url
gh api repos/<owner>/<repo>/issues/<N>/comments
```

### Jules Review Delegation

If the user asks to use Jules for review, load:
- [jules](file:///home/dzack/ai/opencode/skills/jules/SKILL.md)
- [jules/references/anti-slop-review-workflow](file:///home/dzack/ai/opencode/skills/jules/references/anti-slop-review-workflow.md)
- [reviewing-llm-code](file:///home/dzack/ai/opencode/skills/reviewing-llm-code/SKILL.md)
- [anti-slop](file:///home/dzack/ai/opencode/skills/anti-slop/SKILL.md)
- [reviewing-subagent-work](file:///home/dzack/ai/opencode/skills/reviewing-subagent-work/SKILL.md)
- `test-guidelines` if tests/QC/proof surfaces are in scope
- `pr-feedback-triage` if existing review comments are being evaluated

## Issue Workflow

### Filing Issues

**All issues must be labeled immediately upon creation.**

Use
`gh issue create --repo <owner>/<repo> --title "..." --body-file issue.md --label "<label>"`

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

**Mandatory**: If a concrete problem is observed but cannot be fixed trivially in the
current task, log it as an issue.
Do not file speculative concerns; frame them as `enhancement` if necessary.

## Common Rationalizations

| Excuse | Reality |
| --- | --- |
| “The edit is tiny, no checkpoint needed” | Size is irrelevant. Checkpoint first. |
| “I’ll diff at the end when everything is done” | You verify each file immediately after editing it. |
| “Bundling files makes history cleaner” | Each file needs its own safety net. Checkpoint each one. |
| “git add -A is faster” | Faster is not safer. Stage specific files. |
| “I already know what I changed” | Diff anyway. Surprises exist. |
