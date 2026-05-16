# Proof Structure

Dzack-specific conventions for proof presentation.

## Environment Format

Use italic environment names, no numbering.
These are sociological markers — they signal the role of each block to the reader,
creating a parseable structure.
Never omit them.

```markdown
*Theorem.* [Statement here]

*Lemma.* [Statement here]

*Corollary.* [Statement here]

*Proposition.* [Statement here]

*Definition.* [Statement here]

*Example.* [Statement here]

*Remark.* [Statement here]

*Exercise.* [Statement here]
```

Proof delimiters:

```markdown
*Proof.*
[numbered steps]
∎
```

## Step Structure Rules

- **One operation per step.** Each step contains exactly one mathematical operation or
  deduction.
- **Implication chains.** Use `⇒` between related steps.
- **Justifications required.** Every non-definition step ends with `[By ...]`.

### Justification Format

```
[By <reason>]
```

| Reason Type | Example |
| --- | --- |
| Definition | `[By definition]` |
| Algebra | `[Algebra]` |
| Induction hypothesis | `[Induction hypothesis]` |
| Previous result | `[By Lemma 3.2]` |
| Theorem | `[By the Fundamental Theorem of Arithmetic]` |
| Closure property | `[Closure of ZZ under +, *]` |
| Assumption | `[Assume ...]` |

## Variable Tracking

When introducing new variables, specify type and constraints in the same line:

- **Good:** "Let `n ∈ NN` be odd.
  Then `∃k ∈ NN` such that `n = 2k + 1`"
- **Good:** "Let `m = 2k² + 2k`. Since `k ∈ ZZ`, `m ∈ ZZ` [Closure of ZZ under +, *]"
- **Bad:** "Let `n` be odd.
  Then `n = 2k + 1`" (k is unbound)
- **Bad:** "`m = 2k² + 2k ∈ ZZ`" (m was never introduced)

## Assumption Management

Mark assumptions explicitly:

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
| Proof by contrapositive | Show `¬Q ⇒ ¬P`, then `[By contrapositive]` |
| Direct proof | Conclude with the desired statement |
| Case analysis | After all cases, `[Cases exhaustive, result holds in all]` |

## Case Analysis

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

- [ ] All cases are listed
- [ ] Cases are mutually exclusive (no overlap)
- [ ] Cases are jointly exhaustive (cover all possibilities)
- [ ] Each case concludes with the desired result
- [ ] Final step notes that cases are exhaustive

## Common Pitfalls

| Pitfall | Example | Fix |
| --- | --- | --- |
| Unbound variable | "`n = 2k + 1`" (k not introduced) | "`∃k ∈ ZZ` such that `n = 2k + 1`" |
| Missing justification | "`x + y ∈ 2ZZ`" (why?) | "`x + y = 2(k+m) ∈ 2ZZ` [Closure under +]" |
| Multi-operation step | "`n² = (2k+1)² = 4k²+4k+1 = 2(2k²+2k)+1 ∈ 2ZZ+1`" | Split into 3-4 separate steps |
| Implicit assumption | "Since G is abelian..." (not stated) | "Let G be an abelian group. Then..." |
| Non-exhaustive cases | Only proving the easy case | List all cases; verify exhaustiveness |
| Missing base case | "By induction..." (no n=0 check) | Always verify base case separately |
