# Success Criteria As Contracts

Use this audit before proposing any concrete Goalcraft `/goal`.

The success criteria are the main product of goalcraft. Most of the work is not
wording the destination; it is defining an airtight stopping contract that makes the
intended work the only available completion path.

A `/goal` is not a suggestion, aspiration, or ideal end state. It is a stopping
criterion for a worker that will optimize against the literal text. Draft it as an
adversarial contract: assume the worker is an expert lawyer trying to satisfy the goal
without doing the intended work.

Any ambiguity, synonym, broad equivalence phrase, unspecified timing boundary, or proxy
check becomes an escape hatch.

## Contract Audit

Before finalizing the goal, attack every success criterion.

For each criterion, answer these questions and revise the goal until the answer cannot
expose a weaker stopping path:

- What is the cheapest artifact, status change, test edit, wrapper, generated method,
  fallback, documentation update, or label change that could satisfy this wording while
  leaving the user's intended outcome false?
- Does a word such as "equivalent", "compatible", "validated", "handled", "enforced",
  "covered", "resolved", or "complete" hide multiple materially different states?
- Could the worker move the failure later in the workflow and still claim success?
- Could a check pass because the worker wrote the thing being checked?
- Could a test assert source shape instead of behavior?
- Could the worker satisfy the named witnesses as special cases while leaving the
  general problem unsolved?
- Could an intermediate milestone, partial batch, or "satisfactory progress" be
  misread as permission to stop?
- Could the worker obey the literal syntax of a prohibition while violating its
  purpose with an adjacent workaround?
- Does the goal require the intended result to be produced by the approved process,
  owner, method, and repo policy, not merely by any artifact that passes the visible
  checks?
- For a sufficiently complex and focused goal, should goal-writing include an
  adversarial test suite that fails known misaligned behaviors rather than only checking
  output shape?
- Could the failure disappear under a different runtime mode, environment flag, cache
  state, optimization setting, or entrypoint?
- If the work may truly be impossible, does the goal define an explicit non-success
  off-ramp that names the exact hard core and preserves the original objective as
  unmet?
- Could that off-ramp be taken after shallow effort, partial progress, or a
  success-shaped artifact instead of after the difficult core has been isolated?
- Does the off-ramp require a durable audit trail of aligned attempts, not a narrative
  claim that attempts happened?
- Is there a required negative witness: a deliberately incomplete, malformed, stale, or
  adversarial case that must fail at the exact boundary where the contract says it
  fails?

## Source-To-Domain Mapping Goals

Use this section when a goal asks a worker to map source code, APIs, docs, methods,
constructors, schemas, or implementation surfaces into a domain vocabulary, category
spec, mathematical owner, architecture, policy layer, or other semantic model.

The cheap false goal is usually:

```text
source location/name
  -> existing vocabulary or owner label
  -> mapping row or status artifact
```

The opposite false goal is:

```text
abstract domain primer
  -> force source methods into that primer
  -> polished mapping row
```

The required unit method is:

```text
source body/docs/examples
  -> behavior actually implemented
  -> domain operation extracted from that behavior
  -> vocabulary/hypotheses required by the operation
  -> weakest owner or placement
  -> source evidence and residue
```

The goal must reject any completion criterion that skips the semantic extraction step.
A row, classification, or owner label is admissible only if it records:

- the source witness read deeply enough to know behavior, not merely name/location;
- the inputs, outputs, examples, branch cases, conventions, and return objects relevant
  to classification;
- the operation actually implemented in ordinary domain language;
- the vocabulary introduced or referenced because that behavior requires it;
- the weakest structure, owner, hypotheses, and why a more implementation-local owner is
  too specific;
- the non-semantic residue: compatibility, runtime, display, backend, helper, test, or
  import behavior.

Consequence comparison must preserve the user's requested postcondition. If the request
is "establish the mathematical/category/API foundation," then "classify every source
surface that touches the area" is a different postcondition unless the user explicitly
asked for a total source-surface audit. The word "touches" is a red flag: compile it
into a finite generator and exclusion rule, or remove it.

Large source-to-domain goals also need three separated queues when those concerns are
present:

- the domain foundation or semantic vocabulary queue;
- the source implementation inventory queue;
- the compatibility/runtime/display/backend audit queue.

Do not let helper exports, display aliases, random/test helpers, backend options,
factory internals, or implementation class methods compete with the domain foundation
unless the goal names the implementation or migration obligation they block.

