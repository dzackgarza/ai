# Computer Algebra Patterns: Macaulay2, Lean, Z3

Concrete idioms lifted from the source program's verification code. Parent:
[[mathematical-research/SKILL|mathematical-research]]; protocol context in
[[mathematical-research/references/computation|computation]]; the mathematics these
snippets certify is in
[[mathematical-research/references/worked-example|worked-example]].

## Macaulay2: exact certification over ℤ

Full M2 tool-level idiom catalog (local orderings, syzygy certificates, memory
engineering, script harness): [[macaulay2/SKILL|macaulay2]]. The research-protocol
essentials:

Work in `ZZ[...]` and make `% G` (normal form against a strong Gröbner basis over ℤ)
the proof primitive — it handles mixed characteristic exactly, with no field tricks:

```m2
R0 = ZZ[r,s,MonomialOrder=>Lex];
I0 = ideal(r^3+2, s^3+2, r*s^2);  G0 = gb I0;
assert((4 % G0) == 0);        -- char divides 4
assert((2*s % G0) != 0);      -- the decisive coefficient SURVIVES
```

- **Negative assertions are half the proof.** `assert((2*s*W % G) != 0)` is what
  makes the counterexample a counterexample; a script with only `== 0` checks can
  pass on a collapsed ring.
- **Regular sequences via ideal quotients**: `(J : f) == J` certifies `f` is a
  nonzerodivisor mod `J`; chain them to certify a complete intersection.
- **Local structure via colon ideals**: socle as `(I : m)`, Loewy layers as
  `I + m^k` identities, plus a `hilbertFunction` cross-check of the tangent cone
  over the residue field.
- **Group law as polynomial identities in tensor-copy rings**: adjoin a second copy
  of the generators (`U1,V1,U2,V2`) for coproduct compatibility, a third copy for
  associativity, and assert `((xLeft - xRight) % GQ) == 0`. Hopf-ideal claims are
  `isSubset(DeltaMap(K), IT)` / `isSubset(Smap(K), K)`; counit well-definedness is
  `epsA(K) == I0`.
- **Two routes to the decisive number**: compute `[4]^#` both from geometric sums
  (`N4 = 1+lambda+lambda^2+lambda^3`) and by iterating the square word
  `phi = m ∘ Δ`, and assert both — an internal cross-check inside one script.
- **Ablation by ideal**: re-run key identities modulo square-zero quotients
  (`gb(K + ideal(2*s))`, `gb(K + ideal(r*s))`, `gb(K + ideal(2, r^2*s))`) to pin
  which infinitesimal layer creates each phenomenon — the defect dies in `C/(2s)`,
  normality dies one layer earlier. This is deformation ablation as executable
  documentation.
- **Certify the necessity of correction terms**: lift naively without the bridge
  term and assert that exactly one relation fails with a *computed* nonzero
  curvature (`assert(((rn^2*sn*Vn1*Un2) % Gnaive) != 0)`), proving the term is
  forced rather than decorative.
- Section-banner `print`s (`"BASE PASS"`, … `"ALL CHECKS PASSED"`) make logs
  auditable; a failed `assert` kills the script, so the terminal banner is the
  verdict. Bound heavy jobs (`DegreeLimit`) and remember: a nonzero *bounded-degree*
  remainder is not a nonmembership certificate.
- For cross-tool audits, export fully expanded integer polynomials to plain text;
  the independent implementation re-derives its own system and demands
  set-equality up to sign (⇒ identical ideals), hashing the compared payload.

## Lean 4 / mathlib: formalizing the banked result

- **Nontriviality by witness module, closed by kernel decision.** A quotient
  presentation `R = ℤ[a,b]/(a³,b³,a²b+2)` is not syntactically nontrivial. Certify
  `2b ≠ 0` with an explicit finite model — the regular representation on
  `M = ZMod 4 × ZMod 4 × (Fin 5 → ZMod 2)` with `a`,`b` as explicit
  `AddMonoid.End M` — and close every relation by `decide +kernel`
  (`aEnd ^ 3 = 0`, `aEnd ^ 2 * bEnd + 2 = 0`, `2 * bEnd ≠ 0`). Then
  `Subring.closure {aEnd, bEnd}` receives a ring map from `R`, and the
  nonvanishing pulls back. Pattern: *presentation for structure, finite model for
  nondegeneracy.*
