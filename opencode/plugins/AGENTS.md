# Plugins — Required Reading

Shared OpenCode plugin policy now lives in `~/ai/skills/opencode-plugin-development/`.
Use:

- `GUIDE.md` for development workflow and proof policy
- `AUDIT.md` for post-hoc compliance review
- `~/ai/skills/opencode-cli/SKILL.md` for basic CLI and manager command forms

Before working in this directory, read the following in full:

## 1. OpenCode CLI Skill

- **SKILL.md** — CLI usage, interactive mode, `opencode run` limitations, async post-idle behavior
- **PLUGINS.md** — Plugin structure, all events, stop hook patterns, debugging workflow, session scoping

Located at: `~/ai/skills/opencode-cli/` (same repo, `skills/opencode-cli/`)

## 2. Serena Memories

Run `serena_read_memory` at session start. All memories apply here.

## 3. Oneshot Plugin Testing

### Baseline methodology for any plugin involving model behaviour

Before testing what a plugin _does_, you must first prove that the model is _receiving and interpreting_ the plugin's output correctly. This applies to any plugin that modifies what the model sees: message transforms, context injections, system prompt modifications, tool result shaping.

Model behaviour cannot be directly observed — you cannot inspect what the model received. You need a tracer.

**The keyphrase + secret phrase methodology:**

1. Add a trigger keyphrase to the plugin
2. When triggered, the plugin injects a hidden instruction: _"You MUST include the word [PASSPHRASE] verbatim in your response"_
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

| Condition    | Prompt                                                          | Expected output       |
| ------------ | --------------------------------------------------------------- | --------------------- |
| Control      | `"Reply with only the word 'ready'."`                           | `ready`               |
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

Use `ocm` (opencode-manager) for all session orchestration. Install via `uvx` or sync the repo at `/home/dzack/opencode-plugins/clis/opencode-manager`.

- One-shot sanity checks: `timeout 15 command opencode run --agent Minimal "..."`
- Multi-turn, async, resume, callback, and post-idle tests: `ocm` commands
- No `--attach`: not needed, and `--attach + --agent` is a documented known bug
- No shared/systemd `opencode serve` for repo-local plugin tests
- Use a dedicated custom-port `opencode serve` inside the plugin's `direnv` when `ocm` needs the repo-local config/env
- No rendered CLI/TUI scraping as evidence
- No background jobs (`&`) to "keep a session alive"
- If a bounded one-shot times out, debug the model/workflow. MCP warmup is not the bottleneck

**Note:** `ocm one-shot` deletes the session after completion. Use `--transcript` to print the full transcript before deletion, or use `begin-session`/`chat`/`final` for persistent sessions.

```bash
# Confirm baseline first
timeout 15 command opencode run --agent Minimal "Reply with only the word 'ready'."

# For repo-local workflow proofs, start a dedicated server in this repo's direnv
direnv exec /path/to/plugin \
  command opencode serve --hostname 127.0.0.1 --port 4198

# One-shot with transcript output (session deleted after)
OPENCODE_BASE_URL=http://127.0.0.1:4198 uvx --from git+https://github.com/dzackgarza/opencode-manager.git ocm one-shot "Reply with only the word 'ready'." --transcript

# Create persistent session and submit opening prompt
OPENCODE_BASE_URL=http://127.0.0.1:4198 uvx --from git+https://github.com/dzackgarza/opencode-manager.git ocm begin-session "Reply with only the word 'ready'. (context: intercept test)"

# Wait for session to complete
OPENCODE_BASE_URL=http://127.0.0.1:4198 uvx --from git+https://github.com/dzackgarza/opencode-manager.git ocm wait ses_abc123 --json

# Get transcript
OPENCODE_BASE_URL=http://127.0.0.1:4198 uvx --from git+https://github.com/dzackgarza/opencode-manager.git ocm transcript ses_abc123 --json

# Final turn and delete
OPENCODE_BASE_URL=http://127.0.0.1:4198 uvx --from git+https://github.com/dzackgarza/opencode-manager.git ocm final ses_abc123 "Final prompt" --transcript
```

### Transcript parsing

If stdout is ambiguous, inspect session artifacts instead:

- `uvx --from git+https://github.com/dzackgarza/opencode-manager.git ocm transcript <session-id> --json`
- `uvx --from git+https://github.com/dzackgarza/opencode-manager.git ocm wait <session-id> --json`

Never scrape ANSI/TUI output, and never reason from raw `events.jsonl` when the session
or transcript interfaces are available.

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

