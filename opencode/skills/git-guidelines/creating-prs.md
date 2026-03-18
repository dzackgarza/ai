# PR Worker Guide: How to Submit Work That Produces High-Quality Review Feedback

## Purpose

This guide is for PR workers, including agentic coding systems and human contributors using LLM assistance. Its purpose is not to optimize for "getting approved." Its purpose is to make the work legible, falsifiable, and reviewable, so that reviewer feedback is anchored to the actual intended outcome rather than to a post-hoc story constructed after the code already exists.

The main failure to prevent is this:

* code is written first,
* completion criteria are inferred from the resulting code,
* the PR description is retrofitted to match what now exists,
* reviewers evaluate against those retrofitted criteria,
* the result is a tautologous thumbs-up on work that may not meet the original need.

This guide therefore imposes one hard rule:

## Hard rule

**The PR contract must be written before implementation, committed to the branch, and used as the source of truth for the PR body.**

Do not let the code define the task after the fact.

---

## Core principle

A review is only as good as the target it is reviewing against.

If the intended outcome is underspecified, or if the worker allows the implementation to define its own success criteria after the fact, reviewers are forced into local or stylistic review. They can comment on naming, tests, structure, and plausibility, but they cannot reliably say whether the change meets the actual need.

The worker must therefore supply, in advance:

1. the intended outcome,
2. the non-goals,
3. the acceptance criteria,
4. the specific evidence that will count as success,
5. the boundaries of the change,
6. the exact unresolved questions, if any.

That is what enables strong process-alignment feedback.

---

## Required workflow

## Phase 0: Create the PR contract before writing code

Before touching implementation, create a tracked file in the branch. Put it somewhere stable and obvious, for example:

```bash
mkdir -p .pr
$EDITOR .pr/PR_BODY.md
```

This file must be committed before substantive implementation begins.

Recommended companion files:

```text
.pr/
  PR_BODY.md
  REVIEW_LOG.md
  ACCEPTANCE_CHECKS.md
```

### Required contents of `.pr/PR_BODY.md`

This file is the contract. It should be written in plain, direct language and should include these sections.

#### 1. Problem statement

What exact failure, missing capability, or requirement is being addressed?

#### 2. Intended outcome

What must be true after this PR lands?

This must be phrased as externally checkable behavior, not as implementation structure.

Bad:

* Adds a new abstraction for report generation.

Better:

* Generating report X from input Y produces fields A, B, C with exact semantics Z.

#### 3. Non-goals

What is explicitly not being changed?

This protects against scope explosion and collateral edits.

#### 4. Constraints

List all binding constraints up front.

Examples:

* exact arithmetic, not approximate
* no mocks in tests
* preserve existing API
* no new dependencies
* no config-schema changes
* output must remain stable for downstream consumer Z

#### 5. Acceptance criteria

These must be concrete, observable, and falsifiable.

Bad:

* Tests added
* Handles edge cases
* Improves reliability

Better:

* `compute_discriminant(L)` returns `-23` on the canonical fixture lattice
* watch mode no longer rebuilds when only the output directory changes
* invalid input raises `TypeError`
* existing command-line interface remains byte-for-byte unchanged on baseline fixture set

#### 6. Evidence plan

State exactly what evidence will be provided in the PR.

Examples:

* failing test first, then passing test
* command output from real run on fixture X
* diff proving no changes outside listed paths
* benchmark numbers on the specified dataset

#### 7. Change boundary

List the files or subsystems expected to change.

This gives reviewers a prior on what collateral damage to reject.

#### 8. Open questions

If anything remains unresolved, list it explicitly instead of silently substituting your own answer.

---

## Phase 1: TDD before implementation

The PR should be driven by failing checks written before the fix.

The point is not ceremony. The point is to lock the target before implementation exists.

Required sequence:

1. Write failing test or verification artifact.
2. Confirm it fails for the intended reason.
3. Implement the narrowest change that should make it pass.
4. Re-run verification.
5. Record the result in the PR body.

### What counts as acceptable pre-implementation verification

* a failing automated test,
* a reproducible failing command,
* a failing integration check,
* a failing exact output comparison,
* a failing invariant check.

### What does not count

* informal intention,
* a TODO list,
* a verbal claim that the bug exists,
* a post-hoc explanation added after the code already passes,
* content-free checks like `is not None` or `len(x) > 0`.

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

---

## Phase 2: Keep the diff causally legible

