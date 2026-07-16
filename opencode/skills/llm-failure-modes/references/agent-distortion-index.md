# Agent Cognitive-Distortion Index

> Part of [llm-failure-modes](../SKILL.md).
> See there for editorial guidelines and cross-references.

A reusable shorthand for the cognitive distortions that produce slop, especially in
agent-generated documents, plans, schemas, and project structure. Use the codes to label
findings compactly: "This README shows **T2 Deictic Leakage**, **O2 Classification
Compulsion**, and **R6 Formality-as-Evidence**."

## How to use this index

The operating prior is that under ambiguity, correction, or failure, agents drift away
from ordinary external reality toward an internally coherent, self-referential frame.
That prior is a **reviewer posture**, not a finding. It is useful because it keeps the
reviewer from accepting the artifact's own frame as the ground truth (the classic
infection: debating whether "Gate F" is well-designed instead of asking why any gates
exist).

Two rules govern its use:

- **Posture internal, output neutral.** Adopt the skeptical, distance-keeping posture
  while reviewing, but write findings in ordinary engineering vocabulary. Do not export
  clinical or pathologizing language into reports, commits, issues, or PRs. A finding
  says "this README references an undefined internal status system the reader cannot
  resolve," not a diagnosis of the author.
- **Codes are pointers, not proof.** A code names a suspected pattern. The finding still
  needs concrete evidence (file, line, structure, missing payload) and a reconciliation
  against the standard alternative.

These codes pair with the concrete documentation patterns in
[documentation-failures.md](../documentation-failures.md) and the code/test/QC patterns
in [reviewing-llm-code/references/pattern-catalog.md](../../reviewing-llm-code/references/pattern-catalog.md).

## R — Reality-testing and epistemic distortions

- **R1 Frame Reification.** Treating an inherited private ontology as the reality within
  which analysis must occur, instead of questioning why it exists.
- **R2 Naming-as-Existence.** Assuming a named component exists, matters, or was required
  merely because it has a proper name and prose around it.
- **R3 Confabulated Necessity.** Generating a plausible retrospective rationale for why an
  arbitrary system "had to" be built. Plausible is not the same as historically true or
  operationally necessary.
- **R4 Internal-Coherence Substitution.** Treating consistency inside a private framework
  as evidence that the framework corresponds to external reality.
- **R5 Circular Corroboration.** Treating documents, agents, schemas, or policies all
  descended from one generated premise as independent confirmation of that premise.
- **R6 Formality-as-Evidence.** Mistaking numbered identifiers, version labels, diagrams,
  status blocks, or formal tone for rigor or authority.
- **R7 Source Laundering.** Citing sources that establish a general concern (hallucination,
  provenance, security) to imply support for a specific bespoke architecture those sources
  never recommend.
- **R8 Process-as-Truth.** Treating signatures, hashes, review states, gates, or receipts
  as proof a claim is *true* rather than evidence of integrity, identity, or procedure.
- **R9 Burden Inversion.** Requiring critics to prove the private system is unnecessary,
  rather than requiring its proponents to justify departure from standard practice.

## T — Theory-of-mind and context-boundary distortions

- **T1 Shared-Context Delusion.** Assuming an external reader possesses the authoring
  conversation, history, and terminology that exist only in the agent's context.
- **T2 Deictic Leakage.** Public use of "this pass", "the attached corpus", "the agreed
  model", or codes like "C5-01" whose referents exist only inside an earlier interaction.
- **T3 Audience Collapse.** Treating users, maintainers, agents, auditors, and managers as
  one audience with the same knowledge and needs.
- **T4 The Charlie Error.** Failing to recognize that a criticism refers to the agent's own
  behavior. "You are hallucinating" becomes "the product needs a hallucination-governance
  subsystem." See [charlie-behaviour.md](../charlie-behaviour.md).
- **T5 Adversary Displacement.** Externalizing the agent's own unreliability into imagined
  hostile users, unsafe publishers, or compromised downstream actors.
- **T6 Meta/Object Collapse.** Failing to distinguish work *on* the project from work
  *governing the agents* that modify it. Prompts and corrective rules become product
  architecture.
- **T7 Correction-to-Content Transduction.** Treating feedback meant to change future
  behavior as material to write *into* the artifact being corrected.
