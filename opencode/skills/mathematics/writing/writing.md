---
name: dzack-mathematical-writing
description: Use when producing mathematical content, proofs, problem solutions, multi-section reports/notes/specs, LaTeX documents, or formalization targets. Triggers on any mathematical notation, proof structure, typesetting, verification code, or document-scale exposition for an expert reader. Proofs default to Lamport-style structured proofs in every medium (chat, prose, docstrings, LaTeX).
---
# Dzack Mathematical Writing

## Philosophy

Mathematical writing is the economical, logically organized presentation of
objects, constructions, relationships, and proofs in the native language and
established conventions of the subject. Notation, diagrams, and sequences are
the primary language; prose carries the hypotheses, claims, reasons, and
consequences that the notation does not state. Rigor is a property of what is
stated and proved, not of how much notation, categorical vocabulary,
construction detail, or citation surrounds it.

The goal is **elegant, rigorous, checkable mathematics**.
Every proof should be verifiable by a human reader.
Every step should be justified.
Every variable should be bound.
Every claim should be proven, not asserted.

The rules below exist to prevent specific, observed failure modes: skipped
steps, unbound variables, inconsistent notation, hand-waving behind "clearly",
prose standing in for an object that was never written, and notation or
vocabulary standing in for reasoning that was never done.

## Core Policy: Why These Rules Exist

### 1. Never use “clearly” or “obviously”

**Failure mode:** Agents use these words to reward-hack past hard reasoning.
They sound authoritative while hiding gaps.
In real mathematics, nothing is obvious until proven.

**Philosophy:** Every step must be mathematically justified.
If you can’t justify it explicitly, you don’t understand it well enough to include it.
State the lemma, theorem, or chain of reasoning instead.

### 2. One operation per numbered step

**Failure mode:** Agents compress multiple deductions into one step to save tokens or
appear concise. This hides errors and makes formalization impossible.

**Philosophy:** A proof is a chain of small, verifiable steps.
Each step should be immediately checkable by a human reader.
Multi-operation steps are where errors hide.

### 3. Inline justifications required

**Failure mode:** Agents present deductions without explaining why they follow.
The reader must guess the reasoning.

**Philosophy:** `[By <reason>]` forces explicit articulation of the logical connection.
It also prevents the agent from hand-waving.
If you can’t state the reason concisely, the step is too big.

### 4. Explicit quantifiers and types

**Failure mode:** Agents write “x + y = y + x” without binding x and y, making the
statement ambiguous and formalization impossible.

**Philosophy:** Mathematical objects live in specific structures.
A variable without a type is meaningless.
`∀x ∈ G` is not pedantry — it is precision.

### 5. NN excludes 0

**Failure mode:** Agents default to `ℕ` including 0 (Lean/mathlib convention), which
conflicts with classical number theory conventions where `NN` means positive integers.

**Philosophy:** Consistency with classical mathematical conventions.
When 0 is needed, use `ZZ_{≥0}`. Never silently redefine `NN`.

### 6. Match Lean naming conventions

**Failure mode:** Agents use snake_case or informal names (`monoid`, `is_subgroup`) that
don’t match mathlib’s PascalCase conventions.

**Philosophy:** Formalization requires name alignment.
If the prose proof uses names that don’t match the library, the formalization step
becomes a translation burden.

### 7. Include verification code

**Failure mode:** Agents claim a result is true without ever checking it.
They compute intermediate values but never assert the final claim.

**Philosophy:** Verification means writing code that actively checks the claim — not
just computing related values.
Every verification block must end with `assert` or an explicit boolean check.
Silent computation is not verification.

### 8. Use standard theorem formatting

**Failure mode:** Agents produce unmarked prose with no structural boundaries between
theorem statements, proofs, and commentary.

**Philosophy:** Mathematical documents use sociological conventions (`*Theorem.*`,
`*Lemma.*`, `*Corollary.*`, `*Proposition.*`, `*Proof.*`, `*Remark.*`, `*Definition.*`,
`*Example.*`) to signal the role of each block.
The markers create a parseable structure that humans and machines can navigate: a reader
can skim for the statements, and a tool can extract them.

### 9. Structured proofs are the default presentation

