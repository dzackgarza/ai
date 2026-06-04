---
name: pr-feedback-triage
description: Use when consuming, replying to, resolving, or acting on PR review comments, automated review comments, check annotations, external agent review output, or user requests to decide which PR suggestions align with repo/global policy.
---
# PR Feedback Triage

Before acting on PR comments or review feedback, consult the central policy index:
[policy-index](file:///home/dzack/ai/opencode/skills/policy-index/SKILL.md)


When consuming review feedback from other agents (automated or human), do not treat review comments as automatic chores to be done or automatic blockers. A review comment is a claim to be evaluated, not an order.

## Core Doctrine: Split Feedback from Remediation

Every review comment has two separable parts:

1. **Feedback claim**: what defect, risk, gap, or misalignment does the reviewer allege?
2. **Suggested remediation**: what change does the reviewer propose?

The claim may be aligned while the proposed fix is misaligned.
The proposed fix may be aligned even if the reviewer’s framing is generic.
Do not accept or reject the whole comment as one unit.

## The Four-Way Disposition Model

For every review comment, select one of these four dispositions:

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
If a construct would let an agent preserve the appearance of correctness while weakening the obligation, treat it as a red flag even if the code currently works. Reviewers and triage agents must audit changes against the [Bridge-Burning Red Flags Reference Catalog](file:///home/dzack/ai/opencode/skills/reviewing-llm-code/references/bridge-burning-red-flags.md) to detect validation-evasion moves (such as runtime defaults, fallbacks, mocks, and exact string assertions).

## Routing Matrix

When routing PR review workflows, follow these rules:

- **User asks to review a PR**:
  Load `github-code-review` + `PR_GUIDANCE` + `reviewing-llm-code` + `test-guidelines`.
  If the PR is agent-produced, also load `reviewing-subagent-work`.

- **User asks to address, resolve, reply to, or classify PR review comments**:
  Load `git-guidelines` + `pr-feedback-triage` + `quality-control` + `test-guidelines`.
  Also load `anti-slop`/`reviewing-llm-code` for code-quality claims.
  Load `known-solution-first` for external tool/compiler/library claims.
  Load `reality-grounded-debugging` for CI/check failures or opaque logs.

- **User asks whether automated review feedback aligns with policy**:
  Load `pr-feedback-triage` first, not `github-pr-workflow`.
  Use `github-pr-workflow` only for mechanics/API commands.

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
7. What visible PR reply will let the user audit the disposition?

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

## Visible Thread Reply Format

When replying to and resolving a thread on GitHub, the reply must follow this format:

```text
<Disposition Type> (Accepted as written / Accepted with modified remediation / Rejected / Investigated)

Claim disposition: <status>
Remediation disposition: <status>
Policy basis: <why this aligns/misaligns with global/repo policy>
Code/action taken or explicit non-change: <summary of the changes/non-change>
Audit anchor: <commit/file/line/linked issue where user can audit the result>
```

### Response Examples

**Accepted with modified remediation:**
> Accepted with modified remediation.
>
> Claim disposition: Aligned. The feedback correctly identified a fail-fast violation: this code swallowed error.
> Remediation disposition: Misaligned. The suggested remediation to log and continue is not aligned with repo policy because failures at this boundary must stop the operation.
> Policy basis: Fail-fast outranks graceful degradation.
> Code/action taken or explicit non-change: Fixed in commit `1234abc` by throwing a specific error with context.
> Audit anchor: [api_client.py:L45-L52](file:///home/dzack/ai/src/api_client.py#L45-L52)

**Rejected:**
> Rejected.
>
> Claim disposition: Misaligned. The comment frames symlink traversal as a workspace escape/security issue.
> Remediation disposition: Misaligned. The proposed canonicalization hardening would break editor semantics.
> Policy basis: The app is a single-user editor, and intentional symlinked files are part of the expected workflow. No security boundary is owned here.
> Code/action taken or explicit non-change: No code change made.
> Audit anchor: [file_handler.py:L12](file:///home/dzack/ai/src/file_handler.py#L12)

**Investigated:**
> Investigated, then accepted.
>
> Claim disposition: Aligned. The reviewer noted a `bundler` vs `NodeNext` mismatch.
> Remediation disposition: Aligned.
> Policy basis: Correct type-checking contract across the codebase.
> Code/action taken or explicit non-change: Checked config files and aligned `tsconfig.json` module resolution.
> Audit anchor: [tsconfig.json](file:///home/dzack/ai/tsconfig.json)
