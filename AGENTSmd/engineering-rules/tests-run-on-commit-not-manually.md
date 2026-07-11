---
title: Don't Run Test Suites Yourself
order: 10
tags:
- source-system-contract
- source-owner-preference
- source-observed-model-failure
- function-constrain
- function-route
- failure-process-overproduction
- failure-tool-bypass
- retest-policy-change
- retest-toolchain-change
- retest-model-self-evaluation
---

Do not run the full test suite yourself (`just test`, `pytest`, `npm test`, or an
equivalent whole-suite command) except in exceptional circumstances. In a repo correctly
configured for QC, tests run automatically and in layers on commit and push — the
pre-commit hook, the pre-push hook, and CI each fire the appropriate gate — so a manual
full-suite run duplicates work the commit already triggers.

Group work into committable units and let the commit run QC. The commit is the test
trigger: reaching for `just test` outside of committing is almost always redundant, and
treating a hand-run suite as the proof gate bypasses the layered gate that actually
guards the branch.

Running a smaller, focused test while iterating on a single function or bug is fine —
that is targeted feedback, not a suite run. The rule is against manually re-running the
whole gate that the commit fires anyway.

If you are unsure a repo is wired so QC fires on commit and push, verify the wiring
rather than compensating for it by hand:

```bash
uvx --from git+https://github.com/dzackgarza/ai-review-ci ai-review-ci doctor \
  --target . --json
```

Read the report's `global_status`. If QC is not correctly configured, fix the wiring (or
report it) instead of adopting a habit of manual suite runs.
