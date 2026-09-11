# Situation to Source

This file is a hook, not a textbook. Each row names a situation in which agent priors
here have produced broken, backwards, or incoherent designs, and routes to the
authoritative treatment of that subject. Read the source. The local notes exist only for
house deviations, which no external source states.

The purpose is to land in the literature of the field — books, manuals, specifications,
reference documentation, papers — rather than in the far larger body of casual writing
about the same words.

Parent: [[code-patterns/general/general|general patterns]].

## Decomposition, ownership, and module boundaries

**Situation.** Deciding where a behavior lives; a central file that must be edited to add
an instance; a facade written over a component instead of fixing it; two places that
state the same fact; a wrapper that only renames another API.

**Read.**

- Parnas, *On the Criteria To Be Used in Decomposing Systems into Modules*, CACM 15(12),
  1972 — information hiding, and why decomposition by processing step is the wrong seam.
- Ousterhout, *A Philosophy of Software Design* — deep modules, interface versus
  implementation complexity, pass-through methods.
- Hunt & Thomas, *The Pragmatic Programmer* — DRY stated correctly: one authoritative,
  unambiguous representation of each piece of knowledge, which is about knowledge, not
  about text.
- Brooks, *The Mythical Man-Month*, ch. 4 — conceptual integrity, and why one owner of a
  design decision beats many good decisions.

**House deviation.** Ownership here extends past code to documents: a fact owned by a
repository's code, issues, or plans is not restated in prose elsewhere, and a migration
is unfinished while the source still exists.

## Measurement, metrics, and proxies

**Situation.** Reporting a count as progress; optimizing an error count, page count, test
count, or line count; a number appearing twice in one work unit; a metric typed into a
user-facing surface.

**Read.**

- Austin, *Measuring and Managing Performance in Organizations*, 1996 — measurement
  dysfunction: the pattern by which measured parties optimize the measure, and the
  conditions under which it is guaranteed.
- Goodhart's law, and the *measurement dysfunction* literature it anchors.
- Deming, *Out of the Crisis* — management by visible figures alone as a named deadly
  disease.

**House deviation, on method rather than reporting.** A mechanical check cannot stand in
for a semantic judgment. Byte-identity, checksums, and diff size answer "are these the
same bytes", never "do these say the same thing" — so they cannot decide whether two
notes duplicate each other, whether migrated content preserved its meaning, or whether a
construction matches its specification. Work whose question is semantic is read, not
hashed. The mirror failure is doing by hand what a symbolic tool does exactly: a
rename across hundreds of call sites belongs to an LSP or `ast-grep`, not to a fan-out of
agents editing text.

**House deviation.** Reported numbers must be computed at build time or served as data,
never written by hand into a surface, and must be quantities the audience values —
theorems and definitions for a mathematics project, not lines of code.

## What a document is for

**Situation.** Writing a README, a product description, a reference page, or a study
guide; deciding page granularity; a description that opens with internal implementation
choices; a dump with no index, search, or pagination.

**Read.**

- Diátaxis (diataxis.fr) — the four documentation modes, and why mixing them produces
  documents that serve nobody.
- The Stacks Project, introduction and conventions — an authored mathematical text
  broken into tags for navigation, citation, and reuse.
- Wikipedia's Manual of Style, especially summary style and article structure — the
  canonical treatment of splitting and merging reference pages by reader need.

## Genericity and level of abstraction

**Situation.** A proof or function that works because of a hypothesis the code never
states; hard-coding the one case you were shown; treating an illustrative example as a
ruling.

**Read.**

- Riehl, *Category Theory in Context* (free from the author) — universal properties, and
  what it means for a construction to be determined rather than chosen.
- nLab entries on universal property, structure versus property, and forgetful functors.
- Ousterhout, *A Philosophy of Software Design*, on general-purpose versus special-purpose
  interfaces.

**House deviation.** The direction is toward formulations that survive dropping
finiteness, freeness, projectivity, commutativity, rings to semirings, groups to monoids.
[[mathematics/objects-in-code/objects-in-code|objects in code]] carries the mathematical
instances.

**Citing the general form while shipping the special case.** A specific and damaging
variant: the search is done, the general solution is found and named in the write-up, and
then the narrow version is built because the general case is not needed *yet*. The
citation reads as diligence and is in fact the evidence against the decision — it records
that the general form was known and declined. The debt falls due on the next feature, and
is paid by whoever asks for it.

When the general form is understood and the marginal cost over the special case is small,
build the general form. When it is genuinely large, that is a real decision and belongs
in the plan with the cost stated, not in a status note as a thing not done. The test:
name the change that would force the general case, and ask whether it is plausible in
this project. A second character size in a game, a non-free module in an algebra library,
a second tenant in a service — if the answer is that it is coming, the special case is
already wrong.

## Contracts and interfaces

**Situation.** Hand-rolled "raise unless overridden"; an obligation discovered at runtime
rather than at instantiation; an interface shaped by what was convenient to expose rather
than by what its consumer requires.

**Read.**

- The language's own abstract-base-class or trait documentation — in Python, `abc` and
  the data model reference.
- Meyer, *Object-Oriented Software Construction*, on design by contract.
- The consumer's specification, whenever one exists: an endpoint built for a client
  standard is judged against that standard's document, not against plausibility.

## Established patterns before invention

**Situation.** About to design a mechanism in a domain with practitioners; about to coin
a noun; about to write a parser, matcher, state machine, or scheduler.

**Read.** The domain's canonical reference first —
[[known-solution-first/SKILL|known-solution-first]] owns the procedure, and the domain
skills carry the specific texts. A noun you had to invent is evidence that the standard
model was not consulted.

## Tests as statements

**Situation.** Writing a test that records current output; weakening an assertion to make
it pass; asserting an input shape no caller produces.

**Read.**

- Claessen & Hughes, *QuickCheck: A Lightweight Tool for Random Testing of Haskell
  Programs*, ICFP 2000 — properties as the unit of specification.
- The Hypothesis documentation, on choosing properties and shrinking counterexamples.
- [[test-guidelines/SKILL|test-guidelines]] and
  [[mathematics/research/mathematical-testing/mathematical-testing|mathematical testing]]
  for the house proof rules, which are stricter than any of the above.
