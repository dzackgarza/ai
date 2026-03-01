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
