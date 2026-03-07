# Tier instruction files

Each file contains the behavioral instruction injected when a user message
is classified into that tier.

## Files

| File | Tier | Behavioral mode |
|------|------|-----------------|
| `model-self.md` | `model-self` | Answer from context; no web search, no file reads |
| `knowledge.md` | `knowledge` | Search before answering; never answer from training data |
| `C.md` | `C` | Act immediately; TodoWrite only if 3+ distinct steps |
| `B.md` | `B` | TodoWrite the item list first; iterate uniformly |
| `A.md` | `A` | Investigate before acting; state findings before fixing |
| `S.md` | `S` | Scope with todos, gather context, hand off to plan mode |

## How they're loaded

At plugin startup, `../index.ts` loads all six files:

```typescript
const TIER_INSTRUCTIONS: Record<Tier, string> = Object.fromEntries(
  await Promise.all(
    (["model-self", "knowledge", "C", "B", "A", "S"] as const).map(async (tier) => [
      tier,
      await Bun.file(new URL(`tiers/${tier}.md`, import.meta.url)).text().then(t => t.trim()),
    ])
  )
) as Record<Tier, string>;
```

`import.meta.url` resolves relative to `../index.ts`. Files are read once at
startup and cached — no per-message disk I/O.

## How injection works

The instruction is appended as the last message before the agent generates:

```typescript
output.messages.push({
  info: { id: `router-${Date.now()}`, role: "user", model: null },
  parts: [{ type: "text", text: instruction } as TextPart],
});
```

Placing it last maximizes attention — models attend strongly to recent content.

## Editing a tier instruction

1. Edit the relevant `.md` file.
2. Restart opencode (plugin loads at startup, not per-message).
3. Send a faux-rules prompt to trigger the tier without an API call:

   | Tier | Faux prompt |
   |------|-------------|
   | `model-self` | `Describe every tool you have access to.` |
   | `A` | `Audit command-interceptor.ts for security vulnerabilities.` |
   | `S` | `Design a plugin for tracking token usage per session.` |

   See `FAUX_RULES` in `../index.ts` for the full list.

4. Check the opencode session log for the injected instruction.

## Design principles

- **`NB:` opener establishes tier context immediately** — before the model processes anything else.
- **Process constraints over declarative rules.** Required steps (TodoWrite first, state findings before acting) make skipping structurally difficult.
- **Short.** Each file is under 15 lines. Longer instructions compete with the user's actual task for attention.
- **Positive framing.** Negative rules ("Do not monkey-patch") appear only for critical failure modes.
