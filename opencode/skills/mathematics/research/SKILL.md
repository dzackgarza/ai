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
human-verified formal release of the corrected Erdős 796 asymptotic). Dispatch-side
grounding comes from OpenAI's published Cycle Double Cover campaign prompt
([[mathematics/research/references/cdc-prompt|cdc-prompt]]); statement-fidelity and
portfolio discipline from the 2026 Erdős-resolution ecosystem — the
`leanprover/comparator` repos around Alpöge's unit-distance disproof
(`kim-em/erdos-unit-distance`, `plby/Erdos90`), `davidturturean/erdos-870`/`-696`,
`nick-kuhn/erdos-619`, the `agenticsnz/unsorry` swarm, and the
`neelsomani/gpt-erdos` candidate catalog.

Before substantive work, read
[[mathematics/research/references/worked-example|worked-example]] — the concrete
program these rules come from, kept concrete on purpose: the working register is
socle classes, power words, and Gröbner normal forms, and every rule below is
illustrated there with the real mathematics that motivated it. The causal layer —
the cognitive defects each rule is a prosthetic for, and the audit heatmap they
imply — is [[mathematics/research/references/epistemic-defects|epistemic-defects]];
read it before auditing anything, and whenever you are tempted to bend a rule.

## Core invariants (always on)

1. **Every claim is typed, scoped, and caveated.** One machine-readable claim ledger
   is canonical; prose defers to it. Proved, computed-within-bounds,
   solver-conditional, conjectured, open, and false are distinct statuses that never
   blur — see [[mathematics/research/references/claim-status|claim-status]].
2. **Computational failure is never mathematical evidence.** Timeout, OOM, crash,
   missing output, nonzero exit: all inconclusive, always. Symmetrically, a positive
   hit is a candidate for re-validation, not a result.
3. **No banking without an audit.** A result enters the ledger as trusted only when a
   separate audit artifact exists — an independent re-derivation by a different
   agent, not a rerun — see
   [[mathematics/research/references/adversarial-audit|adversarial-audit]].
4. **A theorem in a report is not evidence.** Before citing or extending any claimed
   result, open its log and find the terminal verdict lines for every case it names.
5. **Never claim more than the tool gives.** A solver verdict over one finite
   structure, an exact certificate over a parametric family, and a hand proof
   license different quantifiers — see
   [[mathematics/research/references/claim-status|claim-status]].
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
| Start substantive work in this skill; calibrate to the research register | [[mathematics/research/references/worked-example|worked-example]] |
| Audit a finished result; allocate review attention; decide whether a rule applies to a novel situation | [[mathematics/research/references/epistemic-defects|epistemic-defects]] |
| State, promote, or demote a claim; write a report or results section | [[mathematics/research/references/claim-status|claim-status]] |
| Launch a search, sweep, or verification run; write an audit script | [[mathematics/research/references/computation|computation]] |
| Write Macaulay2/Lean/Z3 verification or search code | [[mathematics/research/references/computer-algebra-patterns|computer-algebra-patterns]] |
| Bank a result; review another agent's push; check a literature theorem | [[mathematics/research/references/adversarial-audit|adversarial-audit]] |
| End a session; enter a program; write or receive a handoff | [[mathematics/research/references/handoff|handoff]] |
| Organize the repo; stage manuscripts; formalize; publish | [[mathematics/research/references/program-shape|program-shape]] |
| Release a formalization; audit formal dependencies; freeze statements | [[mathematics/research/references/formal-release|formal-release]] |
| Formalize a problem statement; guard against misformalization; resolve a problem negatively | [[mathematics/research/references/statement-fidelity|statement-fidelity]] |
| Dispatch agents at an open problem; write a solver-campaign prompt | [[mathematics/research/references/cdc-prompt|cdc-prompt]] |
| Attack many problems at once; run or join a proving swarm; triage candidate LLM solutions | [[mathematics/research/references/portfolio-campaigns|portfolio-campaigns]] |

## Problem-statement documents vs. ongoing-research workflow

