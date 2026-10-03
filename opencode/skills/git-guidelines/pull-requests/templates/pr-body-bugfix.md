<!-- 
PR Body Template: Bugfix
Follows the three-layer model from pr-body-admission-gate.md
Emphasizes TDD: failing test before fix
-->

## Bug Description (Layer 1: Observable Behavior)

<!-- What externally observable behavior was wrong?
     Not: "the function returned None"
     But: "user action X produced error Y instead of result Z"
-->

## Root Cause

<!-- What code/logic was causing the observable failure? -->

## Fix

<!-- What does this PR change? Narrow scope preferred. -->

## GitHub Tracking

<!-- Use closing keywords so GitHub creates Development links automatically.
     Verify with: gh pr view <PR_NUMBER> --json closingIssuesReferences -->

**Closes on merge:**
- Fixes #<!-- issue for this bug -->

**References only:**
- Refs #<!-- parent issue or related work not closed by this PR -->

## Evidence Required (Layer 2: TDD)

**Pre-fix verification:**
- [ ] Added failing test that reproduces the bug (commit: <!-- sha -->)
- [ ] Confirmed test fails for the right reason (not spurious failure)

**Post-fix verification:**
- [ ] Same test now passes (commit: <!-- sha -->)
- [ ] Test would fail if the fix were reverted (proves it tests the actual bug)

**Regression protection:**
| What broken code would pass this test? | How the test prevents it |
|----------------------------------------|--------------------------|
| <!-- false positive scenario --> | <!-- assertion that catches it --> |

## Current Status (Layer 3: Just-in-Time Judgment)

- [ ] **Bug fix**: <!-- ✅ Complete | ⚠️ Partial | ❌ Blocked -->
  - Evidence: <!-- link to test file, CI run showing red→green -->
- [ ] **Regression test**: <!-- ✅ Complete | ⚠️ Needs strengthening | ❌ Missing -->
  - Evidence: <!-- test that would catch this bug in future -->

## Risk Assessment

<!-- Could this fix break anything else? What's the blast radius? -->

**Risk level:** Low / Medium / High

**Reasoning:** <!-- why this risk level -->

**Mitigation:** <!-- what reduces the risk (existing test coverage, narrow scope, etc.) -->

## Review Focus

- Does the test actually reproduce the reported bug?
- Would the test pass on plausibly broken code?
- Is the fix narrower than expected, or does it change unrelated code?
- Does the root cause analysis match what the fix changes?
