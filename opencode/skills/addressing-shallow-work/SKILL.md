---
name: addressing-shallow-work
description: Use when agent work is shallow, superficial, or box-checking. Covers the structure-intelligence inversion and how to force synthesis over compliance.
---

# Addressing Shallow Work

When you observe or are told that agent work was shallow, DO NOT respond by adding more checklists, inventories, or procedural gates.

## The Structure-Intelligence Inversion

More structure ≠ better work. The relationship is often inverted:

- **More checklists** = more opportunities to game via compliance
- **More inventories** = more boxes to check without understanding
- **More procedural gates** = more ways to produce solution-shaped filler

### Why This Happens

Adding requirements like "every X must have a Y" or "require inventory where each row has..." creates **measurable targets**. Measurable targets create optimization surfaces that bypass the actual cognitive work. The agent will produce rows with plausible-looking entries — optimizing for the measurable target (easy) — rather than genuine analysis (hard). The structure provides a template to fill, and filling templates is exactly what models are best at and most likely to default to.

This was observed directly: a model responded to shallow mathematical analysis by proposing "require semantic inventory where every mathematical unit has a row, every row has target research, and every row has incorporation instructions." This would have given the next agent a spreadsheet to populate mechanically — the exact opposite of forcing the holistic mathematical reading that was missing.

### What Was Actually Needed

The fix that eventually worked was simpler and sharper:

> "Read the whole source until you can explain what mathematical understanding changed. Then annotate only from that synthesized understanding. If the agent cannot produce the holistic synthesis, it should block — not compensate with inventories, hashes, or route comments."

The annotations are an *expression* of the analysis, not the analysis itself. If the agent can't produce the synthesis, no amount of structural scaffolding will create it.

## Synthesis Gate

Before proposing any fix for shallow work, produce this statement:

**"The shallow work skipped _____ (a cognitive operation), and the fix must require _____ as output that cannot be produced without doing that operation."**

If your proposed fix is structural (add rows, add gates, add inventories), it will be gamed the same way the original work was gamed. A fix for shallow work must require the agent to produce understanding — not fill a different template.

If your fix contains "require", "inventory", "every X has Y", or "verification gates" — you are creating new boxes. Start over.

## This Principle Applies to Skills Themselves

Any skill that requires intelligent analysis (reviewing work, handling corrections, preparing responses, assessing task progress) cannot use checklists or numbered steps to force that analysis. Forcing questions with "A: [answer explicitly]" slots are boxes. Adding them increases checked boxes, not intelligence.

All behavioral skills in this system use **synthesis gates** instead: a single statement the model must produce that demonstrates understanding. A synthesis gate cannot be filled mechanically — either you can produce the statement or you can't. There is no template.

This skill previously had Q1-Q4 forcing questions. They were removed because they could be filled with plausible content that looked like analysis without requiring it — the exact failure mode this skill describes.

## The Core Principle

Structure should force thinking by making shortcuts impossible, not by providing compliance paths.

If you find yourself writing structural requirements after shallow work was detected, STOP. You are likely making the problem worse.

Ask: "Does this requirement force synthesis that cannot be faked, or does it give the next agent a template to fill?"

## Cross-References

- **jerry-behaviour**: Checklist Theater and Paraphrase-as-Review patterns
- **llm-failure-modes**: Compliance-shaped output and reward hacking
- **prompt-engineering**: Constraint-based instruction that forces thinking
