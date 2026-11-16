# Scholarly Prose Patterns

Use this catalog when revising prose or reviewing exposition under code `PROSE`.
It covers editorial defects, not attribution of text to an AI system.

## Evidence before editing

Read the passage in its argument and identify the audience. For each proposed
finding, locate the wording, name the specific lost information, repetition, or
unsupported inference, and give a correction that preserves the claim. A recurring
pattern requires representative passages from across the inspected scope. A single
word, punctuation mark, parallel construction, or numerical list is not evidence of
a defect. Drop a finding if its only basis is resemblance to generated writing.

Compare the correction against the original hypotheses, quantifiers, qualifications,
attribution, and technical meaning. Reject a smoother rewrite that changes any of
these without justification. Separate mathematical errors from stylistic weaknesses.

## Patterns and repairs

The short examples below illustrate constructions, not quotations from a manuscript.

| Code | Pattern and evidence to seek | Repair and useful exception |
| --- | --- | --- |
| PROSE.01 | Counted title symmetry: a heading such as “Three estimators, three destinies” advertises a numerical arrangement instead of naming the result. | Name the subject or relation. Retain enumeration when the count is mathematically relevant. |
| PROSE.02 | Reused purchase metaphors: several unrelated results describe what an assumption “earns” or “pays for.” | State the bound, reduction, or information supplied. An isolated apt metaphor can remain. |
| PROSE.03 | Repeated corrective contrast: successive explanations introduce the subject by denying an alternative. | State the relation directly. Retain contrasts that distinguish genuinely confusable claims. |
| PROSE.04 | Invented misconception and reveal: an ordinary definition is introduced as a correction to an unspecified conventional belief. | Give the definition; support any historical claim with a source. |
| PROSE.05 | Unprompted defense: the paragraph denies a supposed defect without showing what mathematical issue exists. | State the reason for the choice or the hypotheses resolving the apparent conflict. |
| PROSE.06 | Compression promises: repeated claims that a chapter or argument reduces to a tiny slogan. | Give the actual claim with its conditions. A precise abstract can be brief. |
| PROSE.07 | Slogan headings: a heading such as “Regularization wins” substitutes a verdict for the comparison. | Identify the quantity, regime, or result; preserve the domain of the conclusion. |
| PROSE.08 | Manufactured lesson counts: summaries force heterogeneous observations into repeated fixed-size lists. | Group by mathematical dependence. Keep a list whose entries are independently useful. |
| PROSE.09 | Mirror sentences: matching clauses imply equivalence between mechanisms whose qualifications differ. | State each mechanism and its limits; use symmetry only when the claims support it. |
| PROSE.10 | Agency assigned to objects: an algorithm “wants” a parameter or a direction “chooses” a penalty. | Describe the optimizer, limiting value, or actual operation. Retain established technical terminology. |
| PROSE.11 | Economic decoration: a decomposition becomes a story about budgets or prices without defined economic quantities. | Name the terms and their dependence. Economic terminology is appropriate for actual economic models. |
| PROSE.12 | Repeated self-posed questions: each paragraph announces another question before giving an ordinary statement. | Express the dependency between results. Keep questions that organize a real open problem or requested tutorial. |
| PROSE.13 | Headings about explaining: repeated headings classify paragraphs as explanations rather than identifying their content. | Name the bound, assumption, proof, or interpretation being discussed. |
| PROSE.14 | Announced importance: a sentence declares significance but the following calculation already supplies the consequence. | Let the consequence establish relevance, or state the missing concrete consequence. |
| PROSE.15 | Scripted transitions: a conversational segue changes topics without explaining their connection. | State the transformation or dependency linking the topics. |
| PROSE.16 | Accumulated chapter promises: roadmaps, closing summaries, and previews repeat the same future work. | Keep the navigation needed to find a dependency; remove repeated promises. |
| PROSE.17 | Managerial branding: a routine calculation gets a named strategy, playbook, or audit label. | Use the established name of the mathematical procedure. |
| PROSE.18 | Moral approval replaces a property: a constant or estimator is praised as trustworthy without a defined guarantee. | Specify uniformity, coverage, error control, or the property actually proved. Preserve formally defined terms such as honest confidence sets. |
| PROSE.19 | Inflated scope disclaimers: dramatic universal alternatives exaggerate the limitation being excluded. | State the domain covered and the exact omitted case when relevant. |
| PROSE.20 | Duplicate caveats: nearby sentences repeat the same restriction with different wording. | Keep the restriction where it governs interpretation; repeat only at a separately necessary use. |
| PROSE.21 | Boxed recap duplication: a display box repeats adjacent advice without supplying a reference function or new synthesis. | Consolidate in the location readers need. A useful reference box can remain. |
| PROSE.22 | A result becomes a moral: a calculation ends with generic advice broader than the evidence. | State the consequence within the calculation's hypotheses. |
| PROSE.23 | Promotional significance: novelty or importance is asserted through praise rather than an identified contribution. | Name the result and the evidence for the claimed advance. |
| PROSE.24 | Vague authority: unspecified specialists or literature supposedly establish a claim. | Verify and cite a particular source for that claim, qualify it, or remove the unsupported assertion. |
| PROSE.25 | Boilerplate analysis: generic openings, conclusions, or future-work paragraphs contain no specific problem or result. | Supply the actual unresolved question or cut the empty material. |
| PROSE.26 | Decorative participles: a sentence ends by claiming to demonstrate importance or potential without a further inference. | State the causal or mathematical connection, or end at the supported assertion. |
| PROSE.27 | Mechanical cadence: repeated paragraph molds, transitions, or ornate substitutions obscure logical distinctions. | Let argument structure determine sentence form. Keep precise vocabulary and deliberate authorial patterns. |

## Calibration examples

- A heading “Two connected components” describes a mathematical fact; its numeral is
  not a finding under PROSE.01 or PROSE.08.
- A repeated slogan claiming an estimator always improves prediction is a finding
  when the cited bound holds only under a specified noise model. The repair restores
  that model and states the bound, rather than merely replacing the slogan's words.
- A contrast between pointwise and uniform convergence can be essential. Flagging
  every negative construction would destroy the distinction it teaches.
- An unfamiliar technical term should stay when replacing it with an ordinary word
  changes its definition. Editorial simplicity cannot weaken mathematical precision.

## Limits of the evidence

Editorial guidance about recurring AI prose and studies of vocabulary shifts can
motivate inspection. Population-level frequencies from a particular dataset cannot
identify the author or generator of an individual passage. Verify a study and its
scope before citing it; do not invent bibliographic support for this catalog.