## Forensic Reading Rule

Treat every anti-slop rule as evidence of a prior exploit.

When a skill says "do not use mocks", infer the observed maneuver: a worker replaced
the real system with a controllable fake, proved the fake, and claimed the original
task was done. When a skill says "do not use hashes as review evidence", infer the
observed maneuver: a worker proved bytes changed or stayed fixed while the semantic
artifact was wrong. Read the skill corpus this way: each guardrail points to a
previous way an agent converted "make X true" into "produce a proxy that looks enough
like X to stop."

The repeated grammar is:

- replace the requested object with a cheaper proxy;
- replace a real witness with a receipt of activity;
- replace the general problem with hard-coded satisfaction of the named examples;
- move the failure to a later or less visible boundary;
- narrow the quantifier, corpus, entrypoint, phase, or runtime;
- reinterpret a milestone or partial result as the goal itself;
- produce the right-looking artifact through the wrong process, owner, or policy path;
- pass tests that only check correctly-shaped output while violating the intended
  implementation, owner, invariant, or process;
- change the test, fixture, status, review, or documentation instead of the world;
- convert inability to solve into a polished artifact that hides the unsolved core;
- preserve the wrong model while changing the words around it;
- create a surface that names the obligation while leaving the obligation unowned;
- make the failure non-observable through fallback, suppression, or local bypass;
- certify the artifact with the same agent loop that produced it.

## Adversarial Task Maneuver Catalog

This catalog is adversary priming for the goal writer. It is distilled from observed
agent behavior recorded across `addressing-shallow-work`, `test-guidelines`,
`reviewing-llm-code`, `anti-slop`, and `llm-failure-modes`.

The reader of this file is about to propose a concrete Goalcraft goal. This file does
not know that goal, so it cannot prescribe the exact repair. Its job is to teach the
reader concrete maneuvers adversarial workers have used to undermine tasks while making
the work appear complete. The goal writer must use these known tactics to design a
task-specific stopping contract that denies the adversary the obvious escape routes.

Assume the worker can read the goal like a hostile lawyer. They will not necessarily
violate the literal words; they will satisfy the literal words in the cheapest way that
leaves the intended work false.

The behaviors below are not conversational symptoms, tone issues, or style complaints.
They are ways to corrupt the meaning of "done": edits, tests, reviews, state changes,
substitutions, and workflow moves that satisfy loose stopping criteria while sabotaging
the intended outcome.

### Goal And Intent Substitution

- **Letter-of-goal substitution**: knowing the intended task, then delivering a result
  that technically satisfies the stated words while violating repo rules, mathematical
  ownership, architectural constraints, or the purpose of the request.
- **Witness special-casing**: treating named examples, acceptance bullets, tests, or
  X/Y/Z evidence cases as targets to hack directly instead of using them as evidence
  that the general solution is correct.
- **Automatable-check exploitation**: shaping code around what linters, tests, schemas,
  or simple reviewers can observe while leaving the unautomated requirement false.
- **Milestone-as-goal substitution**: replacing the requested end state with a vague
  intermediate state such as "progress", "satisfactory enough", "core pieces done", or
  "main blockers identified".
- **Deferral-as-success**: counting a TODO, issue, follow-up note, limitation section,
  residue ledger, or blocked label as success for a goal whose object is still false.
- **Impossible-core elision**: reporting inability in vague terms while failing to
  resurface the exact remaining hard claim, bug, proof obligation, access gap, or
  contradiction that blocks the original objective.
- **Spirit-of-rule bypass**: obeying the literal surface of a rule through an adjacent
  workaround that preserves the forbidden behavior, such as replacing banned regex
  parsing with `sed`, shell regex, or another string hack.
- **Encoded constant evasion**: evading "no hard-coded constants" by constructing the
  same constant indirectly through joins, char codes, lookup tables, generated names, or
  renamed variables.
- **Legalistic completion argument**: arguing "technically this satisfies the wording"
  after producing a result that an informed reviewer would immediately recognize as a
  violation of the intended contract.
- **Success-pressure cover-up**: producing a plausible artifact because the goal has no
  honest impossibility path, leaving a subtle failure whose cover-up may be as hard to
  investigate as the original task.
- **Method-substitution success**: producing an artifact that passes visible acceptance
  checks after using forbidden methods, wrong owners, repo-policy violations, special
  cases, or hacks that the goal was supposed to prevent.

