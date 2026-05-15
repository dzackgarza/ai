---
name: knowledge-extraction
description: Use when extracting durable mathematical knowledge from chat logs, transcripts, handwritten notes, markdown scraps, theorem sketches, failed proof attempts, or any noisy/partial mathematical source material. Use for converting raw mathematical discussion into definitions, lemmas, theorems, dependency graphs, proof-gap ledgers, and other research-state artifacts. Do not use for ordinary text summarization or non-mathematical content.
---
# Knowledge Extraction

For the vault mechanics of where extracted content lands (reading, writing, linking,
searching notes), load `obsidian`. For vault-level stewardship policy — inbox intake,
provenance tracking, note taxonomy, and mathematical-vault conventions — load
`mathematical-obsidian-vault-steward`.

## Core policy

This is not summarization.
It is mathematical knowledge reconstruction.
The input is partial records of a developing mathematical object.
The output is durable, structured mathematical artifacts.

Preserve mathematical meaning, not wording or chronological order.
Semantic preservation is mandatory; exact preservation is usually low value.

## Invariants to preserve

For every extracted claim, preserve:

- **Objects**: the exact spaces, schemes, categories, lattices, complexes, morphisms,
  functors, hypotheses under discussion.
- **Status**: definition, observation, proved lemma, conjecture, heuristic, example,
  counterexample, failed assertion, repaired assertion, open question.
- **Dependencies**: which definitions support which lemmas, which lemmas require which
  hypotheses, which claims depend on references, which conclusions are conditional.
- **Failures**: which approaches were tried, why they failed, whether the failure was
  formal, computational, definitional, notational, or merely unresolved.
- **Epistemic level**: known, suspected, plausible, contradicted, unchecked.

## What to produce

Transform raw source material into structured artifacts.
Do not produce compressed transcripts.
A two-hour chat log should become something like:

```
Definition 1.
Lemma 2.
Warning 3.
Failed approach 4.
Correction 5.
Proposition 6.
Remark 7.
Open gap 8.
Related reference 9.
```

The agent must preserve what was mathematically learned, not the order or wording in
which it was learned.
The chronological record answers "How was this discovered?"
The mathematical artifact answers "What is now known, under what hypotheses, by what
argument, and with what caveats?"
Both may matter, but they are different artifacts.

Produce these research-state artifacts:

- Definitions index (objects, structures, conventions, notation)
- Theorem/lemma inventory with precise statements and full hypotheses
- Dependency graph showing what depends on what, in explicit form:
  ```
  Definition A depends on convention C.
  Lemma B uses Definition A and reference R.
  Claim D was rejected because it requires false assertion F.
  Theorem E is plausible conditional on proving Lemma B and checking embedding
  primitivity.
  Open gap G blocks Theorem E but not Lemma B.
  ```
- Proof-gap ledger (missing proofs, missing computations, source-check queues)
- Failed-approaches ledger, using this format for each entry:
  ```
  Failed approach.
  One might try to prove X by reducing to Y. This fails because the reduction does
  not preserve Z.

  Reason for failure.
  The map used in the reduction is only well-defined up to equivalence, while the
  argument requires an on-the-nose identification.

  Consequence.
  Any proof of X must either avoid this reduction or add a rigidity datum.
  ```
- Claims-status audit (proved / conditional / conjectural / false / open)
- Notation reconciliation table (same object under different names)
- Source-provenance table (where each claim came from)
- Paper-readiness classification (raw → parsed → structured → checked → citable →
  paper-ready → internal-only → rejected)

## Hard rules

- Never produce a compressed transcript or summary.
  Produce structured mathematical artifacts.
- Never collapse uncertainty.
  Every claim must have an explicit status.
  "Maybe" must not become "yes."
- Never replace niche, specific, or delicate mathematical content with general textbook
  explanations. A chat log saying "this should follow from Torelli somehow" should
  become:
  ```
  Open gap.
  Determine whether the required identification follows from the relevant Torelli
  theorem. The missing point is not the existence of a period map, but whether the
  chosen lattice marking and involution data determine the required morphism. A
  source check is required.
  ```
  Not the original sentence preserved verbatim, and not a generic "Topic: Torelli"
  summary. The mathematical content and the uncertainty are both preserved.
  Similarly, do not replace:
  ```
  the specific choice of polarization used to view the Coble divisor inside the
  degree-2 Enriques period domain, and the unresolved issue is how to express that
  polarization in the blowup model over P^2
  ```
  with "The discussion was about moduli spaces and period maps."
  The first form preserves the research object; the second discards it.
- Never create a new note for every fragment.
  Integrate into existing structures.
  Ask: what existing mathematical object does this refine?
- Never append blindly.
  Compare new material against current state.
  Reconcile: confirm, refine, weaken, contradict, or supersede existing notes.
  Examples of reconciliation actions:
  - A new chat log proves that an earlier "open gap" is now closed → close the gap, link
    to the proof.
  - A new computation shows a conjectured isometry type was wrong → update the claim,
    note the correction.
  - A source check shows a cited theorem applies only under an extra hypothesis → add
    the hypothesis, mark the claim as conditional.
  - A failed proof attempt explains why an earlier lemma statement was too strong →
    weaken the lemma or record the obstruction.
  - A notation change means two notes refer to the same object under different names →
    merge or add a reconciliation entry.
    Preserve history where useful, but the current mathematical state must remain
    coherent.
