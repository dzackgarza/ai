# <Bugfix> PR Tracker

The PR body is the canonical tracker.
Use one nested checklist tree.
Checked means complete, and every checked line must include same-line proof.

## Task Tree

- [ ] <Milestone or goal>
  - [ ] Reproduce and prove the bug
    - [ ] Capture the observed failure as a red test or reproducible command.
    - [ ] Commit the red proof before implementation.
  - [ ] Fix the bug
    - [ ] Implement the narrow fix.
    - [ ] Verify the same proof now passes.
  - [ ] Regression protection
    - [ ] Run affected tests.
    - [ ] Run system-level validation.

## Evidence Appendices

- Bug description:
- Root cause:
- Fix rationale:
- Risk assessment:

Fixes #