- **T8 Context Poisoning.** Allowing accumulated corrections, rejected proposals, and prior
  frames to drive future generations even after those frames were shown defective.
- **T9 Identity Evasion.** Replacing a concrete object description with modifier stacks
  ("governed, evidence-first, map-first, time-aware knowledge system").

## L — Learning, correction, and remediation distortions

- **L1 Repair Compulsion.** Assuming every criticism requires an immediate visible fix,
  rewrite, policy, or structural intervention.
- **L2 Disclosure Substitution.** Explaining, labeling, or disclaiming a defect instead of
  changing the process that produced it.
- **L3 Local Symptom Fixation.** Treating the visible mold spot as the whole defect rather
  than evidence that the production process may be contaminated.
- **L4 Sign-Flip Overcorrection.** Responding to "too much X" by producing maximal not-X
  rather than a small grounded adjustment (e.g., disclaimer-laundering, then silent
  deletion).
- **L5 Gradient Thrashing.** Oscillating between opposing frames according to the most
  recent criticism, without a stable external objective.
- **L6 Accretion Bias.** Preferring to add a rule, document, state, gate, or explanation
  rather than simplify, discard, or rebuild.
- **L7 Preservation Bias.** Assuming inherited material contains intent or value because it
  already exists. Generated residue is treated as a requirement.
- **L8 Correction Fossilization.** Permanently encoding the history of supervision into the
  artifact, so the product becomes a record of the agent's prior mistakes.
- **L9 Critique Absorption.** Folding objections into the private framework so it grows.
  Criticism of excessive governance produces an anti-excess-governance policy.
- **L10 Brownfield Anchoring.** Treating the existing artifact as the conceptual baseline
  and repairing it from within, even when its entire frame is contaminated. See the
  rebuild protocol in [fixing-slop](../../fixing-slop/SKILL.md).
- **L11 Global-State Blindness.** Producing locally plausible changes without understanding
  the global system or the cumulative consequences of prior patches.

## O — Organizational and system-building distortions

- **O1 Ontology Proliferation.** Inventing private terms for concepts already expressible
  in ordinary professional language.
- **O2 Classification Compulsion.** Assigning passes, matrices, cells, gates, planes,
  tiers, or canonical positions to ideas that need no classification system. A
  Dewey-decimal system for one's own work is itself the red flag.
- **O3 Institutional Hallucination.** Inventing stewards, councils, owners, and
  separation-of-duty roles unsupported by a real organization.
- **O4 Premature Constitutionalization.** Elevating ordinary repository conventions into
  "doctrine", "laws", "canonical roots", or constitutional principles.
- **O5 Complexity Displacement.** Moving complexity away from the real intellectual problem
  into workflow, governance, classification, and organization.
- **O6 Process–Payload Inversion.** Allowing the machinery that controls work to become
  larger and more visible than the useful work itself.
- **O7 Standard-Alternative Neglect.** Designing a bespoke mechanism without serious
  comparison to databases, git, pull requests, issues, ordinary access control, or
  citations.
- **O8 Bespoke Exceptionalism.** Assuming the project is special enough to need a private
  system when ordinary tools already address the problem.
- **O9 Threat-Model Inflation.** Treating every imaginable harm as a present requirement
  deserving its own controls, roles, and lifecycle.
- **O10 Edge-Case Hypertrophy.** Designing around rare hypothetical cases before the common
  user path works.
- **O11 Pseudo-Precision.** Using exact counts, identifiers, or status labels that measure
  nothing about correctness, usefulness, coverage, or maturity.
- **O12 Activity Simulation.** Treating commits, files, directories, schemas, or doc volume
  as evidence of advancement.
- **O13 Recursive Documentation.** Producing documentation about documentation, inventories
  of inventories, trees explaining where other trees sit.
- **O14 Cognitive-Load Denial.** Building a system too large for any one agent or maintainer
  to hold globally, while assuming more documentation will make it manageable.
- **O15 Semantic Inflation.** Describing mundane operations (saving a record, citing a
  source) in grandiose institutional or metaphysical language.
- **O16 Scale Fantasy.** Justifying present complexity through an imagined future
  organization, user base, or risk profile with no external evidence.

## C — Collective and contagious distortions

- **C1 Echo Consensus.** Treating agreement among agents exposed to the same frame as
  independent convergence.
