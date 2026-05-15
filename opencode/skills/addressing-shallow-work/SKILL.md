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

## Before Proposing Structural Fixes

Answer these questions EXPLICITLY before proposing any fix:

**Q1: "Why would adding checklists/structure make shallow work WORSE?"**

A: [answer explicitly - explain the gaming mechanism]

**Q2: "What mental operation did the shallow work skip - synthesis, judgment, or checking facts?"**

A: [answer explicitly - must be cognitive, not procedural]

**Q3: "Can a checklist force that mental operation, or can it be gamed?"**

Decision:
- If operation is "synthesis" → NO, checklists can't force it
- If operation is "holistic understanding" → NO, checklists can't force it
- If operation is "judgment" → NO, checklists can't force it
- If operation is "check specific fact" → YES, checklist might work

A: [answer explicitly]

**Q4: "If NO to Q3: What requirement would make shortcuts IMPOSSIBLE?"**

A: [must require synthesis as OUTPUT, not boxes as INPUT]

Only after answering all four questions: propose your fix.

If your proposed fix contains: "require", "inventory", "every X has Y", "verification gates" → STOP. You're creating boxes to check. Start over.

## Examples of WRONG Fixes

- "Require inventory where every X has a Y" ← box-checking
- "Every row must have research" ← can fake
- "Add verification gates" ← can game
- "Create structured audit trail" ← compliance theater

## Examples of RIGHT Fixes

- "Explain what mathematical understanding changed" ← requires synthesis
- "Block if you cannot produce holistic summary" ← can't shortcut
- "Compare final state to initial and justify every difference" ← forces thinking
- "Produce a narrative thread that assembles ALL insights" ← can't fake

## The Core Principle

Structure should force thinking by making shortcuts impossible, not by providing compliance paths.

If you find yourself writing structural requirements after shallow work was detected, STOP. You are likely making the problem worse.

Ask: "Does this requirement force synthesis that cannot be faked, or does it give the next agent a template to fill?"

## Cross-References

- **jerry-behaviour**: Checklist Theater and Paraphrase-as-Review patterns
- **llm-failure-modes**: Compliance-shaped output and reward hacking
- **prompt-engineering**: Constraint-based instruction that forces thinking
