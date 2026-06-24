# Documentation and Frame-Contamination Failures

> Part of [llm-failure-modes](SKILL.md).
> See there for editorial guidelines and cross-references.

Failure modes where agents externalize private context, correction history, and
self-control machinery into public project artifacts. These failures are most visible
in READMEs, architecture docs, roadmaps, schemas, prompts, generated reports, and review
summaries.

The review target is the production process, not prose polish. A grammatically clean
document can still force the reader to enter the agent's private frame before the reader
can tell what exists, who uses it, or what value it provides.

1. **Private-context leakage**

   The document assumes access to an invisible conversation, prompt, correction, or
   planning state. It uses terms like "pass", "canonical root", "accepted remediation",
   "phase", "owner", or "current status" before grounding them in a public artifact.

   Detection: ask whether a new reader can identify the ordinary artifact, task, input,
   output, and evidence without knowing the agent session history.

2. **Private ontology as public context**

   The document makes readers learn a project-created taxonomy before telling them what
   the thing is. Internal labels become the interface.

   Correction: translate every term into ordinary nouns and verbs first. Keep only terms
   that name a real public interface, data model, command, file format, or domain concept.

3. **Description without identity**

   The document describes governance, status, or architecture before identifying the
   object. A reader sees many adjectives and relationships but cannot answer "what is
   this?"

   Review question: what single ordinary noun names the artifact?

4. **Internal classification substituted for value**

   The document classifies work as blocker, owned, canonical, verified, accepted,
   completed, deprecated, or non-authoritative without showing the user-facing value or
   executable boundary those labels govern.

   Labels can route work; they are not payload.

5. **Invented institutional reality**

   The document creates roles, committees, ownership models, policies, gates, maturity
   levels, or release institutions that do not exist outside the agent-produced text.

   Detection: if removing the role or institution would not remove a real workflow,
   permission boundary, legal requirement, user responsibility, or executable check, it
   is likely invented structure.

6. **Self-certifying doctrine**

   The document claims correctness because another generated policy, report, or summary
   says so. The loop may be internally consistent, but no external reality surface has
   been inspected.

   Correction: trace each authority claim to code, data, command output, user-visible
   behavior, external source, or a contemporaneous issue/PR decision.

7. **Reification by naming**

   A named subsystem, state machine, schema, or roadmap item is treated as existing
   because it has a name and prose around it.

   Review question: where does it run, what input does it accept, what output does it
   emit, and what breaks if it is deleted?

8. **Control-payload inversion**

   The document devotes more structure to trust, governance, proofs, receipts, statuses,
   or review flow than to the useful thing delivered.

   Complexity is not itself evidence of failure. It becomes a finding when the control
   system precedes incidents, categories precede examples, or custom process is
   disproportionate to actual users, data, risks, and workflows.

9. **Pseudo-precision**

   The document uses exact counts, pass numbers, status names, dates, matrices, or
   elaborate tables to make weak facts feel measured.

   Detection: remove the numbers and ask whether the claim still has inspected evidence.

10. **Recursive documentation**

    The document is mostly about how to read, validate, classify, or repair other docs.
    The object-level task recedes behind documentation about documentation.

    Correction: collapse the recursion to the current reader task. Move reusable process
    rules into the owning skill, policy, or agent surface.

11. **Payload absence**

    The document has no smallest complete example, no visible input/output, no command,
    no data sample, no user workflow, and no observable success condition.

    Detection: ask for the smallest complete use case. If it cannot be shown, the
    document is likely a narrative shell.

12. **Meta-work colonizes object work**

    Agent instructions, review history, prompt residues, anti-hallucination doctrine,
    TODO triage, and correction ledgers occupy the public documentation surface.

    Correction: move private agent-control material to `.agents/`, skills, memory, or
    planning records as appropriate. Keep public docs task-facing.

13. **Threat-model inflation**

    The document imports enterprise security, governance, sandboxing, compliance, or
    availability concerns into a private bespoke tool without a concrete owned boundary.

    Detection: ask what actual asset, actor, permission boundary, external user, or
    failure incident requires the model.

14. **Activity without advancement**

    The document records effort, review, migration, cleanup, synthesis, or validation
    activity without stating the object-level capability, decision, or evidence that
    advanced.

    Correction: separate receipts from proof. Receipts show that work happened; proof
    shows that the reader's task or the repository's obligation is satisfied.

15. **Disclosure substituted for repair**

    The document explains that its own bad content is non-authoritative, stale, internal,
    historical, or superseded, while leaving that content in the reader's path.

    Correction: remove the wrong content. A disclaimer can route a reader around a
    temporary hazard, but it does not remediate a permanent documentation boundary error.

## Review Discipline

Use these forcing questions before accepting the document's frame:

- What is the ordinary noun for the artifact?
- Who is the real reader?
- What is the smallest complete input-to-output use case?
- What useful payload appears before the control system?
- Which claims are current behavior, future work, domain fact, or agent process?
- Which claims are backed by inspected reality rather than repeated project narrative?

Do not fix these failures by adding warnings, disclaimers, or more taxonomy. Most of
them require subtraction, relocation, or evidence, not elaboration.

## Cross-References

- `writing-readmes`: public/private boundary gate for README edits.
- `writing-documentation`: general documentation workflow and anti-patterns.
- `reviewing-llm-code/references/pattern-catalog.md`: canonical pattern names for
  review reports.
- `reviewing-subagent-work`: independence discipline for agent-produced reviews.
