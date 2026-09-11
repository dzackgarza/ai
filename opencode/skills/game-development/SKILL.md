---
name: game-development
description: Use when working on a game — engine code, level content, interaction systems, animation, collision and spatial queries, art direction, or the Blender-to-engine asset pipeline. Hooks the situations where agent priors produce ad hoc game mechanisms and routes each to the field's standard reference, plus the pipeline decisions this project has already made.
---
# Game Development

> [!IMPORTANT]
> All code produced under this skill must adhere to the [[policy-index/SKILL#policy-registry|Bridge-Burning Policies]] in `policy-index/SKILL.md`. These are non-negotiable hard constraints that eliminate runtime defaults, fallbacks, mocks, optional critical dependencies, and other agent validation-evasion pathways.

Game problems here are well-trodden problems with published solutions. This file routes
each recurring situation to the standard reference and records only what is specific to
this project. Read the source before designing; do not reconstruct the pattern from
first principles. [[known-solution-first/SKILL|known-solution-first]] owns the search
procedure, and `code-patterns/references/situation-to-source.md` carries the general
design subjects these rest on.

## Object behavior, interaction, and entity structure

**Situation.** Deciding where an object's behavior lives; a player controller that knows
what each object does; a central table or `if` chain over object names; adding an
interactable requires editing the interaction system.

**Read.**

- Nystrom, *Game Programming Patterns* (free at gameprogrammingpatterns.com) —
  **Component** for entity composition, plus Event Queue, State, and Update Method.
- Unreal's Gameplay Framework documentation, and the Actor–Component model: Actors are
  containers of Components that supply the behavior, which is the engine's own answer to
  this question.
- Gregory, *Game Engine Architecture* — the runtime gameplay foundation chapters.

## Spatial queries, activation, and collision

**Situation.** Deciding whether the player can reach, target, or trigger an object;
reaching for a distance comparison between two origins, or a radius on the ground plane.

**Read.**

- Ericson, *Real-Time Collision Detection* — bounding volumes, sphere/AABB/OBB
  intersection tests, and broad-phase queries. The question "can the player interact" is
  an intersection of volumes, and this is the reference for which test to use.
- The engine's own overlap and trace documentation before hand-rolling any of it.

## Animation, assets, and the authoring boundary

**Situation.** About to hard-code an animation, a texture, or a placement in engine code;
a single source file carrying model, collision, markers, and animation; a new visual
feature that would require a code change.

**Read.**

- The Blender Manual on Actions, the NLA editor, and Linked Libraries and Library
  Overrides — the authoring side's own model of reusable, overridable animation data.
- The engine's animation-asset documentation (Animation Blueprints, state machines,
  montages in Unreal) — animations are referenced assets, never inlined curves.

**Project decisions already made.** The 3D model is the upstream source of truth: level
content is built by editing it — tiling layers, collision, empty objects for placement —
and that result is the level. The export boundary decides what the engine consumes:
geometry, collision shapes, named empties, and clips. An artist who does not code must be
able to change any of it without a programmer.

## Placeholder art and production order

**Situation.** Deciding whether to model from primitives, commission art, or borrow
existing assets; proposing polish for a scene that is still untextured blocks.

**Read.** The standard treatments of vertical slices, greyboxing, and prototyping in
game production — Gregory's production chapters, and any current studio-practice guide to
blockout-to-final workflow.

**Project decisions already made.** Borrowed sprite rips, asset packs, and 2D tile sets
are deliberate during development: they give real game feel, they reveal which art is
actually needed before anyone commissions it, and they move a technical demo to something
legible as a game. A 2D-to-3D route is acceptable for the same reason.

## Art direction

**Situation.** Given several reference works; judging whether a proposed style is close to
a target; analyzing concept art.

**Read.**

- Gurney, *Color and Light* — the working vocabulary for judging a target's light,
  palette, and atmosphere instead of naming the style.
- Mateu-Mestre, *Framed Ink* — composition and staging, which is what a concept image is
  usually communicating.
- Schell, *The Art of Game Design* — the lenses on audience and experience, for judging
  whether a reference addresses the same player at all.

**Project decisions already made.** Reference sets are supplied for their common thread —
world topology, shapes, foliage, paths, structures, navigation — not for any one work's
surface style. Styles differ in maturity and audience, not only in look. Concept art fixes
mood, not structure.
