# Claim Status and Ledgers

Owner file for separating proved statements, computational results, conjectures, and
refuted claims across sessions and agents. Parent: [[mathematical-research/SKILL|mathematical-research]].

## The claim ledger

Maintain one machine-readable claim ledger (`CLAIM_LEDGER.tsv`) at the program root:

```tsv
id	claim	status	scope	primary_artifacts	caveat
C2	Rank-four groups are killed by 8	proved_independently_audited	rank 4, arbitrary base	EXPONENT8 report; audit	Group law may be noncommutative
C16	A rank-four counterexample was found	false	no scope	all audits	No SAT candidate survived
```

- Every substantive claim gets a row, including refuted ones (`false` rows stay).
- Prose documents cite row ids and defer to the ledger; never keep two authoritative
  copies of a claim's status.
- When claims depend on each other, record the dependence (a column or the caveat):
  a downgraded claim must drag its dependents down with it.
- When a ledger is replaced, rename the old one `*_SUPERSEDED` — do not edit history
  silently, and do not leave two files both claiming to be current.

## Status taxonomy

| status | meaning |
|---|---|
| `open` | No proof, no counterexample. Say so plainly. |
| `conjectured` | Stated with heuristic support; the evidence is listed, not implied. |
| `inconclusive` | Computation ran without verdict (timeout, OOM, partial, live snapshot). |
| `bounded_computational_theorem` | Exact finite computation closed a stated finite case list. Scope names the enumeration bounds. |
| `conditional_bounded_computational_theorem` | As above, but under named structural reductions; caveat says "review reduction hypotheses before reuse". |
| `solver_conditional` | Rests on an unreplayed solver verdict (e.g. an UNSAT with no independently checkable certificate). |
| `proved` | Hand proof exists; not yet independently audited. |
| `proved_independently_audited` | Hand proof plus an adversarial audit artifact ([[mathematical-research/references/adversarial-audit|adversarial-audit]]). |
| `literature_theorem_plus_checked_specialization` | Cited theorem whose used specialization was independently re-checked. |
| `formalized` | Machine-checked (Lean etc.); axiom set audited. |
| `false` | Refuted. Row is kept; erratum issued. |
| `superseded` | Subsumed by a stronger result; caveat names the successor. |

Promotion rules:

- `solver_conditional` → `bounded_computational_theorem` only via an independently
  checkable certificate or a second independent implementation.
- `proved` → `proved_independently_audited` only via a written audit artifact, never by
  the prover's own rerun.
- Never delete the qualifier as part of "cleanup". A minimality claim that is
  solver-conditional stays visibly solver-conditional in every document, including the
  final paper, until the certificate exists.

Demotion is loud: when a claim turns out false, write a dated erratum that names every
document repeating the claim, and add those documents to a do-not-cite list.

## Scope discipline

- No claim without a scope column. "Killed by 4" is not a claim; "killed by 4, for
  height-one rank-four groups in characteristic 2" is.
- Quantifiers are load-bearing. Do not let "all", "complete", or "closed" survive a
  restatement whose actual coverage is "the enumerated case list under reductions R1–R3".
- Distinguish the actual target claim from stronger intermediates. A case can be
  "closed for the real question" while an intermediate stronger property stays unknown —
  record both statuses; never merge them into one row.
- Record type-level distinctions that invite misuse in the caveat (e.g. "power *word*
  map, not a homomorphism"; "subgroup chain, not a normal filtration"; "module
  filtration, not a subgroup filtration").
- Literature claims: re-derive the specialization you actually use. Published papers
  contain printed errors; when you find one, record it in the caveat and cite the claim
  as `literature_theorem_plus_checked_specialization`, never as bare truth.

## Failure is not evidence

A timeout, out-of-memory kill, crash, missing output file, malformed or footerless log,
or nonzero exit is **inconclusive**, never a mathematical negative. Classify every run
as exactly one of:

`successful` | `mathematically_negative` | `timeout` | `oom` | `software_failure` | `inconclusive`

Only `mathematically_negative` with a terminal verdict banner may feed a `*_theorem`
ledger row. Negative-finding prose additionally follows [[epistemic-integrity/SKILL|epistemic-integrity]].

Symmetrically, a positive hit (a SAT model, a candidate object) is not yet a result:
it triggers the verification protocol of
[[mathematical-research/references/computation|computation]] — independent
re-validation outside the solver — before it may be stated as anything but a
candidate.

## Never claim more than the tool gives

Different computations license different quantifiers. Keep the strength hierarchy
explicit whenever a result is stated (the program's "Golden Rules"):

1. A solver UNSAT over one exact finite structure excludes counterexamples **over
   that exact structure** — nothing more.
2. An exact certificate over a universal/parametric family (e.g. ideal membership
   with an exact remainder) covers **every** specialization of that family — much
   stronger, and the preferred form.
3. An exact *non*membership certificate is a different statement from "the bounded
   search left a nonzero remainder"; only the former is evidence. Say which one you
   have.

A statement's ledger scope must match the level actually computed, and a report may
never quote a stronger level than its logs support.

## Epistemic register in prose

Match the sentence form to the ledger status, uniformly across reports, notes,
manuscripts, and docstrings:

- **Proved**: flat unconditional statement in a theorem environment. The hand proof is
  the evidence of record; the machine check is corroboration ("the proof above is
  independent of computer algebra; for reproducibility, the companion file …").
- **Audited**: flat declarative verdict up front ("The claim is correct."), then what
  was checked.
- **Solver-conditional**: the condition is in the sentence, not a footnote —
  "Conditional on the recorded Z3 UNSAT verdicts, …".
- **Open/scoped**: box the honest global status so it cannot be skimmed past —
  "length nine is minimal in this bridge family; global length eight remains open."
- **Named gap**: an explicit "remaining proof boundary" section listing the exact
  unproved identities. When a paper and its formalization disagree about whether a
  step is proved, the stricter judgment governs staging
  ([[mathematical-research/references/program-shape|program-shape]]).

## Result report anatomy

Every dated result report follows one template, in order:

1. Title, date, status line (including what the result does **not** prove:
   "theorem-strength hand proof, independently audited — still does not prove the
   conjecture").
2. Headline verdict up front, one sentence.
3. Outcome table over the full case universe, with an explicit no-bad-rows line
   ("SAT candidate: 0; unknown, error, or incomplete: 0; total: 190").
4. Independent evidence check naming at least two agreeing checkers.
5. Resource accounting (summed elapsed, peak RSS).
6. Provenance qualification pre-empting anomalies a future auditor will find
   ("88 historical rc≠0 records are retained deliberately; they are crash artifacts,
   not unresolved outcomes").
7. Hashes of drivers and payloads, with cross-tool agreement stated, plus the log
   glob for reproduction.
8. Mathematical interpretation last, with scope caveats ("a bounded computational
   theorem; it does not by itself resolve arbitrary base length…").

## Three-tier closing ledger in documents

End every substantive report, handoff, and manuscript with three explicit lists:

1. **Unconditional and audited** — safe to build on.
2. **Conditional or scoped** — each with its named hypothesis or solver dependence.
3. **Not proved** — what a hasty reader would wrongly assume is included (global
   minimality, sharpness, unrelated constructions not excluded, attribution not yet
   verified by a human).

The third list is mandatory. Its job is to preempt the specific overclaims the document
makes tempting.
