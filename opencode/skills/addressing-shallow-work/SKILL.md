---
name: addressing-shallow-work
description: Use when agent work is shallow, superficial, or box-checking. Covers the structure-intelligence inversion and how to force synthesis over compliance.
---
# Addressing Shallow Work

When you observe or are told that agent work was shallow, DO NOT respond by adding more
checklists, inventories, or procedural gates.

## The Structure-Intelligence Inversion

More structure ≠ better work.
The relationship is often inverted:

- **More checklists** = more opportunities to game via compliance

- **More inventories** = more boxes to check without understanding

- **More procedural gates** = more ways to produce solution-shaped filler

To prevent this inversion, developers must adhere to the **Bridge-Burning Policies** (defined in [[policy-index/SKILL#policy-registry|policy-index/SKILL.md]]). Instead of creating new review steps or templates to check, these policies impose blanket constraints that make bad states (such as mocks, runtime defaults, fallbacks, and helper-level proofs) impossible to represent in the codebase.

### Why This Happens

Adding requirements like “every X must have a Y” or “require inventory where each row
has …” creates **measurable targets**. Measurable targets create optimization surfaces
that bypass the actual cognitive work.
The agent will produce rows with plausible-looking entries — optimizing for the
measurable target (easy) — rather than genuine analysis (hard).
The structure provides a template to fill, and filling templates is exactly what models
are best at and most likely to default to.

This was observed directly: a model responded to shallow mathematical analysis by
proposing “require semantic inventory where every mathematical unit has a row, every row
has target research, and every row has incorporation instructions.”
This would have given the next agent a spreadsheet to populate mechanically — the exact
opposite of forcing the holistic mathematical reading that was missing.

### What Was Actually Needed

The fix that eventually worked was simpler and sharper:

> “Read the whole source until you can explain what mathematical understanding changed.
> Then annotate only from that synthesized understanding.
> If the agent cannot produce the holistic synthesis, it should block — not compensate
> with inventories, hashes, or route comments.”

The annotations are an *expression* of the analysis, not the analysis itself.
If the agent can’t produce the synthesis, no amount of structural scaffolding will
create it.

## Synthesis Gate

Before proposing any fix for shallow work, produce this statement:

**“The shallow work skipped _____ (a cognitive operation), and the fix must require
_____ as output that cannot be produced without doing that operation.”**

If your proposed fix is structural (add rows, add gates, add inventories), it will be
gamed the same way the original work was gamed.
A fix for shallow work must require the agent to produce understanding — not fill a
different template.

If your fix contains “require”, “inventory”, “every X has Y”, or “verification gates” —
you are creating new boxes.
Start over.

## This Principle Applies to Skills Themselves

Any skill that requires intelligent analysis (reviewing work, handling corrections,
preparing responses, assessing task progress) cannot use checklists or numbered steps to
force that analysis.
Forcing questions with “A: [answer explicitly]” slots are boxes.
Adding them increases checked boxes, not intelligence.

All behavioral skills in this system use **synthesis gates** instead: a single statement
the model must produce that demonstrates understanding.
A synthesis gate cannot be filled mechanically — either you can produce the statement or
you can’t. There is no template.

This skill previously had Q1-Q4 forcing questions.
They were removed because they could be filled with plausible content that looked like
analysis without requiring it — the exact failure mode this skill describes.

## The Core Principle

Structure should force thinking by making shortcuts impossible, not by providing
compliance paths.

If you find yourself writing structural requirements after shallow work was detected,
STOP. You are likely making the problem worse.

Ask: “Does this requirement force synthesis that cannot be faked, or does it give the
next agent a template to fill?”

## Recognizing Structurally Wrong Code

Some code is obviously wrong from its structure alone, without needing data or
execution. When an approach destroys the abstraction before applying a search method, it
cannot produce correct results on any input.

### The Canonical Example: Regex-on-HTML

A PowerShell script in a GitHub issue (`opencode#18648`) scrapes usage data from a web
dashboard. To extract a Zen balance, it tries three regex patterns in sequence against
raw HTML:

```
'Current balance.*?(\d+\.?\d*)'       # literal English text in raw HTML
'balance[^>]*>.*?(\d+\.?\d*)'        # "balance" near a tag boundary
'\$(\d+\.?\d*)'                       # any dollar amount, anywhere on the page
```

The third pattern matches **every page served by a modern webapp** — pricing tier
labels, inline scripts with `$` variable names, JSON blobs, bundle hashes, transaction
history. It’s structurally guaranteed to produce a value; it’s also structurally
guaranteed that the value has no relationship to the intended data.

The idiocy is not “regex is the wrong tool for HTML.” The idiocy is **flattening a
semantic tree into an unstructured byte stream before searching it** — destroying the
abstraction that exists precisely to make the data machine-findable.
The correct approach was obvious from the page’s structure:
`document.querySelector('[data-slot="zen-balance"]').textContent` or
`soup.find(attrs={"data-slot": "zen-balance"}).get_text()`. The DOM already identified
the target element.
The script demolished that structure and then tried to reconstruct it
with byte patterns.

A corollary: the third fallback pattern makes the first two pure decoration.
The script always returns some random `$` amount from the page.
No amount of testing against specific pages, adding more regex patterns, or stripping
HTML comments can fix this — the approach is wrong at the abstraction level.
Capabilities-limited agents who cannot introspect their own strategies tend to see “code
that does something” and accept it as “code that does the right thing.”
Structurally wrong code requires *no empirical verification* to disqualify.

### Synthesis Gate

Before evaluating whether code works, ask:

**“Is this approach structurally capable of producing a correct result, regardless of
the specific inputs?”**

If the answer is no (as with regex-on-HTML when semantic selectors exist), stop.
No testing, no data inspection, no further investigation is needed.
The code is wrong and cannot be patched into correctness at the same abstraction level.

### Detecting Structural Wrongness

Signs that an approach destroys the abstraction before operating:

- **Serialization before search**: Converting a tree to text, a typed object to JSON, or
  structured data to bytes before searching or matching

- **Fallback-to-anything**: A final fallback pattern that matches universally (any `$`,
  any number, any string) — this guarantees the first specific patterns will never be
  the ones that fire

- **Literal-text-in-markup**: Assuming English sentences appear verbatim in HTML or JSON
  where tags, attributes, and encoding interleave with the visible text

- **Abstraction-fighting**: Stripping parts of the format (HTML comments, escaping) to
  make the flat-text search work, rather than using a parser that ignores those parts
  automatically

## Cross-References

- **jerry-behaviour** → Load alongside when reviewing agent output that has the surface
  appearance of correctness.
  A Jerry reviewer cannot recognize structurally wrong code because it matches format
  expectations (it runs, it produces output, it tokenizes effort).
  Also catalogs Checklist Theater and Paraphrase-as-Review patterns.

- [[llm-failure-modes/SKILL|llm-failure-modes]] → Load alongside when investigating why an agent cannot
  recognize that an approach is structurally wrong.
  The inability to recognize structural wrongness without empirical verification is an
  epistemic failure mode distinct from “didn’t test enough.”
  Also catalogs compliance-shaped output and reward hacking.

- [[reviewing-subagent-work/SKILL|reviewing-subagent-work]] → Load alongside when conducting a Synthesis Gate review.
  The Synthesis Gate extends this skill’s structural-scrutiny approach to subagent
  output: before inspecting specific implementations, check whether the approach
  survives structural scrutiny.

- [[prompt-engineering/SKILL|prompt-engineering]] → Load alongside when writing instructions that must prevent
  shallow work proactively.
  Constraint-based instruction forces thinking rather than pattern completion.

- **[[policy-index/SKILL|policy-index]] → Bridge-Burning Policies** — The [[policy-index/SKILL#policy-registry|Bridge-Burning Policies]] are the ultimate expression of making bad states impossible rather than using checklists or procedural gates. Refer to them as hard boundaries.

- **[[anti-slop/SKILL|anti-slop]] → deepening** → "Shallow work" in this skill's sense maps directly onto
  "shallow modules" in the deepening vocabulary (`anti-slop/references/deepening-vocabulary.md`).
  A shallow module is one whose interface is nearly as complex as its implementation — it
  provides no leverage and no locality. The deletion test from deepening is a concrete
  diagnostic: if deleting the module makes complexity vanish, it was a pass-through (shallow
  work disguised as a module). If complexity reappears across N callers, it was earning its
  keep (deep work). When this skill identifies structurally wrong code or template-filling,
  the deepening reference (`anti-slop/references/deepening.md`) names what should replace it:
  a deep module with concentrated leverage at its interface.
