---
name: game-development
description: Use when working on a game — engine code, level content, interaction systems, animation, collision and spatial queries, art direction, or the Blender-to-engine asset pipeline. Routes to the production literature on how studios split disciplines and build content pipelines, so that artists and designers change content without touching engine code, plus the RPG-specific systems literature and this project's own pipeline decisions.
---
# Game Development

> [!IMPORTANT]
> All code produced under this skill must adhere to the [[policy-index/SKILL#policy-registry|Bridge-Burning Policies]] in `policy-index/SKILL.md`. These are non-negotiable hard constraints that eliminate runtime defaults, fallbacks, mocks, optional critical dependencies, and other agent validation-evasion pathways.

Game problems here are well-trodden problems with published solutions, and the hardest of
them are organizational rather than technical: who owns a change, and how many people it
has to pass through. This file routes each recurring situation to the standard reference
and records what this project has already decided. Read the source before designing.
[[known-solution-first/SKILL|known-solution-first]] owns the search procedure.

## How production is organized, and why the seams sit where they do

**Situation.** Any design that decides who can change what: a system only a programmer can
extend, content that needs an engineer in the loop, a tool nobody but its author can run,
or a proposal that ignores which discipline owns the artifact.

**Read.**

- Jason Gregory, *Game Engine Architecture* — chapter 1 covers the structure of a typical
  game team (engineers, artists, designers, producers, and the runtime/tools split), and
  the tools chapter covers the asset conditioning pipeline that connects DCC applications
  to the engine. This is the single best grounding for why engines are shaped as they are.
  Table of contents at gameenginebook.com/toc.html.
- Heather Maxwell Chandler, *The Game Production Handbook* — discipline-by-discipline
  roles across production, art, engineering, design, audio and QA, including the technical
  artist role and team organization at scale.
- Clinton Keith, *Agile Game Development with Scrum* — how cross-discipline teams are
  actually run, and why dependencies between disciplines are the thing being managed.
- Jason Schreier, *Blood, Sweat, and Pixels* and *Press Reset* — long-form reporting on
  what goes wrong in real productions. Read these for the failure modes: pipelines that
  force back-and-forth, tools arriving too late, and content churn caused by unclear
  ownership.
- The Toolsmiths (thetoolsmiths.org) and GDC's Tools Tutorial Day — the tools-engineering
  community's own material, including Bungie's *Asset Pipeline: Destiny 2 and Beyond* and
  Insomniac's data-driven property and asset-management systems.

**The principle these converge on.** Disciplines are siloed on purpose, and the pipeline
is the interface between them. An artist authors in a DCC application and never writes
engine code; a designer authors data and never writes engine code; engineers own the
runtime and the tools that consume authored data. Every time a content change requires an
engineer, the seam is in the wrong place, and the cost is paid on every subsequent change.
The technical artist exists precisely to hold that boundary — read *Technical Art Culture
of 'Uncharted 4'* (GDC Vault) for what that role does and how it is staffed.

## The asset pipeline

**Situation.** Deciding what the engine consumes; a single source file carrying model,
collision, markers and animation; an import step that needs hand-holding; a new asset type
that requires code.

**Read.**

- Gregory, *Game Engine Architecture*, on the asset conditioning pipeline: raw DCC output
  is processed into engine-consumable formats by a build step, not loaded directly.
- *Tools Tutorial Day: Bungie's Asset Pipeline: 'Destiny 2' and Beyond* (GDC Vault) — a
  dependency-graph pipeline serving local iteration for content creators across multiple
  studios as well as shipping builds.
- *The Witcher 3: Optimizing Content Pipelines for Open-World Games* (GDC 2015, Martin
  Thorzen) — content pipeline work on an open-world RPG specifically.
- The Blender Manual on Linked Libraries and Library Overrides, for the authoring side's
  own model of shared, overridable data.
- [references/pipeline-topologies.md](references/pipeline-topologies.md) — who owns what
  across authoring tools (Aseprite, Tiled, Blender, the engine), the interchange formats
  that are the real interface, and search patterns for finding how other teams wired
  theirs.

**Project decisions already made.** The 3D model is the upstream source of truth: level
content is built by editing it — tiling layers, collision, empty objects for placement —
and that result is the level. The export boundary decides what the engine consumes:
geometry, collision shapes, named empties, and clips.

## Data-driven content, so designers do not need programmers

**Situation.** Adding an enemy, item, encounter, ability, or tuning value; a system whose
new cases are `if` branches in engine code; numbers compiled into the build.

**Read.**

- Ryan Hipple, *Game Architecture with Scriptable Objects* (Unite Austin 2017) — the
  canonical treatment of designer-authored data assets, runtime sets, and event channels,
  with the sample project at github.com/roboryantron/Unite2017.
- Unreal's own data-driven surfaces: Data Assets, DataTables and Curve Tables, and the
  Gameplay Ability System — the engine's answer to authoring behavior as data.
- Insomniac's data-driven property systems via the Toolsmiths archive — reflection-based
  property editing and asset identity.

**The test.** Adding content is adding data. If a designer cannot add the next item,
enemy, or ability without a programmer, the system is not finished.

## RPG systems: quests, dialogue, and balance

**Situation.** Designing quest state, dialogue flow, branching, or character statistics;
about to hard-code a quest or write dialogue logic into engine code.

**Read.**

- *Behind the Scenes of Cinematic Dialogues in 'The Witcher 3: Wild Hunt'* (GDC 2016,
  Piotr Tomsinski) — the production pipeline and editor behind roughly 35 hours of
  dialogue with a modest animation team; the stages are writing, quest design, and
  automated scene assembly, which is the model to copy.
- *10 Key Quest Design Lessons from 'The Witcher 3' and 'Cyberpunk 2077'* (GDC Vault) —
  quest structure from the studio that ships the most of it.
- Ian Schreiber & Brenda Romero, *Game Balance* — the mathematics of stats, curves,
  economies and progression, which is what RPG tuning data actually encodes.
- Scott Rogers, *Level Up! The Guide to Great Video Game Design* — practical design
  coverage across systems and levels.

## Object behavior, interaction, and entity structure

**Situation.** Deciding where an object's behavior lives; a player controller that knows
what each object does; a central table or `if` chain over object names.

**Read.**

- Robert Nystrom, *Game Programming Patterns* (free at gameprogrammingpatterns.com) —
  **Component** for entity composition, plus Event Queue, State, and Update Method.
- Unreal's Gameplay Framework and the Actor–Component model: Actors are containers of
  Components that supply behavior. This is the engine's own answer.
- Gregory, *Game Engine Architecture*, runtime gameplay foundation chapters.

## Spatial queries, activation, and collision

**Situation.** Deciding whether the player can reach, target, or trigger an object;
reaching for a distance comparison between two origins, or a radius on the ground plane.

**Read.**

- Christer Ericson, *Real-Time Collision Detection* — bounding volumes and intersection
  tests. Interaction range is an intersection of volumes; this is the reference for which
  test to use.
- The engine's overlap and trace documentation, before hand-rolling any of it.

## Animation

**Situation.** About to hard-code an animation, curve, or timing in engine code.

**Read.**

- Jonathan Cooper, *Game Anim: Video Game Animation Explained* — written by an animation
  lead on Assassin's Creed and Mass Effect; covers the animator's side of the pipeline and
  what the engine must expose for animators to work without engineers.
- The Blender Manual on Actions and the NLA editor; the engine's animation-asset
  documentation (Animation Blueprints, state machines, montages).

**Project decision already made.** Animations are referenced assets. An artist who does
not code must be able to replace any of them without a programmer.

## Placeholder art and production order

**Situation.** Deciding whether to model from primitives, commission art, or borrow
existing assets; proposing polish for a scene that is still untextured blocks.

**Read.** Gregory's production material and Chandler's *Game Production Handbook* on
prototyping, vertical slices, and greybox-to-final order.

**Project decisions already made.** Borrowed sprite rips, asset packs, and 2D tile sets
are deliberate during development: they give real game feel, they reveal which art is
actually needed before anyone commissions it, and they move a technical demo to something
legible as a game. A 2D-to-3D route is acceptable for the same reason.

## Art direction

**Situation.** Given several reference works; judging whether a proposed style is close to
a target; analyzing concept art.

**Read.**

- James Gurney, *Color and Light* — the working vocabulary for a target's light, palette
  and atmosphere.
- Marcos Mateu-Mestre, *Framed Ink* — composition and staging, which is usually what a
  concept image communicates.
- Jesse Schell, *The Art of Game Design* — the lenses on audience and experience, for
  judging whether a reference addresses the same player.

**Project decisions already made.** Reference sets are supplied for their common thread —
world topology, shapes, foliage, paths, structures, navigation — not for any one work's
surface style. Styles differ in maturity and audience, not only in look. Concept art fixes
mood, not structure.
