---
name: writing-clearly-and-concisely
description: Use when writing or editing any prose a human will read — docs, commit messages, error messages, explanations, or UI text.
---
# Writing Clearly and Concisely

## Policy index

The numbered rules below carry stable IDs. Cite the ID with the affected passage.

| Policy ID | Rule location |
| --- | --- |
| `CLARITY001`–`CLARITY007` | [Grammar and punctuation](#elementary-rules-of-usage-grammarpunctuation) |
| `CLARITY008`–`CLARITY018` | [Composition](#elementary-principles-of-composition) |
| `CLARITY019` | [Preserve meaning and voice](#preserve-meaning-and-voice) |
| `COPY002` | [[writing/technical-copy/technical-copy#explain-dont-perform-explanation|Explain the actual relation]] |
| `COPY003` | [[writing/technical-copy/technical-copy#lists-that-replace-explanation|Lists that replace explanation]] |

## Overview

William Strunk Jr.'s *The Elements of Style* (1918) teaches you to write clearly and cut
ruthlessly.

## When to Use This Skill

Use this skill whenever you write prose for humans:

- Documentation, README files, technical explanations

- Commit messages, pull request descriptions

- Error messages, UI copy, help text, comments

- Reports, summaries, or any explanation

- Editing to improve clarity

**If you’re writing sentences for a human to read, use this skill.**

## All Rules

### Elementary Rules of Usage (Grammar/Punctuation)

1. **`CLARITY001`** — Form possessive singular by adding 's

2. **`CLARITY002`** — Use comma after each term in series except last

3. **`CLARITY003`** — Enclose parenthetic expressions between commas

4. **`CLARITY004`** — Comma before conjunction introducing co-ordinate clause

5. **`CLARITY005`** — Don’t join independent clauses by comma

6. **`CLARITY006`** — Don’t break sentences in two

7. **`CLARITY007`** — Participial phrase at beginning refers to grammatical subject

### Elementary Principles of Composition

8. **`CLARITY008`** — One paragraph per topic

9. **`CLARITY009`** — Begin paragraph with topic sentence

10. **`CLARITY010`** — **Use active voice**

11. **`CLARITY011`** — **Put statements in positive form**

12. **`CLARITY012`** — **Use definite, specific, concrete language**

13. **`CLARITY013`** — **Omit needless words**

14. **`CLARITY014`** — Avoid succession of loose sentences

15. **`CLARITY015`** — Express co-ordinate ideas in similar form

16. **`CLARITY016`** — **Keep related words together**

17. **`CLARITY017`** — Keep to one tense in summaries

18. **`CLARITY018`** — **Place emphatic words at end of sentence**

### Section V: Words and Expressions Commonly Misused

Alphabetical reference for usage questions

## Additional Principles

### Preserve meaning and voice

**Policy ID: `CLARITY019`**

Apply the economy and authorial-voice principles associated with William Zinsser's
*On Writing Well*: remove clutter while retaining the author's register and exact
meaning. Use [[llm-failure-modes/scholarly-prose|scholarly prose patterns]] for a
contextual editorial pass. Demonstrate redundancy, vagueness, or overstatement before
changing a rhetorical construction. Useful contrast, parallelism, and precise
technical terms take precedence over mechanical simplification.

### Avoid Pseudo-Explanation

**Policy: [[writing/technical-copy/technical-copy#explain-dont-perform-explanation|COPY002]]**

- **Explain, don't gesture.** Replace pseudo-explanatory verbs ("governed by", "driven by", "determined by") with the actual relation: a theorem, mechanism, mapping, or dependency.
- **Define before naming.** Don't introduce vague collections ("a small stock of", "a family of") without defining members or structure.
- **Show connections.** Enumeration is not exposition. State roles and relationships between listed items.
- **Omit gratuitous padding.** If a sentence adds nothing to what follows (like definitions), delete it.
- **Citations don't fix vacuity.** A claim needs content; references cannot repair a sentence that fails to communicate.

### Distinguish Description from Performance

Apply [[writing/technical-copy/technical-copy#lists-that-replace-explanation|COPY003: lists that replace explanation]]
to comma-separated catalogues and repeated lists embedded in sentences. Identify
the missing relation or redundant terms before revising. Preserve useful
enumerations; repair the reasoning rather than merely changing punctuation.

Writing that performs the appearance of explanation without explaining anything is slop. Prefer concrete statements about objects, maps, constraints, and evidence over scholarly-sounding filler.

## Bottom Line

Writing for humans? Read `elements-of-style.md` and apply the rules. Prefer substance over form.
