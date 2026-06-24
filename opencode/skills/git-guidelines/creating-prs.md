# PR Worker Guide: How to Submit Work That Produces High-Quality Review Feedback

## Purpose

This guide is for PR workers, including agentic coding systems and human contributors
using LLM assistance.
Its purpose is not to optimize for “getting approved.”
Its purpose is to make the work legible, falsifiable, and reviewable, so that reviewer
feedback is anchored to the actual intended outcome rather than to a post-hoc story
constructed after the code already exists.

The main failure to prevent is this:

- code is written first,

- completion criteria are inferred from the resulting code,

- the PR description is retrofitted to match what now exists,

- reviewers evaluate against those retrofitted criteria,

- the result is a tautologous thumbs-up on work that may not meet the original need.

This guide therefore imposes one hard rule:

> **Jules-initiated PRs:** For any PR initiated by Jules, a contract must be written
> before implementation, committed to the branch, and used as the source of truth for
> the PR body. Do not let the code define the task after the fact.
> See the **Jules skill → PR Contract** section for the full mandatory workflow,
> template, and required contents.

> **Other PRs:** For any nontrivial PR, or any PR derived from a finalized local plan,
> externalize the plan into the repository's GitHub issue tree and milestone scope before
> opening the PR. Use the PR body to expose the selected issue set or subtree this branch
> claims, plus the implementation plan and evidence for that claim. Contract files are
> optional only for truly trivial changes whose outcome, scope, acceptance criteria, and
> evidence fit directly in the PR body.

* * *

## Core principle

A review is only as good as the target it is reviewing against.

If the intended outcome is underspecified, or if the worker allows the implementation to
define its own success criteria after the fact, reviewers are forced into local or
stylistic review. They can comment on naming, tests, structure, and plausibility, but
they cannot reliably say whether the change meets the actual need.

The worker must therefore supply, in advance:

1. the intended outcome,

2. the non-goals,

3. the acceptance criteria,

4. the specific evidence that will count as success,

5. the boundaries of the change,

6. the exact unresolved questions, if any.

That is what enables strong process-alignment feedback.

* * *

## Source plan to issue tree admission gate

PR creation must be a lossless projection from the finalized source plan or contract into
GitHub's issue tree, milestone scope, and PR claim map. It is not a second round of
planning. If the worker cannot place the work under an existing roadmap node, issue
subtree, or new top-level roadmap issue without inventing scope, user behavior,
acceptance criteria, proof burdens, milestone cuts, or dependency order, the source plan
is not ready to externalize.

The normal sequence is:

1. finalize the plan interactively;
2. inspect existing GitHub issues, sub-issues, milestones, draft PRs, and wiki roadmap
   projection;
3. create or update story-shaped issues under the correct parent issue, using native
   sub-issues for parent/child edges when the active GitHub surface supports them;
4. preserve sibling order through sub-issue order where available, and use issue
   dependencies only for blockers;
5. create or select a GitHub Milestone object for the delivery slice, with scope stated
   as a subtree root or explicit issue set;
6. assign descendant issues that count toward delivery, and the PRs linked to those
   issues, to the milestone;
7. open the PR as a draft from the selected issue set or subtree, assign the milestone,
   and state the close/reference split in the PR body;
8. add PR Development links or closing keywords only for issues this PR fully satisfies
   on merge;
9. keep the PR draft until every claimed issue or proof obligation is complete and
   evidenced.

Before creating the PR, verify that the source plan fixes:

- the externally meaningful story, included scope, explicit exclusions, preserved
  behavior, and observable completion condition;

- the tree placement: root roadmap issue, parent issue or wiki roadmap node, sibling
  order, milestone-sized subtree, and blocker dependencies;

- every proof obligation's actor, trigger or context, intended result, acceptance
  criteria, proof burden, dependencies, and supplied artifacts;

- stable vocabulary and complete referents, so labels such as test IDs, issue numbers,
  file names, transcript phrases, and local shorthand are evidence pointers rather than
  unexplained requirements;

- proof design before implementation assessment. Evidence answers declared criteria; it
  does not define the criteria after code happens to pass;

