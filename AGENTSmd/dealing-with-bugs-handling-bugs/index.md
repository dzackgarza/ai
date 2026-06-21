---
order: 40
title: Dealing With Bugs / Handling Bugs
---

When a bug or failure appears, do not patch first.

Load:

- `reality-grounded-debugging` for the observed-failure protocol, synthesis gate, and
  faithful red proof
- `systematic-debugging` for hypothesis discipline
- `test-driven-development` and `test-guidelines` for red/green proof obligations
- `git-guidelines` for the red-test commit and green-fix commit boundary
- `known-solution-first` as well when the symptom is owned by an external tool,
  compiler, API, package, provider, or library

The required first substantive artifact is a committed red test or reproducer that
fails because of the real observed bug.
Mocks, simulations, stubs, and tests that merely assert the absence of a proposed fix
do not prove the bug.

Only after the red proof exists should implementation change begin.
