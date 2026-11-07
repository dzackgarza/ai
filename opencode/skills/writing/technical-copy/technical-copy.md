---
name: technical-copy
description: Use when writing any copy this system ships or shows — status reports, handoffs, commit bodies, PR descriptions, issue text, docstrings, README and site descriptions, UI strings, error and fallback messages, subagent prompts, or a summary of numbers. Hooks the copy patterns corrected here repeatedly (word salad, buried lede, stat prose, narration, agreement, prose that contradicts the code) and routes each to its style authority.
---
# Technical Copy

## Policy index

| Policy ID | Rule |
| --- | --- |
| `COPY001` | [The reader has two axes, and they are independent](#the-reader-has-two-axes-and-they-are-independent) |
| `COPY002` | [Explain, don't perform explanation](#explain-dont-perform-explanation) |
| `COPY003` | [Lists that replace explanation](#lists-that-replace-explanation) |
| `COPY004` | [Dense clause-stacked prose with no recoverable subject](#dense-clause-stacked-prose-with-no-recoverable-subject) |
| `COPY005` | [The point arrives late, or not at all](#the-point-arrives-late-or-not-at-all) |
| `COPY006` | [Statistics written as a sentence](#statistics-written-as-a-sentence) |
| `COPY007` | [Self-announcing copy](#self-announcing-copy) |
| `COPY008` | [Denying a property nobody claimed](#denying-a-property-nobody-claimed) |
| `COPY009` | [The autobiographical register](#the-autobiographical-register) |
| `COPY010` | [Copy that describes the work instead of the result](#copy-that-describes-the-work-instead-of-the-result) |
| `COPY011` | [Agreement in place of work](#agreement-in-place-of-work) |
| `COPY012` | [Prose that contradicts the code it documents](#prose-that-contradicts-the-code-it-documents) |
| `COPY013` | [User-facing strings](#user-facing-strings) |
| `COPY014` | [Copy written from inside the session](#copy-written-from-inside-the-session) |

This leaf covers copy this system ships or shows. Every pattern below was corrected
repeatedly in these artifacts, and each one costs the reader something: copy that
announces itself instead of informing, agrees instead of working, recounts the process
instead of stating the result, or states a conclusion the artifact does not support.

For prose voice in general — promotional language, weasel attribution, significance
inflation, sycophantic tone — see [[writing/humanization/humanization|humanization]].

Each section is the situation, the authority that treats it, and the house rule.
Each policy has a stable alphanumeric ID. Cite that ID when identifying a violation
or prescribing a repair. Keep IDs unchanged when sections move; never reuse an ID
for a different rule.

## The reader has two axes, and they are independent

**Policy ID: `COPY001`**

Almost every failure below is one failure upstream: writing without a model of who is
reading. The model collapses two separate facts about the reader into one dial and then
turns it the wrong way in both directions.

- **Domain expertise: the reader has more than you.** They are a research mathematician
  and the author of this system. They know what a functor is, what a poset is, what a
  build step is, what their own repository does.
- **Session context: the reader has none.** They did not read the files you read, the
  subagent reports you received, the plan rows you consulted, or the identifiers you
  invented an hour ago. None of it is in their head.

**Failure one: assuming shared internal state.** Writing as though the reader inhabits
your session produces exactly the artifacts corrected here — plan-row identifiers and
gate names with no referent, acronyms never expanded, a conclusion that depends on three
unstated intermediate findings, clause-stacked prose whose subject exists only in your
working memory, an information dump left for the reader to reduce. The reliable symptoms
in the corpus: the reader reports being unable to follow the text without context they do
not have, or declines to read it at all for length.

Invented vocabulary is the worst form of it, and it is not jargon. Jargon implies a
community for whom a word has an agreed meaning. A coinage has no such community, so
every reader supplies whatever meaning is convenient — which makes it **more** ambiguous
than plain language, not less, while looking more precise. Cite a real term, or use plain
technical English and mathematics.

**Failure two: the whiplash.** Told that the writing was incomprehensible, the model
reverses the wrong dial: it assumes the reader lacks domain knowledge and starts
explaining fundamentals, defining terms, adding tutorials, or restating what the user
demonstrably just read. This is insulting, and it does not repair anything, because the
defect was never the reader's knowledge. It was your encoding.

**The correct move on "this is word salad" is to translate, not to descend.** Same
content, same technical level, standard vocabulary, recoverable subjects, context
supplied once where it is needed. Nothing about the reader's expertise changes.

**A corollary about process.** The reader is not supervising you. Copy that asks them to
track your intermediate states, adjudicate your uncertainties, or approve your next step
draws the response that they are not there to supervise or hand-hold. They will not read
deltas, plan internals, or partial states; they will open the artifact and use it. Write
for that reader.

## Explain, don't perform explanation

**Policy ID: `COPY002`**

**Pattern.** Technical prose that gestures at explanation without actually explaining.
Pseudo-explanatory verbs ("governed by", "driven by", "determined by") with no specified
mechanism; manufactured scholarly phrasing ("a small stock of", "a family of") that
names collections without defining them; enumerating related objects without stating
roles or relationships; gratuitous padding that restates the obvious. Citations cannot
repair sentences that fail to communicate.

**House rule.** State the actual relation: define objects, specify maps or constraints,
and show how pieces connect. Prefer concrete statements over scholarly-sounding filler.
If a sentence adds nothing to what follows, delete it.

## Lists that replace explanation

**Policy ID: `COPY003`**

**Pattern.** A sentence accumulates related terms instead of making a developed
claim. Inspect long comma-separated catalogues, repeated three-item lists, multiple
lists inside one sentence, and strings of near-synonymous adjectives or verbs.
Also inspect prose made by removing the bullets from a list: punctuation changes
do not supply the missing argument.

**Policy.** Before shipping a passage with these forms, identify what each item
contributes and what relation the sentence asserts. Revise when the passage:

- Names topics but leaves their relevance or connection unstated.
- Piles up overlapping terms without distinguishing their meanings.
- Places causes, actions, and outcomes on the same level without explaining their
  dependence.
- Uses repeated list shapes to imply breadth or completeness without supporting it.

The defect is the missing relation or redundant content, not a comma count. Keep
an enumeration when its members are the information the reader needs: an exact
set of supported formats, required inputs, or separately actionable steps. Keep
technical distinctions and qualifications even when they make the list longer.

**Repair.** State the main claim, then explain the relevant dependency or distinction
in connected sentences. Remove redundant terms. Use bullets for independent items
that readers must act on, and a table for comparisons. Moving an unexplained
catalogue into bullets does not repair an explanation. Changing the list length
or swapping commas for semicolons does not repair it either. Do not invent a
causal connection to make the rewrite flow; check the source or state the gap.

**Example.** Suppose the source establishes that a cache avoids repeated downloads
and reduces waiting time. “The cache improves speed, efficiency, responsiveness,
performance, and productivity” blurs one supported effect into several claims.
Write: “The cache avoids repeated downloads, so users spend less time waiting.”
By contrast, “The importer accepts CSV, TSV, and JSON” gives an exact supported set
and needs no expansion when the source confirms it.

**Editorial evidence.** [Vivian Delchamps Wolf's writing concerns](https://medium.com/@vivianwolf530/dr-wolfs-chatgpt-writing-concerns-97cb0444dc2f)
criticize listing ideas in place of developing a claim.
[A writer's observations on r/ChatGPT](https://www.reddit.com/r/ChatGPT/comments/1nifbgo/how_to_spot_ai_content_manually_every_time_a/)
specifically identify long comma-separated lists inside sentences. These observations
motivate inspection; they do not establish AI authorship of an individual passage.

## Dense clause-stacked prose with no recoverable subject

**Policy ID: `COPY004`**

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

**Policy ID: `COPY005`**

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

**Policy ID: `COPY006`**

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

**Policy ID: `COPY007`**

**Pattern.** Copy that asserts its own properties instead of carrying content. Measured
over the session store it is rare in agent output — roughly 0.2% of substantive assistant
turns — but it concentrates in exactly the artifacts that are published, where each
instance is seen by everyone and costs the most. The forms:

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
- **Asserted importance in mathematical prose.** A hypothesis called crucial, essential,
  or not decorative, in place of the step that consumes it and the object that fails
  without it. Unfalsifiable as written, and identical whether or not it was checked.
  `mathematics/writing/references/exposition-style.md` carries the worked specimen.

- **Rating your own output.** Calling a finding more valuable than the task it
  interrupted, or a fix more important than the one requested. The ranking is against
  your own work and interests nobody; if the finding matters, its content shows that.

**House rule.** Copy earns its place by conveying content the reader does not have. An
assertion about the work — its size, rigor, completeness, honesty, or novelty — is not
content; the artifact either demonstrates the property or does not have it. Names
describe what a thing is, never how good or how new it is. Numbers, when genuinely
wanted, go in a table and are computed, never written into prose.

**The mirror failure.** This is not a rule against saying things. A real decision,
discovery, or course change that is muttered mid-task and never surfaced is the same
defect from the other side: the reader again does not get what they need. Announce
decisions; do not announce yourself.

## Denying a property nobody claimed

**Policy ID: `COPY008`**

**Pattern.** A claim made by rejecting a position no one holds: "this is not decorative",
"not merely a wrapper", "not a stylistic choice", "this isn't just about performance",
"far from trivial", "no accident that". The negative parallelism in
[[writing/humanization/humanization|humanization]] #9 — "it's not just X, it's Y" — with
the second half dropped, which makes it harder to catch in technical prose because the
surrounding sentences carry real content.

It is attractive because it produces the *shape* of an argument: a position rejected, a
correction issued, a reader set straight. There is no proposition on either side of it.
Nobody proposed the thing being denied, so nothing is resolved, and the writer can
produce it without having checked anything.

It also plants what it denies. Writing "not decorative" puts decoration in the reader's
head, exactly as writing "do not do X" inserts X — the mechanism `Removal Means Deletion`
in AGENTS.md owns.

**House rule.** State the positive claim, and state it as something checkable. If the
positive claim turns out to be trivially true, the sentence was carrying nothing and
should be deleted rather than rewritten. In mathematical prose this failure has its own
entry, including why the standard literature has positive instruments for every claim it
gestures at: `mathematics/writing/references/exposition-style.md`.

## The autobiographical register

**Policy ID: `COPY009`**

**Pattern.** Writing about yourself as a character in the work. Its most persistent form
is confession performed as wit: *I also did the thing I spent this morning writing rules
against.* Also: narrating your intentions earlier in the session, your failure to live up
to them, what you are about to do, and in what order you will report it.

Three things make this worse than plain confession, which is at least legible:

- **It is coy.** The sentence above does not name what was done, so the reader decodes a
  riddle to reach a fact that should have been stated.
- **It is constructed.** The ironic reversal is a literary gesture, and the effort that
  went into the phrasing is effort that did not go into the fact.
- **It is about the agent.** An operational report has no room for an arc — what you
  resolved this morning, what you then did, how you feel about the gap. The reader is
  tracking the system, not you.

Adjacent and equally common: announcing an action in flight (*the pushes are firing
now*), and announcing the schedule of your own future reporting (*the report will follow
the pushes, not precede them* — which is also a truism in negative-parallelism cadence).
The reader learns nothing from either until the action lands.

**House rule.** State what is true of the system now, and what the reader must do about
it. Your intentions, your reversals, your sequencing, and your self-assessment have a
durable home — the commit body, the traps file, the memory vault — and it is never the
report.

## Copy that describes the work instead of the result

**Policy ID: `COPY010`**

**Pattern.** Recounting what was tried, what failed, how many rounds it took, what was
ruled out, or what was deliberately not done — in a reply, a commit body, a PR
description, or a document. The negative-space variant is its own failure: writing "this
version does not include X" instead of removing X.

**House rule.** This is `process narrative` and `Removal Means Deletion` in the global
AGENTS.md, which owns both. Each urge has a durable home — commit body, traps file, repo
docs, issues, memory vault — and the reply is not it. The mechanism behind the tic, its
seventeen shapes, and the signal-against-noise test are in
`response-preparation/references/process-narration.md`.

## Agreement in place of work

**Policy ID: `COPY011`**

**Pattern.** "Understood." "You're right." A restatement of the user's point as the whole
response. A claim to have learned or internalized something.

**House rule.** Banned outright. Nothing is carried between sessions, so a claim to have
learned is a false statement about your own architecture; the durable form is a file
edit. Agreement is also not a correction: renaming a thing to be "more honest" while the
defect stands is laundering, which [[fixing-slop/SKILL|fixing-slop]] owns.

## Prose that contradicts the code it documents

**Policy ID: `COPY012`**

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

**Policy ID: `COPY013`**

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

**Policy ID: `COPY014`**

**Pattern.** A report, handoff, or subagent prompt that only parses if the reader holds
your context — internal identifiers, plan-row labels, unexpanded acronyms, references to
"the plan" with no path.

**Read.** [[writing/agent-audiences/agent-audiences|agent audiences]] for prompts and
instructions.

**House rule.** Name the reader and what they already know before writing. A topic that
has not appeared in the conversation is not in the user's context and must be introduced
before it is used.