- the GitHub Milestone that groups the delivery slice's issues and linked PRs;

- which issues the PR should close on merge, which issues it partially advances, and
  which broader parent, deferred, or excluded issues it should only reference.

The issue-tree, milestone, wiki, and PR projections may add owner, branch, status,
blocker, commit, run, artifact, and review-link metadata. They must not add, delete,
demote, or reinterpret scope, behavior, acceptance criteria, proof burdens,
dependencies, handoffs, or integration semantics.

Stop and repair the source plan when any of these are true:

- the root milestone is defined as tests passing, review readiness, checklist completion,
  or another derived status;

- a user or system behavior is represented only by a test ID, file name, command, commit,
  issue number, or implementation detail;

- an obligation lacks objective acceptance criteria or proof burden;

- a task can be completed by touching documentation, changing a label, classifying a
  failure, or making a check green while leaving the intended behavior unresolved;

- scope relies on private phrases such as "remaining", "in flight", "other relevant", or
  transcript-only context;

- the plan has unresolved product, architecture, dependency, ownership, or sequencing
  decisions;

- scattered sources disagree and the worker would need to choose between competing
  intent, implementation state, hypotheses, or status claims;

- evidence is only provenance, command execution, artifact existence, or green status,
  without showing attained behavior and why the witness rejects plausible broken cases;

- old checkmarks, repeated claims, or source-by-source summaries would become public
  progress without re-evaluation against current acceptance criteria.

- a nontrivial top-level PR checkbox would lack a link to a GitHub issue that owns its
  scope, acceptance criteria, and proof burden.

- the PR checklist would include deferred work, out-of-scope work, backlog work,
  follow-up work for later PRs, unchosen alternatives, or other items that are not
  required before this PR can be ready for review.

- the PR body would only mention issues in checklist prose without closing keywords or
  manual Development links for issues this PR is meant to close.

- a closing keyword would target a parent issue, deferred issue, future issue, partial
  claim, or out-of-scope issue that this PR does not fully complete.

- the PR would span multiple GitHub Milestones without either splitting the PR or naming
  the broader milestone/release that owns the cross-milestone claim and why.

## PR body as issue claim map

Use an issue-linked claim map as the centralized live tracking surface for the current
branch. The issue tree owns the broader decomposition. The GitHub Milestone owns the
delivery grouping. The PR body owns this branch's selected issue set or subtree,
implementation plan, proof claims, evidence, and explicit non-claims. If a checkbox
appears in the PR body, completing it is required before the PR can leave draft.

Minimum body shape:

```markdown
## Intended result
<externally observable project or user result>

## Scope
- Included: <finite surface>
- Excluded: <explicit non-goals>
- Preserved behavior: <baseline that must remain true>

## GitHub tracking
- Target issue set / subtree: <#root, #child list, or explicit issue set>
- Milestone: <GitHub Milestone assigned to the delivery slice and this PR>
- Closes on merge:
  - Closes #<issue fully completed by this PR>
- References only:
  - Refs #<parent, deferred, partial, or excluded issue not closed by this PR>

## Implementation plan
<what is stacked, what is parallel, and what integrates last>

## Claim map
- [ ] **<#issue or story node> - <claim this PR makes>**
  - Proof obligations claimed: <named obligations>
  - Partial / not claimed: <obligations this PR does not satisfy>
  - Evidence required: <proof mapped to each criterion>
  - Current evidence: <links to tests, CI, screenshots, logs, artifacts, or review>

## Automated gates
<authoritative checks named, with live truth owned by CI or rulesets>
```

Use closing keywords only for issues the PR fully completes and should close on merge.
Use `Refs` or prose for parent issues, future work, deferred work, excluded scope,
partial claims, and issues that remain open after this PR. If the PR targets a
non-default branch or GitHub does not show the expected Development links, add the
manual Development links before asking for review.

Use typed nodes. A roadmap, phase, feature, story, proof obligation, or implementation
task should stay at its own altitude. Proof obligations normally live in the owning issue
body as definition-of-done material; split them into child issues only when they are
independently trackable. Parent completion follows from semantic attainment and supported
evidence, not merely from checked descendants.

