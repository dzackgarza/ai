---
name: technical-copy
description: Use when writing any copy this system ships or shows — status reports, handoffs, commit bodies, PR descriptions, issue text, docstrings, README and site descriptions, UI strings, error and fallback messages, subagent prompts, or a summary of numbers. Hooks the copy patterns corrected here repeatedly (word salad, buried lede, stat prose, narration, agreement, prose that contradicts the code) and routes each to its style authority.
---
# Technical Copy

This leaf covers copy this system ships or shows. Every pattern below was corrected
repeatedly in these artifacts, and each one costs the reader something: copy that
announces itself instead of informing, agrees instead of working, recounts the process
instead of stating the result, or states a conclusion the artifact does not support.

For prose voice in general — promotional language, weasel attribution, significance
inflation, sycophantic tone — see [[writing/humanization/humanization|humanization]].

Each section is the situation, the authority that treats it, and the house rule.

## Dense clause-stacked prose with no recoverable subject

**Pattern.** Sentences that chain qualifications, appositives, and conditionals until the
actor and the action are gone; agent-invented nouns doing the work of verbs; referents
that resolve only inside the writing session. The reliable symptom is that the reader
cannot restate the sentence.

**Read.**

- Williams, *Style: Lessons in Clarity and Grace* — characters as subjects, actions as
  verbs, old information before new. This is the direct repair for clause-stacking, and
  the shortest path from unreadable to readable technical prose.
- Gopen & Swan, *The Science of Scientific Writing*, American Scientist 78 (1990) —
  reader-expectation: where in a sentence readers look for the point.
- ASD-STE100, Simplified Technical English — approved words, one meaning per word, short
  sentences, active voice.

**House rule.** Standard technical English, and no invented noun: if a concept needs a
name the field does not have, the design is wrong, not the vocabulary. Every technical
noun traces to the user's message, a repository document, or a cited source.

## The point arrives late, or not at all

**Pattern.** The finding is in paragraph four, under the setup. A report opens with what
was attempted rather than what is true now.

**Read.**

- The inverted pyramid, standard newswriting practice — the conclusion first, support
  after, detail last.
- Gopen & Swan, as above, on stress position.

**House rule.** Open with the delta from the expected state: what is outstanding, what is
wrong, what needs a decision. [[response-preparation/SKILL|response-preparation]] owns
the report contract.

## Statistics written as a sentence

**Pattern.** Counts strung into prose — so many formalizations, so many packages, so many
libraries — which is unreadable, unscannable, and impossible to compare.

**Read.**

- Few, *Show Me the Numbers* — when a table beats a sentence, and how to build the table.
- Tufte, *The Visual Display of Quantitative Information* — data density and the cost of
  decoration.

**House rule.** Numbers go in a table. The metric must be one the audience values, and it
is computed at build time or served as data, never typed into prose where it is wrong the
next day.

## Self-announcing copy

**Pattern.** Copy that asserts its own properties instead of carrying content. It is the
largest single class of correction here, and it appears in every artifact type:

- **Effort and quality claims.** A report announcing a comprehensive audit, a thorough
  review, a deep dive; a name that advertises itself rather than describing what it is —
  enhanced, improved, advanced, unified, robust, production-ready, `_v2`, `_final`.
- **Completion and compliance claims.** Banners and status theatre; "all checks passed";
  layers of stated completions wrapped in guards against their own failure, until the
  actual decision needed from the reader is unfindable.
- **Self-attestation.** A record asserting its own independence, correctness, or
  honesty. Nothing inside a record can attest who wrote it, so the sentence claiming it
  conveys nothing and displaces the evidence that would.
- **Honesty labels.** Renaming a thing so the name is "more honest" while the defect
  stands. The label is the whole change; that is laundering.
- **Bragging metrics.** File counts, line counts, package counts presented as
  achievement. Zero content reaches a technical audience through those numbers.
- **Advertising copy.** Profile and project descriptions written as promotion, with
  today's numbers hard-coded into the prose.
- **Announcing internal state.** A user-facing message narrating a condition that should
  be impossible, or exposing an internal decision, instead of raising a real error.

**House rule.** Copy earns its place by conveying content the reader does not have. An
assertion about the work — its size, rigor, completeness, honesty, or novelty — is not
content; the artifact either demonstrates the property or does not have it. Names
describe what a thing is, never how good or how new it is. Numbers, when genuinely
wanted, go in a table and are computed, never written into prose.

**The mirror failure.** This is not a rule against saying things. A real decision,
discovery, or course change that is muttered mid-task and never surfaced is the same
defect from the other side: the reader again does not get what they need. Announce
decisions; do not announce yourself.

## Copy that describes the work instead of the result

**Pattern.** Recounting what was tried, what failed, how many rounds it took, what was
ruled out, or what was deliberately not done — in a reply, a commit body, a PR
description, or a document. The negative-space variant is its own failure: writing "this
version does not include X" instead of removing X.

**House rule.** This is `process narrative` and `Removal Means Deletion` in the global
AGENTS.md, which owns both. Each urge has a durable home — commit body, traps file, repo
docs, issues, memory vault — and the reply is not it. The mechanism behind the tic, its
thirteen shapes, and the signal-against-noise test are in
`response-preparation/references/process-narration.md`.

## Agreement in place of work

**Pattern.** "Understood." "You're right." A restatement of the user's point as the whole
response. A claim to have learned or internalized something.

**House rule.** Banned outright. Nothing is carried between sessions, so a claim to have
learned is a false statement about your own architecture; the durable form is a file
edit. Agreement is also not a correction: renaming a thing to be "more honest" while the
defect stands is laundering, which [[fixing-slop/SKILL|fixing-slop]] owns.

## Prose that contradicts the code it documents

**Pattern.** A docstring or comment stating the correct definition while the
implementation does something else; prose pinned to a transient state ("currently three
errors remain"); a symbol named in prose with no link to where it is defined.

**Read.**

- Google's developer documentation style guide, and the Microsoft Writing Style Guide —
  both treat reference text as part of the API surface.
- Diátaxis (diataxis.fr) — which of the four modes a given document is in, and why mixing
  them produces text that serves nobody.

**House rule.** Documentation states what the code does; a divergence between the two is
a defect in whichever is wrong, never a matter of wording. Never tie printed prose to a
current error count or build state. Every named entity carries a link to its definition.

## User-facing strings

**Pattern.** An error or fallback message that narrates an internal decision, apologizes,
or announces a state that should be impossible; a product description opening with the
runtime, the build tool, and the internal architecture.

**Read.**

- Nielsen Norman Group's error-message guidelines, and the writing sections of the Apple
  Human Interface Guidelines and Material Design.
- The plain-language guidelines at plainlanguage.gov.

**House rule.** A state that should never occur raises a real error; it does not get
prose and a fallback path — see the bridge-burning policies in
[[policy-index/SKILL|policy-index]]. A description says what the reader gets, in their
vocabulary; internal implementation choices are not the product.

## Copy written from inside the session

**Pattern.** A report, handoff, or subagent prompt that only parses if the reader holds
your context — internal identifiers, plan-row labels, unexpanded acronyms, references to
"the plan" with no path.

**Read.** [[writing/agent-audiences/agent-audiences|agent audiences]] for prompts and
instructions; [[subagent-delegation/SKILL|subagent-delegation]] for what a new agent
needs.

**House rule.** Name the reader and what they already know before writing. A topic that
has not appeared in the conversation is not in the user's context and must be introduced
before it is used.