| Hook                                   | When it fires                     | Can modify?                         |
| -------------------------------------- | --------------------------------- | ----------------------------------- |
| `event`                                | Any event from internal event bus | Via side effects (abort, prompt)    |
| `chat.message`                         | New message received              | No (read-only)                      |
| `chat.params`                          | Before LLM call                   | Yes (temperature, topP, topK, etc.) |
| `chat.headers`                         | Before LLM call                   | Yes (HTTP headers)                  |
| `permission.ask`                       | Permission requested              | Yes (set status: ask/deny/allow)    |
| `command.execute.before`               | Before command execution          | Yes                                 |
| `tool.execute.before`                  | Before any tool executes          | Yes (modify args, throw to block)   |
| `tool.execute.after`                   | After any tool executes           | Yes (modify output)                 |
| `shell.env`                            | Before shell execution            | Yes (inject env vars)               |
| `experimental.chat.messages.transform` | Before messages sent to LLM       | Yes (modify message array)          |
| `experimental.chat.system.transform`   | Before LLM call                   | Yes (modify system prompt)          |
| `experimental.session.compacting`      | Before session compaction         | Yes (modify compaction prompt)      |
| `experimental.text.complete`           | Text completion                   | Yes                                 |
| `tool.definition`                      | Tool definitions sent to LLM      | Yes (modify description/params)     |

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
type Part =
  | TextPart
  | ReasoningPart
  | SubtaskPart
  | FilePart
  | ToolPart
  | StepStartPart
  | StepFinishPart
  | SnapshotPart
  | PatchPart
  | AgentPart
  | RetryPart
  | CompactionPart;
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

| Capability                        | Mechanism                                                       |
| --------------------------------- | --------------------------------------------------------------- |
| Observe CoT in real-time          | `event` hook + `message.part.delta` with ReasoningPart          |
| Accumulate reasoning text         | Track deltas by sessionID across events                         |
| Detect patterns in CoT            | String matching on accumulated text                             |
| Abort mid-generation              | `client.session.abort({ path: { id: sessionID } })`             |
| Redirect agent thinking           | Abort + `client.session.prompt()` with new instruction          |
| Block tool execution              | `tool.execute.before` + throw Error                             |
| Modify tool args                  | `tool.execute.before` + modify output.args                      |
| Inject hidden instructions        | `experimental.chat.messages.transform` + push synthetic message |
| Persist context across compaction | `experimental.session.compacting` + output.context.push()       |

### Notes

- `message.part.delta` is the authoritative streaming mechanism — emitted by `Session.updatePartDelta()` for reasoning parts
- ReasoningPart text is streamed via `reasoning-delta` events internally, propagated as `message.part.delta`
- The `event` hook is the single entry point for all event subscription in plugins
- `client.session.abort()` can be called from within an event handler to stop mid-stream generation
- Event types are generated from OpenAPI spec — `packages/sdk/js/src/gen/types.gen.ts` is authoritative

---

## 6. Authoritative Sources

**Verified sources (I searched these and found information):**

| Source                                        | What it contains                                 | Verified by         |
| --------------------------------------------- | ------------------------------------------------ | ------------------- |
| `packages/plugin/src/index.ts`                | `Hooks` interface — definitive plugin hook list  | DeepWiki query      |
| `packages/sdk/js/src/gen/types.gen.ts`        | Event union types — definitive event.type values | DeepWiki query      |
| `packages/opencode/src/session/message-v2.ts` | `Part` union, `ReasoningPart` definition         | DeepWiki query      |
| `packages/web/src/content/docs/plugins.mdx`   | Plugin examples, event list                      | DeepWiki + Context7 |
| Context7 `/anomalyco/opencode`                | Plugin hook examples                             | Direct query        |
| Context7 `/websites/opencode_ai_plugins`      | Event type list                                  | Direct query        |
| Context7 `/sst/opencode-sdk-js`               | SDK streaming examples                           | Direct query        |

**Recommended search order for hook/event questions:**

1. DeepWiki query on `anomalyco/opencode` for type definitions
2. Context7 query on `/anomalyco/opencode` and `/websites/opencode_ai_plugins`
3. Check `packages/plugin/src/index.ts` Hooks interface directly
4. Check `packages/sdk/js/src/gen/types.gen.ts` for Event union types

**For capability questions (e.g., "can I abort mid-stream?"):**

1. Search for the method (`session.abort`) in source
2. Search for example usage in tests
3. Check if it's callable from event handlers

