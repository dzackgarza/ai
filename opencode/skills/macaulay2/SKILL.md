---
name: macaulay2
description: Use when writing, debugging, or reviewing Macaulay2 (M2) code — Groebner-based verification scripts, local/Artin-chart computations, syzygy or membership certificates, memory-bound GB jobs, batch M2 --script runs, or M2 output consumed by other tools.
---

# Macaulay2

Field-tested M2 idioms from a completed verification-heavy research program
(`github.com/j2d9w5xtjn-png/GrothendieckRankP2`, `m2/` and archived compute scripts).
Only non-obvious material; basic M2 is assumed. Protocol context (when to compute,
what a result may claim): [[mathematical-research/references/computer-algebra-patterns|computer-algebra-patterns]]
and [[mathematical-research/references/computation|computation]].

## Proof primitives

- Make `% G` against `gb` of an ideal **over `ZZ`** the proof primitive for
  mixed-characteristic questions: the strong Gröbner basis over the integers decides
  identities exactly, with no field passage. `(f % G) == 0` proves membership;
  `(f % G) != 0` against a **completed** GB proves nonmembership.
- Assert nonvanishing, not just vanishing: `assert((2*s*W % G) != 0)`. A script with
  only zero-checks passes on a collapsed ring.
- Regular sequence: chain ideal quotients, `assert((J : ideal f) == J)` for each
  successive `f` — nonzerodivisor certificates, no flatness hand-waving.
- Artin local structure by colon ideals: socle as `(I : m)`, Loewy layers as
  `I + m^k == I + ideal(...)` identities, cross-checked by `hilbertFunction` of the
  tangent cone over the residue field.
- Map-stability claims via `isSubset`: a coproduct/antipode/quotient respects an
  ideal iff `isSubset(DeltaMap(K), IT)`; well-definedness of a specialization iff
  `phi(K) == I0`.
- Identities among maps (group laws, coproducts, associativity): adjoin one variable
  copy per tensor factor (`U1,V1,U2,V2`, three copies for associativity) and reduce
  the difference of both routes: `assert(((xLeft - xRight) % GQ) == 0)`.
- `MonomialOrder => Lex` for structured normal forms you intend to read;
  `GRevLex` for the big many-variable checks where you only need zero/nonzero.

## Honesty at the GB boundary

- A bounded computation is not a theorem, and the script itself must say so. Bake
  the epistemic status into the terminal banner:

  ```m2
  if #open == 0 then << "ALL_LOCAL_P4_TARGETS_ZERO branch=" << branchName << endl
  else << "PARTIAL_OR_NONTERMINAL_NO_THEOREM branch=" << branchName << endl;
  ```

  A `gb(J, DegreeLimit => d)` nonzero remainder proves nothing; only membership
  verdicts below the bound, or verdicts against a completed basis, count.
- Distinguish what each computation licenses: a syzygy/membership certificate over a
  parametric `ZZ` chart covers every specialization; a normal form over one finite
  ring covers that ring only.

## Local rings: two routes

- **Mora route**: genuine local orderings via negative weights —

  ```m2
  monoid[Variables => n, MonomialOrder => Weights => splice{n:-1}, Global => false]
  ```

  Standard-basis computations then run at the maximal ideal directly (works over a
  field).
- **Global-certificate route** (preferred over `ZZ`, where Mora is unavailable):
  stay in a *global* polynomial ring and certify localized membership by syzygy —
  build `matrix{{target} | eqs}`, compute `syz`, and select columns whose
  target-coefficient has a **unit constant term** at the origin. A unit-cofactor
  column is an exact membership certificate in the localization at
  `(p, variables)`; no local ordering needed. Keep the witness column
  (`toExternalString witness`) as the durable certificate.

## Memory and scale engineering

- For finite free algebras, skip tensor-product rings entirely: encode
  multiplication and comultiplication as structure-constant tables
  (`Stab = hashTable ...`, lists of 16/64 coordinates) and hand-rolled loops with
  sparsity guards (`if u#i != 0 then ...`). The polynomial ring holds only the
  deformation variables, not the module coordinates.
- Truncated coefficient rings as digit tuples: represent `k[eps]/(eps^3)` elements
  as `{a0,a1,a2}` with explicit `addR`/`mulR` convolution instead of adjoining
  `eps` and reducing repeatedly — removes a whole polynomial ring and its GB from
  peak memory (`certs_lowmem.m2`; its header documents the design).
- Reduce as you go in iterated products: geometric sums as
  `N = (N + power) % GI; power = (power * lambda) % GI` per step, never one giant
  unreduced expression.
- Emit-and-deduplicate while generating equation systems: stream each nonzero
  coordinate into a `MutableHashTable`-backed generator list with a provenance
  label (`"assoc.112.d2"`), instead of materializing the raw redundant list.
- Split independent branches into separate `M2 --script` processes (selected by an
  env var); M2 is single-threaded and per-process peak memory is the binding
  constraint. Step `DegreeLimit` upward across runs rather than retrying a crashed
  full GB.
- Wrap only the expensive call in `elapsedTime`, and `<< "...: " << flush` before
  it so interrupted logs show what was running.

## Pre-flight gates (before the expensive step)

- Probe uncertain APIs in a 10-line scratch script first — e.g. exact lifts via
  `quotient(B, G, DegreeLimit => {d}, MinimalGenerators => false)` versus
  `B // forceGB gens H`, asserting `G*V == B` — before embedding either in a
  multi-hour job.
- Gate the constructed system symbolically, then `error` out on any failure:
  equations vanish at the pinned origin, targets vanish, augmentation preserved,
  and the Jacobian at the closed point (`diff` + constant extraction) has the
  expected rank ("targets have local order ≥ 2"). Print one `GATE ... OK/FAILED`
  line each.
- Run a toy instance of the certificate machinery in-process
  (`toyRow = matrix{{toyTarget, toyGen}}; syz toyRow; assert(...)`) to pin column
  and constant-term conventions before the real syzygy.
- Provide a `GENERATE_ONLY` mode that builds equations and gates but launches no
  GB — cheap to run anywhere, and it separates construction bugs from compute
  failures.

## Script harness conventions

- Scripts are `M2 --script`, assert-driven, sectioned by `print "... PASS"`
  banners, ending in one terminal banner; a failed `assert` aborts with nonzero
  exit, so exit status is the verdict.
- Configure via environment variables, parsed with a portability guard —
  `getenv` returns `""` on some builds and `null` on others:

  ```m2
  envMissing = s -> s === null or (class s === String and #s == 0);
  ```

- Machine-readable interchange: print exact polynomials with `toExternalString`
  between counted sentinels (`EXPORT_EQS_BEGIN count=189` … `E 17 <poly>` …
  `EXPORT_EQS_END`) so an independent parser can demand exact round-trips;
  consumers may truncate only after parsing complete sums.
- Representative-prime audits of uniform-in-`p` constructions: encode the general
  formulas as M2 functions of the parameters and instantiate at one odd prime for
  a bounded exact check, alongside the general hand proof.
- Ablation by ideal: rerun the decisive identities modulo square-zero quotients
  (`gb(K + ideal(2*s))`) to localize which infinitesimal layer creates a
  phenomenon — executable deformation analysis, not commentary.

## Routing

Tool choice among CAS/SMT/ITP:
[[theorem-proving-and-counterexamples/SKILL|theorem-proving-and-counterexamples]].
Run-ledger, cluster, and failure-classification protocol:
[[mathematical-research/references/computation|computation]]. The worked
mathematics these idioms certified:
[[mathematical-research/references/worked-example|worked-example]].