Checklist items must earn reviewer attention. A checkbox is valid only when it represents
a meaningful portion of the PR claim that can be independently judged complete. Test
names, commands, commits, artifacts, green checks, policy declarations, and environment
setup are not top-level progress items unless they are attached to the substantive
obligation they prove or unblock.

For nontrivial PRs, every top-level checkbox must link to the GitHub issue that owns that
claim, acceptance criteria, and proof burden. Deeper checklist nodes may link to issues
when they are independently tracked; otherwise they remain acceptance/proof detail under
the owning issue-linked node.

Do not add checkbox items for deferred work, explicitly excluded scope, future PRs,
parking-lot ideas, unresolved alternatives, or nice-to-have cleanup. Put those in the
`Scope` section, linked issues, or review discussion as prose. A visible open checkbox
means the PR is not done; a checkbox that does not need to be completed before review is
a false blocker and makes the PR impossible to read as complete.

Keep the PR in draft while any in-scope claim item remains open. Mark it ready for review
only after the claim map represents no remaining required work, the evidence under each
item is current, and the automated gates are either green or named as real blockers. If
later feedback reopens required work, convert the PR back to draft.

### Tracking item quality

A PR checkbox is reviewer-hacking when it is easy to tick but empty of correctness. Top-level
items must start from externally meaningful behavior, decisions, or work products, then
attach commits, commands, tests, and artifacts as evidence under that obligation.

"Drive Beamer PDF export from the app menu" is a valid tracking item because it names a
user path, expected output, and proof surface. "Re-run proof coverage," "Update
Implementation-Status," or "Commit proof-artifacts/run.json" is weak unless the item is
nested under the obligation it proves and states the criterion, content, and reviewer use.

Sequencing work is valid when the PR cannot be reviewed correctly without it. "Publish
local review guidance in AGENTS.md before review" can be a legitimate precondition because
it calibrates reviewers against the governing policy. Classification labels such as
`env-blocked` are not standalone tasks; put them under the blocked substantive item with
concrete evidence and an unblock condition.

Do not add amendment-auditability, PR-comment-versioning, or tracking-the-tracking
checkboxes. GitHub already preserves PR comments and review history. When a plan changes,
update the source plan or PR body and use normal review discussion for the decision; do
not make a deliverable out of proving that the discussion exists.

## Content placement

Put each fact in the surface that can represent and enforce it:

- GitHub issue tree: canonical public decomposition for the finalized plan, including
  roadmap nodes, feature/story nodes, parent-child edges, sibling order, blocker
  dependencies, acceptance criteria, and proof obligations.

- GitHub Milestone: delivery or progress bucket over issues and PRs. It should name the
  subtree root or explicit issue set it covers, then attach the descendant issues and
  linked PRs that count toward that delivery slice.

- GitHub PR Development links: closing-keyword or manual links between the PR and the
  in-scope issues that should close when the PR merges.

- PR body: centralized live claim map for the current branch's issue set or subtree,
  implementation plan, substantive tasks, meaningful blockers, acceptance criteria,
  evidence mappings, close/reference split, and checklist items linked to the relevant
  GitHub issues. Deferred or excluded work belongs in prose or linked issues, not as PR
  checkboxes.

- GitHub wiki: durable narrative context and readable roadmap projection. It may render
  or link the issue tree, but it must not become a manually maintained live status mirror.

- Repository guidance or skills: global review policy, definitions of proof/completion,
  evidence standards, naming conventions, and agent calibration.

- CI, rulesets, and security settings: machine-derived invariants such as tests passing,
  required artifact schemas, branch protection, and policy synchronization.

- PR comments or review threads: discussion, resolved objections, local debugging detail,
  and historical context that should not become the current tracking surface.

- Evidence artifacts: generated outputs, screenshots, structured run reports, logs, CI
  runs, and baselines. Artifact existence is not itself progress; link each witness
  beneath the obligation and criterion it supports.

- Local scratchpads and setup surfaces: source inventories, worksheets, command history,
  raw transcripts, obsolete alternatives, repeated classifications, and environment setup.
  Link them only for optional depth when the public node is self-contained.

