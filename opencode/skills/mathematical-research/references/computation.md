# Computational Experiments

Owner file for search, certificate, and verification computations in a research
program. Parent: [[mathematical-research/SKILL|mathematical-research]]. Tool selection
(which solver/CAS) belongs to [[theorem-proving-and-counterexamples/SKILL|theorem-proving-and-counterexamples]],
[[integer-programming/SKILL|integer-programming]], and [[sagemath/SKILL|sagemath]];
this file owns the protocol around any of them. Concrete M2/Lean/Z3 idioms:
[[mathematical-research/references/computer-algebra-patterns|computer-algebra-patterns]].

## Before launching anything

- Write the mathematical purpose of the run in one sentence. No purpose statement, no
  launch.
- Check the current theory first: never spend compute on cases already retired by a
  theorem. After every theoretical advance, re-scope pending arrays and cancel retired
  lanes — the observed waste pattern is search arrays still grinding on rows a proof
  had eliminated.
- Encode the minimal question. When a case resists (timeout, blowup), check whether the
  encoding proves more than the frontier needs; a smaller direct encoding of the actual
  target claim often closes a case that a stronger intermediate encoding cannot.
- Run a small representative case first; size memory and wall time from measured runs,
  not guesses. Use job arrays for independent cases.
- Verify the run is bounded and its output filename is unique before starting.
- Long jobs must checkpoint. A multi-hour job that cannot checkpoint gets redesigned
  into bounded batches before launch, not relaunched after each loss.
- Use exact arithmetic everywhere (integer/bitvector models, exact rings); never
  floats in anything evidence-bearing.

## Gates before queries

A claim built on code is void unless the code passed its gates in the same log:

- **Well-formedness gates** run before any mathematical query: check the encoded
  structure against an independent concrete model (full multiplication/carry tables,
  torsion, associativity over the whole basis), ending in an exact banner
  (`ALL RING CHECKS PASSED`). If a gate fails, the code is wrong — stop; do not
  reinterpret the mathematics.
- **Positive control** (`expect sat`): before the real query, run a sanity instance
  that must be satisfiable. If it is not, print a refusal
  (`STOP sanity did not return SAT; no mathematical verdict`) and emit no verdict.
- **Ablation control**: at least one deliberately weakened encoding (an axiom block
  dropped) where a witness provably exists and must be found. An encoder that has
  never found anything proves nothing by returning UNSAT.
- **Cross-tactic check**: rerun representative cases under a different solver tactic
  or backend.
- **Witness re-validation**: every SAT model is re-checked outside the solver by
  exact arithmetic against the original equations before being called a candidate.
- **Negative assertions**: verifiers also assert that designated quantities are
  *nonzero* (`assert(x != 0)`), so a check cannot pass by everything collapsing to
  zero.

Record control runs in the run ledger with their own classification
(`encoding_control`, `cross_tactic_check`). Banking a result additionally requires a
cross-implementation audit —
[[mathematical-research/references/adversarial-audit|adversarial-audit]].

## Run ledger

Record every experiment as a row in `RUNS.tsv`:

```tsv
run_id	kind	location_or_job	source_hash	status	elapsed_or_freeze	maxrss	classification	notes
```

plus host, software versions, parameters, and commit hash (or SHA-256 of the driver
when outside git). A computation that cannot be pointed to is not evidence.

Discipline for live jobs:

- Long jobs write intermediate results incrementally.
- Never modify a source file associated with a running job.
- Never resubmit a failed job without diagnosing the failure.
- On clusters: nothing substantive on login nodes; submit through the scheduler; record
  job IDs; read the scheduler's accounting (state, elapsed, max RSS, exit code) before
  classifying the outcome. Never claim a job ID that does not exist.

## Truth sources

Discovery computations are not truth sources. The proven pipeline:

1. **Discover** with whatever is effective — universal charts in a CAS, Groebner
   elimination, SAT/SMT sweeps, invariant optimization.