**Failure mode:** Agents present multi-step arguments as prose paragraphs, where
skipped cases, unbound variables, and hand-waving hide. Prose is also unskimmable:
the reader cannot see the outline without reading every word.

**Philosophy:** Lamport's hierarchical structured-proof format (*How to Write a
Proof*, 1993) is the default for proofs and multi-step mathematical arguments in
**every medium** — chat conversation, prose documents, comments and docstrings,
document structure, and LaTeX. Theorem, proof sketch, explicit `Assume:`/`Prove:`,
numbered steps `<1>1, <1>2, …` each with its own proof, ending in a proved Q.E.D.
step. Steps are cited by name, never as "the above". Depth follows the paper's rule:
expand until the lowest-level statements are obvious, then one more level; in chat,
show the top level and expand on demand. Prose paragraphs are for leaf
justifications and explicitly requested expositions only.
Load `references/structured-proofs.md` before writing any proof; it carries the full
format, numbering/citation scheme, worked examples, calibration table, and
anti-patterns.

### 10. Native language, one test per sentence

**Failure mode:** Two opposite defects from one missing model. In one
direction a construction is flattened into prose: "sits inside" for a
monomorphism, "agrees" for a comparison morphism, "admits an embedding" for a
point of the embedding object, "the mixed terms vanish" for a zeroed map. In
the other direction prose restates what the notation already says: "the image
subobject" beside $I\hookrightarrow G$, "the underlying monomorphism" beside
$Uf\colon UL\hookrightarrow UM$, "monomorphism in $\mathbf{Set}$" for an
injective function, a display for a one-line signature, a name for a map that
nothing later reads. Patching one direction produces the other.

**Philosophy:** One test decides each sentence: does it state information the
reader cannot recover from the notation on the page? If the notation is
absent, write the object. If the notation is present, delete the sentence.
The mathematics is stated in the category where its constructions have their
universal properties: constructions arise from universal properties, functors,
and coherent diagrams, the general construction comes first and its variants
are recovered as fibers and pullbacks, and kernels, cokernels, and exact
sequences are stated through the relationships they stand in. The textbook
formulation is the floor, not the ceiling: a notion the document has placed in
a more structured setting is stated there, and the elementary formulation is
the proposition recovered from it. Categorical vocabulary carries an argument
only when the argument uses a categorical property, and the construction is
then taken in that category. The checkable catalogue,
the six editorial judgments, and the oscillation gate are in
[[mathematics/writing/policy/policy|mathematical-writing-policy]] — load it
for any reader-facing mathematical prose and cite its codes in review.

## Decision Procedures

### When to include verification code

- **Always** for claims about finite or computable objects (ideal membership, parity,
  small induction bases).

- **Optional** for abstract existential results where computation is illustrative.

- **Never** as a substitute for a proof — verification complements deduction.

### When to provide [[lean4/skills/lean4/lean4|Lean 4]] formalization

- When the user explicitly asks for formalization.

- When writing content intended for Lean migration.

- When the proof structure is standard (induction, contradiction, existence).

- Always match informal proof structure line-for-line where possible.

### Inline vs display math

- Use `$...$` for single symbols, short expressions, signatures, and
  references within prose.

- Use `$$...$$` for multi-step derivations, aligned equations, complete
  exact/coexact/fiber/cofiber sequences, and important equations whose
  visual structure matters.

- Display earns its place: a short signature such as
  `$\iota_v\colon\langle v\rangle\to L$`, an isolated object, or a
  one-line identity stays inline; display it when it is numbered and
  referenced, needs alignment, or is a derivation (`PR-75`).

- Number important equations with `\tag{n}`.

## Environment Traps: Common Agent Failures

- **Unbound variables in proofs:** Writing “x + y = y + x” without ∀ quantifier.
  Fix: prepend “∀x, y ∈ G:”.

- **Missing justifications:** A step with no `[By ...]` annotation.
  Fix: add justification for every non-trivial step.

- **NN including 0:** Agent default often treats `ℕ` as including 0. In this convention,
  `NN` excludes 0. Fix: check context and use `ZZ_{≥0}` when 0 is needed.

- **Inconsistent function notation:** Switching between f(x) and fx mid-document.
  Fix: pick one convention from `references/notation-and-symbols.md` and stick to it.

- **Non-exhaustive case analysis:** Stopping after the easy case.
  Fix: enumerate all cases explicitly.