- Linked subplans or local scratchpads: derivation material that is too detailed or
  provisional for the issue tree. These are optional depth, not the authoritative tracker
  after issue externalization.

Do not duplicate global policy in the PR body. A PR may include a sequencing task to
publish or sync required guidance before review, but the policy itself stays in the
canonical governing source.

Publish the current plan, not the consolidation process. Do not expose source-by-source
diaries, normalization worksheets, raw agent reasoning, local command history, obsolete
alternatives, or manually maintained histories of PR-body edits as progress.

* * *

## Required workflow

> **PR contract workflow:** The full contract creation workflow, required contents, and
> template are in the **Jules skill → PR Contract** section.
> That section is the authoritative source for Jules-initiated PRs.

For nontrivial non-Jules PRs, use the plan-to-issue-tree sequence first:

```bash
# Create or select the GitHub Milestone object for this delivery slice.
# State the subtree root or explicit issue set in the description.
gh api repos/<OWNER>/<REPO>/milestones -f title="<milestone>" -f state=open -f description="<issue-tree scope>"

# Create or update the roadmap/story node that owns this work.
gh issue create --title "<story-shaped outcome>" --body-file .pr/ISSUE_ROOT.md --label enhancement --milestone "<milestone>"

# Create child issues under the correct parent when native sub-issues are available.
gh issue create --title "<child story or implementation node>" --body-file .pr/ISSUE_<id>.md --label enhancement --milestone "<milestone>" --parent <PARENT_ISSUE_NUMBER>

# Attach existing issues as sub-issues when needed.
gh issue edit <PARENT_ISSUE_NUMBER> --add-sub-issue <CHILD_ISSUE_NUMBER>

# Encode blockers as dependencies, not as roadmap order.
gh issue edit <ISSUE_NUMBER> --add-blocked-by <BLOCKER_ISSUE_NUMBER>

# Verify tree placement and milestone scope before drafting the PR claim map.
gh issue view <PARENT_ISSUE_NUMBER> --json title,body,url,milestone
```

* * *

## Phase 1: TDD before implementation

The PR should be driven by failing checks written before the fix.

The point is not ceremony.
The point is to lock the target before implementation exists.

Required sequence:

1. Write failing test or verification artifact.

2. Confirm it fails for the intended reason.

3. Implement the narrowest change that should make it pass.

4. Re-run verification.

5. Record the result in the PR body.

### What counts as acceptable pre-implementation verification

- a failing automated test,

- a reproducible failing command,

- a failing integration check,

- a failing exact output comparison,

- a failing invariant check.

### What does not count

- informal intention,

- a TODO list,

- a verbal claim that the bug exists,

- a post-hoc explanation added after the code already passes,

- content-free checks like `is not None` or `len(x) > 0`.

### Minimal example

Bad sequence:

1. Write implementation.

2. Run tests.

3. Write PR description saying the feature now works.

Required sequence:

1. Add test showing the feature does not work.

2. Commit test or at least keep it in the branch as part of the work.

3. Implement the fix.

4. Show the exact same test now passes.

* * *

## Phase 2: Keep the diff causally legible

The PR must remain easy to evaluate against the contract.

### Rules

1. **No unrelated edits.** Do not rename nearby symbols, reformat unrelated files,
   update fixtures, or rewrite helpers unless they are required by the contract.

2. **No hidden goal substitution.** If the original goal becomes impossible or
   incorrect, update the PR contract explicitly before changing direction.

3. **No structural completion as substitute for functional completion.** Do not add
   scaffolding, registries, wrappers, or documentation to create the appearance of
   completeness while leaving the core behavior stubbed.

4. **No fake success via fallbacks.** Do not hide failures with defaults, silent
   recovery, or plausible fabricated data.

5. **Prefer deletion and reuse over additive layers.** If a wrapper, fallback, or custom
   implementation is not necessary, remove it.
   If a mature dependency already solves the problem, use it unless a listed constraint
   forbids that.

* * *

## Phase 3: Force the PR body to come from the contract file