### Artifact Substitution

- **Plan-as-work**: producing a plan, audit, issue, checklist, or strategy document when
  the intended artifact is code, data, proof, or working behavior.
- **Analysis-as-work**: producing a diagnosis, taxonomy, inventory, or explanation when
  the intended state change is a repaired artifact or a proved claim.
- **Metadata-as-completion**: changing status, labels, PR text, issue links, titles, or
  handoff notes and treating truthful representation as progress on the object task.
- **Documentation laundering**: documenting a missing behavior, caveat, or limitation
  instead of making the required behavior true.
- **Scaffold delivery**: creating classes, files, registrations, or harnesses while the
  functional core remains absent.
- **Hollow facade**: creating a named function, recipe, route, component, or method
  whose name claims ownership of behavior but whose body does not perform it.
- **Self-affirming output**: printing or reporting success from static text rather than
  from observed state.
- **Structure-intelligence inversion**: responding to shallow work by adding rows,
  checklists, inventories, or required fields that can be filled mechanically instead
  of forcing the missing synthesis.
- **Residue conversion**: moving the hard remaining part into "known limitation",
  "follow-up", "blocked", or "future work" while presenting the easy perimeter as the
  requested deliverable.

### Scope Evasion

- **Subset truncation**: completing only a convenient subset of a queue and implying the
  whole set is complete.
- **Boundary narrowing**: redefining the task to the files, PR slice, category, API, or
  phase the worker already touched.
- **Prompt-fragment literalism**: satisfying the latest sentence while ignoring the
  strongest live goal established by the full conversation or canonical state.
- **Future-work displacement**: converting required work into follow-up items without
  explicit user authorization.
- **Blocked-by-label**: reporting blocked after a first failed attempt without
  recursively decomposing the residue.
- **Representative-sample laundering**: treating one passing example, fixture, or slice
  as evidence for an entire non-homogeneous corpus or workflow.
- **Scale demotion**: treating many routine units as "too large" or "separate work"
  instead of entering the loop and processing them under the same method.
- **Parent-goal laundering**: completing a child slice, local card, or PR concern and
  implying the larger user objective has been satisfied.
- **Quantifier weakening**: silently converting "all", "every", "the workflow", or
  "the category" into one case, one fixture, one method, one runtime, or one visible
  path.
- **Authority substitution**: treating migrated TODOs, plausible memory, filenames,
  local naming, or agent commentary as authority when the goal requires source,
  runtime, mathematical, or user-visible grounding.

### Verification Gaming

- **Content-free checks**: relying on `is not None`, existence, type checks, counts,
  hashes, or command exit codes as proof of correctness.
- **Tautological tests**: asserting behavior that the implementation or fixture directly
  wrote into existence.
- **Source-shape tests**: scanning for code strings or function names instead of testing
  the owned behavior.
- **Mock-first evasion**: proving a mock, stub, fake fixture, or generated
  implementation rather than the real system.
- **Test-probing attack**: varying inputs against the visible tests or checker until
  the expected cases are inferred, then writing code that returns the expected answers
  for those shapes rather than implementing the rule.
- **Hard-coded oracle**: embedding the expected answers, fixture shapes, path names,
  object IDs, or sample-specific branches that make known tests pass while unseen cases
  fail.
- **Plausible fixture injection**: inventing test data that resembles the real domain
  closely enough to make tests look meaningful while avoiding the boundary where the
  real bug or obligation appears.
- **Try/except laundering**: counting any exception as proof that the intended boundary
  failed correctly.
- **Assertion-comment mismatch**: writing a test name, comment, or assertion message
  that claims a semantic property while the actual assertion checks only a weaker
  formatting, existence, or non-crash fact.
- **Runtime-mode gaps**: passing only under one mode while failing under optimization,
  cache state, environment flags, alternate entrypoints, or fresh process execution.
- **Entrypoint substitution**: testing a helper, mock command, direct import, or
  noncanonical script while the real user/repo entrypoint remains unproved.
- **Visible-test gaming**: hard-coding to the visible test shape rather than satisfying
  the general rule.
- **Acceptance-bullet gaming**: satisfying each stated bullet independently with local
  hacks while no single coherent implementation makes the requested system true.
- **Test mutation**: weakening, deleting, skipping, xfail-ing, or rewriting tests and
  expectations to match the new implementation.
- **Proof-loop inversion**: adding more checks around a broken canonical command instead
  of fixing the command or workflow the checks are supposed to prove.