2. **Re-verify** the found object in the smallest exact model: finite enumeration,
   exact integer arithmetic, a self-contained dependency-free script that checks every
   axiom coefficient by coefficient.
3. **Demote** the discovery computation to historical record. The small exact check is
   the citable truth source; the 600-dimensional chart that found it is not.

Supporting rules:

- Stratify searches by semantic invariants (dimension vectors, Hilbert functions, fiber
  types), and keep a case map (an evidence-map TSV) in which every enumerated case ends
  in a terminal status. "Sweep finished" without a per-case map is not closure.
- Make the case universe enumerated and named up front, and print the task→case
  mapping formula in every log so an auditor can re-derive it. Case status is a
  closed vocabulary (`closed UNSAT | vacuous | SAT candidate | unknown | incomplete |
  error`), and a case closes only when **all** of its subtasks hold terminal negative
  verdicts.
- Prefer quantifier-free finite encodings: unroll the finitely many shifts/cases
  explicitly rather than trusting solver quantifier handling.
- Optimize a semantic invariant of the object, not the superficial size of its
  presentation.
- Lift graded, truncated, or specialized discoveries back to exact equations before
  claiming anything: the phenomenon may live in exactly the terms the simplification
  discards (torsion carries, inhomogeneous corrections, constant terms).
- Separate solver-dependent claims (minimality, uniqueness from an UNSAT) from
  unconditional existence claims; see [[mathematical-research/references/claim-status|claim-status]].

## Audit scripts

The auditor is a different artifact from the searcher, and it distrusts everything it
audits:

- Read-only over frozen logs/results; standard-library-only where feasible, and it
  never launches the solver whose output it audits.
- Hashes every source dependency of the run and requires the log's embedded hash
  manifest to match byte-for-byte; recomputes aggregate digests from individual
  entries so a forged summary line is caught.
- Re-derives structural facts instead of trusting the log's self-description: the
  task→case mapping is recomputed from the formula, command lines are re-parsed and
  each flag checked against the task's expected options, banner presence, uniqueness,
  and order are enforced, and redundant channels (per-case verdict line vs summary
  field) are cross-checked against each other.
- Pins expected tool versions and asserts hard-coded numeric fingerprints (rank
  tables, counts) — asserted, not merely printed.
- Ends in one exact, documented PASS banner line, e.g.
  `AUDIT PASS six_of_six_H0_SAT_and_direct4_UNSAT errors=0 unknown=0 SAT=0`.
  Any other terminal state is a failure; strict mode exits nonzero on any unexpected
  log state instead of skipping it.
- One parameterized auditor per log format. Forking a near-copy of an auditor per
  case stratum is an observed failure: the copies drift apart.

Record each auditor's invocation and expected banner in `BUILD_AND_VERIFY.md`
([[mathematical-research/references/handoff|handoff]]) so any future agent can replay
the program's entire evidence base in minutes.

## Naming and what gets committed

- Filenames encode role, parameters, and date: role prefix
  (`audit_` checks an existing artifact, `search_` is an existential sweep,
  `verify_` certifies a named construction, `independent_`/`*_indep_audit_` is a
  third-party re-derivation, `compare_` bridges two tools), parameters in the stem,
  `_YYYYMMDD` suffix on session-specific work, no date on stable infrastructure.
- Scripts named `sample`, `search`, or `probe` are exploratory unless their log
  explicitly records a completed full enumeration — never cite them as exhaustive.
- Git keeps sources, manifests, ledgers, and concise conclusions. Logs, containers,
  and generated results stay out — except frozen terminal evidence logs selected by
  an auditor, which are evidence.
- Every evidence-bearing log carries its own provenance banner stack: exact command,
  per-source SHA-256, interpreter and solver versions, gate PASS lines, per-case
  verdict lines, summary, and a terminal resource line (`elapsed`, `maxrss`,
  platform) plus `DONE`.
