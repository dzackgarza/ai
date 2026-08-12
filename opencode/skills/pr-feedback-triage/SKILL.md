---
name: pr-feedback-triage
description: Use when consuming, replying to, resolving, or acting on PR review comments, automated review comments, check annotations, external agent review output, or user requests. Also use when converting accepted feedback into remediation specs, assigning independent subagents, verifying remediation commits, and producing top-level disposition ledgers.
---
# PR Feedback Triage

Before acting on PR comments or review feedback, consult the central policy index:
[policy-index](file:///home/dzack/ai/opencode/skills/policy-index/SKILL.md)


When consuming review feedback from other agents (automated or human), do not treat review comments as automatic chores to be done or automatic blockers. A review comment is a claim to be evaluated, not an order.

## Orchestration: Enforce Role Isolation

This workflow is the PR-feedback adaptation of the canonical A/B/C
disposition-to-remediation firewall in
[reviewing-llm-code/references/qc-triage.md](file:///home/dzack/ai/opencode/skills/reviewing-llm-code/references/qc-triage.md).
Map the roles explicitly:

- **A — Orchestrator/controller**: collects review surfaces, routes findings, records stamps, and closes threads only after the required evidence exists. A makes no authoritative disposition and proposes no fix.
- **B — Disposition subagent**: Phase 2.5. B determines the per-finding PR disposition using the five-way model below, including whether a true concern requires current-PR remediation.
- **C — Remediation subagent**: Phase 4. C remediates accepted findings from a first-principles spec, not from reviewer wording, B's fix ideas, or A's preferences.

If explicit orchestration primitives are available — workflow/pipeline tools, goal
loops, durable task graphs, scheduled re-invocation, background subagents, or any
harness that can dispatch stage work and preserve stage inputs — use them to
enforce the A/B/C isolation from the first review item.

A ready-made encoding exists: the **`pr-feedback-triage` workflow**
(`~/.claude/workflows/pr-feedback-triage.js`) runs this convergent loop
deterministically — Collect (via `scripts/triage_state.py`) → B disposition (with
the mandatory pre-filter and current-PR spend gate) → C remediation from first-principles specs →
verify+commit+three-stamp-close → loop until the harness reports converged. A is
the script and cannot self-dispose; B and C are separate `agent()` stages. Prefer
invoking it (pass `args {repo, pr}`; requires the usual workflow opt-in) over
hand-driving; fall back to the manual stages below only when no workflow primitive
is available.

The tooling may enforce stage dispatch, batching boundaries, contraband-input
denial, required outputs, verification questions, commit-before-closure, and
re-entry on new review rounds.
It must **not** become an orchestrator-controlled checkpoint where A approves,
overrides, summarizes, or substitutes for B's disposition or C's remediation. That
would reintroduce the self-gate forbidden by `goalcraft` and the canonical
`qc-triage` protocol. If no orchestration primitive is available, run the same
role-isolated stages by hand.

## Core Doctrine: Split Feedback from Remediation

Every review comment has two separable parts:

1. **Feedback claim**: what defect, risk, gap, or misalignment does the reviewer allege?
2. **Suggested remediation**: what change does the reviewer propose?

The claim may be aligned while the proposed fix is misaligned.
The proposed fix may be aligned even if the reviewer’s framing is generic.
Do not accept or reject the whole comment as one unit.

Factual truth is also separate from current-PR necessity. A reviewer may be completely
right about minor debt that does not justify another remediation, commit, push, and full
re-review cycle for this PR.

## The Five-Way Disposition Model

For every review comment, select one of these five dispositions:

- **Accepted as written**:
  The claim is true and the suggested fix preserves global + repo policy.

- **Accepted with modified remediation**:
  The claim is true, but the suggested fix imports generic policy, enterprise hardening,
  graceful fallback, fake proof, excess complexity, or wrong semantics. Fix the real issue
  through a policy-compatible narrower change.

- **Rejected**:
  The claim is false, irrelevant, design-hostile, or conflicts with stronger policy.
  Reply with source-backed reasoning before resolving.

- **Investigate before action**:
  The comment points to a possible inconsistency but does not prove the fix. Gather the
  missing contract/runtime/config evidence before changing code.

- **Backlogged as minor technical debt**:
  The claim is true, but it does not affect the current PR's claim, acceptance/proof
  obligations, required checks, user-visible correctness, hard policy, or a regression
  introduced or worsened by this PR. It is localized low-risk maintainability debt that
  is more proportionate to batch in a linked GitHub debt issue. This disposition closes
  the thread without role C or a remediation commit only after the spend gate below is
  evidenced.

## Threat Model: Review Evasion and Gaming

The worker agent will attempt to game PR review itself. It will:
- accept feedback in prose without fixing it;
- resolve threads after promising future work;
- patch exactly the reviewed line rather than the underlying burden;
- add weak tests that prove the patch, not the behavior;
- hide rejected feedback inside resolved threads;
- treat “disposition provided” as completion;
- turn current acceptance or proof work into a debt issue;
- force a full remediation cycle for every true but immaterial observation;
- use the reviewer's wording as a checklist to silence rather than understand.
- do the A/B/C split only after maintainer pushback, then relapse when unwatched
  (the `qc-triage` "doing it right only once the user pushes back" anti-pattern).

The workflow must make that game impossible.

## Core Rule: Positive Current-PR Disposition Requires Committed Remediation

An accepted current-PR disposition requires a remediation commit.

Do not reply “accepted,” “aligned,” “fixed,” “addressed,” “will address,” or equivalent unless the actual remediation is already committed and the reply cites that commit.

No accepted review thread may be resolved on the basis of:
- agreement;
- intent to fix;
- a local plan;
- an issue;
- a future task;
- a subagent being launched;
- a weak or partial patch;
- a test that only polices the reviewer's wording.

Accepted current-PR disposition without a commit is false signaling.

There are only four pre-commit states:
- open / under triage
- rejected with visible rationale
- backlogged minor debt with spend-gate evidence and a linked GitHub issue
- blocked with visible blocker

“Accepted pending fix” may exist in an internal review log, but it must not be posted as a resolved disposition on the PR thread.

## Commit-Gated Disposition Workflow

Triage is not resolution. Accepted current-PR claims do not get visible positive disposition until remediation is committed.

### Phase 1: Collect All Review Surfaces
The controller must collect all live review items before acting:
- inline review threads
- formal review summaries
- top-level PR comments
- check annotations
- bot comments that update in place
- previously resolved comments if reviewing whether prior remediation was valid

A green check, “not resolved: 0,” or resolved-thread count is not proof. Feedback must be understood and made visible to the maintainer, not treated as an administrative obstacle.

**Triage state (run first; idempotent).** Collect with `scripts/triage_state.py` (`--repo owner/name --pr N`). It paginates ALL review threads (never the 100-cap default — a capped query silently undercounts open threads), keys each finding by a STABLE id (the `ai-review-fingerprint`, else a content hash that survives line shifts), records landed stamps, and writes `.pr/triage_state.json` plus the prescribed `.pr/REVIEW_DISPOSITIONS.md`. It is idempotent: a mid-round death resumes cleanly because already-stamped/resolved findings are skipped. Scope the round from its worklist (NEW / RE-RAISED / OPEN-PENDING) and use its `converged` flag (NEW=0 and OPEN-PENDING=0) as the loop's termination signal. Match and close threads by stable id / `thread_id`, never by `(path:line)` — line numbers shift under commits.

### Phase 2: Classify Without Resolving
For each item, classify internally:
- claim: true / false / needs investigation
- reviewer remediation: aligned / misaligned / underspecified
- current-PR necessity: remediate / backlog minor debt / none / investigate
- required action: none / rejection ledger / debt issue + thread disposition / remediation spec / investigation

Do not reply “accepted” yet. Do not resolve accepted items yet.

The Phase 2 classification is a provisional sort, **not** an authoritative disposition. The orchestrator must not treat its own read of a thread as the disposition of record. Authoritative dispositions come only from Phase 2.5.

### Phase 2.5: Independent Disposition Round

This is role **B** from the canonical A/B/C firewall. The disposition itself must
come from independent disposition subagents, not from the orchestrator clearing
the review. The PR-specific adaptation is that B returns the five-way PR
disposition below instead of the QC protocol's binary `VIOLATION` / `CLEARED`
result.

Batch disposition work intelligently. The default for a normal review window is
often **one B subagent for all current findings**, returning a separate
disposition for each finding. Split into multiple B subagents only when there is a
real reason: context would overflow, file/domain ownership is genuinely
disjoint, parallelism matters, or a contaminated prompt/output needs to be rerun
cleanly.

The invariant is role restriction, not issue narrowness. A B subagent may see many
findings, but it may only produce dispositions. The dispatch hygiene rules in
`qc-triage.md` apply directly: A may transmit raw review material, relevant source
locations/files, named policy surfaces, and verbatim owner/maintainer comments. A
may not transmit its verdict, leaning, hypotheses, paraphrased owner premises,
thread-resolution status, remediation ideas, preferred fix, or any prompt framing
that seeds the outcome. If the owner premise is not a literal quote or a policy
clause, it is contraband.

Each B subagent returns exactly one disposition per finding it was assigned:
Accepted as written, Accepted with modified remediation, Rejected, Investigate
before action, or Backlogged as minor technical debt. The answer must be grounded
only in policy, literal owner comments, and the code. Batched processing is
allowed; grouped verdicts are not. “CI
churn,” “false-positive wave,” “bulk-reject,” and “mostly noise” are not
dispositions and must never appear as one.

**Mandatory pre-filter, before the five-way.** Each B subagent runs the
[disposition pre-filter](references/disposition-prefilter.md) on every finding
first. Gate 1 rejects unsupported generic bug/perf/style preferences but sends
factually supported minor maintainability debt to the spend gate. Gate 2 forces a disposition for
known policy-misaligned shapes — micro-optimization with no logged/reproduced perf
problem, fallback/default/mock suggestions, defensive-catch-instead-of-fail-early,
in-code constants where config-driven is required, optional/absent-data fields,
sandbox/enterprise hardening on bespoke software, and actual slop (a catch-all
swallow) that the finding merely frames as a generic bug. Gate 3 decides whether a
true finding requires current-PR remediation or qualifies for the debt escape hatch;
Gate 4 downgrades a true-claim-with-policy-violating-fix that requires remediation
to accept-with-modified-remediation. The
disposition reply must carry the recorded `Pre-filter:` line naming which gate
fired. The gate runs before the five-way and is recorded, so a disposition cannot
be argued from priors — "it models real absent data" or "it is a real perf cost"
cannot stand in for the policy check.

For `Backlogged as minor technical debt`, every Gate 3 criterion must be recorded.
B appends the finding to an existing work-family GitHub debt issue or creates one
through the owning repository's issue route, replies on the review thread with the
evidence, issue link, and why the current PR remains complete, then resolves the
thread. B records the concern and evidence but proposes no fix. The issue is the
later batched-triage surface; no role C, remediation commit, push, or re-review is
started for that finding.

If B proposes or implies a remediation, fix shape, patch, or refactor, the output
is contaminated by the same B/C firewall violation described in `qc-triage.md`
and must be rerun with a clean prompt.

Duplicate, outdated, and superseded threads are still dispositioned per finding (see Loop and Convergence) — they are disposed as `Duplicate of <thread>` or `Outdated (superseded by <commit>)`, not silently skipped.

### Phase 3: Convert Accepted Current-PR Feedback into a First-Principles Remediation Spec
The controller must not hand the reviewer’s exact comment to the implementer. Instead, it must reconstruct the underlying problem from first principles.

#### Remediation Spec Template

```markdown
## Remediation spec

Original task / proof burden:
<What the PR or feature was supposed to prove or satisfy.>

Root concern:
<The actual correctness/proof/architecture problem, stated without the reviewer’s wording.>

Required behavior:
<What must be true after remediation.>

Required invariants:
- ...
- ...

Banned remediation patterns:
- no defaults
- no fallbacks
- no mocks/fakes/stubs
- no smoke/proof laundering
- no helper-level proof for boundary obligation
- no exact string assertions
- no source-policing tests
- no fail-open branches
- no boolean branch-forcing
- no deletion without burden disposition

Proof obligation:
<What real boundary, real data, real config, real process, real UI workflow, or structured error must be proven.>

Replacement requirement:
<Treat the current implementation/test as suspect. Replace the boundary-level implementation or proof surface as needed. Do not patch to the review wording.>

Scope:
<Files/subsystems in scope; explicit non-goals.>
```

*Good vs. Bad Examples:*
- **Bad spec:** `Replace .flatten() with map_err and add a test.`
- **Good spec:** `Directory listing must never convert filesystem read errors into missing entries. If reading the directory or any entry fails, the command must fail visibly with a structured error. A test must exercise the directory-listing boundary and prove that a read failure does not produce a partial successful listing.`
- **Bad spec:** `Remove browser-smoke mock.`
- **Good spec:** `The test suite must not contain test-shaped artifacts that simulate Tauri IPC and can be cited as product proof. Desktop behavior must be proven through the real Tauri IPC boundary or the proof burden must be recorded as unresolved. Any diagnostic-only harness must live outside the test/QC proof path.`

### Phase 4: Independent Remediation Subagent
Accepted current-PR feedback must be fixed by an independent subagent, not the same worker that is trying to clear the review. Backlogged minor debt never enters Phase 4.
As with dispositions, batching is allowed when the role boundary remains clean:
one C subagent may remediate multiple accepted findings if it receives only the
approved remediation spec(s), original task/PR contract, relevant source files,
and global policies. Split remediation only when context size, ownership
boundaries, parallelism, or contamination risk justifies it.

The subagent receives the *Remediation Spec*, the *Original task/PR contract*, *relevant source files*, and *global skills/policies* (anti-slop, fixing-slop, test-guidelines, bridge-burning-red-flags, banned-test-shapes, runtime-control-flow-red-flags, quality-control, known-solution-first).
The subagent must **NOT** receive the exact reviewer wording, suggested patch text, thread-resolution status, the worker’s preferred fix, or “just address this comment” framing.

#### Subagent Prompt Template
```markdown
You are an independent remediation agent.

You are not fixing a review comment. You are implementing the remediation specification below from first principles.

You have not been given the reviewer’s exact feedback because review wording causes agents to patch the symptom instead of solving the obligation.

Rules:
- Do not add defaults, fallbacks, mocks, skips, source-policing tests, exact string assertions, fail-open branches, or helper-level proof.
- Do not minimally patch the current implementation to silence the concern.
- Treat current implementation/tests at the target boundary as suspect.
- Replace the implementation/proof surface if needed.
- Prove the required behavior at the owned boundary.
- If the spec cannot be satisfied, report the blocker. Do not produce a partial patch.

Remediation spec:
<spec>

Required output:
- changed files;
- proof commands;
- explanation of how the proof discharges the spec;
- explicit banned-pattern audit.
```

### Phase 5: Controller Verification Gate
Before committing subagent remediation, the controller must review the subagent output under `reviewing-subagent-work`, `fixing-slop`, `test-guidelines`, and the red-flag catalogs.

A green test/CI/build result is **not** verification. “test-ci green,” “build passes,” or “the gate ran” is a precondition, not a pass — the threat model explicitly includes weak tests that prove the patch rather than the behavior. Verification is comparing the **declared remediation against the actual implementation** and confirming they align with the spec, by hand, per question below.

Required verification questions — the controller must record an explicit answer to **each**, not a single “verified green”:
1. Did the subagent solve the first-principles spec, or patch the visible symptom? (Check the diff against the spec text directly — e.g. if the spec said “consolidate to ONE engine,” a diff that keeps two and justifies it “empirically” has **failed** this gate regardless of test color.)
2. Is the original proof burden discharged at the owned boundary?
3. Does the diff introduce any banned patterns?
4. Are tests proof-bearing, or merely policing/visibility/existence/string/helper tests?
5. Did the implementation fail open anywhere?
6. Was slop deleted without burden disposition?
7. Would the old broken implementation fail the new proof?
8. Does the result depend on the exact reviewer wording?

The recorded answers are the **verification stamp** carried into Phase 6 / thread closure (see Per-Thread Stamps).

If validation fails — including any deviation from the spec the subagent self-justified — reject and issue a corrected spec or assign a fresh subagent. Do not patch it locally, and do not accept the subagent’s deviation just because tests pass.

### Phase 6: Commit Before Disposition
The commit message must mention:
- root concern;
- proof burden;
- files changed;
- tests/proof added;
- banned-pattern audit result;
- review item(s) remediated.

Only then may the controller post a positive PR-thread reply.

## Review Feedback Disposition Ledger (PR Comment & Repo)

Every PR must have a top-level review ledger.

### Inline and Top-level PR Ledgers
Rejected or modified feedback must not disappear into resolved threads. They must be recorded twice:
1. An inline/thread reply with rationale.
2. A top-level PR comment titled `Review feedback disposition ledger`.

#### Top-level Comment Ledger Format
```markdown
# Review feedback disposition ledger

## Rejected feedback

### <thread/comment link or id>

Claim:
<What the reviewer alleged.>

Disposition:
Rejected.

Why:
<Why the claim is false, not repository-owned, design-hostile, generic review slop, or conflicts with stronger global policy.>

Policy basis:
<Specific policy or product semantics.>

Audit anchor:
<File/line/doc/command that proves the rejection.>

## Accepted with modified remediation

### <thread/comment link or id>

Claim:
<True concern.>

Reviewer remediation:
<Why the proposed fix was misaligned.>

Actual remediation:
<Commit + proof.>
```

### Repo-side dispositions artifact: `.pr/REVIEW_DISPOSITIONS.md`
For large PRs, require a tracked repository artifact at `.pr/REVIEW_DISPOSITIONS.md`:

```markdown
# Review dispositions

## Accepted and remediated

### <review item id / thread URL>

Root concern:
<first-principles concern>

Remediation spec:
<link or pasted summary>

Implementer:
<subagent/session>

Commit:
<sha>

Proof:
<commands/tests/files>

Verification (orchestrator-stamped):
<spec-honored confirmation: declared remediation matches actual implementation; commit hash that closed the thread>

Banned-pattern audit:
<summary>

## Rejected

### <review item id / thread URL>

Claim:
<reviewer claim>

Reason for rejection:
<policy/product evidence>

Top-level PR comment:
<link>

## Still open

### <review item id / thread URL>

Blocker:
<what remains>
```
This file is the durable repository-side audit trail.

## Banned PR Review Handling

- Accepted current-PR disposition without a remediation commit.
- “Will address” followed by resolving the thread.
- “Accepted” without code/proof change.
- Resolving an accepted comment before independent remediation review passes.
- Giving the implementer the exact reviewer wording as the task.
- Asking a subagent to “fix review comment X.”
- Patching only the cited line when the concern is boundary-level.
- Adding tests that assert source shape, strings, existence, visibility, helper branches, or absence of banned tokens.
- Replacing a real proof burden with a policing test.
- Resolving rejected feedback only inline without a top-level ledger entry.
- Treating an issue opened for later work as resolution of current accepted feedback; the only exception is an independent `Backlogged as minor technical debt` disposition that satisfies every current-PR spend-gate criterion.
- Using the debt escape hatch for a current acceptance criterion, proof gap, required check, user-visible defect, hard-policy violation, or PR-caused regression.
- Letting the original worker remediate its own review without independent spec-and-review.
- Disposing findings from the orchestrator’s own judgment instead of an independent disposition subagent (Phase 2.5).
- Grouped verdicts masquerading as dispositions (“CI churn,” “false-positive wave,” “bulk-reject”). Batch processing is allowed; each finding still needs its own disposition.
- Injecting an invented or paraphrased premise (“the owner approved X”) into a disposition or remediation subagent prompt without a verbatim quote.
- Closing an accepted current-PR thread without all three stamps (disposition → remediation → verification-with-commit-hash), or closing backlogged debt without Gate 3 evidence and a linked issue.
- Treating per-push CI re-review as a “snowball” and using that framing to avoid dispositioning the new round.
- Doing the A/B/C split correctly only after maintainer pushback; see the
  `qc-triage` prohibited behavior on supervised-only correctness.

## Loop and Convergence

This is a **convergent loop**, not a single pass and not a snowball:

```
reviews land → Phase 2.5 disposition round (batched if appropriate; one disposition per finding) → record disposition stamps on every thread
  → close rejected/duplicate/outdated/backlogged findings in B → Phase 3–4 remediation round (accepted current-PR findings only) → Phase 5 verify → Phase 6 commit
  → push (triggers a fresh review round) → repeat
```

Each round must **close an entire window** of threads: every open thread in the round gets a disposition stamp, accepts get remediated/verified/closed, rejects/duplicates/outdated get closed with rationale, and backlogged minor debt gets closed with spend-gate evidence plus a linked issue. A round is not “done” while dispositioned threads remain open.

**It converges.** New review rounds on each push are expected and benign — the reviewers re-run against the growing diff. The window shrinks each round because accepted findings are fixed and removed, and rejected/duplicate/outdated/backlogged findings are closed and do not return. The loop **terminates** when a full review round comes back with **no findings requiring current-PR remediation** — i.e. every finding in the latest window disposes as rejected, duplicate, outdated, or backlogged minor debt.

**It only snowballs if your own remediations inject new policy-misaligned slop.** That is precisely what the policy-primed independent remediation subagent (Phase 4) and the verification gate (Phase 5) exist to prevent — every known category of finding has a documented correct remediation, so a correctly-run remediation round does not generate a larger next round. If the window is *growing* round over round, the failure is in the remediation quality (slop is being introduced), not in the existence of the loop. Diagnose and fix the remediation process; do not abandon the loop or hand-wave findings as “noise.” Apply the current-PR spend gate explicitly when a true finding may be minor debt.

**Duplicate / outdated / superseded threads** are still dispositioned per finding, never silently skipped:
- A thread whose finding is already dispositioned elsewhere → `Duplicate of <canonical thread>`, closed with that pointer.
- A thread on code that a later commit replaced → `Outdated (superseded by <commit>)`, closed with that pointer.
- Cross-run duplicates from the same finding re-flagged on a new push → disposed against the canonical thread, not re-litigated from scratch.

A finding being a likely duplicate does **not** authorize the orchestrator to self-judge it — confirm the duplication against the canonical thread; if it is not genuinely the same finding on the same code, it gets its own per-finding disposition.

## Global Principles

### 1. Global policy outranks local self-justification
Local repo docs can narrow or explain what a local artifact is for, but they cannot make mocks, skips, `as any`, fallback defaults, or proof laundering acceptable. The global `quality-control` skill declares an authority hierarchy where `quality-control`, `test-guidelines`, `tool-provisioning`, `known-solution-first`, and `reality-grounded-debugging` outrank domain skills. Domain skills may narrow but not weaken these global policies. For example, `test-guidelines` is explicit that mocks, stubs, fakes, simulated environments, skips, and masking are forbidden with no exceptions.

### 2. Reviewer comments are claims, not commands
This cuts both directions. Do not blindly accept paranoid sandboxing, graceful fallback, enterprise compatibility, or micro-optimization advice. Also, do not reflexively reject comments because they came from a generic reviewer. Typechecking exclusions, `as any`, swallowed errors, stale-state races, and missing console-error gates are real correctness issues even when surfaced by a generic bot.

### 3. The accepted remediation must preserve the purpose of the rule
Identify the substantive reviewer concern, the literal repo rule in tension, the purpose of that rule, and the action that best preserves that purpose. Do not use policy as a shield to avoid a real fix, and do not use a real bug as an excuse to import a misaligned fix.

### 4. Type-system and QC coverage gaps are not style comments
Excluding a TypeScript config/helper file from typechecking, using `expect as any`, or weakening E2E proof boundaries are proof-loop failures. They must be treated as aligned feedback unless the factual premise is false. The remediation must restore the proof surface, not add casts, skips, local QC subcommands, or test-only fakery.

### 5. Race conditions are correctness bugs when they can produce stale user-visible state
They are not "edge cases" in the enterprise-hardening sense. A small generation-token, abort-controller, mounted-state, or request-sequencing fix is aligned when it prevents old async work from overwriting newer user-visible state. The acceptance condition is: small blast radius, no new abstraction stack, preserves observable intended behavior, and prevents a high-probability UI correctness failure.

### 6. Micro-optimizations are rejected by default
"Use this faster API," "make this async," "cache this," or "avoid this loop" is not enough. Incorporate only when the change improves objective correctness, removes complexity, fixes a measured/reproduced user-visible problem, or is essentially zero-risk and semantics-preserving. Otherwise, it is generic code-review slop. The anti-slop guidance already says enterprise-grade edge-case handling is wrong for bespoke software and the correct default is happy path plus loud failure.

### 7. Security/sandbox comments require semantic-contract classification
For private, single-user editor-like software, "workspace escape," "path traversal," and "symlink escape" may be generic security framing that conflicts with intended workflows. Do not ask "could this leave a sandbox?" Ask instead: "does the app own a containment invariant, or does it own editor file identity?" If the user expects symlinked notes to be edited correctly, anti-symlink hardening is misaligned unless the app explicitly owns a security boundary.

### 8. Smoke/harness checks are not proof
A mocked or synthetic browser smoke check can only be a diagnostic health check, and the global no-mock rule means it cannot prove product behavior. Do not let relabeling become resolution (such as renaming a mocked test to `smoke` or `harness` while preserving the unproved artifact). Either the artifact is a non-proof diagnostic and excluded from feature-proof claims, or it must be removed/replaced by a real proof.

### 9. Deletion is also a remediation claim
When a review item is resolved by deletion, require the same scrutiny as a code fix. Never accept “removed” as a complete disposition. The deletion must disposition both the artifact and the original problem or proof burden that caused the artifact to be introduced, ensuring the original burden is either solved, invalidated, explicitly transferred, or recorded as unresolved.

### 10. Scan remediations for Bridge-Burning Red Flags
If a construct would let an agent preserve the appearance of correctness while weakening the obligation, treat it as a red flag even if the code currently works. Reviewers and triage agents must audit changes against the [Bridge-Burning Red Flags Reference Catalog](file:///home/dzack/ai/opencode/skills/policy-index/references/red-flags.md) and the [Runtime Control-Flow Red Flags Catalog](file:///home/dzack/ai/opencode/skills/policy-index/references/runtime-control-flow.md) to detect validation-evasion moves (such as runtime defaults, fallbacks, mocks, exact string assertions, and fail-open control branches).

### 11. Optional / absent-data fields default to required-and-fixed
A finding that an output or contract field is optional/nullable is accepted unless the declaration justifies the absence as a genuine, irreducible domain state. "Models real absent data" is not a sufficient justification by itself: the default is to require the field and fix the data so it is always present, modeling true absence as its own narrow case rather than a shared `optional` every consumer must tolerate. A convenience-optional weakens the interface for everyone, the same way a fallback default does. See the [Optional-Field Axiom](references/disposition-prefilter.md#optional-field-axiom).

## Routing Matrix

When routing PR review workflows, follow these rules:

- **User asks to review a PR**:
  Load `git-guidelines` (see `code-review.md`) + the [Review Guidelines](https://github.com/dzackgarza/ai/wiki/Review-Guidelines) wiki page + `reviewing-llm-code` + `test-guidelines`.
  If the PR is agent-produced, also load `reviewing-subagent-work`.

- **User asks to address, resolve, reply to, or classify PR review comments**:
  Load `git-guidelines` + `pr-feedback-triage` + `quality-control` + `test-guidelines`.
  Also load `anti-slop`/`reviewing-llm-code` for code-quality claims.
  Load `known-solution-first` for external tool/compiler/library claims.
  Load `reality-grounded-debugging` for CI/check failures or opaque logs.

- **User asks whether automated review feedback aligns with policy**:
  Load `pr-feedback-triage` first, not `git-guidelines` (see `pr-workflow.md`).
  Use `git-guidelines` only for mechanics/API commands.

- **User asks an implementer agent to fix review comments**:
  The controller must triage comments first.
  The implementer receives only accepted or accepted-with-modification work items, with the policy-compatible remediation stated explicitly.

## Triage Rubric

For each review item, evaluate:

1. What is the underlying concern?
2. Is the concern factually true in the code/diff/config/runtime?
3. Which global or repo rule does it implicate?
4. What fix does the reviewer suggest?
5. Does that fix preserve:
   - fail-fast behavior
   - no mocks / no fake proof
   - global QC authority
   - type/proof integrity
   - single-user bespoke semantics
   - low complexity / low blast radius
   - user-visible correctness
6. If not, what narrower fix preserves the real concern without importing review slop?
7. Does this true concern require current-PR remediation under Gate 3, or does it meet every criterion for batched minor debt?
8. What visible PR reply will let the user audit the disposition?

### Examples

#### Accepted
- `as any` in proof/test surface → replace with narrow typed surface.
- skipped test or excluded typechecked file → restore proof/QC coverage.
- swallowed error → fail loudly with context.
- stale async request overwrites newer UI state → add small sequencing/cancellation guard.
- request can hang indefinitely → add bounded timeout that fails loudly.

#### Accepted with Modified Remediation (Concern true, fix wrong)
- Config failure is obscure → improve surfaced crash/error context, but do not continue with defaults.
- External API can hang → add fail-loud timeout, not fallback data.
- Type inconsistency signal → investigate and align config, not cargo-cult NodeNext/bundler.

#### Rejected
- symlink "workspace escape" for an editor-like single-user app where symlinks are intended file identity.
- "make this async" because it might be faster.
- `entry.metadata()` micro-optimization with no observed problem.
- sandboxing or path traversal hardening that breaks intended local workflows.
- replacing real proof with browser-smoke/mock harness.
- adding skips, mocks, `type: ignore`, graceful defaults, or fallback warnings.
## Deletion Is Also a Remediation Claim

When a review item is resolved by deletion, require the same scrutiny as a code fix.

The thread response must state:
- what original problem the deleted artifact attempted to solve;
- why that problem is no longer live, or where it is now solved;
- what proof or issue records the disposition;
- why deletion does not weaken the PR’s evidence.

Never accept “removed” as a complete disposition.

A PR thread resolved by deletion must not say only “removed.”

Required format:

```text
Deleted artifact: <file/name>
Original burden: <what it attempted to prove/solve>
Burden disposition:
  - solved by: <real proof surface/implementation>
  - invalidated by: <evidence/contract change>
  - transferred to: <other location>
  - remains open in: <issue number/explicit blocker>
Verification: <how it was verified>
```

Example:

```markdown
Deleted `browser-smoke` mocked IPC test.

Original burden: fast detection that the frontend shell can mount without real Tauri IPC.
Burden disposition: remains useful as a diagnostic, but cannot be proof-bearing under
global no-mock rules. Replaced with real Tauri workflow tests for product behavior;
no diagnostic replacement kept in this PR. The lack of a non-proof shell diagnostic is
accepted because product proof is now covered by <test>.
```

or:

```markdown
Deleted mocked IPC test.

Original burden: product-level Tauri IPC proof.
Burden disposition: not solved. Opened issue #N and this PR remains incomplete for that
proof requirement.
```

## Per-Thread Stamps: Disposition → Remediation → Verification

Every accepted current-PR thread must carry all three stamps before it is closed. The three stamps come from the three stages and must not be collapsed or skipped:

1. **Disposition stamp** — from the Phase 2.5 disposition subagent. Records the five-way disposition, the policy basis, and that it was produced by an independent disposition subagent grounded in policy + literal owner comments.
2. **Remediation stamp** — from the Phase 4 remediation subagent. Records the first-principles remediation, the files changed, and the proof commands the subagent reported.
3. **Verification stamp** — orchestrator-stamped (for now). The orchestrator compares the **declared remediation against the actual implementation in the commit**, confirms they align with the spec (Phase 5 questions), and records the **commit hash**. The commit hash in the verification stamp is what closes the thread — no thread is resolved without it.

A thread disposed as rejected or duplicate/outdated carries only the disposition stamp (with rationale / pointer) and is closed on that basis — it never receives a remediation or verification stamp, because no code changed. A thread dispositioned `Backlogged as minor technical debt` also carries only its disposition stamp, but that stamp must record every Gate 3 criterion, the factual evidence, and the linked GitHub debt issue. Never resolve one of these threads silently.

Ordering is strict for accepted current-PR feedback: no remediation stamp without a prior disposition stamp; no verification stamp (and no thread closure) without a prior remediation stamp **and** a commit hash. An accepted current-PR reply without a verification stamp carrying a real commit hash is false signaling (see Core Rule: Positive Current-PR Disposition Requires Committed Remediation).

## Visible Thread Reply Format

When replying to and resolving an accepted current-PR thread on GitHub, the reply must carry all three stamps:

```text
<Disposition Type> (Accepted as written / Accepted with modified remediation)

Disposition (independent disposition subagent):
  Claim disposition: <true / false / needs investigation>
  Remediation disposition: <aligned / misaligned / underspecified>
  Policy basis: <policy clause + literal owner comment, if any, the disposition rests on>

Remediation (independent remediation subagent):
  Root concern: <first-principles concern, not reviewer wording>
  Code/action taken or explicit non-change: <summary of the changes/non-change>
  Proof: <commands/tests/files the remediation subagent reported>

Verification (orchestrator-stamped):
  Spec honored: <yes — declared remediation matches actual implementation and the spec>
  Commit: <sha>   # this hash is what closes the thread
  Audit anchor: <commit/file/line/linked issue where the user can audit the result>
```

For a thread disposed as Rejected / Duplicate / Outdated, only the Disposition block is required (with rationale and, for duplicate/outdated, a pointer to the canonical thread or superseding commit).

For `Backlogged as minor technical debt`, post a disposition-only reply recording every
Gate 3 criterion, the factual evidence, batching basis, GitHub debt-issue link, and why
the PR remains complete. Resolve it without remediation or verification stamps because
no role C or current-PR code change occurs.

## Tests Added in Response to Review

When a review response adds tests, classify every assertion:

- **Proof assertion**: excludes a plausible broken implementation at the owned boundary.
- **Policing assertion**: checks source shape, review compliance, helper branch, existence, visibility, exact string, or absence of a banned token.
- **Setup assertion**: only prepares the test and must not be cited as proof.

Review feedback is not resolved by policing or setup assertions. Consult the central [Banned Test Shapes Catalog](file:///home/dzack/ai/opencode/skills/policy-index/references/test-proof-rules.md) to ensure all added assertions are proof-bearing.

### Response Examples

**Accepted with modified remediation:**
> Accepted with modified remediation.
>
> Claim disposition: Aligned. The feedback correctly identified a fail-fast violation: this code swallowed error.
> Remediation disposition: Misaligned. The suggested remediation to log and continue is not aligned with repo policy because failures at this boundary must stop the operation.
> Policy basis: Fail-fast outranks graceful degradation.
> Code/action taken or explicit non-change: Fixed in commit `1234abc` by throwing a specific error with context.
> Audit anchor: `src/api_client.py:45-52`

**Rejected:**
> Rejected.
>
> Claim disposition: Misaligned. The comment frames symlink traversal as a workspace escape/security issue.
> Remediation disposition: Misaligned. The proposed canonicalization hardening would break editor semantics.
> Policy basis: The app is a single-user editor, and intentional symlinked files are part of the expected workflow. No security boundary is owned here.
> Code/action taken or explicit non-change: No code change made.
> Audit anchor: `src/file_handler.py:12`

**Investigated:**
> Investigated, then accepted.
>
> Claim disposition: Aligned. The reviewer noted a `bundler` vs `NodeNext` mismatch.
> Remediation disposition: Aligned.
> Policy basis: Correct type-checking contract across the codebase.
> Code/action taken or explicit non-change: Checked config files and aligned `tsconfig.json` module resolution.
> Audit anchor: `tsconfig.json`