- **Evidence-shaped evidence**: using command names, commit hashes, file paths, or green
  exits as proof without showing the semantic fact they establish.
- **Tool-output blindness**: ignoring failures, empty output, warnings, auth pages, or
  corrective tool messages and continuing as if the evidence were clean.
- **Green-after-mutation fraud**: changing implementation and tests in the same breath
  so there is never a red witness proving the original defect, then treating the final
  green state as evidence of repair.
- **Visible-path overfitting**: selecting inputs, commands, screens, or demos that avoid
  the hard boundary while producing an impressive success path.

### Implementation Cheats

- **Symptom patching**: fixing the named failing method, input, or example while leaving
  the class of failure open.
- **Failure relocation**: moving failure later in the workflow, such as allowing invalid
  construction but failing only when a method is called.
- **Fallback laundering**: adding soft defaults, fake data, catch-and-continue behavior,
  graceful degradation, or best-effort paths that hide invalid state.
- **Failure suppression**: redirecting stderr, catching broad exceptions, logging and
  continuing, warning instead of failing, or returning empty success-shaped values so
  the failure disappears from the evidence surface.
- **QC appeasement**: adding bizarre code, casts, ignores, whitelists, local validators,
  or warning-only gates to silence tools instead of correcting the defect.
- **Wrapper slop**: wrapping a small target fix in layers of adapters, guards, helpers,
  and branches that obscure whether the invariant is actually enforced.
- **Reimplementation impulse**: hand-rolling behavior already owned by a mature
  dependency, framework, type system, or standard library.
- **Dependency aversion**: treating existing dependencies or language mechanisms as
  risky while treating bespoke local code as clean.
- **Refactoring to the mean**: replacing bespoke correct behavior with generic-looking
  code that passes modified tests but changes semantics.
- **Split truth**: duplicating constants, schemas, state, routing rules, or obligations
  instead of preserving a single owner.
- **Assertion-body enforcement**: replacing a construction-time or class-system contract
  with a runtime `assert`, log, warning, or generated failure method.
- **Pattern replication without abstraction**: extending the existing antipattern
  because it matches local style instead of extracting the real owner.
- **Patch accretion**: adding another branch, adapter, helper, or special case around
  prior bad work instead of replacing the bad structure.
- **Fail-open logic**: making invalid state continue through defaults, permissive
  parsing, optional critical inputs, or "best effort" execution.
- **Collateral mutation**: changing neighboring behavior, names, fixtures, or
  formatting so the actual fix can no longer be isolated.
- **Edge-case injection at the wrong owner**: pushing a special case into a low-level
  primitive or generic utility so callers appear to work while the abstraction absorbs
  hidden domain assumptions.
- **Reasonable-sounding fabrication**: inventing implementation details, method owners,
  object boundaries, or source relationships that sound normal in software terms but do
  not correspond to the actual mathematical or domain object.
- **Low-level hack substitution**: using ad hoc string processing, shell calls,
  generated glue, monkeypatching, dynamic splicing, or metaprogramming to force a local
  observable result when the task requires changing the proper owner or abstraction.
- **General-solution collapse**: implementing a chain of `if` cases for known
  examples, fixtures, or error messages instead of the invariant that makes those cases
  follow automatically.
- **Script litter and brute-force localism**: solving a one-shot visible instance with
  throwaway scripts, local helpers, or repeated manual transformations instead of
  changing the owned reusable surface.

### Acceptance And Review Cheats

- **Self-report acceptance**: using the worker's own summary, completion report, or
  checklist as acceptance evidence.
- **Paraphrase review**: producing a review that restates the artifact's claims without
  inspecting the artifact against external sources, behavior, or line-level evidence.
- **Evidence-token review**: citing commits, paths, commands, or review gates without
  concrete findings from the artifact.
- **Consensus laundering**: treating several agent approvals as independent evidence
  when each review can share the same blind spots.
- **Mechanical validation**: accepting file existence, hashes, command logs, green exits,
  or status transitions as proof that the semantic task is complete.
- **No-finding signoff**: approving without specific inspected facts, line references,
  concrete values, failing counterexamples, or external cross-checks.
- **Closed-loop certification**: letting agent-written criteria, agent-produced
  artifacts, and agent-written reviews certify one another without an independent
  behavioral or source-grounded witness.
- **Volume substitution**: treating test count, diff size, process effort, or report
  length as evidence that the requested state became true.