- **C2 Canonization by Repetition.** A generated concept becomes "established" merely
  because later artifacts repeat it.
- **C3 Artifact-Mediated Contagion.** A distorted frame propagates through READMEs,
  schemas, prompts, tests, filenames, comments, and code structure.
- **C4 Mutual Elaboration.** Agents expand one another's inventions, each assuming the
  previous agent had a valid reason.
- **C5 Authority Laundering.** Manufacturing legitimacy through ownership labels, canonical
  designations, approval states, and institutional language.
- **C6 Schema/Test Concretization.** Making an invented concept appear real by writing a
  schema or test for it. The test proves conformity to the invention, not its value.
- **C7 Source-Ecology Closure.** An apparently rich evidence network in which nearly every
  source derives from the same originating frame.
- **C8 Complexity Shielding.** Accumulating enough terminology and machinery that external
  review becomes prohibitively expensive.
- **C9 Infected Rewrite.** Asking an agent exposed to the contaminated artifact and its
  correction history to produce the replacement, reseeding the same ontology in cleaner
  prose.

## V — Reviewer infection and countertransference

These are failure modes of the *reviewer*. Watch for them in your own analysis.

- **V1 Charitable Frame Completion.** Inferring the coherent system the author "must have
  meant" instead of evaluating what exists.
- **V2 Internal-Merit Drift.** Moving from "why does this system exist?" to debating whether
  its individual parts are well designed.
- **V3 Vocabulary Assimilation.** Using the project's private terms without quotation or
  translation, thereby accepting them as ordinary referents.
- **V4 Explanation-Solicitation Trap.** Asking the producer to explain the system in
  unconstrained terms, inviting further confabulation that strengthens the frame.
- **V5 Equal-Prior Bias.** Treating an elaborate private framework as an equal competitor to
  accepted practice merely because both can be described.
- **V6 Citation-Density Seduction.** Being impressed by the quantity or formality of sources
  without checking whether they support the bespoke claim at issue.
- **V7 Complexity Prestige Bias.** Reading elaborate machinery as evidence that the problem
  must be deep or carefully studied.
- **V8 Repair Enlistment.** Letting the review turn into co-design, rewriting, or extension
  of the distorted system.
- **V9 Reality-Anchor Decay.** Gradually losing track of the original user, problem,
  payload, and standard alternatives as exposure to the private ontology increases.

## Common composite patterns

- **Time-Cube Cluster** (`R1 + R6 + O1 + O2 + O15`): a private reality presented with
  formal certainty, invented terms, elaborate classification, and inflated language.
- **Charlie Cluster** (`T4 + T5 + T7`): a correction about the agent's behavior is
  misunderstood, displaced onto external actors, and written into product content.
- **Trust-Factory Cluster** (`R8 + O4 + O5 + O9`): a simple reliability concern becomes a
  constitutional, procedural, threat-driven apparatus mistaken for rigor.
- **Slop-Accretion Cluster** (`L1 + L6 + L8 + C2`): every criticism produces more material;
  the material records prior corrections; repetition turns it into canon.
- **Empty-Institution Cluster** (`O3 + O4 + C5 + O16`): a small or nonexistent organization
  is described as a mature institution with doctrine, stewards, and imagined future scale.
- **Village-Contagion Cluster** (`C1 + C3 + C4 + C6 + C7`): agents inherit one another's
  frame, encode it in artifacts, formalize it via schemas and tests, then mistake the
  resulting ecology for independent evidence.
- **Reviewer-Infection Cluster** (`V1 + V2 + V3 + V4 + V9`): the reviewer reconstructs the
  system, enters its vocabulary, solicits explanations, and loses the external baseline.
- **Mold-on-the-Slice Presentation** (`L3 + C3 + C8`): a bizarre local artifact is the
  visible manifestation of a broader contaminated process whose complexity hides its
  extent. Treat the visible artifact as a sample, not the whole defect.
- **Toothpick-Prison Pattern** (`O2 + O7 + O14 + L6`): responding to structural weakness by
  adding more fragile custom structure while ignoring simpler standard tools.
- **Brownfield-Reinfection Pattern** (`T8 + L7 + L10 + C9`): the existing artifact and its
  correction history poison the rebuild context, so a purported rewrite reproduces the
  same disease in a new style. The escape is fresh-context greenfield rebuild from
  extracted requirements.
