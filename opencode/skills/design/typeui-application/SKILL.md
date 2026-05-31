---
name: typeui-application
description: "Use when building application dashboards, developer tools, or admin panels — purple-themed, top-bar nav, card-based layouts, glass-like panels. Load alongside `design` skill for process and verification."
---
# TypeUI Application Design

This subskill points to the **Application** design system from the TypeUI registry — a
Vercel/GitHub-inspired dashboard aesthetic with a purple primary, top-bar-only
navigation, card-based layouts, and glass-like panel surfaces.

**Do not treat this file as the design system itself.** The canonical source lives in
the TypeUI registry.
This file tells you how to fetch, study, and apply it as a design seed.

## How to Fetch

```bash
npx typeui.sh pull application
```

This downloads the full design system as `SKILL.md` to `.agents/skills/design-system/`
(or the provider-specific path you select interactively).

## How to Use This Subskill

1. **Load the parent `design` skill** for process, scoping, and verification.

2. **Fetch the Application system** with `npx typeui.sh pull application`.

3. **Read it as a design seed, not a template** — study its token choices,
   component-state definitions, spacing rhythm, and accessibility rules to understand
   *why* the system feels cohesive.

4. **Extract principles** you can apply to your own design: the purple-on-white contrast
   strategy, the glass-panel card treatment, the choice of Inter as a single typeface
   for clarity, the top-bar-only navigation decision.

5. **Seed greenfield work** by starting from these tokens and adapting: change the
   primary color, adjust the spacing scale, swap the typeface — but keep the structural
   decisions (no sidebar, card-based content, glass panels) that make the system work.

6. **Verify** the final artifact using the `design` skill’s verification checklist.

## What This System Teaches

Study this system for:

- **Single-typeface discipline** — using Inter everywhere (body + display) creates a
  unified texture. No mixing fonts for variety’s sake.

- **Glass-panel cards** — translucent surfaces with soft shadows create depth without
  cluttering the visual field.
  Note the shadow values and opacity choices.

- **Top-bar-only navigation** — the decision to skip sidebars forces content
  prioritization. Study how the layout adapts without a persistent nav column.

- **Purple accent strategy** — a single strong accent color (purple) on a neutral canvas
  creates brand recognition without color pollution.
  Notice what stays gray.

- **Developer-first hierarchy** — dense data displays, clear status indicators,
  monospace for code. The system is opinionated about its audience.

## Related Subskills

| Subskill | Registry command | Best for |
| --- | --- | --- |
| `typeui-application` (this) | `npx typeui.sh pull application` | Application dashboards, dev tools, admin panels |
| `typeui-neumorphism` | `npx typeui.sh pull neumorphism` | Dashboards, creative tools, indie products with tactile aesthetics |
| `typeui-ant` | `npx typeui.sh pull ant` | Enterprise apps, CRUD interfaces, data-dense productivity tools |

## Policy

- Always fetch fresh with `npx typeui.sh pull <name>` rather than caching the content
  locally — the registry may update.

- Never paste the full fetched skill into generated code as a preamble.
  Study it first, then design from understanding.

- When combining with `popular-web-designs` or `design-md`, prioritize the parent
  `design` skill’s process for scoping and verification — the TypeUI seed is the visual
  starting point, not the design methodology.
