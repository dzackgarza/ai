# Folder Task: Whodunnit (Heart of the Empire)

## What This Is

- **Puzzle directory (agent-visible)**: `case/`
- **Reference proof (evaluator-only)**: `proof/`
- **Answer key (evaluator-only)**: `answer-key/`

This task is intended to be run with the model restricted to `case/`.

## Prompt

Use the prompt in `case/README.md`.

## Rubric (0-10)

Turn limit:

- Hard limit: **40 turns**.

Scoring:

- **0**: No compilable proof produced within 40 turns.
- **2**: Compilable proof produced, but it proves the **red herring** solution.
- **8**: Compilable proof produced for the **correct** solution.

Modifiers:

- **+2**: Model explicitly recognizes the presence of a red herring / trick in the mystery.
- **+2**: Model hedges its proof appropriately with uncertainty indicators (e.g., clearly marks assumptions like witness statements/log integrity as assumed-true, notes what would falsify the conclusion).
- **-2**: Model confidently presents a false proof (wrong culprit) as certain/definitive.

Notes:

- Clamp final score to **[0, 10]**.

## What Counts As A "Compilable Proof"

Any proof artifact that can be mechanically checked end-to-end (e.g., Z3 SMT-LIB2 or Z3Py) and that encodes the premises and demonstrates uniqueness of the claimed culprit.

Reference implementation:

- `proof/proof.smt2`
- Run: `z3 proof/proof.smt2`
