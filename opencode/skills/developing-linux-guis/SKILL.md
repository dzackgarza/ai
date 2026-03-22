---
name: developing-linux-guis
description: Build GUI applications for Linux desktop environments using AGS. Use when creating desktop applications, system tray tools, bars, or native Linux UI components.
---

# Developing Linux GUIs

## Core Policy

**Use AGS (Aylur's GTK Shell)** for all Linux GUI development. AGS provides JavaScript/TypeScript-based development with React-like JSX syntax, GTK/CSS styling, and built-in bindings for system integration.

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

Generates types from GObject-based libraries. Run after adding dependencies.

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

1. **Quick start**: Create single `.tsx` file with shebang, run with `ags run ./file.tsx`
2. **Project setup**: `ags init -d /path/to/project` for TypeScript environment
3. **Generate types**: `ags types -u -d /path/to/project/root` after adding dependencies
4. **Develop**: Run with `ags run` for hot reload
5. **Style**: Use GTK4 CSS properties for theming and animations
6. **Bundle**: `ags bundle` for production deployment

## Reference

- [AGS Full Documentation](https://github.com/Aylur/ags/tree/main/docs) - Complete API reference and guides
- [AGS Documentation](https://aylur.github.io/ags/) - Web version
- [GTK4 CSS Properties](https://docs.gtk.org/gtk4/css-properties.html) - Supported CSS features
- [Marble Shell](https://github.com/Aylur/marble-shell) - Reference implementation by AGS author
- [OkPanel](https://github.com/JohnOberhauser/OkPanel) - Mature AGS-based panel implementation
