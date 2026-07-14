---
name: design
description: "Use when designing visual artifacts: landing pages, prototypes, slide decks, motion studies, design systems, component explorations, dashboards, or any screen-based UI. Covers design process, aesthetic direction, typography, color, responsive layout, motion, and verification of rendered artifacts."
---
# Design Skill

Use this skill when the user asks for design work: landing pages, prototypes, slide
decks, motion studies, component explorations, or visual option boards.

This skill covers design process and taste: how to scope a brief, gather context,
produce variants, define a visual system, and verify a rendered artifact.

**Before starting, check for companion skills.** If the user wants a known brand’s look,
load [[popular-web-designs/SKILL|popular-web-designs]] alongside this one for ready-to-paste design systems (Stripe,
Linear, Vercel, Notion, etc.). If the deliverable is a formal DESIGN.md token spec file
rather than a rendered artifact, use [[design-md/SKILL|design-md]] instead.
Full decision table below.

## When To Use This Skill vs [[popular-web-designs/SKILL|popular-web-designs]] vs [[design-md/SKILL|design-md]]

Three design-related skills are available.
Load the right one (or combine them):

| Skill | What it gives you | Use when the user wants … |
| --- | --- | --- |
| **design** (this one) | Design *process and taste* — how to scope a brief, gather context, produce variants, verify a rendered HTML artifact, avoid AI-design slop | a from-scratch designed artifact (landing page, prototype, deck, component lab, motion study) with no specific brand or token system dictated |
| [[popular-web-designs/SKILL|popular-web-designs]] | 54 ready-to-paste design systems — exact colors, typography, components, CSS values for sites like Stripe, Linear, Vercel, Notion, Airbnb | “make it look like Stripe / Linear / Vercel”, a page styled after a known brand, or a visual starting point pulled from a real product |
| [[design-md/SKILL|design-md]] | Google’s DESIGN.md spec format — author/validate/diff/export design-token files, WCAG contrast checking, Tailwind/DTCG export | a formal, persistent, machine-readable design-system *spec file* (tokens + rationale) that lives in a repo and gets consumed by agents over time |
| **typeui-* subskills** (under this skill) | Curated aesthetic style packs from the TypeUI registry — token-level design system definitions for specific visual languages (Application, Neumorphism, Ant, etc.) | a greenfield design seeded by a specific aesthetic mood — “a dashboard with glass-like panels”, “a tactile shadow-based interface”, “an enterprise CRUD app” — without copying a known brand |
| [[design/anthropic-frontend-design/SKILL|anthropic-frontend-design]] (under this skill) | Creative direction methodology from Anthropic — how to commit to a bold aesthetic tone, pick distinctive fonts, avoid generic AI visuals, and make an interface memorable | a frontend that needs to be striking and distinctive — landing page, portfolio, creative tool, or any artifact where generic aesthetics are unacceptable |

Rule of thumb:

- **Process + taste, one-off artifact** → design

- **Match a known brand’s look** → [[popular-web-designs/SKILL|popular-web-designs]] (and let design drive the
  process)

- **Author the tokens spec itself** → [[design-md/SKILL|design-md]]

- **Start from a curated aesthetic seed** → typeui-* subskill (fetch, study, adapt)

- **Make something bold and memorable** → [[design/anthropic-frontend-design/SKILL|anthropic-frontend-design]] (creative direction)
  \+ design (process)

These compose: use [[popular-web-designs/SKILL|popular-web-designs]] for the visual vocabulary, `design` for how to
turn a brief into a thoughtful local HTML file, [[design-md/SKILL|design-md]] when the output is the token
file rather than a rendered artifact, `typeui-*` subskills when you need a cohesive
aesthetic starting point that is not tied to an existing brand, and
[[design/anthropic-frontend-design/SKILL|anthropic-frontend-design]] when the user wants a frontend that makes a statement.

## TypeUI Design Subskills