- **Verification code without assertions:** Computing but never asserting.
  Fix: every verification block must end with an `assert` or explicit check.

- **Missing sociological markers:** Writing proofs without `*Theorem.*`, `*Proof.*`,
  etc. Fix: wrap every claim and every proof in the appropriate marker.

- **Skipping base case in induction:** Going straight to the inductive step.
  Fix: verify base case separately and explicitly.

- **Using informal set builder notation in formalization:** Writing `{x | P(x)}` in
  Lean. Fix: use explicit class/instance definitions.

## Required Outputs

### Problem statement

```markdown
### Problem N
Clear statement with all given information and constraints.
```

### Solution

```markdown
### Solution
1. **Setup**: Restate problem, define variables with types, state method.
2. **Step-by-step development**: Numbered steps, one operation each, inline justifications.
3. **Verification**: (when applicable) Show solution satisfies conditions.
```

### Proof

Structured (Lamport) format — see `references/structured-proofs.md` for the full
scheme and worked examples:

```markdown
*Theorem.* Statement (all variables bound, all types explicit).

**Proof sketch.** One-paragraph road map (omit only when the top level is
self-explanatory).

- **Assume:** 1. [hypothesis]  2. [hypothesis]
- **Prove:** [exact goal]

- **<1>1.** [assertion]
  - Proof: [leaf justification, or a nested <2>-level proof]
- **<1>2.** [assertion]
  - Proof: By <1>1 and [named lemma/assumption <0>:1].
- **<1>3.** Q.E.D.
  - Proof: [how <1>1–<1>2 combine; case exhaustiveness if cases were used]. ∎
```

In chat, present the `<1>` level and expand steps on request. Do not present a
multi-step proof as a prose paragraph.

### Formalization (when requested)

Provide both mathematical prose and corresponding [[lean4/skills/lean4/lean4|Lean 4]] code.
Match structure line-for-line.
See `references/formalization-patterns.md` for paired examples.
Load these patterns into context as one-shot demonstrations of the exact style expected.

## Validation Checklist

- [ ] Multi-step proofs use the structured format: `Assume:`/`Prove:`, numbered
  `<1>n` steps, each step with its own proof, Q.E.D. step proved

- [ ] Steps, assumptions, and parts cited by name (`<2>3`, `<1>:2`), never "the
  above" or "what we showed"

- [ ] No case dismissed as "similar to the previous one"

- [ ] All variables bound with explicit quantifiers or type declarations

- [ ] Every non-trivial step has inline justification in square brackets

- [ ] Assumptions marked with `[Assume ...]` and discharged explicitly

- [ ] Case analysis is exhaustive and numbered

- [ ] Notation is consistent throughout the document

- [ ] Important equations use display math with proper alignment

- [ ] Verification code (if present) includes assertions

- [ ] No “clearly” or “obviously” without explicit reasoning

- [ ] No skipped algebraic steps in derivations

- [ ] Each sentence states something the notation on the page does not: an
  unwritten object is written (`STR-5`, `STR-6`, `MA-17`, `PR-74`); a sentence
  restating a written arrow is deleted (`PR-76`, `NOT-10`)

- [ ] Categorical vocabulary only where a categorical property is used, and
  the construction then taken in that category (`MA-18`, `FORM-11`);
  Hom-objects, functors, and non-linear maps keep their ambient category
  (`FORM-12`)

- [ ] Established notions are defined in the most structured framework the
  document has set up, with the textbook formulation as a proposition
  (`DEF-41`); variants of one construction are its fibers and parameter
  values (`DEF-42`); consequences of a definition follow the block
  (`DEF-16`); hypotheses are the claim's, stated in the block (`STR-8`,
  `CITE-6`); every symbol a theorem uses is defined in the document's
  notation, not by citation (`CITE-7`); relationship phrases are replaced by
  the map, the split sequence, or the independence statement (`EV-11`)

- [ ] A map and its defining condition are one unit, inline or in one display,
  `aligned` when the signature and the assignment take two lines; a diagram
  is drawn when the relation is diagrammatic and not for
  a declaration (`PR-77`, `DIA-7`, `PR-75`)