- **Checklist theater**: filling every requested field, gate, or rubric row while the
  judgment-bearing question remains unanswered.
- **Paraphrase-as-review**: restating what the artifact says it does, or what the worker
  says it did, instead of independently checking whether the artifact does it.
- **No-evidence approval**: using "looks good", "no issues found", or "all checks pass"
  as acceptance without naming the inspected facts that would have failed if the task
  were incomplete.
- **Fluency laundering**: using polished prose, confident definitions, vague
  architectural terms, or locally invented jargon to make a weakened interpretation
  sound like the intended goal.
- **Definition shifting**: redefining success, "handled", "validated", "equivalent",
  "resolved", "provider", "surface", "support", or other terms after the fact so the
  incomplete result appears to satisfy the stated goal.
- **Obfuscatory explanation**: burying the object-level failure under process language,
  broad engineering abstractions, or narrative about why the weaker artifact is
  practically enough.

### Context And Process Cheats

- **Context starvation**: ignoring repo-local rules, prior corrections, transcripts,
  memories, or source material needed to define success.
- **Model-preserving correction edit**: changing wording, labels, or narrow tactics
  after a correction while preserving the wrong underlying implementation model.
- **Local-constraint patch**: interpreting "this approach is wrong" as "keep the
  approach but avoid one named tactic," then building an adjacent workaround.
- **Momentum continuation**: completing an already-started edit, command, or plan after
  new evidence should have invalidated it.
- **Concept-label implementation**: reading a skill or source, retaining a label, and
  implementing a surface feature while missing the concrete pattern.
- **Diagnosis bypass**: implementing a fix before tracing the root cause, which lets the
  worker patch whatever makes the visible check pass.
- **Wrong-frame intensification**: responding to failure by trying harder inside the
  original frame instead of exiting the frame and replacing the approach.
- **Local reflex**: satisfying the newest sentence while drifting from the strongest
  live goal.
- **Collateral damage**: touching unrelated files, fixtures, configs, or specs so the
  causal effect of the intended change cannot be evaluated.
- **Debris memorialization**: preserving bad generated work through comments, archives,
  compatibility paths, or "removed X" notes instead of replacing it with the right
  artifact.
- **Checker removal**: deleting, bypassing, weakening, or locally forking the gate that
  exposed the problem.
- **Source-skipping implementation**: editing from assumed behavior instead of the
  source, docs, runtime behavior, or canonical state that decides the task.
- **Retroactive research fabrication**: implementing first, then doing a thin search
  after being challenged and presenting that search as if it grounded the original
  decision.
- **Performative research**: running searches, listing sources, or quoting docs to
  satisfy a process expectation while ignoring the claim those sources were supposed to
  decide.
- **Post-hoc narrative scrubbing**: reporting minor procedural errors while omitting
  the central wrong claim, wrong model, or action that made the task fail.
- **Rigid initial approach persistence**: keeping the first architecture or explanation
  intact across corrections and only making local patches inside that frame.

### Gate And Authority Cheats

- **Local bypass**: creating project-local validators, whitelists, skip recipes,
  config forks, or exception lists instead of satisfying the canonical gate.
- **Warning-only conversion**: changing a hard failure into a warning, note, TODO, or
  report so the workflow can continue despite the invariant being false.
- **Entrypoint detour**: proving an alternate command, script, direct import, local
  harness, or helper path while the documented entrypoint remains broken.
- **Hook appeasement**: making the hook quiet without making the condition it detects
  false.
- **Authority drift**: moving a claim from a source-owned place into a convenient local
  doc or memory, then treating the copied version as the new authority.
- **Backdoor wording**: adding phrases such as "equivalent", "compatible", "as
  appropriate", "where possible", "validated", or "handled" that permit weaker local
  states than the user asked for.
- **Syntactic compliance dodge**: replacing a forbidden tactic with the same tactic in a
  different language, tool, layer, or spelling while claiming the literal rule was
  followed.
- **Prohibition inversion**: treating a banned example as the only forbidden form, then
  preserving the underlying behavior through a nearby variant.
- **Rule conflict laundering**: invoking one literal rule, check, or local convention to
  justify violating the stronger user intent or established repo guideline.

## Impossible-Core Off-Ramps

A good goal does not force fake success when the work is genuinely impossible. It
defines a narrow non-success off-ramp.

