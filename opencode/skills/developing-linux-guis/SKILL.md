---
name: developing-linux-guis
description: Build GUI applications for Linux desktop environments using AGS. Use when creating desktop applications, system tray tools, bars, or native Linux UI components.
---
# Developing Linux GUIs

## Core Policy

**Use AGS (Aylur’s GTK Shell)** for all Linux GUI development.
AGS provides JavaScript/TypeScript-based development with React-like JSX syntax, GTK/CSS
styling, and built-in bindings for system integration.

## Quick Start

### Single file (no project setup)

Create a file anywhere:

```typescript
// mybar.tsx
import app from "ags/gtk4/app"
import { Astal } from "ags/gtk4"
import { createPoll } from "ags/time"

app.start({
  main() {
    const { TOP, LEFT, RIGHT } = Astal.WindowAnchor
    const clock = createPoll("", 1000, "date")

    return (
      <window visible anchor={TOP | LEFT | RIGHT}>
        <label label={clock} />
      </window>
    )
  },
})
```

Run it:

```bash
ags run ./mybar.tsx
```

### Executable with shebang

```typescript
#!/usr/bin/env -S ags run
import app from "ags/gtk4/app"

app.start({
  main() {
    // entry point
  },
})
```

Make executable:

```bash
chmod +x mybar.tsx
./mybar.tsx
```

## Project Commands

### Initialize a project (recommended for TypeScript)

```bash
ags init -d /path/to/project
```

Generates a template with TypeScript configuration.

### Generate TypeScript types

```bash
ags types -u -d /path/to/project/root
```

Generates types from GObject-based libraries.
Run after adding dependencies.

### Bundle for distribution

```bash
ags bundle
```

Bundles your project into a single executable script.

### Run during development

```bash
ags run
```

Runs without bundling for rapid iteration.

## Core Patterns

### State and reactive polling

```typescript
import { createState } from "ags"
import { createPoll } from "ags/time"

function Bar() {
  const [counter, setCounter] = createState(0)
  const date = createPoll("", 1000, `date "+%H:%M - %A %e."`)

  return (
    <window visible anchor={TOP | LEFT | RIGHT}>
      <centerbox>
        <label $type="start" label={date} />
        <button $type="end" onClicked={() => setCounter((c) => c + 1)}>
          <label label={counter((c) => `clicked ${c} times`)} />
        </button>
      </centerbox>
    </window>
  )
}
```

### System bindings (battery, media players)

```typescript
import { createBinding } from "ags"
import { Battery } from "ags/system"
import { Mpris } from "ags/media"

function BatteryLabel() {
  const percentage = createBinding(Battery.get_default(), "percentage")
  return <label label={percentage((p) => `${Math.round(p * 100)}%`)} />
}

function MediaPlayers() {
  const players = createBinding(Mpris.get_default(), "players")
  return (
    <For each={players}>
      {(player) => (
        <button
          label={createBinding(player, "title")}
          onClicked={() => player.play_pause()}
        />
      )}
    </For>
  )
}
```

### CSS/SASS styling

```scss
button {
  animation: wiggle 2s linear infinite;
}

@keyframes wiggle {
  0% { transform: rotateZ(0); }
  7% { transform: rotateZ(0); }
  15% { transform: rotateZ(-15deg); }
  20% { transform: rotateZ(10deg); }
  25% { transform: rotateZ(-10deg); }
  30% { transform: rotateZ(6deg); }
  35% { transform: rotateZ(-4deg); }
  40% { transform: rotateZ(0); }
  100% { transform: rotateZ(0); }
}
```

## Workflow

1. **Quick start**: Create single `.tsx` file with shebang, run with
   `ags run ./file.tsx`

2. **Project setup**: `ags init -d /path/to/project` for TypeScript environment

3. **Generate types**: `ags types -u -d /path/to/project/root` after adding dependencies

4. **Develop**: Run with `ags run` for hot reload