> **See the Jules skill → PR Contract section** for Jules-specific contract mechanics.
> Still apply this skill's GitHub milestone, Development-link, draft-state, and
> re-publishing rules to Jules-created PRs.

* * *

## Phase 4: Read every review comment with `gh` or bundled tools, not selectively

A worker must not rely on memory, inbox summaries, or partial UI reading.
Review feedback is part of the task state.
It must be read exhaustively and tracked explicitly.

The worker must read:

1. the PR body as currently published,

2. issue-style PR comments,

3. formal reviews,

4. line-level review comments,

5. CI/check failures,

6. review decision state.

### Minimum command set

#### 1. Use the bundled CLI tool to read all feedback surfaces at once

The most robust way to gather all feedback is to use the `extract_unresolved_issues`
tool bundled with the git-guidelines skill:

```bash
uv run --directory ~/ai/opencode/skills/git-guidelines/scripts/extract_unresolved_issues -m extract_unresolved_issues summarize <OWNER>/<REPO>#<PR_NUMBER>
```

This will automatically fetch:

- Top-level PR comments

- Inline code review threads

- Automated check-run errors

#### 2. Inspect structured PR state manually (fallback)

```bash
gh pr view <PR_NUMBER> \
  --json title,body,reviewDecision,latestReviews,reviews,comments,files,statusCheckRollup
```

This should be treated as the baseline state snapshot.

#### 3. Read CI/check status until it settles

```bash
gh pr checks <PR_NUMBER> --watch
```

For machine-readable inspection:

```bash
gh pr checks <PR_NUMBER> --json name,state,bucket,link
```

#### Automated Check Runs

Automated checks can post annotations surfaced via GitHub’s API. Treat GitHub check
state and the linked check details as the current authority for that check.

**Read check status:**

```bash
# List check runs for the PR head commit
gh api repos/<OWNER>/<REPO>/commits/<HEAD_SHA>/check-runs

# Extract annotations from a specific check run
gh api repos/<OWNER>/<REPO>/check-runs/<CHECK_RUN_ID>/annotations
```

Each annotation includes `message`, `path`, `start_line`, `annotation_level`, and a
`details_url` pointing to the check’s detailed report when the provider exposes one.

#### 4. Read formal review objects in chronological order

```bash
gh api repos/<OWNER>/<REPO>/pulls/<PR_NUMBER>/reviews
```

#### 5. Read line-level review comments on the diff

```bash
gh api repos/<OWNER>/<REPO>/pulls/<PR_NUMBER>/comments
```

#### 6. Read issue-style PR comments

```bash
gh api repos/<OWNER>/<REPO>/issues/<PR_NUMBER>/comments
```

These are distinct surfaces.
A worker that reads only one of them will miss actionable feedback.

* * *

## Required review-log discipline

Every actionable review item must be copied into a tracked log file.

Create:

```bash
$EDITOR .pr/REVIEW_LOG.md
```

### Required fields for each item

```markdown
## Review item <N>

- Source: <review / review-comment / issue-comment / CI>
- URL or identifier: <link or id>
- Reviewer:
- File/line:
- Exact actionable request:
- Worker interpretation:
- Planned action:
- Status: open | addressed | rejected-with-rationale
- Commit addressing it:
- Notes:
```

### Hard rules

1. **No silent ignoring.** Every actionable item must appear in the log.

2. **No bundling multiple requests into vague summaries.** Preserve atomicity.

3. **No “addressed” without a commit.**

4. **No rejection without explicit rationale tied to the PR contract.**

5. **If a review item reveals that the contract is wrong, update the contract first.**

This is necessary because agentic workers often continue from their prior frame and
treat review feedback as advisory decoration.
The log must force integration of each item into the task state.

* * *

## Phase 5: Respond to feedback by updating the contract, code, or both

Feedback should be handled through one of only three legal moves.

### Move A: The reviewer found a real defect within the existing contract

Action:

- update code/tests,

- update evidence,

- mark the review item addressed.

### Move B: The reviewer exposed missing or weak acceptance criteria

Action:

- strengthen the contract file,

- add or revise tests first if needed,

- then update code.