- Never discard failed avenues.
  Record them with the attempt, the failure reason, and the mathematical consequence.
- Never reorder material to create a false narrative of discovery.
  False starts must stay separate from final claims.
  Repaired arguments must not be merged with unrepaired ones.

## Labeling requirements

### Claim status

Every mathematical assertion must carry one of:

- `proved in source` — explicitly proved in the source material
- `proved modulo cited theorem` — conditional on a citation
- `proved modulo computation` — conditional on an unperformed computation
- `plausible but unproved` — suggested but not established
- `suggested by examples` — evidence exists but no proof
- `false as stated but repairable` — wrong formulation, correctable
- `false and not useful` — discarded
- `ambiguous (notation changed)` — meaning unstable
- `unresolved (source incomplete)` — cannot determine

### Agent reasoning

Distinguish source content from agent reconstruction:

- `Source-supported` — explicitly present in the source material.
- `Agent reconstruction` — inferred, completed, or repaired by the agent.
- `Status` — what remains to be verified before promotion.

### Provenance

For each important claim, record:

- Which source it came from
- Whether it was asserted, proved, corrected, or inferred
- Whether the source itself was reliable
- Whether an external citation is required
- Whether the statement is paper-ready or internal-only

## Decision procedures

### Create new note vs integrate

| Condition | Action |
| --- | --- |
| Refines an existing definition, lemma, or theorem | Integrate into existing note |
| Supplies an example or counterexample | Append to examples section of existing note |
| Contradicts a current claim | Update existing note, preserve history |
| Records a failed proof strategy | Append to failed-approaches ledger |
| Adds a bibliographic pointer | Integrate into relevant note or bibliography |
| Opens a new gap | Add to proof-gap ledger |
| Represents a stable new mathematical object | Create new note |
| Belongs only in project log | Append to project log, do not create note |

### Classifying mathematical roles

Categorize every extracted item:

- Definition — introduces objects, structures, conventions, or notation
- Construction — builds one object from another
- Claim — asserts a mathematical fact
- Proof step — justifies a claim
- Example — instantiates a definition or tests a claim
- Counterexample — refutes a claim or delimits hypotheses
- Obstruction — identifies why a proposed claim or proof cannot work
- Warning — records a common mistake, false analogy, or unstable notation
- Reference — connects a claim to a citable source
- Open gap — marks missing proof, missing computation, or missing source check
- Editorial — possible paper structure, motivation, exposition

### Paper-readiness spectrum

Classify every item along:

- Raw — copied or transcribed source material
- Parsed — mathematical objects and claims identified
- Structured — definitions, claims, examples, gaps, dependencies separated
- Checked — internally consistent and source-aligned
- Citable — linked to a reliable reference or proved in notes
- Paper-ready — written with precise hypotheses, notation, and proof
- Internal-only — useful for research memory, not publication
- Rejected — false, obsolete, or superseded (may retain as warning)

## Handling images and diagrams

Images, diagrams, and handwritten fragments are mathematical sources, not attachments.
Interpret, transcribe, and check them.

- Convert diagrams to durable forms when possible: TikZ, commutative diagram code,
  explicit matrices, adjacency data, equations, tables, or structured descriptions.
- Keep the original image linked until the transcription has been audited.
- Distinguish: what is visibly present, what is inferred, what is mathematically
  reconstructed, what remains ambiguous.
- Do not silently convert a diagrammatic argument into a theorem unless missing formal
  steps are supplied or marked.

## Anti-patterns

| Pattern | Why bad | Do instead |
| --- | --- | --- |
| Compressed transcript | Preserves noise, discards structure | Structured mathematical artifacts |
| Smooth summary that collapses uncertainty | Destroys epistemic information | Label status explicitly |
| Generic textbook reformulation | Discards specific research object | Preserve niche, precise formulations |
| Note-per-fragment | Creates isolated summaries, no integration | Integrate into existing structures |
| Unlabeled agent reasoning | Confuses source with invention | Label Source-supported vs Agent reconstruction |
| Discarding failed attempts | Loses research state, enables repeat errors | Record in failed-approaches ledger |
| Chronological-order preservation | Obscures mathematical structure | Reorder by dependency |
| Claim without provenance | Unusable for verification or paper writing | Link to source and status |

## Validation checklist

Before considering extraction complete:

- [ ] Every claim has an explicit status label
- [ ] Dependencies between claims are recorded
- [ ] Failed avenues are preserved with failure reasons
- [ ] Agent reasoning is explicitly labeled as such
- [ ] Source provenance is recorded for key claims
- [ ] New material is reconciled with existing state (not blindly appended)
- [ ] Niche mathematical content is preserved, not generalized
- [ ] Images/diagrams are transcribed and linked, not merely described
- [ ] Paper-readiness level is assigned to each item
- [ ] Output answers these continuation questions:
  - What objects are being studied?
  - What is currently defined?
  - What is currently proved?
  - What is conjectured?
  - What failed?
  - What remains open?
  - What depends on what?
  - What sources support which claims?
  - What computations must be reproduced?
  - What notation is fixed?
  - What material is paper-ready?
  - What material is internal research memory?
