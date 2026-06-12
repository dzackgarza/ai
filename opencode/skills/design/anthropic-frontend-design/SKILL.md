---
name: anthropic-frontend-design
description: "Use when the user asks for a visually striking, memorable frontend — landing pages, components, dashboards, posters, or any web UI where generic aesthetics are unacceptable. Load alongside parent `design` skill for process and verification."
---
# Anthropic Frontend Design

This subskill extracts the creative direction methodology from Anthropic’s
`frontend-design` skill
(https://github.com/anthropics/skills/tree/main/skills/frontend-design).

**The canonical source is the Anthropic repo.** This file does not replace it — it
extracts the behavioral rules and cross-references them with the `design` skill’s
process.

The Anthropic skill fills a gap that the parent `design` skill does not fully cover:
**creative direction and aesthetic differentiation** — how to commit to a bold visual
identity, pick the right tone, and make an interface memorable.
The `design` skill handles process, verification, and taste; this one handles creative
ambition.

## How to Use This Subskill

1. **Load the parent `design` skill** for process, scoping, and verification.

2. **Load this subskill** when the user wants a striking, distinctive frontend rather
   than a clean, restrained one.

3. **Optionally fetch the original** from the Anthropic repo for the full context.

4. Apply the creative direction rules below, then use the `design` skill for typography,
   color, layout, responsive, and verification.

## Creative Direction Methodology

Before coding, commit to a clear aesthetic direction:

### 1. Context Scan

- **Purpose**: What problem does this interface solve?
  Who uses it?

- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic,
  organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw,
  art deco/geometric, soft/pastel, industrial/utilitarian.
  Do not pick a middle-ground or generic tone.

- **Constraints**: Framework, performance targets, accessibility requirements.

- **Differentiation**: What is the ONE thing someone will remember about this interface?
  Design around that thing.

### 2. Commit to the Direction

- Bold maximalism and refined minimalism both work — the key is **intentionality**, not
  intensity.

- Every design decision must trace back to the chosen tone.
  If a choice weakens the identity, remove it.

- Do not hedge. Do not add “safe” elements that dilute the aesthetic.

### 3. Match Complexity to Aesthetic

- **Maximalist designs** need elaborate code: extensive animations, layered backgrounds,
  staggered reveals, scroll-triggered effects, custom cursors, grain overlays.

- **Minimalist/refined designs** need restraint: precision spacing, perfect typography,
  subtle transitions, meticulous alignment.

- Elegance comes from executing the chosen vision well, not from the vision itself.

## Anti-Generic Rules

These rules override the parent `design` skill’s defaults when this subskill is loaded.

### Typography

- **Avoid**: Inter, Roboto, Arial, system-ui stacks, Space Grotesk, Poppins — anything
  that ships by default with every AI generator.

- **Prefer**: Distinctive, characterful fonts that match the tone.
  Pair a strong display font with a refined body font.
  Use variable weights to fine-tune hierarchy.

- Google Fonts, CDN fonts, and `@font-face` are all valid.
  Do not let font loading time scare you off a good choice — the output is an artifact,
  not a production site.

### Color

- **Avoid**: Purple-on-white gradients, blue-on-gray enterprise palettes,
  evenly-distributed multi-color schemes.

- **Prefer**: A dominant color with sharp accents.
  Uneven color distribution reads as intentional.
  Black-and-white with a single accent is stronger than four colors in equal measure.

### Layout

- **Avoid**: Centered everything, equal-width columns, predictable card grids.

- **Prefer**: Asymmetry, overlap, diagonal flow, grid-breaking elements, generous
  negative space or controlled density.
  Let the layout reinforce the tone.

### Visual Details

- Add atmosphere through: gradient meshes, noise textures, geometric patterns, layered
  transparencies, dramatic shadows, decorative borders, grain overlays.

- Do not default to solid color backgrounds.
  The background is part of the design.

- Motion must serve the aesthetic: one well-orchestrated page-load stagger creates more
  impact than scattered micro-interactions.

### Diagnostic Signs of LLM-Generated Design

The following patterns are the most reliable visual cues that a design was
produced by an LLM rather than a designer.
If you see these in an artifact, they indicate the model defaulted to averaged
training-set patterns instead of making intentional choices — fix them before
showing the artifact to anyone:

- **Thin colored borders on cards and sections** — pastel 1px borders that an
  LLM adds because it cannot decide between fill, shadow, or no container.
  Real designers pick one structural treatment per component.

- **Gratuitous gradients** — light-blue-to-white, purple-to-pink, or any gradient
  that serves no brand or atmospheric purpose.
  LLMs default to gradients because they are the "safe decorative" option; a
  deliberate designer treats gradients as a specific identity choice.

- **Glow effects** — colored box-shadows, text-shadows with visible hue, or
  radial glows that substitute for real depth.
  These are the LLM equivalent of comic-book emphasis — they signal "I don't know
  how to make this look important without lighting it on fire."

- **Too many font sizes** — five or more distinct sizes where a disciplined
  scale would use three or four.
  The LLM sizes each text element independently rather than treating type as a
  system.

- **Body text below 14px** — especially on non-dashboard surfaces (landing pages,
  marketing sections, editorial layouts).
  The model inherits tiny sizes from enterprise dashboards and applies them
  indiscriminately.

- **Inconsistent vertical rhythm** — uneven padding between unrelated elements
  that should share spacing, card content not optically centered, buttons with
  asymmetric internal padding.
  Vertical inconsistency is the most sensitive diagnostic: it is nearly universal
  in LLM output and almost never appears in human-designed work at the same
  frequency.

These cues are not just "things to avoid" — they are the specific patterns that
make LLM-generated design immediately recognizable.
Eliminating them is the minimum bar for an artifact to be taken seriously.

## Policy

- This subskill is for **artifacts that need to be memorable and distinctive**. For
  clean, restrained, production-style interfaces, use only the parent `design` skill —
  this subskill’s rules would push too hard.

- When in doubt about whether to load this subskill, ask: “Does the user want something
  striking and memorable, or clean and functional?”

- Always use the parent `design` skill’s verification checklist to validate the output —
  creative ambition does not excuse broken accessibility or responsiveness.

## Related Subskills

| Subskill | Source | Best for |
| --- | --- | --- |
| `anthropic-frontend-design` (this) | Anthropic skills repo | Striking, memorable frontends — landing pages, portfolios, creative tools |
| `typeui-application` | TypeUI registry | Polished app dashboards with glass panels |
| `typeui-neumorphism` | TypeUI registry | Tactile, shadow-based interfaces |
| `typeui-ant` | TypeUI registry | Enterprise CRUD, data-dense productivity tools |
