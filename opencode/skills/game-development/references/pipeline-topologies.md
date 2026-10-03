# Pipeline Topologies

How practitioners wire authoring tools into a game. Parent:
[[game-development/SKILL|game development]].

This is a seed for searching, not a prescription. The tools named here are the ones with
the most written about them; the point is the shape of the pipelines people build, which
is stable across whichever tools a project picks.

## The interface is the format, not the tool

A pipeline is defined by two things: which artifact each tool owns, and which interchange
format carries it to the next stage. Choosing tools first produces a pipeline that has to
be rebuilt when one is replaced. Choosing the formats first means a tool can be swapped
for whatever an artist prefers.

Three rules fall out, and they are what most published pipelines have in common:

- **The authoring file is the source of truth and is versioned.** `.blend`, `.aseprite`,
  `.tmx`, `.psd`. It is never generated, and it is never edited downstream.
- **Exported artifacts are build outputs.** Sprite sheets, glTF files, baked caches,
  atlases. They are reproducible from source by running the exporter, so they can be
  regenerated, and nothing hand-edits them.
- **Export runs in a build step, not by hand.** Every tool worth using has a command-line
  interface for exactly this. A pipeline that depends on someone remembering to re-export
  is the pipeline that breaks silently.

Gregory's asset conditioning pipeline (in *Game Engine Architecture*) is the formal
version of this, and Bungie's *Asset Pipeline: Destiny 2 and Beyond* (GDC Vault) is what
it looks like built as a dependency graph at studio scale.

## Who owns what, in the pipelines people publish

| Authoring domain | Commonly used for it | Emits | Consumed by |
| --- | --- | --- | --- |
| Pixel art, sprites, frame animation | Aseprite | PNG sheet plus JSON frame data, via its CLI | 2D engines, web runtimes |
| Tile maps, 2D level layout | Tiled | `.tmx` / `.tmj`, or an exported JSON | engine tilemap loaders |
| 3D models, rigs, skeletal animation | Blender | glTF/GLB, FBX; Alembic for baked caches | engines, web runtimes |
| Multi-department scene assembly | OpenUSD tooling | USD layers | engines with USD import |
| Scene assembly, lighting, gameplay | the engine itself (Unreal, Godot, Three.js) | the build | players |

The format column is where the current engine documentation must be checked, because it
moves: Unreal's Interchange Framework handles glTF and USD alongside the legacy FBX
importer; Godot 4 treats glTF as the default and can import `.blend` directly when Blender
is installed; Three.js and other web runtimes are glTF-first. Read the engine's own import
documentation before committing to a format — this table is a starting point, not a
citation.

## What to search for

The useful write-ups are rarely titled "pipeline". Search patterns that surface them:

- `<tool> to <engine> pipeline` and `<tool> <engine> workflow` — the largest body of
  practitioner writing, mostly blog posts and devlogs.
- `<tool> command line export` or `<tool> CLI batch` — finds the people who automated it,
  which is the half worth reading.
- `<studio or game> asset pipeline GDC` — studio talks, usually the deepest material.
- `<engine> import <format>` on the engine's own documentation — the authoritative answer
  to what is supported now.
- `<tool> naming convention` and `<tool> folder structure` — how teams keep a shared
  project navigable, which is where most small-project pipelines actually fail.

Venues worth going to directly:

- **GDC Vault**, especially the Tools Tutorial Day track, and **thetoolsmiths.org**, the
  tools-engineering community's own site.
- **Engine documentation**: Unreal's Interchange Framework and Datasmith, Godot's import
  pipeline, Three.js loaders.
- **Format specifications**: Khronos for glTF 2.0, the Alliance for OpenUSD for USD.
  These say what a format can carry, which settles arguments about what to put in it.
- **Tool documentation and forums**: the Tiled manual and its discourse forum, the
  Aseprite docs and community, the Blender manual on linked libraries and overrides.
- **Devlogs**: itch.io devlogs and studio engineering blogs, where small teams describe
  the whole chain end to end, including what they abandoned.

## Reading a published pipeline

When evaluating one of these write-ups against this project, ask:

- Which artifact is authoritative, and is it the authoring file or the export?
- What runs the export, and when?
- What happens when an artist changes a source file — how far does the change travel
  without a programmer?
- Which stage owns naming and identity, so that renaming an asset does not break
  references?
- What did they abandon, and why? The devlogs that say this are worth more than the ones
  that do not.
