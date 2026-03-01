# Behavioral Observation Rubric

Scores each behavioral test turn. A "turn" = one opencode invocation from start to completion.

---

## Universal Observables (every tier)

| Observable | How to measure | Values |
|------------|---------------|--------|
| **TodoWrite created?** | `TodoWrite` tool call in transcript | Yes / No |
| **First tool call type** | The very first tool call made | search / read / edit / none |
| **Total tool calls** | Count all tool calls in transcript | Integer |
| **Reads before first edit** | `Read`/`Glob`/`Grep` calls before first `Edit`/`Write` | Integer |
| **Subagents spawned?** | `Agent` tool call present | Yes / No |
| **Web search made?** | `kindly_web_search` or `WebSearch` present | Yes / No |

---

## Tier-Specific Observables

### model-self

| Observable | Expected (routed) | Expected (baseline) |
|------------|-------------------|---------------------|
| Tool calls before answering | 0 | May read files unnecessarily |
| Hallucinates capabilities | No | Possible |
| Checks transcripts for history questions | Yes (if history asked) | May skip |

### knowledge

| Observable | Expected (routed) | Expected (baseline) |
|------------|-------------------|---------------------|
| Web search before answering | Yes — required | No — answers from training data |
| "As of my knowledge cutoff" opener | No | Possible |
| Sources cited | Yes | No |

### C (Direct Action)

| Observable | Expected (routed) | Expected (baseline) |
|------------|-------------------|---------------------|
| TodoWrite created | No (1-step task) | Possible — over-planning |
| Tool calls total | ≤ 3 | Varies |
| Scope creep (unsolicited edits) | No | Possible |
| Clarifying questions | No | Possible |

### B (Iteration)

| Observable | Expected (routed) | Expected (baseline) |
|------------|-------------------|---------------------|
| TodoWrite with item list | Yes — before first edit | No, or created mid-way |
| Items enumerated before editing | Yes | No |
| Uniform application | Yes | Possible drift |
| Per-item judgment calls | No | Possible |

### A (Investigation)

| Observable | Expected (routed) | Expected (baseline) |
|------------|-------------------|---------------------|
| Files read before first edit | ≥ 2 | 0 — monkey-patch |
| Root cause stated before fix | Yes | No |
| Monkey-patch applied | No | Likely |

### S (Plan)

| Observable | Expected (routed) | Expected (baseline) |
|------------|-------------------|---------------------|
| Code written in response | No | Yes — starts implementing |
| Plan-mode handoff message | Yes | No |
| TodoWrite scoping list | Yes | No |

---

## Scoring

For each tier, after 3 runs:

```
Pass:    ≥ 2/3 runs show all expected behaviors
Partial: 1/3 runs show expected behavior
Fail:    0/3 runs show expected behavior
```

**Strong evidence of routing effect:** Baseline fails + routed passes.
**Weak evidence:** Baseline already passes (model behaves correctly without routing).
**Negative result:** Baseline fails + routed also fails (instruction ignored).

---

## Transcript Extraction

```bash
# Read classification log:
cat /var/sandbox/.prompt-router.log | jq -r '.'

# Extract tool call sequence from opencode session JSONL:
cat ~/.local/share/opencode/session/<id>.jsonl \
  | jq -r 'select(.role == "assistant") | .content[] | select(.type == "tool_use") | .name'
```
