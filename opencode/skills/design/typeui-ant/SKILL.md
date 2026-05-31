---
name: typeui-ant
description: "Use when building enterprise applications, CRUD interfaces, productivity tools, or data-dense dashboards — structured, clarity-first, blue primary, Plus Jakarta Sans typography. Load alongside `design` skill for process and verification."
---
# TypeUI Ant Design

This subskill points to the **Ant** design system from the TypeUI registry — an
enterprise-focused aesthetic built for data-dense web applications, with a clean blue
primary, Plus Jakarta Sans typography, and structured, predictable component patterns.

**Do not treat this file as the design system itself.** The canonical source lives in
the TypeUI registry.
This file tells you how to fetch, study, and apply it as a design seed.

## How to Fetch

```bash
npx typeui.sh pull ant
```

This downloads the full design system as `SKILL.md` to `.agents/skills/design-system/`
(or the provider-specific path you select interactively).

## How to Use This Subskill

1. **Load the parent `design` skill** for process, scoping, and verification.

2. **Fetch the Ant system** with `npx typeui.sh pull ant`.

3. **Read it as a design seed, not a template** — study its component-state
   completeness, data-dense layout strategy, Plus Jakarta Sans scaling, and anti-pattern
   enforcement.

4. **Extract principles**: the six-element state matrix (default through error), the
   single-family typography strategy at compact sizes, the spacing rhythm for dense CRUD
   layouts, the explicit anti-pattern list that prevents common enterprise-UI mistakes.

5. **Seed greenfield work** by starting from these tokens and adapting: change the
   primary blue to your brand color, adjust the spacing scale for your content density,
   swap Plus Jakarta Sans for your preferred typeface — but preserve the structural
   decisions (complete state definitions for every component, explicit anti-patterns,
   data-density optimizations) that prevent enterprise UI degradation.

6. **Verify** the final artifact using the `design` skill’s verification checklist, with
   extra attention to the six anti-patterns defined in the Ant system — they catch the
   most common enterprise UI failures.

## What This System Teaches

Study this system for:

- **State completeness as a design principle** — every component defines all six states
  (default, hover, focus-visible, active, disabled, loading, error), plus empty-state
  first-class status. Study how the state matrix drives component API design.

- **Enterprise restraint** — blue primary, neutral everything else.
  Study what *doesn’t* have color (most things) and why that restraint builds trust in
  data-heavy interfaces.

- **Plus Jakarta Sans at small sizes** — geometric sans-serif optimized for legibility
  at 12-14px. Study the x-height and letter spacing choices that make dense tables
  readable.

- **Explicit anti-patterns** — the system lists what NOT to do.
  Study how “no inconsistent spacing rhythm”, “no mixed visual metaphors”, and “no
  inaccessible hit areas” prevent design drift across a large component surface area.

- **Data-dense layout patterns** — tables, data grids, stat blocks, charts on structured
  grids. Study the spacing rhythm that keeps dense information scannable without feeling
  cramped.

- **Enterprise accessibility** — WCAG 2.2 AA enforced via testable rules, not
  guidelines. Study how each accessibility requirement has a corresponding component
  spec.

## Related Subskills

| Subskill | Registry command | Best for |
| --- | --- | --- |
| `typeui-application` | `npx typeui.sh pull application` | Application dashboards, dev tools, admin panels |
| `typeui-neumorphism` | `npx typeui.sh pull neumorphism` | Dashboards, creative tools, indie products with tactile aesthetics |
| `typeui-ant` (this) | `npx typeui.sh pull ant` | Enterprise apps, CRUD interfaces, data-dense productivity tools |

## Policy

- Always fetch fresh with `npx typeui.sh pull <name>` rather than caching the content
  locally — the registry may update.

- Never paste the full fetched skill into generated code as a preamble.
  Study it first, then design from understanding.

- Enterprise CRUD interfaces are especially prone to accessibility degradation.
  Verify every state defined in the Ant system against WCAG AA after generation.

- When combining with `popular-web-designs` or `design-md`, prioritize the parent
  `design` skill’s process for scoping and verification — the TypeUI seed is the visual
  starting point, not the design methodology.