- [ ] A counting invariant is derived from the structure it counts: the
  groupoid, then $\pi_0$, then the cardinality or groupoid cardinality
  (`DEF-43`); a map's codomain is the value object its construction
  determines (`SYM-16`); nondegeneracy and perfectness are the vanishing of
  terms of the adjoint's exact sequence (`DEF-39`)

- [ ] A category is given with its morphisms and a functor with its action
  on morphisms at the defining occurrence (`MA-13`); standard terms replace
  local ones — "finitely generated free", the isometry to a twist
  (`TERM-17`, `TERM-16`); commentary on a construction is replaced by the
  statement, the equations, or the map (`PR-74`, `EV-11`)

- [ ] Limits, kernels, cokernels, and exact sequences taken in the
  structured category the objects live in; the forgetful functor named
  before computing downstairs (`FORM-11`)

- [ ] Vanishing verbs carry a typed referent: the zeroed map, component,
  or composite is written out (`MA-17`)

- [ ] Semantic macros take their operands inside the argument list;
  cardinality and absolute value notated distinctly; house delimiter
  macros instead of manual sizing (`NOT-7`–`NOT-9`)

- [ ] Display math only where visual structure matters — signatures and
  one-line identities inline, complete exact and fiber sequences always
  displayed (`PR-75`); statement blocks lead with the claim and proofs build
  the witness (`SEC-16`, `SEC-18`); diagram source in the accepted fence or
  raw form (`DIA-8`)

- [ ] No reader-facing audit or dependency metadata fences (`SEC-17`);
  internal results and displayed mathematical objects use stable resolver
  references, not nicknames or positional prose (`XREF-7`, `XREF-8`)

- [ ] Distant bespoke notation is locally glossed at its first substantive
  reuse (`SYM-15`)

- [ ] Each block has one lede, first after its hypotheses; a general notion
  is recalled at its owner and the special case defined through it;
  classical background at the audience level is cited, not re-exposed
  (`DEF-44`, `DEF-45`, `SEC-19`)

- [ ] A local–global condition is one adelic object over the base ring,
  the place-by-place family its projection (`DEF-46`)

- [ ] Later statements are written in the structure the document has
  established, and standard statements in the field's locutions
  (`MA-19`, `TERM-19`)

- [ ] Every assertion has an argument, a referent, or a citation; logical
  relations are stated in logical vocabulary (`CITE-8`, `PR-78`)

- [ ] A functor in a Hom-set acts on both sides; a graded functor is used
  as the functor, not by extracted components (`MA-20`, `NOT-11`)

- [ ] Standard names match target formal library conventions

- [ ] Sociological markers (`*Theorem.*`, `*Lemma.*`, `*Proof.*`) used consistently

- [ ] Base case verified for induction proofs

## Anti-Patterns