5. **Style**: Use GTK4 CSS properties for theming and animations

6. **Bundle**: `ags bundle` for production deployment

## AGS Version Contract

**Always target AGS v2 / Astal / Gnim / Gtk4.** The legacy AGS v1 API is officially
deprecated; the legacy docs redirect to v2. Never use v1 patterns unless the project
explicitly pins AGS v1.

Allowed imports:
```
astal/gtk4/app
gi://Gtk?version=4.0
gi://Astal?version=4.0
ags/file
ags/time
ags/process
```

Required app patterns:

- `app.start({ main, requestHandler })`

- Named windows with `name` before `application` (props are set sequentially)

- `application={app}` or `app.add_window(self)`

- `ags request` for external commands

- `ags toggle <WindowName>` for Waybar toggling

- `execAsync` only for CLI calls

- `monitorFile` or explicit refresh for state updates

Forbidden patterns:

- `imports.gi.Ags`, `Service.import`, `Widget.`, `App.config` (AGS v1 API)

- Synchronous `exec(` for CRUD actions — blocks IO, freezes the shell

- `systemctl`, `sqlite`, `better-sqlite`, `OnCalendar` inside AGS source

Static contract tests (add to `tests/contract/`):

```python
def test_no_ags_v1_api():
    text = "\n".join(p.read_text() for p in Path("ags").rglob("*.ts*")
                     if not any(x in p.parts for x in ("node_modules", "@girs", "__stubs__")))
    for s in ["imports.gi.Ags", "Service.import", "Widget.", "App.config"]:
        assert s not in text

def test_no_systemd_or_sqlite_in_ags():
    text = "\n".join(p.read_text() for p in Path("ags").rglob("*.ts*")
                     if not any(x in p.parts for x in ("node_modules", "@girs", "__stubs__")))
    for s in ["systemctl", "sqlite", "better-sqlite", "OnCalendar"]:
        assert s not in text

def test_no_sync_exec_in_ags():
    text = "\n".join(p.read_text() for p in Path("ags").rglob("*.ts*")
                     if not any(x in p.parts for x in ("node_modules", "@girs", "__stubs__")))
    assert " exec(" not in text
    assert "execAsync" in text
```

## Observability: Two Feedback Channels

AGS work requires **two independent feedback channels**. Neither replaces the other.

**Structural observability** — proves the AGS code uses the documented widget/app model.
Catches missing windows, wrong button labels, empty lists, duplicate rows, hidden
editors, incorrect request handler routing.

**Visual observability** — proves the rendered panel is not incoherent.
Catches invisible elements, wrong anchoring, overlapping rows, text clipped to
background color, fullscreen accidents, zero-size panels.

Typechecking alone is insufficient.
A GUI task is not complete without both channels producing evidence.

## Structural Observability: debug-tree via requestHandler

Expose structural state through `ags request`:

```
ags request debug-state
ags request debug-windows
ags request debug-tree Reminders
ags request open-test-state fixtures/three-reminders.json
ags request ping
```

The `requestHandler` mechanism in `app.start` is the documented channel for
CLI-to-running-instance messages.
Example implementation:

```tsx
app.start({
  requestHandler(argv, response) {
    if (argv[0] === "ping") return response("ok")
    if (argv[0] === "debug-tree") return response(JSON.stringify(getWidgetTree(argv[1])))
    if (argv[0] === "open-test-state") {
      loadFixture(argv[1])
      return response("loaded")
    }
  },
  main() { ... }
})
```

Example `debug-tree` response shape:
```json
{
  "window": "Reminders",
  "visible": true,
  "classes": ["reminders-window"],
  "children": [
    {
      "type": "box",
      "class": ["panel"],
      "children": [
        {"type": "label", "text": "Reminders"},
        {"type": "button", "text": "+"},
        {"type": "scrolledwindow", "children_count": 3}
      ]
    }
  ]
}
```