Two different things share this skill. Confusing them produces a diluted
submission document or a workflow that reads like a problem statement.

**Problem-statement documents** are standalone mathematical artifacts
meant to be **submitted to a long-horizon remote worker** (GPT Pro, a
frontier-model campaign, etc.). They are almost purely mathematical:
definitions, the exact completion contract, domain-specific dos and
do-nots, the adversarial checklist for *this* problem. Their entire job
is to tell the remote worker *what counts as solving this problem* and
*what does not*. Exemplars (read the verbatim prompt sections only when
authoring a new submission):
[[mathematics/research/references/cdc-prompt|cdc-prompt]]
(Cycle Double Cover conjecture),
[[mathematics/research/references/jacobian-prompt|jacobian-prompt]]
(Jacobian Conjecture). These are sibling artifacts for different
problems; they share the template structure described here, not a
parent-child relationship.

A problem-statement document contains:
the object definitions with edge cases resolved; the exact completion
contract stated twice (prose + formal); an explicit insufficiency catalog
naming what does not count as progress; a domain-specific adversarial
checklist of the known failure modes of *this* problem; a termination
contract; and contamination hygiene. It does **not** contain claim
ledgers, handoff bundles, run logs, audit protocols, supersession notes,
or any session state. It is read by a fresh remote worker with no prior
context and no access to the local workflow.

**Ongoing-research workflow** is the local orchestration layer for
multi-session work on a hard problem. The problem statement remains the
organizing touchstone — everything traces back to it — but the workflow
adds rules and artifacts the submission document does not carry: a typed
claim ledger ([[mathematics/research/references/claim-status|claim-status]]),
run logs and computation discipline
([[mathematics/research/references/computation|computation]]),
audit artifacts
([[mathematics/research/references/adversarial-audit|adversarial-audit]]),
handoff bundles
([[mathematics/research/references/handoff|handoff]]),
supersession notes, and git-repo provenance. See the route table above
for the right reference per phase.

**Do not let the workflow layer contaminate a submission document.**
When authoring a problem statement for a remote worker, read only the
verbatim prompt sections of the exemplars and the distilled
problem-statement rules they embody. Do not pull in claim-ledger
taxonomy, handoff structure, audit-protocol rules, or computation
discipline — those are local-workflow concerns and will dilute the
mathematical content the remote worker needs. A submission document
full of procedural rules is a defective submission document.

## Route to subskills

- Mining transcripts, notes, and noisy sources into research state —
  [[mathematics/research/knowledge-extraction/SKILL|knowledge-extraction]]
- Failing test suites that enforce mathematical correctness before implementation —
  [[mathematics/research/mathematical-testing/SKILL|mathematical-testing]]
- Substantive 6-gate review of research code —
  [[mathematics/research/research-gate-review/SKILL|research-gate-review]]

## Route to sibling skills

- Proof presentation (Lamport structured proofs), prose, LaTeX, notation discipline —
  [[mathematics/writing/SKILL|mathematical-writing]]
- Solver and CAS selection (SAT/SMT/ITP/CAS) —
  [[lean4/skills/theorem-proving-and-counterexamples/SKILL|theorem-proving-and-counterexamples]],
  [[mathematics/computation/integer-programming/SKILL|integer-programming]], [[mathematics/computation/sagemath/SKILL|sagemath]],
  [[mathematics/lattices/SKILL|lattices]]
- Lean formalization — [[lean4/skills/lean4/SKILL|lean4]],
  [[lean4/skills/aristotle/SKILL|aristotle]]
- Negative findings and coverage claims —
  [[epistemic-integrity/SKILL|epistemic-integrity]]
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
- A kernel-green proof of a statement that does not mean what the problem says —
  vacuous by `autoImplicit`, silently trivial via junk-value definitions, or a
  weaker nested variant of the headline claim.
- Portfolio "progress" counted from template-generated per-problem prose, or a
  solve counted after the problem was already publicly solved.
- An abstract or README announcing "solved" over a body that admits a
  finite-verified curve fit with the symbolic proof still open.