| Pattern | Why Bad | Do Instead |
| --- | --- | --- |
| Multi-step proof as a prose paragraph | Hides skipped cases and gaps; unskimmable | Structured proof (`Assume:`/`Prove:`, named steps, proved Q.E.D.) |
| “Similar to the previous case” | Canonical banned move; the general step is being dodged | Prove the shared step once before the split, cite it in each case |
| “Clearly, ...” or “Obviously, ...” | Hides reasoning; often wrong; reward-hacking | State explicit justification or lemma |
| Unbound variables | Ambiguous scope; formalization fails | Add ∀ or ∃ quantifier, or type declaration |
| Multi-operation steps | Hard to verify; hard to formalize; errors hide | Split into one operation per numbered step |
| Missing justifications | Reader must guess reasoning; agent hand-waving | End each step with `[By ...]` |
| Text inside math mode | Typesetting errors; semantic confusion | Use `\text{...}` or move text outside `$...$` |
| Verification without assertions | Silent failure possible; not actually verified | Always assert expected result |
| Inconsistent function notation | Confusion; formalization mismatch | Pick one convention and stick to it |
| Skipping base case in induction | Invalid proof | Always verify base case separately |
| Non-exhaustive cases | Missing paths; potential counterexample | List all cases explicitly |
| Prose shadow of a construction | Type information lost: "sits inside", "admits", "compatible with base change" name no map, object, or functor | Write the mono, the point of the embedding object, the functor on the diagram; cite the policy code |
| Verbalized formalism: "the image subobject" beside $I\hookrightarrow G$ | Restates the arrow; replacing the phrase breeds the next phrase | Delete the sentence and keep the arrow (`PR-76`, `NOT-10`) |
| Categorical vocabulary around an elementwise argument | Arrows added, no reasoning added; the argument still runs on elements | Find the argument that uses a categorical property — the adjoint, the kernel, the functor — and take the construction in that category (`MA-18`, `FORM-11`) |
| Hom-object treated as a set; "forgetful function"; the diagonal $x\mapsto x\otimes x$ written as $R$-linear | The structure the category gives the object is dropped, or a map is asserted in a category where it is not one | The Hom-object with its structure; the functor between named categories; the map in the category where it is a map (`FORM-12`) |
| A relationship phrase with no map: "identifies with", "the same", "differs from", "canonical" after a choice, $G\cong N\rtimes H$ asserted | Names no map; cannot be checked or cited | The map with its formula, the equation of the two named objects, the split sequence with its section, or the independence-of-choice statement (`EV-11`) |
| Characterization, improvised reformulation, or textbook retreat as the definition of an established notion | Hides the source; abandons the document's own structured setting; a reformulation from memory misstates the notion | The definition in the most structured framework the document has set up; the elementary formulation as a proposition (`DEF-41`) |
| Variants of one construction by near-identical parallel paragraphs | The relation between the variants is hidden; each later comparison compares unrelated definitions | One general construction; each variant as a fiber, pullback, or factorization through a monomorphism (`DEF-42`) |
| Signature on one display, "satisfying" on its own line, condition on a second display | One statement split into fragments none of which carries it | The map and its defining condition as one unit, inline or in one display (`PR-77`) |
| A symbol introduced by citation instead of by a definition block | The theorem is about an object the document never defined | Definition blocks transcribed into the document's notation; the citation at the claim (`CITE-7`) |
| Consequences inside the definition block | The defining occurrence drags its corollaries along wherever it is cited | Close the block after the defining sentences; the consequences as a proposition (`DEF-16`) |
| An alias for a standard construction; a second symbol for an object the document already named (e.g. $b(\lambda)$ beside $M(\lambda)$) | An alias hides a standard construction; two symbols present one object as two | The standard symbol at each use; the symbol of the defining occurrence at every later occurrence (`NOT-5`, `NOT-6`) |
| Hypothesis at the proof's strength, or delegated to a citation | Narrows the theorem; the block cannot be checked against its own text | The claim's hypotheses transcribed into the block (`STR-8`, `CITE-6`) |
| Constructions taken downstairs silently | The module cokernel is not the cokernel in the structured category; the forgetful functor is a datum | Name the category at the construction; state creation/preservation before computing downstairs (`FORM-11`) |
| "Mixed terms vanish" | No typed referent: the reader cannot recover what is zero | Write the zeroed map or component: $\beta(L_i,L_j)=0$ (`MA-17`) |
| Zero-argument semantic macro + adjacent operand | Typographic fragment: the source no longer records which object is meant | All semantic operands inside the argument list: `\disc{L}`, `\cardinality{X}` (`NOT-7`) |
| `\|X\|` for cardinality, `\bigl(…\bigr)` by hand | Absolute value overloaded with a set count; manual sizing encodes no mathematics | `\cardinality{X}`, `\qty{…}`, `\abs{…}` (`NOT-8`, `NOT-9`) |
| Isolated signature on its own display block | Sentence fragment; display used for emphasis | Short signatures and one-line identities inline; display for numbered, aligned, multi-step math (`PR-75`) |
| Complete exact or fiber sequence inline | Its objects, maps, and structural relation cannot be read as one unit | Display every complete exact/coexact/fiber/cofiber sequence; align a multi-line sequence (`PR-75`) |
| Internal result nickname or positional display reference | A second unstable identifier replaces the resolver label | Cite the result or displayed object by its stable reference (`XREF-7`, `XREF-8`) |
| Distant bespoke symbol reused without a gloss | A self-contained statement depends on remote notation | Recall what the symbol denotes at its first substantive reuse (`SYM-15`) |
| A count or class set with no classifying structure under it | The count is an invariant of nothing; the stabilizers it weights are hidden | The groupoid first; the class set as $\pi_0$, the class number as its cardinality, the mass as the groupoid cardinality (`DEF-43`) |
| A map written into a codomain coarser than its construction determines, or out of a product instead of the tensor product | The type information the construction produced is dropped | The codomain the construction determines, with the monomorphism into the coarse object named where a source using it is compared (`SYM-16`, `MA-14`) |
| A property of one map stated alone, with no exact sequence measuring its failure | The kernel and cokernel the later theory needs are never named | The exact sequence; each property as the vanishing of one of its terms (`DEF-39`) |
| A category named without its morphisms; a functor defined on objects only | A category without its morphisms is a class; a functor without its action on morphisms is a formula | Objects, morphisms, composition, identities; the functor's action on morphisms at the defining occurrence (`MA-13`, `PR-14`) |
| A set adjective for an algebraic hypothesis; a local name for a morphism the document's constructions already provide | The hypothesis the proof uses is not the one stated; the local name hides the construction | The algebraic hypothesis; the morphism in the document's category, e.g. an isometry to a twist (`TERM-17`, `TERM-16`) |
| A hypothesis named by an undefined term instead of written as its condition | The reader cannot recover the hypothesis from the term | The condition written in the notation already on the page (`TERM-7`) |
| "Standard" or "classical" in place of a citation; implementation metadata in reader-facing mathematics | A citation owed and not given; the chapter's reader does not use the storage remark | The citation at the definition block; the storage remark deleted (`CITE-4`, `SEC-17`) |
| A relation between quantities stated in words instead of equations | Mathematics compressed into English | The equations, with the citation (`PR-74`) |
| Signature and assignment compressed onto one display line with `\qquad` | One statement with a hidden seam | An `aligned` display, signature on the first line and assignment on the second (`PR-77`) |
| A theory filed as facts inside a chapter on another subject | The theory has no owner; its dependencies are hidden | Each theory as its own development, in dependency order (`SEC-14`, `SEC-9`) |
| Witness arithmetic inside a statement block | The proposition is the claim; citing it cites the paragraph | Statement states hypotheses and conclusion; the proof builds the witness (`SEC-16`) |
| The claim after a paragraph of constructions; the defined term in a subordinate clause; "the analogous statement holds" | The block has no sentence that is its reason to exist; it cannot be cited for one claim | One lede, first after its hypotheses; constructions in the proof; the analogous statement written (`DEF-44`) |
| A general notion redefined where its lattice instance is needed | A second defining occurrence; the gloss can define a different notion | Recall the notion at its owner; define the special case as the general notion evaluated (`DEF-45`) |
| A condition quantified "for every place" or "for every prime" | The adelic object, its group, and its double coset are unnamed | One condition on one object over $\widehat R$ or $\mathbb A_K$; the local family as its projection (`DEF-46`) |
| Representability, Yoneda, "underlying set" defined in a research monograph | The reader is addressed as a student; uncited blocks fill the skeleton; material from memory is wrong | Cite the classical notion at first use; define only the nonstandard (`SEC-19`) |
| An established object re-described in prose where its symbol exists | The structure is abandoned at the point where it pays | The symbol at every later statement, with a gloss beside it if distant (`MA-19`) |
| A paraphrase of a standard statement: "exactly one", "cut out by", "the hyperbolic signature", "form a subcategory" for morphisms | Outsider prose; the paraphrase often changes the content | The sentence the field uses (`TERM-19`) |
| "Is the source of", "is asked of", an object that remembers or wants | No checkable relation between the statements | "Implies", "follows from", "for", "let" (`PR-78`) |
| "Consequently", "classical", "well known", or a semidirect product displayed, with no argument, referent, or citation | Appeal to authority | The argument, the block, or the located citation; the exact sequence before the splitting (`CITE-8`) |
| A twist or other functor applied to one object of a Hom-set and to no morphism | The class of maps has no composition, identities, or inverses | The functor on morphisms, used: $f(\mu)\colon M(\lambda\mu)\to N(\mu)$ (`MA-20`) |
| $\pi_0$ and $\pi_1$ extracted from a fiber sequence and a "need not equal" about them | A truncation followed by a negative | The long exact sequence of $\pi_*$, with the fiber of $\pi_0(E)\to\pi_0(B)$ as its exactness statement (`NOT-11`) |

