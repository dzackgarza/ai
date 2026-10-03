# Formalization Patterns

Dzack-specific paired examples: mathematical prose alongside Lean 4 code.
Match informal proof structure line-for-line where possible.

## Core Translation Principles

1. **Explicit Types:** Always specify the type of every object.

   - Instead of: “Let a be an element …”

   - Write: “Let `a ∈ R...`” or “Let `a : R...`”

2. **Quantify Variables:** Make all quantifiers explicit.

   - Instead of: “`x + y = y + x`”

   - Write: “`∀x, y ∈ G: x + y = y + x`”

3. **State Assumptions:** Include all necessary hypotheses.

   - Instead of: “Since G is abelian …”

   - Write: “Let G be an abelian group.
     Then …”

4. **Use Standard Names:** Match Lean’s naming conventions.

   - `monoid` → `Monoid`

   - `is_subgroup` → `IsSubgroup`

   - `ring_hom` → `RingHom`

5. **Structure Proofs:** Follow Lean’s proof term structure.

   - Use “have” for intermediate results

   - Use “suffices” to break down goals

   - Use “by_cases” for case analysis

## Pattern: Even Numbers Form an Ideal

### Mathematical Style

*Lemma.* `2ZZ` is an ideal of `ZZ`.

*Proof.*

1. Let `x, y ∈ 2ZZ`. Then `∃k, m ∈ ZZ` such that `x = 2k`, `y = 2m`.

2. `⇒ x + y = 2k + 2m = 2(k+m) ∈ 2ZZ` [Closure under +]

3. `∀r ∈ ZZ: r x = r(2k) = 2(rk) ∈ 2ZZ` [Absorption]

4. `⇒ 2ZZ` is an ideal of `ZZ` [By definition]

### SageMath Verification

```python
# SageMath verification
k, m = var('k m')
x, y = 2*k, 2*m  # Even numbers
assert x + y == 2*(k + m)  # Closed under addition
assert x * (2*k + 1) == 2*(2*k^2 + k)  # Absorbs multiplication
```

* * *

## Pattern: Square of Odd Number

### Mathematical Style

*Theorem.* The square of an odd integer is odd.

*Proof.*

1. Let `n ∈ 2ZZ + 1`. Then `∃k ∈ ZZ` such that `n = 2k + 1`.

2. `⇒ n² = (2k + 1)² = 4k² + 4k + 1 = 2(2k² + 2k) + 1` [Algebra]

3. Let `m = 2k² + 2k`. Since `k ∈ ZZ`, `m ∈ ZZ` [Closure of `ZZ` under +,*]

4. `⇒ n² = 2m + 1 ∈ 2ZZ + 1` [Definition of odd]

5. `⇒` The square of an odd integer is odd [Conclusion]

### SymPy Verification

```python
from sympy import symbols, expand
k = symbols('k', integer=True)
n = 2*k + 1  # Odd number
assert expand(n**2) == 4*k**2 + 4*k + 1 == 2*(2*k**2 + 2*k) + 1
```

* * *

## Pattern: Generic Induction Template

### Lean 4 Template

```lean
-- Lean 4 example
theorem example_by_induction (n : ℕ) : P n := by
  induction n with
  | zero => /- base case -/
  | succ k ih => /- inductive step -/
```

### SageMath Verification Template

```python
# SageMath verification
def verify_induction(max_n=10):
    # Base case
    assert P(0), "Base case failed"

    # Inductive step
    for n in range(1, max_n + 1):
        if P(n-1):  # Induction hypothesis
            # Show P(n) follows
            pass  # Implementation depends on P
        else:
            assert False, f"Induction failed at n={n}"
```

* * *

## Pattern: Induction

### Mathematical Style

*Theorem.* For all `n ∈ NN`, `2ⁿ > n`.

*Proof.* By induction on `n`.

- [Base] For `n = 0`: `2⁰ = 1 > 0`.

- [Inductive] Assume `2ᵏ > k` for some `k ≥ 0`. Then `2ᵏ⁺¹ = 2 · 2ᵏ > 2k ≥ k + 1` since
  `k ≥ 0`.

### Lean 4

```lean
theorem two_pow_gt_n (n : ℕ) : 2^n > n :=
  by
  induction' n with k ih
  · -- Base case
    norm_num
  · -- Inductive step
    rw [Nat.pow_succ]
    have : 2 * k ≥ k + 1 := by omega
    exact lt_of_lt_of_le (mul_lt_mul_left' ih 2 (by norm_num)) this
```

### SageMath Verification

```python
def verify_two_pow_gt_n(max_n=20):
    for n in range(max_n + 1):
        assert 2**n > n, f"Failed at n={n}"
    return "All tests passed"

verify_two_pow_gt_n()
```

## Pattern: Contradiction

### Mathematical Style

*Theorem.* `√2` is irrational.

*Proof.* Assume `∃m, n ∈ NN` with `n ≠ 0` and `m.coprime n` such that `m² = 2n²`. Then
... [contradiction].

### Lean 4

```lean
theorem sqrt_two_irrational : ¬ ∃ (m n : ℕ), n ≠ 0 ∧ m.coprime n ∧ m^2 = 2 * n^2 :=
by
  rintro ⟨m, n, hn, h_cop, h⟩
  -- Proof by contradiction...
```

### SageMath Verification

```python
def is_perfect_square(n):
    return int(n**0.5)**2 == n

# Check that √2 is not rational (for small denominators)
for d in range(1, 1000):
    assert not is_perfect_square(2 * d * d), f"√2 is rational with denominator {d}"
```