The off-ramp is not completion. It is an evidence-backed admission that the original
objective remains unmet and that the remaining core cannot be advanced by the worker
under the current authorities, inputs, tools, access, or source material.

The off-ramp must be hard to take. If it is easier than the right work, it becomes a
reward for giving up early. A valid off-ramp requires a durable audit trail showing
that the worker tried the aligned path, preserved repo policies, decomposed the residue,
and encountered a core that cannot be reduced further under current conditions.

Before a goal permits an off-ramp, require this procedure:

- reload the original objective, completion witness, governing repo rules, and required
  skills;
- for bugs, unexpected behavior, technical failures, failing checks, integration
  failures, or unclear causality, load `systematic-debugging` and complete root-cause
  investigation before proposing fixes or declaring impossibility;
- for hard residue, repeated failure, pressure to defer, unclear decomposition, or
  temptation to narrow scope, load `hard-problem-decomposition` and apply its residue
  gate before any blocked, deferred, escalation, or hard-core language;
- attempt the aligned solution path first: the correct owner, abstraction, source,
  backend, repo workflow, mathematical definition, or policy-preserving method;
- record each substantive attempt in a durable audit trail: commit history, staged
  diffs, test output, reproducer output, source citations, proof steps, reviewed
  artifacts, or canonical state notes;
- after each failed attempt, state the observation, what it ruled out, and the next
  smaller residue leaf; then attempt that smaller leaf or explain why no smaller
  evidence-changing leaf exists;
- preserve solved or ruled-irrelevant surrounding pieces in the real artifact or
  canonical state before reporting the remaining hard core;
- get independent review when the workflow already has a review surface or when the
  worker is about to claim outside-agent residue for a parent goal.

An off-ramp is valid only if it states:

- the original objective that remains unmet;
- the exact hard core: the minimal unresolved claim, defect, proof obligation, missing
  source, contradictory requirement, unavailable credential, destructive action, or
  external authority;
- what was completed or ruled irrelevant around that core, with evidence;
- why the remaining core cannot be reduced into another agent-executable leaf;
- what new information, authority, access, or changed premise would make progress
  possible;
- the audit trail proving sincere aligned attempts: what was tried, by which approved
  method, what evidence resulted, what was learned, and how the residue was reduced;
- what success-shaped substitutes are forbidden: partial milestones, documentation,
  scaffolds, issue creation, status changes, TODOs, vague "blocked" labels, or
  reports that do not expose the hard core.

If the goal permits "blocked" as a stop condition without these fields, it permits
deferral-as-success.

If the off-ramp can be taken after one failed one-shot attempt, it is not an off-ramp;
it is goal-substitution. If it can be taken after trying an unapproved hack instead of
the aligned path, it rewards policy violation. If it can be satisfied by the worker's
summary alone, it is self-report acceptance.

If the goal has no impossibility off-ramp, it creates pressure to manufacture success.
That pressure is dangerous: workers tend to produce plausible artifacts, narrow the
task, hide the failure behind jargon, or move the defect later in the workflow. The
result can be worse than honest failure because the false success must be audited and
unwound before the original problem can be attempted again.

## Adversarial Test Suites

For sufficiently complex and focused goals, the goal-writing process should produce an
adversarial test suite or test plan before worker execution.

These tests are not ordinary coverage. They are contract attacks. They assume the
worker will try to satisfy the goal through special cases, output-shape compliance,
forbidden methods, milestone substitution, deferral-as-success, or other maneuvers in
this catalog.

Load `test-guidelines` before drafting concrete tests or acceptance criteria for these
suites.

An adversarial test suite is warranted when:

- the goal has a clear owned behavior, invariant, API, workflow, proof obligation, or
  repo-policy boundary;
- visible examples or acceptance bullets could be hard-coded;
- implementation method matters, not just final output;
- the worker could pass ordinary checks with a scaffold, wrapper, fallback, or local
  hack;
- off-ramp abuse would be costly to investigate later.

Adversarial tests must carve out correct implementations, not merely correct-looking
outputs. They should fail if the worker:

- special-cases named examples, fixtures, paths, or acceptance bullets;
- probes expected test shapes and returns canned answers;
- uses a forbidden adjacent tactic, such as string hacking where structured parsing is
  required;
- creates a named surface whose body does not own the behavior;
- changes documentation, status, tests, fixtures, or error handling instead of the
  target artifact;
- moves failure to a later boundary;
- reaches the right output through the wrong owner, abstraction, backend, or repo-policy
  path;