Structural tests to add (Tier 2):

```python
def test_ags_ping_responds():
    result = subprocess.check_output(["ags", "request", "ping"], text=True)
    assert result.strip() == "ok"

def test_debug_tree_contains_required_widgets():
    result = subprocess.check_output(["ags", "request", "debug-tree", "Reminders"], text=True)
    tree = json.loads(result)
    assert tree["window"] == "Reminders"
    assert tree["visible"] is True
    widget_types = {c["type"] for c in tree["children"][0]["children"]}
    assert "label" in widget_types
    assert "button" in widget_types
    assert "scrolledwindow" in widget_types
```

## Visual Observability: Real Wayland Screenshots

Use `grim` to capture real compositor screenshots.
Its documented usage:

```bash
grim output.png                          # capture all outputs
grim -g "10,20 300x400" region.png       # capture region by geometry
grim -g "$(slurp)" region.png            # capture interactively
```

For Hyprland, get AGS window geometry non-interactively:

```bash
grim -g "$(hyprctl clients -j | jq -r '.[] | select(.class=="ags") | "\(.at[0]),\(.at[1]) \(.size[0])x\(.size[1])"')" screenshot.png
```

**Visual harness structure** — use a repo-local harness, not ad hoc screenshots:

```
tests/visual/
  fixtures/
    empty.json
    one-reminder.json
    three-reminders.json
    long-text.json
    invalid-editor.json
  baselines/
    reminders-empty.png
    reminders-three.png
    editor-empty.png
    editor-invalid-date.png
  scripts/
    run-ags-visual.sh
    capture-window.sh
    compare-image.py
```

Run sequence (`tests/visual/scripts/run-ags-visual.sh`):

```bash
#!/usr/bin/env bash
set -euo pipefail

export XDG_STATE_HOME="$PWD/.tmp/visual-state"
mkdir -p "$XDG_STATE_HOME/rem"
cp tests/visual/fixtures/three-reminders.json "$XDG_STATE_HOME/rem/state.json"

ags run ags/app.tsx &
AGS_PID=$!
sleep 1

ags toggle Reminders
sleep 0.5

grim -g "$(hyprctl clients -j | jq -r '.[] | select(.class=="ags") | "\(.at[0]),\(.at[1]) \(.size[0])x\(.size[1])"')" \
  tests/visual/out/reminders-three.png

python tests/visual/scripts/compare-image.py \
  tests/visual/baselines/reminders-three.png \
  tests/visual/out/reminders-three.png

kill "$AGS_PID"
```

## Visual Oracle Layers

Raw pixel diffs are brittle.
Use layered oracles:

**A. Process oracle** — AGS starts, stays alive, `ags request ping` returns `ok`,
`ags toggle Reminders` succeeds.

**B. Structural oracle** — `debug-tree` contains expected widgets and labels.

**C. Geometry oracle** — screenshot exists; non-transparent bounding box has sane
dimensions; rows do not overlap; editor is inside monitor bounds.

```python
def test_panel_not_empty_or_fullscreen(img):
    bbox = non_background_bbox(img)
    assert bbox.width > 250
    assert bbox.height > 120
    assert bbox.width < 700
    assert bbox.height < 900
```

**D. Image oracle** — perceptual hash close to baseline; SSIM above threshold; OCR
optional as weak check.

**E. Triage artifact** — on failure, save `actual.png`, `expected.png`, `diff.png`,
`debug-tree.json`, AGS logs.

For visual failures requiring triage, pass the artifacts to a multimodal model with only
a narrow question:
```
Compare expected.png and actual.png.
List concrete visual differences only: missing elements, overlap/clipping,
wrong anchoring, unreadable text, wrong spacing, wrong visible state.
Do not propose code changes.
```

## Allowed Widget Vocabulary

For an initial GUI, restrict to only the AGS-documented intrinsic elements:

```
window, box, centerbox, button, entry, label, scrolledwindow
revealer  (only if animation is actually needed)
```

Allowlist enforcement test:

```python
import re
ALLOWED_INTRINSICS = {
    "window", "box", "centerbox", "button", "entry",
    "label", "scrolledwindow", "revealer",
}

def test_ags_uses_only_allowed_intrinsics_initially():
    text = "\n".join(p.read_text() for p in Path("ags").rglob("*.tsx")
                     if not any(x in p.parts for x in ("node_modules", "@girs", "__stubs__")))
    tags = set(re.findall(r"<([a-z][a-z0-9]*)\b", text))
    assert tags <= ALLOWED_INTRINSICS, f"Non-allowlist widgets: {tags - ALLOWED_INTRINSICS}"
```

Do not invent custom layout systems or widget abstractions before the basic UI passes
visual tests.

## CI Tiers

**Tier 1 — Static contract** (always runs, no compositor needed):

- `npm typecheck`, eslint/biome

- Forbidden API scan (v1 imports, systemctl, sqlite, sync exec)

- Allowed widget scan

- Pure helper unit tests

**Tier 2 — Headless structural** (start AGS, no screenshots):

- `ags run` process stays alive

- `ags request ping` returns `ok`

- `ags request debug-tree` returns expected widget tree

- Fixture-driven state tests via `open-test-state`

**Tier 3 — Real visual compositor** (required for GUI acceptance):

- Start compositor/session

- Start AGS with fixed fixture

- Capture PNG with `grim`

- Compare geometry/perceptual baseline

- Archive screenshots and logs

Do not block development on Tier 3 if CI cannot provide Wayland, but require it before
claiming the GUI is correct.

## Required justfile Recipes

Every AGS project must expose these recipes:

```make
ags-visual:
    tests/visual/scripts/run-ags-visual.sh

ags-shot CASE:
    tests/visual/scripts/capture-case.sh {{CASE}}

ags-debug-tree:
    ags request debug-tree Reminders | jq .

ags-open-fixture CASE:
    ags request open-test-state tests/visual/fixtures/{{CASE}}.json
```

## AGS GUI Acceptance Criteria

A GUI task is incomplete unless the agent provides evidence for all of the following:

```
1. AGS version target confirmed: v2/Astal/Gnim/Gtk4
2. Static contract tests pass (Tier 1)
3. app starts under `ags run`
4. `ags request ping` returns ok
5. `ags toggle <WindowName>` works
6. `debug-tree` matches expected widget tree
7. Screenshots exist for all required fixture cases
8. Visual comparisons pass, or differences explicitly listed with artifacts
9. No AGS v1 imports or invented APIs
10. Code uses patterns from official docs or local allowed-patterns doc
```

“GUI works” is not a valid claim without screenshots.
Typechecking passing is not evidence the panel renders correctly.

## Reference

- [AGS Documentation](https://aylur.github.io/ags/) - Web version (v2)

- [AGS App and CLI guide](https://aylur.github.io/ags/guide/app-cli.html) - `app.start`,
  `requestHandler`, named windows, `ags toggle`

- [AGS Utilities](https://aylur.github.io/ags/guide/utilities.html) - `execAsync`,
  `monitorFile`, `createPoll`

- [AGS Intrinsics](https://aylur.github.io/ags/guide/intrinsics.html) - Allowed built-in
  elements

- [AGS Full Documentation](https://github.com/Aylur/ags/tree/main/docs) - Complete API
  reference

- [GTK4 CSS Properties](https://docs.gtk.org/gtk4/css-properties.html) - Supported CSS
  features

- [grim](https://github.com/emersion/grim) - Wayland screenshot tool

- [Marble Shell](https://github.com/Aylur/marble-shell) - Reference implementation by
  AGS author

- [OkPanel](https://github.com/JohnOberhauser/OkPanel) - Mature AGS-based panel
  implementation