- **Build the algebra from library structure, not raw quotients.** Two nested
  `QuadraticAlgebra`s give `A` with freeness and `finrank R A = 4` compositionally
  (`finrank_B = 2`, `finrank_A_over_B = 2`) instead of by hand-rolled basis
  juggling.
- **Prove polynomial identities once, generically, with `linear_combination`.**
  State each identity over an arbitrary `CommRing S` with hypotheses
  `ha : a^3 = 0`, `hab : a^2*b + 2 = 0`, discharge by explicit cofactors
  (`linear_combination a * hab - b * ha`), and transport along algebra maps. The
  cofactors are exactly the Gröbner certificates the M2 script computed — the CAS
  discovers them, Lean replays them.
- **`abbrev` the generator names** (`aB`, `u₁`, `l₂`) so certificates stay readable
  while unfolding definitionally.
- **Reuse the categorical spine**: power maps as convolution powers of the identity
  (`convPowId`), evaluated by group-like/skew-primitive lemmas into geometric sums;
  the antipode obtained as `[n-1]^#` once `[n]^# = unit ∘ counit`; the group-scheme
  formulation through the Hopf/affine-group antiequivalence rather than a bespoke
  scheme layer.
- **Formalize the consistency checks too**: `not_isCocomm` (Deligne forces
  noncommutativity) and `orderOf_universalPoint = 8` are theorems in the file, not
  prose remarks.
- Ship with the venue's gates: warning-free build under the standard linter set,
  `#lint` clean, `#print axioms` on each main theorem showing only
  `propext, Classical.choice, Quot.sound`, no `sorry`; factor the generic layer
  (convolution powers) into its own upstreamable file and keep the counterexample
  file self-contained. For a public release, the executable audit protocol
  (`--trust=0`, prohibited-token scan, frozen statement hashes) is owned by
  [[mathematical-research/references/formal-release|formal-release]].
- Explicit-constant numerics in the kernel: rational cutoff certificate + tail
  bound via algebraic sandwiches (`log((1+z)/(1−z)) ≥ 2(z + z³/3)` reduces `log p`
  bounds to `norm_num`/`linarith` arithmetic); `decide` only on small finite facts,
  never `native_decide` in a release closure; certificates stated as conditional
  theorems with explicit obligation hypotheses.

## Python / Z3: exact finite decision

- **Rings as bitvector digit tuples with hand-coded carries** — never solver
  integers, never floats:

  ```python
  class Rram:  # Z[pi]/(pi^2-2, pi^3): a + b*pi, a in Z/4, b in Z/2
      def mul(self, x, y):
          a, b = x; c, d = y
          return (a*c + 2*ZeroExt(1, b & d),
                  (Extract(0,0,a) & d) ^ (b & Extract(0,0,c)))
  ```

  Gate the symbolic ring against a concrete carry table on all pairs before any
  mathematical query.
- **Sanity SAT before the real query**, and refuse a verdict without it:
  `if sanity != sat: print("STOP sanity did not return SAT; no mathematical verdict")`.
- **Ablation gates that must be SAT**: drop one axiom block (Δ-multiplicativity) so
  a witness provably exists; the encoder must find it or the encoder is broken.
- **Re-validate every SAT model outside the solver** by exact arithmetic over all
  finitely many shifts before calling it a candidate.
- **Quantifier-free by construction**: unroll the finitely many annihilator shifts
  with `itertools.product` instead of trusting quantifier elimination.
- **Print the task→case mapping formula** (`task_id % 3 + 1`, …) and the universe
  size in every log; auditors recompute the mapping instead of trusting it.
- Emit the full provenance banner stack (command, per-source SHA-256, solver
  version, gate PASSes, per-case verdicts, `PROCESS_RESOURCE`, `DONE`) so the
  stdlib-only log auditor of
  [[mathematical-research/references/computation|computation]] has something to
  verify.

## Choosing the substrate

SMT decides existence over one exact finite ring; Gröbner over ℤ certifies
identities over every base of a given shape; an explicit finite model certifies
nondegeneracy; Lean freezes the banked result. Route selection details:
[[theorem-proving-and-counterexamples/SKILL|theorem-proving-and-counterexamples]],
[[integer-programming/SKILL|integer-programming]], [[sagemath/SKILL|sagemath]],
[[lean4/skills/lean4/SKILL|lean4]].