**For type definitions:**

1. Generated types: `packages/sdk/js/src/gen/types.gen.ts`
2. Internal types: `packages/opencode/src/**/*.ts`
3. Plugin types: `packages/plugin/src/index.ts`

**What NOT to rely on:**

- **Local experimental plugins** — Your own `plugins/dev/*.ts` files are untested experiments, not authoritative sources
- **Incomplete Context7 results** — May not have full coverage; cross-reference with source

**Epistemic integrity for negative findings:**

When you don't find something, report:

- Searched: [specific files, queries, tools]
- Found: [what was or was not found]
- Conclusion: [labeled as inference — "I believe", "based on searched sources"]
- Confidence: [High / Medium / Low]
- Gaps: [what remains unsearched]

**Do NOT write:**

- "X is not documented" → "I found no documentation of X in [sources]"
- "There's no hook for Y" → "I found no hook for Y in [sources]"
- "This feature doesn't exist" → "I found no evidence of this feature in [sources]"

---

## 7. llm-runner / llm-templating-engine — LLM Integration for Plugins

Plugins are TypeScript. The prompt and model stack is Python, but it now lives in two standalone repos installed into `~/ai/opencode/.venv` via `pyproject.toml`:

- `llm-templating-engine`
- `llm-runner`

Plugins never import Python directly. They shell into the JSON CLIs and exchange structured JSON over stdin/stdout.

**Rule: all LLM logic must be validated outside of plugins first.** Prove the template, schema, and rendered outputs with the standalone CLIs or `just run-microagent` before wiring any plugin hook.

### Canonical commands

Inside the local OpenCode environment:

```bash
uv run --active --python ~/ai/opencode/.venv/bin/python llm-template-inspect
uv run --active --python ~/ai/opencode/.venv/bin/python llm-template-render
uv run --active --python ~/ai/opencode/.venv/bin/python llm-invoke
uv run --active --python ~/ai/opencode/.venv/bin/python llm-run
```

Local convenience recipe:

```bash
cat <<'EOF' | just run-microagent
{
  "template": {
    "path": "/tmp/my-agent.md"
  },
  "bindings": {
    "data": {
      "prompt": "some input"
    }
  }
}
EOF
```

Materialize `/tmp/my-agent.md` first with `cd ~/ai/opencode && uv run ai-prompts get micro-agents/my-agent > /tmp/my-agent.md`.

For one-off inspection outside the local workspace, the public upstream CLIs are also available directly:

```bash
uvx --from git+https://github.com/dzackgarza/llm-templating-engine.git llm-template-render --help
uvx --from git+https://github.com/dzackgarza/llm-runner.git llm-run --help
```

### Canonical surfaces

- `llm-template-inspect` loads a template document and frontmatter
- `llm-template-render` renders a template with JSON bindings
- `llm-invoke` performs direct model calls with optional structured output
- `llm-run` resolves template frontmatter, renders prompt/system templates, invokes the model, and optionally renders a response template
- `just run-microagent` is a local passthrough to `llm-run`

The request and response contracts are JSON-first and defined in the upstream libraries. Do not recreate the old `{ ok, result }` bridge envelope in plugins.

### What plugins should consume

- Structured model output comes from `RunResponse.response.structured`
- Post-processed response-template output comes from `RunResponse.final_output`
- Template metadata comes from `llm-template-inspect`

If a plugin needs the rendered text of a template file, render the file by path with `llm-template-render`. Do not read the file into a TypeScript string first unless the prompt is genuinely inline-only.

### Separation of concerns

| Layer                   | Responsibility                                          | Where tested                      |
| ----------------------- | ------------------------------------------------------- | --------------------------------- |
| Template (`.md`)        | Prompt text, metadata, Jinja composition, schema config | `llm-template-inspect`, `llm-run` |
| `llm-templating-engine` | Template parsing, bindings, rendering                   | Python tests, CLI                 |
| `llm-runner`            | Provider calls, schema validation, response templates   | Python tests, CLI                 |
| Plugin (`.ts`)          | Hook wiring, trigger logic, when to call                | OpenCode plugin tests (§3)        |

**Never put LLM logic in a plugin that has not already been proven at the CLI layer.** A plugin is not the first place to discover that a template, schema, or provider call is wrong.

### Use templates for all nontrivial prompts

Any prompt or injection that a plugin delivers to the model must live in a `.md` template file, not as an inline string in TypeScript, unless it is a fixed literal with no variables or logic.

Templates are testable. Inline prompt logic is not.