## Pattern: Existence

### Mathematical Style

*Lemma.* In a field, every non-zero element has a multiplicative inverse.

*Proof.* Let `a ≠ 0`. Then `a⁻¹` exists and `a · a⁻¹ = 1`.

### Lean 4

```lean
-- Existence of inverse in a field
example {α : Type} [Field α] (a : α) (ha : a ≠ 0) : ∃ b, a * b = 1 :=
  ⟨a⁻¹, mul_inv_cancel ha⟩
```

### SageMath Verification

```python
# Finding multiplicative inverse in GF(p)
p = 7  # prime field
F = GF(p)

for a in F:
    if a != 0:
        b = a^-1  # inverse exists for non-zero elements
        assert a * b == 1, f"Inverse failed for {a}"
```

## Pattern: Definitions

### Mathematical Style

Let G be a group. A subset `H ⊆ G` is a *subgroup* if:

1. `e ∈ H` (contains identity)

2. `∀a, b ∈ H: ab ∈ H` (closed under multiplication)

3. `∀a ∈ H: a⁻¹ ∈ H` (closed under inverses)

### Corresponding Lean 4

```lean
class Subgroup (G : Type) [Group G] (H : Set G) : Prop where
  one_mem : (1 : G) ∈ H
  mul_mem {a b} : a ∈ H → b ∈ H → a * b ∈ H
  inv_mem {a} : a ∈ H → a⁻¹ ∈ H
```

## Pattern: Theorems and Proofs

### Mathematical Style

*Theorem.* Every finite integral domain is a field.

*Proof.* Let R be a finite integral domain and let `0 ≠ a ∈ R`.

1. Define `φ_a: R → R` by `x ↦ ax`.

2. `φ_a` is injective since R is a domain.

3. Since R is finite, `φ_a` is also surjective.

4. Thus, `∃b ∈ R` such that `ab = 1`.

5. Therefore, `a` has an inverse in R.

### Corresponding Lean 4

```lean
theorem finite_domain_is_field (R : Type) [Ring R] [IsDomain R] [Fintype R] : Field R :=
  { exists_pair_ne := ⟨0, 1, zero_ne_one⟩
    mul_inv_cancel := fun a ha => by
      have : Function.Bijective (fun x => a * x) :=
        (injective_mul_left_iff_ne_zero (id ha : a ≠ 0)).bijective_of_finite_surjective
          (fun x => ⟨a * x, rfl⟩)
      let ⟨b, hb⟩ := this.surjective 1
      ⟨b, hb.symm⟩
    ..‹IsDomain R›, (inferInstance : CommRing R) }
```

## Pattern: Group Theory (Cosets and Normality)

### Mathematical Style

*Lemma.* Let G be a group and `H ≤ G`. If `[G:H] = 2`, then `H ⊲ G`.

*Proof.*

1. Let `g ∈ G`. We show `gH = Hg`.

2. **Case 1:** `g ∈ H`. Then `gH = H = Hg`.

3. **Case 2:** `g ∉ H`. Then `G = H ∪ gH = H ∪ Hg`.

4. Since `[G:H] = 2`, these are disjoint unions.

5. Thus `gH = G \ H = Hg`.

### Corresponding Lean 4

```lean
theorem index_two_normal (G : Type*) [Group G] (H : Subgroup G)
    (hH : Fintype.card (G ⧸ H) = 2) : H.Normal :=
  ⟨fun g => by
    by_cases h : g ∈ H
    · simp [h, Subgroup.mem_carrier, Subgroup.mul_mem_cancel_right H h]
    · have := (Fintype.bijective_iff_injective_and_card
          (fun x => g • x) (by simp)).mp (mul_action.bijective g)
      rw [←Fintype.card_congr (Equiv.Set.compl _)] at hH
      have : {x // x ∈ H} ≃ {x // x ∉ H} := by
        refine Equiv.ofBijective _ ?_
        exact Set.BijOn.bijective (by {
          -- Proof that multiplication by g is a bijection between H and its complement
          -- Implementation details omitted for brevity
          })
      -- Rest of the proof...
  ⟩
```

## Pattern: Sum Formulas (Verification)

### Mathematical Style

*Theorem.* For all `n ∈ NN`, the sum of the first `n` odd numbers equals `n²`.

### Lean 4 Proof

```lean
theorem sum_odds (n : ℕ) : (∑ k in Finset.range n, (2 * k + 1)) = n ^ 2 :=
  by
  -- Base case
  cases n with
  | zero => simp
  | succ n ih =>
    -- Inductive step
    rw [Finset.sum_range_succ, ih, Nat.succ_eq_add_one]
    ring
```

### SageMath Verification

```python
# Verify sum of first n odd numbers equals n²
def verify_sum_odds(max_n=10):
    for n in range(1, max_n + 1):
        odd_sum = sum(2*k + 1 for k in range(n))
        assert odd_sum == n**2, f"Failed at n={n}"
    return "All tests passed"

verify_sum_odds()
```

## Formalization Checklist

- [ ] All variables have explicit types

- [ ] All quantifiers are explicit (∀, ∃)

- [ ] All hypotheses are stated in the theorem/lemma header

- [ ] Proof structure matches the informal version line-for-line

- [ ] Standard library names are used (Monoid, IsSubgroup, RingHom, etc.)

- [ ] Base case is verified for induction proofs

- [ ] Case analysis is exhaustive

- [ ] No sorrys or placeholders in final code

- [ ] SageMath verification code includes assertions

- [ ] Lean code compiles (lake build passes)
