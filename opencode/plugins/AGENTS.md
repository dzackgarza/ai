# Plugins — Required Reading

Before working in this directory, read the following in full:

## 1. OpenCode CLI Skill

- **SKILL.md** — CLI usage, interactive mode, `opencode run` limitations, async post-idle behavior
- **PLUGINS.md** — Plugin structure, all events, stop hook patterns, debugging workflow, session scoping

Located at: `~/ai/skills/opencode-cli/` (same repo, `skills/opencode-cli/`)

## 2. Serena Memories

Run `serena_read_memory` at session start. All memories apply here.

## 3. Oneshot Plugin Testing

### Baseline methodology for any plugin involving model behaviour

Before testing what a plugin *does*, you must first prove that the model is *receiving and interpreting* the plugin's output correctly. This applies to any plugin that modifies what the model sees: message transforms, context injections, system prompt modifications, tool result shaping.

Model behaviour cannot be directly observed — you cannot inspect what the model received. You need a tracer.

**The keyphrase + secret phrase methodology:**

1. Add a trigger keyphrase to the plugin
2. When triggered, the plugin injects a hidden instruction: *"You MUST include the word [PASSPHRASE] verbatim in your response"*
3. Send a controlled prompt containing the keyphrase
4. Verify the passphrase appears in stdout

If the passphrase appears: the injection was delivered, received, and interpreted. The delivery mechanism is confirmed working.

Only after this confirmation is it valid to test the plugin's actual intended behaviour. Skipping this step means any failure in the real behaviour is ambiguous — you cannot distinguish "the plugin didn't fire" from "the plugin fired but the model ignored it" from "the model misunderstood the instruction."

This is the proof-of-concept baseline for all plugin development involving model behaviour. Build it first. Test it first.

---

### Design the test like a controlled experiment

You are testing one specific behaviour: does the plugin's injected instruction reach the model and get followed? Everything else is a confound to eliminate.

A valid test requires:
- **A known baseline** — the control response (no trigger) must be fully determined in advance
- **A single variable** — the only difference between control and experimental prompts is the trigger's presence
- **An unambiguous signal** — the passphrase must be detectable with certainty, not buried in noise
- **Repeatability** — the same stimulus produces the same bounded response every run

**The correct pattern:**

| Condition | Prompt | Expected output |
|-----------|--------|-----------------|
| Control | `"Reply with only the word 'ready'."` | `ready` |
| Experimental | `"Reply with only the word 'ready'. (context: intercept test)"` | `ready` + `SWORDFISH` |

The baseline response is fully determined — one word, no variability. Any passphrase is entirely attributable to the injection. Detection is `grep -i swordfish`.

"What is 2+2?" is weaker: the model may produce multi-line output, making passphrase detection accidental rather than principled. Constrain the response format completely.

### Demand characteristics

The trigger phrase itself must not signal to the model that something unusual is happening. Words like `"intercept"`, `"test"`, `"check"`, `"inject"` prime the model to enter diagnostic or task mode — the equivalent of telling a study subject "we're testing you right now." The trigger must read as inert contextual noise.

The full response cycle is: `prompt → model infers intent → model chooses mode → plugin fires`. The model must be locked into **response mode** before the trigger ever registers.

**Patterns that induce task mode:**
- Action verbs as the main verb: `"run"`, `"do"`, `"check"`, `"test"`, `"inject"`
- Delegation language: `"for me"`, `"please"`, `"can you"`
- Trigger phrase as the grammatical subject: `"intercept test"` alone reads as a command

**The trigger must appear as incidental parenthetical context**, subordinate to a fully determined, trivial instruction the model can only comply with.

### Test sequencing

**Run one test before running any suite.** The purpose of the single test is not just "does this work" — it is specifically to verify that the model produces the expected one-word baseline response and nothing else. Only after confirming the baseline is bounded and deterministic should you run multiple conditions. Parallel tests that share a broken prompt all fail silently.

### Command rules

**Use `opencode run --agent Minimal` with a 15s timeout.** Nothing else.

- No `--attach`: not needed, and `--attach + --agent` is a documented known bug ("No context found for instance")
- No `opencode serve`: not needed for plugin tests
- No `echo | opencode`: that path exists only for async post-idle behavior (stop hooks, etc.)
- No background jobs (`&`): `wait` cannot track jobs across shell calls; failures are silent
- 15s is correct. If it times out, the model is doing task work — not MCP warmup. MCP warmup is never the bottleneck.

```bash
# Confirm baseline first:
timeout 15 opencode run --agent Minimal "Reply with only the word 'ready'."

# Then run experimental condition:
timeout 15 opencode run --agent Minimal "Reply with only the word 'ready'. (context: intercept test)"
```

### Transcript parsing

If you need to inspect output beyond stdout, use `parse_transcript.py --harness opencode <session-id>` from the reading-transcripts skill. Never use raw `jq` against `events.jsonl` or `opencode export`.

## 4. Tool Description Guidelines

When writing `tool({ description: ... })` in any plugin:

- Description = **when to use**, not what it does
- Start with `"Use when..."` — triggering conditions only
- NEVER summarize the tool's workflow or return value (model follows the description as a shortcut and skips the actual behavior)
- NEVER expose internals — file paths, directories, return shapes, implementation details. Tools abstract these away on purpose. Details are provided JIT via return values (e.g. `write_plan` returns the written path when done; the description doesn't need to mention `.serena/plans/`). Leaking internals in the description breaks abstraction, pollutes context (reducing the chance the tool is used in the right circumstances), and encourages the model to manually bypass the tool entirely.
- Use MUST/ALWAYS/NEVER for hard constraints
- Keep it short — one or two sentences

---

## 5. CoT Hooking Mechanisms (Upstream OpenCode)

**Source:** anomalyco/opencode upstream source code (DeepWiki analysis, packages/plugin/src/index.ts, packages/sdk/js/src/gen/types.gen.ts, packages/opencode/src/session/message-v2.ts)

### Plugin Hooks for Observing/Intercepting Agent Actions

**From `packages/plugin/src/index.ts` — `Hooks` interface:**

| Hook | When it fires | Can modify? |
|------|---------------|-------------|
| `event` | Any event from internal event bus | Via side effects (abort, prompt) |
| `chat.message` | New message received | No (read-only) |
| `chat.params` | Before LLM call | Yes (temperature, topP, topK, etc.) |
| `chat.headers` | Before LLM call | Yes (HTTP headers) |
| `permission.ask` | Permission requested | Yes (set status: ask/deny/allow) |
| `command.execute.before` | Before command execution | Yes |
| `tool.execute.before` | Before any tool executes | Yes (modify args, throw to block) |
| `tool.execute.after` | After any tool executes | Yes (modify output) |
| `shell.env` | Before shell execution | Yes (inject env vars) |
| `experimental.chat.messages.transform` | Before messages sent to LLM | Yes (modify message array) |
| `experimental.chat.system.transform` | Before LLM call | Yes (modify system prompt) |
| `experimental.session.compacting` | Before session compaction | Yes (modify compaction prompt) |
| `experimental.text.complete` | Text completion | Yes |
| `tool.definition` | Tool definitions sent to LLM | Yes (modify description/params) |

### Event Types (from `packages/sdk/js/src/gen/types.gen.ts`)

**Message Events:**
- `message.updated`
- `message.removed`
- `message.part.updated` — part created/updated
- `message.part.removed` — part removed
- **`message.part.delta`** — streaming incremental updates (CoT tokens)

**Session Events:**
- `session.created`, `session.updated`, `session.deleted`
- `session.diff`, `session.error`, `session.compacted`
- `session.idle`, `session.status`

**Tool Events:**
- `tool.execute.before`, `tool.execute.after`

**Other:** `command.executed`, `file.edited`, `file.watcher.updated`, `lsp.*`, `permission.*`, `shell.env`, `tui.*`, `todo.updated`, `server.*`, `pty.*`

### Reasoning Parts (from `packages/opencode/src/session/message-v2.ts`)

**`ReasoningPart`** is a defined part type in the `Part` union:
```typescript
type Part = TextPart | ReasoningPart | SubtaskPart | FilePart | ToolPart | 
            StepStartPart | StepFinishPart | SnapshotPart | PatchPart | 
            AgentPart | RetryPart | CompactionPart
```

**CoT streaming events:**
- `reasoning-start` — creates new ReasoningPart
- `reasoning-delta` — updates ReasoningPart.text field
- These trigger `message.part.delta` events with `{ partID, messageID, sessionID, field: "text", delta: "..." }`

### Mid-Stream CoT Observation Pattern

The `event` hook receives `message.part.delta` events for reasoning parts:

```typescript
export const MyPlugin: Plugin = async ({ client }) => {
  const reasoningPartSessions = new Map<string, string>();
  const cotAccumulator = new Map<string, string>();
  
  return {
    event: async ({ event }) => {
      // Track reasoning parts
      if (event.type === "message.part.updated") {
        const part = event.properties.part;
        if (part?.type === "reasoning" && part?.id && part?.sessionID) {
          reasoningPartSessions.set(part.id, part.sessionID);
        }
      }
      
      // Accumulate and check CoT deltas
      if (event.type === "message.part.delta") {
        const { partID, sessionID, field, delta } = event.properties;
        if (!reasoningPartSessions.has(partID) || field !== "text") return;
        
        const accumulated = (cotAccumulator.get(sessionID) ?? "") + delta;
        cotAccumulator.set(sessionID, accumulated);
        
        // Detect trigger in reasoning
        if (accumulated.toLowerCase().includes("trivial")) {
          // Abort mid-stream
          await client.session.abort({ path: { id: sessionID } });
          
          // Re-prompt with corrective instruction
          await client.session.prompt({
            path: { id: sessionID },
            body: {
              noReply: false,
              parts: [{ type: "text", text: "Corrective prompt here" }],
            },
          });
        }
      }
      
      // Cleanup on session end
      if (event.type === "session.deleted") {
        const sessionID = event.properties.sessionID;
        cotAccumulator.delete(sessionID);
        reasoningPartSessions.clear();
      }
    },
  };
};
```

### Capabilities Summary

| Capability | Mechanism |
|------------|-----------|
| Observe CoT in real-time | `event` hook + `message.part.delta` with ReasoningPart |
| Accumulate reasoning text | Track deltas by sessionID across events |
| Detect patterns in CoT | String matching on accumulated text |
| Abort mid-generation | `client.session.abort({ path: { id: sessionID } })` |
| Redirect agent thinking | Abort + `client.session.prompt()` with new instruction |
| Block tool execution | `tool.execute.before` + throw Error |
| Modify tool args | `tool.execute.before` + modify output.args |
| Inject hidden instructions | `experimental.chat.messages.transform` + push synthetic message |
| Persist context across compaction | `experimental.session.compacting` + output.context.push() |

### Notes

- `message.part.delta` is the authoritative streaming mechanism — emitted by `Session.updatePartDelta()` for reasoning parts
- ReasoningPart text is streamed via `reasoning-delta` events internally, propagated as `message.part.delta`
- The `event` hook is the single entry point for all event subscription in plugins
- `client.session.abort()` can be called from within an event handler to stop mid-stream generation
- Event types are generated from OpenAPI spec — `packages/sdk/js/src/gen/types.gen.ts` is authoritative