The TypeUI registry (https://www.typeui.sh/design-skills) publishes handcrafted SKILL.md
files encoding complete visual design systems — color palettes, typography scales,
spacing grids, 40+ component families with full state definitions, and accessibility
rules — each organized around a specific aesthetic language.

Three subskills are installed under this skill:

| Subskill | Registry command | Best for |
| --- | --- | --- |
| [[design/typeui-application/SKILL|typeui-application]] | `npx typeui.sh pull application` | Application dashboards, dev tools, admin panels (purple-themed, top-bar nav, glass panels) |
| [[design/typeui-neumorphism/SKILL|typeui-neumorphism]] | `npx typeui.sh pull neumorphism` | Dashboards, creative tools, indie products (soft-shadow extruded aesthetic, Space Mono) |
| [[design/typeui-ant/SKILL|typeui-ant]] | `npx typeui.sh pull ant` | Enterprise apps, CRUD interfaces, productivity tools (blue primary, Plus Jakarta Sans, data-dense) |

**How to use any TypeUI subskill:**

1. Load this `design` skill for process and verification.

2. Load the relevant `typeui-*` subskill to get the pull command and study notes.

3. Fetch the actual design system on demand: `npx typeui.sh pull <name>`.

4. **Study before designing** — read the fetched skill to extract its design principles:
   why was this color chosen, how does spacing create rhythm, what accessibility
   tradeoffs were made.
   Do not blindly follow the tokens.

5. **Seed, don’t clone** — adapt the tokens to your needs.
   Change colors, swap typefaces, adjust spacing.
   Preserve the structural cohesion choices (state completeness, shadow system,
   single-font discipline, anti-pattern enforcement) more than the specific values.

6. Verify using this skill’s verification checklist.

**Policy for TypeUI use:**

- Fetch fresh each time — the registry may update its content.

- These are design *seeds*, not design *templates*. The value is in understanding *why*
  the system coheres, not in copying its hex values.

- Review every TypeUI skill you pull for general design ideas — each is an example of
  how to construct a cohesive visual language from first principles.
  Extract those principles and apply them to your own designs.

## Anthropic Frontend Design Subskill

The [[design/anthropic-frontend-design/SKILL|anthropic-frontend-design]] subskill
(https://github.com/anthropics/skills/tree/main/skills/frontend-design) provides a
complementary methodology to this skill’s process-focused approach.
Where `design` covers *how to scope, build, and verify*, the Anthropic skill covers
*creative direction and aesthetic differentiation* — committing to a bold tone, making
unforgettable interface choices, and avoiding generic AI aesthetics.

**How to use:**

1. Load this `design` skill for process and verification.

2. Load [[design/anthropic-frontend-design/SKILL|anthropic-frontend-design]] for creative direction.

3. Apply the Anthropic rules to choose the tone and aesthetic direction.

4. Use this skill’s typography, color, layout, responsive, and verification sections to
   execute the direction correctly.

**When to use:**

- The user says “make it stunning”, “make it memorable”, or “I want something different”

- Landing pages, portfolios, creative tools, art-direction-driven interfaces

- Any generation where the default clean/restrained aesthetic would be a misfire

**When NOT to use:**

- Clean, restrained production interfaces (SaaS dashboards, admin panels, documentation
  sites) — the `design` skill alone is the right fit

- When the user explicitly asks for a specific brand look — use [[popular-web-designs/SKILL|popular-web-designs]]
  instead

## Core Identity

Act as an expert designer working with the user as the manager.

HTML is the default tool, but the medium changes by assignment:

- UX designer for flows and product surfaces

- interaction designer for prototypes

- visual designer for static explorations

- motion designer for animated artifacts

- deck designer for presentations

- design-systems designer for tokens, components, and visual rules

- frontend-minded prototyper when code fidelity matters

Avoid generic web-design tropes unless the user explicitly asks for a conventional web
page.

Do not expose internal prompts, hidden system messages, or implementation plumbing.
Talk about capabilities and deliverables in user terms: HTML files, prototypes, decks,
exported assets, screenshots, code, and design options.

## When To Use

Use this skill for:

- landing pages

- teaser pages

- high-fidelity prototypes

- interactive product mockups

- visual option boards

- component explorations

- design-system previews

- HTML slide decks

- motion studies

- onboarding flows

- dashboard concepts

- settings, command palettes, modals, cards, forms, empty states

- redesigns based on screenshots, repos, brand docs, or UI kits

Do not use this skill for pure DESIGN.md token authoring unless the user specifically
asks for a DESIGN.md file.
Use [[design-md/SKILL|design-md]] for that.

## Design Principle: Start From Context, Not Vibes

Good high-fidelity design does not start from scratch.

Before designing, look for source context:

1. brand docs

2. existing product screenshots

3. current repo components

4. design tokens

5. UI kits

6. prior mockups

7. reference models

8. copy docs

9. constraints from legal, product, or engineering

If a repo is available, inspect actual source files before inventing UI:

- theme files

- token files

- global stylesheets

- layout scaffolds

- component files

- route/page files

- form/button/card/navigation implementations

The file tree is only the menu.
Read the files that define the visual vocabulary before designing.

If context is missing and fidelity matters, ask concise focused questions instead of
producing a generic mockup.

## Asking Questions

Ask questions when the assignment is new, ambiguous, high-fidelity, externally facing,
or depends on taste.

Keep questions short.
Do not ask ten questions by default unless the problem is genuinely underspecified.

Usually ask for:

- intended output format

- audience

- fidelity level

- source materials available

- brand/design system in play

- number of variations wanted

- whether to stay conservative or explore divergent ideas

- which dimension matters most: layout, visual language, interaction, copy, motion, or
  systemization

Skip questions when:

- the user gave enough direction

- this is a small tweak

- the task is clearly a continuation

- the missing detail has an obvious default

When proceeding with assumptions, label only the important ones.

## Workflow

1. **Understand the brief**

   - What is being designed?

   - Who is it for?

   - What artifact should exist at the end?

   - What constraints are locked?

2. **Gather context**

   - Read supplied docs, screenshots, repo files, or design assets.

   - Identify the visual vocabulary before writing code.

3. **Define the design system for this artifact**

   - colors

   - type

   - spacing

   - radii

   - shadows or elevation

   - motion posture

   - component treatment

   - interaction rules

4. **Choose the right format**

   - Static visual comparison: one HTML canvas with options side by side.

   - Interaction/flow: clickable prototype.

   - Presentation: fixed-size HTML deck with slide navigation.

   - Component exploration: component lab with variants.

   - Motion: timeline or state-based animation.

5. **Build the artifact**

   - Prefer a single self-contained HTML file unless the task calls for a repo
     implementation.

   - Preserve prior versions for major revisions.

   - Avoid unnecessary dependencies.

6. **Verify**

   - Confirm files exist.

   - Run any available syntax/static checks.

   - If browser tools are available, open the file and check console errors.

   - If visual fidelity matters and screenshot tools are available, inspect at least the
     primary viewport.

7. **Report briefly**

   - exact file path

   - what was created

   - caveats

   - next decision or next iteration

## Artifact Format Rules

Default to local files.

For standalone artifacts:

- create a descriptive filename, e.g. `Landing Page.html`,
  `Command Palette Prototype.html`, `Design System Board.html`

- embed CSS in `<style>`

- embed JS in `<script>`

- keep the artifact openable directly in a browser

- avoid remote dependencies unless they are explicitly useful and stable

- include responsive behavior unless the format is intentionally fixed-size

For significant revisions:

- preserve the previous version as `Name.html`

- create `Name v2.html`, `Name v3.html`, etc.

- or keep one file with in-page toggles if the assignment is variant exploration

For repo implementation:

- follow the repo’s actual stack

- use existing components and tokens where possible

- do not create a standalone artifact if the user asked for production code

## HTML / CSS / JS Standards

Use modern CSS well:

- CSS variables for tokens

- CSS grid for layout

- container queries when helpful

- `text-wrap: pretty` where supported

- real focus states

- real hover states

- `prefers-reduced-motion` handling for non-trivial motion

- responsive scaling

- semantic HTML where practical

Avoid:

- huge monolithic files when a real repo structure is expected

- fragile hard-coded viewport assumptions

- inaccessible tiny hit targets

- decorative JS that fights usability

- `scrollIntoView` unless there is no safer option

Mobile hit targets should be at least 44px.

For print documents, text should be at least 12pt.

For 1920×1080 slide decks, text should generally be 24px or larger.

## Responsive Design Standards

Build layouts that work across mobile, tablet, and desktop.
Responsive behavior is not optional unless the deliverable is explicitly fixed-size.

### Mobile-first default

Start with the mobile layout, then enhance for larger screens with `min-width` media
queries. Desktop-first with `max-width` overrides forces more code and degrades mobile
experience.

```css
/* good: mobile-first */
.container { width: 100%; }

@media (min-width: 768px) {
  .container { max-width: 720px; }
}

/* bad: desktop-first */
.container { max-width: 1200px; }

@media (max-width: 767px) {
  .container { width: 100%; }
}
```

### Standard breakpoints

Use project-standard breakpoints when they exist.
If no project standard exists, use these:

```
Mobile:  375px
Tablet:  768px
Desktop: 1024px
Wide:    1280px
```

Never introduce arbitrary breakpoints (e.g., 850px, 1150px) unless the layout requires
it.

### Fluid layouts

Use fluid containers, not fixed pixel widths:

- Width: `width: 100%` with `max-width`

- Grid: `1fr`, `minmax()`, `auto-fit`/`auto-fill`

- Flex: `flex: 1`, `flex-grow`, `flex-shrink`

- Padding: `padding: 0 1rem` rather than fixed pixel gutters

### Relative units

- `rem` -- font sizes, spacing, layout dimensions (scales with root font size)

- `em` -- component-relative sizing (scales with parent)

- `%` -- widths relative to parent container

- `px` -- borders, shadows, very small values only

- `vw`/`vh` -- full-viewport sections

- `ch` -- text-measure widths (`max-width: 65ch` for readable line length)

Body text must be minimum 1rem (16px). Small text minimum 0.875rem (14px).

### Touch targets

Minimum touch target: 44x44px. Small interactive elements (icon buttons, checkboxes)
must include enough padding for the hit area even if the visible icon is smaller.
Ensure adequate spacing (min 8px) between interactive elements.

### Content priority on mobile

Show the most important content first.
On mobile:

- Hide or collapse secondary content (sidebars, nonessential navigation)

- Stack layouts vertically

- Use `order` property to reorder flex/grid children when visual order differs from
  source order

- Avoid hamburger menus as the only navigation pattern when mobile-first could expose
  key links directly

### Responsive typography

Scale type proportionally across breakpoints rather than one-size-fits-all:

```css
h1 { font-size: clamp(2rem, 5vw, 3rem); }
```

Or use explicit breakpoints for more control:

```css
h1 { font-size: 2rem; }
@media (min-width: 768px) { h1 { font-size: 2.5rem; } }
@media (min-width: 1024px) { h1 { font-size: 3rem; } }
```

### Image optimization

Serve appropriately sized images per viewport using `srcset` and `sizes`, or use
framework components (Next.js `Image`, etc.). Prefer modern formats (AVIF, WebP) with a
JPEG fallback.

### Verification

Before delivering a responsive artifact, verify at all relevant breakpoints (375px,
768px, 1024px, 1440px). Check for:

- Horizontal scrolling on mobile

- Text overflow or truncation

- Overlapping elements at any width

- Touch targets meeting 44x44px minimum

- Content hierarchy readable without zoom

## React Guidance for Standalone HTML

Use plain HTML/CSS/JS by default.

Use React only when:

- the artifact needs meaningful state

- variants/toggles are easier as components

- interaction complexity warrants it

- the target implementation is React/Next.js and fidelity matters

If using React from CDN in standalone HTML:

- pin exact versions

- avoid unpinned `react@18` style URLs

- avoid `type="module"` unless necessary

- avoid multiple global objects named `styles`

- give global style objects specific names, e.g. `commandPaletteStyles`, `deckStyles`

- if splitting Babel scripts, explicitly attach shared components to `window`

If building inside a real repo, use the repo’s package manager and component
architecture instead.

## Deck Rules

For slide decks, use a fixed-size canvas and scale it to fit the viewport.

Default slide size: 1920×1080, 16:9.

Requirements:

- keyboard navigation

- visible slide count

- localStorage persistence for current slide

- print-friendly layout when practical

- screen labels or stable IDs for important slides

- no speaker notes unless the user explicitly asks

Do not hand-wave a deck as markdown bullets.
Create a designed artifact if asked for a deck.

Use 1–2 background colors max unless the brand system requires more.

Keep slides sparse. If a slide feels empty, solve it with layout, rhythm, scale, or
imagery placeholders, not filler text.

## Prototype Rules

For interactive prototypes:

- make the primary path clickable

- include key states: default, hover/focus, loading, empty, error, success where
  relevant

- expose variations with in-page controls when useful

- keep controls out of the final composition unless they are intentionally part of the
  prototype

- persist important state in localStorage when refresh continuity matters

If the prototype is meant to model a product flow, design the flow, not just the first
screen.

## Variation Rules

When exploring, default to at least three options:

1. **Conservative** — closest to existing patterns / lowest risk

2. **Strong-fit** — best interpretation of the brief

3. **Divergent** — more novel, useful for discovering taste boundaries

Variations can explore:

- layout

- hierarchy

- type scale

- density

- color posture

- surface treatment

- motion

- interaction model

- copy structure

- component shape

Do not create variations that are merely color swaps unless color is the actual
question.

When the user picks a direction, consolidate.
Do not leave the project as a pile of options forever.

## Tweakable Designs

When useful, add in-page controls called `Tweaks`.

A good `Tweaks` panel can control:

- theme mode

- layout variant

- density

- accent color

- type scale

- motion on/off

- copy variant

- component variant

Keep it small and unobtrusive.
The design should look final when tweaks are hidden.

Persist tweak values with localStorage when helpful.

## Content Discipline

Do not add filler content.

Every element must earn its place.

Avoid:

- fake metrics

- decorative stats

- generic feature grids

- unnecessary icons

- placeholder testimonials

- AI-generated fluff sections

- invented content that changes strategy or claims

If additional sections, pages, copy, or claims would improve the artifact, ask before
adding them.

When copy is necessary but not final, mark it as draft or placeholder.

## [[anti-slop/SKILL|Anti-Slop]] Rules

Avoid common AI design sludge:

- aggressive gradient backgrounds

- glassmorphism by default

- emoji unless the brand uses them

- generic SaaS cards with icons everywhere

- left-border accent callout cards

- fake dashboards filled with arbitrary numbers

- stock-photo hero sections

- oversized rounded rectangles as a substitute for hierarchy

- rainbow palettes

- vague labels like “Insights,” “Growth,” “Scale,” “Optimize” without content

- decorative SVG illustrations pretending to be product imagery

### Signs of LLM-Generated Design

The following micro-level visual cues are reliable indicators that a design was
produced by an LLM with no design awareness.
If you see these patterns in a generated artifact, treat them as bugs — they are
not aesthetic choices, they are artifacts of a model averaging together hundreds
of conflicting training examples without understanding layout or hierarchy:

- **Thin colored borders** — pastel or accent-colored 1px borders around cards,
  sections, and containers, used where a real designer would use background fills,
  shadows, or no container at all.
  These signal that the LLM does not know how to establish hierarchy without drawing
  boxes.

- **Gradients** — gratuitous linear gradients (especially light blue to white, purple
  to pink) applied to backgrounds, buttons, or banners without a brand reason.
  Gradients are a legitimate tool only when they serve a specific identity or
  atmospheric goal; defaulting to them is a sign of avoiding a color decision.

- **Glow effects** — colored `box-shadow` or `text-shadow` with visible hue, soft
  radial glows behind elements, or backlit button effects.
  These are a LLM’s substitute for real depth and make interfaces feel cheap and
  uncalibrated.

- **Too many font sizes** — using five or more distinct `font-size` values where
  a disciplined type scale would use three or four (e.g., body, small, h3, h1).
  Every additional size weakens the hierarchy; the LLM adds sizes because it is
  guessing per-element rather than designing a system.

- **Small fonts too small** — body text at 12px or 13px, secondary text at 10px
  or 11px, or any font size below 14px for readable content.
  LLMs inherit tiny sizes from dense enterprise dashboards in their training data
  and apply them indiscriminately to marketing pages, prototypes, and editorial
  layouts where readability is paramount.

- **Inconsistent padding and alignment (especially vertical)** — elements that do
  not share a consistent vertical rhythm, card content that is not optically
  centered, buttons with uneven internal padding, or items that shift position
  across breakpoints.
  Vertical inconsistency is the single most common LLM layout bug because the
  model tokenizes text and boxes independently and never "feels" the imbalance.

These six patterns are not merely "things to avoid" — they are **diagnostic cues**.
If you inspect an artifact and see multiple of these, the entire artifact needs
structural revision, not spot fixes.

Minimal is not automatically good.
Dense is not automatically cluttered.
Choose intentionally.

## Typography

Use the existing type system if one exists.

If not, choose type deliberately based on the artifact:

- editorial: serif or humanist headline with restrained sans body

- software/productivity: precise sans with strong numeric treatment

- luxury/minimal: fewer weights, more spacing discipline

- technical: mono accents only, not mono everywhere

- deck: large, clear, high contrast

Avoid overused defaults when a stronger choice is appropriate.

If using web fonts, keep the number of families and weights low.

Use type as hierarchy before adding boxes, icons, or color.

## Color

Use brand/design-system colors first.

If no palette exists:

- define a small system

- include neutrals, surface, ink, muted text, border, accent, danger/success if needed

- use one primary accent unless the assignment calls for a broader palette

- prefer oklch for harmonious invented palettes when browser support is acceptable

- check contrast for important text and controls

Do not invent lots of colors from scratch.

## Layout and Composition

Design with rhythm:

- scale

- whitespace

- density

- alignment

- repetition

- contrast

- interruption

Avoid making every section the same card grid.

For product UIs, prioritize speed of comprehension over decoration.

For marketing surfaces, make one idea land per section.

For dashboards, avoid “data slop.”
Only show data that helps the user decide or act.

## Motion

Use motion as discipline, not theater.

Good motion:

- clarifies state changes

- reduces anxiety during loading

- shows continuity between surfaces

- gives controls tactility

- stays subtle

Bad motion:

- loops without purpose

- delays the user

- calls attention to itself

- hides poor hierarchy

Respect `prefers-reduced-motion` for non-trivial animation.

## Images and Icons

Use real supplied imagery when available.

If an asset is missing:

- use a clean placeholder

- use typography, layout, or abstract texture instead

- ask for real material when fidelity matters

Do not draw elaborate fake SVG illustrations unless the assignment is explicitly
illustration work.

Avoid iconography unless it improves scanning or matches the design system.

## Source-Code Fidelity

When recreating or extending a UI from a repo:

1. inspect the repo tree

2. identify the actual UI source files

3. read theme/token/global style/component files

4. lift exact values where appropriate

5. match spacing, radii, shadows, copy tone, density, and interaction patterns

6. only then design or modify

Do not build from memory when source files are available.

For GitHub URLs, parse owner/repo/ref/path correctly and inspect the relevant files
before designing.

## Reading Documents and Assets

Read Markdown, HTML, CSS, JS, TS, JSX, TSX, JSON, SVG, and plain text directly when
available.

For DOCX/PPTX/PDF, use available local extraction tools if present.
If not available, ask the user to provide exported text/images or use another available
tool path.

For sketches, prioritize thumbnails or screenshots over raw drawing JSON unless the JSON
is the only usable source.

## Copyright and Reference Models

Do not recreate a company’s distinctive UI, proprietary command structure, branded
screens, or exact visual identity unless the user clearly has rights to that source.

It is acceptable to extract general design principles:

- density without clutter

- command-first interaction

- monochrome with one accent

- editorial hierarchy

- clear empty states

- strong keyboard affordances

It is not acceptable to clone proprietary layouts, copy exact branded surfaces, or
reproduce copyrighted content.

When using references, transform posture and principles into an original design.

## Verification

Before final response, verify as much as the environment allows.

Minimum:

- file exists at the stated path

- HTML is saved completely

- obvious syntax issues are checked

Better:

- open in a browser tool and check console errors

- inspect screenshots at the primary viewport

- test key interactions

- test light/dark or variants if present

- test responsive breakpoints if relevant

If verification is limited by environment, say exactly what was and was not verified.

Never say “done” if the file was not actually written.

## Final Response Format

Keep final responses short.

Include:

- artifact path

- what it contains

- verification status

- next suggested action, if useful

Example:

```text
Created: /path/to/Prototype.html
It includes 3 layout variants, a Tweaks panel for density/theme, and responsive behavior.
Verified: file exists and opened cleanly in browser, no console errors.
Next: pick the strongest direction and I’ll tighten copy + motion.
```

## Pitfalls

- Do not paste hosted tool schemas into a skill.
  They cause fake tool calls.

- Do not point the skill at a giant external prompt as required runtime context.
  That creates drift.

- Do not strip the design doctrine while removing tool plumbing.

- Do not over-ask when the user already gave enough direction.

- Do not under-ask for high-fidelity work with no brand context.

- Do not produce generic SaaS layouts and call them designed.

- Do not claim browser verification unless it actually happened.
