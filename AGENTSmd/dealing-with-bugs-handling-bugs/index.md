---
order: 40
title: Dealing With Bugs / Handling Bugs
---

IMPORTANT: when you encounter a bug in an app, DO NOT IMMEDIATELY FIX IT. The fact that a bug exists exposes fundamental flaws in your methodology and testing.

1. STOP IMMEDIATELY. Do NOT take any action until you walk through this guidance step-by-step.
2. Investigate only enough to capture the real observed failure as a faithful red test. Record exactly: what command was run, what the actual output was, what the diff is, what error was thrown. The test must fail because of the ACTUAL observable bug, not because of a scenario you guessed from priors. All investigation is subordinate to this single goal: faithfully encoding the observed failure.
3. IMPORTANT: DO NOT FIX THE BUG! *REPRODUCE* it first with a REAL red test that fails exactly BECAUSE the bug exists. The test must not fail for possibly unrelated reasons. The fact that the test fails right now must PROVE that the bug exists.
4. DO NOT FIX THE BUG YET! COMMIT the red test to establish an AUDIT TRAIL. The git history MUST reflect that the bug was reported and a red test was designed specifically for it and observed to fail. You CAN NOT PROCEED without this commit. If you've skipped this step, you need to start over. Ask the user to revert whatever files you changed.
5.b. IMPORTANT: A MOCK DOES NOT CONSTITUTE A PROOF OF THE EXISTENCE OF A BUG. THE USER IS REPORTING A BUG TO YOU RIGHT NOW. THE BUG IS OBSERVABLE AND REPRODUCIBLE IN LIVE, REAL CODE. DO NOT SIMULATE, MIMIC, OR MOCK BUGS. And CERTAINLY do not present tests with mocks as PROOF that the test "catches" the bug -- false, it catches a SIMULATION of *A* bug that YOU invented. Fixing that simulation is NOT equivalent to fixing the bug that is ACTUALLY observable right now.
5.c. IMPORTANT: a test that simply asserts on the non-existence of a fix is also not a proof of a bug. E.g. if your "fix" involves adding a new API endpoint and your test asserts that the endpoint exists, you have proved nothing about the existence of the ACTUAL underlying problem: you have proved NON-existence of what you BELIEVE is the solution, which is an absurd stance, because if you've written this kind of test then you have still not actually observed or proved the bug exists at all. If your test would STILL pass if the bug DID NOT EXIST, it does NOT prove existence!
6. ONLY once you have a committed red test: stop and explain to the user why the test failing PROVES that the bug exists and is observable. Emphasis on why it actually PROVES the bug exists. "The bug is observed and the test fails" is not a proof: it is correlation with no clear causation either way. The test logic should provide enough information for any external party to reproduce the bug themselves.
7. AFTER the user approves the proof, you may proceed with the fix. When the tests pass, you must AGAIN check with the user: provide steps to reproduce the bug, and wait to get confirmation that the fix truly fixes it. If it does not, you must start over, because your test was fundamentally flawed: it both failed and passed with the bug still present, meaning your entire change was code mutation and thrashing, and thus a net regression. Record the flawed hypothesis in memory so you don't assume it again.

**Refinement for dependency-owned bugs.** The above procedure assumes the bug is in
project-owned code. If the "bug" is a compiler error, library behavior, API failure,
package version mismatch, or any symptom whose meaning is owned by an external project,
then step 2 expands: while capturing the faithful reproduction, also search the exact
error, upstream docs, release notes, and known issues. Establishing the external
contract is part of constructing the reproduction case. Do not web search as a
substitute for faithful reproduction of a project-owned bug. But for dependency-owned
behavior, web search (exact errors, version-specific docs, known fixes) is part of
establishing what the tool actually means. Load `known-solution-first` for the external
half of the investigation.

REMINDER: STOP IMMEDIATELY. DO NOT FIX THE BUG. Your ONLY job when this happens is to CREATE AND COMMIT A RED TEST that proves the observed failure exists. All investigation must be SUBORDINATE to that EXACT task: understanding the failure well enough to encode it in a test. A test you guess from priors (without running the failing code) proves nothing — it replaces the epistemically clean state "I don't know what fails" with the dirty state "I have false beliefs about the failure." State EXPLICITLY to the user WHY your investigations are PRECISELY for constructing a red test if you DO need to dig deeper.

Load `reality-grounded-debugging` alongside for command-output discipline, surface-classification matrix, and the synthesis gate (raw observation, smallest reproducer, missing surface, verification path).
For dependency-owned behavior, also load `known-solution-first` for establishing the
external contract before probing locally.

You must immediately stop and ask yourself why your entire test and QC suite passes when bugs exist, and address the procedural issue first.
Are your tests full of fake or idealized data?
Did you not follow TDD? Do they not exercise real user behaviours and workflows?
If your tests missed this, what else could they have missed?
Your priority is not fixing the bug, it is fixing the PROCESS that led to a situation where tests didn’t catch the bug FOR you.
Thus your immediate concern is stepping back, evaluating the tests and QC for weak or reward-hacked patterns.
Immediately review the testing guidelines skills, determine an entire class of missing tests you need, and implement them.
NEVER fix a bug until you have a red test that PROVES the test suite has been enhanced enough to catch this class of errors.
Immediately use TDD skills, separate the red/green changes into separate commits for auditing purposes.
Again, NEVER fix a bug or an error without re-evaluating why it wasn’t caught earlier.

BE EXTREMELY CAREFUL: if you don’t VERIFY that your test FAILS when the bug is present, the fact that it passes after a “fix” proves absolutely nothing and is worse than useless: you’ve added false signal to the tests, inflated and mutated code, introduced technical debt that will double the work needed from audits/reviews, possibly even warranting starting the bug triage over from scratch.
A “bug fix” is not a code patch: it is an auditable trail of git commits proving the bug exists (before touching any code) with red tests and a clear commit turning all of those tests green.
A test that is green in every historical commit is zero information and proves nothing.
