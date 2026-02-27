# Folder Task: ArXiv Proof Fidelity (2312.03638)

This task tests whether a model actually reads a technical paper and describes how the main theorem is proved, versus summarizing/speculating from the abstract.

## Agent-visible

- `case/`

## Evaluator-only

- `answer-key/`

## Prompt

Use `case/PROMPT.md`.

## Rubric (0-10)

Hard failures:

- If the response is clearly abstract-only (generic outline, speculation, no theorem identification), score **0-2**.

Core scoring:

- **2/10 (worst-tier)**: Summarizes/states/extrapolates from abstract or intro; no concrete proof mechanics.
- **5/10 (medium-tier)**: Correctly identifies the main theorem (or cites the correct theorem label) and gives a nontrivial but still generic "proof summary" that is mostly a list of related results.
- **8/10 (best-tier baseline)**: Gives a structurally correct proof description with the paper's key local geometry claims, including the cusp-by-cusp behavior and the critical counting logic.

Must-have details for 8/10:

- Mentions that the **normalization of the compactification** is **toroidal over cusps 2 and 4** and **semitoroidal over the remaining cusps**.
- Mentions the **double-curve counting argument** as a critical step (not optional / not just "some counting").

Bonus:

- **+2** (cap at 10): Clearly integrates the double-curve logic into the narrative of the proof (what is being counted, why it forces the conclusion), rather than name-dropping.

Clamp final score to **[0, 10]**.
