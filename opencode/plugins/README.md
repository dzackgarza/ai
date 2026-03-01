# prompt-router plugin

Classifies every incoming user message and injects a tier-specific behavioral
instruction so the main agent operates in the correct cognitive mode before acting.

## How it works

```
user message → classify() → tier → load tiers/<tier>.md → inject as synthetic user message
```

1. Faux-rules exact-match check (zero latency, for pipeline testing).
2. LLM classifier using constitutional playbook → precedence-chain decision.
3. Tier instruction appended as the last message before the agent generates.

Killswitch: `KILLSWITCHES.promptRouter` in `killswitches.ts`. Set to `true` to disable entirely.

## Killswitches

All plugins are controlled via `killswitches.ts`. Changes take effect immediately — no session restart needed.

```typescript
// killswitches.ts
export const KILLSWITCHES = {
  promptRouter: false,  // false = active, true = killed
  ...
};
```

**Rule: every new plugin must register a killswitch in `killswitches.ts` before shipping.** Start it as `true` (killed) and enable deliberately. This prevents untested plugins from silently affecting sessions.

## File map

```
plugins/
├── prompt-router.ts          # Plugin entry point — classify + inject
├── killswitches.ts           # Centralized on/off switches (true = killed)
├── tiers/
│   ├── model-self.md         # Tier: answer from context, no tool calls
│   ├── knowledge.md          # Tier: search before answering
│   ├── C.md                  # Tier: act immediately, minimal overhead
│   ├── B.md                  # Tier: iterate uniformly across a set
│   ├── A.md                  # Tier: investigate before acting
│   ├── S.md                  # Tier: scope, gather context, hand off to plan mode
│   └── README.md             # Tier file authoring guide
└── tests/
    └── classifier/
        ├── run.ts            # Test harness
        ├── playbook.md       # Constitutional classifier system prompt
        ├── cases.yaml        # 12 labeled test cases
        ├── scores.yaml       # Per-model accuracy records
        └── README.md         # Classifier test docs
```

## Tier model

| Tier | What it means | When it fires |
|------|--------------|---------------|
| `model-self` | User is asking about the agent itself | "What tools do you have?", "What can you do?" |
| `knowledge` | Requires current external information | Version numbers, recent events, live docs |
| `C` | Focused, bounded task — act immediately | Single-file edit, one-liner, clear scope |
| `B` | Same operation across a set of targets | "Add JSDoc to every exported function" |
| `A` | Unknown root cause — investigate first | Debugging, auditing, tracing failures |
| `S` | Too large to implement without a design | New features, architecture changes |

## Running the classifier test suite

```bash
cd plugins
bun run tests/classifier/run.ts
# Specific model:
bun run tests/classifier/run.ts groq/llama-3.3-70b-versatile
# MD_JSON mode (for models that reject json_object):
bun run tests/classifier/run.ts nvidia/mistralai/mistral-large-3-675b-instruct-2512 --mode MD_JSON
```

See `tests/classifier/README.md` for full harness docs and model compatibility table.

## Environment variables

| Variable | Provider | Required for |
|----------|----------|--------------|
| `GROQ_API_KEY` | Groq | Primary classifier (llama-3.3-70b-versatile, kimi-k2) |
| `NVIDIA_API_KEY` | NVIDIA NIM | Fallback classifier (mistral-large, mistral-small, llama-3.3-70b) |
| `OPENROUTER_API_KEY` | OpenRouter | Last-resort classifier (50 req/day cap — avoid for production) |
| `OPENCODE_SESSION_ID` | — | Session correlation in JSONL log (auto-generated UUID if absent) |

## JSONL session log

Every classification (when killswitch is off) appends one line to
`/var/sandbox/.prompt-router.log`:

```jsonl
{"ts":"2026-03-01T08:00:00.000Z","session_id":"abc-123","prompt":"What is...","tier":"knowledge","reasoning":"...","injected":true}
```

Use this for behavioral testing: verify the classifier is working and confirm
which tier instruction was injected for each user message.
