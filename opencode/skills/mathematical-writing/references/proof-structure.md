# Proof Structure

Formatting conventions for proof presentation, variable tracking, and justification
style.

## Environment Format

### Theorem Statements

Use italic environment names, no numbering:

```markdown
*Theorem.* [Statement here]

*Lemma.* [Statement here]

*Corollary.* [Statement here]

*Proposition.* [Statement here]
```

### Proof Delimiters

```markdown
*Proof.*
[numbered steps]
∎
```

Or end with a clear conclusion line: "Therefore, [result]."

## Step Structure

### Numbered Steps

Each proof is a sequence of numbered steps:

```markdown
1. Let n ∈ NN.
2. ⇒ n² = (2k+1)² [Algebra]
3. ...
```

Rules for numbered steps:
- **One operation per step.** Each step contains exactly one mathematical operation or
  deduction.
- **Implication chains.** Use ⇒ between related steps.
- **Justifications required.** Every non-definition step ends with [By ...].

### Inline Justifications

Justification format: `[By <reason>]`

| Reason Type | Example |
| --- | --- |
| Definition | `[By definition]` |
| Algebra | `[Algebra]` |
| Induction hypothesis | `[Induction hypothesis]` |
| Previous result | `[By Lemma 3.2]` |
| Theorem | `[By the Fundamental Theorem of Arithmetic]` |
| Closure property | `[Closure of ZZ under +, *]` |
| Assumption | `[Assume ...]` |

### Variable Tracking

When introducing new variables, specify type and constraints in the same line:

- **Good:** "Let n ∈ NN be odd.
  Then ∃k ∈ NN such that n = 2k + 1"
- **Good:** "Let m = 2k² + 2k. Since k ∈ ZZ, m ∈ ZZ [Closure of ZZ under +, *]"
- **Bad:** "Let n be odd.
  Then n = 2k + 1" (k is unbound)
- **Bad:** "m = 2k² + 2k ∈ ZZ" (m was never introduced)

## Assumption Management

### Marking Assumptions

Mark assumptions explicitly when they enter scope:

```markdown
1. [Assume n is composite]
2. Then ∃a, b ∈ NN with 1 < a, b < n such that n = ab [By definition]
3. ...
4. [Discharge assumption: contradiction reached]
```

### Discharge Patterns

| Technique | Discharge Marker |
| --- | --- |
| Proof by contradiction | Reach contradiction, then `[Contradiction]` |
| Proof by contrapositive | Show ¬Q ⇒ ¬P, then `[By contrapositive]` |
| Direct proof | Conclude with the desired statement |
| Case analysis | After all cases, `[Cases exhaustive, result holds in all]` |

## Case Analysis

### Numbering Cases

Always number cases explicitly and verify exhaustiveness:

```markdown
1. Let g ∈ G. We show gH = Hg.
2. **Case 1:** g ∈ H.
   - Then gH = H = Hg [By definition of coset].
3. **Case 2:** g ∉ H.
   - Then G = H ∪ gH = H ∪ Hg [Since [G:H] = 2].
   - These are disjoint unions [Cosets partition G].
   - Thus gH = G \ H = Hg.
4. [Cases exhaustive: either g ∈ H or g ∉ H].
```

### Exhaustiveness Checklist

Before finishing case analysis, verify:
- [ ] All cases are listed
- [ ] Cases are mutually exclusive (no overlap)
- [ ] Cases are jointly exhaustive (cover all possibilities)
- [ ] Each case concludes with the desired result
- [ ] Final step notes that cases are exhaustive

## Proof Techniques Summary

### Direct Proof

```markdown
*Theorem.* P ⇒ Q.

*Proof.*
1. Assume P.
2. ... [reasoning]
3. Therefore Q.
```

### Proof by Contradiction

```markdown
*Theorem.* P.

*Proof.*
1. [Assume ¬P]
2. ... [derive contradiction]
3. [Contradiction reached]
4. Therefore P [By contradiction].
```

### Proof by Induction

```markdown
*Theorem.* ∀n ∈ NN: P(n).

*Proof.* By induction on n.
- [Base] For n = 0: P(0) holds because ...
- [Inductive] Assume P(k) for some k ≥ 0 [Induction hypothesis].
  Then P(k+1) follows because ...
- Therefore ∀n ∈ NN: P(n) [By induction].
```

### Proof by Contrapositive

```markdown
*Theorem.* P ⇒ Q.

*Proof.*
1. We show ¬Q ⇒ ¬P [By contrapositive].
2. Assume ¬Q.
3. ... [reasoning]
4. Therefore ¬P.
5. Hence P ⇒ Q [By contrapositive].
```

## Verifiable Examples

### Example: Even Numbers Form an Ideal

```python
# SageMath verification
k, m = var('k m')
x, y = 2*k, 2*m  # Even numbers
assert x + y == 2*(k + m)  # Closed under addition
assert x * (2*k + 1) == 2*(2*k^2 + k)  # Absorbs multiplication
```

1. Let x, y ∈ 2ZZ. Then ∃k, m ∈ ZZ such that x = 2k, y = 2m.
2. ⇒ x + y = 2k + 2m = 2(k + m) ∈ 2ZZ [Closure under +]
3. ∀r ∈ ZZ: r x = r(2k) = 2(rk) ∈ 2ZZ [Absorption]
4. ⇒ 2ZZ is an ideal of ZZ [By definition]

### Example: Square of Odd Number

```python
# SymPy verification
from sympy import symbols, expand
k = symbols('k', integer=True)
n = 2*k + 1  # Odd number
assert expand(n**2) == 4*k**2 + 4*k + 1 == 2*(2*k**2 + 2*k) + 1
```

1. Let n ∈ 2ZZ + 1. Then ∃k ∈ ZZ such that n = 2k + 1.
2. ⇒ n² = (2k + 1)² = 4k² + 4k + 1 = 2(2k² + 2k) + 1 [Algebra]
3. Let m = 2k² + 2k. Since k ∈ ZZ, m ∈ ZZ [Closure of ZZ under +, *]
4. ⇒ n² = 2m + 1 ∈ 2ZZ + 1 [Definition of odd]
5. ⇒ The square of an odd integer is odd [Conclusion]

## Common Pitfalls in Proof Structure

| Pitfall | Example | Fix |
| --- | --- | --- |
| Unbound variable | "n = 2k + 1" (k not introduced) | "∃k ∈ ZZ such that n = 2k + 1" |
| Missing justification | "x + y ∈ 2ZZ" (why?) | "x + y = 2(k+m) ∈ 2ZZ [Closure under +]" |
| Multi-operation step | "n² = (2k+1)² = 4k²+4k+1 = 2(2k²+2k)+1 ∈ 2ZZ+1" | Split into 3-4 separate steps |
| Implicit assumption | "Since G is abelian..." (not stated) | "Let G be an abelian group. Then..." |
| Non-exhaustive cases | Only proving the easy case | List all cases; verify exhaustiveness |
| Missing base case | "By induction..." (no n=0 check) | Always verify base case separately |
