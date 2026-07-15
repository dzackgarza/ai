---
name: typeui-neumorphism
description: "Use when designing dashboards, creative tools, indie products, or any interface where a tactile, shadow-based aesthetic reinforces the brand. Load alongside [[design/SKILL|design]] skill for process and verification."
---
# TypeUI Neumorphism Design

This subskill points to the **Neumorphism** design system from the TypeUI registry — a
soft-shadow, extruded aesthetic where elements appear to push out of or press into the
background surface, paired with Space Mono typography and deep teal accents.

**Do not treat this file as the design system itself.** The canonical source lives in
the TypeUI registry.
This file tells you how to fetch, study, and apply it as a design seed.

## How to Fetch

```bash
npx typeui.sh pull neumorphism
```

This downloads the full design system as `SKILL.md` to `.agents/skills/design-system/`
(or the provider-specific path you select interactively).

## How to Use This Subskill

1. **Load the parent [[design/SKILL|design]] skill** for process, scoping, and verification.

2. **Fetch the Neumorphism system** with `npx typeui.sh pull neumorphism`.

3. **Read it as a design seed, not a template** — study its shadow system,
   monospace-first typography choice, compact density mode, and the “one material shaped
   by light” philosophy.

4. **Extract principles**: the paired shadow system (light/dark shadow on every
   element), the press-state inversion model, the compact spacing that respects shadow
   boundaries, the bold choice of a monospace font as the primary typeface.

5. **Seed greenfield work** by starting from these concepts and adapting: change the
   surface color, swap Space Mono for another distinctive font, adjust shadow intensity
   — but preserve the core insight (depth through shadows alone, not borders or color
   differentiation).

6. **Verify** the final artifact using the [[design/SKILL|design]] skill’s verification checklist,
   paying special attention to accessibility since neumorphism’s reliance on shadow
   contrast can create boundary-detection issues.

## What This System Teaches

Study this system for:

- **Shadow as design language** — where most systems use borders, fills, and elevation
  tokens, neumorphism uses paired light/dark shadows to define hierarchy.
  Study the shadow offset, blur radius, and opacity values.

- **One-material constraint** — the surface and elements share the same background
  color. Depth is purely shadow-driven.
  This constraint forces creative solutions to the layout problems borders normally
  solve.

- **Monospace personality** — Space Mono as the primary typeface is an opinionated
  choice that defines the brand as much as the shadows do.
  Study how the fixed-width character grid interacts with the organic shadow shapes.

- **Compact density mode** — tight spacing balanced against shadow expansion zones.
  Study the gap calculations that prevent adjacent shadows from fusing.

- **Extruded/inset state model** — the press-state inversion (raised elements go inset
  on interaction) creates a physical button-press metaphor.
  Study the shadow transition values.

## Related Subskills

| Subskill | Registry command | Best for |
| --- | --- | --- |
| [[design/typeui-application/SKILL|typeui-application]] | `npx typeui.sh pull application` | Application dashboards, dev tools, admin panels |
| `typeui-neumorphism` (this) | `npx typeui.sh pull neumorphism` | Dashboards, creative tools, indie products with tactile aesthetics |
| [[design/typeui-ant/SKILL|typeui-ant]] | `npx typeui.sh pull ant` | Enterprise apps, CRUD interfaces, data-dense productivity tools |

## Policy

- Always fetch fresh with `npx typeui.sh pull <name>` rather than caching the content
  locally — the registry may update.

- Never paste the full fetched skill into generated code as a preamble.
  Study it first, then design from understanding.

- Neumorphism has specific accessibility challenges (shadow-dependent element
  boundaries). Always verify WCAG AA contrast for focus indicators and fallback border
  treatments for high-contrast mode.

- When combining with [[popular-web-designs/SKILL|popular-web-designs]] or [[design-md/SKILL|design-md]], prioritize the parent
  [[design/SKILL|design]] skill’s process for scoping and verification — the TypeUI seed is the visual
  starting point, not the design methodology.
