# Exposition Style

Dzack-specific pedagogical writing style for mathematical content. The house rules below
sit on top of an opinionated literature; read from it rather than reasoning about
mathematical prose from first principles.

## The standard references

Mathematical writing is one of the best-served subjects in the profession's own
literature, and every one of these authors argues for positions rather than listing
conventions.

- **Halmos, "How to Write Mathematics"** — in Steenrod, Halmos, Schiffer & Dieudonné,
  *How to Write Mathematics* (AMS, 1973; from *l'Enseignement Mathématique*, 1970). The
  canonical essay, by the AMS Committee on Expository Writing. Say something and have one
  thing to say; the spiral plan of organization; write for a reader who must be able to
  reconstruct your thought; the best notation is no notation. Start here.
- **Serre, "How to write mathematics badly"** (Harvard Basic Notions seminar, 2003) — the
  same subject inverted into a catalogue of failures, which is the form that transfers
  fastest. Video and a transcript are both available.
- **Knuth, Larrabee & Roberts, *Mathematical Writing*** (Stanford CS209, 1987; MAA Notes
  14) — thirty-one lectures with guests including Halmos and Lamport, plus a minidictionary
  of usage. The full text is free from Knuth's Stanford page.
- **Mermin, "What's Wrong with These Equations?"**, *Physics Today* 42(10), 1989 — the
  three rules for displayed mathematics inside prose: number every displayed equation
  (Fisher's rule); refer to it by a phrase and not only a number (the Good Samaritan
  rule); a displayed equation is part of a sentence and takes its punctuation (the Math is
  Prose rule). The governing reference for how equations sit in text.
- **Higham, *Handbook of Writing for the Mathematical Sciences***, 3rd ed. (SIAM, 2020) —
  the reference work, cited as recommended style by the AMS Author Handbook and the SIAM
  Style Manual.
- **Krantz, *A Primer of Mathematical Writing***, 2nd ed. (AMS) — grammar, syntax and
  usage at length, plus the surrounding professional practice.
- **Su, "Guidelines for Good Mathematical Writing"** (MAA Focus, 2015) — three free pages,
  the fastest useful read, and the right thing to hand a contributor.
- **The AMS Author Handbook and the SIAM Style Manual** — the house-style authorities when
  a convention is actually in dispute.

Beyond these, working mathematicians maintain advice pages carrying far more specific
guidance — when to number an equation, how to name a lemma, which phrases are dead.
[writing-advice-corpus.md](writing-advice-corpus.md) collects them (Tao, Conrad, Pak,
Vakil, Margalit, Reiter, Tsitsiklis, the Princeton Companion essays) along with the
aggregators for finding the rest.

The anti-patterns recorded at the end of this file are the ones observed here that these
sources do not name explicitly, usually because no human writer produces them.

## Core Principles

1. **Precision Over Brevity**

   - Every step must be mathematically justified

   - No “clearly” or “obviously” without explicit reasoning

   - All algebraic manipulations shown in full

2. **Structured Exposition**

   - Solutions follow a clear, logical progression

   - Each major step is numbered or bulleted

   - Key transitions are explicitly noted

## Problem Presentation

### Problem Statement Format

A problem statement must include:

- Clear, concise wording

- All given information

- Proper mathematical notation with consistent formatting

- Any necessary conditions or constraints

### Solution Structure

1. **Setup**

   - Restate the problem in mathematical terms

   - Define any variables or notation being introduced

   - State the approach or method to be used

2. **Step-by-Step Development**

   - Break down the solution into logical, numbered steps

   - Each step should contain exactly one mathematical operation or concept

   - Include the justification for each step in-line

3. **Verification**

   - Include verification of the solution when appropriate

   - Show that the solution satisfies any initial conditions

   - Check for reasonableness of the result

## Proof Techniques in Exposition

### Direct Proofs

- State what is to be shown

- Present the argument in logical sequence

- Conclude with QED or a clear statement of the result

### Limit Proofs

- Clearly state the limit to be evaluated

- Show all algebraic manipulations

- Justify each limit law or theorem used

- Conclude with the final limit value

### Proof by Contradiction

- State the assumption explicitly: `[Assume ¬P]`

- Derive consequences logically

- Reach a contradiction

- Conclude P holds

### Proof by Induction

- State the predicate P(n) clearly

- Verify base case (usually n = 0 or n = 1)

- State induction hypothesis: `[Assume P(k)]`

- Show P(k) ⇒ P(k+1)

- Conclude ∀n: P(n)

## Example: Polynomial Derivative via Limit Definition

**Problem:** Find the derivative of `f(x) = x² + 3x - 2` using the limit definition.

**Solution:**

1. Write the difference quotient:
   ```
   f'(x) = lim_{h→0} [f(x+h) - f(x)] / h
   ```

2. Expand f(x+h):
   ```
   f(x+h) = (x+h)² + 3(x+h) - 2 = x² + 2xh + h² + 3x + 3h - 2
   ```

3. Compute the difference f(x+h) - f(x):
   ```
   f(x+h) - f(x) = (x² + 2xh + h² + 3x + 3h - 2) - (x² + 3x - 2) = 2xh + h² + 3h
   ```

4. Form the difference quotient:
   ```
   [f(x+h) - f(x)] / h = (2xh + h² + 3h) / h = 2x + h + 3
   ```

5. Take the limit as h → 0:
   ```
   f'(x) = lim_{h→0} (2x + h + 3) = 2x + 3
   ```

**Verification:**

- For `x = 0`, `f'(0) = 3`, which matches the slope of the tangent line.

- The result is consistent with the power rule.

## Best Practices

1. **Clarity**

   - Write for your intended audience

   - Explain non-obvious steps

   - Use consistent notation throughout

2. **Rigor**

   - Don’t skip non-trivial algebraic steps

   - Justify all limit evaluations

   - Check for domain restrictions

3. **Presentation**

   - Use proper mathematical typesetting

   - Align equations for readability

   - Group related expressions together

4. **Verification**

   - Check your work at each step

   - Verify the final answer makes sense in context

   - Consider special cases or edge cases

## Anti-Patterns in Exposition

| Pattern | Why Bad | Do Instead |
| --- | --- | --- |
| Skipping algebraic steps | Reader cannot verify; gaps hide errors | Show every expansion, factorization, simplification |
| Unstated domain restrictions | Solutions may be invalid outside domain | State domain at the beginning; check restrictions |
| Inconsistent variable reuse | Confusion; “x” means two different things | Use distinct names; subscript if needed |
| Missing verification | Errors go undetected | Always verify, at least for a test case |
| Prose-only proofs (no math mode) | Hard to read; ambiguous precedence | Use LaTeX math for all mathematical expressions |

## Assertion of Importance in Place of Mathematics

The characteristic failure of agent-written mathematical prose is a sentence that says a
hypothesis, step, or distinction *matters* rather than saying what it does. A worked
specimen, and everything wrong with one clause:

> The rank condition is stated for a *complete intersection* presentation, and that
> hypothesis is not decorative.

- **"not decorative"** is a negative parallelism: it asserts by denying a property nobody
  claimed. No one proposed that the hypothesis was decoration, so the sentence resolves
  nothing while producing the shape of a correction. It also plants the notion it denies.
  Its relatives: "crucially", "importantly", "it is worth stressing that", "this is not a
  technicality", "genuinely necessary", "far from trivial".

  **Standard mathematical writing almost never does this, for three structural reasons.**

  1. **Hypotheses are load-bearing by construction.** A theorem's hypotheses are exactly
     what its proof consumes, and sharpening a theorem *is* the removal of the ones that
     are decorative. So the claim is true a priori — which is precisely why it can be
     written without checking anything, and why it conveys nothing when true.
  2. **The literature has positive instruments for the intended claim, and all of them
     exhibit rather than assert.** "The hypothesis is necessary", followed by the example
     where the conclusion fails. "Sharp." "Cannot be weakened to." A remark carrying the
     counterexample. Mathematicians do not tell a reader that a hypothesis matters; they
     hand over the object that breaks without it.
  3. **Negation in mathematics carries a truth value.** "f is not continuous", "the
     converse fails", "no such X exists" — each has a proof. "Not decorative" negates
     nothing about any object; it is commentary on the author's own exposition, which
     standard prose reserves for remarks that do real work.
- **"The rank condition"** takes a definite article with no referent. Which condition, on
  what object? The phrase points at something that existed only in the writer's context.
- **"is stated for"** is passive and sourceless. A theorem in a cited paper, a definition
  in this repository, and the writer's own inference are three different epistemic
  objects, and this phrasing conceals which one is in play.
- **"complete intersection presentation"** welds a real term to a vague one. *Complete
  intersection* is standard; a presentation is a generators-and-relations datum; the
  compound is not a term of art and has no fixed meaning. The intended content is
  presumably that the relations form a regular sequence — which is shorter and true.

**The repair is always the same: state the mathematics the emphasis was gesturing at.**
Name the hypothesis exactly, name the step of the argument that consumes it, and give
what fails without it — the counterexample, or the point where the proof breaks.

| Instead of | Write |
| --- | --- |
| "that hypothesis is not decorative" | the step that uses it, and the object satisfying everything else where the conclusion fails |
| "this is a crucial distinction" | the two statements, and one object separating them |
| "the general case is subtle" | which hypothesis fails in general, with a witness |
| "this condition is essential" | the counterexample when it is dropped |
| "as is well known" | the citation |

An emphasis word is admissible only when the sentence it modifies already carries the
checkable claim. If deleting the emphasis loses no information, it was never carrying
any; if deleting it loses the whole point, the point was never stated.
