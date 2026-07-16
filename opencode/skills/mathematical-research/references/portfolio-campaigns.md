# Portfolio Campaigns and Proving Swarms

Owner file for research programs that attack **many problems at once** — a
portfolio sweep over a problem catalog, or a distributed swarm of untrusted
prover agents. Parent: [[mathematical-research/SKILL|mathematical-research]].
Single-campaign dispatch is
[[mathematical-research/references/cdc-prompt|cdc-prompt]]; this file owns the
scale pathologies. Grounded in `neelsomani/gpt-erdos` (677 triaged candidate
solutions), `przchojecki/agentic-erdos` (632-problem portfolio),
`agenticsnz/unsorry` (verifier-gated swarm, ~9k commits, red-teamed), and the
`no-way-labs/residue` two-agent orchestration logs.

## Candidate-claim records

A candidate solution is a typed record from the moment it exists, before any
verification:

- **Freeze the raw transcript, not a cleaned writeup.** The record links the
  exact generation transcript; the candidate text is the unedited model
  output, hedges intact. Polishing before review destroys the tells a
  reviewer needs.
- **Tri-state verification fields**: `manually_verified` and
  `formally_verified` are each `null | true | false` — "not yet reviewed" is
  a distinct state from "reviewed and false".
- **Refutation names the load-bearing false step**, not "didn't hold up":
  "assumes equality of densities forces a 1D compact abelian factor."
- **Novelty is a separate axis from correctness** (`prior_solution` field): a
  valid proof may be a literature rediscovery.
- **Record expert disagreement instead of resolving it** — two named
  reviewers' conflicting verdicts both stay on the record.
- **Record contamination timing**: a solve produced after the problem was
  publicly solved is flagged as contaminated, not counted.

## A green "valid" is one axis of several

The dominant failure buckets in the largest honest catalog are not wrong
proofs — they are non-useful valid ones. Tier candidates by **failure mode**,
not by a confidence score:

| bucket | what it means |
|---|---|
| exact literature solution | correct, already published — a search result, not a result |
| solved-as-stated, hidden constraints | the informal statement omits constraints experts assume; the "solution" answers the wrong reading |
| valid but non-improving | correct proof, weaker than or equal to known results |
| conditional on conjectures | quietly leans on an unproved conjecture |
| subtle error | the classic case — one load-bearing false step |

Every claimed win answers three questions beyond validity: novel? improving?
unconditional?

## Portfolio state is typed, never prose

- Per-problem state lives in **deliberately written typed fields**, validated
  by a linter — never inferred by regex over narrative notes. The observed
  failure: a README "resolved" count computed by matching prose like
  `page status is **proved**`, which silently changes when wording does.
- **Template-generated "attempts" are padding, not reasoning.** A portfolio
  advertising "632 problems attempted" where each attempt is a
  keyword-matched canned `strategy + hardPart` string is Mad-Libs metadata.
  Detection: one fixed `*_method` tag or identical boilerplate across
  problems. Count only per-problem work with evidenced reasoning.
- **Phase-switch with anti-drift guards.** When a problem moves from
  exploration to proof, say so and enforce it: no new computations, empirical
  evidence is not proof progress, and every blocking lemma must be a specific
  quantitative missing estimate ("need X ≤ Y(N) at scale N^{-2}"), not a
  narrative.
- Cheap triage signal that works: **citation recency** — problems whose
  latest reference is decades old (or that have none) are where an agent has
  a chance; anything with post-2000 activity is a specialist's frontier.

## Contamination and community dedup

- **Gate effort on the upstream tracker's live per-problem state** before
  spending compute: only attack problems whose source page is still open
  *and* whose discussion thread shows no solution activity; record the check
  date, and re-check — other agents' solves land weekly.
- **Novelty is timestamped and revocable.** "Absent from the library" is a
  machine pre-filter, not proof of novelty: a name-grep cannot see a renamed
  duplicate, and a target proved today can be upstreamed tomorrow. Record the
  exact library revision the novelty claim was checked against.
- **Quarantine benchmark cohorts.** Imported benchmark suites (Putnam, IMO,
  miniF2F) are a segregated cohort kept out of organic progress metrics; a
  system that selects on benchmark solves contaminates itself silently.

## Swarm anti-gaming invariants

From a red-teamed autonomous-merge system (9/9 attack PRs blocked):

- **Gate separation is absolute**: a hygiene/coordination gate can never
  admit anything into the trusted library; only the kernel gate does. A
  coordination artifact passing review says nothing about mathematical truth.
- **A PR must not be able to edit its own gate**: the files defining gates,
  workflows, and verification tooling carry mandatory human code-owner
  review even under autonomous merge.
- **Statement immutability and defeq binding** stop restate-the-goal attacks
  — [[mathematical-research/references/statement-fidelity|statement-fidelity]].
- **The DoS surface of a verifier-gated system is verifier capacity, not
  correctness.** Duplicate junk proofs waste compute, never soundness — so
  meter *admission* (a governor dispatching from a queue as capacity allows),
  and **measure waste before building coordination machinery** (a read-only
  duplicate-work metric gates whether a dedup lease is worth building).
- **Infra noise must never demote the math.** A quota outage or a failed
  mechanical recompose is not evidence against a goal: floor the priority of
  goals with proved subtrees so they cannot be buried, and keep "evidence
  against the statement" and "my infrastructure flaked" as separate signals
  — the portfolio-scheduler form of "failure is not evidence"
  ([[mathematical-research/references/claim-status|claim-status]]).
- **Failure reshapes the queue**: a goal that resists its proof budget is
  split into claimable sub-lemmas rather than retried or abandoned — the
  queue continuously reshapes toward what the swarm can actually prove.
- **Select reuse-greedy**: prefer claimable goals with the smallest gap
  between their dependencies and the already-proved library, so every proven
  lemma makes the next one cheaper.
- **Provenance-tag the solver.** A deterministic template/CAS solver is
  legitimate but attributed as such; anonymous fixtures are refused; problem
  *sourcing* earns credit on a separate ledger from problem *solving*.
- Coordination can ride git itself: claims as files on a dedicated branch,
  first-push-wins via atomic non-fast-forward rejection, TTL reaping — no
  server, no lock service.

## Cross-agent transfer

From a two-agent (symbolic + computational) orchestration that solved the odd
case of a Knuth problem:

- **Transfer artifacts in the recipient's native representation.** The
  orchestrator converted raw solutions into the receiving agent's coordinate
  system before handing them over; recognition was immediate. Raw dumps in
  the producer's format are noise.
- **Time transfers to stall, not to availability.** Handing over another
  agent's artifacts *before* the recipient has exhausted its own approach
  adds noise; the same artifacts after a stall get read.
- **Transferred tools get adapted, and the adaptation is an artifact.** The
  recipient seeded the transferred search tool with its own structural
  predictions — theory-guided search faster than either input; log the
  adaptation, not just the transfer.
- A failure report must **name the approach class it kills** and why ("any
  approach relying on [property] hits the same obstacle because [reason]") —
  register discipline in
  [[mathematical-research/references/computation|computation]].