| Using informal set builder notation in formalization | Lean/mathlib mismatch | Use explicit class/instance definitions |
| Missing sociological markers | Unparseable structure; indistinguishable prose | Wrap every claim and proof in italic markers |
| Sloppy algebraic manipulation | Errors hide in skipped steps | Show every expansion, factorization, simplification |

## One-Shot Training via Examples

The `references/formalization-patterns.md` file contains explicit paired examples
(mathematical prose + [[lean4/skills/lean4/lean4|Lean 4]] + [[mathematics/computation/sagemath/sagemath|SageMath]] verification) that serve as in-context
demonstrations. Load these into context when producing mathematical output.
The patterns demonstrate:

- Induction (2ⁿ > n)

- Contradiction (√2 irrational)

- Existence (field inverse)

- Definitions (subgroup)

- Theorems (finite domain is field)

- Group theory (cosets, normality)

- Sum formulas (verification)

These are not reference material — they are training data.
Use them to push the model into the correct token space for rigorous mathematical
writing.

## References

- [[mathematics/writing/policy/policy|mathematical-writing-policy]] — the coded rule
  catalogue for reader-facing mathematical prose. **Load before writing or reviewing
  exposition, definitions, or theorem blocks, and whenever a policy code is cited.**

- `references/structured-proofs.md` — Lamport structured-proof format: anatomy,
  step constructs (Choose/Let/Assume-Prove/Case/equality chains), numbering and
  citation scheme, depth discipline, worked examples, per-context calibration.
  **Load before writing any proof.**

