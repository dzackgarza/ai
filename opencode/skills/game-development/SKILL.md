---
name: game-development
description: Use when working on a game — engine code, level content, interaction systems, animation, art direction, or the Blender-to-engine asset pipeline. Teaches the general design principles as they land in game work — ownership of behavior, modelling the real phenomenon, concern seams at the author boundary, purpose before polish, audience — with the standard patterns a practitioner expects as the worked instances.
---
# Game Development

> [!IMPORTANT]
> All code produced under this skill must adhere to the [[policy-index/SKILL#policy-registry|Bridge-Burning Policies]] in `policy-index/SKILL.md`. These are non-negotiable hard constraints that eliminate runtime defaults, fallbacks, mocks, optional critical dependencies, and other agent validation-evasion pathways.

Game work here goes wrong at the level of general design principles, not game trivia.
Each section below names the principle first and shows how it lands in this domain;
`code-patterns/references/first-principles.md` states the principles themselves and
their instances in other domains. Read
[[known-solution-first/SKILL|known-solution-first]] before designing any system in this
skill's scope — game problems are well-trodden problems, and inventing where a standard
pattern exists costs the invention plus the time to have the standard explained back to
you.

## Ownership: Behavior Belongs to the Object That Has It

*Principle: behavior belongs with what it governs; adding an instance must not require
editing a central file.* In this domain that is the interactable pattern, which any
practitioner expects to find:

- The object owns its own interaction data and responses. A chest knows how it opens; a
  portal knows where it leads. The player controller does not hold a table of what
  everything does.
- The object has an **activation volume** — a region, not a point — and the engine
  reports entry and exit.
- The object supplies its own affordance: the floating prompt, the highlight, the
  "press X to open" text, driven by the same data.
- Adding a new interactable is adding content, not editing the interaction system.

Centralized `if` chains over object names, per-object special cases in the player
controller, and interaction logic that must be edited to add a chest are all the
non-pattern.

## Model the Phenomenon, Not a Cheap Stand-In

*Principle: a proxy that is easier to compute is a different claim, and it diverges
exactly where the real thing is interesting.* Whether the player can interact with an
object is an intersection of geometries: a
sphere (or box) around the player against the spherical hull — or bounding volume — of
the object. It is not a distance check between two origins, and it is not a
two-dimensional radius on the ground plane.

A distance check is the approximation that feels equivalent and is not: it ignores
height, ignores object extent, and fails first on exactly the large and tall objects
players most expect to reach. When a geometric condition is described precisely,
implement that geometry. Simulating it with a cheaper proxy is a refusal to implement
the specification.

## Separate Concerns Where the Author Changes

*Principle: a concern seam belongs where a different person, tool, or lifecycle takes
over, and the design must serve whoever changes it next.* Assume an artist arrives
tomorrow and changes everything visual. Every design must survive that.

- **Animations live in the authoring tool** (Blender), exported as reusable clips or
  actions. The engine references them by name or asset; it does not hard-code one
  particular animation's keyframes, curves, or timing.
- **Adding a new visual feature must not require a code change.** If a rain effect, a
  new tiling layer, or a new prop type forces a programmer to teach the pipeline about
  it, the pipeline is the defect. Artists and level designers who do not code must be
  able to add content.
- **Separate the concerns the source file muddles.** A single Blender file that carries
  the model, the tiling, the collision, the placement markers, and the animations is a
  working method, not an architecture. The export boundary decides what the engine
  consumes: geometry, collision shapes, named empties for placement, and clips.
- The 3D model is the upstream source of truth. Level content is built by editing it —
  adding tiling layers, collision, and empty objects for placement — and then using the
  result as the level.

## Purpose Before Polish: Placeholder Art Is a Method

*Principle: derive the work from the artifact's purpose at its current stage; effort
aimed at a later stage is wasted.* Using existing sprite rips, asset packs, or borrowed
tiles during development is deliberate:

- It gives the project real game feel early, which keeps momentum.
- It reveals what art is actually needed. Commissioning art up front costs a great deal
  of time and produces assets that go unused, because nobody yet knew what the game
  required.
- It converts a technical demo into something legible as a game quickly, which is what
  makes design questions answerable at all.

A 2D-to-3D route is reasonable for the same reason: extensive tile sets exist for 2D
games, and a 2D tile can be extrapolated into usable 3D textures. Prefer grabbing an
asset pack over modelling everything from primitives when the goal is to see the game.

## Audience: Art Direction Is Maturity and Reader, Not Palette

*Principle: material supplied together is supplied for what it shares; read the set, not
each item.* When several reference works are supplied, the point is their **common
thread** —
world topology, shapes, foliage, paths, structures, how the player navigates the space
— not any one work's surface style. Reading the set as a list of unrelated styles
misses what was being communicated.

Two further distinctions that are easy to flatten:

- **Aesthetic distance is real.** Styles differ in maturity, not only in look, and a
  reference whose maturity is far from the target is not a near match. A minimal casual
  game and a heavy atmospheric one do not address the same audience.
- **Concept art is about mood and direction**, not structural accuracy. Analyzing the
  layout of a concept image is the wrong focus; the image is there to fix tone.

Before proposing art direction, check where the project actually is. Advice aimed at
polish and effects is wasted on a scene that is still untextured blocks; what that
scene needs is anything that makes it resemble a game.