### Move C: The reviewer identified that the contract itself is wrong

Action:

- revise the contract file explicitly,

- commit that revision,

- then proceed with implementation changes.

### Illegal move

- silently keep the same implementation direction while merely adding a local
  constraint,

- say “addressed” without changing the contract or the code appropriately,

- reinterpret the reviewer’s feedback into something easier and solve that instead.

* * *

## Example of proper feedback integration

Reviewer comment:

> This test only checks that a value is returned.
> It would pass on arbitrary non-empty junk.

Incorrect response pattern:

- add another `isinstance(...)` check,

- reply “done,”

- leave acceptance criteria unchanged.

Required response pattern:

1. add the review item to `.pr/REVIEW_LOG.md`,

2. update the contract file so the acceptance criterion names the exact invariant or
   exact value to be proven,

3. replace the weak test with a substantive one,

4. commit,

5. cite the commit when marking the item addressed.

* * *

## Phase 6: Keep reviewers anchored to outcome, not process theater

The PR should make it easy for reviewers to reject process-shaped nonsense.

### Include a dedicated “Review focus” section

At the end of the contract file, ask reviewers to check:

- whether the intended outcome is the right one,

- whether any acceptance criterion is missing, tautological, or implementation-defined,

- whether any file in the diff falls outside the declared boundary,

- whether any test would pass on plausible junk,

- whether any fallback hides failure instead of surfacing it,

- whether the code satisfies the problem or merely looks complete.

This materially improves reviewer alignment because it keeps the PR anchored to external
success criteria defined before implementation.

* * *

## Patterns workers must actively avoid

### 1. Post-hoc PR narration

Writing the body after the code and then describing what now exists as if it were the
intended target from the start.

### 2. Completion criteria drift

Changing “done” to mean whatever the current code already satisfies.

### 3. Structural completion as surrogate

Submitting scaffolding, docs, wrappers, registrations, and passing trivial tests while
the core outcome is still missing.

### 4. Review-skimming

Reading only the top-level review decision or only the web summary and missing
line-level or issue-level comments.

### 5. Silent partial compliance

Addressing only the easiest fragment of a review item and marking the whole item
resolved.

### 6. Constraint accumulation without frame change

A correction implies “abandon this direction,” but the worker instead adds a local patch
and keeps the original wrong direction.

### 7. Evidence laundering

Replacing real proof with broad claims such as “tested thoroughly,” “handled edge
cases,” or “improved reliability.”

### 8. Reviewer burden shifting

Leaving reviewers to reconstruct the original goal, infer missing constraints, or detect
whether the tests are tautological.

* * *

## Minimal shell workflow

A practical sequence:

```bash
# 0. externalize the finalized plan into a GitHub issue tree and milestone scope
mkdir -p .pr
$EDITOR .pr/ISSUE_ROOT.md
$EDITOR .pr/ISSUE_F1.md
$EDITOR .pr/ISSUE_W1.md
# Create the milestone if it does not already exist.
gh api repos/<OWNER>/<REPO>/milestones -f title="<milestone>" -f state=open -f description="<issue-tree scope>"
gh issue create --title "<story-shaped outcome>" --body-file .pr/ISSUE_ROOT.md --label enhancement --milestone "<milestone>"
gh issue create --title "<foundation>" --body-file .pr/ISSUE_F1.md --label enhancement --milestone "<milestone>" --parent <ISSUE_ROOT_NUMBER>
gh issue create --title "<workstream>" --body-file .pr/ISSUE_W1.md --label enhancement --milestone "<milestone>" --parent <ISSUE_ROOT_NUMBER>
# Attach existing issues as sub-issues when needed, and encode blockers separately.
gh issue edit <ISSUE_ROOT_NUMBER> --add-sub-issue <CHILD_ISSUE_NUMBER>
gh issue edit <ISSUE_W1_NUMBER> --add-blocked-by <ISSUE_F1_NUMBER>

# 1. create tracked PR claim map from the selected issue set before implementation
$EDITOR .pr/PR_BODY.md   # include Closes only for full claims; use Refs for parents/partials/deferred work
$EDITOR .pr/REVIEW_LOG.md

# 2. commit contract early
git add .pr/PR_BODY.md .pr/REVIEW_LOG.md
git commit -m "Add PR contract and review log"

# 3. create draft PR from the tracked issue-linked claim map before implementation
gh pr create --title "<title>" --body-file .pr/PR_BODY.md --milestone "<milestone>" --draft

gh pr view <PR_NUMBER> --json title,body,milestone,closingIssuesReferences,isDraft

# 4. write failing tests / failing verification
pytest path/to/test_file.py -q

# 5. implement narrowly and re-run verification
pytest path/to/test_file.py -q

# 6. keep the PR draft while claimed issue/proof work remains open
# Republish .pr/PR_BODY.md as the claim map changes.
gh pr edit <PR_NUMBER> --body-file .pr/PR_BODY.md --milestone "<milestone>"

# Only after every claimed item is complete and evidenced:
gh pr ready <PR_NUMBER>

# 7. after review arrives, read all feedback surfaces
gh pr view <PR_NUMBER> --comments
gh pr view <PR_NUMBER> --json title,body,milestone,closingIssuesReferences,isDraft,reviewDecision,latestReviews,reviews,comments,files,statusCheckRollup
gh api repos/<OWNER>/<REPO>/pulls/<PR_NUMBER>/reviews
gh api repos/<OWNER>/<REPO>/pulls/<PR_NUMBER>/comments
gh api repos/<OWNER>/<REPO>/issues/<PR_NUMBER>/comments
gh pr checks <PR_NUMBER> --watch

# 8. if review feedback reopens required claim work, return to draft before continuing
gh pr ready <PR_NUMBER> --undo

# Update the issue tree and contract file if needed
$EDITOR .pr/ISSUE_ROOT.md
$EDITOR .pr/ISSUE_F1.md
$EDITOR .pr/PR_BODY.md
$EDITOR .pr/REVIEW_LOG.md

git add .pr/PR_BODY.md .pr/REVIEW_LOG.md <changed code/tests>
git commit -m "Address review feedback"

# 9. republish PR body from the tracked contract
gh pr edit <PR_NUMBER> --body-file .pr/PR_BODY.md --milestone "<milestone>"

# 10. after reopened claim work is complete and evidenced, mark ready again
gh pr ready <PR_NUMBER>
```

* * *

## What reviewers should be able to see immediately

A well-prepared PR should let a reviewer answer these questions in under a minute:

1. What exact outcome is this PR trying to achieve?

2. What counts as success?

3. What is not being changed?

4. What evidence proves the behavior now holds?

5. Which review items remain open?

6. Which ones were addressed in which commits?

If the PR does not expose those answers directly, it is not review-ready.

* * *

## Final rule set

1. Finalize the plan before externalization.

2. Externalize the finalized plan into a GitHub issue tree and GitHub Milestone scope.

3. Assign descendant delivery issues and linked PRs to that GitHub Milestone.

4. Write the PR contract/body before implementation.

5. Add closing-keyword Development links only for issues the PR fully satisfies on merge.

6. Use `Refs` or prose, not closing keywords, for parent issues, partial claims,
   deferred work, future work, and out-of-scope issues.

7. Link nontrivial top-level PR claim items to the owning issues.

8. Keep deferred, excluded, future, and out-of-scope work out of PR checkboxes.

9. Keep the PR draft until every claimed issue and proof obligation is complete and evidenced.

10. Derive the PR body from the tracked contract file, issue tree, and claim map, not
    from memory or the web form.

11. Lock acceptance criteria before code exists.

12. Use failing verification first.

13. Keep the diff within the declared boundary.

14. Read every review surface with `gh`.

15. Log every actionable review item atomically.

16. Do not mark feedback addressed without an identifying commit.

17. If feedback changes the target, update the issue tree, milestone scope, and claim map first.

18. Do not let the implementation define its own success criteria.

19. Do not let a reviewer guess what "done" means.

A PR that follows these rules is much easier to review well, much harder to rubber-stamp
for the wrong reasons, and much less likely to drift into post-hoc self-justifying
completion theater.
