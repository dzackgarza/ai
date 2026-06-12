# Deductive Reasoning Reference

Use this when the active debugging ledger has many hypotheses, assumptions, or contradictions.
The goal is not philosophical formality; it is to prevent unsupported conclusions from driving code changes.

## Ledger Extension

When the main ledger is not enough, add these sections:

```markdown
## Known Facts
- F1:

## Axioms For Elimination
- A1:

## Inferences
- I1: From F__ and A__ by [rule]:

## Eliminated Possibilities
- H__ eliminated by E__ because:

## Current Best Explanation
- Explanation:
- Facts explained:
- Facts not yet explained:
- Remaining alternatives:
```

## Statement Labels

Mark every important statement:

- `fact`: directly observed or read from a reliable source.
- `assumption`: temporarily accepted to make an experiment possible.
- `axiom`: assumption introduced specifically to derive a contradiction or eliminate a branch.
- `inference`: derived from stated premises by a valid rule.
- `hypothesis`: possible causal explanation with predictions and falsifiers.
- `speculation`: idea not yet tied to evidence.

Do not use a speculation as a premise.
Do not let an axiom silently become a fact.

## Valid Inference Patterns

Use these:

- Modus ponens: if `P implies Q`, and `P` is true, infer `Q`.
- Modus tollens: if `P implies Q`, and `Q` is false, infer `not P`.
- Chain reasoning: if `P implies Q`, and `Q implies R`, infer `P implies R`.

Prefer modus tollens for debugging because it eliminates hypotheses cleanly.

## Invalid Patterns

Do not use these:

- Affirming the consequent: `P implies Q`; `Q`; therefore `P`. Other causes may produce `Q`.
- Denying the antecedent: `P implies Q`; `not P`; therefore `not Q`. Other causes may still produce `Q`.
- Correlation as mechanism.
- Absence from a narrow search as nonexistence.
- Plausibility as proof.
- Green tests as proof of diagnosis when the test would not have failed for the original root cause.

## Deduction And Abduction

Use abduction to generate hypotheses:

```markdown
Observation: preview iframe is blank.
Hypothesis: renderer returned empty HTML.
Hypothesis: iframe was never updated.
Hypothesis: app loaded stale served output.
```

Use deduction to eliminate them:

```markdown
If renderer returned empty HTML, generated output file should be empty.
Generated output file contains the expected body.
Therefore renderer-empty-output is eliminated.
```

The best remaining hypothesis is not proven until it explains all facts and competing hypotheses have been eliminated or bounded.

## Axioms For Elimination

Axioms are temporary assumptions, not beliefs.
Use them to isolate a branch:

```markdown
A1: Assume the server sent the expected preview payload.
If A1 is true, the browser should receive event X.
Trace shows event X never reaches the client.
Therefore either A1 is false or the transport path is broken.
Next experiment: log server send and client receive with correlation IDs.
```

After using an axiom:

- Prove it directly,
- eliminate it,
- or leave it as an explicit uncertainty in the final causal case.

## Experiment Record

Each experiment needs:

```markdown
## Experiment E__
- Hypothesis tested:
- Method:
- Expected if true:
- Expected if false:
- Actual:
- Result:
- Hypotheses eliminated or weakened:
- New contradiction, if any:
```

An experiment without an expected true/false split is usually just activity.

## Prevent Circling Back

Before proposing a hypothesis:

- Check whether it has already been eliminated.
- If eliminated, quote the eliminating evidence before reviving it.
- If the evidence was flawed, record the flaw as a contradiction.
- If it was never considered, record why it is newly plausible.

The ledger is the memory.
Use it over intuition.

## When Stuck

If every hypothesis is eliminated and the failure remains:

- Reclassify each "fact" that may actually be an assumption.
- Question each axiom.
- Look for compound causes.
- Inspect a broader boundary instead of a deeper guessed path.
- Design one discriminating experiment that would separate the remaining explanations.
