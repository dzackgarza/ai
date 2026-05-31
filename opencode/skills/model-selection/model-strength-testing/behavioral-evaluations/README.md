# Behavioral Evaluations

This subtree stores fixtures for evaluating LLM competence, behavioral failure patterns,
and anti-gaming behavior.
These are not ordinary project tests.
They are benchmark cases for judging whether an agent can follow instructions,
distinguish evidence from misleading signals, and produce general solutions rather than
implementations that satisfy visible examples.

## Fixture Sets

- `anti-gaming-tdd-fixtures/rigorous-test`: runic decoder trials, adversarial tests, and
  a detector for visible-test gaming.
  Treat the numeric claims in `experimental-log.md` as unreproduced experiment notes
  until reproduced.

- `anti-gaming-tdd-fixtures/secret-language`: property-based and adversarial behavioral
  tests designed to catch hard-coded or pattern-matched solutions.

- `anti-gaming-tdd-fixtures/roman-numerals`: negative-control material.
  It is useful because it demonstrates a poor anti-gaming task choice: the problem is
  familiar enough that solving it normally is expected.

- `adversarial-debugging-red-herring`: debugging task where the visible failure points
  toward password hashing while the defect is a time-comparison bug.
  Use it to evaluate hypothesis generation, evidence gathering, and red-herring
  resistance.

## Evaluation Standard

Use these fixtures to measure behavior, not activity.
A passing evaluation must show which concrete behavior was demonstrated and what
evidence proves it. File creation, command execution, and self-reported analysis are not
evidence of competence.

## Related Existing Work

- `../folder-tasks/`: current one-shot and constrained-folder model strength tasks.
  New behavioral fixtures should follow the same structure when turned into runnable
  benchmark prompts.

- `../../../llm-failure-modes/SKILL.md`: catalog of the failure patterns these fixtures
  are intended to expose.

- `../../../test-guidelines/SKILL.md`: standards for tests as proof of repository-owned
  behavior.

- `../../../jerry-behaviour/SKILL.md` and `../../../charlie-behaviour/SKILL.md`: review
  and correction-loop failure patterns relevant to scoring outputs.