The PR must remain easy to evaluate against the contract.

### Rules

1. **No unrelated edits.**
   Do not rename nearby symbols, reformat unrelated files, update fixtures, or rewrite helpers unless they are required by the contract.

2. **No hidden goal substitution.**
   If the original goal becomes impossible or incorrect, update the PR contract explicitly before changing direction.

3. **No structural completion as substitute for functional completion.**
   Do not add scaffolding, registries, wrappers, or documentation to create the appearance of completeness while leaving the core behavior stubbed.

4. **No fake success via fallbacks.**
   Do not hide failures with defaults, silent recovery, or plausible fabricated data.

5. **Prefer deletion and reuse over additive layers.**
   If a wrapper, fallback, or custom implementation is not necessary, remove it. If a mature dependency already solves the problem, use it unless a listed constraint forbids that.

---

## Phase 3: Force the PR body to come from the contract file

Do not type the PR body interactively. Use the tracked file.

Create the PR with:

```bash
gh pr create \
  --title "<concise outcome-focused title>" \
  --body-file .pr/PR_BODY.md \
  --draft
```

If the PR already exists, update it from the same file:

```bash
gh pr edit <PR_NUMBER> --body-file .pr/PR_BODY.md
```

This prevents silent drift between the reviewed artifact and the stated contract.

### Rule

Every time acceptance criteria, scope, or evidence changes, update `.pr/PR_BODY.md`, commit it, and re-publish the PR body from that file.

The PR description is not a summary written after the work. It is a tracked interface between worker and reviewer.

---

## Suggested PR body template

Use this structure in `.pr/PR_BODY.md`.

```markdown
# Problem

<exact failure / missing capability / requirement>

# Intended outcome

<observable post-merge behavior>

# Non-goals

- ...
- ...

# Constraints

- ...
- ...

# Acceptance criteria

- [ ] ...
- [ ] ...
- [ ] ...

# Evidence plan

- failing test / command:
- passing test / command:
- end-to-end check:

# Change boundary

Expected touched files / subsystems:
- ...
- ...

# Open questions

- ...

# Review focus

Please check specifically:
- whether the acceptance criteria are sufficient,
- whether any goal has been swapped or relaxed,
- whether any changed file falls outside the declared boundary,
- whether verification would still pass on plausible junk output.
```

---

## Phase 4: Read every review comment with `gh`, not selectively

A worker must not rely on memory, inbox summaries, or partial UI reading. Review feedback is part of the task state. It must be read exhaustively and tracked explicitly.

The worker must read:

1. the PR body as currently published,
2. issue-style PR comments,
3. formal reviews,
4. line-level review comments,
5. CI/check failures,
6. review decision state.

### Minimum command set

#### 1. Read the PR and comments in terminal

```bash
gh pr view <PR_NUMBER> --comments
```

#### 2. Inspect structured PR state

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

These are distinct surfaces. A worker that reads only one of them will miss actionable feedback.

---

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

This is necessary because agentic workers often continue from their prior frame and treat review feedback as advisory decoration. The log must force integration of each item into the task state.

---

## Phase 5: Respond to feedback by updating the contract, code, or both

Feedback should be handled through one of only three legal moves.

### Move A: The reviewer found a real defect within the existing contract

Action:

* update code/tests,
* update evidence,
* mark the review item addressed.

### Move B: The reviewer exposed missing or weak acceptance criteria

Action:

* strengthen `.pr/PR_BODY.md`,
* add or revise tests first if needed,
* then update code.

### Move C: The reviewer identified that the contract itself is wrong

Action:

* revise `.pr/PR_BODY.md` explicitly,
* commit that revision,
* then proceed with implementation changes.

### Illegal move

* silently keep the same implementation direction while merely adding a local constraint,
* say “addressed” without changing the contract or the code appropriately,
* reinterpret the reviewer’s feedback into something easier and solve that instead.

---

## Example of proper feedback integration

Reviewer comment:

> This test only checks that a value is returned. It would pass on arbitrary non-empty junk.

Incorrect response pattern:

* add another `isinstance(...)` check,
* reply “done,”
* leave acceptance criteria unchanged.

Required response pattern:

1. add the review item to `.pr/REVIEW_LOG.md`,
2. update `.pr/PR_BODY.md` so the acceptance criterion names the exact invariant or exact value to be proven,
3. replace the weak test with a substantive one,
4. commit,
5. cite the commit when marking the item addressed.

