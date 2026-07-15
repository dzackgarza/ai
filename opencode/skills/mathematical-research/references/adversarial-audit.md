# Independent Audit

Owner file for banking a mathematical result produced by any agent (including
yourself). Parent: [[mathematical-research/SKILL|mathematical-research]]. Related:
[[reviewing-subagent-work/SKILL|reviewing-subagent-work]] for general agent output,
[[research-gate-review/SKILL|research-gate-review]] for gate protocol; this file owns
what "independently verified" means for a mathematical claim.

## The pairing rule

No result is banked without a separate audit artifact: `X_RESULT` does not change the
claim ledger until `X_AUDIT` exists, written by a different session or agent than the
one that produced the result. The audit is a document with its own verdict, scope, and
caveats — not a sentence of agreement in chat. Keep the seats separate: producer and
auditor rotate, but never coincide on one result.

## The reviewer's first move

**A theorem in a report is not evidence.** Before citing or extending any claimed
result, open its log and check that the terminal verdict lines actually exist for
every case the theorem names — every ring, every coefficient, every row. Reports run
ahead of their evidence; the ledger status belongs to what the logs contain, not to
what the prose asserts. Likewise verify the gates passed in that same log
([[mathematical-research/references/computation|computation]]): a claim whose
well-formedness gates never ran is void regardless of its verdict lines.

## Independent means independent

A rerun of the author's code is a reproduction, not an audit. An audit re-establishes
the result along a genuinely different path:

- **Re-derive from the axioms.** Rebuild the defining equations from the mathematical
  definitions, not from the author's files, then compare: the two systems must agree
  exactly (e.g. set-identical up to sign ⇒ identical ideals).
- **Vary the implementation axes**: different coordinate model or normal form,
  different elimination/pivot convention, different solver tactic or backend,
  different language or library — at least one axis, more for headline results.
- **Compare intermediate invariants, not just verdicts**: dimensions, rank tables,
  Hilbert-type data, case counts. Two implementations that agree on a final boolean but
  were never compared on intermediates share too much undetected error surface.
- **Audit the hand-theory layer separately from all code.** Every lemma the
  computation relies on (exhaustiveness of a recursion, soundness of a truncation,
  completeness of an axiom list) gets checked by hand, independent of every script.

State the resulting trust base explicitly and count it: "N independent equation
derivations, M independent eliminations, plus the hand proofs."

Scope the audit to the result's *expected failure modes* and say which were checked:
"found no division by two, no sign error, no misuse of the power word as a group
homomorphism, no hidden commutativity assumption." An audit that does not name the
failure modes it hunted cannot be assessed. The auditor also gates its own
re-derivation with internal sanity assertions, so a bug shared with the original is
caught inside the audit rather than laundered through agreement.

## Consistency sweep

Check the new claim against every banked prior result. For each prior sweep or theorem
whose scope could overlap, either exhibit the non-overlap explicitly (parameters,
lengths, fibers) or stop: an unexplained contradiction with a banked result is a
stop-the-line event, whichever side is wrong. A new positive result must also explain
*why* prior negative sweeps did not find it.

## Audit verdicts and banking

- **Confirmed (green / banked)**: every checkable claim reproduced by independent
  hand audit plus a machine cross-check; the response document names the acceptance
  ("CORRECT — banked as Theorem BR") and the ledger row updates. Pin the exact scope
  in the verdict ("proves [8]=e, not [4]=e").
- **Confirmed with corrections**: verdict survives but stated reasons or side claims
  are wrong — record the false explanation explicitly so it cannot propagate.
- **Rejected**: include the minimal reproducer of the failure, and route the false
  claim through [[mathematical-research/references/claim-status|claim-status]]
  demotion (erratum + do-not-cite).

Handling a prior agent's false claim takes all three mechanisms, never silent
deletion: (1) retraction with root cause named (the bug, not just the retraction);
(2) provenance policing — check whether a suspect file is a byte-copy of a superseded
draft and cite only the corrected package; (3) a written correction note wherever an
earlier summary overstated the state ("an earlier note said X; the current snapshot
instead says Y").

The auditor's response document ends with prioritized asks for the next agent — the
audit seat owns the frontier update, not just the verdict.

Every audit ends with a **caveats / open items** section listing what was *not*
checked (unverified minimality, missing external-CAS confirmation, attribution not yet
human-verified). An audit without a not-checked list is advertising, not an audit.

## Auditing literature

Treat cited papers like agent output: re-derive the specialization actually used.
When a paper's printed claim is stronger than what its proof supports, use only the
supported statement, record the discrepancy, and ledger the dependency as
`literature_theorem_plus_checked_specialization`.

## Escalation ladder for headline results

For a program-defining claim (a counterexample, a resolved conjecture), escalate the
trust base in order, updating the ledger status at each step:

1. Author's exact small-model verification (self-contained script, exact arithmetic).
2. Second implementation by another agent, different axes as above.
3. Third implementation, different again (this is where remaining shared-error surface
   dies).
4. External CAS/prover confirmation on independent infrastructure.
5. Formalization (Lean/mathlib route via [[lean4/skills/lean4/SKILL|lean4]] or
   [[aristotle/SKILL|aristotle]]) with axiom audit (`#print axioms`) — the terminal
   status `formalized`.

Do not announce externally before at least step 3.
