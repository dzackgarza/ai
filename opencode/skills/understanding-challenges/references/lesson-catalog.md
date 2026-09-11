# What Was Actually Not Understood

Ten classes, each recovered from repeated comprehension challenges across this system's
transcripts. Every instance below is a scrubbed summary of a failure class; no verbatim
user message appears here, and none may be added.

Each entry has the same shape: **Shape** (what the output looked like), **Principle**
(the thing that was not understood), **Check** (the question that catches it first).

## Contents

1. [Precision relaxation](#1-precision-relaxation)
2. [Vocabulary treated as the mental model](#2-vocabulary-treated-as-the-mental-model)
3. [Authority without prerequisite reading](#3-authority-without-prerequisite-reading)
4. [Proxy substituted for the goal](#4-proxy-substituted-for-the-goal)
5. [Generality collapse](#5-generality-collapse)
6. [Composition blindness](#6-composition-blindness)
7. [Domain fundamentals skipped](#7-domain-fundamentals-skipped)
8. [No theory of mind](#8-no-theory-of-mind)
9. [Repetition without method change](#9-repetition-without-method-change)
10. [Read the rule, then broke it](#10-read-the-rule-then-broke-it)

## 1. Precision relaxation

**Shape.** The user supplies an exact technical term. The output uses a neighbouring
term that is cheaper to implement, or that the agent finds more familiar. A user names a
submodule of a quotient group; the agent's code and docs call it an ideal, although the
ambient object is not a ring. A user names a functor; the agent ships a method on a
class. A user names a category of objects; the agent ships a constructor and a
convention.

**Principle.** A user message is a specification at the precision it was written. The
technical nouns in it are load-bearing: they fix which theorems apply, which
constructions are legal, and which proofs are available. Substituting a near synonym
does not simplify the task — it silently changes the task to a different, usually false,
one. When the user's word names a thing the codebase has no object for, the missing
object *is* the defect. Building a proxy around the gap entrenches it.

**Check.** Every technical noun in your output traces to the user's message, the plan,
or a cited source. For each noun you introduced: what does it denote, and which existing
object already denotes that? If none does, say so and build the object, or stop and ask.

## 2. Vocabulary treated as the mental model

**Shape.** After a coinage is rejected, the agent deletes the word, adds it to a banned
list, and ships the same design under a new name. Invented nouns for "the thing an
object sits over" or "the thing a method is installed on" reappear as different invented
nouns.

**Principle.** An invented noun is a symptom, not the disease. It exists because the
agent needed to name a thing the correct architecture has no room for. Removing the word
leaves the structure that demanded it, and the next session re-invents a synonym. Worse,
a written prohibition inserts the word into the artifact permanently; every later reader
sees the name with no reliable way to tell a ban from a requirement (see `Removal Means
Deletion` in AGENTS.md).

**Check.** Can the concept be stated using only objects that already exist in the design?
If yes, the coinage was noise — delete the structure, not just the label. If no, the
design is wrong and the repair is architectural. Either way, no banned-word list.

## 3. Authority without prerequisite reading

**Shape.** An agent inspects code, forms a judgment about what the project intends, and
proposes a correction — having read no transcript, no plan, no vault item, and no
repository document. A related shape: an agent treats an agent-written document as
settled intent, when the document was produced by exactly this failure one session
earlier.

**Principle.** On this system, correctness is defined by the user's stated intent, which
lives in transcripts first, in plans and repository documents second, and in code last.
Roughly all written material here is agent-written: it is user decisions filtered through
agents, and it backslides whenever an agent records its own assumptions confidently.
Local code inspection therefore confers no authority to correct architecture. It cannot
distinguish an intended design from an accumulation of earlier misunderstandings.

**Check.** Before any corrective opinion: name the sources read. If the list contains
only code, you have an observation, not a correction. If it contains only agent-written
docs, verify the load-bearing claims against transcripts before relying on them.

## 4. Proxy substituted for the goal

**Shape.** Reorganizing a reference wiki and reporting reduced page count as the win.
Describing a mathematics site by its lines of code. Reporting test counts, error counts,
or checkbox counts as evidence of convergence. Hard-coding any such number into a
user-facing surface.

**Principle.** The proxy is not a weaker version of the goal; it is frequently opposed to
it. A wiki exists to hold more retrievable material, so fewer pages is a loss reported as
a gain. A research site is judged on theorems and definitions, so lines of code tells the
audience nothing about the thing they came for. Once a number is reported twice inside
one work unit, it is functioning as the target, and edits start being justified by the
number moving rather than by a claim becoming true.

**Check.** State the mission in one sentence. State what the number measures. State
whether they are the same thing. If the number is genuinely wanted on a surface, it is
computed at build time or served as data — never typed in by hand, where it is wrong the
day after it is written.

## 5. Generality collapse

**Shape.** Testing injectivity by comparing ranks of kernels, valid only because the
modules in front of the agent happen to be free. Comparing two objects by tuples of
invariants instead of testing for an isomorphism. Asserting what the current library
version computes rather than what is mathematically true. Special-casing a construction
to the one example under discussion, which the user offered as an illustration rather
than a ruling.

**Principle.** House style runs toward the formulation that survives dropping a
hypothesis: finiteness, freeness, projectivity, commutativity, groups to monoids, rings
to semirings. A proof that silently uses the special case is not a weaker proof of the
general claim; it is a proof of a different claim that will break at the first relaxation,
in a way no test will localize. Equal invariants are not equality; equal presentations are
not equality; agreement of computed data is not a statement about the objects.

**Check.** Which hypothesis does my argument actually use? Drop it and see what fails.
If a test would pass on an object the claim is false for, the test asserts nothing. When
the current library cannot compute the true statement, the true statement is still what
gets asserted, and the gap becomes an upstream issue plus a strict expected failure —
never a weakened assertion.

## 6. Composition blindness

**Shape.** Receiving a design that supplies the desired API as a composition of
primitives that already exist, and responding by planning new bespoke code, new wiring,
new boilerplate to reach the same surface.

**Principle.** When a construction falls out of existing primitives, that is the good
case: less code to write, less to maintain, and the result inherits the correctness of
the primitives instead of asserting its own. Treating it as a burden inverts the value.
Manual re-wiring of something the kernel exists to supply is the same error in a
different register — it reintroduces by hand the obligation the abstraction was built to
remove.

**Check.** Before writing a new construction: can it be obtained by composing things that
already exist? If the design has a kernel, a base class, or a framework that owns an
obligation, why am I discharging that obligation by hand? See
`[[known-solution-first/SKILL|known-solution-first]]` and the bespoke software policy.

## 7. Domain fundamentals skipped

**Shape.** Designing an interaction system for a game without the standard interactable
pattern — activation region, object owning its own responses, prompt affordance — and
inventing an ad hoc mechanism instead. Hard-coding one animation into an engine when an
artist will replace it tomorrow. Writing a test that indexes a dictionary by a construct
no practitioner of the language has ever used. Treating a two-dimensional approximation
as an answer to a precisely described three-dimensional geometric condition.

**Principle.** These are well-trodden problems with known solutions, and the user is
working at practitioner level in the domain. Producing an invention where a standard
pattern exists signals that the domain was not consulted, and it costs the user the time
to explain the standard pattern back to you. Simulating a precisely specified solution is
a different failure of the same family: the specification was exact, so an approximation
is a refusal to implement it.

**Check.** What is the standard solution in this domain, and where is it documented? Ask
that before designing, not after review. When the user describes something precisely,
implement that thing; if it cannot be implemented, say which part and why.

## 8. No theory of mind

**Shape.** A status report readable only by someone holding the session's context —
internal identifiers, plan-row labels, resolved acronyms, none defined. A subagent
dispatched with a bounded task and no pointer to the plan that defines correctness. A
push message to a worker telling it something it just wrote itself.

**Principle.** You are the party holding the context: you read the code, the plans, the
subagent reports, the transcripts. If a topic has not appeared in the conversation, it is
not in the user's context and must be introduced before it is used. A freshly started
subagent knows nothing at all — not the plan, not the policy, not the vocabulary — so
whatever it needs must be in its prompt or reachable from a path in its prompt.
Coordination messages that restate what the recipient already knows are pure overhead and
underestimate what the recipient can do unsupervised.

**Check.** For a report: could a reader with none of my context act on this? For a
subagent prompt: does it name the plan, the constraints, and the acceptance statement?
For a coordination message: does the recipient learn anything it did not already have?
`[[response-preparation/SKILL|response-preparation]]` and
`[[subagent-delegation/SKILL|subagent-delegation]]` own the procedures.

## 9. Repetition without method change

**Shape.** The same correction arrives for the third time. The agent fixes the third
instance, agrees that it will be careful, and produces a fourth. Asked what learning from
mistakes means, it summarizes the mistakes.

**Principle.** Being told the same thing repeatedly is evidence about the method, not
about the instance. Learning from a mistake means changing what you do next time, and a
model has no mechanism to carry an intention across sessions. The only durable change is
an edit to a file that the next session will read: the routing table, the skill, the
repository document, the memory vault. Everything else is a promise with no carrier.
This is why a claim to have learned something is not humility but a false statement about
your own architecture.

**Check.** Has this correction fired before? Search the transcripts. If yes, the
deliverable is the routing or document change that makes the next session get it right
without being told, and the instance fix is incidental. Write it, cite the path.

## 10. Read the rule, then broke it

**Shape.** An agent reads a policy document, states the constraint accurately, writes
code that violates it, and confesses when the violation is found. No new information
arrived between reading the rule and breaking it.

**Principle.** Accurate restatement of a constraint is not compliance, and it is not
evidence of compliance — the same session demonstrated that the two are independent.
This is why explanation is never accepted as the discharge of a constraint here: the
faculty that produces a correct account of the rule is not the faculty that applies it.
A correct taxonomy of your own failure is another receipt, not a repair.

**Check.** Before the commit, check the artifact against the constraint text, not against
your memory of having read it. Where a gate exists — hooks, QC, a policy index — let it
run; where one does not, read the rule and the diff side by side. If you notice that you
read a rule and violated it anyway, the fix is a gate, not a resolution.
