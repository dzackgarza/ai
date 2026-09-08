# Coverage and semantic drift in sustained work

Use this lesson when a worker turns a source corpus into a worklist, maps a requirement
to an existing implementation, introduces a reusable definition, or declares a batch
complete. It also applies when a correction reveals that an earlier selection or
interpretation omitted required work.

This is a teaching document about reasoning failures. The examples expose invalid
inferences; they do not establish hidden motives, feelings, or a model's training-time
cause. In an actual investigation, distinguish the observed transition from the
explanation inferred from it. Preserve evidence that challenges the explanation.

## Contents

- [Learn the distinction before applying the rule](#learn-the-distinction-before-applying-the-rule)
- [A worklist is a claim about the source](#a-worklist-is-a-claim-about-the-source)
- [An ingredient is not the requested construction](#an-ingredient-is-not-the-requested-construction)
- [A familiar condition can omit part of the domain](#a-familiar-condition-can-omit-part-of-the-domain)
- [Compilation cannot answer the source question](#compilation-cannot-answer-the-source-question)
- [A correction can invalidate the method](#a-correction-can-invalidate-the-method)
- [Dependency growth amplifies unexamined assumptions](#dependency-growth-amplifies-unexamined-assumptions)
- [Phase separation preserves obligations](#phase-separation-preserves-obligations)
- [Judge the trajectory through time](#judge-the-trajectory-through-time)
- [Put the lesson at the decision boundary](#put-the-lesson-at-the-decision-boundary)
- [Transfer exercises](#transfer-exercises)

## Learn the distinction before applying the rule

A worker can accurately repeat “preserve the mathematics” without recognizing the
mathematical information its next edit removes. Repetition of the instruction is not
evidence of understanding. Nor is intelligence evidence of prior mastery of this
particular distinction.

Teach with a worked case. Identify the original object, the proposed substitute, and
the exact fact lost between them. Vary the presentation while holding the obligation
fixed. Then give a nearby incorrect object that the substitute accepts. Ask the
learner to explain that mismatch and transfer the reasoning to another domain.

Operational rules need both a reason and an observable trigger. “Be more careful”
requires the worker to detect the very blindness being corrected. “Before accepting
this mapping, compare the candidate's inputs and output with the source's requested
construction” gives the worker an action whose result can contradict its proposal.

## A worklist is a claim about the source

Consider a source catalogue with these entries:

```text
### U001
- **Kind:** Definition

#### U002
- **kind:** Definition

### U003
- **Kind:** Terminology
```

Suppose all three introduce vocabulary required by the task. A selector recognizing
only `###` headings, capitalized `Kind`, and the word `Definition` returns U001.
Finishing U001 empties the worklist. It leaves two source obligations unfinished.

Changing the heading level or capitalization preserves the mathematical obligation.
Changing “Definition” to “Terminology” may also preserve definitional content. Those
presentation choices cannot legitimately decide which mathematics exists.

The reasoning error is a change in the domain of “all.” The worker proves something
about every selected row and reports it about every required source unit. The
selector has silently become the authority that determines the task.

This failure can coexist with excellent work on every selected unit. Local correctness
does not repair missing coverage. Adding another check over the same selected rows
also cannot detect what the selector discarded.

**Policy.** Establish the population from the complete admitted source or canonical
catalogue before filtering for a phase or implementation route. Account for each
source-unit identity. Then classify its actual content. Reconcile the resulting
identities, not just their counts, with the worklist and realization records.

A source unit containing both a construction and a theorem contributes obligations
to both phases without needing a new identity. Unrecognized metadata, ambiguous
content, duplicate IDs, and unread sections are unresolved inputs. They cannot
silently count as exclusions or successes.

Use a standard parser or existing source-aware tooling where available. Verify
recognized syntax against the actual admitted formats. A second script sharing the
same selection assumption is not independent coverage evidence. A sample can falsify
a selector; passing samples cannot certify an entire heterogeneous source.

For a genuinely small finite task, direct complete inspection is sufficient. This
rule does not require inventing a new database, parser, dashboard, or permanent ledger.

## An ingredient is not the requested construction

Suppose the requirement is to construct a particular algebra from specified data.
A library offers `IsSpecialAlgebra A : Prop`, where `A` is already an algebra. It may
also offer valuable theorems about algebras satisfying that predicate.

The predicate takes the missing algebra as input. The requested construction must
produce it as output. Mapping the construction to the predicate reverses that
dependency. A matching subject name and substantial nearby theory do not supply A.

Now vary the task. If the source unit asks for the property of being special, this
predicate may be exactly the correct owner. Rejecting it merely because it is
proposition-valued would be the opposite error. Likewise, an existence theorem can
support a noncomputable choice when the source permits that choice and the required
properties and choice-independence have been proved. A full model can also be built
by composing existing generic constructions without having the source's exact name.

**Policy.** Before accepting a reuse mapping, compare the source and candidate at
four boundaries: supplied data and hypotheses; returned object or assertion;
required laws and universal properties; permitted choices and generality. Identify
the relation precisely: the same definition, an equivalent characterization under
stated hypotheses, a component, a special case, or a construction from components.

An “exact” row must explain how the whole source obligation is supplied. For a
compound row, identify the declarations supplying its distinct clauses. Keep useful
partial references in the existing mapping record, with the remaining obligation
visible. Do not discard prior art or start over simply because one proposed exact
match was false. Provenance establishes which source was read; the comparison
establishes what it supplies.

## A familiar condition can omit part of the domain

For a continuous loop f on the unit interval, the intended simple-loop condition is:

```text
f(s) = f(t) implies s = t or {s,t} = {0,1}.
```

A plausible substitute is endpoint equality plus injectivity on the open interval.
It checks interior/interior pairs, but never compares an interior point with an
endpoint. Trace two circles meeting only at a point p: start at p, finish the first
circle at time 1/2, finish the second at time 1. The open-interval restriction is
injective. Nevertheless f(0) = f(1/2) = f(1), so this is not a simple loop.

The missing information is the mixed boundary case. It is not a syntax error or a
difficult theorem. A familiar phrase, “injective except at the endpoints,” was
compressed into a predicate before its quantifier domain was examined.

Change the presentation: describe the loop as a map from the quotient identifying
the interval's two endpoints. Injectivity on that quotient expresses the intended
distinction, provided the passage to the quotient is well-defined. The lesson is
to preserve the equality relation; it is not to mandate a particular encoding.

**Policy.** Translate the source statement into explicit mathematical quantifiers
before implementing it. For a domain split into parts, examine cross-part relations
as well as the relations internal to each part. Compare what each source clause
requires with what the candidate actually says.

Choose separating examples from the source condition, not from the implementation's
constructors. Include an intended example to catch accidental strengthening and a
nearby excluded example to catch weakening. Neither example proves full equivalence:
the clause comparison and required general proofs remain necessary.

The same issue arises when validating each record without checking relationships
between records, checking separate patches without overlap compatibility, or
checking componentwise maps without proving they descend through a quotient.

## Compilation cannot answer the source question

A worker constructs an object, verifies its types, proves lemmas about it, exports
it, and receives successful checks. A later reviewer asks whether it is the object
the source defined. The worker cites those same checks.

The evidence answers a different question. The compiler established consequences
of the supplied declarations. It did not compare the declarations to the source.
Further successful checks of internal consistency cannot close that comparison gap.

The process can be misdirected without anyone intentionally falsifying a result.
Its available feedback concerns syntax, types, and local laws, so successive edits
improve those properties while the source interpretation remains untested. The
observed error is promoting that feedback into authority over semantics.

**Policy.** Establish the source contract before elaboration work, and review the
actual resulting type against that contract before export or downstream use. Keep
the purposes of the checks distinct: source comparison, mathematical derivation,
and build/integration verification. A success transfers only the claim it proves.

Use independent evidence, not merely another reviewer or another tool invocation.
Two reviewers given only the same author-written summary share the same blind spot.
Give the reviewer the original source and the actual declarations. When working
alone, derive the expected condition from the source before inspecting or defending
the implementation. Do not add redundant wrappers or comparison theorems for a
canonical dependency declaration that is already the required object.

## A correction can invalidate the method

A worker completes its selected definitions, discovers an omitted terminology unit,
adds it, then discovers that a later chapter's metadata was parsed differently.
Implementing both omissions repairs two objects. It does not establish that the
selection method now covers the source.

The shared assumption is that the current residual list is exhaustive. Each omission
is evidence against that assumption. Treating the discoveries as isolated extra
tasks preserves the assumption that produced them.

**Policy.** The first counterexample to an exhaustiveness claim invalidates that
claim. Identify the selection assumption it defeats and revisit every completion
claim that actually depended on that assumption. Reconcile the affected source
population, including earlier sections or sources processed by the same method.
Do not wait for a second omitted item before examining the method.

Bound this repair by evidence. A bad selector can invalidate several source-closeout
claims without invalidating the mathematics already implemented. A bad definition
can invalidate dependent interpretations without affecting unrelated definitions.
Preserve correct work, repair the common cause, and resume substantive execution.
Changing the checkbox alone is not implementation remediation.

## Dependency growth amplifies unexamined assumptions

A predicate is accepted under a standard mathematical name. Later code imports that
name and uses it to define orientations or classifications. The later author may
carefully verify the new code while assuming that the imported predicate already
has the standard meaning. A local mistake has become a premise of later work.

The cost is determined partly by this dependency growth. More lemmas or users of
the predicate can increase the eventual repair burden even while other work makes
real progress. A passing downstream build demonstrates consistency with the
predicate; it cannot recover a condition the predicate omitted.

**Policy.** Before a new project-owned definition becomes a premise of another
construction, establish its source comparison. Existing valid evidence may be reused
when the definition, source convention, and relevant assumptions are unchanged.
Repeated full review of unchanged foundations is not required.

When a separating example exposes an error, suspend acceptance of affected
dependents. Trace semantic use, including aliases, typeclass instances, exported
declarations, and mapping claims, rather than treating direct imports as the whole
dependency relation. Fix the owning definition and revisit the claims that used
its intended meaning. Do not merely patch each consumer to compensate for it.

This does not authorize deleting unknown-provenance work or rewriting mathematical
requirements. Continue unrelated work where safe. If the repair requires a choice
between different mathematics, ask the mathematician for that choice.

## Phase separation preserves obligations

A definitions phase precedes a theorem phase. A worker proposes a quotient map but
defers representative independence because “proofs are later.” Alternatively, it
defines a purported normal form as an arbitrary output and defers the property that
makes the output normal. The phase label has removed part of the construction.

Compare two legitimate obligations. Defining a category includes the composition
laws. Classifying all objects of that category generally does not. The distinction
comes from the definition's mathematical contract, not from whether Lean uses
`def`, `theorem`, or a proof field to express the obligation.

**Policy.** Complete the laws needed to construct and use the named object in its
claimed category. Defer only results not needed for that contract. If a theorem is
needed for existence or well-definedness, name that exact dependency and discharge
it at the appropriate phase boundary. Do not pull an entire theorem programme into
the definition phase or weaken the definition to avoid its intrinsic obligations.

## Judge the trajectory through time

Suppose several hours produce useful algebra, followed by a topology definition
with a missing condition, followed by genuine winding-number work that reuses that
definition. “Everything was wasted” ignores the useful mathematics. “The build is
green and work continued” ignores the growing semantic defect.

**Policy.** Reconstruct what became mathematically available at successive times,
what was later invalidated or repaired, and what new work depended on an unresolved
assumption. Distinguish productive construction, necessary integration waits,
repeated investigation, repair, and propagation using actual artifacts and logs.

Commit timestamps are checkpoints, not effort measurements. Commit counts, prose
volume, theorem counts, and the fraction of administrative commits are not a rate
of mathematical progress. State unobserved time as unobserved. Positive net progress
and a recurring defect can both be supported; neither cancels the other.

## Put the lesson at the decision boundary

For each recurring failure, identify the first decision that made it possible and
the next decision that would amplify it. Put the rule at those points in the existing
workflow. A distant warning is insufficient if the operative instructions still
say “consume verified mappings” without requiring evidence for that verification.

| Decision | Evidence required before proceeding | What a failure suspends |
| --- | --- | --- |
| Select a phase's work | Complete source identities and content-based classification | Claims that the selected list is exhaustive |
| Accept a reuse route | Actual source/candidate comparison of the whole obligation | Acceptance of that route as a realization |
| Reuse or export a definition | Source clauses, separating example, intrinsic laws | Dependent semantic claims |
| Close a source or batch | Every required identity linked to valid realization evidence | Whole-source or whole-batch completion |
| Recover from a counterexample | Repair of the defeated assumption and affected uses | Claims relying on the defeated assumption |

Use the existing catalogue, mapping, source code, and completion record. Keep each
fact with its owner. Do not create a competing queue or audit framework merely to
demonstrate that this lesson was loaded. The evidence must be able to change the
next action: reject the mapping, repair the definition, restore omitted work, or
withhold a completion claim.

Instruction text can specify these decisions; it cannot make semantic mistakes
impossible. Check the revised guidance on the observed failures and on unfamiliar
nearby cases. Report a policy edit as a policy edit. Improved future worker behavior
requires observation of future work, not a declaration that the instructions are
now strong enough.

## Transfer exercises

For each exercise, explain the object, the lost information, and the evidence that
would change the next action. Repeating a rule or returning a pass/fail label is
insufficient. The expected reasoning follows so a teacher can assess transfer.

- **Coverage:** Two selectors each return 40 units, but one includes U041 and omits
  U017. Can matching totals support whole-source completion? Explain which source
  identities and classifications must be reconciled. Expected reasoning: equal
  cardinality does not establish equality of the required and realized sets.
- **Constructive content:** A task requests a chosen basis; a candidate theorem
  proves the module is free. What else is needed? Expected reasoning: inspect whether
  existing basis-selection machinery supplies the requested data under the permitted
  choice convention; do not accept the property alone or reimplement that machinery.
- **Mixed cases:** A proposed gluing construction verifies a map separately on two
  patches. What can still fail? Expected reasoning: agreement on their overlap is a
  separate relation needed for the map to descend; local validity does not prove it.
- **Overstrengthening:** A definition says a nondegenerate bilinear form is positive
  definite. Does testing a Euclidean example and rejecting the zero form suffice?
  Expected reasoning: an indefinite nondegenerate form separates the intended class
  from this overly restrictive one. Check the source's exact hypotheses.
- **Correction scope:** An omission is traced to a selector used for three completed
  batches. Must every declaration be rewritten? Expected reasoning: re-establish
  coverage for all three affected claims, preserve valid realizations, and implement
  actual omissions. Do not expand to unrelated batches without evidence.
- **Time:** An hour contains a necessary build wait and a correct reusable
  construction; a later burst adds consumers of a wrong definition. Which period
  made more progress? Expected reasoning: compare the mathematical capabilities and
  affected dependencies; timestamps and output volume alone cannot answer.