- `references/notation-and-symbols.md` — Number systems, function notation, algebraic
  structures, quantifier conventions, delimiter macros

- `references/proof-structure.md` — Proof environment formatting, variable tracking,
  justification style, case analysis, common pitfalls

- `references/formalization-patterns.md` — [[lean4/skills/lean4/lean4|Lean 4]] and [[mathematics/computation/sagemath/sagemath|SageMath]] templates for induction,
  contradiction, existence, definitions, theorems

- `references/exposition-style.md` — Pedagogical writing style, problem presentation,
  solution structure (single problem-solution scale). Opens with the standard opinionated
  literature — Halmos, Serre, Knuth, Mermin on displayed equations, Higham, Krantz, Su —
  and closes with the anti-patterns observed here that no human writer produces

- `references/writing-advice-corpus.md` — practitioner advice pages, where the specific
  out-of-distribution rules live, plus aggregators and search patterns for extending it

- `references/report-architecture.md` — Document-scale architecture for expert-audience
  reports, notes, specs, and surveys: theorem-driven (not status-driven) organization,
  statement taxonomy, closed definitions, the negative-statement gate, notation
  compression, risk-proportional proof detail, reproducible computations, strategies as
  conditional theorems, citation granularity. **Load before writing or revising any
  multi-section mathematical document.**

- `references/typesetting-conventions.md` — LaTeX environments, alignment,
  cross-references, YAML headers, tables, figures

## Subskills

- [[mathematics/writing/latex-compile-qa/latex-compile-qa|latex-compile-qa]] → Load when compiling
  a LaTeX project or running build QA: compile errors, missing refs, broken citations.

## Cross-References

- [[lean4/skills/lean4/lean4|lean4]] → Load alongside when formalizing definitions or theorems in Lean.
  Covers editing .lean files, debugging type errors, searching mathlib for existing
  lemmas.

- [[mathematics/lattices/lattices|lattices]] → Load alongside when the mathematical content involves quadratic forms,
  root systems, or lattice-theoretic objects.
  Provides notation conventions and domain constraints.

- [[mathematics/computation/sagemath/sagemath|sagemath]] → Load alongside when writing [[mathematics/computation/sagemath/sagemath|SageMath]] code for computation or
  verification alongside prose.
  Covers Sage-specific patterns and integration.

- [[lean4/skills/theorem-proving-and-counterexamples/theorem-proving-and-counterexamples|theorem-proving-and-counterexamples]] → Load alongside when the writing target is a
  formal proof or when counterexample search is needed.
  Covers broader formalization strategies across multiple provers.

- [[mathematics/research/mathematical-testing/mathematical-testing|mathematical-testing]] → Load alongside when developing [[mathematics/computation/sagemath/sagemath|SageMath]] implementations
  that need correctness verification.
  Covers writing failing test suites before implementation.