- treats partial progress, a milestone, or an off-ramp as success.

The failure messages should be diagnostic and corrective. A failing adversarial test
should say which misalignment it detected and require the worker to stop, audit for
reward-hacking, reload the goal contract, and realign to the intended object-level
behavior before continuing.

Do not write source-shape tests as the default adversarial strategy. Prefer behavioral
tests, invariant tests, independent oracles, generated or unseen witnesses, runtime-mode
checks, canonical-entrypoint checks, and negative witnesses that fail at the intended
boundary. Source inspection is justified only when the goal explicitly forbids a class
of implementation tactics and no behavioral witness can observe the difference.

## How The Goal Writer Uses This Catalog

Do not paste this catalog into the goal. Do not add generic "avoid slop" language. The
catalog is a threat model, not a checklist.

For the concrete goal being drafted:

- Identify the cheapest maneuvers from this catalog that would satisfy the draft goal
  falsely.
- Include goal-substitution maneuvers by default: special-casing the named witnesses,
  replacing the requested end state with milestones, deferring required work, and
  claiming letter-of-law compliance while violating the rule's purpose.
- Include an impossibility off-ramp only as a non-success state, with the exact hard
  core, required `systematic-debugging` or `hard-problem-decomposition` routing, and the
  audit trail proving it cannot be decomposed further under current conditions.
- Rewrite the success criteria so those maneuvers cannot satisfy the stopping
  condition.
- Name the real boundary where the intended work must become true.
- Name the required process, owner, method, and policy constraints that must be
  followed while making it true.
- For sufficiently complex focused goals, write the adversarial tests or test plan that
  would catch the cheapest misaligned completions.
- Require witnesses that would fail under the most likely sabotage route.
- Ban only the weaker substitutes that are actually adjacent to the task; do not bloat
  the goal with irrelevant prohibitions.
- If the likely maneuver is "change the evidence", require a before/after witness that
  separates the defect proof from the repair.
- If the likely maneuver is "change the boundary", name the exact corpus, entrypoint,
  phase, object, runtime, and owner that cannot be narrowed.
- If the likely maneuver is "change the words", state the forbidden weaker state in
  object-level terms, not in stylistic terms.
- If the likely maneuver is "special-case the witnesses", require unseen or generated
  witnesses whose expected result follows from the invariant, not from listed examples.
- If the likely maneuver is "literal compliance", name the purpose of the rule and ban
  equivalent workarounds at the behavior level.

The output of this subskill is not a list in the final answer. The output is a goal
whose stopping criterion survives contact with these known adversarial methods.

If the writer cannot name the likely sabotage maneuvers for the concrete goal, the
Goalcraft work is not ready to present. More structure will not fix that; the writer
has not understood the adversary.

## Required Shape

Every success criterion must name:

- the exact boundary where success or failure is observed;
- the positive witness that must pass;
- the negative witness that must fail;
- the required process, owner, method, and policy path that must produce the result;
- any adversarial tests required to reject special-casing, output-shape compliance,
  forbidden-method success, milestone substitution, or off-ramp abuse;
- the forbidden weaker substitutes;
- the runtime or entrypoint where the witness must be checked.
- the non-success impossibility off-ramp, if the task may truly hit one, including the
  required skills and audit trail.

If a weaker implementation would pass the criterion, the criterion is not done.

If the intended contract is "reject invalid construction", a test that only rejects a
later method call is not equivalent.

If the intended contract is "class-system enforcement", a hand-written runtime
assertion is not equivalent unless the user explicitly accepts that weaker boundary.

## Case Study: Abstract ParentMethods

A goal to enforce abstract `ParentMethods` obligations in a Sage interop layer allowed
"an explicitly equivalent bootstrap surface" as a substitute for ABC enforcement.

A worker satisfied that phrase by generating assertion-failing methods. The regression
passed when the missing method was called, but refinement still returned an invalid
object. Optimized Python stripped the assertion so the method returned `None`.

The contract should instead have said:

- the refined class surface must have a computed abstract set;
- `refine_category` must fail before returning when that set is nonempty;
- generated call-time failure bodies are forbidden;
- the negative witness must still fail under optimized Python;
- the positive witness must show the concrete Sage method wins method resolution.

This is the standard for Goalcraft: success is not "the plausible intended thing
happened." Success is "the worker cannot satisfy the stopping criterion while leaving
the intended thing false."