---

## Phase 6: Keep reviewers anchored to outcome, not process theater

The PR should make it easy for reviewers to reject process-shaped nonsense.

### Include a dedicated “Review focus” section

At the end of `.pr/PR_BODY.md`, ask reviewers to check:

* whether the intended outcome is the right one,
* whether any acceptance criterion is missing, tautological, or implementation-defined,
* whether any file in the diff falls outside the declared boundary,
* whether any test would pass on plausible junk,
* whether any fallback hides failure instead of surfacing it,
* whether the code satisfies the problem or merely looks complete.

This materially improves reviewer alignment because it keeps the PR anchored to external success criteria defined before implementation.

---

## Patterns workers must actively avoid

### 1. Post-hoc PR narration

Writing the body after the code and then describing what now exists as if it were the intended target from the start.

### 2. Completion criteria drift

Changing “done” to mean whatever the current code already satisfies.

### 3. Structural completion as surrogate

Submitting scaffolding, docs, wrappers, registrations, and passing trivial tests while the core outcome is still missing.

### 4. Review-skimming

Reading only the top-level review decision or only the web summary and missing line-level or issue-level comments.

### 5. Silent partial compliance

Addressing only the easiest fragment of a review item and marking the whole item resolved.

### 6. Constraint accumulation without frame change

A correction implies “abandon this direction,” but the worker instead adds a local patch and keeps the original wrong direction.

### 7. Evidence laundering

Replacing real proof with broad claims such as “tested thoroughly,” “handled edge cases,” or “improved reliability.”

### 8. Reviewer burden shifting

Leaving reviewers to reconstruct the original goal, infer missing constraints, or detect whether the tests are tautological.

---

## Minimal shell workflow

A practical sequence:

```bash
# 0. create tracked PR contract before implementation
mkdir -p .pr
$EDITOR .pr/PR_BODY.md
$EDITOR .pr/REVIEW_LOG.md

# 1. commit contract early
git add .pr/PR_BODY.md .pr/REVIEW_LOG.md
git commit -m "Add PR contract and review log"

# 2. write failing tests / failing verification
pytest path/to/test_file.py -q

# 3. implement narrowly and re-run verification
pytest path/to/test_file.py -q

# 4. create draft PR from the tracked contract
gh pr create --title "<title>" --body-file .pr/PR_BODY.md --draft

# 5. after review arrives, read all feedback surfaces
gh pr view <PR_NUMBER> --comments
gh pr view <PR_NUMBER> --json title,body,reviewDecision,latestReviews,reviews,comments,files,statusCheckRollup
gh api repos/<OWNER>/<REPO>/pulls/<PR_NUMBER>/reviews
gh api repos/<OWNER>/<REPO>/pulls/<PR_NUMBER>/comments
gh api repos/<OWNER>/<REPO>/issues/<PR_NUMBER>/comments
gh pr checks <PR_NUMBER> --watch

# 6. update the contract file if needed
$EDITOR .pr/PR_BODY.md
$EDITOR .pr/REVIEW_LOG.md

git add .pr/PR_BODY.md .pr/REVIEW_LOG.md <changed code/tests>
git commit -m "Address review feedback"

# 7. republish PR body from the tracked contract
gh pr edit <PR_NUMBER> --body-file .pr/PR_BODY.md
```

---

## What reviewers should be able to see immediately

A well-prepared PR should let a reviewer answer these questions in under a minute:

1. What exact outcome is this PR trying to achieve?
2. What counts as success?
3. What is not being changed?
4. What evidence proves the behavior now holds?
5. Which review items remain open?
6. Which ones were addressed in which commits?

If the PR does not expose those answers directly, it is not review-ready.

---

## Final rule set

1. Write the PR contract before implementation.
2. Commit it to the branch.
3. Derive the PR body from that file, not from memory or the web form.
4. Lock acceptance criteria before code exists.
5. Use failing verification first.
6. Keep the diff within the declared boundary.
7. Read every review surface with `gh`.
8. Log every actionable review item atomically.
9. Do not mark feedback addressed without an identifying commit.
10. If feedback changes the target, update the contract first.
11. Do not let the implementation define its own success criteria.
12. Do not let a reviewer guess what “done” means.

A PR that follows these rules is much easier to review well, much harder to rubber-stamp for the wrong reasons, and much less likely to drift into post-hoc self-justifying completion theater.

