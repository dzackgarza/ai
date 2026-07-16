---
name: mathematical-research
description: Use when running or joining an agent-driven mathematical research program — attacking an open problem or conjecture, running computational searches for counterexamples or certificates, banking or auditing another agent's mathematical claim, freezing session state for handoff, or preparing verified results for writeup or formalization.
---

# Mathematical Research

Operating discipline for multi-session, multi-agent mathematical research: how claims
are tracked, computed evidence is trusted, results are audited, and state survives
agent handoffs. Distilled from a completed agent-run program (an open-problem
counterexample taken through discovery, independent audits, Lean formalization, and a
mathlib PR handoff: `github.com/j2d9w5xtjn-png/GrothendieckRankP2`) and from a second,
Lean-first program (`github.com/rishigajjala/erdos-796-lean`: a model-generated,
human-verified formal release of the corrected Erdős 796 asymptotic).

Before substantive work, read
[[mathematical-research/references/worked-example|worked-example]] — the concrete
program these rules come from, kept concrete on purpose: the working register is
socle classes, power words, and Gröbner normal forms, and every rule below is
illustrated there with the real mathematics that motivated it.

## Core invariants (always on)

1. **Every claim is typed, scoped, and caveated.** One machine-readable claim ledger
   is canonical; prose defers to it. Proved, computed-within-bounds,
   solver-conditional, conjectured, open, and false are distinct statuses that never
   blur — see [[mathematical-research/references/claim-status|claim-status]].
2. **Computational failure is never mathematical evidence.** Timeout, OOM, crash,
   missing output, nonzero exit: all inconclusive, always. Symmetrically, a positive
   hit is a candidate for re-validation, not a result.
3. **No banking without an audit.** A result enters the ledger as trusted only when a
   separate audit artifact exists — an independent re-derivation by a different
   agent, not a rerun — see
   [[mathematical-research/references/adversarial-audit|adversarial-audit]].
4. **A theorem in a report is not evidence.** Before citing or extending any claimed
   result, open its log and find the terminal verdict lines for every case it names.
5. **Never claim more than the tool gives.** A solver verdict over one finite
   structure, an exact certificate over a parametric family, and a hand proof
   license different quantifiers — see
   [[mathematical-research/references/claim-status|claim-status]].
6. **Discovery is not verification.** Whatever found the object, the citable truth
   source is the smallest exact, self-contained check of it.
7. **Supersede loudly.** Stale documents are named in dated supersession notes and
   do-not-cite lists; nothing is silently edited or silently trusted.
8. **Theory retires compute; compute guides theory.** Before launching searches, check
   what proofs already exclude; after every proof, re-scope running searches.
9. **Frozen state is untrusted until replayed.** Entering a program, run its recorded
   auditors and match the expected PASS banners before believing any claim.

## Route by phase

| You are about to… | Read |
|---|---|
| Start substantive work in this skill; calibrate to the research register | [[mathematical-research/references/worked-example|worked-example]] |
| State, promote, or demote a claim; write a report or results section | [[mathematical-research/references/claim-status|claim-status]] |
| Launch a search, sweep, or verification run; write an audit script | [[mathematical-research/references/computation|computation]] |
| Write Macaulay2/Lean/Z3 verification or search code | [[mathematical-research/references/computer-algebra-patterns|computer-algebra-patterns]] |
| Bank a result; review another agent's push; check a literature theorem | [[mathematical-research/references/adversarial-audit|adversarial-audit]] |
| End a session; enter a program; write or receive a handoff | [[mathematical-research/references/handoff|handoff]] |
| Organize the repo; stage manuscripts; formalize; publish | [[mathematical-research/references/program-shape|program-shape]] |
| Release a formalization; audit formal dependencies; freeze statements | [[mathematical-research/references/formal-release|formal-release]] |

## Route to sibling skills

- Proof prose, LaTeX, notation discipline —
  [[mathematical-writing/SKILL|mathematical-writing]]
- Solver and CAS selection (SAT/SMT/ITP/CAS) —
  [[theorem-proving-and-counterexamples/SKILL|theorem-proving-and-counterexamples]],
  [[integer-programming/SKILL|integer-programming]], [[sagemath/SKILL|sagemath]],
  [[lattices/SKILL|lattices]]
- Lean formalization — [[lean4/skills/lean4/SKILL|lean4]],
  [[aristotle/SKILL|aristotle]]
- Negative findings and coverage claims —
  [[epistemic-integrity/SKILL|epistemic-integrity]]
- Mining transcripts and notes into research state —
  [[knowledge-extraction/SKILL|knowledge-extraction]]
- Literature search and paper writing —
  [[research-discovery/SKILL|research-discovery]],
  [[research-writing/SKILL|research-writing]]
- Durable plans and cross-session memory — [[plan/SKILL|plan]],
  [[agent-memory/SKILL|agent-memory]]

## Failure modes this skill exists to prevent

- A negative *resource* outcome quoted as a negative *mathematical* result.
- A solver verdict promoted to "theorem" with no independently checkable certificate.
- "Complete/closed/all" surviving restatement while the actual coverage was a bounded
  case list under reductions.
- The next agent relaunching retired searches, or repeating a false claim, because a
  stale unmarked handoff said to.
- Compute burned on cases a theorem already excluded.
- An impressive discovery computation cited as proof while no small exact check exists.
- Two agents "agreeing" via reruns of the same code — shared bugs surviving into
  announcements.
- An UNSAT sweep believed although the encoder was never shown able to find a planted
  solution.
- Handoff rot: stacked supersession banners over a stale narrative, and byte-copied
  bundle documents drifting into mutually inconsistent versions.
